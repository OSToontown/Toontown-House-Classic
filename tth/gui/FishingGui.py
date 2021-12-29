from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from panda3d.core import *
import math, struct

from tth.fishing.FishTank import makeLocalTank as MLT

FishingAngleMax = 50.0

FishingItemFound = "item Found"
FishingExit = "Quit"
FishingCast = "Cast"
angleDiff = 0

class FishingFrame(DirectFrame):

    castButtonColors = ((1, 0, 0, 1),(0, 1, 0, 1),(1, 1, 0, 1),(0.8, 0.5, 0.5, 1))

    def __init__(self,pond,toon):
        self.moneyMgr = gamebase.toonAvatarStream.moneyMgr
        self.accept("moneyChanged",self.__updateMoney)
        self.accept("fishTankChanged",self.__updateFishTank)
        
        self.rodIndex = gamebase.toonAvatarStream.read("rod",0)
        
        self.isCasting = False
        self.power = 0.0
        self.angle = 0.0
        self.pond = pond
        self.toon = toon
        self.toonH = toon.toon.getH()
        
        self.castGui = loader.loadModel('phase_4/models/gui/fishingGui')
        self.castGui.setScale(0.67)
        self.castGui.setPos(0, 1, 0)
        
        DirectFrame.__init__(self)
        self.initialiseoptions(self.__class__)
        
        for nodeName in ('bucket', 'jar', 'display_bucket', 'display_jar'):
            self.castGui.find('**/' + nodeName).reparentTo(self.castGui)
            
        self.exitButton = DirectButton(parent=self.castGui, relief=None, text=('', FishingExit, FishingExit), text_align=TextNode.ACenter, text_scale=0.1, text_fg=Vec4(1, 1, 1, 1), text_shadow=Vec4(0, 0, 0, 1), text_pos=(0.0, -0.12), pos=(1.75, 0, -1.33), textMayChange=0, image=(self.castGui.find('**/exit_buttonUp'), self.castGui.find('**/exit_buttonDown'), self.castGui.find('**/exit_buttonRollover')), command=self.__userExit)
        
        self.arrow = self.castGui.find('**/arrow')
        self.arrowTip = self.arrow.find('**/arrowTip')
        self.arrowTail = self.arrow.find('**/arrowTail')
        self.arrow.reparentTo(self.castGui)
        self.arrow.setColorScale(0.9, 0.9, 0.1, 0.7)
        self.arrow.hide()
        
        self.castGui.find('**/exitButton').removeNode()
        
        self.castButton = DirectLabel(parent=self.castGui, relief=None, text=('',FishingCast,FishingCast),
                                       text_align=TextNode.ACenter, text_scale=(3, 3 * 0.75, 3 * 0.75),
                                       text_fg=Vec4(1, 1, 1, 1), text_shadow=Vec4(0, 0, 0, 1),
                                       text_pos=(0, -4), image=self.castGui.find('**/castButton'),
                                       pos=(0, -0.05, -0.666), scale=(0.036, 1, 0.048), state = DGG.NORMAL,
                                       image_color = self.castButtonColors[0])
                                       
        self.castButton.bind(DGG.B1PRESS,self.__castStart)
        self.castButton.bind(DGG.WITHIN,self.__castMOver,[1])
        self.castButton.bind(DGG.WITHOUT,self.__castMOver,[0])
        
        self.castGui.find('**/castButton').removeNode()
        self.arrow = self.castGui.find('**/arrow')
        self.arrowTip = self.arrow.find('**/arrowTip')
        self.arrowTail = self.arrow.find('**/arrowTail')
        self.arrow.reparentTo(self.castGui)
        self.arrow.setColorScale(0.9, 0.9, 0.1, 0.7)
        self.arrow.hide()
        
        self.jar = DirectLabel(parent=self.castGui, relief=None, text=str(self.getAvMoney()), text_scale=0.16, text_fg=(0.95, 0.95, 0, 1), pos=(-1.12, 0, -1.3), text_font=loader.loadFont("phase_3/models/fonts/MickeyFont"))
        self.bucket = DirectLabel(parent=self.castGui, relief=None, text='', text_scale=0.09, text_fg=(0.95, 0.95, 0, 1), text_shadow=(0, 0, 0, 1), pos=(1.14, 0, -1.33))

        self.itemGui = NodePath('itemGui')
        
        self.itemFrame = DirectFrame(parent=self.itemGui, relief=None, geom=DGG.getDefaultDialogGeom(), geom_scale=(1, 1, 0.6), text=FishingItemFound, text_pos=(0, 0.2), text_scale=0.08, pos=(0, 0, 0.587))
        self.itemLabel = DirectLabel(parent=self.itemFrame, text='', text_scale=0.06, pos=(0, 0, -0.25))
        
        buttons = loader.loadModel('phase_3/models/gui/dialog_box_buttons_gui')
        self.itemGuiCloseButton = DirectButton(parent=self.itemFrame, pos=(0.44, 0, -0.24), relief=None, image=(buttons.find('**/CloseBtn_UP'), buttons.find('**/CloseBtn_DN'), buttons.find('**/CloseBtn_Rllvr')), image_scale=(0.7, 1, 0.7), command=self.__itemGuiClose)
        buttons.removeNode()
        
        jarGui = loader.loadModel('phase_3.5/models/gui/jar_gui')
        bootGui = loader.loadModel('phase_4/models/gui/fishing_boot')
        packageGui = loader.loadModel('phase_3.5/models/gui/stickerbook_gui').find('**/package')
        
        self.itemJellybean = DirectFrame(parent=self.itemFrame, relief=None, image=jarGui, scale=0.5)
        self.itemBoot = DirectFrame(parent=self.itemFrame, relief=None, image=bootGui, scale=0.2)
        self.itemPackage = DirectFrame(parent=self.itemFrame, relief=None, image=packageGui, scale=0.25)
        
        self.itemJellybean.hide()
        self.itemBoot.hide()
        self.itemPackage.hide()
        
        self.castGui.reparentTo(self)
        
        self.boards = self.castGui.find('**/boards')
        self.boards.wrtReparentTo(render2d)
        
        self.__updateFishTank(len(MLT()))
        self.resetFrameSize()
        
    def getAvMoney(self):
        return self.moneyMgr.getMoney(0)[0]
        
    def __userExit(self):
        messenger.send('quitFishing')
        
    def __itemGuiClose(self):
        pass
        
    def __castStart(self,event):
        #print 'start cast'
        if not self.pond.canCast():
            return
            
        if self.getAvMoney() <= 0:
            return self.pond.castError(0)
            
        self.isCasting = True
        
        #install color hook
        self.castButton['image_color'] = self.castButtonColors[2]
        
        #get ready to when user releases it
        self.acceptOnce("mouse1-up",self.__releaseCast)
        messenger.send('fishPanelDone')
        
        #make cast track
        
        av = self.toon.toon
        self.castTrack = Sequence(
                                  ActorInterval(av, 'castlong', playRate=4),
                                  ActorInterval(av, 'cast', startFrame=20),
                                  Func(av.loop, 'fish-neutral')
                                 )
        
        #show arrow and spawn task
        self.arrow.show()
        self.arrow.setColorScale(1, 1, 0, 0.7)
        
        self.getMouse()
        self.initMouseX = self.mouseX
        self.initMouseY = self.mouseY
        
        self.castTask = taskMgr.add(self.__castTask,"fishing_castTask")
        self.toon.b_setState("FishAim",str(self.rodIndex))
        
    def __releaseCast(self):
        #print 'stop casting'
        self.isCasting = False
        
        #remove color hook
        self.castButton['image_color'] = self.castButtonColors[0]
        taskMgr.remove(self.castTask)
        
        self.arrow.hide()
        
        self.toon.b_setState("FishCast",struct.pack("H3d",self.rodIndex,self.angle,self.power*1.1,self.pond.waterLevel))
        messenger.send('loseMoney',[self.rodIndex+1])
        
    def __castTask(self,task):
        self.getMouse()
        deltaX = self.mouseX - self.initMouseX
        deltaY = self.mouseY - self.initMouseY
        if deltaY >= 0:
            if self.power == 0:
                self.arrowTail.setScale(0.075, 0.075, 0)
                self.arrow.setR(0)
            self.castTrack.pause()
            return task.cont
        dist = math.sqrt(deltaX * deltaX + deltaY * deltaY)
        delta = dist / 0.5
        self.power = max(min(abs(delta), 1.0), 0.0)
        self.castTrack.setT(0.2 + self.power * 0.7)
        angle = rad2Deg(math.atan(deltaX / deltaY))
        if self.power < 0.25:
            angle = angle * math.pow(self.power * 4, 3)
        if delta < 0:
            angle += 180
        minAngle = -FishingAngleMax
        maxAngle = FishingAngleMax
        if angle < minAngle:
            self.arrow.setColorScale(1, 0, 0, 1)
            angle = minAngle
        elif angle > maxAngle:
            self.arrow.setColorScale(1, 0, 0, 1)
            angle = maxAngle
        else:
            self.arrow.setColorScale(1, 1 - math.pow(self.power, 3), 0.1, 0.7)
        self.arrowTail.setScale(0.075, 0.075, self.power * 0.2)
        self.arrow.setR(angle)
        
        self.toon.toon.setH(self.toonH-angle-angleDiff)
        
        self.angle = -angle
        
        return task.cont
        
    def getMouse(self):
        if base.mouseWatcherNode.hasMouse():
            self.mouseX = base.mouseWatcherNode.getMouseX()
            self.mouseY = base.mouseWatcherNode.getMouseY()
        else:
            self.mouseX = 0
            self.mouseY = 0
        
    def __castMOver(self,flag,event):
        if flag == 0 and self.isCasting:
            return
        
        self.castButton['image_color'] = self.castButtonColors[flag]
        
    def __updateMoney(self):
        #print 'updating money'
        self.jar["text"] = str(self.getAvMoney())
        self.jar.setText()
        
    def __updateFishTank(self,lenFishTank):
        self.bucket['text'] = '%s/%s' % (lenFishTank, 20)
        
    def removeNode(self):
        self.boards.removeNode()
        self.exitButton.removeNode()
        DirectFrame.removeNode(self)