#s0r00t ONLY HERE!
from __init__ import Area

from panda3d.core import CollisionTraverser, CollisionNode, CollisionHandlerQueue, CollisionRay, TextureStage

class ConcertZone(Area):
    def __init__(self,tp=None):
        self.name = "Concert Zone"
        self.zoneId = 5555

        self.avatarPN = ['wall','props']
        Area.__init__(self,"data/models/MML/mml.bam")

        # self.m2 = loader.loadModel("data/models/streets/street_modules_enhanced.bam")
        # self.m2.reparentTo(self.np)
        # self.m1 = loader.loadModel("data/models/streets/street_modules.bam")
        # self.m2.reparentTo(self.np)


        if tp: tp.done()

    def __tth_area__(self):
        return {
                'name':self.name,
                'models':self.np,
                'bgm':self.theme,
                'speeches':[]
                }