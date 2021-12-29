from direct.distributed.DistributedObject import DistributedObject
from direct.distributed.ClockDelta import globalClockDelta

import Cog, CogDNA, CogStates
from panda3d.core import BitMask32

walkMask = BitMask32(16|8)
elseMask = BitMask32(16)

def delayed(f):
    def wr(*a,**kw):
        taskMgr.doMethodLater(5,lambda t: f(*a,**kw),"delayed-func-%s-%d" % (f,id(f)))
        
    return wr

class SFXData:
    def __init__(self):
        self.custom = False
        self.sound = None
        self.index = -1
        
    def isCustom(self):
        return self.custom
        
    def play(self):
        if self.sound:
            self.sound.play()
        
    def getIndex(self):
        return self.index
        
class CogSfxMgr:
    cache = {}
    def get(self,cat,index):
        if index in self.cache:
            return self.cache[index]
            
        filename = "phase_0/audio/cogs/%s/%s.ogg" % (cat,index)
        f = loader.loadSfx(filename)#,okMissing = True)
        if not f:
            return
            
        self.cache[index] = f
        return f
        
cogSfxMgr = CogSfxMgr()

class DistributedCog(DistributedObject):
    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        self.cog = Cog.Cog() #empty cog
        
        self.ttb = 0
        
    def setState(self,state,arg,ts):
        ts = globalClock.getFrameTime() - globalClockDelta.networkToLocalTime(ts,bits=32)
        self.fsm.request(state,arg,max(ts,-ts))
        
    def setDNA(self,dnaString):
        dna = CogDNA.CogDNA()
        dna.makeFrom(dnaString)
        
        self.fsm = CogStates.getFSM(dna.dept,dna.leader)(self,self.cog)
        
        self.cog.reload(dna.make())
        self.cog.reparentTo(render)
        
        taskMgr.doMethodLater(5,self.__initColl,"init coll for cog %s" % (self.doId))
        
    def __initColl(self,task=None):
        gamebase.curArea.collDict = getattr(gamebase.curArea,"collDict",{})
        gamebase.curArea.collDict[self.cog.cnp.node()] = self.__touch
        
        self.cog.cnp.node().setCollideMask(walkMask)
        
        if task: return task.done
        
    def __touch(self,entry):
        if self.ttb: return
        self.notify.info('cog %d touched, issuing battle request...' % self.doId)
        self.cog.cnp.node().setCollideMask(elseMask)
        gamebase.curArea.collDict[self.cog.cnp.node()] = lambda e:0
        self.sendUpdate('requestBattle',[])
        self.ttb = 1

    def delete(self):      
        del self.fsm
        
        self.cog.cleanup()
        self.cog.removeNode()
        
        DistributedObject.delete(self)
        
    def setChat(self,index):
        spc = L10N.cogSpeech(index)
        text = spc.value
        
        sfx = SFXData()
        if base.config.GetInt('want-cog-sfx',1):
            csfx = cogSfxMgr.get(spc.category,spc.index)
            if csfx:
                sfx.custom = True
                sfx.sound = csfx
                
            else:
                sfx.sfxIndex = 2
            
        self.cog.speak(text,sfx)
       
    @delayed
    def battleRejected(self):
        self.cog.cnp.node().setCollideMask(walkMask)
        gamebase.curArea.collDict[self.cog.cnp.node()] = self.__touch
        self.ttb = 0
        
    #trap door: if a client creates a cog (hacker), gets banned xD (actually just kicked atm)
    def getState(self): return ("Off","",0)
    def getDNA(self): return self.cog.dna.make()
    