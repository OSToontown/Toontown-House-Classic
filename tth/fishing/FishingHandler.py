from direct.actor.Actor import *
from pandac.PandaModules import *
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from direct.showbase.InputStateGlobal import inputState
from direct.showbase.DirectObject import DirectObject

import random, sys, os
from math import *

class HandlePier:
    def __init__(self,pier,area):
        self.cNp = pier.find("**/floor_collision")
        self.cnode = self.cNp.node()
        self.cnode.setFromCollideMask(BitMask32(8))
        
        if not hasattr(area,"collDict"): area.collDict={}
        area.collDict[self.cnode] = self.goInto
        self.area = area
        self.pier = pier

    def goInto(self,entry):
        print 'Pier!',self.pier.getPos()
        self.area.disableControls()
        self.chr = self.area.avatar
        self.tn = self.area.toon

        self.pole = loader.loadModel("data/models/fishing/pole1.bam") #blah.read('pole',1)
        hand=self.chr.torso.find("def_joint_right_hold")
        self.pole.reparentTo(hand)

        self.tn.anim('fish')
        self.chr.setPos(self.pier)

