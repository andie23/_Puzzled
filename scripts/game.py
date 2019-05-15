from game_event_listerners import *

def quit():
    OnInvokeGameQuitListerner().onInvoke()

def reshuffle():
    OnInvokePuzzleReshuffleListerner().onInvoke()    

def stop():
    OnGameStopListerner().onStop()

def pause():
    OnGamePauseListerner().onPause()

def resume():
    OnGameResumeListerner().onResume()

def start():
    OnGameStartListerner().onStart()