from pandac.PandaModules import *
from direct.gui.DirectGui import *
from direct.directnotify import DirectNotifyGlobal

TADPbCancel = 0.05
TADPbCancelPos = (-0.865, 0.0, -0.78)
TADPtrackLabel = 0.066
TADtrackLabelPosZ = 0.08

AvatarDetailPanelClose = 'Close'
AvatarDetailPanelOnline = 'District: %(district)s\nLocation: %(location)s'
Offline = 'offline'

class ToonAvatarDetailPanel(DirectFrame):

    notify = DirectNotifyGlobal.directNotify.newCategory('ToonAvatarDetailPanel')

    def __init__(self, parentPanel, **kw):
        buttons = loader.loadModel('phase_3/models/gui/dialog_box_buttons_gui')
        gui = loader.loadModel('phase_3.5/models/gui/avatar_panel_gui')
        detailPanel = gui.find('**/avatarInfoPanel')
        self.playerId = parentPanel.playerId
        textScale = 0.095
        textWrap = 16.4
        self.playerInfo = parentPanel.playerInfo

        optiondefs = (('pos', (-.575, 0.0, 0.0), None),
         ('scale', 0.5, None),
         ('relief', None, None),
         ('image', detailPanel, None),
         ('image_color', Vec4(1,1,1,1), None),
         ('text', '', None),
         ('text_wordwrap', textWrap, None),
         ('text_scale', textScale, None),
         ('text_pos', (-0.125, 0.775), None))
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, parentPanel.frame)
        self.dataText = DirectLabel(self, text='', text_scale=0.09, text_align=TextNode.ALeft, text_wordwrap=15, relief=None, pos=(-0.85, 0.0, 0.645))
        self.avId = self.playerId
        self.avName = parentPanel.avName

        self.bCancel = DirectButton(self, image=(buttons.find('**/CloseBtn_UP'), buttons.find('**/CloseBtn_DN'), buttons.find('**/CloseBtn_Rllvr')), image_scale=1.1, relief=None, text=AvatarDetailPanelClose, text_scale=TADPbCancel, text_pos=(0.12, -0.01), pos=TADPbCancelPos, scale=2.0, command=self.__handleCancel)
        self.bCancel.hide()
        self.initialiseoptions(ToonAvatarDetailPanel)
        buttons.removeNode()
        gui.removeNode()
        
        self.bCancel['text'] = AvatarDetailPanelClose
        self.bCancel.show()

        online = self.playerInfo.get("isOnline",False)
        location = self.playerInfo.get("location",None)
        if online and location:
            location = int(location)
            
            shard,hoodName = location//10**7, L10N(self.playerInfo.get("lastAreaName","??")) #,location%10**7
            
            try: shardName = base.distMgr.names[shard]
            except: shardName = "?"
            #hoodName = base.hoodMgr.getFullnameFromId(hood)
            text = AvatarDetailPanelOnline % {'district': shardName,'location': hoodName}
        else:
            text = AvatarDetailPanelOnline % {'district': Offline,'location': Offline}
            
        self.dataText['text'] = text
        self.__updateTrackInfo()
        self.__updateTrophyInfo()
        return
        
    def __handleCancel(self):
        self.removeNode()

    def __updateTrackInfo(self):
        xOffset = -0.501814
        xSpacing = 0.1835
        yOffset = 0.1
        ySpacing = -0.115
        inventoryModels = loader.loadModel('phase_3.5/models/gui/inventory_gui')
        buttonModel = inventoryModels.find('**/InventoryButtonUp')
        
        gags = self.playerInfo["gags"]
        invModel = loader.loadModel('phase_3.5/models/gui/inventory_icons')
        AvPropsNew=(
            ('inventory_feather','inventory_megaphone','inventory_lipstick',
            'inventory_bamboo_cane','inventory_pixiedust','inventory_juggling_cubes','inventory_ladder'),
            ('inventory_bannana_peel','inventory_rake','inventory_marbles','inventory_quicksand_icon',
            'inventory_trapdoor','inventory_tnt','inventory_traintracks'),
            ('inventory_1dollarbill','inventory_small_magnet','inventory_5dollarbill',
            'inventory_big_magnet','inventory_10dollarbill','inventory_hypno_goggles','inventory_screen'),
            ('inventory_bikehorn','inventory_whistle','inventory_bugle','inventory_aoogah',
            'inventory_elephant','inventory_fog_horn','inventory_opera_singer'),
            ('inventory_tart','inventory_fruit_pie_slice','inventory_cream_pie_slice',
            'inventory_fruitpie','inventory_creampie','inventory_cake','inventory_wedding'),
            ('inventory_squirt_flower','inventory_glass_of_water','inventory_water_gun',
            'inventory_seltzer_bottle','inventory_firehose','inventory_storm_cloud','inventory_geyser'),
            ('inventory_flower_pot','inventory_sandbag','inventory_anvil','inventory_weight',
            'inventory_safe_box','inventory_piano','inventory_ship')
            )
        
        #print gags
        
        invModels = []
        for track in range(len(AvPropsNew)):
            itemList = []
            for item in range(len(AvPropsNew[track])): itemList.append(invModel.find('**/' + AvPropsNew[track][item]))
            invModels.append(itemList)
    
        for track in xrange(7):
            DirectLabel(parent=self, relief=None, text=L10N('GAG_'+str(track)), text_scale=TADPtrackLabel, text_align=TextNode.ALeft, pos=(-0.9, 0, TADtrackLabelPosZ + track * ySpacing))
            trackGags = gags[track]
            for item in xrange(7):
                numItems = trackGags[item]
                if numItems != -1:
                    if numItems == 0:
                        image_color = Vec4(0.5, 0.5, 0.5, 1)
                        geom_color = Vec4(0.2, 0.2, 0.2, 0.5)
                    else:
                        image_color = Vec4(0, 0.6, 1, 1)
                        geom_color = None
                    DirectLabel(parent=self, image=buttonModel, image_scale=(0.92, 1, 1), image_color=image_color, geom=invModels[track][item], geom_color=geom_color, geom_scale=0.6, relief=None, pos=(xOffset + item * xSpacing, 0, yOffset + track * ySpacing))
                
                else: break

        return

    def __updateTrophyInfo(self):
        color = self.playerInfo.get("starColor",None)
        if color:
            gui = loader.loadModel('phase_3.5/models/gui/avatar_panel_gui')
            star = gui.find('**/avatarStar')
            self.star = DirectLabel(parent=self, image=star, image_color=color, pos=(0.610165, 0, -0.760678), scale=0.9, relief=None)
            gui.removeNode()