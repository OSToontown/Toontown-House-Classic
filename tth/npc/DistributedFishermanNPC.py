from DistributedBlockingNPC import DistributedBlockingNPC
from DistributedBlockingNPCAI import DistributedBlockingNPCAI
from panda3d.core import *

from tth.fishing.FishSellGUI import FishSellGUI, FishTank
from tth.gui.SpeechBubble import NPCSpeechBubble

from direct.gui.DirectGui import DirectFrame

from tth.managers import GUIClock
from tth.npc.NPCGlobals import Fishermen

class DistributedFishermanNPC(DistributedBlockingNPC):
    chat = {
            0:L10N.FishermanSaleCancel,
            1:L10N.FishermanSaleDone,
            2:L10N.FishermanSaleBonus,
            3:L10N.NPCTimeout,
           }
           
    def __init__(self,cr):
        DistributedBlockingNPC.__init__(self,cr)
        self.__attemptingToGoIn = 0
        self.gui = None
        self.sb = None
        self.dummyEA = make_buffer(tuple())
        
    def touched(self,_):
        if not (self.isBusy() or self.__attemptingToGoIn):
            self.d_requestUse()
            self.__attemptingToGoIn = 1
            
    def reject(self):
        self.__attemptingToGoIn = 0
        
    def enter(self,time):
        self.__attemptingToGoIn = 0
        self.notify.info('entering npc (timeout = %d)' % time)
        self.b_lookAtAvatar(gamebase.curArea.avatar)
        
        gamebase.curArea.disableControls()
        gamebase.curArea.obscureBookAndFL(1)
        gamebase.curArea.toon.b_setState('Neutral')
        
        tank = FishTank.makeLocalTank()
        if not len(tank):
            self.gui = DirectFrame() #place holder
            self.clock = DirectFrame() #place holder
            self.__guiDone(0)
            return
        
        self.gui = FishSellGUI('sellFishGuiDone')
        self.acceptOnce('sellFishGuiDone',self.__guiDone)
        self.clock = GUIClock(time,lambda:0)
        
    def __guiDone(self,status,to = 0):
        if status:
            hist = FishTank.makeLocalHistory()
            tank = FishTank.makeLocalTank()
            
            startSpc = hist.getTotalSpecies()
            hist.addTank(tank)
            
            tank.sellAll()
            hist.save()
            
            newSpc = hist.getTotalSpecies()
            delta = (newSpc-startSpc)
            bonus = delta // 10
            
            print 'Fish sold: Start spc: %d, End Spc: %d, Delta: %d, Bonus: %d' % (startSpc,newSpc,delta,bonus)
            
            if bonus:
                st = gamebase.toonAvatarStream
                cHp = int(st.read("hp"))
                nHp = cHp + bonus
                st.write("hp",nHp)
                
                ccHp = int(st.read("curhp"))              
                deltaHp = nHp - ccHp
                
                #wait a few seconds
                #so the effect can be seen
                taskMgr.doMethodLater(2.5,lambda t: gamebase.curArea.toon.b_toonUp(deltaHp),"hp from fishing")
                
                self.b_setClChat(2,make_buffer((newSpc,)))
                
            else:
                self.b_setClChat(1,self.dummyEA)
                
        else:
            if not to:
                self.b_setClChat(0,self.dummyEA)
            
        self.gui.destroy()
        self.clock.destroy()
        gamebase.curArea.enableControls()
        gamebase.curArea.obscureBookAndFL(0)
        
        if not to:
            self.d_requestLeave()
        
    def timedOut(self):
        self.__guiDone(0,1)
        
    def setClChat(self,*args):
        r = DistributedBlockingNPC.setClChat(self,*args)
        
        if not r:
            return
            
        if self.sb and self.sb.exists:
            self.sb.destroy()
            
        self.sb = NPCSpeechBubble(self.toon,r,self.BubbleTimeOut)
        
    def d_setClChat(self,i,a):
        self.sendUpdate('setClChat',[i,a])
        
    def b_setClChat(self,i,a):
        self.setClChat(i,a)
        self.d_setClChat(i,a)
            
class DistributedFishermanNPCAI(DistributedBlockingNPCAI):
    def onTimeOut(self,task):
        self.sendUpdate('setClChat',[3,make_buffer(tuple())])
        return DistributedBlockingNPCAI.onTimeOut(self,task)
        
    def announceGenerate(self):
        DistributedBlockingNPCAI.announceGenerate(self)
        self.origH = Fishermen[self.zoneId % 10**7][-1]