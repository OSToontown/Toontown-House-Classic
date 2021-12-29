from hoods import *

from panda3d.core import *
from direct.gui.DirectGui import *

import random

class BossbotHQ(Hood):
    music = "phase_12/audio/bgm/Bossbot_Entry_v"+str(random.choice(range(1,4)))+".mid"
    zoneId = 10000
    name = "AREA_HQ_BOSS"
    tunOutDelay = .5

    CAM_TUNNEL_DELTA = (40,70,10)

    def __init__(self,tp=None):
        self.av_startpos = (
                            ((0, 0, 0.0158539),(-295.458, 0, 0)),
                            ((-8.45168, 29.2063, 0.0158539),(-368.019, 0, 0)),
                            ((2.20723, 56.7239, 0.0158539),(-392.864, 0, 0)),
                            ((28.9457, 72.9393, 0.0158539),(-460.487, 0, 0)),
                            ((55.0844, 92.6239, 0.0158539),(-390.817, 0, 0)),
                            ((78.1767, 102.347, 0.0158539),(-487.704, 0, 0)),
                            ((118.244, 63.8471, 0.0158539),(-481.462, 0, 0)),
                            ((126.655, 48.093, 0.0158539),(-532.277, 0, 0)),
                            ((121.437, 12.2197, 0.0158539),(-585.351, 0, 0)),
                            ((116.987, -9.96141, 0.0158539),(-516.87, 0, 0)),
                            ((111.204, -45.1401, 0.0158539),(-574.312, 0, 0)),
                            ((69.0051, -60.0332, 0.0158539),(-702.407, 0, 0))
                            )
        Hood.__init__(self,"phase_12/models/bossbotHQ/CogGolfHub.bam")

        self.environ.reparentTo(self.np)

        #Front Three

        self.frontThree = self.environ.find("**/Gate_4")
        self.signSF = self.frontThree.find("**/sign_origin")
        self.baseline(self.signSF,'vtRemingtonPortable.ttf',(0,0,0,1),(0.2,-0.25,0),(0.7,1,0.7),'THE FRONT THREE',9)

        self.kartSF = loader.loadModel("phase_12/models/bossbotHQ/Coggolf_cart3.bam")
        self.kartSF.reparentTo(self.np)
        self.kartSF.setPosHprScale(165,42,0,115.46,0,0,1,1,1)

        #Middle Six
        self.middleSix = self.environ.find("**/Gate_3")
        self.signFT = self.middleSix.find("**/sign_origin")
        self.baseline(self.signFT,'vtRemingtonPortable.ttf',(0,0,0,1),(0,-0.25,0),(0.7,1,0.7),'THE MIDDLE SIX',9)

        self.kartFT = loader.loadModel("phase_12/models/bossbotHQ/Coggolf_cart3.bam")
        self.kartFT.reparentTo(self.np)
        self.kartFT.setPos(149,-84,0)
        self.kartFT.setHpr(56.31,0,0)

        #Back Nine
        self.backNine = self.environ.find("**/Gate_2")
        self.signNB = self.backNine.find("**/sign_origin")
        self.baseline(self.signNB,'vtRemingtonPortable.ttf',(0,0,0,1),(0,-0.25,0),(0.7,1,0.7),'THE BACK NINE',9)

        self.kartNB = loader.loadModel("phase_12/models/bossbotHQ/Coggolf_cart3.bam")
        self.kartNB.reparentTo(self.np)
        self.kartNB.setPosHprScale(-55,17,0,255.96,0,0,1,1,1)

        #Golf Club
        self.golfClub = self.environ.find("**/GateHouse")
        self.signGC = self.golfClub.find("**/sign_origin")
        self.baseline(self.signGC,'vtRemingtonPortable.ttf',(0,0,0,1),(0,-0.5,0),(1.0,1.3,0.7),'COUNTRY CLUB',13)

        x,y,z = self.signGC.getPos()
        self.placesign(x,y,0,0,True)

        #entrace
        self.entrace = self.environ.find('**/TunnelEn*')
        self.baseline(self.entrace.find('**/sign_origin'),'vtRemingtonPortable.ttf',(0,0,0,1),(0.2,-0.25,0),(1,1.3,0.7),'MINI GOLF',6)

        self.entrace.find('**/tun*origin').setPos((4.37416, -2.15352, -16.5616))
        self.entrace.find('**/tun*origin').setH(0)

        from funAreas import MiniGolfZone
        self._tunnelMovie(
                          ((self.entrace,'AREA_MINIGOLF',MiniGolfZone),),tp.getTunnel()
                          )

        if tp:tp.done()

    def baseline(self,parent,font,color,pos,scale,text,ww=7):
        fonto = loader.loadFont("phase_3/models/fonts/{0}".format(font))
        frame = DirectFrame(frameColor=(0,0,0,0),parent=parent)
        frame.setY(-.2)
        self.text = OnscreenText(text=text,font=fonto,pos=pos,scale=scale,parent=frame,fg=color,wordwrap=ww)

    def __tth_area__(self):
        return {
                'name':self.name,
                'models':self.np,
                'bgm':self.theme,
                'gui':self.frame,
                'speeches':[]
                }

class SellbotHQ(Hood):
    music = "phase_9/audio/bgm/encntr_suit_HQ_nbrhood.mid"
    zoneId = 7000
    name = "AREA_HQ_SELL"
    tunOutDelay = .5

    cogPoints = (
                 (91,-203,0.3),
                 (89,-157,0.3),
                 (62,-96,0.3),
                 (39,-87,0.3),
                 (15,-88,0.3),
                 (5,-88,0.3),
                 (-5,-88,0.3),
                 (-15,-88,0.3),
                 (-48,-93,0.3),
                 (-88,-107,0.3),
                 (-94,-127,0.3),
                 (-77,-138,0.3),
                 (-15,-119,0.3),
                 (28,-111,0.3),
                 (61,-122,0.3),
                 (74,-146,0.3),
                 (82,-182,0.3),
                 (81,-203,0.3),
                 (71,-215,0.3),
                 (51,-230,0.3),
                 (25,-241,0.3),
                 (2,-245,0.3),
                 (-35,-238,0.3),
                 (-66,-218,0.3),
                 (-73,-203,0.3),
                 (-78,-178,0.3),
                 (-64,-161,0.3),
                 (-38,-147,0.3),
                 (-17,-140,0.3),
                 (39,-133,0.3),
                 (43,-125,0.3),
                 (25,-117,0.3),
                 (-45,-138,0.3),
                 (-84,-170,0.3),
                 (-80,-220,0.3),
                 (-48,-241,0.3),
                 (-29,-245,0.3),
                 (-3,-256,0.3),
                 (24,-248,0.3),
                 (54,-236,0.3),
                )

    cogWalkDur = 159.2
    def __init__(self,tp=None):
        self.av_startpos = (
                            ((46.8838, -49.7117, 10.0956),(-225.143, 0, 0)),
                            ((-46.5074, -52.0235, 10.0956), (-130.073, 0, 0)),
                            ((28.1122, -144.825, -0.192217), (-299.112, 0, 0)),
                            ((57.2002, -179.01, -8.31569), (-343.583, 0, 0)),
                            ((43.6268, -217.165, -14.8091), (-411.424, 0, 0)),
                            ((-38.4193, -220.343, -7.92804), (-334.282, 0, 0)),
                            ((-54.6728, -184.94, -3.17877), (-373.206, 0, 0)),
                            ((2.62695, -193.398, -19.5944), (-355.481, 0, 0)),
                            )

        font = loader.loadFont('phase_3/models/fonts/vtRemingtonPortable.ttf')

        Hood.__init__(self,"phase_9/models/cogHQ/SellbotHQExterior.bam")

        self.environ.reparentTo(self.np)
        self.entrace = self.np.find('**/Tunnel1')
        self.factTun = self.np.find('**/Tunnel2')

        aspectSF = 0.7227
        cogSignSF = 23
        dgLinkTunnel = self.entrace
        dgLinkTunnel.setName('linktunnel_dg_5316_DNARoot')
        factoryLinkTunnel = self.factTun
        factoryLinkTunnel.setName('linktunnel_sellhq_11200_DNARoot')
        cogSignModel = loader.loadModel('phase_4/models/props/sign_sellBotHeadHQ.bam')
        cogSign = cogSignModel.find('**/sign_sellBotHeadHQ')
        dgSign = cogSign.copyTo(dgLinkTunnel)
        dgSign.setPosHprScale(0.0, -291.5, 29, 180.0, 0.0, 0.0, cogSignSF, cogSignSF, cogSignSF * aspectSF)
        dgSign.node().setEffect(DecalEffect.make())
        dgText = OnscreenText(text='Daisy Gardens', font=font, pos=(0, -0.3), scale=0.1, mayChange=False, parent=dgSign)
        dgText.setDepthWrite(0)
        factorySign = cogSign.copyTo(factoryLinkTunnel)
        factorySign.setPosHprScale(148.625, -155, 27, -90.0, 0.0, 0.0, cogSignSF, cogSignSF, cogSignSF * aspectSF)
        factorySign.node().setEffect(DecalEffect.make())
        factoryTypeText = OnscreenText(text='Sellbot', font=font, pos=(0, -0.25), scale=0.075, mayChange=False, parent=factorySign)
        factoryTypeText.setDepthWrite(0)
        factoryText = OnscreenText(text="Factory", font=font, pos=(0, -0.34), scale=0.12, mayChange=False, parent=factorySign)
        factoryText.setDepthWrite(0)
        doors = self.environ.find('**/doors')
        door0 = doors.find('**/door_0')
        door1 = doors.find('**/door_1')
        door2 = doors.find('**/door_2')
        door3 = doors.find('**/door_3')
        index = 0
        for door in [door0,
             door1,
             door2,
             door3]:
                 doorFrame = door.find('**/doorDoubleFlat/+GeomNode')
                 door.find('**/doorFrameHoleLeft').wrtReparentTo(doorFrame)
                 door.find('**/doorFrameHoleRight').wrtReparentTo(doorFrame)
                 doorFrame.node().setEffect(DecalEffect.make())
                 index += 1

        self.sky = loader.loadModel("phase_9/models/cogHQ/cog_sky.bam")
        self.sky.reparentTo(self.np)
        self.sky.setScale(7.5,7.5,5)
        self.sky.setH(230)

        self.botcam1 = Actor("phase_9/models/char/BotCam-zero.bam",{"botcamneutral":"phase_9/models/char/BotCam-neutral.bam"})
        self.botcam2 = Actor("phase_9/models/char/BotCam-zero.bam",{"botcamneutral":"phase_9/models/char/BotCam-neutral.bam"})
        self.botcam1.reparentTo(self.np)
        self.botcam1.setPos(-28,-40.3,15)
        self.botcam1.loop('botcamneutral')
        self.botcam2.reparentTo(self.np)
        self.botcam2.setPos(28,-40.3,15)
        self.botcam2.loop('botcamneutral')

        from streets import DG_5300
        self._tunnelMovie((
                          (self.entrace,'AREA_ST_5300',DG_5300),
                          (self.factTun,'AREA_HQ_SELL_FACTORYEXT',SellbotHQFactoryExterior),
                          ),tp.getTunnel())

        if tp:tp.done()

    def __tth_area__(self):
        return {
                'name':self.name,
                'models':self.np,
                'bgm':self.theme,
                'gui':self.frame,
                'speeches':[]
                }

class SellbotHQFactoryExterior(Hood):
    music = "phase_9/audio/bgm/encntr_suit_HQ_nbrhood.mid"
    zoneId = 7100
    name = "AREA_HQ_SELL_FACTORYEXT"
    tunOutDelay = .5
    DONT_STORE = True

    cogPoints = ( #needs to be fixed
                 (27,-341,0.05),
                 (0,-341,0.05),
                 (-27,-341,0.05),
                 (-27,-300,0.05),
                 (13,-300,0.05),
                 (13,-278,0.05),
                 (-27,-278,0.05),
                 (-27,-260,0.05),
                 (-27,-236,0.05),
                 (-27,-212,0.05),
                 (-34,-204,0.05),
                 (-60,-200,0.05),
                 (-90,-200,0.05),
                 (-145,-200,0.05),
                 (-188,-200,0.05),
                 (-188,-167,0.05),
                 (-137,-167,0.05),
                 (-41,-167,0.05),
                 (-37,-191,0.05),
                 (-31,-200,0.05),
                 (-13,-212,0.05),
                 (13,-212,0.05),
                 (31,-200,0.05),
                 (55,-182,0.05),
                 (112,-182,0.05),
                 (165,-182,0.05),
                 (165,-200,0.05),
                 (112,-200,0.05),
                 (55,-200,0.05),
                 (34,-206,0.05),
                 (27,-212,0.05),
                 (27,-236,0.05),
                 (-13,-236,0.05),
                 (-13,-260,0.05),
                 (27,-260,0.05),
                 (27,-278,0.05),
                 (27,-300,0.05),
                 (0,-143,0.05),
                 (96,-143,0.05),
                 (96,-120,0.05),
                 (159,-120,0.05),
                 (159,18,0.05),
                 (159,120,0.05),
                 (0,111,0.05),
                 (-193,103,0.05),
                 (-187,0,0.05),
                 (-182,-144,0.05),
                 (-110,-144,0.05),
                 (-110,-80,0.05),
                 (-170,-80,0.05),
                 (-170,-24,0.05),
                 (-73,-24,0.05),
                 (-73,5,0.05),
                 (-23,5,0.05),
                 (-23,-24,0.05),
                 (-23,-120,0.05),
                 (-80,-120,0.05),
                 (-80,-143,0.05),
                 (-23,18,0.05),
                 (63,18,0.05),
                 (147,18,0.05),
                 (147,-96,0.05),
                 (-23,-96,0.05)
                )

    def __init__(self,tp=None):
        self.av_startpos = (
                            ((0, 0, 0),(0,0,0)),
                            )
        Hood.__init__(self,"phase_9/models/cogHQ/SellbotFactoryExterior.bam")

        font = loader.loadFont('phase_3/models/fonts/vtRemingtonPortable.ttf')

        gamebase.toonAvatarStream.write("lastArea",str(SellbotHQ).rsplit('.',1)[-1])
        gamebase.toonAvatarStream.write("lastAreaName",SellbotHQ.name)
        gamebase.toonAvatarStream.write("lastZoneId",SellbotHQ.zoneId)

        self.environ.reparentTo(self.np)
        self.entrace = self.np.find('**/tunnel*')

        aspectSF = 0.7227
        cogSignSF = 23
        elevatorSignSF = 15
        factoryLinkTunnel = self.environ.find('**/tunnel_group2')
        factoryLinkTunnel.setName('linktunnel_sellhq_11000_DNARoot')
        factoryLinkTunnel.find('**/tunnel_sphere').setName('tunnel_trigger')
        cogSignModel = loader.loadModel('phase_4/models/props/sign_sellBotHeadHQ.bam')
        cogSign = cogSignModel.find('**/sign_sellBotHeadHQ')
        hqSign = cogSign.copyTo(factoryLinkTunnel)
        hqSign.setPosHprScale(0.0, -353, 27.5, -180.0, 0.0, 0.0, cogSignSF, cogSignSF, cogSignSF * aspectSF)
        hqSign.node().setEffect(DecalEffect.make())
        hqTypeText = OnscreenText(text="Sellbot", font=font, pos=(0, -0.25), scale=0.075, mayChange=False, parent=hqSign)
        hqTypeText.setDepthWrite(0)
        hqText = OnscreenText(text="Headquarters", font=font, pos=(0, -0.34), scale=0.1, mayChange=False, parent=hqSign)
        hqText.setDepthWrite(0)
        frontDoor = self.environ.find('**/doorway1')
        fdSign = cogSign.copyTo(frontDoor)
        fdSign.setPosHprScale(62.74, -87.99, 17.26, 2.72, 0.0, 0.0, elevatorSignSF, elevatorSignSF, elevatorSignSF * aspectSF)
        fdSign.node().setEffect(DecalEffect.make())
        fdTypeText = OnscreenText(text="Factory", font=font, pos=(0, -0.25), scale=0.075, mayChange=False, parent=fdSign)
        fdTypeText.setDepthWrite(0)
        fdText = OnscreenText(text="Front Entrance", font=font, pos=(0, -0.34), scale=0.1, mayChange=False, parent=fdSign)
        fdText.setDepthWrite(0)
        sideDoor = self.environ.find('**/doorway2')
        sdSign = cogSign.copyTo(sideDoor)
        sdSign.setPosHprScale(-164.78, 26.28, 17.25, -89.89, 0.0, 0.0, elevatorSignSF, elevatorSignSF, elevatorSignSF * aspectSF)
        sdSign.node().setEffect(DecalEffect.make())
        sdTypeText = OnscreenText(text="Factory", font=font, pos=(0, -0.25), scale=0.075, mayChange=False, parent=sdSign)
        sdTypeText.setDepthWrite(0)
        sdText = OnscreenText(text="Side Entrance", font=font, pos=(0, -0.34), scale=0.1, mayChange=False, parent=sdSign)
        sdText.setDepthWrite(0)

        self.elevator1 = loader.loadModel('phase_4/models/modules/elevator.bam')
        self.elevator1.reparentTo(self.environ.find('**/doorway1'))
        self.elevator1.setPos(62.74, -84.99, 0)
        self.elevator1.find('**/light_panel').hide()
        self.elevator1.find('**/light_panel_frame').hide()

        self.elevator2 = loader.loadModel('phase_4/models/modules/elevator.bam')
        self.elevator2.reparentTo(self.environ.find('**/doorway2'))
        self.elevator2.setPos(-162.78, 26.48, 0)
        self.elevator2.setH(-90)
        self.elevator2.find('**/light_panel').hide()
        self.elevator2.find('**/light_panel_frame').hide()

        self.sky = loader.loadModel("phase_9/models/cogHQ/cog_sky.bam")
        self.sky.reparentTo(self.np)
        self.sky.setScale(7.5,7.5,7.5)
        self.sky.setH(230)

        self._tunnelMovie(
                          ((self.entrace,'AREA_HQ_SELL',SellbotHQ),),tp.getTunnel()
                          )

        if tp:tp.done()

    def __tth_area__(self):
        return {
                'name':self.name,
                'models':self.np,
                'bgm':self.theme,
                'gui':self.frame,
                'speeches':[]
                }

class CashbotHQ(Hood):
    music = "phase_9/audio/bgm/encntr_suit_HQ_nbrhood.mid"
    zoneId = 8000
    name = "AREA_HQ_CASH"
    tunOutDelay = .5

    def __init__(self,tp=None):
        self.av_startpos = (
                            ((0, 0, 0.0158539),(-295.458, 0, 0)),
                            ((-8.45168, 29.2063, 0.0158539),(-368.019, 0, 0)),
                            ((2.20723, 56.7239, 0.0158539),(-392.864, 0, 0)),
                            ((28.9457, 72.9393, 0.0158539),(-460.487, 0, 0)),
                            ((55.0844, 92.6239, 0.0158539),(-390.817, 0, 0)),
                            ((78.1767, 102.347, 0.0158539),(-487.704, 0, 0)),
                            ((118.244, 63.8471, 0.0158539),(-481.462, 0, 0)),
                            ((126.655, 48.093, 0.0158539),(-532.277, 0, 0)),
                            ((121.437, 12.2197, 0.0158539),(-585.351, 0, 0)),
                            ((116.987, -9.96141, 0.0158539),(-516.87, 0, 0)),
                            ((69.0051, -60.0332, 0.0158539),(-702.407, 0, 0)),
                            )
        Hood.__init__(self,"phase_10/models/cogHQ/CashBotShippingStation")

        self.font = loader.loadFont('phase_3/models/fonts/vtRemingtonPortable.ttf')

        self.environ.reparentTo(self.np)
        self.entrace = self.np.find('**/Link*1')

        ddLinkTunnel = self.entrace
        ddLinkTunnel.setName('linktunnel_dl_9252_DNARoot')
        locator = self.environ.find('**/sign_origin')
        backgroundGeom = self.environ.find('**/EntranceFrameFront')
        backgroundGeom.node().setEffect(DecalEffect.make())
        signText = OnscreenText(text="Donald's Dreamland", font=self.font, scale=3, fg=(0.87, 0.87, 0.87, 1), mayChange=False, parent=backgroundGeom)
        signText.setPosHpr(locator, 0, 0, 0, 0, 0, 0)
        signText.setDepthWrite(0)

        self.makeElevator(0)
        self.makeElevator(1)
        self.makeElevator(2)

        from streets import DL_9200
        self._tunnelMovie(
                          ((self.entrace,'AREA_ST_9200',DL_9200),),tp.getTunnel()
                          )

        if tp:tp.done()

    def makeElevator(self, originId):
        self.elevatorModel = loader.loadModel('phase_10/models/cogHQ/mintElevator.bam')
        self.elevatorModel.reparentTo(self.np)
        self.leftDoor = self.elevatorModel.find('**/left_door')
        self.rightDoor = self.elevatorModel.find('**/right_door')
        locator = self.environ.find('**/elevator_origin_%s' % originId)
        if locator:
            self.elevatorModel.setPosHpr(locator, 0, 0, 0, 0, 0, 0)
        else:
            print('No origin found for originId: %s' % originId)
        backgroundGeom = self.environ.find('**/ElevatorFrameFront_%d' % originId)
        backgroundGeom.node().setEffect(DecalEffect.make())
        if originId == 0:mintText = "BULLION MINT"
        elif originId == 1:mintText = "COIN MINT"
        elif originId == 2:mintText = "DOLLAR MINT"
        signText = OnscreenText(text="CASHBOT "+mintText, font=self.font, scale=1.5, fg=(0.87, 0.87, 0.87, 1), mayChange=False, parent=backgroundGeom)
        signText.setPosHpr(locator, 0, 0, 14.5, 0, 0, 0)
        signText.setDepthWrite(0)

    def __tth_area__(self):
        return {
                'name':self.name,
                'models':self.np,
                'bgm':self.theme,
                'gui':self.frame,
                'speeches':[]
                }

class LawbotHQ(Hood):
    music = "phase_11/audio/bgm/LB_courtyard.mid"
    zoneId = 9000
    name = "AREA_HQ_LAW"
    tunOutDelay = .5

    cogPoints = (
                    (251,106,-68.4),
                    (170,81,-68.4),
                    (107,39,-68.4),
                    (24,78,-68.4),
                    (-55,103,-68.4),
                    (-32,17,-68.4),
                    (41,-9,-68.4),
                    (135,6,-68.4),
                    (222,44,-68.4),
                    (-10,-26,-68.4),
                    (-16,-76,-68.4),
                    (23,-122,-68.4),
                    (-26,-163,-68.4),
                    (20,-180,-68.4),
                    (75,-151,-68.4),
                    (74,-83,-68.4),
                    (148,-82,-68.4),
                    (206,-67,-68.4),
                    (257,-14,-68.4),
                    (232,24,-68.4),
                    (155,-8,-68.4),
                    (96,-39,-68.4),
                    (29,-37,-68.4),
                    (188,-100,-68.4),
                    (207,-173,-68.4),
                    (137,-243,-68.4),
                    (87,-179,-68.4),
                    (115,-101,-68.4),
                    (71,-180,-68.4),
                    (22,-197,-68.4),
                    (-11,-219,-68.4),
                    (13,-262,-68.4),
                    (-16,-306,-68.4),
                    (-30,-345,-68.4),
                    (-56,-378,-68.4),
                    (-68,-435,-68.4),
                    (-21,-474,-68.4),
                    (15,-448,-68.4),
                    (23,-371,-68.4),
                    (41,-280,-68.4),
                    (61,-219,-68.4),
                    (172,-247,-68.4),
                    (241,-315,-68.4),
                    (264,-398,-68.4),
                    (222,-452,-68.4),
                    (159,-362,-68.4),
                    (88,-314,-68.4),
                    (85,-247,-68.4),
                    (150,-258,-68.4)
                )

    cogWalkDur = 465
    def __init__(self,tp=None):
        self.av_startpos = (
                            ((-139.068, -188.536, -28.6182),(90,0,0)),
                            )
        Hood.__init__(self,"phase_11/models/lawbotHQ/LawbotPlaza")

        self.environ.reparentTo(self.np)
        self.entrace = self.np.find('**/Link*1')

        #the shitty DA door must be worked out (add a solid)
        self.doorDA = self.np.find('**/door_0').find('**/left*')
        self.doorDACn = CollisionNode('door_triggerPlaceholder')
        self.doorDACnP = self.doorDA.attachNewNode(self.doorDACn)
        self.doorDACn.setCollideMask(1)
        self.doorDACn.addSolid(CollisionSphere(0,0,0,10))
        #self.doorDACnP.show()
        self.doorDACnP.setPos(11,11,-20)
        self.doorDACnP.setSx(2.2)
        ug = self.environ.find('**/underground')
        ug.setBin('ground', -10)

        from streets import BR_3300
        self._tunnelMovie(
                          ((self.entrace,'AREA_ST_3300',BR_3300),),tp.getTunnel()
                          )

        #self._doorMovie(((self.doorDA,"AREA_HQ_LAW_DAEXT",LawbotHQDALobby),),tp.getDoor())

        if tp:tp.done()

    def __tth_area__(self):
        return {
                'name':self.name,
                'models':self.np,
                'bgm':self.theme,
                'gui':self.frame,
                'speeches':[]
                }

class LawbotHQDALobby(Hood): #just a prototype at the moment
    music = "phase_11/audio/bgm/LB_courtyard.mid"
    zoneId = 9100
    name = "AREA_HQ_LAW_DAEXT"
    tunOutDelay = .5
    DONT_STORE = True

    def __init__(self,tp=None):
        self.av_startpos = (
                            ((0, 0, 0),(0,0,0)),
                            )
        Hood.__init__(self,"phase_11/models/lawbotHQ/LB_DA_Lobby.bam")

        gamebase.toonAvatarStream.write("lastArea",str(LawbotHQ).rsplit('.',1)[-1])
        gamebase.toonAvatarStream.write("lastAreaName",LawbotHQ.name)
        gamebase.toonAvatarStream.write("lastZoneId",LawbotHQ.zoneId)

        self.environ.reparentTo(self.np)
        self.entrace = self.np.find('**/tunnel*')

        self._tunnelMovie(
                          ((self.entrace,'AREA_HQ_SELL',SellbotHQ),),tp.getTunnel()
                          )

        if tp:tp.done()

    def __tth_area__(self):
        return {
                'name':self.name,
                'models':self.np,
                'bgm':self.theme,
                'gui':self.frame,
                'speeches':[]
                }