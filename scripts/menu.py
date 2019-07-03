from ui_background import appendBackground
from scene_helper import Scene, SceneGlobalData
from bge import logic
from canvas_effects import *

FRONT_POSITION_NODE = 'front_position_node'
CENTER_POSITION_NODE = 'center_position_node'
BACK_POSITION_NODE  = 'back_position_node'

class Menu():
    def __init__(self, canvas, position, isVisible=True):
        self.canvas = canvas
        if not self.canvas.isset():
            self.canvas.add(
                Scene('HUD').getscene().objects[position], isVisible
            )
        else:
            self.canvas.load()

class PopUpMenu(Menu):
    def __init__(self, canvas, position=''):
        super(PopUpMenu, self).__init__(canvas, position, False)
        if 'pop_menu_count' not in logic.globalDict:
            logic.globalDict['pop_menu_count'] = 0
        self.menuCount = logic.globalDict['pop_menu_count']

    def _getBackgroundScene(self):
        id = SceneGlobalData().getBackgroundSceneId()
        if id:
            return Scene(id)
        return None

    def open(self, callback=lambda:()):
        appendBackground(self.canvas.getCanvasObj())
        bgScene = self._getBackgroundScene()
        if bgScene:
            bgScene.suspend()
        dialogPopIn(self.canvas, onFinishAction=self.canvas.resetPosition)
        self.canvas.show()
        self.menuCount += 1
        callback()

    def close(self, callback=lambda:()):
        bgScene = self._getBackgroundScene()
        if bgScene and self.menuCount <= 1:
            bgScene.resume()
        if self.canvas.isset():
            self.canvas.remove()
        if self.menuCount >= 1: 
            self.menuCount -= 1
        callback()
