import sys
import time
import math
import random


# Count the number of search steps in minconflicts
global count
count = 0


# Return a randomly chosen variable from the set of conflicted variables
def Pick_Var(assignment, neighbors):
    candidates = []
    # Generate a set of variables that has
    # conflict/conflicts with its neighbor/neighbors
    for i in range(N):
        for j in neighbors[i]:
            if assignment[i] == assignment[j]:
                candidates.append(i)
                break
    if(len(candidates) == 0):
        return -1
    return random.choice(candidates)


# Return the value for var that minimizes conflicts
def Pick_Value(var, assignment, neighbors, K):
    min = math.inf
    color = -1
    for c in range(K):
        conflicts = 0
        for var2 in neighbors[var]:
            if c == assignment[var2]:
                conflicts += 1
        if (conflicts < min):
            min = conflicts
            color = c
    return color


def minconflicts(assignment, neighbors, max_steps, K):
    global count
    for i in range(max_steps):
        count += 1
        conflicts = 0
        # Calculate the total conflicts
        for j in range(N):
            for k in neighbors[j]:
                if assignment[j] == assignment[k]:
                    conflicts += 1
        # if current_state is a solution
        if conflicts == 0:
            return assignment
        else:
            var = Pick_Var(assignment, neighbors)

            color = Pick_Value(var, assignment, neighbors, K)

            if var == -1 or color == -1:
                return 'failure'

            # adjust the algorithm to avoid plateaus or getting stuck in local depressions
            adjust = random.randint(0,10)
            if adjust <= 7:
                assignment[var] = color
            else:
                assignment[var] = random.randint(0,K - 1)
    return 'failure'


if __name__ == '__main__':

    in_file = ''
    out_file = ''
    mode = 0
    N = 0  # N variables
    M = 0  # M constraints
    K = 0  # K colors
    Cons = []
    Colors = []
    Vars = []

    if len(sys.argv) == 3:
        in_file = open(sys.argv[1], 'r')
        out_file = open(sys.argv[2], 'w')
    else:
        print('Wrong number of arguments. Usage:\npython minconflicts.py <input_file> <output_file> ')
        sys.exit()

    i = 0
    for line in in_file:
        line1 = line.split('\t')
        # Read the first line to get N, M, K
        if i == 0:
            # print(line1)
            N = int(line1[0])
            M = int(line1[1])
            K = int(line1[2])
        # Get the constraints
        elif i <= M:
            c1 = int(line1[0])
            c2 = int(line1[1])
            Cons.append([c1, c2])
        i += 1

    # The neighbors list is such that for a variable var
    # neighbor[var] is a list of its neighbors
    neighbors = [[] for k in range(N)]
    for item in Cons:
        neighbors[item[0]].append(item[1])
        neighbors[item[1]].append(item[0])
    # Set the number of steps allowed before giving up to be 100*N
    max_steps = 100*N
    # Generate random start state
    assignment={}
    for j in range(N):
        assignment[j] = random.randint(0,K - 1)
    # print(assignment)

    startTime = time.time()
    result = minconflicts(assignment, neighbors, max_steps, K)
    print('The Algorithm took {0} second !'.format(time.time() - startTime))

    # Check if there are errors
    if not result is 'failure':
        for j in range(N):
            for k in neighbors[j]:
                if result[k] == result[j]:
                    print(j, k, "conflict")

    if result is 'failure':
        out_file.write("No answer")
    else:
        for var in range(N):
            out_file.write(str(result[var]) + '\n')
    # print(result)
    print("steps:",count)

    in_file.close()
    out_file.close()