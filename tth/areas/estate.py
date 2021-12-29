from __init__ import Area, Tunnel

from panda3d.core import *
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *
from direct.actor.Actor import *
import random
from tth.fishing.FishingHandler import *

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

    def makeMask(self,wall,parent):
        toMask = wall.find("**/wall_collide")
        toMask.node().setFromCollideMask(BitMask32(8))
        toMask.reparentTo(parent)

    def placewall(self, pos, type, h, width, height, color):
        wallm = loader.loadModel("data/models/streets/walls.bam")
        wall = wallm.find("**/"+type)
        wall.reparentTo(self.np)
        wall.setPos(pos)
        wall.setH(h)
        wall.setSz(height)
        wall.setSx(width)
        wall.setColor(color)
        self.makeMask(wallm,wall)
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


class Estate(Hood): #BEING DEVELOPED
    def __init__(self,tp=None):
        self.name = "ESTATE"
        self.zoneId = 1
        self.music = "data/sounds/TC_nbrhood.mp3"

        Hood.__init__(self,None)

        self.environ = loader.loadModel("data/models/estate/exterior.bam")
        self.environ.reparentTo(render)
        self.environ.setPos(-4.99989,-0.000152588,2.28882e-005)

        self.ttcTunnele = self.placetun((0,0,0), 0, False)

        from hoods import TTCentral

        Tunnel(self.ttcTunnele, BitMask32(8), self, (TTCentral,'AREA_TTC'))

        #FISHING PONDS
        self.pier1 = loader.loadModel("data/models/TTC/pier.bam")
        self.pier1.reparentTo(render)
        self.pier1.setPos(49.1029,-124.805,0.344704)
        self.pier1.setHpr(90,0,0)

        self.pier2 = loader.loadModel("data/models/TTC/pier.bam")
        self.pier2.reparentTo(render)
        self.pier2.setPos(46.5222,-134.739,0.390713)
        self.pier2.setHpr(75,0,0)

        self.pier3 = loader.loadModel("data/models/TTC/pier.bam")
        self.pier3.reparentTo(render)
        self.pier3.setPos(41.31,-144.559,0.375978)
        self.pier3.setHpr(45,0,0)

        self.pier4 = loader.loadModel("data/models/TTC/pier.bam")
        self.pier4.reparentTo(render)
        self.pier4.setPos(46.8254,-113.682,0.46015)
        self.pier4.setHpr(135,0,0)

        if tp: tp.done()

    def __tth_area__(self):
        return {
                'name':self.name,
                'models':self.np,
                'bgm':self.theme,
                'gui':self.frame,
                'speeches':[]
                }
