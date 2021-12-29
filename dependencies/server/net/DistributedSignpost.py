from direct.distributed.DistributedNode import DistributedNode
from direct.interval.IntervalGlobal import *
from pandac.PandaModules import *

class DistributedSignpost(DistributedNode):

    """ An instance of these is created and placed in the middle of
    the zone.  It serves to illustrate the creation of AI-side objects
    to populate the world, and a general mechanism for making them
    react to the avatars. """
    
    def __init__(self, cr):
        DistributedNode.__init__(self, cr)
        NodePath.__init__(self, 'signpost')

        # Eventually we will assign a unique string to this, so that
        # all signposts have a unique collision event.
        self.collName = 'collName'
        
        # We want to be able to render the backside of the sign, too.
        self.setTwoSided(1)

        self.text = TextNode('text')
        self.text.setTextColor(0, 0, 1, 1)
        self.text.setCardAsMargin(0.1, 0.1, 0.1, 0.1)
        self.text.setCardColor(1, 1, 1, 1)
        self.text.setCardDecal(True)
        self.text.setShadowColor(0, 0, 0, 1)
        self.text.setShadow(0.03, 0.03)
        self.text.setAlign(TextNode.ACenter)

        self.ival = None
        self.geom = None
        self.assignText()

    def assignText(self):
        """ Makes the visible signpost show the current text
        message. """

        # Remove the previous signpost, if any
        if self.geom:
            self.geom.detachNode()
        
        # Use TextNode.generate() to make the visible geometry, so we
        # can detect collisions.
        self.geom = self.attachNewNode(self.text.generate())

        # Make the card respond to avatar collisions.
        self.geom.setCollideMask(BitMask32(1))
        self.geom.setName(self.collName)

    def setMessage(self, message):
        """ Specifies the message that is displayed on the sign. """
        self.text.setText(message)
        self.assignText()

        # Note that we don't need a getMessage() on the client side,
        # because this is an AI-created object only.

    def setColor(self, r, g, b):
        """ Specifies the color for the sign. """
        self.text.setCardColor(r, g, b, 1)
        self.assignText()

    def d_touched(self, r, g, b):
        """ Call this when an avatar touches the sign.  It sends the
        message up to the AI, along with the avatar's color. """
        
        self.sendUpdate('touched', [r, g, b])

    def react(self):
        """ This method is called by the AI in response to someone
        touching it.  Make something interesting happen,
        temporarily. """

        if self.ival:
            self.ival.finish()
            
        self.ival = Parallel(self.hprInterval(1, (360 * 10, 0, 0), startHpr = (0, 0, 0), blendType = 'easeInOut'),
                             Sequence(self.scaleInterval(0.5, 2, blendType = 'easeInOut'),
                                      self.scaleInterval(0.5, 1, blendType = 'easeInOut')))
        self.ival.start()
        
    def announceGenerate(self):
        """ This method is called after generate(), after all of the
        required fields have been filled in.  At the time of this call,
        the distributed object is ready for use. """

        DistributedNode.announceGenerate(self)

        # By the time we have generate, we have a doId, so we can
        # listen for collision events.
        self.collName = 'signpost-%s' % (self.doId)
        if self.geom:
            self.geom.setName(self.collName)
        self.accept(self.collName, self.collisionDetected)

        # Now that the object has been fully manifested, we can parent
        # it into the scene.
        self.reparentTo(render)

    def disable(self):
        self.ignore(self.collName)

        if self.ival:
            self.ival.finish()
            self.ival = None
        
        # Take it out of the scene graph.
        self.detachNode()

        DistributedNode.disable(self)

    def collisionDetected(self, centry):
        """ Called when the local avatar bumps into the sign. """

        # Tell the AI this happened, then sit back and let him do the
        # work.

        # Also tell the AI what our current avatar color is.
        av = base.w.av
        r, g, b = av.avColor
        self.d_touched(r, g, b)
        
