import random

try:
    NAMES_FILE_PATH = L10N.NAMES_FILE_PATH
except:
    NAMES_FILE_PATH = 'data/etc/languages/names_en.l10n'

TITLE_M = '0'
TITLE_F = '1'
TITLE_NEUTRAL = '2'
FIRST_NAME_M = '3'
FIRST_NAME_F = '4'
FIRST_NAME_NEUTRAL = '5'
CAP_PREFIX = '6'
LAST_NAME_PREFIX = '7'
LAST_NAME_SUFFIX = '8'

class NamePattern:

    def __init__(self, filepath=NAMES_FILE_PATH):
        names = (
            line.strip().split('*')
            for line in open(filepath, 'r').readlines()
            if not line.startswith('#')
        )
        self.nameDict = {}
        self.idDict = {}
        for nameId, part, name in names:
            self.nameDict.setdefault(part, []).append(name)
            self.idDict.setdefault(part, {})
            self.idDict[part][name] = nameId
        for part in self.nameDict:
            self.nameDict[part].sort()

    def fetchAll(self, gender, part=None):
        if part == 'title':
            titleKey = TITLE_M if gender == 'm' else TITLE_F
            return self.nameDict[titleKey] + self.nameDict[TITLE_NEUTRAL]
        elif part == 'first':
            firstNameKey = FIRST_NAME_M if gender == 'm' else FIRST_NAME_F
            return (self.nameDict[firstNameKey] +
                    self.nameDict[FIRST_NAME_NEUTRAL])
        elif part == 'last-prefix':
            return self.nameDict[CAP_PREFIX] + self.nameDict[LAST_NAME_PREFIX]
        elif part == 'last-suffix':
            return self.nameDict[LAST_NAME_SUFFIX]

    def generateRandomToonName(self, gender):
        titlePart = None
        if random.random() > 0.5:
            titles = self.fetchAll(gender, 'title')
            titlePart = random.randint(0, len(titles) - 1)
        firsts = self.fetchAll(gender, 'first')
        firstPart = random.randint(0, len(firsts) - 1)
        lastPrefixPart = None
        lastSuffixPart = None
        if random.random() > 0.5:
            lastPrefixes = self.fetchAll(gender, 'last-prefix')
            lastPrefixPart = random.randint(0, len(lastPrefixes) - 1)
            lastSuffixes = self.fetchAll(gender, 'last-suffix')
            lastSuffixPart = random.randint(0, len(lastSuffixes) - 1)
        return (titlePart, firstPart, lastPrefixPart, lastSuffixPart)

    def getNameString(self, gender, nameParts):
        (titlePart, firstPart, lastPrefixPart, lastSuffixPart) = nameParts
        if titlePart:
            titles = self.fetchAll(gender, 'title')
            titlePart = titles[titlePart]
        else:
            titlePart = ''
        firsts = self.fetchAll(gender, 'first')
        firstPart = firsts[firstPart]
        if lastPrefixPart and lastSuffixPart:
            lastPrefixes = self.fetchAll(gender, 'last-prefix')
            lastPrefixPart = lastPrefixes[lastPrefixPart]
            lastSuffixes = self.fetchAll(gender, 'last-suffix')
            lastSuffixPart = lastSuffixes[lastSuffixPart]
        else:
            lastPrefixPart = ''
            lastSuffixPart = ''
        name = (titlePart + ' ' + firstPart + ' ' +
                lastPrefixPart + lastSuffixPart)
        return unicode(name.decode('latin-1').strip()).replace('\n', '')

    def getStringParts(self, gender, nameParts):
        (titlePart, firstPart, lastPrefixPart, lastSuffixPart) = nameParts
        if titlePart:
            titles = self.fetchAll(gender, 'title')
            titlePart = titles[titlePart]
        else:
            titlePart = ''
        firsts = self.fetchAll(gender, 'first')
        firstPart = firsts[firstPart]
        if lastPrefixPart and lastSuffixPart:
            lastPrefixes = self.fetchAll(gender, 'last-prefix')
            lastPrefixPart = lastPrefixes[lastPrefixPart]
            lastSuffixes = self.fetchAll(gender, 'last-suffix')
            lastSuffixPart = lastSuffixes[lastSuffixPart]
        else:
            lastPrefixPart = ''
            lastSuffixPart = ''
        return [titlePart, firstPart, lastPrefixPart, lastSuffixPart]

    def getNameId(self, namePart, nameString):
        parts = self.fetchAll('m', namePart) + self.fetchAll('f', namePart)
        parts.sort()
        return parts.index(nameString)

if __name__ == '__main__':
    namePattern = NamePattern('../../' + NAMES_FILE_PATH)
    gender = random.choice(('m', 'f'))
    print 'Gender:', 'Male' if gender == 'm' else 'Female'
    nameParts = namePattern.generateRandomToonName(gender)
    print 'Name Parts:', nameParts
    print 'Name String:', namePattern.getNameString(gender, nameParts)
    print "'Sir' Title ID: %d" % namePattern.getNameId('title', 'Sir')