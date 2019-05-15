from bge import logic
from objproperties import ObjProperties
import textwrap

def onHover(controller):
    own = controller.owner
    hover = controller.sensors['hover']
    btnIcon = own.children[0]
    button = Button(own, logic)
    
    if hover.positive and own['is_enabled']:
        if button.isset():
            button.onhoverAction()  
            btnIcon.color = [0.638, 0.638, 0.638, 1.0]
    else:
        btnIcon.color = [1.0, 1.0, 1.0, 1.0]

def onClick(controller):
    gdict = logic.globalDict
    own = controller.owner
    hover = controller.sensors['hover']
    click = controller.sensors['click']
    button = Button(own, logic)

    if not button.isset():
        return

    if hover.positive and click.positive:
        button.onclickAction()

class Widget:
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

class Text(Widget):
    def __init__(self, txtObj, text=None, width=None, limit=None):
        super(Widget, self).__init__()
        Widget.__init__(self, txtObj)
        self.width = width
        self.limit = limit
        self.txtObj = txtObj
        self.text = text
        self.setText(text)
        self.properties = ObjProperties(txtObj)

    def setText(self, text):
        if not self.isEnabled:
            if self.limit and len(text) > self.limit:
                text = '%s...' % text[:self.limit]
            
            if self.width:
                text = textwrap.fill(width=self.width,text=text)

            self.properties.setProp('Text', text)
            self.text = text

    def tabSpaces(self, units):
        txtspace = '{:>%s}' % units
        txt = txtspace.format(self.text)
        self.setText(txt)

class Button(Widget):
    def __init__(self, widgetObj, logic):
        super(Button, self).__init__(widgetObj)
        self.globDict = logic.globalDict 
        self.widgetObj = widgetObj
        self.properties = ObjProperties(widgetObj)
        self.widgetID = self.properties.getProp('widget_id')
        self.btnIcon = widgetObj.children[0]

    def setOnclickAction(self, func, *args, **kwargs):
        self._setCommand('onclick', func, *args, **kwargs)

    def setOnhoverAction(self, func, *args, **kwargs):
        self._setCommand('onhover', func, *args, **kwargs)

    def onclickAction(self):
        return self._action('onclick')
    
    def onhoverAction(self):
        return self._action('onhover')

    def isset(self):
        return self.widgetID in self.globDict

    def _action(self, eventType):
        if not self.isEnabled:
            return
        
        widgetDifinition = self.globDict[self.widgetID]

        if eventType not in widgetDifinition:
            return

        action = widgetDifinition[eventType]
        return action()

    def _setCommand(self, eventType, func, *args, **kwargs):
         self.globDict[self.widgetID] = {}
         widget = self.globDict[self.widgetID]
         widget[eventType] = lambda: func(*args, **kwargs) 