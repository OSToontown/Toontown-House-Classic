from __init__ import Area, Tunnel

from panda3d.core import *
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *
from direct.actor.Actor import *
import random
from tth.fishing.FishingHandler import *

from tth.effects.FireworkShow import *

from tth.misc.HolidayManager import *

import streets

from pandac.PandaModules import *
from direct.showbase.InputStateGlobal import inputState
from direct.showbase.DirectObject import DirectObject

class Hood(Area):

    PREFIX2PHASE = {
                    'TT':'4',
                    'TTC':'4',

                    'DD':'6',
                    'DG':'8',
                    'MM':'6',
                    'BR':'8',
                    'DL':'8',
                    }

    def __init__(self,*a,**kw):
        Area.__init__(self,*a,**kw)
        self.haveFires = False

    def startFires(self):
        self.haveFires = True
        color = LerpColorInterval(self.sky,3,Vec4(0,0,0,1))
        color.start()
        self.startFireworks()

    def restartSky2Theme(self):
        self.haveFires = False
        self.sky.setColor(255,255,255)
        self.newtheme.stop()
        self.theme.play()

    def startFireworks(self):
        self.theme.stop()
        self.newtheme = loader.loadMusic("data/sounds/fireworks.mp3")
        self.newtheme.play()
        self.lnch = loader.loadSfx("data/sounds/rocket_launch.mp3")
        self.lnch.play()
        seq = Sequence()
        seq.append(Wait(4)) #-_- can't you create one sequence?
        seq.append(Func(self.firework,(0,-270,50)))
        seq.append(Wait(3))
        seq.append(Func(self.hideRocket))
        seq.append(Func(self.firework,(50,-270,50)))
        seq.append(Wait(2))
        seq.append(Func(self.firework,(100,270,50)))
        seq.append(Wait(4))
        seq.append(Func(self.firework,(0,270,50)))
        seq.append(Wait(1))
        seq.append(Func(self.firework,(110,270,50)))
        seq.append(Wait(3))
        seq.append(Func(self.firework,(-250,270,50)))
        seq.append(Wait(1))
        seq.append(Func(self.firework,(250,270,50)))
        seq.append(Wait(3))
        seq.append(Func(self.firework,(0,-270,50)))
        seq.append(Wait(2))
        seq.append(Func(self.firework,(80,270,50)))
        seq.append(Wait(4))
        seq.append(Func(self.firework,(250,270,50)))
        seq.append(Wait(6))
        seq.append(Func(self.firework,(-250,270,50)))
        seq.append(Wait(2))
        seq.append(Func(self.firework,(0,-270,50)))
        seq.append(Wait(2))
        seq.append(Func(self.firework,(80,270,50)))
        seq.append(Wait(3))
        seq.append(Func(self.firework,(-250,270,50)))
        seq.append(Wait(2))
        seq.append(Func(self.firework,(250,-270,50)))
        seq.append(Wait(2))
        seq.append(Func(self.firework,(80,270,50)))
        seq.append(Wait(2))
        seq.append(Func(self.firework,(0,-270,50)))
        seq.append(Wait(4))
        seq.append(Func(self.firework,(-250,270,50)))
        seq.append(Wait(2))
        seq.append(Func(self.firework,(80,270,50)))
        seq.append(Wait(3))
        seq.append(Func(self.firework,(80,270,50)))
        seq.append(Wait(5))
        seq.append(Func(self.firework,(0,-270,50)))
        seq.append(Wait(1))
        seq.append(Func(self.restartSky2Theme))
        seq.start() #why this t .-.

    def firework(self,pos):
        FireworkShow(pos)

    def enterTrolley(self,entry):
        try:
            assert not base.isCompiled
            self.trolleyMgr.d_requestBoard(base.cr.doIdBase)
        except:
            pass

    def door(self,doors,type,color,parent):
        door = loader.loadModel("phase_3.5/models/modules/doors_{0}.bam".format(doors)).find('**/'+type)
        door.reparentTo(parent)
        door.setColor(color)
        return door

    def baseline(self,parent,font,color,pos,scale,textx,ww):
        fonto = loader.loadFont("phase_3/models/fonts/{0}".format(font))
        frame = DirectFrame(frameColor=(0,0,0,0),parent=parent)
        frame.setY(-.2)
        self.text = OnscreenText(text=textx,font=fonto,pos=pos,scale=scale,parent=frame,fg=color,wordwrap=ww)

    def placelight(self,pos,h):
        l = loader.loadModel("phase_3.5/models/props/streetlight_TT.bam")
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

    def placetun(self, pos, h, sign = False, hood = 'TT'):
        tunnel = loader.loadModel("phase_{0}/models/modules/safe_zone_tunnel_{1}.bam".format(self.PREFIX2PHASE[hood],hood))
        tunnel.reparentTo(self.np)
        tunnel.setPos(pos)
        tunnel.setH(h)
        if sign:
            sign = loader.loadModel("phase_4/models/props/construction_sign.bam")
            sign.reparentTo(tunnel.find("**/sign_origin"))
            sign.setPos(0,0,-17)
            sign.find("**/sign_board").setPos(0,0,-0.25)
            sign.find("**/p7_3").setPos(0,0,-0.25)
            sign.find("**/stand").setPos(0,0,-0.15)

        return tunnel

    def placesign(self, x, y, z, h, full = False):
        sign = loader.loadModel("phase_4/models/props/construction_sign.bam")
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
        sign = loader.loadModel("phase_{0}/models/props/signs_{1}.bam".format(self.PREFIX2PHASE[nbr],nbr)).find("**/"+sign)
        sign.reparentTo(parent.find("**/sign_origin"))
        sign.setPos(pos)
        sign.setHpr(hpr)
        sign.setScale(scale)
        return sign

    def makeMask(self,wall,parent):
        toMask = wall.find("**/wall_collide")
        toMask.node().setFromCollideMask(BitMask32(8))
        toMask.reparentTo(parent)

    def placewall(self, pos, type, h, width, height, color):
        wallm = loader.loadModel("phase_3.5/models/modules/walls.bam")
        wall = wallm.find("**/"+type)
        wall.reparentTo(self.np)
        wall.setPos(pos)
        wall.setH(h)
        wall.setSz(height)
        wall.setSx(width)
        wall.setColor(color)
        self.makeMask(wallm,wall)
        return wall

    def placelight_TT(self, type, pos, h, arg):
        if arg == 1:
            light = loader.loadModel('phase_3.5/models/props/streetlight_TT.bam').find('**/'+type)
        elif arg == 2:
            light = loader.loadModel('phase_3.5/models/props/tt_m_ara_TT_streetlight_winter.bam').find('**/'+type)
        light.reparentTo(self.np)
        light.setPos(pos)
        light.setH(h)
        return light

    def placetree_TT(self, type, pos, h, arg=1):
        if arg == 1:
            tree = loader.loadModel('phase_3.5/models/props/trees.bam').find('**/'+type)
        elif arg == 2:
            tree = loader.loadModel('phase_3.5/models/props/winter_trees.bam').find('**/'+type)
        tree.reparentTo(self.np)
        tree.setPos(pos)
        tree.setH(h)
        return tree

    def placetree_FF(self, x, y):
        tree = loader.loadModel('phase_14/models/modules/tree_FF.bam')
        tree.reparentTo(self.np)
        tree.setPos(x,y,0)
        return tree

    def placefence_FF(self, pos, h):
        fence = loader.loadModel('phase_5.5/models/estate/terrain_fence.bam')
        fence.reparentTo(self.np)
        fence.setPos(pos)
        fence.setH(h)
        fence.setScale(0.75)
        return fence

    def addCollisionSphere(self,pos,scale):
        CS = self.np.attachNewNode(CollisionNode('colNode'))
        CS.node().addSolid(CollisionSphere(pos,scale))

class TTCentral(Hood,HolidayManager):
    name = "AREA_TTC"
    zoneId = 1000
    music = "phase_4/audio/bgm/TC_nbrhood.mid"

    def __init__(self,tp=None):
        self.av_startpos = (
                            ((113.385, 123.432, 0.221016),(44.7238, 0, 0)),
                            ((117.516, 144.381, 1.01667),(-1.27803, 0, 0)),
                            ((86.847, 72.4855, -2.96953),(-139.41, 0, 0)),
                            ((71.9911, 52.8175, -0.90902),(-304.261, 0, 0)),
                            ((14.6187, 78.9323, -0.484146),(-317.732, 0, 0)),
                            ((-29.663, 116.255, -0.484157),(-525.121, 0, 0)),
                            )

        Hood.__init__(self,"phase_4/models/neighborhoods/toontown_central.bam")

        self.getCurrHoliday()
        self.printHoliday()

        self.sky = loader.loadModel("phase_3.5/models/props/TT_sky.bam")
        self.sky.reparentTo(self.np)
        self.sky.setScale(2)
        self.skyFog = Fog("Sky Fog")
        self.skyFog.setExpDensity(0.001)
        self.sky.setFog(self.skyFog)

        lerper = NodePath('lerper')
        self.sky.find('**/cloud1').setTexProjector(TextureStage.getDefault(), NodePath(), lerper)
        lerper.posInterval(200, VBase3(-1, 0, 0)).loop()

        lerper = NodePath('lerper')
        self.sky.find('**/cloud2').setTexProjector(TextureStage.getDefault(), NodePath(), lerper)
        lerper.posInterval(200, VBase3(-1, 0, 0)).loop()

        self.environ.reparentTo(self.np)
        self.environ.find('**/hill').removeNode()
        self.environ.find('**/base_grass').setScale(1.5)
        self.bd = loader.loadModel("phase_6/models/karting/GasolineAlley_TT.bam")
        self.backdrop = self.bd.find('**/environment_background')
        self.backdrop.reparentTo(self.environ)
        self.backdrop.setScale(1.2,1.2,1)
        self.backdrop.setPos(-70,50,0)
        self.backdrop.setHpr(45,0,0)
        self.fence7 = loader.loadModel('phase_3.5/models/modules/wood_fence.bam')
        self.fence7.reparentTo(self.environ)
        self.fence7.setPos(22.36,-148.113,0.5)
        self.fence7.setH(723.5)

        if self.getSpecialEvent() == "Fireworks":
            self.startFires()

        self.tunnel1 = self.placetun((-56.6, -238, -6.3), 360, False)
        self.sign1 = loader.loadModel("phase_3.5/models/props/tunnel_sign_orange.bam")
        self.sign1.reparentTo(self.tunnel1.find("**/sign_origin"))
        self.sign1.setPosHprScale(0,-.1,0, 0,0,0, 1.5,1,1.5)
        self.icon1 = loader.loadModel("phase_3.5/models/props/mickeySZ.bam")
        self.icon1.reparentTo(self.sign1.find("**/g1"))
        self.icon1.setPos(0,-.1,1.6)
        self.icon1.setScale(1.9)
        self.baseline(self.sign1,'MickeyFont.bam',(0,0.501961,0,1),(0,-1,0),(1.1,1,.9),"Loopy Lane Toontown Central",12)

        self.tunnel2 = self.placetun((209,-65,-3.7), 420, False)
        self.sign2 = loader.loadModel("phase_3.5/models/props/tunnel_sign_orange.bam")
        self.sign2.reparentTo(self.tunnel2.find("**/sign_origin"))
        self.sign2.setPosHprScale(0,-.1,0, 0,0,0, 1.5,1,1.5)
        self.icon2 = loader.loadModel("phase_3.5/models/props/mickeySZ.bam")
        self.icon2.reparentTo(self.sign2.find("**/g1"))
        self.icon2.setPos(0,-.1,1.6)
        self.icon2.setScale(1.9)
        self.baseline(self.sign2,'MickeyFont.bam',(0,0.501961,0,1),(0,-1,0),(1.1,1,.9),"Silly Street Toontown Central",12)

        self.tunnel3 = self.placetun((-176,32,-6.3), 261, False)
        Tunnel(self.tunnel3,BitMask32(8),self,(Dock,'AREA_DDK'))
        self.sign3 = loader.loadModel("phase_3.5/models/props/tunnel_sign_orange.bam")
        self.sign3.reparentTo(self.tunnel3.find("**/sign_origin"))
        self.sign3.setPosHprScale(0,-.1,0, 0,0,0, 1.5,1,1.5)
        self.icon3 = loader.loadModel("phase_3.5/models/props/mickeySZ.bam")
        self.icon3.reparentTo(self.sign3.find("**/g1"))
        self.icon3.setPos(0,-.1,1.6)
        self.icon3.setScale(1.9)
        self.baseline(self.sign3,'MickeyFont.bam',(0,0.501961,0,1),(0,-1,0),(1.1,1,.9),"Punchline Place Toontown Central",14)

        self.speedway = self.placebldg("phase_4/models/modules/Speedway_Tunnel.bam", (-172,22,3), 305)

        self.baseline(self.speedway.find("**/sign_origin"),'MickeyFont.bam',(0.00392157,0.403922,0.803922,1),(0.57014,-3.391417,0),(2.67969,2.5,2.12201),L10N('AREA_SPEEDWAY'),7)
        self.baseline(self.speedway.find("**/sign_origin"),'MickeyFont.bam',(0.00392157,0.803922,0.403922,1),(2.17014,0.591417,0),(1.67969,1.5,2.12201),'Toontown House',7)

        self.trolley = self.placebldg("phase_4/models/modules/trolley_station_TT.bam", (83.15,-118.85,0.4), 218.5)

        trolleyNp = self.trolley.find('**/trolley_sphere')
        trolleyNode = trolleyNp.node()
        trolleyNode.setCollideMask(BitMask32(8))

        self.collDict = self.collDict if hasattr(self,"collDict") else {}
        self.collDict[trolleyNode] = self.enterTrolley

        self.baseline(self.trolley.find("**/sign_origin"),'MickeyFont.bam',(0.992157,0.968627,0.00784314,1),(0.5,0,1.33),(1.4,1,1.4),L10N('PROP_TROLLEY'),7)

        self.building1 = Actor("phase_5/models/char/tt_r_ara_ttc_B2.bam",{"dance":"phase_5/models/char/tt_a_ara_ttc_B2_dance.bam"})
        self.building1.reparentTo(self.np)
        self.building1.loop("dance")
        self.building1.setPos(37,-143,0)
        self.building1.setH(553)
        self.loony = self.sign('TTC',self.building1,'TTC_sign2',(-0.35,0,-1.3),(0,0,0),(0.9,1,0.7))
        self.baseline(self.loony,'MickeyFont.bam',(1,0.501961,0,1),(0,-0.4,0),(1.5,1.8,1.8),"Loony Labs",7)
        self.loony.setR(10)
        self.rock1 = self.loony.hprInterval(1,(0,0,-10))
        self.rock2 = self.loony.hprInterval(1,(0,0,8))
        self.rock = Sequence(self.rock1,self.rock2)
        self.rock.loop()

        self.library = self.placebldg("phase_4/models/modules/library.bam", (45.9,93,4), 270)
        self.door('practical','door_double_round_ur',(0.88,0.45,0.38,1),self.library.find('**/library_door_origin'))
        self.libraryName = "Library"

        self.bank = self.placebldg("phase_4/models/modules/bank.bam", (-36.1796,58.6656,4), -270)
        self.door('practical','door_double_round_ur',(0.88,0.45,0.38,1),self.bank.find("**/bank_door_origin"))
        self.baseline(self.bank.find("**/sign_origin"),'MickeyFont.bam',(1,0.662745,0.32549,1),(0,-1.58,0),(2.9,1.7,3.4),L10N('PROP_BANK'),7)

        self.schoolHouse = self.placebldg("phase_4/models/modules/school_house.bam", (-66,-126,0), 135)
        self.door('practical','door_double_square_ur',(0.88,0.45,0.38,1),self.schoolHouse.find("**/school_door_origin"))
        self.sign('TTC',self.schoolHouse,'TTC_sign3',(-0.45,0,0.3),(0,0,0),(0.9,1,0.9))
        self.baseline(self.schoolHouse.find("**/sign_origin"),'MickeyFont.bam',(1,0.501961,0,1),(-0.35,1,0),(1.5,1,1.8),L10N('PROP_SCHOOLHOUSE'),7)

        self.clothshop = self.placebldg("phase_4/models/modules/clothshopTT.bam", (-118,125,2), 25)
        self.baseline(self.clothshop.find("**/sign_origin"),'MickeyFont.bam',(1,0.611765,0.423529,1),(0,-0.5,0),(1.7,1.6,1.7),L10N('PROP_CLOTHSTORE'),9)
        self.door('practical','door_double_clothshop',(0.91,0.34,0.34,1),self.clothshop.find('**/door_origin'))

        self.hall = self.placebldg("phase_4/models/modules/toonhall.bam", (-22.1796,119.6656,4.03), -360)
        self.door('practical','door_double_round_ur',(0.88,0.45,0.38,1),self.hall.find("**/toonhall_door_origin"))
        self.baseline(self.hall.find("**/sign_origin"),'MickeyFont.bam',(1,1,0,1),(0.3,-0.75,-1.4),(2.2,1.7,2.3),"Flippy\'s ToonHall",6)

        self.placebldg("phase_4/models/modules/gazebo.bam", (10.8,-59.9,-2), -268)

        self.signDG = loader.loadModel("phase_4/models/props/neighborhood_sign_DG.bam")
        self.signDG.reparentTo(self.tunnel2.find("**/sign_origin"))
        self.signDG.setPos(-13,-1.5,-17.35)
        self.signDG.setHpr(0,0,0)
        self.signDG1 = loader.loadModel("phase_4/models/props/neighborhood_sign_DG.bam")
        self.signDG1.reparentTo(self.tunnel2.find("**/sign_origin"))
        self.signDG1.setPos(13,-1.5,-17.35)
        self.signDG1.setHpr(180,0,0)

        self.signDD = loader.loadModel("phase_4/models/props/neighborhood_sign_DD.bam")
        self.signDD.reparentTo(self.tunnel3.find("**/sign_origin"))
        self.signDD.setPos(-13,-1.5,-17.35)
        self.signDD.setHpr(0,0,0)
        self.signDD1 = loader.loadModel("phase_4/models/props/neighborhood_sign_DD.bam")
        self.signDD1.reparentTo(self.tunnel3.find("**/sign_origin"))
        self.signDD1.setPos(13,-1.5,-17.35)
        self.signDD1.setHpr(180,0,0)

        self.signMM = loader.loadModel("phase_4/models/props/neighborhood_sign_MM.bam")
        self.signMM.reparentTo(self.tunnel1.find("**/sign_origin"))
        self.signMM.setPos(-13,-1.5,-17.35)
        self.signMM.setHpr(0,0,0)
        self.signMM1 = loader.loadModel("phase_4/models/props/neighborhood_sign_MM.bam")
        self.signMM1.reparentTo(self.tunnel1.find("**/sign_origin"))
        self.signMM1.setPos(13,-1.5,-17.35)
        self.signMM1.setHpr(180,0,0)

        self.pier1 = loader.loadModel("phase_4/models/props/piers_tt.bam")
        self.pier1.reparentTo(self.np)
        self.pier1.setPos(-33,-57,-3.59855)
        self.pier1.setHpr(210,0,0)
        self.pier2 = loader.loadModel("phase_4/models/props/piers_tt.bam")
        self.pier2.reparentTo(self.np)
        self.pier2.setPos(-40.62,-65.49,-3.64)
        self.pier2.setHpr(240,0,0)
        self.pier3 = loader.loadModel("phase_4/models/props/piers_tt.bam")
        self.pier3.reparentTo(self.np)
        self.pier3.setPos(-43.64,-77.15,-3.59)
        self.pier3.setHpr(270,0,0)
        self.pier4 = loader.loadModel("phase_4/models/props/piers_tt.bam")
        self.pier4.reparentTo(self.np)
        self.pier4.setPos(-41.37,-87.36,-3.56)
        self.pier4.setHpr(310,0,0)

        self.placebldg("phase_3.5/models/props/big_planter.bam", (-50,21,5), 0)
        self.placebldg("phase_3.5/models/props/big_planter.bam", (50,21,5), 0)
        self.placebldg("phase_4/models/props/toontown_central_fountain.bam", (3,63,4), 0)
        self.placebldg("phase_4/models/props/mickey_on_horse.bam", (-121,77,2), 0)

        self.gagShop = self.placebldg("phase_4/models/modules/gagShop_TT.bam", (93,-89,0.4), 800)
        self.door('practical','door_double_square_ur',(1,0.63,0.38,1),self.gagShop.find('**/door_origin'))

        self.placewall((87.6,-111.073,0.5),"wall_lg_brick_ur",-119,9,10,(0.5, 0.9, 0.33, 1))
        self.placewall((87.6,-111.073,10.5),"wall_lg_brick_ur",-119,9,10,(0.5, 0.9, 0.33, 1))
        self.placewall((91.77,-103.573,0.5),"wall_sm_cement_ur",-119,9,20,1)
        self.placewall((95.94,-96.073,0.5),'wall_md_dental_ul',-119,9,10,(1, 0.9, 0.33, 1))
        self.placewall((95.94,-96.073,10.5),"wall_md_dental_ul",-119,9,10,(1, 0.9, 0.33, 1))
        self.placewall((59.69,-137.525,0.5),'wall_md_pillars_ul',198,19,20,(1, 0.9, 0.33, 1))

        self.hq = self.placebldg("phase_3.5/models/modules/hqTT.bam", (-29.1796,27.6656,4), 225)

        self.peris = Actor("phase_3.5/models/props/HQ_periscope-mod.bam",{"chan":"phase_3.5/models/props/HQ_periscope-chan.bam"})
        self.peris.reparentTo(self.hq)
        self.peris.setPos(7.17,-7.67,19.07)
        self.peris.setHpr(110,0,0)
        self.peris.setScale(4)
        self.peris.loop('chan')
        self.teles = Actor("phase_3.5/models/props/HQ_telescope-mod.bam",{"chan":"phase_3.5/models/props/HQ_telescope-chan.bam"})
        self.teles.reparentTo(self.hq)
        self.teles.setPos(7.003,0,13.191)
        self.teles.setHpr(168,81,0)
        self.teles.setScale(4)
        self.teles.loop('chan')

        self.pet = self.placebldg("phase_4/models/modules/PetShopExterior_TT.bam", (-167,88,3), 80)
        self.door('practical','door_double_round_ur',(1,0.87,0.38,1),self.pet.find('**/door_origin'))
        self.baseline(self.pet.find("**/sign_origin"),'MickeyFont.bam',(1,1,0,1),(-0.0715486,0.575594,0),(1.58014,1.5,2.42354),L10N("PROP_PETSHOP"),9)

        self.mickey = Actor("phase_3/models/char/mickey-1200.bam",{"wait":"phase_3/models/char/mickey-wait.bam"})
        self.mickey.reparentTo(self.np)
        self.mickey.loop("wait")
        self.mickey.setPos(0,10,4)
        self.mickey.setHpr(180,0,0)
        fonto = loader.loadFont("phase_3/models/fonts/MickeyFont.bam")
        frame = DirectFrame(frameColor=(0,0,0,0),parent=self.mickey)
        frame.setY(-.2)
        self.text = OnscreenText(text="Mickey",font=fonto,pos=(0,4,0),scale=1,parent=frame,fg=(1,1,0.7,1),wordwrap=9)
        self.text.setBillboardAxis(1)
        self.mickey.hide()
        self.fishs = Actor("phase_4/models/props/SZ_fish-mod.bam",{"swim":"phase_4/props/props/SZ_fish-swim.bam"})
        self.fishs.reparentTo(self.pet)
        self.fishs.setScale(1)
        self.fishs.loop('swim')

        self.gate = self.placebldg("phase_4/models/modules/partyGate_TT.bam", (154,95,2.60), -55)

        self.birds = []
        for i in xrange(3): self.birds.append(loader.loadSfx("data/sounds/TT_bird{0}.mp3".format(i+1)))
        seq = Sequence(Func(self.randomSounds),Wait(1),
                       Func(self.randomSounds),Wait(3),
                       Func(self.randomSounds),Wait(2))
        seq.loop()

        from funAreas import Speedway
        self._tunnelMovie((
		                    #(self.model,"Name of the hood/area",funcname)
                            (self.tunnel3,"AREA_ST_2300",streets.TTC_2300),
                            (self.tunnel1,"AREA_ST_2200",streets.TTC_2200),
                            (self.tunnel2,"AREA_ST_2100",streets.TTC_2100),
                            (self.speedway,"AREA_SPEEDWAY",Speedway)
                            ),tp.getTunnel())

        self.setHolidayProps(self.getCurrHoliday())

        if tp: tp.done()

    def decorationProps(self, arg):
        if arg == 1:
            ropes = loader.loadModel('phase_4/models/modules/tt_m_ara_int_ropes.bam')
            ropes.reparentTo(self.np)
            ropes.setPos(109,68,2.5)
            ropes.setScale(0.75)
            gear = loader.loadModel("phase_9/models/char/gearProp.bam")
            gear.reparentTo(self.np)
            gear.setPos(109,68,11.5)
            gear.hprInterval(15.0, Vec3(0, 360, 0), Vec3(-720, 0, -720)).loop()
            gear.setColorScale(0.6, 0.6, 1.0, 1.0)
            gear2 = loader.loadModel("phase_9/models/char/gearProp.bam")
            gear2.reparentTo(self.np)
            gear2.setScale(0.3)
            gear2.setPos(109,68,11.5)
            gear2.hprInterval(15.0, Vec3(0, -720, 0), Vec3(360, 0, 360)).loop()
            gear2.setColorScale(0.6, 0.6, 1.0, 1.0)
        elif arg == 2:
            tree = loader.loadModel("phase_4/models/props/winter_tree_Christmas.bam")
            tree.reparentTo(self.np)
            tree.setPos(109,68,2.5)

    def setHolidayProps(self, holiday):
        if holiday == "Christmas":
            self.placetree_TT('prop_tree_fat_no_box_ur',(-100,5,2.5),2,2)
            self.placetree_TT('prop_tree_fat_no_box_ur',(100,5,2.5),2,2)
            self.placetree_TT('prop_tree_large_no_box_ul',(-81,-73,0.2),2,2)
            self.placetree_TT('prop_tree_large_no_box_ul',(-48,-123,0.2),2,2)
            self.placetree_TT('prop_tree_large_no_box_ul',(21,-128,0.2),2,2)
            self.placetree_TT('prop_tree_small_no_box_ul',(47,121,2.5),2,2)
            self.placetree_TT('prop_tree_small_no_box_ul',(65,130,2.5),2,2)
            self.placetree_TT('prop_tree_small_no_box_ul',(59,117,2.5),2,2)
            self.placetree_TT('prop_tree_small_ul',(144,120,3),50,2)
            self.placetree_TT('prop_tree_small_ul',(130,132,3),50,2)
            self.placetree_TT('prop_tree_fat_no_box_ur',(-77,121,2.5),2,2)
            self.placetree_TT('prop_tree_fat_no_box_ur',(-139,101,2.5),1,2)
            self.placetree_TT('prop_tree_fat_no_box_ur',(-59,113,2.5),1,2)
            self.placetree_TT('prop_tree_fat_no_box_ur',(-61,132,2.5),1,2)
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
            self.placelight_TT('prop_post_one_light',(-164,65,3),85.5,2)
            self.placelight_TT('prop_post_one_light',(-121,7,3),-25,2)
            self.placelight_TT('prop_post_sign',(-53,-132,0.5),60,2)
            self.decorationProps(2)
        else:
            self.placetree_TT('prop_tree_fat_no_box_ur',(-100,5,2.5),1)
            self.placetree_TT('prop_tree_fat_no_box_ur',(100,5,2.5),1)
            self.placetree_TT('prop_tree_large_no_box_ul',(-81,-73,0.2),1)
            self.placetree_TT('prop_tree_large_no_box_ul',(-48,-123,0.2),1)
            self.placetree_TT('prop_tree_large_no_box_ul',(21,-128,0.2),1)
            self.placetree_TT('prop_tree_small_no_box_ul',(47,121,2.5),1)
            self.placetree_TT('prop_tree_small_no_box_ul',(65,130,2.5),1)
            self.placetree_TT('prop_tree_small_no_box_ul',(59,117,2.5),1)
            self.placetree_TT('prop_tree_small_ul',(144,120,3),50,1)
            self.placetree_TT('prop_tree_small_ul',(130,132,3),50,1)
            self.placetree_TT('prop_tree_fat_no_box_ur',(-77,121,2.5),1)
            self.placetree_TT('prop_tree_fat_no_box_ur',(-139,101,2.5),1)
            self.placetree_TT('prop_tree_fat_no_box_ur',(-59,113,2.5),1)
            self.placetree_TT('prop_tree_fat_no_box_ur',(-61,132,2.5),1)
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
            self.placelight_TT('prop_post_one_light',(-164,65,3),85.5,1)
            self.placelight_TT('prop_post_one_light',(-121,7,3),-25,1)
            self.placelight_TT('prop_post_sign',(-53,-132,0.5),60,1)
            self.decorationProps(1)

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
    zoneId = 2000
    music = "phase_6/audio/bgm/DD_nbrhood.mid"
    name = "AREA_DDK"

    def loadRing(self,ring): return loader.loadSfx("phase_6/audio/sfx/SZ_DD_{0}.mp3".format(ring))

    def requestStormCheck(self):
         isStorm = random.randint(1,4)
         if int(isStorm) == 4:
             self.sky1.hide()
             self.sky2.show()
             self.harborFog = Fog("Harbor Fog")
             self.harborFog.setExpDensity(0.001)
             self.np.setFog(self.harborFog)
         else:
             self.sky1.show()
             self.sky2.hide()
             self.np.clearFog()

    def makeSeq(self):
        #print 'WARNING: EXTREMELY BUGGY PLAYGROUND!!!'
        #print 'BE CAREFUL!'
        #wtf
        self.moveBoat1 = self.boat.posHprInterval(6, (30.43079, -32.5, -4), (90,0,0))
        self.moveBoat2 = self.boat.posHprInterval(6, (-33.5692, -42.5, -4), (40,0,0))
        self.moveBoat3 = self.boat.posHprInterval(4, (-50, -10, -4), (0,0,0))
        self.moveBoat4 = self.boat.posHprInterval(6, (-50, 40, -4), (-50,0,0))
        self.moveBoat5 = self.boat.posHprInterval(6, (9.08847, 50.4189, -4), (-100,0,0))
        self.moveBoat6 = self.boat.posHprInterval(7, (50.1,25,-4), (-180,0,0))

        self.upEPier = self.EPier.hprInterval(4, (89.9995,-0,-0.000199231))
        self.downEPier = self.EPier.hprInterval(4, (89.9995,-44.2599,-0.000199231))
        self.upWPier = self.WPier.hprInterval(4, (-90.399,-0,-0.185446))
        self.downWPier = self.WPier.hprInterval(4, (-90.399,-47.5673,-0.185446))

        self.seq = Sequence(
                            Wait(14),
                            self.sfxInterval_bell,
                            Parallel(self.downEPier,
                                     self.sfxInterval_creack,
                                     self.moveBoat1),
                            self.moveBoat2,
                            Parallel(self.upWPier,
                                     self.sfxInterval_creack,
                                     self.moveBoat3),
                            Wait(14),
                            self.sfxInterval_bell,
                            Parallel(self.downWPier,
                                     self.sfxInterval_creack,
                                     self.moveBoat4),
                            self.moveBoat5,
                            Parallel(self.moveBoat6,
                                     self.sfxInterval_creack,
                                     self.upEPier),
                            )

        #self.check = Sequence(Wait(100),Func(self.requestStormCheck)) ### eventual crash: AssertionError: !is_empty() at line 5385 of panda/src/pgraph/nodePath.cxx
        #self.check.loop()

    def __init__(self,tp=None):
        self.sfx_bell = self.loadRing('shipbell')
        self.sfx_creack = self.loadRing('dockcreak')
        self.sfx_water = self.loadRing('waterlap')

        self.sfxInterval_bell = SoundInterval(self.sfx_bell,loop=0)
        self.sfxInterval_creack = SoundInterval(self.sfx_creack,loop=0)
        self.sfxInterval_water = SoundInterval(self.sfx_water,loop=0)

        self.av_startpos = (
                            ((-59.1714, 94.5382, 3.27433), (176.217, 0, 0)),
                            ((-24.7646, -0.380886, 5.75692), (89.7451, 0, 0)),
                            ((-89.3524, -60.7224, 5.68728), (-39.9791, 0, 0)),
                            ((-39.6974, -81.276, 5.68731), (-17.2666, 0, 0)),
                            ((62.9654, 11.3031, 5.68732), (50.3789, 0, 0)),
                            ((56.2392, 87.5031, 3.27562), (149.781, 0, 0)),
                            )

        Hood.__init__(self,"phase_0/streets/street_donalds_dock_sz.bam")

        ft = None
        if tp:
            if hasattr(tp,'tunnel') and tp.tunnel:
                ft = tp.tunnel.area.name

        self.sky1 = loader.loadModel("phase_3.5/models/props/TT_sky.bam")
        self.sky1.reparentTo(self.np)
        self.sky1.hide()
        self.sky2 = loader.loadModel("phase_3.5/models/props/BR_sky.bam")
        self.sky2.reparentTo(self.np)

        #self.environ.setPos(-25,10,0)
        #self.environ.setHpr(180,0,0)
        self.environ.reparentTo(self.np)
        self.boat = self.environ.find("**/donalds_boat")
        self.boat.setPos(50.1,25,-4)
        self.boat.setHpr(180,0,0)
        if 1:
            self.boat.find('**/wheel').hide()
        self.EPier = self.environ.find("**/east_pier")
        self.EPier.setHpr(89.9995,-0,-0.000199231)
        self.WPier = self.environ.find("**/west_pier")

        self.harborFog = Fog("Harbor Fog")
        self.harborFog.setExpDensity(0.0015)
        self.environ.setFog(self.harborFog)

        self.donald = Actor("phase_6/models/char/donald-wheel-1000.bam",{"wait":"phase_6/models/char/donald-wheel-wheel.bam"})
        self.donald.reparentTo(self.boat)
        self.donald.loop("wait")
        self.donald.setPos(0,-0.3,5)
        fonto = loader.loadFont("phase_3/models/fonts/MickeyFont.bam")
        frame = DirectFrame(frameColor=(0,0,0,0),parent=self.donald)
        frame.setY(-.2)
        self.text = OnscreenText(text="Donald",font=fonto,pos=(0,3.5,0),scale=1,parent=frame,fg=(1,1,0.7,1),wordwrap=9)
        self.text.setBillboardAxis(1)
        self.donald.hide()

        self.trolley = self.environ.find("**/*lley_stat*")

        trolleyNp = self.trolley.find('**/trolley_sphere')
        trolleyNode = trolleyNp.node()
        trolleyNode.setCollideMask(BitMask32(8))

        self.collDict = self.collDict if hasattr(self,"collDict") else {}
        self.collDict[trolleyNode] = self.enterTrolley

        from funAreas import AcornAcres

        self.tunnelAA = self.environ.find('**/linktunnel*')
        self.tunnelTTC = self.np.find('**/link*110*')
        self.tunnel2 = self.np.find('**/link*12*')
        self.tunnel3 = self.np.find('**/link*13*')

        self.makeSeq()

        self._tunnelMovie((
                            (self.tunnelTTC,"AREA_ST_1100",streets.DD_1100),
                            (self.tunnel2,"AREA_ST_1200",streets.DD_1200),
                            (self.tunnel3,"AREA_ST_1300",streets.DD_1300),
                            (self.tunnelAA,"AREA_ACRES",AcornAcres)
                            ),ft)

        if tp: tp.done()

    def __tth_area__(self):
        return {
                'name':self.name,
                'models':self.np,
                'bgm':self.theme,
                'gui':self.frame,
                'speeches':[]
                }

class Garden(Hood):
    zoneId = 3000
    music = "phase_8/audio/bgm/DG_nbrhood.mid"
    name = "AREA_GAR"

    def __init__(self,tp=None):
        self.av_startpos = (
                            ((0,0,0),(0,0,0)),
                            ((-22.3362, 55.8126, 0.0203125), (-109.116, 0, 0)),
                            ((94.0984, 108.491, 0.0203125), (37.4872, 0, 0)),
                            ((57.1513, 186.148, 10.0181), (93.8999, 0, 0)),
                            ((17.5723, 210.424, 10.0201), (122.723, 0, 0)),
                            ((-66.6597, 174.503, 10.0202), (193.304, 0, 0)),
                            ((-91.428, 107.555, 0.0197365), (241.834, 0, 0)),
                            ((-56.3953, 71.353, 0.0197365), (252.283, 0, 0)),
                            )

        Hood.__init__(self,"phase_0/streets/street_daisys_garden_sz.bam")

        ft = None
        if tp:
            if hasattr(tp,'tunnel') and tp.tunnel:
                ft = tp.tunnel.area.name

        self.sky1 = loader.loadModel("phase_3.5/models/props/TT_sky.bam")
        self.sky1.reparentTo(self.np)

        lerper = NodePath('lerper')
        self.sky1.find('**/cloud1').setTexProjector(TextureStage.getDefault(), NodePath(), lerper)
        lerper.posInterval(200, VBase3(-1, 0, 0)).loop()

        lerper = NodePath('lerper')
        self.sky1.find('**/cloud2').setTexProjector(TextureStage.getDefault(), NodePath(), lerper)
        lerper.posInterval(200, VBase3(-1, 0, 0)).loop()

        self.environ.reparentTo(self.np)

        self.trolley = self.environ.find("**/*lley_stat*")

        trolleyNp = self.trolley.find('**/trolley_sphere')
        trolleyNode = trolleyNp.node()
        trolleyNode.setCollideMask(BitMask32(8))

        self.collDict = self.collDict if hasattr(self,"collDict") else {}
        self.collDict[trolleyNode] = self.enterTrolley

        self.tunnelDD = self.environ.find('**/link*520*')
        self.tunnelTTC = self.np.find('**/link*510*')
        self.tunnelSB = self.np.find('**/link*530*')

        self._tunnelMovie((
                            (self.tunnelTTC,"AREA_ST_5100",streets.DG_5100),
                            (self.tunnelDD,"AREA_ST_5200",streets.DG_5200),
                            (self.tunnelSB,"AREA_ST_5300",streets.DG_5300),
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

class Melodyland(Hood):
    zoneId = 4000
    music = "phase_6/audio/bgm/MM_nbrhood.mid"
    name = "AREA_MML"


    def __init__(self,tp=None):
        self.av_startpos = (
                            ((53.0741, 43.5831, -14.5518), (143.28, 0, 0)),
                            ((84.7231, 8.03727, -13.4803), (-268.497, 0, 0)),
                            ((53.3274, -78.9368, -14.5624), (-316.651, 0, 0)),
                            ((117.544, 31.3585, -4.50305), (91.7767, 0, 0)),
                            ((117.388, -0.42139, 3.29827), (-282.908, 0, 0)),
                            ((36.234, -108.965, 6.52058), (-0.393692, 0, 0)),
                            ((-61.5347, -72.2662, 6.52058), (-48.8596, 0, 0)),
                            ((-36.0916, 61.0201, 6.52058), (-163.579, 0, 0)),
                            )

        Hood.__init__(self,"phase_0/streets/street_minnies_melody_land_sz.bam")

        ft = None
        if tp:
            if hasattr(tp,'tunnel') and tp.tunnel:
                ft = tp.tunnel.area.name

        self.sky1 = loader.loadModel("phase_6/models/props/MM_sky.bam")
        self.sky1.reparentTo(self.np)

        self.environ.reparentTo(self.np)

        self.trolley = self.environ.find("**/*lley_stat*")

        trolleyNp = self.trolley.find('**/trolley_sphere')
        trolleyNode = trolleyNp.node()
        trolleyNode.setCollideMask(BitMask32(8))

        self.collDict = self.collDict if hasattr(self,"collDict") else {}
        self.collDict[trolleyNode] = self.enterTrolley

        self.tunnelBR = self.environ.find('**/link*42*')
        self.tunnelTTC = self.np.find('**/link*41*')
        self.tunnelDL = self.np.find('**/link*43*')

        self._tunnelMovie((
                            (self.tunnelTTC,"AREA_ST_4100",streets.MM_4100),
                            (self.tunnelBR,"AREA_ST_4200",streets.MM_4200),
                            (self.tunnelDL,"AREA_ST_4300",streets.MM_4300),
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

class Brrrgh(Hood):
    zoneId = 5000
    music = "phase_8/audio/bgm/TB_nbrhood.mid"
    name = "AREA_BRG"


    def __init__(self,tp=None):
        self.av_startpos = (
                            ((0,0,0),(0,0,0)),
                            ((-112.417, -43.7128, 8.49103), (-66.9642, 0, 0)),
                            ((-108.249, 38.6914, 6.18679), (-88.0856, 0, 0)),
                            ((-64.0579, 86.8788, 6.187), (-119.815, 0, 0)),
                            ((-25.0786, -85.7833, 6.1874), (-18.7785, 0, 0)),
                            ((14.8734, -96.4087, 6.18738), (-712.758, 0, 0)),
                            ((31.7985, 43.7862, 6.18654), (-528.403, 0, 0)),
                            )

        Hood.__init__(self,"phase_0/streets/street_the_burrrgh_sz.bam")

        ft = None
        if tp:
            if hasattr(tp,'tunnel') and tp.tunnel:
                ft = tp.tunnel.area.name

        self.sky1 = loader.loadModel("phase_3.5/models/props/BR_sky.bam")
        self.sky1.reparentTo(self.np)

        self.environ.reparentTo(self.np)

        self.trolley = self.environ.find("**/*lley_stat*")

        trolleyNp = self.trolley.find('**/trolley_sphere')
        trolleyNode = trolleyNp.node()
        trolleyNode.setCollideMask(BitMask32(8))

        self.collDict = self.collDict if hasattr(self,"collDict") else {}
        self.collDict[trolleyNode] = self.enterTrolley

        self.tunnelMM = self.environ.find('**/link*32*')
        self.tunnelDD = self.np.find('**/link*31*')
        self.tunnelLB = self.np.find('**/link*33*')

        print self.tunnelMM,self.tunnelDD,self.tunnelLB
        #print [x for x in self.environ.findAllMatches('**/link*')]
        #exit()

        self._tunnelMovie((
                            (self.tunnelDD,"AREA_ST_3100",streets.BR_3100),
                            (self.tunnelMM,"AREA_ST_3200",streets.BR_3200),
                            (self.tunnelLB,"AREA_ST_3300",streets.BR_3300),
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

class Dreamland(Hood):
    zoneId = 6000
    music = "phase_8/audio/bgm/DL_nbrhood.mid"
    name = "AREA_DDL"


    def __init__(self,tp=None):
        self.av_startpos = (
                            ((0,0,0),(0,0,0)),
                            ((33.6517, 16.8084, -14.9805), (61.388, 0, 0)),
                            ((47.1884, 44.3003, -16.2153), (-213.31, 0, 0)),
                            ((-13.0625, -48.504, -16.4122), (-304.362, 0, 0)),
                            ((-74.8092, -94.4083, 0.0195994), (-66.2486, 0, 0)),
                            ((40.3343, -97.813, 0.0195994), (14.4784, 0, 0)),
                            ((56.371, 94.5328, 0.019721), (96.7167, 0, 0)),
                            ((-38.7332, 97.001, 0.019721), (168.18, 0, 0)),
                            )

        Hood.__init__(self,"phase_0/streets/street_donalds_dreamland_sz.bam")

        ft = None
        if tp:
            if hasattr(tp,'tunnel') and tp.tunnel:
                ft = tp.tunnel.area.name

        self.sky1 = loader.loadModel("phase_8/models/props/DL_sky.bam")
        self.sky1.reparentTo(self.np)

        self.environ.reparentTo(self.np)

        self.trolley = self.environ.find("**/*lley_stat*")

        trolleyNp = self.trolley.find('**/trolley_sphere')
        trolleyNode = trolleyNp.node()
        trolleyNode.setCollideMask(BitMask32(8))

        self.collDict = self.collDict if hasattr(self,"collDict") else {}
        self.collDict[trolleyNode] = self.enterTrolley

        self.tunnelCB = self.environ.find('**/link*92*')
        self.tunnelMM = self.np.find('**/link*91*')

        self._tunnelMovie((
                            (self.tunnelMM,"AREA_ST_9100",streets.DL_9100),
                            (self.tunnelCB,"AREA_ST_9200",streets.DL_9200),
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
