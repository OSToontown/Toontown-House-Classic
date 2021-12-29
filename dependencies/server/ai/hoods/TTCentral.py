class TTCManager:
    def __init__(self,distMgr):
        self.distMgr = distMgr
        
        #for dock we create:
        
        #boat
        self.SZ_trolley = base.air.createDistributedObject(className = 'DistributedTrolleyAI', zoneId = distMgr.get(1000))