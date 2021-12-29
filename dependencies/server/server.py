""" Demonstrates the DC system from the server side, using a
DistributedNode-based avatar. """

class fakeL10N:
    special = {'BOOK_DISGUISE_PARTS':','*20}
    def __call__(self,a):
        if a in self.special: return self.special[a]
        return u"-"

import direct, sys, os, glob, __builtin__, math
__builtin__.glob = glob
__builtin__.pversion = None
__builtin__.isServer = 1

from pandac.PandaModules import *
loadPrcFileData('', 'window-type none')

from tth.l10n import l10n
__builtin__.L10N = l10n('en',0)
L10N.fPrefix = "../../"
L10N.setLanguage("en")

isPublic = 'public' in os.path.abspath(os.curdir)
print ':Server: isPublic=',isPublic

from tth.distributed.HouseDatagram import loads as hdg_ld, dumps as hdg_dp
__builtin__.load_buffer = hdg_ld
__builtin__.make_buffer = hdg_dp

from direct.directbase.DirectStart import *

from FixedSR import FixedServerRepository
from direct.distributed.ClientRepository import ClientRepository
from direct.distributed.PyDatagram import PyDatagram as PyDG

from tth.datahnd.DBMsgTypes import *
from tth.distributed import AsyncUtil

from ai.data import DATAPATH as BLOB_PATH, Blob

door = (4000,4011)[isPublic]
if '-fp' in sys.argv:
    door = 4011
    print 'Forcing public: door',door
    
class TTHServerRepositoryBase(FixedServerRepository):
    extraTypes = [100]
                
    def handleMessageType(self, msgType, di):
        if msgType in self.extraTypes:
            sender = di.getUint32() 
            client = self.clientsByDoIdBase.get(sender)
            
            if not client: self.notify.warning("HandleMsgType: Unknown client: "+str(sender))
            
            if msgType == 100:
                self.handleDBOp(client,di)
                
        else:
            ServerRepository.handleMessageType(self, msgType, di)
         
    @AsyncUtil.threaded         
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
    
    @AsyncUtil.threaded 
    def DB_reportQuery(self,client,st,data):
        datagram = PyDG()
        datagram.addUint16(100)
        datagram.addUint8(st)
        datagram.addString(data)
        self.cw.send(datagram, client.connection)
        self.needsFlush.add(client)

    @AsyncUtil.locked
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

class TTHServerRepository(TTHServerRepositoryBase):
    def __init__(self):
        tcpPort = base.config.GetInt('server-port', 4000)
        dcFileNames = ['tth.dc']
                
        TTHServerRepositoryBase.__init__(self, door, None, dcFileNames = dcFileNames)
        
    def handleClientDisconnect(self, client):
        FixedServerRepository.handleClientDisconnect(self, client)
        print 'dc:',client.doIdBase
        messenger.send('clientDc',[client.doIdBase])
        del base.cTracker[client.doIdBase]
        
    def sendDoIdRange(self, client):
        FixedServerRepository.sendDoIdRange(self, client)
        print ':SR: New client!',client.doIdBase
        taskMgr.doMethodLater(180,lambda task:self.testBot(task,client.doIdBase),"antibot")
        base.cTracker[client.doIdBase] = {'cRef':client}
        
    def kickById(self, clid, reasonCode = 0, reasonStr = "no reason specified"):
        if not clid in base.cTracker:
            print 'SR:KBI: No such id',clid
            return
            
        #send the ban signal
        dg = PyDG()
        dg.addUint16(101)
        dg.addUint16(reasonCode)
        dg.addString(reasonStr)
            
        conn = base.cTracker[clid]["cRef"].connection
        
        self.cw.send(dg, conn)
        self.needsFlush.add(base.cTracker[clid]["cRef"])
        
        taskMgr.doMethodLater(4,lambda task:conn.getManager().closeConnection(conn),'kick client') #bye bye
        print clid,'kicked!'
        
    def testBot(self,task,cl):
        if not cl in base.cTracker:
            print 'SR:TestBot: No such id',cl
            return task.done
            
        cld = base.cTracker[cl]
        if not "acc" in cld:
            print 'Bot detected! Kicking...'
            self.kickById(cl,0x0001,"bot detected")
            
        return task.done
        
base.cTracker = {}
base.logBasePath = 'user/logs/{0}.log'     
base.sr = TTHServerRepository()
print "server created, waiting."

def getAIFreeZonesInitialRange():
    return (18000,20000)

def getAIInterestZones():             
    zones = []
    basic_zones = xrange(1000,20000,1000)
    for bz in basic_zones:
        for x in xrange(bz,bz+500,100):
            for a in range(x,x+40,1):
                zones.append(a)
        
    zones2 = []
    for zone in zones:
        for b in xrange(10): #amount of districts
            zones2.append(zone + 10**7*b)
                
    zones2 = set(zones2)
    print len(zones2)
    return zones2
    
from ai.DistrictManager import DistrictManager
class TTHAIRepository(ClientRepository):
    def __init__(self):
        dcFileNames = ['tth.dc']
        
        ClientRepository.__init__(self, dcFileNames = dcFileNames,
                                  dcSuffix = 'AI')

        url = URLSpec('http://127.0.0.1:'+str(door))
        self.connect([url],
                     successCallback = self.connectSuccess,
                     failureCallback = self.connectFailure)
                     
        #free zone manager
        self.freeZones = set(range(*getAIFreeZonesInitialRange())) #have interest here anyway
        
    def getFreeZone(self):
        if len(self.freeZones):
            _z  = self.freeZones.pop()
            print 'use new free zone:',_z
            return _z
        else:
            _z = __import__('random').randint(*getAIFreeZonesInitialRange())
            print 'OUT OF FREE ZONES! RETURNING RANDOM:',_z
            return _z
            
    def addFreeZone(self,x):
        self.freeZones.add(x)
        
    def connectFailure(self, statusCode, statusString):
        raise StandardError(str(statusCode)+","+statusString)

    def connectSuccess(self):
        """ Successfully connected.  But we still can't really do
        anything until we've got the doID range. """
        self.acceptOnce('createReady', self.createReady)

    def createReady(self):      
        base.cTracker[self.doIdBase]["acc"] = "AI"
        
        self.timeManager = self.createDistributedObject(className = 'TimeManagerAI', zoneId = 1000)
        self.async = self.createDistributedObject(className = 'AIAsync', zoneId = 1000)
        self.datahnd = self.createDistributedObject(className = 'DataHandlerAI', zoneId = 1000)
        self.friendMgr = self.createDistributedObject(className = 'FriendshipMgrAI', zoneId = 1000)
        
        taskMgr.doMethodLater(2,self.tskAdminMsg,"send admin updates from file")
        
        print 'Setting zones...'
        iz = getAIInterestZones()
        base.sr.clientsByDoIdBase[self.doIdBase].explicitInterestZoneIds = iz
        base.sr.updateClientInterestZones(base.sr.clientsByDoIdBase[self.doIdBase])
        print 'DONE!'
            
        del iz

        print 'Spawning district manager...'
        self.distMgrs = []
        for i in xrange(1,10): self.distMgrs.append(DistrictManager(i))
        print 'DONE!'
            
    def tskAdminMsg(self,task):
        if os.path.exists('./admin.msg'):
            f = open('./admin.msg','rb')
            msg = f.read()
            f.close()
            os.unlink('./admin.msg')
            
            print 'MSG!',msg
            
            self.async.sendUpdate("sendAdminMsg",[msg])
                
        if os.path.exists('./stat.req'):
            os.unlink('./stat.req')
            
            print 'saving stat'
            
            f = open('stat.res','wb')
            f.write(str(len(base.cTracker))+'\n')
            for x,y in base.cTracker.items():
                acc = y.get("acc","NOT_SET")
                f.write(str(x)+":"+str(acc)+'\n')
                
            f.close()
            
        if os.path.exists('./exec.me'):
            f = open('./exec.me','rb')
            msg = f.read()
            f.close()
            os.unlink('./exec.me')
            
            exec msg in globals(),locals()
            
        return task.again
        
    def id2c(self,doId):
        _r = 10**6
        return _r*(doId//_r)+1
        
    def getAvLocation(self,toonId):
        x = base.avatars.get(str(toonId),None)
        if x: return getattr(x,"zoneId",None)
        
    def getAvFromId(self,doId):
        try: c = base.sr.clientsByDoIdBase.get(int(doId),None)
        except: c = None
        
        if c:
            objs = c.objectsByDoId
            for obj in objs.values():
                if obj.dclass.getName() == "DistributedAvatar":
                    return self.doId2do.get(obj.doId)
                    
    def getDoIdFromToonId(self,toonId):
        x = base.avatars.get(str(toonId),None)
        if x: return getattr(x,"doId",None)
        
    def getToonIdFromDoId(self,doId):
        av = self.getAvFromId(doId)
        if av:
            try: return av.data['toonId']
            except: pass
            
    def getNameFromDoId(self,doId):
        av = self.getAvFromId(doId)
        if av:
            try: return av.data['name']
            except: pass
            
base.air = TTHAIRepository()

def addAvatar(id,av):
    messenger.send('playerOn',[id])
    base.avatars[str(id)] = av
    
def delAvatar(id):
    messenger.send('playerOff',[id])
    try: base.avatars[str(id)]
    except: print 'failed to delAvatar',id
    
base.avatars = {}

base.accept("newAv",addAvatar)
base.accept("lostAv",delAvatar)

run()