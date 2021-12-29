from direct.distributed.ClockDelta import globalClockDelta
from direct.interval.IntervalGlobal import *

from panda3d.core import *
import random

nonSeen = ~True
missed = ~False
ok = nonSeen * missed
group = missed - nonSeen

RING_STATIC = 0
RING_MOVING = 1

import MGZone
class RingGameZone(MGZone.MinigameZone):
    name = "AREA_MG_RIN"
    music = "phase_4/audio/bgm/MG_toontag.mid"
    
    localAvMask = BitMask32(8) | BitMask32(1)
    YOFFSET = 15

    def __init__(self,tp = None):
        self.origin = tp.origin
        MGZone.MinigameZone.__init__(self, tp, tp.zoneId, wantAvatar = True, wantCamera = False)
        self.avatar.physControls.setCollisionsActive(False)
        self.avatar.physControls.isAirbone = True
        
        self.pusher = CollisionHandlerPusher()
        self.pusher.addCollider(self.cNodepath, self.avatar)
        self.pusher.setHorizontal(0)
        base.cTrav.addCollider(self.cNodepath, self.pusher)
        
        base.cam.reparentTo(self.avatar)
        base.cam.setPos(0,0,-15)
        base.cam.setP(90)
        
        self.originalCamFar = base.camLens.getFar()
        self.originalCamFov = base.camLens.getFov()
        
        base.camLens.setFov(80)
        base.camLens.setFar(150)
        
        self.toon.b_setState('Swim')
        
        self.__fog = Fog('ringGameFog')
        self.__fog.setColor((0,0,.6,1))
        self.__fog.setLinearRange(0.1, 149)
        render.setFog(self.__fog)
        
        base.setBackgroundColor((0,0,.6,1))
        
        self.keyMap = {0:0,1:0,2:0,3:0}
        
        self.accept('arrow_up',self.handleKey,[0,1])
        self.accept('arrow_down',self.handleKey,[1,1])
        self.accept('arrow_left',self.handleKey,[2,1])
        self.accept('arrow_right',self.handleKey,[3,1])
        
        self.accept('arrow_up-up',self.handleKey,[0,0])
        self.accept('arrow_down-up',self.handleKey,[1,0])
        self.accept('arrow_left-up',self.handleKey,[2,0])
        self.accept('arrow_right-up',self.handleKey,[3,0])
        
        self.moveAvTaskName = base.cr.uniqueName('ring_game_move_av_task')
        taskMgr.add(self.moveAvTask,self.moveAvTaskName)
        
        #base.cam.wrtReparentTo(render) #finally stabilish the stupid camera
        
    def moveAvTask(self, task):
        if self.distMg:
            t = globalClock.getFrameTime() - self.distMg.startTime
            distance = t * self.YOFFSET
            distance %= 150
            distance += 20
            self.distMg.environNode.setY(-distance)
            
            if self.distMg.state == "Play":
                #down: -y
                #up: +y
                #left: -x
                if self.keyMap[0]:
                    pass #self.avatar.
            
        return task.cont
        
    def destroy(self):
        MGZone.MinigameZone.destroy(self)
        base.camLens.setFov(self.originalCamFov)
        base.camLens.setFar(self.originalCamFar)
        render.clearFog()
        taskMgr.remove(self.moveAvTaskName)
        
    def handleKey(self, key, code):
        self.keyMap[key] = code

    def __tth_area__(self):
        return {
                'name':"MGZone",
                'models':self.np,
                'bgm':self.theme,
                'gui':self.frame,
                'speeches':[]
                }

import DistributedMinigame
class DistRingGame(DistributedMinigame.DistributedMinigame):
    ENVIRON_LENGTH = 150.0
    SEA_FLOOR_Z = -35.0 / 2.0 + 3.0
    TOON_INITIAL_SPACING = 4.0
    TOON_Y = 0
    
    def __init__(self,cr):
        DistributedMinigame.DistributedMinigame.__init__(self,cr)
        self.originalTagData = {}
    
    def enterWait(self, ts):
        DistributedMinigame.DistributedMinigame.enterWait(self, ts)  
        for toon in self.toons:
            av = self.cr.identifyAvatar(toon)
            
            if not av:
                self.notify.warning('No such avatar %d' % toon)
                continue
            
            p = av.toon.tag.getParent()
            oPos = p.getPos()
            oHpr = p.getHpr()
            
            p.setPos(.2,-1,0)
            p.setHpr(90,0,-30)
            
            self.originalTagData[toon] = (oPos,oHpr)
    
    def loadEnviron(self):
        self.environModel = loader.loadModel('phase_4/models/minigames/swimming_game')
        self.environModel.setPos(0, self.ENVIRON_LENGTH / 2.0, self.SEA_FLOOR_Z)
        self.environModel.flattenMedium()
        
        self.environNode = self.mgNp.attachNewNode('environNode')
        self.environBlocks = []
        for i in range(0, 2):
            instance = self.environModel.instanceUnderNode(self.environNode, 'model')
            y = self.ENVIRON_LENGTH * i
            instance.setY(y)
            self.environBlocks.append(instance)
            for j in range(0, 2):
                instance = self.environModel.instanceUnderNode(self.environNode, 'blocks')
                x = self.ENVIRON_LENGTH * (j + 1)
                instance.setY(y)
                instance.setX(-x)
                self.environBlocks.append(instance)

            for j in range(0, 2):
                instance = self.environModel.instanceUnderNode(self.environNode, 'blocks')
                x = self.ENVIRON_LENGTH * (j + 1)
                instance.setY(y)
                instance.setX(x)
                self.environBlocks.append(instance)
               
        i = self.toons.index(self.cr.doIdBase)             
        x = i * self.TOON_INITIAL_SPACING
        x -= self.TOON_INITIAL_SPACING * (len(self.toons) - 1) / 2.0
        gamebase.curArea.avatar.setPosHpr(x, self.TOON_Y, 0, 0, -90, 0)
        
        DistributedMinigame.DistributedMinigame.loadEnviron(self)
        
    def setHitLevel(self, data):
        pass
       
    def setRingData(self, data):
        print 'Set ring data:', load_buffer(data)
        
import DistributedMinigameAI
class DistRingGameAI(DistributedMinigameAI.DistributedMinigameAI):
    numRings = 16

    def announceGenerate(self):
        DistributedMinigameAI.DistributedMinigameAI.announceGenerate(self)
               
        self.hitLevel = []
        for _ in self.toons:
            x = []
            for i in xrange(self.numRings):
                x.append(nonSeen)
                
            self.hitLevel.append(x)
            
        self.round = 0
        self.__r = 0
        
        #generate ring levels
        diff = self.getDifficulty()
        
        self.staticRings = int(self.numRings/(diff+.1))
        self.movingRings = self.numRings - self.staticRings
        
        allrings = [RING_STATIC]*self.staticRings
        allrings += [RING_STATIC]*self.movingRings
        random.shuffle(allrings)
        
        self.rings = allrings[:]
        self.ringsPos = []
        self.ringsTracks = []
        
        numPlayers = len(self.toons)
        for ring in self.rings:
            pattern = random.choice([0,1,2])
            applies = random.choice(range(1,numPlayers+1))
            cellsX = range(10)
            cellsZ = range(5)
            
            random.shuffle(cellsX)
            random.shuffle(cellsZ)
            
            x = zip(cellsX[:numPlayers],cellsZ[:numPlayers])
            
            y = [pattern] * applies + [0] * (5-applies)
            random.shuffle(y)
            
            self.ringsPos.append(x)
            self.ringsTracks.append(y)
            
        self.ringData = make_buffer((self.rings,self.ringsPos,self.ringsTracks))
        
    def __update(self, ind, code):
        self.hitLevel[ind][self.round] = code
        self.__r += 1
        if self.__r == len(self.toons):
            self.__nextRound()
            
    def __nextRound(self):
        self.__r = 0
        self.round += 1
        
    def hit(self):
        ind = self.toons.index(self.cr.getAvatarIdFromSender())
        self.__update(ind, ok)
        
    def miss(self):
        ind = self.toons.index(self.cr.getAvatarIdFromSender())
        self.__update(ind, missed)
        
    def getHitLevel(self):
        return make_buffer(self.hitLevel)
        
    def getRingData(self):
        return self.ringData
        
        