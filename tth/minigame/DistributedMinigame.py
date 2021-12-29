from direct.distributed.DistributedObject import DistributedObject
from direct.distributed.ClockDelta import globalClockDelta
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *

from direct.fsm.FSM import FSM

from panda3d.core import *

class DistributedMinigame(DistributedObject, FSM):
    def __init__(self,cr):
        DistributedObject.__init__(self,cr)
        FSM.__init__(self,'Minigame')
        
        self.mgNp = render.attachNewNode('MinigameNP')
        
    def setState(self, state, ts):
        self.request(state, globalClockDelta.localElapsedTime(ts, bits=32))
        
    def generateInit(self):
        DistributedObject.generateInit(self)
        self.sendUpdate('reachedZone',[])
        
    def setToons(self,toons):
        self.toons = toons
        
    def loadEnviron(self):
        gamebase.curArea.setDistMg(self)
         
    def disable(self):
        DistributedObject.disable(self)
        self.mgNp.removeNode()
        
    def enterWait(self, ts):
        self.startTime = ts
        self.loadEnviron()
        