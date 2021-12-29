import CogDNA, random

from panda3d.core import *
from direct.gui.DirectGui import *

cog = loader.loadModel("phase_3.5/models/char/suitC-mod")

class Cog(NodePath):
    def __init__(self,dna):
        self.dna = CogDNA.CogDNA()
        self.dna.makeFrom(dna)
        NodePath.__init__(self,str(self.dna.level))
        cog.instanceTo(self)
        
        self.tag = OnscreenText(decal=True,text=str(self.dna.level),scale=1.2,fg=(0,0,0,1),bg=(1,1,1,.3),mayChange=1)
        self.tag.reparentTo(self)
        self.tag.setBillboardAxis()
        
        self.tag.setZ(4)
        
        bounds = map(lambda x:max(x,-x),map(lambda x:x[0]-x[1],zip(*self.getTightBounds())))
        
        cs = CollisionSphere(0,0,0,.9)
        cn = CollisionNode(self.getName()+'_cnode')
        cn.addSolid(cs)
        cn.setCollideMask(16)
        
        self.cnp = self.attachNewNode(cn)
        self.cnp.setScale(*bounds)
        self.cnp.show()
        
        self.setScale(.5)
        
    def reload(self,dna):
        self.dna.makeFrom(dna)
        self.setName(str(self.dna.level))
        
        self.tag.setText(str(self.dna.level))

class StreetWalker:
    def __init__(self,file="nothingRes.txt"):
        self.cogs = []
        self.points = file #eval(open("tth/cogs/"+file,"rb").read())
        
        self.__click = 0
        
        print len(self.points)
        
        for i,point in enumerate(self.points):
            print i
            dna = CogDNA.CogDNA()
            dna.isWaiter = 1
            dna.dept = random.choice(range(4))
            dna.leader = 0
            dna.level = i
            
            c = Cog(dna.make())
            c.reparentTo(render)
            c.setPos(point)
            c.isDis = False
            self.cogs.append(c)
            
            cn = c.cnp
            cn.node().setName(str(i))
            
            gamebase.clickDict[cn] = self.__setLevel
            gamebase.clickDictR[cn] = self.__remove
            
    def __setLevel(self,entry):
        index = int(entry.getIntoNode().getName())
        print 'set',index,self.__click
        cog = self.cogs[index]
        if cog.isDis:
            print 'disabled, enabling...'
            cog.isDis = False
            cog.setScale(cog,2)
            return 
            
        dna = cog.dna
        dna.level = self.__click
        self.__click += 1
        dna.lives += 1
        
        cog.reload(dna.make())
        cog.setScale(cog,2)
        
    def __remove(self,entry):
        index = int(entry.getIntoNode().getName())
        print index,self.__click
        cog = self.cogs[index]
        
        if cog.isDis:
            print 'already disabled, ignoring...'
        
        dna = cog.dna
        dna.level = 0
        dna.lives = 0
        
        cog.reload(dna.make())
        cog.setScale(cog,.5)
        cog.isDis = True
        
    def save(self,file):
        l = []
        for cog in self.cogs:
            if not cog.isDis:
                l.append(c.getPos())
            
        print 'saved to file',file
        