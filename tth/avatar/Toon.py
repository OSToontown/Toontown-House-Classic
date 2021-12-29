from direct.actor import Actor
from direct.directnotify import DirectNotifyGlobal
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from direct.task.Task import Task
from pandac.PandaModules import *
import random
import types

import AccessoryGlobals
import Motion
import ShadowCaster
import ToonDNA
import ToonGlobals
from ToonHead import *
from tth.areas import ZoneUtil
from tth.base import TTHouseGlobals
from tth.distributed import DelayDelete
from tth.effects import Wake

# Compile the animation lists into three dictionaries:
# ToonGlobals.LegsAnimDict, ToonGlobals.TorsoAnimDict, and
# ToonGlobals.HeadAnimDict. This is lazy instantiation, and Python will only
# make this happen the first time Toon is imported.
ToonGlobals.compileAnimLists()

class Toon(ToonHead, Actor.Actor, ShadowCaster.ShadowCaster):

    notify = DirectNotifyGlobal.directNotify.newCategory('Toon')

    # ActiveToons is a container of Toon objects that are currently being
    # managed by the margin manager.
    ActiveToons = []

    # afk-timeout is a Config.prc variable which specifies the time in seconds
    # before the Toon is kicked from the game.
    afkTimeout = base.config.GetInt('afk-timeout', 600)

    def __init__(self):
        self.name = None
        if hasattr(self, 'Toon_initialized'):
            return None
        self.Toon_initialized = True
        Actor.Actor.__init__(self, None, None, None, flattenable=0, setFinal=1)
        ShadowCaster.ShadowCaster.__init__(self)
        ToonHead.__init__(self)
        self.avatarType = 'toon'

        self.__font = TTHouseGlobals.getInterfaceFont()

        self.soundChatBubble = base.loadSfx(
            'phase_3/audio/sfx/GUI_balloon_popup.mp3')
        self.soundTeleport = None

        # TODO: Add support for future-style nametags.
        self.setFont(ToonGlobals.getToonFont())

        self.getGeomNode().showThrough(TTHouseGlobals.ShadowCameraBitmask)
        self.collTube = None
        self.scale = 1.0
        self.height = 0.0

        self.style = None
        self.hatNodes = []
        self.glassesNodes = []
        self.backpackNodes = []

        self.ghostMode = 0

        # TODO: Add chat support for future-style nametags.
        self.__chatDialogueList = []
        self.__currentDialogue = None

        self.forwardSpeed = 0.0
        self.rotateSpeed = 0.0
        self.motion = Motion.Motion(self)
        self.standWalkRunReverse = None
        self.playingAnim = None
        self.forceJumpIdle = False

        self.effectTrack = None
        self.emoteTrack = None
        self.emote = None

        self.__bookActors = []
        self.__holeActors = []
        self.holeClipPath = None

        # wake is used to create a ripple effect when running through water.
        self.wake = None
        self.lastWakeTime = 0

        self.isDisguised = 0
        self.defaultColorScale = None
        self.jar = None

        self.animFSM = ClassicFSM('Toon', [
            State('off', self.enterOff, self.exitOff),
            State('neutral', self.enterNeutral, self.exitNeutral),
            State('victory', self.enterVictory, self.exitVictory),
            State('Happy', self.enterHappy, self.exitHappy),
            State('Sad', self.enterSad, self.exitSad),
            State('Catching', self.enterCatching, self.exitCatching),
            State('CatchEating', self.enterCatchEating, self.exitCatchEating),
            State('Sleep', self.enterSleep, self.exitSleep),
            State('walk', self.enterWalk, self.exitWalk),
            State('jumpSquat', self.enterJumpSquat, self.exitJumpSquat),
            State('jump', self.enterJump, self.exitJump),
            State('jumpAirborne', self.enterJumpAirborne,
                                  self.exitJumpAirborne),
            State('jumpLand', self.enterJumpLand, self.exitJumpLand),
            State('run', self.enterRun, self.exitRun),
            State('swim', self.enterSwim, self.exitSwim),
            State('swimhold', self.enterSwimHold, self.exitSwimHold),
            State('dive', self.enterDive, self.exitDive),
            State('cringe', self.enterCringe, self.exitCringe),
            State('OpenBook', self.enterOpenBook, self.exitOpenBook,
                  ['ReadBook', 'CloseBook']),
            State('ReadBook', self.enterReadBook, self.exitReadBook),
            State('CloseBook', self.enterCloseBook, self.exitCloseBook),
            State('TeleportOut', self.enterTeleportOut, self.exitTeleportOut),
            State('Died', self.enterDied, self.exitDied),
            State('TeleportedOut', self.enterTeleportedOut,
                                   self.exitTeleportedOut),
            State('TeleportIn', self.enterTeleportIn, self.exitTeleportIn),
            State('Emote', self.enterEmote, self.exitEmote),
            State('SitStart', self.enterSitStart, self.exitSitStart),
            State('Sit', self.enterSit, self.exitSit),
            State('Push', self.enterPush, self.exitPush),
            State('Squish', self.enterSquish, self.exitSquish),
            State('FallDown', self.enterFallDown, self.exitFallDown),
            State('GolfPuttLoop', self.enterGolfPuttLoop,
                                  self.exitGolfPuttLoop),
            State('GolfRotateLeft', self.enterGolfRotateLeft,
                                    self.exitGolfRotateLeft),
            State('GolfRotateRight', self.enterGolfRotateRight,
                                     self.exitGolfRotateRight),
            State('GolfPuttSwing', self.enterGolfPuttSwing,
                                   self.exitGolfPuttSwing),
            State('GolfGoodPutt', self.enterGolfGoodPutt,
                                  self.exitGolfGoodPutt),
            State('GolfBadPutt', self.enterGolfBadPutt, self.exitGolfBadPutt),
            State('Flattened', self.enterFlattened, self.exitFlattened),
            State('CogThiefRunning', self.enterCogThiefRunning,
                                     self.exitCogThiefRunning),
            State('ScientistJealous', self.enterScientistJealous,
                                      self.exitScientistJealous),
            State('ScientistEmcee', self.enterScientistEmcee,
                                    self.exitScientistEmcee),
            State('ScientistWork', self.enterScientistWork,
                                   self.exitScientistWork),
            State('ScientistLessWork', self.enterScientistLessWork,
                                       self.exitScientistLessWork),
            State('ScientistPlay', self.enterScientistPlay,
                                   self.enterScientistPlay)
        ], 'off', 'off')
        self.animFSM.enterInitialState()


    def stopAnimations(self):
        if hasattr(self, 'animFSM'):
            if not self.animFSM.isInternalStateInFlux():
                self.animFSM.request('off')
            else:
                self.notify.warning(
                    'animFSM in flux, state=%s, not requesting off' % (
                        self.animFSM.getCurrentState().getName())
                )
        else:
            self.notify.warning('animFSM has been deleted')

        if self.effectTrack != None:
            self.effectTrack.finish()
            self.effectTrack = None
        if self.emoteTrack != None:
            self.emoteTrack.finish()
            self.emoteTrack = None
        if self.wake:
            self.wake.stop()
            self.wake.destroy()
            self.wake = None

    def delete(self):
        if hasattr(self, 'Toon_deleted'):
            return None
        self.Toon_deleted = True

        self.stopAnimations()

        self.rightHands = None
        self.rightHand = None
        self.leftHands = None
        self.leftHand = None
        self.headParts = None
        self.torsoParts = None
        self.hipsParts = None
        self.legsParts = None
        del self.animFSM

        for bookActor in self.__bookActors:
            bookActor.cleanup()
        del self.__bookActors

        for holeActor in self.__holeActors:
            holeActor.cleanup()
        del self.__holeActors

        self.soundTeleport = None
        self.motion.delete()
        self.motion = None

        Actor.Actor.cleanup(self)

        del self.__font
        del self.style
        del self.soundChatBubble

        # TODO: Add support for removing future-style nametags.

        ShadowCaster.ShadowCaster.delete(self)
        Actor.Actor.delete(self)
        ToonHead.delete(self)

    def isLocal(self):
        """
        Inheritors should override. This is used to determine whether this is a
        local copy of the Toon or not.
        """
        return False

    def updateToonDNA(self, newDNA, fForce=0):
        """
        Updates the Toon's DNA based on the changes made in newDNA.
        If fForce is True, however, an update to the entire Toon DNA is forced.
        """
        self.style.gender = newDNA.getGender()
        oldDNA = self.style
        if fForce or (newDNA.head is not oldDNA.head):
            self.swapToonHead(newDNA.head)
        if fForce or (newDNA.torso is not oldDNA.torso):
            self.swapToonTorso(newDNA.torso, genClothes=0)
            self.loop('neutral')
        if fForce or (newDNA.legs is not oldDNA.legs):
            self.swapToonLegs(newDNA.legs)
        self.swapToonColor(newDNA)
        self.__swapToonClothes(newDNA)
        hat, glasses, backpack, shoes = newDNA.getAccessories()
        self.setHat(*hat)
        self.setGlasses(*glasses)
        self.setBackpack(*backpack)
        self.setShoes(*shoes)

    def setDNAString(self, dnaString):
        """
        Sets or updates the Toon's DNA using a net string blob. These can be
        gotten from a ToonDNA object by calling its makeNetString() method.
        """
        newDNA = ToonDNA.ToonDNA(dnaString)
        if len(newDNA.torso) < 2:
            # TODO: Naked Toons are not currently supported.
            newDNA.torso = newDNA.torso + 's'
        self.setDNA(newDNA)

    def setDNA(self, dna):
        """
        Sets or updates the Toon's DNA using a ToonDNA object. The Toon's DNA
        will not be set if its 'isDisguised' attribute is True.
        """
        if hasattr(self, 'isDisguised') and self.isDisguised:
            return None
        if self.style:
            self.updateToonDNA(dna)
        else:
            self.style = dna
            self.generateToon()
            self.initializeDropShadow()
            # TODO: Add support for future-style nametags.

    def getAvatarScale(self):
        return self.scale

    def setAvatarScale(self, scale):
        if self.scale != scale:
            self.scale = scale
            self.getGeomNode().setScale(scale)
            self.setHeight(self.height)

    def getHeight(self):
        return self.height

    def setHeight(self, height):
        """
        Adjusts the nametag, and collision tubes based on the provided height.
        """
        self.height = height
        # TODO: Add support for future-style nametags.
        if self.collTube:
            self.collTube.setPointB(0, 0, height - self.getRadius())
            if self.collNodePath:
                self.collNodePath.forceRecomputeBounds()
        # TODO: Add support for battle collisions.

    def getRadius(self):
        return ToonGlobals.ToonAvatarRadius

    def getName(self):
        return self.name

    def setName(self, name, doTag=True, doShadow=True):
        """
        Sets the 'name' attribute to the provided name, and updates the Toon's
        nametag. Does nothing if the 'isDisguised' attribute is True.
        """
        if hasattr(self, 'isDisguised') and self.isDisguised:
                return None
        self.name = name
        # TODO: Remove dependencies on doTag and doShadow.
        if doTag:
            self.placeTag(name)
        # TODO: Add support for future-style nametags.

    def setDisplayName(self, name):
        """
        Updates only the Toon's nametag with the provided name. Does nothing if
        the 'isDisguised' attribute is True.
        """
        if hasattr(self, 'isDisguised') and self.isDisguised:
                return None
        # TODO: Add support for future-style nametags.

    def getType(self):
        return self.avatarType

    def getFont(self):
        return self.__font

    def setFont(self, font):
        self.__font = font
        # TODO: Add support for future-style nametags.

    def getStyle(self):
        return self.style

    def setStyle(self, style):
        self.style = style

    def getDialogueArray(self):
        """
        Returns the collect dialogue array based on the Toon's species.
        """
        animalType = self.style.getAnimal()
        try:
            return eval(animalType.capitalize() + 'DialogueArray')
        except NameError:
            return None

    def playCurrentDialogue(self, dialogue, chatFlags, interrupt=1):
        """
        Plays the dialogue sound effect that is provided. If none is provided,
        and chatFlags contains the CFSpeech flag, the dialogue sound effect for
        the current display chat will be played, alongside the chat bubble
        sound effect.
        If interrupt is True, the currently playing dialogue sound effect will
        stop before the new one plays.
        """
        if interrupt and (self.__currentDialogue is not None):
            self.__currentDialogue.stop()
        self.__currentDialogue = dialogue
        if dialogue:
            base.playSfx(dialogue, node=self)
        # TODO: Add a second condition for playing chat based on the current
        #       display chat.

    def playDialogueForString(self, chatString):
        """
        Calls playDialogue() with the correct arguments based on the string
        provided.
        """
        searchString = chatString.lower()
        if searchString.find(L10N.DialogSpecial) >= 0:
            dialType = 'special'
        elif searchString.find(L10N.DialogExclamation) >= 0:
            dialType = 'exclamation'
        elif searchString.find(L10N.DialogQuestion) >= 0:
            dialType = 'question'
        elif random.randint(0, 1):
            dialType = 'statementA'
        else:
            dialType = 'statementB'
        stringLength = len(chatString)
        if stringLength <= TTHouseGlobals.DialogLength1:
            length = 1
        elif stringLength <= TTHouseGlobals.DialogLength2:
            length = 2
        elif stringLength <= TTHouseGlobals.DialogLength3:
            length = 3
        else:
            length = 4
        self.playDialogue(dialType, length)

    def getDialogueSfx(self, dialType, length):
        """
        Returns the correct dialogue sound effect based on the dialogue type,
        and length provided.
        """
        dialogueArray = self.getDialogueArray()
        if not dialogueArray:
            return None
        if dialType in ('statementA', 'statementB'):
            sfxIndex = min(length-1, 2)
        elif dialType is 'question':
            sfxIndex = 3
        elif dialType is 'exclamation':
            sfxIndex = 4
        elif dialType is 'special':
            sfxIndex = 5
        else:
            notify.error('Unrecognized dialogue type: ', type)
        if sfxIndex < len(dialogueArray):
            return dialogueArray[sfxIndex]

    def playDialogue(self, dialType, length):
        """
        Plays the correct dialogue sound effect based on the dialogue type,
        and length provided.
        """
        sfx = self.getDialogueSfx(dialType, length)
        if sfx:
            base.playSfx(sfx, node=self)

    def isInView(self):
        """
        Returns whether or not this Toon is visible by the client's camera.
        """
        pos = self.getPos(camera)
        eyePos = Point3(pos[0], pos[1], pos[2] + self.getHeight())
        return base.camNode.isInView(eyePos)

    def getAirborneHeight(self):
        height = self.getPos(self.shadowPlacer.shadowNodePath)
        return height.getZ() + 0.025

    def initializeBodyCollisions(self, collIdStr):
        self.collTube = CollisionTube(
            0, 0, 0.5, 0, 0, self.height - self.getRadius(), self.getRadius())
        self.collNode = CollisionNode(collIdStr)
        self.collNode.addSolid(self.collTube)
        self.collNodePath = self.attachNewNode(self.collNode)
        if self.ghostMode:
            self.collNode.setCollideMask(TTHouseGlobals.GhostBitmask)
        else:
            self.collNode.setCollideMask(
                TTHouseGlobals.WallBitmask|TTHouseGlobals.PieBitmask)

    def stashBodyCollisions(self):
        if hasattr(self, 'collNodePath'):
            self.collNodePath.stash()

    def unstashBodyCollisions(self):
        if hasattr(self, 'collNodePath'):
            self.collNodePath.unstash()

    def disableBodyCollisions(self):
        """
        Completely removes the Toon's body collisions.
        """
        if hasattr(self, 'collNodePath'):
            self.collNodePath.removeNode()
            del self.collNodePath
        self.collTube = None

    def addActive(self):
        """
        Adds this Toon to the margin manager.
        """
        try:
            Toon.ActiveToons.remove(self)
        except ValueError:
            pass
        Toon.ActiveToons.append(self)
        # TODO: Add support for future-style nametags.

    def removeActive(self):
        """
        Removes this Toon from the margin manager.
        """
        try:
            Toon.ActiveToons.remove(self)
        except ValueError:
            pass
        # TODO: Add support for future-style nametags.

    def loop(self, animName, restart=1, partName=None, fromFrame=None,
             toFrame=None):
        return Actor.Actor.loop(self, animName, restart, partName, fromFrame,
                                toFrame)

    def parentToonParts(self):
        if self.hasLOD():
            for lodName in self.getLODNames():
                torso = self.getPart('torso', lodName)
                if not torso.find('**/def_head').isEmpty():
                    self.attach('head', 'torso', 'def_head', lodName)
                else:
                    self.attach('head', 'torso', 'joint_head', lodName)
                self.attach('torso', 'legs', 'joint_hips', lodName)
        else:
            self.attach('head', 'torso', 'joint_head')
            self.attach('torso', 'legs', 'joint_hips')

    def unparentToonParts(self):
        if self.hasLOD():
            for lodName in self.getLODNames():
                self.getPart('head', lodName).reparentTo(self.getLOD(lodName))
                self.getPart('torso', lodName).reparentTo(self.getLOD(lodName))
                self.getPart('legs', lodName).reparentTo(self.getLOD(lodName))
        else:
            self.getPart('head').reparentTo(self.getGeomNode())
            self.getPart('torso').reparentTo(self.getGeomNode())
            self.getPart('legs').reparentTo(self.getGeomNode())

    def setLODs(self):
        self.setLODNode()
        levelOneIn = base.config.GetInt('lod1-in', 20)
        levelOneOut = base.config.GetInt('lod1-out', 0)
        levelTwoIn = base.config.GetInt('lod2-in', 80)
        levelTwoOut = base.config.GetInt('lod2-out', 20)
        levelThreeIn = base.config.GetInt('lod3-in', 280)
        levelThreeOut = base.config.GetInt('lod3-out', 80)
        self.addLOD(1000, levelOneIn, levelOneOut)
        self.addLOD(500, levelTwoIn, levelTwoOut)
        self.addLOD(250, levelThreeIn, levelThreeOut)

    def generateToon(self):
        self.setLODs()
        self.generateToonLegs()
        self.generateToonHead()
        self.generateToonTorso()
        self.generateToonColor()
        self.parentToonParts()
        self.rescaleToon()
        self.resetHeight()
        self.setupToonNodes()
        self.generateToonAccessories()

    def setupToonNodes(self):
        """
        Sets up convenience variables for commonly used Toon parts.
        """
        rightHand = NodePath('rightHand')
        self.rightHand = None
        self.rightHands = []
        leftHand = NodePath('leftHand')
        self.leftHands = []
        self.leftHand = None

        for lodName in self.getLODNames():
            torso = self.getPart('torso', lodName)

            hand = torso.find('**/joint_Rhold')
            if not torso.find('**/def_joint_right_hold').isEmpty():
                hand = torso.find('**/def_joint_right_hold')
            self.rightHands.append(hand)
            rightHand = rightHand.instanceTo(hand)
            if not torso.find('**/def_joint_left_hold').isEmpty():
                hand = torso.find('**/def_joint_left_hold')
            self.leftHands.append(hand)
            leftHand = leftHand.instanceTo(hand)
            if self.rightHand is None:
                self.rightHand = rightHand
            if self.leftHand is None:
                self.leftHand = leftHand

        self.headParts = self.findAllMatches('**/__Actor_head')
        self.legsParts = self.findAllMatches('**/__Actor_legs')
        self.hipsParts = self.legsParts.findAllMatches('**/joint_hips')
        self.torsoParts = self.hipsParts.findAllMatches('**/__Actor_torso')

    def getBookActors(self):
        if self.__bookActors:
            return self.__bookActors
        bookActor = Actor.Actor('phase_3.5/models/props/book-mod',
                                {'book': 'phase_3.5/models/props/book-chan'})
        bookActor2 = Actor.Actor(other=bookActor)
        bookActor3 = Actor.Actor(other=bookActor)
        self.__bookActors = [bookActor, bookActor2, bookActor3]
        hands = self.getRightHands()
        for bookActor, hand in zip(self.__bookActors, hands):
            bookActor.reparentTo(hand)
            bookActor.hide()
        return self.__bookActors

    def getHoleActors(self):
        if self.__holeActors:
            return self.__holeActors
        holeActor = Actor.Actor('phase_3.5/models/props/portal-mod',
                                {'hole': 'phase_3.5/models/props/portal-chan'})
        holeActor2 = Actor.Actor(other=holeActor)
        holeActor3 = Actor.Actor(other=holeActor)
        self.__holeActors = [holeActor, holeActor2, holeActor3]
        for ha in self.__holeActors:
            if hasattr(self, 'uniqueName'):
                holeName = self.uniqueName('toon-portal')
            else:
                holeName = 'toon-portal'
            ha.setName(holeName)
        return self.__holeActors

    def rescaleToon(self):
        animalStyle = self.style.getAnimal()
        bodyScale = ToonGlobals.toonBodyScales[animalStyle]
        headScale = ToonGlobals.toonHeadScales[animalStyle]
        self.setAvatarScale(bodyScale)
        for lod in self.getLODNames():
            self.getPart('head', lod).setScale(headScale)

    def getBodyScale(self):
        animalStyle = self.style.getAnimal()
        bodyScale = ToonGlobals.toonBodyScales[animalStyle]
        return bodyScale

    def resetHeight(self):
        if (not hasattr(self, 'style')) or (not self.style):
            return None
        animal = self.style.getAnimal()
        bodyScale = ToonGlobals.toonBodyScales[animal]
        headScale = ToonGlobals.toonHeadScales[animal][2]
        legHeight = ToonGlobals.legHeightDict[self.style.legs]
        torsoHeight = ToonGlobals.torsoHeightDict[self.style.torso]
        headHeight = ToonGlobals.headHeightDict[self.style.head]
        self.shoulderHeight = (legHeight*bodyScale) + (torsoHeight*bodyScale)
        height = self.shoulderHeight + (headHeight*headScale)
        self.setHeight(height)

    def generateToonLegs(self, copy=1):
        filePrefix = 'phase_3' + ToonGlobals.LegDict.get(self.style.legs)
        if filePrefix is None:
            self.notify.error('Unknown leg style: %s' % self.style.legs)
        self.loadModel(filePrefix + '1000', 'legs', '1000', copy)
        self.loadModel(filePrefix + '500', 'legs', '500', copy)
        self.loadModel(filePrefix + '250', 'legs', '250', copy)
        if not copy:
            self.showPart('legs', '1000')
            self.showPart('legs', '500')
            self.showPart('legs', '250')
        legsAnims = ToonGlobals.LegsAnimDict[self.style.legs]
        self.loadAnims(legsAnims, 'legs', '1000')
        self.loadAnims(legsAnims, 'legs', '500')
        self.loadAnims(legsAnims, 'legs', '250')
        self.findAllMatches('**/boots_short').stash()
        self.findAllMatches('**/boots_long').stash()
        self.findAllMatches('**/shoes').stash()

    def swapToonLegs(self, legStyle, copy=1):
        self.unparentToonParts()
        self.removePart('legs', '1000')
        self.removePart('legs', '500')
        self.removePart('legs', '250')

        # BUGFIX: Until upstream Panda3D includes this, we have to do it here.
        if 'legs' in self._Actor__commonBundleHandles:
            del self._Actor__commonBundleHandles['legs']

        self.style.legs = legStyle
        self.generateToonLegs(copy)
        self.generateToonColor()
        self.parentToonParts()
        self.rescaleToon()
        self.resetHeight()
        del self.shadowJoint
        self.initializeDropShadow()
        # TODO: Add support for future-style nametags.

    def generateToonTorso(self, copy=1, genClothes=1):
        filePrefix = 'phase_3' + ToonGlobals.TorsoDict.get(self.style.torso)
        if filePrefix is None:
            self.notify.error('Unknown torso style: %s' % self.style.torso)
        self.loadModel(filePrefix + '1000', 'torso', '1000', copy)
        if len(self.style.torso) == 1:
            # Naked torsos only have one LOD:
            self.loadModel(filePrefix + '1000', 'torso', '500', copy)
            self.loadModel(filePrefix + '1000', 'torso', '250', copy)
        else:
            self.loadModel(filePrefix + '500', 'torso', '500', copy)
            self.loadModel(filePrefix + '250', 'torso', '250', copy)
        if not copy:
            self.showPart('torso', '1000')
            self.showPart('torso', '500')
            self.showPart('torso', '250')
        torsoAnims = ToonGlobals.TorsoAnimDict[self.style.torso]
        self.loadAnims(torsoAnims, 'torso', '1000')
        self.loadAnims(torsoAnims, 'torso', '500')
        self.loadAnims(torsoAnims, 'torso', '250')

        # Finally, generate the clothes if specified, and the Toon isn't naked:
        if genClothes and (len(self.style.torso) > 1):
            self.generateToonClothes()

    def swapToonTorso(self, torsoStyle, copy=1, genClothes=1):
        self.unparentToonParts()
        self.removePart('torso', '1000')
        self.removePart('torso', '500')
        self.removePart('torso', '250')

        # BUGFIX: Until upstream Panda3D includes this, we have to do it here.
        if 'torso' in self._Actor__commonBundleHandles:
            del self._Actor__commonBundleHandles['torso']

        self.style.torso = torsoStyle
        self.generateToonTorso(copy, genClothes)
        self.generateToonColor()
        self.parentToonParts()
        self.rescaleToon()
        self.resetHeight()
        self.setupToonNodes()
        self.generateBackpack()

    def generateToonHead(self, copy=1):
        ToonHead.generateToonHead(
            self, copy, self.style, ('1000', '500', '250'))

        # For the moment, only dog Toons have head animations (for their ears):
        if self.style.getAnimal() == 'dog':
            headAnims = ToonGlobals.HeadAnimDict[self.style.head]
            self.loadAnims(headAnims, 'head', '1000')
            self.loadAnims(headAnims, 'head', '500')
            self.loadAnims(headAnims, 'head', '250')

    def swapToonHead(self, headStyle, copy=1):
        self.stopLookAroundNow()
        self.eyelids.request('open')
        self.unparentToonParts()
        self.removePart('head', '1000')
        self.removePart('head', '500')
        self.removePart('head', '250')

        # BUGFIX: Until upstream Panda3D includes this, we have to do it here.
        if 'head' in self._Actor__commonBundleHandles:
            del self._Actor__commonBundleHandles['head']

        self.style.head = headStyle
        self.generateToonHead(copy)
        self.generateToonColor()
        self.parentToonParts()
        self.rescaleToon()
        self.resetHeight()
        self.eyelids.request('open')
        self.startLookAround()

    def generateToonColor(self):
        ToonHead.generateToonColor(self, self.style)
        armColor = self.style.getArmColor()
        gloveColor = self.style.getGloveColor()
        legColor = self.style.getLegColor()
        for lodName in self.getLODNames():
            torso = self.getPart('torso', lodName)
            if len(self.style.torso) == 1:
                parts = torso.findAllMatches('**/torso*')
                parts.setColor(armColor)
            for pieceName in ('arms', 'neck'):
                piece = torso.find('**/' + pieceName)
                piece.setColor(armColor)
            hands = torso.find('**/hands')
            hands.setColor(gloveColor)
            legs = self.getPart('legs', lodName)
            for pieceName in ('legs', 'feet'):
                piece = legs.find('**/%s;+s' % pieceName)
                piece.setColor(legColor)

    def swapToonColor(self, dna):
        self.setStyle(dna)
        self.generateToonColor()

    def __swapToonClothes(self, dna):
        self.setStyle(dna)
        self.generateToonClothes(fromNet=1)

    def sendLogSuspiciousEvent(self, msg):
        return None # virtual function.

    def generateToonClothes(self, fromNet=0):
        swappedTorso = 0
        if not self.hasLOD():
            return None

        # If we are a naked Toon, we don't have any clothes. Simply swap the
        # torso, and exit the function. Otherwise, continue:
        torso = self.style.torso
        if len(torso) < 2:
            # TODO: Naked Toons are not currently supported.
            return 0

        # First, if we are a girl Toon, and fromNet is False, swap the torso if
        # necessary:
        if (self.style.getGender() is 'f') and (not fromNet):
            try:
                bottomPair = ToonDNA.GirlBottoms[self.style.botTex]
            except:
                bottomPair = ToonDNA.GirlBottoms[0]
            if (torso[1] is 's') and (bottomPair[1] is ToonDNA.SKIRT):
                self.swapToonTorso(torso[0] + 'd', genClothes=0)
                swappedTorso = 1
            elif (torso[1] is 'd') and (bottomPair[1] is ToonDNA.SHORTS):
                self.swapToonTorso(torso[0] + 's', genClothes=0)
                swappedTorso = 1

        # Next, load the textures for the clothing items:

        def loadClothesTexture(texName, defaultTexName):
            tex = loader.loadTexture(texName, okMissing=True)
            if tex is None:
                self.notify.warning("Failed to load texture: '%s'" % texName)
                tex = loader.loadTexture(defaultTexName)
            tex.setMinfilter(Texture.FTLinearMipmapLinear)
            tex.setMagfilter(Texture.FTLinear)
            return tex

        defaultTexName = ToonDNA.Shirts[0]
        try:
            texName = ToonDNA.Shirts[self.style.topTex]
        except:
            texName = defaultTexName
        shirtTex = loadClothesTexture(texName, defaultTexName)
        defaultTexName = ToonDNA.Sleeves[0]
        try:
            texName = ToonDNA.Sleeves[self.style.sleeveTex]
        except:
            texName = defaultTexName
        sleeveTex = loadClothesTexture(texName, defaultTexName)
        if self.style.getGender() is 'm':
            defaultTexName = ToonDNA.BoyShorts[0]
            try:
                texName = ToonDNA.BoyShorts[self.style.botTex]
            except:
                texName = defaultTexName
        else:
            defaultTexName = ToonDNA.GirlBottoms[0][0]
            try:
                texName = ToonDNA.GirlBottoms[self.style.botTex][0]
            except:
                texName = defaultTexName
        bottomTex = loadClothesTexture(texName, defaultTexName)

        # Finally, set the textures and colors for the clothing items:
        try:
            shirtColor = ToonDNA.ClothesColors[self.style.topTexColor]
        except:
            shirtColor = ToonDNA.ClothesColors[0]
        try:
            sleeveColor = ToonDNA.ClothesColors[self.style.sleeveTexColor]
        except:
            sleeveColor = ToonDNA.ClothesColors[0]
        try:
            bottomColor = ToonDNA.ClothesColors[self.style.botTexColor]
        except:
            bottomColor = ToonDNA.ClothesColors[0]
        darkBottomColor = bottomColor * 0.5
        darkBottomColor.setW(1.0)
        for lodName in self.getLODNames():
            thisPart = self.getPart('torso', lodName)
            top = thisPart.find('**/torso-top')
            top.setTexture(shirtTex, 1)
            top.setColor(shirtColor)
            sleeves = thisPart.find('**/sleeves')
            sleeves.setTexture(sleeveTex, 1)
            sleeves.setColor(sleeveColor)
            bottoms = thisPart.findAllMatches('**/torso-bot')
            for bottomNum in range(0, bottoms.getNumPaths()):
                bottom = bottoms.getPath(bottomNum)
                bottom.setTexture(bottomTex, 1)
                bottom.setColor(bottomColor)
            caps = thisPart.findAllMatches('**/torso-bot-cap')
            caps.setColor(darkBottomColor)
        return swappedTorso

    def generateHat(self, fromRTM=False):
        hat = self.getHat()
        if hat[0] >= len(ToonDNA.HatModels):
            self.notify.warning('Invalid hat index: %d' % hat[0])
            return None

        # First, remove any currently loaded hats, and show our Toon's ears:
        if len(self.hatNodes) > 0:
            for hatNode in self.hatNodes:
                hatNode.removeNode()
            self.hatNodes = []
        self.showEars()

        # If the hat index is 0, we don't have a hat, so simply exit the
        # function here:
        if hat[0] is 0:
            return None

        # Otherwise, load the hat:
        hatGeom = loader.loadModel(ToonDNA.HatModels[hat[0]], okMissing=True)
        if not hatGeom:
            self.notify.warning('Failed to load hat: %d' % hat[0])
            return None

        # If we are putting on one of these hats, hide the Toon's ears:
        if hat[0] in (54,):
            self.hideEars()

        # Next, if this hat has a specified texture, load and set it:
        if hat[1]:
            texName = ToonDNA.HatTextures[hat[1]]
            tex = loader.loadTexture(texName, okMissing=True)
            if tex is None:
                self.notify.warning("Failed to load texture: '%s'" % texName)
            else:
                tex.setMinfilter(Texture.FTLinearMipmapLinear)
                tex.setMagfilter(Texture.FTLinear)
                hatGeom.setTexture(tex, 1)

        # Finally, attach the hat to the Toon's head and set its transforms:
        if fromRTM:
            reload(AccessoryGlobals)
        transOffset = None
        transTable = AccessoryGlobals.ExtendedHatTransTable.get(hat[0])
        if transTable:
            transOffset = transTable.get(self.style.head[:2])
        if transOffset is None:
            transTable = AccessoryGlobals.HatTransTable
            transOffset = transTable.get(self.style.head[:2])
            if transOffset is None:
                return None
        hatGeom.setPos(transOffset[0][0], transOffset[0][1], transOffset[0][2])
        hatGeom.setHpr(transOffset[1][0], transOffset[1][1], transOffset[1][2])
        hatGeom.setScale(transOffset[2][0], transOffset[2][1],
                         transOffset[2][2])
        headNodes = self.findAllMatches('**/__Actor_head')
        for headNode in headNodes:
            hatNode = headNode.attachNewNode('hatNode')
            self.hatNodes.append(hatNode)
            hatGeom.instanceTo(hatNode)

    def generateGlasses(self, fromRTM=False):
        glasses = self.getGlasses()
        if glasses[0] >= len(ToonDNA.GlassesModels):
            self.notify.warning('Invalid glasses index: %d' % glasses[0])
            return None

        # First, remove any currently loaded glasses, and show our Toon's
        # eyelashes:
        if len(self.glassesNodes) > 0:
            for glassesNode in self.glassesNodes:
                glassesNode.removeNode()
            self.glassesNodes = []
        self.showEyelashes()

        # If the glasses index is 0, we don't have any glasses, so simply exit
        # the function here:
        if glasses[0] is 0:
            return None

        # Otherwise, load the glasses:
        glassesGeom = loader.loadModel(ToonDNA.GlassesModels[glasses[0]],
                                       okMissing=True)
        if not glassesGeom:
            self.notify.warning('Failed to load glasses: %d' % glasses[0])
            return None

        # If we are putting on one of these glasses, hide the Toon's eyelashes:
        if glasses[0] in (15, 16):
            self.hideEyelashes()

        # Next, if these glasses have a specified texture, load and set it:
        if glasses[1]:
            texName = ToonDNA.GlassesTextures[glasses[1]]
            tex = loader.loadTexture(texName, okMissing=True)
            if tex is None:
                self.notify.warning("Failed to load texture: '%s'" % texName)
            else:
                tex.setMinfilter(Texture.FTLinearMipmapLinear)
                tex.setMagfilter(Texture.FTLinear)
                glassesGeom.setTexture(tex, 1)

        # Finally, attach the glasses to the Toon's head and set their
        # transforms:
        if fromRTM:
            reload(AccessoryGlobals)
        transOffset = None
        transTable = AccessoryGlobals.ExtendedGlassesTransTable.get(glasses[0])
        if transTable:
            transOffset = transTable.get(self.style.head[:2])
        if transOffset is None:
            transTable = AccessoryGlobals.GlassesTransTable
            transOffset = transTable.get(self.style.head[:2])
            if transOffset is None:
                return None
        glassesGeom.setPos(transOffset[0][0], transOffset[0][1],
                           transOffset[0][2])
        glassesGeom.setHpr(transOffset[1][0], transOffset[1][1],
                           transOffset[1][2])
        glassesGeom.setScale(transOffset[2][0], transOffset[2][1],
                             transOffset[2][2])
        headNodes = self.findAllMatches('**/__Actor_head')
        for headNode in headNodes:
            glassesNode = headNode.attachNewNode('glassesNode')
            self.glassesNodes.append(glassesNode)
            glassesGeom.instanceTo(glassesNode)

    def generateBackpack(self, fromRTM=False):
        backpack = self.getBackpack()
        if backpack[0] >= len(ToonDNA.BackpackModels):
            self.notify.warning('Invalid backpack index: %d' % backpack[0])
            return None

        # First, remove any currently loaded backpacks:
        if len(self.backpackNodes) > 0:
            for backpackNode in self.backpackNodes:
                backpackNode.removeNode()
            self.backpackNodes = []

        # If the backpack index is 0, we don't have a backpack, so simply exit
        # the function here:
        if backpack[0] is 0:
            return None

        # Otherwise, load the backpack:
        backpackGeom = loader.loadModel(ToonDNA.BackpackModels[backpack[0]],
                                        okMissing=True)
        if not backpackGeom:
            self.notify.warning('Failed to load backpack: %d' % backpack[0])
            return None

        # Next, if this backpack has a specified texture, load and set it:
        if backpack[1]:
            texName = ToonDNA.BackpackTextures[backpack[1]]
            tex = loader.loadTexture(texName, okMissing=True)
            if tex is None:
                self.notify.warning("Failed to load texture: '%s'" % texName)
            else:
                tex.setMinfilter(Texture.FTLinearMipmapLinear)
                tex.setMagfilter(Texture.FTLinear)
                backpackGeom.setTexture(tex, 1)

        # Finally, attach the backpack to the Toon's torso and set its
        # transforms:
        if fromRTM:
            reload(AccessoryGlobals)
        transOffset = None
        transTable = AccessoryGlobals.ExtendedBackpackTransTable.get(
                                                         backpack[0])
        if transTable:
            transOffset = transTable.get(self.style.torso[:1])
        if transOffset is None:
            transTable = AccessoryGlobals.BackpackTransTable
            transOffset = transTable.get(self.style.torso[:1])
            if transOffset is None:
                return None
        backpackGeom.setPos(transOffset[0][0], transOffset[0][1],
                            transOffset[0][2])
        backpackGeom.setHpr(transOffset[1][0], transOffset[1][1],
                            transOffset[1][2])
        backpackGeom.setScale(transOffset[2][0], transOffset[2][1],
                              transOffset[2][2])
        nodes = self.findAllMatches('**/def_joint_attachFlower')
        for node in nodes:
            theNode = node.attachNewNode('backpackNode')
            self.backpackNodes.append(theNode)
            backpackGeom.instanceTo(theNode)

    def generateShoes(self):
        shoes = self.getShoes()
        if shoes[0] >= len(ToonDNA.ShoesModels):
            self.notify.warning('Invalid shoes index: %d' % shoes[0])
            return None

        # First, stash any currently used shoes:
        self.findAllMatches('**/feet;+s').stash()
        self.findAllMatches('**/boots_short;+s').stash()
        self.findAllMatches('**/boots_long;+s').stash()
        self.findAllMatches('**/shoes;+s').stash()

        # If the shoes index is 0, we don't have any shoes, so simply exit the
        # function here:
        if shoes[0] is 0:
            self.findAllMatches('**/feet;+s').unstash()
            return None

        # Otherwise, unstash the wanted shoes:
        shoesGeoms = self.findAllMatches(
            '**/%s;+s' % ToonDNA.ShoesModels[shoes[0]])
        for shoesGeom in shoesGeoms:
            shoesGeom.unstash()

        # Finally, if these shoes have a specified texture, load and set it:
        for shoesGeom in shoesGeoms:
            texName = ToonDNA.ShoesTextures[shoes[1]]
            if (self.style.legs is 'l') and (shoes[0] is 3):
                texName = texName[:-4] + 'LL.jpg'
            tex = loader.loadTexture(texName, okMissing=True)
            if tex is None:
                self.notify.warning("Failed to load texture: '%s'" % texName)
            else:
                tex.setMinfilter(Texture.FTLinearMipmapLinear)
                tex.setMagfilter(Texture.FTLinear)
                shoesGeom.setTexture(tex, 1)

    def generateToonAccessories(self):
        self.generateHat()
        self.generateGlasses()
        self.generateBackpack()
        self.generateShoes()

    def setHat(self, hatIdx, textureIdx, colorIdx, fromRTM=False):
        self.style.hat = (hatIdx, textureIdx, colorIdx)
        self.generateHat(fromRTM=fromRTM)

    def getHat(self):
        return self.style.hat

    def setGlasses(self, glassesIdx, textureIdx, colorIdx, fromRTM=False):
        self.style.glasses = (glassesIdx, textureIdx, colorIdx)
        self.generateGlasses(fromRTM=fromRTM)

    def getGlasses(self):
        return self.style.glasses

    def setBackpack(self, backpackIdx, textureIdx, colorIdx, fromRTM=False):
        self.style.backpack = (backpackIdx, textureIdx, colorIdx)
        self.generateBackpack(fromRTM=fromRTM)

    def getBackpack(self):
        return self.style.backpack

    def setShoes(self, shoesIdx, textureIdx, colorIdx):
        self.style.shoes = (shoesIdx, textureIdx, colorIdx)
        self.generateShoes()

    def getShoes(self):
        return self.style.shoes

    def getShadowJoint(self):
        if hasattr(self, 'shadowJoint'):
            return self.shadowJoint
        shadowJoint = NodePath('shadowJoint')
        for lodName in self.getLODNames():
            joint = self.getPart('legs', lodName).find('**/joint_shadow')
            shadowJoint = shadowJoint.instanceTo(joint)

        self.shadowJoint = shadowJoint
        return shadowJoint

    def getShadowJoint(self):
        if hasattr(self, 'shadowJoint'):
            return self.shadowJoint
        shadowJoint = NodePath('shadowJoint')
        for lodName in self.getLODNames():
            joint = self.getPart('legs', lodName).find('**/joint_shadow')
            shadowJoint = shadowJoint.instanceTo(joint)
        self.shadowJoint = shadowJoint
        return shadowJoint

    def getRightHands(self):
        return self.rightHands

    def getLeftHands(self):
        return self.leftHands

    def getHeadParts(self):
        return self.headParts

    def getHipsParts(self):
        return self.hipsParts

    def getTorsoParts(self):
        return self.torsoParts

    def getLegsParts(self):
        return self.legsParts

    def findSomethingToLookAt(self):
        if self.randGen.random() < 0.1:
            x = self.randGen.choice((-0.8, -0.5, 0, 0.5, 0.8))
            y = self.randGen.choice((-0.5, 0, 0.5, 0.8))
            self.lerpLookAt(Point3(x, 1.5, y), blink=1)
        else:
            ToonHead.findSomethingToLookAt(self)

    def setForceJumpIdle(self, value):
        self.forceJumpIdle = value

    def showBooks(self):
        for bookActor in self.getBookActors():
            bookActor.show()

    def hideBooks(self):
        for bookActor in self.getBookActors():
            bookActor.hide()

    def getWake(self):
        if not self.wake:
            self.wake = Wake.Wake(render, self)
        return self.wake

    def getJar(self):
        if not self.jar:
            self.jar = loader.loadModel(
                'phase_5.5/models/estate/jellybeanJar.bam')
            self.jar.setP(290.0)
            self.jar.setY(0.5)
            self.jar.setZ(0.5)
            self.jar.setScale(0.0)
        return self.jar

    def removeJar(self):
        if self.jar:
            self.jar.removeNode()
            self.jar = None

    def setSpeed(self, forwardSpeed, rotateSpeed):
        self.forwardSpeed = forwardSpeed
        self.rotateSpeed = rotateSpeed
        action = None
        if self.standWalkRunReverse is None:
            return None
        if forwardSpeed >= ToonGlobals.RunCutOff:
            action = ToonGlobals.RUN_INDEX
        elif forwardSpeed > ToonGlobals.WalkCutOff:
            action = ToonGlobals.WALK_INDEX
        elif forwardSpeed < -ToonGlobals.WalkCutOff:
            action = ToonGlobals.REVERSE_INDEX
        elif rotateSpeed != 0.0:
            action = ToonGlobals.WALK_INDEX
        else:
            action = ToonGlobals.STAND_INDEX
        anim, rate = self.standWalkRunReverse[action]
        self.motion.enter()
        self.motion.setState(anim, rate)
        if anim != self.playingAnim:
            self.playingAnim = anim
            self.playingRate = rate
            self.stop()
            self.loop(anim)
            self.setPlayRate(rate, anim)
            # TODO: Add support for disguise animations.
        elif rate != self.playingRate:
            self.playingRate = rate
            if not self.isDisguised:
                self.setPlayRate(rate, anim)
            # TODO: Add support for disguise animations.
        showWake, wakeWaterHeight = ZoneUtil.getWakeInfo()
        if showWake and (self.getZ(render) < wakeWaterHeight):
            if abs(forwardSpeed) > ToonGlobals.WalkCutOff:
                currT = globalClock.getFrameTime()
                deltaT = currT - self.lastWakeTime
                if action is ToonGlobals.RUN_INDEX:
                    if (deltaT > ToonGlobals.WakeRunDelta) or (
                        deltaT > ToonGlobals.WakeWalkDelta):
                        self.getWake().createRipple(
                            wakeWaterHeight, rate=1, startFrame=4)
                        self.lastWakeTime = currT
        return action

    def enterOff(self, animMultiplier=1, ts=0, callback=None, extraArgs=[]):
        self.setActiveShadow(0)
        self.playingAnim = None

    def exitOff(self):
        return None

    def enterNeutral(self, animMultiplier=1, ts=0, callback=None,
                     extraArgs=[]):
        anim = 'neutral'
        self.pose(anim, int(self.getNumFrames(anim) * self.randGen.random()))
        self.loop(anim, restart=0)
        self.setPlayRate(animMultiplier, anim)
        self.playingAnim = anim
        self.setActiveShadow(1)

    def exitNeutral(self):
        self.stop()

    def enterVictory(self, animMultiplier=1, ts=0, callback=None,
                     extraArgs=[]):
        anim = 'victory'
        frame = int(ts * self.getFrameRate(anim) * animMultiplier)
        self.pose(anim, frame)
        self.loop('victory', restart=0)
        self.setPlayRate(animMultiplier, 'victory')
        self.playingAnim = anim
        self.setActiveShadow(0)

    def exitVictory(self):
        self.stop()

    def enterHappy(self, animMultiplier=1, ts=0, callback=None, extraArgs=[]):
        self.playingAnim = None
        self.playingRate = None
        self.standWalkRunReverse = (
            ('neutral', 1.0), ('walk', 1.0), ('run', 1.0), ('walk', -1.0)
        )
        self.setSpeed(self.forwardSpeed, self.rotateSpeed)
        self.setActiveShadow(1)

    def exitHappy(self):
        self.standWalkRunReverse = None
        self.stop()
        self.motion.exit()

    def enterSad(self, animMultiplier=1, ts=0, callback=None, extraArgs=[]):
        self.playingAnim = 'sad'
        self.playingRate = None
        self.standWalkRunReverse = (
            ('sad-neutral', 1.0), ('sad-walk', 1.2), ('sad-walk', 1.2),
            ('sad-walk', -1.0)
        )
        self.setSpeed(0, 0)
        # TODO: Disable Toon emotions.
        self.setActiveShadow(1)
        if self.isLocal():
            self.controlManager.disableAvatarJump()

    def exitSad(self):
        self.standWalkRunReverse = None
        self.stop()
        self.motion.exit()
        # TODO: Enable Toon emotions.
        if self.isLocal():
            self.controlManager.enableAvatarJump()

    def enterCatching(self, animMultiplier=1, ts=0, callback=None,
                      extraArgs=[]):
        self.playingAnim = None
        self.playingRate = None
        self.standWalkRunReverse = (
            ('catch-neutral', 1.0), ('catch-run', 1.0), ('catch-run', 1.0),
            ('catch-run', -1.0)
        )
        self.setSpeed(self.forwardSpeed, self.rotateSpeed)
        self.setActiveShadow(1)

    def exitCatching(self):
        self.standWalkRunReverse = None
        self.stop()
        self.motion.exit()

    def enterCatchEating(self, animMultiplier=1, ts=0, callback=None,
                         extraArgs=[]):
        self.playingAnim = None
        self.playingRate = None
        self.standWalkRunReverse = (
            ('catch-eatneutral', 1.0), ('catch-eatnrun', 1.0),
            ('catch-eatnrun', 1.0), ('catch-eatnrun', -1.0)
        )
        self.setSpeed(self.forwardSpeed, self.rotateSpeed)
        self.setActiveShadow(0)

    def exitCatchEating(self):
        self.standWalkRunReverse = None
        self.stop()
        self.motion.exit()

    def enterWalk(self, animMultiplier=1, ts=0, callback=None, extraArgs=[]):
        self.loop('walk')
        self.setPlayRate(animMultiplier, 'walk')
        self.setActiveShadow(1)

    def exitWalk(self):
        self.stop()

    def getJumpDuration(self):
        if self.playingAnim is 'neutral':
            return self.getDuration('jump', 'legs')
        else:
            return self.getDuration('running-jump', 'legs')

    def enterJump(self, animMultiplier=1, ts=0, callback=None, extraArgs=[]):
        if not self.isDisguised:
            if self.playingAnim is 'neutral':
                anim = 'jump'
            else:
                anim = 'running-jump'
            self.playingAnim = anim
            self.setPlayRate(animMultiplier, anim)
            self.play(anim)
        self.setActiveShadow(1)

    def exitJump(self):
        self.stop()
        self.playingAnim = 'neutral'

    def enterJumpSquat(self, animMultiplier=1, ts=0, callback=None,
                       extraArgs=[]):
        if not self.isDisguised:
            if self.playingAnim is 'neutral':
                anim = 'jump-squat'
            else:
                anim = 'running-jump-squat'
            self.playingAnim = anim
            self.setPlayRate(animMultiplier, anim)
            self.play(anim)
        self.setActiveShadow(1)

    def exitJumpSquat(self):
        self.stop()
        self.playingAnim = 'neutral'

    def enterJumpAirborne(self, animMultiplier=1, ts=0, callback=None,
                          extraArgs=[]):
        if not self.isDisguised:
            if (self.playingAnim is 'neutral') or self.forceJumpIdle:
                anim = 'jump-idle'
            else:
                anim = 'running-jump-idle'
            self.playingAnim = anim
            self.setPlayRate(animMultiplier, anim)
            self.loop(anim)
        self.setActiveShadow(1)

    def exitJumpAirborne(self):
        self.stop()
        self.playingAnim = 'neutral'

    def enterJumpLand(self, animMultiplier=1, ts=0, callback=None,
                      extraArgs=[]):
        if not self.isDisguised:
            if self.playingAnim is 'running-jump-idle':
                anim = 'running-jump-land'
            else:
                anim = 'jump-land'
            self.playingAnim = anim
            self.setPlayRate(animMultiplier, anim)
            self.play(anim)
        self.setActiveShadow(1)

    def exitJumpLand(self):
        self.stop()
        self.playingAnim = 'neutral'

    def enterRun(self, animMultiplier=1, ts=0, callback=None, extraArgs=[]):
        self.loop('run')
        self.setPlayRate(animMultiplier, 'run')
        # TODO: Disable Toon emotions.
        self.setActiveShadow(1)

    def exitRun(self):
        self.stop()
        # TODO: Enable Toon emotions.

    def enterCringe(self, animMultiplier=1, ts=0, callback=None, extraArgs=[]):
        self.loop('cringe')
        self.getGeomNode().setPos(0, 0, -2)
        self.setPlayRate(animMultiplier, 'swim')

    def exitCringe(self, animMultiplier=1, ts=0, callback=None, extraArgs=[]):
        self.stop()
        self.getGeomNode().setPos(0, 0, 0)
        self.playingAnim = 'neutral'
        self.setPlayRate(animMultiplier, 'swim')

    def enterDive(self, animMultiplier=1, ts=0, callback=None, extraArgs=[]):
        self.loop('swim')
        if hasattr(self.getGeomNode(), 'setPos'):
            self.getGeomNode().setPos(0, 0, -2)
            self.setPlayRate(animMultiplier, 'swim')
            self.setActiveShadow(0)
            self.dropShadow.hide()
            # TODO: Add support for future-style nametags.

    def exitDive(self):
        self.stop()
        self.getGeomNode().setPos(0, 0, 0)
        self.playingAnim = 'neutral'
        self.dropShadow.show()
        # TODO: Add support for future-style nametags.

    def enterSwimHold(self, animMultiplier=1, ts=0, callback=None,
                      extraArgs=[]):
        self.getGeomNode().setPos(0, 0, -2)
        # TODO: Add support for future-style nametags.
        self.pose('swim', 55)

    def exitSwimHold(self):
        self.stop()
        self.getGeomNode().setPos(0, 0, 0)
        self.playingAnim = 'neutral'
        self.dropShadow.show()
        # TODO: Add support for future-style nametags.

    def enterSwim(self, animMultiplier=1, ts=0, callback=None, extraArgs=[]):
        # TODO: Disable Toon emotions.
        self.playingAnim = 'swim'
        self.loop('swim')
        self.setPlayRate(animMultiplier, 'swim')
        self.getGeomNode().setP(-89.0)
        self.dropShadow.hide()
        if self.isLocal():
            self.useSwimControls()
        # TODO: Add support for future-style nametags.
        self.startBobSwimTask()
        self.setActiveShadow(0)

    def exitSwim(self):
        self.stop()
        self.playingAnim = 'neutral'
        self.stopBobSwimTask()
        self.getGeomNode().setPosHpr(0, 0, 0, 0, 0, 0)
        self.dropShadow.show()
        if self.isLocal():
            self.useWalkControls()
        # TODO: Add support for future-style nametags.
        # TODO: Enable Toon emotes.

    def startBobSwimTask(self):
        swimBob = getattr(self, 'swimBob', None)
        if swimBob:
            swimBob.finish()
        self.getGeomNode().setZ(4.0)
        # TODO: Add support for future-style nametags.
        self.swimBob = Sequence(
            self.getGeomNode().posInterval(
                1, (0, -3, 3), blendType='easeInOut'
            ),
            self.getGeomNode().posInterval(
                1, (0, -3, 4), blendType='easeInOut'
            )
        )
        self.swimBob.loop()

    def stopBobSwimTask(self):
        swimBob = getattr(self, 'swimBob', None)
        if swimBob:
            swimBob.finish()
        self.getGeomNode().setPos(0, 0, 0)
        # TODO: Add support for future-style nametags.

    def enterOpenBook(self, animMultiplier=1, ts=0, callback=None,
                      extraArgs=[]):
        # TODO: Disable Toon emotes.
        self.playingAnim = 'openBook'
        self.stopLookAround()
        self.lerpLookAt(Point3(0, 1, -2))
        bookTracks = Parallel()
        for bookActor in self.getBookActors():
            bookTracks.append(
                ActorInterval(bookActor, 'book', startTime=1.2, endTime=1.5)
            )
        bookTracks.append(
            ActorInterval(self, 'book', startTime=1.2, endTime=1.5)
        )
        if hasattr(self, 'uniqueName'):
            trackName = self.uniqueName('openBook')
        else:
            trackName = 'openBook'
        self.track = Sequence(
            Func(self.showBooks),
            bookTracks,
            Wait(0.1),
        name=trackName)
        if callback:
            self.track.setDoneEvent(self.track.getName())
            self.acceptOnce(self.track.getName(), callback, extraArgs)
        self.track.start(ts)
        self.setActiveShadow(0)

    def exitOpenBook(self):
        self.playingAnim = 'neutralob'
        if self.track is not None:
            self.ignore(self.track.getName())
            self.track.finish()
            DelayDelete.cleanupDelayDeletes(self.track)
            self.track = None
        self.hideBooks()
        self.startLookAround()
        # TODO: Enable Toon emotions.

    def enterReadBook(self, animMultiplier=1, ts=0, callback=None,
                      extraArgs=[]):
        # TODO: Disable Toon emotes.
        self.playingAnim = 'readBook'
        self.stopLookAround()
        self.lerpLookAt(Point3(0, 1, -2))
        self.showBooks()
        for bookActor in self.getBookActors():
            bookActor.pingpong('book', fromFrame=38, toFrame=118)
        self.pingpong('book', fromFrame=38, toFrame=118)
        self.setActiveShadow(0)

    def exitReadBook(self):
        self.playingAnim = 'neutralrb'
        self.hideBooks()
        for bookActor in self.getBookActors():
            bookActor.stop()
        self.startLookAround()
        # TODO: Enable Toon emotes.

    def enterCloseBook(self, animMultiplier=1, ts=0, callback=None,
                       extraArgs=[]):
        # TODO: Disable Toon emotes.
        self.playingAnim = 'closeBook'
        bookTracks = Parallel()
        for bookActor in self.getBookActors():
            bookTracks.append(
                ActorInterval(bookActor, 'book', startTime=4.96, endTime=6.5)
            )
        bookTracks.append(
            ActorInterval(self, 'book', startTime=4.96, endTime=6.5)
        )
        if hasattr(self, 'uniqueName'):
            trackName = self.uniqueName('closeBook')
        else:
            trackName = 'closeBook'
        self.track = Sequence(
            Func(self.showBooks),
            bookTracks,
            Func(self.hideBooks),
        name=trackName)
        if callback:
            self.track.setDoneEvent(self.track.getName())
            self.acceptOnce(self.track.getName(), callback, extraArgs)
        self.track.start(ts)
        self.setActiveShadow(0)

    def exitCloseBook(self):
        self.playingAnim = 'neutralcb'
        if self.track is not None:
            self.ignore(self.track.getName())
            self.track.finish()
            DelayDelete.cleanupDelayDeletes(self.track)
            self.track = None
        # TODO: Enable Toon emotes.

    def getSoundTeleport(self):
        if not self.soundTeleport:
            self.soundTeleport = base.loadSfx(
                'phase_3.5/audio/sfx/AV_teleport.mp3')
        return self.soundTeleport

    def getTeleportOutTrack(self, autoFinishTrack=1):

        def showHoles(holes, hands):
            for hole, hand in zip(holes, hands):
                hole.reparentTo(hand)

        def reparentHoles(holes, toon):
            holes[0].reparentTo(toon)
            holes[1].detachNode()
            holes[2].detachNode()
            holes[0].setBin('shadow', 0)
            holes[0].setDepthTest(0)
            holes[0].setDepthWrite(0)

        def cleanupHoles(holes):
            holes[0].detachNode()
            holes[0].clearBin()
            holes[0].clearDepthTest()
            holes[0].clearDepthWrite()

        holes = self.getHoleActors()
        hands = self.getRightHands()
        holeTrack = Track(
            (0.0, Func(showHoles, holes, hands)),
            (0.5, SoundInterval(self.getSoundTeleport(), node=self)),
            (1.708, Func(reparentHoles, holes, self)),
            (3.4, Func(cleanupHoles, holes))
        )
        if hasattr(self, 'uniqueName'):
            trackName = self.uniqueName('teleportOut')
        else:
            trackName = 'teleportOut'
        track = Parallel(holeTrack, name=trackName, autoFinish=autoFinishTrack)
        for hole in holes:
            track.append(ActorInterval(hole, 'hole', duration=3.4))
        track.append(ActorInterval(self, 'teleport', duration=3.4))
        return track

    def enterTeleportOut(self, animMultiplier=1, ts=0, callback=None,
                         extraArgs=[]):
        name = self.name
        if hasattr(self, 'doId'):
            name += '-' + str(self.doId)
        self.notify.debug('enterTeleportOut %s' % name)
        if self.ghostMode or self.isDisguised:
            if callback:
                callback(*extraArgs)
            return None
        self.playingAnim = 'teleport'
        # TODO: Disable Toon emotes.
        if self.isLocal():
            autoFinishTrack = 0
        else:
            autoFinishTrack = 1
        self.track = self.getTeleportOutTrack(autoFinishTrack)
        self.track.setDoneEvent(self.track.getName())
        self.acceptOnce(self.track.getName(), self.finishTeleportOut,
                        [callback, extraArgs])
        holeClip = PlaneNode('holeClip')
        self.holeClipPath = self.attachNewNode(holeClip)
        self.getGeomNode().setClipPlane(self.holeClipPath)
        # TODO: Add support for future-style nametags.
        self.track.start(ts)
        self.setActiveShadow(0)

    def finishTeleportOut(self, callback=None, extraArgs=[]):
        name = self.name
        if hasattr(self, 'doId'):
            name += '-' + str(self.doId)
        self.notify.debug('finishTeleportOut %s' % name)
        if self.track is not None:
            self.ignore(self.track.getName())
            self.track.finish()
            DelayDelete.cleanupDelayDeletes(self.track)
            self.track = None
        if hasattr(self, 'animFSM'):
            self.animFSM.request('TeleportedOut')
        if callback:
            callback(*extraArgs)

    def exitTeleportOut(self):
        name = self.name
        if hasattr(self, 'doId'):
            name += '-' + str(self.doId)
        self.notify.debug('exitTeleportOut %s' % name)
        if self.track is not None:
            self.ignore(self.track.getName())
            self.track.finish()
            self.track = None
        geomNode = self.getGeomNode()
        if geomNode and not geomNode.isEmpty():
            self.getGeomNode().clearClipPlane()
        # TODO: Add support for future-style nametags.
        if self.holeClipPath:
            self.holeClipPath.removeNode()
            self.holeClipPath = None
        # TODO: Enable Toon emotes.
        if self and not self.isEmpty():
            self.show()

    def getTeleportInTrack(self):
        hole = self.getHoleActors()[0]
        hole.setBin('shadow', 0)
        hole.setDepthTest(0)
        hole.setDepthWrite(0)
        holeTrack = Sequence()
        holeTrack.append(Func(hole.reparentTo, self))
        pos = Point3(0, -2.4, 0)
        holeTrack.append(Func(hole.setPos, self, pos))
        holeTrack.append(
            ActorInterval(hole, 'hole', startTime=3.4, endTime=3.1)
        )
        holeTrack.append(Wait(0.6))
        holeTrack.append(
            ActorInterval(hole, 'hole', startTime=3.1, endTime=3.4)
        )

        def restoreHole(hole):
            hole.setPos(0, 0, 0)
            hole.detachNode()
            hole.clearBin()
            hole.clearDepthTest()
            hole.clearDepthWrite()

        holeTrack.append(Func(restoreHole, hole))
        # TODO: Add support for future-style nametags.
        toonTrack = Sequence(
            Wait(0.3),
            Func(self.getGeomNode().show),
            ActorInterval(self, 'jump', startTime=0.45)
        )
        if hasattr(self, 'uniqueName'):
            trackName = self.uniqueName('teleportIn')
        else:
            trackName = 'teleportIn'
        return Parallel(holeTrack, toonTrack, name=trackName)

    def enterTeleportIn(self, animMultiplier=1, ts=0, callback=None,
                        extraArgs=[]):
        if self.ghostMode or self.isDisguised:
            if callback:
                callback(*extraArgs)
            return None
        self.show()
        self.playingAnim = 'teleport'
        # TODO: Disable Toon emotes.
        self.pose('teleport', self.getNumFrames('teleport') - 1)
        self.getGeomNode().hide()
        # TODO: Add support for future-style nametags.
        self.track = self.getTeleportInTrack()
        if callback:
            self.track.setDoneEvent(self.track.getName())
            self.acceptOnce(self.track.getName(), callback, extraArgs)
        self.track.start(ts)
        self.setActiveShadow(0)

    def exitTeleportIn(self):
        self.playingAnim = None
        if self.track is not None:
            self.ignore(self.track.getName())
            self.track.finish()
            DelayDelete.cleanupDelayDeletes(self.track)
            self.track = None
        if (not self.ghostMode) and (not self.isDisguised):
            self.getGeomNode().show()
            # TODO: Add support for future-style nametags.
        # TODO: Enable Toon emotes.

    def enterTeleportedOut(self, animMultiplier=1, ts=0, callback=None,
                           extraArgs=[]):
        self.setActiveShadow(0)

    def exitTeleportedOut(self):
        return None

    def getDiedInterval(self, autoFinishTrack=1):
        sound = loader.loadSfx('phase_5/audio/sfx/ENC_Lose.mp3')
        if hasattr(self, 'uniqueName'):
            trackName = self.uniqueName('died')
        else:
            trackName = 'died'
        # TODO: Manage Toon emotes.
        ival = Sequence(
            Func(self.sadEyes),
            Func(self.blinkEyes),
            Track(
                (0, ActorInterval(self, 'lose')),
                (2, SoundInterval(sound, node=self)),
                (5.333, self.scaleInterval(
                    1.5, VBase3(0.01, 0.01, 0.01), blendType='easeInOut')
                )
            ),
            Func(self.detachNode),
            Func(self.setScale, 1, 1, 1),
            Func(self.normalEyes),
            Func(self.blinkEyes),
        name=trackName, autoFinish=autoFinishTrack)
        return ival

    def enterDied(self, animMultiplier=1, ts=0, callback=None, extraArgs=[]):
        if self.ghostMode:
            if callback:
                callback(*extraArgs)
            return None
        if self.isDisguised:
            self.takeOffSuit()
        self.playingAnim = 'lose'
        # TODO: Disable Toon emotes.
        if self.isLocal():
            autoFinishTrack = 0
        else:
            autoFinishTrack = 1
        if hasattr(self, 'jumpLandAnimFixTask') and self.jumpLandAnimFixTask:
            self.jumpLandAnimFixTask.remove()
            self.jumpLandAnimFixTask = None
        self.track = self.getDiedInterval(autoFinishTrack)
        if callback:
            self.track = Sequence(
                self.track,
                Func(callback, *extraArgs),
            autoFinish=autoFinishTrack)
        self.track.start(ts)
        self.setActiveShadow(0)

    def finishDied(self, callback = None, extraArgs=[]):
        if self.track is not None:
            self.ignore(self.track.getName())
            self.track.finish()
            DelayDelete.cleanupDelayDeletes(self.track)
            self.track = None
        if hasattr(self, 'animFSM'):
            self.animFSM.request('TeleportedOut')
        if callback:
            callback(*extraArgs)

    def exitDied(self):
        if self.track is not None:
            self.ignore(self.track.getName())
            self.track.finish()
            DelayDelete.cleanupDelayDeletes(self.track)
            self.track = None
        # TODO: Enable Toon emotes.
        self.show()

    def enterSitStart(self, animMultiplier=1, ts=0, callback=None,
                      extraArgs=[]):
        # TODO: Disable Toon emotes.
        self.playingAnim = 'sit-start'
        self.track = Sequence(ActorInterval(self, 'sit-start'))
        self.track.start(ts)
        self.setActiveShadow(0)

    def exitSitStart(self):
        self.playingAnim = 'neutral'
        if self.track is not None:
            self.track.finish()
            DelayDelete.cleanupDelayDeletes(self.track)
            self.track = None
        # TODO: Enable Toon emotes.

    def enterSit(self, animMultiplier=1, ts=0, callback=None, extraArgs=[]):
        # TODO: Disable Toon emotes.
        self.playingAnim = 'sit'
        self.loop('sit')
        self.setActiveShadow(0)

    def exitSit(self):
        self.playingAnim = 'neutral'
        # TODO: Enable Toon emotes.

    def enterSleep(self, animMultiplier=1, ts=0, callback=None, extraArgs=[]):
        self.stopLookAround()
        self.stopBlink()
        self.closeEyes()
        self.lerpLookAt(Point3(0, 1, -4))
        self.loop('neutral')
        self.setPlayRate(animMultiplier * 0.4, 'neutral')
        # TODO: Display L10N.ToonSleepString in chat.
        if self.isLocal():
            # TODO: Add AFK timeout.
            pass
        self.setActiveShadow(0)

    def exitSleep(self):
        # TODO: Remove AFK timeout.
        self.startLookAround()
        self.openEyes()
        self.startBlink()
        # TODO: Clear display chat if necessary.
        self.lerpLookAt(Point3(0, 1, 0), time=0.25)
        self.stop()

    def enterPush(self, animMultiplier=1, ts=0, callback=None, extraArgs=[]):
        # TODO: Disable Toon emotes.
        self.playingAnim = 'push'
        self.track = Sequence(ActorInterval(self, 'push'))
        self.track.loop()
        self.setActiveShadow(1)

    def exitPush(self):
        self.playingAnim = 'neutral'
        if self.track is not None:
            self.track.finish()
            DelayDelete.cleanupDelayDeletes(self.track)
            self.track = None
        # TODO: Enable Toon emotes.

    def enterEmote(self, animMultiplier=1, ts=0, callback=None, extraArgs=[]):
        if not extraArgs:
            return None
        emoteIndex = extraArgs[0]
        self.playingAnim = None
        self.playingRate = None
        self.standWalkRunReverse = (
            ('neutral', 1.0), ('walk', 1.0), ('run', 1.0), ('walk', -1.0)
        )
        self.setSpeed(self.forwardSpeed, self.rotateSpeed)
        # TODO: Finish the Toon emote code.
        self.setActiveShadow(1)

    def doEmote(self, emoteIndex, animMultiplier=1, ts=0, callback=None,
                extraArgs=[]):
        if not self.isLocal():
            # TODO: Exit the function if this Toon is ignored.
            pass
        if self.isLocal():
            self.wakeUp()
            if self.hasTrackAnimToSpeed():
                self.trackAnimToSpeed(None)
        # TODO: Finish the Toon emote code.

    def __returnToLastAnim(self, task):
        if self.playingAnim:
            self.loop(self.playingAnim)
        elif self.hp > 0:
            self.loop('neutral')
        else:
            self.loop('sad-neutral')
        return Task.done

    def __finishEmote(self, task):
        if self.isLocal():
            if self.hp > 0:
                self.b_setAnimState('Happy')
            else:
                self.b_setAnimState('Sad')
        return Task.done

    def exitEmote(self):
        self.stop()
        if self.emoteTrack is not None:
            self.emoteTrack.finish()
            self.emoteTrack = None
        taskMgr.remove(self.taskName('finishEmote'))

    def enterSquish(self, animMultiplier=1, ts=0, callback=None, extraArgs=[]):
        # TODO: Disable Toon emotes.
        sound = loader.loadSfx('phase_9/audio/sfx/toon_decompress.mp3')
        lerpTime = 0.1
        node = self.getGeomNode().getChild(0)
        origScale = node.getScale()
        self.track = Sequence(
            LerpScaleInterval(
                node, lerpTime, VBase3(2, 2, 0.025), blendType='easeInOut'
            ),
            Wait(1.0),
            Parallel(
                Sequence(
                    Wait(0.4),
                    LerpScaleInterval(
                        node, lerpTime, VBase3(1.4, 1.4, 1.4),
                        blendType='easeInOut'
                    ),
                    LerpScaleInterval(
                        node, lerpTime/2.0, VBase3(0.8, 0.8, 0.8),
                        blendType='easeInOut'
                    ),
                    LerpScaleInterval(node, lerpTime/3.0, origScale,
                                      blendType='easeInOut'
                    )
                ),
                ActorInterval(self, 'jump', startTime=0.2),
                SoundInterval(sound)
            )
        )
        self.track.start(ts)
        self.setActiveShadow(1)

    def exitSquish(self):
        self.playingAnim = 'neutral'
        if self.track is not None:
            self.track.finish()
            DelayDelete.cleanupDelayDeletes(self.track)
            self.track = None
        # TODO: Enable Toon emotes.

    def enterFallDown(self, animMultiplier=1, ts=0, callback=None,
                      extraArgs=[]):
        self.playingAnim = 'fallDown'
        # TODO: Disable Toon emotes.
        self.track = Sequence(
            ActorInterval(self, 'slip-backward'),
        name='fallTrack')
        if callback:
            self.track.setDoneEvent(self.track.getName())
            self.acceptOnce(self.track.getName(), callback, extraArgs)
        self.track.start(ts)

    def exitFallDown(self):
        self.playingAnim = 'neutral'
        if self.track != None:
            self.ignore(self.track.getName())
            self.track.finish()
            DelayDelete.cleanupDelayDeletes(self.track)
            self.track = None
        # TODO: Enable Toon emotes.

    def enterGolfPuttLoop(self, animMultiplier=1, ts=0, callback=None,
                          extraArgs=[]):
        self.loop('loop-putt')

    def exitGolfPuttLoop(self):
        self.stop()

    def enterGolfRotateLeft(self, animMultiplier=1, ts=0, callback=None,
                            extraArgs=[]):
        self.loop('rotateL-putt')

    def exitGolfRotateLeft(self):
        self.stop()

    def enterGolfRotateRight(self, animMultiplier=1, ts=0, callback=None,
                             extraArgs=[]):
        self.loop('rotateR-putt')

    def exitGolfRotateRight(self):
        self.stop()

    def enterGolfPuttSwing(self, animMultiplier=1, ts=0, callback=None,
                           extraArgs=[]):
        self.loop('swing-putt')

    def exitGolfPuttSwing(self):
        self.stop()

    def enterGolfGoodPutt(self, animMultiplier=1, ts=0, callback=None,
                          extraArgs=[]):
        self.loop('good-putt', restart=0)

    def exitGolfGoodPutt(self):
        self.stop()

    def enterGolfBadPutt(self, animMultiplier=1, ts=0, callback=None,
                         extraArgs=[]):
        self.loop('badloop-putt', restart=0)

    def exitGolfBadPutt(self):
        self.stop()

    def enterFlattened(self, animMultiplier=1, ts=0, callback=None,
                       extraArgs=[]):
        # TODO: Disable Toon emotes.
        lerpTime = 0.1
        node = self.getGeomNode().getChild(0)
        self.origScale = node.getScale()
        self.track = Sequence(
            LerpScaleInterval(node, lerpTime, VBase3(2, 2, 0.025),
                              blendType='easeInOut')
        )
        self.track.start(ts)
        self.setActiveShadow(1)

    def exitFlattened(self):
        self.playingAnim = 'neutral'
        if self.track is not None:
            self.track.finish()
            DelayDelete.cleanupDelayDeletes(self.track)
            self.track = None
        node = self.getGeomNode().getChild(0)
        node.setScale(self.origScale)
        # TODO: Enable Toon emotes.

    def enterCogThiefRunning(self, animMultiplier=1, ts=0, callback=None,
                             extraArgs=[]):
        self.playingAnim = None
        self.playingRate = None
        self.standWalkRunReverse = (
            ('neutral', 1.0), ('run', 1.0), ('run', 1.0), ('run', -1.0)
        )
        self.setSpeed(self.forwardSpeed, self.rotateSpeed)
        self.setActiveShadow(1)

    def exitCogThiefRunning(self):
        self.standWalkRunReverse = None
        self.stop()
        self.motion.exit()

    def enterScientistJealous(self, animMultiplier=1, ts=0, callback=None,
                              extraArgs=[]):
        self.loop('scientistJealous')
        if hasattr(self, 'showScientistProp'):
            self.showScientistProp()

    def exitScientistJealous(self):
        self.stop()

    def enterScientistEmcee(self, animMultiplier=1, ts=0, callback=None,
                            extraArgs=[]):
        self.loop('scientistEmcee')

    def exitScientistEmcee(self):
        self.stop()

    def enterScientistWork(self, animMultiplier=1, ts=0, callback=None,
                           extraArgs=[]):
        self.loop('scientistWork')

    def exitScientistWork(self):
        self.stop()

    def enterScientistLessWork(self, animMultiplier=1, ts=0, callback=None,
                               extraArgs=[]):
        self.loop('scientistWork', fromFrame=319, toFrame=619)

    def exitScientistLessWork(self):
        self.stop()

    def enterScientistPlay(self, animMultiplier=1, ts=0, callback=None,
                           extraArgs=[]):
        self.loop('scientistGame')
        if hasattr(self, 'scientistPlay'):
            self.scientistPlay()

    def exitScientistPlay(self):
        self.stop()

    def startQuestMap(self):
        return None # virtual function.

    def stopQuestMap(self):
        return None # virtual function.

    def getPieces(self, *pieces):
        results = []
        for lodName in self.getLODNames():
            for partName, pieceNames in pieces:
                part = self.getPart(partName, lodName)
                if part:
                    if type(pieceNames) == types.StringType:
                        pieceNames = (pieceNames,)
                    for pieceName in pieceNames:
                        npc = part.findAllMatches('**/%s;+s' % pieceName)
                        for i in range(npc.getNumPaths()):
                            results.append(npc[i])
        return results

    def setPartsAdd(self, parts):
        for thingIndex in range(0, parts.getNumPaths()):
            thing = parts[thingIndex]
            if thing.getName() not in ('joint_attachMeter', 'joint_nameTag'):
                thing.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MAdd))
                thing.setDepthWrite(False)
                self.setBin('fixed', 1)

    def setPartsNormal(self, parts, alpha=0):
        for thingIndex in range(0, parts.getNumPaths()):
            thing = parts[thingIndex]
            if thing.getName() not in ('joint_attachMeter', 'joint_nameTag'):
                thing.setAttrib(ColorBlendAttrib.make(ColorBlendAttrib.MNone))
                thing.setDepthWrite(True)
                self.setBin('default', 0)
                if alpha:
                    thing.setTransparency(1)
                    thing.setBin('transparent', 0)

    def __doToonGhostColorScale(self, scale, lerpTime, keepDefault=0):
        if keepDefault:
            self.defaultColorScale = scale
        if scale is None:
            scale = VBase4(1, 1, 1, 1)
        node = self.getGeomNode()
        caps = self.getPieces(('torso', 'torso-bot-cap'))
        track = Sequence()
        track.append(Func(node.setTransparency, 1))
        track.append(ShowInterval(node))
        if scale[3] is not 1:
            for cap in caps:
                track.append(HideInterval(cap))
        track.append(
            LerpColorScaleInterval(node, lerpTime, scale,
                                   blendType='easeInOut')
        )
        if scale[3] is 1:
            track.append(Func(node.clearTransparency))
            for cap in caps:
                track.append(ShowInterval(cap))
        elif scale[3] is 0:
            track.append(Func(node.clearTransparency))
            track.append(HideInterval(node))
        return track

    def placeTag(self, name):
        # TODO: Remove this, and add support for future-style nametags.
        tag = OnscreenText(
            scale=0.38, text=name, bg=(0.8, 0.8, 0.8, 0.5),
            fg=(0.285156, 0.328125, 0.726562, 1.0), decal=True
        )
        tag.wrtReparentTo(self.find('**/def_head'))
        tag.setBillboardPointEye()
        tag.setDepthTest(True)
        tag.setDepthWrite(True)
        tag.setZ(tag, self.find('**/__Actor_head').getZ(self) - 0.6)
        tag.setFont(BTFont)
        tag.setAlign(TextNode.ACenter)
        tag.setSz(0.7)
        tag.setSx(0.8)
        tag.setWordwrap(8.0)
        self.tag = tag
        dummy = self.attachNewNode('dummy')
        z = map(Point3.getZ, self.getTightBounds())
        z = z[1] - z[0]
        dummy.setPos(0.2, 0, z+1.5)
        self.tag.reparentTo(dummy)

    def anim(self, name, playRate=1, loop=True):
        self.stop()
        self.setPlayRate(playRate, name)
        if loop:
            self.loop(name)
        else:
            self.play(name)