from BookPage import *
from direct.task.Task import Task
from tth.cogs.CogHead import CogHead
from DisguisePage import getCogName, SUIT_FONT
import SummonCogDialog

COG_QUOTAS = ((30, 25, 20, 15, 10, 5, 2, 1), (45, 40, 35, 30, 25, 20, 15, 10))
COG_UNSEEN = 1
COG_BATTLED = 2
COG_DEFEATED = 3
COG_COMPLETE1 = 4
COG_COMPLETE2 = 5

SuitPageTitle,SuitPageMystery,SuitPageQuota,SuitPageCogRadar,SuitPageBuildingRadarS,\
    SuitPageBuildingRadarP,IssueSummons = map(L10N,
                                               ("BOOK_SUIT_TITLE","BOOK_SUIT_MYSTERY","BOOK_SUIT_QUOTA",
                                                "BOOK_SUIT_RADAR","BOOK_SUIT_RADARSING","BOOK_SUIT_RADARPLURAL",
                                                "BOOK_SUIT_ISSUE")
                                              )

EmblemTypes = Enum(('Silver', 'Gold'))
localAvatar_emblems = ["SILVER!","GOLD!"]

SCALE_FACTOR = 1.5
RADAR_DELAY = 0.2
BUILDING_RADAR_POS = (0.375,
 0.065,
 -0.225,
 -0.5)
PANEL_COLORS = (Vec4(0.8, 0.78, 0.77, 1),
 Vec4(0.75, 0.78, 0.8, 1),
 Vec4(0.75, 0.82, 0.79, 1),
 Vec4(0.825, 0.76, 0.77, 1))
PANEL_COLORS_COMPLETE1 = (Vec4(0.7, 0.725, 0.545, 1),
 Vec4(0.625, 0.725, 0.65, 1),
 Vec4(0.6, 0.75, 0.525, 1),
 Vec4(0.675, 0.675, 0.55, 1))
PANEL_COLORS_COMPLETE2 = (Vec4(0.9, 0.725, 0.32, 1),
 Vec4(0.825, 0.725, 0.45, 1),
 Vec4(0.8, 0.75, 0.325, 1),
 Vec4(0.875, 0.675, 0.35, 1))
SHADOW_SCALE_POS = ((1.225,
  0,
  10,
  -0.03),
 (0.9,
  0,
  10,
  0),
 (1.125,
  0,
  10,
  -0.015),
 (1.0,
  0,
  10,
  -0.02),
 (1.0,
  -0.02,
  10,
  -0.01),
 (1.05,
  0,
  10,
  -0.0425),
 (1.0,
  0,
  10,
  -0.05),
 (0.9,
  -0.0225,
  10,
  -0.025),
 (1.25,
  0,
  10,
  -0.03),
 (1.0,
  0,
  10,
  -0.01),
 (1.0,
  0.005,
  10,
  -0.01),
 (1.0,
  0,
  10,
  -0.01),
 (0.9,
  0.005,
  10,
  -0.01),
 (0.95,
  0,
  10,
  -0.01),
 (1.125,
  0.005,
  10,
  -0.035),
 (0.85,
  -0.005,
  10,
  -0.035),
 (1.2,
  0,
  10,
  -0.01),
 (1.05,
  0,
  10,
  0),
 (1.1,
  0,
  10,
  -0.04),
 (1.0,
  0,
  10,
  0),
 (0.95,
  0.0175,
  10,
  -0.015),
 (1.0,
  0,
  10,
  -0.06),
 (0.95,
  0.02,
  10,
  -0.0175),
 (0.9,
  0,
  10,
  -0.03),
 (1.15,
  0,
  10,
  -0.01),
 (1.0,
  0,
  10,
  0),
 (1.0,
  0,
  10,
  0),
 (1.1,
  0,
  10,
  -0.04),
 (0.93,
  0.005,
  10,
  -0.01),
 (0.95,
  0.005,
  10,
  -0.01),
 (1.0,
  0,
  10,
  -0.02),
 (0.9,
  0.0025,
  10,
  -0.03))

class SuitPage(BookPage):

    def __init__(self,book):
        BookPage.__init__(self,book)
        
        _defCogsState = [-1]*32
        _defCogsSummon = [0]*32
        
        self.AVATAR_cogCounts = gamebase.toonAvatarStream.read("cogsBattled",_defCogsState) 
        self.AVATAR_cogsSummon = gamebase.toonAvatarStream.read("cogsSummon",_defCogsSummon) 
        
        self.AVATAR_cogs = []
        
        for d in range(4):
            for t in range(8):
                s = COG_UNSEEN
                c = self.AVATAR_cogCounts[8*d+t]
                if c > -1:
                    s = COG_BATTLED
                    if c > 0:
                        s = COG_DEFEATED
                        if c >= COG_QUOTAS[0][t]:
                            s = COG_COMPLETE1
                            if c >= COG_QUOTAS[1][t]:
                                s = COG_COMPLETE2
                                
                self.AVATAR_cogs.append(s)
                
        self.AVATAR_cogRadar = [all(a == COG_COMPLETE1 for a in self.AVATAR_cogs[x:x+8]) for x in xrange(0,32,8)]
        self.AVATAR_buildingRadar = [all(a == COG_COMPLETE2 for a in self.AVATAR_cogs[x:x+8]) for x in xrange(0,32,8)]
        
    def AVATAR_hasCogSummons(self,index):
        d = self.AVATAR_cogsSummon[index]
        #print "get has summons for",index,d
        return bool(d)

    def setup(self):
        frameModel = loader.loadModel('phase_3.5/models/gui/suitpage_frame')
        frameModel.setScale(0.03375, 1, 0.045)
        frameModel.setPos(0, 10, -0.575)
        self.guiTop = NodePath('guiTop')
        self.guiTop.reparentTo(self.frame)
        self.frameNode = NodePath('frameNode')
        self.frameNode.reparentTo(self.guiTop)
        self.panelNode = NodePath('panelNode')
        self.panelNode.reparentTo(self.guiTop)
        self.iconNode = NodePath('iconNode')
        self.iconNode.reparentTo(self.guiTop)
        self.enlargedPanelNode = NodePath('enlargedPanelNode')
        self.enlargedPanelNode.reparentTo(self.guiTop)
        frame = frameModel.find('**/frame')
        frame.wrtReparentTo(self.frameNode)
        screws = frameModel.find('**/screws')
        screws.wrtReparentTo(self.iconNode)
        icons = frameModel.find('**/icons')
        del frameModel
        self.title = DirectLabel(parent=self.iconNode, relief=None, text=SuitPageTitle, text_scale=0.1, text_pos=(0.04, 0), textMayChange=0)
        self.radarButtons = []
        icon = icons.find('**/corp_icon')
        self.corpRadarButton = DirectButton(parent=self.iconNode, relief=None, state=DGG.DISABLED, image=icon, image_scale=(0.03375, 1, 0.045), image2_color=Vec4(1.0, 1.0, 1.0, 0.75), pos=(-0.2, 10, -0.575), command=self.toggleRadar, extraArgs=[0])
        self.radarButtons.append(self.corpRadarButton)
        icon = icons.find('**/legal_icon')
        self.legalRadarButton = DirectButton(parent=self.iconNode, relief=None, state=DGG.DISABLED, image=icon, image_scale=(0.03375, 1, 0.045), image2_color=Vec4(1.0, 1.0, 1.0, 0.75), pos=(-0.2, 10, -0.575), command=self.toggleRadar, extraArgs=[1])
        self.radarButtons.append(self.legalRadarButton)
        icon = icons.find('**/money_icon')
        self.moneyRadarButton = DirectButton(parent=self.iconNode, relief=None, state=DGG.DISABLED, image=(icon, icon, icon), image_scale=(0.03375, 1, 0.045), image2_color=Vec4(1.0, 1.0, 1.0, 0.75), pos=(-0.2, 10, -0.575), command=self.toggleRadar, extraArgs=[2])
        self.radarButtons.append(self.moneyRadarButton)
        icon = icons.find('**/sales_icon')
        self.salesRadarButton = DirectButton(parent=self.iconNode, relief=None, state=DGG.DISABLED, image=(icon, icon, icon), image_scale=(0.03375, 1, 0.045), image2_color=Vec4(1.0, 1.0, 1.0, 0.75), pos=(-0.2, 10, -0.575), command=self.toggleRadar, extraArgs=[3])
        self.radarButtons.append(self.salesRadarButton)
        for radarButton in self.radarButtons:
            radarButton.building = 0
            radarButton.buildingRadarLabel = None

        gui = loader.loadModel('phase_3.5/models/gui/suitpage_gui')
        self.panelModel = gui.find('**/card')
        self.shadowModels = []
        for index in range(1, 32 + 1):
            self.shadowModels.append(gui.find('**/shadow' + str(index)))

        del gui
        self.makePanels()
        self.radarOn = [0,
         0,
         0,
         0]
        priceScale = 0.1
        emblemIcon = loader.loadModel('phase_3.5/models/gui/tt_m_gui_gen_emblemIcons')
        silverModel = emblemIcon.find('**/tt_t_gui_gen_emblemSilver')
        goldModel = emblemIcon.find('**/tt_t_gui_gen_emblemGold')
        self.silverLabel = DirectLabel(parent=self.frame, relief=None, pos=(-0.25, 0, -0.69), scale=priceScale, image=silverModel, image_pos=(-0.4, 0, 0.4), text=str(localAvatar_emblems[EmblemTypes.Silver]), text_fg=(0.95, 0.95, 0, 1), text_shadow=(0, 0, 0, 1), text_align=TextNode.ALeft)
        self.goldLabel = DirectLabel(parent=self.frame, relief=None, pos=(0.25, 0, -0.69), scale=priceScale, image=goldModel, image_pos=(-0.4, 0, 0.4), text=str(localAvatar_emblems[EmblemTypes.Gold]), text_fg=(0.95, 0.95, 0, 1), text_shadow=(0, 0, 0, 1), text_align=TextNode.ALeft)
        if 1:#not base.cr.wantEmblems:
            self.silverLabel.hide()
            self.goldLabel.hide()
        #self.accept(localAvatar.uniqueName('emblemsChange'), self.__emblemChange)
        self.guiTop.setZ(0.625)

        self.updatePage()
        self.bigPanel = None
        self.nextPanel = None

    def __emblemChange(self, newEmblems):
        self.silverLabel['text'] = str(newEmblems[0])
        self.goldLabel['text'] = str(newEmblems[1])

    def grow(self, panel, pos):
        if self.bigPanel:
            print 'setting next panel - ' + str(panel)
            self.nextPanel = panel
            self.nextPanelPos = pos
            return
        print 'big panel - ' + str(panel)
        self.bigPanel = panel
        panel.reparentTo(self.enlargedPanelNode)
        panel.setScale(panel.getScale() * SCALE_FACTOR)
        if panel.summonButton:
            panel.summonButton.show()
            panel.summonButton['state'] = DGG.NORMAL

    def shrink(self, panel, pos):
        print 'trying to shrink - ' + str(panel)
        if panel != self.bigPanel:
            self.nextPanel = None
            return
        print 'shrink panel - ' + str(panel)
        self.bigPanel = None
        panel.setScale(panel.scale)
        panel.reparentTo(self.panelNode)
        if panel.summonButton:
            panel.summonButton.hide()
            panel.summonButton['state'] = DGG.DISABLED
        if self.nextPanel:
            self.grow(self.nextPanel, self.nextPanelPos)
        return

    def toggleRadar(self, deptNum):
        messenger.send('wakeup')
        if self.radarOn[deptNum]:
            self.radarOn[deptNum] = 0
        else:
            self.radarOn[deptNum] = 1
        deptSize = 8
        panels = self.panels[deptSize * deptNum:8 * (deptNum + 1)]
        if self.radarOn[deptNum]:
            if hasattr(base.cr, 'currSuitPlanner'):
                if base.cr.currSuitPlanner != None:
                    base.cr.currSuitPlanner.d_suitListQuery()
                    self.acceptOnce('suitListResponse', self.updateCogRadar, extraArgs=[deptNum, panels])
                    taskMgr.doMethodLater(1.0, self.suitListResponseTimeout, 'suitListResponseTimeout-later', extraArgs=(deptNum, panels))
                    if self.radarButtons[deptNum].building:
                        base.cr.currSuitPlanner.d_buildingListQuery()
                        self.acceptOnce('buildingListResponse', self.updateBuildingRadar, extraArgs=[deptNum])
                        taskMgr.doMethodLater(1.0, self.buildingListResponseTimeout, 'buildingListResponseTimeout-later', extraArgs=(deptNum,))
                else:
                    self.updateCogRadar(deptNum, panels)
                    self.updateBuildingRadar(deptNum)
            else:
                self.updateCogRadar(deptNum, panels)
                self.updateBuildingRadar(deptNum)
            self.radarButtons[deptNum]['state'] = DGG.DISABLED
        else:
            self.updateCogRadar(deptNum, panels)
            self.updateBuildingRadar(deptNum)
        return

    def suitListResponseTimeout(self, deptNum, panels):
        self.updateCogRadar(deptNum, panels, 1)

    def buildingListResponseTimeout(self, deptNum):
        self.updateBuildingRadar(deptNum, 1)

    def makePanels(self):
        self.panels = []
        base.panels = []
        xStart = -0.66
        yStart = -0.18
        xOffset = 0.199
        yOffset = 0.284
        for dept in range(0, 4):
            row = []
            color = PANEL_COLORS[dept]
            for type in range(0, 8):
                panel = DirectLabel(parent=self.panelNode, pos=(xStart + type * xOffset, 0.0, yStart - dept * yOffset), relief=None, state=DGG.NORMAL, image=self.panelModel, image_scale=(1, 1, 1), image_color=color, text=SuitPageMystery, text_scale=0.045, text_fg=(0, 0, 0, 1), text_pos=(0, 0.185, 0), text_font=SUIT_FONT, text_wordwrap=7)
                panel.scale = 0.6
                panel.setScale(panel.scale)
                panel.quotaLabel = None
                panel.head = None
                panel.shadow = None
                panel.count = 0
                panel.summonButton = None
                self.addCogRadarLabel(panel)
                self.panels.append(panel)
                base.panels.append(panel)

        return

    def addQuotaLabel(self, panel):
        index = self.panels.index(panel)
        count = str(self.AVATAR_cogCounts[index])
        if self.AVATAR_cogs[index] < COG_COMPLETE1:
            quota = str(COG_QUOTAS[0][index % 8])
        else:
            quota = str(COG_QUOTAS[1][index % 8])
        quotaLabel = DirectLabel(parent=panel, pos=(0.0, 0.0, -0.215), relief=None, state=DGG.DISABLED, text=SuitPageQuota % (count, quota), text_scale=0.045, text_fg=(0, 0, 0, 1), text_font=SUIT_FONT)
        panel.quotaLabel = quotaLabel
        return

    def addSuitHead(self, panel, suitName):
        panelIndex = self.panels.index(panel)
        shadow = panel.attachNewNode('shadow')
        shadowModel = self.shadowModels[panelIndex]
        shadowModel.copyTo(shadow)
        coords = SHADOW_SCALE_POS[panelIndex]
        shadow.setScale(coords[0])
        shadow.setPos(coords[1], coords[2], coords[3])
        panel.shadow = shadow
        panel.head = CogHead(suitName//8,suitName%8)
        panel.head.reparentTo(panel)
        
        head = panel.head
        head.setDepthTest(1)
        head.setDepthWrite(1)
        p1 = Point3()
        p2 = Point3()
        head.calcTightBounds(p1, p2)
        d = p2 - p1
        biggest = max(d[0], d[2])
        column = suitName % 8
        s = (0.2 + column / 100.0) / biggest
        pos = -0.14 + (8 - column - 1) / 135.0
        head.setPosHprScale(0, 0, pos, 180, 0, 0, s, s, s)

    def addCogRadarLabel(self, panel):
        cogRadarLabel = DirectLabel(parent=panel, pos=(0.0, 0.0, -0.215), relief=None, state=DGG.DISABLED, text='', text_scale=0.05, text_fg=(0, 0, 0, 1), text_font=SUIT_FONT)
        panel.cogRadarLabel = cogRadarLabel
        return

    def addSummonButton(self, panel):
        buttons = loader.loadModel('phase_3/models/gui/dialog_box_buttons_gui')
        okButtonList = (buttons.find('**/ChtBx_OKBtn_UP'), buttons.find('**/ChtBx_OKBtn_DN'), buttons.find('**/ChtBx_OKBtn_Rllvr'))
        gui = loader.loadModel('phase_3.5/models/gui/stickerbook_gui')
        iconGeom = gui.find('**/summons')
        summonButton = DirectButton(parent=panel, pos=(0.1, 0.0, -0.13), scale=0.1, relief=None, state=DGG.NORMAL, image=okButtonList, image_scale=13.0, geom=iconGeom, geom_scale=0.7, text=('',
         IssueSummons,
         IssueSummons,
         ''), text_scale=0.4, text_pos=(-1.1, -0.4), command=self.summonButtonPressed, extraArgs=[panel])
        panel.summonButton = summonButton
        return

    def summonButtonPressed(self, panel):
        panelIndex = self.panels.index(panel)
        self.summonDialog = SummonCogDialog.SummonCogDialog(panelIndex)
        self.summonDialog.load()
        base.acceptOnce(self.summonDialog.doneEvent, self.summonDone, extraArgs=[panel])
        self.summonDialog.enter()

    def summonDone(self, panel):
        if self.summonDialog:
            self.summonDialog.unload()
            self.summonDialog = None
        index = self.panels.index(panel)
        if not self.AVATAR_hasCogSummons(index):
            panel.summonButton.hide()
        return

    def addBuildingRadarLabel(self, button):
        gui = loader.loadModel('phase_3.5/models/gui/suit_detail_panel')
        zPos = BUILDING_RADAR_POS[self.radarButtons.index(button)]
        buildingRadarLabel = DirectLabel(parent=button, relief=None, pos=(0.225, 0.0, zPos), state=DGG.DISABLED, image=gui.find('**/avatar_panel'), image_hpr=(0, 0, 90), image_scale=(0.05, 1, 0.1), image_pos=(0, 0, 0.015), text=SuitPageBuildingRadarP % '0', text_scale=0.05, text_fg=(1, 0, 0, 1), text_font=SUIT_FONT)
        gui.removeNode()
        button.buildingRadarLabel = buildingRadarLabel
        return

    def resetPanel(self, dept, type):
        panel = self.panels[dept * 8 + type]
        panel['text'] = SuitPageMystery
        if panel.cogRadarLabel:
            panel.cogRadarLabel.hide()
        if panel.quotaLabel:
            panel.quotaLabel.hide()
        if panel.head:
            panel.head.hide()
        if panel.shadow:
            panel.shadow.hide()
        if panel.summonButton:
            panel.summonButton.hide()
        color = PANEL_COLORS[dept]
        panel['image_color'] = color
        for button in self.radarButtons:
            if button.buildingRadarLabel:
                button.buildingRadarLabel.hide()

    def setPanelStatus(self, panel, status):
        index = self.panels.index(panel)
        if status == COG_UNSEEN:
            panel['text'] = SuitPageMystery
        elif status == COG_BATTLED:
            panel['text'] = getCogName(index)
            if panel.quotaLabel:
                panel.quotaLabel.show()
            else:
                self.addQuotaLabel(panel)
            if panel.head and panel.shadow:
                panel.head.show()
                panel.shadow.show()
            else:
                self.addSuitHead(panel, index)
            if self.AVATAR_hasCogSummons(index):
                if panel.summonButton:
                    panel.summonButton.show()
                else:
                    self.addSummonButton(panel)
        elif status == COG_DEFEATED:
            count = str(self.AVATAR_cogCounts[index])
            if self.AVATAR_cogs[index] < COG_COMPLETE1:
                quota = str(COG_QUOTAS[0][index % 8])
            else:
                quota = str(COG_QUOTAS[1][index % 8])
            panel.quotaLabel['text'] = SuitPageQuota % (count, quota)
        elif status == COG_COMPLETE1:
            panel['image_color'] = PANEL_COLORS_COMPLETE1[index / 8]
        elif status == COG_COMPLETE2:
            panel['image_color'] = PANEL_COLORS_COMPLETE2[index / 8]

    def updateAllCogs(self, status):
        for index in range(0, len(self.AVATAR_cogs)):
            self.AVATAR_cogs[index] = status

        self.updatePage()

    def updatePage(self):
        index = 0
        cogs = self.AVATAR_cogs
        for dept in range(0, 4):
            for type in range(0, 8):
                self.updateCogStatus(dept, type, cogs[index])
                index += 1

        self.updateCogRadarButtons(self.AVATAR_cogRadar)
        self.updateBuildingRadarButtons(self.AVATAR_buildingRadar)

    def updateCogStatus(self, dept, type, status):
        if dept < 0 or dept > 4:
            print 'ucs: bad cog dept: ', dept
        elif type < 0 or type > 8:
            print 'ucs: bad cog type: ', type
        elif status < COG_UNSEEN or status > COG_COMPLETE2:
            print 'ucs: bad status: ', status
        else:
            self.resetPanel(dept, type)
            panel = self.panels[dept * 8 + type]
            if status == COG_UNSEEN:
                self.setPanelStatus(panel, COG_UNSEEN)
            elif status == COG_BATTLED:
                self.setPanelStatus(panel, COG_BATTLED)
            elif status == COG_DEFEATED:
                self.setPanelStatus(panel, COG_BATTLED)
                self.setPanelStatus(panel, COG_DEFEATED)
            elif status == COG_COMPLETE1:
                self.setPanelStatus(panel, COG_BATTLED)
                self.setPanelStatus(panel, COG_DEFEATED)
                self.setPanelStatus(panel, COG_COMPLETE1)
            elif status == COG_COMPLETE2:
                self.setPanelStatus(panel, COG_BATTLED)
                self.setPanelStatus(panel, COG_DEFEATED)
                self.setPanelStatus(panel, COG_COMPLETE2)

    def updateCogRadarButtons(self, radars):
        for index in range(0, len(radars)):
            if radars[index] == 1:
                self.radarButtons[index]['state'] = DGG.NORMAL

    def updateCogRadar(self, deptNum, panels, timeout = 0):
        taskMgr.remove('suitListResponseTimeout-later')
        if not timeout and hasattr(base.cr, 'currSuitPlanner') and base.cr.currSuitPlanner != None:
            cogList = base.cr.currSuitPlanner.suitList
        else:
            cogList = []
        for panel in panels:
            panel.count = 0

        for cog in cogList:
            self.panels[cog].count += 1

        for panel in panels:
            panel.cogRadarLabel['text'] = SuitPageCogRadar % panel.count
            if self.radarOn[deptNum]:
                panel.quotaLabel.hide()

                def showLabel(label):
                    label.show()

                taskMgr.doMethodLater(RADAR_DELAY * panels.index(panel), showLabel, 'showCogRadarLater', extraArgs=(panel.cogRadarLabel,))

                def activateButton(s = self, index = deptNum):
                    self.radarButtons[index]['state'] = DGG.NORMAL
                    return Task.done

                if not self.radarButtons[deptNum].building:
                    taskMgr.doMethodLater(RADAR_DELAY * len(panels), activateButton, 'activateButtonLater')
            else:
                panel.cogRadarLabel.hide()
                panel.quotaLabel.show()

        return

    def updateBuildingRadarButtons(self, radars):
        for index in range(0, len(radars)):
            if radars[index] == 1:
                self.radarButtons[index].building = 1

    def updateBuildingRadar(self, deptNum, timeout = 0):
        taskMgr.remove('buildingListResponseTimeout-later')
        if not timeout and hasattr(base.cr, 'currSuitPlanner') and base.cr.currSuitPlanner != None:
            buildingList = base.cr.currSuitPlanner.buildingList
        else:
            buildingList = [0,
             0,
             0,
             0]
        button = self.radarButtons[deptNum]
        if button.building:
            if not button.buildingRadarLabel:
                self.addBuildingRadarLabel(button)
            if self.radarOn[deptNum]:
                num = buildingList[deptNum]
                if num == 1:
                    button.buildingRadarLabel['text'] = SuitPageBuildingRadarS % num
                else:
                    button.buildingRadarLabel['text'] = SuitPageBuildingRadarP % num

                def showLabel(button):
                    button.buildingRadarLabel.show()
                    button['state'] = DGG.NORMAL

                taskMgr.doMethodLater(RADAR_DELAY * 8, showLabel, 'showBuildingRadarLater', extraArgs=(button,))
            else:
                button.buildingRadarLabel.hide()
        return