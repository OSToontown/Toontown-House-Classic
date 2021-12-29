from panda3d.core import *
from direct.interval.IntervalGlobal import *

import random

class FireworkShow:
    def __init__(self,pos):
        self.fireworkNode = render.attachNewNode('fireworks')
        self.fireworkNode.setScale(50)
        self.fireworkNode.setBillboardAxis()
        self.fireworkNode.setPos(pos)
        colors = [Vec4(255,0,0,1),Vec4(0,255,0,1),Vec4(0,0,255,1)]
        col = random.choice(colors)
        self.fireworkNode.setColor(col)
        self.startFirstUp()

    def startFirstUp(self):
        self.particles = loader.loadModel("data/effects/particles.bam")
        #self.particles.ls()
        self.particle = self.particles.find("**/tt_t_efx_ext_particleSparkle")
        self.particle.reparentTo(self.fireworkNode)

        ups = [(5),(4),(3),(2)]
        randomUp = random.choice(ups)

        particleX = self.particle.getX()
        particleY = self.particle.getY()

        self.startUping = LerpPosInterval(self.particle,2,(particleX,particleY,randomUp))
        self.startUping.start()
        uping1 = loader.loadSfx("data/sounds/uping1.mp3")
        uping2 = loader.loadSfx("data/sounds/uping2.mp3")
        upingSfx = [uping1,uping2]
        randSfx = random.choice(upingSfx)
        randSfx.play()
        seq = Sequence()
        seq.append(Wait(2))
        seq.append(Func(self.startParticleExplosion))
        seq.start()
    def startParticleExplosion(self):
        self.particleExploding1 = self.particles.find("**/tt_t_efx_ext_particleSparkles")
        self.particleExploding1.reparentTo(self.fireworkNode)
        self.particleExploding1.setPos(self.particle.getPos())
        self.particle.remove()
        seq = Sequence()
        seq.append(Wait(.1))
        seq.append(Func(self.continueParticleExplosion))
        seq.start()

    def continueParticleExplosion(self):
        self.particleExploding2 = self.particles.find("**/tt_t_efx_ext_particleWhiteGlow")
        self.particleExploding2.reparentTo(self.fireworkNode)
        self.particleExploding2.setPos(self.particleExploding1.getPos())
        self.particleExploding1.remove()
        seq = Sequence()
        seq.append(Wait(.1))
        seq.append(Func(self.moreParticleExplosion))
        seq.start()
    def moreParticleExplosion(self):
        self.particleExploding3 = self.particles.find("**/tt_t_efx_ext_particleBlast")
        self.particleExploding3.reparentTo(self.fireworkNode)
        self.particleExploding3.setPos(self.particleExploding2.getPos())
        self.particleExploding2.remove()
        seq = Sequence()
        seq.append(Wait(.1))
        seq.append(Func(self.otherParticleExplosion))
        seq.start()
    def otherParticleExplosion(self):
        self.particleExploding4 = self.particles.find("**/tt_t_efx_ext_particleStars")
        self.particleExploding4.reparentTo(self.fireworkNode)
        self.particleExploding4.setPos(self.particleExploding3.getPos())
        self.particleExploding3.remove()
        explosion1 = loader.loadSfx("data/sounds/explosion1.mp3")
        explosion2 = loader.loadSfx("data/sounds/explosion2.mp3")
        explosion3 = loader.loadSfx("data/sounds/explosion3.mp3")
        explodeSfx = [explosion1,explosion2,explosion3]
        randSfx = random.choice(explodeSfx)
        randSfx.play()
        seq = Sequence()
        seq.append(Wait(.1))
        seq.append(Func(self.makeFirework))
        seq.start()
    def makeFirework(self):
        self.firework = loader.loadModel("data/effects/tflip.bam")
        self.firework.reparentTo(self.fireworkNode)
        self.firework.setPos(self.particleExploding4.getPos())
        self.particleExploding4.remove()
        seq = Sequence()
        seq.append(Wait(1))
        seq.append(Func(self.loseFirework))
        seq.start()
    def loseFirework(self):
        down1 = loader.loadSfx("data/sounds/dowing1.mp3")
        down2 = loader.loadSfx("data/sounds/dowing2.mp3")
        dowingSfx = [down1,down2]
        randSfx = random.choice(dowingSfx)
        randSfx.play()
        self.losingFirework = self.particles.find("**/tt_t_efx_ext_particleSplat")
        self.losingFirework.reparentTo(self.fireworkNode)
        self.losingFirework.setPos(self.firework.getPos())
        self.firework.remove()
        lFx = self.losingFirework.getX()
        lFy = self.losingFirework.getY()
        lFz = self.losingFirework.getZ()
        dowing = LerpPosInterval(self.losingFirework,2,(lFx,lFy,-10))
        dowing.start()
        seq = Sequence()
        seq.append(Wait(2))
        seq.append(Func(self.continueLoseFirework))
        seq.start()
    def continueLoseFirework(self):
        self.losingFirework1 = self.particles.find("**/tt_t_efx_ext_particleSplash3")
        self.losingFirework1.reparentTo(self.fireworkNode)
        self.losingFirework1.setPos(self.losingFirework.getPos())
        self.losingFirework.remove()
        lFx = self.losingFirework1.getX()
        lFy = self.losingFirework1.getY()
        lFz = self.losingFirework1.getZ()
        dowing = LerpPosInterval(self.losingFirework1,.1,(lFx,lFy,lFz -5))
        dowing.start()

        
