# -*- coding: latin-1 -*-  #
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *
from tth.managers import Timer
from tth.avatar.loader import loadToonData, getAvatarName, getAvatarDNA
from random import randint, shuffle
from direct.task import Task
from direct.actor.Actor import Actor

from tth.avatar.ToonDNA import ToonDNA
from tth.avatar.ToonHead import ToonHead

from hashlib import md5,sha256
import os, sys

from tth.areas.etc import *

class LoadingScreen:
    def __init__(self):
        self.loadingImage = OnscreenImage(image="phase_3/maps/loading_bg_clouds.jpg")
        self.loadingImage.reparentTo(render2d)
        self.ttlogo = OnscreenImage(image="phase_0/toontown-logo-new.png",scale=.45,pos=(0,0,0))
        self.ttlogo.setSx(1)
        self.ttlogo.setSz(.5)
        self.ttlogo.reparentTo(self.loadingImage)
        self.ttlogo.setTransparency(TransparencyAttrib.MAlpha)
        gamebase.themeMusic = loader.loadMusic("phase_3/audio/bgm/tt_theme.mid")
        gamebase.themeMusic.setLoop(1)
        gamebase.themeMusic.play()
        #version = "Alpha-TTH 8wRJQj5y"

        #Version1 = OnscreenText(text = str(version), font=loader.loadFont('phase_3/models/fonts/ImpressBT.ttf'), pos = (1,0.9,1), scale = 0.07)

        self.falseBar = DirectWaitBar(text = "", value = 0, pos = (0,0,-.8))
        self.falseBar.setSz(.5)
        self.falseBar.setSx(1.2)
        self.falseBar["barColor"] = (0,0.99,0,1)

        Timer((.1,3)['-fast' not in sys.argv],self.dismiss,self.step)

        self.bar_anim_brpoints = [0]
        for _ in xrange(8):
            self.bar_anim_brpoints.append(randint(3,98))
        self.bar_anim_brpoints.append(83)
        self.bar_anim_brpoints.append(100)
        self.bar_anim_brpoints.sort(key=int)

        #loading function 1: test for Blob

        #DEPRECATED
        #print 'Testing for Blob. Exists:',
        #print os.path.isfile(gamebase.findpath("userdata.blob"))

        #if not os.path.isfile(gamebase.findpath("userdata.blob")):
        #   from tth.datahnd.Blob import newBlob
        #  print 'Creating new blob...'
        # newBlob(gamebase.findpath("userdata.blob"))

    def step(self,time):
        self.falseBar['value'] = [i for i in self.bar_anim_brpoints if i<=(3-time)/3*100][-1]

    def dismiss(self):
        if '-getStuckInLoadScreen' in sys.argv:
            return

        if base.cr.isConnected2:
            print 'Removing loading screen...'
            self.loadingImage.destroy()
            self.falseBar.destroy()
            #Wait(7) #wtf

            #this is stupid. dont ask why.
            #who in the fuck did this? i WASTED 20 minutes trying to remove this "BUG"
            #if im_stupid:
            #Why the fuck do you guys wait for 7 seconds! >:C
            #IndentationError : indent out of range

            fake_grayscreen = False
            if fake_grayscreen:
                print 'gray screen is not a bug. dont freak out'
                gray = OnscreenImage(image = 'data/gray.png', pos = (0, 0, 0.0), parent=render2d)
                [base.graphicsEngine.renderFrame() for i in xrange(8)]
                gray.destroy()

            messenger.send("load-chooseatoon-screen")
        else:
            base.cr.onConnLoad = True

NAME_ROTATIONS = (7, -11, 1, -5, 3.5, -5)
NAME_POSITIONS = ((0, 0, 0.26),
 (-0.03, 0, 0.25),
 (0, 0, 0.27),
 (-0.03, 0, 0.25),
 (0.03, 0, 0.26),
 (0, 0, 0.26))
DELETE_POSITIONS = ((0.187, 0, -0.26),
 (0.31, 0, -0.167),
 (0.231, 0, -0.241),
 (0.314, 0, -0.186),
 (0.243, 0, -0.233),
 (0.28, 0, -0.207))
POSITIONS = (Vec3(-0.840167, 0, 0.359333),
 Vec3(0.00933349, 0, 0.306533),
 Vec3(0.862, 0, 0.3293),
 Vec3(-0.863554, 0, -0.445659),
 Vec3(0.00999999, 0, -0.5181),
 Vec3(0.864907, 0, -0.445659))
COLORS = (Vec4(0.917, 0.164, 0.164, 1),
 Vec4(0.152, 0.75, 0.258, 1),
 Vec4(0.598, 0.402, 0.875, 1),
 Vec4(0.133, 0.59, 0.977, 1),
 Vec4(0.895, 0.348, 0.602, 1),
 Vec4(0.977, 0.816, 0.133, 1))

class DeleteFrame(DirectLabel):
    def __init__(self, position = 0, name = "this toon"):

        from tth.gui import dialog

        DirectLabel.__init__(self, image = DGG.getDefaultDialogGeom(), relief=None)
        self.initialiseoptions(DeleteFrame)

        self.position = position

        _text = L10N('CTP_DELETEDIAG') % name

        self.blockingFrame = DirectFrame(frameColor = (0,0,0,.1),frameSize = (10,-10,1,-1),
                                         state = DGG.NORMAL,parent = self)

        self._text = OnscreenText(text=_text,scale=.065,parent=self,wordwrap=.75/.065,pos = (0,.360))
        self.entry = DirectEntry(parent = self._text, scale = .1, width = 8,
                                 numLines = 1, focus = 1, pos=(-.4,0,-.215),
                                 relief = DGG.RIDGE, obscured = 1,
                                 command = self.__ok)

        self.pw = globalBlob.read('acc_passwd')
        if self.pw == "NO_SUCH_FILE":
            print 'Dev account detected!'
            self.pw = ""
            self._text.setText("This is a dev account (no password). Press OK to delete %s." % name)
            #self.entry["state"] = DGG.DISABLED

        self.stText = OnscreenText(text="",scale=.4,parent=self.entry,pos = (.5,-.4),mayChange = 1,align=TextNode.ALeft)

        self.okButt = DirectButton(parent = self, geom = dialog.okButtons,
                                   command = self.__ok, scale = 1.25, relief = None,
                                   pos=(-.1,0,-.41))

        self.cancelButt = DirectButton(parent = self, geom = dialog.cancelButtons,
                                   command = self.removeNode, scale = 1.25, relief = None,
                                   pos=(.1,0,-.41))

        self.resetFrameSize()
        self.reparentTo(self.getParent())

    def __ok(self, text = None):
        if text is None: text = self.entry.get()
        if text: hashed = self._hash(text)
        else: hashed = ""

        if hashed == self.pw:
            print 'OK!'
            self.__success()

        else:
            print 'FAILED!'
            self.stText.setText(L10N('CTP_DELETE_ST_FAILED'))
            self.stText['fg'] = (1,0,0,1)

    def _hash(self,passwd):
        return md5(sha256(passwd).digest()).hexdigest()[::-1]

    def __success(self):
        self.removeNode()
        globalBlob.delToon(self.position)
        self._ctpScr.dismiss()
        messenger.send("load-chooseatoon-screen")

class AvatarChoice(DirectButton):
    MODE_CREATE = 0
    MODE_CHOOSE = 1

    def __init__(self, position = 0, _ctpScr = None):
        DirectButton.__init__(self, relief=None, text='', state=DGG.NORMAL,
                              text_font=loader.loadFont('phase_3/models/fonts/MickeyFont.bam'),
                              text_wordwrap = 8)
        self.initialiseoptions(AvatarChoice)
        self.mode = None

        self._ctpScr = _ctpScr

        name = getAvatarName(position)
        if not name:
            self.mode = AvatarChoice.MODE_CREATE
            self.name = ''
        else:
            self.mode = AvatarChoice.MODE_CHOOSE
            self.name = name
        self.position = position
        self.pickAToonGui = loader.loadModel('phase_3/models/gui/tt_m_gui_pat_mainGui.bam')
        self.buttonBgs = map(lambda x: self.pickAToonGui.find('**/tt_t_gui_pat_square'+x),('Red','Green','Purple','Blue','Pink','Yellow'))
        self['image'] = self.buttonBgs[position]
        self.setScale(1.01)
        if self.mode is AvatarChoice.MODE_CREATE:
            self['command'] = self.__handleChoice
            self['text'] = (L10N('CTP_MAK'),)
            self['text_pos'] = (0, 0)
            self['text0_scale'] = .1
            self['text1_scale'] = .12
            self['text2_scale'] = .12
            self['text0_fg'] = (0, 1, 0.8, 0.5)
            self['text1_fg'] = (0, 1, 0.8, 1)
            self['text2_fg'] = (0.3, 1, 0.9, 1)
        else:
            self['command'] = self.__handleChoice
            self['text'] = ('', L10N('CTP_PLAYTHIS').replace('\\n','\n'), L10N('CTP_PLAYTHIS').replace('\\n','\n'))
            self['text_scale'] = .12
            self['text_fg'] = (1, 0.9, 0.1, 1)
            self.nameText = DirectLabel(parent=self, relief=None, scale=0.08, pos=NAME_POSITIONS[position], text=self.name,
                                        hpr=(0, 0, NAME_ROTATIONS[position]), text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1),
                                        text_wordwrap=8, state=DGG.DISABLED)

            self.head = hidden.attachNewNode('head')
            self.head.setPosHprScale(0, 5, -0.1, 180, 0, 0, 0.24, 0.24, 0.24)
            self.head.reparentTo(self.stateNodePath[0], 20)
            self.head.instanceTo(self.stateNodePath[1], 20)
            self.head.instanceTo(self.stateNodePath[2], 20)

            self.dna = ToonDNA(dnaType='t')
            dnaString = getAvatarDNA(self.position)
            #print dnaString,len(dnaString),self.dna.isValidNetString(dnaString),sys.exit()
            self.dna.makeFromNetString(dnaString)

            self.headModel = self._ctpScr.loadHead(self.head,self.dna)
            self.headModel.startBlink()
            self.headModel.startLookAround()

            trashcanGui = loader.loadModel('phase_3/models/gui/trashcan_gui.bam')
            self.deleteButton = DirectButton(parent=self, image=(trashcanGui.find('**/TrashCan_CLSD'),
                                                                 trashcanGui.find('**/TrashCan_OPEN'),
                                                                 trashcanGui.find('**/TrashCan_RLVR')),
                                             text='', relief=None, pos=DELETE_POSITIONS[position], scale=0.45, command=self.__handleDelete)
            trashcanGui.removeNode()

        self.resetFrameSize()

    def __handleChoice(self):
        print 'CHOICE',self
        #self.sounds['GUI_click'].play()
        gamebase.toonChosen(self.position)

    def __handleDelete(self):
        DeleteFrame(self.position, self.name)._ctpScr = self._ctpScr

class ChooseAToonScreen:
    def __init__(self): #based on original from TT
        self.frame=DirectFrame(frameColor=(1, 1, 1, 1),parent=base.a2dBackground)
        self.frame.wrtReparentTo(base.cam2d)#render2d)

        gui = loader.loadModel('phase_3/models/gui/pick_a_toon_gui.bam')
        gui2 = loader.loadModel('phase_3/models/gui/quit_button.bam')
        newGui = loader.loadModel('phase_3/models/gui/tt_m_gui_pat_mainGui.bam')

        self.pickAToonBG = newGui.find('**/tt_t_gui_pat_background')
        self.pickAToonBG.setTexture(loader.loadTexture("phase_3/maps/tt_t_gui_pat_background.jpg"),1) #changed to the recent TT bg. (Old Pick A Toon BG was phase_0/newpat.jpg)
        self.pickAToonBG.reparentTo(self.frame)
        self.pickAToonBG.setPos(0.0, 2.73, 0.0)
        self.pickAToonBG.setScale(1, 1, 1)

        self.title = OnscreenText(text=L10N('CTP_CHOOSETEXT'),pos=(0,.82),scale=.15,parent=self.frame,
                                  font=loader.loadFont("phase_3/models/fonts/MickeyFont.bam"),fg=Vec4(1,.82,.1,1),wordwrap=18)

        quitHover = gui.find('**/QuitBtn_RLVR')
        self.quitButton = DirectButton(image=(quitHover, quitHover, quitHover), relief=None, text=L10N('CTP_EXIT'),
                                       text_font=loader.loadFont("phase_3/models/fonts/MickeyFont.bam"), text_fg=(0.977, 0.816, 0.133, 1),
                                       text_pos=(0, -0.035), text_scale=.1, image_scale=1, image1_scale=1.05, image2_scale=1.05,
                                       scale=1.05, pos=(1.08, 0, -0.907), command=sys.exit, parent=self.frame)

        gui.removeNode()
        gui2.removeNode()
        newGui.removeNode()
        #return
        self.panelList = []
        for i in xrange(6):
            panel = AvatarChoice(i,self)
            panel.setPos(POSITIONS[i])
            #panel.wrtReparentTo(self.frame)
            self.panelList.append(panel)

    def __init__OLD(self):
        self.frame=DirectFrame(frameColor=(1, 1, 1, 1),parent=base.a2dBackground)
        self.bgImage=OnscreenImage(image="data/images/patbg_old.jpg",parent=render2d)
        self.base=base
        base.setBackgroundColor(0,0,0)
        OnscreenText(text=L10N('CTP_CHOOSETEXT'),pos=(0,.8),fg=Vec4(1,.8,0,1),parent=self.frame,scale=.1,font=loader.loadFont("phase_3/models/fonts/MickeyFont.bam"))
        self.buttons = []
        for i in xrange(6):
            _i = i
            _x=([-.88,-.05,.785][i%3])
            _y=[.37,-.45][i>2]
            #print _i,_x,_y
            b = DirectFrame(frameColor=(0,0,0,0),scale=1,pos=(_x,0,_y),frameSize=(-.32,.42,.35,-.38),parent=self.frame,state=DGG.NORMAL)
            name = getAvatarName(i)
            print i,name ####### debug
            if name:
                self.loadHead(b,_i)
                t = OnscreenText(text=unicode(name.decode('latin-1')),parent=b,wordwrap=8,scale=.1,fg=(1,1,1,1),pos=(.05,.2),font=loader.loadFont("phase_3/models/fonts/ImpressBT.ttf"))
            else:
                t = OnscreenText(text=L10N('CTP_MAK'),parent=b,wordwrap=5,scale=.13,fg=Vec4(1,1,1,1),pos=(.05,0),font=loader.loadFont("phase_3/models/fonts/MickeyFont.bam"))
            self.buttons.append((b,t))
            #b.bind(DGG.B1PRESS,lambda e:gamebase.toonChosen(i))
            b.bind(DGG.B1PRESS,self.chosen,extraArgs=[i])
            b.bind(DGG.WITHIN,self.mOver,extraArgs=[i])
            b.bind(DGG.WITHOUT,self.mOut,extraArgs=[i])

        self.exitButt = DirectFrame(frameColor=(0,0,0,0),scale=1,pos=(0,0,-.92),frameSize=(-.2,.2,.06,-.06),parent=self.frame,state=DGG.NORMAL)
        self.exitButt.bind(DGG.B1PRESS,sys.exit)
        self.exitButt.bind(DGG.WITHIN,self.mOver,extraArgs=[6])
        self.exitButt.bind(DGG.WITHOUT,self.mOut,extraArgs=[6])
        t=OnscreenText(text=L10N('CTP_EXIT'),parent=self.exitButt,scale=.1,fg=Vec4(.1,1,.1,1),pos=(.02,-.04),font=loader.loadFont("phase_3/models/fonts/MickeyFont.bam"))
        self.buttons.append((self.exitButt,t))

    def chosen(self,i,event):
        self.sounds['GUI_rollover'].play()
        gamebase.toonChosen(i)

    def mOver(self,i,event):
        self.sounds['GUI_rollover'].play()
        _t = self.buttons[i][1]
        _t.setScale(_t.getScale()[0]+0.02)

    def mOut(self,i,event):
        self.sounds['GUI_rollover'].play()
        _t = self.buttons[i][1]
        _t.setScale(_t.getScale()[0]-0.02)

    def delete(self,i):

        globalBlob.delToon(i)
        #reload this screen
        self.dismiss()
        messenger.send("load-chooseatoon-screen")

    def loadHead(self, parent, dna):
        data = loadToonData(id)
        '''
        numb,toontype = data["head"],["cat","pig","dog","horse","bear","mouse","duck","rabbit","monkey"][int(data['spc'])]
        headcolor = data["color1"].split(',')
        _args = [toontype]
        _args.extend(map(lambda x:float(x.strip('()')),headcolor))
        _args.append(numb)
        _args.append(data["gender"])
        head = loadToonHead(*_args)
        '''

        head = ToonHead()
        head.setupHead(dna,True)
        head.reparentTo(parent)

        head.setDepthTest(True)
        head.setDepthWrite(True)
        head.setDepthOffset(0) #Any higher than -50 makes the heads glitch.

        head.setTwoSided(True)
        return head

    def dismiss(self):
        print 'Removendo a tela escolha-um-toon...'
        print 'If you understand this sentence, CONGRATS !'
        self.frame.removeNode()
        for x in self.panelList:
            x.removeNode()
