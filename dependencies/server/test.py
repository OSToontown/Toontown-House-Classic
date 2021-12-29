#coding: latin-1
from panda3d.core import *
from direct.gui.DirectGui import *
import direct.directbase.DirectStart

VirtualFileSystem.getGlobalPtr().mount("data/phase_3.mf","",0)
      
class SpeechBubbleBase2(NodePath):
    def __init__(self, speech):
        self.speech = speech
        
        NodePath.__init__(self,'SBBase')
        
        box = loader.loadModel("phase_3/models/props/chatbox.bam")
        box.setBillboardAxis()
        box.reparentTo(self)

        if not speech: return
        
        text = TextNode('chatbox_text')
        if not isinstance(speech,unicode): speech = unicode(speech,'latin-1')
        
        text.setWtext(speech)
        text.setFont(loader.loadFont('phase_3/models/fonts/vtRemingtonPortable.ttf'))
        
        bw = map(Vec3.getX,box.getTightBounds())
        bw = abs(bw[0]-bw[1])
        
        bh = map(Vec3.getZ,box.getTightBounds())
        bh = abs(bh[0]-bh[1])
        
        text.setWordwrap(bw/.525) #35 by default
        
        textNp = box.find('**/top').attachNewNode(text)
        textNp.setColor(Vec4(0,0,0,1),1)
        textNp.setScale(.5)
        textNp.setDepthOffset(100)
       
        w = text.getWidth() / 1.75
        h = text.getHeight()
        l = text.getNumRows()
        
        textNp.wrtReparentTo(hidden)
        box.setSx(w/bw)
        
        textNp.setX(box,1)
        box.setSz((l*1.2)/bh)
        box.setZ((3-l)*1.2)
        textNp.wrtReparentTo(box.find('**/top'))
        
        self.text = text
        self.textNp = textNp
        self.box = box
        
#t = "We don't wanna this.\nLine 2 neither.\nLine 3 even less!"
t = "We don't wanna this to fall into the wrong hands."
#t = "Short!"
#t = "Two\nLines."
#t = "This text is so long that will be wordwraped!"

t = "Voc� n�o tem cacife pra falar comigo."

x = SpeechBubbleBase2(t)
x.reparentTo(aspect2d)
        
x.setScale(.1)
        
run()