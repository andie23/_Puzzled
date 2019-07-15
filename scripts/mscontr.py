from bge import logic
import Rasterizer as R
from mscursor import *
from scene_helper import Scene

CURSOR_DISTANCE = 1

def init():
    loadCursorObjs()
    defaultCursor = Cursor(ARROW_POINTER)
    defaultCursor.setAsDefault()
    defaultCursor.use()

    R.setMousePosition(
        int(R.getWindowWidth()/2), int(R.getWindowHeight()/2)
    )

def loadCursorObjs():
    '''
    Loads all cursor objects from hidden layer into active layer.
    Cursors are parented to an empty cursor object and 
    visibility set to False.
    '''
    
    from objproperties import ObjProperties
    
    scene = Scene('HUD').getscene()
    parentCursor = getCursorObj()
    cursorList = ObjProperties().getPropObjGroup(
        'mouse_pointer', scene, 0
    )
    
    for cursor in cursorList:
        cursor.visible = False
        scene.addObject(cursor, parentCursor)
        scene.objects[str(cursor)].setParent(parentCursor)

def getCursorObj():
    '''
    Returns Empty cursor object
    '''
    return Scene('HUD').getscene().objects['mouse_cursor']
    
def getMouseToWorldCoordinates(camera):
    '''
    Converts mouse coordinates to 3D worldspace coordinates
    '''

    z = CURSOR_DISTANCE
    pos = camera.worldPosition
    vec = camera.getScreenVect(*logic.mouse.position)
    
    projection = [
        pos[0] - vec[0] * z, 
        pos[1] - vec[1] * z, 
        pos[2] - vec[2] * z
    ]
    return projection

def update(cont):
    '''
    Update mouse cursor position
    '''

    cam = cont.owner
    mousePos = getMouseToWorldCoordinates(cam)
    cursor =  getCursorObj()

    cursor.worldPosition = mousePos
    cursor.worldOrientation = cam.worldOrientation