from direct.distributed.ClockDelta import globalClockDelta

from tth.distributed import AsyncUtil

from tth.cogs.CogStates import BasicCogFSM
from tth.cogs import CogDNA

from tth.book.DisguisePage import getCogName

from panda3d.core import NodePath, Point3

import random, string

from direct.showbase.DirectObject import *

class PathUtil:
    def __init__(self,points):
        self.np = NodePath("dummy")
        self.points = points
        
        self.seq = BasicCogFSM.makeWalkSequence(points,self.np)
        self.dur = self.seq.getDuration()
        
    def seqCopy(self):
        newNp = NodePath('dummy_new')
        return newNp,BasicCogFSM.makeWalkSequence(self.points,newNp)
        
    def __iterIvals(self,ivals,target):
        s = 0
        for ival in ivals:
            s += ival.getDuration()
            if s >= target:
                i = ival
                i2 = ivals[(ivals.index(ival)+1)%len(ivals)]
                break
            
        p1 = repr(i.ivals[1]).split()[-5:-2]
        p1p = Point3(*map(float,p1))
        
        p2 = Point3(*map(float,repr(i2.ivals[1]).split()[-5:-2]))
        
        self.np.setPos(p1p)
        self.np.lookAt(p2)
        h = [str(self.np.getH())]
        self.np.iPosHpr()
            
        return (s,','.join(p1+h))
        
    def t2pos(self,t):
        ivals = list(self.seq.ivals)
        return self.__iterIvals(ivals,t)
        
class CogMaker(DirectObject):
    verbose = 0
    def __init__(self,zoneMgr,zoneId,cogDeptRatio=(.25,.25,.25,.25),cogTotalAvarage=10,
                 levelRange=(1,3),maxDiff=2,wannaBuildingOnly = False):
        self.zoneMgr = zoneMgr
        self.zoneId = zoneId
        
        self.curCogs = []
        self.ratio = cogDeptRatio
        self.total = cogTotalAvarage
        self.levelRange = levelRange
        self.maxDiff = maxDiff
        self.wannaBuildingOnly = wannaBuildingOnly
        
        assert sum(self.ratio) == 1
        
        self.points = []
        self.time = 0
        
        assert not (self.levelRange[0]>10 and not wannaBuildingOnly)
        
        taskMgr.doMethodLater(4,self.monitorTask,"cog monitor of zone "+str(self.zoneId))
        self.accept("makeCogAt"+str(self.zoneId),self.makeCog)
        self.accept("cogOverflowAt"+str(self.zoneId),self.getRidOfCog)
        
    @AsyncUtil.locked
    def getNextDept(self):
        if 1 in self.ratio: return self.ratio.index(1)
            
        depts = {0:0,1:0,2:0,3:0}
        #print 'generating dept'
        for x in self.curCogs:
            dept = x.dna.dept
            if not dept in depts: depts[dept] = 0
            depts[dept] += 1
              
        r = []
        for i,rt in zip(range(4),self.ratio):
            R = (float(depts[i])/max(1,len(self.curCogs)))
            D = R-rt
            if rt == 0: D = 2**30 #never
            r.append(D)
            
        m = min(r)
        return r.index(m)
        
    @AsyncUtil.locked
    def getNextPoint(self):
        def _isValid(all,needle,MINDIST = 8):
            alls = all[:]
            alls.sort(key=float)
            
            if needle == -1: return False #default value, kinda asking to fail this test
    
            smallers = [x for x in alls if x<needle]
            largers = [x for x in alls if x>needle]
    
            if smallers:
                ds =  needle - smallers[-1]
                #print '\tDS:',ds
                if ds < MINDIST: return False
        
            if largers:
                dl = largers[0] - needle
                #print '\tDL:',dl
                if dl < MINDIST: return False
    
            return True
    
        x = map(lambda a:a-3,filter(None,map(lambda b: b.getPos()[0],self.curCogs)))
        
        p = -1
        attemps = 0
        maxatt = 10
        
        while not _isValid(x,p) and attemps <= maxatt:
            #print p,'is invalid'
            p,pos = self.pathMgr.t2pos(random.randint(10,int(self.time-10))) #already fixed
            attemps += 1
            
        return p,pos
        
        #old method
        #causes cogs in law hq to walk in circles like in a ritual
        #idea: good for a "cogs gone crazy" event, to launch lawbot fo LOL
        MAX_OPTS = 2
        
        if len(x)<2: return len(x)*5+15
        
        x.insert(0,0)
        x.insert(-1,self.time)
        x.sort(key=float)
        #print "X:",x

        r = []
        for i in xrange(len(x)-1):
            #print i,x[i],x[i+1],x[i+1]-x[i]
            dt = round(x[i+1]-x[i],2)
            r.append(max(dt,-dt))
    
        #print "RES:",r

        r = list(r)
        #print "R:",r

        sr = r[:]
        sr.sort(key=float)
        #print "SR:",sr

        points = []

        for blah in xrange(1,min(1,len(sr))+1): points.append(r.index(sr[-blah]))

        #print "POINTS:",points

        return random.choice([max(n,-n) for n in map(lambda k:(x[k]+x[k+1])/2.,points)])
        
    def setPoints(self,points):
        self.points = points
        self.pathMgr = PathUtil(points)
      
    @AsyncUtil.threaded      
    def makeCog(self):
        if self.verbose: print 'making a cog at',self.zoneId
        
        dept = self.getNextDept()

        level = random.randint(*self.levelRange)
               
        #make index
        minIndex = max(0,level-5)
        _maxIndex = (5,7)[self.wannaBuildingOnly]
        maxIndex = min(_maxIndex,level-1)
                        
        if minIndex > maxIndex:
            print 'Warning from',self,': min index > max index, ignoring...'
            return
        
        index = random.randint(minIndex, maxIndex)
        
        if self.verbose:
            print '\tIndex range:',(minIndex,maxIndex)
            print '\tDept, index, level, name:',(dept,index,level,getCogName(dept*8+index))
        
        dna = CogDNA.randomDna(dept=dept,level=level-index,index=index)
        
        btime = self.getNextPoint() #random.randint(20,int(self.time-20))
        ftime,posStr = btime #self.pathMgr.t2pos(btime)
        wtime = globalClock.getFrameTime()+ftime
        ntime = globalClockDelta.localToNetworkTime(wtime,bits=32)
        
        if self.verbose:
            print '\tDNA Mask:',dna.encode('hex')
            print '\tWalk Time (base, local and network) and path pos:',(ftime,wtime,ntime),posStr
            print
        
        cog = base.air.createDistributedObject(className="DistributedCogAI",zoneId=self.zoneId)
        cog.setDNA(dna)
        
        flyTime = globalClockDelta.localToNetworkTime(globalClock.getFrameTime(),bits=32)        
        cog.setState("FlyIn",posStr,flyTime)
        taskMgr.doMethodLater(3.05,lambda t:self.__walk(cog,ftime),"cogWalk_"+str(dna))
        
        self.curCogs.append(cog)
      
    @AsyncUtil.threaded
    def getRidOfCog(self):
        for x in self.curCogs:
            if x.state[0] == "Walk":
                print "getting rid of cog %s at %s" % (x.doId,self.zoneId)
                x.setState("FlyAway","0,0,0,0")
                taskMgr.doMethodLater(4,lambda t:base.air.sendDeleteMsg(x.doId),"destroy cog")
                break
        
    def __walk(self,cog,t):
        t += globalClock.getFrameTime()
        cog.setState("Walk",self.pathMgr.seqCopy(),globalClockDelta.localToNetworkTime(t,bits=32))
        
    def monitorTask(self,task):
        totalCogs = len(self.curCogs)
        
        if abs(totalCogs-self.total) >= self.maxDiff:
            self.makeCog()#bool(totalCogs-self.total>0))
                
        return task.again