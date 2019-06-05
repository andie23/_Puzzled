from objproperties import ObjProperties
from navigator import SceneHelper
from timer import Timer
from animate import *
from bge import logic
from canvas_global_data import CanvasGlobalData
from logger import logger

log = logger()

class Canvas(CanvasGlobalData):
    def __init__(self, canvas, id, scene):
        super(Canvas, self).__init__(id)
        self._canvasName = canvas
        self.setScene(scene)

    def __getScene(self):
        return SceneHelper(logic).getscene(self.getScene())

    def isset(self):
        return  ObjProperties().getObjByPropVal(
            'canvas_id', self.getId(), self.__getScene().objects
        ) is not None

    def add(self, node, isVisible=True):
        log.debug('Adding canvas to the scene..')
        self.setNode(node)
        self._addCanvasObj(isVisible)

    def load(self):
        log.debug('Loading existing canvas properties..')
        canvasObj = self.__getScene().objects[self._canvasName]
        canvasObj['canvas_id']  = self.getId()
        self.setObj(canvasObj)
        self._tagWidgets(canvasObj)

    def hide(self):
        self._setvisibility(False)

    def show(self):
        self._setvisibility(True)

    def remove(self):
        log.debug('Removing canvas %s', self._canvasName)
        self.getCanvasObj().endObject()
        self.delete()

    def resetPosition(self):
        if not self.getNode():
            return
        log.debug('Resetting %s canvas position', self._canvasName)
        self.getCanvasObj().position = self.getNode().position

    def _getWidget(self, name):
        widgets = self.getCanvasObj().childrenRecursive
        if name not in widgets:
            return
        return widgets[name]
            
    def _tagWidgets(self, canvas):
        canvasId = canvas['canvas_id']
        log.debug('Tagging canvas %s children with own reference', self._canvasName)
        for child in canvas.childrenRecursive:
            log.debug('Tagging child %s ', str(child))
            child['parent_canvas_id'] = canvasId
            child['widget_id'] = '%s_%s' % (canvasId, str(child))

    def _setvisibility(self, bool, obj=None):
        if not obj:
            obj = self.getCanvasObj()
        
        if '_hidden' not in obj:
            log.debug('Setting visibility for canvas %s to %s', str(obj), bool)
            obj.visible = bool

        for child in obj.childrenRecursive:
            if '_hidden' not in child:
                log.debug('Setting visibility for child %s to %s', str(child), bool)
                child.visible = bool

    def _addCanvasObj(self, isVisible):
        log.debug('setting inactive canvas object')
        scene = self.__getScene()
        canvas = scene.objectsInactive[self._canvasName]
        
        log.debug('assigning identity %s to canvas %s', self.getId(), self._canvasName)
        canvas['canvas_id'] = self.getId()
        self._tagWidgets(canvas)
        self._setvisibility(isVisible, canvas)

        log.debug('adding canvas %s into the scene on node %s', self._canvasName, self.getNode())
        scene.addObject(canvas, self.getNode(), 0)
        self.setObj(ObjProperties().getObjByPropVal(
            'canvas_id', self.getId(), scene.objects
        ))
