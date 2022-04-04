from heapq import heappush, heappop, heapify
from state import State
import timeit

initial_state = [7, 4, 2, 3, 1, 5, 0, 8, 6]
goal_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
goal_node = State
board_len = 9
board_side = 3
nodes_expanded = 0
max_search_depth = 0
max_frontier_size = 0

moves = list() # Untuk backtrace dan printresult
costs = set()

def ast(start_state):

    global max_frontier_size, goal_node, max_search_depth

    explored = set()
    heap = list()
    heapEntry = {}
    key = h(start_state)

    root = State(start_state, None, None, 0, 0, key)

    entry = (key, 0, root)

    heappush(heap, entry)

    heapEntry[root.map] = entry

    while heap:

        node = heappop(heap)
        # print(node[2].state) Kalau ingin melihat steps nya 
        explored.add(node[2].map)

        if node[2].state == goal_state:
            goal_node = node[2]
            return heap

        neighbors = expand(node[2]) # List of states

        for neighbor in neighbors:

            neighbor.key = neighbor.cost + h(neighbor.state)

            entry = (neighbor.key, neighbor.move, neighbor)

            if neighbor.map not in explored:

                heappush(heap, entry)

                explored.add(neighbor.map)

                heapEntry[neighbor.map] = entry

                if neighbor.depth > max_search_depth:
                    max_search_depth += 1

            elif neighbor.map in heapEntry and neighbor.key < heapEntry[neighbor.map][2].key:

                hindex = heap.index((heapEntry[neighbor.map][2].key,
                                     heapEntry[neighbor.map][2].move,
                                     heapEntry[neighbor.map][2]))

                heap[int(hindex)] = entry

                heapEntry[neighbor.map] = entry

                heapify(heap)

        if len(heap) > max_frontier_size:
            max_frontier_size = len(heap)


def ida(start_state):

    global costs

    threshold = h(start_state)

    while 1:
        response = dls_mod(start_state, threshold)

        if type(response) is list:
            return response
            break

        threshold = response

        costs = set()


def dls_mod(start_state, threshold):

    global max_frontier_size, goal_node, max_search_depth, costs

    explored, stack = set(), list([State(start_state, None, None, 0, 0, threshold)])
    while stack:
        node = stack.pop()
        # print(node.state) total expanded
        explored.add(node.map)
        if node.state == goal_state:
            goal_node = node
            return stack

        if node.key > threshold:
            costs.add(node.key)

        if node.depth < threshold:

            neighbors = reversed(expand(node))

            for neighbor in neighbors:
                if neighbor.map not in explored:

                    neighbor.key = neighbor.cost + h(neighbor.state)
                    stack.append(neighbor)
                    explored.add(neighbor.map)

                    if neighbor.depth > max_search_depth:
                        max_search_depth += 1

            if len(stack) > max_frontier_size:
                max_frontier_size = len(stack)

    return min(costs)


def expand(node):

    global nodes_expanded
    nodes_expanded += 1

    neighbors = list()

    neighbors.append(State(move(node.state, 1), node, 1, node.depth + 1, node.cost + 1, 0))
    neighbors.append(State(move(node.state, 2), node, 2, node.depth + 1, node.cost + 1, 0))
    neighbors.append(State(move(node.state, 3), node, 3, node.depth + 1, node.cost + 1, 0))
    neighbors.append(State(move(node.state, 4), node, 4, node.depth + 1, node.cost + 1, 0))

    nodes = list() #Nodes merupakan list of S   tates

    for neighbor in neighbors: 
        if neighbor.state:
            nodes.append(neighbor)

    return nodes


def move(state, position):

    new_state = state[:]

    index = new_state.index(0)

    if position == 1:  # Up

        if index not in range(0, board_side):

            temp = new_state[index - board_side]
            new_state[index - board_side] = new_state[index]
            new_state[index] = temp

            return new_state
        else:
            return None

    if position == 2:  # Down

        if index not in range(board_len - board_side, board_len):

            temp = new_state[index + board_side]
            new_state[index + board_side] = new_state[index]
            new_state[index] = temp

            return new_state
        else:
            return None

    if position == 3:  # Left

        if index not in range(0, board_len, board_side):

            temp = new_state[index - 1]
            new_state[index - 1] = new_state[index]
            new_state[index] = temp

            return new_state
        else:
            return None

    if position == 4:  # Right

        if index not in range(board_side - 1, board_len, board_side):

            temp = new_state[index + 1]
            new_state[index + 1] = new_state[index]
            new_state[index] = temp

            return new_state
        else:
            return None


def h(state):
    count = 0;
    for i in range(0,8):
        if state.index(i) != goal_state.index(i):
            count = count + 1
    return count


def backtrace(stateList):

    moves.clear()

    current_node = goal_node
    
    while initial_state != current_node.state:

        if current_node.move == 1:
            movement = 'Up'
        elif current_node.move == 2:
            movement = 'Down'
        elif current_node.move == 3:
            movement = 'Left'
        else:
            movement = 'Right'

        moves.insert(0, movement)

        stateList.append(current_node.state)
        
        current_node = current_node.parent

    stateList.append(current_node.state) 

    stateList.reverse()

    return moves

def printState(state):
    print("| {} {} {} |\n| {} {} {} | \n| {} {} {} |\n"
        .format(state[0], state[1], state[2], state[3], state[4], state[5], state[6], state[7], state[8]))

def printResult():

    global moves, nodes_expanded

    stateList = list()
    moves = backtrace(stateList)

    for states in stateList:
        printState(states)

    print("Path to goal: " + str(moves))
    print("\nCost of path: " + str(len(moves)))
    print("\nNumber of nodes expanded: " + str(nodes_expanded))
    nodes_expanded = 0



def main(): 

    print("A* Algorithm")
    
    startTime = timeit.default_timer()
    
    ast(initial_state)
    
    endTime = timeit.default_timer()
    
    printResult()
    print("\nThe time for the operation:" + str((endTime-startTime)))
    
    print("\nIDA* Algorithm")
    startTime = timeit.default_timer()

    ida(initial_state)
    
    endTime = timeit.default_timer()

    printResult()
    print("\nThe time for the operation:" + str((endTime-startTime)))





if __name__ == '__main__':
    main()
