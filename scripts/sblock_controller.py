from bge import logic
from session_global_data import SessionGlobalData
from block_listerners import OnDetectMovableBlocksListerner
from lblock import LogicalBlock

DIRECTION_MAP = {
    'y+': 'DOWN',
    'y-': 'UP',
    'x+': 'LEFT',
    'x-': 'RIGHT'
}

def detect(controller):
    session = SessionGlobalData()
    scene = logic.getCurrentScene()
    sensors = controller.sensors
    session.clearMovableBlocks()

    for sensor in sensors:
        axisname = str(sensor)
        if axisname not in DIRECTION_MAP:
            continue
        if sensor.positive:
            block = LogicalBlock(sensor.hitObject)
            session.setMovableBlock(
                str(block.blockID), 
                DIRECTION_MAP[axisname]
            )
    OnDetectMovableBlocksListerner().onDetect(session.getMovableBlocks())
