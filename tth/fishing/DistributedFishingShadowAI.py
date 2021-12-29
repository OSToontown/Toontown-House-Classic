from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.distributed.ClockDelta import globalClockDelta

from FishingGlobals import getTargetRadius, MinShadowDelta, ShadowMoveTime
import random

from panda3d.core import Vec3

MPRatio = 2

class DistributedFishingShadowAI(DistributedObjectAI):
    def __init__(self,cr):
        DistributedObjectAI.__init__(self,cr)
        self.pos = (0,0,0)
        self.time = 0
        self.pond = None
        
        self.move = False
        
    def getPondDoId(self):
        return self.pond.doId
        
    def getPoint(self):
        return self.pos+(self.time,)
        
    def setPond(self,pond):
        self.pond = pond
        self.radius = getTargetRadius(self.pond.getArea())
        
    def getMoveTime(self):
        return random.randint(*ShadowMoveTime)
        
    def startMoving(self):
        self.move = True
        taskMgr.doMethodLater(self.getMoveTime(),self.moveTask,"move fish %d" % self.doId)
        
    def stopMoving(self):
        self.move = False
        
    def makePos(self):
        def _length(a,b):
            return (Vec3(a)-Vec3(b)).length()
            
        def _new():
            x = (random.random()*MPRatio-1)*self.radius
            y = (random.random()*MPRatio-1)*self.radius
            
            return (x,y,0)
            
        cpos = self.pos
        npos = Vec3(cpos) #copy
        
        while _length(cpos,npos) < MinShadowDelta:
            npos = _new()
            
        return tuple(npos)
        
    def moveTask(self,task):
        if not self.move:
            return task.done
        
        self.pos = self.makePos()
        self.time = globalClockDelta.localToNetworkTime(globalClock.getFrameTime(),bits=32)
        
        #print 'move fish',self.doId,self.pos,self.time
        
        self.sendUpdate('setPoint',self.getPoint())
            
        taskMgr.doMethodLater(self.getMoveTime(),self.moveTask,"move fish %d" % self.doId)
        return task.done
        
    def announceGenerate(self):
        DistributedObjectAI.announceGenerate(self)
        self.startMoving()
        
    def disable(self):
        DistributedObjectAI.disable(self)
        self.stopMoving()
        