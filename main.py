# -*- coding: latin-1 -*- #

from panda3d.core import *
from direct.interval.IntervalGlobal import *
from direct.showbase.DirectObject import *
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from direct.gui import DirectGuiGlobals as DGG
loadPrcFile('dependencies/etc/Config.prc')
import __builtin__, os, sys
from urllib import urlopen as ulib_uo
import direct.directbase.DirectStart
wp = WindowProperties()
wp.setFixedSize(False)
base.win.requestProperties(wp)

class Resolver:
    def __init__(self,attr):
        self.attr = attr

        self.methods = {
                        'o':self._os_environ,
                        'a':self._sys_argv,
                        }


    def resolve(self,default=None,method=None):
        if type(method) is not str:
            method = ''.join(self.methods.keys())

        for m in method:
            r = self.methods[m]()
            if r: return r

        return default

    def _sys_argv(self):
        #look in sys.argv
        #when looking into sys.argv, add "-" to the beggining
        #eg. look for 'svaddr'->'-svaddr'

        if '-'+self.attr in sys.argv:
            return sys.argv[sys.argv.index('-'+self.attr)+1]

    def _os_environ(self):
        #look in on.environ
        #when looking into os.environ, add "TTH_" to the beggining and make it uppercase
        #eg. look for 'svaddr'->'TTH_SVADDR'

        return os.environ.get("TTH_"+self.attr.upper(),None)

__builtin__.Resolver = Resolver

from tth.l10n import l10n

from tth.distributed.HouseDatagram import loads as hdg_ld, dumps as hdg_dp
__builtin__.load_buffer = hdg_ld
__builtin__.make_buffer = hdg_dp
#process key (if comp.)
def _load_buffer(buff): return pkl_ld(zlib.decompress(buff.decode('base64')))
if hasattr(__builtin__,"isCompiled"):
    if not '-k' in sys.argv:
        print 'NO KEY!'
        sys.exit()

    key = sys.argv[sys.argv.index('-k')+1]
    rs = _load_buffer(ulib_uo("https://toontownhouse.org/play/keyinfo2.py?key="+key).read())
    if "error" in rs: sys.exit('KEY_ERROR:'+str(rs['error']))
    _USER = rs['u']
    lang = rs['lang']
    __builtin__.glob = glob_copy

else:
    lang = Resolver('l').resolve('en')
    _USER = Resolver('u').resolve('test')

__builtin__.L10N = l10n(lang)

#mount the MFs
mfRoot = "./"
if not hasattr(__builtin__,"isCompiled"): mfRoot = "data/"
mfs = [mfRoot+x for x in os.listdir(mfRoot) if x.endswith(".mf")]
vfs = VirtualFileSystem.getGlobalPtr()
for mf in mfs: print "mounting",mf,vfs.mount(mf,".",VirtualFileSystem.MFReadOnly,(lambda x,y:x.decode(y))("ggu0hf3","rot13"))
getModelPath().appendDirectory("./data")

FONT = loader.loadFont('phase_3/models/fonts/ImpressBT.ttf')
GEOM = loader.loadModel('phase_3/models/gui/dialog_box_gui.bam')

DGG.setDefaultFont(FONT)
DGG.setDefaultDialogGeom(GEOM)

from tth.avatar.loader import *
from tth.lsc import *
from tth.areas.createatoon import *
from tth.datahnd.NetworkedBlobWithCR import *
from tth.datahnd.NetworkedBlob import *
from tth.datahnd.Blob import *
from tth.base import TTHouseUtils

# start list of areas import
from tth.areas.Toontorial import *
from tth.areas.area51 import *
from tth.areas.hoods import *
from tth.areas.estate import *
from tth.areas.funAreas import *
from tth.areas.coghqs import *
from tth.areas.indoors import * 
#from tth.areas.doyouthinkimcoolbecauseihaveawesomefilenamesideas import * #name written at hand !
#from tth.areas.idk import * #idk why
#end list

from tth.managers import *

import os
import sys
import math
import time
import zlib
import __builtin__

ver = '0.0.61'

print '=========================='
print 'Toontown House has started'
print 'Build Version:', ver
print '=========================='

###############################

VER_INC = True
#aint no server anyway, this is not needed atm
if 0: #Resolver('svaddr').resolve('') not in ["localhost","74.130.151.113","78.236.116.224","187.107.209.205"]: #'-fp' in sys.argv and VER_INC:#
    if not hasattr(__builtin__,'isCompiled'):
        #print('HEY! I (nacib) am making some changes to the server! It means that if you connect it will crash!')
        print("HEY! I (s0r00t or nacib) is doing nothing! It means that if you connect it will crash!")
        #print('IF YOU WANNA PLAY DO ---- NOT ---- USE -fp')
        print('exiting!')
        sys.exit()
###############################

if not hasattr(__builtin__,"isCompiled"):
    print ('Not compiled! Using standard glob...')
    import glob
    __builtin__.glob = glob

class ToontownHouseError(Exception):pass

##################################################
#implemetation of Cogtown Injector for easy debugging!
def runInjectorCode():
        global text
        exec (text.get(1.0, "end"),globals())

def openInjector():
    import Tkinter as tk
    from direct.stdpy import thread
    root = tk.Tk()
    root.geometry('600x400')
    root.title('Cogtown (TTH version) Injector')
    root.resizable(False,False)
    global text
    frame = tk.Frame(root)
    text = tk.Text(frame,width=70,height=20)

    #text.insert(1.0, "#set gags\n\ng = gamebase.toonAvatarStream.read('gags',[[-1]*7]*7)\ng[0][-1] = 0\ngamebase.toonAvatarStream.write('gags',g)\n\n#clone code > FOR DEBUGGING\nt=gamebase.toonAvatar[0]\na=gamebase.curArea\n\nx=base.cr.createDistributedObject\\\n\t(className='DistributedAvatar',zoneId=base.distMgr.get(a.zoneId))\n\nd=load_buffer(t.dna)\nd['toontype']='cat'\nx.b_setToonDna(make_buffer(d))\n\nt.b_speak('SUCCESSFULLY CLONED MYSELF LOL!')")
    #text.insert(1.0, "gamebase.toonAvatar[0].toon._m.physControls.setCollisionsActive(0)\nca = gamebase.curArea\n\nnp = ca.np\nav = ca.avatar\n\np=av.getPos()\np2=p-(18,0,0)\n\nav.posInterval(5,p,p2).start()")
    #text.insert(1.0, "for x in [base.cam,gamebase.curArea.avatar]:\n\tprint x\n\tprint '\\tPARENT:',x.getParent()\n\tprint '\\tPOS:',x.getPos()\n\tprint '\\tHPR:', x.getHpr()\n\tprint '\\tSCALE:',x.getScale(render)\n\tprint")
    #text.insert(1.0, "AREA = (AcornAcres,MiniGolfZone)[gamebase.curArea.__class__ == AcornAcres]\nprint AREA\nfakeT = hidden.attachNewNode('fakeTunnel')\nfakeT.attachNewNode(CollisionNode('tunnel_trigger'))\nt = Tunnel(fakeT,0,gamebase.curArea,(AREA,''))\nx = Teleporter(AREA,'')\nx.tunnel = t\nx.go()")
    #text.insert(1.0, "av = gamebase.curArea.avatar\n#base.lolDoor.goInto(None)\nbase.cam.reparentTo(av)\nbase.cam.setPos(0,-20,4.7)\nbase.cam.setH(0)\ngamebase.curArea.enableControls()")
    #text.insert(1.0, "from tth.cogs import Cog, CogDNA\nfor x in render.findAllMatches('**/suit*'): x.removeNode()\n\ndna = CogDNA.CogDNA()\ndna.dept = 0\ndna.leader = 7\n\ndata = dna.make()\nprint data.encode('hex')\n\nc = Cog.Cog(data)\nc.reparentTo(render)\nif 0:c.play('neutral')\n\n#gamebase.curArea.takeControlOf(c)")
    #text.insert(1.0, "from tth.cogs import Cog, CogDNA\ndna = CogDNA.CogDNA()\ndna.dept = 0\ndna.leader = 6\n\ndata = dna.make()\n\n#c.removeNode()\nc = Cog.Cog(data)\nc.reparentTo(render)\n\n#c.reload(data[:-1]+'\\1')")
    #text.insert(1.0, "lastH=0\nps=[]\nav = gamebase.curArea.av\n\ndef log():\n\th=av.getH()\n\tdh = lastH-h\n\tglobal lastH\n\tlastH=h\n\tps.append((av.getPos(),h))\n\tprint ps[-1]\n\nbase.accept('space',log)")
    #text.insert(1.0, "from tth.cogs.CogStreetWalker import *\ns = StreetWalker(gamebase.curArea.cogPoints)\n")
    #text.insert(1.0, "import random\nfrom tth.cogs.DistributedCog import *\ndcogs = []\nfor i in xrange(20):\n dc = DistributedCog(base.cr)\n dc.setDNA(CogDNA.randomDna(dept = 3))\n dc.setState('Walk','',random.random()*100)\n dcogs.append(dc)\n\ndc=random.choice(dcogs)\ndc.setState('FlyIn',repr(dc.cog.getPos())[:-1].strip('LPoint3f('),0)\nbase.cam.reparentTo(dc.cog)")
    #text.insert(1.0, "def findCog():\n\tfor id,obj in base.cr.doId2do.items():\n\t\tif obj.dclass.getName() == 'DistributedCog':\n\t\t\treturn obj\n\nx = findCog()\ns = x.fsm.walkSeq\nprint s\n\nav = gamebase.curArea.avatar\n\nbase.cam.reparentTo(x.cog)#av)")
    #text.insert(1.0, "def findCog():\n\tfor id,obj in base.cr.doId2do.items():\n\t\tif obj.dclass.getName() == 'DistributedCog':\n\t\t\treturn obj\n\nx = findCog()\nCogSpeechBubble(x.cog,'test123')")
    #text.insert(1.0, "def findPond():\n\tfor id,obj in base.cr.doId2do.items():\n\t\tif obj.dclass.getName() == 'DistributedPond':\n\t\t\treturn obj\n\nx = findPond()")
    #text.insert(1.0, "def findMg():\n\tfor id,obj in base.cr.doId2do.items():\n\t\tif obj.dclass.getName() == 'DistCannonGame':\n\t\t\treturn obj\n\nx = findMg()")
    #text.insert(1.0, "from tth.cogs.DistributedCog import *\ndc = DistributedCog(base.cr)\ndc.zoneId = gamebase.curArea.zoneId\ndc.setDNA(CogDNA.randomDna())\ndc.setState('Walk','',0)")
    #text.insert(1.0, "from tth.cogs.DistributedCog import DistributedCog\nbase.cr.createDistributedObject(className='DistributedCog',zoneId=10007000)")
    #text.insert(1.0,"x=gamebase.curArea.toon.fsm\nx.bob.setPos(0,0,0)")
    #text.insert(1.0,"from tth.fishing.Fish import Fish\nfrom tth.fishing.FishPanel import FishPanel\nf = Fish(0,0,10)\n\np = FishPanel(f)\np.setSwimBounds(-0.3, 0.3, -0.235, 0.25)\np.setSwimColor(1.0, 1.0, 0.74901, 1.0)\np.show()")
    #text.insert(1.0,"from tth.fishing.FishTank import *\nst=gamebase.toonAvatarStream\ntank=FishTank(st)\nprint tank")
    #text.insert(1.0,"from tth.fishing.FishSellGUI import *\nFishSellGUI('blah')")
    #text.insert(1.0,"from tth.distributed.HouseDatagram import *\ndg = HouseDatagram()\nobj = (3,10,'g')\npk = dg.packObject(obj)\nprint dg.unpackObject(pk)")
    #text.insert(1.0,"x = base.cr.doId2do[52]\nx.cnp.node().setCollideMask(BitMask32(16|8))\nprint x.cnp.node().getNetCollideMask()")
    #text.insert(1.0,"from tth.gui import SpeechBubble\nSpeechBubbleBase.boxScale = .7")
    #text.insert(1.0,"from tth.gui.MarginManager import MarginManager\nmm = MarginManager()")
    #text.insert(1.0,"ca = gamebase.curArea\nav = ca.avatar\nav.reparentTo(ca.np.find('**/npc*fish*or*'))\nav.iPosHpr()\nprint ca.toon.zoneId, av.getPos(render), av.getH(render)")
    #text.insert(1.0,"from tth.misc.RainManager import *\nrm = DistributedRainMgr(base.cr)\nrm.generate()\nrm.enterRain(0)")
    #text.insert(1.0,"from tth.misc.EQManager import *\nrm = DistributedEQMgr(base.cr)\nrm.generate()\nrm.enterShake(0)")
    #text.insert(1.0,"from tth.areas.etc import *\nx = TeleportCircle.performClose(0)")
    #text.insert(1.0,"print {x:y for x,y in base.cr.doId2do.items() if x>10**6}.values()[0]")
    #text.insert(1.0,"gamebase.curArea.toon.b_toonUp(100)")
    #text.insert(1.0,"from tth.fishing.FishTank import *\ngamebase.toonAvatarStream.write('fishHistory',{})\ntank=makeLocalTank()\nfor i in xrange(13):\n\ttank.addFish(Fish(i,0,30))\n\nprint tank")
    #text.insert(1.0,"from tth.fishing import *\nfish=FishingGlobals.getRandomFish(5000,0)\nw = FishingGlobals.getRandomWeight(*fish[1]+(0,))\nprint Fish.Fish(*fish[1]+(w,))")
    #text.insert(1.0,"from tth.distributed.NametagArrows import *\nna = NametagArrows()\n#t = na.collected.values()[0].tagModel\n")
    text.insert(1.0, "print(gamebase.curArea.avatar.getPos())\nprint(gamebase.curArea.avatar.getHpr())")

    text.pack(side="left")
    tk.Button(root,text="Inject!",command=runInjectorCode).pack()
    scroll = tk.Scrollbar(frame)
    scroll.pack(fill="y",side="right")
    scroll.config(command=text.yview)
    text.config(yscrollcommand=scroll.set)
    frame.pack(fill="y")

    thread.start_new_thread(root.mainloop,())


##################################################

if '--debug' in sys.argv or '-d' in sys.argv:
    print 'debug argv detected'
    if not '-nd' in sys.argv: loadPrcFileData("", "want-directtools #t")
    if '-tk' in sys.argv: loadPrcFileData("", "want-tk #t")
    if not '--noinj' in sys.argv and not '-ni' in sys.argv:openInjector()

if '--no-audio' in sys.argv or '-na' in sys.argv:
    print 'FINE! NO SOUND THEN >:C' #-_- + not working
    loadPrcFileData("", "audio-library-name null")

if '-nf' in sys.argv:
    level = sys.argv[sys.argv.index('-nf')+1]

    loadPrcFileData("", "notify-level "+level)

    annoying = ["gobj","util","audio","gsg","event","express"]
    for x in annoying: loadPrcFileData("", "notify-level-"+x+" warning")

import direct.directbase.DirectStart

base.isInjectorOpen = '--debug' in sys.argv #or '-d' in sys.argv
base.isCompiled = hasattr(__builtin__,"isCompiled")

from tth.distributed.ToontownHouseClientRepository import ToontownHouseClientRepository
base.cr = ToontownHouseClientRepository()

from panda3d.physics import PhysicsManager
base.physicsMgr = PhysicsManager() #used by fishing bubbles
base.enableParticles()

base.frdMgr = FriendshipManager()
base.distMgr = DistrictManager()
base.distMgr.district = int(sys.argv[sys.argv.index('-fd')+1]) if ('-fd' in sys.argv) else base.distMgr.district
base.chatMgr = ChatManager()
base.codeRedemptionMgr = CDRManager()
base.hoodMgr = HoodManager()

base.cTrav = CollisionTraverser('baseTraveser')

from tth.gui.MarginManager import MarginManager
base.marginMgr = MarginManager()

class GameBase(DirectObject):
    def __init__(self):
        base.disableMouse()

        if base.appRunner: self.dir = base.appRunner.multifileRoot
        elif hasattr(__builtin__,'isCompiled'):
            self.dir = '' #use absolute paths relative to mf root
            self.isCompiled = True
        else: self.dir = os.path.abspath(os.curdir)

        print self.dir

        sys.path.append(self.dir)

        self.accept("load-chooseatoon-screen",self.loadChooseAToonScr)
        self.accept("init-createatoon",self.enterCreateAToon)
        self.accept("end-createatoon",lambda:self.toonChosen(self.toonId))
        self.accept("playMinigame",self.playMG)
        self.accept("f9",self.screenshot)

        self.curArea = None

        self.sounds = {}

        exts = ('mp3','wav','ogg')
        for x in (3,3.5,5,0):
            for ext in exts:
                for s in TTHouseUtils.globVFS("phase_"+str(x)+"/audio/sfx/GUI_*."+ext,"phase_"+str(x)+"/audio/sfx"):
                    sf = s.split('/')[-1].split('.')[0]
                    self.sounds[sf] = loader.loadSfx(s)
        DGG.setDefaultRolloverSound(self.sounds['GUI_rollover'])
        DGG.setDefaultClickSound(self.sounds['GUI_click'])

        self.pickerNode = CollisionNode('mouseRay')
        self.pickerNP = camera.attachNewNode(self.pickerNode)
        self.pickerNode.setIntoCollideMask(BitMask32.allOff())
        self.pickerNode.setFromCollideMask(BitMask32(16))
        self.pickerRay = CollisionRay()
        self.pickerNode.addSolid(self.pickerRay)

        self.handler = CollisionHandlerQueue()

        self.clickTrav = CollisionTraverser('clickTrav')
        self.clickTrav.addCollider(self.pickerNP, self.handler)

        self.clickDict = {}
        self.clickDictR = {}
        self.accept('mouse1',self._click,[0])
        self.accept('mouse3',self._click,[1])

    def _click(self,button):
        #print 'click with button',button

        if not base.mouseWatcherNode.hasMouse(): return
        mpos = base.mouseWatcherNode.getMouse()
        self.pickerRay.setFromLens(base.camNode, mpos.getX(), mpos.getY())

        self.clickTrav.traverse(render)

        entriesNumb = self.handler.getNumEntries()
        #print entriesNumb

        di = (self.clickDict,self.clickDictR)[button]
        if entriesNumb > 0:
            self.handler.sortEntries()
            for i in xrange(min(1,entriesNumb)): #only one
                e = self.handler.getEntry(i)
                node = e.getIntoNodePath()
                print i, node
                if node in di:
                    di[node](e)

    def screenshot(self):
        if not os.path.exists(TTHouseGlobals.ScreenShotDirectory):
            os.mkdirs(TTHouseGlobals.ScreenShotDirectory)
        base.win.saveScreenshot(
            '%s/tth-screenshot_%d.jpg' % (
            TTHouseGlobals.ScreenShotDirectory, time.time())
        )

    def findpath(self,path):
        #returns path relative to main.py dir
        p = os.path.join(self.dir,path)
        #if self.isCompiled: p = p.replace('/','\\')
        return p

    def loadChooseAToonScr(self):
        if base.config.GetBool('want-new-pat', False):
            from tth.lsc import PickAToon
            self.chooseAtoonScr = PickAToon.PickAToon()
        else:
            self.chooseAtoonScr = ChooseAToonScreen()
        if '-fast' in sys.argv:
            try:
                v = sys.argv[sys.argv.index('-fast')+1]
                self.toonChosen(int(v))
            except Exception as e:
                print 'FastMode: couldn\'t load toon!',e

    def toonChosen(self,toonId):
        print 'Toon chosen:',toonId
        self.themeMusic.stop()
        self.chooseAtoonScr.dismiss()
        self.toonId = toonId
        self.toonAvatar = loadToonAvatar(toonId)

        if not self.toonAvatar[0]: return #entered create a toon

        self.toonAvatarStream = AvatarStream(self.toonId)

        #load last area
        messenger.send('loadToon')

        def evalArea(a):
            return eval(a.replace('tth.areas.',''))

        if "-51" in sys.argv: #28/02/2014 AREA 51 WONT WORK !!!
            print "It looks like somebody want to know what's inside the Area 51 ! Let's torture him..." #lol
            tp = Teleporter(Area51,"AREA_51") #btw, there was a L10N glich here, quite funny... :D
        elif "-fa" in sys.argv:
            print "Forcing an area..."
            tp = Teleporter(evalArea(sys.argv[sys.argv.index('-fa')+1]),'')
        #28/02/2014 s0r00t's level editor was completely removed (please don't remove this comment)
        else:
            print 'Loaded (LA):',self.toonAvatar[2],self.toonAvatar[3]
            tp = Teleporter(evalArea(self.toonAvatar[2]),self.toonAvatar[3])

        tp.wantCircle = (0,1)
        tp.go()

    def enterCreateAToon(self):
        Teleporter(CreateAToon,"MAT",[self.toonId]).go()

    def playMG(self,zoneid,gid):
        from tth.minigame.MinigameGenerator import games
        _,zone,name = games[gid]
        tp = Teleporter(zone,name)
        tp.zoneId = zoneid
        tp.origin = gamebase.curArea
        tp.go()

props = WindowProperties()
props.setTitle('Toontown House [{0}]'.format(lang.upper()))
props.setCursorFilename("toonmono.cur")
base.win.requestProperties(props)

gamebase = GameBase()

__builtin__.gamebase = gamebase
__builtin__.ToontownHouseError = ToontownHouseError

def __deprecatedBuiltinBubble(*a,**kw):
    raise ToontownHouseError("Using deprecated builtin bubble!!")

__builtin__.SpeechBubble = __deprecatedBuiltinBubble

__builtin__.BTFont = loader.loadFont('phase_3/models/fonts/ImpressBT.ttf')

base.user = _USER

_server = Resolver('svaddr').resolve('gameserver-lv.toontownhouse.org')
print _server,__import__('socket').gethostbyname(_server)

if not '--nonet' in sys.argv:
    if '-udb' in sys.argv: __builtin__.globalBlob = NetworkedBlobWithCR(base.cr,_USER) #Connect to data server
    else: __builtin__.globalBlob = NetworkedBlob(_server,36911,_USER) #Connect to data server

else: __builtin__.globalBlob = Blob('userdata.blob') #local blob

def _print(*args): print args
__builtin__._print = _print

gamebase.ldScr = LoadingScreen()
run()
