from direct.distributed.DistributedObject import DistributedObject
from direct.distributed.ClockDelta import globalClockDelta
from panda3d.core import *

from FishingGlobals import *

from tth.effects import Bubbles

class DistributedFishingShadow(DistributedObject):
    def generate(self):
        DistributedObject.generate(self)
        self.shadow = loader.loadModel('phase_3/models/props/drop_shadow')
        self.shadow.setPos(0, 0, -0.1)
        self.shadow.setScale(0.33)
        self.shadow.setColorScale(1, 1, 1, 0.75)
        self.everMoved = 0
        
    def setPondDoId(self,doId):     
        try: self.pond
        except: pass
        else: return
        
        self.pond = base.cr.doId2do[doId]
        self.pond.addFish(self)

        self.centerPoint = getTargetCenter(self.pond.getArea())
        self.maxRadius = getTargetRadius(self.pond.getArea())
        
        self.shadow.reparentTo(render)
        
        self.collSphere = CollisionSphere(0,0,0,self.shadow.getBounds().getRadius()*1.5)
        self.collNode = CollisionNode('fishShadowCN')
        self.collNode.addSolid(self.collSphere)
        self.collNode.setCollideMask(BitMask32(FishMask))
        self.collNp = self.shadow.attachNewNode(self.collNode)
        
        #self.collNp.show()
        
        self.bubbles = Bubbles.Bubbles(self.shadow, render)
        self.bubbles.renderParent.setDepthWrite(0)
        self.bubbles.start()       

    def getDestPos(self, x, y):
        return Vec3(self.centerPoint)+Vec3(x, y, 0)
        
    def setPoint(self,x,y,z,time):
        ts = globalClockDelta.localElapsedTime(time,bits=32)
        
        pos1 = self.shadow.getPos()   
        pos2 = self.getDestPos(x,y)
        
        if not self.everMoved:
            self.everMoved = 1
            self.shadow.setPos(pos2) #fuck interval, just set
            return
        
        delta = (pos1-pos2).length()
        
        ival = self.shadow.posInterval(delta/ShadowSpeed,pos2,pos1)
        ival.start()
        ival.setT(ts)