import math
from tth.tth.areas.estates.EstatePlane import EstatePlane
from tth.tth.gardening.GardenDropGame import GardenDropGame
 
class Estate(Hood):
    name = "AREA_ESTATE"
    zoneId = 1
    music = "phase_13/audio/bgm/party_waltz_dance.mid"
 
    def __init__(self,tp=None):
        self.isNight = False
 
        self.sky = loader.loadModel("phase_3.5/models/props/TT_sky.bam")
        self.sky.reparentTo(render)
        self.sky.setScale(2)
 
        lerper = NodePath('lerper')
        self.sky.find('**/cloud1').setTexProjector(TextureStage.getDefault(), NodePath(), lerper)
        lerper.posInterval(200, VBase3(-1, 0, 0)).loop()
 
        lerper = NodePath('lerper')
        self.sky.find('**/cloud2').setTexProjector(TextureStage.getDefault(), NodePath(), lerper)
        lerper.posInterval(200, VBase3(-1, 0, 0)).loop()
 
        Hood.__init__(self,'phase_5.5/models/estate/terrains.bam')
        self.environ.reparentTo(self.np)
        self.environ.setPos(-4.99989,-0.000152588,2.28882e-005)
        self.tunnel = self.environ.find('**/endtunnel')
        self.tunnel.setPos(-42,-88,6.55)
        self.tunnel.setHpr(180,20,20)
        self.tunnel.setScale(1.25,1.02,0.8)
 
        self.Fog = Fog("Estate Fog")
        self.Fog.setExpDensity(0.002)
        self.np.setFog(self.Fog)
 
        self.pier1 = loader.loadModel("phase_4/models/props/piers_tt.bam")
        self.pier1.reparentTo(self.np)
        self.pier1.setPos(49.1029,-124.805,0.344704)
        self.pier1.setHpr(90,0,0)
        self.pier2 = loader.loadModel("phase_4/models/props/piers_tt.bam")
        self.pier2.reparentTo(self.np)
        self.pier2.setPos(46.5222,-134.739,0.390713)
        self.pier2.setHpr(75,0,0)
        self.pier3 = loader.loadModel("phase_4/models/props/piers_tt.bam")
        self.pier3.reparentTo(self.np)
        self.pier3.setPos(41.31,-144.559,0.375978)
        self.pier3.setHpr(45,0,0)
        self.pier4 = loader.loadModel("phase_4/models/props/piers_tt.bam")
        self.pier4.reparentTo(self.np)
        self.pier4.setPos(46.8254,-113.682,0.46015)
        self.pier4.setHpr(135,0,0)
 
        self.sun = loader.loadModel('phase_4/models/props/sun.bam')
        self.moon = loader.loadModel('phase_5.5/models/props/moon.bam')
        self.sunMoonNode = self.np.attachNewNode('sunMoon')
        self.sunMoonNode.setPosHpr(0, 0, 0, 0, 0, 0)
        if self.sun:
            self.sun.reparentTo(self.sunMoonNode)
            self.sun.setY(270)
            self.sun.setScale(2)
            self.sun.setBillboardPointEye()
        if self.moon:
            self.moon.reparentTo(self.sunMoonNode)
            self.moon.setY(-270)
            self.moon.setScale(15)
            self.moon.setBillboardPointEye()
        self.sunMoonNode.setP(30)
 
        self.wheelbarrow = loader.loadModel("phase_5.5/models/estate/wheelbarrel.bam")
        self.wheelbarrow.reparentTo(self.np)
        self.wheelbarrow.setPos(-132,-0,0.71)
        self.wheelbarrow.setHpr(-197,0,0)
 
        self.jukebox = loader.loadModel("phase_13/models/parties/jukebox_model.bam")
        self.jukebox.reparentTo(self.np)
        self.jukebox.setPos(26.1,0,10.71)
        self.jukebox.setHpr(-3,0,0)
 
        self.createToonHouse('1',color=(1,0.4,0.4,1),name="House 1")
        self.createToonHouse('2',0.18,color=(0.4,0.8,0.5,1),name="House 2")
        self.createToonHouse('3',0.18,-90,pos=(0,1.75,0))
        self.createToonHouse('4',0.18)
        self.createToonHouse('5',(-0.17,0.17,0.17),90,color=(0.59,0.39,0.85,1),name="House 3")
        self.createToonHouse('6',(-0.05,0.05,0.05),0,(0.5,-0.25,0),color=(0.9,0.85,0.2,1),name="House 6")
        self.createToonHouse('7',h=0,color=(0.96,0.6,0.7,1),name="House 5")
        self.createToonHouse('8',0.18,-90,(0,1.5,0),color=(0.4,0.5,0.7,1),name="House 4")
        self.createToonHouse('9',0.11,0)
        self.createToonHouse('10',(0.15,-0.15,0.15),p=180)
 
        EstatePlane.start()
        GardenDropGame.__init__()
 
        self.changeTime()
        self.setHolidayProps(None)
        self.loadSfx()
        self.timeCheck()
 
        seq = Sequence(Func(self.sounds),Wait(10),
                       Func(self.sounds),Wait(20),
                       Func(self.sounds),Wait(15))
        seq.loop()
 
    def loadSfx(self):
        self.birds = []
        for i in xrange(3): 
            self.birds.append(loader.loadSfx("phase_4/audio/sfx/SZ_TC_bird{0}.mp3".format(i+1)))
        self.cricketSound = base.loadSfx('phase_14/audio/sfx/cricketChirp.mp3')
        self.cricketSound.setVolume(0.7)
 
    def sounds(self): 
        if self.isNight == True:
            self.cricketSound.play()
        else:
            random.choice(self.birds).play()
 
    def turnNight(self):
        self.isNight=True
        estateLight = AmbientLight('estateLight')
        estateLight.setColor(VBase4(0.6, 0.6, 0.6, 1))
        lightNode = self.np.attachNewNode(estateLight)
        render.setLight(lightNode)
 
    def turnDay(self):
        self.isNight=False
        render.clearLight()
 
    def timeCheck(self):
        Check = Sequence()
        Check.append(Func(self.turnDay))
        Check.append(Wait(183))
        Check.append(Func(self.turnNight))
        Check.append(Wait(363))
        Check.append(Func(self.turnDay))
        Check.append(Wait(270))
        Check.start()
 
    def changeTime(self):
 
        self.changeToNight = self.sky.find('**/Sky').colorInterval(5,Vec4(0,0,0,1))
        self.move1 = self.sunMoonNode.hprInterval(5,(0,210,0))
        self.changeToDay = self.sky.find('**/Sky').colorInterval(5,Vec4(1,1,1,1))
        self.move2 = self.sunMoonNode.hprInterval(5,(0,30,0))
 
        self.TimeSequence = Sequence(
                                         Wait(180),
                                         Parallel(self.changeToNight,
                                                  self.move1),
                                         Wait(360),
                                         Parallel(self.changeToDay,
                                                  self.move2),
                                         Wait(270))
        self.TimeSequence.loop()
 
    def createToonHouse(self, locator, scale=.12, h=180, pos=0, p=0, color=(1,0.8,0.7,1), name="Toon's House", type=2):
 
        if type == 1:
            house = loader.loadModel('phase_5.5/models/estate/houseA.bam')
        if type == 2:
            house = loader.loadModel('phase_5.5/models/estate/houseBs.bam')
        house.reparentTo(self.environ.find('**/locator_house'+locator))
        house.setScale(scale)
        house.setH(h)
        house.setPos(pos)
        house.setP(p)
        house.find("**/mat_origin").setZ(2.5)
        house.find("**/mat").setColor(0.3)
        self.baseline(house.find("**/sign_origin"),'MickeyFont.bam',color,(0,0.3,0),(1.7,1.6,1.7),name,5,hpr=(90,0,0))
        self.baseline(house.find("**/mat_origin"),'MickeyFont.bam',color,(0.05,0,0),(0.5,0.6,1.7),name,5,hpr=(90,-90,0))
        colorList = ['**/rock_wall_front','**/attic']
        for colorItem in colorList:
            house.find(colorItem).setColor(color)
        door = loader.loadModel("phase_3.5/models/modules/doors_practical.bam").find('**/door_double_round_ul')
        door.reparentTo(house.find('**/door_origin'))
        door.setColor(0.88,0.45,0.38,1)
        door.setH(-90)
 
    def setHolidayProps(self, holiday):
        if holiday == None:
            self.placetree_TT('prop_tree_fat_no_box_ur',(127.118,41.6667,-0.018425),0,1)
            self.placetree_TT('prop_tree_fat_no_box_ur',(130.934,-112.295,4.87703),0,1)
            self.placetree_TT('prop_tree_fat_no_box_ur',(-123.438,-61.7798,-0.0212231),0,1)
            self.placetree_TT('prop_tree_fat_no_box_ur',(-89.2946,155.887,5.88637),0,1)
            self.placetree_TT('prop_tree_fat_no_box_ur',(-19.0631,94.8639,0.251884),0,1)
            self.placetree_TT('prop_tree_large_no_box_ur',(-58.2389,22.6873,2.35777),0,1)
            self.placetree_TT('prop_tree_large_no_box_ur',(-33.3073,-226.712,-0.227959),30,1)
            self.placetree_TT('prop_tree_large_no_box_ur',(91.8022,151.809,0.25066),30,1)
            self.placetree_TT('prop_tree_large_no_box_ur',(-108.708,-179.715,-0.88939),30,1)
            self.placetree_TT('prop_tree_large_no_box_ur',(172.91,27.0758,-0.424359),30,1)
            self.placetree_TT('prop_tree_large_no_box_ur',(48.166,-157.726,0.00427294),30,1)
            self.placetree_TT('prop_tree_large_no_box_ur',(7.15445,-172.415,0.00508118),30,1)
            self.placetree_TT('prop_tree_large_no_box_ur',(61.8133,-2.20992,8.10629),30,1)
            self.placetree_TT('prop_tree_large_no_box_ur',(48.166,-157.726,0.00427294),30,1)
            self.placetree_TT('prop_tree_large_no_box_ur',(-93.9252,46.3882,0.163597),30,1)
            self.placetree_TT('prop_tree_large_no_box_ur',(-87.9846,38.8645,0.038681),30,1)
            self.placetree_TT('prop_tree_large_no_box_ur',(58.2562,73.7532,0.0911045),30,1)
            self.placetree_TT('prop_tree_large_no_box_ur',(98.8038,-66.3475,0.0390043),30,1)
            self.placetree_TT('prop_tree_large_no_box_ur',(-49.0482,-129.666,0.329399),30,1)
            self.placetree_TT('prop_tree_small_no_box_ul',(-51.4214,-24.6363,4.02119),2,1)
            self.placetree_TT('prop_tree_small_no_box_ul',(-63.7942,5.18094,2.61119),2,1)
            self.placetree_TT('prop_tree_small_no_box_ul',(-20.39423,-10.9763,7.15569),2,1)
            self.placetree_TT('prop_tree_small_no_box_ul',(15.92633,-29.2208,6.08492),2,1)
            self.placetree_TT('prop_tree_small_no_box_ul',(-65.0909,-28.2464,4.00514),2,1)
            self.placetree_TT('prop_tree_small_no_box_ul',(-140.916,-118.105,7.46346),2,1)
            self.placetree_TT('prop_tree_small_no_box_ul',(-61.57,-191.095,8.61497),2,1)
            self.placetree_TT('prop_tree_small_no_box_ul',(-50.9591,9.1061,3.06965),2,1)
            self.placetree_TT('prop_tree_small_no_box_ul',(53.3863,-192.501,8.15125),2,1)
            self.placetree_TT('prop_tree_small_no_box_ul',(-168.464,111.89,2.8051),2,1)
            self.placetree_TT('prop_tree_small_no_box_ul',(19.1518,86.819,0.062892),2,1)
            self.placetree_TT('prop_tree_small_no_box_ul',(67.6897,-96.6978,0.0356426),2,1)
            self.placetree_TT('prop_tree_small_no_box_ul',(23.4233,80.1862,0.0406952),2,1)
            self.placetree_TT('prop_tree_small_no_box_ul',(-58.1199,-141,0.0263481),2,1)
            self.placetree_TT('prop_tree_small_no_box_ul',(42.2373,9.56175,8.36716),2,1)
        elif holiday == "Christmas":
            self.placetree_TT('prop_tree_fat_no_box_ur',(127.118,41.6667,-0.018425),0,2)
            self.placetree_TT('prop_tree_fat_no_box_ur',(130.934,-112.295,4.87703),0,2)
            self.placetree_TT('prop_tree_fat_no_box_ur',(-123.438,-61.7798,-0.0212231),0,2)
            self.placetree_TT('prop_tree_fat_no_box_ur',(-89.2946,155.887,5.88637),0,2)
            self.placetree_TT('prop_tree_fat_no_box_ur',(-19.0631,94.8639,0.251884),0,2)
            self.placetree_TT('prop_tree_large_no_box_ur',(-58.2389,22.6873,2.35777),0,2)
            self.placetree_TT('prop_tree_large_no_box_ur',(-33.3073,-226.712,-0.227959),30,2)
            self.placetree_TT('prop_tree_large_no_box_ur',(91.8022,151.809,0.25066),30,2)
            self.placetree_TT('prop_tree_large_no_box_ur',(-108.708,-179.715,-0.88939),30,2)
            self.placetree_TT('prop_tree_large_no_box_ur',(172.91,27.0758,-0.424359),30,2)
            self.placetree_TT('prop_tree_large_no_box_ur',(48.166,-157.726,0.00427294),30,2)
            self.placetree_TT('prop_tree_large_no_box_ur',(7.15445,-172.415,0.00508118),30,2)
            self.placetree_TT('prop_tree_large_no_box_ur',(61.8133,-2.20992,8.10629),30,2)
            self.placetree_TT('prop_tree_large_no_box_ur',(48.166,-157.726,0.00427294),30,2)
            self.placetree_TT('prop_tree_large_no_box_ur',(-93.9252,46.3882,0.163597),30,2)
            self.placetree_TT('prop_tree_large_no_box_ur',(-87.9846,38.8645,0.038681),30,2)
            self.placetree_TT('prop_tree_large_no_box_ur',(58.2562,73.7532,0.0911045),30,2)
            self.placetree_TT('prop_tree_large_no_box_ur',(98.8038,-66.3475,0.0390043),30,2)
            self.placetree_TT('prop_tree_large_no_box_ur',(-49.0482,-129.666,0.329399),30,2)
            self.placetree_TT('prop_tree_small_no_box_ul',(-51.4214,-24.6363,4.02119),2,2)
            self.placetree_TT('prop_tree_small_no_box_ul',(-63.7942,5.18094,2.61119),2,2)
            self.placetree_TT('prop_tree_small_no_box_ul',(-20.39423,-10.9763,7.15569),2,2)
            self.placetree_TT('prop_tree_small_no_box_ul',(15.92633,-29.2208,6.08492),2,2)
            self.placetree_TT('prop_tree_small_no_box_ul',(-65.0909,-28.2464,4.00514),2,2)
            self.placetree_TT('prop_tree_small_no_box_ul',(-140.916,-118.105,7.46346),2,2)
            self.placetree_TT('prop_tree_small_no_box_ul',(-61.57,-191.095,8.61497),2,2)
            self.placetree_TT('prop_tree_small_no_box_ul',(-50.9591,9.1061,3.46965),2,2)
            self.placetree_TT('prop_tree_small_no_box_ul',(53.3863,-192.501,8.15125),2,2)
            self.placetree_TT('prop_tree_small_no_box_ul',(-168.464,111.89,2.8051),2,2)
            self.placetree_TT('prop_tree_small_no_box_ul',(19.1518,86.819,0.062892),2,2)
            self.placetree_TT('prop_tree_small_no_box_ul',(67.6897,-96.6978,0.0356426),2,2)
            self.placetree_TT('prop_tree_small_no_box_ul',(23.4233,80.1862,0.0406952),2,2)
            self.placetree_TT('prop_tree_small_no_box_ul',(-58.1199,-141,0.0263481),2,2)
            self.placetree_TT('prop_tree_small_no_box_ul',(42.2373,9.56175,8.36716),2,2)