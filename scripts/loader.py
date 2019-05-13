from bge import logic 

def add_loading_screen(func):
    from navigator import overlayLoadingScreen
    overlayLoadingScreen()
    def main(*args, **kwargs):
        return func(*args, **kwargs)
    return main

        
