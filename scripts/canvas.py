from objproperties import ObjProperties

class Canvas:
    def __init__(self, canvasObjName, logic, sceneID=None):
        if sceneID:
            self.scene = logic.getSceneList()[sceneID]
        else:
            self.scene = logic.getCurrentScene()
        self._canvasObjName = canvasObjName
        self.globDict = logic.globalDict
        self.inactiveObjs = self.scene.objectsInactive
        self.canvasID = None
        self.widgets = None
        self.canvasObj = None

    def load(self, canvasID):
        self.canvasID = canvasID
        self.canvasObj = self.scene.objects[self._canvasObjName]
        self.widgets = self._getWidgets()
    
    def add(self, canvasID, positionNode):
        self.canvasID = canvasID  
        self.canvasObj = self._loadCanvas(positionNode)
        self.widgets = self._getWidgets()

    def setColor(self, color, applyToChildren=False):
        self.canvasObj.color = color

        if applyToChildren:
            for name, widget in self.widgets.items():
                widget.color = color

    def remove(self):
        self.canvas.endObject()

    def _loadCanvas(self, positionNode):
        inactiveCanvas = self.inactiveObjs[self._canvasObjName]
        canvasProps = ObjProperties(inactiveCanvas)
        canvasProps.setProp('canvas_id', self.canvasID)
        self.scene.addObject(inactiveCanvas, positionNode, 0)
        activeCanvas =  canvasProps.getObjByPropVal(
            'canvas_id', self.canvasID, self.scene.objects
        )

        return activeCanvas
    
    def _getWidget(self, widgetObjName):
        name = '%s.%s' % (self.canvasID, widgetObjName)
        return self.widgets[name]

    def _getWidgets(self):
        widgetList = self.canvasObj.children
        keyedWidgets = {}
        for widget in widgetList:
            name = str(widget)
            widgetProp = ObjProperties(widget)
            widgetID = '%s.%s' % (self.canvasID, name)
            keyedWidgets[widgetID] = widget
            widgetProp.setProp('widget_id', widgetID)
        return keyedWidgets

class HudCanvas(Canvas):
    def __init__(self, logic, sceneID=None):
        super(Canvas, self).__init__()
        Canvas.__init__(self, 'hud_canvas', logic, sceneID)
        self.Obj = ObjProperties()

    @property
    def titleTxtObj(self):
        return self._getWidget('txt_hud_title')
    
    @property
    def clockTxtObj(self):
        return self._getWidget('txt_hud_clock')
    
    @property
    def prevTimeTxtObj(self):
        return self._getWidget('txt_hud_prev_time')

    @property
    def movesTxtObj(self):
        return self._getWidget('txt_hud_moves')

    @property
    def prevMovesTxtObj(self):
        return self._getWidget('txt_hud_prev_moves')
    
class AssessmentCanvas(Canvas):
    def __init__(self, logic):
        super(Canvas, self).__init__()
        Canvas.__init__(self, 'assessment_canvas', logic)
        self.scene = logic.getCurrentScene()
        self.Obj = ObjProperties()
    
    @property
    def titleTxtObj(self):
        return self._getWidget('txt_assessment_title')

    @property
    def currentTimeTxtObj(self):
        return self._getWidget('txt_current_time')
    
    @property
    def currentMovesTxtObj(self):
        return self._getWidget('txt_current_moves')
    
    @property
    def previousMovesTxtObj(self):
        return self._getWidget('txt_previous_moves')
   
    @property
    def previousTimeTxtObj(self):
        return self._getWidget('txt_previous_time')
    
    @property
    def timeAssessmentTxtObj(self):
        return self._getWidget('txt_time_assessment')
    
    @property
    def movesAssessmentTxtObj(self):
        return self._getWidget('txt_moves_assessment')

    @property
    def overrallAssessmentTxtObj(self):
        return self._getWidget('txt_overall_assessment')
    
    @property
    def statusTxtObj(self):
        return self._getWidget('txt_benchmark_status')

class ListCanvas(Canvas):
    def __init__(self, logic):
        super(Canvas, self).__init__()
        Canvas.__init__(self, 'list_canvas', logic)
        self.scene = logic.getCurrentScene()
        self.Obj = ObjProperties()

    @property
    def titleTxtObj(self): 
        return self._getWidget('txt_title_ls')

    @property
    def nextBtnObj(self): 
        return self._getWidget('btn_next')
    
    @property
    def previousBtnObj(self): 
        return self._getWidget('btn_previous')

class PatternCanvas(Canvas):
    def __init__(self, logic):
        super(Canvas, self).__init__()
        Canvas.__init__(self, 'pattern_canvas', logic)

    @property
    def backBtnObj(self):
        return self._getWidget('btn_back')

    @property
    def titleTxtObj(self):
        return self._getWidget('txt_pattern_title')
    
    @property
    def descriptionTxtObj(self):
        return self._getWidget('txt_pattern_description')   

class ChallengeCanvas(Canvas):
    def __init__(self, logic):
        super(Canvas, self).__init__()
        Canvas.__init__(self, 'challenge_canvas', logic)

    @property
    def titleTxtObj(self):
        return self._getWidget('txt_title')

    @property
    def timeLabelTxtObj(self):
        return self._getWidget('txt_time_label')
    
    @property
    def movesLabelTxtObj(self): 
        return self._getWidget('txt_moves_label')
    
    @property
    def movesTxtObj(self): 
        return self._getWidget('txt_moves')
    
    @property
    def timeTxtObj(self): 
        return self._getWidget('txt_time')
    
    @property
    def statusTxtObj(self): 
        return self._getWidget('txt_status')
    
    @property
    def playBtnObj(self): 
        return self._getWidget('btn_play')
   
    @property
    def patternBtnObj(self): 
        return self._getWidget('btn_pattern')
    

