from bge import logic
from timer import Timer 
from animate import initAnimation
from navigator import *
from notification import showNotification
import game
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
	def setBlockState():
		overlayDialog()
		shelper = SceneHelper(logic)
		shelper.pause(['MAIN', 'HUD'])
		dialog.puzzledDialog()
	
	showNotification("You have failed the challenge",
		duration=5.0, callback=setBlockState)
	game.stop()
	setEventScript('NO_COLOR_MODE')

def setEventScript(scriptName):
	from sscripts import SCRIPTS
	scene = SceneHelper(logic).getscene('MAIN')
	mainObj = scene.objects['puzzle_main']
	mainObj.sendMessage('event_script_resetted')
	logic.globalDict['eventScript'] = SCRIPTS[scriptName]

def hasModes():
    return 'mode' in logic.globalDict['eventScript']

def isModeSet(mode):
    return mode in logic.globalDict['eventScript']['mode']

def getModeSetting(mode):
    return logic.globalDict['eventScript']['mode'][mode]