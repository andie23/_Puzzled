from global_dictionary import GlobDict

class CanvasGlobalData(GlobDict):
    def __init__(self, id):
        super(CanvasGlobalData, self).__init__('canvas_data')
        self._id = id
        if self._id not in self.data:
            self.data[self._id] = {}
        
        self.data = self.data[self._id]
        if not self.data:
            self.setDefaults()

    def getId(self):
        return str(self._id)
    
    def getScene(self):
        return self.data['scene']
    
    def getCanvasObj(self):
        return self.data['obj']
    
    def getNode(self):
        return self.data['node']

    def isEnabled(self):
        return self.data['is_enabled']
    
    def enable(self):
        self.data['is_enabled'] = True
    
    def disable(self):
        self.data['is_enabled'] = False

    def setDefaults(self):
        self.data['scene'] = ''
        self.data['obj'] = None
        self.data['node'] = None
        self.data['is_enabled'] = True

    def setScene(self, scene):
        self.data['scene'] = scene
    
    def setObj(self, obj):
        self.data['obj'] = obj
    
    def setNode(self, node):
        self.data['node'] = node
    
    def delete(self):
        del self.data
