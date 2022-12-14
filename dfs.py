#
# Utilities
#
import time
class Timer():
    def __init__(self):
        self.reset()

    def reset(self):
        self.start = time.time()
        self.events = {}
        self.current_events = {}

    def time(self, message = ''):
        duration = time.time() - self.start
        print(f"{message} ===> Duration: {duration}")
        self.reset()

    def start_event(self, evt):
        self.current_events[evt] = time.time()

    def stop_event(self, evt):
        if evt not in self.events:
            self.events[evt] = (0, 0)

        self.events[evt] = (self.events[evt][0] + time.time() - self.current_events[evt], self.events[evt][1] + 1)


    def print_events(self):
        for evt, v in self.events.items():
            print(f"{evt} - avg {v[0] / v[1]} - total {v[0]} - number {v[1]}")


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

# Clone an array of possibilities
def clone_pos(pos):
    return [l.copy() for l in pos]


# Generating
# * Hash to 3x3 cell correspondence -> cor
# * Propagation of possibilities to the right and the left -> next_r and next_b
# * Possibilities for 3x3 cells -> center[0] and center[1] (not aptly named...)
# * Boundary conditions -> nw, ne, se, sw, n, e, s, w
t.reset()

cor = generate_all_predecessors(3, 3)
np = len(cor)

next_r = []
next_b = []
next_d = []
next_rr = []

next_r = [[((i & 0b011011011) << 1) + o1 * 0b001000000 + o2 * 0b000001000 + o3 * 0b000000001 for o1 in [0, 1] for o2 in [0, 1] for o3 in [0, 1]] for i in range(0, np)]
next_b = [[((i & 0b000111111) << 3) + o for o in range(0, 8)] for i in range(0, np) ]

center = [
    {i for i in range(0, np) if get_next(cor[i], 1, 1) == 0},
    {i for i in range(0, np) if get_next(cor[i], 1, 1) == 1}
]


nw = set(range(0, np))
nw = {i for i in nw if get_next(cor[i], 0, 0) == 0}
nw = {i for i in nw if get_next(cor[i], 0, 1) == 0}
nw = {i for i in nw if get_next(cor[i], 1, 0) == 0}

ne = set(range(0, np))
ne = {i for i in ne if get_next(cor[i], 0, 2) == 0}
ne = {i for i in ne if get_next(cor[i], 1, 2) == 0}
ne = {i for i in ne if get_next(cor[i], 0, 1) == 0}

se = set(range(0, np))
se = {i for i in se if get_next(cor[i], 2, 2) == 0}
se = {i for i in se if get_next(cor[i], 2, 1) == 0}
se = {i for i in se if get_next(cor[i], 1, 2) == 0}

sw = set(range(0, np))
sw = {i for i in sw if get_next(cor[i], 2, 0) == 0}
sw = {i for i in sw if get_next(cor[i], 1, 0) == 0}
sw = {i for i in sw if get_next(cor[i], 2, 1) == 0}

n = {i for i in range(0, np) if get_next(cor[i], 0, 1) == 0}
e = {i for i in range(0, np) if get_next(cor[i], 1, 2) == 0}
s = {i for i in range(0, np) if get_next(cor[i], 2, 1) == 0}
w = {i for i in range(0, np) if get_next(cor[i], 1, 0) == 0}

t.time("Preparation done")


# Order in which we try the different cells ; we want to first try cells with not many possibilities
# Hence not being purely linear but as an "expanding square"
def get_index(N, M):
    # Linear version commented out, it is twice slower as the expanding square below
    # res = []
    # for i in range(0, N):
        # for j in range(0, M):
            # res.append((i, j))

    # return res

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


# From array of hashes to matrix of alive and dead cells
def format_result(res):
    N = len(res)
    M = len(res[0])
    res = [[cor[c]  for c in l] for l in res]
    return [res[0][0][i] + [res[0][j][i][2] for j in range(1, M)] for i in range(0, 3)] + [res[i][0][2] + [res[i][j][2][2]   for j in range(1, M)]   for i in range(1, N)]


def find_predecessor(goal):
    N = len(goal)
    M = len(goal[0])

    # Grid of possibilities
    pos = [[None] * M for i in range(0, N)]
    for i in range(0, N):
        for j in range(0, M):
            pos[i][j] = center[goal[i][j]]

    # Setting boundary conditions
    pos[0][0] = pos[0][0].intersection(nw)
    pos[0][-1] = pos[0][-1].intersection(ne)
    pos[-1][-1] = pos[-1][-1].intersection(se)
    pos[-1][0] = pos[-1][0].intersection(sw)

    for j in range(1, M-1):
        pos[0][j] = pos[0][j].intersection(n)
        pos[-1][j] = pos[-1][j].intersection(s)

    for i in range(1, N-1):
        pos[i][0] = pos[i][0].intersection(w)
        pos[i][-1] = pos[i][-1].intersection(e)

    # Recursively search following the expanding squares path
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

    # Iterative version of the above
    def search_iter():
        states = []
        indexes = get_index(N, M)
        NI = len(indexes)

        states.append((pos, 0))

        # u = Timer()




        while len(states) > 0:

            # u.start_event("state pop")

            state = states.pop()



            p = state[0]
            idx = state[1]
            i, j = indexes[idx]

            # u.stop_event("state pop")

            # u.start_event("if")
            if idx == NI - 1:
                if len(p[i][j]) > 0:
                    p[i][j] = list(p[i][j])[0]
                    return p

            # u.stop_event("if")

            for c in p[i][j]:


                # u.start_event("clone")
                _p = clone_pos(p)
                # u.stop_event("clone")


                _p[i][j] = c

                if i < N-1:
                    # u.start_event("inter")
                    _p[i+1][j] = _p[i+1][j].intersection(next_b[c])
                    # u.stop_event("inter")
                    if len(_p[i+1][j]) == 0:
                        continue

                if j < M-1:
                    # u.start_event("inter")
                    _p[i][j+1] = _p[i][j+1].intersection(next_r[c])
                    # u.stop_event("inter")
                    if len(_p[i][j+1]) == 0:
                        continue

                # if i < N-1 and j < M-1:
                    # _p[i+1][j+1] = _p[i+1][j+1].intersection(next_d[c])
                    # if len(_p[i+1][j+1]) == 0:
                        # continue

                # if j < M-2:
                    # _p[i][j+2] = _p[i][j+2].intersection(next_rr[c])
                    # if len(_p[i][j+2]) == 0:
                        # continue

                states.append((_p, idx+1))

        return None

    # res = search(pos, get_index(N, M), 0)
    res = search_iter()


    v = Timer()

    if res is None:
        return None
    else:
        return format_result(res)









t.reset()

goal = [
    [0, 0, 1, 1, 0, 0],
    [1, 1, 1, 1, 0, 1],
    [0, 0, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 1],
    [1, 1, 0, 1, 0, 1]
]


res = find_predecessor(goal)

t.time("Found one predecessor")


print_grid(goal)
print_grid(res)
print_grid(next(res))



# for i in range(0, 40):
    # res = find_predecessor(goal)


