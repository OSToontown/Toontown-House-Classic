import StreetMapsGlobals as QuestMapGlobals
from direct.gui.DirectGui import *
from panda3d.core import *
from direct.task.Task import *
wantMaps = True


DonaldsDock = 1000
ToontownCentral = 2000
TheBrrrgh = 3000
MinniesMelodyland = 4000
DaisyGardens = 5000
OutdoorZone = 6000
FunnyFarm = 7000
GoofySpeedway = 8000
DonaldsDreamland = 9000
BarnacleBoulevard = 1100
SeaweedStreet = 1200
LighthouseLane = 1300
SillyStreet = 2100
LoopyLane = 2200
PunchlinePlace = 2300
WalrusWay = 3100
SleetStreet = 3200
PolarPlace = 3300
AltoAvenue = 4100
BaritoneBoulevard = 4200
TenorTerrace = 4300
ElmStreet = 5100
MapleStreet = 5200
OakStreet = 5300
LullabyLane = 9100
PajamaPlace = 9200
ToonHall = 2513
BossbotHQ = 10000
BossbotLobby = 10100
BossbotCountryClubIntA = 10500
BossbotCountryClubIntB = 10600
BossbotCountryClubIntC = 10700
SellbotHQ = 11000
SellbotLobby = 11100
SellbotFactoryExt = 11200
SellbotFactoryInt = 11500
CashbotHQ = 12000
CashbotLobby = 12100
CashbotMintIntA = 12500
CashbotMintIntB = 12600
CashbotMintIntC = 12700
LawbotHQ = 13000
LawbotLobby = 13100
LawbotOfficeExt = 13200
LawbotOfficeInt = 13300
LawbotStageIntA = 13300
LawbotStageIntB = 13400
LawbotStageIntC = 13500
LawbotStageIntD = 13600
Tutorial = 15000
MyEstate = 16000
GolfZone = 17000
PartyHood = 18000
Tutorial = 15000

dnaMap = {Tutorial: 'toontown_central',
 ToontownCentral: 'toontown_central',
 DonaldsDock: 'donalds_dock',
 MinniesMelodyland: 'minnies_melody_land',
 GoofySpeedway: 'goofy_speedway',
 TheBrrrgh: 'the_burrrgh',
 DaisyGardens: 'daisys_garden',
 FunnyFarm: 'not done yet',
 DonaldsDreamland: 'donalds_dreamland',
 OutdoorZone: 'outdoor_zone',
 BossbotHQ: 'cog_hq_bossbot',
 SellbotHQ: 'cog_hq_sellbot',
 CashbotHQ: 'cog_hq_cashbot',
 LawbotHQ: 'cog_hq_lawbot',
 GolfZone: 'golf_zone'}


class QuestMap(DirectFrame):
    def __init__(self, av,hoodid,zoneid, **kw):
        DirectFrame.__init__(self, relief=None, sortOrder=50)
        self.initialiseoptions(QuestMap)
        self.container = DirectFrame(parent=self, relief=None)
        self.marker = DirectFrame(parent=self.container, relief=None)
        self.cogInfoFrame = DirectFrame(parent=self.container, relief=None)
        cm = CardMaker('bg')
        cm.setFrame(-0.5, 0.5, -0.5, 0.5)
        bg = self.cogInfoFrame.attachNewNode(cm.generate())
        bg.setTransparency(1)
        bg.setColor(0.5, 0.5, 0.5, 0.5)
        bg.setBin('fixed', 0)
        self.cogInfoFrame['geom'] = bg
        self.cogInfoFrame['geom_pos'] = (0, 0, 0)
        self.cogInfoFrame['geom_scale'] = (6, 1, 2)
        self.cogInfoFrame.setScale(0.05)
        self.cogInfoFrame.setPos(0, 0, 0.6)
        self.buildingMarkers = []
        self.av = av
        self.wantToggle = False
        self.updateMarker = True
        self.cornerPosInfo = None
        self.hqPosInfo = None
        self.fishingSpotInfo = None
        self.load()
        self.setScale(1.5)
        bg.removeNode()
        self.hoodId = hoodid
        self.zoneId = zoneid
        self.suitPercentage = {}

    def load(self):
        gui = loader.loadModel('phase_4/models/questmap/questmap_gui.bam')
        icon = gui.find('**/tt_t_gui_qst_arrow')
        iconNP = aspect2d.attachNewNode('iconNP')
        icon.reparentTo(iconNP)
        icon.setR(90)
        self.marker['geom'] = iconNP
        self.marker['image'] = iconNP
        self.marker.setScale(0.05)
        iconNP.removeNode()
        
        self.mapOpenButton = DirectButton(
                                          image=(
                                                 gui.find('**/tt_t_gui_qst_mapClose'),
                                                 gui.find('**/tt_t_gui_qst_mapClose'),
                                                 gui.find('**/tt_t_gui_qst_mapTryToOpen')
                                                 ),
                                          relief=None,
                                          #pos=(1.25, 0, -0.63),
                                          pos=(-.08, 0, 1-.63),
                                          parent = base.a2dBottomRight,
                                          scale=0.205,
                                          command=self.show
                                          )
                                          
        self.mapCloseButton = DirectButton(
                                           image=(
                                                  gui.find('**/tt_t_gui_qst_mapOpen'),
                                                  gui.find('**/tt_t_gui_qst_mapOpen'),
                                                  gui.find('**/tt_t_gui_qst_mapTryToClose')
                                                  ),
                                           relief=None,
                                           #pos=(1.25, 0, -0.63),
                                           pos=(-.08, 0, 1-.63),
                                           parent = base.a2dBottomRight,
                                           scale=0.205,
                                           command=self.hide
                                           )
        
        self.mapOpenButton.hide()
        self.mapCloseButton.hide()
        gui.removeNode()
        icons = loader.loadModel('phase_3/models/gui/cog_icons')
        cIcon = icons.find('**/CorpIcon')
        lIcon = icons.find('**/LegalIcon')
        mIcon = icons.find('**/MoneyIcon')
        sIcon = icons.find('**/SalesIcon')
        cogInfoTextColor = (0.2, 0.2, 0.2, 1)
        textPos = (1.2, -0.2)
        textScale = 0.8
        self.cInfo = DirectLabel(parent=self.cogInfoFrame, text='', text_fg=cogInfoTextColor, text_pos=textPos, text_scale=textScale, geom=cIcon, geom_pos=(-0.2, 0, 0), geom_scale=0.8, relief=None)
        self.cInfo.setPos(-2.2, 0, 0.5)
        self.lInfo = DirectLabel(parent=self.cogInfoFrame, text_fg=cogInfoTextColor, text='', text_pos=textPos, text_scale=textScale, geom=lIcon, geom_pos=(-0.2, 0, 0), geom_scale=0.8, relief=None)
        self.lInfo.setPos(-2.2, 0, -0.5)
        self.mInfo = DirectLabel(parent=self.cogInfoFrame, text_fg=cogInfoTextColor, text='', text_pos=textPos, text_scale=textScale, geom=mIcon, geom_pos=(-0.2, 0, 0), geom_scale=0.8, relief=None)
        self.mInfo.setPos(0.8, 0, 0.5)
        self.sInfo = DirectLabel(parent=self.cogInfoFrame, text_fg=cogInfoTextColor, text='', text_pos=textPos, text_scale=textScale, geom=sIcon, geom_pos=(-0.2, 0, 0), geom_scale=0.8, relief=None)
        self.sInfo.setPos(0.8, 0, -0.5)
        icons.removeNode()
        return

    def updateCogInfo(self): #not implemented yet
        currPercentage = CogGlobals.getCogRatio()
        self.cInfo['text'] = '%s%%' % currPercentage[0]
        self.lInfo['text'] = '%s%%' % currPercentage[1]
        self.mInfo['text'] = '%s%%' % currPercentage[2]
        self.sInfo['text'] = '%s%%' % currPercentage[3]
        
    def destroy(self):
        self.ignore('questPageUpdated')
        self.mapOpenButton.destroy()
        self.mapCloseButton.destroy()
        del self.mapOpenButton
        del self.mapCloseButton
        DirectFrame.destroy(self)


    def transformAvPos(self, pos):
        if self.cornerPosInfo is None:
            return (0, 0)
        topRight = self.cornerPosInfo[0]
        bottomLeft = self.cornerPosInfo[1]
        relativeX = (pos.getX() - bottomLeft.getX()) / (topRight.getX() - bottomLeft.getX()) - 0.5
        relativeY = (pos.getY() - bottomLeft.getY()) / (topRight.getY() - bottomLeft.getY()) - 0.5
        return (relativeX, relativeY)

    def update(self, task):
        if self.av:
            if self.updateMarker:
                relX, relY = self.transformAvPos(self.av.getPos())
                self.marker.setPos(relX, 0, relY)
                self.marker.setHpr(0, 0, -180 - self.av.getH())
        i = 0
        for buildingMarker in self.buildingMarkers:
            buildingMarker.setScale((math.sin(task.time * 16.0 + i * math.pi / 3.0) + 1) * 0.005 + 0.04)
            i = i + 1

        return Task.cont

    def updateMap(self):
        if self.av:
            try:
                hoodId = self.hoodId
                zoneId = self.zoneId
                mapsGeom = loader.loadModel('phase_4/models/questmap/%s_maps' % dnaMap[hoodId])
                mapImage = mapsGeom.find('**/%s_%s_english' % (dnaMap[hoodId], zoneId))
                if not mapImage.isEmpty():
                    self.container['image'] = mapImage
                    self.resetFrameSize()
                    self.cornerPosInfo = QuestMapGlobals.CornerPosTable.get('%s_%s_english' % (dnaMap[hoodId], zoneId))
                    self.hqPosInfo = QuestMapGlobals.HQPosTable.get('%s_%s_english' % (dnaMap[hoodId], zoneId))
                    self.fishingSpotInfo = QuestMapGlobals.FishingSpotPosTable.get('%s_%s_english' % (dnaMap[hoodId], zoneId))
                    self.cogInfoPos = QuestMapGlobals.CogInfoPosTable.get('%s_%s_english' % (dnaMap[hoodId], zoneId))
                    self.cogInfoFrame.setPos(self.cogInfoPos)
                    self.hide()
                    self.hoodId = hoodId
                    self.zoneId = zoneId
                    #self.updateQuestInfo()
                    #self.updateCogInfo()
                    taskMgr.add(self.update, 'questMapUpdate')
                else:
                    self.stop()
                mapsGeom.removeNode()
            except:
                self.stop()


    def start(self):
        if not wantMaps:
          return
        else:
          self.container.show()
          self.accept('questPageUpdated', self.updateMap)
          self.handleMarker()
          self.updateMap()

    def initMarker(self, task):
        if self.av:
        #if not hasattr(base.cr.playGame.getPlace(), 'isInterior') or not base.cr.playGame.getPlace().isInterior:
            relX, relY = self.transformAvPos(self.av.getPos())
            self.marker.setPos(relX, 0, relY)
            self.marker.setHpr(0, 0, -180 - self.av.getH())
            self.marker['geom_scale'] = 1.4 * task.time % 0.5 * 10 + 1
            self.marker['geom_color'] = (1,
             1,
             1,
             0.8 - 1.4 * task.time % 0.5 * 2 / 0.8 + 0.2)
        if task.time < 1:
            return Task.cont
        else:
            self.marker['geom_color'] = (1, 1, 1, 0)
            return Task.done


    def show(self):
        taskMgr.add(self.initMarker, 'questMapInit')
        DirectFrame.show(self)
        self.mapOpenButton.hide()
        if self.container['image']:
            self.mapCloseButton.show()

    def hide(self):
        taskMgr.remove('questMapInit')
        DirectFrame.hide(self)
        if self.container['image']:
            self.mapOpenButton.show()
        self.mapCloseButton.hide()

    def toggle(self):
        if self.isHidden():
            self.show()
        else:
            self.hide()

    def obscureButton(self):
        self.mapOpenButton.hide()
        self.mapCloseButton.hide()

    def stop(self):
        self.container['image'] = None
        for marker in self.buildingMarkers:
            marker.destroy()

        self.buildingMarkers = []
        self.container.hide()
        self.hide()
        self.obscureButton()
        self.ignore('questPageUpdated')
        taskMgr.remove('questMapUpdate')
        return

    def handleMarker(self):
        self.updateMarket = not gamebase.curArea.isInterior

    def acceptOnscreenHooks(self):
        if self.wantToggle:
            self.accept('alt', self.toggle)
        else:
            self.accept('alt', self.show)
            self.accept('alt-up', self.hide)
        self.updateMap()

    def ignoreOnscreenHooks(self):
        self.ignore('alt')
        self.ignore('alt')
        self.ignore('alt-up')
        self.obscureButton()
