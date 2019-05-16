from bge import logic
from objproperties import ObjProperties

class Widget():
    def __init__(self, widget):
        self.widget = widget
        self.properties = ObjProperties(widget)
        self.isEnabled = self.properties.getProp('is_enabled')

    def enable(self, isEnabled=False):
        self.properties.setProp('is_enabled', isEnabled)

    def setColor(self, color):
        self.widget.color = color

    def hide(self):
        self.widget.visible = False
    
    def show(self):
        self.widget.visible = True

    def isVisible(self):
        return self.widget.visible


