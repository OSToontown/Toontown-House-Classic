from panda3d.core import *
from direct.gui.DirectGui import *
import direct.directbase.DirectStart

VirtualFileSystem.getGlobalPtr().mount("../../data/phase_3.mf",".",0)

from dialog import *

d = CancelDialog(text="blah",button_relief=None,buttonGeomList=[cancelButtons])

wantedW = 1

setDialogWidth(d,wantedW)

run()