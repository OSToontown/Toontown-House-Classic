from panda3d.core import *
from direct.fsm.FSM import FSM

from direct.showbase.DirectObject import DirectObject
from tth.ohs.DistributedTrolley import *

class MinigameZone(DirectObject):
    localAvMask = BitMask32(8)
    def __init__(self, tp, zoneId, wantAvatar = True, wantCamera = False, wantControls = False, hud2keep = [0,1,1,1,0], environ = None):
        gamebase.curArea = self
        
        base.camera.setPos(0,0,0)
        base.camera.setHpr(0,0,0)
        self.avatar = gamebase.toonAvatar[0].toon
        self.toon = gamebase.toonAvatar[0]
        self.toon.b_setState('Neutral')
        
        self.avatar.setPos(0,0,0)
        self.avatar.setHpr(0,0,0)
        
        _z = zoneId 
        base.cr.setObjectZone(self.toon,_z)
        self.zoneId = zoneId
        
        print 'Setting up MGZONE @',zoneId
        
        self.np = NodePath(self.name)
        self.np.reparentTo(render)
        self.avatar.reparentTo(self.np)
        
        if environ: self.environ = loader.loadModel(environ)
        
        self.keyMap = {"left":0, "right":0, "forward":0, "cam-left":0, "cam-right":0, "backward":0,"control":0,"coll":0}
        self.allKeys = {}
        base.win.setClearColor(Vec4(0,0,0,1))
        
        if self.music:
            self.theme = loader.loadMusic(self.music)
            self.theme.setLoop(1)
            self.theme.play()
        
        self.frame = DirectFrame(frameColor=(0,0,0,0),parent=base.a2dBackground)
        self.hud = setupHud(self.frame)
        
        for i,x in enumerate(hud2keep):
            if len(self.hud) < i: break
            if not x: self.hud[i].removeNode()
        
        self.floater = NodePath(PandaNode("floater"))
        
        if wantControls: self.enableControls()

        self.task = taskMgr.add(self.area_task,'taskForMGZone-%d' % zoneId)

        #self.movingJumping,self.movingForward,self.movingNeutral,self.movingRotation,self.movingBackward = [False for i in xrange(5)]
        self.movingWalk,self.movingJumping = False,False
        self.canMove = wantControls
        
        self.collHand = CollisionHandlerQueue()
        self.pusher = CollisionHandlerPusher()
        self.cNode = CollisionNode('avatarCNode')
        
        self.cNode.setIntoCollideMask(self.localAvMask)
        self.cNode.setFromCollideMask(self.localAvMask)
        
        self.ray = CollisionRay(0,0,-1,0,0,-1)
        self.cNode.addSolid(self.ray)
        self.cNodepath = self.avatar.attachNewNode(self.cNode)
        if base.isInjectorOpen:
            self.cNodepath.show()
            base.cTrav.showCollisions(render)
        self.camCNode = CollisionNode('camCNode')
        self.camCNode.addSolid(CollisionRay(0,0,-1,0,0,-1))
        self.camCNode.setFromCollideMask(BitMask32(1))
        self.camCNode.setIntoCollideMask(BitMask32.allOff())
        self.camNp = base.cam.attachNewNode(self.camCNode)
        
        base.cTrav.addCollider(self.cNodepath, self.collHand)
        base.cTrav.addCollider(self.camNp, self.pusher)
        base.cTrav.setRespectPrevTransform(True)
        
        self.handleAnim = wantControls
        
        if wantCamera:
            base.cam.reparentTo(self.avatar)
            base.cam.setPos(0,-20,4.7)
            base.cam.setH(0)
            
        else:
            base.camera.reparentTo(render)
            base.cam.iPosHpr()

        self.lastBroadcastTransform = None
        times_per_second = 8
        taskMgr.doMethodLater(1./times_per_second, self.updateAvatar, 'updateAvatar')
        
        if wantAvatar: self.avatar.show()
        else: self.avatar.hide()
        
        self.distMg = None
        self.__tp = tp
        
    def setDistMg(self, mg):
        self.__tp.done()
        del self.__tp
        self.distMg = mg
            
    def disableControls(self):
        self.handleAnim = False
        for input,(key,keyMapName) in self.allKeys.items():
            inputState.set(input, False)
            self.keyMap[keyMapName] = 0
        self.ignoreAll()
            
    def enableControls(self):
        self.setWatchKey('arrow_up', 'forward', 'forward')
        self.setWatchKey('control-arrow_up', 'forward', 'forward')
        self.setWatchKey('alt-arrow_up', 'forward', 'forward')
        self.setWatchKey('shift-arrow_up', 'forward', 'forward')
        self.setWatchKey('arrow_down', 'reverse', 'backward')
        self.setWatchKey('control-arrow_down', 'reverse', 'backward')
        self.setWatchKey('alt-arrow_down', 'reverse', 'backward')
        self.setWatchKey('shift-arrow_down', 'reverse', 'backward')
        self.setWatchKey('arrow_left', 'turnLeft', 'left')
        self.setWatchKey('control-arrow_left', 'turnLeft', 'left')
        self.setWatchKey('alt-arrow_left', 'turnLeft', 'left')
        self.setWatchKey('shift-arrow_left', 'turnLeft', 'left')
        self.setWatchKey('arrow_right', 'turnRight', 'right')
        self.setWatchKey('control-arrow_right', 'turnRight', 'right')
        self.setWatchKey('alt-arrow_right', 'turnRight', 'right')
        self.setWatchKey('shift-arrow_right', 'turnRight', 'right')
        self.setWatchKey('control', 'jump', 'control')
        self.handleAnim = True
            
    def setWatchKey(self, key, input, keyMapName):
        def watchKey(active=True):
            if active:
                inputState.set(input, True)
                self.keyMap[keyMapName] = 1
            else:
                inputState.set(input, False)
                self.keyMap[keyMapName] = 0
                
        self.accept(key, watchKey, [True])
        self.accept(key+'-up', watchKey, [False])
        self.allKeys[input] = (key,keyMapName)
    
    def area_task(self, task):
        startpos = self.avatar.getPos()
        if self.handleAnim:
            ij,iw = self.keyMap['control'],(self.keyMap['forward'] or self.keyMap['backward'] or self.keyMap['left'] or self.keyMap['right'])
            it = self.keyMap['left'] or self.keyMap['right']
            
            jp = '-zhang'
            
            if iw:
                if not self.movingWalk:
                    self.movingWalk = True
                    
                    if ij: self.toon.b_setState('Jump')
                    else: self.toon.b_setState('Walk',('run','walk')[it])
                    
            else:
                if self.movingWalk:
                    self.movingWalk = False
                    
                    if ij: self.toon.b_setState('Jump')
                    else: self.toon.b_setState('Neutral')
                    
            if ij:
                if not self.movingJumping:
                    self.movingJumping = True
                    
                    if iw: self.toon.b_setState('Jump')
                    else: self.toon.b_setState('Jump')
                    
            else:
                if self.movingJumping:
                    self.movingJumping = False
                    
                    if iw: self.toon.b_setState('Walk',('run','walk')[it])
                    else: self.toon.b_setState('Neutral')
        
        base.cTrav.traverse(self.np)

        n = self.collHand.getNumEntries()
        for i in xrange(n):
            entry = self.collHand.getEntry(i)
                
            if hasattr(self,"collDict"):
                for obj in self.collDict:
                    if self.keyMap["coll"]:print 'COLLDICT!',obj,entry.getIntoNode()==obj
                    if entry.getIntoNode() == obj: self.collDict[obj](entry)
                
            if self.keyMap["coll"]:print entry
            
        if hasattr(self,"taskMethod"): self.taskMethod(task)
        
        return task.cont
       
    def updateAvatar(self,task):
        if not self.np: return task.done
        currentTransform = self.avatar.getTransform(self.np)
        #if self.lastBroadcastTransform == currentTransform: return task.again
        self.lastBroadcastTransform = currentTransform
        x, y, z = currentTransform.getPos()
        h, p, r = currentTransform.getHpr()
        self.toon.sendUpdate("setSmPosHpr",[x, y, z, h, p, r, 0])

        return task.again
        
    def __tth_area__(self):
        return {
                'name':"MGZone",
                'models':self.np,
                'bgm':self.theme,
                'gui':self.frame,
                'speeches':[]
                }
                
    def destroy(self):
        self.cNodepath.removeNode()
        #remove hud
        for x in self.hud: x.removeNode()