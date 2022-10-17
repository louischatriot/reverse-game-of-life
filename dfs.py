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
    s = []
    for j in range(0, np):
        if check_cols(cor[i], cor[j]):
            s.append(j)
    next_r.append(s)

    s = []
    for j in range(0, np):
        if check_rows(cor[i], cor[j]):
            s.append(j)
    next_b.append(s)

print(len(next_b[234]))



    # t = 0

    # for cc in p:
        # t+=1
        # if check_cols(c, cc):
            # next_r[hash(c)].append(hash(cc))

        # if check_rows(c, cc):
            # next_b[hash(c)].append(hash(cc))


    # print(t)
    # print(len(next_r[0]))
    # 1/0

# print(len(next_r[0]))

# print(sum([len(i) for i in next_r]) / 512)



t.time("Preparation done")


# Generated using the following code and its variants
# cells = generate_all_predecessors(3, 3)
# nw = [[], []]
# for c in cells:
    # n = get_neighbors(c, 1, 1)
    # if n == 3:
        # nw[1].append(c)
    # elif n == 2:
        # nw[c[0][0]].append(c)
    # else:
        # nw[0].append(c)

