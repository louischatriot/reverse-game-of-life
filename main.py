import time
class Timer():
    def __init__(self):
        self.reset()

    def reset(self):
        self.start = time.time()

    def time(self, message = ''):
        duration = time.time() - self.start
        print(f"{message} ===> Duration: {duration}")
        self.reset()

t = Timer()

from data import nw, ne, sw, se, w, n, e, s, center




def print_grid(input):
    M = len(input[0])
    print('-' * (2 * M - 1))
    for l in input:
        print(' '.join(['X' if i == 1 else '.' for i in l]))
    print('-' * (2 * M - 1))


def get_neighbors(input, i, j):
    N = len(input)
    M = len(input[0])

    neighbors = 0
    for oi in [-1, 0, 1]:
        for oj in [-1, 0, 1]:
            if oi != 0 or oj != 0:
                if i + oi >= 0 and i + oi < N:
                    if j + oj >= 0 and j + oj < M:
                        neighbors += input[i + oi][j + oj]

    return neighbors


# Get number of neighbors for one cell (can be center, border or corner cell)
def get_cell_neighbor(cell, nw = False, ne = False, sw = False, se = False, w = False, n = False, e = False, s = False):
    N = len(input)
    M = len(input[0])

    if nw:
        if N != 2 or M != 2:
            raise ValueError("Wrong cell size")
        return get_neighbors(cell, 0, 0)


def generate_all_predecessors(N, M):
    res = [[]]
    for i in range(0, N * M):
        res = [[0] + c for c in res] + [[1] + c for c in res]

    return [[c[i * M:(i + 1) * M] for i in range(0, N)] for c in res]


def next(input):
    N = len(input)
    M = len(input[0])

    output = [[0 for i in range(0, M)] for i in range(0, N)]

    for i in range(0, N):
        for j in range(0, M):
            neighbors = get_neighbors(input, i, j)

            if neighbors == 3:
                output[i][j] = 1
            elif neighbors == 2:
                output[i][j] = input[i][j]
            else:
                output[i][j] = 0

    return output


def check_cols(N, l, c):
    for i in range(0, N):
        if l[i][-2] != c[i][0]:
            return False
        if l[i][-1] != c[i][1]:
            return False

    return True


# total_merge means we arrive at the end of the line so we don't increase grid length
def merge_possibility_in_line(pos_lines, cells, total_merge = False):
    N = len(cells[0])
    res = []

    # Actually slower than a big and with two cases (one for N=2 and one for N=3) but much cleaner
    # Without a function we can use this but it's slower
    # if [l[i][-2] for i in range(0, N)] == [c[i][0] for i in range(0,N)] and [l[i][-1] for i in range(0, N)] == [c[i][1] for i in range(0,N)]:
    for c in cells:
        for l in pos_lines:

            if check_cols(N, l, c):
                if not total_merge:
                    _l = [l[i] + [c[i][2]] for i in range(0, N)]
                    res.append(_l)
                else:
                    res.append(l)

    return res


def merge_lines(lines1, lines2, total_merge = False):
    res = []

    for l1 in lines1:
        for l2 in lines2:
            if l1[-2] == l2[0] and l1[-1] == l2[1]:
                if not total_merge:
                    l = [_l for _l in l1]
                    l.append(l2[2])
                    res.append(l)
                else:
                    res.append(l1)

    return res


def find_predecessor(goal):
    t.reset()

    N = len(goal)
    M = len(goal[0])

    goal = [[0 for i in range(0, M + 2)]] + [[0] + goal[i] + [0] for i in range(0,N)] + [[0 for i in range(0, M + 2)]]
    N += 2
    M += 2

    # All possible predecessors per cell in the goal
    pos = []
    pos.append([nw[goal[0][0]]] + [n[goal[0][j]] for j in range(1, M - 1)] + [ne[goal[0][-1]]])
    for i in range(1, N - 1):
        pos.append([w[goal[i][0]]] + [center[goal[i][j]] for j in range(1, M - 1)] + [e[goal[i][-1]]])
    pos.append([sw[goal[-1][0]]] + [s[goal[-1][j]] for j in range(1, M - 1)] + [se[goal[-1][-1]]])

    t.time("Calculated predecessors")

    # Removing obvious non matches by looking around (ahead only for now) the cell
    _pos = []
    for i in range(0, N):
        line = []
        for j in range(0, M):
            pos_cell = []
            for c in pos[i][j]:
                if j == M - 1:
                    pos_cell.append(c)
                else:
                    for cc in pos[i][j+1]:
                        if check_cols(len(c), c, cc):
                            pos_cell.append(c)
                            break

            line.append(pos_cell)
        _pos.append(line)

    pos = _pos


    t.time("Optimized predecessors")




    # Calculating line by line
    # for i in range(0, N):
        # lines = pos[i][0]

        # for j in range(1, M):
            # lines = merge_possibility_in_line(lines, pos[i][j], True if j == M - 1 else False)

        # if i == 0:
            # pos_grids = [[l for l in lines[i]] for i in range(0, len(lines))]
        # else:
            # pos_grids = merge_lines(pos_grids, lines, True if i == N - 1 else False)


        # print(len(pos_grids))


    # Expanding square technique
    i = 0
    j = 0
    pos_grids = pos[0][0]
    while i < N - 1 or j < M - 1:
        if j < M - 1:
            j += 1

            column = pos[0][j]
            for ti in range(1, i + 1):
                column = merge_lines(column, pos[ti][j], True if ti == N - 1 else False)


            pos_grids = merge_possibility_in_line(pos_grids, column, True if j == M - 1 else False)


        if i < j and i < N - 1:
            i += 1

            line = pos[i][0]
            for tj in range(1, j + 1):
                line = merge_possibility_in_line(line, pos[i][tj], True if tj == M - 1 else False)

            pos_grids = merge_lines(pos_grids, line, True if i == N - 1 else False)

        print(len(pos_grids))

    t.time("Calculated full predecessors")

    # Return first solution if any
    if len(pos_grids) == 0:
        return None
    else:
        return pos_grids[0]




# start = time.time()


# centers = center[0] + center[1]
# center_predecessors = { 0: [i for i in range(0, len(center[0]))], 1: [i for i in range(len(center[0]), len(centers))] }

# center_transitions = [[False] * len(centers) for i in range(0, len(centers))]
# for i in range(0, len(centers)):
    # for j in range(0, len(centers)):
        # if check_cols(3, centers[i], centers[j]):
            # center_transitions[i][j] = True



# goal = [0, 0, 0, 1, 1, 0, 0]
# M = len(goal)


# line = [[i] for i in center_predecessors[goal[0]]]

# for j in range(1, 2):
    # _line = []

    # for l in line:
        # for c in center_predecessors[goal[j]]:
            # if center_transitions[l[-1]][c]:
                # print("============================")
                # print_grid(centers[l[-1]])
                # print_grid(centers[c])



                # _line.append(l + [c])

    # line = _line

    # print(len(line))









# print(time.time() - start)

# 1/0






goal = [
    [0, 0, 1, 1, 0],
    [1, 1, 1, 1, 0],
    [0, 0, 1, 1, 1]
]


# goal = [
    # [1, 1, 1, 1, 1],
    # [1, 1, 1, 1, 1],
    # [1, 1, 1, 1, 1]
# ]


start = time.time()

res = find_predecessor(goal)

duration = time.time() - start
print(f"===> Duration: {duration}")



print_grid(goal)
print_grid(res)
print_grid(next(res))




# input = [
    # [0, 1, 0, 0],
    # [0, 0, 1, 0],
    # [1, 1, 1, 0],
    # [0, 0, 0, 0]
# ]

# print_grid(input)

# print("==========================")

# input = next(input)

# print_grid(input)

# print("==========================")

# input = next(input)

# print_grid(input)

# print("==========================")

# input = next(input)

# print_grid(input)

# print("==========================")

# input = next(input)


