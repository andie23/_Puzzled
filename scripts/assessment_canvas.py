from canvas import Canvas

class AssessmentCanvas(Canvas):
    def __init__(self):
        super(AssessmentCanvas, self).__init__(
            'assessment_canvas', 'assessment_canvas', 'HUD'
        )

    @property
    def titleTxtObj(self):
        return self._getWidget('txt_assessment_title')
    
    @property
    def reshuffleBtnObj(self):
        return self._getWidget('btn_assessment_reshuffle')
    
    @property
    def exitBtnObj(self):
        return self._getWidget('btn_assessment_exit')

    @property
    def currentTimeTxtObj(self):
        return self._getWidget('txt_current_time')
    
    @property
    def currentStreakTxtObj(self):
        return self._getWidget('txt_current_streak')
    
    @property
    def streakAssessmentTxtObj(self):
        return self._getWidget('txt_streak_assessment')
    
    @property
    def currentMovesTxtObj(self):
        return self._getWidget('txt_current_moves')
   
    @property
    def previousStreakTxtObj(self):
        return self._getWidget('txt_previous_streak')
   
    @property
    def previousMovesTxtObj(self):
        return self._getWidget('txt_previous_moves')
   
    @property
    def previousTimeTxtObj(self):
        return self._getWidget('txt_previous_time')
    
    @property
    def timeAssessmentTxtObj(self):
        return self._getWidget('txt_time_assessment')
    
    @property
    def movesAssessmentTxtObj(self):
        return self._getWidget('txt_moves_assessment')

    @property
    def overrallAssessmentTxtObj(self):
        return self._getWidget('txt_overall_assessment')
    
    @property
    def statusTxtObj(self):
        return self._getWidget('txt_benchmark_status')
