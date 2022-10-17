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


def check_rows(l1, l2):
    return l1[-2] == l2[0] and l1[-1] == l2[1]


def generate_all_predecessors(N, M):
    res = [[]]
    for i in range(0, N * M):
        res = [[0] + c for c in res] + [[1] + c for c in res]

    return [[c[i * M:(i + 1) * M] for i in range(0, N)] for c in res]


def hash(c):
    s = ''.join([''.join(map(str, l)) for l in c])
    n = int(s, 2)
    return n


t.reset()

p = generate_all_predecessors(3, 3)
np = len(p)

cor = [None] * np
next_r = []
next_b = []


for c in p:
    cor[hash(c)] = c


for i in range(0, np):
    s = set()
    for j in range(0, np):
        if check_cols(cor[i], cor[j]):
            s.add(j)
    next_r.append(s)

    s = set()
    for j in range(0, np):
        if check_rows(cor[i], cor[j]):
            s.add(j)
    next_b.append(s)


t.time("Preparation done")


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


def get_next(input, i, j):
    neighbors = get_neighbors(input, i, j)

    if neighbors == 3:
        return 1
    elif neighbors == 2:
        return input[i][j]
    else:
        return 0


center = [
    {i for i in range(0, np) if get_next(cor[i], 1, 1) == 0},
    {i for i in range(0, np) if get_next(cor[i], 1, 1) == 1}
]


nw = [i for i in range(0, np) if get_next(cor[i], 0, 0) == 0]
nw = [i for i in nw if get_next(cor[i], 0, 1) == 0]
nw = [i for i in nw if get_next(cor[i], 1, 0) == 0]

n = [i for i in range(0, np) if get_next(cor[i], 0, 1) == 0]


# n = [i for i in n if any(check_cols(cor[j], cor[i]) for j in nw)]

# nw = [i for i in nw if any(check_cols(cor[i], cor[j]) for j in n)]

# w = [i for i in range(0, np) if get_next(cor[i], 1, 0) == 0]

# w = [i for i in w if any(check_rows(cor[j], cor[i]) for j in nw)]




def clone_pos(pos):
    N = len(pos)
    M = len(pos[0])

    clone = [[None] * M for i in range(0, N)]
    for i in range(0, N):
        for j in range(0, M):
            clone[i][j] = pos[i][j].copy()

    return clone


def get_index(N, M):
    idx = [(0, 0)]

    i = 0
    j = 0
    while i < N-1 or j < M-1:
        if j < M-1:
            j += 1

            for ii in range(0, i+1):
                idx.append((ii, j))

        if i < N-1:
            i += 1

            for jj in range(0, j+1):
                idx.append((i, jj))

    return idx



def find_predecessor(goal):
    N = len(goal)
    M = len(goal[0])

    pos = [[None] * M for i in range(0, N)]

    for i in range(0, N):
        for j in range(0, M):
            pos[i][j] = center[goal[i][j]]

    pos[0][0] = pos[0][0].intersection(nw)

    for j in range(1, M-1):
        pos[0][j] = pos[0][j].intersection(n)

    def search(pos, indexes, idx):
        NI = len(indexes)

        if idx == NI - 1:
            if len(pos[N-1][M-1]) > 0:
                return pos
            else:
                return None

        i, j = indexes[idx]

        for c in pos[i][j]:
            _pos = clone_pos(pos)
            _pos[i][j] = [c]

            if i < N-1:
                _pos[i+1][j] = _pos[i+1][j].intersection(next_b[c])

            if j < M-1:
                _pos[i][j+1] = _pos[i][j+1].intersection(next_r[c])

            r = search(_pos, indexes, idx+1)
            if r is not None:
                return r

        return None


    return search(pos, get_index(N, M), 0)








t.reset()

goal = [
    [0, 0, 1, 1, 0, 0],
    [1, 1, 1, 1, 0, 1],
    [0, 0, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 1]
]


res = find_predecessor(goal)

t.time("Found one predecessor")


for l in res:
    print(l)


