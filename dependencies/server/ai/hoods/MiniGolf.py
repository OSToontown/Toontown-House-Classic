class MGManager:
    def __init__(self,distMgr):
        self.distMgr = distMgr
        
        #for minigolf we create:
        
        #kart
        #* DistributedDockBoat is meant to Dock, but its just a "sequence sync" so will work well here xD
        self.SZ_kart = base.air.createDistributedObject(className = 'DistributedDockBoatAI', zoneId = distMgr.get(2450))