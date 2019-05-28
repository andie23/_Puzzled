from canvas import Canvas

class HudCanvas(Canvas):
    def __init__(self, sceneId='HUD'):
        super(HudCanvas, self).__init__(
            'hud_canvas', 'hud_canvas', sceneId
        )

    @property
    def pauseBtnObj(self):
        return self._getWidget('btn_hud_pause')
    
    @property
    def reshuffleBtnObj(self):
        return self._getWidget('btn_hud_reshuffle_puzzle')
    
    @property
    def homeBtnObj(self):
        return self._getWidget('btn_hud_challenges_menu')
    
    @property
    def patternBtnObj(self):
        return self._getWidget('btn_hud_pattern_view')

    @property
    def titleTxtObj(self):
        return self._getWidget('txt_hud_title')
    
    @property
    def clockTxtObj(self):
        return self._getWidget('txt_hud_clock')


    @property
    def movesTxtObj(self):
        return self._getWidget('txt_hud_moves')
