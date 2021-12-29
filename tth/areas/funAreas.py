from hoods import *
from etc import Teleporter

from panda3d.core import *
#from kartShop import KartShop #now ported to indoors.
from indoors import KartShop

class Speedway(Hood):
    name = "AREA_SPEEDWAY"
    zoneId = 1400
    music = "phase_6/audio/bgm/GS_SZ.mid"

    def __init__(self, tp = None):
        self.av_startpos = (
        ((5.56815, -37.4307, 0.00348638),(-212.146, 0, 0)),
        ((8.37403, -76.0139, -0.00596408),(-137.184, 0, 0)),
        ((20.082, -91.4763, -0.0216007),(-175.539, 0, 0)),
        ((18.9959, -112.672, -0.0216004),(-196.544, 0, 0)),
        ((2.6628, -130.863, -0.021599),(-244.426, 0, 0)),
        ((-14.5224, -130.272, -0.0215979),(-310.499, 0, 0)),
        ((-23.6093, -106.275, -0.0215975),(-242.351, 0, 0)),
        ((3.62289, -29.9418, -0.118529) , (-195.653, 0, 0)),
        ((18.5745, -4.11153, -0.33125) ,(-411.898, 0, 0)),
        ((21.0235, 23.8256, -0.33125),(-526.499, 0, 0)),
        ((-1.15884, 56.7613, -0.20069),(-520.052, 0,0)),
        ((-12.182, 48.536, -0.331378),(-506.147, 0, 0)),
        )

        Hood.__init__(self,"phase_6/models/karting/GasolineAlley_TT.bam")

        self.sky = loader.loadModel("phase_3.5/models/props/TT_sky.bam")
        self.sky.reparentTo(self.np)
        self.sky.setScale(1.3)

        lerper = NodePath('lerper')
        self.sky.find('**/cloud1').setTexProjector(TextureStage.getDefault(), NodePath(), lerper)
        lerper.posInterval(200, VBase3(-1, 0, 0)).loop()

        lerper = NodePath('lerper')
        self.sky.find('**/cloud2').setTexProjector(TextureStage.getDefault(), NodePath(), lerper)
        lerper.posInterval(200, VBase3(-1, 0, 0)).loop()

        self.environ.reparentTo(self.np)
        self.environ.find('**/GS_blimp').hprInterval(150, (360,0,0)).loop()

        self.tun = self.placetun((60,175,-7),180,False)
        self.sign3 = loader.loadModel("phase_4/models/props/tunnel_sign_green.bam")
        self.sign3.reparentTo(self.tun.find("**/sign_origin"))
        self.sign3.setPosHprScale(0,-.1,0, 0,0,0, 1.5,1,1.5)
        self.icon3 = loader.loadModel("phase_4/models/props/goofySZ.bam")
        self.icon3.reparentTo(self.sign3.find("**/g1"))
        self.icon3.setPos(0,-.1,1.6)
        self.icon3.setScale(1.9)
        self.baseline(self.sign3,'MickeyFont.bam',(0,0.501961,0,1),(0,-1,0),(1.1,1,0.9),L10N('AREA_TTC')+"Playground",14)

        self.placebldg("phase_6/models/karting/kartShop.bam",(0,10,0),0)

        #won't work
        # for k in self.environ.findAllMatches("**/door"):
                # kNode = k.node()
                # kNode.setCollideMask(BitMask32(8))

        # self.collDict = self.collDict if hasattr(self,"collDict") else {}
        # self.collDict[kNode] = Teleporter(KartShop, "AREA_KARTSHOP").go()

        self.placebldg("phase_6/models/karting/tt_m_ara_gfs_leaderBoardCrashed.bam",(1,-111,0),180)
        self.placebldg("phase_6/models/karting/KartArea_WrenchJack.bam",(-33,5,0),180)
        self.placebldg("phase_6/models/karting/KartArea_Tires.bam",(33,5,0),0)

        self.placetree((-13,58,-0.3))
        self.placetree((13,58,-0.3))
        self.placetree((-13,-35,-0.3))
        self.placetree((13,-35,-0.3))
        self.placetree((-10,-76,-0.3))
        self.placetree((10,-76,-0.3))
        self.placetree((-32,-144,-0.3))
        self.placetree((32,-144,-0.3))
        self.placelight((-10,-52,-0.7))
        self.placelight((10,-52,-0.7))
        self.placelight((64,3,0))
        self.placelight((-64,3,0))
        self.placelight((64,22,0))
        self.placelight((-64,22,0))

        self.box = loader.loadModel("phase_6/models/karting/GoofyStadium_Mailbox.bam")
        self.box.reparentTo(self.np)

        self.box.setPos(16,-50,0)

        self.box.setHpr(210,0,0)

        self.box.setScale(10)
        self.flag = loader.loadModel("phase_6/models/karting/flag.bam")
        self.flag.reparentTo(self.np)

        self.flag.setPos(-18,6,-0.2)

        self.flag2 = loader.loadModel("phase_6/models/karting/flag.bam")
        self.flag2.reparentTo(self.np)

        self.flag2.setPos(18,6,-0.2)

        self.sign = loader.loadModel("phase_6/models/karting/KartShowBlockSign.bam")
        self.sign.reparentTo(self.np)

        self.sign.setPos(-16,-50,0)

        self.sign.setHpr(-120,0,0)

        self.sign.setScale(26)

        self.goofy = Actor("phase_6/models/char/TT_G-1500.bam",{"wait":"phase_6/models/char/TT_GWait.bam"})
        self.goofy.reparentTo(self.np)
        self.goofy.loop("wait")
        self.goofy.setPos(1,-95,0)
        self.goofy.setHpr(180,0,0)
        fonto = loader.loadFont("phase_3/models/fonts/MickeyFont.bam")
        frame = DirectFrame(frameColor=(0,0,0,0),parent=self.goofy)
        frame.setY(-.2)
        self.text = OnscreenText(text="Goofy",font=fonto,pos=(0,5,0),scale=1,parent=frame,fg=(1,1,0.7,1),wordwrap=9)
        self.text.setBillboardAxis(1)
        self.goofy.hide()

        self.placeann((25,-150,-0.7),(-140,0,0))
        self.placeann((-26,-149,-0.7),(-212,0,0))
        self.placeann((-38,-135,-0.7),(-212,0,0))
        self.placeann((37,-137.5,-0.7),(-140,0,0))

        self.placecone((13,-4,-0.3))
        self.placecone((13,20,-0.3))
        self.placecone((-14,18,-0.3))
        self.placecone((-14,-3,-0.3))
        self.placecone((-23,9,-0.3))
        self.placecone((45,-138,-0.6))
        self.placecone((25,-109,0))
        self.placecone((24,-111,0),45)
        self.placecone((75,-106,0),-120,110,0)
        self.placecone((76.5,-107.5,0),-90,0,110)
        self.placecone((26,-154,-0.7),42)
        self.placecone((1,-187,1.22),42)

        self.placekrate((1,-187,-0.7))
        self.placekrate((-48,-115,-0.7))
        self.placekrate((-50,-113,-0.7),45)
        self.placekrate((-49,-114,1.22),60)

        self._tunnelMovie(((self.tun,'AREA_TTC',TTCentral),),tp.getTunnel())

        if tp: tp.done()

    def placetree(self,pos):
        t = loader.loadModel("phase_6/models/karting/GoofyStadium_TreeBase.bam")
        t.reparentTo(self.np)
        t.setPos(pos)
        t.setScale(12)
        return t

    def __tth_area__(self):
        return {
                'name':self.name,
                'models':self.np,
                'bgm':self.theme,
                'speeches':[]
                }

    def placelight(self,pos):
        l = loader.loadModel("phase_6/models/karting/GoofyStadium_Lamppost_Base1.bam")
        l.reparentTo(self.np)
        l.setPos(pos)
        l.setScale(14)
        return l

    def placeann(self,pos,hpr):
        a = loader.loadModel("phase_6/models/karting/announcer.bam")
        a.reparentTo(self.np)
        a.setPos(pos)
        a.setHpr(hpr)
        return a

    def placecone(self,pos,h=0,p=0,r=0):
        c = loader.loadModel("phase_6/models/karting/cone.bam")
        c.reparentTo(self.np)
        c.setPos(pos)
        c.setHpr(h,p,r)
        return c

    def placekrate(self,pos,h=0,p=0,r=0):
        k = loader.loadModel("phase_6/models/karting/krate.bam")
        k.reparentTo(self.np)
        k.setPos(pos)
        k.setHpr(h,p,r)
        k.setScale(1.2)
        return k

    def __tth_area__(self):
        return {
                'name':self.name,
                'models':self.np,
                'bgm':self.theme,
                'gui':self.frame,
                'speeches':[]
                }

class AcornAcres(Hood):
    music = "phase_6/audio/bgm/OZ_SZ.mid"
    name = "AREA_ACRES"
    zoneId = 2400
    def __init__(self,tp=None):
        self.av_startpos = (
                            ((15.9029, -139.908, 4.69807),(-567.076, 0, 0)),
                            ((-4.88025, -53.0072, 0.446336),(-617.6, 0, 0)),
                            ((-28.3566, -71.185, 0.878941),(-575.218, 0, 0)),
                            )
        Hood.__init__(self,"phase_6/models/golf/golf_outdoor_zone.bam")

        self.sky = loader.loadModel("phase_3.5/models/props/TT_sky.bam")
        self.sky.reparentTo(self.np)
        self.sky.setScale(2.5)

        lerper = NodePath('lerper')
        self.sky.find('**/cloud1').setTexProjector(TextureStage.getDefault(), NodePath(), lerper)
        lerper.posInterval(200, VBase3(-1, 0, 0)).loop()

        lerper = NodePath('lerper')
        self.sky.find('**/cloud2').setTexProjector(TextureStage.getDefault(), NodePath(), lerper)
        lerper.posInterval(200, VBase3(-1, 0, 0)).loop()

        self.environ.reparentTo(self.np)
        self.environ.setPos(-60,-20,0)

        self.table = loader.loadModel("phase_6/models/golf/picnic_table.bam")
        self.table.reparentTo(self.np)
        self.table.setPos(-22.0614,-23.779,1.45)

        self.table = loader.loadModel("phase_6/models/golf/picnic_table.bam")
        self.table.reparentTo(self.np)
        self.table.setPos(35.4114,-35.0274,0.5)
        self.table.setHpr(0,1.10906,0)

        self.gametable = loader.loadModel("phase_6/models/golf/game_table.bam")
        self.gametable.reparentTo(self.np)
        self.gametable.setPos(91.7,5.68547,1.0)
        self.gametable.setHpr(30,1.45363,0)
        self.checkers = loader.loadModel("phase_6/models/golf/checker_game.bam")
        self.checkers.reparentTo(self.gametable.find('**/basket_locator'))

        self.gametable = loader.loadModel("phase_6/models/golf/game_table.bam")
        self.gametable.reparentTo(self.np)
        self.gametable.setPos(-75.439,62.507,0.55)
        self.gametable.setHpr(90,-1.45363,0)
        self.checkers = loader.loadModel("phase_6/models/golf/checker_game.bam")
        self.checkers.reparentTo(self.gametable.find('**/basket_locator'))

        self.gametable = loader.loadModel("phase_6/models/golf/game_table.bam")
        self.gametable.reparentTo(self.np)
        self.gametable.setPos(7.156,116.564,0.79)
        self.gametable.setHpr(0,-1.45363,0)
        self.checkers = loader.loadModel("phase_6/models/golf/checker_game.bam")
        self.checkers.reparentTo(self.gametable.find('**/basket_locator'))

        self.toG = loader.loadModel("phase_6/models/golf/chip_dale_NoSign_enterance.bam")
        self.toG.reparentTo(self.np)
        self.toG.setPos(-264.137,-15.4392,0.227776)
        self.toG.setHpr(105,-0.422594,0.309814)
        self.toG.setScale(1.0546)
        self.baseline(self.toG.find("**/sign_origin"),'Comedy.bam',(0.012,0.678,0.890,1.000),(0,0,-0.2),(2.3,3,1.7),'Mini Golf',7)

        self.toD = loader.loadModel("phase_6/models/golf/outdoor_zone_entrance.bam")
        self.toD.reparentTo(self.np)
        self.toD.setPos(86.7098,148.899,0.0205739)
        self.toD.setHpr(321.091,0,0)
        self.sign('DD',self.toD,'DD_sign2',(0,0,0),(0,0,0),(2,1,1.4))
        self.baseline(self.toD.find("**/sign_origin"),'Comedy.bam',(0.439216,0.247059,0.184314,1),(0,0,0),(2.5,1.5,5.7),"Coniferous Creek Acorn Acres",10)

        self.toF = loader.loadModel("phase_6/models/golf/outdoor_zone_entrance.bam")
        self.toF.reparentTo(self.np)
        self.toF.setPos(-47.8387,-143.259,0.1)
        self.toF.setHpr(180,0,0.1)
        self.sign('DD',self.toF,'DD_sign2',(0,0,0),(0,0,-3),(1.85,1,1.35))
        self.baseline(self.toF.find("**/sign_origin"),'Comedy.bam',(0.439216,0.247059,0.184314,1),(0,0,-0.2),(2.5,1.5,5.7),'?????? Acorn Acres',6)

        lerper = NodePath('lerper')
        self.empty = Actor("phase_6/models/golf/golf_waterfall_model.bam",{"falling":"phase_6/models/golf/golf_waterfall.bam"})
        self.empty.reparentTo(self.np)
        self.empty.loop("falling")
        self.empty.setPos(-255, -205, 0)
        self.empty.setH(-35)
        self.empty.setTexProjector(TextureStage.getDefault(), NodePath(), lerper)
        lerper.posInterval(4, VBase3(0, -1, 0)).loop()

        self.signC = self.placesign(-48.1255,-136.145,0.0177824,180,True)

        self.chip = Actor("phase_6/models/char/chip_1000.bam",{"wait":"phase_6/models/char/chip_idle.bam"})
        self.chip.reparentTo(self.np)
        self.chip.loop("wait")
        self.chip.setPos(0,-49,0.4)
        self.dale = Actor("phase_6/models/char/dale_1000.bam",{"wait":"phase_6/models/char/dale_idle.bam"})
        self.dale.reparentTo(self.chip)
        self.dale.loop("wait")
        self.dale.setPos(-4,0,0.1)
        fonto = loader.loadFont("phase_3/models/fonts/MickeyFont.bam")
        frame = DirectFrame(frameColor=(0,0,0,0),parent=self.chip)
        frame.setY(-.2)
        self.text = OnscreenText(text="Chip",font=fonto,pos=(0,3.5,0),scale=1,parent=frame,fg=(1,1,0.7,1),wordwrap=9)
        self.text.setBillboardAxis(1)
        fonto = loader.loadFont("phase_3/models/fonts/MickeyFont.bam")
        frame = DirectFrame(frameColor=(0,0,0,0),parent=self.dale)
        frame.setY(-.2)
        self.text = OnscreenText(text="Dale",font=fonto,pos=(0,3.5,0),scale=1,parent=frame,fg=(1,1,0.7,1),wordwrap=9)
        self.text.setBillboardAxis(1)
        self.chip.hide()

        lerper2 = NodePath('lerper')
        self.geyser = loader.loadModel("phase_6/models/golf/golf_geyser_model.bam")
        self.geyser.reparentTo(self.np)
        self.geyser.setPos(51,-145,-49)
        self.geyser.setTexProjector(TextureStage.getDefault(), NodePath(), lerper2)
        lerper2.posInterval(0.5, VBase3(0, 1, 0)).loop()
        cnodePath = self.geyser.attachNewNode(CollisionNode('geyserCol'))
        cnodePath.node().addSolid(CollisionTube(0, 0, 42.1, 0, 0, 0,4))
        self.geyCol = loader.loadModel("phase_11/models/lawbotHQ/LB_floor_tile.bam")
        self.geyCol.reparentTo(self.geyser)
        self.geyCol.setPos(8,-10,44)
        self.geyCol.hide()

        self.geyserSfx = SoundInterval(loader.loadSfx("phase_6/audio/sfx/OZ_Geyser_No_Toon.mp3"),loop=0)

        self.seq = Sequence(Parallel(self.geyser.scaleInterval(6,(1)),
                                       self.geyserSfx,
                                       self.geyser.posInterval(4,(51,-145,0))),
                        #Wait(4),
                        self.geyser.posInterval(2,(51,-145,-5)),
                        #Wait(2),
                        self.geyser.posInterval(4,(51,-145,0)),
                        #Wait(4),
                        self.geyser.posInterval(2,(51,-145,-5)),
                        #Wait(2),
                        self.geyser.scaleInterval(6,(0)),
                        Wait(7))

        self._tunnelMovie(
                          (
                           (self.toG,'AREA_MINIGOLF',MiniGolfZone),
                           (self.toD,'AREA_DDK',Dock)
                          ),tp.getTunnel())
        if tp: tp.done()

    def __tth_area__(self):
        return {
                'name':self.name,
                'models':self.np,
                'bgm':self.theme,
                'gui':self.frame,
                'speeches':[]
                }

    def water(self):
       gamebase.toonAvatar[0].b_setState,"swim" #wtf

class MiniGolfZone(Hood):
    music = "phase_6/audio/bgm/GZ_SZ.mid"
    name = "AREA_MINIGOLF"
    zoneId = 2450
    tunOutDelay = 0

    def __init__(self,tp=None):
        self.av_startpos = (
                            ((11.2384, 38.5296, -0.132651),(-4.07842, 0, 0)),
                            ((50.5617, 83.788, -0.132651),(-112.977, 0, 0)),
                            ((-7.62188, 85.2232, -0.127286),(-268.053, 0, 0)),
                            ((-38.2074, 129.683, -0.131641),(-334.871, 0, 0)),
                            ((-20.5172, 167.837, -0.131641),(-416.795, 0, 0)),
                            ((-9.74981, 169.52, -0.131641),(-451.147, 0, 0))
                            )
        Hood.__init__(self,"phase_6/models/golf/golf_hub2.bam")

        self.sky = loader.loadModel("phase_3.5/models/props/TT_sky.bam")
        self.sky.reparentTo(self.np)
        self.sky.setScale(2.5)

        lerper = NodePath('lerper')
        self.sky.find('**/cloud1').setTexProjector(TextureStage.getDefault(), NodePath(), lerper)
        lerper.posInterval(200, VBase3(-1, 0, 0)).loop()

        lerper = NodePath('lerper')
        self.sky.find('**/cloud2').setTexProjector(TextureStage.getDefault(), NodePath(), lerper)
        lerper.posInterval(200, VBase3(-1, 0, 0)).loop()

        self.environ.reparentTo(self.np)
        self.environ.setPos(0,0,-.1)

        blimp = loader.loadModel("phase_6/models/karting/GasolineAlley_TT.bam").find('**/GS_blimp')
        if blimp.isEmpty():
            return
        blimp.setPos(-70, 250, -70)
        blimpBase = NodePath('blimpBase')
        blimpBase.setPos(0, -200, 25)
        blimpBase.setH(-40)
        blimp.reparentTo(blimpBase)
        blimpRoot = NodePath('blimpRoot')
        blimpRoot.setPos(0, -70, 40)
        blimpRoot.reparentTo(self.np)
        blimpBase.reparentTo(blimpRoot)
        self.rotateBlimp = blimpRoot.hprInterval(360, Vec3(360, 0, 0))
        self.rotateBlimp.loop()

        self.ps = loader.loadModel("phase_6/models/karting/Parkingspot.bam")
        self.ps.reparentTo(self.np)
        self.ps.setPos(133.588,47.396,-0.05)
        self.ps.setHpr(58.732,0,0)
        self.ps1 = loader.loadModel("phase_6/models/karting/Parkingspot.bam")
        self.ps1.reparentTo(self.np)
        self.ps1.setPos(121.484,23.65,-0.05)
        self.ps1.setHpr(75.142,0,0)
        self.ps2 = loader.loadModel("phase_6/models/karting/Parkingspot.bam")
        self.ps2.reparentTo(self.np)
        self.ps2.setPos(117.751,-1.069,-0.05)
        self.ps2.setHpr(81.928,0,0)
        self.ps2.setHpr(75.142,0,0)
        self.ps3 = loader.loadModel("phase_6/models/karting/Parkingspot.bam")
        self.ps3.reparentTo(self.np)
        self.ps3.setPos(10.725,-95.93,-0.05)
        self.ps3.setHpr(-30.762,0,0)
        self.ps4 = loader.loadModel("phase_6/models/karting/Parkingspot.bam")
        self.ps4.reparentTo(self.np)
        self.ps4.setPos(-16.308,-86.81,-0.05)
        self.ps4.setHpr(-16.949,0,0)
        self.ps5 = loader.loadModel("phase_6/models/karting/Parkingspot.bam")
        self.ps5.reparentTo(self.np)
        self.ps5.setPos(-41.97,-87.26,-0.05)
        self.ps5.setHpr(-9.108,0,0)
        self.ps6 = loader.loadModel("phase_6/models/karting/Parkingspot.bam")
        self.ps6.reparentTo(self.np)
        self.ps6.setPos(-97.77,-27.878,-0.05)
        self.ps6.setHpr(-87.415,0,0)
        self.ps7 = loader.loadModel("phase_6/models/karting/Parkingspot.bam")
        self.ps7.reparentTo(self.np)
        self.ps7.setPos(-100.205,-2.018,-0.05)
        self.ps7.setHpr(284.36,0,0)
        self.ps8 = loader.loadModel("phase_6/models/karting/Parkingspot.bam")
        self.ps8.reparentTo(self.np)
        self.ps8.setPos(-106.58,21.819,-0.05)
        self.ps8.setHpr(-66.64,0,0)

        self.toB = loader.loadModel("phase_6/models/golf/Golfzone_To_Bossbot_Tunnel.bam")

        self.toB.reparentTo(self.np)
        self.toB.setPos(100,-95,0.05)
        self.toB.setHpr(45,0,0)
        self.baseline(self.toB.find("**/sign_origin"),'vtRemingtonPortable.ttf',(0,0,0,1),(0,-0.25,-.1),(0.7,1),"Bossbot Headquarters",13)

        #Hard
        self.golf_tunnel1 = loader.loadModel("phase_6/models/golf/golf_tunnel1.bam")
        self.golf_tunnel1.reparentTo(self.np)
        self.golf_tunnel1.setPos(-129.472,37.2723,0.129929)
        self.golf_tunnel1.setHpr(-54.6042,0,0)
        self.baseline(self.golf_tunnel1.find("**/sign_origin"),'MickeyFont.bam',(1,0,0,1),(-0.2,0.3,0),(0.42,.9,0.5),L10N('GOLF_HARD'),18)

        self.golf_tunnel2 = loader.loadModel("phase_6/models/golf/golf_tunnel2.bam")
        self.golf_tunnel2.reparentTo(self.np)
        self.golf_tunnel2.setPos(-110,-5,0.129929)
        self.golf_tunnel2.setHpr(-75,0,0)
        self.baseline(self.golf_tunnel2.find("**/sign_origin"),'MickeyFont.bam',(1,0,0,1),(-0.2,0.3,0),(0.42,.9,0.5),L10N('GOLF_HARD'),18)

        self.golf_tunnel3 = loader.loadModel("phase_6/models/golf/golf_tunnel1.bam")
        self.golf_tunnel3.reparentTo(self.np)
        self.golf_tunnel3.setPos(-110,-5,0.129929)
        self.golf_tunnel3.setHpr(-75,0,0)
        self.baseline(self.golf_tunnel3.find("**/sign_origin"),'MickeyFont.bam',(1,0,0,1),(-0.2,0.3,0),(0.42,.9,0.5),L10N('GOLF_HARD'),18)

        #Medium
        self.golf_tunnel4 = loader.loadModel("phase_6/models/golf/golf_tunnel1.bam")
        self.golf_tunnel4.reparentTo(self.np)
        self.golf_tunnel4.setPos(-66.3251,-96.9588,0.129929)
        self.golf_tunnel4.setHpr(7.99989,0,0)
        self.baseline(self.golf_tunnel4.find("**/sign_origin"),'MickeyFont.bam',(1,1,0,1),(-0.3,0.4,0),(0.5,.5,0.7),L10N('GOLF_MED'),10)

        self.golf_tunnel5 = loader.loadModel("phase_6/models/golf/golf_tunnel2.bam")
        self.golf_tunnel5.reparentTo(self.np)
        self.golf_tunnel5.setPos(-20,-100,0.129929)
        self.golf_tunnel5.setHpr(-15,0,0)
        self.baseline(self.golf_tunnel5.find("**/sign_origin"),'MickeyFont.bam',(1,1,0,1),(-0.3,0.4,0),(0.5,.5,0.7),L10N('GOLF_MED'),10)

        self.golf_tunnel6 = loader.loadModel("phase_6/models/golf/golf_tunnel1.bam")
        self.golf_tunnel6.reparentTo(self.np)
        self.golf_tunnel6.setPos(-20,-100,0.129929)
        self.golf_tunnel6.setHpr(-15,0,0)
        self.baseline(self.golf_tunnel6.find("**/sign_origin"),'MickeyFont.bam',(1,1,0,1),(-0.3,0.4,0),(0.5,.5,0.7),L10N('GOLF_MED'),10)

        #Easy
        self.golf_tunnel7 = loader.loadModel("phase_6/models/golf/golf_tunnel2.bam")
        self.golf_tunnel7.reparentTo(self.np)
        self.golf_tunnel7.setPos(135,20,0.129929)
        self.golf_tunnel7.setHpr(75,0,0)
        self.baseline(self.golf_tunnel7.find("**/sign_origin"),'MickeyFont.bam',(0,0.501961,0.25098,1),(-0.3,0.4,0),(0.5,.5,0.7),L10N('GOLF_EASY'),10)

        self.golf_tunnel8 = loader.loadModel("phase_6/models/golf/golf_tunnel1.bam")
        self.golf_tunnel8.reparentTo(self.np)
        self.golf_tunnel8.setPos(130.87,-26.3261,0.129929)
        self.golf_tunnel8.setHpr(95.7167,0,0)
        self.baseline(self.golf_tunnel8.find("**/sign_origin"),'MickeyFont.bam',(0,0.501961,0.25098,1),(-0.3,0.4,0),(0.5,.5,0.7),L10N('GOLF_EASY'),10)

        self.golf_tunnel9 = loader.loadModel("phase_6/models/golf/golf_tunnel1.bam")
        self.golf_tunnel9.reparentTo(self.np)
        self.golf_tunnel9.setPos(135,20,0.129929)
        self.golf_tunnel9.setHpr(75,0,0)
        self.baseline(self.golf_tunnel9.find("**/sign_origin"),'MickeyFont.bam',(0,0.501961,0.25098,1),(-0.3,0.4,0),(0.5,.5,0.7),L10N('GOLF_EASY'),10)

        #Acorn Acres tunnel
        self.toAA = loader.loadModel("phase_6/models/golf/chip_dale_NoSign_enterance.bam")
        self.toAA.reparentTo(self.np)
        self.toAA.setPos(5,145,0)

        self.baseline(self.toAA.find("**/sign_origin"),'MickeyFont.bam',(0.705882,0.156863,0.235294,1),(0,0,0),(2,1,2),L10N('AREA_ACRES'),10)

        #Golf cars
        easyColor = (0,0.501961,0.25098,1)
        mediumColor = (1,1,0,1)
        hardColor = (1,0,0,1)

        self.gCar1 = loader.loadModel("phase_6/models/golf/golf_cart3.bam")
        self.gCar1.reparentTo(self.ps)
        self.toColor1 = self.gCar1.find("**/main_body")
        self.toColor1.setColor(easyColor)
        self.gCar2 = loader.loadModel("phase_6/models/golf/golf_cart3.bam")
        self.gCar2.reparentTo(self.ps1)
        self.toColor2 = self.gCar2.find("**/main_body")
        self.toColor2.setColor(easyColor)
        self.gCar3 = loader.loadModel("phase_6/models/golf/golf_cart3.bam")
        self.gCar3.reparentTo(self.ps2)
        self.toColor3 = self.gCar3.find("**/main_body")
        self.toColor3.setColor(easyColor)

        self.gCar4 = loader.loadModel("phase_6/models/golf/golf_cart3.bam")
        self.gCar4.reparentTo(self.ps3)
        self.toColor4 = self.gCar4.find("**/main_body")
        self.toColor4.setColor(mediumColor)
        self.gCar5 = loader.loadModel("phase_6/models/golf/golf_cart3.bam")
        self.gCar5.reparentTo(self.ps4)
        self.toColor5 = self.gCar5.find("**/main_body")
        self.toColor5.setColor(mediumColor)
        self.gCar6 = loader.loadModel("phase_6/models/golf/golf_cart3.bam")
        self.gCar6.reparentTo(self.ps5)
        self.toColor6 = self.gCar6.find("**/main_body")
        self.toColor6.setColor(mediumColor)

        self.gCar7 = loader.loadModel("phase_6/models/golf/golf_cart3.bam")
        self.gCar7.reparentTo(self.ps6)
        self.toColor7 = self.gCar7.find("**/main_body")
        self.toColor7.setColor(hardColor)
        self.gCar8 = loader.loadModel("phase_6/models/golf/golf_cart3.bam")
        self.gCar8.reparentTo(self.ps7)
        self.toColor8 = self.gCar8.find("**/main_body")
        self.toColor8.setColor(hardColor)
        self.gCar9 = loader.loadModel("phase_6/models/golf/golf_cart3.bam")
        self.gCar9.reparentTo(self.ps8)
        self.toColor9 = self.gCar9.find("**/main_body")
        self.toColor9.setColor(hardColor)

        #Extra Props
        self.vCar1 = loader.loadModel("phase_6/models/golf/golf_cart3.bam")
        self.vCar1.reparentTo(self.np)
        self.vCar1.setPos(-35,116,0)
        self.vCar1.setHpr(30,0,0)
        self.color = self.vCar1.find("**/main_body")
        self.color.setColor(0.129,0.478,1.000,1.000)
        self.cushion = self.vCar1.find("**/seat1")

        #load a npc
        # TODO: Make this be a dedicated NPC (generated on the server).
        '''self.minigolf_npc = EToon(np=self.cushion,toontype="pig",color_head=(rgb2p(0,255,255)),color_torso=(rgb2p(0,255,255)),
                                  color_legs=(rgb2p(0,255,255)),body="l",gender="skirt",legsSz=1,headn=0,
                                  autoShow=True,clt=("30","22",None),name = "Dora")
        self.minigolf_npc.anim('sit')
        self.minigolf_npc._toon.setPos((0, -0.975, -0.715))
        self.minigolf_npc._toon.setH(180)
        '''

        self.seq = Sequence(self.vCar1.posHprInterval(10,(30,0,0),(10,0,0)),Wait(1),
                            self.vCar1.posHprInterval(10,(20,-80,0),(-20,0,0)),Wait(1),
                            self.vCar1.hprInterval(3,(180,0,0)),Wait(1),
                            self.vCar1.posInterval(10,(-35,116,0)),Wait(1),
                            self.vCar1.hprInterval(3,(30,0,0)),Wait(1)
                            )

        from coghqs import BossbotHQ
        self._tunnelMovie(
                          (
                           (self.toAA,'AREA_ACRES',AcornAcres),
                           (self.toB,'AREA_HQ_BOSS',BossbotHQ)
                          ),tp.getTunnel())

        if tp: tp.done()

    def __tth_area__(self):
        return {
                'name':self.name,
                'models':self.np,
                'bgm':self.theme,
                'gui':self.frame,
                'speeches':[]
                }
