from listerner import Listerner

class BlockListerner(Listerner):
    def __init__(self, block, channel):
        Listerner.__init__(self, '%s_%s' % (block.blockID, channel))
        self.block = block

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

class OnStartBlockDetection(Listerner):
    def __init__(self):
        Listerner.__init__(self, 'SPACE_BLOCK_ONSTART_DETECTION')
    
    def onStart(self):
        self.updateListerners(lambda listerner: listerner())

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

class OnDurationStartBlockListerner(BlockListerner):
    def __init__(self, block):
        BlockListerner.__init__(self, block, 'ONDURATION_START')

    def onStart(self):
        self.updateListerners(lambda listerner: listerner())

class OnDurationExpireBlockListerner(BlockListerner):
    def __init__(self, block):
        BlockListerner.__init__(self, block, 'ONDURATION_EXPIRE')

    def onExpire(self):
        self.updateListerners(lambda listerner: listerner())

class OnDelayStartBlockListerner(Listerner):
    def __init__(self, block):
        Listerner.__init__(self, block, 'DELAY_START')

    def onStart(self):
        self.updateListerners(lambda listerner: listerner())

class onDelayExpireBlockListerner(Listerner):
    def __init__(self, block):
        Listerner.__init__(self, block, 'DELAY_EXPIRE')

    def onExpire(self):
        self.updateListerners(lambda listerner: listerner())
