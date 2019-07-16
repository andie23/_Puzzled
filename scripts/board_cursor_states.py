from session_global_data import SessionGlobalData

class BoardCursorStates(SessionGlobalData):
    def __init__(self):
        super(BoardCursorStates, self).__init__()
        if 'board_cursor_states' not in self.data:
            self.data['board_cursor_states'] = {
                'onClick': None,
                'onHover': None
            }
        self.states = self.data['board_cursor_states']

    def setOnHoverCursor(self, cursor):
        self.states['onHover'] = cursor        
    
    def setOnClickCursor(self, cursor):
        self.states['onClick'] = cursor

    def onHoverCursor(self):
        return self.states['onHover']

    def onClickCursor(self):
        return self.states['onClick']
