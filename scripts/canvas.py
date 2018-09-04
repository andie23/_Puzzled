from objproperties import ObjProperties
from navigator import SceneHelper
from threading import Timer

class Canvas():
    def __init__(self, canvasObjName, logic, sceneName=None):
        if sceneName:
            shelper = SceneHelper(logic)
            self.scene = shelper.getscene(sceneName)
        else:
            self.scene = logic.getCurrentScene()
        self._canvasObjName = canvasObjName
        self.globDict = logic.globalDict
        self.inactiveObjs = self.scene.objectsInactive
        self.canvasID = None
        self.widgets = None
        self.canvasObj = None
    
    def disableWidgets(self):
        for widget in self.widgets:
            if 'is_enabled' in widget:
                widget['is_enabled'] = False

    def enableWidgets(self):
        for widget in self.widgets:
            if 'is_enabled' in widget:
                widget['is_enabled'] = True

    def isset(self):
        return True if self._canvasObjName in self.scene.objects else False

    def load(self, canvasID):
        self.canvasID = canvasID
        self.canvasObj = self.scene.objects[self._canvasObjName]
        self.widgets = self._getWidgets()

    def add(self, canvasID, node):
        self.canvasID = canvasID
        self.canvasObj = self._loadCanvas(node)
        self.widgets = self._getWidgets()

    def setColor(self, color, applyToChildren=False):
        self.canvasObj.color = color

        if applyToChildren:
            for name, widget in self.widgets.items():
                widget.color = color

    def remove(self):
        self.canvas.endObject()

    def _loadCanvas(self, node):
        inactiveCanvas = self.inactiveObjs[self._canvasObjName]
        canvasProps = ObjProperties(inactiveCanvas)
        canvasProps.setProp('canvas_id', self.canvasID)
        
        if 'position_node' in node:
            activeCanvasID = node['position_node']
            if activeCanvasID and activeCanvasID != self.canvasID:
                activeCanvasObj = canvasProps.getObjByPropVal(
                    'canvas_id', activeCanvasID, self.scene.objects
                )
                if activeCanvasObj:
                    activeCanvasObj.endObject()         
            node['position_node'] = self.canvasID

        self.scene.addObject(inactiveCanvas, node, 0)
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

class NotificationCanvas(Canvas):
    def __init__(self, logic, sceneID=None):
        super(Canvas, self).__init__()
        Canvas.__init__(self, 'notification_canvas', logic, sceneID)
        self.Obj = ObjProperties(self.canvasObj)

    def setDuration(self, duration):
        self.canvasObj['duration'] = duration

    @property
    def infoTxtObj(self):
        return self._getWidget('txt_notification_info')
    
class InfoDialogCanvas(Canvas):
    def __init__(self, logic, sceneID=None):
        super(Canvas, self).__init__()
        Canvas.__init__(self, 'info_dialog_canvas', logic, sceneID)
        self.Obj = ObjProperties()

    @property
    def titleTxtObj(self):
        return self._getWidget('txt_info_dialog_title')
    
    @property
    def subtitleTxtObj(self):
        return self._getWidget('txt_info_dialog_subtext')
    
    @property
    def confirmBtnObj(self):
        return self._getWidget('btn_info_dialog_ok')
    
class ConfirmDialogCanvas(Canvas):
    def __init__(self, logic, sceneID=None):
        super(Canvas, self).__init__()
        Canvas.__init__(self, 'confirmation_dialog_canvas', logic, sceneID)
        self.Obj = ObjProperties()

    @property
    def titleTxtObj(self):
        return self._getWidget('txt_confir_dialog_title')
    
    @property
    def subtitleTxtObj(self):
        return self._getWidget('txt_confir_dialog_subtext')
    
    @property
    def confirmBtnObj(self):
        return self._getWidget('btn_confir_dialog_ok')
    
    @property
    def cancelBtnObj(self):
        return self._getWidget('btn_confir_dialog_no')
    
    

class PauseDialogCanvas(Canvas):
    def __init__(self, logic, sceneID=None):
        super(Canvas, self).__init__()
        Canvas.__init__(self, 'pause_dialog_canvas', logic, sceneID)
        self.Obj = ObjProperties()

    @property
    def subtitleTxtObj(self):
        return self._getWidget('txt_pause_dialog_subtext')
    
    @property
    def titleTxtObj(self):
        return self._getWidget('txt_pause_dialog_title')
    
    @property
    def homeBtnObj(self):
        return self._getWidget('btn_pause_dialog_home')
    
    @property
    def shuffleBtnObj(self):
        return self._getWidget('btn_pause_dialog_reshuffle')
   
    @property
    def returnBtnObj(self):
        return self._getWidget('btn_pause_dialog_play')
    
class HudCanvas(Canvas):
    def __init__(self, logic, sceneID=None):
        super(Canvas, self).__init__()
        Canvas.__init__(self, 'hud_canvas', logic, sceneID)
        self.Obj = ObjProperties()

    @property
    def pauseBtnObj(self):
        return self._getWidget('btn_hud_pause')
    
    @property
    def reshuffleBtnObj(self):
        return self._getWidget('btn_hud_reshuffle_puzzle')
    
    @property
    def homeBtnObj(self):
        return self._getWidget('btn_hud_challenges_menu')
    
    @property
    def patternBtnObj(self):
        return self._getWidget('btn_hud_pattern_view')

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
    def reshuffleBtnObj(self):
        return self._getWidget('btn_assessment_reshuffle')
    
    @property
    def exitBtnObj(self):
        return self._getWidget('btn_assessment_exit')

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
    def playBtnObj(self):
        return self._getWidget('btn_play_pattern')

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
    

