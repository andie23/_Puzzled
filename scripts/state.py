from puzzle import BlockProperties
from bge import logic
from logger import logger

MATCH_COLOR = [0.369, 0.625, 1.0, 1.0]
DEFAULT_COLOR = [1.0, 1.0, 1.0, 1.0]
COLOR_LESS = [0.0, 0.0, 0.0, 0.3]

SCENE = logic.getCurrentScene()
CONT = logic.getCurrentController()

CURRENT_LOGICBLOCK = BlockProperties(CONT.owner)
CURRENT_VISUALBLOCK = BlockProperties(
    CURRENT_LOGICBLOCK.getVisualBlockObj(SCENE)
)
BLOCKNUM =  CURRENT_LOGICBLOCK.getBlockNumber()

SET_DEFAULT_COL_CODE = 'DEFcol'
SET_MATCH_COL_CODE = 'MATcol' 
ACTIVATE_ALERT_MODE_CODE = 'ALEmod'
DISABLE_COL_CODE = 'DIScol'
DEACTIVATE_ALERT_MODE_CODE = 'DEALmod'

LOG = logger()

def setMsgSensorSubjects():
    '''
    Set subjects for all message sensors by building them with
    subject code and block number.

    '''
    LOG.debug('Assigning subject names to message sensors for block %s', BLOCKNUM)    
    sen = CONT.sensors
    blockNum = CURRENT_LOGICBLOCK.getBlockNumber()
    sen['set_default_col'].subject = buildSubj(SET_DEFAULT_COL_CODE, blockNum)
    sen['set_match_col'].subject = buildMsgSubj(SET_MATCH_COL_CODE, blockNum)
    sen['activate_alert_mode'].subject = buildMsgSubj(ACTIVATE_ALERT_MODE_CODE, blockNum)
    sen['disable_col'].subject = buildMsgSubj(DISABLE_COL_CODE, blockNum)
    sen['deactivate_alert_mode'].subject = buildMsgSubj(DEACTIVATE_ALERT_MODE_CODE, blockNum)

def buildMsgSubj(code, blockNum):
    '''
    Build message subject concantinating code and blocknumber seperated by "_"
    '''
    
    subj = '{0}_{1}'.format(code, blockNum)
    LOG.debug('Created subject: %s', subj)

    return subj
    
def animateVisualBloc(animationName, frameStart=0, frameEnd=20, speed):
    '''
    play visualblock animation
    '''
    
    LOG.debug('playing animation %s for blocknum: %s', animationName, BLOCKNUM)
    
    layer = 0 
    priority = 1
    blendin = 1.0
    mode = logic.KX_ACTION_MODE_LOOP
    layerWeight = 0.0
    ipoFlags = 1
    
    CURRENT_VISUALBLOCK.playAction(animationName, frameStart, frameEnd, layer, 
         priority, blendin, mode, layerWeight, ipoFlags, speed)

def isMsgRcvr(sensor, code):
    '''
    Checks if the message sensor is positive or
    a wildcard subject was passed
    '''
    return sensor.positive or buildMsgSubj(code, '*') in sensor.subjects

def visualBlockBlinkAnim():
    '''
    play blinking animation of visual block if alert mode is set
    '''
    
    if CURRENT_LOGICBLOCK.isInAlertMode():
        animName = 'visualBlockRedFlash'
        normalSpeed = CURRENT_LOGICBLOCK.getProp('blink_anim_normal_speed')
        fastSpeed = CURRENT_LOGICBLOCK.getProp('blink_anim_fast_speed')
        isAnimSpeedToggled = CURRENT_LOGICBLOCK.getProp('is_blink_anim_speed_toggled')        
        speed = normalSpeed

        if isAnimSpeedToggled:
            speed = fastSpeed
            LOG.debug('anim %s speed has been toggled to %s', animName, fastSpeed)
        
        animateVisualBloc(animationName=animName, speed=speed)
        
        if not alertModeSen.usePosPulseMode:
            # activate alert_mode loop
            alertModeSen.usePosPulseMode = True
            LOG.debug('PosPulsMode enabled')
    else:
        if alertModeSen.usePosPulseMode:
            # deactivate alert_mode loop
            alertModeSen.usePosPulseMode = False
            LOG.debug('PosPulsMode disabled')

def setDefaultCol():
    '''
    Set the color of the visual block to the DEFAULT_COLOR state if
    message subject prefix is equal to SET_DEFAULT_COL_SUBJ
    '''
    
    msgSen = CONT.sensors['set_default_col']
    
    if isMgsRcvr(msgSen, SET_DEFAULT_COL_CODE):
        CURRENT_VISUALBLOCK.setColor(DEFAULT_COLOR)
        LOG.debug('Default color set for block %s', BLOCKNUM)

  
def setMatchCol():
    '''
    Set the color of the visual block to the MATCH_COLOR state if
    message subject prefix is equal to SET_MATCH_COL_SUBJ
    ''' 
     
    msgSen = CONT.sensors['set_match_col']
   
    if isMgsRcvr(msgSen, SET_MATCH_COL_CODE):
        CURRENT_VISUALBLOCK.setColor(MATCH_COLOR)
        LOG.debug('Match color set for block %s', BLOCKNUM)
        
def disableCol():
    '''
    Set the color of the visual block to COLOR_LESS state if
    message subject prefix is equal to DISABLE_COL_MSG_CODE
    '''
      
    msgSen = CONT.sensors['disable_col']
    
    if isMgsRcvr(msgSen, DISABLE_COL_CODE):
        CURRENT_VISUALBLOCK.setColor(COLOR_LESS)
        LOG.debug('Colorless color set for block %s', BLOCKNUM)


def activateAlertMode():
    '''
    Activate alert mode of the visual block to the ALERT MODE state if
    message subject prefix is equal to SET_DEFAULT_COL_SUBJ
    '''

    msgSen = CONT.sensors['activate_alert_mode']
    alertModeSen = CONT.sensors['alert_mode']
    
    if isMgsRcvr(msgSen, ACTIVATE_ALERT_MODE_CODE):
        CURRENT_LOGICALBLOCK.activateAlertMode()
        LOG.debug('Alert mode has been triggered for blocknum: %s', BLOCKNUM)

def deactivateAlertMode():
    '''
    Deactivate alert mode of the visual block to the default state if
    message subject prefix is equal to SET_DEFAULT_COL_SUBJ
    '''
    
    msgSen = CONT.sensors['deactivate_alert_mode']
    alertModeSen = CONT.sensors['alert_mode']

    if isMgsRcvr(msgSen, DEACTIVATE_ALERT_MODE_CODE):
        CURRENT_LOGICALBLOCK.deactivateAlertMode()
        LOG.debug('Alert mode has been disabled for blocknum: %s', BLOCKNUM)
    