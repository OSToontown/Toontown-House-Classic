from direct.distributed.DistributedObject import DistributedObject

from FriendshipGlobals import *

QUERY_AV = "Checking if %s is avaiable..."
KICK = "You are already friends with %s.\nWould you like to remove it from your friends list?"
NOKICK = "You are already friends with %s\n(and cannot kick it at the moment)"
ASK = "%s would like to be your friend."
CANCEL = "\n\nCancel"
OK = "\n\nOK"
YES = "\n\nYes"
NO = "\n\nNo"

RS_OK = "You're now friends with %s!"
RS_SENT = "Asking %s to be friends..."
RS_NO = "%s said no, thank you."
RS_BUSY = "%s is busy at the moment. Try again later!"
RS_ERROR = "An error occured! Try again later..."
RS_KICKED = "%s has left your friends list!"

canKick = False

class FriendshipMgr(DistributedObject):    
    def __init__(self,cr):
        DistributedObject.__init__(self,cr)
        self.curReq = None
        self.curName = ""
        self.dialog = None
        
        self.accept("askFriend",self.ask)
        
    def updateRequest(self,sender,status):
        if self.curReq != sender:
            print 'bad ur',sender,self.curReq
            return
            
        from tth.gui import dialog
            
        if status == ST_ACCEPT:
            print self.curReq,'accepted!'
            self.dialog.cleanup()
            self.dialog = dialog.OkDialog(text=RS_OK%self.curName,buttonGeomList=[dialog.okButtons],
                                          buttonTextList=(("",OK,OK),),button_relief=None,
                                          command=self.__cancel,pos=DIALOG_POS)
            self.curReq = None
            self.curName = ""
            
            messenger.send('stream_reload')
            messenger.send('friendsListChanged')
            
        elif status == ST_REJECT:
            print self.curReq,'rejected!'
            self.dialog.cleanup()
            
            self.dialog = dialog.OkDialog(text=RS_NO%self.curName,buttonGeomList=[dialog.okButtons],
                                          buttonTextList=(("",OK,OK),),button_relief=None,
                                          command=self.__cancel,pos=DIALOG_POS)
            self.curReq = None
            self.curName = ""
                
        elif status == ST_SENT:
            print self.curReq,'sent!'
            self.dialog["text"] = RS_SENT%self.curName
            
        elif status == ST_BUSY:
            print self.curReq,'is busy!'
            self.dialog["text"] = RS_BUSY%self.curName
            self.curReq = None
            self.curName = ""
            
        elif status == ST_CANCEL:
            print self.curReq,'canceled!'
            self.dialog.cleanup()
            self.curReq = None
            self.curName = ""
            messenger.send('okFrAsk')
            
        elif status == ST_ERROR:
            print self.curReq,'gave an error!'
            self.dialog["text"] = RS_ERROR
            self.curReq = None
            self.curName = ""
            
        #self.dialog.resetFrameSize()
                
    def incomeRequest(self,sender,name):
        if self.curReq:
            print 'got req, but already busy!'
            self.sendUpdate("updateRequest",[sender,ST_BUSY])
            return
            
        if name == str(0x6EB3):
            messenger.send('playerLeft',[sender])
            return
            
        self.curReq = sender
        self.curName = name
        
        from tth.gui import dialog
        self.dialog = dialog.YesNoDialog(text=ASK % name,pos=DIALOG_POS,
                                         command=self.__callback,
                                         buttonGeomList=[dialog.okButtons,dialog.cancelButtons],
                                         buttonTextList=(("",YES,YES),("",NO,NO)),
                                         button_relief=None)
        
        messenger.send('noFrAsk')
        
    def __callback(self,result):
        if self.dialog: self.dialog.cleanup()
        
        if not result: self.__reject()
        else: self.__accept()
        
        messenger.send('okFrAsk')
        
    def __accept(self):
        self.sendUpdate('updateRequest',[self.curReq,ST_ACCEPT])
        self.curReq = None
        self.curName = ""
        
        messenger.send('stream_reload')
        messenger.send('friendsListChanged')
        
    def __reject(self):
        self.sendUpdate('updateRequest',[self.curReq,ST_REJECT])
        self.curReq = None
        self.curName = ""
        
    def __cancel(self,*args):
        if self.dialog: self.dialog.cleanup()
        if self.curReq:
            self.sendUpdate('updateRequest',[base.cr.doIdBase,ST_CANCEL])
            
        self.curReq = None
        self.curName = ""
        
        messenger.send('okFrAsk')
        
    def __kick(self,arg):        
        self.dialog.cleanup()
        
        from tth.gui import dialog
        print arg
        if arg > 0:
            print self.curReq,'kicked!'

            self.dialog = dialog.OkDialog(text=RS_KICKED%self.curName,buttonGeomList=[dialog.okButtons],
                                          buttonTextList=(("",OK,OK),),button_relief=None,
                                          command=self.__cancel,pos=DIALOG_POS)
            
            #self.sendUpdate("requestFriend",[0x6EB3,str(self.curReq)])
            self.curReq = None
            self.curName = ""
            
            messenger.send('stream_reload')
            messenger.send('friendsListChanged')
        
        messenger.send('okFrAsk')
        self.curReq = None
        self.curName = ""
        
    def ask(self,target,name,myName):
        if self.curReq:
            print 'attempted to req, but already busy!'
            return
        
        from tth.gui import dialog
        
        if base.frdMgr.isFriend(target.playerId):
            if canKick: self.dialog = dialog.OkCancelDialog(text=KICK%name,
                                                buttonGeomList=[
                                                                dialog.okButtons,
                                                                dialog.cancelButtons
                                                                ],
                                                buttonTextList=(
                                                                ("",OK,OK),
                                                                ("",CANCEL,CANCEL)
                                                                ),
                                                button_relief=None,
                                                command=self.__kick,
                                                pos=DIALOG_POS) 
                                                
            else: self.dialog = dialog.CancelDialog(text=NOKICK%name,
                                                buttonGeomList=[dialog.okButtons],
                                                buttonTextList=[("",OK,OK)],
                                                button_relief=None,
                                                command=self.__kick,
                                                pos=DIALOG_POS)                              
            self.curReq = 0x6EB3 #random number, means clicked on kick
            self.curName = "__kickDialog__"
            return
    
        self.curReq = target.doId
        self.curName = name
        self.sendUpdate("requestFriend",[target.doId,myName])
        self.dialog = dialog.CancelDialog(text=QUERY_AV%name,buttonGeomList=[dialog.cancelButtons],
                                          buttonTextList=(("",CANCEL,CANCEL),),button_relief=None,
                                          command=self.__cancel,pos=DIALOG_POS)
                                          
        messenger.send('noFrAsk')
        
    def toonOn(self,id): messenger.send('friendOnline',[id])
    def toonOff(self,id): messenger.send('friendOffline',[id])