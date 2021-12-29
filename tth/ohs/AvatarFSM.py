from panda3d.core import *
from direct.interval.IntervalGlobal import *
from direct.fsm.FSM import *
from pandac.PandaModules import *

from direct.actor.Actor import Actor

from tth.fishing import FishingFSM

class AvatarFSM(FSM,FishingFSM.FishingFSM):
    def setToon(self,toon):
        self.toon = toon
        
    def __getBooks(self):
        try:
            self.__books
        
        except:
            _b = Actor("phase_3.5/models/props/book-mod.bam",{'x':"phase_3.5/models/props/book-chan.bam"})
            _b2 = Actor(other=_b)
            _b3 = Actor(other=_b)
        
            self.__books = (_b,_b2,_b3)
            for book, hand in zip(self.__books,self.toon.toon.getRightHands()):
                book.reparentTo(hand)
                book.hide()
                
        return self.__books
        
    def __init__(self):
        FSM.__init__(self,'AvatarFSM')
        FishingFSM.FishingFSM.__init__(self)
        
        self.toon = None
        self.walkingFootStep = loader.loadSfx('phase_3.5/audio/sfx/AV_footstep_runloop.wav')
        self.walkingFootStep.setLoop(1)
        self.teleportsound = loader.loadSfx('phase_3.5/audio/sfx/AV_teleport.mp3')

    def enterSit(self,arg,ts):
        self._anim('sit')
    
    def enterWalk(self,arg,ts):
        self._anim(arg)
        if self.toon.isLocalToon:
            self.walkingFootStep.play()
            
    def exitWalk(self):
        if self.toon.isLocalToon:
            self.walkingFootStep.stop()
    
    def enterNone(self,arg,ts): pass
    def exitNone(self): pass
    
    def __showBooks(self):
        for book in self.__getBooks():
            book.show()
            
    def __hideBooks(self):
        for book in self.__getBooks():
            book.hide()
    
    def enterOpenBook(self,arg,ts): 
        self.toon.toon.stopLookAround()
        self.toon.toon.lerpLookAt(Point3(0, 1, -2))
        bookTrack = Parallel()
        
        for book in self.__getBooks():
            bookTrack.append(ActorInterval(book, 'x', startTime=1.2, endTime=1.5))
        
        bookTrack.append(ActorInterval(self.toon.toon, 'book', startTime=1.2, endTime=1.5))
            
        trackName = 'openBook'
        track = Sequence(Func(self.__showBooks), bookTrack, Wait(0.1), name=trackName)
        track.start(ts)
        
    def enterReadBook(self,arg,ts):
        self.toon.toon.stopLookAround()
        self.toon.toon.lerpLookAt(Point3(0, 1, -2))
        self.__showBooks()
        for bookActor in self.__getBooks():
            bookActor.pingpong('x', fromFrame=38, toFrame=118)

        self.toon.toon.pingpong('book', fromFrame=38, toFrame=118)
        
    def enterCloseBook(self,arg,ts):
        bookTracks = Parallel()
        for bookActor in self.__getBooks():
            bookTracks.append(ActorInterval(bookActor, 'x', startTime=4.96, endTime=6.5))

        bookTracks.append(ActorInterval(self.toon.toon, 'book', startTime=4.96, endTime=6.5))
        trackName = 'closeBook'
        track = Sequence(Func(self.__showBooks), bookTracks, Func(self.__hideBooks), name=trackName)
        track.start(ts)
        
    def enterNeutral(self,arg,ts): 
        self.walkingFootStep.stop()
        self._anim('neutral')
        
    def exitNeutral(self): pass
    
    def enterJump(self,arg,ts): self._anim('jump-zhang')
    def exitJump(self): pass
    
    def __getHoles(self):
        try:
            self.__holeActors
        except:
            holeActor = Actor('phase_3.5/models/props/portal-mod', {'hole': 'phase_3.5/models/props/portal-chan'})
            holeActor2 = Actor(other=holeActor)
            holeActor3 = Actor(other=holeActor)
            self.__holeActors = [holeActor, holeActor2, holeActor3]
            for ha in self.__holeActors:
                holeName = 'toon-portal'
                ha.setName(holeName)

        return self.__holeActors
    
    def enterTeleport(self,target=None,ts=None):
        if self.toon.isLocalToon:
            gamebase.curArea.disableControls()
            gamebase.curArea.destroyHud()
            #aspect2d.stash()

        def showHoles(holes, hands):
            for hole, hand in zip(holes, hands):
                hole.reparentTo(hand)

        def reparentHoles(holes, toon):
            holes[0].reparentTo(toon)
            holes[1].detachNode()
            holes[2].detachNode()
            holes[0].setBin('shadow', 0)
            holes[0].setDepthTest(0)
            holes[0].setDepthWrite(0)

        def cleanupHoles(holes):
            holes[0].detachNode()
            holes[0].clearBin()
            holes[0].clearDepthTest()
            holes[0].clearDepthWrite()

        holes = self.__getHoles()
        hands = self.toon.toon.getRightHands()
        holeTrack = Track((0.0, Func(showHoles, holes, hands)), (0.5, SoundInterval(self.teleportsound, node=self.toon.toon)), (1.708, Func(reparentHoles, holes, self.toon.toon)), (3.4, Func(cleanupHoles, holes)))
        trackName = 'teleportOut'
        track = Parallel(holeTrack, name=trackName, autoFinish=1)
        for hole in holes:
            track.append(ActorInterval(hole, 'hole', duration=3.4))

        track.append(ActorInterval(self.toon.toon, 'teleport', duration=3.4))
        
        s = Sequence(track)
        if target not in [None,"None"] and self.toon.isLocalToon:
            s.append(Func(base.hoodMgr.bookTp,int(target)))
        
        s.start(ts)
    
    def exitTeleport(self): 
       aspect2d.unstash()
       #self._anim('teleport',-1,False) #wtf
       
    def enterSwim(self,arg,ts):
        self._anim('swim')
 
    def _anim(self,*args):
        self.toon.toon.anim(*args)
        
