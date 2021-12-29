from direct.distributed.DistributedObjectAI import *
from direct.distributed.ClockDelta import globalClockDelta

class DistributedDockBoatAI(DistributedObjectAI): 
    def __init__(self,cr):
        DistributedObjectAI.__init__(self,cr)
        self.startTime = globalClock.getFrameTime()
        
    def getT(self):
        return globalClockDelta.localToNetworkTime(self.startTime, bits = 32)