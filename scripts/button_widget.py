from bge import logic
from button_global_data import ButtonGlobalData
from widgets import Widget

class Button(ButtonGlobalData):
    def __init__(self, buttonObj):
        super(Button, self).__init__(buttonObj['widget_id'])
        self.buttonObj = buttonObj
        self.btnIcon = self.buttonObj.children[0]
        self.widget = Widget(buttonObj)

    def isButtonEnabled(self):
        return self.widget.isParentEnabled() and self.isEnabled()

    def hide(self):
        self.widget.hide()

    def show(self):
        self.widget.show()
    
    def _setBtnColor(self, color):
        if self.widget.isParentEnabled() and self.isEnabled():
            self.btnIcon.color = color
    
    def _runAction(self, action):
        if self.widget.isParentEnabled() and self.isEnabled():
            return action()

    def applyHoverColor(self):
        self._setBtnColor(self.getOnhoverColor())

    def applyDefaultColor(self):
        self._setBtnColor(self.getDefaultColor())
 
    def runOnHoverAction(self):
        return self._runAction(self.getOnhoverAction())
        
    def runOnClickAction(self):
        return self._runAction(self.getOnclickAction())
