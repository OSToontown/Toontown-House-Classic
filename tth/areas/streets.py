from __init__ import Area, Tunnel, BitMask32
from direct.interval.IntervalGlobal import *
from tth.gui.StreetMaps import QuestMap

STPATH = "phase_0/streets/street_%s"
class Street(Area):
    DONT_STORE = True
    mapPaused = False
    
    def loadMaps(self):
        hood = self.hood
        disneyId = self.disneyId
        self.map=QuestMap(gamebase.toonAvatar[0].toon,hood,disneyId)
        self.map.start()
        self.map.acceptOnscreenHooks()
       
    def destroy(self):
        self.map.stop()
        self.map.removeNode()
        Area.destroy(self)
    
    def __tth_area__(self):
        return {
                'name':self.name,
                'models':self.np,
                'bgm':self.theme,
                'gui':self.frame,
                'speeches':[]
                }
                
    def enableControls(self):
        try:
            self.map.acceptOnscreenHooks()
        except AttributeError:
            pass
            
        Area.enableControls(self)
        
    def disableControls(self):
        try:
            self.map.ignoreOnscreenHooks()
        except AttributeError:
            pass
            
        Area.disableControls(self)
        
    def obscureBookAndFL(self,flag):
        Area.obscureBookAndFL(self,flag)
        if flag:
            self.mapPaused = True
            self.map.stop()
            
        else:
            if self.mapPaused:
                self.mapPaused = False
                self.map.start()
                
class HoodStreet(Street):
    hasHQ = False
    def __init__(self,environ = None,tp = None):
        Street.__init__(self,environ)
        self.environ.reparentTo(self.np)
        
        gamebase.toonAvatarStream.write("lastArea",str(self.tunnelSz).rsplit('.',1)[-1])
        gamebase.toonAvatarStream.write("lastAreaName",self.tunnelSz.name)
        gamebase.toonAvatarStream.write("lastZoneId",self.tunnelSz.zoneId)
        
        self.sky = loader.loadModel(self.SKYMODEL)
        self.sky.reparentTo(self.np)
        self.sky.setScale(10)
        sets=open("tth/areas/mapSet.py",'w')
        sets.write("wantMap=True")
        
        self.loadMaps()
        
        self.tunnels = {}
        
        ft = None
        if tp:
            if hasattr(tp,'tunnel') and tp.tunnel:
                ft = tp.tunnel.area.name
                
        self.__setupTunnels(ft)
        
    def __setupTunnels(self,fromTunnel):
        #print 'stTunnels'
        
        _to_fix = []
        _tunnels = []
        
        for x in self.environ.findAllMatches('**/link*'):
            _,hood,name,_ = repr(x).split('/')[-1].split('_')
            
            #determine target
            name = str(int(name) // 100 * 100)
            hood = hood.upper()
            if hood == "TT": hood = "TTC"
            
            if name.endswith("000"):
                if not self.hasHQ and name[-3:] != str(self.zoneId)[:-3]:
                    target = self.tunnelSz 
                else:
                    print '\t*** hq tunnel:',name
                    target = base.hoodMgr.getHQFromOldStyle(int(name),self.tunnelSz)
                
            else: target = target = eval(hood+"_"+name)
                
            _tunnels.append((x,name,target))
                
            print '\t',name,target
            
        self._tunnelMovie(_tunnels,fromTunnel)
            
#toontown central streets
class TTCStreet(HoodStreet):
    music = "phase_3.5/audio/bgm/TC_SZ.mid"
    SKYMODEL = "phase_3.5/models/props/TT_sky"
    def __init__(self,tp=None):
        from hoods import TTCentral
        self.tunnelSz = TTCentral
        
        HoodStreet.__init__(self,STPATH % "toontown_central_"+self.name.split('_')[-1],tp)

        if tp: tp.done()
        
class TTC_2100(TTCStreet):
    zoneId = 1100
    name = "AREA_ST_2100"
    hood = 2000
    disneyId = 2100
        
class TTC_2200(TTCStreet):
    zoneId = 1200
    name = "AREA_ST_2200"
    hood = 2000
    disneyId = 2200
        
class TTC_2300(TTCStreet):
    zoneId = 1300
    name = "AREA_ST_2300"
    hood = 2000
    disneyId = 2300
        
#docks streets
class DDStreet(HoodStreet):
    music = "phase_6/audio/bgm/DD_SZ.mid"
    SKYMODEL = "phase_3.5/models/props/BR_sky"
    def __init__(self,tp=None):     
        from hoods import Dock
        self.tunnelSz = Dock
        
        HoodStreet.__init__(self,STPATH % "donalds_dock_"+self.name.split('_')[-1],tp)
        
        if tp: tp.done()
    
class DD_1100(DDStreet):
    zoneId = 2100
    name = "AREA_ST_1100"
    hood = 1000
    disneyId = 1100

class DD_1200(DDStreet):
    zoneId = 2200
    name = "AREA_ST_1200"
    hood = 1000
    disneyId = 1200
        
class DD_1300(DDStreet):
    zoneId = 2300
    name = "AREA_ST_1300"
    hood = 1000
    disneyId = 1300
    
#garden streets
class DGStreet(HoodStreet):
    music = "phase_8/audio/bgm/DG_SZ.mid"
    SKYMODEL = "phase_3.5/models/props/TT_sky"
    def __init__(self,tp=None):     
        from hoods import Garden
        self.tunnelSz = Garden
        
        HoodStreet.__init__(self,STPATH % "daisys_garden_"+self.name.split('_')[-1],tp)
        
        if tp: tp.done()
    
class DG_5100(DGStreet):
    zoneId = 3100
    name = "AREA_ST_5100"
    hood = 5000
    disneyId = 5100

class DG_5200(DGStreet):
    zoneId = 3200
    name = "AREA_ST_5200"
    hood = 5000
    disneyId = 5200
    
class DG_5300(DGStreet):
    zoneId = 3300
    name = "AREA_ST_5300"
    hasHQ = True
    hood = 5000
    disneyId = 5300
    
#mml streets
class MMStreet(HoodStreet):
    music = "phase_6/audio/bgm/MM_SZ.mid"
    SKYMODEL = "phase_6/models/props/MM_sky"
    def __init__(self,tp=None):     
        from hoods import Melodyland
        self.tunnelSz = Melodyland
        
        HoodStreet.__init__(self,STPATH % "minnies_melody_land_"+self.name.split('_')[-1],tp)
        
        if tp: tp.done()
        
class MM_4100(MMStreet):
    zoneId = 4100
    name = "AREA_ST_4100"
    hood = 4000
    disneyId = 4100
    
class MM_4200(MMStreet):
    zoneId = 4200
    name = "AREA_ST_4200"
    hood = 4000
    disneyId = 4200
    
class MM_4300(MMStreet):
    zoneId = 4300
    name = "AREA_ST_4300"
    hood = 4000
    disneyId = 4300
    
#brrrgh streets
class BRStreet(HoodStreet):
    music = "phase_8/audio/bgm/TB_SZ.mid"
    SKYMODEL = "phase_3.5/models/props/BR_sky"
    def __init__(self,tp=None):     
        from hoods import Brrrgh
        self.tunnelSz = Brrrgh
        
        HoodStreet.__init__(self,STPATH % "the_burrrgh_"+self.name.split('_')[-1],tp)
		
        if tp: tp.done()
        
class BR_3100(BRStreet):
    zoneId = 5100
    name = "AREA_ST_3100"
    hood = 3000
    disneyId = 3100
    
class BR_3200(BRStreet):
    zoneId = 5200
    name = "AREA_ST_3200"
    hood = 3000
    disneyId = 3200
    
class BR_3300(BRStreet):
    zoneId = 5300
    name = "AREA_ST_3300"
    hasHQ = True
    hood = 3000
    disneyId = 5300
    
#dreamland streets
class DLStreet(HoodStreet):
    music = "phase_8/audio/bgm/DL_SZ.mid"
    SKYMODEL = "phase_8/models/props/DL_sky"
    def __init__(self,tp=None):     
        from hoods import Dreamland
        self.tunnelSz = Dreamland
        
        HoodStreet.__init__(self,STPATH % "donalds_dreamland_"+self.name.split('_')[-1],tp)
        
        if tp: tp.done()
        
class DL_9100(DLStreet):
    zoneId = 6100
    name = "AREA_ST_9100"
    hood = 9000
    disneyId = 9100

class DL_9200(DLStreet):
    zoneId = 6200
    name = "AREA_ST_9200"
    hasHQ = True
    hood = 9000
    disneyId = 9200
    
