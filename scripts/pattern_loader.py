from bge import logic
from objproperties import ObjProperties
from puzzle_loader import PuzzleLoader

class PatternLoader():
    def __init__(self, scene, pattern):
        self.scene = scene
        self.pattern = pattern
    
    def load(self):
        staticBlocks = ObjProperties().getPropObjGroup(
            'static_block', self.scene
        )
        puzzleLoader = PuzzleLoader(self.scene)
        puzzleLoader.setStaticBlockNumbers(self.pattern, staticBlocks)
        self._loadVsBlocks(staticBlocks)
    
    def _loadVsBlocks(self, staticBlocks):
        for staticBlock in staticBlocks:
            vsBlock =  ObjProperties().getObjByPropVal(
                'visual_block', staticBlock['block_number'], 
                self.scene.objectsInactive
            )
            self.scene.addObject(vsBlock)
            vsBlock = self.scene.objects[str(vsBlock)]
            vsBlock.visible = False
            vsBlock.position = staticBlock.position
            vsBlock.setParent(staticBlock, False, False)
