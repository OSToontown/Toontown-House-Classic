from direct.distributed.DistributedSmoothNode import DistributedSmoothNode
from direct.distributed.ClockDelta import globalClockDelta
from direct.controls.GravityWalker import GravityWalker
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import *
from direct.actor.Actor import Actor
from pandac.PandaModules import *
from tth.avatar.Toon import *
from tth.avatar.ToonAvatarPanel import ToonAvatarPanel as TAP

from tth.gui import SpeechBubble

from AvatarFSM import AvatarFSM

class DistributedAvatar(DistributedSmoothNode):
    def __init__(self, cr):
        DistributedSmoothNode.__init__(self, cr)
        NodePath.__init__(self, 'avatar')

        self.sb = None

        self.toon = Toon()
        self.dna = make_buffer({"name":'placeHolder',"dna":'\0'*15,"toonId":0})
        self._state = ("Neutral","None",0)

        self.isLocalToon = False

    def setState(self,state,arg,ts):
        ts = globalClock.getFrameTime() - globalClockDelta.networkToLocalTime(ts,bits=32)
        ts = max(ts,-ts)
        self._state = (state,arg,ts)
        self.fsm.request(state,arg,ts)

    def d_setState(self,state,arg,ts):
        self.sendUpdate("setState",[state,arg,ts])

    def b_setState(self,state,arg="None",ts = None):
        if ts is None: ts = globalClock.getFrameTime()
        ts = globalClockDelta.localToNetworkTime(ts,bits=32)

        self.setState(state,arg,ts)
        self.d_setState(state,arg,ts)

    def getState(self):
        return self._state

    def loadByDNA(self):
        data = load_buffer(self.dna)

        try:
            self.toon.physControls.deleteCollisions()
            self.toon.physControls.disableAvatarControls()

        except:
            pass

        self.toon.cleanup()
        self.toon.removeNode()
        self.toon = Toon()
        self.toon.setDNAString(data['dna'])
        self.toon.setName(data['name'])
        self.toon.reparentTo(self)

        if self.isLocalToon:
            wc = GravityWalker(legacyLifter=True)
            wc.setWallBitMask(BitMask32(1))
            wc.setFloorBitMask(BitMask32(2))
            wc.setWalkSpeed(15,24,10,60) #someone put (20,10,20,60) but its too fast and jump got wierd
            wc.initializeCollisions(base.cTrav, self.toon, floorOffset=0.025, reach=4.0)
            wc.enableAvatarControls()
            self.toon.physControls = wc
            self.toon.physControls.placeOnFloor()

        else:
            cn = CollisionNode(self.getName()+'-cnode')
            cs = CollisionSphere(0,0,0,1)
            cn.addSolid(cs)
            cn.setCollideMask(BitMask32(16)|BitMask32(1))

            self.cnp = self.attachNewNode(cn)
            self.cnp.setZ(3)
            self.cnp.setSz(3)

            gamebase.clickDict[self.cnp] = self.__click
            #self.cnp.show()

    def __click(self,e):
        id = load_buffer(self.dna).get('toonId',None)
        if id:
            self.tap = TAP(int(id),self.doId,load_buffer(self.dna))

    def setToonDna(self,data):
        self.dna = data
        self.loadByDNA()

        self.toon.reparentTo(self)
        self.toon.show()

    def d_setToonDna(self,data):
        self.sendUpdate('setToonDna',[data])

    def b_setToonDna(self,data):
        self.setToonDna(data)
        self.d_setToonDna(data)

    def getToonDna(self):
        return self.dna

    def speak(self,speech):
        if self.sb and self.sb.exists: self.sb.destroy()
        self.sb = SpeechBubble.ToonSpeechBubble(self.toon, base.chatMgr.parse(speech))

    def d_speak(self,speech): self.sendUpdate("speak",[speech])

    def b_speak(self,speech):
        #speech = str(speech)
        speech = speech.encode('latin-1') #'base64')
        self.speak(speech)
        self.d_speak(speech)

    def setToonDna(self,data):
        self.dna = data
        self.loadByDNA()

    def generate(self):
        DistributedSmoothNode.generate(self)
        self.activateSmoothing(True, False)
        self.startSmooth()

        self.fsm = AvatarFSM()
        self.fsm.setToon(self)

        self.setName("toon_"+str(self.doId))
        self.reparentTo(render)

    def disable(self):
        self.stopSmooth()
        self.stopPosHprBroadcast()
        self.detachNode()
        DistributedSmoothNode.disable(self)

    def delete(self):
        try:
            self.cnp.removeNode()
            del gamebase.clickDict[self.cnp]
            self.tap.removeNode()
            self.toon.physControls.disableAvatarControls()
        except: pass
        self.toon.removeNode()
        DistributedSmoothNode.delete(self)

    def toonUp(self, hp, showText = 1):
        if self.isLocalToon:
            messenger.send('laffChangedUC',[hp])

        if showText:
            red = Vec4(.9,0,0,1)
            green = Vec4(0,.9,0,1)

            _text = str(hp)
            _color = red
            if hp > 0:
                _text = '+'+_text
                _color = green

            _colorNA = Vec4(*tuple(_color)[:-1]+(0,))

            hpText = OnscreenText(text = _text, fg = _color, parent = self.toon, font = loader.loadFont('phase_3/models/fonts/MickeyFont.bam'))
            hpText.setScale(1.25)
            hpText.setBillboardPointEye()

            iv = Sequence(
                          hpText.posInterval(.5,(0,0,6),(0,0,3),blendType='easeOut'),
                          Wait(.3),
                          LerpColorInterval(hpText, .1, _color, _colorNA),
                          Func(hpText.removeNode)
                          )
            iv.start()

            return hpText

    def d_toonUp(self, hp, showText=1):
        self.sendUpdate('toonUp',[hp,showText])

    def b_toonUp(self, hp, showText=1):
        self.d_toonUp(hp, showText)
        self.toonUp(hp, showText)