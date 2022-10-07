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



# cells = generate_all_predecessors(3, 3)

# res = [[], []]
# for c in cells:
    # n = get_neighbors(c, 1, 1)
    # if n == 3:
        # res[1].append(c)
    # elif n == 2:
        # res[c[1][1]].append(c)
    # else:
        # res[0].append(c)

# print(res)



# for c in res[1]:
    # # print_grid(c)
    # # print_grid(next(c))
    # print(next(c)[1][1])

# 1/0





# for c in w[1]:
    # # print_grid(next(c))
    # print(next(c)[1][0])


# 1/0




# total_merge means we arrive at the end of the line so we don't increase grid length
def merge_possibility_in_line(pos_lines, cells, total_merge = False):
    N = len(cells[0])
    res = []

    # Checking N like this is ugly
    if N == 2:
        for c in cells:
            for l in pos_lines:
                if l[0][-2] == c[0][0] and l[0][-1] == c[0][1] and l[1][-2] == c[1][0] and l[1][-1] == c[1][1]:
                    if not total_merge:
                        _l = [l[0] + [c[0][2]], l[1] + [c[1][2]]]
                        res.append(_l)
                    else:
                        res.append(l)

    if N == 3:
        for c in cells:
            for l in pos_lines:
                if l[0][-2] == c[0][0] and l[0][-1] == c[0][1] and l[1][-2] == c[1][0] and l[1][-1] == c[1][1] and l[2][-2] == c[2][0] and l[2][-1] == c[2][1]:
                    if not total_merge:
                        _l = [l[0] + [c[0][2]], l[1] + [c[1][2]], l[2] + [c[2][2]]]
                        res.append(_l)
                    else:
                        res.append(l)

    return res


def find_predecessor(goal):
    N = len(goal)
    M = len(goal[0])

    goal = [[0 for i in range(0, M + 2)]] + [[0] + goal[i] + [0] for i in range(0,N)] + [[0 for i in range(0, M + 2)]]
    N += 2
    M += 2

    print_grid(goal)


    # goal[0] = goal[2]

    # print_grid(goal)

    # 1/0

    # First line
    # pos_lines = nw[goal[0][0]]

    # for j in range(1, M - 1):
        # cells = n[goal[0][j]]
        # pos_lines = merge_possibility_in_line(pos_lines, cells)


    # cells = ne[goal[0][-1]]
    # pos_lines = merge_possibility_in_line(pos_lines, cells, True)

    # Next lines except the last
    i = 1
    pos_lines = w[goal[i][0]]

    for j in range(1, M - 1):
        cells = center[goal[i][j]]
        pos_lines = merge_possibility_in_line(pos_lines, cells)

    cells = e[goal[i][-1]]
    pos_lines = merge_possibility_in_line(pos_lines, cells, True)


    print(len(pos_lines))

    1/0

    for t in pos_lines:
        # t = pos_lines[500]

        # print_grid(t)

        u = next(t)
        print(u[1])
        # print_grid(u)

        # if sum(u[0]) != 0:
            # print("NOOOOOES")
            # print_grid(t)
            # print_grid(u)
            # 1/0




goal = [
    [0, 0, 1, 1, 0],
    [1, 1, 1, 1, 0],
    [0, 0, 1, 1, 1]
]


find_predecessor(goal)





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


