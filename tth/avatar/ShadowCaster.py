from direct.directnotify import DirectNotifyGlobal
from direct.showbase.ShadowPlacer import ShadowPlacer
from pandac.PandaModules import *

from tth.base import TTHouseGlobals

ShadowGrayLevel = 0.5
ModelDropShadow = 'phase_3/models/props/drop_shadow.bam'
ModelSquareDropShadow = 'phase_3/models/props/square_drop_shadow.bam'

class ShadowCaster:

    notify = DirectNotifyGlobal.directNotify.newCategory('ShadowCaster')

    def __init__(self, squareShadow=False):
        if squareShadow:
            self.shadowFileName = ModelSquareDropShadow
        else:
            self.shadowFileName = ModelDropShadow
        self.dropShadow = None
        self.shadowPlacer = None
        self.activeShadow = 0
        self.storedActiveState = 0

    def delete(self):
        self.deleteDropShadow()
        self.shadowJoint = None

    def initializeDropShadow(self, hasGeomNode=True):
        self.deleteDropShadow()
        if hasGeomNode:
            self.getGeomNode().setTag('cam', 'caster')
        dropShadow = loader.loadModel(self.shadowFileName)
        dropShadow.setScale(0.4)
        dropShadow.flattenMedium()
        dropShadow.setBillboardAxis(2)
        dropShadow.setColor(0.0, 0.0, 0.0, ShadowGrayLevel, 1)
        self.shadowPlacer = ShadowPlacer(
            base.shadowTrav, dropShadow, TTHouseGlobals.WallBitmask,
            TTHouseGlobals.FloorBitmask
        )
        self.dropShadow = dropShadow
        self.dropShadow.reparentTo(self.getShadowJoint())
        self.setActiveShadow(1)
        self.showShadow()
        self.dropShadow.setColor(0.0, 0.0, 0.0, ShadowGrayLevel, 1)

    def deleteDropShadow(self):
        if self.shadowPlacer:
            self.shadowPlacer.delete()
            self.shadowPlacer = None
        if self.dropShadow:
            self.dropShadow.removeNode()
            self.dropShadow = None

    def setActiveShadow(self, isActive=1):
        if self.shadowPlacer is None:
            return None
        if self.activeShadow != isActive:
            self.activeShadow = isActive
            if isActive:
                self.shadowPlacer.on()
            else:
                self.shadowPlacer.off()

    def setShadowHeight(self, shadowHeight):
        if self.dropShadow:
            self.dropShadow.setZ(-shadowHeight)

    def getShadowJoint(self):
        if hasattr(self, 'shadowJoint'):
            return self.shadowJoint
        shadowJoint = self.find('**/attachShadow')
        if shadowJoint.isEmpty():
            self.shadowJoint = NodePath(self)
        else:
            self.shadowJoint = shadowJoint
        return self.shadowJoint

    def hideShadow(self):
        self.dropShadow.hide()

    def showShadow(self):
        self.dropShadow.show()