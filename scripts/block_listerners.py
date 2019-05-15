from listerner import Listerner
from logger import logger

log = logger()
class GeneralBlockListerner(Listerner):
    def __init__(self, channel):
        from session_listerner_global_data import SessionListernerData
        super(GeneralBlockListerner, self).__init__(SessionListernerData(channel))

class BlockListerner(GeneralBlockListerner):
    def __init__(self, block, channel):
        channel = '%s_%s' % (block.blockID, channel)
        super(BlockListerner, self).__init__(channel)
        self.block = block

class OnMatchListerner(GeneralBlockListerner):
    '''
    Non block specific listerner for matched blocks
    '''
    def __init__(self):
        super(OnMatchListerner, self).__init__('ANY_BLOCK_ONMATCH')

    def onMatch(self):
        self.updateListerners(lambda listerner: listerner())

class OnMisMatchListerner(GeneralBlockListerner):
    '''
    Non block specific listerner for mismatched blocks
    '''

    def __init__(self):
        super(OnMisMatchListerner, self).__init__('ANY_BLOCK_ONMISMATCH')

    def onMisMatch(self):
        self.updateListerners(lambda listerner: listerner())

class OnClickBlockListerner(BlockListerner):
    def __init__(self, block):
        super(OnClickBlockListerner, self).__init__(block, 'CLICK')

    def onClick(self, controller, movableDirection, spaceBlock):
        log.debug('%s updating onclick listerners %s', self.block.blockID, self.getListerners())
        self.updateListerners(lambda listerner: listerner(
            self.block, controller, movableDirection, spaceBlock)
        )

class OnBlockSlidingListerner(BlockListerner):
    def __init__(self, block):
        super(OnBlockSlidingListerner, self).__init__(block, 'ONSLIDING')
    
    def onSliding(self, blockMotion):
        self.updateListerners(lambda listerner: listerner(blockMotion))

class OnBlockMovementListerner(Listerner):
    def __init__(self):
        from session_listerner_global_data import SessionListernerData
        super(OnBlockMovementListerner, self).__init__(SessionListernerData('ON_BLOCK_MOVEMENT'))
    
    def onMove(self):
        self.updateListerners(lambda listerner: listerner())

class OnBlockMovementStartListerner(BlockListerner):
    def __init__(self, block):
        super(OnBlockMovementStartListerner,self).__init__(block, 'ONMOVE_START')

    def onStart(self):
        self.updateListerners(lambda listerner: listerner())

class OnBlockMovementStopListerner(BlockListerner):
    def __init__(self, block):
        super(OnBlockMovementStopListerner, self).__init__(block, 'ONMOVE_STOP')

    def onStop(self, spaceBlock):
        self.updateListerners(lambda listerner: listerner(self.block, spaceBlock))

class OnDetectBlockListerner(BlockListerner):
    def __init__(self, block):
        super(OnDetectBlockListerner, self).__init__(block, 'ONDETECT')

    def onDetect(self, axisname):
        log.debug('Running %s onBlock detect listerner %s', self.block.blockID, self.getListerners())
        self.updateListerners(lambda listerner: listerner(axisname))

class OnMatchBlockListerner(BlockListerner):
    def __init__(self, block):
        super(OnMatchBlockListerner, self).__init__(block, 'ON_BLOCK_MATCH')

    def onMatch(self):
        self.updateListerners(lambda listerner: listerner())

class OnMisMatchBlockListerner(BlockListerner):
    def __init__(self, block):
        super(OnMisMatchBlockListerner, self).__init__(block, 'ON_BLOCK_MISMATCH')

    def onMisMatch(self):
        self.updateListerners(lambda listerner: listerner())
