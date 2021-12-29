from direct.distributed.DistributedObjectAI import DistributedObjectAI
from pandac.PandaModules import *

from random import choice,random

class AIAsync(DistributedObjectAI):

    def __init__(self, cr):
        DistributedObjectAI.__init__(self, cr)

    def sendAdminMsg(self, msg):
        #show it
        print 'MSG!',msg
        text = TextNode('adminMsgTextNode')
        text.setWtext(u'Admin:'+unicode(msg.decode('latin-1')))
        text.setWordwrap(1/.07)
        text.setAlign(TextNode.ALeft)
        text.setCardColor(1, 0, 0, .75)
        text.setCardAsMargin(.2, .2, .2, .2)
        text.setCardDecal(True)
        textNp = aspect2d.attachNewNode(text)
        textNp.setScale(0.07)
        textNp.setColor(Vec4(0,0,0,1))
        x = choice([-1.2,.3])
        z = (min(.8,random()+.1)*2)-1
        textNp.setPos(x,1,z)
        
        gamebase.sounds['GUI_whisper'].play()
        
        taskMgr.doMethodLater(5,lambda *a: textNp.removeNode(),'rmvText')
        
    def sendSpecialMsg(self, msg):
        pass #not implemented yet
        
        