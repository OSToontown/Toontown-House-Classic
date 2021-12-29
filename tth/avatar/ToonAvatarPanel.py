from pandac.PandaModules import *
from direct.gui.DirectGui import *
from ToonHead import ToonHead
from ToonDNA import ToonDNA
from tth.gui.hud import LaffOMeter
from direct.directnotify import DirectNotifyGlobal
from ToonAvatarDetailPanel import ToonAvatarDetailPanel

AvatarPanelFriends = L10N('APFriends')
AvatarPanelWhisper,AvatarPanelSecrets,AvatarPanelGoTo,AvatarPanelPet,\
    AvatarPanelIgnore,AvatarPanelReport,AvatarPanelDetail,\
    AvatarPanelGroupInvite,AvatarPanelGroupMember,\
    AvatarPanelGroupMemberKick = map(
                                     L10N,
                                     (
                                      "APWhisper","APSecrets","APGoTo",
                                      "APPet","APIgnore","APReport",
                                      "APDetail","APGroupInvite",
                                      "APGroupMember","APGroupMemberKick"
                                      )
                                    )


TAPwhisperButton = 0.06
TAPsecretsButton = 0.045
TAPgroupFrame = 0.05
TAPgroupButton = 0.055
IGNORE_SCALE = 0.06
STOP_IGNORE_SCALE = 0.04

from direct.showbase.DirectObject import DirectObject
class ToonAvatarPanel(DirectObject):

    notify = DirectNotifyGlobal.directNotify.newCategory('ToonAvatarPanel')

    def __init__(self, playerId, doId, dna):
        self.notify.info('Opening toon panel, avId=%d' % playerId)
        print('Opening toon panel, avId=%d' % playerId)
        
        self.playerId = playerId
        self.doId = doId
        self.playerInfo = dna
        self.avName = dna['name']
                
        messenger.send("requestToonData",[self.playerId,self.doId,self.__gotInfo])
        
        self.laffMeter = None
        wantsLaffMeter = True

        gui = loader.loadModel('phase_3.5/models/gui/avatar_panel_gui')
        self.frame = DirectFrame(image=gui.find('**/avatar_panel'), relief=None, pos=(1.1, 100, 0.525))
        self.frame.wrtReparentTo(gamebase.curArea.hud[4])
        gamebase.curArea.hud[4].obscure(1)
        
        self.disabledImageColor = Vec4(1, 1, 1, 0.4)
        self.text0Color = Vec4(1, 1, 1, 1)
        self.text1Color = Vec4(0.5, 1, 0.5, 1)
        self.text2Color = Vec4(1, 1, 0.5, 1)
        self.text3Color = Vec4(0.6, 0.6, 0.6, 1)
        self.head = self.frame.attachNewNode('head')
        self.head.setPos(0.02, 0, 0.3)
        
        self.headModel = ToonHead()
        self.headModel.setupHead(ToonDNA(dna['dna']),True) #must be ToonDNA, to be fixed
        self.headModel.reparentTo(self.head)
        self.headModel.startBlink()
        self.headModel.startLookAround()
        
        self.headModel.setScale(.135)
        self.head.setH(180)
        
        self.healthText = DirectLabel(parent=self.frame, text='', pos=(0.06, 0, 0.2), text_pos=(0, 0), text_scale=0.05)
        self.healthText.hide()
        self.nameLabel = DirectLabel(parent=self.frame, pos=(0.0125, 0, 0.4), relief=None, text=self.avName, text_fg=Vec4(0, 0, 0, 1), text_pos=(0, 0), text_scale=0.042, text_wordwrap=7.5, text_shadow=(1, 1, 1, 1))
        self.closeButton = DirectButton(parent=self.frame, image=(gui.find('**/CloseBtn_UP'),
         gui.find('**/CloseBtn_DN'),
         gui.find('**/CloseBtn_Rllvr'),
         gui.find('**/CloseBtn_UP')), relief=None, pos=(0.157644, 0, -0.379167), command=self.__handleClose)
        self.friendButton = DirectButton(parent=self.frame, image=(gui.find('**/Frnds_Btn_UP'),
         gui.find('**/Frnds_Btn_DN'),
         gui.find('**/Frnds_Btn_RLVR'),
         gui.find('**/Frnds_Btn_UP')), image3_color=self.disabledImageColor, image_scale=0.9, relief=None, text=AvatarPanelFriends, text_scale=0.06, pos=(-0.103, 0, 0.133), text0_fg=self.text0Color, text1_fg=self.text1Color, text2_fg=self.text2Color, text3_fg=self.text3Color, text_pos=(0.06, -0.02), text_align=TextNode.ALeft, command=self.__handleFriend)
        
        if 0: self.friendButton['state'] = DGG.DISABLED
        
        self.goToButton = DirectButton(parent=self.frame, image=(gui.find('**/Go2_Btn_UP'),
         gui.find('**/Go2_Btn_DN'),
         gui.find('**/Go2_Btn_RLVR'),
         gui.find('**/Go2_Btn_UP')), image3_color=self.disabledImageColor, image_scale=0.9, relief=None, pos=(-0.103, 0, 0.045), text=AvatarPanelGoTo, text0_fg=self.text0Color, text1_fg=self.text1Color, text2_fg=self.text2Color, text3_fg=self.text3Color, text_scale=0.06, text_pos=(0.06, -0.015), text_align=TextNode.ALeft, command=self.__handleGoto)
        
        if 1: self.goToButton['state'] = DGG.DISABLED
        
        self.whisperButton = DirectButton(parent=self.frame, image=(gui.find('**/ChtBx_ChtBtn_UP'),
         gui.find('**/ChtBx_ChtBtn_DN'),
         gui.find('**/ChtBx_ChtBtn_RLVR'),
         gui.find('**/ChtBx_ChtBtn_UP')), image3_color=self.disabledImageColor, image_scale=0.9, relief=None, pos=(-0.103, 0, -0.0375), text=AvatarPanelWhisper, text0_fg=self.text0Color, text1_fg=self.text1Color, text2_fg=self.text2Color, text3_fg=self.text3Color, text_scale=TAPwhisperButton, text_pos=(0.06, -0.0125), text_align=TextNode.ALeft, command=self.__handleWhisper)
        
        if 1: self.whisperButton['state'] = DGG.DISABLED
        
        self.secretsButton = DirectButton(parent=self.frame, image=(gui.find('**/Amuse_Btn_UP'),
         gui.find('**/Amuse_Btn_DN'),
         gui.find('**/Amuse_Btn_RLVR'),
         gui.find('**/Amuse_Btn_UP')), image3_color=self.disabledImageColor, image_scale=0.9, relief=None, pos=(-0.103, 0, -0.13), text=AvatarPanelSecrets, text0_fg=self.text0Color, text1_fg=self.text1Color, text2_fg=self.text2Color, text3_fg=self.text3Color, text_scale=TAPsecretsButton, text_pos=(0.055, -0.01), text_align=TextNode.ALeft, command=self.__handleSecrets)
        
        if 1: self.secretsButton['state'] = DGG.DISABLED
        
        ignoreStr, ignoreCmd, ignoreScale = (AvatarPanelIgnore, lambda:0, IGNORE_SCALE) #self.getIgnoreButtonInfo()
        self.ignoreButton = DirectButton(parent=self.frame, image=(gui.find('**/Ignore_Btn_UP'),
         gui.find('**/Ignore_Btn_DN'),
         gui.find('**/Ignore_Btn_RLVR'),
         gui.find('**/Ignore_Btn_UP')), image3_color=self.disabledImageColor, image_scale=0.9, relief=None, pos=(-0.103697, 0, -0.21), text=ignoreStr, text0_fg=self.text0Color, text1_fg=self.text1Color, text2_fg=self.text2Color, text3_fg=self.text3Color, text_scale=ignoreScale, text_pos=(0.06, -0.015), text_align=TextNode.ALeft, command=ignoreCmd)
        if 1:
            self.reportButton = DirectButton(parent=self.frame, image=(gui.find('**/report_BtnUP'),
             gui.find('**/report_BtnDN'),
             gui.find('**/report_BtnRLVR'),
             gui.find('**/report_BtnUP')), image3_color=self.disabledImageColor, image_scale=0.65, relief=None, pos=(-0.103, 0, -0.29738), text=AvatarPanelReport, text0_fg=self.text0Color, text1_fg=self.text1Color, text2_fg=self.text2Color, text3_fg=self.text3Color, text_scale=0.06, text_pos=(0.06, -0.015), text_align=TextNode.ALeft, command=lambda:0)
        
        if 1:
            self.ignoreButton['state'] = DGG.DISABLED
            self.reportButton['state'] = DGG.DISABLED
        
        self.detailButton = DirectButton(parent=self.frame, image=(gui.find('**/ChtBx_BackBtn_UP'),
         gui.find('**/ChtBx_BackBtn_DN'),
         gui.find('**/ChtBx_BackBtn_Rllvr'),
         gui.find('**/ChtBx_BackBtn_UP')), relief=None, text=('',
         AvatarPanelDetail,
         AvatarPanelDetail,
         ''), text_fg=self.text2Color, text_shadow=(0, 0, 0, 1), text_scale=0.055, text_pos=(-0.075, -0.01), text_align=TextNode.ARight, pos=(-0.133773, 0, -0.395), command=self.__handleDetails)
        self.detailButton["state"] = DGG.DISABLED
        #self.__makeBoardingGui()
        #self.__makePetGui(avatar)
        #self.__checkGroupStatus()
        gui.removeNode()
        
        self.dtPanel = None
        
        self.accept('noFrAsk',self.toggle,[self.friendButton,DGG.DISABLED])
        self.accept('okFrAsk',self.toggle,[self.friendButton,DGG.NORMAL])

        self.frame.show()
    
    def toggle(self,x,state):
        x['state'] = state
        
    def __gotInfo(self,data):
        avatar = data
        #print data
        self.playerInfo.update(data)
        
        if 1:
            self.__makeLaffMeter(avatar)
            self.__updateHp(int(avatar['curhp']), int(avatar['hp']))
            self.healthText.show()
        menuX = -0.05
        menuScale = 0.064

        self.toggle(self.detailButton,DGG.NORMAL)
        messenger.send('avPanelDone')
        return

    def disableAll(self):
        self.detailButton['state'] = DGG.DISABLED
        self.reportButton['state'] = DGG.DISABLED
        self.ignoreButton['state'] = DGG.DISABLED
        self.goToButton['state'] = DGG.DISABLED
        self.secretsButton['state'] = DGG.DISABLED
        self.whisperButton['state'] = DGG.DISABLED
        self.petButton['state'] = DGG.DISABLED
        self.friendButton['state'] = DGG.DISABLED
        self.closeButton['state'] = DGG.DISABLED
        self.groupButton['state'] = DGG.DISABLED
        self.boardingInfoButton['state'] = DGG.DISABLED

    def cleanup(self):
        if not hasattr(self, 'frame') or self.frame == None:
            return
        self.notify.info('Clean up toon panel, avId=%d' % self.playerId)
        if self.dtPanel: self.dtPanel.removeNode()
        if self.frame: self.frame.destroy()
        self.frame = None
        self.dtPanel = None
        self.headModel.stopBlink()
        self.headModel.stopLookAroundNow()
        self.headModel.delete()
        del self.headModel
        self.laffMeter = None
        
        self.ignoreAll()
        gamebase.curArea.hud[4].obscure(0)

    def __handleGoto(self):
        pass

    def __handleToPet(self):
        self.disableAll()
        return

    def __petDetailsLoaded(self, avatar):
        self.cleanup()
        return

    def __handleWhisper(self):
        base.localAvatar.chatMgr.whisperTo(self.avName, self.avId, None)
        return

    def __handleSecrets(self):
        base.localAvatar.chatMgr.noWhisper()
        ToontownFriendSecret.showFriendSecret(ToontownFriendSecret.AvatarSecret)

    def __handleFriend(self):
        messenger.send('askFriend', [self,self.avName,gamebase.toonAvatarStream.read("name")])

    def __handleDetails(self):
        self.dtPanel = ToonAvatarDetailPanel(self)

    def __handleDisableAvatar(self):
        if not base.cr.isFriend(self.avId):
            self.cleanup()
            AvatarPanelBase.currentAvatarPanel = None
        else:
            self.healthText.hide()
            if self.laffMeter != None:
                self.laffMeter.stop()
                self.laffMeter.destroy()
                self.laffMeter = None
        return

    def __handleGenerateAvatar(self, avatar):
        newAvatar = base.cr.doId2do.get(self.avatar.doId)
        if newAvatar:
            self.avatar = newAvatar
        self.__updateLaffMeter(avatar, avatar.hp, avatar.maxHp)
        self.__checkGroupStatus()

    def __updateLaffMeter(self, avatar, hp, maxHp):
        if self.laffMeter == None:
            self.__makeLaffMeter(avatar)
        self.__updateHp(avatar.hp, avatar.maxHp)
        self.laffMeter.show()
        self.healthText.show()
        return

    def __makeLaffMeter(self, avatar):
    
        _hp = map(int,(avatar['curhp'], avatar['hp']))
        _spc = int(avatar['spc'])
        print _spc
        _color = avatar['color1']
        
        self.laffMeter = LaffOMeter(self.frame, _hp, _spc, _color)
        self.laffMeter._meter.setPos(-0.1, 0, 0.24)
        self.laffMeter._meter.setScale(0.03)

    def __updateHp(self, hp, maxHp, quietly = 0):
        if self.laffMeter != None and hp != None and maxHp != None:
            self.laffMeter.update(map(int,(hp, maxHp)))
            self.healthText['text'] = '%d / %d' % (hp, maxHp)
        return

    def __handleClose(self):
        self.cleanup()

    def getAvId(self):
        if hasattr(self, 'avatar'):
            if self.avatar:
                return self.avatar.doId
        return None

    def getPlayerId(self):
        if hasattr(self, 'playerId'):
            return self.playerId
        return None

    def isHidden(self):
        if not hasattr(self, 'frame') or not self.frame:
            return 1
        return self.frame.isHidden()

    def getType(self):
        return 'toon'

    def handleInvite(self):
        if localAvatar.boardingParty.isInviteePanelUp():
            localAvatar.boardingParty.showMe(BoardingPendingInvite, pos=(0, 0, 0))
        else:
            self.groupButton['state'] = DGG.DISABLED
            localAvatar.boardingParty.requestInvite(self.avId)

    def handleKick(self):
        if not base.cr.playGame.getPlace().getState() == 'elevator':
            self.confirmKickOutDialog = TTDialog.TTDialog(style=TTDialog.YesNo, text=BoardingKickOutConfirm % self.avName, command=self.__confirmKickOutCallback)
            self.confirmKickOutDialog.show()

    def __confirmKickOutCallback(self, value):
        if self.confirmKickOutDialog:
            self.confirmKickOutDialog.destroy()
        self.confirmKickOutDialog = None
        if value > 0:
            if self.groupButton:
                self.groupButton['state'] = DGG.DISABLED
            localAvatar.boardingParty.requestKick(self.avId)
        return

    def __checkGroupStatus(self):
        self.groupFrame.hide()
        if hasattr(self, 'avatar'):
            if self.avatar and hasattr(self.avatar, 'getZoneId') and localAvatar.getZoneId() == self.avatar.getZoneId():
                if localAvatar.boardingParty:
                    if self.avId in localAvatar.boardingParty.getGroupMemberList(localAvatar.doId):
                        if localAvatar.boardingParty.getGroupLeader(localAvatar.doId) == localAvatar.doId:
                            self.groupButton['text'] = ('', AvatarPanelGroupMemberKick, AvatarPanelGroupMemberKick)
                            self.groupButton['image'] = self.kickOutImageList
                            self.groupButton['command'] = self.handleKick
                            self.groupButton['state'] = DGG.NORMAL
                        else:
                            self.groupButton['text'] = ('', AvatarPanelGroupMember, AvatarPanelGroupMember)
                            self.groupButton['command'] = None
                            self.groupButton['image'] = self.inviteImageDisabled
                            self.groupButton['image_color'] = Vec4(1, 1, 1, 0.4)
                            self.groupButton['state'] = DGG.NORMAL
                    else:
                        self.groupButton['text'] = ('', AvatarPanelGroupInvite, AvatarPanelGroupInvite)
                        self.groupButton['command'] = self.handleInvite
                        self.groupButton['image'] = self.inviteImageList
                        self.groupButton['state'] = DGG.NORMAL
                    if base.config.GetBool('want-boarding-groups', 1):
                        base.setCellsAvailable([base.rightCells[0]], 0)
                        self.groupFrame.show()
        return

    def handleReadInfo(self, task = None):
        self.boardingInfoButton['state'] = DGG.DISABLED
        if self.boardingInfoText:
            self.boardingInfoText.destroy()
        self.boardingInfoText = TTDialog.TTDialog(style=TTDialog.Acknowledge, text=BoardingPartyInform % localAvatar.boardingParty.maxSize, command=self.handleCloseInfo)

    def handleCloseInfo(self, *extraArgs):
        self.boardingInfoButton['state'] = DGG.NORMAL
        if self.boardingInfoText:
            self.boardingInfoText.destroy()
            del self.boardingInfoText
        self.boardingInfoText = None
        return

    def __makePetGui(self, avatar):
        petGui = loader.loadModel('phase_3.5/models/gui/PetControlPannel')
        self.petButton = DirectButton(parent=self.frame, image=(petGui.find('**/PetControlToonButtonUp1'), petGui.find('**/PetControlToonButtonDown1'), petGui.find('**/PetControlToonButtonRollover1')), geom=petGui.find('**/PetBattleIcon'), geom3_color=self.disabledImageColor, relief=None, pos=(0.22, -0.2, -0.475), text=('',
         AvatarPanelPet,
         AvatarPanelPet,
         ''), text_fg=self.text2Color, text_shadow=(0, 0, 0, 1), text_scale=0.325, text_pos=(-1.3, 0.05), text_align=TextNode.ACenter, command=self.__handleToPet)
        self.petButton.setScale(0.15)
        if base.wantPets:
            self.petButton['state'] = avatar.hasPet() or DGG.DISABLED
            self.petButton.hide()
        petGui.removeNode()
        return

    def __makeBoardingGui(self):
        self.confirmKickOutDialog = None
        groupAvatarBgGui = loader.loadModel('phase_3.5/models/gui/tt_m_gui_brd_avatarPanelBg')
        boardingGroupBGImage = groupAvatarBgGui.find('**/tt_t_gui_brd_avatar_panel_party')
        self.groupFrame = DirectFrame(parent=self.frame, relief=None, image=boardingGroupBGImage, image_scale=(0.5, 1, 0.5), textMayChange=1, text=BoardingPartyTitle, text_wordwrap=16, text_scale=TAPgroupFrame, text_pos=(0.01, 0.08), pos=(0, 0, -0.61))
        groupInviteGui = loader.loadModel('phase_3.5/models/gui/tt_m_gui_brd_inviteButton')
        self.inviteImageList = (groupInviteGui.find('**/tt_t_gui_brd_inviteUp'),
         groupInviteGui.find('**/tt_t_gui_brd_inviteDown'),
         groupInviteGui.find('**/tt_t_gui_brd_inviteHover'),
         groupInviteGui.find('**/tt_t_gui_brd_inviteUp'))
        self.kickOutImageList = (groupInviteGui.find('**/tt_t_gui_brd_kickoutUp'),
         groupInviteGui.find('**/tt_t_gui_brd_kickoutDown'),
         groupInviteGui.find('**/tt_t_gui_brd_kickoutHover'),
         groupInviteGui.find('**/tt_t_gui_brd_kickoutUp'))
        self.inviteImageDisabled = groupInviteGui.find('**/tt_t_gui_brd_inviteDisabled')
        self.groupButton = DirectButton(parent=self.groupFrame, image=self.inviteImageList, image3_color=self.disabledImageColor, image_scale=0.85, relief=None, text=('', AvatarPanelGroupInvite, AvatarPanelGroupInvite), text0_fg=self.text0Color, text1_fg=self.text1Color, text2_fg=self.text2Color, text3_fg=self.text3Color, text_scale=TAPgroupButton, text_pos=(-0.0, -0.1), text_align=TextNode.ACenter, command=self.handleInvite, pos=(0.01013, 0, -0.05464))
        helpGui = loader.loadModel('phase_3.5/models/gui/tt_m_gui_brd_help')
        helpImageList = (helpGui.find('**/tt_t_gui_brd_helpUp'),
         helpGui.find('**/tt_t_gui_brd_helpDown'),
         helpGui.find('**/tt_t_gui_brd_helpHover'),
         helpGui.find('**/tt_t_gui_brd_helpDown'))
        self.boardingInfoButton = DirectButton(parent=self.groupFrame, relief=None, text_pos=(-0.05, 0.05), text_scale=0.06, text_align=TextNode.ALeft, text_fg=Vec4(1, 1, 1, 1), text_shadow=Vec4(0, 0, 0, 1), image=helpImageList, image_scale=(0.5, 1, 0.5), image3_color=self.disabledImageColor, scale=1.05, command=self.handleReadInfo, pos=(0.1829, 0, 0.02405))
        self.boardingInfoText = None
        groupInviteGui.removeNode()
        groupAvatarBgGui.removeNode()
        helpGui.removeNode()
        return