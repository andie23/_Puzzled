from canvas import Canvas

class InitialAssessmentCanvas(Canvas):
    def __init__(self):
        super(InitialAssessmentCanvas, self).__init__(
            'initial_assessment_canvas', 'initial_assessment_canvas', 'ASSESSMENT'
        )

    @property
    def titleTxtObj(self):
        return self._getWidget('txt_initial_title')

    @property
    def reshuffleBtnObj(self):
        return self._getWidget('btn_initial_reshuffle')
    
    @property
    def exitBtnObj(self):
        return self._getWidget('btn_initial_exit')

    @property
    def currentTimeTxtObj(self):
        return self._getWidget('txt_initial_time')

    @property
    def currentMovesTxtObj(self):
        return self._getWidget('txt_initial_moves')

    @property
    def currentStreakTxtObj(self):
        return self._getWidget('txt_initial_streak')
