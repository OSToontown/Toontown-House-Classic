from pandac.PandaModules import *

from tth.base import TTHouseGlobals

# General
ToonAvatarRadius = 1.4
FloorOffset = 0.025

# Movement
WalkCutOff = 0.5
RunCutOff = 8.0
ToonSpeedFactor = 1.25
ToonForwardSpeed = 16.0 * ToonSpeedFactor
ToonJumpForce = 24.0
ToonReverseSpeed = 8.0 * ToonSpeedFactor
ToonRotateSpeed = 80.0 * ToonSpeedFactor
ToonForwardSlowSpeed = 6.0
ToonJumpSlowForce = 4.0
ToonReverseSlowSpeed = 2.5
ToonRotateSlowSpeed = 33.0
STAND_INDEX = 0
WALK_INDEX = 1
RUN_INDEX = 2
REVERSE_INDEX = 3
STRAFE_LEFT_INDEX = 4
STRAFE_RIGHT_INDEX = 5
WakeRunDelta = 0.1
WakeWalkDelta = 0.2

# Head
HeadDict = {
    'dls':'/models/char/tt_a_chr_dgm_shorts_head_',
    'dss':'/models/char/tt_a_chr_dgm_skirt_head_',
    'dsl':'/models/char/tt_a_chr_dgs_shorts_head_',
    'dll':'/models/char/tt_a_chr_dgl_shorts_head_',
    'c':'/models/char/cat-heads-',
    'h':'/models/char/horse-heads-',
    'm':'/models/char/mouse-heads-',
    'r':'/models/char/rabbit-heads-',
    'f':'/models/char/duck-heads-',
    'p':'/models/char/monkey-heads-',
    'b':'/models/char/bear-heads-',
    's':'/models/char/pig-heads-'
}
EyelashDict = {
    'd':'/models/char/dog-lashes',
    'c':'/models/char/cat-lashes',
    'h':'/models/char/horse-lashes',
    'm':'/models/char/mouse-lashes',
    'r':'/models/char/rabbit-lashes',
    'f':'/models/char/duck-lashes',
    'p':'/models/char/monkey-lashes',
    'b':'/models/char/bear-lashes',
    's':'/models/char/pig-lashes'
}
DogMuzzleDict = {
    'dls':'/models/char/dogMM_Shorts-headMuzzles-',
    'dss':'/models/char/dogMM_Skirt-headMuzzles-',
    'dsl':'/models/char/dogSS_Shorts-headMuzzles-',
    'dll':'/models/char/dogLL_Shorts-headMuzzles-'
}
toonHeadScales = {
    'mouse':Point3(1.0),
    'cat':Point3(1.0),
    'duck':Point3(1.0),
    'rabbit':Point3(1.0),
    'horse':Point3(1.0),
    'dog':Point3(1.0),
    'monkey':Point3(1.0),
    'bear':Point3(1.0),
    'pig':Point3(1.0)
}
headHeightDict = {
    'dls':0.75,
    'dss':0.5,
    'dsl':0.5,
    'dll':0.75,
    'cls':0.75,
    'css':0.5,
    'csl':0.5,
    'cll':0.75,
    'hls':0.75,
    'hss':0.5,
    'hsl':0.5,
    'hll':0.75,
    'mls':0.75,
    'mss':0.5,
    'rls':0.75,
    'rss':0.5,
    'rsl':0.5,
    'rll':0.75,
    'fls':0.75,
    'fss':0.5,
    'fsl':0.5,
    'fll':0.75,
    'pls':0.75,
    'pss':0.5,
    'psl':0.5,
    'pll':0.75,
    'bls':0.75,
    'bss':0.5,
    'bsl':0.5,
    'bll':0.75,
    'sls':0.75,
    'sss':0.5,
    'ssl':0.5,
    'sll':0.75
}

# Body
LegDict = {
    's':'/models/char/tt_a_chr_dgs_shorts_legs_',
    'm':'/models/char/tt_a_chr_dgm_shorts_legs_',
    'l':'/models/char/tt_a_chr_dgl_shorts_legs_'
}
TorsoDict = {
    's':'/models/char/dogSS_Naked-torso-',
    'm':'/models/char/dogMM_Naked-torso-',
    'l':'/models/char/dogLL_Naked-torso-',
    'ss':'/models/char/tt_a_chr_dgs_shorts_torso_',
    'ms':'/models/char/tt_a_chr_dgm_shorts_torso_',
    'ls':'/models/char/tt_a_chr_dgl_shorts_torso_',
    'sd':'/models/char/tt_a_chr_dgs_skirt_torso_',
    'md':'/models/char/tt_a_chr_dgm_skirt_torso_',
    'ld':'/models/char/tt_a_chr_dgl_skirt_torso_'
}
toonBodyScales = {
    'mouse':0.6,
    'cat':0.73,
    'duck':0.66,
    'rabbit':0.74,
    'horse':0.85,
    'dog':0.85,
    'monkey':0.68,
    'bear':0.85,
    'pig':0.77
}
legHeightDict = {
    's':1.5,
    'm':2.0,
    'l':2.75
}
torsoHeightDict = {
    's':1.5,
    'm':1.75,
    'l':2.25,
    'ss':1.5,
    'ms':1.75,
    'ls':2.25,
    'sd':1.5,
    'md':1.75,
    'ld':2.25
}

# Animations
LegsAnimDict = {}
TorsoAnimDict = {}
HeadAnimDict = {}
Phase3AnimList = (
    ('neutral', 'neutral'),
    ('run', 'run')
)
Phase3_5AnimList = (
    ('walk', 'walk'),
    ('teleport', 'teleport'),
    ('book', 'book'),
    ('jump', 'jump'),
    ('running-jump', 'running-jump'),
    ('jump-squat', 'jump-zstart'),
    ('jump-idle', 'jump-zhang'),
    ('jump-land', 'jump-zend'),
    ('running-jump-squat', 'leap_zstart'),
    ('running-jump-idle', 'leap_zhang'),
    ('running-jump-land', 'leap_zend'),
    ('pushbutton', 'press-button'),
    ('throw', 'pie-throw'),
    ('victory', 'victory-dance'),
    ('sidestep-left', 'sidestep-left'),
    ('conked', 'conked'),
    ('cringe', 'cringe'),
    ('wave', 'wave'),
    ('shrug', 'shrug'),
    ('angry', 'angry'),
    ('tutorial-neutral', 'tutorial-neutral'),
    ('left-point', 'left-point'),
    ('right-point', 'right-point'),
    ('right-point-start', 'right-point-start'),
    ('give-props', 'give-props'),
    ('give-props-start', 'give-props-start'),
    ('right-hand', 'right-hand'),
    ('right-hand-start', 'right-hand-start'),
    ('duck', 'duck'),
    ('sidestep-right', 'jump-back-right'),
    ('periscope', 'periscope')
)
Phase4AnimList = (
    ('sit', 'sit'),
    ('sit-start', 'intoSit'),
    ('swim', 'swim'),
    ('tug-o-war', 'tug-o-war'),
    ('sad-walk', 'losewalk'),
    ('sad-neutral', 'sad-neutral'),
    ('up', 'up'),
    ('down', 'down'),
    ('left', 'left'),
    ('right', 'right'),
    ('applause', 'applause'),
    ('confused', 'confused'),
    ('bow', 'bow'),
    ('curtsy', 'curtsy'),
    ('bored', 'bored'),
    ('think', 'think'),
    ('battlecast', 'fish'),
    ('cast', 'cast'),
    ('castlong', 'castlong'),
    ('fish-end', 'fishEND'),
    ('fish-neutral', 'fishneutral'),
    ('fish-again', 'fishAGAIN'),
    ('reel', 'reel'),
    ('reel-H', 'reelH'),
    ('reel-neutral', 'reelneutral'),
    ('pole', 'pole'),
    ('pole-neutral', 'poleneutral'),
    ('slip-forward', 'slip-forward'),
    ('slip-backward', 'slip-backward'),
    ('catch-neutral', 'gameneutral'),
    ('catch-run', 'gamerun'),
    ('catch-eatneutral', 'eat_neutral'),
    ('catch-eatnrun', 'eatnrun'),
    ('catch-intro-throw', 'gameThrow'),
    ('swing', 'swing'),
    ('pet-start', 'petin'),
    ('pet-loop', 'petloop'),
    ('pet-end', 'petend'),
    ('scientistJealous', 'scientistJealous'),
    ('scientistEmcee', 'scientistEmcee'),
    ('scientistWork', 'scientistWork'),
    ('scientistGame', 'scientistGame')
)
Phase5AnimList = (
    ('water-gun', 'water-gun'),
    ('hold-bottle', 'hold-bottle'),
    ('firehose', 'firehose'),
    ('spit', 'spit'),
    ('tickle', 'tickle'),
    ('smooch', 'smooch'),
    ('happy-dance', 'happy-dance'),
    ('sprinkle-dust', 'sprinkle-dust'),
    ('juggle', 'juggle'),
    ('climb', 'climb'),
    ('sound', 'shout'),
    ('toss', 'toss'),
    ('hold-magnet', 'hold-magnet'),
    ('hypnotize', 'hypnotize'),
    ('struggle', 'struggle'),
    ('lose', 'lose'),
    ('melt', 'melt')
)
Phase5_5AnimList = (
    ('takePhone', 'takePhone'),
    ('phoneNeutral', 'phoneNeutral'),
    ('phoneBack', 'phoneBack'),
    ('bank', 'jellybeanJar'),
    ('callPet', 'callPet'),
    ('feedPet', 'feedPet'),
    ('start-dig', 'into_dig'),
    ('loop-dig', 'loop_dig'),
    ('water', 'water')
)
Phase6AnimList = (
    ('headdown-putt', 'headdown-putt'),
    ('into-putt', 'into-putt'),
    ('loop-putt', 'loop-putt'),
    ('rotateL-putt', 'rotateL-putt'),
    ('rotateR-putt', 'rotateR-putt'),
    ('swing-putt', 'swing-putt'),
    ('look-putt', 'look-putt'),
    ('lookloop-putt', 'lookloop-putt'),
    ('bad-putt', 'bad-putt'),
    ('badloop-putt', 'badloop-putt'),
    ('good-putt', 'good-putt')
)
Phase9AnimList = (
    ('push', 'push'),
)
Phase10AnimList = (
    ('leverReach', 'leverReach'),
    ('leverPull', 'leverPull'),
    ('leverNeutral', 'leverNeutral')
)
PhaseAnimLists = {
    'phase_3':Phase3AnimList,
    'phase_3.5':Phase3_5AnimList,
    'phase_4':Phase4AnimList,
    'phase_5':Phase5AnimList,
    'phase_5.5':Phase5_5AnimList,
    'phase_6':Phase6AnimList,
    'phase_9':Phase9AnimList,
    'phase_10':Phase10AnimList
}

def compileAnimLists():
    """
    "Lazy instantiation" of LegsAnimDict, TorsoAnimDict, and HeadAnimDict.
    Compiles the animation lists into dictionaries that follow the format of:
        anim->filename.
    Lazy instantiation is used to increase start-up performance.
    """

    def makeAnimDict(phaseStr, animList, partDict, globalAnimDict):
        for key, value in partDict.items():
            globalAnimDict.setdefault(key, {})
            for anim in animList:
                globalAnimDict[key][anim[0]] = phaseStr + value + anim[1]

    for phaseStr, animList in PhaseAnimLists.items():
        makeAnimDict(phaseStr, animList, LegDict, LegsAnimDict)
        makeAnimDict(phaseStr, animList, TorsoDict, TorsoAnimDict)
        filteredHeadDict = {k: v for k, v in HeadDict.items() if 'd' in k}
        makeAnimDict(phaseStr, animList, filteredHeadDict, HeadAnimDict)

def unloadPhaseAnims(phaseStr='phase_3'):
    """
    Unloads the animations of the provided phase file on the local avatar. This
    function also has a set of pure code legibility functions:
        unloadBasicAnims(), unloadTutorialBattleAnims(), unloadMinigameAnims(),
        unloadBattleAnims(), unloadSellbotHQAnims(), unloadCashbotHQAnims().
    """
    animList = PhaseAnimLists.get(phaseStr)
    if not animList:
        raise ValueError("Tried to unload nonexistent phase '%s'" % phaseStr)
    elif not hasattr(base, 'localAvatar'):
        raise AttributeError(
            "Tried to unload phase '%s' on undefined avatar" % phaseStr)
    for anim in animList:
        if anim[0] in LegsAnimDict[base.localAvatar.style.legs]:
            base.localAvatar.unloadAnims([anim[0]], 'legs', None)
        elif anim[0] in TorsoAnimDict[base.localAvatar.style.torso]:
            base.localAvatar.unloadAnims([anim[0]], 'torso', None)
        elif 'd' in base.localAvatar.style.head:
            if anim[0] in HeadAnimDict[base.localAvatar.style.head]:
                base.localAvatar.unloadAnims([anim[0]], 'head', None)

def unloadBasicAnims():
    unloadPhaseAnims('phase_3')

def unloadTutorialBattleAnims():
    unloadPhaseAnims('phase_3.5')

def unloadMinigameAnims():
    unloadPhaseAnims('phase_4')

def unloadBattleAnims():
    unloadPhaseAnims('phase_5')

def unloadSellbotHQAnims():
    unloadPhaseAnims('phase_9')

def unloadCashbotHQAnims():
    unloadPhaseAnims('phase_10')

# Dialog
DogDialogueArray = []
CatDialogueArray = []
HorseDialogueArray = []
RabbitDialogueArray = []
MouseDialogueArray = []
DuckDialogueArray = []
MonkeyDialogueArray = []
BearDialogueArray = []
PigDialogueArray = []

def loadDialog():
    loadPath = 'phase_3.5/audio/dial/'
    DogDialogueFiles = (
        'AV_dog_short', 'AV_dog_med', 'AV_dog_long', 'AV_dog_question',
        'AV_dog_exclaim', 'AV_dog_howl'
    )
    for filename in DogDialogueFiles:
        DogDialogueArray.append(base.loadSfx(loadPath + filename + '.mp3'))

    catDialogueFiles = (
        'AV_cat_short', 'AV_cat_med', 'AV_cat_long', 'AV_cat_question',
        'AV_cat_exclaim', 'AV_cat_howl'
    )
    for filename in catDialogueFiles:
        CatDialogueArray.append(base.loadSfx(loadPath + filename + '.mp3'))

    horseDialogueFiles = (
        'AV_horse_short', 'AV_horse_med', 'AV_horse_long', 'AV_horse_question',
        'AV_horse_exclaim', 'AV_horse_howl'
    )
    for filename in horseDialogueFiles:
        HorseDialogueArray.append(base.loadSfx(loadPath + filename + '.mp3'))

    rabbitDialogueFiles = (
        'AV_rabbit_short', 'AV_rabbit_med', 'AV_rabbit_long',
        'AV_rabbit_question', 'AV_rabbit_exclaim', 'AV_rabbit_howl'
    )
    for filename in rabbitDialogueFiles:
        RabbitDialogueArray.append(base.loadSfx(loadPath + filename + '.mp3'))

    mouseDialogueFiles = (
        'AV_mouse_short', 'AV_mouse_med', 'AV_mouse_long', 'AV_mouse_question',
        'AV_mouse_exclaim', 'AV_mouse_howl'
    )
    for filename in mouseDialogueFiles:
        MouseDialogueArray.append(base.loadSfx(loadPath + filename + '.mp3'))

    duckDialogueFiles = (
        'AV_duck_short', 'AV_duck_med', 'AV_duck_long', 'AV_duck_question',
        'AV_duck_exclaim', 'AV_duck_howl'
    )
    for filename in duckDialogueFiles:
        DuckDialogueArray.append(base.loadSfx(loadPath + filename + '.mp3'))

    monkeyDialogueFiles = (
        'AV_monkey_short', 'AV_monkey_med', 'AV_monkey_long',
        'AV_monkey_question', 'AV_monkey_exclaim', 'AV_monkey_howl'
    )
    for filename in monkeyDialogueFiles:
        MonkeyDialogueArray.append(base.loadSfx(loadPath + filename + '.mp3'))

    bearDialogueFiles = (
        'AV_bear_short', 'AV_bear_med', 'AV_bear_long', 'AV_bear_question',
        'AV_bear_exclaim', 'AV_bear_howl'
    )
    for filename in bearDialogueFiles:
        BearDialogueArray.append(base.loadSfx(loadPath + filename + '.mp3'))

    pigDialogueFiles = (
        'AV_pig_short', 'AV_pig_med', 'AV_pig_long', 'AV_pig_question',
        'AV_pig_exclaim', 'AV_pig_howl'
    )
    for filename in pigDialogueFiles:
        PigDialogueArray.append(base.loadSfx(loadPath + filename + '.mp3'))

def unloadDialog():
    """
    Convenience function for deleting the loaded dialog sound effects.
    """
    DogDialogueArray[:] = []
    CatDialogueArray[:] = []
    HorseDialogueArray[:] = []
    RabbitDialogueArray[:] = []
    MouseDialogueArray[:] = []
    DuckDialogueArray[:] = []
    MonkeyDialogueArray[:] = []
    BearDialogueArray[:] = []
    PigDialogueArray[:] = []

# Font
ToonFont = None

def getToonFont():
    global ToonFont
    if ToonFont == None:
        ToonFont = loader.loadFont(TTHouseGlobals.ToonFontPath, lineHeight=1.0)
    return ToonFont