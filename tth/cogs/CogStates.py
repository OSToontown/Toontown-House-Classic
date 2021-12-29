from panda3d.core import Vec3
from direct.fsm.FSM import FSM
from direct.interval.IntervalGlobal import *
from direct.actor.Actor import Actor

blah = ('walk','neutral','anvil-drop','drop','sidestep-left',
              'sidestep-right','squirt-large','landing','walknreach',
              'rake','hypnotize','soak',"walk","neutral","flailing",
              "lose","pie-small","squirt-small","slip-forward",
              "slip-backward","tug-o-war")

class BasicCogFSM(FSM):
    name = 'CogFSM'
    def __init__(self,dcog,cog):
        FSM.__init__(self,self.name)
        self.dcog = dcog
        self.cog = cog
        
        self.area = base.hoodMgr.symbols[self.dcog.zoneId % 10**7][0]
        self.walkSeq = BasicCogFSM.makeWalkSequence(self.area.cogPoints,self.cog)
              
        self.propellerSounds = map(lambda x:loader.loadSfx("phase_5/audio/sfx/ENC_propeller_%s.mp3"%x),("in","out"))
        
    def enterNeutral(self,*args):
        self.cog.stop()
        self.cog.loop("neutral")
        
    def exitNeutral(self): pass
    
    def enterDrop(self,isAnvil,ts):
        self.cog.stop()
        self.cog.play('anvil-'*isAnvil=="anvil")
        
    def exitDrop(self): pass
    
    def enterWalk(self,arg,ts):
        ts = ts%self.area.cogWalkDur
        #print self.dcog,'gonna walk',ts
        self.walkSeq.loop()
        self.walkSeq.setT(ts)
        
        self.cog.stop()
        self.cog.loop('walk')
        
    def exitWalk(self):
        #print self.dcog,'stopped walking'
        self.walkSeq.finish()
        
        self.cog.stop()
        self.cog.loop('neutral')
        
        self.walkSeq  = BasicCogFSM.makeWalkSequence(self.area.cogPoints,self.cog)
        
    def enterFlyIn(self,pos,ts):
        self.propeller = Actor("phase_4/models/props/propeller-mod",{"x":"phase_4/models/props/propeller-chan"})
        self.propeller.reparentTo(self.cog.find('**/cogHead*'))
        
        timing = 3*8
               
        dur = self.cog.getDuration('landing')
        pr = (timing/8)/dur
        
        dur2 = self.propeller.getDuration('x')
        pr2 = (timing/8)/dur2
        
        posAndH = map(float,pos.split(','))
        pos = posAndH[:-1]
        h = posAndH[-1]
        
        self.cog.setH(h)
        
        pos = Vec3(*pos)
        
        pos2 = Vec3(pos)
        pos2.setZ(pos2.getZ()+timing)
        
        self.mdownSeq = Sequence(
                            Parallel(
                                     ActorInterval(self.cog,'landing',playRate=pr),
                                     ActorInterval(self.propeller,'x',playRate=pr2),
                                     self.cog.posInterval(timing/8,pos,startPos=pos2),
                                     SoundInterval(self.propellerSounds[0],node=self.cog,duration=3)
                                    ),
                            )
        self.mdownSeq.start(ts)
        
    def exitFlyIn(self):
        self.propeller.cleanup()
        self.propeller.removeNode()
        
        self.mdownSeq.finish()
        
    def enterFlyAway(self,pos,ts):
        self.propeller = Actor("phase_4/models/props/propeller-mod",{"x":"phase_4/models/props/propeller-chan"})
        self.propeller.reparentTo(self.cog.find('**/cogHead*'))
        
        timing = 3*8
               
        dur = self.cog.getDuration('landing')
        pr = (timing/8)/dur
        
        pos = self.cog.getPos()
        
        pos2 = Vec3(pos)
        pos2.setZ(pos2.getZ()+timing)
        
        fr = self.cog.getFrameRate('landing')
        animTimeInAir = 28 / fr
        
        mupSeq = Parallel(
                            Parallel(
                                     ActorInterval(self.cog,'landing',playRate=pr),
                                     ActorInterval(self.propeller,'x',playRate=-1),
                                    ),
                            Sequence(
                                     Wait(.1),
                                     self.cog.posInterval(timing/8,pos2,startPos=pos)
                                    )
                            )
        mupSeq.start(ts)
        
    def exitFlyAway(self):
        self.propeller.cleanup()
        self.propeller.removeNode()
    
    @staticmethod
    def makeWalkSequence(points,cog):
        def _angle(p1,p2):
            p1 = Vec3(p1)
            p2 = Vec3(p2)
            
            map(lambda x:x.setZ(0),(p1,p2))
            map(Vec3.normalize,(p1,p2))
            
            return p1.angleDeg(p2)
            
        s = Sequence()
        for i in xrange(len(points)):
            #if i+1>len(points): break
            
            curp = Vec3(points[i])
            
            nextp = Vec3(points[(i+1)%len(points)])
            d = (curp-nextp).length()
            t = d/8
            
            h = _angle(curp,nextp)
            
            #print curp,nextp,d,t,h
            
            s.append(
                     Parallel(
                               Func(cog.lookAt,*nextp),
                               cog.posInterval(t,nextp,startPos=curp),
                              )
                    )
            
            
        curp = Vec3(points[0])
        nextp = Vec3(points[1])
        d = (curp-nextp).length()
        t = d/8
        h = _angle(curp,nextp)
        
        #s.append(Parallel(Func(cog.lookAt,*nextp),cog.posInterval(t,nextp,startPos=curp)))
        #print s
        
        return s
        
    def enterOff(self,*args): pass
    def exitOff(self): pass
        
    def __del__(self):
        #print 'deleting fsm of',self.cog.getName()
        self.request('Off')
    
def getFSM(*args):
    return BasicCogFSM