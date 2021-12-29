

from pandac.PandaModules import *
from direct.gui.DirectGui import *
from direct.fsm import StateData
from tth.avatar import ToonAvatarPanel

FLPPets = 1
FLPOnline = 2
FLPAll = 3
FLPOnlinePlayers = 4
FLPPlayers = 5
FLPEnemies = 6

FriendsListPanelNewFriend,FriendsListPanelSecrets,\
    FriendsListPanelOnlineFriends,FriendsListPanelAllFriends,\
    FriendsListPanelIgnoredFriends,FriendsListPanelPets,\
    FriendsListPanelPlayers,\
    FriendsListPanelOnlinePlayers = map(
                                        lambda x:L10N(x).replace('\\n','\n'),
                                        ("FLPNewFriend","FLPSecrets",\
                                         "FLPOnlineFriends","FLPAllFriends",\
                                         "FLPIgnoredFriends","FLPPets",\
                                         "FLPPlayers","FLPOnlinePlayers"
                                        )
                                        )

FLPnewFriend = 0.045
FLPsecrets = 0.045
FLPsecretsPos = (0.152, 0.0, 0.14)
FLPtitle = 0.04

class FriendsListPanel(DirectFrame, StateData.StateData):
    def __init__(self,parent):
        self.leftmostPanel = FLPOnline #Pets
        self.rightmostPanel = FLPAll
        
        DirectFrame.__init__(self, relief=None, parent = parent)
        self.listScrollIndex = [0]*15
        self.initialiseoptions(FriendsListPanel)
        StateData.StateData.__init__(self, 'friends-list-done')
        self.friends = {}
        self.textRolloverColor = Vec4(1, 1, 0, 1)
        self.textDownColor = Vec4(0.5, 0.9, 1, 1)
        self.textDisabledColor = Vec4(0.4, 0.8, 0.4, 1)
        self.panelType = FLPOnline

        self.isLoaded=1
        gui = loader.loadModel('phase_3.5/models/gui/friendslist_gui')
        auxGui = loader.loadModel('phase_3.5/models/gui/avatar_panel_gui')
        self.title = DirectLabel(parent=self, relief=None, text='', text_scale=FLPtitle, text_fg=(0, 0.1, 0.4, 1), pos=(0.007, 0.0, 0.2))
        background_image = gui.find('**/FriendsBox_Open')
        self['image'] = background_image
        self.setPos(1.1, 0, 0.54) #1.1, 0, 0.54
        self.scrollList = DirectScrolledList(parent=self, relief=None, incButton_image=(gui.find('**/FndsLst_ScrollUp'),
         gui.find('**/FndsLst_ScrollDN'),
         gui.find('**/FndsLst_ScrollUp_Rllvr'),
         gui.find('**/FndsLst_ScrollUp')), incButton_relief=None, incButton_pos=(0.0, 0.0, -0.316), incButton_image3_color=Vec4(0.6, 0.6, 0.6, 0.6), incButton_scale=(1.0, 1.0, -1.0), decButton_image=(gui.find('**/FndsLst_ScrollUp'),
         gui.find('**/FndsLst_ScrollDN'),
         gui.find('**/FndsLst_ScrollUp_Rllvr'),
         gui.find('**/FndsLst_ScrollUp')), decButton_relief=None, decButton_pos=(0.0, 0.0, 0.117), decButton_image3_color=Vec4(0.6, 0.6, 0.6, 0.6), itemFrame_pos=(-0.17, 0.0, 0.06), itemFrame_relief=None, numItemsVisible=8, items=[])
        clipper = PlaneNode('clipper')
        clipper.setPlane(Plane(Vec3(-1, 0, 0), Point3(0.2, 0, 0)))
        clipNP = self.scrollList.attachNewNode(clipper)
        self.scrollList.setClipPlane(clipNP)
        self.close = DirectButton(parent=self, relief=None, image=(auxGui.find('**/CloseBtn_UP'), auxGui.find('**/CloseBtn_DN'), auxGui.find('**/CloseBtn_Rllvr')), pos=(0.01, 0, -0.38), command=self.__close)
        self.left = DirectButton(parent=self, relief=None, image=(gui.find('**/Horiz_Arrow_UP'),
         gui.find('**/Horiz_Arrow_DN'),
         gui.find('**/Horiz_Arrow_Rllvr'),
         gui.find('**/Horiz_Arrow_UP')), image3_color=Vec4(0.6, 0.6, 0.6, 0.6), pos=(-0.15, 0.0, -0.38), scale=(-1.0, 1.0, 1.0), command=self.__left)
        self.right = DirectButton(parent=self, relief=None, image=(gui.find('**/Horiz_Arrow_UP'),
         gui.find('**/Horiz_Arrow_DN'),
         gui.find('**/Horiz_Arrow_Rllvr'),
         gui.find('**/Horiz_Arrow_UP')), image3_color=Vec4(0.6, 0.6, 0.6, 0.6), pos=(0.17, 0, -0.38), command=self.__right)
        self.newFriend = DirectButton(parent=self, relief=None, pos=(-0.14, 0.0, 0.14), image=(auxGui.find('**/Frnds_Btn_UP'), auxGui.find('**/Frnds_Btn_DN'), auxGui.find('**/Frnds_Btn_RLVR')), text=('', FriendsListPanelNewFriend, FriendsListPanelNewFriend), text_scale=FLPnewFriend, text_fg=(0, 0, 0, 1), text_bg=(1, 1, 1, 1), text_pos=(0.1, -0.085), textMayChange=0, command=self.__newFriend)
        self.secrets = DirectButton(parent=self, relief=None, pos=FLPsecretsPos, image=(auxGui.find('**/ChtBx_ChtBtn_UP'), auxGui.find('**/ChtBx_ChtBtn_DN'), auxGui.find('**/ChtBx_ChtBtn_RLVR')), text=('',
         FriendsListPanelSecrets,
         FriendsListPanelSecrets,
         ''), text_scale=FLPsecrets, text_fg=(0, 0, 0, 1), text_bg=(1, 1, 1, 1), text_pos=(-0.04, -0.085), textMayChange=0, command=self.__secrets)
        gui.removeNode()
        auxGui.removeNode()
        return

    def unload(self):
        if self.isLoaded == 0:
            return None
        self.isLoaded = 0
        self.exit()
        del self.title
        del self.scrollList
        del self.close
        del self.left
        del self.right
        del self.friends
        DirectFrame.destroy(self)
        return None

    def makeFriendButton(self, friendTuple, colorChoice = None, bold = 0):
        toonId, friendName = friendTuple
        thing = toonId
        fg = (0.8,0.5,0.1,1)
        if colorChoice: fg = colorChoice
        fontChoice = loader.loadFont('phase_3/models/fonts/ImpressBT.ttf')
        fontScale = 0.04
        bg = None
        if colorChoice and bold:
            fontScale = 0.04
            colorS = 0.7
            bg = (colorChoice[0] * colorS, colorChoice[1] * colorS, colorChoice[2] * colorS, colorChoice[3])
        command = self.__choseFriend
        db = DirectButton(relief=None, text=friendName, text_scale=fontScale,
                          text_align=TextNode.ALeft, text_fg=fg, text_shadow=bg,
                          text1_bg=self.textDownColor, text2_bg=self.textRolloverColor,
                          text3_fg=self.textDisabledColor, text_font=fontChoice,
                          textMayChange=0, command=command, extraArgs=[thing])
        return db

    def load(self):pass
        
    def enter(self):
        if self.isLoaded == 0:
            self.load()
        self.__updateScrollList()
        self.__updateTitle()
        self.__updateArrows()
        gamebase.curArea.hud[4].obscure(1)
        self.show()
        
        self.accept('friendOnline', self.__friendOnline)
        self.accept('friendPlayers', self.__friendPlayers)
        self.accept('friendOffline', self.__friendOffline)
        self.accept('friendsListChanged', self.__friendsListChanged)

    def exit(self,code=-1):
        self.isEntered = 0
        if code != 1: gamebase.curArea.hud[4].obscure(0)
        
        self.listScrollIndex[self.panelType] = self.scrollList.index
        self.hide()
 
        self.ignore('friendOnline')
        self.ignore('friendOffline')
        self.ignore('friendsListChanged')

    def __close(self):
        messenger.send('wakeup')
        self.exit()

    def __left(self):
        messenger.send('wakeup')
        self.listScrollIndex[self.panelType] = self.scrollList.index
        if self.panelType > self.leftmostPanel:
            self.panelType -= 1
        self.__updateScrollList()
        self.__updateTitle()
        self.__updateArrows()

    def __right(self):
        messenger.send('wakeup')
        self.listScrollIndex[self.panelType] = self.scrollList.index
        if self.panelType < self.rightmostPanel:
            self.panelType += 1
        self.__updateScrollList()
        self.__updateTitle()
        self.__updateArrows()

    def __secrets(self):
        messenger.send('wakeup')
        #ToontownFriendSecret.showFriendSecret(ToontownFriendSecret.AvatarSecret)

    def __newFriend(self):
        messenger.send('wakeup')
        messenger.send('friendAvatar', [None, None, None])
        return

    def __choseFriend(self, friendId):
        self.exit(1)
        self.avpanel = ToonAvatarPanel.ToonAvatarPanel(int(friendId),0,base.frdMgr.getDna(friendId))

    def __updateScrollList(self):
        newFriends = []
        petFriends = []
        toons = []
        
        if self.panelType == FLPAll: toons = base.frdMgr.friends           
        elif self.panelType == FLPOnline: toons = filter(lambda x:base.frdMgr.isOnline(x[0]),base.frdMgr.friends)
        elif self.panelType == FLPPets: toons = []
        elif self.panelType == FLPEnemies: toons = []

        for friendPair in self.friends.keys():
            friendButton = self.friends[friendPair]
            self.scrollList.removeItem(friendButton, refresh=0)
            friendButton.destroy()
            del self.friends[friendPair]

        for friendPair in toons:
            friendButton = self.makeFriendButton(friendPair,(0.8,0.5,0.1,1), 0)
            if friendButton:
                self.scrollList.addItem(friendButton, refresh=0)
                self.friends[friendPair] = friendButton

        self.scrollList.index = self.listScrollIndex[self.panelType]
        self.scrollList.refresh()

    def __updateTitle(self):
        if self.panelType == FLPOnline:
            self.title['text'] = FriendsListPanelOnlineFriends
        elif self.panelType == FLPAll:
            self.title['text'] = FriendsListPanelAllFriends
        elif self.panelType == FLPPets:
            self.title['text'] = FriendsListPanelPets
        elif self.panelType == FLPPlayers:
            self.title['text'] = FriendsListPanelPlayers
        elif self.panelType == FLPOnlinePlayers:
            self.title['text'] = FriendsListPanelOnlinePlayers
        else:
            self.title['text'] = FriendsListPanelIgnoredFriends
        self.title.resetFrameSize()

    def __updateArrows(self):
        if self.panelType == self.leftmostPanel:
            self.left['state'] = 'inactive'
        else:
            self.left['state'] = 'normal'
        if self.panelType == self.rightmostPanel:
            self.right['state'] = 'inactive'
        else:
            self.right['state'] = 'normal'

    def __friendOnline(self, doId, commonChatFlags, whitelistChatFlags):
        if self.panelType == FLPOnline:
            self.__updateScrollList()

    def __friendOffline(self, doId):
        if self.panelType == FLPOnline:
            self.__updateScrollList()

    def __friendPlayers(self, doId):
        if self.panelType == FLPPlayers:
            self.__updateScrollList()

    def __friendsListChanged(self, arg1 = None, arg2 = None):
        if self.panelType != FLPEnemies:
            self.__updateScrollList()

    def __ignoreListChanged(self):
        if self.panelType == FLPEnemies:
            self.__updateScrollList()