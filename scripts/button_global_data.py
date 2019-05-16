from bge import logic
from global_dictionary import GlobDict

class ButtonGlobalData(GlobDict):
    def __init__(self, buttonId):
        super(ButtonGlobalData, self).__init__('button_data')
        self.buttonId = buttonId
        
        if not self.isset():
            self.data[buttonId] = {}

        self.data = self.data[buttonId]

        if not self.data:
            self.setDefaults()
    
    def setDefaults(self):
        self.data['onclick_action'] = lambda:()
        self.data['onhover_action'] = lambda:()
        self.data['onhover_color'] = [0.638, 0.638, 0.638, 1.0]
        self.data['onclick_sound'] = ''
        self.data['onhover_sound'] = ''
        self.data['default_color'] = [1.0, 1.0, 1.0, 1.0]
        self.data['is_enabled'] = True

    def isset(self):
        return self.buttonId in self.data
    
    def isEnabled(self):
        return self.data['is_enabled']

    def getOnhoverColor(self):
        return self.data['onhover_color']

    def getOnclickAction(self):
        return self.data['onclick_action']
    
    def getOnhoverAction(self):
        return self.data['onhover_action']

    def getOnclickSound(self):
        return self.data['onclick_sound']
    
    def getOnhoverSound(self):
        return self.data['onhover_sound']
    
    def getDefaultColor(self):
        return self.data['default_color']
    
    def setOnclickAction(self, action):
        self.data['onclick_action'] = action
    
    def setOnhoverAction(self, action):
        self.data['onhover_action'] = action
    
    def setOnclickSound(self, sound):
        self.data['onclick_sound'] = sound
    
    def setOnhoverSound(self, sound):
        self.data['onhover_sound'] = sound

    def setOnhoverColor(self, color):
        self.data['onhover_color'] = color

    def enable(self):
        self.data['is_enabled'] = True
    
    def disable(self):
        self.data['is_enabled'] = False
