import FishingPond
class DockManager:
    def __init__(self,distMgr):
        self.distMgr = distMgr
        
        #for dock we create:
        
        #boat
        self.SZ_boat = base.air.createDistributedObject(className = 'DistributedDockBoatAI', zoneId = distMgr.get(2000))
        self.SZ_trolley = base.air.createDistributedObject(className = 'DistributedTrolleyAI', zoneId = distMgr.get(2000))
        
        self.SZ_pound = FishingPond.FishingPond(self,distMgr.get(2000))
        
        self.st1_pound = FishingPond.FishingPond(self,distMgr.get(2100))
        self.st2_pound = FishingPond.FishingPond(self,distMgr.get(2200))
        self.st3_pound = FishingPond.FishingPond(self,distMgr.get(2300))