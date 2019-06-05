from bge import logic
from canvas_global_data import CanvasGlobalData

class Widget():
    def __init__(self, widget):
        self.widget = widget

    def isParentEnabled(self):
        parentCanvas = CanvasGlobalData(
            self.widget['parent_canvas_id']
        )
        return parentCanvas.isEnabled()

    def hide(self):
        self.widget.visible = False
    
    def show(self):
        self.widget.visible = True

    def isVisible(self):
        return self.widget.visible


