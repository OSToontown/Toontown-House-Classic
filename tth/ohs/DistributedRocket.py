from direct.distributed.DistributedObject import DistributedObject
from direct.distributed.ClockDelta import globalClockDelta
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *

from direct.fsm.FSM import FSM

from direct.task.Task import Task

class DistributedRocket(DistributedObject,FSM):
    def __init__(self,cr):
        FSM.__init__(self,'RocketFSM')
        DistributedObject.__init__(self,cr)
        
        self._area = None
        
    def generate(self):
        DistributedObject.generate(self)
        taskMgr.doMethodLater(.5,self.__initGoem,'blah')
            
    def enterWait(self, ts): pass 
    def exitWait(self): pass 
               
    def enterLaunched(self,ts,task=None):
        print 'Launched!',ts
        if not self._area:
            taskMgr.doMethodLater(.5,self.enterLaunched,"el2",extraArgs=[ts])
            return Task.done
            
        self._area.startFireworks(ts)
        return Task.done
        
    def exitLaunched(self): pass
        
    def setState(self, state, timestamp):
        self.request(state, [globalClockDelta.localElapsedTime(timestamp)])
        
    def __initGoem(self,task):
        if not gamebase.curArea: return task.again
        if not gamebase.curArea.np: return task.again
    
        a = gamebase.curArea
        a.loadRocket()
        
        self._area = a