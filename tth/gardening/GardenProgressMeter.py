import math
from tth.gardening.GardenDropGame import GardenDropGame

class GardenProgressMeter:
 
    def __init__(self, typePromotion = 'game', level = 0):
        self.typePromotion = None
        if typePromotion == 'shovel':
            self.typePromotion = "SHOVEL"
        elif typePromotion == 'wateringCan':
            self.typePromotion = "WATERINGCAN"
        elif typePromotion == 'game':
            self.typePromotion == "GAMEWIN"
        else:
            print 'No type of %s' % typePromotion
 
        self.acceptErrorDialog = None
        self.doneEvent = 'Game Done'
        self.sprites = []
 
    def load(self):
        model = loader.loadModel('phase_5.5/models/gui/package_delivery_panel.bam')
        model1 = loader.loadModel('phase_3.5/models/gui/matching_game_gui.bam')
 
        self.model = model
        self.model1 = model1
 
        background = model.find('**/bg')
        itemBoard = model.find('**/item_board')
 
        frameGui = loader.loadModel('phase_3/models/gui/dialog_box_gui.bam')
        self.frame = DirectFrame(scale=1.1, relief=None, image=frameGui, image_scale=(1.75, 1, 0.75), image_color=(1,1,1,1), frameSize=(-0.5,
         0.5,
         -0.45,
         -0.05))
 
        frameGui2 = loader.loadModel('phase_3.5/models/gui/jar_gui.bam')
        self.jar = DirectFrame(parent=self.frame, scale=(0.65,1.4,1.3), relief=None, image=frameGui2, image_scale=(1.75, 1, 0.75), image_color=(1,1,1,1), pos=(-0.5,-0.15,-0.075), frameSize=(-0.5,
         0.45,
         -0.45,
         -0.05))
 
        gui2 = loader.loadModel('phase_3/models/gui/quit_button.bam')
        self.font = loader.loadFont("phase_3/models/fonts/MickeyFont.bam")
 
        congratsMessage = 'Super Congratulations!!'
        if GardenDropGame.levelNumber == 5:
            congratsMessage2 = "You have won the Garden Drop Game!"
        else:
            congratsMessage2 = "Click 'Next' to go to the next level!"
            self.nextButton = DirectButton(parent=self.frame, relief=None, image=(gui2.find('**/QuitBtn_UP'), gui2.find('**/QuitBtn_DN'), gui2.find('**/QuitBtn_RLVR')), pos=(0, 1.0, -0.32), scale=0.9, text='Next', text_font=self.font, text0_fg=(1, 1, 1, 1), text1_fg=(1, 1, 1, 1), text2_fg=(1, 1, 1, 1), text_scale=0.045, text_pos=(0, -0.01), command=GardenDropGame._GardenDropGame__handlePlay)
 
        self.congratsText = DirectLabel(scale=1.1, relief=None, text_pos=(0, 0.2), text_wordwrap=16, text=congratsMessage, text_font=self.font, pos=(0.0, 0.0, 0.0), text_scale=0.1, text0_fg=(1, 1, 1, 1), parent=self.frame)
 
        self.font2 = loader.loadFont("phase_3/models/fonts/Comedy.bam")
        self.congratsText2 = DirectLabel(scale=1.1, relief=None, text_pos=(0.2, 0.025), text_wordwrap=10, text=congratsMessage2, text_font=self.font2, pos=(0.0, 0.0, 0.0), text_scale=0.085, text0_fg=(0, 0, 0, 1), parent=self.frame)
 
        self.quitButton = DirectButton(parent=self.frame, relief=None, image=(gui2.find('**/QuitBtn_UP'), gui2.find('**/QuitBtn_DN'), gui2.find('**/QuitBtn_RLVR')), pos=(0.5, 1.0, -0.32), scale=0.9, text='Exit', text_font=self.font, text0_fg=(1, 1, 1, 1), text1_fg=(1, 1, 1, 1), text2_fg=(1, 1, 1, 1), text_scale=0.045, text_pos=(0, -0.01), command=self.__handleExit)
 
        return True
 
    def unload(self):
        self.frame.destroy()
        del self.frame
 
        if self.acceptErrorDialog:
            self.acceptErrorDialog.cleanup()
            self.acceptErrorDialog = None
 
        GardenDropGame.playGardenDrop()
        base.taskMgr.remove('gameTask')
 
        return True
 
    def __handleExit(self):
        self._GardenProgressMeter__acceptExit()
        GardenDropGame.levelNumber = 1
 
    def __acceptExit(self, buttonValue = None):
        if hasattr(self, 'frame'):
            self.unload()
            messenger.send(self.doneEvent)