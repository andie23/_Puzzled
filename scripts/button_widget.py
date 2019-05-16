from bge import logic
from button_global_data import ButtonGlobalData

class Button(ButtonGlobalData):
    def __init__(self, buttonObj):
        super(Button, self).__init__(buttonObj['widget_id'])
        self.buttonObj = buttonObj
        self.btnIcon = self.buttonObj.children[0]

    def applyHoverColor(self):
        self.btnIcon.color = self.getOnhoverColor()

    def applyDefaultColor(self):
        self.btnIcon.color = self.getDefaultColor()
 
    def runOnHoverAction(self):
        onhoverAction = self.getOnhoverAction()
        return onhoverAction()

    def runOnClickAction(self):
        onClickAction = self.getOnclickAction()
        return onClickAction()
