from block import Block
from logger import logger
from bge import logic
 
DETECTION_POINTS = {
    'LEFT' : [10.0, 0.0, 0.0],
    'RIGHT' : [-10.0, 0.0, 0.0],
    'DOWN' : [0.0, 10.0, 0.0],
    'UP' : [0.0, -10.0, 0.0]
}
log = logger()

class SpaceBlock(Block):
    def __init__(self):
        scene = logic.getCurrentScene()
        super(SpaceBlock, self).__init__(
            scene, scene.objects['space_block']
        )

    def detectLogicalBlocks(self):
        detectedObjs = {}    
        for direction, point in DETECTION_POINTS.items():
            block = self.obj.rayCastTo(
                point, 1.0, 'logical_block'
            )
            if not block:
                continue
            detectedObjs[str(block['block_number'])] = direction 
        return detectedObjs

    def setPosition(self, node):
        self.obj.position[0] = node.position[0]
        self.obj.position[1] = node.position[1]
        self.setNode(node)

    @property
    def isDisabled(self):
        return self.obj['is_disabled']

    @property
    def isLocked(self):
        return self.obj['is_locked']

    def enable(self):
        self.obj['is_disabled'] = False
        log.debug('Spaceblock is enabled')
    
    def disable(self):
        self.obj['is_disabled'] = True
        log.debug('Spaceblock is disabled')

    def unLock(self):
        self.obj['is_locked'] = False
        log.debug('Spaceblock is unlocked')
    
    def lock(self):
        self.obj['is_locked'] = True
        log.debug('Spaceblock is now locked')
