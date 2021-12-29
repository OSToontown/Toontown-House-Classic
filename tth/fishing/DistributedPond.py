from direct.distributed.DistributedObject import DistributedObject
from direct.distributed.ClockDelta import globalClockDelta
from direct.interval.IntervalGlobal import *

from panda3d.core import *

from tth.gui import FishingGui, dialog
from tth.managers import GUIClock
import FishingGlobals, Fish, FishPanel, FishTank, struct

BusyMask = BitMask32(2)
EmptyMask = BitMask32(2) | BitMask32(8)

class DistributedPond(DistributedObject):
    def announceGenerate(self):
        DistributedObject.announceGenerate(self)
        taskMgr.doMethodLater(2,self.__initGeom,"init geom of pond %d" % self.doId)
        
        self.fishes = []
        self.toons = [0,0,0,0]
        
        self.isEstate = False
        self.cReq = None
        self.__cCaughtFish = None
        
    def __initGeom(self,task):
        try:
            self.pondNp = gamebase.curArea.environ.find("**/fishing_spot*").getParent()
            self.piers = self.pondNp.findAllMatches('**/board')
            
            for index,pier in enumerate(self.piers):
                cnode = pier.getParent().find('**/floor*coll*').node()
                cnode.setCollideMask(BitMask32(8)|BitMask32(2))
                cnode.setPythonTag("pierIndex",index)
                
                gamebase.curArea.collDict = getattr(gamebase.curArea,"collDict",{})
                gamebase.curArea.collDict[cnode] = self.__enter
                        
                #format the origin
                dummy = pier.attachNewNode('avOrigin')
                pos = dummy.getPos(gamebase.curArea.np)
                h = dummy.getH(gamebase.curArea.np)
                
                pier.setPythonTag('avOrigin',pos)
                pier.setPythonTag('avOriginH',h)
            
        except AttributeError as e:
            #print 'init geom failed',e
            return task.again
            
        else:
            #print 'init geom completed'
            return task.done
        
    def addFish(self,fish):
        self.fishes.append(fish)
            
    def setEstate(self,estate):
        self.isEstate = bool(estate) 
        self.radius,self.waterLevel = FishingGlobals.getTargetRadius(self.getArea()),FishingGlobals.getWaterLevel(self.getArea())
        
    def getArea(self):
        if self.isEstate: return "estate"
        return self.zoneId % 10**7
        
    def __enter(self,entry):
        if not self.cReq or self.hasLocalToon():
            index = entry.getIntoNode().getPythonTag('pierIndex')
            self.d_requestEnter(index)
        
    def d_requestEnter(self,index):
        self.sendUpdate('requestEnter',[index])
        self.cReq = index
        
    def d_requestExit(self):
        self.sendUpdate('requestExit',[])
        
    def setToons(self,t1,t2,t3,t4):
        self.toons = (t1,t2,t3,t4)
        for index,toon in enumerate((t1,t2,t3,t4)):
            self._setPierBusy(index,toon != 0)
            
    def _setPierBusy(self,index,flag = False):
        try:
            self.piers
            
        except:
            taskMgr.doMethodLater(2,lambda t:self._setPierBusy(index,flag),"re-setPierBusy")
            return
       
        pier = self.piers[index]
        cnode = pier.getParent().find('**/floor*coll*').node()
        
        _mask = EmptyMask
        if flag: _mask = BusyMask
        
        #print 'setting pier',flag,_mask
        
        cnode.setCollideMask(_mask)
        
    def accept(self):
        if self.cReq is None:
            return #ignore
        
        self.__accepted()
        
    def reject(self):
        self.cReq = None
        
    def __accepted(self):
        print 'accepted to pier %s, entering...' % self.cReq
        av = gamebase.curArea.avatar
        
        p1 = av.getPos()
        p2 = self.piers[self.cReq].getPythonTag('avOrigin')
        
        h1 = av.getHpr()
        h2 = Vec3(self.piers[self.cReq].getPythonTag('avOriginH'),0,0)
        
        d = (p1-p2).length()
        dh = (h1-h2).length()
        
        posI = av.posInterval(d/4,p2,p1)
        hI = av.hprInterval(dh/60,h2,h1)
        
        gamebase.curArea.disableControls()
        gamebase.curArea.obscureBookAndFL(1)
        
        gamebase.curArea.toon.b_setState('Walk','run')
        Sequence(ParallelEndTogether(posI,hI),Func(self.__setupFishing)).start()
        
        self.cReq = None
        
    def hasLocalToon(self):
        return base.cr.doIdBase in self.toons
        
    def __setupFishing(self):
        rodIndex = gamebase.toonAvatarStream.read("rod",0)
        t = gamebase.curArea.toon
        
        def __setCamera():
            base.cam.setPos(Point3(0,-27,30))
            base.cam.setP(-38)
            base.cam.wrtReparentTo(render)
            
        def __setGui():
            self.gui = FishingGui.FishingFrame(self,t)
        
        Parallel(
                 Func(t.b_setState,'FishEnterPier',str(rodIndex)),
                 Func(__setCamera),
                 Sequence(
                    Wait(1.95),
                    Func(t.b_setState,'FishNeutral',str(rodIndex)),
                    Func(__setGui),
                 )
                ).start()
                
        base.acceptOnce('quitFishing',self.__quitFishing)
        base.accept('catchFish',self.__catchFish)
        
        self.tank = FishTank.FishTank(gamebase.toonAvatarStream)
        self.timer = GUIClock(45,self.__timeOut)
        self.hist = FishTank.makeLocalHistory()
        self.hist.addTank(self.tank)
        
        self.panel = FishPanel.FishPanel(None,doneEvent = 'fishPanelDone')
        self.panel.setSwimBounds(-0.3, 0.3, -0.235, 0.25)
        self.panel.setSwimColor(1.0, 1.0, 0.74901, 1.0)
        self.panel.setPos(0,0,.5)
        self.panel.hide()
                
    def __quitFishing(self):
        t = gamebase.curArea.toon
        av = gamebase.curArea.avatar
        self.cArea = gamebase.curArea
        
        base.cam.reparentTo(av)
        base.cam.setPos(0,-20,4.7)
        base.cam.setHpr(0,0,0)
        
        p = av.getPos()

        dummy = av.attachNewNode('dummy')
        dummy.setPos(p)
        dummy.setH(av.getH())
        dummy.setY(dummy,-10)

        p2 = dummy.getPos()
        dummy.removeNode()
        
        self.__fishPanelDone()
        self.gui.removeNode()
        self.timer.destroy()
        
        del self.tank
        del self.hist
        
        rodIndex = gamebase.toonAvatarStream.read("rod",0)
        Sequence(
                 Func(t.b_setState,'FishLeavePier',str(rodIndex)),
                 Wait(2),
                 Func(t.b_setState,'Walk','walk'),
                 av.posInterval(2,p2,p),
                 Func(self.cArea.enableControls),
                 Func(self.cArea.obscureBookAndFL,0),
                 Func(t.b_setState,'Neutral'),
                 Func(self.d_requestExit),
                ).start()
        
    def __catchFish(self):
        if self.__cCaughtFish is not None:
            print 'Already got fish (%s), ignoring...' % self.__cCaughtFish
            return
            
        rodIndex = gamebase.toonAvatarStream.read("rod",0)
            
        print
        print 'Generation of random fish'
        rarityBase,(index,subIndex) = FishingGlobals.getRandomFish(self.getArea(),rodIndex)
        weight = FishingGlobals.getRandomWeight(index,subIndex,rodIndex)
        print '\tRod:',rodIndex
        print '\tRarity base:',rarityBase
        print '\tWeight:',weight
        
        fish = Fish.Fish(index,subIndex,weight)
        print '\tFish:',fish
                
        base.acceptOnce('fishPanelDone',self.__fishPanelDone)
        base.acceptOnce('stopReeling',self.__stopReeling)
        
        t = gamebase.curArea.toon
        data = [gamebase.toonAvatarStream.read("rod",0)]+map(float,t.fsm.bob.getPos())
        t.b_setState("FishReel",struct.pack("H3d",*data))
        
        code = {1:1,2:2,3:0}[self.hist.compareFish(fish)]
        self.hist.addFish(fish)
        
        print '\tCode:',code
        print
        
        self.panel.update(fish)
        self.panel.show(code)
        
        self.tank.addFish(fish)
        
        self.__cCaughtFish = fish
        self.timer.resetTime(45)
        
    def __fishPanelDone(self):
        self.panel.hide()
        
        self.__cCaughtFish = None
        gamebase.curArea.toon.b_setState("FishNeutral",str(gamebase.toonAvatarStream.read("rod",0)))
        
    def __stopReeling(self):
        gamebase.curArea.toon.b_setState("FishNeutral",str(gamebase.toonAvatarStream.read("rod",0)))
        
    def canCast(self):
        if self.tank.isFull():
            self.castError(1)
            return False
            
        self.timer.resetTime(45)
        return True
            
    def castError(self,code):
        if code == 0:
            self.cDialog = dialog.OkDialog(
                                           text=L10N.FishingBroke, text_wordwrap = 18, command = self.__handleErrorDialog,
                                           relief=None, buttonGeomList=[dialog.okButtons], button_relief = None
                                           )
        
        elif code == 1:
            self.cDialog = dialog.OkDialog(
                                           text=L10N.FishingTankFull, text_wordwrap = 18, command = self.__handleErrorDialog,
                                           relief=None, buttonGeomList=[dialog.okButtons], button_relief = None
                                           )
                                           
        self.gui.stash()
                                           
    def __handleErrorDialog(self,_):
        self.cDialog.cleanup()
        self.cDialog = None
        self.__quitFishing()
        
    def __timeOut(self):
        try:
            self.cDialog.cleanup()
        except:
            pass
            
        self.__quitFishing()
        