from bge import logic
from block import Block
from block_motion import BlockMotion

class LogicalBlock(Block):
    def __init__(self, obj):
        super(LogicalBlock, self).__init__(logic.getCurrentScene(), obj)

    @property
    def isMatch(self):
        return self.obj['is_match']

    @property
    def wasMatch(self):
        return self.obj['was_match']

    def getVisualBlock(self):
        vsBlock = self.obj['_visual_block']
        return self.scene.objects[vsBlock]

    def setColor(self, color):
        vsBlock = self.getVisualBlock()
        vsBlock.color = color

    def setVsBlock(self, vsblock):
        self.obj['_visual_block'] = vsblock

    def setMatch(self, boolval):
        self.obj['is_match'] = boolval

    def setWasMatch(self, boolval):
        self.obj['was_match'] = boolval

    def evaluateMatch(self):
        if not self.positionNode:
            return False

        if self.positionNodeID == self.blockID:
            self.setMatch(True)
            return True

        if self.positionNodeID != self.blockID:
            if self.isMatch:
                self.setWasMatch(True)
            self.setMatch(False)
            return False