import FishingGlobals, struct
from direct.directnotify import DirectNotifyGlobal
from direct.actor.Actor import Actor

class Fish(Actor):

    notify = DirectNotifyGlobal.directNotify.newCategory('FishBase')

    def __init__(self, species, subIndex, weight):
        self.species = species
        self.subIndex = subIndex
        self.weight = weight
        
        Actor.__init__(self,*self.getActor())

    def getSubIndex(self):
        return self.subIndex
        
    def getSpecies(self):
        return self.species

    def getWeight(self):
        return self.weight

    def setWeight(self, weight):
        self.weight = weight

    def getVitals(self):
        return (self.species, self.subIndex, self.weight)

    def getValue(self):
        return FishingGlobals.getValue(*self.getVitals())

    def getSpeciesName(self):
        return L10N.FishNames[self.species][self.subIndex]

    def getRarity(self):
        return FishingGlobals.getRarity(self.species, self.subIndex)

    def getPhase(self):
        dict = FishingGlobals.FishFileDict
        fileInfo = dict.get(self.species)
        return fileInfo[0]

    def getActor(self):
        prefix = 'phase_%s/models/char/' % self.getPhase()
        dict = FishingGlobals.FishFileDict
        fileInfo = dict.get(self.species)
        actor = (prefix + fileInfo[1], {'intro': prefix + fileInfo[2],
         'swim': prefix + fileInfo[3]})
        return actor

    def getSound(self):
        sound = None
        loop = None
        delay = None
        playRate = None
        if base.config.GetBool('want-fish-audio', 1):
            soundDict = FishingGlobals.FishAudioFileDict
            fileInfo = soundDict.get(self.species, None)
            if fileInfo:
                prefix = 'phase_%s/audio/sfx/' % self.getPhase()
                sound = loader.loadSfx(prefix + soundDict[self.species][0])
                loop = soundDict[self.species][1]
                delay = soundDict[self.species][2]
                playRate = soundDict[self.species][3]
        return (sound,
         loop,
         delay,
         playRate)

    def __str__(self):
        return '%s, weight: %s value: %s' % (self.getSpeciesName(), self.weight, self.getValue())
        
    def makeNetString(self):
        s = ""
        s += chr(self.species)
        s += chr(self.subIndex)
        s += struct.pack("f",self.weight)
        return s
       
    @classmethod
    def makeFromNetString(cls,data):
        spc = ord(data[0])
        si = ord(data[1])
        w = struct.unpack("f",data[2:])[0]
        return cls(spc,si,w)
        
    def copy(self):
        st = self.makeNetString()
        return self.__class__.makeFromNetString(st)
        
        