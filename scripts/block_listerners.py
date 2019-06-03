from listerner import Listerner
from logger import logger

log = logger()

class BlockListerner(Listerner):
    def __init__(self, channel):
        from session_listerner_global_data import SessionListernerData
        super(BlockListerner, self).__init__(SessionListernerData(channel))

class OnBlockInitListerner(BlockListerner):
    def __init__(self):
        super(OnBlockInitListerner, self).__init__('ON_BLOCK_INIT')
    
    def onInit(self, block):
        log.debug('Block %s initialised', block.blockID)
        self.updateListerners(lambda listerner: listerner(block))

class OnDetectLogicalBlocksListerner(BlockListerner):
    def __init__(self):
        super(OnDetectLogicalBlocksListerner, self).__init__('ON_DETECT_BLOCKS')
    
    def onDetect(self, movableBlocks):
        log.debug('Spaceblock detected %s. Updating listerners %s', movableBlocks,self.getListerners())
        self.updateListerners(lambda listerner: listerner(movableBlocks))

class OnMatchListerner(BlockListerner):
    def __init__(self):
        super(OnMatchListerner, self).__init__('ON_BLOCK_MATCH')

    def onMatch(self, block):
        log.debug('Block %s has matched, updating listerners %s', block.blockID, self.getListerners())
        self.updateListerners(lambda listerner: listerner(block))

class OnMisMatchListerner(BlockListerner):
    def __init__(self):
        super(OnMisMatchListerner, self).__init__('ON_BLOCK_MISMATCH')

    def onMisMatch(self, block, wasMatch):
        log.debug('Block %s has mis-matched, updating listerners %s', block.blockID, self.getListerners())
        self.updateListerners(lambda listerner: listerner(block, wasMatch))

class OnBlockMovementStartListerner(BlockListerner):
    def __init__(self):
        super(OnBlockMovementStartListerner,self).__init__('ONMOVE_START')

    def onStart(self, block):
        self.updateListerners(lambda listerner: listerner(block))

class OnBlockMovementStopListerner(BlockListerner):
    def __init__(self):
        super(OnBlockMovementStopListerner, self).__init__('ONMOVE_STOP')

    def onStop(self, block):
        log.debug('block %s has stopped, updating listerners %s', block.blockID, self.getListerners())
        self.updateListerners(lambda listerner: listerner(block))
