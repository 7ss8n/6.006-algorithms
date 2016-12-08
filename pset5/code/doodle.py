###################################
##########  PROBLEM 5-4 ###########
###################################

from operator import itemgetter
from collections import deque


def pp(matrix):
    for i in range(len(matrix)):
        print(matrix[i])


def recoverPath2D(moveArray2D):
    """
    Starting from last move, follow parent pointers back until we get a parent points to (0,0), which is the start point
    """
    currentIndex = (len(moveArray2D)-1, len(moveArray2D[0])-1)
    print("Start:", currentIndex)
    moveSeq = deque()

    while currentIndex != (0, 0):
        moveSeq.appendleft(moveArray2D[currentIndex[0]][currentIndex[1]][1])
        currentIndex = moveArray2D[currentIndex[0]][currentIndex[1]][2]
    return list(moveSeq)



def double_kill(ghost1, ghost2):
    """
    Compute the shortest move sequence which will make both ghosts disappear.

    Parameters
    ----------
    ghost1: []
        ordered list of moves which will make ghost1 disappear
    ghost2: []
        ordered list of moves which will make ghost2 disappear

    Returns
    -------
    seq : []
        move sequence of minimal length which will make both ghosts disappear
    """

    #initialize empty move array with |ghost1|+1 columns and |ghost2|+1 rows
    # note: (0,0) is a _ empty starting space
    

    ghost1 = ['_']+ghost1
    ghost2 = ['_']+ghost2

    moveArray = [[0 for i in range(len(ghost1))] for j in range(len(ghost2))]
    moveArray[0][0] = (0, '_', (-1,-1))

    # fill in the moveArray row by row
    for i in range(len(ghost2)): # for a given row
        for j in range(len(ghost1)): # for each element in that row
            
            #case 0: i=0 and j=0 means that we're in the starting slot
            if (i==0 and j==0):
                continue
            #case 1: i=0 means that there are no slots above
            elif i==0:
                # (Num. moves of left slot +1, letter of this col., index of left slot)
                moveArray[i][j] = (moveArray[i][j-1][0]+1, ghost1[j], (i,j-1))

            #case 2: j=0 means that there are no slots to the left
            elif j==0:
                # (Num. moves of above slot +1, letter of this row, indes of above slot)
                moveArray[i][j] = (moveArray[i-1][j][0]+1, ghost2[i], (i-1, j))


            else: # consider item to left, item above, and diagonal item (if letter are the same)
                # consider left, up, diagonal
                left = moveArray[i][j-1]
                up = moveArray[i-1][j]
                
                if ghost1[j] == ghost2[i]:
                    diagonal = moveArray[i-1][j-1]
                    # if we want the left parent
                    if (left[0] < up[0]) and (left[0] < diagonal[0]):
                        moveArray[i][j] = (left[0]+1, ghost1[j], (i,j-1))

                    # if we want the above parent
                    elif up[0] < diagonal[0]:
                        moveArray[i][j] = (up[0]+1, ghost2[i], (i-1,j))

                    else: #use diagonal
                        moveArray[i][j] = (diagonal[0]+1, ghost2[i], (i-1,j-1))

                else: # do not consider diagonal
                    if left[0] < up[0]:
                        moveArray[i][j] = (left[0]+1, ghost1[j], (i,j-1))
                    else:
                        moveArray[i][j] = (up[0]+1, ghost2[i], (i-1,j))

    return recoverPath2D(moveArray)


# res = double_kill(['A','B','B','B'], ['C','B','B','B','B'])
# print(res)

# #
# PART B: Fill in the code for part b
#

def triple_kill(ghost1, ghost2, ghost3):
    """
    Compute the shortest move sequence which will make all three ghosts disappear.

    Parameters
    ----------
    ghost1: []
        ordered list of moves which will make ghost1 disappear
    ghost2: []
        ordered list of moves which will make ghost2 disappear
    ghost3: []
        ordered list of moves which will make ghost3 disappear

    Returns
    -------
    seq : []
        move sequence of minimal length which will make all three ghosts disappear
    """
    
    raise NotImplementedError

