from direct.actor.Actor import *
from pandac.PandaModules import *
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from direct.showbase.InputStateGlobal import inputState
from direct.showbase.DirectObject import DirectObject

import random, sys, os
from math import *

from tth.gui.hud import *

from etc import Teleporter

class Tunnel:
    def __init__(self, tunnelModel, tunnelMask, area, dest): 
        #try to find the trigger
        self.cNp = tunnelModel.find('**/*trigger')
        if self.cNp.isEmpty():
            self.cNp = tunnelModel.find('**/*sphere')
            if self.cNp.isEmpty():
                raise ToontownHouseError('Tunnel 0x001: can\'t handle this tunnel!')
            
        self.cnode = self.cNp.node()
        self.cnode.setCollideMask(tunnelMask)
        
        if not hasattr(area,"collDict"): area.collDict={}
        area.collDict[self.cnode] = self.goInto
        
        self.area = area
        self.dest = dest
        self.model = tunnelModel
        
        self.inUse = 0
        
    def goInto(self,entry):
        if self.inUse:
            return
            
        print ':Tunnel: Going into',self
        
        self.inUse = 1
        self.cNp.removeNode()
        
        av = self.area.avatar
        
        self.area.disableControls()
        self.area.hideHud()

        av = self.area.avatar

        self.area.toon.b_setState('Walk','run')
        
        sc = av.getScale(render)
        av.reparentTo(self.model.find('**/tun*gin'))
        av.setPos(0,0,0)
        av.setH(180)
        av.setScale(render,sc)
        
        base.cam.setPos(0,0,0)
        base.cam.setHpr(0,0,0)
        
        sc = base.cam.getScale(render)
        
        base.cam.reparentTo(self.model.find('**/tun*gin'))
        base.cam.setPos(self.area.CAM_TUNNEL_DELTA)
        base.cam.lookAt(self.model.find('**/tun*gin'))
        base.cam.setP(0)
        base.cam.setScale(render,sc)
                
        p = av.getPos() - (0,20,0)
        p2 = av.getPos()
                
        Sequence(
                 av.posInterval(1.5,p,startPos=p2),
                 av.hprInterval(.5,(90,0,0),startHpr=(180,0,0)),
                 av.posInterval(1,p+(-15,0,0),startPos=p),
                 Func(Teleporter(*self.dest,tunnel=self).go)
                ).start()

    def __repr__(self):
        return 'Tunnel from {0} to {1}'.format(self.area.name,self.dest[1])

def parentLoop(np,last,_name='render'):
            last = np
            np = np.getParent()
            if np.isEmpty(): return last.getName()
            if np.getName() == _name:
                return last.getName()
            return parentLoop(np,last)
        
def findNodeAt(np,needle,exact=False,_name='render'):
            if np.isEmpty(): return False
            if exact:
                if np.getName() == needle: return True
            else:
                if needle in np.getName(): return True 
            if np.getName() == _name: return False
            return findNodeAt(np.getParent(),needle,exact)
           
class PlaceBase(DirectObject):
    def __init__(self,environ=None):    
        gamebase.curArea = self
        
        base.camera.setPos(0,0,0)
        base.camera.setHpr(0,0,0)
        self.avatar = gamebase.toonAvatar[0].toon
        self.toon = gamebase.toonAvatar[0]
        self.toon.b_setState('Neutral')

        self.cam1Pos,self.cam1Hpr = (0,2,4.7),(0,0,0)
        self.cam2Pos,self.cam2Hpr = (2,21,4.7),(175,0,0)
        self.cam3Pos,self.cam3Hpr = (0,-30,4.7),(0,0,0)
        
        self.avatar.setPos(0,0,0)
        self.avatar.setHpr(0,0,0)
        
        _z = self.zoneId
        if self.zoneId == 1:
            _z = __import__('random').randint(20000,100000) #default is (20000,100000)
        
        _z = base.distMgr.get(_z)
        base.cr.setObjectZone(self.toon,_z)
        
        self.avatar.show()
        
        print 'Setting up',self.name
        
        self.np = NodePath(self.name)
        self.np.reparentTo(render)
        self.avatar.reparentTo(self.np)
        
        if hasattr(self,"av_startpos"):
            rp = random.choice(self.av_startpos)
            print rp
            self.avatar.setPos(rp[0])
            self.avatar.setHpr(rp[1])
        
        if environ: self.environ = loader.loadModel(environ)
        
        self.keyMap = {"left":0, "right":0, "forward":0, "cam-left":0, "cam-right":0, "backward":0,"control":0,"coll":0}
        self.allKeys = {}
        base.win.setClearColor(Vec4(0,0,0,1))
        
        if self.music:
            self.theme = loader.loadMusic(self.music)
            self.theme.setLoop(1)
            self.theme.play()
        
        self.frame = DirectFrame(frameColor=(0,0,0,0),parent=base.a2dBackground)
                
        self.floater = NodePath(PandaNode("floater"))
        self.enableControls()

        self.task = taskMgr.add(self.area_task,self.name)

        self.movingWalk,self.movingJumping = False,False
        self.canMove = True
        
        self.collHand = CollisionHandlerQueue()
        self.pusher = CollisionHandlerPusher()
        
        self.cNode = CollisionNode('avatarCNode')
        self.cNode.setIntoCollideMask(BitMask32(8))
        self.cNode.setFromCollideMask(BitMask32(8))
        
        self.ray = CollisionSphere(0,0,0,1) #CollisionRay(0,0,-1,0,0,-1)
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
        
        #self.pusher.addCollider(self.camNp, base.cam)
        
        base.cTrav.setRespectPrevTransform(True)
        
        self.camTarget = self.avatar
        self.last = 0
        self.handleAnim = True
        
        base.camera.reparentTo(self.avatar)
        _Z = 4.7
        base.camera.setPos(0, -20, _Z) 

        self.lastBroadcastTransform = None
        times_per_second = 8
        taskMgr.doMethodLater(1./times_per_second, self.updateAvatar, 'updateAvatar')
        #self.toon.startPosHprBroadcast()

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
        self.accept("tab",self.changeCam)
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
                    else: self.toon.b_setState('Walk',(('run','walk'),('walk','walk'))[it][self.keyMap['backward']])
                    
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
                    
                    if iw: self.toon.b_setState('Walk',(('run','walk'),('walk','walk'))[it][self.keyMap['backward']])
                    else: self.toon.b_setState('Neutral')
        
        base.cTrav.traverse(render) #self.np <--- NEVER!!!!!!!!!
        #this line was so shitty so shitty
        #that i wasted 10 hours (in 2 days)
        #trying to find out an error
        #caused by it

        #self.keyMap["coll"] = 1
        n = self.collHand.getNumEntries()
        #print n
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
        if not self.np or not base.cr.isConnected():
            print 'Avatar pos updater: unable to broadcast pos (no connection or zone destroyed!)'
            return task.done
        currentTransform = self.avatar.getTransform(render)
        #if self.lastBroadcastTransform == currentTransform: return task.again
        self.lastBroadcastTransform = currentTransform
        x, y, z = currentTransform.getPos()
        h, p, r = currentTransform.getHpr()
        self.toon.sendUpdate("setSmPosHpr",[x, y, z, h, p, r, 0])

        return task.again

    def changeCam(self):
        cam1Pos = self.cam1Pos
        cam1Hpr =  self.cam1Hpr
        cam2Pos = self.cam2Pos
        cam2Hpr =  self.cam2Hpr
        cam3Pos = self.cam3Pos
        cam3Hpr = self.cam3Hpr

        self.firstMovement = LerpPosHprInterval(base.cam,.5,cam1Pos,cam1Hpr)
        self.secondMovement = LerpPosHprInterval(base.cam,.5,cam2Pos,cam2Hpr)
        self.thirdMovement = LerpPosHprInterval(base.cam,.5,cam3Pos,cam3Hpr)
        self.backToNormal = LerpPosHprInterval(base.cam,.5,(0,-20,4.7),(0,0,0))
        
        try:
          if self.nowCam == "normal": 
            self.firstMovement.start()
            self.nowCam = "1"
          elif self.nowCam == "1": 
            self.secondMovement.start()
            self.nowCam = "2"
          elif self.nowCam == "2": 
            self.thirdMovement.start()
            self.nowCam = "3"
          elif self.nowCam == "3": 
            self.backToNormal.start()
            self.nowCam = "normal"
          else: print("Camera numeration invalid!")

        except AttributeError:
          self.firstMovement.start()
          self.nowCam = "1"
           
class Area(PlaceBase):
    tunOutDelay = 5
    CAM_TUNNEL_DELTA = (0,40,10)
    isInterior = False
    def __init__(self,environ=None):
        self.gamebase=gamebase
        
        if not getattr(self,"DONT_STORE",False):
            gamebase.toonAvatarStream.write("lastArea",str(self.__class__).rsplit('.',1)[-1])
            gamebase.toonAvatarStream.write("lastAreaName",self.name)
            gamebase.toonAvatarStream.write("lastZoneId",self.zoneId)
        
        PlaceBase.__init__(self,environ)
        
        self.hud = setupHud(self.frame)
        self.hudOk = 1

        self.bigtext = OnscreenText(text=L10N(self.name),scale=.15,pos=(0,-.4),wordwrap=2.6/.2,fg=(1,.5,.08,1),shadow=(.05,.05,.05,0),font=loader.loadFont('phase_3/models/fonts/MinnieFont.bam'))
        
        taskMgr.doMethodLater(7, self._destroyText, 'DestroyText')
    
    def _destroyText(self,task):
            self.bigtext.destroy()
            return task.done
                            
    def destroy(self):
        self.cNodepath.removeNode()
        self.destroyHud()
        aspect2d.show()
        
    def destroyHud(self):
        if not self.hudOk:
            return
        self.hudOk = 0
        for x in self.hud: x.removeNode()
        
    def _tunnelMovie(self,tunnels,fromTunnel):
        print 'TUNNEL MOVIE: COME FROM',fromTunnel
        
        fromNp = None
        finalPos = None
        endAvSc = None
        
        seq = Sequence()
        setSeq = Parallel()
        
        #find the tunnel
        for np,name,target in tunnels:
            if target.name == fromTunnel:
                #found it!
                if not fromNp:
                    if 1:
                        fromNp = np
                        #np.ls()
                
                        self.toon.b_setState('Walk','run') #('walk','run') #('run')    ##Fixed it
                    
                        self.toon.physControls.setCollisionsActive(False)
                        self.disableControls()
                        
                        avSc = self.avatar.getScale(self.np)
                        self.avatar.setPos(0,0,0)              
                        self.avatar.setH(0)              
                        self.avatar.reparentTo(np.find('**/tun*gin'))
                        self.avatar.setPos((-15,-22.5,0))
                        self.avatar.setH(-90)
                        
                        base.cam.reparentTo(self.avatar)
                        base.cam.setPos(0,0,0)
                        base.cam.setHpr(0,0,0)

                        base.cam.reparentTo(np.find('**/tun*gin'))
                        base.cam.setPos(self.CAM_TUNNEL_DELTA)
                        base.cam.lookAt(np.find('**/*gin'))
                        base.cam.setP(0)
                        base.cam.setScale(1)

                        p = self.avatar.getPos() + (13.5,0,0)
                        p2 = self.avatar.getPos()
                        
                        dummyNp = np.find('**/tun*gin').attachNewNode('dummy')
                        dummyNp.setPos(p+(0,30,0))
                        finalPos = dummyNp.getPos(self.np)
                        dummyNp.removeNode()

                        _seq = Sequence(
                                    Wait(self.tunOutDelay),
                                    self.avatar.posInterval(2.5,p,startPos=p2),
                                    self.avatar.hprInterval(.5,(0,0,0),startHpr=(-90,0,0)),
                                    self.avatar.posInterval(2,p+(0,40,0),startPos=p),
                                    )
                        seq.append(_seq)  
                    
                        self.hideHud()

                else: print ':SetupTunnel: Detected more than one from tunnels, perhaps cog hq? Ignoring...'
                
            setSeq.append(Func(self._setupSingleTunnel,np,target)) #set it up
                
        seq.append(setSeq)
        seq.append(Func(self._restoreTunnelMovie,finalPos,fromNp.find('**/tun*gin').getH(self.np) if fromNp else 0,endAvSc))
        seq.start()
        
    def _doorMovie(self,doors,fromDoor):
        print 'DOOR MOVIE: COME FROM',fromDoor
        
        fromNp = None
        finalPos = None
        endAvSc = None
        
        seq = Sequence()
        setSeq = Parallel()
        
        #find the tunnel
        for np,name,target in doors:
            if target.name == fromDoor:
                #found it!
                if not fromNp:
                    if 1:
                        fromNp = np
                        #np.ls()
                
                        self.toon.b_setState('Walk','run')
                    
                        self.toon.physControls.setCollisionsActive(False)
                        self.disableControls()
                        
                        avSc = self.avatar.getScale(self.np)
                        self.avatar.setPos(0,0,0)              
                        self.avatar.setH(0)              
                        self.avatar.reparentTo(np.find('**/*gin'))
                        self.avatar.setPos((-15,-22.5,0))
                        self.avatar.setH(-90)
                        
                        base.cam.reparentTo(self.avatar)
                        base.cam.setPos(0,0,0)
                        base.cam.setHpr(0,0,0)
                        base.cam.reparentTo(np.find('**/*gin'))
                        base.cam.setPos(self.CAM_TUNNEL_DELTA)
                        base.cam.lookAt(np.find('**/*gin'))
                        base.cam.setP(0)
                        base.cam.setScale(1)

                        p = self.avatar.getPos() + (0,5,0)
                        p2 = self.avatar.getPos()
                        
                        dummyNp = np.find('**/*gin').attachNewNode('dummy')
                        dummyNp.setPos(p+(0,5,0))
                        finalPos = dummyNp.getPos(self.np)
                        dummyNp.removeNode()

                        _seq = Sequence(
                                    Wait(self.tunOutDelay),
                                    self.avatar.posInterval(2.5,p,startPos=p2),
                                    )
                        seq.append(_seq)  
                    
                        self.hideHud()

                else: print ':SetupDoors: Detected more than one from doors, perhaps cog hq? Ignoring...'
                
            setSeq.append(Func(self._setupSingleDoor,np,target)) #set it up
                
        seq.append(setSeq)
        if bool(fromNp): seq.append(Func(self._restoreTunnelMovie,finalPos,fromNp.find('**/*gin').getH(self.np) if fromNp else 0,endAvSc))
        seq.start()
        
        return bool(fromNp)
        
    def _restoreTunnelMovie(self,endPos = None, endH=0, endAvSc=None):
        #self.toon.b_setState('Walk')        
        self.avatar.physControls.setCollisionsActive(True)
        self.avatar.physControls.placeOnFloor()
        self.enableControls()
                     
        self.toon.b_setState('Neutral')

        self.avatar.wrtReparentTo(self.np)
        
        if endPos is not None:
            if endPos != self.avatar.getPos():
                self.avatar.setPos(endPos)
                print "Tunnel 0x002 (WARNING): Restoring FromAnimation: bad pos %s, should be %s, fixing..." % (self.avatar.getPos(),endPos)
                #raise ToontownHouseError("Tunnel 0x002: Restoring FromAnimation: bad pos %s(), good=%s" % (self.avatar.getPos(),endPos))
        
        if endAvSc is not None and endAvSc != self.avatar.getScale(render):
            self.avatar.setScale(render,endAvSc)
            print "Tunnel 0x003 (WARNING): Restoring FromAnimation: bad avSc %s, should be %s, fixing..." % (self.avatar.getScale(render),endAvSc)
        
        self.avatar.setH(endH)
        self.showHud()
        
        base.cam.setPos(0, 0, 0)
        base.cam.setHpr(0, 0, 0)
        base.cam.reparentTo(self.avatar)
        base.cam.setPos(0, -20, 4.7)
        
    def hideHud(self): aspect2d.stash()
    def showHud(self): aspect2d.unstash()
    
    def obscureBookAndFL(self,flag):
        func = NodePath.stash
        if not flag: func = NodePath.unstash
        map(lambda x: func(self.hud[x]),(0,4))
    
    def _setupSingleTunnel(self,np,target):
        print 'SET SINGLE TUNNEL',np
        Tunnel(np,BitMask32(8),self,(target,target.name))
        
    def _setupSingleDoor(self,np,target):
        from tth.building.DistributedDoor import LocalDoor
        print 'SET SINGLE DOOR',np
        base.lolDoor = LocalDoor(np,BitMask32(8),self,(target,target.name))
        
    def takeControlOf(self,c): #doesnt work
            from direct.controls.GravityWalker import GravityWalker
            wc = GravityWalker(legacyLifter=True)
            wc.setWallBitMask(BitMask32(1))
            wc.setFloorBitMask(BitMask32(2))
            wc.setWalkSpeed(20,10,20,60)
            wc.initializeCollisions(base.cTrav, c, floorOffset=0.025, reach=4.0)
            wc.enableAvatarControls()
            c.physControls = wc
            c.physControls.placeOnFloor()
            
            base.cam.reparentTo(c)
            base.cam.setPos(0,30,5)
            base.cam.setHpr(0,0,0)
            self.avatar.physControls.disableAvatarControls()
