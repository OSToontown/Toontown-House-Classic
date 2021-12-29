from direct.fsm import StateData
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import ClassicFSM, State

class Motion(StateData.StateData):

    notify = DirectNotifyGlobal.directNotify.newCategory('Motion')

    def __init__(self, toon):
        self.toon = toon
        self.doneEvent = 'motionDone'
        StateData.StateData.__init__(self, self.doneEvent)
        self.fsm = ClassicFSM.ClassicFSM('Motion', [
            State.State('off', self.enterOff, self.exitOff),
            State.State('neutral', self.enterNeutral, self.exitNeutral),
            State.State('walk', self.enterWalk, self.exitWalk),
            State.State('run', self.enterRun, self.exitRun),
            State.State('sad-neutral', self.enterSadNeutral,
                                       self.exitSadNeutral),
            State.State('sad-walk', self.enterSadWalk, self.exitSadWalk),
            State.State('catch-neutral', self.enterCatchNeutral,
                                         self.exitCatchNeutral),
            State.State('catch-run', self.enterCatchRun, self.exitCatchRun),
            State.State('catch-eatneutral', self.enterCatchEatNeutral,
                                            self.exitCatchEatNeutral),
            State.State('catch-eatnrun', self.enterCatchEatNRun,
                                         self.exitCatchEatNRun)
        ], 'off', 'off')
        self.fsm.enterInitialState()

    def delete(self):
        del self.fsm

    def enter(self):
        self.notify.debug('enter')

    def exit(self):
        self.fsm.requestFinalState()

    def enterOff(self, rate=0):
        self.notify.debug('enterOff')

    def exitOff(self):
        self.notify.debug('exitOff')

    def enterNeutral(self, rate=0):
        self.notify.debug('enterNeutral')

    def exitNeutral(self):
        self.notify.debug('exitNeutral')

    def enterWalk(self, rate=0):
        self.notify.debug('enterWalk')
        # TODO: Disable Toon emotions.

    def exitWalk(self):
        self.notify.debug('exitWalk')
        # TODO: Disable Toon emotions.

    def enterRun(self, rate=0):
        self.notify.debug('enterRun')
        # TODO: Disable Toon emotions.

    def exitRun(self):
        self.notify.debug('exitRun')
        # TODO: Disable Toon emotions.

    def enterSadNeutral(self, rate=0):
        self.notify.debug('enterSadNeutral')

    def exitSadNeutral(self):
        self.notify.debug('exitSadNeutral')

    def enterSadWalk(self, rate=0):
        self.notify.debug('enterSadWalk')

    def exitSadWalk(self):
        self.notify.debug('exitSadWalk')

    def enterCatchNeutral(self, rate=0):
        self.notify.debug('enterCatchNeutral')

    def exitCatchNeutral(self):
        self.notify.debug('exitCatchNeutral')

    def enterCatchRun(self, rate=0):
        self.notify.debug('enterCatchRun')

    def exitCatchRun(self):
        self.notify.debug('exitCatchRun')

    def enterCatchEatNeutral(self, rate=0):
        self.notify.debug('enterCatchEatNeutral')

    def exitCatchEatNeutral(self):
        self.notify.debug('exitCatchEatNeutral')

    def enterCatchEatNRun(self, rate=0):
        self.notify.debug('enterCatchEatNRun')

    def exitCatchEatNRun(self):
        self.notify.debug('exitCatchEatNRun')

    def setState(self, anim, rate):
        if self.toon.playingAnim != anim:
            self.fsm.request(anim, [rate])