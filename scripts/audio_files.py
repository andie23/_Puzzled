from config import SOUND_DIR
from bge import logic

def __getSound(soundFile):
    filePath = '//%s/%s' % (SOUND_DIR, soundFile)
    return logic.expandPath(filePath)

SLIDING_BLOCK = __getSound('zapsplat_whoosh.mp3')
SINGLE_DING = __getSound('zapsplat_desk_bell_single_ring.mp3')
CLOCK_TICKING = __getSound('soundbites_ticking_clock.mp3')