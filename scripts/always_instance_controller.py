from bge import logic
from always_instance_global_data import AlwaysInstanceGlobalData
from logger import logger

log = logger()

def runAction(controller):
    own = controller.owner
    instanceData = AlwaysInstanceGlobalData(own['instance_id'])
    runnableAction = instanceData.getAction()
    try:
        # if action returns true, kill the Always instance
        if runnableAction():
            log.debug('Deleting always instance %s', instanceData.id)
            own.endObject()
            instanceData.deleteData()
    except Exception as error:
        log.debug('Always instance error %s', error)
        own.endObject()
        log.debug('Deleting always instance %s after exception', instanceData.id)
        instanceData.deleteData()
