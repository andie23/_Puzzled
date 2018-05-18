'''
The state manager module shall monitor the puzzle block and
change it's state accordingly based on parameters provided.

These states are asthetic in nature, such as:
    1. changing the color of the block when it's matching the correct static block,
    2. Entering an alert mode when a matched puzzle block is mismatched
    3. Changing the color of the puzzle block to black if alert mode timer runsout
'''

def main():
    pass

def changeColorOnMatch():
    '''
    When the block's number is matching the current static block number, 
    change the color of the visualblock to indicate that it's in the correct
    position.
    '''
    pass

def enterAlertModeOnBlockMisMatch(expiry=0, expiryAction=None):
    '''
    Enter alert mode when a matched block gets mismatched.

    An expiry timer is the time limit of alertMode.

    An expiryAction is an event that must occur when the expiry time
    has been reached.
    '''
    pass

def removeColor(scope, offset=0):
    '''
    Remove color from the current puzzle block or all blocks.

    scope specifies the blocks to be affected... either the current one
    or all blocks.
    '''

    pass

def influenceAlertModeToOtherBlocks(scope):
    '''
    When a puzzle block enters alertmode, this state will influence the puzzle
    block closest to it or all  blocks which are not matched. This can be set in the scope
  
    @param: scope: scope of influence nearest blocks or all blocks
    '''
    pass

def changePuzzleOrientation(orientations, changeTrigger, offset=0):
    '''
    Change orientation of the puzzle on the fly based on the 

    @param : orientations: a list of orientations to switch to during the game
    @param : eventTrigger: an event that should trigger the puzzle orientation change
    '''

    pass

def lockPuzzleOnMismatches(misMatchCount, duration):
    '''
    Lock the puzzle if the maximum number of mismatches have been exceeded
    for a duration period.
    '''
    pass

def enterTimerMode(timeLimit, expiryAction=None):
    '''
    The game as a whole enters time trial state  
    '''
    pass

def lockPuzzle(duration):
    '''
    Lock the whole puzzle for a duration of time.
    @param: duration: determines how long the puzzle should be looked.
    '''
    pass

