from direct.distributed.DistributedObject import *
from direct.distributed.ClockDelta import globalClockDelta

class DistributedDockBoat(DistributedObject):
    def __init__(self,cr):
        DistributedObject.__init__(self,cr)
        
        self.startTime = 0
        
    def setT(self,t):
        self.startTime = globalClockDelta.networkToLocalTime(t, bits = 32)
    
    def getT(self):
        return globalClockDelta.localToNetworkTime(self.startTime, bits = 32)
        
    def announceGenerate(self):
        DistributedObject.announceGenerate(self)
        print 'Boat generate @ zone',self.zoneId
        taskMgr.doMethodLater(2,self._doTask,"set seq time")
    
    def _doTask(self,task):
        elapsed = globalClock.getFrameTime() - self.startTime

        try:
            seq = gamebase.curArea.seq
        except:
            return task.again
            
        _T = elapsed % seq.getDuration()
        
        seq.loop()
        seq.setT(_T)
        
        return task.done