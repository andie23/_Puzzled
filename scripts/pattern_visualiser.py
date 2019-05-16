from bge import logic
from objproperties import ObjProperties
from puzzle_loader import PuzzleLoader
from animate import initAnimation

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
    def setVsBlockCol(vsblock):
        vsBlock.color = [0.369, 0.625, 1.0, 1.0]
    
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
        initAnimation({
            'scene_id' : 'PATTERN_VIEW',
            'target_obj' : vsBlock,
            'anim_name' : 'fade_in_match_color',
            'fstart' : 0.0, 
            'fstop' : 5.0, 
            'speed': 1.0,
            'on_finish_action' : lambda: setVsBlockCol(vsBlock)
        })
    
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

