from pandac.PandaModules import *
from direct.gui.DirectGui import *

import random, sys

class MarginCell(DirectFrame):
    def __init__(self, manager, parent, size, parId, x, y):
        DirectFrame.__init__(self)
        self.initialiseoptions(MarginCell)

        self.manager = manager
        self.data = None
        self.parId = parId

        self.reparentTo(parent)
        self.setPos(x,0,y)
        
        self.w, self.h = size
        self["frameSize"] = (-self.w/2.,self.w/2.,-self.h/2.,self.h/2.)
        
        if base.isInjectorOpen or '--showcells' in sys.argv:
            l = [1,.5,.3]
            random.shuffle(l)
            l.append(random.randint(7,10)/10.,)
            self["frameColor"] = l
            
        else: self["frameColor"] = (0,0,0,0)
        
        self.resetFrameSize()
        
    def isFree(self):
        return not bool(self.data)
        
    def allocate(self):
        self.data = "<allocated by manager>"
        
    def destroy(self):
        DirectFrame.destroy(self)
        if self.data: self.data.destroy()