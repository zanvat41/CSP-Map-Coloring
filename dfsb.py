import sys
import copy
import math
import time
from collections import deque


#  number of search
global search
#  number arc pruning calls
global prune
search = 0
prune = 0


# Functions for plain DFSB
# Check if this var-color pair consistent with the constraints
def is_Consistent(var, color, assignment, Cons):
    for con in Cons:
        # Check every constraint that var involved in.
        # The given var cannot has the same color as the other var
        # in this constraint
        if var in con:
            # get the other var in the constraint
            if var == con[0]:
                var2 = con[1]
            else:
                var2 = con[0]
            if var2 in assignment:
                if (assignment[var2] == color):
                    return False
    return True


def Select_Unassigned_Var(Vars, assignment):
    for var in Vars:
        if not var in assignment:
            return var
    return -1


# Algorithm from lecture slide
def Plain_Backtracking(assignment, N, Vars, Cons, Colors):
    global search
    if len(assignment) == N:
        return assignment
    var = Select_Unassigned_Var(Vars, assignment)
    if var == -1:
        return 'failure'
    for color in Colors:
        if is_Consistent(var, color, assignment, Cons):
            search += 1
            assignment[var] = color
            result = Plain_Backtracking(assignment, N, Vars, Cons, Colors)
            if result != 'failure':
                return result
            assignment.pop(var)
    return 'failure'


# Functions for DFSB++
# The AC-3 function modified from the algorithm in lecture slides
def AC3(assignment, l, neighbors, domainsNew):
    while len(l) != 0:
        a = l.popleft()
        [remove, domainsNew] = Remove_Inconsistent_Values(a, domainsNew)

        # If you remove anythingfrom a variable, then
        # add all arcs that go into that variable back
        # into the queue
        if remove:
            global prune
            prune += 1
            if len(domainsNew[a[0]]) == 0:
                return (False, domainsNew)

            # List of neighbors of a[0] except a[1]
            neighborList = [item for item in neighbors[a[0]] if item != a[1]]
            for var in neighborList:
                b = [var, a[0]]
                if not var in assignment:
                    l.append(b)

    return (True, domainsNew)


def Remove_Inconsistent_Values(a, domainsNew):
    removed = False
    if len(domainsNew[a[1]]) == 1:
        c = domainsNew[a[1]][0]
        if c in domainsNew[a[0]]:
            domainsNew[a[0]].remove(c)
            removed = True
    return (removed, domainsNew)


def is_Consistent_Plus(var, c, assignment, neighbors):
    for var2 in neighbors[var]:
        if var2 in assignment and c == assignment[var2]:
            return False

    return True

# Order the domain values of the the variable with least constraining value comes first
def Order_Domain_Values(var, neighbors, domains):
    order = []
    for c in domains[var]:
        # When c rules out a value in the domain of a neighbor of var,
        # weight++
        weight = 0
        for var2 in neighbors[var]:
            if c in domains[var2]:
                weight += 1
        order.append([c, weight])
    # a value with lower weight is less constraining
    order = sorted(order, key=lambda x: x[1])
    colors = [item[0] for item in order]
    return colors


# Pick the most constrained variable
def Select_Unassigned_Plus(domains, assignment, N):
    min = math.inf
    var = -1
    for i in range(N):
        if (len(domains[i]) < min) and (i not in assignment):
            min = len(domains[i])
            var = i
    return var


# Algorithm from lecture slide
def Backtracking_Plus(assignment, N, neighbors, domains):
    global search
    if len(assignment) == N:
        return assignment

    var = Select_Unassigned_Plus(domains, assignment, N)

    if var == -1:
        return 'failure'

    colors = Order_Domain_Values(var, neighbors, domains)
    for c in colors:
        domainsNew = copy.deepcopy(domains)
        if is_Consistent_Plus(var, c, assignment, neighbors):
            domainsNew[var] = [item for item in domains[var] if item == c]
            array = []
            for var2 in neighbors[var]:
                a = [var2, var]
                if not var2 in assignment:
                    array.append(a)
                l = deque(array)
            [inference, dlist] = AC3(assignment, l, neighbors, domainsNew)
            if inference:
                search += 1
                assignment[var] = c
                domainsNew = dlist
                result = Backtracking_Plus(assignment, N, neighbors, domainsNew)
                if result != 'failure':
                    return result
                assignment.pop(var)

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

    if len(sys.argv) == 4:
        in_file = open(sys.argv[1], 'r')
        out_file = open(sys.argv[2], 'w')
        mode = int(sys.argv[3])
    else:
        print('Wrong number of arguments. Usage:\npython dfsb.py <input_file> <output_file> <mode_flag>')
        sys.exit()

    if mode != 0 and mode != 1:
        print('Illegal argument: <mode_flag> should be 0 or 1')
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

    # Create the color list
    for j in range(K):
        Colors.append(j)

    # Create the vars list
    for j in range(N):
        Vars.append(j)

    # print(str(N)+"\n"+str(M)+"\n"+str(K))
    # print(Cons)
    # print(Colors)
    # print(Vars)

    if mode == 0:
        startTime = time.time()
        result = Plain_Backtracking({}, N, Vars, Cons, Colors)
        print('The Algorithm took {0} second !'.format(time.time() - startTime))
    else:
        # The neighbors list is such that for a variable var
        # neighbor[var] is a list of its neighbors
        neighbors = [[] for k in range(N)]
        for item in Cons:
            neighbors[item[0]].append(item[1])
            neighbors[item[1]].append(item[0])
        # sort each neighbors[var]
        for k in range(N):
            j = list(set(neighbors[k]))
            neighbors[k] = j
        # The domains list is the color choices for each variable
        domains = [[] for k in range(N)]
        for i in range(0, N):
            for j in range(0, K):
                domains[i].append(j)

        startTime = time.time()
        result = Backtracking_Plus({}, N, neighbors, domains)
        print('The Algorithm took {0} second !'.format(time.time() - startTime))

        # Check if there are errors
        if not result is 'failure':
            for j in range(N):
                for k in neighbors[j]:
                    if result[k] == result[j]:
                        print(j, k, "conflict")

    print("search:", search)
    print("prune:", prune)
    # Print to output file
    if result is 'failure':
        out_file.write("No answer")
    else:
        for var in range(N):
            out_file.write(str(result[var]) + '\n')
    # print(result)

    in_file.close()
    out_file.close()