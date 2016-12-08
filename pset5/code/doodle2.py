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

    while currentIndex != (-1, -1):
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
    moveArray = [[None for i in range(len(ghost1)+1)] for j in range(len(ghost2)+1)]
    moveArray[0][0] = (0, '_', (-1,-1))

    # fill in the moveArray row by row
    for i in range(len(ghost2)+1): # for a given row
        for j in range(len(ghost1)+1): # for each element in that row
            
            #case 0: i=0 and j=0 means that we're in the starting slot
            if i==0 and j==0:
                continue
            #case 1: i=0 means that there are no slots above
            elif i==0:
                # (Num. moves of left slot +1, letter of this col., index of left slot)
                moveArray[i][j] = (moveArray[i][j-1][0]+1, ghost1[j-1], (i,j-1))

            #case 2: j=0 means that there are no slots to the left
            elif j==0:
                # (Num. moves of above slot +1, letter of this row, indes of above slot)
                moveArray[i][j] = (moveArray[i-1][j][0]+1, ghost2[i-1], (i-1, j))


            else: # consider item to left, item above, and diagonal item (if letter are the same)
                # if the letter of ghost 1 and ghost 2 are the same, we can combine moves
                if ghost1[j-1] == ghost2[i-1]:
                    possibleParentCoords = [(i,j-1), (i-1,j), (i-1,j-1)]
                # else just consider LEFT and ABOVE
                else:
                    possibleParentCoords = [(i, j-1), (i-1, j)]
                
                # figure out the best parent to inherit the path from
                shortestLength = float('inf')
                bestParentCoord = None
                
                for coord in possibleParentCoords:
                    if moveArray[coord[0]][coord[1]][0] < shortestLength:
                        bestParentCoord = coord

                # this means that we should use the letter to the left
                if bestParentCoord[0] == i:
                    letter = ghost1[j-1]
                # use the letter above
                else:
                    letter = ghost2[i-1]

                # finally, store the best move in the current slot
                moveArray[i][j] = (moveArray[bestParentCoord[0]][bestParentCoord[1]][0]+1, letter, bestParentCoord)

    pp(moveArray)
    return recoverPath2D(moveArray)


res = double_kill(['A','B','B','B'], ['C','B','B','B','B'])
print(res)

#
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

