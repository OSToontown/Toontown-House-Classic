from pandac.PandaModules import *
from direct.gui.DirectGui import *

from tth.book.DisguisePage import getCogName,SUIT_FONT,suitDeptFullnames

class CogAvatarPanel:
    def __init__(self, avatar):
        gui = loader.loadModel('phase_3.5/models/gui/suit_detail_panel')
        self.frame = DirectFrame(geom=gui.find('**/avatar_panel'), geom_scale=0.21, geom_pos=(0, 0, 0.02), relief=None, pos=(1.1, 100, .525))
        self.frame.wrtReparentTo(gamebase.curArea.hud[4])
        disabledImageColor = Vec4(1, 1, 1, 0.4)
        text0Color = Vec4(1, 1, 1, 1)
        text1Color = Vec4(0.5, 1, 0.5, 1)
        text2Color = Vec4(1, 1, 0.5, 1)
        text3Color = Vec4(1, 1, 1, 0.2)
        self.head = self.frame.attachNewNode('head')
        
        copyPart = avatar.find('**/cogHead*').copyTo(self.head)
        copyPart.setDepthTest(1)
        copyPart.setDepthWrite(1)

        p1 = Point3()
        p2 = Point3()
        self.head.calcTightBounds(p1, p2)
        d = p2 - p1
        biggest = max(d[0], d[1], d[2])
        s = 0.3 / biggest
        self.head.setPosHprScale(0, 0, 0, 180, 0, 0, s, s, s)
        
        avName = getCogName(avatar.dna.dept*8+avatar.dna.leader)
        if avatar.dna.isSkel: avName = L10N('COG_SKEL')
        
        self.nameLabel = DirectLabel(parent=self.frame, pos=(0.0125, 0, 0.36), relief=None, text=avName, text_font=SUIT_FONT, text_fg=Vec4(0, 0, 0, 1), text_pos=(0, 0), text_scale=0.047, text_wordwrap=7.5, text_shadow=(1, 1, 1, 1))
        level = avatar.dna.level
        
        dept = suitDeptFullnames[('c','l','m','s')[avatar.dna.dept]]
        self.levelLabel = DirectLabel(parent=self.frame, pos=(0, 0, -0.1), relief=None, text=L10N('BOOK_DISGUISE_LEVEL') % level, text_font=SUIT_FONT, text_align=TextNode.ACenter, text_fg=Vec4(0, 0, 0, 1), text_pos=(0, 0), text_scale=0.05, text_wordwrap=8.0)
        corpIcon = avatar.corpMedallion.copyTo(hidden)
        corpIcon.iPosHprScale()
        self.corpIcon = DirectLabel(parent=self.frame, geom=corpIcon, geom_scale=0.13, pos=(0, 0, -0.175), relief=None)
        corpIcon.removeNode()
        self.deptLabel = DirectLabel(parent=self.frame, pos=(0, 0, -0.28), relief=None, text=dept, text_font=SUIT_FONT, text_align=TextNode.ACenter, text_fg=Vec4(0, 0, 0, 1), text_pos=(0, 0), text_scale=0.05, text_wordwrap=8.0)
        self.closeButton = DirectButton(parent=self.frame, relief=None, pos=(0.0, 0, -0.36), text="Close", text_font=SUIT_FONT, text0_fg=Vec4(0, 0, 0, 1), text1_fg=Vec4(0.5, 0, 0, 1), text2_fg=Vec4(1, 0, 0, 1), text_pos=(0, 0), text_scale=0.05, command=self.cleanup)
        gui.removeNode()
        menuX = -0.05
        menuScale = 0.064
        gamebase.curArea.hud[4].obscure(1)
        self.frame.show()

    def cleanup(self):
        if self.frame == None:
            return
        self.frame.destroy()
        del self.frame
        self.frame = None
        self.head.removeNode()
        del self.head
        gamebase.curArea.hud[4].obscure(0)
