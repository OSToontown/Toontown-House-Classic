"""
File: loader.py
    Module: tth.avatar
Author: Nacib
Date: JULY/25/2013
Description: Handle avatar stuff: models(actor), basics, avatar class, etc
FROM COGTOWN #LOOOOOOOL
"""

from Toon import Toon
from direct.actor.Actor import *
from direct.showbase.DirectObject import *

from direct.task.Task import *

from direct.gui.DirectGui import *
from pandac.PandaModules import *

import math, tth.distributed.HouseDatagram as pickle
from StringIO import *

class ExtendedDna:

    def __init__(self, dna, **kwargs):
        self.dna = dna
        self.data = {'dna':self.dna}
        self.data.update(kwargs)

    def update(self,**extraData):
        self.data.update(extraData)

    def make(self):
        return make_buffer(self.data)

def loadToonData(id):
    data = globalBlob.allToon()
    for key in data.keys():
        if not key.endswith(str(id)): del data[key]
    nd = {}
    for key in data.keys():
        nd[key[:-1]] = data[key]
    return nd

def writeToonData(id,attr,overwrite=1,async=True):
    for key in attr.keys():
        globalBlob.write(key+str(id),attr[key],not overwrite,async)
    globalBlob.flush()

def getAvatarName(slot):
    data = loadToonData(slot)
    name=None
    if "name" in data:
        name = data["name"]
    return name

def getAvatarDNA(slot):
    data = loadToonData(slot)
    return data.get("dna","").decode('base64')

def saveNewToon(slot,name,dna,nmba='',_nta=''):
    #print 'saving toon, dna is',dna
    toonId = globalBlob.newToon(name,nmba,slot,_nta)[-1]
    writeToonData(slot, {"toonId":toonId,
                        "name":name,
                        "dna":dna.encode('base64'),
                        "lastArea":"tth.areas.Tutorial",
                        "lastAreaName":"AREA_Toontorial",
                        "hp":"15",
                        "curhp":"15",
                        "other":pickle.dumps({}) #put pickled extra data here
                        },False)

def loadToonAvatar(slot):
    print 'Loading toon at slot',slot
    data = loadToonData(slot)
    if not "name" in data:
        print 'No such toon! Launching create-a-toon...'
        #there is not a toon in this slot! (WAT? cog?)(Fixed LOL)
        messenger.send('init-createatoon')
        return (None,None)

    zone = 1
    if "lastZoneId" in data:
        zone = data["lastZoneId"]

    zone = int(zone)
    #load avatar model

    _map = lambda *a,**k: tuple(map(*a,**k))
    dna = ExtendedDna(data['dna'].decode('base64'),toonId = data["toonId"], name = data['name']).make()

    t = base.cr.createDistributedObject(className = 'DistributedAvatar', zoneId = base.distMgr.get(zone))
    t.isLocalToon = True
    t.b_setToonDna(dna)

    tag = t.toon.tag

    from direct.controls.GravityWalker import GravityWalker

    if True:
        wc = GravityWalker(legacyLifter=True)
        wc.setWallBitMask(BitMask32(1))
        wc.setFloorBitMask(BitMask32(2))
        wc.setWalkSpeed(18.0, 24.0, 8.0, 80.0)
        wc.initializeCollisions(base.cTrav, t, floorOffset=0.025, reach=4.0)

        wc.enableAvatarControls()
        t.physControls = wc
        t.physControls.placeOnFloor()

    return (t,tag,data["lastArea"],data["lastAreaName"])

class AvatarStream(DirectObject):
    class MoneyManager(DirectObject):
        def __init__(self,stream):
            self.stream = stream

            self.updateCarryInfo()
            self.updateMoney(True)

            self.accept("incomeMoney",self.incomeMoney)
            self.accept("loseMoney",self.loseMoney)
            self.accept("moneyCarryChanged",self.updateCarryInfo)

        def updateCarryInfo(self):
            self.carry_total = self.stream.read("bankSize",10000)
            self.carry_jar = self.stream.read("jarSize",40)

        def updateMoney(self,mayFix = False):
            self.bank = t = self.stream.read("bankTotal",0)
            self.jar = j = self.stream.read("jarTotal",0)

            #print 'MoneyMgr: updating money:',self.jar,self.bank

            if self.jar > self.carry_jar and mayFix:
                exc = self.jar - self.carry_jar
                #print 'MoneyMgr: jar needs fix; overflow =',exc

                self.jar = self.carry_jar

                self.bank += exc

            if self.jar < 0:
                missing = 0 - self.jar
                #print 'MoneyMgr: jar is negative; missing =',missing,'removing from bank...'

                self.jar = 0

                self.bank -= missing

            if self.bank < 0:
                #print 'MoneyMgr: bank is negative; setting to zero (toon is broke)...'
                self.bank = 0

            if self.bank > self.carry_total and mayFix:
                #print 'MoneyMgr: bank needs fix; overflow =',self.bank - self.carry_total
                self.bank = self.carry_total

            if self.bank != t or self.jar != j:
                self.stream.write("jarTotal",self.jar)
                self.stream.write("bankTotal",self.bank)

            messenger.send("moneyChanged")

        def incomeMoney(self,amount):
            #push into the jar and let update money fix it
            #print 'MoneyMgr: incoming money:',amount
            self.stream.add("jarTotal",amount)
            self.updateMoney(True)

        def loseMoney(self,amount):
            #push into the jar and let update money fix it
            #print 'MoneyMgr: losing money:',amount
            self.stream.sub("jarTotal",amount)
            self.updateMoney(True)

        def getMoney(self,update = 1):
            if update: self.updateMoney(True)
            return (self.jar,self.bank,self.jar+self.bank)

    def __init__(self,toonSlot):
        self.slot = toonSlot
        self.data = loadToonData(toonSlot)
        self._ex_attr = ["name","dna","lastZoneId","lastArea","lastAreaName","toonId"]

        self.moneyMgr = self.MoneyManager(self)
        self.accept('stream_reload',self.__reload)

    def __reload(self):
        self.data = loadToonData(self.slot)

    def read(self, attr, default=None):
        if attr in self._ex_attr:
            return self.data[attr]
        else:
            return self.loadInPickled(self.data["other"],attr,default)

    def write(self, attr, value):
        if attr in self._ex_attr:
            self.data[attr] = value
            writeToonData(self.slot,{attr:value})

        else:
            self.saveInPickled(attr,value)
            writeToonData(self.slot,{"other":self.data["other"]})

    def loadInPickled(self, data, attr, default=None):
        _data = pickle.loads(data)
        if not attr in _data:
            self.saveInPickled(attr,default)
            writeToonData(self.slot,{"other":self.data["other"]})
            _data = pickle.loads(self.data["other"])
        return _data.get(attr,default)

    def saveInPickled(self, attr, value):
        data = pickle.loads(self.data["other"])
        data[attr] = value
        self.data["other"] = pickle.dumps(data)

    def add(self, attr, value):
        cur = self.read(attr,0)
        new = cur+value
        self.write(attr,new)

    def sub(self, attr, value):
        cur = self.read(attr,0)
        new = cur-value
        self.write(attr,new)

    def setPlayRate (self, *args,**kw): self._toon.setPlayRate(*args,**kw) # WHAT THE FUCK!!
