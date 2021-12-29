from pandac.PandaModules import *
from direct.gui.DirectGui import *
from direct.interval.IntervalGlobal import SoundInterval
from panda3d.core import *

from tth.managers import MGR_SFX_speech as MSs

class ChatBalloon(NodePath):
    TEXT_SHIFT = (0.1, -0.05, 1.1)
    TEXT_SHIFT_PROP = 0.08
    NATIVE_WIDTH = 10.0
    MIN_WIDTH = 2.5
    BUBBLE_PADDING = 0.3
    BUBBLE_PADDING_PROP = 0.05

    def __init__(self, model,text, font=None, textColor=(0,0,0,1), balloonColor=(1,1,1,1),
                 wordWrap = 10.0):
        NodePath.__init__(self,'SBBase')
        
        self.model = loader.loadModel("phase_3/models/props/%s.bam" %model)

        root = NodePath('balloon')
        root.setBillboardPointWorld()
        root.reparentTo(self)
        root.setScale(.255)

        # Add balloon geometry:
        balloon = self.model.copyTo(root)
        top = balloon.find('**/top')
        middle = balloon.find('**/middle')
        bottom = balloon.find('**/bottom')

        balloon.setColor(balloonColor)
        if balloonColor[3] < 1.0:
            balloon.setTransparency(1)

        # Render the text into a TextNode, using the font:
        t = root.attachNewNode(TextNode('text'))
        if not font: font = loader.loadFont("phase_3/models/fonts/ImpressBT.ttf") 
        if not isinstance(text,unicode): text = unicode(text,'latin-1')
        t.node().setFont(font)
        t.node().setWordwrap(wordWrap)
        t.node().setWtext(text)
        t.node().setTextColor(textColor)

        width, height = t.node().getWidth(), t.node().getHeight()

        # Turn off depth write for the text: The place in the depth buffer is
        # held by the chat bubble anyway, and the text renders after the bubble
        # so there's no risk of the bubble overwriting the text's pixels.
        t.setAttrib(DepthWriteAttrib.make(0))
        t.setPos(self.TEXT_SHIFT)
        t.setX(t, self.TEXT_SHIFT_PROP*width)
        t.setZ(t, height)

        if width < self.MIN_WIDTH:
            width = self.MIN_WIDTH
            t.setX(t, width/2.0)
            t.node().setAlign(TextNode.ACenter)

        # Set the balloon's size:
        width *= 1+self.BUBBLE_PADDING_PROP
        width += self.BUBBLE_PADDING
        balloon.setSx(width/self.NATIVE_WIDTH)
        middle.setSz(height)
        top.setZ(top, height-1)
		
        self.text = t.node()
        self.box = root
        return root

class ToonSpeechBubble(ChatBalloon):
    def __init__(self, toon, speech, time = 6):
        self.toon = toon
        self.time = time
        
        self.tag = toon.tag
        if self.tag:
            self.tag.hide()
            
        model = "chatbox"
        isThought = 0
        if speech.startswith("."):
           speech = speech[1:]
           model = "chatbox_thought_cutout"
           isThought = 1
           
        ChatBalloon.__init__(self,model,speech,textColor=(0,0,0,1), balloonColor=(1,1,1,1),wordWrap = 10.0)

        self.reparentTo(self.toon)
        self.box.setZ(self.tag.getZ(self.toon))
                            
        self.exists = True
        spc = self.toon.style.getAnimal()
        if spc and not isThought:
            SoundInterval(MSs(spc,speech), node = self, volume = 3).start()

        self.frame = self.box
        if not isThought:
            taskMgr.doMethodLater(time,self._destroyTask, 'destroyTask')
        
    def _destroyTask(self,task):
        self.frame.hide()
        self.frame.removeNode()
        self.exists = False
        if self.tag: self.tag.show()
        return task.done
        
    def destroy(self):
        self.frame.hide()
        if self.tag: self.tag.show()
        self.tag = None
        self.exists = False
        
class NPCSpeechBubble(ToonSpeechBubble): pass

class CogSpeechBubble(ChatBalloon):
    def __init__(self, cog, speech, time = 6):
        self.cog = cog
        self.time = time
        
        self.tag = cog.nameTag
        if self.tag: self.tag.hide()
        
        ChatBalloon.__init__(self,"chatbox",speech,font=loader.loadFont('phase_3/models/fonts/vtRemingtonPortable.ttf'))
        
        self.reparentTo(self.cog)
        self.box.setZ(self,self.tag.getZ(self.cog))
                            
        self.exists = True

        self.frame = self.box
        taskMgr.doMethodLater(time,self._destroyTask, 'destroyTask')
        
    def _destroyTask(self,task):
        self.frame.hide()
        self.frame.removeNode()
        self.exists = False
        if self.tag: self.tag.show()
        return task.done
        
    def destroy(self):
        self.frame.hide()
        if self.tag: self.tag.show()
        self.tag = None
        self.exists = False

