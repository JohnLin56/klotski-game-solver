import heapq
import sys
import queue
from queue import PriorityQueue
import copy


class Piece:
    def __init__(self, number, type, position, order):
        """ number = output number
            type = empty, single, caocao, 1x2(horizontal), 2x1(vertical)
            position = where the block is relative to its composition
            order = number distinguishing similar size pieces"""
        self.number = number
        self.type = type
        self.position = position
        self.order = order


def configure(input):
    """read from input file and output a starting state"""
    board = [[], [], [], [], []]
    r = 0
    empty_order = 0
    horizontal_order = 0
    vertical_order = 0
    caocao_order = 0
    single_order = 0
    while r != 5:
        c = 0
        while c != 4:
            if input[r][c] == 0:
                board[r].append(Piece(0, "empty", "center", empty_order))
                c += 1
                empty_order += 1
            elif input[r][c] == 1:
                if r == 0 or input[r - 1][c] != 1:
                    board[r].append(Piece(1, "caocao", "top left", caocao_order))
                    c += 1
                    board[r].append(Piece(1, "caocao", "top right", caocao_order))
                    c += 1
                else:
                    board[r].append(Piece(1, "caocao", "bottom left", caocao_order))
                    c += 1
                    board[r].append(Piece(1, "caocao", "bottom right", caocao_order))
                    c += 1
            elif input[r][c] == 7:
                board[r].append(Piece(4, "single", "center", single_order))
                c += 1
                single_order += 1
            else:
                if r == 0 or input[r - 1][c] != input[r][c]:
                    if r == 4 or input[r + 1][c] != input[r][c]:
                        board[r].append(Piece(2, "horizontal", "left", horizontal_order))
                        c += 1
                        board[r].append(Piece(2, "horizontal", "right", horizontal_order))
                        c += 1
                        horizontal_order += 1
                    else:
                        board[r].append(Piece(3, "vertical", "top", vertical_order))
                        c += 1
                        vertical_order = + 1
                else:
                    board[r].append(Piece(3, "vertical", "bottom", board[r - 1][c].order))
                    c += 1
        r += 1
    return board


def convert_state_to_string(state):
    """ convert a state to a string for dictionary """
    outcome = []
    for r in state:
        for c in r:
            outcome.append(c.number)
    return ''.join(str(i) for i in outcome)


def convert_state_to_int(state):
    """ convert a state to an int for explored set """
    outcome = []
    for r in state:
        for c in r:
            outcome.append(c.number)
    return int(''.join(str(i) for i in outcome))


def successor_states(state: list):
    """ return a list of succcessor stages """
    output = []
    empty_posi = []
    row = 0
    while row != 5: # find the empty postions first
        column = 0
        while column != 4:
            if state[row][column].number == 0:
                empty_posi.append([row, column])
            column += 1
        row += 1
    r = 0
    while r != 5:
        c = 0
        while c != 4:
            for empty in empty_posi:
                mod_state = copy.deepcopy(state)
                if r - empty[0] == 1 and c == empty[1]:  # piece is below empty
                    if state[r][c].type == "single":
                        holder = mod_state[r][c]
                        mod_state[r][c] = mod_state[empty[0]][c]
                        mod_state[empty[0]][c] = holder
                        output.append(mod_state)
                    elif state[r][c].type == "vertical" and state[r][c].position == "top":
                        holder = mod_state[r][c]
                        mod_state[r][c] = mod_state[r + 1][c]
                        mod_state[r + 1][c] = mod_state[empty[0]][c]
                        mod_state[empty[0]][c] = holder
                        output.append(mod_state)
                elif r - empty[0] == -1 and c == empty[1]:  # piece is above empty
                    if state[r][c].type == "single":
                        holder = mod_state[r][c]
                        mod_state[r][c] = mod_state[empty[0]][c]
                        mod_state[empty[0]][c] = holder
                        output.append(mod_state)
                    elif state[r][c].type == "vertical":
                        holder = mod_state[r][c]
                        mod_state[r][c] = mod_state[r - 1][c]
                        mod_state[r - 1][c] = mod_state[empty[0]][c]
                        mod_state[empty[0]][c] = holder
                        output.append(mod_state)
                elif c - empty[1] == 1 and r == empty[0]:  # piece is on the right of empty
                    if state[r][c].type == "single":
                        holder = mod_state[r][c]
                        mod_state[r][c] = mod_state[r][empty[1]]
                        mod_state[r][empty[1]] = holder
                        output.append(mod_state)
                    elif state[r][c].type == "horizontal":
                        holder = mod_state[r][c]
                        mod_state[r][c] = mod_state[r][c + 1]
                        mod_state[r][c + 1] = mod_state[r][empty[1]]
                        mod_state[r][empty[1]] = holder
                        output.append(mod_state)
                elif c - empty[1] == -1 and r == empty[0]:  # piece is on the left of empty
                    if state[r][c].type == "single":
                        holder = mod_state[r][c]
                        mod_state[r][c] = mod_state[r][empty[1]]
                        mod_state[r][empty[1]] = holder
                        output.append(mod_state)
                    elif state[r][c].type == "horizontal":
                        holder = mod_state[r][c]
                        mod_state[r][c] = mod_state[r][c - 1]
                        mod_state[r][c - 1] = mod_state[r][empty[1]]
                        mod_state[r][empty[1]] = holder
                        output.append(mod_state)
            # after treating empty as individual, check if empty are next to each other to allow bigger piece to move
            mod_state = copy.deepcopy(state)
            # first empty must be top left of second empty due to the nature of searching empty blocks. Therefore,
            # check whether the difference of rows is -1 while holding the column constant, or vice-versa.
            if empty_posi[0][1] - empty_posi[1][1] == -1 and empty_posi[0][0] == empty_posi[1][0]:
                # empty blocks are horizontally next to each other
                if r - empty_posi[0][0] == 1 and c == empty_posi[0][1]:  # empty blocks are above the pieces
                    if state[r][c].type == "horizontal" and state[r][c].position == "left":
                        holder = mod_state[r][c]
                        mod_state[r][c] = mod_state[empty_posi[0][0]][empty_posi[0][1]]
                        mod_state[empty_posi[0][0]][empty_posi[0][1]] = holder
                        holder = mod_state[r][c + 1]
                        mod_state[r][c + 1] = mod_state[empty_posi[1][0]][empty_posi[1][1]]
                        mod_state[empty_posi[1][0]][empty_posi[1][1]] = holder
                        output.append(mod_state)
                    elif state[r][c].type == "caocao" and state[r][c].position == "top left":
                        holder = mod_state[r][c]
                        mod_state[r][c] = mod_state[r + 1][c]
                        mod_state[r + 1][c] = mod_state[empty_posi[0][0]][empty_posi[0][1]]
                        mod_state[empty_posi[0][0]][empty_posi[0][1]] = holder
                        holder = mod_state[r][c + 1]
                        mod_state[r][c + 1] = mod_state[r + 1][c + 1]
                        mod_state[r + 1][c + 1] = mod_state[empty_posi[1][0]][empty_posi[1][1]]
                        mod_state[empty_posi[1][0]][empty_posi[1][1]] = holder
                        output.append(mod_state)
                elif r - empty_posi[0][0] == -1 and c == empty_posi[0][1]:  # empty blocks are below the pieces
                    if state[r][c].type == "horizontal" and state[r][c].position == "left":
                        holder = mod_state[r][c]
                        mod_state[r][c] = mod_state[empty_posi[0][0]][empty_posi[0][1]]
                        mod_state[empty_posi[0][0]][empty_posi[0][1]] = holder
                        holder = mod_state[r][c + 1]
                        mod_state[r][c + 1] = mod_state[empty_posi[1][0]][empty_posi[1][1]]
                        mod_state[empty_posi[1][0]][empty_posi[1][1]] = holder
                        output.append(mod_state)
                    elif state[r][c].type == "caocao" and state[r][c].position == "bottom left":
                        holder = mod_state[r][c]
                        mod_state[r][c] = mod_state[r - 1][c]
                        mod_state[r - 1][c] = mod_state[empty_posi[0][0]][empty_posi[0][1]]
                        mod_state[empty_posi[0][0]][empty_posi[0][1]] = holder
                        holder = mod_state[r][c + 1]
                        mod_state[r][c + 1] = mod_state[r - 1][c + 1]
                        mod_state[r - 1][c + 1] = mod_state[empty_posi[1][0]][empty_posi[1][1]]
                        mod_state[empty_posi[1][0]][empty_posi[1][1]] = holder
                        output.append(mod_state)
            elif empty_posi[0][0] - empty_posi[1][0] == -1 and empty_posi[0][1] == empty_posi[1][1]:
                # empty blocks are vertically next to each other
                if c - empty_posi[0][1] == 1 and r == empty_posi[0][0]:  # empty blocks are on the left
                    if state[r][c].type == "vertical" and state[r][c].position == "top":
                        holder = mod_state[r][c]
                        mod_state[r][c] = mod_state[empty_posi[0][0]][empty_posi[0][1]]
                        mod_state[empty_posi[0][0]][empty_posi[0][1]] = holder
                        holder = mod_state[r + 1][c]
                        mod_state[r + 1][c] = mod_state[empty_posi[1][0]][empty_posi[1][1]]
                        mod_state[empty_posi[1][0]][empty_posi[1][1]] = holder
                        output.append(mod_state)
                    elif state[r][c].type == "caocao" and state[r][c].position == "top left":
                        holder = mod_state[r][c]
                        mod_state[r][c] = mod_state[r][c + 1]
                        mod_state[r][c + 1] = mod_state[empty_posi[0][0]][empty_posi[0][1]]
                        mod_state[empty_posi[0][0]][empty_posi[0][1]] = holder
                        holder = mod_state[r + 1][c]
                        mod_state[r + 1][c] = mod_state[r + 1][c + 1]
                        mod_state[r + 1][c + 1] = mod_state[empty_posi[1][0]][empty_posi[1][1]]
                        mod_state[empty_posi[1][0]][empty_posi[1][1]] = holder
                        output.append(mod_state)
                elif c - empty_posi[0][1] == -1 and r == empty_posi[0][0]:  # empty blocks are on the right
                    if state[r][c].type == "vertical" and state[r][c].position == "top":
                        holder = mod_state[r][c]
                        mod_state[r][c] = mod_state[empty_posi[0][0]][empty_posi[0][1]]
                        mod_state[empty_posi[0][0]][empty_posi[0][1]] = holder
                        holder = mod_state[r + 1][c]
                        mod_state[r + 1][c] = mod_state[empty_posi[1][0]][empty_posi[1][1]]
                        mod_state[empty_posi[1][0]][empty_posi[1][1]] = holder
                        output.append(mod_state)
                    elif state[r][c].type == "caocao" and state[r][c].position == "top right":
                        holder = mod_state[r][c]
                        mod_state[r][c] = mod_state[r][c - 1]
                        mod_state[r][c - 1] = mod_state[empty_posi[0][0]][empty_posi[0][1]]
                        mod_state[empty_posi[0][0]][empty_posi[0][1]] = holder
                        holder = mod_state[r + 1][c]
                        mod_state[r + 1][c] = mod_state[r + 1][c - 1]
                        mod_state[r + 1][c - 1] = mod_state[empty_posi[1][0]][empty_posi[1][1]]
                        mod_state[empty_posi[1][0]][empty_posi[1][1]] = holder
                        output.append(mod_state)
            c += 1
        r += 1
    return output


def check_goal(state):
    """return boolean value for whether the state is a goal state"""
    return state[3][1].number == 1 and state[4][2].number == 1


def man_heu(state):
    # find top left 1 first, then calculate its position from top left 1 of goal state.
    r = 0
    position = []
    while r != 5:
        c = 0
        while c != 4:
            if state[r][c].number == 1:
                position.append((r, c))
            c += 1
        r += 1
    # solution position is always r = 3 and c = 1
    return abs(3 - position[0][0]) + abs(1 - position[0][1])


def self_created_heu(state):
    # similar to the Manhattan heuristic, we first find out the distance of the current caocao from the goal state.
    r = 0
    position = []
    while r != 5:
        c = 0
        while c != 4:
            if state[r][c].number == 1:
                position.append((r, c))
            c += 1
        r += 1
    # solution position is always r = 3 and c = 1
    man_distance = abs(3 - position[0][0]) + abs(1 - position[0][1])
    row = position[0][0] + 1
    column = position[0][1] + 1  # we are using the bottom right piece of caocao to detect any obstacle.
    obstacle = 0
    while row != 4 or column != 2:  # count how many pieces are in the way of moving to goal state.
        if row < 4:
            row += 1
        elif row > 4:
            row -= 1
        elif column < 2:
            column += 1
        elif column > 2:
            column -= 1
        if state[row][column].type != "empty":
            obstacle += 1
    return man_distance + obstacle


def dfs_search(start_state):
    p = {convert_state_to_string(start_state): "root"}
    front = [start_state]
    e = []
    while len(front) != 0:
        ex = front.pop()
        if convert_state_to_int(ex) not in e:
            e.append(convert_state_to_int(ex))  # add to explored list
            if check_goal(ex):
                break  # break out of loop when it is the goal state
            su = successor_states(ex)
            for one in su:
                if convert_state_to_int(one) not in e:
                    p[convert_state_to_string(one)] = convert_state_to_string(ex)
                    front.append(one)
    return (p, ex)


if __name__ == '__main__':
    filename = sys.argv[1]
    # store in list of list; first list = first line of file
    f = open(filename, "r")
    counter = 0
    inputfile = []
    while counter != 5:
        line = f.readline()
        inputfile.append([int(x) for x in line.strip()])
        counter += 1
    f.close()
    start = configure(inputfile)
    key = convert_state_to_string(start)
    path = {key: "root"}
    frontier = []
    explored = []
    output = []
    g = 0
    h = man_heu(start)
    entry_count = 0
    heapq.heappush(frontier, (g + h, entry_count, start))
    entry_count += 1
    while len(frontier) != 0:
        expand = heapq.heappop(frontier)
        if convert_state_to_int(expand[2]) not in explored:
            explored.append(convert_state_to_int(expand[2]))  # add to explored list
            if check_goal(expand[2]):
                break  # break out of loop when it is the goal state
            successor = successor_states(expand[2])
            for each in successor:
                if convert_state_to_int(each) not in explored:
                    parent = convert_state_to_string(expand[2])
                    path[convert_state_to_string(each)] = parent
                    g_count = 1
                    while path.get(parent) != "root":
                        g_count += 1
                        parent = path.get(
                            parent)  # trace back to root, so we know how many step it takes to get to this state
                    cost = g_count + man_heu(each)  # ######## change man_heu to self_created_heu
                    heapq.heappush(frontier, (cost, entry_count, each))
                    entry_count += 1
    answer = copy.deepcopy(expand[2])
    trace_back = convert_state_to_string(answer)
    solution = []
    while path[trace_back] != "root":
        solution.append(trace_back)
        trace_back = path[trace_back]
    solution.append(key)
    filename = sys.argv[3]
    f = open(filename, "w")
    f.write("Cost of the solution: " + str(expand[0]))
    count = len(solution)
    while count != 0:
        for char in range(0, len(solution[count - 1])):
            if char % 4 == 0:
                f.write("\n")
            f.write(solution[count - 1][char])
        count -= 1
        f.write("\n")
    f.close()
    filename = sys.argv[2]  ################################# dfs
    dfs = dfs_search(start)  # return (path, goal state)
    dfs_path = dfs[0]
    last_state = convert_state_to_string(dfs[1])
    step_count = 0
    dfs_solution = []
    while dfs_path[last_state] != "root":
        step_count += 1
        dfs_solution.append(last_state)
        last_state = dfs_path[last_state]
    dfs_solution.append(key)
    f = open(filename, "w")
    f.write("Cost of the solution: " + str(step_count))
    count = len(dfs_solution)
    while count != 0:
        for char in range(0, len(dfs_solution[count - 1])):
            if char % 4 == 0:
                f.write("\n")
            f.write(dfs_solution[count - 1][char])
        count -= 1
        f.write("\n")
    f.close()
