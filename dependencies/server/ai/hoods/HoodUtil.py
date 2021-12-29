def makeDoor(cr,zone,target):
    x = cr.createDistributedObject(className='DistributedDoorAI',zoneId=zone)
    x.d_setTarget(target)
    return x