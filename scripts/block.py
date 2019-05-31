from bge import logic

class Block():
    def __init__(self, scene, obj):
        self.obj = obj
        self.scene = scene

    def setNode(self, node):
        self.obj['position_node'] = str(node)

    @property
    def positionNode(self):
        node = self.obj['position_node']
        if node:
            return self.scene.objects[node]
        return None
    
    @property
    def positionNodeID(self):
        node = self.positionNode
        return node['block_number'] if node else 0
    
    @property
    def blockID(self):
        return self.obj['block_number']
