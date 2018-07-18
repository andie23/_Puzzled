from objproperties import ObjProperties

class ButtonWidget:
    def __init__(self, btnObj, logic):
        self.btnObj = btnObj
        self.globDict = logic.globalDict
        self.btnID = 'WorldCanvas.%s' % str(btnObj)
 
    def setCommand(self, func, *args, **kwargs):
         btnProps = ObjProperties(self.btnObj)
         btnProps.setProp('btnID', self.btnID)
         self.globDict[self.btnID] = { 
            'command' : lambda: func(*args, **kwargs) 
         }

class ChallengeCanvas():
    BLUE = [0.369, 0.625, 1.0, 1.0]
    RED =  [1.0, 0.083, 0.098, 1.0]
    
    def __init__(self, logic):
        self.scene = logic.getCurrentScene()
        self.inactiveObjs = self.scene.objectsInactive
        self.globDict = logic.globalDict
        self.widgets = {}
        self.canvas = None
        self.canvasName = None

    def add(self, cname, posObj):
        canvas = self.inactiveObjs['canvas']
        canvasProps = ObjProperties(canvas)
        canvasProps.setProp('canvasID', cname)
        self.scene.addObject(canvas, posObj, 0)
        canvas =  canvasProps.getObjByPropVal(
            'canvasID', cname, self.scene.objects
        )
        widgets = canvas.children
        self.canvas = canvas
        self.canvasName = '%s' % cname
    
        for widget in widgets:
            widgetName = str(widget)
            widgetID = '%s.%s' % (cname, widgetName)
            self.widgets[widgetID] = widget
    
    def setColor(self, color):
        self.canvas.color = color

    def remove(self):
        self.canvas.endObject()

    def setTitleTxt(self, txt):
        widgetID = '%s.txt_title' % self.canvasName
        self._setTxt(widgetID, txt)

    def setTimeTxt(self, txt):
        widgetID = '%s.txt_time' % self.canvasName
        self._setTxt(widgetID, txt)    
    
    def setMovesTxt(self, txt):
        widgetID = '%s.txt_moves' % self.canvasName
        self._setTxt(widgetID, txt)

    def _setTxt(self, txtID, val):
        if txtID not in self.widgets:
            return

        txtWidget = self.widgets[txtID]
        prop = ObjProperties(txtWidget)
        prop.setProp('Text', val)
        
    def setPlayBtn(self, func, *args, **kwargs):
        self._setBtnCommand(
            '%s.btn_play' % self.canvasName, func, *args, **kwargs
        )
    
    def setPatternBtn(self, func, *args, **kwargs):
        self._setBtnCommand(
            '%s.btn_pattern' % self.canvasName, func, *args, **kwargs
        )
    
    def _setBtnCommand(self, btnID, func, *args, **kwargs):
         if btnID not in self.widgets:
            return

         button = self.widgets[btnID]
         btnProps = ObjProperties(button)
         btnProps.setProp('btnID', btnID)
         self.globDict[btnID] = { 
            'command' : lambda: func(*args, **kwargs) 
         }
