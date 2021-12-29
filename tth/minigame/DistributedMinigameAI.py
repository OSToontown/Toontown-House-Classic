from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.distributed.ClockDelta import globalClockDelta
from direct.interval.IntervalGlobal import *

from direct.fsm.FSM import FSM

from panda3d.core import *

#states are:
#Off
#Wait
#Play
#Gags
#Cleanup

class DistributedMinigameAI(DistributedObjectAI, FSM):
    def __init__(self,cr):
        DistributedObjectAI.__init__(self,cr)
        FSM.__init__(self,'MinigameAI')
        
        self.__state = ("Off",0)   
        self.ready = 0
        self.done = 0
        self.reached = 0
        
    def setToons(self, toons):
        self.toons = toons
    
    def d_setToons(self,toons):
        self.sendUpdate('setToons',toons)
        
    def getToons(self):
        return self.toons
        
    def setState(self, state):
        self.__state = (state,globalClockDelta.localElapsedTime(globalClock.getFrameTime(), bits=32))
        self.request(state)
        
    def d_setState(self, state, ts):
        self.__state = (state,ts)
        self.sendUpdate('setState',[state,ts])
        
    def b_setState(self, state):
        lts = globalClock.getFrameTime()
        ts = globalClockDelta.localElapsedTime(lts, bits=32)
        
        self.setState(state)
        self.d_setState(state,ts)
        
    def getState(self):
        return self.__state
        
    def reportDone(self):
        self.done += 1
        if self.ready == len(self.toons):
            self.b_setState("Cleanup")
        
    def reportReady(self):
        self.ready += 1
        if self.ready == len(self.toons):
            self.b_setState("Play")
            
    def reachedZone(self):
        self.reached += 1
        if self.reached == len(self.toons):
            self.allReached()
            
    def allReached(self):
        self.b_setState("Wait")
        
    def enterCleanup(self):
        self.manager.freeTrolleyZone(self.zoneId)
        
    def getDifficulty(self):
        return self.zoneId % 10**7 // 1000