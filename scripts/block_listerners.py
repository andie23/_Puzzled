from listerner import Listerner
from logger import logger

class BlockListerner(Listerner):
    def __init__(self, block, channel):
        Listerner.__init__(self, '%s_%s' % (block.blockID, channel))
        self.block = block

class OnMatchListerner():
    '''
    Non block specific listerner for matched blocks
    '''

    def __init__(self):
        Listerner.__init__(self, 'ANY_BLOCK_ONMATCH')
    
    def onMatch(self):
        self.updateListerners(lambda listerner: listerner(block))

class OnMisMatchListerner():
    '''
    Non block specific listerner for mismatched blocks
    '''
    
    def __init__(self):
        Listerner.__init__(self, 'ANY_BLOCK_ONMISMATCH')

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

class OnStateChangeBlockListerner(BlockListerner):
    def __init__(self, block):
        BlockListerner.__init__(self, block, 'ONSTATE_CHANGE')

    def onChange(self, prevState, newState):
        self.updateListerners(lambda listerner: listerner(prevState, newState))
