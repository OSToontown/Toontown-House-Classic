from direct.distributed.DistributedObjectAI import *
from direct.distributed.ClockDelta import globalClockDelta

class DistributedDoorAI(DistributedObjectAI):
    def __init__(self,cr):
        DistributedObjectAI.__init__(self,cr)
        self.state = ("Closed",0,"Closed",0)
        self.target = ""
        
    def d_setTarget(self,target):
        self.target = target
        self.sendUpdate("setTarget",[self.target])
        
    def d_setStateL(self,state):
        time = globalClockDelta.localToNetworkTime(globalClock.getFrameTime())
        self.state[0:2] = [state,time]
        self.sendUpdate("setState",self.state)
        
    def d_setStateR(self,state):
        time = globalClockDelta.localToNetworkTime(globalClock.getFrameTime())
        self.state[2:4] = [state,time]
        self.sendUpdate("setState",self.state)
        
    def getTarget(self):
        return self.target
        
    def getState(self):
        return self.state
        
    def requestOpen(self,side):
        self.__open(side)
        print 'opening door %s, side=%s' % (self,side)
        
    def __open(self,side):
        index = (0,2)[side=='R']
        if self.state[index] == "Open": return
        (self.d_setStateL,0,self.d_setStateR)[index]("Open")
        taskMgr.doMethodLater(CLOSEDELAY,lambda t:self.__close(index),"close door")
        
    def __close(self,index):
        print 'close door %s, side=%s' % (self,side)
        if self.state[index] == "Closed": return
        (self.d_setStateL,0,self.d_setStateR)[index]("Closed")