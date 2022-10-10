from data import nw, ne, sw, se, w, n, e, s, center



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


def check_cols(l, c):
    N = len(l)

    for i in range(0, N):
        if l[i][-2] != c[i][0]:
            return False
        if l[i][-1] != c[i][1]:
            return False

    return True


# total_merge means we arrive at the end of the line so we don't increase grid length
def merge_on_col(pos_lines, cells, total_merge = False):
    N = len(cells[0])
    res = []

    # Actually slower than a big and with two cases (one for N=2 and one for N=3) but much cleaner
    # Without a function we can use this but it's slower
    # if [l[i][-2] for i in range(0, N)] == [c[i][0] for i in range(0,N)] and [l[i][-1] for i in range(0, N)] == [c[i][1] for i in range(0,N)]:
    for c in cells:
        for l in pos_lines:

            if check_cols(l, c):
                if not total_merge:
                    _l = [l[i] + c[i][2:] for i in range(0, N)]
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
                    l = [_l for _l in l1] + l2[2:]
                    res.append(l)
                else:
                    res.append(l1)

    return res


def final_merge_lines(lines1, lines2):
    for l1 in lines1:
        for l2 in lines2:
            if l1[-2] == l2[0] and l1[-1] == l2[1]:
                return [_l for _l in l1] + l2[2:]

    return None



def find_predecessor(goal):
    t.reset()

    N = len(goal)
    M = len(goal[0])

    goal = [[0 for i in range(0, M + 2)]] + [[0] + goal[i] + [0] for i in range(0,N)] + [[0 for i in range(0, M + 2)]]
    N += 2
    M += 2

    # motifs_center = {}
    # motifs_n = {}
    # motifs_s = {}

    # for a in [0, 1]:
        # for b in [0, 1]:
            # motifs_center[str(a) + str(b)] = merge_on_col(center[a], center[b])
            # motifs_n[str(a) + str(b)] = merge_on_col(n[a], n[b])
            # motifs_s[str(a) + str(b)] = merge_on_col(s[a], s[b])

    # t.time("Precalculated motifs")

    # All possible predecessors per cell in the goal
    pos = []
    pos.append([nw[goal[0][0]]] + [n[goal[0][j]] for j in range(1, M - 1)] + [ne[goal[0][-1]]])
    for i in range(1, N - 1):
        pos.append([w[goal[i][0]]] + [center[goal[i][j]] for j in range(1, M - 1)] + [e[goal[i][-1]]])
    pos.append([sw[goal[-1][0]]] + [s[goal[-1][j]] for j in range(1, M - 1)] + [se[goal[-1][-1]]])




    # pos = []
    # pos.append([nw[goal[0][0]]] + [motifs_n[str(goal[0][j]) + str(goal[0][j + 1])] for j in range(1, M - 1, 2)] + [ne[goal[0][-1]]])
    # for i in range(1, N - 1):
        # pos.append([w[goal[i][0]]] + [motifs_center[str(goal[i][j]) + str(goal[i][j + 1])] for j in range(1, M - 1, 2)] + [e[goal[i][-1]]])
    # pos.append([sw[goal[-1][0]]] + [motifs_s[str(goal[-1][j]) + str(goal[-1][j + 1])] for j in range(1, M - 1, 2)] + [se[goal[-1][-1]]])


    # N = len(pos)
    # M = len(pos[0])



    t.time("Calculated predecessors")

    # Removing obvious non matches by looking around (ahead only for now) the cell
    _pos = []
    for i in range(0, N):
        line = []
        for j in range(0, M):
            # Right look-ahead
            pos_cell = []
            for c in pos[i][j]:
                if j == M - 1:
                    pos_cell.append(c)
                else:
                    for cc in pos[i][j + 1]:
                        if check_cols(c, cc):
                            pos_cell.append(c)
                            break

            # Bottom look-ahead
            if i != N - 1:
                _pos_cell = pos_cell
                pos_cell = []
                for c in _pos_cell:
                    for cc in pos[i + 1][j]:
                        if c[-2] == cc[0] and c[-1] == cc[1]:
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
            # lines = merge_on_col(lines, pos[i][j], True if j == M - 1 else False)

        # if i == 0:
            # pos_grids = [[l for l in lines[i]] for i in range(0, len(lines))]
        # else:
            # pos_grids = merge_lines(pos_grids, lines, True if i == N - 1 else False)


        # print(len(pos_grids))


    # Expanding square technique
    def expanding_square_solve(pos):
        NP = len(pos)
        MP = len(pos[0])

        i = 0
        j = 0
        pos_grids = pos[0][0]
        while i < NP - 1 or j < MP - 1:
            if j < MP - 1:
                j += 1

                column = pos[0][j]
                for ti in range(1, i + 1):
                    column = merge_lines(column, pos[ti][j], True if ti == N - 1 else False)


                pos_grids = merge_on_col(pos_grids, column, True if j == M - 1 else False)


            if i < NP - 1:
                i += 1

                line = pos[i][0]
                for tj in range(1, j + 1):
                    line = merge_on_col(line, pos[i][tj], True if tj == M - 1 else False)

                pos_grids = merge_lines(pos_grids, line, True if i == N - 1 else False)

        return pos_grids


    def flip_i(m):
        return [m[i] for i in range(len(m) - 1, -1, -1)]


    def flip_j(m):
        return [[m[i][j] for j in range(len(m[i]) - 1, -1, -1)] for i in range(0, len(m))]


    def flip_ij(m):
        return [[m[i][j] for j in range(len(m[i]) - 1, -1, -1)] for i in range(len(m) - 1, -1, -1)]




    # pos_grids = expanding_square_solve(pos)

    c_i = N // 2
    c_j = M // 2

    pos_nw = [pos[i][0:c_j] for i in range(0, c_i)]
    pos_ne = [pos[i][c_j:] for i in range(0, c_i)]
    pos_sw = [pos[i][0:c_j] for i in range(c_i, N)]
    pos_se = [pos[i][c_j:] for i in range(c_i, N)]

    pos_ne = flip_j(pos_ne)
    pos_sw = flip_i(pos_sw)
    pos_se = flip_i(flip_j(pos_se))

    pg_nw = expanding_square_solve(pos_nw)
    pg_ne = expanding_square_solve(pos_ne)
    pg_sw = expanding_square_solve(pos_sw)
    pg_se = expanding_square_solve(pos_se)


    # Could merge in the reverse order to save these flips
    pg_ne = [flip_j(s) for s in pg_ne]
    pg_sw = [flip_i(s) for s in pg_sw]
    pg_se = [flip_ij(s) for s in pg_se]


    pg_n = merge_on_col(pg_nw, pg_ne)
    pg_s = merge_on_col(pg_sw, pg_se)

    res = final_merge_lines(pg_n, pg_s)

    t.time("Calculated full predecessors")

    # Return the solution if any
    return res

    # Return first solution if any
    # if len(pos_grids) == 0:
        # return None
    # else:
        # return pos_grids[0]




# start = time.time()


# centers = center[0] + center[1]
# center_predecessors = { 0: [i for i in range(0, len(center[0]))], 1: [i for i in range(len(center[0]), len(centers))] }

# center_transitions = [[False] * len(centers) for i in range(0, len(centers))]
# for i in range(0, len(centers)):
    # for j in range(0, len(centers)):
        # if check_cols(centers[i], centers[j]):
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
    [0, 0, 1, 1, 0, 0],
    [1, 1, 1, 1, 0, 1],
    [0, 0, 1, 1, 1, 1]
]

# goal = [
    # [1,1,1,1,1,1],
    # [1,1,1,1,1,1],
    # [1,1,1,1,1,1],
    # [1,1,1,1,1,1],
    # [1,1,1,1,1,1],
    # [1,1,1,1,1,1],
    # [1,1,1,1,1,1]
# ]


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


