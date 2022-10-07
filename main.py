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



# cells = generate_all_predecessors(2, 3)
# res = [[], []]
# for c in cells:
    # n = get_neighbors(c, 0, 1)
    # if n == 3:
        # res[1].append(c)
    # elif n == 2:
        # res[c[0][1]].append(c)
    # else:
        # res[0].append(c)

# print(res)



# for c in res[0]:
    # print_grid(next(c))


# for c in n[1]:
    # print_grid(next(c))


# 1/0





def merge_possibility_in_line(pos_lines, cells):
    _res = []

    for c in cells:

        # print("===========================")
        # print_grid(c)

        for l in pos_lines:
            # print_grid(l)


            if l[0][-2] == c[0][0] and l[0][-1] == c[0][1] and l[1][-2] == c[1][0] and l[1][-1] == c[1][1]:
                _l = [l[0] + [c[0][2]], l[1] + [c[1][2]]]

                # l[0].append(c[0][2])
                # l[1].append(c[1][2])


                # print("MATCH")
                # print_grid(_l)
                # print("%%%%%%%%%%%%%")

                _res.append(_l)

    return _res


def find_predecessor(goal):
    N = len(goal)
    M = len(goal[0])

    goal = [[0 for i in range(0, M + 2)]] + [[0] + goal[i] + [0] for i in range(0,N)] + [[0 for i in range(0, M + 2)]]
    N += 2
    M += 2

    print_grid(goal)

    # Working on the first line

    pos_lines = nw[goal[0][0]]

    print(len(pos_lines))


    for i in range(1, M - 1):
        cells = n[goal[0][i]]

        pos_lines = merge_possibility_in_line(pos_lines, cells)

        print(len(pos_lines))




        # print(len(pos_lines))

    for t in pos_lines:
        # t = pos_lines[500]

        # print_grid(t)

        u = next(t)
        # print_grid(u)

        uu = ''.join(map(str, u[0]))


        if uu != '0000000':
            print_grid(t)
            print("NOOOOOES")




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


