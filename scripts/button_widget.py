from bge import logic
from button_global_data import ButtonGlobalData
from widgets import Widget

class Button(ButtonGlobalData):
    def __init__(self, buttonObj):
        super(Button, self).__init__(buttonObj['widget_id'])
        self.buttonObj = buttonObj
        self.btnIcon = self.buttonObj.children[0]
        self.widget = Widget(buttonObj)

    def toggleBtn(self, anotherBtn, anotherBtnToggleAction, ownToggleAction):
        '''
        Swap between buttons continously when clicked on and run their 
        defined actions
        '''

        anotherBtn.setOnclickAction(
            lambda: self._toggle(anotherBtnToggleAction, anotherBtn, self)
        )

        self.setOnclickAction(
            lambda: self._toggle(ownToggleAction, self, anotherBtn)
        )

    def _toggle(self, toggleAction, inactiveBtn, activeBtn):
        '''
        Switches active button into camera view and inactive button
        into off camera view and runs toggle action
        '''

        from copy import deepcopy
        onscreenPosition = deepcopy(inactiveBtn.buttonObj.worldPosition)
        offscreenPosition = deepcopy(activeBtn.buttonObj.worldPosition)
        
        activeBtn.buttonObj.worldPosition = onscreenPosition 
        inactiveBtn.buttonObj.worldPosition = offscreenPosition
        
        toggleAction()

    def isButtonEnabled(self):
        return self.widget.isParentEnabled() and self.isEnabled()

    def hide(self):
        self._setIconVisibility(False)

    def show(self):
        self._setIconVisibility(True)

    def applyHoverColor(self):
        self._setBtnColor(self.getOnhoverColor())

    def applyDefaultColor(self):
        self._setBtnColor(self.getDefaultColor())
 
    def runOnHoverAction(self):
        return self._runAction(self.getOnhoverAction())
        
    def runOnClickAction(self):
        return self._runAction(self.getOnclickAction())

    def _setIconVisibility(self, bool):
        self.btnIcon.visible = bool

    def _setBtnColor(self, color):
        if self.widget.isParentEnabled() and self.isEnabled():
            self.btnIcon.color = color
    
    def _runAction(self, action):
        if self.widget.isParentEnabled() and self.isEnabled():
            return action()