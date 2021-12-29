from DistributedNPC import DistributedNPC
import math

obscureHSetter = 0
lookAtAvDist = 4

class DistributedBlockingNPC(DistributedNPC):
    chat = {}
    BubbleTimeOut = 8
    def __init__(self,cr):
        DistributedNPC.__init__(self,cr)
        self.cUser = 0
        
    def isBusy(self):
        return self.cUser != 0
      
    def d_requestUse(self):
        if self.isBusy(): return
        self.sendUpdate('requestUse',[])
        
    def d_requestLeave(self):
        self.sendUpdate('requestLeave',[])
        
    def setToon(self,t):
        self.cUser = t
        
    def reject(self):
        pass
        
    def enter(self,timeout):
        #this is supossed to be overwritten
        #by a subclass
        pass
        
    def timedOut(self):
        #same of enter
        pass
        
    def b_lookAtAvatar(self,av):        
        ax, ay = tuple(self.getPos())[:2]
        bx, by = tuple(av.getPos())[:2]
        ang = math.atan2(by-ay, bx-ax) * (180/math.pi) - 90
        
        self.sendUpdate('setClH',[ang])
        self.setH(ang)
        
        av.setH(ang-180)
        
        p = self.getPos()
        angR = (ang+90)*(math.pi/180)
        p[0] += lookAtAvDist * math.cos(angR)
        p[1] += lookAtAvDist * math.sin(angR)
        av.setPos(p)
        
    if obscureHSetter:
        def setH(self,h):
            print 'attempt to set NPC %d obscured H to %d, ignoring...' % (self.doId,h)
            
    def setClChat(self,index,extraArgsBuff):
        extraArgsBuff = load_buffer(extraArgsBuff)
        if not index in self.chat.keys():
            return
            
        try:
            return self.chat[index] % extraArgsBuff
            
        except:
            return
            