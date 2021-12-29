from direct.distributed.DistributedObjectAI import DistributedObjectAI

class DistributedAvatarAI(DistributedObjectAI):

    def announceGenerate(self):
        DistributedObjectAI.announceGenerate(self)
        self.shard = -1
        
    def speak(self,speech):
        clientId = base.air.id2c(self.doId)
        if clientId in base.cTracker:
            log = base.cTracker[clientId]["log"]
            log.write('speech: '+speech+'\n')
        
    def setToonDna(self,data):
        self.dna = data
        
        #print 'TOON AI: SET DATA',data,len(data),exit()
        self.data = load_buffer(self.dna)
        
        #now we an id
        messenger.send("newAv",[self.data.get("toonId",-1),self])
        
    def delete(self):
        DistributedObjectAI.delete(self)
        messenger.send("lostAv",[self.data.get("toonId",-1)])
        try:
            messenger.send("shard_lose"+str(self.shard),[self])
        except: pass

    def setLocation(self,*args):
        DistributedObjectAI.setLocation(self,*args)
        
        sh = self.zoneId // 10**7
        
        try:
            if sh == self.shard: return
            messenger.send("shard_new"+str(sh),[self])
            messenger.send("shard_lose"+str(self.shard),[self])
        except: pass
        
        self.shard = sh