from direct.distributed.ClockDelta import globalClockDelta
from direct.interval.IntervalGlobal import *

from panda3d.core import *

#states are:
#Off
#Wait
#Play
#Cleanup

import MGZone
class CannonGameZone(MGZone.MinigameZone):
    name = "AREA_MG_CANNON"
    music = "phase_4/audio/bgm/MG_cannon_game.mid"
    def __init__(self,tp = None):
        self.origin = tp.origin
        MGZone.MinigameZone.__init__(self, tp.zoneId, wantAvatar = True, wantCamera = True)
        tp.done()
        
    def area_task(self,task):
        if self.distMg:
            pass
            
        MGZone.MinigameZone.area_task(self,task)
        return task.cont
        
    def __tth_area__(self):
        return {
                'name':"MGZone",
                'models':self.np,
                'bgm':self.theme,
                'gui':self.frame,
                'speeches':[]
                }

import DistributedMinigame
class DistCannonGame(DistributedMinigame.DistributedMinigame):
    def loadEnviron(self):
        self.environ = loader.loadModel('phase_4/models/minigames/toon_cannon_gameground')
        self.environ.reparentTo(self.mgNp)
        
        self.tower = loader.loadModel('phase_4/models/minigames/toon_cannon_water_tower')
        self.tower.reparentTo(self.mgNp)
        self.tower.setPos(0,50,0)
        
        numCannons = len(self.toons)
        localCannId = self.toons.index(self.cr.doIdBase)
        
        av = gamebase.curArea.avatar
        gamebase.curArea.distMg = self
        
        #print numCannons,localCannId 
        cannonPos = (
                     (0,),
                     (-5,5),
                     (-10,0,10),
                     (-15,-5,5,15),
                     )[numCannons - 1]
        
        self.cannons = []
        for i,p in enumerate(cannonPos):
            cannon = loader.loadModel('phase_4/models/minigames/toon_cannon')
            cannon.reparentTo(self.mgNp)
            cannon.setPos(p,-200,0)
            if i == localCannId:
                av.reparentTo(cannon)
                base.cam.wrtReparentTo(render)   
                av.setP(-90)
                
            self.cannons.append(cannon)

    
import DistributedMinigameAI
class DistCannonGameAI(DistributedMinigameAI.DistributedMinigameAI):
    pass