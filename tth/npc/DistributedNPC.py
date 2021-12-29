from direct.distributed.DistributedNode import DistributedNode
from direct.distributed.ClockDelta import globalClockDelta

from tth.avatar.Toon import *

import NPCGlobals
from panda3d.core import *

CollMask = {'outer': BitMask32(8),
            'inner':BitMask32(1)}

class DistributedNPC(DistributedNode):
    def __init__(self,cr):
        DistributedNode.__init__(self,cr)
        NodePath.__init__(self,'DistributedNPC')
        self.name = ""
        self.toon = None

    def announceGenerate(self):
        DistributedNode.announceGenerate(self)
        self.reparentTo(render)

    def setId(self,npcId):
        self.npcName = L10N.NPCToonNames[npcId]
        self.setName('DistributedNPC-'+str(npcId))
        self.npcId = npcId

        #generate the toon
        self.dna = ToonDNA.ToonDNA()
        self.dna.newToonFromProperties(*NPCGlobals.NPCToonDict[npcId][2])

        if not self.toon:
            self.toon = Toon()
            self.toon.reparentTo(self)

            self.toon.setDNA(self.dna)
            self.toon.loop('neutral')
            self.toon.useLOD('1000')

            self.toon.setName(self.npcName,1,1)
            self.toon.tag['fg'] = NPCGlobals.NPCNametagColor
            taskMgr.doMethodLater(10,self.initBodyColl,"init body coll of npc")

    def initBodyColl(self, task):
        if not gamebase.curArea:
            print 'bad curArea, redoing...'
            return task.again

        self.inCn = CollisionNode(self.getName()+'-cnode-inner')
        cs = CollisionSphere(0,0,0,1)
        self.inCn.addSolid(cs)
        self.inCn.setCollideMask(CollMask['inner'])

        self.inCnp = self.attachNewNode(self.inCn)
        self.inCnp.setZ(3)
        self.inCnp.setSz(3)

        self.ouCn = CollisionNode(self.getName()+'-cnode-outer')
        cs = CollisionSphere(0,0,0,1.1)
        self.ouCn.addSolid(cs)
        self.ouCn.setCollideMask(CollMask['outer'])

        self.ouCnp = self.attachNewNode(self.ouCn)
        self.ouCnp.setZ(3)
        self.ouCnp.setScale(1.5,1.5,3)

        #self.inCnp.show()
        #self.ouCnp.show()

        gamebase.curArea.collDict[self.ouCn] = self.touched
        return task.done

    def touched(self,entry):
        #must be subclassed
        return
