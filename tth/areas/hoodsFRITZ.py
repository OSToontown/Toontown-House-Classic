#old hoods
from __init__ import Area, Tunnel
from tth.fishing.FishingHandler import *

from panda3d.core import Vec4, TextureStage, Texture, TransparencyAttrib, CollisionTraverser, CollisionNode
from panda3d.core import CollisionHandlerQueue, CollisionRay, BitMask32, RenderAttrib, AlphaTestAttrib
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *
from direct.actor.Actor import *
import random

class Hood(Area):
    def enterTrolley(self,entry):
        self.trolleyMgr.d_requestBoard(self.toon.doId)

    def baseline(self,parent,font,color,pos,scale,textx,ww):
        fonto = loader.loadFont("data/fonts/{0}".format(font))
        frame = DirectFrame(frameColor=(0,0,0,0),parent=parent)
        frame.setY(-.2)
        self.text = OnscreenText(text=textx,font=fonto,pos=pos,scale=scale,parent=frame,fg=color,wordwrap=ww)

    def placelight(self,pos,h):
        l = loader.loadModel("data/models/DDK/streetlight.bam")
        l.reparentTo(self.np)
        l.setPos(pos)
        l.setH(h)
        return l

    def placebldg(self, path, pos, h):
        nmodel = loader.loadModel(path)
        nmodel.reparentTo(self.np)
        nmodel.setPos(pos)
        nmodel.setH(h)
        return nmodel

    def placetun(self, pos, h, sign = False):
        tunnel = loader.loadModel("data/models/TTC/tunnel_TT.bam")
        tunnel.reparentTo(self.np)
        tunnel.setPos(pos)
        tunnel.setH(h)
        if sign:
            sign = loader.loadModel("data/models/TTC/construction_sign.bam")
            sign.reparentTo(tunnel.find("**/sign_origin"))
            sign.setPos(0,0,-17)
            sign.find("**/sign_board").setPos(0,0,-0.25)
            sign.find("**/p7_3").setPos(0,0,-0.25)
            sign.find("**/stand").setPos(0,0,-0.15)

        return tunnel

    def placesign(self, x, y, z, h, full = False):
        sign = loader.loadModel("data/models/TTC/construction_sign.bam")
        sign.reparentTo(self.np)
        sign.setX(x)
        sign.setY(y)
        sign.setZ(z)
        sign.setH(h)
        if not full:
            sign.find("**/sign_board").removeNode()
            sign.find("**/p7_3").removeNode()
            sign.find("**/stand").removeNode()

        return sign

    def sign(self,nbr,parent,sign,pos,hpr,scale):
        sign = loader.loadModel("data/models/TTC/signs_{0}.bam".format(nbr)).find("**/"+sign)
        sign.reparentTo(parent.find("**/sign_origin"))
        sign.setPos(pos)
        sign.setHpr(hpr)
        sign.setScale(scale)
        return sign

    def placewall(self, pos, type, h, width, height, color):
        wall = loader.loadModel("data/models/streets/walls.bam").find("**/"+type)
        wall.reparentTo(self.np)
        wall.setPos(pos)
        wall.setH(h)
        wall.setSz(height)
        wall.setSx(width)
        wall.setColor(color)
        return wall

    def makeMask(self,wall,parent):
        toMask = wall.find("**/wall_collide")
        toMask.node().setFromCollideMask(BitMask32(8))
        toMask.reparentTo(parent)

class OldTTCentral(Hood):
    def __init__(self,tp=None):
        self.name = "AREA_TTC"
        self.zoneId = 1000
        self.music = "data/sounds/ttc/ttc.ogg"

        self.av_startpos = (
        ((-11.03705883026123,39.30888748168945,4.015645503997803),(-545.7789916992188,0.0,0.0)),
        ((14.714707374572754,2.844557762145996,4.027131080627441),(-492.5708312988281,0.0,0.0)),
        ((25.963918685913086,-24.225643157958984,0.015818731859326363),(-533.1298217773438,0.0,0.0)),
        ((18.48322105407715,-37.39312744140625,-0.5424529314041138),(-579.6152954101562,0.0,0.0)),
        ((-23.09368133544922,-49.44618225097656,-3.3533806800842285),(-608.7874755859375,0.0,0.0)),
        ((-11.975284576416016,-115.15393829345703,0.018701769411563873),(-515.4699096679688,0.0,0.0)),
        ((52.929527282714844,-111.75133514404297,0.5203400254249573),(-463.4405822753906,0.0,0.0)),
        ((67.84265899658203,-53.23139572143555,0.025164341554045677),(-362.22943115234375,0.0,0.0)),
        ((72.93415069580078,-3.088984966278076,0.43976959586143494),(-393.5452575683594,0.0,0.0)),
        ((113.36840057373047,20.807981491088867,2.516672134399414),(-411.7684326171875,0.0,0.0)),
        ((127.08181762695312,45.851768493652344,2.516672134399414),(-358.1191711425781,0.0,0.0)),
        ((112.93789672851562,68.28999328613281,2.516672134399414),(-312.8993835449219,0.0,0.0)),
        ((-73.6427993774414,7.083807468414307,2.0421409606933594),(-297.6528625488281,0.0,0.0)),
        ((-113.28948974609375,75.28752899169922,2.515838623046875),(-581.64599609375,0.0,0.0))
        )

        Hood.__init__(self,"data/models/TTC/ttc.bam") #recomp causes texture problems for me #can you recompile it for yourself?

        self.sky = loader.loadModel("data/models/TTC/TT_sky.bam")
        self.sky.reparentTo(self.np)
        self.environ.reparentTo(self.sky)

        self.placebldg("data/models/TTC/gazebo.bam", (10.8,-59.9,-2), -268) #thanks to JuniorCog for the positions

        tr = self.placebldg("data/models/TTC/trolleyTT.bam", (83,-118,0.4), 218.5)
        #for m in tr.findAllMatches("**/tunn*"): m.removeNode()

        self.placebldg("data/models/TTC/toonhall.bam", (-18.1796,103.6656,4), -360)
        self.placebldg("data/models/TTC/library.bam", (45.9,93,4), 270)
        self.placebldg("data/models/TTC/bank.bam", (-36.1796,58.6656,4), -270)
        self.placebldg("data/models/TTC/school_house.bam", (125,140,2.5), -45)
        self.placebldg("data/models/TTC/gagShop_TT.bam", (91,-90,0.4), 800)
        self.placebldg("data/models/TTC/clothshopTT.bam", (-110,122,2), -5)
        self.placebldg("data/models/TTC/petshopTT.bam", (-70,-123,0.4), 120)
        self.placebldg("data/models/TTC/hqTT.bam", (-29.1796,26.6656,4), 230)
        self.placebldg("data/models/TTC/partyGate_TT.bam", (154,95,2.60), -55)
        self.speedwayTun = self.placebldg("data/models/TTC/Speedway_Tunnel.bam", (-172,22,3), 300)

        from funAreas import Speedway
        Tunnel(self.speedwayTun, BitMask32(8), self, (Speedway,'AREA_SPEEDWAY'))

        self.placetun((-56.6, -243, -6.3), 360, True)
        self.placetun((209,-65,-3.7), 420, True)
        self.ddkTunnel = self.placetun((-178,32,-6.3), 261, False)
        Tunnel(self.ddkTunnel, BitMask32(8), self, (Dock,'AREA_DDK'))

        self.placesign(74.7426, -131.237, 0.4, -145, True)
        self.placesign(88.0317, -112.015, 0.516633, -120.000015259, True)
        self.placesign(52.3783, -141.175, 0.516633, -160.0, True)
        self.placesign(31.9725, -145.567, 0.516633, -159.999969482, True)

        self.placewall((89.5, -100, 0.5),"wall_lg_brick_ur",-110,20,9,(1, 0.9, 0.33, 1))
        self.placewall((89.5, -100, 9.5),"wall_lg_brick_ur",-110,20,9,(1, 0.9, 0.33, 1))
        #self.placewall((101.9, -85, 0.5),"wall_lg_brick_ur",-110,20,18,(1, 0.9, 0.33, 1))
        self.placewall((60.5, -136.5, 0.5),'*md_dental_ur',198,39,18,(0.99,0.89,0.49,0))

        if tp: tp.done()

    def __tth_area__(self):
        return {
                'name':self.name,
                'models':self.np,
                'bgm':self.theme,
                'gui':self.frame,
                'speeches':[]
                }

class TTCentral(Hood):
    def __init__(self,tp=None):
        self.name = "AREA_TTC"
        self.zoneId = 1000
        self.music = "data/sounds/ttc/ttc.ogg"

        self.av_startpos = (
        ((-11.03705883026123,39.30888748168945,4.015645503997803),(-545.7789916992188,0.0,0.0)),
        ((14.714707374572754,2.844557762145996,4.027131080627441),(-492.5708312988281,0.0,0.0)),
        ((25.963918685913086,-24.225643157958984,0.015818731859326363),(-533.1298217773438,0.0,0.0)),
        ((18.48322105407715,-37.39312744140625,-0.5424529314041138),(-579.6152954101562,0.0,0.0)),
        ((-23.09368133544922,-49.44618225097656,-3.3533806800842285),(-608.7874755859375,0.0,0.0)),
        ((-11.975284576416016,-115.15393829345703,0.018701769411563873),(-515.4699096679688,0.0,0.0)),
        ((52.929527282714844,-111.75133514404297,0.5203400254249573),(-463.4405822753906,0.0,0.0)),
        ((67.84265899658203,-53.23139572143555,0.025164341554045677),(-362.22943115234375,0.0,0.0)),
        ((72.93415069580078,-3.088984966278076,0.43976959586143494),(-393.5452575683594,0.0,0.0)),
        ((113.36840057373047,20.807981491088867,2.516672134399414),(-411.7684326171875,0.0,0.0)),
        ((127.08181762695312,45.851768493652344,2.516672134399414),(-358.1191711425781,0.0,0.0)),
        ((112.93789672851562,68.28999328613281,2.516672134399414),(-312.8993835449219,0.0,0.0)),
        ((-73.6427993774414,7.083807468414307,2.0421409606933594),(-297.6528625488281,0.0,0.0)),
        ((-113.28948974609375,75.28752899169922,2.515838623046875),(-581.64599609375,0.0,0.0))
        )

        Hood.__init__(self,"data/models/TTC/ttc_recomp.bam")

        self.sky = loader.loadModel("data/models/TTC/TT_sky.bam")
        self.sky.reparentTo(self.np)

        self.environ.reparentTo(self.np)
        #self.environ.setPos(9.15527,-1.90735,0)
        self.environ.setHpr(-90,0,-0)

        self.pier1 = loader.loadModel("data/models/TTC/pier.bam")
        self.pier1.reparentTo(self.np)
        self.pier1.setPos(-63.5335,41.648,-3.36708)
        self.pier1.setHpr(120,0,0)
        HandlePier(self.pier1,self)

        self.pier2 = loader.loadModel("data/models/TTC/pier.bam")
        self.pier2.reparentTo(self.np)
        self.pier2.setPos(-90.2253,42.5202,-3.3105)
        self.pier2.setHpr(-130,0,0)

        self.pier3 = loader.loadModel("data/models/TTC/pier.bam")
        self.pier3.reparentTo(self.np)
        self.pier3.setPos(-94.9218,31.4153,-3.20083)
        self.pier3.setHpr(-105,0,0)

        self.pier4 = loader.loadModel("data/models/TTC/pier.bam")
        self.pier4.reparentTo(self.np)
        self.pier4.setPos(-77.5199,46.9817,-3.28456)
        self.pier4.setHpr(-180,0,0)

        self.tunnel1 = self.placetun((-239.67,64.08,-6.18),-90,True)
        self.sign1 = loader.loadModel("data/models/TTC/tunnel_sign_orange.bam")
        self.sign1.reparentTo(self.tunnel1.find("**/sign_origin"))
        self.sign1.setPosHprScale(0,-.1,0, 0,0,0, 1.5,1,1.5)
        self.icon1 = loader.loadModel("data/models/TTC/mickeySZ.bam")
        self.icon1.reparentTo(self.sign1.find("**/g1"))
        self.icon1.setPos(0,-.1,1.6)
        self.icon1.setScale(1.9)
        self.baseline(self.sign1,'MickeyFont.bam',(0,0.501961,0,1),(0,-1,0),(.9,.8,.9),"The Robust Sidewalk Toontown Central",12)

        self.tunnel2 = self.placetun((-68.38,-202.64,-3.58),-31,True)
        self.sign2 = loader.loadModel("data/models/TTC/tunnel_sign_orange.bam")
        self.sign2.reparentTo(self.tunnel2.find("**/sign_origin"))
        self.sign2.setPosHprScale(0,-.1,0, 0,0,0, 1.5,1,1.5)
        self.icon2 = loader.loadModel("data/models/TTC/mickeySZ.bam")
        self.icon2.reparentTo(self.sign2.find("**/g1"))
        self.icon2.setPos(0,-.1,1.6)
        self.icon2.setScale(1.9)
        self.baseline(self.sign2,'MickeyFont.bam',(0,0.501961,0,1),(0,-1,0),(.9,.8,.9),"Yellow Sunday Toontown Central",12)

        self.tunnel3 = self.placetun((27.6402,176.475,-6.18),171,False)
        Tunnel(self.tunnel3,BitMask32(8),self,(Dock,'AREA_DDK'))
        self.sign3 = loader.loadModel("data/models/TTC/tunnel_sign_orange.bam")
        self.sign3.reparentTo(self.tunnel3.find("**/sign_origin"))
        self.sign3.setPosHprScale(0,-.1,0, 0,0,0, 1.5,1,1.5)
        self.icon3 = loader.loadModel("data/models/TTC/mickeySZ.bam")
        self.icon3.reparentTo(self.sign3.find("**/g1"))
        self.icon3.setPos(0,-.1,1.6)
        self.icon3.setScale(1.9)
        self.baseline(self.sign3,'MickeyFont.bam',(0,0.501961,0,1),(0,-1,0),(.9,.8,.9),"Sandwich with Gardens Toontown Central",14)

        self.speedway = loader.loadModel("data/models/TTC/Speedway_Tunnel.bam")
        self.speedway.reparentTo(self.np)
        self.speedway.setPos(20.9205,172.683,3.24925)
        self.speedway.setHpr(-150,-0.083787,0.0101321)

        from funAreas import Speedway
        Tunnel(self.speedway,BitMask32(8),self,(Speedway,'AREA_SPEEDWAY'))
        self.baseline(self.speedway.find("**/sign_origin"),'MickeyFont.bam',(0.00392157,0.403922,0.803922,1),(2.07014,0.591417,0),(2.67969,1,2.12201),L10N('AREA_SPEEDWAY'),7)

        self.trolley = loader.loadModel("data/models/TTC/trolleyTT.bam")
        self.trolley.reparentTo(self.np)
        self.trolley.setPos(-120.945,-77.5626,0.525)
        self.trolley.setHpr(128,0,0)

        trolleyNp = self.trolley.find('**/trolley_sphere')
        trolleyNode = trolleyNp.node()
        trolleyNode.setCollideMask(BitMask32(8))

        self.collDict = self.collDict if hasattr(self,"collDict") else {}
        self.collDict[trolleyNode] = self.enterTrolley

        self.baseline(self.trolley.find("**/sign_origin"),'MickeyFont.bam',(0.992157,0.968627,0.00784314,1),(0.5,0,1.33),(1.4,1,1.4),L10N('PROP_TROLLEY'),7)

        self.library = loader.loadModel("data/models/TTC/library.bam")
        self.library.reparentTo(self.np)
        self.library.setPos(91.4475,-44.9255,4)
        self.library.setHpr(180,0,0)
        #self.door('practical','door_double_round_ur',(0.88,0.45,0.38,1),self.library,'library_door_origin')
        self.libraryName = "Library"

        self.bank = loader.loadModel("data/models/TTC/bank.bam")
        self.bank.reparentTo(self.np)
        self.bank.setPos(57.1796,38.6656,4)
        self.bank.setHpr(0,0,0)
        #self.door('practical','door_double_round_ur',(0.88,0.45,0.38,1),self.bank,'bank_door_origin')
        self.baseline(self.bank.find("**/sign_origin"),'MickeyFont.bam',(1,0.662745,0.32549,1),(0,-1.58,0),(2.9,1,3.4),L10N('PROP_BANK'),7)

        self.schoolHouse = loader.loadModel("data/models/TTC/school_house.bam")
        self.schoolHouse.reparentTo(self.np)
        self.schoolHouse.setPos(129.919,-138.445,2.4997)
        self.schoolHouse.setHpr(-140,0,0)
        #self.door('practical','door_double_square_ur',(0.88,0.45,0.38,1),self.schoolHouse,'school_door_origin')
        self.sign('all',self.schoolHouse,'TTC_sign3',(-0.35,0,0.3),(0,0,0),(0.9,1,0.9))
        self.baseline(self.schoolHouse.find("**/sign_origin"),'MickeyFont.bam',(1,0.501961,0,1),(0,1,0),(1.5,1,1.8),L10N('PROP_SCHOOLHOUSE'),7)


        self.clothshop = loader.loadModel("data/models/TTC/clothshopTT.bam")
        self.clothshop.reparentTo(self.np)
        self.clothshop.setPos(106.265,160.831,3)
        self.clothshop.setHpr(-30,0,0)
        #self.door('practical','door_double_clothshop',(0.88,0.45,0.38,1),self.clothshop,'door_origin')
        self.baseline(self.clothshop.find("**/sign_origin"),'MickeyFont.bam',(1,0.611765,0.423529,1),(0,-0.5,0),(1.7,1,1.7),L10N('PROP_CLOTHSTORE'),9)



        self.hall = loader.loadModel("data/models/TTC/toonhall.bam")
        self.hall.reparentTo(self.np)
        self.hall.setPos(116.66,24.29,4)
        self.hall.setHpr(-90,0,-0)
        #self.door('practical','door_double_round_ur',(0.88,0.45,0.38,1),self.hall,'toonhall_door_origin')
        self.baseline(self.hall.find("**/sign_origin"),'MickeyFont.bam',(1,1,0,1),(0.3,0,-1.4),(2.2,1,2.3),L10N('PROP_HALL'),5)



        self.tree1 = loader.loadModel("data/models/TTC/trees.bam").find("**/prop_tree_large_ur")
        self.tree1.reparentTo(self.np)
        self.tree1.setPos(-79.7819,79.5309,0)
        self.tree1.setHpr(135,0,0)

        self.tree2 = loader.loadModel("data/models/TTC/trees.bam").find("**/prop_tree_large_ur")
        self.tree2.reparentTo(self.np)
        self.tree2.setPos(-127.003,30.3763,0)
        self.tree2.setHpr(135,0,0)

        self.tree3 = loader.loadModel("data/models/TTC/trees.bam").find("**/prop_tree_large_ur")
        self.tree3.reparentTo(self.np)
        self.tree3.setPos(-128.16,-24.0245,0.000663757)
        self.tree3.setHpr(135,0,0)

        self.gazebo = loader.loadModel("data/models/TTC/gazebo.bam")
        self.gazebo.reparentTo(self.np)
        self.gazebo.setPos(-60.94,-8.8,-2)
        self.gazebo.setHpr(-178,0,0)

        self.gazebo = loader.loadModel("data/models/TTC/gazebo.bam")
        self.gazebo.reparentTo(self.np)
        self.gazebo.setPos(-60.94,-8.8,-2)
        self.gazebo.setHpr(-178,0,0)

        self.tree4 = loader.loadModel("data/models/TTC/trees.bam").find("**/prop_tree_small_ur")
        self.tree4.reparentTo(self.np)
        self.tree4.setPos(119.621,-127.865,2.49998)
        self.tree4.setHpr(-15,0,0)

        self.tree5 = loader.loadModel("data/models/TTC/trees.bam").find("**/prop_tree_small_ur")
        self.tree5.reparentTo(self.np)
        self.tree5.setPos(127.424,-59.0748,2.5)
        self.tree5.setHpr(-15,0,0)

        self.tree6 = loader.loadModel("data/models/TTC/trees.bam").find("**/prop_tree_small_ur")
        self.tree6.reparentTo(self.np)
        self.tree6.setPos(120.107,-44.4808,2.5)
        self.tree6.setHpr(-15,0,0)

        self.tree7 = loader.loadModel("data/models/TTC/trees.bam").find("**/prop_tree_small_ur")
        self.tree7.reparentTo(self.np)
        self.tree7.setPos(96.8622,-146.373,2.52)
        self.tree7.setHpr(-15,0,0)

        self.tree8 = loader.loadModel("data/models/TTC/trees.bam").find("**/prop_tree_small_ur")
        self.tree8.reparentTo(self.np)
        self.tree8.setPos(114.056,-57.3443,2.5)
        self.tree8.setHpr(-15,0,0)

        self.signDG = loader.loadModel("data/models/TTC/neighborhood_sign_DG.bam")
        self.signDG.reparentTo(self.np)
        self.signDG.setPos(21.3941,-144.665,2.99998)
        self.signDG.setHpr(-35,0,0)
        self.signDG1 = loader.loadModel("data/models/TTC/neighborhood_sign_DG.bam")
        self.signDG1.reparentTo(self.np)
        self.signDG1.setPos(44.1038,-157.906,2.99998)
        self.signDG1.setHpr(148,0,0)

        self.signMM = loader.loadModel("data/models/TTC/neighborhood_sign_MM.bam")
        self.signMM.reparentTo(self.np)
        self.signMM.setPos(-143.503,-8.9528,0.499987)
        self.signMM.setHpr(90,0,0)
        self.signMM1 = loader.loadModel("data/models/TTC/neighborhood_sign_MM.bam")
        self.signMM1.reparentTo(self.np)
        self.signMM1.setPos(-143.242,16.9541,0.499977)
        self.signMM1.setHpr(-90,0,0)

        self.signDD = loader.loadModel("data/models/TTC/neighborhood_sign_DD.bam")
        self.signDD.reparentTo(self.np)
        self.signDD.setPos(-59.1768,92.9836,0.499824)
        self.signDD.setHpr(-9,0,0)
        self.signDD1 = loader.loadModel("data/models/TTC/neighborhood_sign_DD.bam")
        self.signDD1.reparentTo(self.np)
        self.signDD1.setPos(-33.749,88.9499,0.499825)
        self.signDD1.setHpr(170,0,0)

        self.tree9 = loader.loadModel("data/models/TTC/trees.bam").find("**/prop_tree_fat_ur")
        self.tree9.reparentTo(self.np)
        self.tree9.setPos(142.717,108.674,2.49998)
        self.tree9.setHpr(135,0,0)

        self.tree10 = loader.loadModel("data/models/TTC/trees.bam").find("**/prop_tree_fat_ur")
        self.tree10.reparentTo(self.np)
        self.tree10.setPos(6.33804,100.879,2.5)
        self.tree10.setHpr(135,0,0)

        self.tree11 = loader.loadModel("data/models/TTC/trees.bam").find("**/prop_tree_large_ul")
        self.tree11.reparentTo(self.np)
        self.tree11.setPos(-23.998,74.1829,0)
        self.tree11.setHpr(180,0,0)

        self.tree12 = loader.loadModel("data/models/TTC/trees.bam").find("**/prop_tree_fat_ur")
        self.tree12.reparentTo(self.np)
        self.tree12.setPos(103.397,79.4494,2.5)
        self.tree12.setHpr(135,0,0)

        self.tree13 = loader.loadModel("data/models/TTC/trees.bam").find("**/prop_tree_fat_ur")
        self.tree13.reparentTo(self.np)
        self.tree13.setPos(116.09,54.81,2.5)
        self.tree13.setHpr(135,0,0)

        self.bp1 = loader.loadModel("data/models/TTC/big_planter.bam")
        self.bp1.reparentTo(self.np)
        self.bp1.setPos(18.9496,-48.977,4.95856)
        self.bp1.setHpr(-135,0,0)

        self.bp2 = loader.loadModel("data/models/TTC/big_planter.bam")
        self.bp2.reparentTo(self.np)
        self.bp2.setPos(19.2327,52.5553,4.95837)
        self.bp2.setHpr(-135,0,0)

        self.tree14 = loader.loadModel("data/models/TTC/trees.bam").find("**/prop_tree_fat_ul")
        self.tree14.reparentTo(self.np)
        self.tree14.setPos(6.51316,-96.6973,2.49997)
        self.tree14.setHpr(135,0,0)

        self.gagShop = loader.loadModel("data/models/TTC/gagShop_TT.bam")
        self.gagShop.reparentTo(self.np)
        self.gagShop.setPos(-86.6848,-90.5693,0.500015)
        self.gagShop.setHpr(-15,0,0)
        #self.door('practical','door_double_square_ur',(1,0.63,0.38,1),self.gagShop,'door_origin')


        self.wall = loader.loadModel("data/models/TTC/walls.bam")
        self.wall1 = self.wall.find("**/wall_lg_brick_ur")
        self.wall1.reparentTo(self.np)
        self.wall1.setPos(-107.954,-85.0626,-0.18)
        self.wall1.setHpr(150,0,0)
        self.wall1.setSx(15)
        self.wall1.setSz(20)
        self.wall1.setColor(1,0.9,0.33,1)
        self.makeMask(self.wall,self.wall1)
        self.wall = loader.loadModel("data/models/TTC/walls.bam")
        self.wall2 = self.wall.find("**/wall_lg_brick_ur")
        self.wall2.reparentTo(self.np)
        self.wall2.setPos(-94.9639,-92.5626,-0.18)
        self.wall2.setHpr(150,0,0)
        self.wall2.setSx(15)
        self.wall2.setSz(20)
        self.wall2.setColor(0.99,0.89,0.49,1)
        self.makeMask(self.wall,self.wall2)
        self.wall = loader.loadModel("data/models/TTC/walls.bam")
        self.wall3 = self.wall.find("**/wall_lg_brick_ur")
        self.wall3.reparentTo(self.np)
        self.wall3.setPos(-139.693,-54.0363,-0.18)
        self.wall3.setHpr(110,0,0)
        self.wall3.setSx(15)
        self.wall3.setSz(20)
        self.wall3.setColor(1,1,0.59,1)
        self.makeMask(self.wall,self.wall3)
        self.wall = loader.loadModel("data/models/TTC/walls.bam")
        self.wall4 = self.wall.find("**/wall_lg_brick_ur")
        self.wall4.reparentTo(self.np)
        self.wall4.setPos(-139.693,-54.0363,-0.18)
        self.wall4.setHpr(110,0,0)
        self.wall4.setSx(15)
        self.wall4.setSz(20)
        self.wall4.setColor(1,1,0.59,1)
        self.makeMask(self.wall,self.wall4)
        self.wall = loader.loadModel("data/models/TTC/walls.bam")
        self.wall5 = self.wall.find("**/wall_lg_brick_ur")
        self.wall5.reparentTo(self.np)
        self.wall5.setPos(-148.706,-25.452,-0.18)
        self.wall5.setHpr(90,0,0)
        self.wall5.setSx(10)
        self.wall5.setSz(20)
        self.wall5.setColor(0.9,0.56,0.34,1)
        self.makeMask(self.wall,self.wall5)
        self.wall = loader.loadModel("data/models/TTC/walls.bam")
        self.wall6 = self.wall.find("**/wall_lg_brick_ur")
        self.wall6.reparentTo(self.np)
        self.wall6.setPos(-144.824,-39.9409,-0.18)
        self.wall6.setHpr(105,0,0)
        self.wall6.setSx(15)
        self.wall6.setSz(20)
        self.wall6.setColor(0.99,0.89,0.49,1)
        self.makeMask(self.wall,self.wall6)

        self.tree15 = loader.loadModel("data/models/TTC/trees.bam").find("**/prop_tree_fat_ul")
        self.tree15.reparentTo(self.np)
        self.tree15.setPos(-53.7466,-73.3194,0.00999998)
        self.tree15.setHpr(105,0,0)

        self.hq = loader.loadModel("data/models/TTC/hqTT.bam")
        self.hq.reparentTo(self.np)
        self.hq.setPos(24.6425,24.8587,4.00001)
        self.hq.setHpr(135,0,0)
        self.peris = Actor("data/models/TTC/perisMod.bam",{"chan":"data/models/TTC/perisChan.bam"})
        self.peris.reparentTo(self.hq)
        self.peris.setPos(7.17,-7.67,19.07)
        self.peris.setHpr(110,0,0)
        self.peris.setScale(4)
        self.peris.loop('chan')
        self.teles = Actor("data/models/TTC/telesMod.bam",{"chan":"data/models/TTC/telesChan.bam"})
        self.teles.reparentTo(self.hq)
        self.teles.setPos(7.003,0,13.191)
        self.teles.setHpr(168,81,0)
        self.teles.setScale(4)
        self.teles.loop('chan')

        self.pet = loader.loadModel("data/models/TTC/petshopTT.bam")
        self.pet.reparentTo(self.np)
        self.pet.setPos(-124.375,74.3749,0.5)
        self.pet.setHpr(49,0,0)
        #self.door('practical','door_double_round_ur',(1,0.87,0.38,1),self.pet,'door_origin')
        self.baseline(self.pet.find("**/sign_origin"),'MickeyFont.bam',(1,1,0,1),(-0.0715486,0.575594,0),(1.58014,1,2.42354),"PET SHOP",9)

        self.fishs = Actor("data/models/TTC/fishs.bam",{"swim":"data/models/TTC/fishsS.bam"})
        self.fishs.reparentTo(self.pet)
        self.fishs.setScale(1)
        self.fishs.loop('swim')

        self.fence = loader.loadModel("data/models/TTC/wood_fence.bam")
        self.fence.reparentTo(self.np)
        self.fence.setPos(38.282,163.591,2.95929)
        self.fence.setHpr(31,0,0)
        self.fence.setScale(1.18418)

        self.gate = loader.loadModel("data/models/TTC/partyGate_TT.bam")
        self.gate.reparentTo(self.np)
        self.gate.setPos(77.935,-159.939,2.60141)
        self.gate.setHpr(195,0,0)

        self.birds = []
        for i in xrange(3): self.birds.append(loader.loadSfx("data/sounds/TT_bird{0}.mp3".format(i+1)))
        seq = Sequence(Func(self.randomSounds),Wait(1),
                       Func(self.randomSounds),Wait(3),
                       Func(self.randomSounds),Wait(2))
        seq.loop()

        if tp: tp.done()

    def randomSounds(self): random.choice(self.birds).play()

    def __tth_area__(self):
        return {
                'name':self.name,
                'models':self.np,
                'bgm':self.theme,
                'gui':self.frame,
                'speeches':[]
                }

class Dock(Hood):

    def loadRing(self,ring): return loader.loadSfx("data/sounds/{0}.mp3".format(ring))

    def makeSeq(self):
        self.moveBoat1 = self.boat.posInterval(4, (50.1,25,-4))
        self.moveBoat2 = self.boat.hprInterval(4, (120,0,0))
        self.moveBoat3 = self.boat.posHprInterval(4, (8.43079, -26.5, -4), (90,0,0))
        self.moveBoat4 = self.boat.posHprInterval(4, (-33.5692, -26.5, -4), (0,0,0))
        self.moveBoat5 = self.boat.posHprInterval(4, (-50, -10, -4), (0,0,0))
        self.moveBoat6 = self.boat.posHprInterval(4, (-50, 40, -4), (-80,0,0))
        self.moveBoat7 = self.boat.posHprInterval(4, (9.08847, 50.4189, -4), (-80,0,0))
        self.moveBoat8 = self.boat.posHprInterval(4, (60, 25, -4), (-180,0,0))

        self.upEPier = self.EPier.hprInterval(4, (89.9995,-0,-0.000199231))
        self.downEPier = self.EPier.hprInterval(4, (89.9995,-44.2599,-0.000199231))
        self.upWPier = self.WPier.hprInterval(4, (-90.399,-0,-0.185446))
        self.downWPier = self.WPier.hprInterval(4, (-90.399,-47.5673,-0.185446))

        self.seq = Sequence(
                            self.sfxInterval_bell,
                            Parallel(
                                self.sfxInterval_creack,
                                self.upEPier),
                            Wait(8),
                            self.sfxInterval_creack,
                            self.downEPier,
                            self.moveBoat1,
                            self.moveBoat2,
                            self.moveBoat3,
                            self.moveBoat4,
                            Parallel(self.upWPier,
                                     self.sfxInterval_water,
                                     self.sfxInterval_bell,
                                     self.moveBoat5),
                            Wait(8),
                            self.sfxInterval_creack,
                            self.downWPier,
                            self.moveBoat6,
                            self.moveBoat7,
                            self.moveBoat8,
                            )

    def __init__(self,tp=None):
        self.music = "data/sounds/DD_nbrhood.mp3"
        self.name = "AREA_DDK"

        self.sfx_bell = self.loadRing('bell')
        self.sfx_creack = self.loadRing('creack')
        self.sfx_water = self.loadRing('water')

        self.sfxInterval_bell = SoundInterval(self.sfx_bell,loop=0)
        self.sfxInterval_creack = SoundInterval(self.sfx_creack,loop=0)
        self.sfxInterval_water = SoundInterval(self.sfx_water,loop=0)

        self.zoneId = 2000
        newModel = loader.loadModel

        Hood.__init__(self,"data/models/DDK/dd.bam")

        self.av_startpos = (((-60,40,0),(0,0,0)))

        self.environ.setPos(-25,10,0)
        self.environ.setHpr(180,0,0)
        self.environ.reparentTo(self.np)
        self.boat = self.environ.find("**/donalds_boat")
        self.boat.setPos(50.1,25,-4)
        self.boat.setHpr(180,0,0)
        self.EPier = self.environ.find("**/east_pier")
        self.WPier = self.environ.find("**/west_pier")

        signTr = self.placebldg("data/models/TTC/trolleyTT.bam", (-25,-90,5.67), 180).find("**/sign_origin")
        self.baseline(signTr,'MickeyFont.bam',(1,0.737255,0.501961,1),(0.5,0,1.33),(1.4,1,1.4),L10N('PROP_TROLLEY'),7)

        self.ttcTunnel = self.placetun((-198.22,-108.72,-0.975), -34, False)
        Tunnel(self.ttcTunnel, BitMask32(8), self, (TTCentral,'AREA_TTC'))

        self.placetun((164.82,-51.14,-0.975), 90, True)
        self.placetun((-214.99,74.98,-0.975), -90, True)

        self.clothshop = self.placebldg("data/models/TTC/clothshopTT.bam",(-88.0457,115.078,3.25565),45)
        self.baseline(self.clothshop.find("**/sign_origin"),'MickeyFont.bam',(0.701961,0,0,1),(0,0,0),(1.5,1,1.5),L10N('PROP_CLOTHSTORE'),12)
        ##self.door('practical','door_double_clothshop',(0.91,0.34,0.34,1),self.clothshop)

        self.tunnelAA = self.placebldg("data/models/DDK/outdoor.bam", (-53.1974,172.046,3.27967),52.125)

        from funAreas import AcornAcres
        Tunnel(self.tunnelAA,BitMask32(8),self,(AcornAcres,'AREA_ACRES'))

        #self.sign('DD',self.tunnelAA,'DD_sign2',(0,0,0),(0,0,0),(2,1,1.4))
        self.baseline(self.tunnelAA.find("**/sign_origin"),'Comedy.bam',(0.439216,0.247059,0.184314,1),(0,0,0),(1.5,1,1.4),L10N('AREA_ACRES'),12)

        self.gs = self.placebldg("data/models/DDK/gagshop.bam",(-121.761,-24.113,5.66699),-90)
        ##self.door('practical','door_double_square_ur',(1.000,0.737,0.302,1),self.gs)

        self.hq = self.placebldg("data/models/DDK/hq.bam",(-8.4986,104.147,1.66701),-90)

        self.pier1 = newModel("data/models/DDK/pier.bam")
        self.pier1.reparentTo(self.np)
        self.pier1.setPos(-1.79822,139.984,3.59855)
        self.pier1.setHpr(135,0,0)
        self.pier2 = newModel("data/models/DDK/pier.bam")
        self.pier2.reparentTo(self.np)
        self.pier2.setPos(-11.6229,148.498,3.64751)
        self.pier2.setHpr(165,0,0)
        self.pier3 = newModel("data/models/DDK/pier.bam")
        self.pier3.reparentTo(self.np)
        self.pier3.setPos(-23.6427,149.15,3.59725)
        self.pier3.setHpr(-165,0,0)
        self.pier3 = newModel("data/models/DDK/pier.bam")
        self.pier3.reparentTo(self.np)
        self.pier3.setPos(-31.3754,141.368,3.56653)
        self.pier3.setHpr(-135,0,0)

        self.ps = self.placebldg("data/models/TTC/petshopTT.bam", (40.2718,-89.8663,3.28834),-165)
        self.fish = Actor("data/models/DDK/fish-zero.bam",{"swim":"data/models/DDK/fish-swim.bam"})
        self.fish.reparentTo(self.ps)
        self.fish.loop('swim')
        ##self.door('practical','door_double_square_ur',(0.86,0.48,0.23,1),self.ps)
        self.baseline(self.ps.find("**/sign_origin"),'MickeyFont.bam',(1,1,0,1),(0,0.180612,0),(1.51565,1,3.00508),L10N('PROP_PETSHOP'),12)

        self.gate = self.placebldg("data/models/TTC/partyGate_TT.bam", (36.9924,113.67,3.28138), 315)

        #Extras
        self.placelight((-103.41,40.92,5.69),-180)
        self.placelight((-106.95,-41.49,5.67),-165)
        self.placelight((-60.98,-71.34,5.73),-120)
        self.placelight((2.52,-74.03,5.67),-135)
        self.placelight((58.21,-37.67,5.68),45)
        self.placelight((57.15,57.28,5.71),-45)
        self.ch3 = newModel("data/models/DDK/flats.bam").find("**/prop_nets")
        self.ch3.reparentTo(self.np)
        self.ch3.setPos(-122.68,-38.45,5.57)
        self.ch3.setHpr(60,2,0)
        self.ch3.setScale(0.7)
        self.ch4 = newModel("data/models/DDK/crate.bam")
        self.ch4.reparentTo(self.np)
        self.ch4.setPos(-108.75,44.58,5.7)
        self.ch4.setHpr(45,0,0)
        self.ch5 = newModel("data/models/DDK/crate.bam")
        self.ch5.reparentTo(self.np)
        self.ch5.setPos(-108.87,41.47,5.7)
        self.ch5.setHpr(105,0,0)
        self.ch6 = newModel("data/models/DDK/crate.bam")
        self.ch6.reparentTo(self.np)
        self.ch6.setPos(1.33,-75.44,5.71)
        self.ch6.setHpr(105,0,0)
        self.ch6 = newModel("data/models/DDK/crate.bam")
        self.ch6.reparentTo(self.np)
        self.ch6.setPos(-1.26,-72.98,5.8)
        self.ch6.setHpr(60,0,0)
        self.ch7 = newModel("data/models/DDK/crate.bam")
        self.ch7.reparentTo(self.np)
        self.ch7.setPos(-71.17,-77.38,5.65)
        self.ch7.setHpr(90,0,0)
        self.ch8 = newModel("data/models/DDK/crate.bam")
        self.ch8.reparentTo(self.np)
        self.ch8.setPos(-74.57,-74.96,5.69)
        self.ch8.setHpr(45,0,0)
        self.ch9 = newModel("data/models/DDK/flats.bam").find("**/prop_ship_wheel")
        self.ch9.reparentTo(self.np)
        self.ch9.setPos(-79.04,-78.04,5.67)
        self.ch9.setHpr(90,0,0)
        self.ch9.setScale(0.5)
        self.ch10 = newModel("data/models/DDK/crate.bam")
        self.ch10.reparentTo(self.np)
        self.ch10.setPos(61.03,55.59,5.65)
        self.ch10.setHpr(-75,0,0)
        self.ch11 = newModel("data/models/DDK/crate.bam")
        self.ch11.reparentTo(self.np)
        self.ch11.setPos(58.24,51.29,5.7)
        self.ch11.setHpr(-120,0,0)
        self.ch12 = newModel("data/models/DDK/crate.bam")
        self.ch12.reparentTo(self.np)
        self.ch12.setPos(-71.02,-69.91,5.67)
        self.ch12.setHpr(-90,0,0)
        self.ch13 = newModel("data/models/DDK/chimneys.bam").find("**/prop_chimney")
        self.ch13.reparentTo(self.np)
        self.ch13.setPos(77.77,44.8,23.71)
        self.ch13.setHpr(-90,0,0)
        self.ch13.setColor(0.63,0.47,0.24,1)
        self.ch14 = newModel("data/models/DDK/chimneys.bam").find("**/prop_chimney")
        self.ch14.reparentTo(self.np)
        self.ch14.setPos(-6,-94,25)
        self.ch14.setHpr(180,0,0)
        self.ch14.setColor(0.63,0.47,0.24,1)
        self.ch15 = newModel("data/models/DDK/TT.bam")
        self.ch15.reparentTo(self.np)
        self.ch15.setPos(-82.34,-70.8,5.67)
        self.ch15.setHpr(146,0,0)
        self.ch15.setScale(1.5)
        self.ch16 = newModel("data/models/DDK/TT.bam")
        self.ch16.reparentTo(self.np)
        self.ch16.setPos(-107.27,-53.79,5.67)
        self.ch16.setHpr(-35,0,0)
        self.ch16.setScale(1.5)
        self.ch17 = newModel("data/models/DDK/DG.bam")
        self.ch17.reparentTo(self.np)
        self.ch17.setPos(-118.81,-0.75,5.67)
        self.ch17.setHpr(89,0,0)
        self.ch17.setScale(1.5)
        self.ch18 = newModel("data/models/DDK/DG.bam")
        self.ch18.reparentTo(self.np)
        self.ch18.setPos(-118.86,30.91,5.67)
        self.ch18.setHpr(-90,0,0)
        self.ch18.setScale(1.5)
        self.ch19 = newModel("data/models/DDK/BR.bam")
        self.ch19.reparentTo(self.np)
        self.ch19.setPos(69.03,24.96,5.67)
        self.ch19.setHpr(-90,0,0)
        self.ch19.setScale(1.5)
        self.ch20 = newModel("data/models/DDK/BR.bam")
        self.ch20.reparentTo(self.np)
        self.ch20.setPos(68.83,-6.93,5.67)
        self.ch20.setHpr(90,0,0)
        self.ch20.setScale(1.5)
        self.ch21 = newModel("data/models/DDK/palm.bam")
        self.ch21.reparentTo(self.np)
        self.ch21.setPos(-55,115,3.25331)
        self.ch21.setHpr(0,0,0)
        self.ch21.setScale(1.3)
        self.ch22 = newModel("data/models/DDK/palm.bam")
        self.ch22.reparentTo(self.np)
        self.ch22.setPos(-59.7445,135.255,3.30638)
        self.ch22.setHpr(135,0,0)
        self.ch22.setScale(0.7)
        self.ch23 = newModel("data/models/DDK/palm.bam")
        self.ch23.reparentTo(self.np)
        self.ch23.setPos(-100,85,3.2338)
        self.ch23.setHpr(-75,0,0)
        self.ch23.setScale(1.1)
        self.ch24 = newModel("data/models/DDK/palm.bam")
        self.ch24.reparentTo(self.np)
        self.ch24.setPos(64.4875,91.0424,3.25886)
        self.ch24.setHpr(285,0,0)
        self.ch24.setScale(1.1)
        self.ch25 = newModel("data/models/DDK/palm.bam")
        self.ch25.reparentTo(self.np)
        self.ch25.setPos(59.0938,-64.9951,3.29744)
        self.ch25.setHpr(-159,0,0)
        self.ch25.setScale(1.5304)
        self.ch26 = newModel("data/models/DDK/palm.bam")
        self.ch26.reparentTo(self.np)
        self.ch26.setPos(51.4007,-72.6317,3.29744)
        self.ch26.setHpr(-18,0,0)
        self.ch26.setScale(0.8)
        self.ch27 = newModel("data/models/DDK/palm.bam")
        self.ch27.reparentTo(self.np)
        self.ch27.setPos(19.2,-83.3846,3.29744)
        self.ch27.setHpr(91,0,0)
        self.ch27.setScale(1.3)
        self.ch28 = newModel("data/models/DDK/palm.bam")
        self.ch28.reparentTo(self.np)
        self.ch28.setPos(-10.8767,181.675,3.23742)
        self.ch28.setHpr(-120,0,0)
        self.ch28.setScale(1.40798)
        self.ch29 = newModel("data/models/DDK/palm.bam")
        self.ch29.reparentTo(self.np)
        self.ch29.setPos(-15,180,3.23697)
        self.ch29.setHpr(45,0,0)
        self.chw = newModel("data/models/DDK/walls.bam")
        self.ch30 = self.chw.find("**/wall_md_blank_ur")
        self.ch30.reparentTo(self.np)
        self.ch30.setColor(0.42,0.16,0.16,1)
        self.ch30.setPos(-122.3,34.38,5.67)
        self.ch30.setHpr(79,0,0)
        self.ch30.setSx(15)
        self.ch30.setSz(20)
        self.makeMask(self.chw,self.ch30)
        self.chw = newModel("data/models/DDK/walls.bam")
        self.ch31 = self.chw.find("**/wall_md_blank_ur")
        self.ch31.reparentTo(self.np)
        self.ch31.setColor(0.38,0.3,0.18,1)
        self.ch31.setPos(-124.96,-49.96,5.67)
        self.ch31.setHpr(90,0,0)
        self.ch31.setSx(15.6)
        self.ch31.setSz(20)
        self.makeMask(self.chw,self.ch31)
        self.chw = newModel("data/models/DDK/walls.bam")
        self.ch32 = self.chw.find("**/wall_md_board_ur")
        self.ch32.reparentTo(self.np)
        self.ch32.setColor(0.71,0.49,0.35,1)
        self.ch32.setPos(-112.88,-57.6,5.67)
        self.ch32.setHpr(147,0,0)
        self.ch32.setSx(15)
        self.ch32.setSz(20)
        self.makeMask(self.chw,self.ch32)
        self.chw = newModel("data/models/DDK/walls.bam")
        self.ch33 = self.chw.find("**/wall_md_blank_ur")
        self.ch33.reparentTo(self.np)
        self.ch33.setColor(0.42,0.16,0.16,1)
        self.ch33.setPos(-64.61,-90.2,5.67)
        self.ch33.setHpr(146,0,0)
        self.ch33.setSx(20.7)
        self.ch33.setSz(20.3)
        self.makeMask(self.chw,self.ch33)
        self.chw = newModel("data/models/DDK/walls.bam")
        self.ch34 = self.chw.find("**/wall_lg_brick_ur")
        self.ch34.reparentTo(self.np)
        self.ch34.setColor(0.17,0.44,0.28,1)
        self.ch34.setPos(-55,-90,5.67)
        self.ch34.setHpr(-180,0,0)
        self.ch34.setSx(10)
        self.ch34.setSz(20.3)
        self.makeMask(self.chw,self.ch34)
        self.chw = newModel("data/models/DDK/walls.bam")
        self.ch35 = self.chw.find("**/wall_md_blank_ur")
        self.ch35.reparentTo(self.np)
        self.ch35.setColor(0.42,0.16,0.16,1)
        self.ch35.setPos(5.6,-99.86,5.67)
        self.ch35.setHpr(90,0,0)
        self.ch35.setSx(10)
        self.ch35.setSz(20.3)
        self.makeMask(self.chw,self.ch35)
        self.chw = newModel("data/models/DDK/walls.bam")
        self.ch36 = self.chw.find("**/wall_md_blank_ur")
        self.ch36.reparentTo(self.np)
        self.ch36.setColor(0.42,0.16,0.16,1)
        self.ch36.setPos(5.6,-90,5.67)
        self.ch36.setHpr(-180,0,0)
        self.ch36.setSx(15.6)
        self.ch36.setSz(20.3)
        self.makeMask(self.chw,self.ch36)
        self.chw = newModel("data/models/DDK/walls.bam")
        self.ch37 = self.chw.find("**/wall_sm_wood_ur")
        self.ch37.reparentTo(self.np)
        self.ch37.setColor(0.874016,0.610097,0.610097,1)
        self.ch37.setPos(75,60,5.67)
        self.ch37.setHpr(-90,0,0)
        self.ch37.setSx(15)
        self.ch37.setSz(20.3)
        self.makeMask(self.chw,self.ch37)
        self.chw = newModel("data/models/DDK/walls.bam")
        self.ch38 = self.chw.find("**/wall_sm_wood_ur")
        self.ch38.reparentTo(self.np)
        self.ch38.setColor(0.75,0.75,0.75,1)
        self.ch38.setPos(75,45,5.67)
        self.ch38.setHpr(-90,0,0)
        self.ch38.setSx(20)
        self.ch38.setSz(20.3)
        self.makeMask(self.chw,self.ch38)
        self.chw = newModel("data/models/DDK/walls.bam")
        self.ch39 = self.chw.find("**/wall_md_board_ur")
        self.ch39.reparentTo(self.np)
        self.ch39.setColor(0.93,0.15,0.15,1)
        self.ch39.setPos(75,-10,5.67)
        self.ch39.setHpr(-90,0,0)
        self.ch39.setSx(15)
        self.ch39.setSz(20.3)
        self.makeMask(self.chw,self.ch39)
        self.chw = newModel("data/models/DDK/walls.bam")
        self.ch40 = self.chw.find("**/wall_md_blank_ur")
        self.ch40.reparentTo(self.np)
        self.ch40.setColor(0.38,0.31,0.19,1)
        self.ch40.setPos(75,-25,5.67)
        self.ch40.setHpr(-90,0,0)
        self.ch40.setSx(15)
        self.ch40.setSz(20.5)
        self.makeMask(self.chw,self.ch40)
        self.chw = newModel("data/models/DDK/walls.bam")
        self.ch41 = self.chw.find("**/wall_md_blank_dr")
        self.ch41.reparentTo(self.np)
        self.ch41.setColor(0.384314,0.305635,0.187618,1)
        self.ch41.setPos(-124,-14.56,5.67)
        self.ch41.setHpr(90,0,0)
        self.ch41.setSx(10)
        self.ch41.setSz(20.3)
        self.makeMask(self.chw,self.ch41)
        self.chw = newModel("data/models/DDK/walls.bam")
        self.ch42 = self.chw.find("**/wall_sm_wood_ur")
        self.ch42.reparentTo(self.np)
        self.ch42.setColor(0.874016,0.610097,0.610097,1)
        self.ch42.setPos(90,60,5.67)
        self.ch42.setHpr(180,0,0)
        self.ch42.setSx(15)
        self.ch42.setSz(20.3)
        self.makeMask(self.chw,self.ch42)
        self.chw = newModel("data/models/DDK/walls.bam")
        self.ch43 = self.chw.find("**/wall_md_blank_ur")
        self.ch43.reparentTo(self.np)
        self.ch43.setColor(0.42,0.16,0.16,1)
        self.ch43.setPos(-119.44,49.1,5.67)
        self.ch43.setHpr(165,0,0)
        self.ch43.setSx(15)
        self.ch43.setSz(20.3)
        self.makeMask(self.chw,self.ch43)
        self.chw = newModel("data/models/DDK/walls.bam")
        self.ch44 = self.chw.find("**/wall_lg_brick_ur")
        self.ch44.reparentTo(self.np)
        self.ch44.setColor(0.17,0.44,0.28,1)
        self.ch44.setPos(-10,-90,5.67)
        self.ch44.setHpr(-180,0,0)
        self.ch44.setSx(15)
        self.ch44.setSz(20.3)
        self.makeMask(self.chw,self.ch44)
        self.chw = newModel("data/models/DDK/walls.bam")
        self.ch45 = self.chw.find("**/wall_md_blank_ur")
        self.ch45.reparentTo(self.np)
        self.ch45.setColor(0.38,0.31,0.19,1)
        self.ch45.setPos(75,-40,5.67)
        self.ch45.setHpr(0,0,0)
        self.ch45.setSx(15)
        self.ch45.setSz(20.3)
        self.ch45.setColor(255,255,255)
        self.makeMask(self.chw,self.ch45)

        self.makeSeq()

        if tp: tp.done()

    def __tth_area__(self):
        return {
                'name':self.name,
                'models':self.np,
                'bgm':self.theme,
                'gui':self.frame,
                'speeches':[]
                }