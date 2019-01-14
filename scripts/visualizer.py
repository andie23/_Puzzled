from bge import logic
from objproperties import ObjProperties
from puzzle import PuzzleLoader
from time import sleep
from patterns import PUZZLE_PATTERNS_4X4
from widgets import Button, Text
from canvas import PatternCanvas
from navigator import *
from animate import initAnimation

def main(controller):
    if not 'setup_to_visualise' in logic.globalDict:
        return
    setup = logic.globalDict['setup_to_visualise']
    setCanvas(setup)
    patternStruct = PUZZLE_PATTERNS_4X4[setup['pattern']]
    vs = PatternVisualiser(logic)
    vs.visualise(patternStruct)

def setCanvas(setup):
    pcanvas = PatternCanvas()
    pcanvas.loadStatic()
    playBtn = Button(pcanvas.playBtnObj, logic)
    playBtn.setOnclickAction(navToPuzzle, setup)
    
    returnBtn = Button(pcanvas.backBtnObj, logic)
    returnBtn.setOnclickAction(closePatternScreen)
    Text(pcanvas.titleTxtObj, setup['name'])
    
    if 'description' in setup:
        Text(pcanvas.descriptionTxtObj, setup['description'])
        return
    
    Text(pcanvas.descriptionTxtObj,'''
            No Description
        ''')

def markVisualBlocks(controller):
    own = ObjProperties(controller.owner)
    if not own.getProp('isset'):
       own.setProp('timer', 0)
       return

    timer = own.getProp('timer')
    limit = own.getProp('limit')
    
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
        initAnimation({
            'scene_id' : 'PATTERN_VIEW',
            'target_obj' : vsBlock,
            'anim_name' : 'fade_in_match_color',
            'fstart' : 0.0, 
            'fstop' : 5.0, 
            'speed': 0.06
        })

    
class PatternVisualiser:
    def __init__(self, logic):
        self.globalDict = logic.globalDict
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

