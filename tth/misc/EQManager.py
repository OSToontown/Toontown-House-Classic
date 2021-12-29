#usage of EQ:
# - short for "EarthQuake"
# - no spoiling if someone reads the dc file
from direct.distributed.DistributedObject import DistributedObject
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.distributed.ClockDelta import globalClockDelta

from direct.interval.IntervalGlobal import *
from direct.fsm.FSM import FSM

from panda3d.core import Point3

class DistributedEQMgr(DistributedObject, FSM):
    tremorPoints = ((.4,1),(.1,.6),(.3,-.3),(.1,0))
    def __init__(self,cr):
        DistributedObject.__init__(self,cr)
        FSM.__init__(self,'EQMgr')
    
    def generate(self):
        self.shakeSfx = loader.loadMusic('phase_5/audio/sfx/SA_tremor.mp3')
        self.shakeSfx.setLoop(1)
        
        self.shakeSeq = Sequence()
        for time,z in self.tremorPoints:
            self.shakeSeq.append(render.posInterval(time,Point3(0,0,z)))
        
    def setState(self,state,ts):
        ts = globalClock.getFrameTime() - globalClockDelta.networkToLocalTime(ts,bits=32)
        self.request(state,max(ts,-ts))
        
    def enterShake(self,ts):
        self.shakeSeq.loop()
        self.shakeSeq.setT(ts)
        
        self.shakeSfx.play()
        try:
            gamebase.curArea.theme.setVolume(.2)
            
        except:
            raise #pass
        
    def exitRain(self):
        self.shakeSeq.finish()
        self.shakeSfx.stop()
        
        try:
            gamebase.curArea.theme.setVolume(1)
            
        except:
            pass
        
class DistributedEQMgrAI(DistributedObjectAI):        
    pass
    