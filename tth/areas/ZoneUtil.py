from direct.directnotify import DirectNotifyGlobal

from tth.base import TTHouseGlobals

zoneUtilNotify = DirectNotifyGlobal.directNotify.newCategory('ZoneUtil')

def getCanonicalZoneId(zoneId):
    zoneId = zoneId % 2000
    if zoneId < 1000:
        zoneId = zoneId + TTHouseGlobals.ToontownCentral
    else:
        zoneId = (zoneId-1000) + TTHouseGlobals.GoofySpeedway
    return zoneId

def getWakeInfo(hoodId=None, zoneId=None):
    wakeWaterHeight = 0
    showWake = 0
    try:
        # TODO: If one of these is false, fetch the current zone/hoodId:
        if hoodId is None:
            hoodId = 2000
        if zoneId is None:
            zoneId = 2000
        canonicalZoneId = getCanonicalZoneId(zoneId)
        if canonicalZoneId == TTHouseGlobals.DonaldsDock:
            wakeWaterHeight = TTHouseGlobals.DDWakeWaterHeight
            showWake = 1
        elif canonicalZoneId == TTHouseGlobals.ToontownCentral:
            wakeWaterHeight = TTHouseGlobals.TTWakeWaterHeight
            showWake = 1
        elif canonicalZoneId == TTHouseGlobals.OutdoorZone:
            wakeWaterHeight = TTHouseGlobals.OZWakeWaterHeight
            showWake = 1
        elif hoodId == TTHouseGlobals.MyEstate:
            wakeWaterHeight = TTHouseGlobals.EstateWakeWaterHeight
            showWake = 1
    except AttributeError:
        pass
    return (showWake, wakeWaterHeight)