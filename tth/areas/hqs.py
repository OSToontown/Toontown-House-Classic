from hoods import *
from etc import Teleporter

from panda3d.core import *
from kartShop import KartShop

class HQ_TTC_34000(Area):
    name = "AREA_ST_34000"
    zoneId = 34000
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

        #self.goofy.hide()

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