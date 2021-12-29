from direct.distributed.PyDatagram import PyDatagram as PyDG
from tth.datahnd.Blob import Blob
import threading as trd, zlib

from tth.datahnd.DBMsgTypes import *

class NetworkedBlobWithCR:
    def __init__(self,cr,user):
        self.cr = cr
        cr.setDBUser(user)

    def __makeDGBase(self):
        dg = PyDG()
        dg.addUint16(DBOP_CODE)
        dg.addUint32(self.cr.doIdBase)
        return dg
        
    def write(self,file,data,append_ignored=None,async=True):
        dg = self.__makeDGBase()
        dg.addUint8(DB_REQ_Types['write'])
        dg.addString(file)
        dg.addString(str(data))
        
        self.cr.dbReq = map(lambda x:DB_RES_Types['write'+x],('Ok','Failed'))
        
        t = self.cr._dbRequest(dg)
        if not async: return t.result_queue.get()
    
    def read(self,file):
        dg = self.__makeDGBase()
        dg.addUint8(DB_REQ_Types['query'])
        dg.addString(file)
        
        self.cr.dbReq = map(lambda x:DB_RES_Types['queryResult'+x],('Ok','Failed'))
        return self.cr._dbRequest(dg).result_queue.get()
        
    def newToon(self,name,isAp,spot,nta):
        dg = self.__makeDGBase()
        dg.addUint8(DB_REQ_Types['newToon'])
        
        dg.addString(name)
        dg.addBool(isAp)
        dg.addUint8(spot)
        dg.addString(nta)
        
        self.cr.dbReq = map(lambda x:DB_RES_Types['newToon'+x],('Ok','Failed'))
        return self.cr._dbRequest(dg).result_queue.get()
        
    def delToon(self,spot):
        dg = self.__makeDGBase()
        dg.addUint8(DB_REQ_Types['delToon'])
        
        dg.addUint8(spot)
        
        self.cr.dbReq = map(lambda x:DB_RES_Types['delToon'+x],('Ok','Failed'))
        return self.cr._dbRequest(dg).result_queue.get()
        
    def all(self,verbose=0):
        if verbose:
            print ':SrvData: Contacting server for "all"...'
            
        data = self.bake()
        #data = zlib.decompress(data[-1]).split(chr(1))[1:]
        if verbose:
            print ':SrvData: "all" sent by server!',data          
            
        return Blob.debake(data)
        
    def bake(self):
        return self.read("__ALL__")[-1]
        
    def flush(self): pass
    