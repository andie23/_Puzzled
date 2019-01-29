from bge import logic
from timer import Timer 
from animate import initAnimation
from navigator import *
from notification import showNotification
import dialog

def startTimeTrial(setting):
    timer = Timer('time_trial', 'MAIN')
    timer.setTimer(setting['limit'], setting['on_finish'])
    timer.start()
    showNotification(
        "You have %s seconds left!!" % timer.timerLimit
    )

def stopTimeTrial():
	timer = Timer('time_trial', 'MAIN')
	if timer.isAlive():
		timer.load()
		timer.stop()

def set_blocks_to_transparent():
	setEventScript('NO_COLOR_MODE')
	showNotification("Changing appearance of blocks..")

def set_blocks_to_default_color():
	setEventScript('DEFAULT_MODE')

def end_game_and_set_blocks_to_transparent():
	from game import stop
	def reloadDialog():
		overlayDialog()
		shelper = SceneHelper(logic)
		shelper.pause(['MAIN', 'HUD'])
		dialog.puzzledDialog()
	
	showNotification("You have failed the challenge",
		duration=5.0, callback=reloadDialog)
	stop()
	setEventScript('NO_COLOR_MODE')

def setEventScript(scriptName):
	from game import setPuzzleState

	scene = SceneHelper(logic).getscene('MAIN')
	mainObj = scene.objects['puzzle_main']
	mainObj.sendMessage('event_script_resetted')
	setPuzzleState('block_script', scriptName)

def hasModes():
	from game import getPuzzleState
   
	return 'mode' in getPuzzleState('block_states')

def isModeSet(mode):
	from game import getPuzzleState
    
	return mode in getPuzzleState('block_states')['mode']

def getModeSetting(mode):
	from game import getPuzzleState
    
	return getPuzzleState('block_states')['mode'][mode]