from objproperties import ObjProperties

class ChallengeCanvas():
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
        canvasProps.setProp('cname', cname)
        self.scene.addObject(canvas, posObj, 0)
        canvas =  canvasProps.getObjByPropVal(
            'cname', cname, self.scene.objects
        )
        widgets = canvas.children
        self.canvas = canvas
        self.canvasName = cname
    
        for widget in widgets:
            widgetName = str(widget)
            widgetID = '%s.%s' % (cname, widgetName)
            self.widgets[widgetID] = widget

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
        
    def setPlayBtn(self, func, **kwargs):
        self._setBtnCommand(
            '%s.btn_play' % self.canvasName, func, kwargs
        )
    
    def setPatternBtn(self, func, **kwargs):
        self._setBtnCommand(
            '%s.btn_pattern' % self.canvasName, func, kwargs
        )
    
    def _setBtnCommand(self, btnID, func, *args, **kwargs):
         if btnID not in self.widgets:
            return

         button = self.widgets[btnID]
         btnProps = ObjProperties(button)
         btnProps.setProp('btnID', btnID)
         
         # set callback function in global dictionary. Will be referenced later
         # when a button event occurs...         
         self.globDict[btnID] = { 'command' : func }

         if kwargs:
             self.globDict[btnID]['kwargs'] = kwargs   
