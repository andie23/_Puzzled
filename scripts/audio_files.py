from config import SOUND_DIR
from bge import logic

def __getSound(soundFile):
    filePath = '//%s/%s' % (SOUND_DIR, soundFile)
    return logic.expandPath(filePath)

ALERT_TONE = __getSound('zapsplat_multimedia_alert_error_002_26393.mp3')
SINGLE_BEEP = __getSound('zapsplat_multimedia_beep_digital_001_26599.mp3')
OMNIOUS_BELL_RING = __getSound('skyclad_sound_belldistant_muffled_reverb.mp3')
SLIDING_BLOCK = __getSound('zapsplat_whoosh.mp3')
SINGLE_DING = __getSound('zapsplat_desk_bell_single_ring.mp3')
CLOCK_TICKING = __getSound('soundbites_ticking_clock.mp3')
NOTIFICATION_CHIME = __getSound('zapsplat_notification_chime_bell.mp3')
BUTTON_CLICK = __getSound('zapsplat_dial_single_number_button.mp3')
UI_MAXIMISE_WOOSH = __getSound('zapsplat_interface_sound_whoosh.mp3')