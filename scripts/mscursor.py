from objproperties import ObjProperties
from global_dictionary import GlobDict
from scene_helper import Scene

ARROW_POINTER = 'arrow_pointer'
HAND_POINTER = 'hand_pointer'
FIST_POINTER = 'fist_pointer'

class CursorGlobalData(GlobDict):
    def __init__(self):
        super(CursorGlobalData, self).__init__('mouse_cursor_data')
        if not self.data:
            self.setDefaults()
    
    def getActiveCursor(self):
        return self.data['active_cursor']
    
    def getDefaultCursor(self):
        return self.data['default_cursor']

    def setDefault(self, cursor):
        self.data['default_cursor'] = cursor
    
    def setActiveCursor(self, cursor):
        self.data['active_cursor'] = cursor
    
    def setDefaults(self):
        self.data['default_cursor'] = None
        self.data['active_cursor'] = None

class Cursor(CursorGlobalData):
    def __init__(self, cursor):
        super(Cursor, self).__init__()
        self.cursor = cursor

    def use(self):
        activeCursor = self.getActiveCursor()
        if activeCursor:
            self.hide(activeCursor)
        
        self.setActiveCursor(self.cursor)
        self.show()
    
    def setAsDefault(self):
        self.setDefault(self.cursor) 
    
    def hide(self, cursor=None):
        cur = self.cursor if not cursor else cursor
        self._setvisibility(cur, False)
    
    def show(self, cursor=None):
        cur = self.cursor if not cursor else cursor
        self._setvisibility(cur, True)

    def getCursorObj(self, cursor=None):
        cur = self.cursor if not cursor else cursor        
        return Scene('HUD').getscene().objects[cur]

    def setWorldScale(self, scale):
        self.getCursorObj().worldScale = scale

    def _setvisibility(self, cursor, bool):
        self.getCursorObj(cursor).visible = bool
