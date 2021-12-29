from direct.distributed.DistributedObject import DistributedObject
from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.distributed.ClockDelta import globalClockDelta

from direct.interval.IntervalGlobal import *
from direct.fsm.FSM import FSM

from panda3d.core import Point3
import random

def instancedNp(f):
    def wrap(*args):
        r = f(*args)
        return r.copyTo(hidden)
    return wrap

class DistributedRainMgr(DistributedObject, FSM):
    wdropModel = "phase_0/models/waterdrop"
    cloudZ = 50
    xRange = 100
    
    groundZ = -100
    dropTime = abs(groundZ/10)
    #a very bad concept of gravity 10, and
    #gravity is acceleration not constant speed
    #like this lol
   
    dropsPerSec = 75
    dropDelay = 1
    
    wdropNp = None
    
    @instancedNp
    def getDrop(self):
        if DistributedRainMgr.wdropNp:
            return DistributedRainMgr.wdropNp
            
        wd = loader.loadModel(self.wdropModel)
        #wd.setAlphaScale(.75)
        DistributedRainMgr.wdropNp = wd
        return wd
    
    def __init__(self,cr):
        DistributedObject.__init__(self,cr)
        FSM.__init__(self,'RainMgr')
    
    def generate(self):
        self.rainSfx = loader.loadMusic('phase_0/audio/tthrain.wav')
        self.rainSfx.setVolume(100)
        self.rainSfx.setLoop(1)
        
    def setState(self,state,ts):
        ts = globalClock.getFrameTime() - globalClockDelta.networkToLocalTime(ts,bits=32)
        self.request(state,max(ts,-ts))
        
    def enterRain(self,_):
        self.rainSeq = Sequence(Wait(self.dropDelay),Func(self.__rain))
        self.rainSeq.loop()
        self.rainSfx.play()
        try:
            gamebase.curArea.theme.setVolume(.2)
            
        except:
            raise #pass
        
    def exitRain(self):
        self.rainSeq.finish()
        self.rainSfx.stop()
        
        try:
            gamebase.curArea.theme.setVolume(1)
            
        except:
            pass
        
    def __rain(self):
        for i in xrange(self.dropsPerSec):
            d = self.getDrop()
            d.reparentTo(base.cam)
            pos = ((self.xRange/2.)-random.randint(0,self.xRange),random.randint(0,100),random.randint(7,15))
            d.setPos(pos)
            d.setScale(.025,.025,.03)
            d.setH(90)
        
            pos2 = Point3(pos)
            pos2.setZ(self.groundZ)
        
            d.wrtReparentTo(render)
        
            Sequence(
                     d.posInterval(self.dropTime,pos2),
                     Func(d.removeNode)
                     ).start()
        
class DistributedRainMgrAI(DistributedObjectAI):        
    pass
    