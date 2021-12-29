from direct.task import Task
from direct.fsm import StateData
from direct.gui.DirectGui import *
from pandac.PandaModules import *
from tth.managers import ToontownTimer 
import MinigameGlobals 

MRPgameTitleText = 0.11
MRgameTitleTextPos = (-0.046, 0.2, 0.092)
MRPplayButton = 0.055
MRPinstructionsText = 0.07
MRPinstructionsTextWordwrap = 26.5
MRPinstructionsTextPos = (-0.115, 0.05, 0)
MinigameRulesPanelPlay = 'PLAY'

class MinigameRulesPanel(StateData.StateData):


    def __init__(self, panelName, gameTitle, instructions, doneEvent, timeout = MinigameGlobals.rulesDuration):
        StateData.StateData.__init__(self, doneEvent)
        self.gameTitle = gameTitle
        self.instructions = instructions
        self.TIMEOUT = timeout

    def load(self):
        minigameGui = loader.loadModel('phase_4/models/gui/minigame_rules_gui.bam')
        buttonGui = loader.loadModel('phase_3.5/models/gui/inventory_gui')
        self.frame = DirectFrame(image=minigameGui.find('**/minigame-rules-panel'), relief=None, pos=(0.1375, 0, -0.6667))
        self.gameTitleText = DirectLabel(parent=self.frame, text=self.gameTitle, scale=MRPgameTitleText, text_align=TextNode.ACenter, text_font="phase_3/fonts/ImpressBT.ttf", text_fg=(1.0, 0.33, 0.33, 1.0), pos=MRgameTitleTextPos, relief=None)
        self.instructionsText = DirectLabel(parent=self.frame, text=self.instructions, scale=MRPinstructionsText, text_align=TextNode.ACenter, text_wordwrap=MRPinstructionsTextWordwrap, pos=MRPinstructionsTextPos, relief=None)
        self.playButton = DirectButton(parent=self.frame, relief=None, image=(buttonGui.find('**/InventoryButtonUp'), buttonGui.find('**/InventoryButtonDown'), buttonGui.find('**/InventoryButtonRollover')), image_color=Vec4(0, 0.9, 0.1, 1), text=MinigameRulesPanelPlay, text_fg=(1, 1, 1, 1), text_pos=(0, -0.02, 0), text_scale=MRPplayButton, pos=(1.0025, 0, -0.203), scale=1.05, command=self.playCallback)
        minigameGui.removeNode()
        buttonGui.removeNode()
        self.timer = ToontownTimer.ToontownTimer()
        self.timer.reparentTo(self.frame)
        self.timer.setScale(0.4)
        self.timer.setPos(0.997, 0, 0.064)
        self.frame.hide()
        return

    def unload(self):
        self.frame.destroy()
        del self.frame
        del self.gameTitleText
        del self.instructionsText
        self.playButton.destroy()
        del self.playButton
        del self.timer

    def enter(self):
        self.frame.show()
        self.timer.countdown(self.TIMEOUT, self.playCallback)
        self.accept('enter', self.playCallback)

    def exit(self):
        self.frame.hide()
        self.timer.stop()
        self.ignore('enter')

    def playCallback(self):
        messenger.send(self.doneEvent)