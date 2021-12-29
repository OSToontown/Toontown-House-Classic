import random, math
from pandac.PandaModules import *
from direct.distributed import DistributedObject
 
SPIN_RATE = 1.25
COUNT_DOWN = 1
 
class DistributedFlower(DistributedObject.DistributedObject):
    def load(self):
        self.bigFlower = loader.loadModel('phase_8/models/props/DG_flower-mod.bam')
        self.bigFlower.setPos(1.39, 92.91, 2.0)
        self.bigFlower.setScale(2.5)
        self.bigFlower.reparentTo(self.np)
        self.flowerCollSphere = CollisionSphere(0, 0, 0, 4.5)
        self.flowerCollSphereNode = CollisionNode('bigFlowerCollide')
        self.flowerCollSphereNode.addSolid(self.flowerCollSphere)
        self.bigFlower.attachNewNode(self.flowerCollSphereNode)
        self.flowerTrigSphere = CollisionSphere(0, 0, 0, 6.0)
        self.flowerTrigSphere.setTangible(0)
        self.flowerTrigSphereNode = CollisionNode('bigFlowerTrigger')
        self.flowerTrigSphereNode.addSolid(self.flowerTrigSphere)
        self.bigFlower.attachNewNode(self.flowerTrigSphereNode)
        taskMgr.add(self.__flowerSpin, 'DG-flowerSpin')
 
    def unload(self):
        taskMgr.remove('DG-flowerSpin')
        del self.bigFlower
        del self.flowerCollSphere
        del self.flowerCollSphereNode
 
    def __flowerSpin(self, task):
        global COUNT_DOWN
        COUNT_DOWN += 1
        if COUNT_DOWN == 1000:
            COUNT_DOWN = 1
            self.setHeight(random.randint(2,10))
        self.bigFlower.setH(self.bigFlower.getH() + SPIN_RATE)
        return Task.cont
 
    def setHeight(self, newHeight):
        pos = self.bigFlower.getPos()
        self.bigFlower.posInterval(1, (pos[0], pos[1], newHeight)).start()