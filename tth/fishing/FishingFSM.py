from direct.interval.IntervalGlobal import *
from direct.task.Task import Task
from direct.actor import Actor
from panda3d.core import *

from direct.showutil import Rope
from tth.effects import Ripples

from FishingGlobals import *

import struct, math, random

#im working on this and all fishing stuff, so stop editing all fish stuff plz!! thx

class FishingFSM:
    def __init__(self):
        self.rod = None
        self.lastCastData = ""
        
    def __loadRod(self,index,force = False):
        if self.rod:
            if not force:
                return
                
        rod = int(index)
        rodFile = RodFileDict.get(rod)
        
        if rodFile:
            rodModel = Actor.Actor(rodFile,{'cast': 'phase_4/models/props/fishing-pole-chan'})
            rodModel.pose('cast',0)
            self.ptop = rodModel.find('**/joint_attachBill')
            
            self.line = Rope.Rope('Line')
            self.line.setColor(1, 1, 1, 0.4)
            self.line.setTransparency(1)
            self.lineSphere = BoundingSphere(Point3(-0.6, -2, -5), 5.5)
            #self.lineSphere.setTransparency(1)
			
            self.bob = loader.loadModel('phase_4/models/props/fishing_bob')
            self.bob.setScale(1.5)
            self.bob.reparentTo(self.toon.toon)
            
            self.ripples = Ripples.Ripples(rodModel)
            self.ripples.setScale(0.4)
            self.ripples.hide()
            
            self.splashSounds = map(base.loadSfx,('phase_4/audio/sfx/TT_splash1.mp3','phase_4/audio/sfx/TT_splash2.mp3'))
            
        else:
            rodModel = Actor.Actor() #dummy
            
        av = self.toon.toon
        rightHand = av.rightHand
        rodModel.reparentTo(rightHand)
        self.rod = rodModel
        
        if self.toon.isLocalToon:
            self.__makeCollStuff()
    
    def enterFishEnterPier(self,arg,ts):
        self.__loadRod(arg)
        self.__hideLine()
        ActorInterval(self.toon.toon,"pole").start(ts)
        
    def enterFishNeutral(self,arg,ts):
        #print '**fishneutral'
        self.__loadRod(arg)
        self.__hideLine()
        self.toon.toon.loop("poleneutral")
        
    def enterFishLeavePier(self,arg,ts):
        self.__loadRod(arg)
        self.__hideLine()
        self.bob.removeNode()
        Sequence(
                 ParallelEndTogether(
                    self.rod.scaleInterval(2,(1,1,1),(0,0,0)),
                    ActorInterval(self.toon.toon,"pole",playRate = -1)
                 ),
                 Func(self.rod.cleanup),
                 Func(self.rod.removeNode)
                ).start(ts)
                
    def enterFishAim(self,arg,ts):
        self.__loadRod(arg)
        self.__hideLine()
        
    def enterFishCast(self,arg,ts):
        rod,angle,power,waterLevel = struct.unpack("H3d",arg)
        self.lastCastData = arg
        self.__loadRod(rod)
        
        av = self.toon.toon
        
        self.castTrack = Sequence(
                                  ActorInterval(av, 'castlong', playRate=4),
                                  ActorInterval(av, 'cast', startFrame=20),
                                  Func(av.loop, 'fish-neutral')
                                 )
                                 
        startT = 0.7 + (1 - power) * 0.3
        self.castTrack.start(startT)
        trackLocal = Sequence(
                              Wait(1.2 - startT),
                              Func(self.startMoveBobTask,power,waterLevel),
                              Func(self.__showLineCasting)
                             )
        
        trackOther = Parallel(
                              Sequence(
                                       ActorInterval(av, 'cast'),
                                       Func(self.rod.pose, 'cast', 0),
                                       Func(av.loop, 'fish-neutral')
                                      ),
                              Sequence(
                                       Wait(1.0),
                                       Func(self.startMoveBobTask,power,waterLevel),
                                       Func(self.__showLineCasting)
                                      )
                             )
        self.track = trackLocal if self.toon.isLocalToon else trackOther
        self.track.start(ts)
        
        #print angle,power,waterLevel,ts
        
    def enterFishReel(self,arg,ts):
        rod,bobX,bobY,bobZ = struct.unpack("H3d",arg)
        self.__loadRod(rod)
        
        self.bob.show()
        self.bob.setPos(Point3(bobX,bobY,bobZ))
        
        self.__showLineReeling()
        
        av = self.toon.toon
        self.reelTrack = Sequence(
                                  Parallel(
                                           ActorInterval(av, 'reel'),
                                           ActorInterval(self.rod, 'cast', startFrame=63, endFrame=127)
                                           ),
                                  ActorInterval(av, 'reelneutral'),
                                  Func(self.__hideLine),
                                  Func(self.bob.hide),
                                  ActorInterval(av, 'fishAGAIN'),
                                  )
        if self.toon.isLocalToon:
            self.reelTrack.append(Func(messenger.send,'stopReeling'))
            
        self.reelTrack.start()
        self.reelTrack.setT(ts)
        
    def exitFishCast(self):
        self.bob.hide()
        
    def exitFishReel(self):
        self.bob.hide()
        self.reelTrack.pause()
        del self.reelTrack
        
    def startMoveBobTask(self,power,wl):
        task = Task(self.moveBobTask)
        task.power = power
        task.waterLevel = wl
        self.bob.show()
        self.bob.setPos(Point3(0,3,8.5))
        taskMgr.add(task,"move bob")
        
    def __showLineWaiting(self):
        self.ptop.show()
        self.line.setup(4,
                         (
                          (None, (0, 0, 0)),
                          (None, (0, -2, -4)),
                          (self.bob, (0, -1, 0)),
                          (self.bob, (0, 0, 0))
                         )
                         )
        self.line.ropeNode.setBounds(self.lineSphere)
        self.line.reparentTo(self.ptop)

    def __showLineCasting(self):
        self.ptop.show()
        self.line.setup(2, ((None, (0, 0, 0)), (self.bob, (0, 0, 0))))
        self.line.ropeNode.setBounds(self.lineSphere)
        self.line.reparentTo(self.ptop)

    def __showLineReeling(self):
        self.ptop.show()
        self.line.setup(2, ((None, (0, 0, 0)), (self.bob, (0, 0, 0))))
        self.line.ropeNode.setBounds(self.lineSphere)
        self.line.reparentTo(self.ptop)
        
    def __hideLine(self):
        self.ptop.hide()
        
    def moveBobTask(self, task):
        g = 32.2
        t = task.time
        
        vZeroMax = 25.0
        angleMax = 30.0
        
        vZero = task.power * vZeroMax
        angle = deg2Rad(task.power * angleMax)
        deltaY = vZero * math.cos(angle) * t
        deltaZ = vZero * math.sin(abs(angle)) * t - g * t * t / 2.0
        deltaPos = Point3(0, deltaY, deltaZ)
        self.bobStartPos = Point3(0.0, 3.0, 8.5)
        pos = self.bobStartPos + deltaPos
        self.bob.setPos(pos)
        #print pos[2],
        if pos[2] < task.waterLevel:
            self.__showLineWaiting()
            SoundInterval(random.choice(self.splashSounds),node=self.toon.toon).start()
            self.toon.toon.loop('fishneutral')
            if self.toon.isLocalToon:
                self.startWatchBob()
            return Task.done
        else:
            return Task.cont
            
    def startWatchBob(self):
        print '**watching bob'
        self.bobCNodePath.unstash()
        self.wbTask = taskMgr.add(self.__bobCollTask,"bob coll task")
        base.accept('fishPanelDone',self.stopWatchBob)
        
    def stopWatchBob(self):
        print '**not watching bob'
        taskMgr.remove(self.wbTask)
        
    def __bobCollTask(self,task):
        self.fishingTrav.traverse(render)
        entriesNumb = self.collHand.getNumEntries() 
        
        if entriesNumb > 0:
            self.collHand.sortEntries()
            e = self.collHand.getEntry(0)
            node = e.getIntoNodePath()
            print '**got fishing collision into', node
            
            messenger.send('catchFish')
            return task.done
            
        return task.cont
        
    def __makeCollStuff(self):
        self.fishingTrav = CollisionTraverser('FishingTrav')
        self.collHand = CollisionHandlerQueue()
        
        self.bobCNode = CollisionNode('bobCollNode')
        self.bobCNode.setCollideMask(BitMask32(FishMask))
        
        self.bobSphere = CollisionSphere(0,0,0,self.bob.getBounds().getRadius()*1.25)
        self.bobCNode.addSolid(self.bobSphere)
        
        self.bobCNodePath = self.bob.attachNewNode(self.bobCNode)
        #self.bobCNodePath.show()
        
        self.fishingTrav.addCollider(self.bobCNodePath, self.collHand)
        self.fishingTrav.setRespectPrevTransform(True)