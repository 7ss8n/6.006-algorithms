###################################
##########  PROBLEM 4-4 ###########
###################################
#
# PART A: Fill in the code for part a
# 

from collections import deque

def printMatrix3D(m):
    for row in m:
        print(row)
    print("\n")


def latencies(N, L):
    """
    Compute the latencies between every pair of servers in the 6006LE network. 
    The servers are numbered with IDs from 0...N-1.

    Parameters
    ----------
    N : int
        number of servers in the network
    L : function 
        L(i,j), where i and j are server IDs, will output the latency for the router connection between i and j. Latency must be a positive float value, in the range [0, float('inf')]

    Returns
    -------
    A : [][] (list of lists)
        N by N matrix, where A[i][j] is the latency of the shortest walk from i to j.
    """
    # YOUR CODE HERE
    A = [[[0 for x in range(N)] for y in range(N)] for z in range(N+1)]

    #NOTE: order of indexing is z, x, y
    # intialize A with the weights of edges that we know
    for x in range(N):
        for y in range(N):
            A[0][x][y] = L(x,y)

    #printMatrix3D(A[0])

    for k in range(N):
        for u in range(N):
            for v in range(N):
                A[0][u][v] = min(A[0][u][v], A[0][u][k]+A[0][k][v])

    #printMatrix3D(A[0])
    return A[0]


    

#
# PART B: Fill in the code for part b
#
def conservative_latencies(N, L):
    """
    Compute the latencies between every pair of servers in the 6006LE network. 
    The servers are numbered with IDs from 0...N-1.

    Parameters
    ----------
    N : int
        number of servers in the network
    L : function 
            L(i,j), where i and j are server IDs, will output the latency for the router connection between i and j. Latency must be a positive float value, in the range [0, float('inf')]

    Returns
    -------
    B : [][] (list of lists)
        N by N matrix, where B[i][j] is the latency of the SECOND shortest walk from i to j.
    """
    # YOUR CODE HERE
    A = [[[0 for x in range(N)] for y in range(N)] for z in range(N+1)]

    #initialize the second-best matrix B to start out with infinity for every distance
    B = [[[float("inf") for x in range(N)] for y in range(N)] for z in range(N+1)]
    
    # parent[i][j] is a list of nodes that could be directly before j in the path from i to j
    # we have a list in place of a single number to allow for multiple shortest paths
    parent = [[0 for x in range(N)] for y in range(N)]

    #create one last array to keep track of when there are multiple best paths
    numBestPathsArray = [[1 for x in range(N)] for y in range(N)]

    #NOTE: order of indexing is z, x, y
    # intialize A with the weights of edges that we know
    for x in range(N):
        for y in range(N):
            A[0][x][y] = L(x,y)

            #also initialize our parent array
            if x == y or L(x,y) == float("inf"):
                parent[x][y] = -1
            else:
                parent[x][y] = x


    #printMatrix3D(A[0])
    for k in range(N):
        for u in range(N):
            for v in range(N):

                # if using the intermediate node produces a shorter path, update the shortest path in A
                if A[0][u][k]+A[0][k][v] < A[0][u][v]:

                    #If the previous best path from u to v is better than our second best path from u to v,
                    #update B to have the previous shortest path from A
                    if A[0][u][v] < B[0][u][v]:
                        B[0][u][v] = A[0][u][v]

                    # Now update the shortest path in A
                    A[0][u][v] = A[0][u][k]+A[0][k][v]

                    # now the node right before v in the best path from u->v is the node right before v in the best path from k->v
                    parent[u][v] = parent[k][v]

                    #since the path was improved, there is now only ONE shortest path from u->v
                    numBestPathsArray[u][v] = 1

                # if the new path we are considering has the SAME length as our shortest path so far, increment the number of shortest paths
                elif (A[0][u][k]+A[0][k][v] == A[0][u][v] and (k != u and k != v)):
                    numBestPathsArray[u][v] += 1

                #If k is not equal to u or v, consider 2 cases where the second shortest path could be improved using intermediate node k
                if (k != u and k != v):
                    #Case 1: consider adding 2SP from u to k and 1SP from k to v
                    if B[0][u][k]+A[0][k][v] < B[0][u][v]:
                        B[0][u][v] = B[0][u][k]+A[0][k][v]

                    #Case 2: consider adding 1SP from u to k and 2SP from k to v
                    if A[0][u][k]+B[0][k][v] < B[0][u][v]:
                        B[0][u][v] = A[0][u][k]+B[0][k][v]

    print("Num best paths")
    print(numBestPathsArray)


    # now build the shortest paths from each u to v
    shortestPathDict = {}
    for u in range(N):
        for v in range(N):
            start = u
            end = v

            #path is a deque to allow fast appending to left
            path = deque()
            while end != start:
                path.appendleft(end)
                end = parent[start][end]
            path.appendleft(start)
            shortestPathDict[(u,v)] = path

    # print("Shortest path dict")
    # print(shortestPathDict)
    #print(parent)
    #printMatrix3D(B[0])

    # now determine the shortest nontrivial cycle around each vertex in the graph
    shortestCycleDict = {}
    for startVertex in range(N):
        bestCycleLength = float("inf") #if no cycle is found, then a cycle will just have length infinity

        # for every other vertex, see if going to that vertex and back will result in a better cycle
        for otherVertex in range(N):
            if ((A[0][startVertex][otherVertex] + A[0][otherVertex][startVertex] < bestCycleLength) and (startVertex != otherVertex)):
                bestCycleLength = A[0][startVertex][otherVertex] + A[0][otherVertex][startVertex]

        # add the shortest cycle to the dictionary
        shortestCycleDict[startVertex] = bestCycleLength

    #print("Cycle dict")
    #print(shortestCycleDict)
    #For each vertex in every shortest path in A, see if adding a single nontrivial cycle will improve the second best path in B
    for i,j in shortestPathDict:
        
        # see if there are multiple shortest paths from i to j, in which case B should also contain the shortest path length
        if numBestPathsArray[i][j] > 1:
            B[0][i][j] = A[0][i][j]
            continue # the value in B can't get any smaller if this is the case

        # see if the shortest path plus a cycle at some vertex v improves our SBP
        shortestPath = shortestPathDict[(i,j)] # a sequence of vertices
        for v in shortestPath:
            if A[0][i][j] + shortestCycleDict[v] < B[0][i][j]:
                B[0][i][j] = A[0][i][j] + shortestCycleDict[v]

    return B[0]


def main():
    pass
    # N = 5
    # inf = float("inf")
    # cost_matrix =   [
    #                     [0,     1,      2,      2,      inf],
    #                     [1,     0,      inf,    3,      8],
    #                     [2,     inf,    0,      4,      1],
    #                     [2,     3,      4,      0,      1],
    #                     [inf,   8,      1,      1,      0]
    #                 ]
    # L = lambda x, y: cost_matrix[x][y]

    # latencies(5, L)



if __name__ == '__main__':
    main()
