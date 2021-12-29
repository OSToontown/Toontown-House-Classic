import random, math
from pandac.PandaModules import *
from direct.distributed import DistributedObject
 
SPIN_RATE = 0.5
COUNT_DOWN = 1
 
class DistributedPiano(DistributedObject.DistributedObject):
    def __init__(self):
        self.direction = "right"
        self.speedUpSound = base.loadSfx('phase_6/audio/sfx/SZ_MM_gliss.mp3')
        self.changeDirectionSound = base.loadSfx('phase_6/audio/sfx/SZ_MM_cymbal.mp3')
 
    def load(self):
        self.environ.find('**/center_icon').setPos(0,-20.1,0)
        self.environ.find('**/midkey_floor').setPos(0,20.1,0)
        self.environ.find('**/pond_floor').setPos(0,20.1,0)
        self.environ.find('**/pond_floor').setScale(1.01,1.01,1)
        self.environ.find('**/MMsz_water').setPos(0,20.0,0)
        self.environ.find('**/midkey_floor').setScale(1.01,1.01,1)
        self.environ.find('**/midkey_floor_1').setScale(1.01,1.01,1)
        base.accept('entermidkey_floor_1', self.enter)
        base.accept('entermid_fishpond', self.enter)
        base.accept('exitmidkey_floor_1', self.exit)
        base.accept('exitmid_fishpond', self.exit)
        base.taskMgr.add(self.changeDirection, 'MM-pianoSpin')
 
    def unload(self):
        taskMgr.remove('MM-pianoSpin')
        del self.direction
        del self.speedUpSound
        del self.changeDirectionSound
 
    def changeDirection(self, task):
        global COUNT_DOWN
        COUNT_DOWN += 1
        if COUNT_DOWN == 1000:
            self.direction = "left"
            base.playSfx(self.changeDirectionSound)
        if COUNT_DOWN == 2000:
            self.direction = "right"
            COUNT_DOWN = 1
            base.playSfx(self.changeDirectionSound)
        piano = self.environ.find('**/center_icon')
        if self.direction == "left":
            piano.setH(piano.getH() - SPIN_RATE)
        elif self.direction == "right":
            piano.setH(piano.getH() + SPIN_RATE)
        return Task.cont
 
    def enter(self,collide):
        global SPIN_RATE
        gamebase.currArea.toon.wrtReparentTo(self.environ.find('**/center_icon'))
        SPIN_RATE += 0.075
        if SPIN_RATE >= 3:
            SPIN_RATE = 0.5
        base.playSfx(self.speedUpSound)
 
    def exit(self,collide):
        gamebase.currArea.toon.wrtReparentTo(self.np)