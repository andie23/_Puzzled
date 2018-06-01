#########################################################
# Author: Andrew Mfune
# Date: 22/05/2018
# Description: Contains class modules for puzzle blocks
#########################################################
from objproperties import ObjProperties
from random import randint
from logger import logger
from exception import PuzzleLoaderError

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

    def getStaticBlocks(self):
        props = ObjProperties()
        staticBlocks = props.getPropObjGroup('static_block', self.scene, 1)
        return staticBlocks

    def getLogicalBlocks(self, layer=1):
        props = ObjProperties()
        logicalBlocks = props.getPropObjGroup('logical_block', self.scene, layer)
        return logicalBlocks

    def getVisualBlocks(self):
        props = ObjProperties()
        visualBlocks = props.getPropObjGroup('visual_block', self.scene, 0)
        return visualBlocks
    
    def addVisualBlocks(self):
        '''
        This methods loads a visual_block, which is a puzzle block a player will
        see as they interact with the game. The visual blocks are added and parented to
        logical blocks that share the same block_number.
        '''

        logicalBlocks = self.getLogicalBlocks()
        visualBlocks = self.getVisualBlocks()
        
        for logicalBlock in logicalBlocks:
            objProp = ObjProperties()
            logicalBlockProp = ObjProperties(logicalBlock)
            logicalBlockNum = logicalBlockProp.getProp('block_number')
            visualBlock = objProp.getObjByPropVal(
                'block_number', logicalBlockNum, visualBlocks
            )

            self.scene.addObject(visualBlock, logicalBlock, 0)
            self.scene.objects[str(visualBlock)].setParent(logicalBlock, 0, 0)
            logicalBlockProp.setProp('_visual_block', visualBlock)
            visualBlock.position = logicalBlock.position
            self.log.debug(' Assigned visual block %s to logical block %s', 
                            visualBlock, logicalBlock)
                
    def addLogicalBlock(self, staticBlockObj):
        '''
        Add a logical block to a static block object position. 
        '''
        self.scene.addObject('logical_block', staticBlockObj, 0)
        # adjust the z axis abit lower so that objects raycast can detect the
        # static block better..
        staticBlockObj.position[2] = -0.1
        self.log.debug('static_block %s has been assigned a logic block',
                         staticBlockObj)

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
         

class BlockProperties(ObjProperties):
    def __init__(self, blockObj):
        super(ObjProperties, self).__init__()
        self.own = blockObj
    
    def getVisualBlockObj(self, scene):
        visualBlockName = self.getProp('_visual_block')
        return scene.objects[str(visualBlockName)]

    def getCurrentStaticBlock():
        return self.getProp('current_static_block')

    def getGroupName(self):
        return self.getProp('group_name')

    def getBlockMoveSpeed(self):
        return self.getProp('block_move_speed')
    
    def getBlockNumber(self):
        return self.getProp('block_number')

    def isMatchingStaticBlock(self):
        return self.getProp('is_matching_static_block')
    
    def wasMatchingStaticBlock(self):
        return self.getProp('was_matching_static_block')
    
    def isMoving(self):
        return self.getProp('is_moving')
    
    def isInAlertMode(self):
        return self.getProp('is_in_alert_mode')
    
    def setColor(self, color):
        self.own.color = color
    
    def setAlertMode(self, bool):
        self.setProp('is_in_alert_mode', bool)
    
    def setMovementSpeed(self, speed):
        self.setProp('block_move_speed', speed)

    def setIsMoving(self, boolVal):
        self.setProp('is_moving', boolVal)

    def setExpiry(self, boolVal):
        self.setProp('is_expired', boolVal)

class SpaceBlock(ObjProperties):
    def __init__(self, spaceBlock):
        super(ObjProperties, self).__init__()
        self.own = spaceBlock

    def isLocked(self):
        return self.getProp('is_locked', self.own)
    
    def unLock(self):
        self.setProp('is_locked', False, self.own)
    
    def lock(self):
        self.setProp('is_locked', True, self.own)
    

class PuzzleBlockLogic(BlockProperties):
    def __init__(self, controller):
        super(BlockProperties, self).__init__()
        self.cont = controller 
        self.own = controller.owner
        self.log = logger()

    def getMotionLoc(self, spaceDirection):
        xAxis = 0
        yAxis = 1
        motionLoc = [0.0, 0.0, 0.0]
        speed = self.getBlockMoveSpeed()
  
        if spaceDirection == 'UP':
            motionLoc[yAxis] = speed
        
        elif spaceDirection == 'DOWN':
            motionLoc[yAxis] = -speed
            
        elif spaceDirection == 'RIGHT':
            motionLoc[xAxis] = speed
        
        elif spaceDirection == 'LEFT':
            motionLoc[xAxis] = -speed
        
        return motionLoc

    def move(self, motionLoc):
        self.own.applyMovement(motionLoc)

    def getActiveDirectionalKey(self, directionEventMap):
        '''
        directionEventMap
        {
            'UP': keyVal,
            'DOWN': keyVal,
            'LEFT': keyVal,
            'RIGHT': keyVal
        }
        '''

        spaceDirection = self.getSpaceBlockDirection()

        if spaceDirection in directionEventMap:
            return directionEventMap[spaceDirection]
        return None
    
    def snapToObj(self, obj):
        self.own.position[0] = obj.position[0]
        self.own.position[1] = obj.position[1]
    
    def getCurrentStaticBlock(self):
        staticBlockSen = self.getStaticBlockSensor()

        if staticBlockSen.positive:
            return staticBlockSen.hitObject
        return None

    def getStaticBlockSensor(self):
        return self.cont.sensors['z_static_block_sensor']

    def getSpaceBlockSensors(self):
        x = self.cont.sensors['x_space_bloc_sensor']
        xn = self.cont.sensors['xn_space_bloc_sensor']
        y = self.cont.sensors['y_space_bloc_sensor']
        yn = self.cont.sensors['yn_space_bloc_sensor']

        return {'UP' : y, 'DOWN' : yn, 'LEFT' : xn, 'RIGHT' : x}

        
    def getSpaceBlockDirection(self):
        directionalSensors = self.getSpaceBlockSensors()

        for directionName, spaceSensor in directionalSensors.items():
            if spaceSensor.positive:
               # self.log.debug('Block %s facing space object on %s',
               #                self.own, directionName)
               return directionName
        return None

    def matchBlockNumToStaticNum(self):
        currentStaticBlock = self.getCurrentStaticBlock()
        if currentStaticBlock:
            staticBlockNumber = self.getProp('block_number', currentStaticBlock)
            blockNumber = self.getBlockNumber()
            isMatchingStaticBlock = staticBlockNumber == blockNumber
 
            if not isMatchingStaticBlock:
                if self.getProp('is_matching_static_block'):
                    self.setProp('was_matching_static_block', True)        

            self.setProp(
                'is_matching_static_block', 
                 isMatchingStaticBlock
            )
           