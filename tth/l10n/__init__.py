#Translation system
from random import choice
import locale, L10NLocalizer

class HackedDict: #prototype, not used
    def __init__(self):
        self.__it = []
        self.__vs = []
        
    def __setitem__(self,item,val):
        self.__it.append(item)
        self.__vs.append(val)
        
    def __getitem__(self,item):
        if not item in self.__it:
            raise KeyError(item)
            
        return self.__vs[self.__it.index(item)]
        
    def items(self): return self.__it[:]

findpath = lambda x,y: y+x

class CogSpeech:
    value = None
    index = None
    category = None

class l10n:
    def __init__(self,language,autoSet = 1):
        '''
        self.languages = {
                          'pt':'pt.l10n',
                          'en':'english.l10n',
                          'fr':'french.l10n', 
                          'jp':'japanese.l10n'  #broken ;-;
#						  'dog':'dog.l10n', #LOOOOOOOOOOOOL
                          }
        '''
        
        self.languages = {
                          'pt':'portuguese',
                          'en':'english',
                          'fr':'french', 
                          'jp':'japanese'
                          }
                          
        self._sleeve = None
        #self.fPrefix = '' #(fixed) #lol i fixed it myself before you.
        if autoSet: self.setLanguage(language)
	
    def buildDB(self):
        self.db = self.module.__dict__ #{}
        
        #f = open(findpath('data/etc/languages/'+self.languages[self.language],self.fPrefix),'rb')
        for line in self.module.OldData.replace('\r','\n').split('\n'):
            line = line.strip('\r\n')
            if not line or line.startswith('#'): continue
            _d = line.split('#',1)[0].split(' ',1)
            #print _d
            self.db[_d[0]] = unicode(_d[1])
        
    def sc_buildDB(self):
        self.sc_db = {}
        #f = open(findpath('data/etc/languages/speedchat_'+self.language.upper()+'.l10n',self.fPrefix),'rb')
        for line in self.module.SpeedChatData.replace('\r','\n').split('\n'):
            line = line.strip('\r\n')
            if not line or line.startswith('#'): continue
            _d = line.split('#',1)[0].split(' ',1)
            #print _d
            self.sc_db[_d[0]] = unicode(_d[1])

    def cog_buildDB(self):
        self.cog_db = {}
        #f = open(findpath('data/etc/languages/cogs_'+self.language.upper()+'.l10n',self.fPrefix),'rb')
        for line in self.module.CogData.replace('\r','\n').split('\n'):
            line = line.strip('\r\n')
            if not line or line.startswith('#'): continue
            category,index,_str = line.split('#',1)[0].split(' ',2)
            
            index = int(index)
            x = CogSpeech()
            x.category = category
            x.index = index
            x.value = unicode(_str)
            self.cog_db[index] = x
            
    def sc_fetch(self,_str):
        #print 'fetching',_str
        rs = []
        if _str.endswith("*"):
            for item,val in self.sc_db.items():
                if item.startswith(_str[:-1]):
                    rs.append((val,item))
        
        elif _str.endswith("%"):
            for item,val in self.sc_db.items():
                if item.startswith(_str[:-1]) and not '_' in item[len(_str):] and len(self.sc_fetch(item+"_*"))<=1:
                    #print 'L10N::_%',item,item[len(_str):]
                    rs.append((val,item))
                    
        else:
            if not _str in self.sc_db:
                print ":l10n:SC: Unknown: {0} (LANG={1})".format(_str,self.language)
                rs.append(u"L10N 0x001: NOT FOUND")
            else:
                rs.append((self.sc_db[_str],_str))
                
        return rs
        
    def cog_fetch(self,cat):
        for x in self.cog_db.values():
            if x.category == cat:
                yield (x.value,x.index)
        
    def getSleeveTexture(self):
        if self._sleeve: return self._sleeve
        country = locale.getdefaultlocale()[0][3:].lower()
        print ':L10N: Setting sleeve flag for',country
        self._sleeve = (country,loader.loadTexture("data/models/toons/sleeves/{0}.png".format(country)))
        return self._sleeve
            
    def tip(self): #returns a random tip in selected language
        messages=filter(None,self.module.TipData.split('\n'))
        if not messages:
            raise ToontownHouseError('L10N 0x002: NO TIPS AVAIABLE FOR '+self.language)
        
        return choice(messages)
	
    def cogSpeechAI(self,type,(dept,index)):
        if type == 1: #deny
            return choice(list(self.cog_fetch("BATTLE_DENY")))[-1]
            
        elif type == 2: #accept
            return choice(list(self.cog_fetch("BATTLE_ACCEPT_%s_%s" % (dept,index))))[-1]
            
    def cogSpeech(self, index):
        return self.cog_db[index]#.value
        
    def setLanguage(self,language):		
        if not language in self.languages:
            raise ToontownHouseError('L10N 0x000: Invalid language!')
            
        self.module,_,_ = L10NLocalizer.getModule(self.languages[language])
        self.language = language
        
        self.buildDB()
        self.sc_buildDB()
        self.cog_buildDB()

    def buildName(self): #?????
       langName = self.language.upper()
       print 'Current Loaded Names: names_'+langName+'.txt'
       return langName

    def __call__(self,_str):
        if not _str in self.db:
            print ":l10n: Unknown: {0} (LANG={1})".format(_str,self.language)
            return u"L10N 0x001: NOT FOUND"
        return self.db[_str]
        
    def __getattr__(self,y):
        if y in self.__dict__:
            return self.__dict__[y]
        elif y in dir(self.module):
            return getattr(self.module,y)
        raise AttributeError(y)