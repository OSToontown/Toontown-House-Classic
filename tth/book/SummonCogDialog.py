from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import StateData

from DisguisePage import SUIT_FONT, getCogName
from tth.cogs.CogHead import CogHead

GlobalDialogColor = Vec4(1,1,1,.4)

SummonDlgTitle = 'Issue a Cog Summons'
SummonDlgButton1 = 'Summon a Cog'
SummonDlgButton2 = 'Summon a Cog Building'
SummonDlgButton3 = 'Summon a Cog Invasion'
SummonDlgSingleConf = 'Would you like to issue a summons to a %s?'
SummonDlgBuildingConf = 'Would you like to summon a %s to a nearby Toon building?'
SummonDlgInvasionConf = 'Would you like to summon a %s invasion?'
SummonDlgNumLeft = 'You have %s left.'
SummonDlgDelivering = 'Delivering Summons...'
SummonDlgSingleSuccess = 'You have successfully summoned the Cog.'
SummonDlgSingleBadLoc = "Sorry, Cogs aren't allowed here.  Try somewhere else."
SummonDlgBldgSuccess = 'You have successfully summoned the Cogs. %s has agreed to let them temporarily take over %s!'
SummonDlgBldgSuccess2 = 'You have successfully summoned the Cogs. A Shopkeeper has agreed to let them temporarily take over their building!'
SummonDlgBldgBadLoc = 'Sorry, there are no Toon buildings nearby for the Cogs to take over.'
SummonDlgInvasionSuccess = "You have successfully summoned the Cogs. It's an invasion!"
SummonDlgInvasionBusy = 'A %s cannot be found now.  Try again when the Cog invasion is over.'
SummonDlgInvasionFail = 'Sorry, the Cog invasion has failed.'
SummonDlgShopkeeper = 'The Shopkeeper '

class SummonCogDialog(DirectFrame, StateData.StateData):

    notify = DirectNotifyGlobal.directNotify.newCategory('SummonCogDialog')
    notify.setInfo(True)

    def __init__(self, suitIndex):
        DirectFrame.__init__(self, parent=aspect2dp, pos=(0, 0, 0.3), relief=None, image=DGG.getDefaultDialogGeom(), image_scale=(1.6, 1, 0.7), image_pos=(0, 0, 0.18), image_color=GlobalDialogColor, text=SummonDlgTitle, text_scale=0.12, text_pos=(0, 0.4), borderWidth=(0.01, 0.01), sortOrder=NO_FADE_SORT_INDEX)
        StateData.StateData.__init__(self, 'summon-cog-done')
        self.initialiseoptions(SummonCogDialog)
        self.suitIndex = suitIndex
        base.summonDialog = self
        self.popup = None
        self.suitName = self.suitIndex
        self.suitFullName = getCogName(self.suitName)
        return

    def unload(self):
        if self.isLoaded == 0:
            return None
        self.isLoaded = 0
        self.exit()
        DirectFrame.destroy(self)
        return None

    def load(self):
        if self.isLoaded == 1:
            return
        self.isLoaded = 1
        gui = loader.loadModel('phase_3/models/gui/dialog_box_buttons_gui')
        guiButton = loader.loadModel('phase_3/models/gui/quit_button')
        
        head = CogHead(self.suitName//8,self.suitName%8)
        head.reparentTo(self)
        
        head.setDepthTest(1)
        head.setDepthWrite(1)
        p1 = Point3()
        p2 = Point3()
        head.calcTightBounds(p1, p2)
        d = p2 - p1
        biggest = max(d[0], d[2])
        column = self.suitName % 8
        s = (0.2 + column / 100.0) / biggest
        pos = -0.14 + (8 - column - 1) / 135.0
        head.setPosHprScale(0, 0, pos, 180, 0, 0, s, s, s)
     
        self.head = head
        
        z = self.head.getZ()
        self.head.setPos(-0.4, -0.1, z + 0.2)
        self.suitLabel = DirectLabel(parent=self, relief=None, text=self.suitFullName, text_font=SUIT_FONT, pos=(-0.4, 0, 0), scale=0.07)
        closeButtonImage = (gui.find('**/CloseBtn_UP'), gui.find('**/CloseBtn_DN'), gui.find('**/CloseBtn_Rllvr'))
        buttonImage = (guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR'))
        disabledColor = Vec4(0.5, 0.5, 0.5, 1)
        self.summonSingleButton = DirectButton(parent=self, relief=None, text=SummonDlgButton1, image=buttonImage, image_scale=(1.7, 1, 1), image3_color=disabledColor, text_scale=0.06, text_pos=(0, -0.01), pos=(0.3, 0, 0.25), command=self.issueSummons, extraArgs=['single'])
        self.summonBuildingButton = DirectButton(parent=self, relief=None, text=SummonDlgButton2, image=buttonImage, image_scale=(1.7, 1, 1), image3_color=disabledColor, text_scale=0.06, text_pos=(0, -0.01), pos=(0.3, 0, 0.125), command=self.issueSummons, extraArgs=['building'])
        self.summonInvasionButton = DirectButton(parent=self, relief=None, text=SummonDlgButton3, image=buttonImage, image_scale=(1.7, 1, 1), image3_color=disabledColor, text_scale=0.06, text_pos=(0, -0.01), pos=(0.3, 0, 0.0), command=self.issueSummons, extraArgs=['invasion'])
        self.statusLabel = DirectLabel(parent=self, relief=None, text='', text_wordwrap=12, pos=(0.3, 0, 0.25), scale=0.07)
        self.cancel = DirectButton(parent=self, relief=None, image=closeButtonImage, pos=(0.7, 0, -0.1), command=self.__cancel)
        gui.removeNode()
        guiButton.removeNode()
        self.hide()
        return

    def enter(self):
        if self.isEntered == 1:
            return
        self.isEntered = 1
        if self.isLoaded == 0:
            self.load()
        self.disableButtons()
        self.enableButtons()
        self.popup = None
        base.transitions.fadeScreen(0.5)
        self.show()
        return

    def exit(self):
        if self.isEntered == 0:
            return None
        self.isEntered = 0
        self.cleanupDialogs()
        base.transitions.noTransitions()
        self.ignoreAll()
        self.hide()
        messenger.send(self.doneEvent, [])
        return None

    def cleanupDialogs(self):
        self.head = None
        if self.popup != None:
            self.popup.cleanup()
            self.popup = None
        return

    def cogSummonsDone(self, returnCode, suitIndex, buildingId):
        self.cancel['state'] = DGG.NORMAL
        if self.summonsType == 'single':
            if returnCode == 'success':
                self.statusLabel['text'] = SummonDlgSingleSuccess
            elif returnCode == 'badlocation':
                self.statusLabel['text'] = SummonDlgSingleBadLoc
            elif returnCode == 'fail':
                self.statusLabel['text'] = SummonDlgInvasionFail
        elif self.summonsType == 'building':
            if returnCode == 'success':
                building = base.cr.doId2do.get(buildingId)
                dnaStore = base.cr.playGame.dnaStore
                buildingTitle = dnaStore.getTitleFromBlockNumber(building.block)
                buildingInteriorZone = building.zoneId + 500 + building.block
                npcName = TTLocalizer.SummonDlgShopkeeper
                npcId = NPCToons.zone2NpcDict.get(buildingInteriorZone)
                if npcId:
                    npcName = NPCToons.getNPCName(npcId[0])
                if buildingTitle:
                    self.statusLabel['text'] = SummonDlgBldgSuccess % (npcName, buildingTitle)
                else:
                    self.statusLabel['text'] = SummonDlgBldgSuccess2
            elif returnCode == 'badlocation':
                self.statusLabel['text'] = SummonDlgBldgBadLoc
            elif returnCode == 'fail':
                self.statusLabel['text'] = SummonDlgInvasionFail
        elif self.summonsType == 'invasion':
            if returnCode == 'success':
                self.statusLabel['text'] = SummonDlgInvasionSuccess
            elif returnCode == 'busy':
                self.statusLabel['text'] = SummonDlgInvasionBusy % self.suitFullName
            elif returnCode == 'fail':
                self.statusLabel['text'] = SummonDlgInvasionFail
    
    def __reqCogSummons(self,summonsType,suitIndex):
        taskMgr.doMethodLater(4,self.__programedFail,"summonfail")
        
    def __programedFail(self,task):
        self.cogSummonsDone('fail', -1, -1)
        return task.done

    def hideSummonButtons(self):
        self.summonSingleButton.hide()
        self.summonBuildingButton.hide()
        self.summonInvasionButton.hide()

    def issueSummons(self, summonsType):
        if summonsType == 'single':
            text = SummonDlgSingleConf
        elif summonsType == 'building':
            text = SummonDlgBuildingConf
        elif summonsType == 'invasion':
            text = SummonDlgInvasionConf
        text = text % self.suitFullName

        def handleResponse(resp):
            self.popup.cleanup()
            self.popup = None
            self.reparentTo(self.getParent(), NO_FADE_SORT_INDEX)
            base.transitions.fadeScreen(0.5)
            if resp:
                self.notify.info('issuing %s summons for %s' % (summonsType, self.suitIndex))
                self.accept('cog-summons-response', self.cogSummonsDone)
                self.summonsType = summonsType
                self.doIssueSummonsText()
                self.__reqCogSummons(self.summonsType, self.suitIndex)
                self.hideSummonButtons()
                self.cancel['state'] = DGG.DISABLED
            return

        self.reparentTo(self.getParent(), 0)
        self.popup = YesNoDialog(parent=aspect2dp, text=text, fadeScreen=1, command=handleResponse)

    def doIssueSummonsText(self):
        self.disableButtons()
        self.statusLabel['text'] = SummonDlgDelivering

    def disableButtons(self):
        self.summonSingleButton['state'] = DGG.DISABLED
        self.summonBuildingButton['state'] = DGG.DISABLED
        self.summonInvasionButton['state'] = DGG.DISABLED
        
    def AVATAR_hasCogSummons(self,index,type):
        value = gamebase.toonAvatarStream.read("cogsSummon",[0]*32)[index]
        values = {}
        values["single"],values["building"],values["invasion"] =  map(lambda x:bool(int(x)),str(bin(value))[2:].ljust(3,'0'))
        
        return values[type]

    def enableButtons(self):
        if self.AVATAR_hasCogSummons(self.suitIndex, 'single'):
            self.summonSingleButton['state'] = DGG.NORMAL
        if self.AVATAR_hasCogSummons(self.suitIndex, 'building'):
            self.summonBuildingButton['state'] = DGG.NORMAL
        if self.AVATAR_hasCogSummons(self.suitIndex, 'invasion'):
            self.summonInvasionButton['state'] = DGG.NORMAL

    def __cancel(self):
        self.exit()