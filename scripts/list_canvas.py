from canvas import Canvas

class ListCanvas(Canvas):
    def __init__(self):
        super(ListCanvas, self).__init__(
            'list_canvas', 'list_canvas', 'CHALLENGES_MENU'
        )

    @property
    def pageNumTxtObj(self):
        return self._getWidget('txt_page_number')

    @property
    def titleTxtObj(self): 
        return self._getWidget('txt_title_ls')

    @property
    def nextBtnObj(self): 
        return self._getWidget('btn_next')
    
    @property
    def previousBtnObj(self): 
        return self._getWidget('btn_previous')