from bge import logic
from navigator import *
from hud import HudClock
from patterns import PUZZLE_PATTERNS_4X4
from block_behavior_map import BLOCK_BEHAVIORS
from os import getenv
from hud import HudClock, HudCanvas
from logger import logger
from pcache import Profile
import dialog

log = logger()

def createSession():
    chng = getLoadedChallenge()
    logic.globalDict['play_session'] = {
        'player': getDefaultUser(),
        'challenge' : {
            'id' : getChallengeId(chng['name']),
            'name' : chng['name']
        },
        'puzzle' : {
            'listerners': {},
            'block_states' : {},
            'block_count' : 15,
            'block_behavior' : BLOCK_BEHAVIORS[chng['behavior']],
            'block_pattern' : PUZZLE_PATTERNS_4X4[chng['pattern']],
            'movable_blocks' : {},
            'match_list' : [],
            'match_streak_list': [],
        },
        'play' : {
            'moves' : 0,
            'time' : 0.0,
            'match_streak' : 0
        },
        'game' : {
            'status': ''
        }
    }
    log.debug('Created session: %s', logic.globalDict['play_session'])

def getSession():
    if isSessionSet():
        return logic.globalDict['play_session']
    return None

def isSessionSet():
    return 'play_session' in logic.globalDict
    
def getSessionVar(main, var=None):
    session = getSession()
    if var is None:
        return session[main]
    return session[main][var]

def getBlocksInMatchStreak():
    return getPuzzleState('match_streak_list')

def getChallengeId(name):
    return name.replace(' ', '_').upper()

def getActiveChallenge(var=None):
    return getSessionVar('challenge', var)

def getPuzzleState(var=None):
    return getSessionVar('puzzle', var)

def getPlayStats(var=None):
    return getSessionVar('play', var)

def getLoadedChallenge():
    return logic.globalDict['loaded_challenge']

def getGameStatus():
    return getSessionVar('game', 'status')

def getDefaultUser(var=None):
    if 'default_user' not in logic.globalDict:
        user = getenv("USERNAME") 
        if not user:
            user = 'Default'
        profile = Profile()
        profile.name = user
        if not profile.fetch():
            profile.add()
        logic.globalDict['default_user'] = {
            'id' : profile.id, 
            'name': profile.name
        }
    if var:
        return logic.globalDict['default_user'][var]
    return logic.globalDict['default_user']

def clearMovableBlocks():
    setPuzzleState('movable_blocks', {})

def addMovableBlock(block):
    getPuzzleState('movable_blocks').update(block)

def addMatchStreak(blockId):
    getPuzzleState('match_streak_list').append(blockId)

def addMatch(blockId):
    getPuzzleState('match_list').append(blockId)

def setPlayStats(var, val):
    setSessionVar('play', var, val)

def changeEventScript(scriptname):
    setPuzzleState('block_behavior', BLOCK_BEHAVIORS[scriptname])

def setPuzzleState(var, val):
    setSessionVar('puzzle', var, val)

def setGameStatus(val):
    setSessionVar('game', 'status', val)

def setSessionVar(main, var, val):
    getSession()[main][var] = val

def getBlockBehavior():
    return getPuzzleState('block_behavior')

def getAllListerners():
    return getPuzzleState('listerners')

def getChannel(channel):
    listerner = getPuzzleState('listerners')
    if channel in listerner:
        return listerner[channel]

def setChannel(channel, data):
    listerners = getAllListerners()
    listerners[channel] = data
    setPuzzleState('listerners', listerners)

def removeMatch(blockId):
    matches = getPuzzleState('match_list')
    matches.remove(blockId)

@dialog.confirm('QUIT' ,'Really? you want to exit to the main menu?')
def quit():
    navToChallenges()
    setGameStatus('EXITED')

@dialog.confirm('RESHUFFLE', 'Are you stuck or something? do you want to reshuffle?')
def reshuffle():
    shelper = SceneHelper(logic)
    closeAssessmentScreen()
    shelper.restart(['MAIN', 'HUD'])
    setGameStatus('RESTARTED')

def stop():
    from block import SpaceBlock

    scene = SceneHelper(logic).getscene('MAIN') 
    SpaceBlock(scene).lock()
    HudClock().stop()
    setPlayStats('time', HudClock().snapshot)
    hud = HudCanvas('HUD')
    hud.load()
    hud.disableWidgets()
    setGameStatus('STOPPED')

def pause():
    overlayDialog()
    shelper = SceneHelper(logic)
    shelper.pause(['MAIN', 'HUD'])
    dialog.pauseDialog()
    setGameStatus('PAUSED')

def resume():
    shelper = SceneHelper(logic)
    shelper.resume(['MAIN', 'HUD'])
    setGameStatus('RESUMED')
    closeDialogScreen()

def start(controller):
    from block import SpaceBlock
    from modes import hasModes, isModeSet, startTimeTrial, getModeSetting

    scene = SceneHelper(logic).getscene('MAIN')
    SpaceBlock(scene).unLock()
    HudClock().start()