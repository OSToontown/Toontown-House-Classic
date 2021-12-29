from direct.distributed.PyDatagram import PyDatagram as PyDG
from direct.distributed.PyDatagramIterator import PyDatagramIterator as PyDGIter

import random

'''
attributes:

name: type, values

dept: uint8, 0-3
lives: uint8, 1 or 2 (2 = v2.0 cog,1 = normal)
leader: unit8, 0-7
level: uint8, 1-12
isWaiter: bool, true or false (of course -_-)
isSkel: bool, true or false (of course -_-)

default: a level 1 flunky (v 1.0)

'''

class CogDNA:
    dpets = range(4)
    leaders = range(8)
    levels = range(1,13)
    maxLives = 2
    
    DGSize = 6
    
    def __init__(self):
        self.dept = 0
        self.lives = 1
        self.leader = 0
        self.level = 1
        self.isWaiter = False
        self.isSkel = False
        
    def isValidDept(self,dp): return dp in self.dpets
    def isValidLevel(self,level): return level in self.levels
    def isValidLeader(self,ld): return ld in self.leaders
    def isValidLives(self,lvs): return lvs <= self.maxLives
    
    def isValidData(self,data):
        return len(data) == self.DGSize
    
    def make(self):
        dg = PyDG()
        dg.addUint8(self.dept)
        dg.addUint8(self.leader)
        dg.addUint8(self.level)
        dg.addUint8(self.lives)
        dg.addBool(self.isWaiter)
        dg.addBool(self.isSkel)
        
        return dg.getMessage()
        
    def makeFrom(self,data):
        if not self.isValidData(data):
            raise ToontownHouseError("CogDNA 0x000: bad data for dna")
        
        dg = PyDG()
        dg.appendData(data)
        dgi = PyDGIter(dg)
        
        self.dept = dgi.getUint8()
        self.leader = dgi.getUint8()
        self.level = dgi.getUint8()
        self.lives = dgi.getUint8()
        self.isWaiter = dgi.getBool()
        self.isSkel = dgi.getBool()
        
def randomDna(**rules):
    s = ''
    
    #dept
    s += chr(rules.get("dept",random.choice(CogDNA.dpets)))
    
    #leader
    index = rules.get("index",random.choice(CogDNA.leaders))
    s += chr(index)
    
    #level (matches leader rule)
    s += chr(rules.get("level",random.randint(1,5))+index)
    
    #lives (v X.0)
    s += chr(rules.get("lives",1))
    
    #waiter / skel
    s += chr(bool(rules.get("isWaiter",False)))
    s += chr(bool(rules.get("isSkel",False)))
    
    return s