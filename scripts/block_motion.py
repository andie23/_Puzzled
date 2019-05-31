from objproperties import ObjProperties

class BlockMotion(ObjProperties):
    def __init__(self, blockObj):
        super(BlockMotion, self).__init__(blockObj)

    def getMotionLoc(self, direction):
        xAxis = 0
        yAxis = 1
        motionLoc = [0.0, 0.0, 0.0]
        speed = self.getProp('speed')
  
        if direction == 'UP':
            motionLoc[yAxis] = speed
        
        elif direction == 'DOWN':
            motionLoc[yAxis] = -speed
            
        elif direction == 'RIGHT':
            motionLoc[xAxis] = speed
        
        elif direction == 'LEFT':
            motionLoc[xAxis] = -speed
        
        return motionLoc

    def enableMovement(self):
        self.setProp('is_moving', True)

    def suspendMovement(self):
        self.setProp('is_moving', False)
        
    @property
    def speed(self):
        return self.getProp('speed')

    @property
    def isInMotion(self):
        return self.getProp('is_moving')
    
    def start(self, direction):
        self.setProp('movable_direction', direction)
        self.enableMovement()

    def slide(self, direction=''):
        if not direction:
            direction = self.getProp('movable_direction')
        motionLoc = self.getMotionLoc(direction)
        self.applyMotionLoc(motionLoc)

    def applyMotionLoc(self, motionLoc):
        self.own.applyMovement(motionLoc)

    def snapToObj(self, obj):
        self.own.position[0] = obj.position[0]
        self.own.position[1] = obj.position[1]
        self.setProp('position_node', str(obj))
        self.setProp('movable_direction', '')
