# cleaner latencies template

###################################
##########  PROBLEM 4-4 ###########
###################################
#
# PART A: Fill in the code for part a
# 

from collections import deque

def printMatrix3D(m):
	"""
	Helper function to print out matrices in a nice way.
	"""
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

    # run floyd-warshal
    for k in range(N):
        for u in range(N):
            for v in range(N):
                A[0][u][v] = min(A[0][u][v], A[0][u][k]+A[0][k][v])

    return A[0]


def reconstructPaths(nextMatrix, N):
	"""
	Helper function to reconstruct paths given the next matrix
	Implementation from: https://en.wikipedia.org/wiki/Floyd%E2%80%93Warshall_algorithm#Path_reconstruction
	"""
	shortestPathDict = {}
	for u in range(N):
		for v in range(N):
			start = u
			end = v

			if nextMatrix[u][v] == None:
				return []
			path = [u]

			while start != end:
				start = nextMatrix[start][end]
				path.append(start)

			shortestPathDict[(u,v)] = path

	return shortestPathDict

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
    
    # initialize next_matrix to have value of Null in each element
    next_matrix = [[None for x in range(N)] for y in range(N)]

    # intialize A with the weights of edges that we know
    for x in range(N):
    	for y in range(N):
            A[0][x][y] = L(x,y)

            next_matrix[x][y] = y

    for k in range(N):
    	for u in range(N):
    		for v in range(N):
    			
    			# if k is the start or end node, do nothing
    			if k==u or k==v:
    				pass

    			else:
    				# if going through k could improve our best path
    				if A[0][u][k]+A[0][k][v] < A[0][u][v]:

    					# update B
    					B[0][u][v] = min(B[0][u][v], A[0][u][v], A[0][u][k]+B[0][k][v], B[0][u][k]+A[0][k][v])

    					# update A
    					A[0][u][v] = A[0][u][k]+A[0][k][v]

    					# now the node right before v in the best path from u->v is the node right before v in the best path from k->v
    					next_matrix[u][v] = next_matrix[u][k]

    				# if going through k would result in a path equal to our best path
    				elif A[0][u][k]+A[0][k][v] == A[0][u][v]:

    					# update B
    					# if there is a new shortest path of equal length, then the second shortest path length could be the minimum path length
    					B[0][u][v] = min(B[0][u][v], A[0][u][k]+B[0][k][v], B[0][u][k]+A[0][k][v], A[0][u][v])

    				# if going through k is worse than our current best path
    				elif A[0][u][k]+A[0][k][v] > A[0][u][v]:
    					# update B
    					B[0][u][v] = min(B[0][u][v], A[0][u][k]+B[0][k][v], B[0][u][k]+A[0][k][v], A[0][u][k]+A[0][k][v])

    #build a dictionary of shortest paths to iterate through, looking for cycles
    shortestPathDict = reconstructPaths(next_matrix, N)

    for i,j in shortestPathDict:
    	# see if the shortest path plus a cycle at some vertex v improves our SBP
    	shortestPath = shortestPathDict[(i,j)] # a sequence of vertices
    	for v in shortestPath:
    		if A[0][i][j] + B[0][v][v] < B[0][i][j]:
    			B[0][i][j] = A[0][i][j] + B[0][v][v]

    return B[0]


def main():
    pass

if __name__ == '__main__':
    main()
