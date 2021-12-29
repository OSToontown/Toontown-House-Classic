import direct.directbase.DirectStart
from direct.actor.Actor import Actor
from direct.showbase.DirectObject import DirectObject
from panda3d.core import *
from pandac.PandaModules import *
from direct.interval.IntervalGlobal import *
import random
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import CollisionTraverser,CollisionNode
from panda3d.core import CollisionHandlerQueue,CollisionRay
from panda3d.core import PandaNode,NodePath,Camera,TextNode
from panda3d.core import Vec3,Vec4,BitMask32
import random, sys, os, math
from direct.gui.DirectGui import *

def runInjectorCode():
        global text
        exec (text.get(1.0, "end"),globals())
    
def openInjector():
    import Tkinter as tk
    from direct.stdpy import thread
    root = tk.Tk()
    root.geometry('600x400')
    root.title('Injector')
    root.resizable(False,False)
    global text
    frame = tk.Frame(root)
    text = tk.Text(frame,width=70,height=20)
    #text.insert(1.0, "")
    text.pack(side="left")
    tk.Button(root,text="Inject!",command=runInjectorCode).pack()
    scroll = tk.Scrollbar(frame)
    scroll.pack(fill="y",side="right")
    scroll.config(command=text.yview)
    text.config(yscrollcommand=scroll.set)
    frame.pack(fill="y")
    
    thread.start_new_thread(root.mainloop,())
    

##################################################


openInjector()

class NuttyRiver: #dafuq?
    def __init__(self):
        self.theme = loader.loadMusic("data/sounds/TC_SZ.mp3")
        self.theme.setLoop(1)
        self.theme.setPlayRate(.4)
        self.theme.play()

        self.sky = loader.loadModel("data/models/PDD/AA/sky.bam")
        self.sky.reparentTo(render)
        self.sky.setSy(1.2)

        self.lake = loader.loadModel("data/models/PDD/AA/golf_outdoor_zone.bam").find("**/water1")
        self.lake.reparentTo(render)

        self.gou = loader.loadModel("data/models/PDD/AA/golf_outdoor_zone.bam").find("**/petri_dishes")
        self.gou.reparentTo(render)

        
        #Street
        for i in range(2):
          self.street = loader.loadModel("data/models/streets/street_enhanced_DG.bam").find("**/DG_street_w_grass_60x40")
          self.street.reparentTo(render)
          self.street.setPos(0,i*40,0)
          self.street.find("**/street_w_grass_60x40_sidewalk").setTexture(loader.loadTexture("data/models/streets/maps/grassOZ.jpg"),1)
          self.street.find("**/street_w_grass_60x40_curb").setTexture(loader.loadTexture("data/models/streets/maps/grassOZ.jpg"),1)
          self.street.find("**/street_w_grass_60x40_grass").setTexture(loader.loadTexture("data/models/streets/maps/grassOZ.jpg"),1)
          self.street.find("**/street_w_grass_60x40_street").setTexture(loader.loadTexture("data/models/streets/maps/dustroad.jpg"),1)
        self.curve = loader.loadModel("data/models/streets/street_enhanced_DG.bam").find("**/DG_exterior_wholecorner_w_grass")
        self.curve.reparentTo(render)
        self.curve.setPos(0,70,0)
        self.curve.find("**/exterior_wholecorner_w_grass_sidewalk").setTexture(loader.loadTexture("data/models/streets/maps/grassOZ.jpg"),1)
        self.curve.find("**/exterior_wholecorner_w_grass_curb").setTexture(loader.loadTexture("data/models/streets/maps/grassOZ.jpg"),1)
        self.curve.find("**/exterior_wholecorner_w_grass_grass").setTexture(loader.loadTexture("data/models/streets/maps/grassOZ.jpg"),1)
        self.curve.find("**/exterior_wholecorner_w_grass_street").setTexture(loader.loadTexture("data/models/streets/maps/dustroad.jpg"),1)
        self.curve1 = loader.loadModel("data/models/streets/street_enhanced_DG.bam").find("**/DG_exterior_wholecorner_w_grass")
        self.curve1.reparentTo(render)
        self.curve1.setPos(60,110,0)
        self.curve1.setHpr(180,0,0)
        self.curve1.find("**/exterior_wholecorner_w_grass_sidewalk").setTexture(loader.loadTexture("data/models/streets/maps/grassOZ.jpg"),1)
        self.curve1.find("**/exterior_wholecorner_w_grass_curb").setTexture(loader.loadTexture("data/models/streets/maps/grassOZ.jpg"),1)
        self.curve1.find("**/exterior_wholecorner_w_grass_grass").setTexture(loader.loadTexture("data/models/streets/maps/grassOZ.jpg"),1)
        self.curve1.find("**/exterior_wholecorner_w_grass_street").setTexture(loader.loadTexture("data/models/streets/maps/dustroad.jpg"),1)
        self.prep = loader.loadModel("data/models/streets/street_enhanced_DG.bam").find("**/DG_street_slope_30x40")
        self.prep.reparentTo(render)
        self.prep.setPos(60,140,0)
        self.prep.setHpr(180,0,0)
        self.prep.find("**/street_slope_30x40_sidewalk").setTexture(loader.loadTexture("data/models/streets/maps/grassOZ.jpg"),1)
        self.prep.find("**/street_slope_30x40_curb").setTexture(loader.loadTexture("data/models/streets/maps/grassOZ.jpg"),1)
        self.prep.find("**/street_slope_30x40_grass").setTexture(loader.loadTexture("data/models/streets/maps/grassOZ.jpg"),1)
        self.prep.find("**/street_slope_30x40_street").setTexture(loader.loadTexture("data/models/streets/maps/dustroad.jpg"),1)
        self.prep1 = loader.loadModel("data/models/streets/street_enhanced_DG.bam").find("**/DG_street_slope_30x40")
        self.prep1.reparentTo(render)
        self.prep1.setPos(60,140,0)
        self.prep1.find("**/street_slope_30x40_sidewalk").setTexture(loader.loadTexture("data/models/streets/maps/grassOZ.jpg"),1)
        self.prep1.find("**/street_slope_30x40_curb").setTexture(loader.loadTexture("data/models/streets/maps/grassOZ.jpg"),1)
        self.prep1.find("**/street_slope_30x40_grass").setTexture(loader.loadTexture("data/models/streets/maps/grassOZ.jpg"),1)
        self.prep1.find("**/street_slope_30x40_street").setTexture(loader.loadTexture("data/models/streets/maps/dustroad.jpg"),1)


        for i in range(6):
          self.wood = loader.loadModel("data/models/streets/wood_fence.bam")
          self.wood.reparentTo(render)
          self.wood.setPos(30,i*10,0)
          self.wood.setHpr(90,0,0)
        for i in range(3):
          self.wood = loader.loadModel("data/models/streets/wood_fence.bam")
          self.wood.reparentTo(render)
          self.wood.setPos(30,i*-10,0)
          self.wood.setHpr(90,0,0)
        for i in range(12):
          self.wood = loader.loadModel("data/models/streets/wood_fence.bam")
          self.wood.reparentTo(render)
          self.wood.setPos(-30,i*10,0)
          self.wood.setHpr(90,0,0)
        for i in range(3):
          self.wood = loader.loadModel("data/models/streets/wood_fence.bam")
          self.wood.reparentTo(render)
          self.wood.setPos(-30,i*-10,0)
          self.wood.setHpr(90,0,0)
        for i in range(4):
          self.wood = loader.loadModel("data/models/streets/wood_fence.bam")
          self.wood.reparentTo(render)
          self.wood.setPos(i*10,120,0)
        for i in range(4):
          self.wood = loader.loadModel("data/models/streets/wood_fence.bam")
          self.wood.reparentTo(render)
          self.wood.setPos(i*-10,120,0)

        self.wood = loader.loadModel("data/models/streets/wood_fence.bam")
        self.wood.reparentTo(render)
        self.wood.setPos(30,60,0)
        self.wood = loader.loadModel("data/models/streets/wood_fence.bam")
        self.wood.reparentTo(render)
        self.wood.setPos(40,60,0)
        self.wood = loader.loadModel("data/models/streets/wood_fence.bam")
        self.wood.reparentTo(render)
        self.wood.setPos(50,60,0)
        self.wood = loader.loadModel("data/models/streets/wood_fence.bam")
        self.wood.reparentTo(render)
        self.wood.setPos(60,60,0)
        self.wood = loader.loadModel("data/models/streets/wood_fence.bam")
        self.wood.reparentTo(render)
        self.wood.setPos(70,60,0)
        self.wood = loader.loadModel("data/models/streets/wood_fence.bam")
        self.wood.reparentTo(render)
        self.wood.setPos(80,60,0)

        self.wood = loader.loadModel("data/models/streets/wood_fence.bam")
        self.wood.reparentTo(render)
        self.wood.setPos(90,60,0)
        self.wood.setHpr(90,0,0)
        self.wood = loader.loadModel("data/models/streets/wood_fence.bam")
        self.wood.reparentTo(render)
        self.wood.setPos(90,70,0)
        self.wood.setHpr(90,0,0)
        self.wood = loader.loadModel("data/models/streets/wood_fence.bam")
        self.wood.reparentTo(render)
        self.wood.setPos(90,80,0)
        self.wood.setHpr(90,0,0)
        self.wood = loader.loadModel("data/models/streets/wood_fence.bam")
        self.wood.reparentTo(render)
        self.wood.setPos(90,90,0)
        self.wood.setHpr(90,0,0)
        self.wood = loader.loadModel("data/models/streets/wood_fence.bam")
        self.wood.reparentTo(render)
        self.wood.setPos(90,100,0)
        self.wood.setHpr(90,0,0)
        self.wood = loader.loadModel("data/models/streets/wood_fence.bam")
        self.wood.reparentTo(render)
        self.wood.setPos(90,110,0)
        self.wood.setHpr(90,0,0)

        self.wood = loader.loadModel("data/models/streets/wood_fence.bam")
        self.wood.reparentTo(render)
        self.wood.setPos(80,120,0)

        self.wood = loader.loadModel("data/models/streets/wood_fence.bam")
        self.wood.reparentTo(render)
        self.wood.setPos(90,120,4)
        self.wood.setHpr(90,0,0)
        self.wood = loader.loadModel("data/models/streets/wood_fence.bam")
        self.wood.reparentTo(render)
        self.wood.setPos(90,130,4)
        self.wood.setHpr(90,0,0)
        self.wood = loader.loadModel("data/models/streets/wood_fence.bam")
        self.wood.reparentTo(render)
        self.wood.setPos(90,140,4)
        self.wood.setHpr(90,0,0)
        self.wood = loader.loadModel("data/models/streets/wood_fence.bam")
        self.wood.reparentTo(render)
        self.wood.setPos(90,150,4)
        self.wood.setHpr(90,0,0)

        self.wood = loader.loadModel("data/models/streets/wood_fence.bam")
        self.wood.reparentTo(render)
        self.wood.setPos(30,120,4)
        self.wood.setHpr(90,0,0)
        self.wood = loader.loadModel("data/models/streets/wood_fence.bam")
        self.wood.reparentTo(render)
        self.wood.setPos(30,130,4)
        self.wood.setHpr(90,0,0)
        self.wood = loader.loadModel("data/models/streets/wood_fence.bam")
        self.wood.reparentTo(render)
        self.wood.setPos(30,140,4)
        self.wood.setHpr(90,0,0)
        self.wood = loader.loadModel("data/models/streets/wood_fence.bam")
        self.wood.reparentTo(render)
        self.wood.setPos(30,150,4)
        self.wood.setHpr(90,0,0)

        self.wood = loader.loadModel("data/models/streets/wood_fence.bam")
        self.wood.reparentTo(render)
        self.wood.setPos(20,-20,0)
        self.wood = loader.loadModel("data/models/streets/wood_fence.bam")
        self.wood.reparentTo(render)
        self.wood.setPos(10,-20,0)

        self.wood = loader.loadModel("data/models/streets/wood_fence.bam")
        self.wood.reparentTo(render)
        self.wood.setPos(-20,-20,0)
        self.wood = loader.loadModel("data/models/streets/wood_fence.bam")
        self.wood.reparentTo(render)
        self.wood.setPos(-30,-20,0)

        self.wood = loader.loadModel("data/models/streets/wood_fence.bam")
        self.wood.reparentTo(render)
        self.wood.setPos(29.9,160,3)
        self.wood1 = loader.loadModel("data/models/streets/wood_fence.bam")
        self.wood1.reparentTo(render)
        self.wood1.setPos(80,160,3)

        #Buildings
        self.toD = loader.loadModel("data/models/PDD/AA/ozE.bam")
        self.toD.reparentTo(render)
        self.toD.setPos(0,-23.3,-.5)
        self.toD.setHpr(180,0,0)
        self.sign('DD',self.toD,'DD_sign2',(0,0,0),(0,0,-3),(1.85,1,1.35))
        self.baseline(self.toD.find("**/sign_origin"),'Comedy.bam',(0.439216,0.247059,0.184314,1),(0,0,-0.2),(1.6,1,1.7),'Donald\'s Dock Playground',7)

        self.toA = loader.loadModel("data/models/PDD/AA/ozE.bam")
        self.toA.reparentTo(render)
        self.toA.setPos(60,152,-.45)
        self.sign('DD',self.toA,'DD_sign2',(0,0,0),(0,0,-3),(1.85,1,1.35))
        self.baseline(self.toA.find("**/sign_origin"),'Comedy.bam',(0.439216,0.247059,0.184314,1),(0,0,-0.2),(1.6,1,1.7),'Chip \'N Dale\'s Acorn Acres',7)
        
        #Props
        self.tree = loader.loadModel("data/models/PDD/AA/ozE.bam").find('**/outdoor_zone_entrance_tree2')
        self.tree.reparentTo(render)
        self.tree.setPos(10,50,0)
        self.tree1 = loader.loadModel("data/models/PDD/AA/ozE.bam").find('**/outdoor_zone_entrance_tree2')
        self.tree1.reparentTo(render)
        self.tree1.setPos(-48,105,0)
        self.tree2 = loader.loadModel("data/models/PDD/AA/ozE.bam").find('**/outdoor_zone_entrance_tree2')
        self.tree2.reparentTo(render)
        self.tree2.setPos(65,55,0)
 
        self.tree3 = loader.loadModel("data/models/PDD/AA/ozE.bam").find('**/outdoor_zone_entrance_tree2')
        self.tree3.reparentTo(render)
        self.tree3.setPos(-35,30,0)
        self.tree3.setScale(0.7)
        self.tree4 = loader.loadModel("data/models/PDD/AA/ozE.bam").find('**/outdoor_zone_entrance_tree2')
        self.tree4.reparentTo(render)
        self.tree4.setPos(18,105,0)
        self.tree4.setScale(0.5)

    def sign(self,nbr,parent,sign,pos,hpr,scale):
        self.signn = loader.loadModel("data/models/PDD/AA/signs_{0}.bam".format(nbr)).find("**/"+sign)
        self.signn.reparentTo(parent.find("**/sign_origin"))
        self.signn.setPos(pos)
        self.signn.setHpr(hpr)
        self.signn.setScale(scale)
    def baseline(self,parente,font,color,pos,scale,textx,ww):
        fonto = loader.loadFont("data/fonts/{0}".format(font))
        frame = DirectFrame(frameColor=(0,0,0,0))
        frame.reparentTo(parente)
        frame.setY(-.2)
        self.text = OnscreenText(text=textx,font=fonto,pos=pos,scale=scale,parent=frame,fg=color,wordwrap=ww)
        #self.text.rgbPanel()

          
nr = NuttyRiver()
run()
