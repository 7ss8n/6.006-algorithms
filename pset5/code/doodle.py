###################################
##########  PROBLEM 5-4 ###########
###################################

# def double_kill(ghost1, ghost2, memo = {}, parent = {}):
#     """
#     Compute the shortest move sequence which will make both ghosts disappear.

#     Parameters
#     ----------
#     ghost1: []
#         ordered list of moves which will make ghost1 disappear
#     ghost2: []
#         ordered list of moves which will make ghost2 disappear

#     Returns
#     -------
#     seq : []
#         move sequence of minimal length which will make both ghosts disappear
#     """

#     #base cases
#     if len(ghost1) == 1 and len(ghost2) == 1:
#         if ghost1[0]==ghost2[0]:
#             return 1
#         else:
#             return 2
#     if (len(ghost1) + len(ghost2)) == 1:
#         return 1

#     #check if subproblem has been solved already
#     if str((ghost1,ghost2)) in memo:
#         return memo[str((ghost1,ghost2))]

#     #recursive cases
#     else:
#         if len(ghost1) == 0:
#             result = 1 + double_kill(ghost1, ghost2[1:], memo)

#         elif len(ghost2) == 0:
#             result = 1 + double_kill(ghost1[1:], ghost2, memo)

#         elif ghost1[0] == ghost2[0]:
#             result = 1 + double_kill(ghost1[1:], ghost2[1:], memo)

#         else:
#             result = 1 + min(double_kill(ghost1, ghost2[1:], memo), double_kill(ghost1[1:], ghost2, memo))

#         memo[str((ghost1,ghost2))] = result
#         print("Subproblem:", result)
#         return result
# matrix = [[0 for i in ghost1] for j in ghost2]
def double_kill(ghost1, ghost2, memo = {}):
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
    #print("G1:", ghost1, "G2:", ghost2)
    #base cases
    if len(ghost1) == 1 and len(ghost2) == 1:
        if ghost1[0]==ghost2[0]:
            return ghost1
        else:
            return ghost1+ghost2

    # if either list is empty, just return the other list
    elif len(ghost1) == 0:
        memo[str((ghost1,ghost2))] = ghost2
        return ghost2

    elif len(ghost2) == 0:
        memo[str((ghost1,ghost2))] = ghost1
        return ghost1

    #check if subproblem has been solved already
    if str((ghost1,ghost2)) in memo:
        print("Found existing subproblem.")
        return memo[str((ghost1,ghost2))]

    #recursive cases: if there are elements left in both lists
    else:
        if ghost1[0] == ghost2[0]:
            result = ghost1[:1] + double_kill(ghost1[1:], ghost2[1:], memo)

        else:
            take_g1 = ghost1[:1] + double_kill(ghost1[1:], ghost2, memo)
            take_g2 = ghost2[:1] + double_kill(ghost1, ghost2[1:], memo)

            if len(take_g1) < len(take_g2):
                result = take_g1
            else:
                result = take_g2

        memo[str((ghost1,ghost2))] = result
        return result


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

