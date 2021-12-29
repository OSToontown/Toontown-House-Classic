from direct.distributed.DistributedObject import DistributedObject
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *

class DistributedPellet(DistributedObject):

    """ This is a funny little pellet that can be dropped on the
    ground as a demonstration.  This could have inherited from
    DistributedNode, but we inherit from DistributedObject instead
    just to show that you don't always need to inherit from
    DistributedNode. """
    
    def __init__(self, cr):
        DistributedObject.__init__(self, cr)

        # We re-use the smiley model again to make pellets.
        self.model = loader.loadModel('smiley.egg')
        self.model.setScale(0.1)

        self.initialPos = (0, 0, 0)

    def setInitialPos(self, x, y, z):
        self.initialPos = (x, y, z)

    def getInitialPos(self):
        return self.initialPos
        
    def announceGenerate(self):
        DistributedObject.announceGenerate(self)

        # Start it slowly bouncing with an interval.
        x, y, z = self.initialPos
        self.model.setPos(x, y, z + 3)
        i1 = self.model.posInterval(2, (x, y, z), blendType = 'easeInOut')
        i2 = self.model.posInterval(2, (x, y, z + 3), blendType = 'easeInOut')
        self.ival = Sequence(i1, i2)
        self.ival.loop()

        self.model.reparentTo(render)

        # Note that, although all the instances of the
        # DistributedPellet will be bouncing at the same speed
        # (because they're all playing a similar interval on
        # themselves), they may not be in sync with other instances of
        # the same pellet on different clients (because there's
        # nothing in the above that synchronizes the intervals).

    def disable(self):
        # When the pellet is disabled, stop it bouncing and take it
        # out of the scene graph.
        self.ival.pause()
        self.model.detachNode()
        DistributedObject.disable(self)
