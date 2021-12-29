from direct.directnotify import DirectNotifyGlobal
from direct.gui.DirectGui import *
from direct.gui.OnscreenText import ScreenPrompt
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *
import random

from tth.avatar import NamePattern
from tth.avatar import Toon, ToonDNA
from tth.avatar import ToonGlobals
from tth.avatar.loader import saveNewToon
from tth.gui import UnicodeText

# Create-A-Toon Stage IDs:
GenderShop = 0
BodyShop = 1
ColorShop = 2
ClothingShop = 3
NameShop = 4
InitialStage = GenderShop
FinalStage = NameShop

# Directions for the Toon walk transition:
FORWARD = 1
BACK = -1

CATToonScale = Point3(1, 1, 1)
CATToonRotateMult = -2
CATTitleColor = VBase4(1, 0.8, 0, 1)
CATTitleFont = loader.loadFont('phase_3/models/fonts/MickeyFont.bam')
CATTitlePosition = Point3(0, 0, 0.825)
CATTitleScale = Point3(0.2, 1, 0.15)
CATNextButtonPosition = Point3(1.1, 0, -0.85)
CATNextButtonScale = Point3(0.3, 0.3, 0.3)
CATBackButtonPosition = Point3(0.8, 0, -0.85)
CATBackButtonScale = Point3(0.3, 0.3, 0.3)
CATCloseButtonPosition = Point3(-1.2, 0, -0.85)
CATCloseButtonScale = Point3(0.5, 0.5, 0.5)
CATRoomNodePaths = ('', 'drafting_table', 'easel', 'sewing_machine', '')
CATRoomTitles = map(L10N,
    (
        'CAT_TITLE_GENDER', 'CAT_TITLE_SPECIES', 'CAT_TITLE_COLOR',
        'CAT_TITLE_CLOTHES', 'CAT_TITLE_NAME'
    )
)
CATToonSpecies = map(L10N,
    (
        'SPC_DOG', 'SPC_CAT', 'SPC_HORSE', 'SPC_MOUSE', 'SPC_RABBIT',
        'SPC_DUCK', 'SPC_MONKEY', 'SPC_BEAR', 'SPC_PIG'
    )
)
CATWallColors = (
    VBase4(0.5, 0.3, 0.2, 1), VBase4(0, 0.6, 0.6, 1), VBase4(0.7, 0, 0.2, 1),
    VBase4(0, 0.7, 0.5, 1), VBase4(0.6, 0.7, 0.2, 1)
)
CATToonLandingPositions = (
    (Point3(0, 0, 0), Vec3(0, 0, 0)), (Point3(0, 0, 0), Vec3(0, 0, 0)),
    (Point3(0, 0, 0), Vec3(0, 0, 0)), (Point3(0, 0, 0), Vec3(0, 0, 0)),
    (Point3(-4, 0, 0), Vec3(-20, 0, 0))
)
CATCameraPosition = (Point3(0.75, -17.793, 4), Vec3(0, 0, 0))

class CreateAToon:

    notify = DirectNotifyGlobal.directNotify.newCategory('CreateAToon')

    def __tth_area__(self):
        return None

    def __init__(self, args, tp=None):
        gamebase.curArea = self
        self.slot = args[0]
        self.currentStage = None
        self.toonWalkTrack = None
        self.toon = None
        self.namePattern = NamePattern.NamePattern()
        self.load()
        self.enterStage(InitialStage)
        if tp is not None:
            tp.done()

    def load(self):
        self.backgroundMusic = loader.loadMusic(
            'phase_3/audio/bgm/create_a_toon.mid')
        self.backgroundMusic.setLoop(1)
        self.backgroundMusic.play()

        self.np = render.attachNewNode('CreateAToonSet')
        self.toonNp = self.np.attachNewNode('Toon')
        self.toonNp.setPos(CATCameraPosition[0].getX(), 0, 0)
        self.toonNp.setH(CATCameraPosition[1].getX() + 180)
        self.createAToonModel = loader.loadModel(
            'phase_3/models/gui/create_a_toon.bam')
        self.floor = self.createAToonModel.find('**/floor').copyTo(self.np)
        self.wall = self.createAToonModel.find('**/wall_floor').copyTo(self.np)
        self.stool = self.createAToonModel.find('**/stool').copyTo(self.np)
        self.stage = None

        self.parentFrame = DirectFrame(parent=base.a2dBackground)
        self.stageFrame = DirectFrame(parent=base.a2dBackground)

        self.title = TextNode('CreateAToonTitle')
        self.title.setTextColor(CATTitleColor)
        self.title.setFont(CATTitleFont)
        self.title.setAlign(TextNode.ACenter)
        self.titleNp = self.parentFrame.attachNewNode(self.title)
        self.titleNp.setPos(CATTitlePosition)
        self.titleNp.setScale(CATTitleScale)

        self.mainGui = loader.loadModel(
            'phase_3/models/gui/tt_m_gui_mat_mainGui.bam')
        self.nameShopGui = loader.loadModel(
            'phase_3/models/gui/tt_m_gui_mat_nameShop.bam')
        nextUp = self.mainGui.find('**/*nextUp')
        nextDown = self.mainGui.find('**/*nextDown')
        nextDisabled = self.mainGui.find('**/*nextDisabled')
        closeUp = self.mainGui.find('**/*closeUp')
        closeDown = self.mainGui.find('**/*closeDown')
        self.nextButton = DirectButton(
            parent=self.parentFrame, pos=CATNextButtonPosition,
            scale=CATNextButtonScale, text='', relief=None,
            geom=(nextUp, nextDown, nextUp, nextDisabled),
            command=lambda: self.enterStage(self.currentStage + 1),
            clickSound=gamebase.sounds['GUI_click'],
            rolloverSound=gamebase.sounds['GUI_rollover']
        )
        self.backButton = DirectButton(
            parent=self.parentFrame, pos=CATBackButtonPosition,
            hpr=(180, 0, 0), scale=CATBackButtonScale, text='', relief=None,
            geom=(nextUp, nextDown, nextUp, nextDisabled),
            command=lambda: self.enterStage(self.currentStage - 1),
            clickSound=gamebase.sounds['GUI_click'],
            rolloverSound=gamebase.sounds['GUI_rollover']
        )
        self.closeButton = DirectButton(
            parent=self.parentFrame, pos=CATCloseButtonPosition,
            scale=CATCloseButtonScale, text='', relief=None,
            geom=(closeUp, closeDown, closeUp, closeUp),
            command=self.leave, clickSound=gamebase.sounds['GUI_click'],
            rolloverSound=gamebase.sounds['GUI_rollover']
        )
        self.__loadRotationGUI()
        self.__loadShuffleGUI()
        self.__loadGenderShopGUI()
        self.__loadBodyShopGUI()
        self.__loadColorShopGUI()
        self.__loadClothingShopGUI()
        self.__loadNameShopGUI()

        self.shuffleShowLerp = None

        base.cam.setPos(CATCameraPosition[0])
        base.cam.setHpr(CATCameraPosition[1])

        self.globalGUI = loader.loadModel('phase_0/models/makeatoon/gui2.egg')
        self.globalGUI.find('**/body').setTexture('phase_0/maps/makeatoon')


    def dismiss(self):
        if self.toonWalkTrack:
            self.toonWalkTrack.finish()
            self.toonWalkTrack = None
        self.np.removeNode()
        if self.stageFrame:
            self.stageFrame.removeNode()
        if self.shuffleShowLerp:
            self.shuffleShowLerp.finish()
            self.shuffleShowLerp = None
        self.createAToonModel.removeNode()
        self.parentFrame.removeNode()
        self.mainGui.removeNode()
        self.nameShopGui.removeNode()
        self.backgroundMusic.stop()

    def leave(self):
        gamebase.curArea = None
        gamebase.themeMusic = loader.loadMusic(
            'phase_3/audio/bgm/tt_theme.mid')
        gamebase.themeMusic.setLoop(1)
        base.transitions.fadeIn()
        gamebase.themeMusic.play()
        messenger.send('load-chooseatoon-screen')
        self.dismiss()

    def finalize(self):
        dna = ToonDNA.ToonDNA(netString=self.toon.style.makeNetString())
        saveNewToon(
            *map(str, [
                self.slot, self.names[0], dna.makeNetString(),
                '', ''
                ]
            )
        )
        base.transitions.fadeIn()
        messenger.send('end-createatoon')
        self.dismiss()

    def enterStage(self, stage):
        if self.currentStage == FinalStage:
            # Since we were in the final stage, we must remove the "OK" button
            # that was created, and replace the "next" button, as we are moving
            # to a previous stage:
            self.okButton.removeNode()
            nextUp = self.mainGui.find('**/*nextUp')
            nextDown = self.mainGui.find('**/*nextDown')
            nextDisabled = self.mainGui.find('**/*nextDisabled')
            self.nextButton = DirectButton(
                parent=self.parentFrame, pos=CATNextButtonPosition,
                scale=CATNextButtonScale, text='', relief=None,
                geom=(nextUp, nextDown, nextUp, nextDisabled),
                command=lambda: self.enterStage(self.currentStage + 1),
                clickSound=gamebase.sounds['GUI_click'],
                rolloverSound=gamebase.sounds['GUI_rollover']
            )
        # Store the old stage so that we can specify which stage we are coming
        # FROM to playWalkTransition():
        oldStage = self.currentStage
        self.currentStage = stage
        if not self.toon:
            self.createStage()
            self.showStageGUI()
        else:
            direction = FORWARD if stage > oldStage else BACK
            self.playWalkTransition(oldStage, stage, direction)

    def playWalkTransition(self, fromStage, toStage, direction=FORWARD):
        toonWalkSpeed = 1.25
        camXLimit = 8.0 # The Toon will be out of view at this X position.
        getWalkDuration = lambda x: toonWalkSpeed + (abs(x)/camXLimit)
        startX = CATToonLandingPositions[fromStage][0].getX()
        endX = CATToonLandingPositions[toStage][0].getX()
        walkDurationFrom = getWalkDuration(startX)
        walkDurationTo = getWalkDuration(endX)
        rotateDuration = 0.5

        def hideGUI():
            self.stageFrame.hide()
            if self.nextButton:
                self.nextButton.hide()
            self.backButton.hide()

        def showGUI():
            self.stageFrame.show()
            self.showStageGUI()
            if self.nextButton:
                self.nextButton.show()
            self.backButton.show()

        self.toonWalkTrack = Sequence(
            Func(hideGUI),
            Func(self.toon.loop, 'run'),
            self.toon.quatInterval(
                rotateDuration,
                hpr=Vec3(90 if direction == FORWARD else -90, 0, 0)
            ),
            self.toon.posInterval(
                walkDurationFrom,
                Point3(camXLimit if direction == BACK else -camXLimit, 0, 0)
            ),
            Func(self.createStage)
        )
        pos, hpr = CATToonLandingPositions[toStage]
        self.toonWalkTrack.append(
            self.toon.posInterval(
                walkDurationTo, pos,
                startPos=Point3(
                    -camXLimit if direction == BACK else camXLimit, 0, 0
                )
            )
        )
        self.toonWalkTrack.append(
            self.toon.quatInterval(rotateDuration, quat=hpr)
        )
        self.toonWalkTrack.append(Func(self.toon.loop, 'neutral', 0))
        self.toonWalkTrack.append(Func(showGUI))
        self.toonWalkTrack.start()

    def createStage(self):
        self.cleanUpStage()
        nodePath = CATRoomNodePaths[self.currentStage]
        self.notify.debug("Showing room nodePath: '%s'..." % nodePath)
        self.createAToonModel.find('**/%s' % nodePath).copyTo(self.stage)
        self.createStageTitle()
        self.wall.setColor(CATWallColors[self.currentStage])

    def cleanUpStage(self):
        if self.stage:
            self.stage.removeNode()
            self.stage = None
        self.stage = self.np.attachNewNode('CreateAToonStage')

    def createStageTitle(self):
        titleText = L10N('CAT_CHOOSE') + ' ' + CATRoomTitles[self.currentStage]
        self.title.setWtext(titleText)

    def rotateToonRightTask(self, task):
        self.toon.setH(self.toon.getH() - CATToonRotateMult)
        return task.cont

    def rotateToonLeftTask(self, task):
        self.toon.setH(self.toon.getH() + CATToonRotateMult)
        return task.cont

    def rotateToon(self, direction, event=None):
        if not taskMgr.getTasksNamed('rotateToonTask'):
            if direction == FORWARD:
                taskMgr.add(self.rotateToonRightTask, 'rotateToonTask')
            else:
                taskMgr.add(self.rotateToonLeftTask, 'rotateToonTask')

    def stopRotateToon(self, event=None):
        if taskMgr.getTasksNamed('rotateToonTask'):
            taskMgr.remove('rotateToonTask')

    def rebindShuffleGUI(self, shuffleFunc, historyDecFunc, historyIncFunc):
        # Because we only have one shuffle button, we must re-bind its
        # functions whenever we wish to use it.
        self.shuffleHistory = []
        self.shuffleHistoryPtr = 0
        self.maxShuffleHistory = 10
        self.shuffleBtn['command'] = shuffleFunc
        self.shuffleDecBtn['command'] = historyDecFunc
        self.shuffleIncBtn['command'] = historyIncFunc
        self.shuffleDecBtn.hide()
        self.shuffleIncBtn.hide()
        self.shuffleFrame.hide()
        self.updateShuffleArrows()

    def __shuffle(self, shuffleFunc):
        """
        This is a decorator to help create a shuffleFunc to pass to
        rebindShuffleGUI(). It handles most of the shuffle history, but a
        self.shuffleHistory.append() line must still be included.
        """
        def shuffle(self=self):
            shuffleFunc(self)
            if len(self.shuffleHistory) > self.maxShuffleHistory:
                self.shuffleHistory.pop(0)
            self.shuffleHistoryPtr = len(self.shuffleHistory) - 1
            if len(self.shuffleHistory) == 2:
                self.startShowShuffleLerp()
            self.updateShuffleArrows()
        return shuffle

    def __shuffleHistoryDec(self, historyDecFunc):
        """
        This is a decorator to help create a historyDecFunc to pass to
        rebindShuffleGUI(). It handles most of the shuffle history, but the
        decorated function must still fetch
        self.shuffleHistory[self.shuffleHistoryPtr] itself.
        """
        def shuffleHistoryDec(self=self):
            self.shuffleHistoryPtr -= 1
            if self.shuffleHistoryPtr < 0:
                self.shuffleHistoryPtr = 0
            self.updateShuffleArrows()
            historyDecFunc(self)
        return shuffleHistoryDec

    def __shuffleHistoryInc(self, historyIncFunc):
        """
        This is a decorator to help create a historyIncFunc to pass to
        rebindShuffleGUI(). It handles most of the shuffle history, but the
        decorated function must still fetch
        self.shuffleHistory[self.shuffleHistoryPtr] itself.
        """
        def shuffleHistoryInc(self=self):
            self.shuffleHistoryPtr += 1
            if self.shuffleHistoryPtr >= len(self.shuffleHistory):
                self.shuffleHistoryPtr = len(self.shuffleHistory) - 1
            self.updateShuffleArrows()
            historyIncFunc(self)
        return shuffleHistoryInc

    def updateShuffleArrows(self):
        if self.shuffleHistoryPtr == 0:
            self.shuffleDecBtn['state'] = DGG.DISABLED
        else:
            self.shuffleDecBtn['state'] = DGG.NORMAL
        if self.shuffleHistoryPtr >= (len(self.shuffleHistory) - 1):
            self.shuffleIncBtn['state'] = DGG.DISABLED
        else:
            self.shuffleIncBtn['state'] = DGG.NORMAL

    def startShowShuffleLerp(self):
        self.shuffleShowLerp = Sequence(
            Parallel(
                Func(self.shuffleFrame.show),
                Func(self.shuffleIncBtn.show),
                Func(self.shuffleDecBtn.show)
            ),
            Parallel(
                self.shuffleFrameShowLerp,
                self.shuffleIncBtnShowLerp,
                self.shuffleDecBtnShowLerp
            )
        )
        self.shuffleShowLerp.start()

    def setGender(self, gender):
        if self.toon:
            self.toon.stopBlink()
            self.toon.stopLookAroundNow()
            self.toon.delete()
        style = ToonDNA.ToonDNA()
        style.newToonRandom(gender=gender)
        self.toon = Toon.Toon()
        self.toon.setDNA(style)
        self.toon.useLOD(1000)
        self.toon.startBlink()
        self.toon.startLookAround()
        self.toon.reparentTo(self.toonNp)
        self.toon.setScale(CATToonScale)
        self.toon.loop('neutral')
        self.nextButton['state'] = DGG.NORMAL

    def getSpeciesName(self, animal):
        speciesIndex = ToonDNA.toonSpeciesNames.index(animal)
        return CATToonSpecies[speciesIndex]

    def getSpeciesStart(self):
        species = self.toon.style.head[0]
        if species in ToonDNA.toonSpeciesTypes:
            self.species = species
            return ToonDNA.toonSpeciesTypes.index(species)

    def getGenderColorList(self, gender):
        if gender == 'm':
            return ToonDNA.defaultBoyColorList
        else:
            return ToonDNA.defaultGirlColorList

    def updateScrollButtons(self, choice, length, start, lButton, rButton):
        if choice == ((start-1) % length):
            rButton['state'] = DGG.DISABLED
        elif choice != ((start-1) % length):
            rButton['state'] = DGG.NORMAL
        if choice == (start % length):
            lButton['state'] = DGG.DISABLED
        elif choice != (start % length):
            lButton['state'] = DGG.NORMAL
        if lButton['state'] == rButton['state'] == DGG.DISABLED:
            # Fix the buttons if they both get disabled:
            if choice == (start % length):
                lButton['state'] = DGG.DISABLED
                rButton['state'] = DGG.NORMAL
            elif choice == ((start-1) % length):
                lButton['state'] = DGG.NORMAL
                rButton['state'] = DGG.DISABLED
            else:
                lButton['state'] = DGG.NORMAL
                rButton['state'] = DGG.NORMAL

    def updateHead(self):
        self.updateScrollButtons(
            self.headChoice, len(self.headList), self.headStart,
            self.headLButton, self.headRButton
        )
        headIndex = ToonDNA.getHeadStartIndex(self.species) + self.headChoice
        newHead = ToonDNA.toonHeadTypes[headIndex]
        self.toon.style.head = newHead
        self.toon.swapToonHead(newHead)
        self.toon.loop('neutral', 0)
        self.toon.swapToonColor(self.toon.style)
        self.updateAccessories()

    def swapSpecies(self, offset):
        length = len(ToonDNA.toonSpeciesTypes)
        self.speciesChoice = (self.speciesChoice+offset) % length
        self.updateScrollButtons(
            self.speciesChoice, length, self.speciesStart, self.speciesLButton,
            self.speciesRButton
        )
        self.species = ToonDNA.toonSpeciesTypes[self.speciesChoice]
        self.headList = ToonDNA.getHeadList(self.species)
        maxHeadChoice = len(self.headList) - 1
        if self.headChoice > maxHeadChoice:
            self.headChoice = maxHeadChoice
        self.updateHead()
        speciesName = self.getSpeciesName(self.toon.style.getAnimal())
        self.speciesFrame['text'] = speciesName

    def swapHead(self, offset):
        self.headList = ToonDNA.getHeadList(self.species)
        length = len(self.headList)
        self.headChoice = (self.headChoice+offset) % length
        self.updateHead()

    def swapTorso(self, offset):
        torsoOffset = 0
        if self.toon.style.gender == 'm':
            length = len(ToonDNA.toonTorsoTypes[:3])
        else:
            length = len(ToonDNA.toonTorsoTypes[3:6])
            if self.toon.style.torso[1] == 'd':
                torsoOffset = 3
        self.torsoChoice = (self.torsoChoice+offset) % length
        self.updateScrollButtons(
            self.torsoChoice, length, self.torsoStart, self.torsoLButton,
            self.torsoRButton
        )
        torso = ToonDNA.toonTorsoTypes[torsoOffset+self.torsoChoice]
        self.toon.style.torso = torso
        self.toon.swapToonTorso(torso)
        self.toon.loop('neutral', 0)
        self.toon.swapToonColor(self.toon.style)
        self.updateAccessories()

    def swapLegs(self, offset):
        length = len(ToonDNA.toonLegTypes)
        self.legChoice = (self.legChoice+offset) % length
        self.updateScrollButtons(
            self.legChoice, length, self.legStart, self.legLButton,
            self.legRButton
        )
        newLeg = ToonDNA.toonLegTypes[self.legChoice]
        self.toon.style.legs = newLeg
        self.toon.swapToonLegs(newLeg)
        self.toon.loop('neutral', 0)
        self.toon.swapToonColor(self.toon.style)
        self.updateAccessories()

    def swapAllColor(self, offset):
        length = len(self.colorList)
        choice = (self.headChoice+offset) % length
        self.updateScrollButtons(
            choice, length, 0, self.toonColorLButton, self.toonColorRButton
        )
        self.swapHeadColor(offset)
        oldArmColorIndex = self.colorList.index(self.toon.style.armColor)
        oldLegColorIndex = self.colorList.index(self.toon.style.legColor)
        self.swapArmColor(choice - oldArmColorIndex)
        self.swapLegColor(choice - oldLegColorIndex)

    def swapHeadColor(self, offset):
        length = len(self.colorList)
        self.headChoice = (self.headChoice+offset) % length
        self.updateScrollButtons(
            self.headChoice, length, 0, self.headColorLButton,
            self.headColorRButton
        )
        newColor = self.colorList[self.headChoice]
        self.toon.style.headColor = newColor
        self.toon.swapToonColor(self.toon.style)

    def swapArmColor(self, offset):
        length = len(self.colorList)
        self.armChoice = (self.armChoice+offset) % length
        self.updateScrollButtons(
            self.armChoice, length, 0, self.torsoColorLButton,
            self.torsoColorRButton
        )
        newColor = self.colorList[self.armChoice]
        self.toon.style.armColor = newColor
        self.toon.swapToonColor(self.toon.style)

    def swapLegColor(self, offset):
        length = len(self.colorList)
        self.legChoice = (self.legChoice+offset) % length
        self.updateScrollButtons(
            self.legChoice, length, 0, self.legColorLButton,
            self.legColorRButton
        )
        newColor = self.colorList[self.legChoice]
        self.toon.style.legColor = newColor
        self.toon.swapToonColor(self.toon.style)

    def swapGloveColor(self, offset):
        length = len(ToonDNA.defaultGloveColorList)
        self.gloveChoice = (self.gloveChoice+offset) % length
        self.updateScrollButtons(
            self.gloveChoice, length, 0, self.gloveColorLButton,
            self.gloveColorRButton
        )
        newColor = ToonDNA.defaultGloveColorList[self.gloveChoice]
        self.toon.style.gloveColor = newColor
        self.toon.swapToonColor(self.toon.style)

    def swapTop(self, offset):
        length = len(self.tops)
        self.topChoice += offset
        if self.topChoice <= 0:
            self.topChoice = 0
        self.updateScrollButtons(
            self.topChoice, length, 0, self.topLButton, self.topRButton
        )
        if (self.topChoice >= len(self.tops)) or (
            len(self.tops[self.topChoice]) != 4):
            self.notify.warning('topChoice index is out of range!')
            return None
        self.toon.style.topTex = self.tops[self.topChoice][0]
        self.toon.style.topTexColor = self.tops[self.topChoice][1]
        self.toon.style.sleeveTex = self.tops[self.topChoice][2]
        self.toon.style.sleeveTexColor = self.tops[self.topChoice][3]
        if self.toon.generateToonClothes() == 1:
            self.toon.loop('neutral', 0)

    def swapBottom(self, offset):
        length = len(self.bottoms)
        self.bottomChoice += offset
        if self.bottomChoice <= 0:
            self.bottomChoice = 0
        self.updateScrollButtons(
            self.bottomChoice, length, 0, self.bottomLButton,
            self.bottomRButton
        )
        if (self.bottomChoice >= len(self.bottoms)) or (
            len(self.bottoms[self.bottomChoice]) != 2):
            self.notify.warning('bottomChoice index is out of range!')
            return None
        self.toon.style.botTex = self.bottoms[self.bottomChoice][0]
        self.toon.style.botTexColor = self.bottoms[self.bottomChoice][1]
        if self.toon.generateToonClothes() == 1:
            self.toon.loop('neutral', 0)

    def swapHat(self, offset):
        length = len(self.hats)
        self.hatChoice += offset
        if self.hatChoice <= 0:
            self.hatChoice = 0
        self.updateScrollButtons(
            self.hatChoice, length, 0, self.hatLButton,
            self.hatRButton
        )
        self.toon.setHat(*self.hats[self.hatChoice])

    def swapGlasses(self, offset):
        length = len(self.glasses)
        self.glassesChoice += offset
        if self.glassesChoice <= 0:
            self.glassesChoice = 0
        self.updateScrollButtons(
            self.glassesChoice, length, 0, self.glassesLButton,
            self.glassesRButton
        )
        self.toon.setGlasses(*self.glasses[self.glassesChoice])

    def swapBackpack(self, offset):
        length = len(self.backpacks)
        self.backpackChoice += offset
        if self.backpackChoice <= 0:
            self.backpackChoice = 0
        self.updateScrollButtons(
            self.backpackChoice, length, 0, self.backpackLButton,
            self.backpackRButton
        )
        self.toon.setBackpack(*self.backpacks[self.backpackChoice])

    def swapShoes(self, offset):
        length = len(self.shoes)
        self.shoesChoice += offset
        if self.shoesChoice <= 0:
            self.shoesChoice = 0
        self.updateScrollButtons(
            self.shoesChoice, length, 0, self.shoesLButton,
            self.shoesRButton
        )
        self.toon.setShoes(*self.shoes[self.shoesChoice])

    def updateAccessories(self):
        self.toon.setHat(*self.toon.getHat())
        self.toon.setGlasses(*self.toon.getGlasses())
        self.toon.setBackpack(*self.toon.getBackpack())
        self.toon.setShoes(*self.toon.getShoes())

    def approvalAction(self):
        print 'Coming soon...'

    def enterTypeAName(self):
        print 'Coming soon...'

    def enterTypedName(self, *args):
        print 'Coming soon...'

    def generateName(self):
        gender = self.toon.style.gender
        nameParts = self.namePattern.generateRandomToonName(gender)
        self.updatePickAName(nameParts)

    def updatePickAName(self, nameParts):
        gender = self.toon.style.gender
        self.names[0] = self.namePattern.getNameString(gender, nameParts)
        names = self.namePattern.getStringParts(gender, nameParts)
        self.titleActive = 0
        self.firstActive = 0
        self.lastActive = 0
        if nameParts[0]:
            self.titleActive = 1
        if nameParts[1]:
            self.firstActive = 1
        if nameParts[2] and nameParts[3]:
            self.lastActive = 1
        if self.titleActive:
            self.titleIndex = nameParts[0]
            self.nameIndices[0] = self.namePattern.getNameId('title', names[0])
            self.nameFlags[0] = 1
        if self.firstActive:
            self.firstIndex = nameParts[1]
            self.nameIndices[1] = self.namePattern.getNameId('first', names[1])
            self.nameFlags[1] = 1
        if self.lastActive:
            self.prefixIndex = nameParts[2]
            self.suffixIndex = nameParts[3]
            self.nameIndices[2] = self.namePattern.getNameId('last-prefix', names[2])
            self.nameIndices[3] = self.namePattern.getNameId('last-suffix', names[3])
            if names[2] in self.namePattern.nameDict[NamePattern.CAP_PREFIX]:
                self.nameFlags[3] = 1
            else:
                self.nameFlags[3] = 0
        self.updateCheckBoxes()
        self.updateLists()
        self.listsChanged()
        self.nameResult['text'] = self.names[0]

    def makeNameLabel(self, te, index, others):
        alig = others[0]
        listName = others[1]
        if alig == TextNode.ARight:
            newpos = (0.44, 0, 0)
        elif alig == TextNode.ALeft:
            newpos = (0, 0, 0)
        else:
            newpos = (0.2, 0, 0)
        df = DirectFrame(
            state='normal', relief=None, text=te, text_scale=0.1,
            text_pos=newpos, text_align=alig, textMayChange=0
        )
        df.bind(
            DGG.B1PRESS, lambda x, df = df: self.nameClickedOn(listName, index)
        )
        return df

    def makeScrollList(self, gui, ipos, mcolor, nitems, nitemMakeFunction,
                       nitemMakeExtraArgs):
        it = nitems[:]
        ds = DirectScrolledList(
            items=it, itemMakeFunction=nitemMakeFunction,
            itemMakeExtraArgs=nitemMakeExtraArgs, parent=self.stageFrame,
            relief=None, command=self.listsChanged, pos=ipos, scale=0.6,
            incButton_image=(self.arrowUp, self.arrowDown, self.arrowHover,
                             self.arrowUp),
            incButton_relief=None, incButton_scale=(1.2, 1.2, -1.2),
            incButton_pos=(0.0189, 0, -0.5335), incButton_image0_color=mcolor,
            incButton_image1_color=mcolor, incButton_image2_color=mcolor,
            incButton_image3_color=Vec4(1, 1, 1, 0), decButton_image=(
                self.arrowUp, self.arrowDown, self.arrowHover, self.arrowUp),
            decButton_relief=None, decButton_scale=(1.2, 1.2, 1.2),
            decButton_pos=(0.0195, 0, 0.1779), decButton_image0_color=mcolor,
            decButton_image1_color=mcolor, decButton_image2_color=mcolor,
            decButton_image3_color=Vec4(1, 1, 1, 0),
            itemFrame_pos=(-0.2, 0, 0.028), itemFrame_scale=1.0,
            itemFrame_relief=DGG.RAISED,
            itemFrame_frameSize=(-0.07, 0.5, -0.52, 0.12),
            itemFrame_frameColor=mcolor, itemFrame_borderWidth=(0.01, 0.01),
            numItemsVisible=5, forceHeight=0.1
        )
        return ds

    def makeHighlight(self, npos):
        return DirectFrame(
            parent=self.stageFrame, relief='flat', scale=(0.552, 0, 0.11),
            state='disabled', frameSize=(-0.07,  0.52, -0.5, 0.1),
            borderWidth=(0.01, 0.01), pos=npos, frameColor=(1, 0, 1, 0.4)
        )

    def makeCheckBox(self, npos, ntex, ntexcolor, comm):
        return DirectCheckButton(
            parent=self.stageFrame, relief=None, scale=0.1, boxBorder=0.08,
            boxImage=self.circle, boxImageScale=4,
            boxImageColor=VBase4(0, 0.25, 0.5, 1), boxRelief=None, pos=npos,
            text=ntex, text_fg=ntexcolor,
            text_scale=0.8, text_pos=(0.2, 0),
            indicator_pos=(-0.566667, 0, -0.045),
            indicator_image_pos=(-0.26, 0, 0.075),
            command=comm, text_align=TextNode.ALeft
        )

    def restoreIndexes(self, oi):
        self.titleIndex = oi[0]
        self.firstIndex = oi[1]
        self.prefixIndex = oi[2]
        self.suffixIndex = oi[3]

    def updateLists(self):
        oldindex = [self.titleIndex, self.firstIndex, self.prefixIndex,
                    self.suffixIndex]
        self.titleScrollList.scrollTo(self.titleIndex - 2)
        self.restoreIndexes(oldindex)
        self.firstnameScrollList.scrollTo(self.firstIndex - 2)
        self.restoreIndexes(oldindex)
        self.lastprefixScrollList.scrollTo(self.prefixIndex - 2)
        self.restoreIndexes(oldindex)
        self.lastsuffixScrollList.scrollTo(self.suffixIndex - 2)
        self.restoreIndexes(oldindex)

    def showList(self, listToDo):
        listToDo.show()
        listToDo.decButton['state'] = 'normal'
        listToDo.incButton['state'] = 'normal'

    def hideList(self, listToDo):
        listToDo.decButton['state'] = 'disabled'
        listToDo.incButton['state'] = 'disabled'
        for item in listToDo['items']:
            if item.__class__.__name__ != 'str':
                item.hide()

    def listsChanged(self):
        if not self.listsLoaded:
            return None
        newname = ''
        if self.titleActive:
            self.showList(self.titleScrollList)
            self.titleHigh.show()
            titleItems = self.titleScrollList['items']
            newtitle = titleItems[self.titleScrollList.index + 2]['text']
            self.nameIndices[0] = self.namePattern.getNameId('title', newtitle)
            newname += newtitle + ' '
        else:
            self.nameIndices[0] = -1
            self.hideList(self.titleScrollList)
            self.titleHigh.hide()
        if self.firstActive:
            self.showList(self.firstnameScrollList)
            self.firstHigh.show()
            firstItems = self.firstnameScrollList['items']
            newfirst = firstItems[self.firstnameScrollList.index + 2]['text']
            self.nameIndices[1] = self.namePattern.getNameId('first', newfirst)
            newname += newfirst
            if self.lastActive:
                newname += ' '
        else:
            self.firstHigh.hide()
            self.hideList(self.firstnameScrollList)
            self.nameIndices[1] = -1
        if self.lastActive:
            self.showList(self.lastprefixScrollList)
            self.showList(self.lastsuffixScrollList)
            self.prefixHigh.show()
            self.suffixHigh.show()
            lpItems = self.lastprefixScrollList['items']
            lsItems = self.lastsuffixScrollList['items']
            lp = lpItems[self.lastprefixScrollList.index + 2]['text']
            ls = lsItems[self.lastsuffixScrollList.index + 2]['text']
            self.nameIndices[2] = self.namePattern.getNameId('last-prefix', lp)
            self.nameIndices[3] = self.namePattern.getNameId('last-suffix', ls)
            newname += lp
            if lp in self.namePattern.nameDict[NamePattern.CAP_PREFIX]:
                ls = ls.capitalize()
                self.nameFlags[3] = 1
            else:
                self.nameFlags[3] = 0
            newname += ls
        else:
            self.hideList(self.lastprefixScrollList)
            self.hideList(self.lastsuffixScrollList)
            self.prefixHigh.hide()
            self.suffixHigh.hide()
            self.nameIndices[2] = -1
            self.nameIndices[3] = -1
        self.titleIndex = self.titleScrollList.index + 2
        self.firstIndex = self.firstnameScrollList.index + 2
        self.prefixIndex = self.lastprefixScrollList.index + 2
        self.suffixIndex = self.lastsuffixScrollList.index + 2
        self.nameResult['text'] = newname
        self.names[0] = newname

    def nameClickedOn(self, listType, index):
        if listType == 'title':
            self.titleIndex = index
        elif listType == 'first':
            self.firstIndex = index
        elif listType == 'prefix':
            self.prefixIndex = index
        else:
            self.suffixIndex = index
        self.updateLists()
        self.listsChanged()

    def titleToggle(self, value):
        if not self.titleActive:
            self.titleActive = 1
            self.listsChanged()
            self.titleActive and self.titleScrollList.refresh()
        else:
            self.titleActive = 0
            self.listsChanged()
            self.titleActive and self.titleScrollList.refresh()
        self.updateCheckBoxes()

    def firstToggle(self, value):
        if not self.firstActive:
            self.firstActive = 1
            self.listsChanged()
            self.firstnameScrollList.refresh()
        elif self.lastActive:
            self.firstActive = 0
            self.listsChanged()
            self.firstnameScrollList.refresh()
        self.updateCheckBoxes()

    def lastToggle(self, value):
        if not self.lastActive:
            self.lastActive = 1
            self.listsChanged()
            self.lastprefixScrollList.refresh()
            self.lastsuffixScrollList.refresh()
        elif self.firstActive:
            self.lastActive = 0
            self.listsChanged()
            self.lastprefixScrollList.refresh()
            self.lastsuffixScrollList.refresh()
        self.updateCheckBoxes()

    def updateCheckBoxes(self):
        self.titleCheck['indicatorValue'] = self.titleActive
        self.titleCheck.setIndicatorValue()
        self.firstCheck['indicatorValue'] = self.firstActive
        self.firstCheck.setIndicatorValue()
        self.lastCheck['indicatorValue'] = self.lastActive
        self.lastCheck.setIndicatorValue()

    def showStageGUI(self):
        # First, hide any existing GUI that is parented to the stageFrame:
        self.hideRotationGUI()
        self.hideShuffleGUI()
        self.hideGenderShopGUI()
        self.hideBodyShopGUI()
        self.hideColorShopGUI()
        self.hideClothingShopGUI()
        self.hideNameShopGUI()

        # Then, show the GUI for the current stage:
        if self.currentStage == GenderShop:
            self.showGenderShopGUI()
        elif self.currentStage == BodyShop:
            self.showBodyShopGUI()
        elif self.currentStage == ColorShop:
            self.showColorShopGUI()
        elif self.currentStage == ClothingShop:
            self.showClothingShopGUI()
        elif self.currentStage == NameShop:
            self.showNameShopGUI()
        else:
            self.notify.error(
                'Failed to load Create-A-Toon GUI. Stage: {0}'.format(
                    self.currentStage
                )
            )

    def __loadRotationGUI(self):
        arrowRotateUp = self.mainGui.find('**/*arrowRotateUp')
        arrowRotateDown = self.mainGui.find('**/*arrowRotateDown')
        self.arrowRotateRight = DirectButton(
            parent=self.stageFrame, pos=(0.3, 0, -0.65), scale=0.5, text='',
            relief=None, geom=(arrowRotateUp, arrowRotateDown, arrowRotateUp,
                               arrowRotateUp),
            clickSound=gamebase.sounds['GUI_click'],
            rolloverSound=gamebase.sounds['GUI_rollover']
        )
        self.arrowRotateRight.bind(DGG.B1PRESS, self.rotateToon,
                                   extraArgs=[FORWARD])
        self.arrowRotateRight.bind(DGG.B1RELEASE, self.stopRotateToon)
        self.arrowRotateLeft = DirectButton(
            parent=self.stageFrame, pos=(-0.3, 0, -0.65), hpr=(-180, 0, 0),
            scale=0.5, text='', relief=None, geom=(arrowRotateUp,
                arrowRotateDown, arrowRotateUp, arrowRotateUp),
            clickSound=gamebase.sounds['GUI_click'],
            rolloverSound=gamebase.sounds['GUI_rollover']
        )
        self.arrowRotateLeft.bind(DGG.B1PRESS, self.rotateToon,
                                  extraArgs=[BACK])
        self.arrowRotateLeft.bind(DGG.B1RELEASE, self.stopRotateToon)
        self.hideRotationGUI()

    def hideRotationGUI(self):
        self.arrowRotateRight.hide()
        self.arrowRotateLeft.hide()

    def showRotationGUI(self):
        self.arrowRotateRight.show()
        self.arrowRotateLeft.show()

    def __loadShuffleGUI(self):
        shuffleFrame = self.mainGui.find('**/*shuffleFrame')
        shuffleUp = self.mainGui.find('**/*shuffleUp')
        shuffleDown = self.mainGui.find('**/*shuffleDown')
        shuffleArrowUp = self.mainGui.find('**/*shuffleArrowUp')
        shuffleArrowDown = self.mainGui.find('**/*shuffleArrowDown')
        shuffleArrowDisabled = self.mainGui.find('**/*shuffleArrowDisabled')
        self.shuffleParentFrame = DirectFrame(
            parent=self.stageFrame, relief=DGG.RAISED, frameColor=(1, 0, 0, 0)
        )
        self.shuffleFrame = DirectFrame(
            parent=self.shuffleParentFrame, image=shuffleFrame,
            image_scale=(-0.6, 0.6, 0.6), relief=None, frameColor=(1, 1, 1, 1)
        )
        self.shuffleFrame.hide()
        self.shuffleBtn = DirectButton(
            parent=self.shuffleParentFrame, relief=None,
            image=(shuffleUp, shuffleDown, shuffleUp),
            image_scale=(-0.6, 0.6, 0.6), image1_scale=(-0.63, 0.6, 0.6),
            image2_scale=(-0.63, 0.6, 0.6), text=L10N('CAT_SHUFFLE'),
            text_scale=0.08, text_pos=(0, -0.02), text_fg=(1, 1, 1, 1),
            text_shadow=(0, 0, 0, 1)
        )
        self.shuffleIncBtn = DirectButton(
            parent=self.shuffleParentFrame, relief=None, image=(shuffleArrowUp,
                shuffleArrowDown, shuffleArrowUp, shuffleArrowDisabled),
            image_scale=(-0.6, 0.6, 0.6), image1_scale=(-0.7, 0.7, 0.7),
            image2_scale=(-0.7, 0.7, 0.7), pos=(0.202, 0, 0)
        )
        self.shuffleIncBtn.hide()
        self.shuffleDecBtn = DirectButton(
            parent=self.shuffleParentFrame, relief=None, image=(shuffleArrowUp,
                shuffleArrowDown, shuffleArrowUp, shuffleArrowDisabled),
            image_scale=(0.6, 0.6, 0.6), image1_scale=(0.7, 0.7, 0.7),
            image2_scale=(0.7, 0.7, 0.7), pos=(-0.202, 0, 0)
        )
        self.shuffleDecBtn.hide()
        self.shuffleShowLerp = None
        self.shuffleFrameShowLerp = LerpColorInterval(
            self.shuffleFrame, 0.5, Vec4(1, 1, 1, 1), Vec4(1, 1, 1, 0)
        )
        self.shuffleIncBtnShowLerp = LerpColorInterval(
            self.shuffleIncBtn, 0.5, Vec4(1, 1, 1, 1), Vec4(1, 1, 1, 0)
        )
        self.shuffleDecBtnShowLerp = LerpColorInterval(
            self.shuffleDecBtn, 0.5, Vec4(1, 1, 1, 1), Vec4(1, 1, 1, 0)
        )
        self.hideShuffleGUI()

    def hideShuffleGUI(self):
        self.shuffleParentFrame.hide()

    def showShuffleGUI(self):
        self.shuffleParentFrame.show()

    def __loadGenderShopGUI(self):
        boyUp = self.mainGui.find('**/*boyUp')
        boyDown = self.mainGui.find('**/*boyDown')
        girlUp = self.mainGui.find('**/*girlUp')
        girlDown = self.mainGui.find('**/*girlDown')
        self.boyBtn = DirectButton(
            parent=self.stageFrame, pos=Vec3(-0.4, 0, -0.8), scale=0.5,
            text='', relief=None, geom=(boyUp, boyDown, boyUp, boyDown),
            command=self.setGender, extraArgs=['m'],
            clickSound=gamebase.sounds['GUI_click'],
            rolloverSound=gamebase.sounds['GUI_rollover']
        )
        self.girlBtn = DirectButton(
            parent=self.stageFrame, pos=Vec3(0.4, 0, -0.8), scale=0.5, text='',
            relief=None, geom=(girlUp, girlDown, girlUp, girlDown),
            command=self.setGender, extraArgs=['f'],
            clickSound=gamebase.sounds['GUI_click'],
            rolloverSound=gamebase.sounds['GUI_rollover']
        )
        self.boyText = OnscreenText(
            text=L10N('CAT_BOY'), parent=self.boyBtn,
            pos=(0, 0.3), fg=(1, 1, 1, 1), scale=0.15
        )
        self.boyText.hide()
        self.girlText = OnscreenText(
            text=L10N('CAT_GIRL'), parent=self.girlBtn,
            pos=(0, 0.3), fg=(1, 1, 1, 1), scale=0.15
        )
        self.girlText.hide()

        def boyIn(event=None):
            self.boyBtn.setScale(0.53)
            self.boyText.show()

        def boyOut(event=None):
            self.boyBtn.setScale(0.5)
            self.boyText.hide()

        def girlIn(event=None):
            self.girlBtn.setScale(0.53)
            self.girlText.show()

        def girlOut(event=None):
            self.girlBtn.setScale(0.5)
            self.girlText.hide()

        self.boyBtn.bind(DGG.WITHIN, boyIn)
        self.boyBtn.bind(DGG.WITHOUT, boyOut)
        self.girlBtn.bind(DGG.WITHIN, girlIn)
        self.girlBtn.bind(DGG.WITHOUT, girlOut)
        self.hideGenderShopGUI()

    def hideGenderShopGUI(self):
        self.boyBtn.hide()
        self.girlBtn.hide()

    def showGenderShopGUI(self):
        self.boyBtn.show()
        self.girlBtn.show()
        self.backButton['state'] = DGG.DISABLED
        if not self.toon:
            self.nextButton['state'] = DGG.DISABLED

    def __loadBodyShopGUI(self):
        shuffleFrame = self.mainGui.find('**/*shuffleFrame')
        shuffleArrowUp = self.mainGui.find('**/*shuffleArrowUp')
        shuffleArrowDown = self.mainGui.find('**/*shuffleArrowDown')
        shuffleArrowDisabled = self.mainGui.find('**/*shuffleArrowDisabled')

        # Toon Species
        self.speciesFrame = DirectFrame(
            parent=self.stageFrame, image=shuffleFrame,
            image_scale=(-0.6, 0.6, 0.6), relief=None, pos=(1, 0, 0.3),
            hpr=(0, 0, 0), scale=1.3, frameColor=(1, 1, 1, 1),
            text='', text_scale=0.0625, text_pos=(-0.001, -0.015),
            text_fg=(1, 1, 1, 1)
        )
        self.speciesLButton = DirectButton(
            parent=self.speciesFrame, relief=None, image=(shuffleArrowUp,
                shuffleArrowDown, shuffleArrowUp, shuffleArrowDisabled),
            image_scale=(0.6, 0.6, 0.6), image1_scale=(0.7, 0.7, 0.7),
            image2_scale=(0.7, 0.7, 0.7), pos=(-0.2, 0, 0),
            command=self.swapSpecies, extraArgs=[-1]
        )
        self.speciesRButton = DirectButton(
            parent=self.speciesFrame, relief=None, image=(shuffleArrowUp,
                shuffleArrowDown, shuffleArrowUp, shuffleArrowDisabled),
            image_scale=(-0.6, 0.6, 0.6), image1_scale=(-0.7, 0.7, 0.7),
            image2_scale=(-0.7, 0.7, 0.7), pos=(0.2, 0, 0),
            command=self.swapSpecies, extraArgs=[1]
        )

        # Toon Head
        self.headFrame = DirectFrame(
            parent=self.stageFrame, image=shuffleFrame,
            image_scale=(-0.6, 0.6, 0.6), relief=None, pos=(1, 0, 0.05),
            hpr=(0, 0, 2), scale=0.9, frameColor=(1, 1, 1, 1),
            text=L10N('CAT_HEAD'), text_scale=0.0625,
            text_pos=(-0.001, -0.015), text_fg=(1, 1, 1, 1)
        )
        self.headLButton = DirectButton(
            parent=self.headFrame, relief=None, image=(shuffleArrowUp,
                shuffleArrowDown, shuffleArrowUp, shuffleArrowDisabled),
            image_scale=(0.6, 0.6, 0.6), image1_scale=(0.7, 0.7, 0.7),
            image2_scale=(0.7, 0.7, 0.7), pos=(-0.2, 0, 0),
            command=self.swapHead, extraArgs=[-1]
        )
        self.headRButton = DirectButton(
            parent=self.headFrame, relief=None, image=(shuffleArrowUp,
                shuffleArrowDown, shuffleArrowUp, shuffleArrowDisabled),
            image_scale=(-0.6, 0.6, 0.6), image1_scale=(-0.7, 0.7, 0.7),
            image2_scale=(-0.7, 0.7, 0.7), pos=(0.2, 0, 0),
            command=self.swapHead, extraArgs=[1]
        )

        # Toon Torso
        self.bodyFrame = DirectFrame(
            parent=self.stageFrame, image=shuffleFrame,
            image_scale=(0.6, 0.6, 0.6), relief=None, pos=(1, 0, -0.15),
            hpr=(0, 0, -2), scale=0.9, frameColor=(1, 1, 1, 1),
            text=L10N('CAT_TORSO'), text_scale=0.0625,
            text_pos=(-0.001, -0.015), text_fg=(1, 1, 1, 1)
        )
        self.torsoLButton = DirectButton(
            parent=self.bodyFrame, relief=None, image=(shuffleArrowUp,
                shuffleArrowDown, shuffleArrowUp, shuffleArrowDisabled),
            image_scale=(0.6, 0.6, 0.6), image1_scale=(0.7, 0.7, 0.7),
            image2_scale=(0.7, 0.7, 0.7), pos=(-0.2, 0, 0),
            command=self.swapTorso, extraArgs=[-1]
        )
        self.torsoRButton = DirectButton(
            parent=self.bodyFrame, relief=None, image=(shuffleArrowUp,
                shuffleArrowDown, shuffleArrowUp, shuffleArrowDisabled),
            image_scale=(-0.6, 0.6, 0.6), image1_scale=(-0.7, 0.7, 0.7),
            image2_scale=(-0.7, 0.7, 0.7), pos=(0.2, 0, 0),
            command=self.swapTorso, extraArgs=[1]
        )

        # Toon Legs
        self.legsFrame = DirectFrame(
            parent=self.stageFrame, image=shuffleFrame,
            image_scale=(-0.6, 0.6, 0.6), relief=None, pos=(1, 0, -0.35),
            hpr=(0, 0, 3), scale=0.9, frameColor=(1, 1, 1, 1),
            text=L10N('CAT_LEGS'), text_scale=0.0625,
            text_pos=(-0.001, -0.015), text_fg=(1, 1, 1, 1)
        )
        self.legLButton = DirectButton(
            parent=self.legsFrame, relief=None, image=(shuffleArrowUp,
                shuffleArrowDown, shuffleArrowUp, shuffleArrowDisabled),
            image_scale=(0.6, 0.6, 0.6), image1_scale=(0.7, 0.7, 0.7),
            image2_scale=(0.7, 0.7, 0.7), pos=(-0.2, 0, 0),
            command=self.swapLegs, extraArgs=[-1]
        )
        self.legRButton = DirectButton(
            parent=self.legsFrame, relief=None, image=(shuffleArrowUp,
                shuffleArrowDown, shuffleArrowUp, shuffleArrowDisabled),
            image_scale=(-0.6, 0.6, 0.6), image1_scale=(-0.7, 0.7, 0.7),
            image2_scale=(-0.7, 0.7, 0.7), pos=(0.2, 0, 0),
            command=self.swapLegs, extraArgs=[1]
        )
        self.hideBodyShopGUI()

    def hideBodyShopGUI(self):
        self.speciesFrame.hide()
        self.headFrame.hide()
        self.bodyFrame.hide()
        self.legsFrame.hide()

    def showBodyShopGUI(self):
        self.backButton['state'] = DGG.NORMAL
        self.speciesFrame.show()
        self.headFrame.show()
        self.bodyFrame.show()
        self.legsFrame.show()
        self.showRotationGUI()
        self.showShuffleGUI()
        self.species = None
        self.speciesStart = self.getSpeciesStart()
        self.speciesChoice = self.speciesStart
        self.headStart = 0
        headIndex = ToonDNA.toonHeadTypes.index(self.toon.style.head)
        self.headChoice = headIndex - ToonDNA.getHeadStartIndex(self.species)
        self.torsoStart = 0
        self.torsoChoice = ToonDNA.toonTorsoTypes.index(
                              self.toon.style.torso) % 3
        self.legStart = 0
        self.legChoice = ToonDNA.toonLegTypes.index(self.toon.style.legs)
        if (self.toon.style.gender == 'm') or (
            ToonDNA.GirlBottoms[self.toon.style.botTex][1] == ToonDNA.SHORTS):
            torsoPool = ToonDNA.toonTorsoTypes[:3]
        else:
            torsoPool = ToonDNA.toonTorsoTypes[3:6]
        speciesName = self.getSpeciesName(self.toon.style.getAnimal())
        self.speciesFrame['text'] = speciesName

        @self.__shuffle
        def shuffleBodyParts(self=self):
            self.speciesChoice = random.randint(
                0, len(ToonDNA.toonSpeciesTypes) - 1)
            self.headChoice = random.randint(
                0, len(ToonDNA.toonHeadTypes) - 1)
            self.torsoChoice = random.randint(0, len(torsoPool) - 1)
            legPool = ToonDNA.toonLegTypes + ('m', 'l', 'l', 'l')
            self.legChoice = random.randint(0, len(legPool) - 1)
            self.swapSpecies(0)
            self.swapTorso(0)
            self.swapLegs(0)
            self.shuffleHistory.append(
                (self.speciesChoice, self.headChoice,
                 self.torsoChoice, self.legChoice)
            )

        @self.__shuffleHistoryInc
        def incBodyPartsHistory(self=self):
            (self.speciesChoice, self.headChoice, self.torsoChoice,
             self.legChoice) = self.shuffleHistory[self.shuffleHistoryPtr]
            self.swapSpecies(0)
            self.swapTorso(0)
            self.swapLegs(0)

        @self.__shuffleHistoryDec
        def decBodyPartsHistory(self=self):
            (self.speciesChoice, self.headChoice, self.torsoChoice,
             self.legChoice) = self.shuffleHistory[self.shuffleHistoryPtr]
            self.swapSpecies(0)
            self.swapTorso(0)
            self.swapLegs(0)

        self.rebindShuffleGUI(
            shuffleBodyParts, decBodyPartsHistory, incBodyPartsHistory
        )
        self.shuffleParentFrame.setPos(1, 0, -0.6)
        length = len(ToonDNA.toonSpeciesTypes)
        self.updateScrollButtons(
            self.speciesChoice, length, self.speciesStart, self.speciesLButton,
            self.speciesRButton
        )
        length = len(ToonDNA.getHeadList(self.species))
        self.updateScrollButtons(
            self.headChoice, length, self.headStart,
            self.headLButton, self.headRButton
        )
        if self.toon.style.gender == 'm':
            length = len(ToonDNA.toonTorsoTypes[:3])
        else:
            length = len(ToonDNA.toonTorsoTypes[3:6])
        self.updateScrollButtons(
            self.torsoChoice, length, self.torsoStart, self.torsoLButton,
            self.torsoRButton
        )
        length = len(ToonDNA.toonLegTypes)
        self.updateScrollButtons(
            self.legChoice, length, self.legStart, self.legLButton,
            self.legRButton
        )

    def __loadColorShopGUI(self):
        shuffleFrame = self.mainGui.find('**/*shuffleFrame')
        shuffleArrowUp = self.mainGui.find('**/*shuffleArrowUp')
        shuffleArrowDown = self.mainGui.find('**/*shuffleArrowDown')
        shuffleArrowDisabled = self.mainGui.find('**/*shuffleArrowDisabled')

        # Toon Color
        self.toonColorFrame = DirectFrame(
            parent=self.stageFrame, image=shuffleFrame,
            image_scale=(-0.6, 0.6, 0.6), relief=None, pos=(1, 0, 0.3),
            hpr=(0, 0, 0), scale=1.3, frameColor=(1, 1, 1, 1),
            text='Toon', text_scale=0.0625, text_pos=(-0.001, -0.015),
            text_fg=(1, 1, 1, 1)
        )
        self.toonColorLButton = DirectButton(
            parent=self.toonColorFrame, relief=None, image=(shuffleArrowUp,
                shuffleArrowDown, shuffleArrowUp, shuffleArrowDisabled),
            image_scale=(0.6, 0.6, 0.6), image1_scale=(0.7, 0.7, 0.7),
            image2_scale=(0.7, 0.7, 0.7), pos=(-0.2, 0, 0),
            command=self.swapAllColor, extraArgs=[-1]
        )
        self.toonColorRButton = DirectButton(
            parent=self.toonColorFrame, relief=None, image=(shuffleArrowUp,
                shuffleArrowDown, shuffleArrowUp, shuffleArrowDisabled),
            image_scale=(-0.6, 0.6, 0.6), image1_scale=(-0.7, 0.7, 0.7),
            image2_scale=(-0.7, 0.7, 0.7), pos=(0.2, 0, 0),
            command=self.swapAllColor, extraArgs=[1]
        )

        # Head Color
        self.headColorFrame = DirectFrame(
            parent=self.stageFrame, image=shuffleFrame,
            image_scale=(-0.6, 0.6, 0.6), relief=None, pos=(1, 0, 0.05),
            hpr=(0, 0, 2), scale=0.9, frameColor=(1, 1, 1, 1),
            text=L10N('CAT_HEAD'), text_scale=0.0625,
            text_pos=(-0.001, -0.015), text_fg=(1, 1, 1, 1)
        )
        self.headColorLButton = DirectButton(
            parent=self.headColorFrame, relief=None, image=(shuffleArrowUp,
                shuffleArrowDown, shuffleArrowUp, shuffleArrowDisabled),
            image_scale=(0.6, 0.6, 0.6), image1_scale=(0.7, 0.7, 0.7),
            image2_scale=(0.7, 0.7, 0.7), pos=(-0.2, 0, 0),
            command=self.swapHeadColor, extraArgs=[-1]
        )
        self.headColorRButton = DirectButton(
            parent=self.headColorFrame, relief=None, image=(shuffleArrowUp,
                shuffleArrowDown, shuffleArrowUp, shuffleArrowDisabled),
            image_scale=(-0.6, 0.6, 0.6), image1_scale=(-0.7, 0.7, 0.7),
            image2_scale=(-0.7, 0.7, 0.7), pos=(0.2, 0, 0),
            command=self.swapHeadColor, extraArgs=[1]
        )

        # Torso Color
        self.torsoColorFrame = DirectFrame(
            parent=self.stageFrame, image=shuffleFrame,
            image_scale=(0.6, 0.6, 0.6), relief=None, pos=(1, 0, -0.15),
            hpr=(0, 0, -2), scale=0.9, frameColor=(1, 1, 1, 1),
            text=L10N('CAT_TORSO'), text_scale=0.0625,
            text_pos=(-0.001, -0.015), text_fg=(1, 1, 1, 1)
        )
        self.torsoColorLButton = DirectButton(
            parent=self.torsoColorFrame, relief=None, image=(shuffleArrowUp,
                shuffleArrowDown, shuffleArrowUp, shuffleArrowDisabled),
            image_scale=(0.6, 0.6, 0.6), image1_scale=(0.7, 0.7, 0.7),
            image2_scale=(0.7, 0.7, 0.7), pos=(-0.2, 0, 0),
            command=self.swapArmColor, extraArgs=[-1]
        )
        self.torsoColorRButton = DirectButton(
            parent=self.torsoColorFrame, relief=None, image=(shuffleArrowUp,
                shuffleArrowDown, shuffleArrowUp, shuffleArrowDisabled),
            image_scale=(-0.6, 0.6, 0.6), image1_scale=(-0.7, 0.7, 0.7),
            image2_scale=(-0.7, 0.7, 0.7), pos=(0.2, 0, 0),
            command=self.swapArmColor, extraArgs=[1]
        )

        # Leg Color
        self.legColorFrame = DirectFrame(
            parent=self.stageFrame, image=shuffleFrame,
            image_scale=(0.6, 0.6, 0.6), relief=None, pos=(1, 0, -0.35),
            hpr=(0, 0, -2), scale=0.9, frameColor=(1, 1, 1, 1),
            text=L10N('CAT_LEGS'), text_scale=0.0625,
            text_pos=(-0.001, -0.015), text_fg=(1, 1, 1, 1)
        )
        self.legColorLButton = DirectButton(
            parent=self.legColorFrame, relief=None, image=(shuffleArrowUp,
                shuffleArrowDown, shuffleArrowUp, shuffleArrowDisabled),
            image_scale=(0.6, 0.6, 0.6), image1_scale=(0.7, 0.7, 0.7),
            image2_scale=(0.7, 0.7, 0.7), pos=(-0.2, 0, 0),
            command=self.swapLegColor, extraArgs=[-1]
        )
        self.legColorRButton = DirectButton(
            parent=self.legColorFrame, relief=None, image=(shuffleArrowUp,
                shuffleArrowDown, shuffleArrowUp, shuffleArrowDisabled),
            image_scale=(-0.6, 0.6, 0.6), image1_scale=(-0.7, 0.7, 0.7),
            image2_scale=(-0.7, 0.7, 0.7), pos=(0.2, 0, 0),
            command=self.swapLegColor, extraArgs=[1]
        )
        self.hideColorShopGUI()

    def hideColorShopGUI(self):
        self.toonColorFrame.hide()
        self.headColorFrame.hide()
        self.torsoColorFrame.hide()
        self.legColorFrame.hide()

    def showColorShopGUI(self):
        self.toonColorFrame.show()
        self.headColorFrame.show()
        self.torsoColorFrame.show()
        self.legColorFrame.show()
        self.showRotationGUI()
        self.showShuffleGUI()
        self.colorList = self.getGenderColorList(self.toon.style.gender)
        try:
            self.headChoice = self.colorList.index(self.toon.style.headColor)
            self.armChoice = self.colorList.index(self.toon.style.armColor)
            self.legChoice = self.colorList.index(self.toon.style.legColor)
        except:
            self.headChoice = 1
            self.armChoice = 1
            self.legChoice = 1

        @self.__shuffle
        def shuffleColors(self=self):
            self.headChoice = random.randint(0, len(self.colorList) - 1)
            self.armChoice = random.randint(0, len(self.colorList) - 1)
            self.legChoice = random.randint(0, len(self.colorList) - 1)
            self.swapHeadColor(0)
            self.swapArmColor(0)
            self.swapLegColor(0)
            self.shuffleHistory.append(
                (self.headChoice, self.armChoice, self.legChoice)
            )

        @self.__shuffleHistoryInc
        def incColorsHistory(self=self):
            newChoices = self.shuffleHistory[self.shuffleHistoryPtr]
            (self.headChoice, self.armChoice, self.legChoice) = newChoices
            self.swapHeadColor(0)
            self.swapArmColor(0)
            self.swapLegColor(0)

        @self.__shuffleHistoryDec
        def decColorsHistory(self=self):
            newChoices = self.shuffleHistory[self.shuffleHistoryPtr]
            (self.headChoice, self.armChoice, self.legChoice) = newChoices
            self.swapHeadColor(0)
            self.swapArmColor(0)
            self.swapLegColor(0)

        self.rebindShuffleGUI(
            shuffleColors, decColorsHistory, incColorsHistory
        )
        self.shuffleParentFrame.setPos(1, 0, -0.6)
        self.swapHeadColor(0)
        self.swapArmColor(0)
        self.swapLegColor(0)

    def __loadClothingShopGUI(self):
        shuffleFrame = self.mainGui.find('**/*shuffleFrame')
        shuffleUp = self.mainGui.find('**/*shuffleUp')
        shuffleDown = self.mainGui.find('**/*shuffleDown')
        shuffleArrowUp = self.mainGui.find('**/*shuffleArrowUp')
        shuffleArrowDown = self.mainGui.find('**/*shuffleArrowDown')
        shuffleArrowDisabled = self.mainGui.find('**/*shuffleArrowDisabled')

        # Top
        self.topFrame = DirectFrame(
            parent=self.stageFrame, image=shuffleFrame,
            image_scale=(-0.6, 0.6, 0.6), relief=None, pos=(1, 0, 0),
            hpr=(0, 0, 2), scale=0.9, frameColor=(1, 1, 1, 1),
            text=L10N('CAT_SHIRT'), text_scale=0.0625,
            text_pos=(-0.001, -0.015), text_fg=(1, 1, 1, 1)
        )
        self.topLButton = DirectButton(
            parent=self.topFrame, relief=None, image=(shuffleArrowUp,
                shuffleArrowDown, shuffleArrowUp, shuffleArrowDisabled),
            image_scale=(0.6, 0.6, 0.6), image1_scale=(0.7, 0.7, 0.7),
            image2_scale=(0.7, 0.7, 0.7), pos=(-0.2, 0, 0),
            command=self.swapTop, extraArgs=[-1]
        )
        self.topRButton = DirectButton(
            parent=self.topFrame, relief=None, image=(shuffleArrowUp,
                shuffleArrowDown, shuffleArrowUp, shuffleArrowDisabled),
            image_scale=(-0.6, 0.6, 0.6), image1_scale=(-0.7, 0.7, 0.7),
            image2_scale=(-0.7, 0.7, 0.7), pos=(0.2, 0, 0),
            command=self.swapTop, extraArgs=[1]
        )

        # Bottom
        self.bottomFrame = DirectFrame(
            parent=self.stageFrame, image=shuffleFrame,
            image_scale=(0.6, 0.6, 0.6), relief=None, pos=(1, 0, -0.2),
            hpr=(0, 0, -2), scale=0.9, frameColor=(1, 1, 1, 1),
            text='', text_scale=0.0625, text_pos=(-0.001, -0.015),
            text_fg=(1, 1, 1, 1)
        )
        self.bottomLButton = DirectButton(
            parent=self.bottomFrame, relief=None, image=(shuffleArrowUp,
                shuffleArrowDown, shuffleArrowUp, shuffleArrowDisabled),
            image_scale=(0.6, 0.6, 0.6), image1_scale=(0.7, 0.7, 0.7),
            image2_scale=(0.7, 0.7, 0.7), pos=(-0.2, 0, 0),
            command=self.swapBottom, extraArgs=[-1]
        )
        self.bottomRButton = DirectButton(
            parent=self.bottomFrame, relief=None, image=(shuffleArrowUp,
                shuffleArrowDown, shuffleArrowUp, shuffleArrowDisabled),
            image_scale=(-0.6, 0.6, 0.6), image1_scale=(-0.7, 0.7, 0.7),
            image2_scale=(-0.7, 0.7, 0.7), pos=(0.2, 0, 0),
            command=self.swapBottom, extraArgs=[1]
        )

        # Glove Color
        self.gloveColorFrame = DirectFrame(
            parent=self.stageFrame, image=shuffleFrame,
            image_scale=(-0.6, 0.6, 0.6), relief=None, pos=(1, 0, -0.4),
            hpr=(0, 0, 3), scale=0.9, frameColor=(1, 1, 1, 1),
            text=L10N.Gloves, text_scale=0.0625,
            text_pos=(-0.001, -0.015), text_fg=(1, 1, 1, 1)
        )
        self.gloveColorLButton = DirectButton(
            parent=self.gloveColorFrame, relief=None, image=(shuffleArrowUp,
                shuffleArrowDown, shuffleArrowUp, shuffleArrowDisabled),
            image_scale=(0.6, 0.6, 0.6), image1_scale=(0.7, 0.7, 0.7),
            image2_scale=(0.7, 0.7, 0.7), pos=(-0.2, 0, 0),
            command=self.swapGloveColor, extraArgs=[-1]
        )
        self.gloveColorRButton = DirectButton(
            parent=self.gloveColorFrame, relief=None, image=(shuffleArrowUp,
                shuffleArrowDown, shuffleArrowUp, shuffleArrowDisabled),
            image_scale=(-0.6, 0.6, 0.6), image1_scale=(-0.7, 0.7, 0.7),
            image2_scale=(-0.7, 0.7, 0.7), pos=(0.2, 0, 0),
            command=self.swapGloveColor, extraArgs=[1]
        )

        # Hat
        self.hatFrame = DirectFrame(
            parent=self.stageFrame, image=shuffleFrame,
            image_scale=(0.6, 0.6, 0.6), relief=None, pos=(1, 0, 0.2),
            hpr=(0, 0, -2), scale=0.9, frameColor=(1, 1, 1, 1),
            text=L10N('ACCESSORY_HAT'), text_scale=0.0625,
            text_pos=(-0.001, -0.015), text_fg=(1, 1, 1, 1)
        )
        self.hatLButton = DirectButton(
            parent=self.hatFrame, relief=None, image=(shuffleArrowUp,
                shuffleArrowDown, shuffleArrowUp, shuffleArrowDisabled),
            image_scale=(0.6, 0.6, 0.6), image1_scale=(0.7, 0.7, 0.7),
            image2_scale=(0.7, 0.7, 0.7), pos=(-0.2, 0, 0),
            command=self.swapHat, extraArgs=[-1]
        )
        self.hatRButton = DirectButton(
            parent=self.hatFrame, relief=None, image=(shuffleArrowUp,
                shuffleArrowDown, shuffleArrowUp, shuffleArrowDisabled),
            image_scale=(-0.6, 0.6, 0.6), image1_scale=(-0.7, 0.7, 0.7),
            image2_scale=(-0.7, 0.7, 0.7), pos=(0.2, 0, 0),
            command=self.swapHat, extraArgs=[1]
        )

        # Glasses
        self.glassesFrame = DirectFrame(
            parent=self.stageFrame, image=shuffleFrame,
            image_scale=(-0.6, 0.6, 0.6), relief=None, pos=(1, 0, 0),
            hpr=(0, 0, 2), scale=0.9, frameColor=(1, 1, 1, 1),
            text=L10N('ACCESSORY_GLASSES'), text_scale=0.0625,
            text_pos=(-0.001, -0.015), text_fg=(1, 1, 1, 1)
        )
        self.glassesLButton = DirectButton(
            parent=self.glassesFrame, relief=None, image=(shuffleArrowUp,
                shuffleArrowDown, shuffleArrowUp, shuffleArrowDisabled),
            image_scale=(0.6, 0.6, 0.6), image1_scale=(0.7, 0.7, 0.7),
            image2_scale=(0.7, 0.7, 0.7), pos=(-0.2, 0, 0),
            command=self.swapGlasses, extraArgs=[-1]
        )
        self.glassesRButton = DirectButton(
            parent=self.glassesFrame, relief=None, image=(shuffleArrowUp,
                shuffleArrowDown, shuffleArrowUp, shuffleArrowDisabled),
            image_scale=(-0.6, 0.6, 0.6), image1_scale=(-0.7, 0.7, 0.7),
            image2_scale=(-0.7, 0.7, 0.7), pos=(0.2, 0, 0),
            command=self.swapGlasses, extraArgs=[1]
        )

        # Backpack
        self.backpackFrame = DirectFrame(
            parent=self.stageFrame, image=shuffleFrame,
            image_scale=(0.6, 0.6, 0.6), relief=None, pos=(1, 0, -0.2),
            hpr=(0, 0, -2), scale=0.9, frameColor=(1, 1, 1, 1),
            text=L10N('ACCESSORY_BACKPACK'), text_scale=0.0625,
            text_pos=(-0.001, -0.015), text_fg=(1, 1, 1, 1)
        )
        self.backpackLButton = DirectButton(
            parent=self.backpackFrame, relief=None, image=(shuffleArrowUp,
                shuffleArrowDown, shuffleArrowUp, shuffleArrowDisabled),
            image_scale=(0.6, 0.6, 0.6), image1_scale=(0.7, 0.7, 0.7),
            image2_scale=(0.7, 0.7, 0.7), pos=(-0.2, 0, 0),
            command=self.swapBackpack, extraArgs=[-1]
        )
        self.backpackRButton = DirectButton(
            parent=self.backpackFrame, relief=None, image=(shuffleArrowUp,
                shuffleArrowDown, shuffleArrowUp, shuffleArrowDisabled),
            image_scale=(-0.6, 0.6, 0.6), image1_scale=(-0.7, 0.7, 0.7),
            image2_scale=(-0.7, 0.7, 0.7), pos=(0.2, 0, 0),
            command=self.swapBackpack, extraArgs=[1]
        )

        # Shoes
        self.shoesFrame = DirectFrame(
            parent=self.stageFrame, image=shuffleFrame,
            image_scale=(-0.6, 0.6, 0.6), relief=None, pos=(1, 0, -0.4),
            hpr=(0, 0, 3), scale=0.9, frameColor=(1, 1, 1, 1),
            text=L10N('ACCESSORY_SHOES'), text_scale=0.0625,
            text_pos=(-0.001, -0.015), text_fg=(1, 1, 1, 1)
        )
        self.shoesLButton = DirectButton(
            parent=self.shoesFrame, relief=None, image=(shuffleArrowUp,
                shuffleArrowDown, shuffleArrowUp, shuffleArrowDisabled),
            image_scale=(0.6, 0.6, 0.6), image1_scale=(0.7, 0.7, 0.7),
            image2_scale=(0.7, 0.7, 0.7), pos=(-0.2, 0, 0),
            command=self.swapShoes, extraArgs=[-1]
        )
        self.shoesRButton = DirectButton(
            parent=self.shoesFrame, relief=None, image=(shuffleArrowUp,
                shuffleArrowDown, shuffleArrowUp, shuffleArrowDisabled),
            image_scale=(-0.6, 0.6, 0.6), image1_scale=(-0.7, 0.7, 0.7),
            image2_scale=(-0.7, 0.7, 0.7), pos=(0.2, 0, 0),
            command=self.swapShoes, extraArgs=[1]
        )
        self.toggleClothes = DirectButton(
            parent=self.stageFrame, relief=None, pos=(1, 0, 0.2),
            image=(shuffleUp, shuffleDown, shuffleUp),
            image_scale=(-0.6, 0.6, 0.6), image1_scale=(-0.63, 0.6, 0.6),
            image2_scale=(-0.63, 0.6, 0.6), text='',
            text_scale=0.05, text_pos=(0, -0.015), text_fg=(1, 1, 1, 1),
            text_shadow=(0, 0, 0, 1)
        )
        self.hideClothingShopGUI()

    def hideClothingShopGUI(self):
        self.topFrame.hide()
        self.bottomFrame.hide()
        self.gloveColorFrame.hide()
        self.hatFrame.hide()
        self.glassesFrame.hide()
        self.backpackFrame.hide()
        self.shoesFrame.hide()
        self.toggleClothes.hide()

    def showClothingShopGUI(self):
        self.showRotationGUI()
        self.showShuffleGUI()
        self.tops = ToonDNA.getRandomizedTops(self.toon.style.gender,
                                              tailorId=ToonDNA.MAKE_A_TOON)
        self.bottoms = ToonDNA.getRandomizedBottoms(
               self.toon.style.gender, tailorId=ToonDNA.MAKE_A_TOON)
        if self.toon.style.gender == 'm':
            self.hats = ToonDNA.MATBoyHats
            self.glasses = ToonDNA.MATBoyGlasses
            self.backpacks = ToonDNA.MATBoyBackpacks
            self.shoes = ToonDNA.MATBoyShoes
        else:
            self.hats = ToonDNA.MATGirlHats
            self.glasses = ToonDNA.MATGirlGlasses
            self.backpacks = ToonDNA.MATGirlBackpacks
            self.shoes = ToonDNA.MATGirlShoes
        try:
            self.hatChoice = self.hats.index(list(self.toon.getHat()))
        except:
            self.hatChoice = 0
        try:
            self.glassesChoice = self.glasses.index(
                list(self.toon.getGlasses())
            )
        except:
            self.glassesChoice = 0
        try:
            self.backpackChoice = self.backpacks.index(
                list(self.toon.getBackpack())
            )
        except:
            self.backpackChoice = 0
        try:
            self.shoesChoice = self.shoes.index(list(self.toon.getShoes()))
        except:
            self.shoesChoice = 0
        self.gloveChoice = ToonDNA.defaultGloveColorList.index(
                                    self.toon.style.gloveColor)
        self.topChoice = self.tops.index(
            (self.toon.style.topTex, self.toon.style.topTexColor,
             self.toon.style.sleeveTex, self.toon.style.sleeveTexColor))
        self.bottomChoice = self.bottoms.index(
            (self.toon.style.botTex, self.toon.style.botTexColor))
        bottomText = L10N('CAT_SHORTS')
        if self.toon.style.gender == 'f':
            bottomText = L10N('CAT_SKIRT')
        self.bottomFrame['text'] = bottomText

        @self.__shuffle
        def shuffleClothes(self=self):
            self.topChoice = random.randint(0, len(self.tops) - 1)
            self.bottomChoice = random.randint(0, len(self.bottoms) - 1)
            self.gloveChoice = random.randint(
                0, len(ToonDNA.defaultGloveColorList) - 1
            )
            self.swapTop(0)
            self.swapBottom(0)
            self.swapGloveColor(0)
            self.shuffleHistory.append(
                (self.topChoice, self.bottomChoice, self.gloveChoice)
            )

        @self.__shuffleHistoryDec
        def decClothesHistory(self=self):
            newChoices = self.shuffleHistory[self.shuffleHistoryPtr]
            (self.topChoice, self.bottomChoice, self.gloveChoice) = newChoices
            self.swapTop(0)
            self.swapBottom(0)
            self.swapGloveColor(0)

        @self.__shuffleHistoryInc
        def incClothesHistory(self=self):
            newChoices = self.shuffleHistory[self.shuffleHistoryPtr]
            (self.topChoice, self.bottomChoice, self.gloveChoice) = newChoices
            self.swapTop(0)
            self.swapBottom(0)
            self.swapGloveColor(0)

        @self.__shuffle
        def shuffleAccessories(self=self):
            self.hatChoice = random.randint(0, len(self.hats) - 1)
            self.glassesChoice = random.randint(0, len(self.glasses) - 1)
            self.backpackChoice = random.randint(0, len(self.backpacks) - 1)
            self.shoesChoice = random.randint(0, len(self.shoes) - 1)
            self.swapHat(0)
            self.swapGlasses(0)
            self.swapBackpack(0)
            self.swapShoes(0)
            self.shuffleHistory.append(
                (self.hatChoice, self.glassesChoice, self.backpackChoice,
                 self.shoesChoice)
            )

        @self.__shuffleHistoryDec
        def decAccessoriesHistory(self=self):
            newChoices = self.shuffleHistory[self.shuffleHistoryPtr]
            (self.hatChoice, self.glassesChoice, self.backpackChoice,
             self.shoesChoice) = newChoices
            self.swapHat(0)
            self.swapGlasses(0)
            self.swapBackpack(0)
            self.swapShoes(0)

        @self.__shuffleHistoryInc
        def incAccessoriesHistory(self=self):
            newChoices = self.shuffleHistory[self.shuffleHistoryPtr]
            (self.hatChoice, self.glassesChoice, self.backpackChoice,
             self.shoesChoice) = newChoices
            self.swapHat(0)
            self.swapGlasses(0)
            self.swapBackpack(0)
            self.swapShoes(0)

        self.shuffleParentFrame.setPos(1, 0, -0.6)
        self.toggleClothes.show()

        def showClothesGui():
            self.topFrame.show()
            self.bottomFrame.show()
            self.gloveColorFrame.show()
            self.hatFrame.hide()
            self.glassesFrame.hide()
            self.backpackFrame.hide()
            self.shoesFrame.hide()
            self.rebindShuffleGUI(
                shuffleClothes, decClothesHistory, incClothesHistory
            )
            self.toggleClothes['command'] = showAccessoriesGui
            self.toggleClothes['text'] = L10N('CAT_ACCESSORIES')
            self.toggleClothes.setPos(1, 0, 0.2)

        def showAccessoriesGui():
            self.topFrame.hide()
            self.bottomFrame.hide()
            self.gloveColorFrame.hide()
            self.hatFrame.show()
            self.glassesFrame.show()
            self.backpackFrame.show()
            self.shoesFrame.show()
            self.rebindShuffleGUI(
                shuffleAccessories, decAccessoriesHistory,
                incAccessoriesHistory
            )
            self.toggleClothes['command'] = showClothesGui
            self.toggleClothes['text'] = L10N('CAT_CLOTHES')
            self.toggleClothes.setPos(1, 0, 0.4)

        showClothesGui()
        self.swapTop(0)
        self.swapBottom(0)
        self.swapGloveColor(0)
        self.swapHat(0)
        self.swapGlasses(0)
        self.swapBackpack(0)
        self.swapShoes(0)

    def __loadNameShopGUI(self):
        self.typeANameGUIElements = []
        self.pickANameGUIElements = []
        self.allTitles = []
        self.allFirsts = []
        self.allPrefixes = []
        self.allSuffixes = []
        self.titleIndex = 0
        self.firstIndex = 0
        self.prefixIndex = 0
        self.suffixIndex = 0
        self.titleActive = 0
        self.firstActive = 0
        self.lastActive = 0
        self.nameIndices = [-1, -1, -1, 1]
        self.nameFlags = [1, 1, 1, 0]
        self.names = ['', '', '', '']
        self.loadedNameShopOnce = 0
        self.listsLoaded = 0
        nameBalloon = loader.loadModel('phase_3/models/props/chatbox_input')
        guiButton = loader.loadModel('phase_3/models/gui/quit_button')
        gui = loader.loadModel('phase_3/models/gui/tt_m_gui_mat_nameShop')
        self.arrowUp = gui.find('**/tt_t_gui_mat_namePanelArrowUp')
        self.arrowDown = gui.find('**/tt_t_gui_mat_namePanelArrowDown')
        self.arrowHover = gui.find('**/tt_t_gui_mat_namePanelArrowHover')
        self.squareUp = gui.find('**/tt_t_gui_mat_namePanelSquareUp')
        self.squareDown = gui.find('**/tt_t_gui_mat_namePanelSquareDown')
        self.squareHover = gui.find('**/tt_t_gui_mat_namePanelSquareHover')
        typePanel = self.nameShopGui.find('**/*typeNamePanel')
        self.typeNamePanel = DirectFrame(
            parent=self.stageFrame, image=None, relief='flat',
            scale=(0.75, 0.7, 0.7), state='disabled',
            pos=(-0.0163, 0, 0.075), image_pos=(0, 0, 0.025),
            frameColor=(1, 1, 1, 0)
        )
        self.typePanelFrame = DirectFrame(
            image=typePanel, relief='flat', frameColor=(1, 1, 1, 0),
            pos=(-0.008, 0, 0.019)
        )
        self.typePanelFrame.reparentTo(self.typeNamePanel, sort=1)
        self.typeANameGUIElements.append(self.typeNamePanel)
        self.typeANameGUIElements.append(self.typePanelFrame)
        self.nameLabel = OnscreenText(
            L10N('MAT_PLEASE_TYPE_A_NAME'), parent=self.stageFrame,
            style=ScreenPrompt, scale=0.1, pos=(-0.0163333, 0.53)
        )
        self.nameLabel.wrtReparentTo(self.typeNamePanel, sort=2)
        self.typeANameGUIElements.append(self.nameLabel)
        self.typeNotification = OnscreenText(
            L10N.CATAllNewNames, parent=self.stageFrame,
            style=ScreenPrompt, scale=0.08, pos=(-0.0163333, 0.15)
        )
        self.typeNotification.wrtReparentTo(self.typeNamePanel, sort=2)
        self.typeANameGUIElements.append(self.typeNotification)
        self.nameEntry = DirectEntry(
            parent=self.stageFrame, relief=None, scale=0.08,
            entryFont=ToonGlobals.getToonFont(), width=8.0, numLines=2,
            focus=0, cursorKeys=1, pos=(0.0, 0.0, 0.39),
            text_align=TextNode.ACenter, command=self.enterTypedName,
            autoCapitalize=1
        )
        self.nameEntry.wrtReparentTo(self.typeNamePanel, sort=2)
        self.typeANameGUIElements.append(self.nameEntry)
        self.submitButton = DirectButton(
            parent=self.stageFrame, relief=None, image=(self.squareUp,
                self.squareDown, self.squareHover, self.squareUp),
            image_scale=(1.2, 0, 1.1), pos=(-0.01, 0, -0.25),
            text=L10N('BOOK_OPT_NameShopSubmitButton'), text_scale=0.06,
            text_pos=(0, -0.02), command=self.enterTypedName
        )
        self.submitButton.wrtReparentTo(self.typeNamePanel, sort=2)
        self.typeNamePanel.setPos(-0.42, 0, -0.078)
        self.typeANameGUIElements.append(self.submitButton)
        self.randomButton = DirectButton(
            parent=self.stageFrame, relief=None, image=(self.squareUp,
                self.squareDown, self.squareHover, self.squareUp),
            image_scale=(1.15, 1.1, 1.1), scale=(1.05, 1, 1),
            pos=(0, 0, -0.25), text=L10N('CAT_SHUFFLE'), text_scale=0.06,
            text_pos=(0, -0.02), command=self.generateName
        )
        self.pickANameGUIElements.append(self.randomButton)
        self.typeANameButton = DirectButton(
            parent=self.stageFrame, relief=None, image=(self.squareUp,
                self.squareDown, self.squareHover, self.squareUp),
            image_scale=(1, 1.1, 0.9), pos=(0.0033, 0, -0.38833),
            scale=(1.2, 1, 1.2), text=L10N('MAT_TYPE_A_NAME'),
            text_scale=0.06, text_pos=(0, -0.02),
            command=self.enterTypeAName
        )
        self.pickANameGUIElements.append(self.typeANameButton)
        self.nameResult = DirectLabel(
            parent=self.stageFrame, relief=None, scale=(0.09, 0.084, 0.084),
            pos=(0.005, 0, 0.585), text=' \n ', text_scale=0.8,
            text_align=TextNode.ACenter, text_wordwrap=8.0
        )
        self.boyTitles = [' '] + [' '] + self.namePattern.fetchAll(
                                                      'm', 'title')
        self.girlTitles = [' '] + [' '] + self.namePattern.fetchAll(
                                                      'f', 'title')
        self.boyFirsts = [' '] + [' '] + self.namePattern.fetchAll(
                                                      'm', 'first')
        self.girlFirsts = [' '] + [' '] + self.namePattern.fetchAll(
                                                      'f', 'first')
        self.allPrefixes = [' '] + [' '] + self.namePattern.fetchAll(
                                                 None, 'last-prefix')
        self.allSuffixes = [' '] + [' '] + self.namePattern.fetchAll(
                                                 None, 'last-suffix')
        self.pickANameGUIElements.append(self.nameResult)
        self.titleScrollList = self.makeScrollList(
            gui, (-0.6, 0, 0.202), (1, 0.8, 0.8, 1), self.allTitles,
            self.makeNameLabel, [TextNode.ACenter, 'title']
        )
        self.firstnameScrollList = self.makeScrollList(
            gui, (-0.2, 0, 0.202), (0.8, 1, 0.8, 1), self.allFirsts,
            self.makeNameLabel, [TextNode.ACenter, 'first']
        )
        self.lastprefixScrollList = self.makeScrollList(
            gui, (0.2, 0, 0.202), (0.8, 0.8, 1, 1), self.allPrefixes,
            self.makeNameLabel, [TextNode.ARight, 'prefix']
        )
        self.lastsuffixScrollList = self.makeScrollList(
            gui, (0.55, 0, 0.202), (0.8, 0.8, 1, 1), self.allSuffixes,
            self.makeNameLabel, [TextNode.ALeft, 'suffix']
        )
        gui.removeNode()
        self.pickANameGUIElements.append(self.lastprefixScrollList)
        self.pickANameGUIElements.append(self.lastsuffixScrollList)
        self.pickANameGUIElements.append(self.titleScrollList)
        self.pickANameGUIElements.append(self.firstnameScrollList)
        self.titleHigh = self.makeHighlight((-0.710367, 0.0, 0.132967))
        self.firstHigh = self.makeHighlight((-0.310367, 0.0, 0.132967))
        self.pickANameGUIElements.append(self.titleHigh)
        self.pickANameGUIElements.append(self.firstHigh)
        self.prefixHigh = self.makeHighlight((0.09, 0.0, 0.132967))
        self.suffixHigh = self.makeHighlight((0.44, 0.0, 0.132967))
        self.pickANameGUIElements.append(self.prefixHigh)
        self.pickANameGUIElements.append(self.suffixHigh)
        nameBalloon.removeNode()
        imageList = (
            guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'),
            guiButton.find('**/QuitBtn_RLVR')
        )
        buttonImage = [imageList, imageList]
        buttonText = [L10N.CATNameShopContinueSubmission, L10N.CATNameShopChooseAnother]
        self.approvalDialog = DirectDialog(
            dialogName='approvalstate', topPad=0, fadeScreen=0.2,
            pos=(0, 0.1, 0.1), button_relief=None, image_color=(1, 1, 0.75, 1),
            text_align=TextNode.ACenter, text=L10N.CATNameShopReview,
            buttonTextList=buttonText, buttonImageList=buttonImage,
            buttonValueList=[1, 0], command=self.approvalAction
        )
        self.approvalDialog.buttonList[0].setPos(0, 0, -0.3)
        self.approvalDialog.buttonList[1].setPos(0, 0, -0.43)
        self.approvalDialog['image_scale'] = (0.8, 1, 0.77)
        for x in range(0, 2):
            self.approvalDialog.buttonList[x]['text_pos'] = (0, -0.01)
            self.approvalDialog.buttonList[x]['text_scale'] = (0.04, 0.06)
            self.approvalDialog.buttonList[x].setScale(1.2, 1, 1)
        self.approvalDialog.hide()
        guiButton.removeNode()
        self.hideNameShopGUI()

    def hideNameShopGUI(self):
        self.hideCollection(self.typeANameGUIElements)
        self.hideCollection(self.pickANameGUIElements)

    def showNameShopGUI(self):
        self.listsLoaded = 0
        if self.toon.style.gender == 'm':
            self.allTitles = self.boyTitles
            self.allFirsts = self.boyFirsts
        else:
            self.allTitles = self.girlTitles
            self.allFirsts = self.girlFirsts
        okUp = self.mainGui.find('**/*okUp')
        okDown = self.mainGui.find('**/*okDown')
        if self.nextButton:
            self.nextButton.removeNode()
            self.nextButton = None
        self.okButton = DirectButton(
            parent=self.parentFrame, pos=CATNextButtonPosition,
            scale=0.8, text='', relief=None,
            geom=(okUp, okDown, okUp, okUp),
            command=self.finalize,
            clickSound=gamebase.sounds['GUI_click'],
            rolloverSound=gamebase.sounds['GUI_rollover']
        )
        if not self.loadedNameShopOnce:
            nameShopGui = loader.loadModel('phase_3/models/gui/tt_m_gui_mat_nameShop')
            self.namePanel = DirectFrame(
                parent=self.stageFrame, image=None, relief='flat',
                state='disabled', pos=(-0.42, 0, -0.15), image_pos=(0, 0, 0.025),
                frameColor=(1, 1, 1, 0.3)
            )
            panel = nameShopGui.find('**/tt_t_gui_mat_namePanel')
            self.panelFrame = DirectFrame(
                image=panel, scale=(0.75, 0.7, 0.7), relief='flat',
                frameColor=(1, 1, 1, 0), pos=(-0.0163, 0, 0.1199)
            )
            self.panelFrame.reparentTo(self.namePanel, sort=1)
            self.pickANameGUIElements.append(self.namePanel)
            self.pickANameGUIElements.append(self.panelFrame)
            self.nameResult.reparentTo(self.namePanel, sort=2)
            self.circle = nameShopGui.find('**/tt_t_gui_mat_namePanelCircle')
            self.titleCheck = self.makeCheckBox(
                (-0.615, 0, 0.371), L10N('MAT_TITLE'), (0, 0.25, 0.5, 1),
                self.titleToggle
            )
            self.firstCheck = self.makeCheckBox(
                (-0.2193, 0, 0.371), L10N('MAT_FIRST'), (0, 0.25, 0.5, 1),
                self.firstToggle
            )
            self.lastCheck = self.makeCheckBox(
                (0.3886, 0, 0.371), L10N('MAT_LAST'), (0, 0.25, 0.5, 1),
                self.lastToggle
            )
            del self.circle
            self.pickANameGUIElements.append(self.titleCheck)
            self.pickANameGUIElements.append(self.firstCheck)
            self.pickANameGUIElements.append(self.lastCheck)
            self.titleCheck.reparentTo(self.namePanel, sort=2)
            self.firstCheck.reparentTo(self.namePanel, sort=2)
            self.lastCheck.reparentTo(self.namePanel, sort=2)
            nameShopGui.removeNode()
            self.lastprefixScrollList.reparentTo(self.namePanel)
            self.lastprefixScrollList.decButton.wrtReparentTo(self.namePanel, sort=2)
            self.lastprefixScrollList.incButton.wrtReparentTo(self.namePanel, sort=2)
            self.lastsuffixScrollList.reparentTo(self.namePanel)
            self.lastsuffixScrollList.decButton.wrtReparentTo(self.namePanel, sort=2)
            self.lastsuffixScrollList.incButton.wrtReparentTo(self.namePanel, sort=2)
            self.titleHigh.reparentTo(self.namePanel)
            self.prefixHigh.reparentTo(self.namePanel)
            self.firstHigh.reparentTo(self.namePanel)
            self.suffixHigh.reparentTo(self.namePanel)
            self.randomButton.reparentTo(self.namePanel, sort=2)
            self.typeANameButton.reparentTo(self.namePanel, sort=2)
            self.loadedNameShopOnce = 1
        self.pickANameGUIElements.remove(self.titleScrollList)
        self.pickANameGUIElements.remove(self.firstnameScrollList)
        self.titleScrollList.destroy()
        self.firstnameScrollList.destroy()
        self.titleScrollList = self.makeScrollList(
            None, (-0.6, 0, 0.202), (1, 0.8, 0.8, 1), self.allTitles,
            self.makeNameLabel, [TextNode.ACenter, 'title']
        )
        self.firstnameScrollList = self.makeScrollList(
            None, (-0.2, 0, 0.202), (0.8, 1, 0.8, 1), self.allFirsts,
            self.makeNameLabel, [TextNode.ACenter, 'first']
        )
        self.pickANameGUIElements.append(self.titleScrollList)
        self.pickANameGUIElements.append(self.firstnameScrollList)
        self.titleScrollList.reparentTo(self.namePanel, sort=-1)
        self.titleScrollList.decButton.wrtReparentTo(self.namePanel, sort=2)
        self.titleScrollList.incButton.wrtReparentTo(self.namePanel, sort=2)
        self.firstnameScrollList.reparentTo(self.namePanel, sort=-1)
        self.firstnameScrollList.decButton.wrtReparentTo(self.namePanel, sort=2)
        self.firstnameScrollList.incButton.wrtReparentTo(self.namePanel, sort=2)
        self.listsLoaded = 1
        self.generateName()
        self.typeANameButton['text'] = L10N('MAT_TYPE_A_NAME')
        for np in self.pickANameGUIElements:
            np.show()
        self.typeANameButton.hide()
        self.listsChanged()

    def hideCollection(self, collection):
        for np in collection:
            np.hide()