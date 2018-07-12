from objproperties import ObjProperties

class Menu:
    def __init__(self):
        pass

class ChallengesMenu(Menu):
    def __init__(self, scene):
        self.scene = scene
        super(Menu, self).__init__()
    
    def addCanvas(self, name, posObj, txtTitle='Default',
            txtTime='00:00:00.0', txtMoves=0):

        inactiveObjs = self.scene.objectsInactive
        canvas = inactiveObjs['canvas']
        canvasProps = ObjProperties(canvas)
        canvasProps.setProp('cname', name)
        canvasWidgets = canvas.children

        for widget in canvasWidgets:
            widgetName = str(widget)
            widgProps = ObjProperties(widget)

            if widgetName == 'txt_moves':
                widgProps.setProp('Text', txtMoves)
                continue

            if widgetName == 'txt_title':
                widgProps.setProp('Text', txtTitle)
                continue

            if widgetName == 'txt_time':
                widgProps.setProp('Text', txtTime)
                continue

        self.scene.addObject(canvas, posObj, 0)

