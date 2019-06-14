from canvas import Canvas

class ChallengeViewerCanvas(Canvas):
    def __init__(self):
        super(ChallengeViewerCanvas, self).__init__(
            'challenge_view_canvas', 'challenge_view_canvas', 'HUD'
        )

    @property
    def exitBtnObj(self):
        return self._getWidget('btn_challenge_exit')
    
    @property
    def streakCountTxtObj(self):
        return self._getWidget('txt_benchmark_streaks')
    
    @property
    def timeTxtObj(self):
        return self._getWidget('txt_benchmark_time')
   
    @property
    def movesTxtObj(self):
        return self._getWidget('txt_benchmark_moves')

    @property
    def playBtnObj(self):
        return self._getWidget('btn_challenge_launcher')

    @property
    def titleTxtObj(self):
        return self._getWidget('txt_challenge_title')

    @property
    def playTimeTxtObj(self):
        return self._getWidget('txt_playtime_stats')    

    @property
    def playCountTxtObj(self):
        return self._getWidget('txt_playcount_stats')
    
    @property
    def losesTxtObj(self):
        return self._getWidget('txt_loses_stats')

    @property
    def winsTxtObj(self):
        return self._getWidget('txt_win_stats')
