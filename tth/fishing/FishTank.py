from Fish import *

class FishHistory:
    species = FishingGlobals.FishLocationDict.keys()
    totalSpecies = len(FishingGlobals.FishLocationDict.keys())
    subindexesBySpecies = map(len,FishingGlobals.FishLocationDict.values())
    
    spcKeys = []
    for spc in species:
        for i in xrange(subindexesBySpecies[spc]):
            spcKeys.append((spc,i))
            
    NeverCaught = -1
    
    NewFish = 1
    NewRecord = 2
    Nothing = 3
    
    def __init__(self,stream):
        self.stream = stream
        self.historyData = stream.read("fishHistory",{})
        self.__fix()
        
    def __fix(self):
        for key in self.spcKeys:
            if not key in self.historyData:
                self.historyData[key] = self.NeverCaught
                
        self.stream.write('fishHistory',self.historyData)
        
    def compareFish(self,fish):
        spc,subindex,wg = fish.getVitals()
        code = self.historyData[(spc,subindex)]
        
        if code == -1: return self.NewFish
        elif wg > code: return self.NewRecord
        return self.Nothing
        
    def compareTank(self,tank):
        newRecords = set()
        newSpecies = set()
        
        def __efd(f):
            return f.getVitals()[:-1]
        
        for fish in tank.fishes:
            cp = self.compareFish(fish)
            if cp == self.NewFish: newSpecies.add(__efd(fish))
            elif cp == self.NewRecord: newRecords.add(__efd(fish))
            
        return map(len,(newRecords,newSpecies))
        
    def addFish(self,fish):
        if self.compareFish(fish) == self.Nothing:
            return
            
        spc,subindex,wg = fish.getVitals()
        self.historyData[(spc,subindex)] = wg
        
    def addTank(self,tank):
        for fish in tank.fishes:
            self.addFish(fish)
            
    def getTotalSpecies(self):
        return len(filter(lambda x:x != self.NeverCaught,self.historyData.values()))
            
    def save(self):
        self.stream.write("fishHistory",self.historyData)
        
class FishTank:
    maxSize = 20
    def __init__(self,stream):
        self.stream = stream
        self.tankData = stream.read("fishTank",[])
        self.fishes = []
        self.loadTank()
        
    def loadTank(self):
        for data in self.tankData:
            self.fishes.append(Fish.makeFromNetString(data))
            
    def addFish(self,fish):
        dna = fish.makeNetString()
        self.fishes.append(Fish.makeFromNetString(dna)) #just copy the fish, so it can be deleted later
        
        self.tankData = map(Fish.makeNetString,self.fishes)
        
        #print 'Added fish',fish,self.tank
        self.stream.write("fishTank",self.tankData)
        messenger.send("fishTankChanged",[len(self)])
        
    def getTotalJbs(self):
        return sum(map(Fish.getValue,self.fishes))
        
    def sellAll(self):
        messenger.send('incomeMoney',[self.getTotalJbs()])
        self.tankData = []
        self.fishes = []
        self.stream.write("fishTank",self.tankData)
        
    def __repr__(self):
        s = "Fishing Tank (%d fishes currently)\n" % len(self.fishes)
        for fish in self.fishes:
            s += '\t'+str(fish)+'\n'
            
        s += "----------------\n"
        s += "Total value: %d jellybean(s)" % self.getTotalJbs()
            
        return s
        
    def __len__(self):
        return len(self.fishes)
        
    def isFull(self):
        return len(self) >= self.maxSize
        
def makeLocalTank():
    return FishTank(gamebase.toonAvatarStream)
    
def makeLocalHistory():
    return FishHistory(gamebase.toonAvatarStream)