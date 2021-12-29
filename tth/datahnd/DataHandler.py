from direct.distributed.DistributedObject import *

class DataHandler(DistributedObject):
        
    def response(self,t,d):
        if t in self.interested:
            cb = self.interested[t]["callback"]
            args = self.interested[t]["extraArgs"]
            cb(load_buffer(d),*args)
            del self.interested[t]
        
    def generate(self):
        DistributedObject.generate(self)
        self.interested = {}
        
        self.accept("requestToonData",self.__reqData)
        
    def __reqData(self,t,doId,cb,args=[]):
        self.interested[t] = {'extraArgs':args,'callback':cb}
        self.sendUpdate('request',[t,doId])