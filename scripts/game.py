from game_event_listerners import *
log = logger()

def quit():
    OnGameQuitListerner().onQuit()

def reshuffle():
    OnPuzzleReshuffleListerner().onReshuffle()    

def stop():
    OnGameStopListerner().onStop()

def pause():
    OnGamePauseListerner().onPause()

def resume():
    OnGameResumeListerner().onResume()

def start():
    OnGameStartListerner().onStart()