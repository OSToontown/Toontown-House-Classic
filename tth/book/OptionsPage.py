#this is the original one, gotta adapt yet!
from BookPage import *
from direct.directnotify import DirectNotifyGlobal
from direct.interval.IntervalGlobal import *
from panda3d.core import *
import fileinput
import os

PageMode_Options = 1
PageMode_Codes = 2
PageMode_Gfx = 3

OptionsPageTitle,OptionsTabTitle,OptionsPagePurchase,OptionsPageLogout,OptionsPageExitToontown,\
	OptionsPageMusicOnLabel,OptionsPageMusicOffLabel,OptionsPageSFXOnLabel,OptionsPageSFXOffLabel,\
	OptionsPageToonChatSoundsOnLabel,OptionsPageToonChatSoundsOffLabel,OptionsPageFriendsEnabledLabel,\
	OptionsPageFriendsDisabledLabel,OptionsPageWhisperEnabledLabel,OptionsPageWhisperDisabledLabel,\
	OptionsPageSpeedChatStyleLabel,OptionsPageDisplayWindowed,OptionsPageDisplayEmbedded,OptionsPageSelect,\
	OptionsPageToggleOn,OptionsPageToggleOff,OptionsPageChange,OptionsPageDisplaySettings,OptionsPageDisplaySettingsNoApi,\
	OptionsPageExitConfirm,OptionsPageCodesTab,CdrPageTitle,CdrInstructions,CdrResultSuccess,CdrResultInvalidCode,\
	CdrResultExpiredCode,CdrResultUnknownError,CdrResultMailboxFull,CdrResultAlreadyInMailbox,CdrResultAlreadyInQueue,\
	CdrResultAlreadyInCloset,CdrResultAlreadyBeingWorn,CdrResultAlreadyReceived,CdrResultTooManyFails,CdrResultServiceUnavailable,\
	NameShopSubmitButton = map(L10N,("BOOK_OPT_OptionsPageTitle",
					  				"BOOK_OPT_OptionsTabTitle",
									"BOOK_OPT_OptionsPagePurchase",
									"BOOK_OPT_OptionsPageLogout",
									"BOOK_OPT_OptionsPageExitToontown",
									"BOOK_OPT_OptionsPageMusicOnLabel",
									"BOOK_OPT_OptionsPageMusicOffLabel",
									"BOOK_OPT_OptionsPageSFXOnLabel",
									"BOOK_OPT_OptionsPageSFXOffLabel",
									"BOOK_OPT_OptionsPageToonChatSoundsOnLabel",
									"BOOK_OPT_OptionsPageToonChatSoundsOffLabel",
									"BOOK_OPT_OptionsPageFriendsEnabledLabel",
									"BOOK_OPT_OptionsPageFriendsDisabledLabel",
									"BOOK_OPT_OptionsPageWhisperEnabledLabel",
									"BOOK_OPT_OptionsPageWhisperDisabledLabel",
									"BOOK_OPT_OptionsPageSpeedChatStyleLabel",
									"BOOK_OPT_OptionsPageDisplayWindowed",
									"BOOK_OPT_OptionsPageDisplayEmbedded",
									"BOOK_OPT_OptionsPageSelect",
									"BOOK_OPT_OptionsPageToggleOn",
									"BOOK_OPT_OptionsPageToggleOff",
									"BOOK_OPT_OptionsPageChange",
									"BOOK_OPT_OptionsPageDisplaySettings",
									"BOOK_OPT_OptionsPageDisplaySettingsNoApi",
									"BOOK_OPT_OptionsPageExitConfirm",
									"BOOK_OPT_OptionsPageCodesTab",
									"BOOK_OPT_CdrPageTitle",
									"BOOK_OPT_CdrInstructions",
									"BOOK_OPT_CdrResultSuccess",
									"BOOK_OPT_CdrResultInvalidCode",
									"BOOK_OPT_CdrResultExpiredCode",
									"BOOK_OPT_CdrResultUnknownError",
									"BOOK_OPT_CdrResultMailboxFull",
									"BOOK_OPT_CdrResultAlreadyInMailbox",
									"BOOK_OPT_CdrResultAlreadyInQueue",
									"BOOK_OPT_CdrResultAlreadyInCloset",
									"BOOK_OPT_CdrResultAlreadyBeingWorn",
									"BOOK_OPT_CdrResultAlreadyReceived",
									"BOOK_OPT_CdrResultTooManyFails",
									"BOOK_OPT_CdrResultServiceUnavailable",
									"BOOK_OPT_NameShopSubmitButton"))

OptionsTabTitle.format("\n")

OPoptionsTab = 0.07
OPCodesInstructionPanelTextPos = (0, -0.01)
OPCodesInstructionPanelTextWordWrap = 6
OPCodesResultPanelTextPos = (0, 0.35)
OPCodesResultPanelTextScale = 0.06
OPCodesResultPanelTextWordWrap = 9
OPCodesInputTextScale = 0.8
OPCodesSubmitTextScale = 0.07
OPCodesSubmitTextPos = (0, -0.02)

class OptionsPage(BookPage):
	notify = DirectNotifyGlobal.directNotify.newCategory('OptionsPage')
	def setup(self):
		self.optionsTabPage = OptionsTabPage(self.frame)
		self.optionsTabPage.hide()
		self.codesTabPage = CodesTabPage(self.frame)
		self.codesTabPage.hide()
		self.gfxTabPage = GfxTabPage(self.frame)
		self.gfxTabPage.hide()
		titleHeight = 0.61
		self.title = DirectLabel(parent=self.frame, relief=None, text=OptionsPageTitle, text_scale=0.12, pos=(0, 0, titleHeight))
		normalColor = (1, 1, 1, 1)
		clickColor = (0.8, 0.8, 0, 1)
		rolloverColor = (0.15, 0.82, 1.0, 1)
		diabledColor = (1.0, 0.98, 0.15, 1)
		gui = loader.loadModel('phase_3.5/models/gui/fishingBook.bam')
		self.optionsTab = DirectButton(parent=self.frame, relief=None, text=OptionsPageTitle, text_scale=OPoptionsTab, text_align=TextNode.ALeft, text_pos=(0.01, 0.0, 0.0), image=gui.find('**/tabs/polySurface1'), image_pos=(0.55, 1, -0.91), image_hpr=(0, 0, -90), image_scale=(0.033, 0.033, 0.035), image_color=normalColor, image1_color=clickColor, image2_color=rolloverColor, image3_color=diabledColor, text_fg=Vec4(0.2, 0.1, 0, 1), command=self.setMode, extraArgs=[PageMode_Options], pos=(-0.12, 0, 0.77))
		self.codesTab = DirectButton(parent=self.frame, relief=None, text=OptionsPageCodesTab, text_scale=OPoptionsTab, text_align=TextNode.ALeft, text_pos=(-0.035, 0.0, 0.0), image=gui.find('**/tabs/polySurface2'), image_pos=(0.12, 1, -0.91), image_hpr=(0, 0, -90), image_scale=(0.033, 0.033, 0.035), image_color=normalColor, image1_color=clickColor, image2_color=rolloverColor, image3_color=diabledColor, text_fg=Vec4(0.2, 0.1, 0, 1), command=self.setMode, extraArgs=[PageMode_Codes], pos=(0.31, 0, 0.77))
		self.gfxTab = DirectButton(parent=self.frame, relief=None, text="Graphics", text_scale=OPoptionsTab, text_align=TextNode.ALeft, text_pos=(-1.63, 0.0, 0.0), image=gui.find('**/tabs/polySurface2'), image_pos=(-1.5, 1, -0.91), image_hpr=(0, 0, -90), image_scale=(0.033, 0.033, 0.035), image_color=normalColor, image1_color=clickColor, image2_color=rolloverColor, image3_color=diabledColor, text_fg=Vec4(0.2, 0.1, 0, 1), command=self.setMode, extraArgs=[PageMode_Gfx], pos=(1.08, 0, 0.77))
		self.setMode(PageMode_Options)
		#self.optionsTab.place()
		#self.codesTab.place()
		#self.gfxTab.place()

	def setMode(self, mode):
		if mode == PageMode_Options:
			self.mode = PageMode_Options
			self.title['text'] = OptionsPageTitle
			self.optionsTab['state'] = DGG.DISABLED
			self.optionsTab.setPos(-0.12, 0, 0.75)
			self.optionsTabPage.enter()
			self.codesTab['state'] = DGG.NORMAL
			self.codesTab.setPos(0.31, 0, 0.77)
			self.codesTabPage.exit()
			self.gfxTab['state'] = DGG.NORMAL
			self.gfxTab.setPos(1.08, 0, 0.77)
			self.gfxTabPage.exit()
		elif mode == PageMode_Codes:
			self.mode = PageMode_Codes
			self.title['text'] = CdrPageTitle
			self.optionsTab['state'] = DGG.NORMAL
			self.optionsTab.setPos(-0.12, 0, 0.77)
			self.optionsTabPage.exit()
			self.gfxTab['state'] = DGG.NORMAL
			self.gfxTab.setPos(1.08, 0, 0.77)
			self.gfxTabPage.exit()
			self.codesTab['state'] = DGG.DISABLED
			self.codesTab.setPos(0.31, 0, 0.75)
			self.codesTabPage.enter()
		elif mode == PageMode_Gfx:
			self.mode = PageMode_Gfx
			self.title['text'] = 'Graphic Options'
			self.optionsTab['state'] = DGG.NORMAL
			self.optionsTab.setPos(-0.12, 0, 0.77)
			self.optionsTabPage.exit()
			self.codesTab['state'] = DGG.NORMAL
			self.codesTab.setPos(0.31, 0, 0.77)
			self.codesTabPage.exit()
			self.gfxTab['state'] = DGG.DISABLED
			self.gfxTab.setPos(1.08, 0, 0.75)
			self.gfxTabPage.enter()
		else:
			raise StandardError, 'OptionsPage::setMode - Invalid Mode %s' % mode


class OptionsTabPage(DirectFrame):

	notify = DirectNotifyGlobal.directNotify.newCategory('OptionsTabPage')
	DisplaySettingsTaskName = 'save-display-settings'
	DisplaySettingsDelay = 60
	ChangeDisplaySettings = base.config.GetBool('change-display-settings', 1)
	ChangeDisplayAPI = base.config.GetBool('change-display-api', 0)

	def __init__(self, parent = aspect2d):
		self.parent = parent
		self.currentSizeIndex = None
		DirectFrame.__init__(self, parent=self.parent, relief=None, pos=(0.0, 0.0, 0.0), scale=(1.0, 1.0, 1.0))
		self.load()
		return

	def destroy(self):
		self.parent = None
		DirectFrame.destroy(self)
		return

	def load(self):
		self.displaySettings = None
		self.displaySettingsChanged = 0
		self.displaySettingsSize = (None, None)
		self.displaySettingsFullscreen = None
		self.displaySettingsEmbedded = None
		self.displaySettingsApi = None
		self.displaySettingsApiChanged = 0
		guiButton = loader.loadModel('phase_3/models/gui/quit_button.bam')
		gui = loader.loadModel('phase_3.5/models/gui/friendslist_gui.bam')
		titleHeight = 0.61
		textStartHeight = 0.45
		textRowHeight = 0.145
		leftMargin = -0.72
		buttonbase_xcoord = 0.35
		buttonbase_ycoord = 0.45
		button_image_scale = (0.7, 1, 1)
		button_textpos = (0, -0.02)
		options_text_scale = 0.052
		disabled_arrow_color = Vec4(0.6, 0.6, 0.6, 1.0)
		self.speed_chat_scale = 0.055
		self.Music_Label = DirectLabel(parent=self, relief=None, text='', text_align=TextNode.ALeft, text_scale=options_text_scale, pos=(leftMargin, 0, textStartHeight))
		self.SoundFX_Label = DirectLabel(parent=self, relief=None, text='', text_align=TextNode.ALeft, text_scale=options_text_scale, text_wordwrap=16, pos=(leftMargin, 0, textStartHeight - textRowHeight))
		#self.Friends_Label = DirectLabel(parent=self, relief=None, text='', text_align=TextNode.ALeft, text_scale=options_text_scale, text_wordwrap=16, pos=(leftMargin, 0, textStartHeight - 3 * textRowHeight))
		#self.Whispers_Label = DirectLabel(parent=self, relief=None, text='', text_align=TextNode.ALeft, text_scale=options_text_scale, text_wordwrap=16, pos=(leftMargin, 0, textStartHeight - 4 * textRowHeight))
		#self.DisplaySettings_Label = DirectLabel(parent=self, relief=None, text='', text_align=TextNode.ALeft, text_scale=options_text_scale, text_wordwrap=10, pos=(leftMargin, 0, textStartHeight - 5 * textRowHeight))
		#self.SpeedChatStyle_Label = DirectLabel(parent=self, relief=None, text=OptionsPageSpeedChatStyleLabel, text_align=TextNode.ALeft, text_scale=options_text_scale, text_wordwrap=10, pos=(leftMargin, 0, textStartHeight - 6 * textRowHeight))
		#self.ToonChatSounds_Label = DirectLabel(parent=self, relief=None, text='', text_align=TextNode.ALeft, text_scale=options_text_scale, text_wordwrap=15, pos=(leftMargin, 0, textStartHeight - 2 * textRowHeight + 0.025))
		#self.ToonChatSounds_Label.setScale(0.9)
		self.Music_toggleButton = DirectButton(parent=self, relief=None, image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR')), image_scale=button_image_scale, text='', text_scale=options_text_scale, text_pos=button_textpos, pos=(buttonbase_xcoord, 0.0, buttonbase_ycoord), command=self.__doToggleMusic)
		self.SoundFX_toggleButton = DirectButton(parent=self, relief=None, image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR')), image_scale=button_image_scale, text='', text_scale=options_text_scale, text_pos=button_textpos, pos=(buttonbase_xcoord, 0.0, buttonbase_ycoord - textRowHeight), command=self.__doToggleSfx)
		#self.Friends_toggleButton = DirectButton(parent=self, relief=None, image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR')), image_scale=button_image_scale, text='', text_scale=options_text_scale, text_pos=button_textpos, pos=(buttonbase_xcoord, 0.0, buttonbase_ycoord - textRowHeight * 3), command=self.__doToggleAcceptFriends)
		#self.Whispers_toggleButton = DirectButton(parent=self, relief=None, image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR')), image_scale=button_image_scale, text='', text_scale=options_text_scale, text_pos=button_textpos, pos=(buttonbase_xcoord, 0.0, buttonbase_ycoord - textRowHeight * 4), command=self.__doToggleAcceptWhispers)
		#self.DisplaySettingsButton = DirectButton(parent=self, relief=None, image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR')), image3_color=Vec4(0.5, 0.5, 0.5, 0.5), image_scale=button_image_scale, text=OptionsPageChange, text3_fg=(0.5, 0.5, 0.5, 0.75), text_scale=options_text_scale, text_pos=button_textpos, pos=(buttonbase_xcoord, 0.0, buttonbase_ycoord - textRowHeight * 5), command=self.__doDisplaySettings)
		self.ToonChatSounds_toggleButton = DirectButton(parent=self, relief=None, image=(guiButton.find('**/QuitBtn_UP'),
		 guiButton.find('**/QuitBtn_DN'),
		 guiButton.find('**/QuitBtn_RLVR'),
		 guiButton.find('**/QuitBtn_UP')), image3_color=Vec4(0.5, 0.5, 0.5, 0.5), image_scale=button_image_scale, text='', text3_fg=(0.5, 0.5, 0.5, 0.75), text_scale=options_text_scale, text_pos=button_textpos, pos=(buttonbase_xcoord, 0.0, buttonbase_ycoord - textRowHeight * 2 + 0.025), command=self.__doToggleToonChatSounds)
		self.ToonChatSounds_toggleButton.setScale(0.8)
		
		#####
		self.ToonChatSounds_toggleButton.hide()
		#####
		
		self.exitButton = DirectButton(parent=self, relief=None, image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR')), image_scale=1.15, text=OptionsPageExitToontown, text_scale=options_text_scale, text_pos=button_textpos, textMayChange=0, pos=(0.45, 0, -0.6), command=self.__handleExitShowWithConfirm)
		guiButton.removeNode()
		gui.removeNode()
		return

	def enter(self):
		self.show()
		taskMgr.remove(self.DisplaySettingsTaskName)
		self.settingsChanged = 0
		self.__setMusicButton()
		self.__setSoundFXButton()
		#self.__setAcceptFriendsButton()
		#self.__setAcceptWhispersButton()
		#self.__setDisplaySettings()
		#self.__setToonChatSoundsButton()
		
		#self.speedChatStyleText.enter()
		#self.speedChatStyleIndex = base.localAvatar.getSpeedChatStyleIndex()
		#self.updateSpeedChatStyle()
	# if self.parent.book.safeMode:
		#self.exitButton.hide()
	#else:
	#self.exitButton.show()

	def exit(self):
		self.ignore('confirmDone')
		self.hide()
		#self.speedChatStyleText.exit()

	def unload(self):
		#self.writeDisplaySettings()
		taskMgr.remove(self.DisplaySettingsTaskName)
		if self.displaySettings != None:
			self.ignore(self.displaySettings.doneEvent)
			self.displaySettings.unload()
		self.displaySettings = None
		self.exitButton.destroy()
		self.Music_toggleButton.destroy()
		self.SoundFX_toggleButton.destroy()
		self.Friends_toggleButton.destroy()
		self.Whispers_toggleButton.destroy()
		self.DisplaySettingsButton.destroy()
		#self.speedChatStyleLeftArrow.destroy()
		#self.speedChatStyleRightArrow.destroy()
		del self.exitButton
		del self.SoundFX_Label
		del self.Music_Label
		del self.Friends_Label
		del self.Whispers_Label
		del self.SpeedChatStyle_Label
		del self.SoundFX_toggleButton
		del self.Music_toggleButton
		del self.Friends_toggleButton
		del self.Whispers_toggleButton
		del self.speedChatStyleLeftArrow
		del self.speedChatStyleRightArrow
		#self.speedChatStyleText.exit()
		#self.speedChatStyleText.destroy()
		#del self.speedChatStyleText
		self.currentSizeIndex = None
		return

	def __doToggleMusic(self):
		messenger.send('wakeup')
		if base.musicActive:
			base.enableMusic(0)
			#Settings.setMusic(0)
		else:
			base.enableMusic(1)
			#Settings.setMusic(1)
		#self.settingsChanged = 1
		self.__setMusicButton()

	def __setMusicButton(self):
		if base.musicActive:
			self.Music_Label['text'] = OptionsPageMusicOnLabel
			self.Music_toggleButton['text'] = OptionsPageToggleOff
		else:
			self.Music_Label['text'] = OptionsPageMusicOffLabel
			self.Music_toggleButton['text'] = OptionsPageToggleOn

	def __doToggleSfx(self):
		messenger.send('wakeup')
		if base.sfxActive:
			base.enableSoundEffects(0)
		   # Settings.setSfx(0)
		else:
			base.enableSoundEffects(1)
			#Settings.setSfx(1)
			# self.settingsChanged = 1
		self.__setSoundFXButton()

	def __doToggleToonChatSounds(self):
		messenger.send('wakeup')
		if base.toonChatSounds:
			base.toonChatSounds = 0
			Settings.setToonChatSounds(0)
		else:
			base.toonChatSounds = 1
			Settings.setToonChatSounds(1)
		self.settingsChanged = 1
		self.__setToonChatSoundsButton()

	def __setSoundFXButton(self):
		if base.sfxActive:
			self.SoundFX_Label['text'] = OptionsPageSFXOnLabel
			self.SoundFX_toggleButton['text'] = OptionsPageToggleOff
		else:
			self.SoundFX_Label['text'] = OptionsPageSFXOffLabel
			self.SoundFX_toggleButton['text'] = OptionsPageToggleOn
		#self.__setToonChatSoundsButton()

	def __setToonChatSoundsButton(self):
		if True:
			self.ToonChatSounds_Label['text'] = OptionsPageToonChatSoundsOnLabel
			self.ToonChatSounds_toggleButton['text'] = OptionsPageToggleOff
		else:
			self.ToonChatSounds_Label['text'] = OptionsPageToonChatSoundsOffLabel
			self.ToonChatSounds_toggleButton['text'] = OptionsPageToggleOn
		if base.sfxActive:
			self.ToonChatSounds_Label.setColorScale(1.0, 1.0, 1.0, 1.0)
			self.ToonChatSounds_toggleButton['state'] = DGG.NORMAL
		else:
			self.ToonChatSounds_Label.setColorScale(0.5, 0.5, 0.5, 0.5)
			self.ToonChatSounds_toggleButton['state'] = DGG.DISABLED

	def __doToggleAcceptFriends(self):
		messenger.send('wakeup')
		if base.localAvatar.acceptingNewFriends:
			base.localAvatar.acceptingNewFriends = 0
			Settings.setAcceptingNewFriends(0)
		else:
			base.localAvatar.acceptingNewFriends = 1
			Settings.setAcceptingNewFriends(1)
		self.settingsChanged = 1
		self.__setAcceptFriendsButton()

	def __doToggleAcceptWhispers(self):
		messenger.send('wakeup')
		if base.localAvatar.acceptingNonFriendWhispers:
			base.localAvatar.acceptingNonFriendWhispers = 0
			Settings.setAcceptingNonFriendWhispers(0)
		else:
			base.localAvatar.acceptingNonFriendWhispers = 1
			Settings.setAcceptingNonFriendWhispers(1)
		self.settingsChanged = 1
		self.__setAcceptWhispersButton()

	def __setAcceptFriendsButton(self):
		if True:
			self.Friends_Label['text'] = OptionsPageFriendsEnabledLabel
			self.Friends_toggleButton['text'] = OptionsPageToggleOff
		else:
			self.Friends_Label['text'] = OptionsPageFriendsDisabledLabel
			self.Friends_toggleButton['text'] = OptionsPageToggleOn

	def __setAcceptWhispersButton(self):
		if True:
			self.Whispers_Label['text'] = OptionsPageWhisperEnabledLabel
			self.Whispers_toggleButton['text'] = OptionsPageToggleOff
		else:
			self.Whispers_Label['text'] = OptionsPageWhisperDisabledLabel
			self.Whispers_toggleButton['text'] = OptionsPageToggleOn

	def __doDisplaySettings(self):
		if self.displaySettings == None:
			self.displaySettings = DisplaySettingsDialog.DisplaySettingsDialog()
			self.displaySettings.load()
			self.accept(self.displaySettings.doneEvent, self.__doneDisplaySettings)
		self.displaySettings.enter(self.ChangeDisplaySettings, self.ChangeDisplayAPI)
		return

	def __doneDisplaySettings(self, anyChanged, apiChanged):
		if anyChanged:
			self.__setDisplaySettings()
			properties = base.win.getProperties()
			self.displaySettingsChanged = 1
			self.displaySettingsSize = (properties.getXSize(), properties.getYSize())
			self.displaySettingsFullscreen = properties.getFullscreen()
			self.displaySettingsEmbedded = self.isPropertiesEmbedded(properties)
			self.displaySettingsApi = base.pipe.getInterfaceName()
			self.displaySettingsApiChanged = apiChanged

	def isPropertiesEmbedded(self, properties):
		result = False
		if properties.getParentWindow():
			result = True
		return result

	def __setDisplaySettings(self):
		properties = base.win.getProperties()
		if properties.getFullscreen():
			screensize = '%s x %s' % (properties.getXSize(), properties.getYSize())
		else:
			screensize = OptionsPageDisplayWindowed
		isEmbedded = self.isPropertiesEmbedded(properties)
		if isEmbedded:
			screensize = OptionsPageDisplayEmbedded
		api = base.pipe.getInterfaceName()
		settings = {'screensize': screensize,
		 'api': api}
		if self.ChangeDisplayAPI:
			OptionsPage.notify.debug('change display settings...')
			text = OptionsPageDisplaySettings % settings
		else:
			OptionsPage.notify.debug('no change display settings...')
			text = OptionsPageDisplaySettingsNoApi % settings
		self.DisplaySettings_Label['text'] = text

	def writeDisplaySettings(self, task = None):
		if not self.displaySettingsChanged:
			return
		taskMgr.remove(self.DisplaySettingsTaskName)
		self.notify.info('writing new display settings %s, fullscreen %s, embedded %s, %s to SettingsFile.' % (self.displaySettingsSize,
		 self.displaySettingsFullscreen,
		 self.displaySettingsEmbedded,
		 self.displaySettingsApi))
		Settings.setResolutionDimensions(self.displaySettingsSize[0], self.displaySettingsSize[1])
		Settings.setWindowedMode(not self.displaySettingsFullscreen)
		Settings.setEmbeddedMode(self.displaySettingsEmbedded)
		if self.displaySettingsApiChanged:
			api = self.DisplaySettingsApiMap.get(self.displaySettingsApi)
			if api == None:
				self.notify.warning('Cannot save unknown display API: %s' % self.displaySettingsApi)
			else:
				Settings.setDisplayDriver(api)
		Settings.writeSettings()
		self.displaySettingsChanged = 0
		return Task.done

	def __handleExitShowWithConfirm(self):
		self.confirm = YesNoDialog(dialogName="YesNoCancelDialog",command = self.__handleConfirm,text=OptionsPageExitConfirm)

	def __handleConfirm(self,status):
		if not status:
			self.confirm.cleanup()
		else:
			sys.exit()

class CodesTabPage(DirectFrame):

	notify = DirectNotifyGlobal.directNotify.newCategory('CodesTabPage')
	
	def __init__(self, parent = aspect2d):
		self.parent = parent
		DirectFrame.__init__(self, parent=self.parent, relief=None, pos=(0.0, 0.0, 0.0), scale=(1.0, 1.0, 1.0))
		self.load()
		return

	def destroy(self):
		self.parent = None
		DirectFrame.destroy(self)
		return

	def load(self):
		cdrGui = loader.loadModel('phase_3.5/models/gui/tt_m_gui_sbk_codeRedemptionGui.bam')
		instructionGui = cdrGui.find('**/tt_t_gui_sbk_cdrPresent')
		flippyGui = cdrGui.find('**/tt_t_gui_sbk_cdrFlippy')
		codeBoxGui = cdrGui.find('**/tt_t_gui_sbk_cdrCodeBox')
		self.resultPanelSuccessGui = cdrGui.find('**/tt_t_gui_sbk_cdrResultPanel_success')
		self.resultPanelFailureGui = cdrGui.find('**/tt_t_gui_sbk_cdrResultPanel_failure')
		self.resultPanelErrorGui = cdrGui.find('**/tt_t_gui_sbk_cdrResultPanel_error')
		self.successSfx = base.loadSfx('phase_3.5/audio/sfx/tt_s_gui_sbk_cdrSuccess.mp3')
		self.failureSfx = base.loadSfx('phase_3.5/audio/sfx/tt_s_gui_sbk_cdrFailure.mp3')
		self.instructionPanel = DirectFrame(parent=self, relief=None, image=instructionGui, image_scale=0.8, text=CdrInstructions, text_pos=OPCodesInstructionPanelTextPos, text_align=TextNode.ACenter, text_scale=OPCodesResultPanelTextScale, text_wordwrap=OPCodesInstructionPanelTextWordWrap, pos=(-0.429, 0, -0.05))
		self.codeBox = DirectFrame(parent=self, relief=None, image=codeBoxGui, pos=(0.433, 0, 0.35))
		self.flippyFrame = DirectFrame(parent=self, relief=None, image=flippyGui, pos=(0.44, 0, -0.353))
		self.codeInput = DirectEntry(parent=self.codeBox, relief=DGG.GROOVE, scale=0.08, pos=(-0.33, 0, -0.006), borderWidth=(0.05, 0.05), frameColor=((1, 1, 1, 1), (1, 1, 1, 1), (0.5, 0.5, 0.5, 0.5)), state=DGG.NORMAL, text_align=TextNode.ALeft, text_scale=OPCodesInputTextScale, width=10.5, numLines=1, focus=1, backgroundFocus=0, cursorKeys=1, text_fg=(0, 0, 0, 1), suppressMouse=1, autoCapitalize=0, command=self.__submitCode)
		submitButtonGui = loader.loadModel('phase_3/models/gui/quit_button.bam')
		self.submitButton = DirectButton(parent=self, relief=None, image=(submitButtonGui.find('**/QuitBtn_UP'),
		 submitButtonGui.find('**/QuitBtn_DN'),
		 submitButtonGui.find('**/QuitBtn_RLVR'),
		 submitButtonGui.find('**/QuitBtn_UP')), image3_color=Vec4(0.5, 0.5, 0.5, 0.5), image_scale=1.15, state=DGG.NORMAL, text=NameShopSubmitButton, text_scale=OPCodesSubmitTextScale, text_align=TextNode.ACenter, text_pos=OPCodesSubmitTextPos, text3_fg=(0.5, 0.5, 0.5, 0.75), textMayChange=0, pos=(0.45, 0.0, 0.0896), command=self.__submitCode)
		self.resultPanel = DirectFrame(parent=self, relief=None, image=self.resultPanelSuccessGui, text='', text_pos=OPCodesResultPanelTextPos, text_align=TextNode.ACenter, text_scale=OPCodesResultPanelTextScale, text_wordwrap=OPCodesResultPanelTextWordWrap, pos=(-0.42, 0, -0.0567))
		self.resultPanel.hide()
		closeButtonGui = loader.loadModel('phase_3/models/gui/dialog_box_buttons_gui')
		self.closeButton = DirectButton(parent=self.resultPanel, pos=(0.296, 0, -0.466), relief=None, state=DGG.NORMAL, image=(closeButtonGui.find('**/CloseBtn_UP'), closeButtonGui.find('**/CloseBtn_DN'), closeButtonGui.find('**/CloseBtn_Rllvr')), image_scale=(1, 1, 1), command=self.__hideResultPanel)
		closeButtonGui.removeNode()
		cdrGui.removeNode()
		submitButtonGui.removeNode()
		return

	def enter(self):
		self.show()
		#localAvatar.chatMgr.fsm.request('otherDialog')
		self.codeInput['focus'] = 1
		self.codeInput.enterText('')
		self.__enableCodeEntry()

	def exit(self):
		self.resultPanel.hide()
		self.hide()
		#localAvatar.chatMgr.fsm.request('mainMenu')

	def unload(self):
		self.instructionPanel.destroy()
		self.instructionPanel = None
		self.codeBox.destroy()
		self.codeBox = None
		self.flippyFrame.destroy()
		self.flippyFrame = None
		self.codeInput.destroy()
		self.codeInput = None
		self.submitButton.destroy()
		self.submitButton = None
		self.resultPanel.destroy()
		self.resultPanel = None
		self.closeButton.destroy()
		self.closeButton = None
		del self.successSfx
		del self.failureSfx
		return

	def __submitCode(self, input = None):
		if input == None:
			input = self.codeInput.get()
		self.codeInput['focus'] = 1
		if input == '':
			return
		messenger.send('wakeup')
		if hasattr(base, 'codeRedemptionMgr'):
			base.codeRedemptionMgr.redeemCode(input, self.__getCodeResult)
		self.codeInput.enterText('')
		self.__disableCodeEntry()
		return

	def __getCodeResult(self, result, awardMgrResult):
		self.notify.debug('result = %s' % result)
		self.notify.debug('awardMgrResult = %s' % awardMgrResult)
		self.__enableCodeEntry()
		if result == 0:
			self.resultPanel['image'] = self.resultPanelSuccessGui
			self.resultPanel['text'] = CdrResultSuccess
		elif result == 1 or result == 3:
			self.resultPanel['image'] = self.resultPanelFailureGui
			self.resultPanel['text'] = CdrResultInvalidCode
		elif result == 2:
			self.resultPanel['image'] = self.resultPanelFailureGui
			self.resultPanel['text'] = CdrResultExpiredCode	
		elif result == 4:
			self.resultPanel['image'] = self.resultPanelErrorGui
			if awardMgrResult == 0:
				self.resultPanel['text'] = CdrResultSuccess
			elif awardMgrResult == 1 or awardMgrResult == 2 or awardMgrResult == 15 or awardMgrResult == 16:
				self.resultPanel['text'] = CdrResultUnknownError
			elif awardMgrResult == 3 or awardMgrResult == 4:
				self.resultPanel['text'] = CdrResultMailboxFull
			elif awardMgrResult == 5 or awardMgrResult == 10:
				self.resultPanel['text'] = CdrResultAlreadyInMailbox
			elif awardMgrResult == 6 or awardMgrResult == 7 or awardMgrResult == 11:
				self.resultPanel['text'] = CdrResultAlreadyInQueue
			elif awardMgrResult == 8:
				self.resultPanel['text'] = CdrResultAlreadyInCloset
			elif awardMgrResult == 9:
				self.resultPanel['text'] = CdrResultAlreadyBeingWorn
			elif awardMgrResult == 12 or awardMgrResult == 13 or awardMgrResult == 14:
				self.resultPanel['text'] = CdrResultAlreadyReceived
		elif result == 5:
			self.resultPanel['text'] = CdrResultTooManyFails
			self.__disableCodeEntry()
		elif result == 6:
			self.resultPanel['text'] = CdrResultServiceUnavailable
			self.__disableCodeEntry()
		if result == 0:
			self.successSfx.play()
		else:
			self.failureSfx.play()
		self.resultPanel.show()

	def __hideResultPanel(self):
		self.resultPanel.hide()

	def __disableCodeEntry(self):
		self.codeInput['state'] = DGG.DISABLED
		self.submitButton['state'] = DGG.DISABLED

	def __enableCodeEntry(self):
		self.codeInput['state'] = DGG.NORMAL
		self.codeInput['focus'] = 1
		self.submitButton['state'] = DGG.NORMAL

class GfxTabPage(DirectFrame):
	
	notify = DirectNotifyGlobal.directNotify.newCategory('GfxTabPage')
	
	def __init__(self, parent = aspect2d):
		self.parent = parent
		DirectFrame.__init__(self, parent=self.parent, relief=None, pos=(0.0, 0.0, 0.0), scale=(1.0, 1.0, 1.0))
		
		#Just some default values
		self.gfxConfig = [False, 0, False, [640, 480]]
		
		self.gfxConfig[0] = ConfigVariableBool('fullscreen').getValue()
		self.gfxConfig[1] = ConfigVariableInt('multisamples').getValue()
		self.gfxConfig[2] = ConfigVariableBool('head-tag').getValue()
		self.gfxConfig[3][0] = ConfigVariableInt('win-width').getValue()
		self.gfxConfig[3][1] = ConfigVariableInt('win-height').getValue()

		self.ResRaw = []
		self.screenBits = []
		info = base.pipe.getDisplayInformation()
		for idx in range(info.getTotalDisplayModes()):
			width = info.getDisplayModeWidth(idx)
			height = info.getDisplayModeHeight(idx)
			self.ResRaw.append([int(width), int(height)])
		self.ResList = []
		for x in self.ResRaw:
			if x not in self.ResList:
				self.ResList.append(x)
		self.ResNum = len(self.ResList)
		self.SO = 0
		self.load()
		return

	def destroy(self):
		self.parent = None
		DirectFrame.destroy(self)
		return

	def load(self):
		self.displaySettings = None
		self.displaySettingsChanged = 0
		self.displaySettingsSize = (None, None)
		self.displaySettingsFullscreen = None
		self.displaySettingsEmbedded = None
		self.displaySettingsApi = None
		self.displaySettingsApiChanged = 0
		guiButton = loader.loadModel('phase_3/models/gui/quit_button.bam')
		gui = loader.loadModel('phase_3.5/models/gui/friendslist_gui.bam')
		ScreenSizeBG = loader.loadModel('phase_3.5/models/gui/speedChatGui.bam')
		titleHeight = 0.61
		textStartHeight = 0.45
		textRowHeight = 0.145
		leftMargin = -0.72
		buttonbase_xcoord = 0.35
		buttonbase_ycoord = 0.45
		button_image_scale = (0.7, 1, 1)
		button_textpos = (0, -0.02)
		options_text_scale = 0.052
		disabled_arrow_color = Vec4(0.6, 0.6, 0.6, 1.0)
		self.speed_chat_scale = 0.055
		self.AA_Label = DirectLabel(parent=self, relief=None, text='', text_align=TextNode.ALeft, text_scale=options_text_scale, pos=(leftMargin, 0, textStartHeight))
		self.AA_toggleButton = DirectButton(parent=self, relief=None, image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR')), image_scale=button_image_scale, text='', text_scale=options_text_scale, text_pos=button_textpos, pos=(buttonbase_xcoord, 0.0, buttonbase_ycoord), command=self.__doToggleAA)
		self.FS_Label = DirectLabel(parent=self, relief=None, text='', text_align=TextNode.ALeft, text_scale=options_text_scale, text_wordwrap=16, pos=(leftMargin, 0, textStartHeight - textRowHeight))
		self.FS_toggleButton = DirectButton(parent=self, relief=None, image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR')), image_scale=button_image_scale, text='', text_scale=options_text_scale, text_pos=button_textpos, pos=(buttonbase_xcoord, 0.0, buttonbase_ycoord - textRowHeight), command=self.__doToggleFS)
		self.ToggleTag_Label = DirectLabel(parent=self, relief=None, text='', text_align=TextNode.ALeft, text_scale=options_text_scale, text_wordwrap=16, pos=(leftMargin, 0, textStartHeight - textRowHeight * 2))
		self.ToggleTag_toggleButton = DirectButton(parent=self, relief=None, image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR')), image_scale=button_image_scale, text='', text_scale=options_text_scale, text_pos=button_textpos, pos=(buttonbase_xcoord, 0.0, buttonbase_ycoord - textRowHeight * 2), command=self.__doToggleTag)
		self.ScreenSize_Label = DirectLabel(parent=self, relief=None, text="Screen resolution", text_align=TextNode.ALeft, text_scale=options_text_scale, pos=(leftMargin, 0, textStartHeight - 3 * textRowHeight))
		self.ScreenSizeLeftArrow = DirectButton(parent=self, relief=None, image=(gui.find('**/Horiz_Arrow_UP'),
		 gui.find('**/Horiz_Arrow_DN'),
		 gui.find('**/Horiz_Arrow_Rllvr'),
		 gui.find('**/Horiz_Arrow_UP')), image3_color=Vec4(1, 1, 1, 0.5), scale=(-1.0, 1.0, 1.0), pos=(0.25, 0, buttonbase_ycoord - textRowHeight * 3), command=self.__doScreenSizeLeft)
		self.ScreenSizeRightArrow = DirectButton(parent=self, relief=None, image=(gui.find('**/Horiz_Arrow_UP'),
		 gui.find('**/Horiz_Arrow_DN'),
		 gui.find('**/Horiz_Arrow_Rllvr'),
		 gui.find('**/Horiz_Arrow_UP')), image3_color=Vec4(1, 1, 1, 0.5), pos=(0.65, 0, buttonbase_ycoord - textRowHeight * 3), command=self.__doScreenSizeRight)
		self.ScreenSize_Text = DirectLabel(parent=self, relief=None, text='', text_scale=self.speed_chat_scale, pos=(0.45, 0, buttonbase_ycoord - textRowHeight * 3 - 0.018))
		self.applyButton = DirectButton(parent=self, relief=None, image=(guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR')), image_scale=1.15, text='Apply Changes', text_scale=options_text_scale, text_pos=button_textpos, textMayChange=0, pos=(0.45, 0, -0.6), command=self.__doApplyButton)
		return
	
	def enter(self):
		self.show()
		self.__setAAButton()
		self.__setFSButton()
		self.__setToggleTagButton()
		self.__setScreenSizeText()
		
	def exit(self):
		self.hide()
		
	def unload(self):
		return

	def __doToggleAA(self):
		messenger.send('wakeup')
		if self.gfxConfig[1] == 8:
			self.gfxConfig[1] = 0
			self.AA_toggleButton['text'] = "None"
		else:
			self.gfxConfig[1] = self.gfxConfig[1] + 1
			self.AA_toggleButton['text'] = str(self.gfxConfig[1]) + "x"
		
	def __setAAButton(self):
		self.AA_Label['text'] = "Current Anti-Aliasing setting:"
		self.AA_toggleButton['text'] = str(self.gfxConfig[1]) + "x"
		if self.gfxConfig[1] == 0:
			self.AA_toggleButton['text'] = "None"
		
	def __doToggleFS(self):
		messenger.send('wakeup')
		if self.gfxConfig[0]:
			self.gfxConfig[0] = False
		else:
			self.gfxConfig[0] = True
		self.__setFSButton()
	
	def __setFSButton(self):
		if self.gfxConfig[0]:
			self.FS_Label['text'] = "Fullscreen is on"
			self.FS_toggleButton['text'] = OptionsPageToggleOff
		else:
			self.FS_Label['text'] = "Fullscreen is off"
			self.FS_toggleButton['text'] = OptionsPageToggleOn
			
	def __doToggleTag(self):
		messenger.send('wakeup')
		if self.gfxConfig[2]:
			self.gfxConfig[2] = False
		else:
			self.gfxConfig[2] = True
		self.__setToggleTagButton()
	
	def __setToggleTagButton(self):
		if self.gfxConfig[2]:
			self.ToggleTag_Label['text'] = "Toon nametags will move"
			self.ToggleTag_toggleButton['text'] = "Toggle"
		else:
			self.ToggleTag_Label['text'] = "Toon nametags will appear still"
			self.ToggleTag_toggleButton['text'] = "Toggle"
			
	def __doScreenSizeRight(self):
		self.SO = self.SO + 1
		if self.SO >= self.ResNum:
			self.SO = 0
		self.gfxConfig[3] = self.ResList[self.SO]
		self.__setScreenSizeText()
		
	def __doScreenSizeLeft(self):
		self.SO = self.SO - 1
		if self.SO == 1:
			self.SO = self.ResNum
		self.gfxConfig[3] = self.ResList[self.SO]
		self.__setScreenSizeText()

	def __setScreenSizeText(self):
		self.ScreenSize_Text['text'] = str(self.gfxConfig[3][0])+" x "+str(self.gfxConfig[3][1])
		
	def __doApplyButton(self):
		if self.gfxConfig[0]:
			tempF = "#t"
		else:
			tempF = "#f"
		if self.gfxConfig[2]:
			tempF2 = "#t"
		else:
			tempF2 = "#f"
		newPrc = "notify-level warning\ndefault-directnotify-level info\nicon-filename toontown.ico\ndirect-gui-edit 1\ndefault-model-extension .bam\nload-display pandagl\naux-display pandadx9\naux-display pandadx8\naux-display tinydisplay\naudio-library-name p3fmod_audio\nfmod-use-surround-sound true\nwant-directtools #f\nwant-tk #f\nwindow-title Toontown House\nwin-width "+str(self.gfxConfig[3][0])+"\nwin-height "+str(self.gfxConfig[3][1])+"\nfullscreen "+tempF+"\nmultisamples "+str(self.gfxConfig[1])+"\nwin-orgin 0 0\nshow-frame-rate-meter #t\nhead-tag "+tempF2
		os.remove("etc/Config.prc")
		open('etc/Config.prc','w').write(newPrc)
		self.__handleApplyWithConfirm()
			
	def __handleApplyWithConfirm(self):
		self.confirm = YesNoDialog(dialogName="YesNoCancelDialog",command = self.__handleApply,text="Applying these changes requires that you restart the game.\nWould you like to restart right now?")

	def __handleApply(self,status):
		if not status:
			self.confirm.cleanup()
		else:
			sys.exit()
