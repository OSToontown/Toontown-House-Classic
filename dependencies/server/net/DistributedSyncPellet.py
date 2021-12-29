from direct.distributed.DistributedObject import DistributedObject
from direct.distributed.ClockDelta import globalClockDelta
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *

class DistributedSyncPellet(DistributedObject):

    """ This is an improvement on DistributedPellet.  It bounces up
    and down in the same way, but it also takes advantage of the
    network time sync provided by the TimeManager in server2.py to
    record the precise time at which the pellet started bouncing, so
    that it bounces in sync on all clients. """
    
    def __init__(self, cr):
        DistributedObject.__init__(self, cr)

        self.model = loader.loadModel('smiley.egg')
        self.model.setScale(0.1)

        self.initialPos = (0, 0, 0)
        self.startTime = 0

    def setInitialPos(self, x, y, z):
        self.initialPos = (x, y, z)

    def getInitialPos(self):
        return self.initialPos

    def setStartTime(self, startTime):
        # The start time is transmitted as a network time; we convert
        # it to local time for storage.  Note that we use a 32-bit
        # conversion to allow for long-ago start times.  (The default
        # 16-bit conversion only supports a time that can't get older
        # than about 5 minutes).
        
        self.startTime = globalClockDelta.networkToLocalTime(startTime, bits = 32)

    def getStartTime(self):
        # We convert the start time back into network time for
        # transmission.  The 32-bit conversion must be specified here
        # again.
        
        return globalClockDelta.localToNetworkTime(self.startTime, bits = 32)
        
    def announceGenerate(self):
        DistributedObject.announceGenerate(self)

        # Start it slowly bouncing with an interval.
        x, y, z = self.initialPos
        self.model.setPos(x, y, z + 3)
        i1 = self.model.posInterval(2, (x, y, z), blendType = 'easeInOut')
        i2 = self.model.posInterval(2, (x, y, z + 3), blendType = 'easeInOut')
        self.ival = Sequence(i1, i2)

        # How much time has elapsed since the sequence started?
        elapsed = globalClock.getFrameTime() - self.startTime

        # Start the interval looping, then skip to the appropriate
        # point in its cycle.
        self.ival.loop()
        self.ival.setT(elapsed % self.ival.getDuration())

        self.model.reparentTo(render)

    def disable(self):
        # When the pellet is disabled, stop it bouncing and take it
        # out of the scene graph.
        self.ival.pause()
        self.model.detachNode()
        DistributedObject.disable(self)
