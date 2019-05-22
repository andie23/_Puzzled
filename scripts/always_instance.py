from always_instance_global_data import AlwaysInstanceGlobalData
from objproperties import ObjProperties

class AlwaysInstance(AlwaysInstanceGlobalData):
    '''
    Creates an object instance in the scene that runs 
    specified actions continously
    '''

    def __init__(self, id, scene):
        super(AlwaysInstance, self).__init__(id)
        self.scene = scene

    def addInstance(self, action):
        '''
        Add object in the scene with an always 
        sensor(with PosPulse mode == True) set in logic bricks
        '''

        if self.getInstance():
            return

        instance = ObjProperties().getPropObjGroup(
            'always_instance', self.scene, 0
        )[0]
        instance['instance_id'] = self.id
        self.scene.addObject(instance)
        self.setAction(action)
    
    def getInstance(self):
        instance = ObjProperties().getObjByPropVal(
            'instance_id', self.getId(), self.scene.objects
        )
        return instance

    def removeInstance(self):
        instance = self.getInstance()
        if instance:
            instance.endObject()
            self.deleteData()
    
