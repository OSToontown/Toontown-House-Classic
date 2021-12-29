from direct.distributed.DistributedObject import DistributedObject

class AccountMgr(DistributedObject):
    def generate(self):
        DistributedObject.generate(self)
        if base.cr.isLocalId(self.doId):
            taskMgr.doMethodLater(1,self._send,"send")
        
    def _send(self,task):
        self.cr.sendUpdateToChannel(self,1,"setData",[make_buffer({"acc":base.user})])
        self.cr.sendDeleteMsg(self.doId)
        return task.done
        
    def setData(self,data):
        pass
        