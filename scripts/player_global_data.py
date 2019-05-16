from global_dictionary import GlobDict
PLAYER_DATA =  { 'id' : '', 'name' : ''}

class PlayerGlobalData(GlobDict):
    def __init__(self):
        super(PlayerGlobalData, self).__init__('player_data')
        if not self.data:
            self.setDefaults()

    def setDefaults(self):
        self.data['id'] = ''
        self.data['name'] = ''

    def getId(self):
        return self.data['id']
 
    def getName(self):
        return self.data['name']
    
    def setId(self, id):
        self.data['id'] = id
    
    def setName(self, name):
        self.data['name'] = name