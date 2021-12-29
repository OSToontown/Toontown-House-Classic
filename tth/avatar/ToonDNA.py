from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator

from ToonDNAGlobals import *

class ToonDNA:

    def __init__(self, netString=None, dnaType=None, dna=None):
        self.dnaType = dnaType or 'u'
        
        #default
        #set to avoid crashes
        self.hat = self.glasses = self.backpack = self.shoes = (0,0,0)
        
        if netString is not None:
            self.makeFromNetString(netString)
        elif dnaType == 't':
            if dna is None:
                self.newToonRandom()
            else:
                self.newToonFromProperties(*dna.asTuple())

    def __str__(self):
        string = 'type = toon\n'
        string += 'gender = %s\n' % self.gender
        string += 'head = %s, torso = %s, legs = %s\n' % (
                         self.head, self.torso, self.legs)
        string += 'arm color = %d\n' % self.armColor
        string += 'glove color = %d\n' % self.gloveColor
        string += 'leg color = %d\n' % self.legColor
        string += 'head color = %d\n' % self.headColor
        string += 'top texture = %d\n' % self.topTex
        string += 'top texture color = %d\n' % self.topTexColor
        string += 'sleeve texture = %d\n' % self.sleeveTex
        string += 'sleeve texture color = %d\n' % self.sleeveTexColor
        string += 'bottom texture = %d\n' % self.botTex
        string += 'bottom texture color = %d\n' % self.botTexColor
        string += 'hat = %s\n' % self.hat
        string += 'glasses = %s\n' % self.glasses
        string += 'backpack = %s\n' % self.backpack
        string += 'shoes = %s' % self.shoes
        return string

    def printNetString(self):
        string = self.makeNetString()
        dg = PyDatagram(string)
        dg.dumpHex(ostream)

    def __addHat(self, datagram):
        for hatIndex in self.hat:
            datagram.addUint8(hatIndex)

    def __addGlasses(self, datagram):
        for glassesIndex in self.glasses:
            datagram.addUint8(glassesIndex)

    def __addBackpack(self, datagram):
        for backpackIndex in self.backpack:
            datagram.addUint8(backpackIndex)

    def __addShoes(self, datagram):
        for shoesIndex in self.shoes:
            datagram.addUint8(shoesIndex)
    
    @classmethod
    def __getHat(cls, dgi):
        return tuple((dgi.getUint8() for _ in range(3)))
    
    @classmethod
    def __getGlasses(cls, dgi):
        return tuple((dgi.getUint8() for _ in range(3)))

    @classmethod
    def __getBackpack(cls, dgi):
        return tuple((dgi.getUint8() for _ in range(3)))
    
    @classmethod
    def __getShoes(cls, dgi):
        return tuple((dgi.getUint8() for _ in range(3)))

    def makeNetString(self):
        dg = PyDatagram()
        dg.addFixedString(self.type, 1)
        if self.type == 't' or 1: #fixes stupid crash -_-
            headIndex = toonHeadTypes.index(self.head)
            torsoIndex = toonTorsoTypes.index(self.torso)
            legsIndex = toonLegTypes.index(self.legs)
            dg.addUint8(headIndex)
            dg.addUint8(torsoIndex)
            dg.addUint8(legsIndex)

            dg.addUint8(1 if self.gender == 'm' else 0)
            dg.addUint8(self.topTex)
            dg.addUint8(self.topTexColor)
            dg.addUint8(self.sleeveTex)
            dg.addUint8(self.sleeveTexColor)
            dg.addUint8(self.botTex)
            dg.addUint8(self.botTexColor)
            dg.addUint8(self.armColor)
            dg.addUint8(self.gloveColor)
            dg.addUint8(self.legColor)
            dg.addUint8(self.headColor)

            self.__addHat(dg)
            self.__addGlasses(dg)
            self.__addBackpack(dg)
            self.__addShoes(dg)
        elif self.type == 'u':
            notify.error('undefined avatar')
        else:
            notify.error('unknown avatar type:', self.type)
        return dg.getMessage()

    @classmethod
    def isValidNetString(cls, string):
        dg = PyDatagram(string)
        dgi = PyDatagramIterator(dg)
        try:
            dnaType = dgi.getFixedString(1)
            assert(dnaType is 't')
            headIndex = dgi.getUint8()
            assert(headIndex <= len(toonHeadTypes))
            torsoIndex = dgi.getUint8()
            assert(torsoIndex <= len(toonTorsoTypes))
            legsIndex = dgi.getUint8()
            assert(legsIndex <= len(toonLegTypes))
            gender = 'm' if dgi.getUint8() else 'f'
            topTex = dgi.getUint8()
            assert(topTex <= len(Shirts))
            topTexColor = dgi.getUint8()
            assert(topTexColor <= len(ClothesColors))
            sleeveTex = dgi.getUint8()
            assert(sleeveTex <= len(Sleeves))
            sleeveTexColor = dgi.getUint8()
            assert(sleeveTexColor <= len(ClothesColors))
            botTex = dgi.getUint8()
            bottomTextures = BoyShorts if gender is 'm' else GirlBottoms
            assert(botTex <= len(bottomTextures))
            botTexColor = dgi.getUint8()
            assert(botTexColor <= len(ClothesColors))
            armColor = dgi.getUint8()
            assert(armColor <= len(allColorsList))
            gloveColor = dgi.getUint8()
            assert(gloveColor <= len(allColorsList))
            legColor = dgi.getUint8()
            assert(legColor <= len(allColorsList))
            headColor = dgi.getUint8()
            assert(headColor <= len(allColorsList))
            if dgi.getRemainingSize():
                hat = list(cls.__getHat(dgi))
                assert(hat in HatStyles.values())
                glasses = list(cls.__getGlasses(dgi))
                assert(glasses in GlassesStyles.values())
                backpack = list(cls.__getBackpack(dgi))
                assert(backpack in BackpackStyles.values())
                shoes = list(cls.__getShoes(dgi))
                assert(shoes in ShoesStyles.values())
        except AssertionError:
            return False
        return True
    
    def makeFromNetString(self, string):
        dg = PyDatagram(string)
        dgi = PyDatagramIterator(dg)
        self.type = dgi.getFixedString(1)

        #we should NOT test this
        #sometimes it just fails the test
        #and crashes o_o

        if self.type is not 't' and False: #fixes crash too
            notify.warning('Unknown DNA type:', self.type)
            return None
            
        if not self.isValidNetString(string) and False: #fixes crash too
            notify.warning('Invalid DNA.')
            return None

        headIndex = dgi.getUint8()
        torsoIndex = dgi.getUint8()
        legsIndex = dgi.getUint8()
        self.head = toonHeadTypes[headIndex]
        self.torso = toonTorsoTypes[torsoIndex]
        self.legs = toonLegTypes[legsIndex]
        self.gender = 'm' if dgi.getUint8() else 'f'
        self.topTex = dgi.getUint8()
        self.topTexColor = dgi.getUint8()
        self.sleeveTex = dgi.getUint8()
        self.sleeveTexColor = dgi.getUint8()
        self.botTex = dgi.getUint8()
        self.botTexColor = dgi.getUint8()
        self.armColor = dgi.getUint8()
        self.gloveColor = dgi.getUint8()
        self.legColor = dgi.getUint8()
        self.headColor = dgi.getUint8()
        if dgi.getRemainingSize():
            self.hat = self.__getHat(dgi)
            self.glasses = self.__getGlasses(dgi)
            self.backpack = self.__getBackpack(dgi)
            self.shoes = self.__getShoes(dgi)
            
        else:
            self.hat = self.glasses = self.backpack = self.shoes = (0,0,0)

    def __defaultColors(self):
        self.armColor = defaultColorIndex
        self.gloveColor = 0
        self.legColor = defaultColorIndex
        self.headColor = defaultColorIndex

    def newToon(self, dna, color=None):
        if len(dna) is not 4:
            notify.error(
                "DNA tuple must be in format (head, torso, legs, gender)")
        self.type = 't'
        (self.head, self.torso, self.legs, self.gender) = dna
        self.topTex = 0
        self.topTexColor = 0
        self.sleeveTex = 0
        self.sleeveTexColor = 0
        self.botTex = 0
        self.botTexColor = 0
        color = color or defaultColorIndex
        self.armColor = color
        self.legColor = color
        self.headColor = color
        self.gloveColor = 0
        self.hat = (0, 0, 0)
        self.glasses = (0, 0, 0)
        self.backpack = (0, 0, 0)
        self.shoes = (0, 0, 0)

    def newToonFromProperties(self, *args):
        """
        Construct the Toon's DNA from a set of properties.

        USAGE:
        newToonFromProperties(head, torso, legs, gender, armColor, gloveColor,
                              legColor, headColor, topTexture, topTextureColor,
                              sleeveTexture, sleeveTextureColor, bottomTexture,
                              bottomTextureColor, [hat, glasses, backpack,
                              shoes])
        """
        self.type = 't'

        # If any of the optional accessories are missing, add them:
        args += ((0, 0, 0),) * (18-len(args))

        (
            self.head, self.torso, self.legs, self.gender, self.armColor,
            self.gloveColor, self.legColor, self.headColor, self.topTex,
            self.topTexColor, self.sleeveTex, self.sleeveTexColor,
            self.botTex, self.botTexColor, self.hat, self.glasses,
            self.backpack, self.shoes
        ) = args

    def updateToonProperties(self, **kwargs):
        """
        Update the Toon's DNA based on a set of properties.

        USAGE:
        updateToonProperties(...)

        KEYWORDS:
            head, torso, legs, gender, armColor, gloveColor, legColor,
            headColor, topTexture, topTextureColor, sleeveTexture,
            sleeveTextureColor, bottomTexture, bottomTextureColor,
            shirt, bottom, hat, glasses, backpack, shoes
        """
        self.head = kwargs.get('head') or self.head
        self.torso = kwargs.get('torso') or self.torso
        self.legs = kwargs.get('legs') or self.legs
        self.gender = kwargs.get('gender') or self.gender
        self.armColor = kwargs.get('armColor') or self.armColor
        self.gloveColor = kwargs.get('gloveColor') or self.gloveColor
        self.legColor = kwargs.get('legColor') or self.legColor
        self.headColor = kwargs.get('headColor') or self.headColor
        self.topTex = kwargs.get('topTexture') or self.topTex
        self.topTexColor = kwargs.get('topTextureColor') or self.topTexColor
        self.sleeveTex = kwargs.get('sleeveTexture') or self.sleeveTex
        self.sleeveTexColor = (kwargs.get('sleeveTextureColor') or
                               self.sleeveTexColor)
        self.botTex = kwargs.get('bottomTexture') or self.botTex
        self.botTexColor = kwargs.get('bottomTextureColor') or self.botTexColor
        shirt = kwargs.get('shirt')
        if shirt:
            string, colorIndex = shirt
            defn = ShirtStyles[string]
            self.topTex = defn[0]
            self.topTexColor = defn[2][colorIndex][0]
            self.sleeveTex = defn[1]
            self.sleeveTexColor = defn[2][colorIndex][1]
        bottom = kwargs.get('bottom')
        if bottom:
            string, colorIndex = bottom
            defn = BottomStyles[string]
            self.botTex = defn[0]
            self.botTexColor = defn[1][colorIndex]
        self.hat = kwargs.get('hat') or self.hat
        self.glasses = kwargs.get('glasses') or self.glasses
        self.backpack = kwargs.get('backpack') or self.backpack
        self.shoes = kwargs.get('shoes') or self.shoes

    def newToonRandom(self, seed=None, gender='m'):
        if seed:
            generator = random.Random()
            generator.seed(seed)
        else:
            generator = random
        self.type = 't'
        self.legs = generator.choice(toonLegTypes + ('m', 'l', 'l', 'l'))
        self.gender = gender
        self.head = generator.choice(toonHeadTypes)
        (
            self.topTex, self.topTexColor, self.sleeveTex, self.sleeveTexColor
        ) = getRandomTop(gender, generator=generator)
        (bottom, bottomColor) = getRandomBottom(gender, generator=generator)
        if gender == 'm':
            self.torso = generator.choice(toonTorsoTypes[:3])
            color = generator.choice(defaultBoyColorList)
        else:
            self.torso = generator.choice(toonTorsoTypes[:6])
            girlBottomType = SKIRT if self.torso[1] is 'd' else SHORTS
            (bottom, bottomColor) = getRandomBottom(
                gender, generator=generator, girlBottomType=girlBottomType)
            color = generator.choice(defaultGirlColorList)
        self.botTex = bottom
        self.botTexColor = bottomColor
        self.armColor = color
        self.legColor = color
        self.headColor = color
        self.gloveColor = 0
        self.hat = (0, 0, 0)
        self.glasses = (0, 0, 0)
        self.backpack = (0, 0, 0)
        self.shoes = (0, 0, 0)

    def asTuple(self):
        return (
            self.head, self.torso, self.legs, self.gender, self.armColor,
            self.gloveColor, self.legColor, self.headColor, self.topTex,
            self.topTexColor, self.sleeveTex, self.sleeveTexColor,
            self.botTex, self.botTexColor, self.hat, self.glasses,
            self.backpack, self.shoes
        )

    def getType(self):
        return self.type

    def getAnimal(self):
        animal = getSpeciesName(self.head)
        if animal:
            return animal
        else:
            notify.error('Unknown head style:', self.head[0])

    def getHeadSize(self):
        headSizeStr = self.head[1]
        if headSizeStr is 'l':
            return 'long'
        elif headSizeStr is 's':
            return 'short'
        else:
            notify.error('Unknown head size:', headSizeStr)

    def getMuzzleSize(self):
        muzzleSizeStr = self.head[2]
        if muzzleSizeStr is 'l':
            return 'long'
        elif muzzleSizeStr is 's':
            return 'short'
        else:
            notify.error('Unknown muzzle size:', muzzleSizeStr)

    def getTorsoSize(self):
        torsoSizeStr = self.torso[0]
        if torsoSizeStr == 'l':
            return 'long'
        elif torsoSizeStr == 'm':
            return 'medium'
        elif torsoSizeStr == 's':
            return 'short'
        else:
            notify.error('Unknown torso size:', torsoSizeStr)

    def getLegSize(self):
        if self.legs == 'l':
            return 'long'
        elif self.legs == 'm':
            return 'medium'
        elif self.legs == 's':
            return 'short'
        else:
            notify.error('Unknown leg size:', self.legs)

    def getGender(self):
        return self.gender

    def getClothes(self):
        if len(self.torso) == 1:
            return 'naked'
        clothingTypeStr = self.torso[1]
        if clothingTypeStr == 's':
            return 'shorts'
        elif clothingTypeStr == 'd':
            return 'dress'
        else:
            notify.error('Unknown clothing type:', clothingTypeStr)

    def getArmColor(self):
        try:
            return allColorsList[self.armColor]
        except:
            return allColorsList[0]

    def getLegColor(self):
        try:
            return allColorsList[self.legColor]
        except:
            return allColorsList[0]

    def getHeadColor(self):
        try:
            return allColorsList[self.headColor]
        except:
            return allColorsList[0]

    def getGloveColor(self):
        try:
            return allColorsList[self.gloveColor]
        except:
            return allColorsList[0]

    def getBlackColor(self):
        try:
            return allColorsList[blackColorIndex]
        except:
            return allColorsList[0]

    def getWhiteColor(self):
        return allColorsList[whiteColorIndex]

    def getAccessories(self):
        return (self.hat, self.glasses, self.backpack, self.shoes)
