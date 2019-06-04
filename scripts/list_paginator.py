from bge import logic

class ListPaginator:
    def __init__(self, name, logic):
        self.gdict = logic.globalDict
        self.pgID = '%s.paginator' % name
        self.perPage = 0
        self.groupList = []
        self.curIndex = 0

    def isset(self):
        return self.pgID in self.gdict
    
    def load(self):
        props = self.gdict[self.pgID]
        self.perPage = props['perPage']
        self.groupList = props['groupList']
        self.curIndex = props['curIndex']

    def updateGlobalIndex(self, val):
        self.gdict[self.pgID]['curIndex'] = val 

    def paginate(self, listItems, itemsPerpage):
        groupList = self.groupItems(listItems, itemsPerpage)
        self.perPage = itemsPerpage
        self.groupList = groupList
        
        self.gdict[self.pgID] = {
            'perPage': itemsPerpage,
            'groupList' : groupList,
            'curIndex' : self.curIndex
        }

    def get(self):
        return self.groupList[self.curIndex]
    
    def next(self):
        groupLen = len(self.groupList) -1
        if self.curIndex >= groupLen:
            self.curIndex = 0
        else:
            self.curIndex += 1
        self.updateGlobalIndex(self.curIndex)
        return self.groupList[self.curIndex]

    def previous(self):
        if self.curIndex <= 0:
            groupLen = len(self.groupList) -1
            self.curIndex = groupLen
        else:
            self.curIndex -= 1
        self.updateGlobalIndex(self.curIndex)
        return self.groupList[self.curIndex]

    def groupItems(self, listItems, itemsPerGroup):
        curIndex = 0
        itemGroupList = [[]]

        for item in listItems:
            if len(itemGroupList[curIndex]) >= itemsPerGroup:
                curIndex +=1
                itemGroupList.append([])
            itemGroupList[curIndex].append(item)
        return itemGroupList