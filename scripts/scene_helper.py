from bge import logic
from global_dictionary import GlobDict

class SceneGlobalData(GlobDict):
    def __init__(self):
        super(SceneGlobalData, self).__init__('scene_data')
        if not self.data:
            self._setDefaults()
    
    def getBackgroundSceneId(self):
        return self.data['background_scene']
    
    def getOverlaySceneId(self):
        return self.data['overlay_scene']

    def setBackgroundSceneId(self, scene):
        self.data['background_scene'] = scene
    
    def setOverlaySceneId(self, scene):
        self.data['overlay_scene'] = scene
    
    def _setDefaults(self):
        self.data['background_scene'] = None
        self.data['overlay_scene'] = None

class Scene(SceneGlobalData):
    def __init__(self, id):
        super(Scene, self).__init__()
        self._id = id

    def isset(self):
        return True if self.getscene() else False

    def addOverlay(self):
        scene = self.getscene(self.getOverlaySceneId())
        self.setOverlaySceneId(self._id)
        if scene and scene != self._id:
            scene.replace(self._id)
        else:
            logic.addScene(self._id, 1)
    
    def addBackground(self):
        scene = self.getscene(self.getBackgroundSceneId())
        self.setBackgroundSceneId(self._id)
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

    def isSuspended(self):
        return self.getscene().suspended

    def restart(self):
        self.getscene().restart()

    def suspend(self):
        self.getscene().suspend()
    
    def resume(self):
        self.getscene().resume()

    def remove(self):
        if self.getBackgroundSceneId() == self._id:
            self.setBackgroundSceneId(None)
        elif self.getOverlaySceneId() == self._id:
            self.setOverlaySceneId(None)
        self.getscene().end()
