from objproperties import ObjProperties
from navigator import SceneHelper
from timer import Timer
from animate import *
from bge import logic

class Canvas():

    def __init__(self, canvasObjName, canvasId, sceneName=None):
        self.id = canvasId
        self.scene = self.getScene(sceneName)
        self.sceneName = sceneName
        self.canvasObj = None
        self.posNode = None
        self._canvasObjName = canvasObjName
        
        if 'loaded_canvas' not in logic.globalDict:
            logic.globalDict['loaded_canvas'] = {}

    def getScene(self, sceneName):
        return SceneHelper(logic).getscene(sceneName)

    def setWidgetVal(self, var, val):
        for widget in self.canvasObj.childrenRecursive:
            if var in widget:
                widget[var] = val
        
    def disableWidgets(self):
        self.setWidgetVal('is_enabled', False)

    def enableWidgets(self):
        self.setWidgetVal('is_enabled', True)
   
    def isset(self):
        return  ObjProperties().getObjByPropVal(
            'canvas_id', self.id, self.scene.objects
        ) is not None

    def loadStatic(self):
        self.canvasObj = self.scene.objects[self._canvasObjName]
        self.canvasObj['canvas_id'] = self.id
        self._setWidgetIds()
        self._setGlobDict()

    def load(self):
        props = logic.globalDict['loaded_canvas'][self.id]
        self.sceneName = props['scene_name']
        self.scene = self.getScene(props['scene_name'])
        self.canvasObj = ObjProperties().getObjByPropVal(
            'canvas_id', self.id, self.scene.objects
        )

    def add(self, node):
        self._setNode(node)
        self._setCanvas()
        self._setWidgetIds()
        self._setGlobDict()
    
    def hide(self, widget=None):
        if not widget and self.canvasObj:
            widget = self.canvasObj
        if widget:
            for childWidget in widget.childrenRecursive:
                childWidget.visible = False
            widget.visible = False
        return widget

    def show(self, obj):
        for childWidget in obj.childrenRecursive:
            if '_hidden' not in childWidget:
                childWidget.visible = True
        if '_hidden' not in obj:
            obj.visible = True

    def remove(self):
        self.canvasObj.endObject()
        del logic.globalDict['loaded_canvas'][self.id]
    
    def popIn(self):
        initAnimation({
            'scene_id' : self.sceneName, 
            'target_obj' : self.canvasObj,
            'anim_name' : 'dialog_pop_in', 
            'fstart' : 0.0,
            'fstop' : 2.0,
            'speed' : 0.1,
            'on_start_action': lambda: self.show(self.canvasObj)
        })
    
    def fadeIn(self):
        def anim(obj, speed=0.09):    
            initAnimation({
                'scene_id' : self.sceneName, 
                'target_obj' : obj,
                'anim_name' : 'fade_in', 
                'fstart' : 0.0,
                'fstop' : 5.0,
                'speed' : speed,
                'on_start_action': lambda: self.show(obj)
            })

        for childWidget in self.canvasObj.childrenRecursive:
            if '_hidden' not in childWidget:
                anim(childWidget)

        anim(self.canvasObj)

    def setColor(self, color, applyToChildren=False):
        self.canvasObj.color = color

        if applyToChildren:
            for name, widget in self.widgets.items():
                widget.color = color

    def _setGlobDict(self):    
        logic.globalDict['loaded_canvas'][self.id] = {
            'scene_name' : self.sceneName
        }

    def _setCanvas(self):
        inactiveObjs = self.scene.objectsInactive
        inactiveCanvas = inactiveObjs[self._canvasObjName]
        inactiveCanvas['canvas_id'] = self.id
        inactiveCanvas = self.hide(inactiveCanvas)

        self.scene.addObject(inactiveCanvas, self.posNode, 0)
        self.canvasObj =  ObjProperties().getObjByPropVal(
            'canvas_id', self.id, self.scene.objects
        )

    def _setNode(self, node):
        if 'position_node' not in node:
            return
        activeCanvasId = node['position_node']
        if activeCanvasId and activeCanvasId != self.id:
            activeCanvasObj = ObjProperties().getObjByPropVal(
                'canvas_id', activeCanvasId, self.scene.objects
            )
            if activeCanvasObj:
                activeCanvasObj.endObject()
        node['position_node'] = self.id
        self.posNode = node

    def _getWidget(self, widgetObjName):
        identifier = '%s.%s' % (self.id, widgetObjName)
        for widget in self.canvasObj.childrenRecursive:
            if 'widget_id' not in widget:
                continue
            if identifier == widget['widget_id']:
                return widget
        return None

    def _setWidgetIds(self):
        for widget in self.canvasObj.children:
            widget['widget_id'] = '%s.%s' % (self.id, widget)

class NotificationCanvas(Canvas):
    def __init__(self, sceneId='HUD'):
        super(Canvas, self).__init__()
        Canvas.__init__(self, 'notification_canvas', 'notification_canvas', sceneId)
        self.Obj = ObjProperties(self.canvasObj)
        self.animId = 'notification_canvas_anim'
        self.sceneId = sceneId

    @property
    def infoTxtObj(self):
        return self._getWidget('txt_notification_info')

class InfoDialogCanvas(Canvas):
    def __init__(self, sceneID=None):
        super(Canvas, self).__init__()
        Canvas.__init__(self, 'info_dialog_canvas', 'info_dialog_canvas', sceneID)
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
    def __init__(self, sceneID=None):
        super(Canvas, self).__init__()
        Canvas.__init__(self, 'confirmation_dialog_canvas', 'confirmation_dialog_canvas', sceneID)
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
    def __init__(self, sceneID=None):
        super(Canvas, self).__init__()
        Canvas.__init__(self, 'pause_dialog_canvas', 'pause_dialog_canvas', sceneID)
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

class PuzzledDialogCanvas(Canvas):
    def __init__(self, sceneID=None):
        super(Canvas, self).__init__()
        Canvas.__init__(self, 'puzzled_dialog_canvas', 'puzzled_dialog_canvas', sceneID)
        self.Obj = ObjProperties()

    @property
    def subtitleTxtObj(self):
        return self._getWidget('txt_puzzled_dialog_subtext')
    
    @property
    def titleTxtObj(self):
        return self._getWidget('txt_puzzled_dialog_title')
    
    @property
    def homeBtnObj(self):
        return self._getWidget('btn_puzzled_dialog_home')
    
    @property
    def shuffleBtnObj(self):
        return self._getWidget('btn_puzzled_dialog_reshuffle')

class HudCanvas(Canvas):
    def __init__(self, sceneId='HUD'):
        super(Canvas, self).__init__()
        Canvas.__init__(self, 'hud_canvas', 'hud_canvas', sceneId)
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
    def prevStreakTxtObj(self):
        return self._getWidget('txt_hud_prev_streak')
    
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
    def __init__(self):
        super(Canvas, self).__init__()
        Canvas.__init__(self, 'assessment_canvas', 'assessment_canvas', 'ASSESSMENT')
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
    def currentStreakTxtObj(self):
        return self._getWidget('txt_current_streak')
    
    @property
    def streakAssessmentTxtObj(self):
        return self._getWidget('txt_streak_assessment')
    
    @property
    def currentMovesTxtObj(self):
        return self._getWidget('txt_current_moves')
   
    @property
    def previousStreakTxtObj(self):
        return self._getWidget('txt_previous_streak')
   
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
    def __init__(self):
        super(Canvas, self).__init__()
        Canvas.__init__(self, 'list_canvas', 'list_canvas', 'CHALLENGES_MENU')
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
    def __init__(self):
        super(Canvas, self).__init__()
        Canvas.__init__(self, 'pattern_canvas', 'pattern_canvas', 'PATTERN_VIEW')

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
    def __init__(self, canvasId):
        super(Canvas, self).__init__()
        Canvas.__init__(self, 'challenge_canvas', canvasId, 'CHALLENGES_MENU')

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
    

