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




def generate_all_predecessors(N, M):
    return [i for i in range(0, N * M)]


def get_neighbors(input, i, j, N, M):
    neighbors = 0

    input = input >> max(0, (M * (N - i - 2) + M - j - 2))

    res = 0
    res += input & 1
    input = input >> 1
    res += input & 1
    input = input >> 1
    res += input & 1
    input = input >> 1 + M - j - 2
    res += input & 1
    input = input >> 2
    res += input & 1
    input = input >> 1 + M - j - 2
    res += input & 1
    input = input >> 1
    res += input & 1
    input = input >> 1
    res += input & 1

    return res


def check_cols(a, b):
    N = 3
    ra = 0b011
    rb = 0b110

    for i in range(0, N):
        if a & ra != (b & rb) >> 1:
            return False
        ra = ra << 3
        rb = rb << 3

    return True





input = 0b010110111

r = get_neighbors(input, 1, 1, 3, 3)



a = 0b010110111
b = 0b100101110

N = 100000

t.reset()
for i in range(0, N):
    r = check_cols(a, b)

t.time("DONE")
1/0


# . X .     X . .
# X X .     X . X
# X X X     X X .




