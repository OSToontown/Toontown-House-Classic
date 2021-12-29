class FunnyFarm(Hood):
    def makeSeq(self):
        self.planeFly1 = self.airplane.posInterval(15,Point3(152, -165, 100),startPos=Point3(-400, -165, 100))
        self.planeFly2 = self.airplane.posInterval(8,Point3(230, 60, 7),startPos=Point3(152, -165, 100))
        self.planePace = Sequence(self.planeFly1,self.planeFly2,Wait(8))
        self.planePace.loop()
 
    def __init__(self,tp=None):
        self.name = "AREA_FF"
        self.zoneId = 7000
        self.music = "phase_14/audio/bgm/FF_nbrhood.mp3"
         
        self.av_startpos = (
                            ((11.01, 46.3, 0), (-106.3, 0, 0)),
                            ((93.78, 115.385, 0), (133.34, 0, 0)),
                            ((-122.99, 26.27, 0), (349.09, 0, 0)),
                            ((-36.82, -13.09, 0), (490, 0, 0)),
                            ((43.99, -46.49, 0), (242.99, 0, 0)),
                            ((5.55, 25.22, 0), (90, 0, 0)),
                            ((23.69, -51, 0), (-11.1, 0, 0)),
                            ((-67.418, 20.93, 0), (-260.42, 0, 0)),
                            ((86.847, 72.48, 0), (-190.41, 0, 0)),
                            ((71.9911, 52.81, 0), (-22.26, 0, 0)),
                            ((14.6187, 78.93, 0), (-317.73, 0, 0)),
                            ((-29.663, 116.25, 0), (-525.12, 0, 0)),
                            )
 
        Hood.__init__(self,"phase_14/models/neighborhoods/funny_farm.bam")
 
        self.sky = loader.loadModel("phase_14/models/modules/FF_sky.bam")
        self.sky.reparentTo(self.np)
        self.sky.setScale(2)
 
        self.airplane = Actor("phase_4/models/props/SZ_airplane-mod.bam",{"wave":"phase_4/models/props/SZ_airplane-wave.bam"})
        self.airplane.reparentTo(render)
        self.airplane.loop('wave')
        self.airplane.setScale(-45,45,45)
        self.airplane.setPos(152, -136, 100)
        self.airplane.setBillboardAxis(0)
        self.makeSeq()
 
        self.environ.reparentTo(self.np)
 
        self.placetree_FF(0,66)
        self.placetree_FF(-64,39)
        self.placetree_FF(71,-77)
        self.placetree_FF(16,1)
        self.placetree_FF(-57,-57)
        self.placetree_FF(99,37)
        self.placetree_FF(98,91)
        self.placetree_FF(-41,102)
 
        self.placefence_FF((119.5,101,0),-50)
        self.placefence_FF((77.5,133,0),-10)
 
        self.clothshop = self.placebldg("phase_8/models/modules/clothshopDG.bam",(-82,-64,0),145)
        self.baseline(self.clothshop.find("**/sign_origin"),'MickeyFont.bam',(0,0.501961,0,1),(0,-0.5,0),(1.7,1.6,1.7),L10N('PROP_CLOTHSTORE'),9)
        self.door('practical','door_double_clothshop',(0.91,0.34,0.34,1),self.clothshop.find('**/door_origin'))

        self.placebldg("phase_14/models/modules/shed.bam",(-78,107,-0.5),-61.5)
        self.placebldg("phase_4/models/props/goofy_statue.bam",(59,-6,0),0)
        self.placebldg("phase_6/models/golf/golf_gazebo",(5,25,0),0)
 
        self.gs = self.placebldg("phase_14/models/modules/gagshop_FF.bam",(96.244,-74.932,0),70)
        self.door('practical','door_double_square_ur',(1,0.47,0.38,1),self.gs.find('**/door_origin'))
 
        self.pet = self.placebldg("phase_6/models/modules/PetShopExterior_DD.bam", (11,120,0), -4)
        self.door('practical','door_double_round_ur',(1,0.47,0.38,1),self.pet.find('**/door_origin'))
        self.baseline(self.pet.find("**/sign_origin"),'MickeyFont.bam',(1,1,0,1),(-0.0715486,0.575594,0),(1.58014,1.5,2.42354),L10N("PROP_PETSHOP"),9)
 
        self.tunnel1 = self.placetun((-51,-175,-6.6), 0, True, 'FF')
        self.sign1 = loader.loadModel("phase_4/models/props/tunnel_sign_red.bam")
        self.sign1.reparentTo(self.tunnel1.find("**/sign_origin"))
        self.sign1.setPosHprScale(0,-.1,0, 0,0,0, 1.5,1,1.5)
        self.icon1 = loader.loadModel("phase_3.5/models/props/mickeySZ.bam")
        self.icon1.reparentTo(self.sign1.find("**/g1"))
        self.icon1.setPos(0,-.1,1.6)
        self.icon1.setScale(1.9)
        self.baseline(self.sign1,'MickeyFont.bam',(0,0.501961,0,1),(0,-0.45,0),(1.1,0.9,.9),"Cock-A-Doodle Drive",12)
        self.baseline(self.sign1,'MickeyFont.bam',(0,0.501961,0,1),(0,-2,0),(1.1,0.85,.9),"Funny Farm",12)
 
        self.tunnel2 = self.placetun((-237,41.33,-6.6), 284, True, 'FF')
        self.sign2 = loader.loadModel("phase_4/models/props/tunnel_sign_red.bam")
        self.sign2.reparentTo(self.tunnel2.find("**/sign_origin"))
        self.sign2.setPosHprScale(0,-.1,0, 0,0,0, 1.5,1,1.5)
        self.icon2 = loader.loadModel("phase_3.5/models/props/mickeySZ.bam")
        self.icon2.reparentTo(self.sign2.find("**/g1"))
        self.icon2.setPos(0,-.1,1.6)
        self.icon2.setScale(1.9)
        self.baseline(self.sign2,'MickeyFont.bam',(0,0.501961,0,1),(0,-1,0),(1.1,1,.9),"Tractor Trail Funny Farm",10)
 
        self.tunnelAA = self.placebldg("phase_6/models/golf/outdoor_zone_entrance.bam", (110.5,124,0.01),312)
        from funAreas import AcornAcres
        Tunnel(self.tunnelAA,BitMask32(8),self,(AcornAcres,'AREA_ACRES'))
        self.sign('DD',self.tunnelAA,'DD_sign2',(0,0,0),(0,0,0),(2,1,1.4))
        self.baseline(self.tunnelAA.find("**/sign_origin"),'Comedy.bam',(0.439216,0.247059,0.184314,1),(0,0,0),(2.3,1.5,5.7),"Barking Boulevard Funny Farm",10)
 
        self.facade = self.placebldg("phase_3.5/models/modules/facade_bN.bam",(-127,72,0),46)
        self.facadeGlass = loader.loadModel("phase_3.5/models/modules/facade_bN.bam").find('**/showcase')
        self.facadeGlass.reparentTo(self.facade)
        self.facadeGlass.setScale(-1,1,1)
        self.goldenbean = loader.loadModel("phase_4/models/props/jellybean4.bam")
        self.goldenbean.reparentTo(self.facade)
        self.goldenbean.setPos(0,-1.5,4)
        self.goldenbean.setH(90)
        self.goldenbean.setScale(5)
        self.goldenbean.setBillboardAxis(1.5)
        self.goldenbean.setColor(1,0.9,0)
        self.goldenbean.hprInterval(3,Point3(0,0,0),startHpr=Point3(360,0,0)).loop()
        self.glow = loader.loadModel("phase_3.5/models/props/glow.bam")
        self.glow.reparentTo(self.facade)
        self.glow.setPos(0,-1.37,4.1)
        self.glow.setScale(3)
        self.glow.setBillboardAxis(1.65)
        self.glow.setColor(1,0.9,0)
 
        self.facade2 = self.placebldg("phase_3.5/models/modules/facade_a.bam",(121,6,0),234)
        self.gavel = loader.loadModel("phase_5/models/props/gavel.bam")
        self.gavel.reparentTo(self.facade2)
        self.gavel.setPos(0,-1,5)
        self.gavel.setH(180)
        self.gavel.setScale(3)
        self.teeth = loader.loadModel("phase_5/models/props/teeth-mod.bam")
        self.teeth.reparentTo(self.facade2)
        self.teeth.setPos(-2.5,-1,4)
        self.teeth.setH(180)
        self.teeth.setScale(4)
 
        self.placewall((-136.8,24.8,0),'wall_md_dental_ul',120,9,10,(1, 0.7, 0.33, 1))
        self.placewall((-136.8,24.8,10),'wall_md_pillars_ul',120,9,10,(1, 0.7, 0.33, 1))
        self.placewall((-141.2,32.4,0),'wall_lg_brick_ul',150,19,20,(1, 0.7, 0.33, 1))
        self.placewall((-129.2,-32.8,0),'wall_md_board_ur',90,19,10,(1, 0.5, 0.33, 1))
        self.placewall((-129.2,-32.8,10),'wall_sm_wood_ur',90,19,10,(1, 0.7, 0.33, 1))
        self.placewall((-135.6,-50.4,0),'wall_md_blank_ur',70,19,20,(0.42,0.16,0.16,1))
 
        self.fountain = loader.loadModel("phase_5.5/models/estate/garden_mickey_shovel")
        self.fountain.reparentTo(self.np)
        self.fountain.setScale(0.08)
        self.fountain.setPos(-53,9,0)
 
        self.table1 = loader.loadModel('phase_6/models/golf/game_table.bam') 
        self.table1.reparentTo(self.np) 
        self.table1.setPos(56,61,0) 
        self.table1.setHpr(9,0,0)
        self.findfour = loader.loadModel("phase_6/models/golf/findfour_game.bam")
        self.findfour.reparentTo(self.table1.find('**/basket_locator'))
        self.findfour.find('**/pieces').hide()
        self.table2 = loader.loadModel('phase_6/models/golf/game_table.bam') 
        self.table2.reparentTo(self.np) 
        self.table2.setPos(14,-39,0) 
        self.table2.setHpr(90,0,0) 
        self.findfour = loader.loadModel("phase_6/models/golf/findfour_game.bam")
        self.findfour.reparentTo(self.table2.find('**/basket_locator'))
        self.findfour.find('**/pieces').hide()
        self.table3 = loader.loadModel('phase_6/models/golf/game_table.bam') 
        self.table3.reparentTo(self.np) 
        self.table3.setPos(-31,34,0) 
        self.table3.setHpr(-45,0,0) 
        self.findfour = loader.loadModel("phase_6/models/golf/findfour_game.bam")
        self.findfour.reparentTo(self.table3.find('**/basket_locator'))
        self.findfour.find('**/pieces').hide()
        self.table4 = loader.loadModel('phase_6/models/golf/game_table.bam') 
        self.table4.reparentTo(self.np) 
        self.table4.setPos(-97,0,0) 
        self.table4.setHpr(90,0,0) 
        self.findfour = loader.loadModel("phase_6/models/golf/findfour_game.bam")
        self.findfour.reparentTo(self.table4.find('**/basket_locator'))
        self.findfour.find('**/pieces').hide()
 
        self.addCollisionSphere((-134,-16,2),5)
        self.addCollisionSphere((-141,25,2),4)
        self.addCollisionSphere((91,132,2),8)
        self.addCollisionSphere((119,106,2),8)
 
        if tp: tp.done()
 
    def __tth_area__(self):
        return {
                'name':self.name,
                'models':self.np,
                'bgm':self.theme,
                'gui':self.frame,
                'speeches':[]
                }