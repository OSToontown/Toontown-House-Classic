from direct.distributed.DistributedObject import *
from direct.distributed.ClockDelta import globalClockDelta

from direct.interval.IntervalGlobal import *

CLOSEDELAY = 2.5
    
class LocalDoor:
    def __init__(self, doorModel, doorMask, area, dest): 
        #try to find the trigger
        self.cNp = doorModel.find('**/*trigger*')
        if self.cNp.isEmpty():
            self.cNp = doorModel.find('**/*sphere*')
            if self.cNp.isEmpty():
                raise ToontownHouseError('Door 0x001: can\'t handle this door!')
            
        #self.cNp.show()
            
        self.cnode = self.cNp.node()
        self.cnode.setCollideMask(doorMask)
        
        if not hasattr(area,"collDict"): area.collDict={}
        area.collDict[self.cnode] = self.goInto
        
        self.area = area
        self.dest = dest
        self.model = doorModel
        
    def goInto(self,entry):
        print ':Door: Going into',self
        self.cNp.removeNode()        
        #self.area.disableControls()
        
        av = self.area.avatar

        av = self.area.avatar
        av.reparentTo(self.model)
        
        self.area.toon.b_setState("Walk","run")
        
        av.setH(0)
        
        messenger.send("openDoor_"+self.model.getName(),["R"])
        
        Sequence(
                 #av.posInterval(2,(0,10,0),(0,0,0)),
                 #Func(Teleporter(*self.dest).go)
                ).start()

    def __repr__(self):
        return 'Door from {0} to {1}; name = {2}'.format(self.area.name,self.dest[1],self.model.getName())
    
class DoorHandler:
    def __init__(self):
       self.target = None
       self.leftDoor = None
       self.rightDoor = None
       
    def setTarget(self,target,task=None):
        if not (gamebase.curArea and gamebase.curArea.np):
            if not task:
                taskMgr.doMethodLater(.5,lambda task:self.setTarget(target,task),"set door target")
                return
            else:
                return task.again
                
        self.target = gamebase.curArea.np.find("**/"+target)
        #detect doors
        self.leftDoor = self.target.find('**/left*')
        self.rightDoor = self.target.find('**/right*')
        
        print 'DOOR:',self,'setTarget',self.target
        
    def request(self,*a):pass

class DistributedDoor(DistributedObject):
    def __init__(self,cr):
        DistributedObject.__init__(self,cr)
        self.handler = DoorHandler()
        print 'DOOR:',self,'created!'
       
    def setState(self,stateL,tsL,stateR,tsR):
        print 'DOOR:',self,'set state',stateL,tsL,stateR,tsR
        timeL = globalClockDelta.localElapsedTime(tsL)
        timeR = globalClockDelta.localElapsedTime(tsR)
        self.handler.request((stateL,stateR),(timeL,timeR))
        
    def setTarget(self,target):
        self.handler.setTarget(target)
        self.accept("openDoor_"+target,self._open)
        
    def _open(self,side):
        self.sendUpdate("requestEnter",[side])
        
    def disable(self):
        DistributedObject.disable(self)
        del self.handler

    def detectLeaks(self): pass #fixes a crash
        