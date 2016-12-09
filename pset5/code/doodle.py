###################################
##########  PROBLEM 5-4 ###########
###################################

from operator import itemgetter
from collections import deque


def pp(matrix):
    for i in range(len(matrix)):
        print(matrix[i])


def recoverPath2D(moveArray, ghost1, ghost2):
    """
    Starting from last move, follow parent pointers back until we get a parent points to (0,0), which is the start point
    """
    moveSeq = deque()

    i = len(moveArray)-1
    j = len(moveArray[0])-1

    while (i + j) > 0:
        if i==0: # we can only move left
            moveSeq.appendleft(ghost1[j])
            j-=1

        elif j==0: # we can only move up
            moveSeq.appendleft(ghost2[i])
            i-=1

        else: # consider left, up, diagonal
            leftParent = moveArray[i][j-1]
            aboveParent = moveArray[i-1][j]
            diagonalParent = moveArray[i-1][j-1]

            if ghost1[j] == ghost2[i]: # go diagonal
                moveSeq.appendleft(ghost2[i])
                i -= 1
                j -= 1
            elif leftParent < aboveParent: # go left
                moveSeq.appendleft(ghost1[j])
                j-=1
            else: # go up
                moveSeq.appendleft(ghost2[i])
                i-=1
    
    return moveSeq


def recoverPath3D(moveArray, ghost1, ghost2, ghost3):
    moveSeq = deque()

    k = len(moveArray)-1
    i = len(moveArray[0])-1
    j = len(moveArray[0][0])-1
    print(moveArray[k][i][j])

    while (i+j+k) > 0:
        if i==0 and j==0: # we can only move in k direction
            moveSeq.appendleft(ghost3[k])
            k-=1

        elif j==0 and k==0: # we can only move in i direction
            moveSeq.appendleft(ghost2[i])
            i-=1

        elif i==0 and k==0: # we can only move in j direction
            moveSeq.appendleft(ghost1[j])
            j-=1

        elif i==0: # we can only move in j or k directions
            if ghost1[j] == ghost3[k] and moveArray[k-1][i][j-1] <= moveArray[k-1][i][j] and moveArray[k-1][i][j-1] <= moveArray[k][i][j-1]: 
                # move diagonally if it is best 
                moveSeq.appendleft(ghost3[k])
                j-=1
                k-=1
            else: # move in j or k direction
                if moveArray[k][i][j-1] < moveArray[k-1][i][j]: # move in j
                    moveSeq.appendleft(ghost1[j])
                    j-=1
                else:
                    moveSeq.appendleft(ghost3[k]) # move in k
                    k-=1

        elif j==0: # we can only move in i or k directions
            if ghost2[i] == ghost3[k] and moveArray[k-1][i-1][j] <= moveArray[k-1][i][j] and moveArray[k-1][i-1][j] <= moveArray[k][i-1][j]: 
            # move diagonally
                moveSeq.appendleft(ghost3[k])
                i-=1
                k-=1
            else: # move in i or k direction
                if moveArray[k][i-1][j] < moveArray[k-1][i][j]: # move in i
                    moveSeq.appendleft(ghost2[i])
                    i-=1
                else:
                    moveSeq.appendleft(ghost3[k])
                    k-=1

        elif k==0: # we can only move in i or j directions
            if ghost1[j] == ghost2[i] and moveArray[k][i-1][j-1] <= moveArray[k][i-1][j] and moveArray[k][i-1][j-1] <= moveArray[k][i][j-1]: 
            # move diagonally
                moveSeq.appendleft(ghost2[i])
                j-=1
                i-=1
            else: # move in i or j direction
                if moveArray[k][i-1][j] < moveArray[k][i][j-1]: # move in i
                    moveSeq.appendleft(ghost2[i])
                    i-=1
                else:
                    moveSeq.appendleft(ghost1[j])
                    j-=1

        else: # we can go in any of 7 directions
            parent_j = moveArray[k][i][j-1]
            parent_i = moveArray[k][i-1][j]
            parent_k = moveArray[k-1][i][j]

            if ghost1[j] == ghost2[i] and ghost1[j] == ghost3[k]: # use ijk
                moveSeq.appendleft(ghost2[i])
                i-=1
                j-=1
                k-=1
            elif ghost1[j] == ghost2[i]: # use ij
                moveSeq.appendleft(ghost2[i])
                i-=1
                j-=1
            elif ghost1[j] == ghost3[k]: # use jk
                moveSeq.appendleft(ghost1[j])
                j-=1
                k-=1
            elif ghost2[i] == ghost3[k]: # use ik
                moveSeq.appendleft(ghost2[i])
                i-=1
                k-=1
            else: # use whichever of i, j, k is shortest
                if parent_i < parent_j and parent_i < parent_k: # use parent_i
                    moveSeq.appendleft(ghost2[i])
                    i-=1
                elif parent_j < parent_i and parent_j < parent_k: # use parent_j
                    moveSeq.appendleft(ghost1[j])
                    j-=1
                else:
                    moveSeq.appendleft(ghost3[k])
                    k-=1
    return moveSeq

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
    ghost1 = ['_'] + ghost1
    ghost2 = ['_'] + ghost2
    #initialize empty move array with |ghost1|+1 columns and |ghost2|+1 rows
    moveArray = [[0 for i in range(len(ghost1))] for j in range(len(ghost2))]

    # fill in the moveArray row by row
    for i in range(len(ghost2)): # for a given row
        for j in range(len(ghost1)): # for each element in that row
            
            #case 0: i=0 and j=0 means that we're in the starting slot
            if (i==0 and j==0):
                continue
            #case 1: i=0 means that there are no slots above
            elif i==0:
                # (Num. moves of left slot +1, letter of this col., index of left slot)
                moveArray[i][j] = moveArray[i][j-1]+1

            #case 2: j=0 means that there are no slots to the left
            elif j==0:
                # (Num. moves of above slot +1, letter of this row, indes of above slot)
                moveArray[i][j] = moveArray[i-1][j]+1

            else: # consider item to left, item above, and diagonal item (if letter are the same)
                # consider left, up, diagonal
                left = moveArray[i][j-1]
                up = moveArray[i-1][j]
                
                if ghost1[j] == ghost2[i]:
                    diagonal = moveArray[i-1][j-1]
                    # if we want the left parent
                    if (left < up) and (left < diagonal):
                        moveArray[i][j] = left+1

                    # if we want the above parent
                    elif up < diagonal:
                        moveArray[i][j] = up+1

                    else: #use diagonal
                        moveArray[i][j] = diagonal+1

                else: # do not consider diagonal
                    if left < up:
                        moveArray[i][j] = left+1
                    else:
                        moveArray[i][j] = up+1
    return recoverPath2D(moveArray, ghost1, ghost2)


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
    ghost1 = ['_']+ghost1
    ghost2 = ['_']+ghost2
    ghost3 = ['_']+ghost3

    # [ghost3][ghost2][ghost1] order of indexing

    moveArray = [[[0 for i in range(len(ghost1))] for j in range(len(ghost2))] for k in range(len(ghost3))]
    #moveArray[0][0][0] = (0, '_', (-1,-1,-1)) #add in the blank starting spot
    
    for k in range(len(ghost3)): # consider one ij plane at a time
        for i in range(len(ghost2)): # for a given row
            for j in range(len(ghost1)): # fill in the whole column of that row

                # ignore the origin 
                if i==0 and j==0 and k==0:
                    continue

                # parent must be from left
                elif k==0 and i==0:
                    moveArray[k][i][j] = moveArray[k][i][j-1]+1

                # parent must be above
                elif k==0 and j==0:
                    moveArray[k][i][j] = moveArray[k][i-1][j]+1

                # parent must be from behind (on k axis)
                elif i==0 and j==0:
                    moveArray[k][i][j] = moveArray[k-1][i][j]+1

                elif k==0: # we are in the front plane, so 
                    # consider: parent i, parent j, parent ij
                    if ghost1[j] == ghost2[i]:
                        moveArray[k][i][j] = 1 + min(moveArray[k][i-1][j], moveArray[k][i][j-1], moveArray[k][i-1][j-1])
                    else:
                        moveArray[k][i][j] = 1 + min(moveArray[k][i-1][j], moveArray[k][i][j-1])

                elif j==0: # we are in the left plane
                    # consider: parent i, parent k, parent ik
                    if ghost2[i] == ghost3[k]:
                        moveArray[k][i][j] = 1 + min(moveArray[k][i-1][j], moveArray[k-1][i][j], moveArray[k-1][i-1][j])
                    else:
                        moveArray[k][i][j] = 1 + min(moveArray[k][i-1][j], moveArray[k-1][i][j])

                elif i==0: # we are in the top plane
                    # consider: parent j, parent k, and parent jk
                    if ghost1[j] == ghost3[k]:
                        moveArray[k][i][j] = 1 + min(moveArray[k][i][j-1], moveArray[k-1][i][j], moveArray[k-1][i][j-1])
                    else:
                        moveArray[k][i][j] = 1 + min(moveArray[k][i][j-1], moveArray[k-1][i][j])

                else:
                    # all possible parents
                    parent_i = moveArray[k][i-1][j]
                    parent_j = moveArray[k][i][j-1]
                    parent_k = moveArray[k-1][i][j]
                    parent_ij = moveArray[k][i-1][j-1]
                    parent_jk = moveArray[k-1][i][j-1]
                    parent_ik = moveArray[k-1][i-1][j]
                    parent_ijk = moveArray[k-1][i-1][j-1]

                    if ghost1[j] == ghost3[k] and ghost1[j] == ghost2[i]: # then ijk is possible
                        moveArray[k][i][j] = 1 + min(parent_i, parent_j, parent_k, parent_ij, parent_jk, parent_ik, parent_ijk)
                    
                    elif ghost1[j] == ghost2[i]: #ij is possible
                        moveArray[k][i][j] = 1 + min(parent_i, parent_j, parent_k, parent_ij)

                    elif ghost2[i] == ghost3[k]: #ik is possible
                        moveArray[k][i][j] = 1 + min(parent_i, parent_j, parent_k, parent_ik)

                    elif ghost1[j] == ghost3[k]: #jk is possible
                        moveArray[k][i][j] = 1 + min(parent_i, parent_j, parent_k, parent_jk)

                    else: # just consider i, j, k
                        moveArray[k][i][j] = 1 + min(parent_i, parent_j, parent_k)      

    print("Matrix ans:", moveArray[len(ghost3)-1][len(ghost2)-1][len(ghost1)-1])
    return recoverPath3D(moveArray, ghost1, ghost2, ghost3)


moves1 = ['C', 'B', 'A']
moves2 = ['B', 'A', 'B']
moves3 = ['D', 'C', 'D']
student_res = triple_kill(moves1, moves2, moves3)
print(student_res)