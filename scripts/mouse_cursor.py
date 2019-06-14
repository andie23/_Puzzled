import Rasterizer as R

def init(cont):
    own = cont.owner
    # scale down the mouse cursor to be smaller. If left uncheck,
    # the cursor model appears too big because it's so close to the 
    # screen
    own.worldScale = [0.005, 0.005, 0.005]
    
    # set the mouse cursor at the center of the screen
    R.setMousePosition(
        int(R.getWindowWidth()/2), int(R.getWindowHeight()/2)
    )
 
def move(cont):
    own = cont.owner
    mouseSen = cont.sensors['Mouse']
    mousePos = mouseSen.raySource
    own.position = mousePos