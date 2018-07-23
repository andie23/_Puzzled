from bge import logic
from objproperties import ObjProperties
from puzzle import PuzzleLoader
from time import sleep
from patterns import PUZZLE_PATTERNS_4X4

def visualisePattern(controller):
    if not 'visualise_pattern' in logic.globalDict
       return
    
    scene = logic.getCurrentScene()
    pattern = logic.globalDict['visualise_pattern']
    own = ObjProperties(controller.owner)

    staticBlocks = own.getPropObjGroup('static_block', scene)
    visualBlocks = own.getPropObjGroup('visual_block', scene)
    puzzle = PuzzleLoader(scene)
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
            vsBlock.color = [0.369, 0.625, 1.0, 1.0]


