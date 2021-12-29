class AcresManager:
    def __init__(self,distMgr):
        self.distMgr = distMgr
        
        #for acres we create:
        
        #geyser
        #* DistributedDockBoat is meant to Dock, but its just a "sequence sync" so will work well here xD
        self.SZ_geyser = base.air.createDistributedObject(className = 'DistributedDockBoatAI', zoneId = distMgr.get(2400))