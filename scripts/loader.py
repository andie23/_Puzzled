from bge import logic 

def add_loading_screen(func):
    from navigator import overlayLoadingScreen
    overlayLoadingScreen()
    def main(*args, **kwargs):
        return func(*args, **kwargs)
    return main

def remove_static_loader(objname):
    def main(func):
        def submain(*args, **kwargs):
            if func(*args, **kwargs):
                scene = logic.getCurrentScene()
                if objname in scene.objects:
                    scene.objects[objname].endObject()
        return submain
    return main

def runFunc():
    if 'close_loader' in logic.globalDict:
        logic.getCurrentScene().end()
        del logic.globalDict['close_loader']