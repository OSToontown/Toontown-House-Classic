from panda3d.core import *
from direct.gui.DirectGui import *
import __builtin__

class CancelDialog(DirectDialog):
    def __init__(self, parent = None, **kw):
        # Inherits from DirectFrame
        optiondefs = (
            # Define type of DirectGuiWidget
            ('buttonTextList',  ['Cancel'],   DGG.INITOPT),
            ('buttonValueList', [DGG.DIALOG_CANCEL], DGG.INITOPT),
            )
        # Merge keyword options with default options
        self.defineoptions(kw, optiondefs)
        DirectDialog.__init__(self, parent)
        self.initialiseoptions(CancelDialog)
        
if not getattr(__builtin__,'isServer',False):
    buttonsM = loader.loadModel('phase_3/models/gui/dialog_box_buttons_gui.bam')
    okButtons = map(lambda x: buttonsM.find("**/*OKBtn_"+x),('UP','DN','Rllvr'))
    cancelButtons = map(lambda x: buttonsM.find("**/CloseBtn_"+x),('UP','DN','Rllvr'))

def setDialogWidth(dialog,width):
    space = sum(map(lambda x:max(x,-x),map(lambda x:x[0],dialog['image'].getTightBounds())))
    _s = dialog['image_scale']
    _s[0] = width/space
    dialog['image_scale'] = _s
    dialog.resetFrameSize()