from bge import logic

class GlobDict():
    def __init__(self, header):
        self.globDict = logic.globalDict
        if header not in self.globDict:
            self.globDict[header] = {}
        self.data = self.globDict[header]
