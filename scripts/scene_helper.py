from bge import logic

class Scene:
    def __init__(self, id):
        self._id = id
        if 'scene_data' not in logic.globalDict:
            logic.globalDict['scene_data'] = {}
        self._data = logic.globalDict['scene_data']
        if not self._data:
            self._setDefaults()

    def isset(self):
        return True if self.getscene() else False

    def addOverlay(self):
        scene = self.getscene(self._getOverlaySceneId())
        self._setOverlaySceneId(self._id)
        if scene and scene != self._id:
            scene.replace(self._id)
        else:
            logic.addScene(self._id, 1)
    
    def addBackground(self):
        scene = self.getscene(self._getBackgroundSceneId())
        self._setBackgroundSceneId(self._id)
        if scene and scene != self._id:
            scene.replace(self._id)
        else:
            logic.addScene(self._id, 0)

    def getscene(self, name=None):
        if not name:
            name = self._id

        for scene in logic.getSceneList():
            if str(scene) == name:
                return scene

    def restart(self):
        self.getscene().restart()

    def suspend(self):
        self.getscene().suspend()
    
    def resume(self):
        self.getscene().resume()

    def remove(self):
        if self._getBackgroundSceneId() == self._id:
            self._setBackgroundSceneId(None)
        elif self._getOverlaySceneId() == self._id:
            self._setOverlaySceneId(None)
        self.getscene().end()

    def _getBackgroundSceneId(self):
        return self._data['background_scene']
    
    def _getOverlaySceneId(self):
        return self._data['overlay_scene']

    def _setBackgroundSceneId(self, scene):
        self._data['background_scene'] = scene
    
    def _setOverlaySceneId(self, scene):
        self._data['overlay_scene'] = scene
    
    def _setDefaults(self):
        self._data['background_scene'] = None
        self._data['overlay_scene'] = None


