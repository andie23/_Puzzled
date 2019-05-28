from canvas import Canvas

class PuzzledDialogCanvas(Canvas):
    def __init__(self, sceneID=None):
        super(PuzzledDialogCanvas, self).__init__(
            'puzzled_dialog_canvas', 'puzzled_dialog_canvas', sceneID
        )

    @property
    def subtitleTxtObj(self):
        return self._getWidget('txt_puzzled_dialog_subtext')
    
    @property
    def titleTxtObj(self):
        return self._getWidget('txt_puzzled_dialog_title')
    
    @property
    def homeBtnObj(self):
        return self._getWidget('btn_puzzled_dialog_home')
    
    @property
    def shuffleBtnObj(self):
        return self._getWidget('btn_puzzled_dialog_reshuffle')
