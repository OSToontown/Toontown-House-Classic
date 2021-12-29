from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.distributed.ClockDelta import globalClockDelta
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *

from direct.fsm.FSM import FSM

from direct.task.Task import Task

class DistributedRocketAI(DistributedObjectAI,FSM):
    def __init__(self,cr):
        FSM.__init__(self,'RocketAIFSM')
        DistributedObjectAI.__init__(self,cr)
        
        self._state = []
        
    def generate(self):
        DistributedObject.generate(self)
            
    def enterWait(self): pass 
    def exitWait(self): pass 
               
    def enterLaunched(self): pass
    def exitLaunched(self):
        taskMgr.doMethodLater(1800,lambda t: self.setState('Launched'),"LaunchRocket") #1/2 hour
        
    def setState(self, state):
        t = globalClock.getFrameTime()
        self._state = [state,t]
        self.request(state)
        self.sendUpdate("setState",[state,globalClockDelta.localToNetworkTime(t)])
        
    def getState(self):
        return self._state
        