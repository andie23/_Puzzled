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
        self.bgSceneResume = True

    def _getBackgroundScene(self):
        id = SceneGlobalData().getBackgroundSceneId()
        if id:
            return Scene(id)
        return None

    def open(self, callback=lambda:()):
        # parent a background object to the canvas to
        # hide background scene and to occlude other active HUD widgets
        # to prevent accidental inputs

        appendBackground(self.canvas.getCanvasObj())

        # Suspend background scene to prevent it's objects
        # from accidentally reacting to inputs when interacting with hud
        # widgets
        bgScene = self._getBackgroundScene()
        if bgScene and not bgScene.isSuspended():
            bgScene.suspend()
        else:
            # set to false to prevent this menu item from resuming 
            # background scene if it didn't originally suspend it
            self.bgSceneResume = False
        dialogPopIn(self.canvas, onFinishAction=self.canvas.resetPosition)
        callback()

    def close(self, callback=lambda:()):
        bgScene = self._getBackgroundScene()
        # Resume suspended background scene as long as it's resumable
        if bgScene and self.bgSceneResume:
            bgScene.resume()

        if self.canvas.isset():
            self.canvas.remove()
        callback()
