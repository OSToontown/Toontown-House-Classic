from panda3d.core import *
from __init__ import Area

######################################
#NAME: INDOORS BUILDINGS
#AUTHOR: Jean
#DATE: 28/02/14
######################################
#toon_interior - typical one room building.
#toon_interior_2 - same as toon_interior 1
#toon_interior_l - Building with huge door.
#toon_interior_T - largest building.
######################################

#since it was already made, i decided to implement it here, since it's a ''INDOORS'' area.
class KartShop(Area):
    def __init__(self, tp=None):
        self.name = "area_kartshop"
        self.music =  "data/sounds/ttc/gsw-shop.ogg"
        self.zoneId = 1404

        self.sky = loader.loadModel("phase_3.5/models/props/TT_sky.bam")
        self.sky.reparentTo(self.np)
        self.sky.setScale(2)
        self.skyFog = Fog("Sky Fog")
        self.skyFog.setExpDensity(0.001)
        self.sky.setFog(self.skyFog)

        self.avatarPN = ['wall','props']
        self.pointView = False  #var for the future feature to change the point of view, in here it should be blocked
        Area.__init__(self,"phase_6/models/karting/KartShop_Interior.bam")
        self.avatar.setPos(0,0,0)

        if tp: tp.done()

    def __tth_area__(self):
        return {
                'name':self.name,
                'models':self.np,
                'bgm':self.theme,
                'speeches':[]
                }

class ToonHQ(Area):
#In general, all toon hq should look the same in-game. The only problem here is the music, and door warp.
    def __init__(self, tp=None):
        self.name = "area_toonhq"
        self.music =  "phase3.5/audio/TC_SZ_activity.mid"
        self.zoneId = 1405

        self.sky = loader.loadModel("phase_3.5/models/props/TT_sky.bam")
        self.sky.reparentTo(self)
        self.sky.setScale(2)
        self.skyFog = Fog("Sky Fog")
        self.skyFog.setExpDensity(0.001)
        self.sky.setFog(self.skyFog)

        self.avatarPN = ['wall','props']
        Area.__init__(self,"phase3.5/models/modules/HQ_interior")
        self.avatar.setPos(0,0,0)

        if tp: tp.done()

    def __tth_area__(self):
        return {
                'name':self.name,
                'models':self.np,
                'bgm':self.theme,
                'speeches':[]
                }

class TTCSchoolHouse(Area):
#TODO
    def __init__(self, tp=None):
        self.name = "area_ttcschool"
        self.music =  "phase3.5/audio/TC_SZ_activity.mid"
        self.zoneId = 1406

        self.avatarPN = ['wall','props']
        Area.__init__(self,"phase3.5/models/modules/toon_interior_l")
        self.avatar.setPos(0,0,0)

        if tp: tp.done()

    def __tth_area__(self):
        return {
                'name':self.name,
                'models':self.np,
                'bgm':self.theme,
                'speeches':[]
                }