from exception import ObjError

class ObjProperties:
    '''
    Games Properties utility class for retrieving, setting values and searching game
    obj properties.
    '''
    def __init__(self, obj=None):
        self.own = obj
    
    def getProp(self, propname, obj=None):
        '''
        Get value by property name

        @param: propname <string>
        @param: obj <scene object>

        @returns: <string> or None
        '''

        if obj is None:
            if self.own is None:
                raise ObjError('"None" not game object.')
            obj  = self.own

        if propname in obj:
            return obj[propname]
        
        return None
    
    def getObjByPropVal(self, propname, val, objs):
        '''
        Get object whose property has a certain value. A list of objects
        is required to be given in this method to pull this off.
        @param: propname <string>
        @param: val <string>
        @param: objs <object string>

        @returns: <scene object> or None
        '''

        for obj in objs:
            objVal = self.getProp(propname, obj)
            if objVal == val:
                return obj
        return None
    
    def setProp(self, propname, value, obj=None):
        '''
        Set a property's value through its property name

        @param: propname <string>
        @param: value <string>
        @param: obj <scene object>
        '''

        if obj is None:
            if self.own is None:
                raise ObjError('"None" not game object.')
            obj  = self.own
        
        if propname in obj:
            obj[propname] = value

    def getPropObjGroup(self, propname, scene, layer=1):
        '''
        Get a group of objects from a scene sharing the same property name.

        @param: propname <string>
        @param: scene <scene object>
        @param: layer <int> allowed values are 1(active layer) or 0(inactive layer)

        @returns: <obj list>
        '''

        assert layer == 0 or layer == 1 
        if layer == 1:
            objs = scene.objects
        else:
            objs = scene.objectsInactive
        
        objGroup = []
        
        for obj in objs:
            if propname in obj:
                objGroup.append(obj)

        return objGroup 
    
    def getObjGroupByPropVal(self, propname, val, scene, layer=1):
        assert layer == 0 or layer == 1 
        if layer == 1:
            objs = scene.objects
        else:
            objs = scene.objectsInactive
        
        objGroup = []
        
        for obj in objs:
            if propname in obj and obj[propname] == val:
                objGroup.append(obj)

        return objGroup 

