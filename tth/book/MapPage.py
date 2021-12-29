from BookPage import *
import random

SHOW_UNDER_CLOUDS = True #False

MapPageTitle,MapPageBackToPlayground,MapPageBackToCogHQ,MapPageGoHome,MapPageYouAreHere,MapPageYouAreAtHome,\
    MapPageYouAreAtSomeonesHome,MapPageGoTo = map(L10N,(
                                                         "BOOK_MAP","BOOK_MAP_BACKTOSZ","BOOK_MAP_BACKTOHQ",
                                                         "BOOK_MAP_HOME","BOOK_MAP_UR","BOOK_MAP_ESTATE",
                                                         "BOOK_MAP_SOMEONES","BOOK_MAP_GOTO",
                                                        )
                                                        )
                                                        
MapPageYouAreHere += " %s\n%s"                                           
MapPageYouAreAtHome.format("\n")
MapPageGoTo+="\n%s"

MPsafeZoneButton = 0.055
MPgoHomeButton = 0.055
MPhoodLabel = 0.06
MPhoodLabelWordwrap = 14

def intersection(a, b):
     return list(set(a) & set(b))

class MapPage(BookPage):

    def setup(self):
        mapModel = loader.loadModel('phase_3.5/models/gui/toontown_map')
        self.map = DirectFrame(parent=self.frame, relief=None, image=mapModel.find('**/toontown_map'), image_scale=(1.8, 1, 1.35), scale=0.97, pos=(0, 0, 0.0775))
        mapModel.removeNode()
        self.allZones = [
                         2000,1000, #docks,central
                         5000, #brrrgh
                         4000, #mml
                         3000, #gardens
                         2400, 1400, #acres, speedway
                         6000, # dreamland
                         10000, # bossbot hq
                         7000, # sellbot hq
                         8000, # cashbot hq
                         9000, # lawbot hq
                         ]
                         
        self.safezones = [2000,1000,5000,4000,3000,2400,1400,6000,7000,8000,9000,10000]
        self.avZones = [2000,1000,5000,4000,3000,2400,1400,6000,10000,7000,8000,9000]
        
        #for hood in ToontownGlobals.Hoods:
         #   if hood not in [ToontownGlobals.GolfZone, ToontownGlobals.FunnyFarm]:
          #      self.allZones.append(hood)

        self.cloudScaleList = (((0.55, 0, 0.4), (0.35, 0, 0.25)),
         (),
         ((0.45, 0, 0.45), (0.5, 0, 0.4)),
         ((0.7, 0, 0.45),),
         ((0.55, 0, 0.4),),
         ((0.6, 0, 0.4), (0.5332, 0, 0.32)),
         ((0.7, 0, 0.45), (0.7, 0, 0.45)),
         ((0.7998, 0, 0.39),),
         ((0.5, 0, 0.4),),
         ((-0.45, 0, 0.4),),
         ((-0.45, 0, 0.35),),
         ((0.5, 0, 0.35),),
         ((0.5, 0, 0.35),))
        self.cloudPosList = (((0.575, 0.0, -0.04), (0.45, 0.0, -0.25)),
         (),
         ((0.375, 0.0, 0.4), (0.5625, 0.0, 0.2)),
         ((-0.02, 0.0, 0.23),),
         ((-0.3, 0.0, -0.4),),
         ((0.25, 0.0, -0.425), (0.125, 0.0, -0.36)),
         ((-0.5625, 0.0, -0.07), (-0.45, 0.0, 0.2125)),
         ((-0.125, 0.0, 0.5),),
         ((0.66, 0.0, -0.4),),
         ((-0.68, 0.0, -0.444),),
         ((-0.6, 0.0, 0.45),),
         ((0.66, 0.0, 0.5),),
         ((0.4, 0.0, -0.35),))
        self.labelPosList = ((0.594, 0.0, -0.075),
         (0.0, 0.0, -0.1),
         (0.475, 0.0, 0.25),
         (0.1, 0.0, 0.15),
         (-0.3, 0.0, -0.375),
         (0.2, 0.0, -0.45),
         (-0.55, 0.0, 0.0),
         (-0.088, 0.0, 0.47),
         (0.7, 0.0, -0.5),
         (-0.7, 0.0, -0.5),
         (-0.7, 0.0, 0.5),
         (0.7, 0.0, 0.5),
         (0.45, 0.0, -0.45))
        self.labels = []
        self.clouds = []
        guiButton = loader.loadModel('phase_3/models/gui/quit_button')
        buttonLoc = (0.45, 0, -0.74)
        if 0: #base.housingEnabled:
            buttonLoc = (0.55, 0, -0.74)
        self.safeZoneButton = DirectButton(parent=self.map, relief=None, image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR')), image_scale=(1.3, 1.1, 1.1), pos=buttonLoc, text=MapPageBackToPlayground, text_scale=MPsafeZoneButton, text_pos=(0, -0.02), textMayChange=0, command=self.backToSafeZone)
        self.goHomeButton = DirectButton(parent=self.map, relief=None, image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR')), image_scale=(0.66, 1.1, 1.1), pos=(0.15, 0, -0.74), text=MapPageGoHome, text_scale=MPgoHomeButton, text_pos=(0, -0.02), textMayChange=0, command=self.goHome)
        self.goHomeButton.hide()
        guiButton.removeNode()
        self.hoodLabel = DirectLabel(parent=self.map, relief=None, pos=(-0.43, 0, -0.726), text='', text_scale=MPhoodLabel, text_pos=(0, 0), text_wordwrap=MPhoodLabelWordwrap)
        self.hoodLabel.hide()
        cloudModel = loader.loadModel('phase_3.5/models/gui/cloud')
        cloudImage = cloudModel.find('**/cloud')
        for hood in self.allZones:
            abbrev = base.hoodMgr.getNameFromId(hood)
            fullname = base.hoodMgr.getFullnameFromId(hood)
            hoodIndex = self.allZones.index(hood)
            label = DirectButton(parent=self.map, relief=None, pos=self.labelPosList[hoodIndex], pad=(0.2, 0.16), text=('', fullname, fullname), text_bg=Vec4(1, 1, 1, 0.4), text_scale=0.055, text_wordwrap=8, rolloverSound=None, clickSound=None, pressEffect=0, command=self.__buttonCallback, extraArgs=[hood], sortOrder=1)
            label.bind(DGG.WITHIN, self.__hoverCallback, extraArgs=[1, hoodIndex])
            label.bind(DGG.WITHOUT, self.__hoverCallback, extraArgs=[0, hoodIndex])
            label.resetFrameSize()
            self.labels.append(label)
            hoodClouds = []
            for cloudScale, cloudPos in zip(self.cloudScaleList[hoodIndex], self.cloudPosList[hoodIndex]):
                cloud = DirectFrame(parent=self.map, relief=None, state=DGG.DISABLED, image=cloudImage, scale=(cloudScale[0], cloudScale[1], cloudScale[2]), pos=(cloudPos[0], cloudPos[1], cloudPos[2]))
                cloud.hide()
                hoodClouds.append(cloud)

            self.clouds.append(hoodClouds)

        cloudModel.removeNode()

        zone = gamebase.toonAvatar[0].zoneId % 10**7
        print zone

        if zone >= 7000: self.safeZoneButton['text'] = MapPageBackToCogHQ
        else: self.safeZoneButton['text'] = MapPageBackToPlayground
        
        if zone and zone in self.safezones: self.safeZoneButton.hide()
        else: self.safeZoneButton.show()
        
        if True: self.goHomeButton.hide()
        elif base.housingEnabled: self.goHomeButton.show()
        
        if False: #base.cr.playGame.getPlaceId() == ToontownGlobals.MyEstate:
            if base.cr.playGame.hood.loader.atMyEstate():
                self.hoodLabel['text'] = MapPageYouAreAtHome
                self.hoodLabel.show()
            else:
                avatar = base.cr.identifyAvatar(base.cr.playGame.hood.loader.estateOwnerId)
                if avatar:
                    avName = avatar.getName()
                    self.hoodLabel['text'] = MapPageYouAreAtSomeonesHome % GetPossesive(avName)
                    self.hoodLabel.show()
        elif zone:
            hoodName = base.hoodMgr.id2name.get(zone, '')
            streetName = L10N('AREA_ST_'+str(zone))
            
            if streetName.startswith("L10N"): streetName = ""
            
            if hoodName:
                self.hoodLabel['text'] = MapPageYouAreHere % (hoodName, streetName)
                self.hoodLabel.show()
            else:
                self.hoodLabel.hide()
        else:
            self.hoodLabel.hide()
            
        safeZonesVisited = self.allZones
        hoodsAvailable = self.avZones
        hoodVisibleList = intersection(safeZonesVisited, hoodsAvailable)
        hoodTeleportList = hoodVisibleList #base.localAvatar.getTeleportAccess()
        
        self.hoodTeleportList = hoodTeleportList
        
        for hood in self.allZones:
            label = self.labels[self.allZones.index(hood)]
            clouds = self.clouds[self.allZones.index(hood)]
            if hood in hoodVisibleList:
                label['text_fg'] = (0, 0, 0, 1)
                label.show()
                for cloud in clouds:
                    cloud.hide()

                fullname = base.hoodMgr.getFullnameFromId(hood)
                if hood in hoodTeleportList:
                    text = MapPageGoTo % fullname
                    label['text'] = ('', text, text)
                else:
                    label['text'] = ('', fullname, fullname)
            else:
                label['text_fg'] = (0, 0, 0, 0.65)
                label.show()
                for cloud in clouds:
                    cloud.show()

    def backToSafeZone(self):
        back = base.hoodMgr.getSafezoneCode(gamebase.toonAvatar[0].zoneId % 10**7)
        self.book.close(tpRequest = (str(back),))
        
    def goHome(self):
        pass

    def __buttonCallback(self, hood):
        if hood in self.hoodTeleportList:
            print 'Teleport',hood
            self.book.close(tpRequest = (str(hood),))

    def __hoverCallback(self, inside, hoodIndex, pos):
        if not SHOW_UNDER_CLOUDS: return # do not show below cloud
        alpha = 0.25 if inside else 1.0
        try:
            clouds = self.clouds[hoodIndex]
        except ValueError:
            clouds = []

        for cloud in clouds:
            cloud.setColor((1,
             1,
             1,
             alpha))