from direct.distributed.DistributedNodeAI import DistributedNodeAI
from pandac.PandaModules import *

class DistributedSignpostAI(DistributedNodeAI):

    """ This is the AI-side implementation of DistributedSignpost. """

    def __init__(self, cr):
        DistributedNodeAI.__init__(self, cr)

        self.message = ''
        self.color = (1, 1, 1)

    def setMessage(self, message):
        self.message = message

    def d_setMessage(self, message):
        self.sendUpdate('setMessage', [message])

    def b_setMessage(self, message):
        self.d_setMessage(message)
        self.setMessage(message)

    def getMessage(self):
        return self.message

    def setColor(self, r, g, b):
        self.color = (r, g, b)

    def d_setColor(self, r, g, b):
        self.sendUpdate('setColor', [r, g, b])

    def b_setColor(self, r, g, b):
        self.d_setColor(r, g, b)
        self.setColor(r, g, b)

    def getColor(self):
        return self.color

    def touched(self, r, g, b):
        """ This is called by the client when an avatar touches the
        sign. """

        self.d_react()
        self.b_setColor(r, g, b)
        self.b_setMessage("Don't touch me!")

    def d_react(self):
        """ This is sent by the AI to the clients. """
        self.sendUpdate('react', [])
