from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.distributed.ClockDelta import globalClockDelta

class DistributedPondAI(DistributedObjectAI):
    isEstate = 0
    
    def __init__(self,cr):
        DistributedObjectAI.__init__(self,cr)
        self.toons = [0,0,0,0]  
        self.accept('clientDc',self.handleClientDC)
        
    def getEstate(self):
        return self.isEstate
        
    def getArea(self):
        if self.isEstate: return "estate"
        return self.zoneId % 10**7
        
    def getToons(self):
        return self.toons
        
    def requestEnter(self,index):
        if not -1 < index < len(self.toons):
            print 'PondAI: ignoring bad index',index
            return
            
        sender = self.cr.getAvatarIdFromSender()
        
        if self.toons[index] != 0:
            self.sendUpdateToChannel(sender,'reject',[])
            return
        
        self.toons[index] = sender
        self.sendUpdateToChannel(sender,'accept',[])
        
        self.d_updateToons()
        
    def requestExit(self):
        sender = self.cr.getAvatarIdFromSender()
        
        if sender not in self.toons:
            print 'PondAI: ignoring bad request exit from',sender
            return
            
        self.__handleExit(sender)
        
    def __handleExit(self,sender):
        index = self.toons.index(sender)
        self.toons[index] = 0
        
        self.d_updateToons()
    
    def d_updateToons(self):
        self.sendUpdate('setToons',self.toons)
        
    def handleClientDC(self,doId):
        if doId in self.toons:
            print doId,'dc in pier, setting pier free...'
            self.__handleExit(doId)