from DistributedNPCAI import DistributedNPCAI

class DistributedBlockingNPCAI(DistributedNPCAI):
    timeout = 45
    def __init__(self,cr):
        DistributedNPCAI.__init__(self,cr)
        self.accept('clientDc',self.handleClientDC)
        self.cUser = 0
        
    def announceGenerate(self):
        DistributedNPCAI.announceGenerate(self)
        self.origH = self.getH()
        
    def isBusy(self):
        return self.cUser != 0
             
    def getToon(self):
        return self.cUser
      
    def requestUse(self):
        s = self.cr.getAvatarIdFromSender()
        
        if self.isBusy():
            self.sendUpdateToChannel(s,'reject',[])
            return
            
        else:
            self.sendUpdateToChannel(s,'enter',[self.timeout])
            
        self.cUser = s
        self.d_updateToon()
        print '** accepted enter request on npc %d from %d' % (self.doId,s)
        
        self.timeOutTask = taskMgr.doMethodLater(self.timeout,self.onTimeOut,"timeout task for blocking npc %s" % self.doId)
        
    def requestLeave(self):
        s = self.cr.getAvatarIdFromSender()
        if s == self.cUser:
            taskMgr.remove(self.timeOutTask)
            self.__handleExit()
        
    def onTimeOut(self,task):
        print 'client %d timed out (%d secs) on npc %d, removing...' % (self.cUser,self.timeout,self.doId)
        self.sendUpdateToChannel(self.cUser,'timedOut',[])
        self.__handleExit()
        return task.done
        
    def __handleExit(self):
        self.cUser = 0
        
        ang = self.origH
        self.sendUpdate('setH',[ang])
        self.setH(ang)
        
        self.d_updateToon()
        
    def d_updateToon(self):
        self.sendUpdate('setToon',[self.cUser])
        
    def handleClientDC(self,doId):
        if doId == self.cUser:
            print doId,'dc in blocking npc, setting free...'
            self.__handleExit()
            taskMgr.remove(self.timeOutTask)

    def setClH(self,h):
        print 'setting npc %d H to %s (cur = %s)' % (self.doId, h, self.getH())
        DistributedNPCAI.setH(self,h)
        
    def getClH(self):
        return self.getH()
        
    def setClChat(self,index,extraArgsBuff):
        pass
        