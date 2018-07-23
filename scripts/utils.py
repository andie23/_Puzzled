#########################################################
# Author: Andrew Mfune
# Date: 22/05/2018
# Description: Module contains generic utility methods that
#              can be reused throughout the program.
#########################################################
from config import HOME_PATH, DATA_DIR, LOG_FILE_NAME, DB_NAME
from os import mkdir, listdir, path
from random import randint
from datetime import datetime, timedelta
from copy import deepcopy

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
        itemGroupList = []
        itemGroup = []
        maxGroups = len(listItems) / itemsPerGroup

        for item in listItems:
            itemGroup.append(item)
            if (len(itemGroup) >= itemsPerGroup or len(itemGroupList) == int(maxGroups)):
                itemGroup.reverse()
                group = deepcopy(itemGroup)
                itemGroupList.append(group)
                itemGroup = []
        return itemGroupList

class RandNumScope():
    '''
    Return a list of random numbers by specified scope size
    and sizelimit a number should be under
    '''
    def __init__(self, scopeSize, sizeLimit):
        self.scopeSize = scopeSize
        self.sizeLimit = sizeLimit

    def get(self):
        numList = []
        randNum = 1

        for num in range(1, self.scopeSize):
            while randNum in numList:
                randNum = randint(1, self.sizeLimit)
            
            numList.append(randNum)

        return numList

def frmtTime(timer):
    time = str(timedelta(seconds=timer))
    return time[:7]

def animate(object, name,  speed, start=0, end=20):
    '''
    Play animations on specified scene objects.
    '''
    from bge import logic
    layer = 0 
    priority = 1
    blendin = 1.0
    mode = logic.KX_ACTION_MODE_LOOP
    layerWeight = 0.0
    ipoFlags = 1
    
    object.playAction(name, start, end, layer, 
         priority, blendin, mode, layerWeight, ipoFlags, speed)

def calcPercDiff(originNum, newNum):
    decrease = originNum - newNum
    percDecrease = decrease / originNum * 100
    return int(percDecrease)

def getPercBetween(minval, maxval):
    '''
    Get percentage of curVal and maxVal
    returns int
    '''

    diff = maxval - minval
    div = minval/maxval
    perc = div * 100
    
    return int(perc)


def dataDirPath():
    '''
    Return full path of the game's directory. The game directory is 
    created if not found.
    '''

    path = '{0}\{1}'.format(HOME_PATH, DATA_DIR)
    
    if DATA_DIR not in listdir(HOME_PATH):
        mkdir(path)
         
    return path

def positionTxt(txt, right=0, left=0):
    if right > 0:
        txtspace = '{:>%s}' % right
        txt = txtspace.format(txt)
    elif left > 0:
        txtspace = '{:<%s}' % left
        txt = txtspace.format(txt)
    
    return txt

def logPath():
    '''
    Returns full path of where the log file is located
    '''
    
    return '{0}\{1}'.format(dataDirPath(), LOG_FILE_NAME)

def curdatetime():
    return str(datetime.today())

def getDBPath():
    return '{0}\{1}'.format(dataDirPath(), DB_NAME)

def isPathExists(pathaddress):
    return path.exists(pathaddress)