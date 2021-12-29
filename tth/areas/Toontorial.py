from direct.interval.IntervalGlobal import *

from __init__ import Area
from etc import *
from hoods import TTCentral
from panda3d.core import Vec4, TextureStage, Texture, CollisionSphere, CollisionNode, BitMask32
from tth.avatar import ToonGlobals
from tth.avatar.Toon import *
from tth.base.TTHouseUtils import rgb2p
from tth.cogs.CogDNA import CogDNA
from tth.cogs.DistributedCog import DistributedCog
from tth.gui.SpeechBubble import *

class Tutorial(Area):
    cogPoints = ((-42.5, 18.5, -0.47),(-42.5, 33.9, -0.47),(-87.3, 33.9, -0.47),(-89.2, 18.5, -0.47))
    cogWalkDur = 1
    def __init__(self,tp=None):
        self.name = 'AREA_Toontorial'
        self.zoneId = 1
        self.music = "phase_3.5/audio/bgm/TC_SZ_activity.mid"

        self.avatarPN = ['wall','props']
        Area.__init__(self,"phase_3.5/models/modules/toon_interior_tutorial.bam")
        self.sky = loader.loadModel("phase_3.5/models/props/TT_sky.bam")
        self.sky.reparentTo(self.np)
        walltex = loader.loadTexture("phase_3.5/maps/stripeB5.jpg")
        tsw = TextureStage('tsw')
        tsw.setMode(TextureStage.MBlend)
        tsw.setColor(Vec4(rgb2p(175,241,150)+(1,)))
        self.environ.find("**/random_tc1_TI_wallpaper").setTexture(tsw, walltex)
        self.environ.find("**/random_tc1_TI_wallpaper_border").setTexture(tsw, walltex)

        floortex = loader.loadTexture("phase_3/maps/floor_create_toon.jpg")
        tsf = TextureStage('tsf')
        tsf.setMode(TextureStage.MBlend)
        tsf.setColor(Vec4(rgb2p(114,55,19)+(1,)))
        self.environ.find("**/random_tc1_TI_floor").setTexture(tsf, floortex, 1)
        self.environ.reparentTo(self.np)
        self.environ.setScale((1.6,1.6,1))
        #for m in self.environ.findAllMatches('**/*wall*'):m.setColorScale(Vec4(.1,1,.1,1),1)
        #for m in self.environ.findAllMatches('**/random*'):m.setColorScale(Vec4(.1,1,.1,1),1)

        tomDna = ToonDNA.ToonDNA()
        tomDna.newToonFromProperties('dll', 'ms', 'm', 'm', 7, 0, 7, 7, 2, 6, 2, 6, 2, 16)

        self.npctut = Toon()
        self.npctut.reparentTo(self.np.find("**/npc_o*"))
        self.npctut.setDNA(tomDna)
        self.npctut.setName("Tutorial Tom",1,0) #no shadow

        self.npctut.anim('neutral')
        self.npctut.tag["fg"] = (1,.5,.25,1)

        self.furniture("phase_3.5/models/modules/couch_2person.bam", "random_mo1_TI_couch_2person")
        self.furniture("phase_3.5/models/modules/couch_1person.bam", "random_mo2_TI_couch_1person")
        self.furniture("phase_3.5/models/modules/bookcase.bam", "random_mo1_TI_bookcase")
        self.furniture("phase_3.5/models/modules/bookcase_low.bam", "random_mo1_TI_bookcase_low")
        self.furniture("phase_3.5/models/modules/paper_trashcan.bam", "random_mo1_TI_paper_trashcan")
        self.furniture("phase_3.5/models/modules/chair.bam", "random_mo1_TI_chair")
        self.furniture("phase_3.5/models/modules/rug.bam", "random_mo1_TI_rug")
        self.furniture("phase_3.5/models/modules/desk_only_wo_phone.bam", "random_mo1_TI_desk_only_wo_phone")
        #self.furniture("data/models/furniture/big_planter.bam", "random_mo1_TI_big_planter") need to be fixed since before mf files x)
        self.furniture("phase_3.5/models/modules/coatrack.bam", "random_mo1_TI_coatrack")
        self.door = loader.loadModel("phase_3.5/models/modules/doors_practical.bam")
        self.door.find("**/door_skyler_ur_flat").reparentTo(self.environ.find("**/door_origin"))

        self.door.setDepthOffset(99999)
        self.door.setDepthTest(True)
        self.door.setDepthWrite(True)

        self.door.setSy(10)
        self.avatar.setPos(-5,13.1,0)
        self.avatar.setH(-4.8)

		#using new bubble
        #self.speech = SpeechBubble(self.npctut,L10N('SPEECH_TUT_COMEHERE'))
        self.speech = ToonSpeechBubble(self.npctut,L10N('SPEECH_TUT_COMEHERE'),10)
        #self.wc.addInPattern('%in-into')

        #base.accept('againcollision_walls', self.onDesk)

        self.csDesk = CollisionSphere(0,0,0,4)
        cnode = CollisionNode('desk')
        self.cnodePath = self.npctut.attachNewNode(cnode)
        self.cnodePath.node().addSolid(self.csDesk)
        cnode.setIntoCollideMask(BitMask32(8))
        cnode.setFromCollideMask(BitMask32(8))
        if -1>0 or base.isInjectorOpen: #if is debugging will show. if you remove the "-" will show.
            self.cnodePath.show()
            self.cNodepath.show()

        self.collDict = {cnode:self.onDesk}

        if base.isInjectorOpen: base.cTrav.showCollisions(render)# crash

        for x in self.hud:
            x.reparentTo(hidden)

        #load external stuff
        self.external = loader.loadModel('phase_0/streets/tutorial.bam')
        self.external.reparentTo(self.np)
        self.external.setPos(-26,46,0)
        self.external.setH(180)

        #the external cog
        self.cog = DistributedCog(base.cr)
        self.cog.zoneId = -1
        self.cog.doId = -1

        dna = '\0\0\1\0\0\0'
        want_easterEgg = 1
        if want_easterEgg:
            dna = CogDNA()
            dna.dept = 3
            dna.leader = 6
            dna.level = 11
            dna.isWaiter = 1
            dna.lives = 3
            dna = dna.make()

        self.cog.setDNA(dna)
        self.cog.setState('Walk','',0)

        base.cam.iPosHpr()
        base.cam.reparentTo(self.avatar)
        base.cam.setPos(0,-20,4.7)
        self.ignore('tab')

        if tp: tp.done()

    def onDesk(self,entry):
        if not self.canMove: return
        print "!DESK!"
        self.disableControls()

        self.cnodePath.removeNode()

        if self.speech.exists: self.speech.frame.hide()

        #using new bubble
        #Sequence(Func(lambda *a,**k:SpeechBubble(self.npctut,L10N('SPEECH_TUT_GOTOTTC'))),
        Sequence(Func(lambda *a,**k:ToonSpeechBubble(self.npctut,L10N('SPEECH_TUT_GOTOTTC'))),
                 Wait(6),Func(self._go_ttc)).start()

        #hide toon and place camera
        self.avatar.hide()
        base.cam.reparentTo(self.npctut)

        base.cam.setPos(0,20,5)
        base.cam.setH(180)

    def furniture(self, model, node):
        nmodel = loader.loadModel(model)
        nmodel.reparentTo(self.environ.find("**/"+node))

    def _go_ttc(self,*a,**k):
        self.avatar.show()
        base.cam.setPos(0, -20, 4.7)
        base.cam.setH(0)
        base.cam.reparentTo(self.avatar)
        if not base.isInjectorOpen: Teleporter(TTCentral,'AREA_TTC').go()

    def __tth_area__(self):
        return {
                'name':self.name,
                'models':self.np,
                'bgm':self.theme,
                'gui':self.frame,
                'speeches':[]
                }

    def destroy(self):
        Area.destroy(self)
        self.cog.delete()