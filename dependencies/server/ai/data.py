from tth.datahnd.Blob import Blob
import sys, os

try: import cPickle as pickle
except ImportError:
    print 'cPickle failed, using standard...'
    import pickle

DATAPATH = "/var/game/data/"
if '-lc' in sys.argv: DATAPATH = "data/" #"../../server/data/"

def loadToonData(globalBlob,id):
    data = globalBlob.all()
    for key in data.keys():
        if not key.endswith(str(id)): del data[key]
    nd = {}
    for key in data.keys():
        nd[key[:-1]] = data[key]
    return nd
    
def writeToonData(globalBlob,id,attr,overwrite=1):
    for key in attr.keys():
        globalBlob.write(key+str(id),attr[key],not overwrite)
    globalBlob.flush()

class AvatarStream:
    def __init__(self,account,toonSlot):
        self.slot = toonSlot
        self.blob = Blob(account)
        self.data = loadToonData(self.blob,toonSlot)
        self._ex_attr = ["name","head","body","texture1","texture2","level","lastArea","spc",
                            "lastAreaName","hp","curhp","color1","color2","color3","lastZoneId"]
        
    def read(self, attr, default=None):
        if attr in self._ex_attr:
            return self.data[attr]
        else:
            return self.loadInPickled(self.data["other"],attr,default)
            
    def loadInPickled(self, data, attr, default=None):
        _data = pickle.loads(data)
        return _data.get(attr,default)
        
    def write(self, attr, value):
        if attr in self._ex_attr:
            self.data[attr] = value
            writeToonData(self.blob,self.slot,{attr:value})
            
        else:
            self.saveInPickled(attr,value)
            writeToonData(self.blob,self.slot,{"other":self.data["other"]})
            
    def loadInPickled(self, data, attr, default=None):
        _data = pickle.loads(data)
        if not attr in _data:
            self.saveInPickled(attr,default)
            writeToonData(self.blob,self.slot,{"other":self.data["other"]})
            _data = pickle.loads(self.data["other"])
        return _data.get(attr,default)   
    
    def saveInPickled(self, attr, value):
        data = pickle.loads(self.data["other"])
        data[attr] = value
        self.data["other"] = pickle.dumps(data)

def toonId2stream(toonId):
    #test if toon id exists
    toonpath = os.path.abspath(DATAPATH+"toons/{0}.toon".format(toonId))
    if os.path.isfile(toonpath):
        f = open(toonpath,"rb")
        
        data = f.read()
        #sys.exit("debug: path %s data val: %s" % (toonpath,data))
        
        _,acc,spot = data.split('!')
        f.close()
            
        accpath = DATAPATH+"blobs/{0}.blob".format(acc)
        
        if os.path.exists(accpath): return AvatarStream(accpath,spot)
        else: print 'bad accpath',accpath 
        
    else: print 'bad toonpath',toonpath
    
def doId2stream(doId):
    try:
        av = base.air.getAvFromId(base.air.id2c(int(doId)))
        return toonId2stream(av.data["toonId"])  
    except: 
        return
    