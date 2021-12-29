from pandac.PandaModules import *
import sys, time, signal, os, __builtin__, glob

class fakeL10N:
    def __call__(self,*a): return u"-"
    
__builtin__.L10N = fakeL10N()

def __exit(*args):
    print 'exiting'
    os._exit(0)
    
#signal.signal(signal.CTRL_C_EVENT,os.kill)

USE_DS = 0
if USE_DS:
    from direct.stdpy import threading
else:
    import threading

sys.path.append("../..")
sys.path.append("..")

loadPrcFileData("","window-type none")
import direct.directbase.DirectStart

from ai.data import DATAPATH as BLOB_PATH, Blob

from tth.datahnd.DBMsgTypes import *

from direct.distributed.ServerRepository import ServerRepository
from direct.distributed.PyDatagram import PyDatagram as PyDG
class FakeServer(ServerRepository):
    extraTypes = [100]
    
    DB_RES_Types = {
                'queryResultOk': 1,
                'queryResultFailed': 2,
                'badUser': 3,
                'userOk': 4,
                'writeOk': 5,
                'writeFailed': 6,
                }
                
    DB_REQ_Types = {
                'query': 1,
                'write': 2,
                'setUser': 3,
                }
                
    def sendDoIdRange(self, client):
        ServerRepository.sendDoIdRange(self, client)
        base.cTracker[client.doIdBase] = {'cRef':client}
                
    def handleMessageType(self, msgType, di):
        if msgType in self.extraTypes:
            sender = di.getUint32() 
            client = self.clientsByDoIdBase.get(sender)
            
            if not client: self.notify.warning("HandleMsgType: Unknown client: "+str(sender))
            
            if msgType == 100:
                self.handleDBOp(client,di)
                
        else:
            ServerRepository.handleMessageType(self, msgType, di)
           
    def handleDBOp(self,client,di):
        #test if its tracked
        ct = base.cTracker.get(client.doIdBase,None)
        if not ct:
            self.notify.warning("HandleDBOp: Unknown client: "+str(client.doIdBase))
            return
            
        op = di.getUint8()
        if not op in DB_REQ_Types.values():
            self.notify.warning("HandleDBOp: Unknown op: "+str(op))
            return
            
        if op == DB_REQ_Types['setUser']:
            user = di.getString()
            
            _blob = self.DB_openBlob(user)
            if not _blob[0]:
                self.notify.warning("Bad user: "+user+" "+_blob[1])
                self.DB_reportUser(client,DB_RES_Types['badUser'])
                return
                
            ct["blob"] = _blob[0]
            ct["user"] = user
            self.DB_reportUser(client,DB_RES_Types['userOk'])
            return
            
        #if not set user, we supposed its already set
        #test anyway
        
        _blob = ct.get("blob")
        
        if op == DB_REQ_Types['query']:
            if not _blob:
                self.notify.warning("HandleDBOp: Detected attempt to make db op before setuser")
                self.DB_reportQuery(client,DB_RES_Types['queryResultFailed'],"NO_USER")
                return
            
            file = di.getString()
            
            if file == "__ALL__": data = _blob.bake()
            else: data = _blob.read(file)
            
            self.DB_reportQuery(client,DB_RES_Types['queryResultOk'],data)
            
        elif op == DB_REQ_Types['write']:
            if not _blob:
                self.notify.warning("HandleDBOp: Detected attempt to make db op before setuser")
                self.DB_reportQuery(client,DB_RES_Types['writeFailed'],"NO_USER")
                return
            
            file = di.getString()
            data = di.getString()
            _blob.write(file,data,False)
            _blob.flush()
            self.DB_reportQuery(client,DB_RES_Types['writeOk'],"W_OK")
            
        elif op == DB_REQ_Types['newToon']:
            if not _blob:
                self.notify.warning("HandleDBOp: Detected attempt to make db op before setuser")
                self.DB_reportQuery(client,DB_RES_Types['newToonFailed'],"NO_USER")
                return
            
            name = di.getString()
            approved = di.getBool()
            spot = di.getUint8()
            nameToA = di.getString()
            
            tid = self.DB_newToon(ct["user"],*map(str,(name,approved,spot,nameToA)))
            
            self.DB_reportQuery(client,DB_RES_Types['newToonOk'],tid)
            
        elif op == DB_REQ_Types['delToon']:
            if not _blob:
                self.notify.warning("HandleDBOp: Detected attempt to make db op before setuser")
                self.DB_reportQuery(client,DB_RES_Types['delToonFailed'],"NO_USER")
                return
            
            spot = str(di.getUint8())
            
            of = _blob.files
            nf = {}
            
            for f,c in of.items():
                if not f.endswith(str(spot)): nf[f]=c
                
            _blob.files = nf
            _blob.flush()
                        
            self.DB_reportQuery(client,DB_RES_Types['delToonOk'],"DEL_OK")  
            
    def DB_openBlob(self,user):
        try: return (Blob("{0}blobs/{1}.blob".format(BLOB_PATH,user)),"")
        except Exception as e: return (None,str(e))
        
    def DB_reportUser(self,client,st):
        datagram = PyDG()
        datagram.addUint16(100)
        datagram.addUint8(st)
        datagram.addString("failed to set given user")
        self.cw.send(datagram, client.connection)
        self.needsFlush.add(client)
    
    def DB_reportQuery(self,client,st,data):
        datagram = PyDG()
        datagram.addUint16(100)
        datagram.addUint8(st)
        datagram.addString(data)
        self.cw.send(datagram, client.connection)
        self.needsFlush.add(client)

    def DB_newToon(self,acc,name,ia,spot,nToAp = None):
        #print 'make toon',acc,name,ia,spot,nToAp
        _id = -1
        _toons = [int(t.replace('\\','/').split('/')[-1].split('.',1)[0]) for t in glob.glob('./data/toons/*.toon')]
        _toons.sort()
        if len(_toons): _id = _toons[-1]+1
        else: _id = 0

        _id = str(_id)
    
        if not ia and nToAp:
            with open('./data/toons/'+_id+'.nta','wb') as f: f.write('!'.join([nToAp,acc,spot]))
    
        with open('./data/toons/'+_id+'.toon','wb') as f:
            f.write('!'.join([name,acc,spot]))
        
        return _id
            
base.sr = FakeServer(4003, None, dcFileNames = [])
base.cTracker = {}
run()