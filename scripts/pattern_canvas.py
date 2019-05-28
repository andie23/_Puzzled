from canvas import Canvas

class PatternCanvas(Canvas):
    def __init__(self):
        super(PatternCanvas, self).__init__(
            'pattern_canvas', 'pattern_canvas', 'PATTERN_VIEW'
        )

    @property
    def backBtnObj(self):
        return self._getWidget('btn_pattern_back')
    
    @property
    def prevStreakTxtObj(self):
        return self._getWidget('txt_vs_prev_streak')
    
    @property
    def prevTimeTxtObj(self):
        return self._getWidget('txt_vs_prev_time')
   
    @property
    def prevMovesTxtObj(self):
        return self._getWidget('txt_vs_prev_moves')

    @property
    def playBtnObj(self):
        return self._getWidget('btn_pattern_play')

    @property
    def titleTxtObj(self):
        return self._getWidget('txt_pattern_title')

    @property
    def playTimeTxtObj(self):
        return self._getWidget('txt_pattern_play_time')    

    @property
    def playCountTxtObj(self):
        return self._getWidget('txt_pattern_play_count')
    
    @property
    def losesTxtObj(self):
        return self._getWidget('txt_pattern_loses')

    @property
    def winsTxtObj(self):
        return self._getWidget('txt_pattern_wins')
