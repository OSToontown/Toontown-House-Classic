from panda3d.core import *
from direct.gui.DirectGui import *
BUTT_W = .6
BUTT_H = .07
TEXT_SCALE = (BUTT_H/2.,BUTT_H)
FRAME_COLOR = Vec4(1,1,1,.9)
class ExtendableList:
    def __init__(self,pos,items):
        self.pos = pos
        self.items = items
        
    def addItem(self,item):
        self.items.append(item)
        
    def make(self,frame,i=0):
        self.f = DirectFrame(pos=(BUTT_W,0,0),parent=frame,frameSize=(0,BUTT_W,BUTT_H+.01,-(BUTT_H+.01)*len(self.items)),frameColor=(0,0,0,0),state=DGG.NORMAL)
        self.f.bind(DGG.WITHIN,self._within)
        for a,i in enumerate(self.items):
            i.make(self.f,a)
            i.show()
            
        return self.f
    def _within(self,e): self.f.bind(DGG.WITHOUT,lambda *a: self._hide())
        
    def _hide(self):
        if not self.f:
            return
            
        if base.mouseWatcherNode.hasMouse():
            mx = base.mouseWatcherNode.getMouseX()*4/3.
            fx = self.f.getX(aspect2d)
            cond = mx<fx
            if cond:
                self.f.hide()        
        else:
            self.f.hide()
            
class SimpleButton:
    def __init__(self,text,iText=None):
        self.f = DirectFrame(frameSize=(0,BUTT_W,BUTT_H+.01,-.01),text=text,text_pos=(0,+.01),text_align=TextNode.ALeft,frameColor=FRAME_COLOR,text_scale=TEXT_SCALE,state=DGG.NORMAL)
        self.f.hide()
        self.text = text
        self.iText = iText
        self.f.bind(DGG.B1PRESS,self.onClick)
        
        self.emotion = None
        
    def onClick(self,ev):
        gamebase.curArea.toon.b_speak('@{0}'.format(self.iText))
        base.distMgr.menuGui.removeNode()
        
        if self.emotion:
            gamebase.curArea.toon.b_amin(self.emotion)
        
    def make(self,frame,i):
        self.f.reparentTo(frame)
        self.f.setPos(0,0,-(BUTT_H+.01)*i)
        return self.f
        
    def show(self):
        self.f.show()
        
class ExtendableButt:
    def __init__(self,(text,iText)):
        self.f = DirectFrame(frameSize=(0,BUTT_W,BUTT_H+.01,-.01),text=text.upper(),text_pos=(0,+.01),text_align=TextNode.ALeft,frameColor=FRAME_COLOR,text_scale=TEXT_SCALE,state=DGG.NORMAL)
        
        self._list = ExtendableList((0,0,0),[])
            
        self.f.hide()
        
        self.addItem = self._list.addItem
        self.text = text
        self.f.bind(DGG.WITHIN,self.show)
        self.f.bind(DGG.WITHOUT,self.hide)
        
    def make(self,frame,i):
        self.f.reparentTo(frame)
        self.f.setPos(0,0,-(BUTT_H+.01)*i)
        self._list.make(self.f,i)
        return self.f
        
    def show(self,event=None):
        self.f.show()
        if event is None:
            for x in self.f.getChildren(): x.hide()
        else:
            for x in self.f.getChildren(): x.show()
            
    def hide(self,event=None):
        if base.mouseWatcherNode.hasMouse():
            mx = base.mouseWatcherNode.getMouseX()*4/3.
            fx = self.f.getX(aspect2d)+BUTT_W
            if mx<fx:
                for x in self.f.getChildren(): x.hide()
                
        else:
            for x in self.f.getChildren(): x.hide()
     
def bake():    
    global EL_ROOT,EB_EMOT,EB_JBWK,EB_RACE,EB_PETS,EB_HELLO,EB_GOODBYE,EB_SAD,EB_FRND,EB_SORRY,EB_STINKY,EB_PLACES,EB_TASK,EB_BTL,EB_GSHOP,SB_YES,SB_NO,SB_OK
    EL_ROOT = ExtendableList((-2,0,0),[])
    
    #emotions
    EB_EMOT = ExtendableButt(*L10N.sc_fetch("SC_EMOT"))
    for x in L10N.sc_fetch("SC_EMOT_%"):
        EB_EMOT.addItem(SimpleButton(*x))
        
    #jellybean week
    EB_JBWK = ExtendableButt(*L10N.sc_fetch("SC_JELLYWEEK"))
    EB_JBWK_GET = ExtendableButt(*L10N.sc_fetch("SC_JELLYWEEK_GET"))
    for x in L10N.sc_fetch("SC_JELLYWEEK_GET_*"): EB_JBWK_GET.addItem(SimpleButton(*x))
    EB_JBWK_SPD = ExtendableButt(*L10N.sc_fetch("SC_JELLYWEEK_SPEND"))
    for x in L10N.sc_fetch("SC_JELLYWEEK_SPEND_*"): EB_JBWK_SPD.addItem(SimpleButton(*x))
    
    EB_JBWK.addItem(EB_JBWK_GET)
    EB_JBWK.addItem(EB_JBWK_SPD)
        
    #race
    EB_RACE = ExtendableButt(*L10N.sc_fetch("SC_RACE"))
    EB_RACE_PL = ExtendableButt(*L10N.sc_fetch("SC_RACE_PL"))
    for x in L10N.sc_fetch("SC_RACE_PL_*"): EB_RACE_PL.addItem(SimpleButton(*x))
    EB_RACE_RC = ExtendableButt(*L10N.sc_fetch("SC_RACE_RC"))
    for x in L10N.sc_fetch("SC_RACE_RC_*"): EB_RACE_RC.addItem(SimpleButton(*x))
    EB_RACE_TK = ExtendableButt(*L10N.sc_fetch("SC_RACE_TK"))
    for x in L10N.sc_fetch("SC_RACE_TK_*"): EB_RACE_TK.addItem(SimpleButton(*x)) 
    EB_RACE_CP = ExtendableButt(*L10N.sc_fetch("SC_RACE_CP"))
    for x in L10N.sc_fetch("SC_RACE_CP_*"): EB_RACE_CP.addItem(SimpleButton(*x))
    EB_RACE_TA = ExtendableButt(*L10N.sc_fetch("SC_RACE_TA"))
    for x in L10N.sc_fetch("SC_RACE_TA_*"): EB_RACE_TA.addItem(SimpleButton(*x))
    
    EB_RACE.addItem(EB_RACE_PL)
    EB_RACE.addItem(EB_RACE_RC)
    EB_RACE.addItem(EB_RACE_TK)
    EB_RACE.addItem(EB_RACE_CP)
    EB_RACE.addItem(EB_RACE_TA)
    
    for x in L10N.sc_fetch("SC_RACE_%"): EB_RACE.addItem(SimpleButton(*x))
    
    #pets
    EB_PETS = ExtendableButt(*L10N.sc_fetch("SC_PETS"))
    EB_PETS_TR = ExtendableButt(*L10N.sc_fetch("SC_PETS_TR"))
    for x in L10N.sc_fetch("SC_PETS_TR_*"): EB_PETS_TR.addItem(SimpleButton(*x))
    EB_PETS.addItem(EB_PETS_TR)
    for x in L10N.sc_fetch("SC_PETS_%"): EB_PETS.addItem(SimpleButton(*x))
        
    #hello
    EB_HELLO = ExtendableButt(*L10N.sc_fetch("SC_HELLO"))
    for x in L10N.sc_fetch("SC_HELLO_*"): EB_HELLO.addItem(SimpleButton(*x))
    
    #GOODBYE
    EB_GOODBYE = ExtendableButt(*L10N.sc_fetch("SC_GOODBYE"))
    for x in L10N.sc_fetch("SC_GOODBYE_*"): EB_GOODBYE.addItem(SimpleButton(*x))
    
    #SAD
    EB_SAD = ExtendableButt(*L10N.sc_fetch("SC_SAD"))
    for x in L10N.sc_fetch("SC_SAD_*"): EB_SAD.addItem(SimpleButton(*x))
    
    #friendly
    EB_FRND = ExtendableButt(*L10N.sc_fetch("SC_FRIENDLY"))
    EB_FRND_YOU = ExtendableButt(*L10N.sc_fetch("SC_FRIENDLY_YOU"))
    for x in L10N.sc_fetch("SC_FRIENDLY_YOU_*"): EB_FRND_YOU.addItem(SimpleButton(*x))
    EB_FRND_LIKE = ExtendableButt(*L10N.sc_fetch("SC_FRIENDLY_LIKE"))
    for x in L10N.sc_fetch("SC_FRIENDLY_LIKE_*"): EB_FRND_LIKE.addItem(SimpleButton(*x))
    
    EB_FRND.addItem(EB_FRND_YOU)
    EB_FRND.addItem(EB_FRND_LIKE)
    
    for x in L10N.sc_fetch("SC_FRIENDLY_%"): EB_FRND.addItem(SimpleButton(*x))
    
    #sorry
    EB_SORRY = ExtendableButt(*L10N.sc_fetch("SC_SORRY"))
    for x in L10N.sc_fetch("SC_SORRY_*"): EB_SORRY.addItem(SimpleButton(*x))
    
    #STINKY
    EB_STINKY = ExtendableButt(*L10N.sc_fetch("SC_STINKY"))
    for x in L10N.sc_fetch("SC_STINKY_*"): EB_STINKY.addItem(SimpleButton(*x))
    
    #places
    EB_PLACES = ExtendableButt(*L10N.sc_fetch("SC_PLACES"))
    EB_PLACES_PG = ExtendableButt(*L10N.sc_fetch("SC_PLACES_PG"))
    for x in L10N.sc_fetch("SC_PLACES_PG_*"): EB_PLACES_PG.addItem(SimpleButton(*x))
    EB_PLACES_CG = ExtendableButt(*L10N.sc_fetch("SC_PLACES_CG"))
    for x in L10N.sc_fetch("SC_PLACES_CG_*"): EB_PLACES_CG.addItem(SimpleButton(*x))
    EB_PLACES_ES = ExtendableButt(*L10N.sc_fetch("SC_PLACES_ES"))
    for x in L10N.sc_fetch("SC_PLACES_ES_*"): EB_PLACES_ES.addItem(SimpleButton(*x))
    EB_PLACES_PY = ExtendableButt(*L10N.sc_fetch("SC_PLACES_PY"))
    for x in L10N.sc_fetch("SC_PLACES_PY_*"): EB_PLACES_PY.addItem(SimpleButton(*x))
    EB_PLACES_W8 = ExtendableButt(*L10N.sc_fetch("SC_PLACES_W8"))
    for x in L10N.sc_fetch("SC_PLACES_W8_*"): EB_PLACES_W8.addItem(SimpleButton(*x))
    
    EB_PLACES.addItem(EB_PLACES_PG)
    EB_PLACES.addItem(EB_PLACES_CG)
    EB_PLACES.addItem(EB_PLACES_ES)
    EB_PLACES.addItem(EB_PLACES_PY)
    EB_PLACES.addItem(EB_PLACES_W8)
    
    for x in L10N.sc_fetch("SC_PLACES_%"): EB_PLACES.addItem(SimpleButton(*x))
    
    #task
    EB_TASK = ExtendableButt(*L10N.sc_fetch("SC_TASK"))
    SB_TASK_MY = SimpleButton(*L10N.sc_fetch("SC_TASK_MY"))
    EB_TASK_CHOOSE = ExtendableButt(*L10N.sc_fetch("SC_TASK_CHOOSE"))
    for x in L10N.sc_fetch("SC_TASK_CHOOSE_*"): EB_TASK_CHOOSE.addItem(SimpleButton(*x))
    EB_TASK_NEED = ExtendableButt(*L10N.sc_fetch("SC_TASK_NEED"))
    for x in L10N.sc_fetch("SC_TASK_NEED_*"): EB_TASK_NEED.addItem(SimpleButton(*x))
    
    #EB_TASK.addItem(EB_TASK_MY)
    EB_TASK.addItem(EB_TASK_CHOOSE)
    EB_TASK.addItem(EB_TASK_NEED)
    
    for x in L10N.sc_fetch("SC_TASK_%"): EB_TASK.addItem(SimpleButton(*x))
    
    #battle
    EB_BTL = ExtendableButt(*L10N.sc_fetch("SC_BATTLE"))
    EB_BTL_GAGS = ExtendableButt(*L10N.sc_fetch("SC_BATTLE_GAGS"))
    for x in L10N.sc_fetch("SC_BATTLE_GAGS_*"): EB_BTL_GAGS.addItem(SimpleButton(*x))
    EB_BTL_TA = ExtendableButt(*L10N.sc_fetch("SC_BATTLE_TA"))
    for x in L10N.sc_fetch("SC_BATTLE_TA_*"): EB_BTL_TA.addItem(SimpleButton(*x))
    EB_BTL_CGS = ExtendableButt(*L10N.sc_fetch("SC_BATTLE_CGS"))
    for x in L10N.sc_fetch("SC_BATTLE_CGS_*"): EB_BTL_CGS.addItem(SimpleButton(*x))
    
    EB_BTL.addItem(EB_BTL_GAGS)
    EB_BTL.addItem(EB_BTL_TA)
    EB_BTL.addItem(EB_BTL_CGS)
    
    for x in L10N.sc_fetch("SC_BATTLE_%"): EB_BTL.addItem(SimpleButton(*x))
    
    #gag shop
    EB_GSHOP = ExtendableButt(*L10N.sc_fetch("SC_GAGSHOP"))
    for x in L10N.sc_fetch("SC_GAGSHOP_*"): EB_GSHOP.addItem(SimpleButton(*x))
    
    #others
    SB_YES = SimpleButton(*L10N.sc_fetch("SC_YES")[0])
    SB_NO = SimpleButton(*L10N.sc_fetch("SC_NO")[0])
    SB_OK = SimpleButton(*L10N.sc_fetch("SC_OK")[0])
def makeSCMenu(frame):
    bake()
    itemsToAdd = [EB_EMOT,EB_JBWK and 0,EB_RACE and 0,EB_PETS,EB_HELLO,
                  EB_GOODBYE,EB_SAD,EB_FRND,EB_SORRY,EB_STINKY,
                  EB_PLACES,EB_TASK,EB_BTL,EB_GSHOP,
                  SB_YES,SB_NO,SB_OK]
    for x in itemsToAdd:
        if x: EL_ROOT.addItem(x)
    origin = frame.attachNewNode('chatOrigin')
    base.distMgr.menuGui = EL_ROOT.make(origin)
 
from direct.showbase.DirectObject import DirectObject
from string import ascii_lowercase as letters

class ClassicChatBox(DirectObject):
    def __installKeyHooks__(self,uninstall = False):
        method = lambda x: self.accept(x,self.__addNavs__,[x])
        if uninstall: method = self.ignore
        extra = self.accept(".",self.__addNavs__,["."])
        if uninstall: self.ignore(".")
        
        map(method,letters)
 
    def __sendChat__(self, message):        
        
        t = gamebase.curArea.toon
        t.b_speak(message)
 
        return True
 
    def __setNone__(self):
 
        text = self.OldChatBoxEntry['text']
        self.OldChatBoxEntry.set(text)
 
        return True
 
    def __action__(self, message):
 
        self.OldChatBoxGui.removeNode()
        self.OldChatBoxEntry.removeNode()
        self.OldChatBoxClose.removeNode()
        self.OldChatBoxBack.removeNode()
        self.OldChatBoxTalk.removeNode()
 
        self.__addOnButton__()
 
        self.__sendChat__(message)
 
        return True
 
    def __delNavs__(self):
 
        self.OldChatBoxGui.removeNode()
        self.OldChatBoxEntry.removeNode()
        self.OldChatBoxClose.removeNode()
        self.OldChatBoxBack.removeNode()
        self.OldChatBoxTalk.removeNode()
 
        self.__addOnButton__()
 
        return True
 
    def __sayIt__(self):
 
        arguments = self.OldChatBoxEntry.get(1.0)
        self.__action__(arguments)
 
        return True
 
    def __addNavs__(self,firstLetter = ""):
 
        self.__installKeyHooks__(True)
        self.OldChatBoxOpen.removeNode()
        self.OldChatBoxGui = DirectFrame(parent = self.frame, pos=((-0.18-.15)*0+.9, 0,0.918-1), scale=1, frameSize=(0,0,0,0), image=self.ChatBox.find("**/quick_talker"))
  
        self.OldChatBoxEntry = DirectEntry(text = "", 
        scale=.04, 
        parent = self.frame, 
        command=self.__action__, 
        frameSize = (-.0, 32.6, 1, -0.5), 
        frameColor=(0,0,0,0), 
        cursorKeys = 1, 
        numLines = 1, 
        width = 21, #21 is fine (15.5 = bad effect)
        focus=1, 
        text_scale=1.5, 
        initialText = firstLetter,
        pos = (.24,0,-.085))
 
        self.OldChatBoxBack = DirectButton(parent = self.frame, 
        image=(self.ChatBox.find('**/ChtBx_BackBtn_UP'), 
        self.ChatBox.find('**/ChtBx_BackBtn_DN'), 
        self.ChatBox.find('**/ChtBx_BackBtn_Rllvr')), 
        relief=None, 
        command=self.__setNone__, 
        text = ("", "Clear", "Clear", "Clear"), 
        text_pos=(0, -0.09), 
        geom=None, scale=1.1, 
        pad=(0.01, 0.01), 
        suppressKeys=0, 
        #pos = (0.525-.15,0,0.912), 
        pos = (1.607,0,-.073), 
        hpr = (0,0,0), 
        text_scale=0.05, 
        borderWidth=(0.015, 0.01))
 
        self.OldChatBoxClose = DirectButton(parent = self.frame, 
        image=(self.ChatBox.find('**/CloseBtn_UP'), 
        self.ChatBox.find('**/CloseBtn_DN'), 
        self.ChatBox.find('**/CloseBtn_Rllvr')), 
        relief=None, 
        command=self.__delNavs__, 
        text = ("", "Cancel", "Cancel", "Cancel"), 
        text_pos=(0, -0.09), 
        geom=None, 
        scale=1.1, 
        pad=(0.01, 0.01), 
        suppressKeys=0, 
        #pos = (-0.966-.15,0,0.911), 
        pos = (.115,0,-.0745),
        hpr = (0,0,0), 
        text_scale=0.05, 
        borderWidth=(0.015, 0.01))
 
        self.OldChatBoxTalk = DirectButton(frameSize=None, 
        parent = self.frame,
        image=(self.ChatBox.find('**/ChtBx_ChtBtn_UP'), 
        self.ChatBox.find('**/ChtBx_ChtBtn_DN'), 
        self.ChatBox.find('**/ChtBx_ChtBtn_RLVR')), 
        relief=None, 
        command=self.__sayIt__, 
        text = ("", "Say It", "Say It", "Say It"), 
        text_pos=(0, -0.09), 
        geom=None, 
        scale=1.1, 
        pad=(0.01, 0.01), 
        suppressKeys=0, 
        #pos = (0.62-.15,0,0.912), 
        pos = (1.7,0,-.07),
        hpr = (0,0,0), 
        text_scale=0.05, 
        borderWidth=(0.015, 0.01))
 
        return True
 
    def __addOnButton__(self):
 
        self.OldChatBoxOpen = DirectButton(parent = self.frame, 
        image=(self.ChatBox.find('**/ChtBx_ChtBtn_UP'), 
        self.ChatBox.find('**/ChtBx_ChtBtn_DN'), 
        self.ChatBox.find('**/ChtBx_ChtBtn_RLVR')), 
        command=self.__addNavs__, 
        relief=None, 
        text = "", #("", "ToonTalker", "ToonTalker", "ToonTalker"), 
        text_pos=(0, -0.09), 
        geom=None, 
        scale=1.2, 
        pad=(0.01, 0.01), 
        suppressKeys=0, 
        pos = (.1,0,0.918-1), 
        hpr = (0,0,0), 
        #color=(0,0,1,1), 
        text_scale=0.059999999999999998, 
        borderWidth=(0.015, 0.01))
        
        self.__installKeyHooks__()
 
        return True
 
    def __init__(self,frame):
        self.ChatBox = loader.loadModel("phase_3.5/models/gui/chat_input_gui.bam")
        self.frame = frame
        self.__addOnButton__()
        
    def reparentTo(self,x):
        if self.OldChatBoxOpen: self.OldChatBoxOpen.wrtReparentTo(x)
        else:
            for y in [self.OldChatBoxGui,self.OldChatBoxEntry,self.OldChatBoxBack,self.OldChatBoxClose]:
                y.wrtReparentTo(x)
                
    def removeNode(self):
        if self.OldChatBoxOpen: self.OldChatBoxOpen.removeNode()
        else:
            for y in [self.OldChatBoxGui,self.OldChatBoxEntry,self.OldChatBoxBack,self.OldChatBoxClose]:
                y.removeNode()
                
        self.__installKeyHooks__(True)
                
    def getParent(self):
        return self.frame
