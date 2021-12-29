from direct.distributed.DistributedNodeAI import DistributedNodeAI

class DistributedNPCAI(DistributedNodeAI):
    def getId(self):
        return self.npcId
        
    def announceGenerate(self):
        DistributedNodeAI.announceGenerate(self)
        print 'npc (%s) generated at zone %s under doId %d' % (self.__class__.__name__,self.zoneId,self.doId)