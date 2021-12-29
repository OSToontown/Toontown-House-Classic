# -*- coding: latin-1 -*-
"""
File: etc.py
    Module: cogtown.areas
Author: Nacib
Date: AUGUST/14/2013
Description: some util stuff
FROM COGTOWN
"""

from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.task.Task import *
from direct.interval.IntervalGlobal import *
from random import choice, random, randint
from tth.managers import Timer

import sys

class OldTeleportCircle(NodePath):
    openScale = (32,1,32)
    closedScale = (2,1,2)
    time = .75
    
    method = "iris" #iris or tpCircle

    def __init__(self):
        NodePath.__init__(self,"TPCircle")
        self.hide()
        
        if self.method == "tpCircle":
            self.img = OnscreenImage(image="phase_0/tpCircle.png",parent = self)
            self.img.reparentTo(self)
            
        elif self.method == "iris": #not working
            self.img = loader.loadModel("phase_3/models/misc/iris.bam")
            
        else:
            raise AtrributeError("method must be iris or tpCircle")
        
        self.img.setTransparency(TransparencyAttrib.MAlpha)
        self.reparentTo(render2d)
        self.setScale(self.openScale)
        self.show()
     
    @classmethod     
    def getOpenSeq(cls, autoDestroy = 1):
        t = cls()
        s = Sequence(t.scaleInterval(cls.time,cls.openScale,cls.closedScale))
        if autoDestroy:
            s.append(Func(t.removeNode))
            
        return t,s
        
    @classmethod     
    def getCloseSeq(cls, autoDestroy = 1):
        t = cls()
        s = Sequence(t.scaleInterval(cls.time,cls.closedScale,cls.openScale))
        if autoDestroy:
            s.append(Func(t.removeNode))
            
        return t,s
    
    @classmethod
    def performOpen(cls, autoDestroy = 1):
        t,s = cls.getOpenSeq(autoDestroy)
        s.start()
        return t,s
        
    @classmethod
    def performClose(cls, autoDestroy = 1):
        t,s = cls.getCloseSeq(autoDestroy)
        s.start()
        return t,s
        
class TeleportCircle:
    @classmethod     
    def getOpenSeq(cls, autoDestroy = 1):
        s = Sequence(Func(base.transitions.irisIn),Wait(.5))
        if autoDestroy: s.append(Func(base.transitions.noIris))
        return (None,s)
        
    @classmethod     
    def getCloseSeq(cls, autoDestroy = 1):
        s = Sequence(Func(base.transitions.irisOut),Wait(.525))
        if autoDestroy: s.append(Func(base.transitions.noIris))
        return (None,s)
    
    @classmethod
    def performOpen(cls, autoDestroy = 1):
        _,s = cls.getOpenSeq(autoDestroy)
        s.start()
        return None,s
        
    @classmethod
    def performClose(cls, autoDestroy = 1):
        _,s = cls.getCloseSeq(autoDestroy)
        s.start()
        return None,s

class TeleportScreen:
    def __init__(self,name,_time=3):
        if not name.startswith('AREA_'):
            if not name.startswith('MG_'):
                name = 'AREA_'+name
                
        _slot = int(gamebase.toonId)
        self.loadingImage = OnscreenImage(image="phase_0/etc/background%s.png" % _slot,parent=render2d)
        _text = u"{0} {1}...".format(L10N('TPS_GOINGTO'),L10N(name))
        self.text = OnscreenText(text=_text,pos=(-1.2,-.72),scale=.07,fg=(0,0,139,139),font=BTFont,align=TextNode.ALeft)
        self.ttlogo = OnscreenImage(image="phase_0/toontown-logo-new.png",scale=.3,pos=(0,0,.70))
        self.ttlogo.setSx(.8)
        self.ttlogo.reparentTo(self.loadingImage)
        self.ttlogo.setTransparency(TransparencyAttrib.MAlpha)
        self.tipFrame = loader.loadModel('phase_3/models/gui/toon_council').find('**/scroll')
        self.tipFrame.reparentTo(self.ttlogo)
        self.tipFrame.setZ(-2.175)
        self.tipFrame.setSz(1.3)
        self.tipFrame.setSx(.615)
        self.ttlogo.setTransparency(TransparencyAttrib.MAlpha)
        
        self.text.reparentTo(render2d)
        self.text.setX(-.9)

        selected=L10N('TPS_TIPTITLE')+'\n'+L10N.tip()
        
        self.tipText = TextNode('tiptext')
        self.tipText.setWordwrap(20)
        self.tipText.setWtext(selected)
        self.tipText.setFont(loader.loadFont("phase_3/models/fonts/ImpressBT.ttf"))
        self.tipText.setTextColor(0,0,0,1)
        self.tipTextNp = self.tipFrame.attachNewNode(self.tipText)
        self.tipTextNp.setScale(.12)
        self.tipTextNp.setX(-1.2)
        self.tipTextNp.setZ(.15)
        
        self.falseBar = DirectWaitBar(text = "", value = 0, pos = (0,0,-.8), parent = render2d)
        self.falseBar.setSz(.5)
        self.falseBar.setSx(.9)
        
        Timer(_time,lambda:0,self.step)
        
        self.bar_anim_brpoints = [0]
        for i in xrange(8): self.bar_anim_brpoints.append(randint(1,90))
        self.bar_anim_brpoints.append(83)
        self.bar_anim_brpoints.append(100)
        self.bar_anim_brpoints.sort(key=int)
        
    def step(self,time):
        self.falseBar['value'] = [i for i in self.bar_anim_brpoints if i<=(3-time)/3*100][-1]

    def dismiss(self):
        #print 'Removing tp screen...'
        self.loadingImage.destroy()
        self.text.destroy()
        taskMgr.remove('timerTask')
        self.falseBar.destroy()

class Teleporter:
    def __init__(self, target, name="", extraArgs=[], tunnel = None, door = None):
        self.target = target
        self.name=name
        self.extraArgs=extraArgs
        self.tunnel = tunnel
        self.door = door
        self.wantScreen = True
        self.dtime = 0
        self.wantCircle = (1,1)
        
        if not hasattr(self.target,"__tth_area__"):
            raise ToontownHouseError('Teleporter 0x000: invalid target given (%s)!' % self.target) #WTF
        
    def go(self):
        if not self.wantCircle[0]:
            print 'Teleporter: no circle, going...'
            return self.__go()
        
        Sequence(TeleportCircle.getCloseSeq()[1],Func(self.__go)).start()
            
    def __go(self):
        _time = self.dtime
        #default behaviour is not having time
        #if no screen
        
        if self.wantScreen:
            self.lsc = TeleportScreen(self.name)
            _time = (1,4)[base.isInjectorOpen]
            if '-fast' in sys.argv:
                _time = .1
        
        #destroy current area
        if gamebase.curArea is not None:
            a = gamebase.curArea.__tth_area__()
            if a:
                taskMgr.remove(a['name'])
                gamebase.curArea.avatar.reparentTo(NodePath('dummy'))
                base.cam.wrtReparentTo(render)#gamebase.curArea.avatar)

                if hasattr(gamebase.curArea,"seq"): gamebase.curArea.seq.finish()
                
                a["models"].removeNode()
                a["gui"].destroy()
                a["bgm"].stop()
               
                for s in a["speeches"]:
                    try:
                        s.frame.destroy()
                    except:
                        pass
                print 'Removed',a["name"]
                gamebase.curArea.destroy()
                gamebase.curArea.ignoreAll()

        if len(self.extraArgs): taskMgr.doMethodLater(_time,self._goTaskArgs, 'tpTask', extraArgs = [self.extraArgs])
        else: taskMgr.doMethodLater(_time,self._goTask, 'tpTask')
        
    def _goTask(self,task):
        self.target(tp = self)
        return Task.done
    
    def _goTaskArgs(self,*args):
        l = args
        self.target(*l,tp = self)
        return Task.done
        
    def getTunnel(self):
        try: return self.tunnel.area.name
        except: return None
        
    def getDoor(self):
        try: return self.door.area.name
        except: return None
        
    def done(self):
        if self.wantScreen:
            self.lsc.dismiss()

        if self.wantCircle[1]:
            Sequence(Wait(.3),Func(TeleportCircle.performOpen,1)).start()
