from panda3d.core import *
from __init__ import Area

class KartShop(Area):
    def __init__(self, tp=None):
        self.name = "Goofy's Auto Shop"
        self.music =  "data/sounds/ttc/gsw-shop.ogg"
        self.zoneId = 1404

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