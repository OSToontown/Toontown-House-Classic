from __init__ import Area, Tunnel

from panda3d.core import Vec4, TextureStage, Texture, TransparencyAttrib, CollisionTraverser, CollisionNode
from panda3d.core import CollisionHandlerQueue, CollisionRay, BitMask32, RenderAttrib, AlphaTestAttrib
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *
from direct.actor.Actor import *

class Hood(Area):
    def __init__(self,*a,**k):
        Area.__init__(self,*a,**k)

    def makeMask(self,wall,parent):
        toMask = wall.find("**/wall_collide")
        toMask.node().setFromCollideMask(BitMask32(8))
        toMask.reparentTo(parent)

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

    def placewall(self, pos, type, h, width, height, color):
        wallm = loader.loadModel("data/models/streets/walls.bam")
        wall = wallm.find("**/"+type)
        wall.reparentTo(self.np)
        wall.setPos(pos)
        wall.setH(h)
        wall.setSz(height)
        wall.setSx(width)
        wall.setColor(color)
        toMask = wallm.find("**/wall_collide")
        toMask.node().setFromCollideMask(BitMask32(8))
        toMask.reparentTo(wall)
        return wall

    def placetree_TT(self, type, pos, arg):
        if arg == 1:
            tree = loader.loadModel('data/models/TTC/trees.bam').find('**/'+type)
        elif arg == 2:
            tree = loader.loadModel('data/models/TTC/winter_trees.bam').find('**/'+type)
        tree.reparentTo(self.np)
        tree.setPos(pos)
        return tree

    def placelight_TT(self, type, pos, hpr, arg):
        if arg == 1:
            light = loader.loadModel('data/models/TTC/streetlight_TT.bam').find('**/'+type)
        elif arg == 2:
            light = loader.loadModel('data/models/TTC/winter_streetlight_TT.bam').find('**/'+type)
        light.reparentTo(self.np)
        light.setPos(pos)
        light.setHpr(hpr)
        return light

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

        Hood.__init__(self,"data/models/TTC/ttc.bam") #recomp causes texture problems for me #can you recompile it for yourself?

        self.sky = loader.loadModel("data/models/TTC/TT_sky.bam")
        self.sky.reparentTo(self.np)
        self.environ.reparentTo(self.sky)

        self.placebldg("data/models/TTC/gazebo.bam", (10.8,-59.9,-2), -268) #thanks to JuniorCog for the positions

        tr = self.placebldg("data/models/TTC/trolleyTT.bam", (83.15,-118.85,0.4), 218.5)
        #for m in tr.findAllMatches("**/tunn*"): m.removeNode()

        self.placebldg("data/models/TTC/toonhall.bam", (-29.1796,27.6656,4), -360)
        self.placebldg("data/models/TTC/library.bam", (45.9,93,4), 270)
        self.placebldg("data/models/TTC/bank.bam", (-36.1796,58.6656,4), -270)
        self.placebldg("data/models/TTC/school_house.bam", (-66,-126,0), 135)
        self.placebldg("data/models/TTC/gagShop_TT.bam", (93,-89,0.4), 800)
        self.placebldg("data/models/TTC/clothshopTT.bam", (-118,125,2), 25)
        self.placebldg("data/models/TTC/petshopTT.bam", (-167,88,3), 80)
        self.placebldg("data/models/TTC/hqTT.bam", (-29.1796,27.6656,4), 225)
        self.placebldg("data/models/TTC/partyGate_TT.bam", (154,95,2.60), -55)
        self.placebldg("data/models/TTC/big_planter.bam", (-50,21,5), 0)
        self.placebldg("data/models/TTC/big_planter.bam", (50,21,5), 0)
        self.placebldg("data/models/TTC/fountain.bam", (3,63,4), 0)
        self.placebldg("data/models/TTC/mickey_on_horse.bam", (-121,77,2), 0)
        self.speedwayTun = self.placebldg("data/models/TTC/Speedway_Tunnel.bam", (-172,22,3), 305)

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

        self.placewall((87.6,-111.073,0.5),"wall_lg_brick_ur",-119,10,9,(0.5, 0.9, 0.33, 1))
        self.placewall((87.6,-111.073,10.5),"wall_lg_brick_ur",-119,10,9,(0.5, 0.9, 0.33, 1))
        self.placewall((91.77,-103.573,0.5),"wall_sm_cement_ur",-119,20,9,1)
        self.placewall((95.94,-96.073,0.5),'wall_md_dental_ul',-119,10,9,(1, 0.9, 0.33, 1)
        self.placewall((95.94,-96.073,10.5),"wall_md_dental_ul",-119,10,9,(1, 0.9, 0.33, 1))
        self.placewall((59.69,-137.525,0.5),'wall_md_pillars_ul',198,20,19,(1, 0.9, 0.33, 1))

        self.setHolidayProps("Christmas")

        if tp: tp.done()

    def decorationProps(self, arg):
        if arg == 1:
            ropes = loader.loadModel('data/models/TTC/ropes.bam')
            ropes.reparentTo(self.np)
            ropes.setPos(109,68,2.5)
            ropes.setScale(0.75)
            gear = loader.loadModel("data/models/TTC/gearProp.bam")
            gear.reparentTo(self.np)
            gear.setPos(109,68,11.5)
            gear.hprInterval(15.0, Vec3(0, 360, 0), Vec3(-720, 0, -720)).loop()
            gear.setColorScale(0.6, 0.6, 1.0, 1.0)
            gear2 = loader.loadModel("data/models/TTC/gearProp.bam")
            gear2.reparentTo(self.np)
            gear2.setScale(0.3)
            gear2.setPos(109,68,11.5)
            gear2.hprInterval(15.0, Vec3(0, -720, 0), Vec3(360, 0, 360)).loop()
            gear2.setColorScale(0.6, 0.6, 1.0, 1.0)
        elif arg == 2:
            tree = loader.loadModel("data/models/TTC/winter_tree_Christmas.bam")
            tree.reparentTo(self.np)
            tree.setPos(109,68,2.5)

    def setHolidayProps(self, holiday):
        if holiday == None:
            self.placetree_TT('prop_tree_fat_no_box_ur',(-100,5,2.5),1)
            self.placetree_TT('prop_tree_fat_no_box_ur',(100,5,2.5),1)
            self.placetree_TT('prop_tree_large_no_box_ul',(-81,-73,0.2),1)
            self.placetree_TT('prop_tree_large_no_box_ul',(-48,-123,0.2),1)
            self.placetree_TT('prop_tree_large_no_box_ul',(21,-128,0.2),1)
            self.placetree_TT('prop_tree_small_no_box_ul',(47,121,2.5),1)
            self.placetree_TT('prop_tree_small_no_box_ul',(65,130,2.5),1)
            self.placetree_TT('prop_tree_small_no_box_ul',(59,117,2.5),1)
            self.placetree_TT('prop_tree_fat_no_box_ur',(-77,121,2.5),1)
            self.placelight_TT('prop_post_three_light',(72,-100,0.5),60,1)
            self.placelight_TT('prop_post_three_light',(42,-128,0.5),60,1)
            self.placelight_TT('prop_post_three_light',(88.5,45.3,3),0,1)
            self.placelight_TT('prop_post_three_light',(88.5,78.5,3),0,1)
            self.placelight_TT('prop_post_three_light',(-93,95,3),0,1)
            self.placelight_TT('prop_post_three_light',(-93,58.5,3),0,1)
            self.placelight_TT('prop_post_one_light',(23,105,4),0,1)
            self.placelight_TT('prop_post_one_light',(-23,105,4),0,1)
            self.placelight_TT('prop_post_one_light',(60,31,4),0,1)
            self.placelight_TT('prop_post_one_light',(-60,31,4),0,1)
            self.placelight_TT('prop_post_sign',(-53,-132,0.5),60,1)
            self.decorationProps(1)
        elif holiday == "Christmas":
            self.placetree_TT('prop_tree_fat_no_box_ur',(-100,5,2.5),2)
            self.placetree_TT('prop_tree_fat_no_box_ur',(100,5,2.5),2)
            self.placetree_TT('prop_tree_large_no_box_ul',(-81,-73,0.2),2)
            self.placetree_TT('prop_tree_large_no_box_ul',(-48,-123,0.2),2)
            self.placetree_TT('prop_tree_large_no_box_ul',(21,-128,0.2),2)
            self.placetree_TT('prop_tree_small_no_box_ul',(47,121,2.5),2)
            self.placetree_TT('prop_tree_small_no_box_ul',(65,130,2.5),2)
            self.placetree_TT('prop_tree_small_no_box_ul',(59,117,2.5),2)
            self.placetree_TT('prop_tree_fat_no_box_ur',(-77,121,2.5),2)
            self.placelight_TT('prop_post_three_light',(72,-100,0.5),60,2)
            self.placelight_TT('prop_post_three_light',(42,-128,0.5),60,2)
            self.placelight_TT('prop_post_three_light',(88.5,45.3,3),0,2)
            self.placelight_TT('prop_post_three_light',(88.5,78.5,3),0,2)
            self.placelight_TT('prop_post_three_light',(-93,95,3),0,2)
            self.placelight_TT('prop_post_three_light',(-93,58.5,3),0,2)
            self.placelight_TT('prop_post_one_light',(23,105,4),0,2)
            self.placelight_TT('prop_post_one_light',(-23,105,4),0,2)
            self.placelight_TT('prop_post_one_light',(60,31,4),0,2)
            self.placelight_TT('prop_post_one_light',(-60,31,4),0,2)
            self.placelight_TT('prop_post_sign',(-53,-132,0.5),60,2)
            self.decorationProps(2)

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

    def makeSeq(self,t):
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
        self.seq.loop()
        self.seq.setT(t)

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
        self.baseline(signTr,'MickeyFont.bam',(1,0.737255,0.501961,1),(0.5,0,1.33),(1.4,1,1.4),'Trolley Games',7)

        self.ttcTunnel = self.placetun((-198.22,-108.72,-0.975), -34, False)
        Tunnel(self.ttcTunnel, BitMask32(8), self, (TTCentral,'AREA_TTC'))

        self.placetun((164.82,-51.14,-0.975), 90, True)
        self.placetun((-214.99,74.98,-0.975), -90, True)

        self.clothshop = self.placebldg("data/models/TTC/clothshopTT.bam",(-88.0457,115.078,3.25565),45)
        self.baseline(self.clothshop.find("**/sign_origin"),'MickeyFont.bam',(0.701961,0,0,1),(0,0,0),(1.5,1,1.5),"Clothing Store",12)
        #self.door('practical','door_double_clothshop',(0.91,0.34,0.34,1),self.clothshop)

        self.tunnelAA = self.placebldg("data/models/DDK/outdoor.bam", (-53.1974,172.046,3.27967),52.125)

        from funAreas import AcornAcres
        Tunnel(self.tunnelAA,BitMask32(8),self,(AcornAcres,'AREA_ACRES'))

        #self.sign('DD',self.tunnelAA,'DD_sign2',(0,0,0),(0,0,0),(2,1,1.4))
        self.baseline(self.tunnelAA.find("**/sign_origin"),'Comedy.bam',(0.439216,0.247059,0.184314,1),(0,0,0),(1.5,1,1.4),"Acorn Acres",12)

        self.gs = self.placebldg("data/models/TTC/gagShop_TT.bam",(-121.761,-24.113,5.66699),-90)
        #self.door('practical','door_double_square_ur',(1.000,0.737,0.302,1),self.gs)

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
        #self.door('practical','door_double_square_ur',(0.86,0.48,0.23,1),self.ps)
        self.baseline(self.ps.find("**/sign_origin"),'MickeyFont.bam',(1,1,0,1),(0,0.180612,0),(1.51565,1,3.00508),"Pet Shop",12)

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

        if tp: tp.done()

    def playSfx(self,sfxe):
        self.sfxx = loader.loadMusic("data/sounds/{0}.mp3".format(sfxe))
        self.sfxx.play()

    def door(self,arg,door,color,parent):
        self.doorx = loader.loadModel("data/models/DDK/doors_{0}.bam".format(arg)).find("**/"+door)
        self.doorx.reparentTo(parent.find("**/door_origin"))
        self.doorx.setColor(color)
        self.doorx.setY(-.2)

    def __tth_area__(self):
        return {
                'name':self.name,
                'models':self.np,
                'bgm':self.theme,
                'gui':self.frame,
                'speeches':[]
                }