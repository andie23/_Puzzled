from block_effects import *
from block_listerners import *
from audio import Audio
from audio_files import *

def default(block, onMatchListerner, onMisMatchListerner):
    vsBlock = block.getVisualBlock()
    onMatchListerner.attach(
        'match_default_behavior', 
        lambda: animate_match_color(vsBlock)
    )
    onMatchListerner.attach('play_ring_sound', Audio(SINGLE_DING).play)
    onMisMatchListerner.attach(
        'mis_match_default_behavior', 
        lambda: animate_default_color(vsBlock)
    )

def redAlert(block, onMatchListerner, onMisMatchListerner):
    vsblock = block.getVisualBlock()
    def onMisMatch():
        def resetTimers(playback):
            playback.unsetTimers()
            return True
        
        use_red_color(vsblock)
        Audio(ALERT_TONE).play()
        annoyingBeepAudio = Audio(SINGLE_BEEP)
        redFlashPlayback = animate_red_flashes(
            vsblock, delay=2.0, duration=5.0, speed=0.4,
            onstartAction=annoyingBeepAudio.play
        )

        fadeOutPlayBack = animate_to_transparent(
            vsblock, delay=10.0, 
            onfinishAction=Audio(OMNIOUS_BELL_RING).play
        )
        
        onMatchListerner.attach('clear_red_flash_timers', 
            lambda:resetTimers(redFlashPlayback))
        
        onMatchListerner.attach('clear_fade_out_timers', 
            lambda:resetTimers(fadeOutPlayBack))
            
    onMatchListerner.attach('match_default_behavior', 
            lambda: animate_match_color(vsblock))
    onMatchListerner.attach('play_ring_sound', Audio(SINGLE_DING).play)
    onMisMatchListerner.attach('mis_match_default_behavior', onMisMatch)
    onMisMatch()

    