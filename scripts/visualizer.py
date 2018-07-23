from bge import logic
from objproperties import ObjProperties
from puzzle import PuzzleLoader
from time import sleep
from patterns import PUZZLE_PATTERNS_4X4
from widgets import Button

def main():
    if not 'pattern_to_visualise' in logic.globalDict:
        return
    scene = logic.getCurrentScene()
    vsPatternName = logic.globalDict['pattern_to_visualise']
    vsPatternStruct = PUZZLE_PATTERNS_4X4[vsPatternName]
    vs = PatternVisualiser(logic)
    vs.visualise(vsPatternStruct)

    sceneObjs = scene.objects
    returnBtn = Button(sceneObjs['btn_close_scene'], logic)
    returnBtn.setOnclickAction(scene.end)

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
                vsBlock.color = [0.369, 0.625, 1.0, 1.0]

