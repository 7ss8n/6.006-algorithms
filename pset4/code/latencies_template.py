###################################
##########  PROBLEM 4-4 ###########
###################################
#
# PART A: Fill in the code for part a
# 

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
    B = [[[0 for x in range(N)] for y in range(N)] for z in range(N+1)]
    
    #NOTE: order of indexing is z, x, y
    # intialize A with the weights of edges that we know
    for x in range(N):
        for y in range(N):
            A[0][x][y] = L(x,y)
            B[0][x][y] = L(x,y)

    #printMatrix3D(A[0])
    for k in range(N):
        for u in range(N):
            for v in range(N):
                # if this is true, we should update A
                if A[0][u][k]+A[0][k][v] < A[0][u][v]:
                    A[0][u][v] = A[0][u][k]+A[0][k][v]


    



    printMatrix3D(B[0])
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
