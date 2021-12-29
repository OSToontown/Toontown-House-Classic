from panda3d.core import *
from direct.distributed.ClientRepository import ClientRepository
from direct.distributed.PyDatagram import PyDatagram as PyDG
from sys import exit
from tth.datahnd.DBMsgTypes import *
from tth.gui import dialog

import AsyncUtil
import __builtin__,sys

class ToontownHouseClientRepositoryBase(ClientRepository):
    extraTypes = [100,101] #db and kick      
    def handleMessageType(self, msgType, di):
        if msgType in self.extraTypes:
            if msgType == 100:
                self.handleDBOpResult(di)
                
            elif msgType == 100:
                self.handleKick(di)
                
        else:
            ClientRepository.handleMessageType(self, msgType, di)
                
    def __init__(self,*args,**kw):
        ClientRepository.__init__(self, *args, **kw)
        
        self.onConnLoad = False
        self.dbReq = []
        self.dbResult = []
        
        self.kickCode = -1        
      
    def setDBUser(self,user,task = None):
        if not self.isConnected():
            if task: return task.again
            taskMgr.doMethodLater(1,self.setDBUser,"setuser",extraArgs = [user])
            return

        datagram = PyDG()
        datagram.addUint16(100)
        datagram.addUint32(self.doIdBase)
        
        datagram.addUint8(DB_REQ_Types['setUser'])
        datagram.addString(user)
        
        self.send(datagram)
        self.dbReq = map(lambda x:DB_RES_Types[x],('badUser','userOk'))
        
        if task: return task.done
        
    def handleDBOpResult(self,di):
        status = di.getUint8()
        #print 'handle db status',status
        if not status in self.dbReq:
            self.notify.warning("DB: Recieved unexpected status: "+str(status))
            return
            
        theStr = di.getString()
        self.dbReq = []
        self.dbResult = [status,theStr]
        
        #btw if it's about setUser, handle HERE
        if status in map(lambda x:DB_RES_Types[x],('badUser','userOk')):
            print 'got user res'
            if status == DB_RES_Types['badUser']:
                print 'OMG ITS BAD!'
                
            self.dbResult = []
     
    @AsyncUtil.threaded
    def _dbRequest(self,dg):
        self.send(dg)
        
        while not self.dbResult:
            self.readerPollOnce()
            
        return self.__clearDbRes()
            
    def __clearDbRes(self):
        x = self.dbResult[:]
        self.dbResult = []
        self.dbReq = []
        return x
        
    def handleKick(self,di):
        reason = di.getUint16()
        string = di.getString()
        
        self.notify.warning("Server is kicking us out (%s): %s" %(reason,string))
        
    def handleGenerate(self, di):
        self.currentSenderId = di.getUint32()
        zoneId = di.getUint32()
        classId = di.getUint16()
        doId = di.getUint32()

        # Look up the dclass
        dclass = self.dclassesByNumber[classId]

        distObj = self.doId2do.get(doId)
        if distObj and distObj.dclass == dclass:
            # We've already got this object.  Probably this is just a
            # repeat-generate, synthesized for the benefit of someone
            # else who just entered the zone.  REJECT <///Accept///> the new updates,
            # <///but don't///> AND OF COURSE DO NOT make a formal generate.
            #assert(self.notify.debug("performing generate-update for %s %s" % (dclass.getName(), doId)))
            #dclass.receiveUpdateBroadcastRequired(distObj, di)
            #dclass.receiveUpdateOther(distObj, di)
            self.notify.info("ignoring generate-update for %s %s" % (dclass.getName(),doId))
            return

        assert(self.notify.debug("performing generate for %s %s" % (dclass.getName(), doId)))
        dclass.startGenerate()
        # Create a new distributed object, and put it in the dictionary
        distObj = self.generateWithRequiredOtherFields(dclass, doId, di, 0, zoneId)
        dclass.stopGenerate()

class ToontownHouseClientRepository(ToontownHouseClientRepositoryBase):
    def __init__(self):
        dcFileNames = ['dependencies/server/tth.dc']
        
        
        ToontownHouseClientRepositoryBase.__init__(self, dcFileNames = dcFileNames)
        
        self.onConnLoad = False
        self.isConnected2 = False
        
        door = (4000,4011)[hasattr(__builtin__,'isCompiled')]
        if '-fp' in sys.argv: door = 4011 #force public
        self.url = URLSpec('http://%s:%s' % (Resolver('svaddr').resolve('gameserver-lv.toontownhouse.org'), door ))
        self._connect()
        
    def _connect(self):
        self.connect([self.url],
                        successCallback = self.connectSuccess,
                        failureCallback = self.connectFailure)
        
    def connectFailure(self, statusCode, statusString):
        print "Not connected!",statusCode,statusString
        #base.transitions.fadeScreen(1)
        
        def _cb(a):
            print a
            self.diag.cleanup()
            if a == -1:
                sys.exit()
            self._connect()
            
        self.diag = dialog.OkCancelDialog(text="Failed to connect to the server! Error code: "+str(statusCode)+'. Try again?',
                                          command = _cb, fadeScreen=1, buttonGeomList=[dialog.okButtons,dialog.cancelButtons],
                                          button_relief = None, buttonTextList = [("","\n\nOK","\n\nOK"),("","\n\nExit","\n\nExit")])
        
    def connectSuccess(self):
        print ":CR: Connected!"
        self.setInterestZones([1000]) #hear AI async
        
        self.acceptOnce('createReady', self.createReady)
        
        taskMgr.doMethodLater(1,self.monitorConn,'monitor connection')
        
    def monitorConn(self,task):
        if not self.isConnected():
            self.disconnect() #really? disconnect? its already -_-
            base.transitions.fadeScreen(0.5)
            base.disableAllAudio()
            base.ignoreAll()
            dialog.OkDialog(text="Your internet connection to the servers has been unexpectedly broken.", text_wordwrap = 18, command = exit,
                            fadeScreen=1, relief=None, buttonGeomList=[dialog.okButtons], button_relief = None)
            return task.done
        
        return task.again
        
    def createReady(self): 
        self.isConnected2 = True
        if self.onConnLoad:
            gamebase.ldScr.dismiss()
        self.createDistributedObject(className = 'AccountMgr', zoneId = 1000)
        
    def identifyAvatar(self, doId):
        return self.doId2do.get(doId+1)