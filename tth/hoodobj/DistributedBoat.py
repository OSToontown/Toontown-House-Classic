import random, math
from pandac.PandaModules import *
from direct.distributed import DistributedObject
 
class DistributedBoat(DistributedObject.DistributedObject):
    def __init__(self):
        self.waveSound = base.loader.loadSfx('phase_6/audio/sfx/SZ_DD_waterlap.mp3')
 
        self.sfx_bell = self.loadRing('shipbell')
        self.sfx_creack = self.loadRing('dockcreak')
        self.sfx_water = self.loadRing('waterlap')
        
        self.sfxInterval_bell = SoundInterval(self.sfx_bell,loop=0)
        self.sfxInterval_creack = SoundInterval(self.sfx_creack,loop=0)
        self.sfxInterval_water = SoundInterval(self.sfx_water,loop=0)
 
    def loadRing(self,ring):
        return loader.loadSfx("phase_6/audio/sfx/SZ_DD_{0}.mp3".format(ring))
 
    def makeSeq(self):
        self.moveBoat1 = self.boat.posHprInterval(6, (30.43079, -32.5, -4), (90,0,0))
        self.moveBoat2 = self.boat.posHprInterval(6, (-33.5692, -42.5, -4), (40,0,0))
        self.moveBoat3 = self.boat.posHprInterval(4, (-50, -10, -4), (0,0,0))
        self.moveBoat4 = self.boat.posHprInterval(6, (-50, 40, -4), (-50,0,0))
        self.moveBoat5 = self.boat.posHprInterval(6, (9.08847, 50.4189, -4), (-100,0,0))
        self.moveBoat6 = self.boat.posHprInterval(6, (50.1,25,-4), (-180,0,0))
        
        self.upEPier = self.EPier.hprInterval(5, (89.9995,-0,-0.000199231))
        self.downEPier = self.EPier.hprInterval(4, (89.9995,-44.2599,-0.000199231))
        self.upWPier = self.WPier.hprInterval(4, (-90.399,-0,-0.185446))
        self.downWPier = self.WPier.hprInterval(4, (-90.399,-47.5673,-0.185446))
 
        self.fogHorn = SoundInterval(loader.loadSfx("phase_5/audio/sfx/SZ_DD_foghorn.mp3"),loop=0)
        
        self.seq = Sequence(
                            Wait(14),
                            Parallel(self.sfxInterval_bell,
                                     self.downEPier,
                                     self.sfxInterval_creack,
                                     self.moveBoat1),
                            self.moveBoat2,
                            Parallel(self.upWPier,
                                     self.sfxInterval_creack,
                                     self.moveBoat3),
                            self.fogHorn,
                            Wait(14),
                            Parallel(self.sfxInterval_bell,
                                     self.downWPier,
                                     self.sfxInterval_creack,
                                     self.moveBoat4),
                            self.moveBoat5,
                            Parallel(self.moveBoat6,
                                     self.sfxInterval_creack,
                                     self.upEPier),
                            self.fogHorn,
                            )
        self.seq.loop()
 
    def load(self):
        self.boat = self.environ.find("**/donalds_boat")
        self.boat.setPos(50.1,25,-4)
        self.boat.setHpr(180,0,0)
        if 0:
            self.boat.find('**/wheel').hide()
        self.EPier = self.environ.find("**/east_pier")
        self.EPier.setHpr(89.9995,-0,-0.000199231)
        self.WPier = self.environ.find("**/west_pier")
        base.accept('enterdonalds_boat_floor', self.enter)
        base.accept('exitdonalds_boat_floor', self.exit)
        self.makeSeq()
 
    def unload(self):
        self.seq.finish()
        del self.seq
        del self.boat
        del self.EPier
        del self.WPier
 
    def enter(self,collide):
        gamebase.currArea.wrtReparentTo(self.environ.find('**/donalds_boat'))
        SoundInterval(self.waveSound,loop=100).loop()
 
    def exit(self,collide):
        gamebase.currArea.toon.wrtReparentTo(self.np)
        self.speedUpSound.stop()