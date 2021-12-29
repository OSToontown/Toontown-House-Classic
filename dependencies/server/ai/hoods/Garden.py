import FishingPond
class GardenManager:
    def __init__(self,distMgr):
        self.distMgr = distMgr
        
        self.SZ_trolley = base.air.createDistributedObject(className = 'DistributedTrolleyAI', zoneId = distMgr.get(3000))
        
        self.SZ_pound = FishingPond.FishingPond(self,distMgr.get(3000))
        
        self.st1_pound = FishingPond.FishingPond(self,distMgr.get(3100))
        self.st2_pound = FishingPond.FishingPond(self,distMgr.get(3200))
        self.st3_pound = FishingPond.FishingPond(self,distMgr.get(3300))