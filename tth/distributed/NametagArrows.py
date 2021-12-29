from panda3d.core import *
from direct.gui.DirectGui import *
from direct.showbase.DirectObject import DirectObject

import math

class Tag:
    maxRefDist = 500
    transformData = {
                     0:((0,0,0),(.15,)),
                     1:((0,0,0),(.15,)),
                     2:((0,0,0),(.15,)),
                     3:((0,0,0),(.15,)),
                    }
                     
    def __init__(self, tagModel, cell, ref1, ref2):
        self.tagModel = tagModel
        self.cell = cell
        
        self.cell.data = self
        self.tagModel.iHpr(render)
        self.tagModel.reparentTo(self.cell)
        
        t = self.tagModel
        t.setZ(-.05)
        t.setX(0)
        t.setScale(*self.transformData[cell.parId][1])
        #t.node().setWordwrap(10)
        t.setHpr(*self.transformData[cell.parId][0])
        
        self.taskName = 'updateTag_'+str(id(t))
        taskMgr.add(self.__task,self.taskName)
        
        self.arrow = loader.loadModel('phase_3/models/props/arrow')
        self.arrow.setColorScale(t.getColor())
        self.arrow.reparentTo(t)
        self.arrow.setZ(.75)
        self.arrow.setScale(.75)
        
        self.dummy = render.attachNewNode('dummy')
        
        self.refs = (ref1,ref2)
        
    def getStatus(self):
        if not self.distObj in base.cr.doId2do.values():
            return -1
            
        dist = self.refs[0].getPos(self.refs[1])
        if dist < self.maxRefDist:
            return -2 #bugged
            
        return 0
        
    def __task(self, task):
        if self.getStatus() < 0:
            return task.done
        
        '''
        #turn my arrow's 2d pos
        #into a 3d pos
        f = base.camLens.getFov()
        f2 = ((f[0]*(3.14/180))/.1,f[1]/6)
        
        x = self.arrow.getX(render2d) * f2[0]
        z = self.arrow.getZ(render2d) * f2[1]
        
        v1 = Vec3(x,0,z) + Vec3(self.refs[1].getPos(render))
        v2 = Vec3(self.refs[0].getPos(render))
        
        self.dummy.setPos(v1)
        #map(lambda x:x.setY(0), (v1,v2))
        
        x1, x2 = map(Vec3.getX, (v1,v2))
        z1, z2 = map(Vec3.getZ, (v1,v2))
        
        dx = x1-x2
        dz = z1-z2
        angle = abs(math.atan2(dx,dz) * (180/math.pi)) % 360
        
        #print v1, v2, angle#, exit()
        self.arrow.setR(angle - 0)
        '''
        
        cam = base.cam
        toon = cam

        location = self.refs[0].getPos(toon)
        rotation = toon.getQuat(cam)

        camSpacePos = rotation.xform(location)
        arrowRadians = math.atan2(camSpacePos[0], camSpacePos[1])
        arrowDegrees = arrowRadians/math.pi*180

        self.arrow.setR(arrowDegrees - 90)
        
        return task.cont
        
    def destroy(self):
        self.tagModel.removeNode()
        self.cell.data = None
        taskMgr.remove(self.taskName)

class NametagArrows(DirectObject):
    collectables = {
                    'DistributedAvatar':('toon','avatarChat-%d'),
                    #'DistributedCog':('cog','cogChat-%d'),
                    }
                    
    collectAvarage = 5
                    
    def __init__(self):
        self.collected = {}
        taskMgr.add(self.updateTask,"nametag arrows task")
        
    def updateTask(self,task):
        tc = len(self.collected)
        if tc <= self.collectAvarage:
            self.__collect()
            
        for doId,tag in self.collected.items():
            status = tag.getStatus()
            if status < 0:
                print 'NametagArrows: tag %s is bad (%d), destroying...' % (tag, status)
                tag.destroy()
                del self.collected[doId]
                
        return task.cont
        
    def __collect(self):
        for doId,obj in base.cr.doId2do.items():
            if len(self.collected) > self.collectAvarage:
                break
                
            c = self.collectables.get(obj.dclass.getName()) 
            if not c or doId in self.collected:
                continue
            
            print 'NametagArrows: potential collect: %s (doId = %d)' % (obj,doId)
                
            t1 = getattr(obj,c[0],None)
            if not t1:
                print '\tNametagArrows: failed to collect: t1'
                continue

            cell = base.marginMgr.allocate(1)
            if not cell:
                #print '\tNametagArrows: failed to collect: cell',cell
                #too noisy
                break
                
            tagCp = self.__makeTag(t1)
            
            _tag = Tag(tagCp,cell[0],t1,base.cam)
            _tag.distObj = obj
            self.collected[doId] = _tag
            
            print 'NametagArrows: collected %s (doId = %d)' % (obj,doId)
            
    def __makeTag(self,obj):
        return NodePath(obj.makeTag())