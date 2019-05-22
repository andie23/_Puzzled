from global_dictionary import GlobDict

class AlwaysInstanceGlobalData(GlobDict):
    def __init__(self, id):
        super(AlwaysInstanceGlobalData, self).__init__('always_instances')
        self.id = id
        
        if self.id not in self.data:
            self.data[self.id] = {}

        self.data = self.data[self.id]
        
        if not self.data:
            self.setDefaults()

    def getAction(self):
        return self.data['action']

    def getId(self):
        return self.data['id']

    def setAction(self, action):
        self.data['action'] = action
    
    def setDefaults(self):
        self.data['id'] = ''
        self.data['action'] = ''
    
    def deleteData(self):
        del self.data
