from hoods import TTCentral, Dock, Acres, MiniGolf, Garden, Melodyland, Brrrgh, Dreamland
from hoods import LawHQ, SellHQ

from direct.showbase.DirectObject import DirectObject

class DistrictManager(object,DirectObject):
    def __init__(self,distId):
        self.distId = distId
        
        #spawn some exclusive managers
        self.TTCManager = TTCentral.TTCManager(self)
        self.DockManager = Dock.DockManager(self)
        self.AcresManager = Acres.AcresManager(self)
        self.MGManager = MiniGolf.MGManager(self)
        self.GardenManager = Garden.GardenManager(self)
        self.MelodylandManager = Melodyland.MelodylandManager(self)
        self.BRManager = Brrrgh.BRManager(self)
        self.DreamlandManager = Dreamland.DLManager(self)
        
        self.HQ_LAW = LawHQ.LawbotHQManager(self)
        self.HQ_SELL = SellHQ.SellbotHQManager(self)
        
        self.toons = set()
        self.accept("shard_new"+str(self.distId),self._new)
        self.accept("shard_lose"+str(self.distId),self._lose)
        
        self._obj = base.air.createDistributedObject(className = 'DistributedDistrict', zoneId=1000)
        self._obj.id = self.distId
        
    def _new(self,t):
        self.toons.add(t)
        self._update()
        
    def _lose(self,t):
        if t in self.toons: self.toons.remove(t)
        self._update()
        
    def _update(self):
        if self._obj.canUpdate:
            self._obj.sendUpdate('setToons',[len(self.toons)])
        
    def get(self,zone):
        return 10**7*self.distId+zone