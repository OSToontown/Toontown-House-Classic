from tth.fishing.DistributedFishingShadowAI import DistributedFishingShadowAI
from tth.npc.DistributedFishermanNPC import DistributedFishermanNPCAI
from tth.npc.NPCGlobals import Fishermen
class FishingPond:
    NUM_FISHES = 2
    def __init__(self,zoneMgr,zoneId,wantNpc = True):
        self.zoneMgr = zoneMgr
        self.zoneId = zoneId
        
        self.pond = base.air.createDistributedObject(className = 'DistributedPondAI', zoneId = self.zoneId)
        self.fishes = []
        
        for i in xrange(self.NUM_FISHES):
            fish = DistributedFishingShadowAI(base.air)
            fish.setPond(self.pond)
            fish = base.air.createDistributedObject(distObj = fish, zoneId = self.zoneId)
            
            self.fishes.append(fish)
            
        if wantNpc:
            _npc = DistributedFishermanNPCAI(base.air)
            #print self.zoneId % 10**7,Fishermen[self.zoneId % 10**7]#,exit() 
            npcId, pos, h = Fishermen[self.zoneId % 10**7]
            _npc.npcId = npcId
            
            self.npc = base.air.createDistributedObject(distObj = _npc, zoneId = self.zoneId)
            self.npc.sendUpdate('setId',[npcId])
            self.npc.setPos(pos)
            self.npc.setH(h)