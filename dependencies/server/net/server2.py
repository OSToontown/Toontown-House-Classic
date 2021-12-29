""" Demonstrates the DC system from the server side, using a
DistributedSmoothNode-based avatar. """

import direct
from pandac.PandaModules import *
loadPrcFileData('', 'window-type none')
from direct.directbase.DirectStart import *
import random

from direct.distributed.ServerRepository import ServerRepository
from direct.distributed.ClientRepository import ClientRepository

class MyServerRepository(ServerRepository):
    def __init__(self):
        tcpPort = base.config.GetInt('server-port', 4400)
        dcFileNames = ['direct.dc', 'net.dc']
        
        ServerRepository.__init__(self, tcpPort, None, dcFileNames = dcFileNames)

server = MyServerRepository()

# We also need an AI for the server in this case, if for no other
# reason than to respond to the TimeManager requests.  An AI is just a
# special kind of a client that creates (and manages) the objects that
# reside in the world independently of the regular clients in the
# game.

# The AI often has a slightly different perspective of its objects
# (e.g. it usually doesn't need to render anything), so it uses a
# different class to represent them, named FooAI.py instead of Foo.py.
# self.dcSuffix makes this difference.

# This particular AI creates only a TimeManager object, but it could
# create any number of other objects as well, if we had any persistent
# server-side objects in our world.

class MyAIRepository(ClientRepository):
    def __init__(self):
        dcFileNames = ['direct.dc', 'net.dc']
        
        ClientRepository.__init__(self, dcFileNames = dcFileNames,
                                  dcSuffix = 'AI')

        tcpPort = base.config.GetInt('server-port', 4400)
        url = URLSpec('http://127.0.0.1:%s' % (tcpPort))
        self.connect([url],successCallback = self.connectSuccess,failureCallback = self.connectFailure)
        
    def connectFailure(self, statusCode, statusString):
        raise StandardError, statusString

    def connectSuccess(self):
        """ Successfully connected.  But we still can't really do
        anything until we've got the doID range. """
        self.acceptOnce('createReady', self.createReady)

    def createReady(self):
        """ Now we're ready to go! """
        # Put the time manager in zone 1 where the clients can find it.
        self.timeManager = self.createDistributedObject(
            className = 'TimeManagerAI', zoneId = 1)

        # Put a bunch of signposts in the various zones that clients
        # will visit.
        self.signPosts = []
        for zoneId in range(101, 110):
            signPost = self.createDistributedObject(
                className = 'DistributedSignpostAI', zoneId = zoneId)
            signPost.b_setMessage("Welcome to zone %s" % (zoneId))

            x = random.uniform(-5, 5)
            y = random.uniform(5, 20)
            z = 0
            signPost.b_setPosHpr(x, y, z, 0, 0, 0)
            self.signPosts.append(signPost)

air = MyAIRepository()

run()
