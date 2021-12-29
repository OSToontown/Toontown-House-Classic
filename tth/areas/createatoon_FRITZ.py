#coding: latin-1
"""
Author: Nacib
Date: JULY/25/2013
Description: Create-a-toon screen
FROM COGTOWN

"""

from direct.gui.DirectGui import *
from direct.actor.Actor import *
from pandac.PandaModules import *
import sys, os
from random import *

from tth.avatar.names import generateRandomToonNameExt as grtn, fetchAll
from tth.gui import UnicodeText
from tth.base.TTHouseUtils import rgb2p
from tth.avatar.Toon import Toon, ToonDNA
from tth.avatar.loader import saveNewToon

TOON_SCALE = 0.8

def hex2p(h):
    r,g,b = map(lambda x:int(x,16)*256/15.,[h[i:i+1] for i in range(0,len(h),2)])
    return map(lambda x: min(x,1.00),rgb2p(r,g,b))

class CreateAToon:
    def __init__(self,args,tp=None):
        self.slot=args[0]

        gamebase.curArea = self

        self.CAT_music = loader.loadMusic("phase_3/audio/bgm/create_a_toon.mid")
        self.CAT_music.setLoop(1)
        self.CAT_music.play()

        self.frame = DirectFrame(parent=base.a2dBackground)
        self.textframe = DirectFrame(parent=base.a2dBackground)

        environ = loader.loadModel('phase_3/models/gui/create_a_toon.bam')
        self.floor = environ.find('**/floor')
        self.wall = environ.find('**/wall_floor')
        self.stool = environ.find('**/stool')

        #self.anim = Actor("phase_3/models/makeatoon/roomAnim_model.bam",{"drop":"phase_3/models/makeatoon/roomAnim_roomDrop.bam"})
        #self.anim.reparentTo(render)

        self._colors = range(1,len(ToonDNA.allColorsList[1:]))
        color = choice(self._colors)
        self.data = {
                    "gender":"",
                    "color1":color,
                    "color2":color,
                    "color3":color,
                    "color4":0,
                    "top":"bss1",
                    "topC":0,
                    "bot":"bbs1",
                    "botC":0,
                    "name":grtn("M"),
                    "spc":0,
                    "head":0,
                    "body":"l",
                    "legs":.5,
                    "head":0,
                    }

        self.np = render.attachNewNode('CreateAToonSet')

        self.environ = self.np.attachNewNode('parte-que-interessa') #what is it?
        self.floor.reparentTo(self.np)
        self.wall.reparentTo(self.np)
        self.stool.reparentTo(self.np)

        self.env_room_zones = ['','drafting_table','easel','sewing_machine','']
        self.env_room_titles = map(L10N,["CAT_TITLE_GENDER","CAT_TITLE_SPECIES","CAT_TITLE_COLOR","CAT_TITLE_CLOTHES","CAT_TITLE_NAME"])

        self.curzone = 0

        self.titleText = TextNode('titleText')
        self.titleText.setTextColor(1,.8,0,1)
        self.titleText.setFont(loader.loadFont('phase_3/models/fonts/MickeyFont.bam'))
        self.titleText.setAlign(TextNode.ACenter)
        self.titleTextNp = self.textframe.attachNewNode(self.titleText)
        self.titleTextNp.setPos(0,0,.675)
        self.titleTextNp.setScale(.2,1,.25)

        loader.loadModel('phase_3.5/models/props/TT_sky.bam').reparentTo(self.np)

        self.playCrash = map(base.loader.loadSfx, ["phase_3/audio/sfx/tt_s_ara_mat_crash_boing.mp3","phase_3/audio/sfx/tt_s_ara_mat_crash_glassBoing.mp3",
                                                        "phase_3/audio/sfx/tt_s_ara_mat_crash_wood.mp3","phase_3/audio/sfx/tt_s_ara_mat_crash_woodBoing.mp3",
                                                        "phase_3/audio/sfx/tt_s_ara_mat_crash_woodGlass.mp3"])

        self.wallColors = ((0.5,0.3,0.2,1),(0,0.6,0.6,1),(0.7,0,0.2,1),(0,0.7,0.5,1),(0.6,0.7,0.2,1))

        self.nextZone()

        base.accept('x',lambda:self.toon.reColor((random(),)*3,(random(),)*3,(random(),)*3))

        self.toonTypes =  map(L10N,["SPC_CAT","SPC_PIG","SPC_DOG","SPC_HORSE","SPC_BEAR","SPC_MOUSE","SPC_DUCK","SPC_RABBIT","SPC_MONKEY"])
        self._hModels = ["cat","pig","dog","horse","bear","mouse","duck","rabbit","monkey"]

        #self._clrNames =  map(L10N,["COLOR_GOLDEN","COLOR_LIGHTBLUE","COLOR_DARKBLUE","COLOR_PINK","COLOR_DARKGREEN",
         #                   "COLOR_LIGHTGREEN","COLOR_BROWN","COLOR_PURPLE","COLOR_RED","COLOR_ORANGE","COLOR_YELLOW"])
        #doesnt matter atm

        self.cColor = 0

        self.maxTopM = len(ToonDNA.ShirtStyles['bss1']) #len(ToonDNA.getTops('m'))
        self.maxTopF = len(ToonDNA.ShirtStyles['bss1']) #len(ToonDNA.getTops('f'))

        self.maxBotM = len(ToonDNA.BottomStyles['bbs1']) #len(ToonDNA.getBottoms('m'))
        self.maxBotF = len(ToonDNA.BottomStyles['bbs1']) #len(ToonDNA.getBottoms('f'))

        self.names = [sorted(fetchAll(self.data['gender'],['t','f','l1','l2'][i])) for i in xrange(4)]

        self.dna = ToonDNA.ToonDNA(dnaType='t')
        self.updateDNA()

        self.toon = Toon()
        self.toon.setH(135)
        self.toon.loop('neutral')
        self.toon.reparentTo(self.np)

        if tp: tp.done()

    def updateDNA(self):
        def __makeHead():
            tt = {'d': 'dog','c': 'cat','h': 'horse','m':'mouse','r':'rabbit','f':'duck','p':'monkey','b':'bear','s':'pig'}
            tt = dict(zip(tt.values(),tt.keys()))[self._hModels[self.data['spc']]]

            numb = self.data['head']
            if tt[0] == "m": numb %= 2

            tt += (("ss","sl","ls","ll"),("ss","ls"))[tt=="m"][int(numb)]
            return tt

        def __makeTorso():
            x = self.data['body']
            return x+'s'

        self.dna.updateToonProperties(
                                       head = __makeHead(),
                                       torso = __makeTorso(),
                                       legs = {.5:'s',.75:'m',1:'l'}[self.data['legs']],
                                       gender = self.data['gender'].lower(),
                                       armColor = self.data['color2'],
                                       gloveColor = self.data['color4'],
                                       legColor = self.data['color3'],
                                       headColor = self.data['color1'],
                                       topTexture = None,
                                       topTextureColor = None,
                                       sleeveTexture = None,
                                       sleeveTextureColor = None,
                                       bottomTexture = None,
                                       bottomTextureColor = None,
                                       shirt = ("bss1",self.data['topC']),
                                       bottom = ("bbs1",self.data['botC'])
                                    )

    def reloadToon(self):
        self.updateDNA()

        self.toon.cleanup()
        self.toon.removeNode()

        self.toon = Toon()
        self.toon.reparentTo(self.np)
        self.toon.setH(135)
        self.toon.setDNA(self.dna)
        self.toon.loop('neutral')
        self.toon.setScale(self.toon,1/TOON_SCALE)

    def cleanUpEnviron(self):
        self.environ.removeNode()
        self.environ = self.np.attachNewNode('parte-que-interessa') #tuw

    def getGuiItem(self,name):
        self.gui_items = {m.getName().split('_')[-1]:m for m in loader.loadModel('phase_3/models/gui/tt_m_gui_mat_mainGui.bam').findAllMatches('**') if m.getName()}
        if name == 'ALL':
            return self.gui_items.keys()
        return self.gui_items[filter(lambda x: name in x,self.gui_items.keys())[0]]

    def getNameGuiItem(self,name):
        self.gui_items = {m.getName().split('_')[-1]:m for m in loader.loadModel('phase_3/models/gui/tt_m_gui_mat_nameShop.bam').findAllMatches('**') if m.getName()}
        if name == 'ALL':
            return self.gui_items.keys()
        return self.gui_items[filter(lambda x: name in x,self.gui_items.keys())[0]]

    def nextZone(self):
        self.cleanUpEnviron()
        print 'Showing',self.env_room_zones[self.curzone%len(self.env_room_zones)]
        self.loadZone(self.env_room_zones[self.curzone%len(self.env_room_zones)]).reparentTo(self.environ)
        self.environment.find('**/'+self.env_room_zones[self.curzone]).scaleInterval(0.1,(1,1,1),startScale=(1,1,0)).start()
        self.playCrash[self.curzone].play()
        self.loadZoneGui()
        self.loadZoneTitle()
        self.wall.setColor(self.wallColors[self.curzone])
        self.curzone+=1

    def previousZone(self):
        self.curzone-=2
        self.cleanUpEnviron()
        print 'Showing',self.env_room_zones[self.curzone%len(self.env_room_zones)]
        self.loadZone(self.env_room_zones[self.curzone%len(self.env_room_zones)]).reparentTo(self.environ)
        self.environment.find('**/'+self.env_room_zones[self.curzone]).scaleInterval(0.1,(1,1,1),startScale=(1,1,0)).start()
        self.playCrash[self.curzone].play()
        self.loadZoneGui()
        self.loadZoneTitle()
        self.wall.setColor(self.wallColors[self.curzone])
        self.curzone+=1

    def loadZone(self,zone):
        base.cam.setPos((-0.7046, -16.793, 4))
        base.cam.setH(0)
        if hasattr(self,"toon"):
            self.toon.setH(135)
            self.toon.setPos(0,0,0)
        self.environment = loader.loadModel('phase_3/models/gui/create_a_toon.bam')
        return self.environment.find('**/'+zone)

    def loadZoneTitle(self):
        self.titleText.setWtext(L10N('CAT_CHOOSE')+ " " +self.env_room_titles[self.curzone%len(self.env_room_titles)])

    def setGender(self,gender):
        self.data['gender']=gender
        if gender == 'M':
            self.gui_boyButton['state'] = DGG.DISABLED
            self.gui_girlButton['state'] = DGG.NORMAL
        if gender == 'F':
            self.gui_girlButton['state'] = DGG.DISABLED
            self.gui_boyButton['state'] = DGG.NORMAL

        self.nextButton['state'] = DGG.NORMAL

        self.names = [sorted(fetchAll(self.data['gender'],['t','f','l1','l2'][i])) for i in xrange(4)]

        try: self.gui_boyText.destroy()
        except: pass
        try: self.gui_girlText.destroy()
        except: pass

        if gender == 'F' and self.data['bot'] > self.maxBotF: self.data['bot'] = 3

        self.data['name'] = grtn(gender)

        self.reloadToon()

    def nextToonType(self):
        self.data["spc"] += 1
        if self.data["spc"] >= 9: self.data["spc"] = 0
        self.gui_tFt.setText(self.toonTypes[self.data["spc"]])
        self.gui_tFt.setSx(3./len(self.toonTypes[self.data["spc"]]))

        self.reloadToon()

    def prevToonType(self):
        self.data["spc"] -= 1
        if self.data["spc"] == -1: self.data["spc"] = 8
        self.gui_tFt.setText(self.toonTypes[self.data["spc"]])
        self.gui_tFt.setSx(3./len(self.toonTypes[self.data["spc"]]))

        self.reloadToon()

    def nextToonHead(self):
        self.data["head"] += 1
        if self.data["head"] >= 4: self.data["head"] = 0

        self.reloadToon()

    def prevToonHead(self):
        self.data["head"] -= 1
        if self.data["head"] == -1: self.data["head"] = 3

        self.reloadToon()

    def nextToonTorso(self):
        self.data["body"] = ["l","s","m"][(["l","s","m"].index(self.data["body"])+1)%3]

        self.reloadToon()

    def prevToonTorso(self):
        self.data["body"] = ["l","s","m"][["l","s","m"].index(self.data["body"])-1]

        self.reloadToon()

    def nextToonLegs(self):
        self.data["legs"] = [.5,.75,1][([.5,.75,1].index(self.data["legs"])+1)%3]

        self.reloadToon()

    def prevToonLegs(self):
        self.data["legs"] = [.5,.75,1][[.5,.75,1].index(self.data["legs"])-1]

        self.reloadToon()

    def nextToonColor(self,id=None):
        self.cColor = (self.cColor+1)%len(self._colors)
        _c = self._colors[self.cColor]
        if id is None:
            self.data["color1"] = (_c)
            self.data["color2"] = (_c)
            self.data["color3"] = (_c)

        else:
            self.data["color"+str(id)] = _c

        self.reloadToon() #self.toon.reColor(self.data['color1'],self.data['color2'],self.data['color3'])

    def prevToonColor(self,id=None):
        self.cColor -= 1
        _c = self._colors[self.cColor]
        if id is None:
            self.data["color1"] = _c
            self.data["color2"] = _c
            self.data["color3"] = _c

        else:
            self.data["color"+str(id)] = _c

        self.reloadToon() #self.toon.reColor(self.data['color1'],self.data['color2'],self.data['color3'])

    def changeTop(self,isPrev=False):
        _maxTop = getattr(self,'maxTop'+self.data['gender'])
        if isPrev:
            self.data["topC"] -= 1
            if self.data["topC"]  < 0: self.data["topC"] = _maxTop

        else:
            self.data["topC"] += 1
            if self.data["topC"] > _maxTop: self.data["topC"] = 0

        self.reloadToon() #self.toon.reTexture(self.data['top'],str(self.data['bot'])+('s'*(self.data['gender']=='F')),None)

    def changeBot(self,isPrev=False):
        _max = getattr(self,'maxBot'+self.data['gender'])
        if isPrev:
            self.data["botC"] -= 1
            if self.data["botC"] < 0: self.data["botC"] = _max

        else:
            self.data["botC"] += 1
            if self.data["botC"] > _max: self.data["botC"] = 0

        self.reloadToon() #self.toon.reTexture(self.data['top'],str(self.data['bot'])+('s'*(self.data['gender']=='F')),None)

    def shuffle(self,zone):

        #print ':CAT:Shuffle:sDict'
        _d = [0,0,0,0]
        _d[1] = {'head':range(4),'body':['l','m','s'],'legs':[.5,.75,1],'spc':range(8)}

        _d[2] = {'color1':self._colors,'color2':self._colors,'color3':self._colors,'color4':self._colors}

        _d[3] = {'top':range(100),'bot':range(20)}

        #print ':CAT:Shuffle:apply'

        for a,v in _d[zone].items(): self.data[a]=choice(v)

        #print ':CAT:Shuffle:reload'

        if zone == 1 or 1: self.reloadToon()
        #if zone == 2: self.toon.reColor(self.data['color1'],self.data['color2'],self.data['color3'])
        #if zone == 3: self.toon.reTexture(self.data['top'],str(self.data['bot'])+('s'*(self.data['gender']=='F')),None)

    def typeName(self):

        self.gui_tanf = self.getNameGuiItem('typeName')
        self.gui_tanf.reparentTo(self.frame)

    def exit_gaveup(self): #xD
        gamebase.curArea = None
        gamebase.themeMusic = loader.loadMusic("phase_3/audio/bgm/tt_theme.mid")
        gamebase.themeMusic.setLoop(1)
        base.transitions.fadeIn()
        gamebase.themeMusic.play()
        messenger.send('load-chooseatoon-screen')
        self.dismiss()

    def exit_fnAA(self):
        saveNewToon(*map(str,[self.slot,self.buildName(),self.dna.makeNetString(),'','']))
        base.transitions.fadeIn()
        messenger.send('end-createatoon')
        self.dismiss()

    def gui_n_updateButt(self):
        g_circle = self.getNameGuiItem('ircle')
        g_circle.setColor(Vec4(.2,1,.2,1),1)
        _b = self.data['name'][:-1]
        bts = (self.gui_tnb,self.gui_fnb,self.gui_lnb)
        for i,b in enumerate(bts):
            b['geom'] = (g_circle,None,None,None)
            if not _b[i]: b['geom'] = (None,g_circle,g_circle,None)

        _b = self.data['name'][-1]
        for i in xrange(4):
            eval('self.sl'+str(i+1)).show()
            if not _b[i]: eval('self.sl'+str(i+1)).hide()
        self.buildName()

    def recompileName(self,old,new):
        _name = self.data['name'][-1]
        changes = [0,0,0,0]
        for i,(n,o) in enumerate(zip(new,old)):
            if n == o: changes[i]=0
            elif not n and o: changes[i]=1
            elif n and not o: changes[i]=2

        changes[-1] = changes[-2]

        for i,change in enumerate(changes):
            if change > 0:
                _name[i] = (7,None)[change==1]

        return _name

    def gui_n_butt_click(self,i):
        _now = self.data['name'][:3]
        _new = list(_now[:])
        _new[i] = not _now[i]

        _nname = self.recompileName(_now,_new)

        #print _new
        if _new in ([True,False,True],[True,True,True],[True,True,False],[False,True,True],[False,True,False]):
            self.data['name'] = tuple(_new+[_nname])

        for i in xrange(4):
            if _nname[i]: self.gui_n_frameClick(i+1,_nname[i])

        self.gui_n_updateButt()

    def gui_n_frameClick(self,_frameId,_item):
        for i in self.gui_li[_frameId]:
            i['frameColor'] = (0.0,0.0,0.0,0.0)
        self.gui_li[_frameId][_item]['frameColor'] = (1,230./255,196./255,1)

        eval('self.sl'+str(_frameId)).scrollTo(_item,True)
        self.buildName()

    def gui_n_selectFI(self,f,i,event):
        self.data['name'][-1][f] = i
        self.gui_n_frameClick(f+1,i)
        self.buildName()

    def buildName(self):
        _n = []
        _nms = self.data['name'][-1]
        for i,n in enumerate(_nms):
            if n is not None:
                _n.append(self.names[i][n])
                if i == 3:
                    _n.pop()
                    _n[-1]+=self.names[i][n]


        _text = unicode(' '.join(_n).decode('latin-1'))
        #print ':CAT:Name built:',_text
        self.gui_nameText.setText(_text)

        return ' '.join(_n)

    def loadZoneGui(self):
        self.frame.removeNode()
        self.frame = DirectFrame(parent=base.a2dBackground)
        _zone = self.curzone%len(self.env_room_titles)

        self.gui_nextUp = self.getGuiItem("nextUp")
        self.gui_nextDown = self.getGuiItem("nextDown")
        self.gui_nextDis = self.getGuiItem("nextDisabled")

        self.gui_ok = self.getGuiItem("okUp")

        self.nextButton = DirectButton(parent=self.frame,pos=Vec3(1.1,0,-.85),scale=.3,text="",relief=None,
                                       geom=(self.gui_nextUp,self.gui_nextDown,self.gui_nextUp,self.gui_nextDis),
                                       command=self.nextZone,clickSound=gamebase.sounds['GUI_click'],
                                       rolloverSound=gamebase.sounds['GUI_rollover'])

        self.backButton = DirectButton(parent=self.frame,pos=Vec3(.8,0,-.85),scale=.3,text="",relief=None,
                                       geom=(self.gui_nextUp,self.gui_nextDown,self.gui_nextUp,self.gui_nextDis),
                                       command=self.previousZone,clickSound=gamebase.sounds['GUI_click'],
                                       rolloverSound=gamebase.sounds['GUI_rollover'])

        self.closeButton = DirectButton(parent=self.frame,pos=Vec3(-1.2,0,-.85),scale=.5,text="",relief=None,
                                       geom=self.getGuiItem('closeUp'),
                                       command=self.exit_gaveup,clickSound=gamebase.sounds['GUI_click'],
                                       rolloverSound=gamebase.sounds['GUI_rollover'])

        self.backButton.setH(180)

        if 0 < _zone <= 3:
            self.gui_tFs = DirectButton(parent=self.frame,pos=Vec3(1,0,-.55),text="",scale=.694105,
                                        relief=None,geom=self.getGuiItem('shuffleUp'),command=self.shuffle,extraArgs=[_zone])

            shuffleText = TextNode('shuffletext')
            shuffleText.setFont(BTFont)
            shuffleText.setAlign(TextNode.ACenter)
            shuffleText.setWtext(L10N('CAT_SHUFFLE'))
            shuffleTextNp = self.gui_tFs.attachNewNode(shuffleText)
            shuffleTextNp.setColor((1,1,1,1))
            shuffleTextNp.setPos(0,0,-.04)
            shuffleTextNp.setScale(.075)

        if _zone == 0:
            self.backButton['state'] = DGG.DISABLED
            self.gui_boyUp = self.getGuiItem("boyUp")
            self.gui_boyDown = self.getGuiItem("boyDown")
            self.gui_girlUp = self.getGuiItem("girlUp")
            self.gui_girlDown = self.getGuiItem("girlDown")

            self.gui_boyButton = DirectButton(parent=self.frame,pos=Vec3(-.4,0,-.8),scale=.5,text="",relief=None,
                                              geom=(self.gui_boyUp,self.gui_boyDown,self.gui_boyUp,self.gui_boyDown),
                                              command=self.setGender,extraArgs=["M"],clickSound=gamebase.sounds['GUI_click'],
                                              rolloverSound=gamebase.sounds['GUI_rollover'])

            self.gui_girlButton = DirectButton(parent=self.frame,pos=Vec3(.4,0,-.8),scale=.5,text="",relief=None,
                                              geom=(self.gui_girlUp,self.gui_girlDown,self.gui_girlUp,self.gui_girlDown),
                                              command=self.setGender,extraArgs=["F"],clickSound=gamebase.sounds['GUI_click'],
                                              rolloverSound=gamebase.sounds['GUI_rollover'])

            self.backButton.destroy()
            self.nextButton['state'] = DGG.DISABLED

            def _boyIn(e):
                self.gui_boyButton.setScale(.53)
                self.gui_boyText = OnscreenText(text=L10N('CAT_BOY'),parent=self.gui_boyButton,pos=(0,.3),fg=(1,1,1,1),scale=.15)

            def _boyOut(e):
                self.gui_boyButton.setScale(.5)
                self.gui_boyText.destroy()

            def _girlIn(e):
                self.gui_girlButton.setScale(.53)
                self.gui_girlText = OnscreenText(text=L10N('CAT_GIRL'),parent=self.gui_girlButton,pos=(0,.3),fg=(1,1,1,1),scale=.15)

            def _girlOut(e):
                self.gui_girlButton.setScale(.5)
                self.gui_girlText.destroy()

            self.gui_boyButton.bind(DGG.WITHIN, _boyIn)
            self.gui_boyButton.bind(DGG.WITHOUT, _boyOut)

            self.gui_girlButton.bind(DGG.WITHIN, _girlIn)
            self.gui_girlButton.bind(DGG.WITHOUT, _girlOut)

            if self.data['gender']: self.setGender(self.data['gender'])

        elif _zone == 1:
            self.gui_arUp = self.getGuiItem("arrowRotateUp")
            self.gui_arDown = self.getGuiItem("arrowRotateDown")
            self.gui_sframe = self.getGuiItem("Frame")
            self.gui_sUp = self.getGuiItem("shuffleArrowUp")
            self.gui_sDown = self.getGuiItem("shuffleArrowDown")

            #type

            self.gui_arRightButton = DirectButton(parent=self.frame,pos=Vec3(.4,0,-.65),scale=.5,text="",relief=None,
                                       geom=(self.gui_arUp,self.gui_arDown,self.gui_arUp,self.gui_arUp),
                                       command=lambda:self.toon.setH(self.toon,25),clickSound=gamebase.sounds['GUI_click'],
                                       rolloverSound=gamebase.sounds['GUI_rollover'])

            self.gui_arLeftButton = DirectButton(parent=self.frame,pos=Vec3(-.15,0,-.65),scale=.5,text="",relief=None,
                                       geom=(self.gui_arUp,self.gui_arDown,self.gui_arUp,self.gui_arUp),
                                       command=lambda:self.toon.setH(self.toon,-25),clickSound=gamebase.sounds['GUI_click'],
                                       rolloverSound=gamebase.sounds['GUI_rollover'])

            self.gui_tFrame = DirectButton(parent=self.frame,pos=Vec3(1,0,.3),scale=.8,text="",relief=None,
                                       geom=self.gui_sframe,command=self.nextToonType,clickSound=gamebase.sounds['GUI_click'],
                                       rolloverSound=gamebase.sounds['GUI_rollover'])

            self.gui_tFlb = DirectButton(parent=self.gui_tFrame,pos=Vec3(-.338,0,0),text="",relief=None,geom=(self.gui_sUp,self.gui_sDown,
                                         self.gui_sDown,self.gui_sDown),command=self.prevToonType)

            self.gui_tFrb = DirectButton(parent=self.gui_tFrame,pos=Vec3(.338,0,0),text="",relief=None,geom=(self.gui_sUp,self.gui_sDown,
                                         self.gui_sDown,self.gui_sDown),command=self.nextToonType)

            self.gui_tFt = OnscreenText(text=L10N('SPC_CAT'),scale=.2,parent=self.gui_tFrame,pos=(0,-.07),font=BTFont,fg=(1,1,1,1),mayChange=1)
            self.gui_tFrb.setH(180)
            self.gui_arLeftButton.setH(180)

            #head

            self.gui_tHeadFrame = DirectButton(parent=self.frame,pos=Vec3(1,0,.1),scale=.5235,text="",relief=None,
                                       geom=self.gui_sframe,command=self.nextToonHead,clickSound=gamebase.sounds['GUI_click'],
                                       rolloverSound=gamebase.sounds['GUI_rollover'])


            DirectButton(parent=self.gui_tHeadFrame,pos=Vec3(-.338,0,0),text="",relief=None,geom=(self.gui_sUp,self.gui_sDown,
                                         self.gui_sDown,self.gui_sDown),command=self.prevToonHead)

            DirectButton(parent=self.gui_tHeadFrame,pos=Vec3(.338,0,0),text="",relief=None,geom=(self.gui_sUp,self.gui_sDown,
                                         self.gui_sDown,self.gui_sDown),command=self.nextToonHead).setH(180)

            headText = TextNode('head text')
            headText.setFont(BTFont)
            headText.setAlign(TextNode.ACenter)
            headText.setWtext(L10N('CAT_HEAD'))
            headTextNp = self.gui_tHeadFrame.attachNewNode(headText)
            headTextNp.setPos(0,0,0)
            headTextNp.setColor((1,1,1,1))
            headTextNp.setScale(.12)

            #torso

            self.gui_tTorsoFrame = DirectButton(parent=self.frame,pos=Vec3(1,0,-.1),scale=.5235,text="",relief=None,
                                       geom=self.gui_sframe,command=self.nextToonTorso,clickSound=gamebase.sounds['GUI_click'],
                                       rolloverSound=gamebase.sounds['GUI_rollover'])


            DirectButton(parent=self.gui_tTorsoFrame,pos=Vec3(-.338,0,0),text="",relief=None,geom=(self.gui_sUp,self.gui_sDown,
                                         self.gui_sDown,self.gui_sDown),command=self.prevToonTorso)

            DirectButton(parent=self.gui_tTorsoFrame,pos=Vec3(.338,0,0),text="",relief=None,geom=(self.gui_sUp,self.gui_sDown,
                                         self.gui_sDown,self.gui_sDown),command=self.nextToonTorso).setH(180)

            OnscreenText(text=L10N('CAT_TORSO'),scale=.12,parent=self.gui_tTorsoFrame,pos=(0,-.04),font=BTFont,fg=(1,1,1,1))

            #legs

            self.gui_tLegsFrame = DirectButton(parent=self.frame,pos=Vec3(1,0,-.3),scale=.5235,text="",relief=None,
                                       geom=self.gui_sframe,command=self.nextToonLegs,clickSound=gamebase.sounds['GUI_click'],
                                       rolloverSound=gamebase.sounds['GUI_rollover'])


            DirectButton(parent=self.gui_tLegsFrame,pos=Vec3(-.338,0,0),text="",relief=None,geom=(self.gui_sUp,self.gui_sDown,
                                         self.gui_sDown,self.gui_sDown),command=self.prevToonLegs)

            DirectButton(parent=self.gui_tLegsFrame,pos=Vec3(.338,0,0),text="",relief=None,geom=(self.gui_sUp,self.gui_sDown,
                                         self.gui_sDown,self.gui_sDown),command=self.nextToonLegs).setH(180)

            OnscreenText(text=L10N('CAT_LEGS'),scale=.12,parent=self.gui_tLegsFrame,pos=(0,-.04),font=BTFont,fg=(1,1,1,1))

        elif _zone == 2:
            self.gui_arUp = self.getGuiItem("arrowRotateUp")
            self.gui_arDown = self.getGuiItem("arrowRotateDown")
            self.gui_sframe = self.getGuiItem("Frame")
            self.gui_sUp = self.getGuiItem("shuffleArrowUp")
            self.gui_sDown = self.getGuiItem("shuffleArrowDown")

            #type

            self.gui_arRightButton = DirectButton(parent=self.frame,pos=Vec3(.4,0,-.65),scale=.5,text="",relief=None,
                                       geom=(self.gui_arUp,self.gui_arDown,self.gui_arUp,self.gui_arUp),
                                       command=lambda:self.toon.setH(self.toon,25),clickSound=gamebase.sounds['GUI_click'],
                                       rolloverSound=gamebase.sounds['GUI_rollover'])

            self.gui_arLeftButton = DirectButton(parent=self.frame,pos=Vec3(-.15,0,-.65),scale=.5,text="",relief=None,
                                       geom=(self.gui_arUp,self.gui_arDown,self.gui_arUp,self.gui_arUp),
                                       command=lambda:self.toon.setH(self.toon,-25),clickSound=gamebase.sounds['GUI_click'],
                                       rolloverSound=gamebase.sounds['GUI_rollover'])

            self.gui_tFrame = DirectButton(parent=self.frame,pos=Vec3(1,0,.5),scale=.8,text="",relief=None,
                                       geom=self.gui_sframe,command=self.nextToonColor,clickSound=gamebase.sounds['GUI_click'],
                                       rolloverSound=gamebase.sounds['GUI_rollover'])

            self.gui_tFlb = DirectButton(parent=self.gui_tFrame,pos=Vec3(-.338,0,0),text="",relief=None,geom=(self.gui_sUp,self.gui_sDown,
                                         self.gui_sDown,self.gui_sDown),command=self.prevToonColor)

            self.gui_tFrb = DirectButton(parent=self.gui_tFrame,pos=Vec3(.338,0,0),text="",relief=None,geom=(self.gui_sUp,self.gui_sDown,
                                         self.gui_sDown,self.gui_sDown),command=self.nextToonColor)

            self.gui_tFt = OnscreenText(text="Toon",scale=.115,parent=self.gui_tFrame,pos=(0,-.04), #the word 'Toon' is equal for all langs
                            font=BTFont,fg=(1,1,1,1))
            self.gui_tFt.setSx(.75)
            self.gui_tFrb.setH(180)
            self.gui_arLeftButton.setH(180)

            #head

            self.gui_tHeadFrame = DirectButton(parent=self.frame,pos=Vec3(1,0,.3),scale=.5235,text="",relief=None,
                                       geom=self.gui_sframe,command=self.nextToonColor,clickSound=gamebase.sounds['GUI_click'],
                                       rolloverSound=gamebase.sounds['GUI_rollover'],extraArgs=['1'])


            DirectButton(parent=self.gui_tHeadFrame,pos=Vec3(-.338,0,0),text="",relief=None,geom=(self.gui_sUp,self.gui_sDown,
                                         self.gui_sDown,self.gui_sDown),command=self.prevToonColor,extraArgs=['1'])

            DirectButton(parent=self.gui_tHeadFrame,pos=Vec3(.338,0,0),text="",relief=None,geom=(self.gui_sUp,self.gui_sDown,
                                         self.gui_sDown,self.gui_sDown),command=self.nextToonColor,extraArgs=['1']).setH(180)

            headText = TextNode('head text')
            headText.setFont(BTFont)
            headText.setAlign(TextNode.ACenter)
            headText.setWtext(L10N('CAT_HEAD'))
            headTextNp = self.gui_tHeadFrame.attachNewNode(headText)
            headTextNp.setPos(0,0,0)
            headTextNp.setColor((1,1,1,1))
            headTextNp.setScale(.12)

            #torso

            self.gui_tTorsoFrame = DirectButton(parent=self.frame,pos=Vec3(1,0,.1),scale=.5235,text="",relief=None,
                                       geom=self.gui_sframe,command=self.nextToonColor,clickSound=gamebase.sounds['GUI_click'],
                                       rolloverSound=gamebase.sounds['GUI_rollover'],extraArgs=['2'])


            DirectButton(parent=self.gui_tTorsoFrame,pos=Vec3(-.338,0,0),text="",relief=None,geom=(self.gui_sUp,self.gui_sDown,
                                         self.gui_sDown,self.gui_sDown),command=self.prevToonColor,extraArgs=['2'])

            DirectButton(parent=self.gui_tTorsoFrame,pos=Vec3(.338,0,0),text="",relief=None,geom=(self.gui_sUp,self.gui_sDown,
                                         self.gui_sDown,self.gui_sDown),command=self.nextToonColor,extraArgs=['2']).setH(180)

            OnscreenText(text=L10N('CAT_TORSO'),scale=.12,parent=self.gui_tTorsoFrame,pos=(0,-.04),
                         font=BTFont,fg=(1,1,1,1))

            #gloves

            self.gui_tGlovesFrame = DirectButton(parent=self.frame,pos=Vec3(1,0,-.1),scale=.5235,text="",relief=None,
                                       geom=self.gui_sframe,command=self.nextToonColor,extraArgs=['4'])


            DirectButton(parent=self.gui_tGlovesFrame,pos=Vec3(-.338,0,0),text="",relief=None,geom=(self.gui_sUp,self.gui_sDown,
                                         self.gui_sDown,self.gui_sDown),command=self.prevToonColor,extraArgs=['4'])

            DirectButton(parent=self.gui_tGlovesFrame,pos=Vec3(.338,0,0),text="",relief=None,geom=(self.gui_sUp,self.gui_sDown,
                                         self.gui_sDown,self.gui_sDown),command=self.nextToonColor,extraArgs=['4']).setH(180)

            OnscreenText(text=L10N.Gloves,scale=.12,parent=self.gui_tGlovesFrame,pos=(0,-.04),
                         font=BTFont,fg=(1,1,1,1))

            #legs

            self.gui_tLegsFrame = DirectButton(parent=self.frame,pos=Vec3(1,0,-.3),scale=.5235,text="",relief=None,
                                       geom=self.gui_sframe,command=self.nextToonColor,clickSound=gamebase.sounds['GUI_click'],
                                       rolloverSound=gamebase.sounds['GUI_rollover'],extraArgs=['3'])


            DirectButton(parent=self.gui_tLegsFrame,pos=Vec3(-.338,0,0),text="",relief=None,geom=(self.gui_sUp,self.gui_sDown,
                                         self.gui_sDown,self.gui_sDown),command=self.prevToonColor,extraArgs=['3'])

            DirectButton(parent=self.gui_tLegsFrame,pos=Vec3(.338,0,0),text="",relief=None,geom=(self.gui_sUp,self.gui_sDown,
                                         self.gui_sDown,self.gui_sDown),command=self.nextToonColor,extraArgs=['3']).setH(180)

            OnscreenText(text=L10N('CAT_LEGS'),scale=.12,parent=self.gui_tLegsFrame,pos=(0,-.04),font=BTFont,fg=(1,1,1,1))

        elif _zone == 3:
            self.gui_arUp = self.getGuiItem("arrowRotateUp")
            self.gui_arDown = self.getGuiItem("arrowRotateDown")
            self.gui_sframe = self.getGuiItem("Frame")
            self.gui_sUp = self.getGuiItem("shuffleArrowUp")
            self.gui_sDown = self.getGuiItem("shuffleArrowDown")

            #type

            self.gui_arRightButton = DirectButton(parent=self.frame,pos=Vec3(.4,0,-.65),scale=.5,text="",relief=None,
                                       geom=(self.gui_arUp,self.gui_arDown,self.gui_arUp,self.gui_arUp),
                                       command=lambda:self.toon.setH(self.toon,25),clickSound=gamebase.sounds['GUI_click'],
                                       rolloverSound=gamebase.sounds['GUI_rollover'])

            self.gui_arLeftButton = DirectButton(parent=self.frame,pos=Vec3(-.15,0,-.65),scale=.5,text="",relief=None,
                                       geom=(self.gui_arUp,self.gui_arDown,self.gui_arUp,self.gui_arUp),
                                       command=lambda:self.toon.setH(self.toon,-25),clickSound=gamebase.sounds['GUI_click'],
                                       rolloverSound=gamebase.sounds['GUI_rollover'])

            self.gui_tFrame = DirectButton(parent=self.frame,pos=Vec3(1,0,.3),scale=.8,text="",relief=None,
                                       geom=self.gui_sframe,command=self.nextToonColor,clickSound=gamebase.sounds['GUI_click'],
                                       rolloverSound=gamebase.sounds['GUI_rollover'],state=DGG.DISABLED)

            self.gui_tFrame.hide()

            self.gui_tFlb = DirectButton(parent=self.gui_tFrame,pos=Vec3(-.338,0,0),text="",relief=None,geom=(self.gui_sUp,self.gui_sDown,
                                         self.gui_sDown,self.gui_sDown),command=self.prevToonColor)

            self.gui_tFrb = DirectButton(parent=self.gui_tFrame,pos=Vec3(.338,0,0),text="",relief=None,geom=(self.gui_sUp,self.gui_sDown,
                                         self.gui_sDown,self.gui_sDown),command=self.nextToonColor)

            self.gui_tFt = OnscreenText(text="Toon",scale=.115,parent=self.gui_tFrame,pos=(0,-.04),
                            font=BTFont,fg=(1,1,1,1))
            self.gui_tFt.setSx(.75)
            self.gui_tFrb.setH(180)
            self.gui_arLeftButton.setH(180)

            #head

            self.gui_tHeadFrame = DirectButton(parent=self.frame,pos=Vec3(1,0,.1),scale=.5235,text="",relief=None,
                                       geom=self.gui_sframe,command=self.changeTop,clickSound=gamebase.sounds['GUI_click'],
                                       rolloverSound=gamebase.sounds['GUI_rollover'],extraArgs=['1'])


            DirectButton(parent=self.gui_tHeadFrame,pos=Vec3(-.338,0,0),text="",relief=None,geom=(self.gui_sUp,self.gui_sDown,
                                         self.gui_sDown,self.gui_sDown),command=self.changeTop)

            DirectButton(parent=self.gui_tHeadFrame,pos=Vec3(.338,0,0),text="",relief=None,geom=(self.gui_sUp,self.gui_sDown,
                                         self.gui_sDown,self.gui_sDown),command=self.changeTop).setH(180)

            OnscreenText(text=L10N("CAT_SHIRT"),scale=.12,parent=self.gui_tHeadFrame,pos=(0,-.04),
                         font=BTFont,fg=(1,1,1,1))

            #torso

            self.gui_tTorsoFrame = DirectButton(parent=self.frame,pos=Vec3(1,0,-.1),scale=.5235,text="",relief=None,
                                       geom=self.gui_sframe,command=self.changeBot,clickSound=gamebase.sounds['GUI_click'],
                                       rolloverSound=gamebase.sounds['GUI_rollover'])


            DirectButton(parent=self.gui_tTorsoFrame,pos=Vec3(-.338,0,0),text="",relief=None,geom=(self.gui_sUp,self.gui_sDown,
                                         self.gui_sDown,self.gui_sDown),command=self.changeBot,extraArgs=[True])

            DirectButton(parent=self.gui_tTorsoFrame,pos=Vec3(.338,0,0),text="",relief=None,geom=(self.gui_sUp,self.gui_sDown,
                                         self.gui_sDown,self.gui_sDown),command=self.changeBot).setH(180)

            botText = L10N("CAT_SHORTS")
            if self.data['gender']=='F': botText=L10N("CAT_SKIRT")

            OnscreenText(text=botText,scale=.12,parent=self.gui_tTorsoFrame,pos=(0,-.04),
                         font=BTFont,fg=(1,1,1,1))

        elif _zone == 4:
            self.nextButton['geom'] = self.gui_ok
            self.nextButton['command'] = self.exit_fnAA
            self.nextButton.setScale(.8)
            base.cam.setPos(1, -21.1231, 4)
            base.cam.setH(-2)
            self.toon.setPos(5, -1, 0)
            self.toon.setH(90)

            g_up = (self.getNameGuiItem('ArrowUp'),self.getNameGuiItem('ArrowUp'),
                    self.getNameGuiItem('ArrowDown'),self.getNameGuiItem('ArrowDown'))

            g_down = (self.getNameGuiItem('ArrowUp'),self.getNameGuiItem('ArrowUp'),
                      self.getNameGuiItem('ArrowDown'),self.getNameGuiItem('ArrowDown'))

            g_circle = self.getNameGuiItem('ircle')
            g_circle.setColor(Vec4(.2,1,.2,1),1)

            for g in g_down: g.setP(180)

            DirectFrame(parent=self.frame,frameSize=(-.15,.16,-.19,.19),frameColor=(230./255,190./255,207./255,1),pos=(-1.075,0,-.03))
            DirectFrame(parent=self.frame,frameSize=(-.15,.16,-.19,.19),frameColor=(190./255,230./255,196./255,1),pos=(-.675,0,-.03))
            DirectFrame(parent=self.frame,frameSize=(-.16,.16,-.19,.19),frameColor=(237./255,185./255,236./255,1),pos=(-.27,0,-.03))
            DirectFrame(parent=self.frame,frameSize=(-.15,.18,-.19,.19),frameColor=(237./255,185./255,236./255,1),pos=(.07,0,-.03))

            self.gui_nPanel = self.getNameGuiItem('namePanel')
            self.gui_nPanel.reparentTo(self.frame)
            self.gui_nPanel.setScale(.75)
            self.gui_nPanel.setX(-.5)

            self.gui_nameText = OnscreenText(align=TextNode.ACenter,text=unicode('\x135\x135'),parent=self.gui_nPanel,
                                             pos=(.025,.675),wordwrap=1/.075,scale=(.07,.1))
            self.buildName()

            _dPos,_iPos = ((0,0,.13),(0,0,-.33))
            _lz = .08

            self.sl1=DirectScrolledList(parent=self.frame,pos=(-1.075,0,_lz),
                                        numItemsVisible=5,itemFrame_frameColor=(1,0.0,0.0,1),itemFrame_pos = (0, 0, 0),
                                        decButton_geom = g_up,incButton_geom = g_down,
                                        decButton_relief = None,incButton_relief = None,
                                        decButton_pos = _dPos,incButton_pos = _iPos,
                                        decButton_scale = .695,incButton_scale = .695,
                                        decButton_clickSound=gamebase.sounds['GUI_click'],
                                        decButton_rolloverSound=gamebase.sounds['GUI_rollover'],
                                        incButton_clickSound=gamebase.sounds['GUI_click'],
                                        incButton_rolloverSound=gamebase.sounds['GUI_rollover'])

            self.sl2=DirectScrolledList(parent=self.frame,pos=(-.675,0,_lz),
                                        numItemsVisible=5,itemFrame_frameColor=(1,0.0,0.0,1),
                                        decButton_geom = g_up,incButton_geom = g_down,
                                        decButton_relief = None,incButton_relief = None,
                                        decButton_pos = _dPos,incButton_pos = _iPos,
                                        decButton_scale = .695,incButton_scale = .695,
                                        decButton_clickSound=gamebase.sounds['GUI_click'],
                                        decButton_rolloverSound=gamebase.sounds['GUI_rollover'],
                                        incButton_clickSound=gamebase.sounds['GUI_click'],
                                        incButton_rolloverSound=gamebase.sounds['GUI_rollover'])


            self.sl3=DirectScrolledList(parent=self.frame,pos=(-.27,0,_lz),
                                        numItemsVisible=5,itemFrame_frameColor=(1,0.0,0.0,1),
                                        decButton_geom = g_up,incButton_geom = g_down,
                                        decButton_relief = None,incButton_relief = None,
                                        decButton_pos = _dPos,incButton_pos = _iPos,
                                        decButton_scale = .695,incButton_scale = .695,
                                        decButton_clickSound=gamebase.sounds['GUI_click'],
                                        decButton_rolloverSound=gamebase.sounds['GUI_rollover'],
                                        incButton_clickSound=gamebase.sounds['GUI_click'],
                                        incButton_rolloverSound=gamebase.sounds['GUI_rollover'])


            self.sl4=DirectScrolledList(parent=self.frame,pos=(.07,0,_lz),
                                        numItemsVisible=5,itemFrame_frameColor=(1,0.0,0.0,1),
                                        decButton_geom = g_up,incButton_geom = g_down,
                                        decButton_relief = None,incButton_relief = None,
                                        decButton_pos = _dPos,incButton_pos = _iPos,
                                        decButton_scale = .695,incButton_scale = .695,
                                        decButton_clickSound=gamebase.sounds['GUI_click'],
                                        decButton_rolloverSound=gamebase.sounds['GUI_rollover'],
                                        incButton_clickSound=gamebase.sounds['GUI_click'],
                                        incButton_rolloverSound=gamebase.sounds['GUI_rollover'])

            self.gui_li = [0,[],[],[],[]]

            for i in xrange(4):
                _sl = eval('self.sl'+str(i+1))
                for b,name in enumerate(self.names[i]):
                    l = DirectLabel(text = unicode(name.decode('latin-1')),text_scale=(.045,.055),
                                     frameColor = (0,0,0,0), state=DGG.NORMAL)
                    l.bind(DGG.B1PRESS,self.gui_n_selectFI,[i,b])
                    _sl.addItem(l)
                    self.gui_li[i+1].append(l)
                    if self.data['name'][-1][i] == b:
                        print i,b,self.data['name'][-1][i]
                        _sl.selectListItem(l)
                        self.gui_n_frameClick(i+1,b)

            self.gui_tnb = DirectButton(pos=Vec3(-1.185, 0, 0.275),scale=.6,geom=g_circle,relief=None,parent=self.frame,clickSound=gamebase.sounds['GUI_click'],
                                       rolloverSound=gamebase.sounds['GUI_rollover'],command=self.gui_n_butt_click,extraArgs=[0])
            self.gui_tnb.setColor(.2,1,.2,1)
            self.gui_tnt = UnicodeText(L10N('MAT_TIT'),self.gui_tnb.getParent(),pos=(-1.085,0,.245),align = TextNode.ALeft, fg=Vec4(0,0,1,1), scale=.06)

            self.gui_lnb = DirectButton(pos=Vec3(-.178, 0, 0.275),scale=.6,geom=g_circle,relief=None,parent=self.frame,clickSound=gamebase.sounds['GUI_click'],
                                       rolloverSound=gamebase.sounds['GUI_rollover'],command=self.gui_n_butt_click,extraArgs=[2])
            self.gui_lnb.setColor(.2,1,.2,1)
            self.gui_lnt = UnicodeText(L10N('MAT_FIR'),self.gui_lnb.getParent(),pos=(-.078,0,.245),align = TextNode.ALeft, fg=Vec4(0,0,1,1), scale=.06)

            self.gui_fnb = DirectButton(pos=Vec3(-.787, 0, 0.275),scale=.6,geom=g_circle,relief=None,parent=self.frame,clickSound=gamebase.sounds['GUI_click'],
                                       rolloverSound=gamebase.sounds['GUI_rollover'],command=self.gui_n_butt_click,extraArgs=[1])
            self.gui_fnb.setColor(.2,1,.2,1)
            self.gui_fnt = UnicodeText(L10N('MAT_LAS'),self.gui_fnb.getParent(),pos=(-.687,0,.245),align = TextNode.ALeft, fg=Vec4(0,0,1,1), scale=.06)

            self.gui_n_updateButt()

            ######################################

            self.typeNameBt = DirectButton(parent = self.gui_nPanel,geom=self.getNameGuiItem('quareUp'),relief=None,clickSound=gamebase.sounds['GUI_click'],
                                            rolloverSound=gamebase.sounds['GUI_rollover'],pos=Vec3(0,0,-.529),text="Escreva um nome",
                                            command=self.typeName,scale=.07,geom_scale=1.8/.07).hide() #dont implement this right now



    def dismiss(self):
        self.np.removeNode()
        self.frame.removeNode()
        self.textframe.removeNode()
        self.CAT_music.stop()

    def __tth_area__(self): pass



