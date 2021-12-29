from Blob import Blob
from thread import start_new_thread as snt
import sys, os, gc

try: import cPickle as pickle
except ImportError:
    print 'cPickle failed, using standard...'
    import pickle

DATAPATH = "/var/game/data/"
if '-lc' in sys.argv: DATAPATH = "data/"

def loadToonData(globalBlob,id):
    data = globalBlob.all()
    for key in data.keys():
        if not key.endswith(str(id)): del data[key]
    nd = {}
    for key in data.keys():
        nd[key[:-1]] = data[key]
    return nd
 
def fix_gags(gags):
    _g = []
    for i,x in enumerate(gags):
        _g.append([])
        for a in x:
            _g[i].append(min(1,a))
            
    return _g
 
#read only 
class AvatarStream:
    def __init__(self,account,toonSlot):
        self.slot = toonSlot
        self.blob = Blob(account)
        self.data = loadToonData(self.blob,toonSlot)
        self._ex_attr = ["name","head","body","texture1","texture2","level","lastArea","spc",
                            "lastAreaName","hp","curhp","color1","color2","color3","lastZoneId","toonId"]
        
    def read(self, attr, default=None):
        if attr in self._ex_attr:
            return self.data[attr]
        else:
            return self.loadInPickled(self.data["other"],attr,default)
            
    def loadInPickled(self, data, attr, default=None):
        _data = pickle.loads(data)
        return _data.get(attr,default)  

class Request:
    
    EXPORTED = ['hp','curhp','gags',"toonId",
                "name","head","body","legs",
                "top","bot","color1","color2",
                "color3","lastArea","lastAreaName",
                "gender","spc"]
    
    GAGS_DEFAULT = [[-1]*7]*7
    GAGS_DEFAULT[-2][0] = 0 #squirt
    GAGS_DEFAULT[-3][0] = 0 #throw
    
    DEFAULTS = [15,15,GAGS_DEFAULT,-1,"??",0,"s",1,
                1,1,(0,0,0),(0,0,0),(0,0,0),
                "tth.areas.TTCentral","AREA_TTC",
                "shorts",0]

    def __init__(self,toonId,doId,callback):
        #test if toon id exists
        toonpath = os.path.abspath(DATAPATH+"toons/{0}.toon".format(toonId))
        if os.path.isfile(toonpath):
            f = open(toonpath,"rb")
            _,acc,spot = f.read().split('!')
            f.close()
            
            accpath = DATAPATH+"blobs/{0}.blob".format(acc)
            if os.path.exists(accpath):
                s = AvatarStream(accpath,spot)
                data = {}
                
                for i,x in enumerate(self.EXPORTED):
                    data[x] = s.read(x,self.DEFAULTS[i])
                               
                data['gags'] = fix_gags(data['gags'])
                
                del s
                gc.collect()
                callback(toonId,doId,data)
                
            else: print 'bad accpath',accpath
        
        else: print 'bad toonpath',toonpath
       
def makeAsyncReq(*a):
    snt(Request,a)
       
from direct.distributed.DistributedObjectAI import *

class DataHandlerAI(DistributedObjectAI):

    def request(self,toonId,doId):
        makeAsyncReq(toonId,doId,self.__send)
        
    def __send(self,t,do,d):
        l = base.air.getAvLocation(t)
                
        d['location'] = l
        d['isOnline'] = bool(l)
                
        self.sendUpdate('response',[int(t),make_buffer(d)])