from direct.distributed.DistributedObjectAI import DistributedObjectAI

from datetime import datetime

class AccountMgrAI(DistributedObjectAI):        
    def setData(self,data):
        clientId = base.air.id2c(self.doId)
        print 'AI: ACCMGR.SETDATA!',data,clientId
        if not clientId in base.cTracker:
            print 'accMgrAI: invalid id',clientId
            return
        base.cTracker[clientId].update(**load_buffer(data))
        _acc = base.cTracker[clientId]["acc"]
        log = open(base.logBasePath.format(_acc),'ab')
        log.write('-'*10+'\n')
        log.write(datetime.now().strftime('%d %b %y %H:%M:%S\n'))
        base.cTracker[clientId]["log"] = log