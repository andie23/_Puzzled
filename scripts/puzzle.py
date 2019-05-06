#########################################################
# Author: Andrew Mfune
# Date: 22/05/2018
# Description: Contains class modules for puzzle blocks
#########################################################
from objproperties import ObjProperties
from random import randint
from logger import logger
from exception import PuzzleLoaderError
from block import LogicalBlock

class PuzzleLoader():
    '''
    This is a puzzle setup module that contains methods for loading
    logical puzzle blocks into the scene, visual blocks and assigning 
    numbers to individual blocks and static blocks.
    '''

    def __init__(self, scene):
        self.scene = scene
        self.objs = scene.objects
        self.log = logger()
 
    def getBlocks(self, title, layer=1):
        blocks = ObjProperties().getPropObjGroup(title, self.scene, layer)
        return blocks
 
    def getStaticBlocks(self):
        return self.getBlocks('static_block')

    def getLogicalBlocks(self, layer=1):
        return self.getBlocks('logical_block', layer)

    def getVisualBlocks(self, layer=1):
        return self.getBlocks('visual_block', layer)
    
    def addVisualBlocks(self):
        '''
        This methods loads a visual_block, which is a puzzle block a player will
        see as they interact with the game. The visual blocks are added and parented to
        logical blocks that share the same block_number.
        '''

        logicalBlockObjs = self.getLogicalBlocks()
        inactvObjs = self.scene.objectsInactive
        
        for logicalBlockObj in logicalBlockObjs:
            obj = ObjProperties()
            logicalBlock = LogicalBlock(self.scene, logicalBlockObj)
            inactVsBlock = obj.getObjByPropVal(
                'visual_block', logicalBlock.blockID, inactvObjs
            )
            
            self.scene.addObject(inactVsBlock, logicalBlockObj, 0)
            actVsBlock = obj.getObjByPropVal(
                'visual_block', logicalBlock.blockID, self.scene.objects
            )
            actVsBlock.position = logicalBlockObj.position
            actVsBlock.setParent(logicalBlockObj, 0, 0)
            logicalBlock.setProp('_visual_block', str(actVsBlock))

    def refreshVsBlocks(self):
        vsBlocks = self.getVisualBlocks()
        lgBlocks = self.getLogicalBlocks()
        obj = ObjProperties()

        for vsBlock in vsBlocks:
            vsBlock.removeParent()
            lgBlock = obj.getObjByPropVal(
                'block_number', vsBlock['visual_block'],lgBlocks
            )
            vsBlock.position = lgBlock.position
            vsBlock.setParent(lgBlock, 0, 0)
            lgBlock['_visual_block'] = str(vsBlock)

    def removeVsBlocks(self):   
        vsblocks = self.getVisualBlocks() 
        for vsblock in vsblocks:
            vsblock.endObject()
    
    def addLogicalBlock(self, staticBlockObj):
        '''
        Add a logical block to a static block object position. 
        '''
        inactiveObjs = self.scene.objectsInactive
        logicalBlock = inactiveObjs['logical_block']
        logicalBlock['position_node'] = str(staticBlockObj)
        self.scene.addObject(logicalBlock, staticBlockObj, 0)
        # adjust the z axis abit lower so that objects raycast can detect the
        # static block better..
        staticBlockObj.position[2] = -0.1

    def addSpaceBlock(self, staticBlockObj):
        '''
        Adds a spaceblock to a static block position
        '''

        self.scene.addObject('space_block', staticBlockObj, 0)
        # adjust the z axis abit lower so that objects raycast can detect the
        # static block better..
        staticBlockObj.position[2] = -0.1
        self.log.debug('Space block has been added into the scene')
 
    def setStaticBlockNumbers(self, numberStructure, staticBlocks=[]):
        '''
        Assign static block numbers that will be used when matching logical_blocks 
        to static_blocks. The numbers assigned to static_blocks is
        based on the order and pattern in the numberStructure. 

        The method expects a number structure such as :
            {
                1 : [1, 2, 3, 4],
                2 : [5, 6, 7, 8],
                3 : [9, 10, 11, 12],
                4 : [13, 14, 15],
            }
        The dictionary key / index numbers represent static block rows. The list values of these
        index numbers represents the order in which numbers must be assigned to static blocks.. 

        Required static_block properties:
            @property row <int>
            @property index <int>
    
        In summary, the numberStructure represents the pattern in which the puzzle needs to be solved..
        '''

        self.log.debug('Using numberStructure %s to assign block_numbers to static blocks',
                         numberStructure)

        if not staticBlocks:
            staticBlocks = self.getStaticBlocks()
        
        for staticBlock in staticBlocks:
            staticBlocProp = ObjProperties(staticBlock)
            staticBlocIndex = staticBlocProp.getProp('index')
            staticBlocRow = staticBlocProp.getProp('row')

            if staticBlocRow in numberStructure:
                numStructRow = numberStructure[staticBlocRow]
                numStructIndexVal = numStructRow[staticBlocIndex]
                staticBlocProp.setProp('block_number', numStructIndexVal)
                self.log.debug('''
                    Static block %s has been assigned block_number %s 
                ''', staticBlock, numStructIndexVal)
            else:
                error = '''
                        Static obj %s's row %s not found in number structure!
                        ''', staticBlock, staticBlockRow
                self.log.error(error)
                raise PuzzleBlockLoaderError(error)

    def setLogicalBlockNumbers(self):
        '''
        Assigns random block_numbers to logical_blocks in the active scene.
        
        Note: By default, a logical block does not have a block_number
        '''

        logicalBlocks = self.getLogicalBlocks()
        lbCount = len(logicalBlocks)
        generatedNums = []

        for logicalBlock in logicalBlocks:
            lbProp = ObjProperties(logicalBlock)
            randomNum = 0
            
            # Skip random number 0 because blocks are counted from 1 to 15 
            # for example..
            while(randomNum in generatedNums or randomNum == 0):
                randomNum = randint(0, lbCount)
            
            generatedNums.append(randomNum)
            lbProp.setProp('block_number', randomNum)
            self.log.debug('%s assigned to logic_block', randomNum)

    def addLogicalBlocks(self):
        '''
        Adds logical blocks to the scene based on the available static_blocks. 
        The space object is assigned a random static block in this method 
        '''
        staticBlocks = self.getStaticBlocks()
        staticBlockCount = len(staticBlocks) -1 

        randNumber = randint(0, staticBlockCount)
        
        for index, staticBlock in enumerate(staticBlocks):
            if index == randNumber:
                self.addSpaceBlock(staticBlock)
            else:
                self.addLogicalBlock(staticBlock)

