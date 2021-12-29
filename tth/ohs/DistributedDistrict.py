from direct.distributed.DistributedObject import DistributedObject

class DistributedDistrict(DistributedObject):
    def __init__(self,cr):
        self.id,self.toons,self.canUpdate = 0,0,False
        DistributedObject.__init__(self,cr)
        self.accept('forceShardUpdate',self.__forcedUpdate)
        
    def setId(self,id): self.id = id
    def getId(self): return self.id
    
    def setToons(self,toons):
        self.toons = toons
        messenger.send('shardUpdate',[self.id,self.toons])
        
    def getToons(self): return self.toons
    
    def announceGenerate(self):
        DistributedObject.announceGenerate(self)
        self.canUpdate = True
        
    def __forcedUpdate(self): self.setToons(self.toons)
        