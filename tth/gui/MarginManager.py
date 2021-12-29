from pandac.PandaModules import *
from direct.showbase.DirectObject import DirectObject
from MarginCell import *
import random

CellW = .4
CellH = .2
CellPadding = .025

cells = (

#left cells
(
(CellW/2.+CellPadding,.4),
(CellW/2.+CellPadding,.6),
(CellW/2.+CellPadding,.8),
(CellW/2.+CellPadding,1),
(CellW/2.+CellPadding,1.2),
(CellW/2.+CellPadding,1.4),
(CellW/2.+CellPadding,1.6),
),

#right cells
(
(-CellW/2.-CellPadding,.4),
(-CellW/2.-CellPadding,.6),
(-CellW/2.-CellPadding,.8),
(-CellW/2.-CellPadding,1),
),
)

HorRange = (.15,.87)

class MarginManager(DirectObject):
    def __init__(self):
        self.sidecells = set()
        self.horcells = [[],[]] #this is important enough to have an order
        lefts, rights  = cells
        
        for c in lefts: self.sidecells.add(MarginCell(self,base.a2dBottomLeft,(CellW,CellH),0,*c))
        for c in rights: self.sidecells.add(MarginCell(self,base.a2dBottomRight,(CellW,CellH),1,*c))
        
        self.horParent = base.a2dBottomLeft.attachNewNode('margin manager hor placholder')
        if '--showcells' in sys.argv: self.horParent.assign(DirectFrame(frameSize = (-.1,.1,-.1,.1),frameColor = (1,1,1,.7)))
        self.horParent.setY(-1)
        
        self._generateHorCells()
        self.accept('window-event',self.__windowEv)
        
    def _getMaxHorCells(self, asp):
        maxc = int((2*(asp)/CellW) * (HorRange[1]-HorRange[0]))
        return maxc
        
    def _generateHorCells(self):
        asp = base.getAspectRatio()
        mc = self._getMaxHorCells(asp)
           
        #assert len(self.horcells[0]) == len(self.horcells[1])
        if len(self.horcells[0]) == mc:
            print 'mcMgr: ignoring hor update (max equals to current: %d for aspect %s)' % (mc,asp)
            return
            
        if len(self.horcells[0]) > mc: self._horOverflow(0,mc,asp)
        if len(self.horcells[1]) > mc: self._horOverflow(1,mc,asp)

        rt = -asp + (HorRange[0]*asp) + (CellW)
        __range = (len(self.horcells[0]),mc)
        
        self._reposHor(self.horcells[0],rt)
        self._reposHor(self.horcells[1],rt)
        
        print 'mcMgr: gonna generate extra hor cells (from %d to %d)' % __range
        for i in xrange(*__range):
            print 'mcMgr: generate extra hor cell (index = %d)' % i
            _x = rt + i * (CellW+CellPadding)
            
            self.horcells[0].append(MarginCell(self,self.horParent,(CellW,CellH),2,_x,.85)) #aspect2d
            self.horcells[1].append(MarginCell(self,self.horParent,(CellW,CellH),3,_x,-.85))

    def _reposHor(self, nc, rt):
        for i,c in enumerate(nc):
            print 'mcMgr: repos hor cell (index = %d)' % i
            c.setX(rt + i * (CellW+CellPadding))
            
    def _horOverflow(self,index,nmax,asp):
        print 'mcMgr: hor overflow at index %d, max is %d' % (index,nmax)
        nc = filter(lambda x: not x.isFree(), self.horcells[index])[:nmax]
        
        for c in self.horcells[index]:
            if not c in nc:
                c.destroy()
                
        #now repos them
        rt = -asp + (HorRange[0]*asp) + (CellW)
        self._reposHor(nc,rt)
                
        self.horcells[index] = nc
        
    def __windowEv(self,*_):
        print 'mcMgr: window ev detected', base.getAspectRatio()
        self._generateHorCells()
        
    def allocate(self,amount = 1):
        allc = self.horcells[0]+self.horcells[1]+list(self.sidecells)
        random.shuffle(allc)
        possible = filter(MarginCell.isFree, allc)
        possible = possible[:min(len(possible),amount)]
        
        map(MarginCell.allocate,possible)
        
        random.shuffle(possible)
        return possible