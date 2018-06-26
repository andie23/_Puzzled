###########################################################
# Author: Andrew Mfune
# Date: 22/05/2018
# Description: This module contains a list of PATTERNS that
#               the player must solve in the game.
###########################################################
PUZZLE_PATTERNS_4X4 = {
    'CLASSIC':  { 
      1 : [1, 2, 3, 4], 
      2 : [5, 6, 7,8],
      3 : [9, 10, 11, 12],
      4 : [13, 14, 15, 0]
    },
    'PAT_1': {
       1 : [0, 1, 2, 3], 
       2 : [4, 5, 6, 7],
       3 : [8, 9, 10, 11],
       4 : [12, 13, 14, 15]
    },
    'PAT_2': {
      1 : [4, 8, 12, 0],
      2 : [3, 7, 11, 15],
      3 : [2, 6, 10, 14],
      4 : [1, 5, 9, 13] 
    },
    'PAT_3': {
       1 : [13, 14, 15, 0], 
       2 : [9, 10, 11, 12],
       3 : [5, 6, 7, 8],
       4 : [1, 2, 3, 4]
    },
    'PAT_4': {
       1 : [0, 4, 8, 12], 
       2 : [1, 5, 9, 13],
       3 : [2, 6, 10, 14],
       4 : [3, 7, 11, 15]
    },
    'PAT_5': {
       1 : [15, 14, 13, 0], 
       2 : [12, 11, 10, 9],
       3 : [8, 7, 6, 5],
       4 : [4, 3, 2,1]
    },
    'PAT_6': {
       1 : [3, 2, 1, 0], 
       2 : [7, 6, 5, 4],
       3 : [11, 10, 9, 8],
       4 : [15, 14, 13, 12]
     },
    'PAT_7': {
       1 : [0, 12, 5, 4], 
       2 : [13, 11, 6, 3],
       3 : [14, 10, 7, 2],
       4 : [15, 9, 8, 1]
     },
    'PAT_8': {
       1 : [1, 2, 9, 10], 
       2 : [3, 4, 11, 12],
       3 : [5, 6, 13, 14],
       4 : [7 ,8 , 15, 0]
     },
     'PAT_9': {
          1 : [6, 5, 14, 13],
          2 : [7, 4, 15, 12],
          3 : [8, 3, 0, 11],
          4 : [1, 2, 9, 10] 
      },
     'PAT_10': {
           1 : [0, 3, 2, 1], 
           2 : [15, 4, 5, 6],
           3 : [14, 9, 8, 7],
           4 : [13, 12, 11, 10]
       },
     'PAT_11': {
           1 : [4, 3, 2, 1], 
           2 : [5, 0, 15, 14],
           3 : [6, 13, 12, 11],
           4 : [7, 8, 9, 10]
       },
     'PAT_12': {
           1 : [1, 9, 10, 2], 
           2 : [3, 11, 12, 4],
           3 : [5, 13, 14, 6],
           4 : [7, 15, 0, 8]
      },
     'PAT_13': {
           1 : [1, 2, 3, 4], 
           2 : [9, 10, 11, 12],
           3 : [13, 14, 15, 0],
           4 : [5, 6, 7, 8]
      },
     'PAT_14': {
           1 : [3, 11, 4, 12], 
           2 : [2, 10, 5, 13],
           3 : [1, 9, 6, 14],
           4 : [0, 8, 7, 15]
      },
     'PAT_15': {
           1 : [1, 2, 3, 4], 
           2 : [5, 0, 6, 7],
           3 : [8, 9, 10, 11],
           4 : [12, 13, 14, 15]
      }
}