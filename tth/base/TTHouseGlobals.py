from pandac.PandaModules import *

# File Paths
ScreenShotDirectory = 'screenshots'

# Bit Masks
WallBitmask = BitMask32(1)
FloorBitmask = BitMask32(2)
PieBitmask = BitMask32(256)
GhostBitmask = BitMask32(2048)
ShadowCameraBitmask = BitMask32.bit(2)

# Font
InterfaceFont = None
InterfaceFontPath = 'phase_3/models/fonts/ImpressBT.ttf'
ToonFontPath = 'phase_3/models/fonts/ImpressBT.ttf'

def getInterfaceFont():
    global InterfaceFontPath
    global InterfaceFont
    if InterfaceFont is None:
        if InterfaceFontPath is None:
            InterfaceFont = TextNode.getDefaultFont()
        else:
            InterfaceFont = loader.loadFont(InterfaceFontPath, lineHeight=1.0)
    return InterfaceFont

def setInterfaceFont(path):
    global InterfaceFontPath
    global InterfaceFont
    InterfaceFontPath = path
    InterfaceFont = loader.loadFont(InterfaceFontPath, lineHeight=1.0)

# Dialogue
DialogLength1 = 6
DialogLength2 = 12
DialogLength3 = 20

# Zone IDs
DonaldsDock = 1000
ToontownCentral = 2000
TheBrrrgh = 3000
MinniesMelodyland = 4000
DaisyGardens = 5000
OutdoorZone = 6000
FunnyFarm = 7000
GoofySpeedway = 8000
DonaldsDreamland = 9000

# Wake
TTWakeWaterHeight = -4.79
DDWakeWaterHeight = 1.669
EstateWakeWaterHeight = -0.3
OZWakeWaterHeight = -0.5