from bge import logic
from objproperties import ObjProperties
from puzzle_loader import PuzzleLoader
from block_effects import animate_match_color

def markVisualBlocks(controller):
    own = ObjProperties(controller.owner)
    if not own.getProp('isset'):
       # stop marking blocks if property isset is false
       own.setProp('timer', 0)
       return

    timer = own.getProp('timer')
    limit = own.getProp('limit')
    # Pause marker for a duration of time before marking
    # the next block
    if timer >= limit:
        own.setProp('timer', 0)
        setNextMark(own)

def setNextMark(own): 
    scene = logic.getCurrentScene()
    vsBlocks = own.getPropObjGroup('visual_block', scene)
    blockNum = own.getProp('current_mark')
    
    if blockNum >= len(vsBlocks):
        return
    
    blockNum += 1
    own.setProp('current_mark', blockNum)

    vsBlock = own.getObjByPropVal(
        'block_number', blockNum, vsBlocks
    )

    if vsBlock:
        animate_match_color(vsBlock)
    
class PatternVisualiser:
    def __init__(self, logic):
        self.scene = logic.getCurrentScene()
        self.cont = logic.getCurrentController()

    def visualise(self, pattern):
        own = ObjProperties(self.cont.owner)
        staticBlocks = own.getPropObjGroup('static_block', self.scene)
        visualBlocks = own.getPropObjGroup('visual_block', self.scene)
        puzzle = PuzzleLoader(self.scene)
        puzzle.setStaticBlockNumbers(pattern, staticBlocks)
        
        for vsBlock in visualBlocks:
            vsProperty = ObjProperties(vsBlock)
            vsNum = vsProperty.getProp('block_number')  
        
            stBlock = vsProperty.getObjByPropVal(
                'block_number', vsNum, staticBlocks
            )
            if not stBlock:
                continue
            
            vsBlock.position = stBlock.position
            if vsNum != 0:
                vsBlock.visible = True
                
        own.setProp('isset', True)

