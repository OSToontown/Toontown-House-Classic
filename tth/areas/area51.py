#s0r00t ONLY HERE!
from __init__ import Area

from panda3d.core import CollisionTraverser, CollisionNode, CollisionHandlerQueue, CollisionRay, TextureStage

class NacibKilledMe(Area): # I think it will kill main.py at line 249
    def __init__(self,tp=None):
        self.name = "Toontown Central"
        self.music = "data/sounds/ttc/ttc.ogg"
        self.zoneId = 512
        self.avatarPN = ['wall','props']
        Area.__init__(self,"data/models/TTC/ttcrecomp.bam")

        self.sky = loader.loadModel("data/models/TTC/TT_sky.bam")
        self.sky.reparentTo(self.np)
        # self.sky.setSz(2) even area51 can't manage to host that :D
        # self.sky.setZ(-200)
        self.environ.reparentTo(self.sky)

        self.placebldg("data/models/TTC/gazebo.bam", (10.8,-59.9,-2), -268)
        self.placebldg("data/models/TTC/trolleyTT.bam", (83,-118,0.4), 218.5)
        self.placebldg("data/models/TTC/toonhall.bam", (-18.1796,103.6656,4), -360)
        self.placebldg("data/models/TTC/library.bam", (45.9,93,4), 270)
        self.placebldg("data/models/TTC/bank.bam", (-36.1796,58.6656,4), -270)
        self.placebldg("data/models/TTC/school_house.bam", (125,140,2.5), -45)
        self.placebldg("data/models/TTC/gagShop_TT.bam", (91,-90,0.4), 800)
        self.placebldg("data/models/TTC/clothshopTT.bam", (-110,122,2), -5)
        self.placebldg("data/models/TTC/Speedway_Tunnel.bam", (-172,22,3), 300)
        self.placebldg("data/models/TTC/petshopTT.bam", (-70,-123,0.4), 120)
        self.placebldg("data/models/TTC/hqTT.bam", (-29.1796,26.6656,4), 230)
        self.placebldg("data/models/TTC/partyGate_TT.bam", (154,95,2.60), -55)
        self.placetun("data/models/TTC/tunnel_TT.bam", (-56.6, -243, -6.3), 360, True)
        self.placetun("data/models/TTC/tunnel_TT.bam", (209,-65,-3.7), 420, True)
        self.placetun("data/models/TTC/tunnel_TT.bam", (-178,32,-6.3), 261, True)

        self.wallt = loader.loadModel("data/models/furniture/walls.bam")
        self.wallt.reparentTo(self.environ)
        self.wallt.setTexture(loader.loadTexture("data/maps/wallt.jpg"), 1)
        self.wallt.setTexScale(TextureStage.getDefault(), 1, 1)
        self.wallt.setPos(10,10,10)
        self.wallt.setScale(128,64,10)

        if tp: tp.done()

    def placebldg(self, path, pos, h):
        self.nmodel = loader.loadModel(path)
        self.nmodel.reparentTo(self.environ)
        self.nmodel.setPos(pos)
        self.nmodel.setH(h)

    def placetun(self, path, pos, h, sign):
        self.tunnel = loader.loadModel(path)
        self.tunnel.reparentTo(self.environ)
        self.tunnel.setPos(pos)
        self.tunnel.setH(h)
        if sign == True:
            self.sign = loader.loadModel("data/models/TTC/construction_sign.bam")
            self.sign.reparentTo(self.tunnel.find("**/sign_origin"))
            self.sign.setPos(0,0,-17)
            self.sign.find("**/sign_board").setPos(0,0,-0.25)
            self.sign.find("**/p7_3").setPos(0,0,-0.25)
            self.sign.find("**/stand").setPos(0,0,-0.15)

    def __tth_area__(self):
        return {
                'name':self.name,
                'models':self.np,
                'bgm':self.theme,
                'speeches':[]
                }

class Area51(Area): #NOT WORKING !!!
        name = "AREA_51"
        zoneId = 51
        music = ""

        avatarPN = ['wall','props']
        #Area.__init__(self,"")

        # self.m2 = loader.loadModel("data/models/streets/street_modules_enhanced.bam")
        # self.m2.reparentTo(self.np)
        # self.m1 = loader.loadModel("data/models/streets/street_modules.bam")
        # self.m2.reparentTo(self.np)


        #if tp: tp.done()

        def __tth_area__(self):
            return {
                    'name':self.name,
                    'models':self.np,
                    'bgm':self.theme,
                    'speeches':[]
                    }