from direct.distributed.DistributedObjectAI import DistributedObjectAI
from direct.distributed.ClockDelta import globalClockDelta
import CogDNA

class DistributedCogAI(DistributedObjectAI):
    def __init__(self, cr):
        DistributedObjectAI.__init__(self, cr)
        self.state = ("Off","",0)
        self.dna = CogDNA.CogDNA()
        
        self._np = None
        self._seq = None
        
    def setState(self,state,arg,ts=None):        
        if not ts: ts = globalClockDelta.localToNetworkTime(globalClock.getFrameTime(),bits=32)
        
        if state == "Walk":
            self.__handleWalk(*(arg+(ts,)))
            arg = ""
            
        else: self.__handleExitWalk() 
        
        self.state = (state,arg,ts)
        self.sendUpdate('setState',self.state)
        
        #print 'CogAI->setState',self.state
        
    def getState(self):
        return self.state
        
    def setDNA(self,dnaString):
        self.dna.makeFrom(dnaString)
        self.sendUpdate('setDNA',[self.dna.make()])
        
    def getDNA(self):
        return self.dna.make()
        
    def announceGenerate(self):
        DistributedObjectAI.announceGenerate(self)
        w = base.air.id2c(self.doId)
        if w != 1:
            print '!!!! FOUND NON-AI COG %s, CREATED BY %s!! DESTROYING AND BANNING CLIENT (BAN LEVEL 0)' % (self.doId,w)
            base.sr.kickById(w)
            
    def __handleWalk(self,np,seq,ts):
        if self._seq: self._seq.finish()
        if self._np: self._np()
        
        self._np = np
        self._seq = seq
        
        self._seq.loop()
        self._seq.setT(ts)
        
    def __handleExitWalk(self):
        self._np = None
        self._seq = None
        
    def getPos(self):
        if self._np and self._seq: return self._seq.getT(),self._np.getPos()
        return 0,(0,0,0)
        
    def requestBattle(self):
        #auto-reject
        
        rejectMsg = L10N.cogSpeechAI(1,(self.dna.dept,self.dna.leader))
        #print rejectMsg
        
        self.sendUpdate('setChat',[rejectMsg])
        self.sendUpdateToChannel(self.cr.getAvatarIdFromSender(),'battleRejected',[])
        