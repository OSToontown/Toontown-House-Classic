import FishingPond
class BRManager:
    def __init__(self,distMgr):
        self.distMgr = distMgr
        
        self.SZ_trolley = base.air.createDistributedObject(className = 'DistributedTrolleyAI', zoneId = distMgr.get(5000))
        self.SZ_pound = FishingPond.FishingPond(self,distMgr.get(5000),True)
        
        self.st1_pound = FishingPond.FishingPond(self,distMgr.get(5100))
        self.st2_pound = FishingPond.FishingPond(self,distMgr.get(5200))
        self.st3_pound = FishingPond.FishingPond(self,distMgr.get(5300))