from listerner import Listerner
from logger import logger
from global_dictionary import PuzzleSessionGlobalData

class GeneralBlockListerner(Listerner):
    def __init__(self, channel):
        listernerContainer = PuzzleSessionGlobalData().listerners
        Listerner.__init__(self, listernerContainer, channel)
    
class BlockListerner(GeneralBlockListerner):
    def __init__(self, block, channel):
        channel = '%s_%s' % (block.blockID, channel)
        GeneralBlockListerner.__init__(self, channel)
        self.block = block

class OnMatchListerner(GeneralBlockListerner):
    '''
    Non block specific listerner for matched blocks
    '''
    def __init__(self):
        GeneralBlockListerner.__init__(self, 'ANY_BLOCK_ONMATCH')
    
    def onMatch(self):
        self.updateListerners(lambda listerner: listerner(block))

class OnMisMatchListerner(GeneralBlockListerner):
    '''
    Non block specific listerner for mismatched blocks
    '''

    def __init__(self):
        GeneralBlockListerner.__init__(self, 'ANY_BLOCK_ONMISMATCH')

    def onMisMatch(self):
        self.updateListerners(lambda listerner: listerner())

class OnClickBlockListerner(BlockListerner):
    def __init__(self, block):
        BlockListerner.__init__(self, block, 'CLICK')

    def onClick(self, controller, movableDirection, spaceBlock):
        self.updateListerners(lambda listerner: listerner(
            self.block, controller, movableDirection, spaceBlock)
        )

class OnBlockSlidingListerner(BlockListerner):
    def __init__(self, block):
        BlockListerner.__init__(self, block, 'ONSLIDING')
    
    def onSliding(self, blockMotion):
        self.updateListerners(lambda listerner: listerner(blockMotion))

class OnBlockMovementStartListerner(BlockListerner):
    def __init__(self, block):
        BlockListerner.__init__(self, block, 'ONMOVE_START')

    def onStart(self):
        self.updateListerners(lambda listerner: listerner())

class OnBlockMovementStopListerner(BlockListerner):
    def __init__(self, block):
        BlockListerner.__init__(self, block, 'ONMOVE_STOP')
    
    def onStop(self, spaceBlock):
        self.updateListerners(lambda listerner: listerner(self.block, spaceBlock))

class OnDetectBlockListerner(BlockListerner):
    def __init__(self, block):
        BlockListerner.__init__(self, block, 'ONDETECT')

    def onDetect(self, axisname):
        self.updateListerners(lambda listerner: listerner(axisname))

class OnMatchBlockListerner(BlockListerner):
    def __init__(self, block):
        BlockListerner.__init__(self, block, 'ONMATCH')

    def onMatch(self):
        self.updateListerners(lambda listerner: listerner())

class OnMisMatchBlockListerner(BlockListerner):
    def __init__(self, block):
        BlockListerner.__init__(self, block, 'ONMISMATCH')

    def onMisMatch(self):
        self.updateListerners(lambda listerner: listerner())
