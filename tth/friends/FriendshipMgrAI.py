from direct.distributed.DistributedObjectAI import DistributedObjectAI
from thread import start_new_thread as snt

from dependencies.server.ai.data import doId2stream,toonId2stream

from FriendshipGlobals import *

class FriendshipMgrAI(DistributedObjectAI):
    def __init__(self,cr):
        DistributedObjectAI.__init__(self,cr)
        self.reqs = {}
        
       # self.accept('playerOn',self.__onOrOff,[1])
       # self.accept('playerOff',self.__onOrOff,[0])
        
    #def __onOrOff(self,state,id):
        #if id == -1:
       #     return 
       # prefix = ("Off","On")[state]
        #print prefix,id
        
        #fr = toonId2stream(id).read("friends",[])
        #for f in fr:
            #if base.air.getAvLocation(f):
               # print '\t',f
               # _id = base.air.id2c(x.doId)
               # self.sendUpdateToChannel(_id,"toonOn",[int(id)])
        
    def requestFriend(self,to,name):
        sender = base.air.getAvatarIdFromSender()
        
        if to == 0x6EB3:
            #kicking
            to = int(name)
            toC = base.air.getDoIdFromToonId(to)
            print sender,'kicks',to
            if toC:
                print to,'is online as',toC,'notifying...'
                self.sendUpdateToChannel(toC,"incomeRequest",[base.air.getToonIdFromDoId(sender),str(0x6EB3)])
            return
        
        toC = base.air.id2c(to)
        
        #check if its valid ID
        if not base.air.getAvFromId(toC):
            self.sendUpdateToChannel(sender,"updateRequest",[to,ST_ERROR])
            return
            
        if 0: #base.air.isBusy(to):
            self.sendUpdateToChannel(sender,"updateRequest",[to,ST_BUSY])
            return
            
        #ok, send it
        self.sendUpdateToChannel(sender,"updateRequest",[to,ST_SENT])
        self.sendUpdateToChannel(toC,"incomeRequest",[sender,name])
        
        self.reqs[sender] = (to,toC)
        
    def updateRequest(self,sender,status):
        to,toC = self.reqs.get(sender,(None,None))
        if not to:
            print 'bad ur',sender,to,toC
            return
        
        reporter = base.air.getAvatarIdFromSender()
        
        print 'ur',reporter,sender,to,status
        
        if reporter == toC:
            if status == ST_ACCEPT:
                #accepted, notify sender and save
                self.sendUpdateToChannel(sender,"updateRequest",[to,ST_ACCEPT])
                
                snt(self.writeFriendship,(toC,sender))
                #self.writeFriendship(toC,sender)
                
                del self.reqs[sender]
            
            elif status == ST_REJECT:
                #rejected, notify sender
                self.sendUpdateToChannel(sender,"updateRequest",[to,ST_REJECT])
                del self.reqs[sender]
                
            elif status == ST_BUSY:
                #busy, notify sender
                self.sendUpdateToChannel(sender,"updateRequest",[to,ST_BUSY])
                del self.reqs[sender]
            
        elif reporter == sender:
            if status == ST_CANCEL:
                #canceled, notify to
                self.sendUpdateToChannel(toC,"updateRequest",[sender,ST_CANCEL])
                del self.reqs[sender]
                
    def writeFriendship(self,a,b):
        s1 = doId2stream(a)
        s2 = doId2stream(b)
        
        names = map(base.air.getNameFromDoId,(a,b))
        ids = map(base.air.getToonIdFromDoId,(a,b))
        zipped = zip(ids,names)
        
    #    print 'niz', names, ids, zipped
        
        if s1:
            friends1 = s1.read("friends",[])
            print 'F1',friends1
            friends1.append(zipped[1])
            s1.write("friends",friends1)
            
        if s2:
            friends2 = s2.read("friends",[])
            print 'F2',friends2
            friends2.append(zipped[0])
            s2.write("friends",friends2)