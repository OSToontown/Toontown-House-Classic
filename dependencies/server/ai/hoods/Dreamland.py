import FishingPond
class DLManager:
    def __init__(self,distMgr):
        self.distMgr = distMgr
        
        self.SZ_trolley = base.air.createDistributedObject(className = 'DistributedTrolleyAI', zoneId = distMgr.get(6000))
        
        self.SZ_pound = FishingPond.FishingPond(self,distMgr.get(6000))
        
        self.st1_pound = FishingPond.FishingPond(self,distMgr.get(6100))
        self.st2_pound = FishingPond.FishingPond(self,distMgr.get(6200))