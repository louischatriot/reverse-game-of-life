
def print_grid(input):
    for l in input:
        print(' '.join(['X' if i == 1 else '.' for i in l]))


def next(input):
    N = len(input)
    M = len(input[0])

    output = [[0 for i in range(0, M)] for i in range(0, N)]

    for i in range(0, N):
        for j in range(0, M):
            neighbors = 0
            for oi in [-1, 0, 1]:
                for oj in [-1, 0, 1]:
                    if oi != 0 or oj != 0:
                        if i + oi >= 0 and i + oi < N:
                            if j + oj >= 0 and j + oj < M:
                                neighbors += input[i + oi][j + oj]

            if neighbors == 3:
                output[i][j] = 1
            elif neighbors in [2, 3]:
                output[i][j] = input[i][j]
            else:
                output[i][j] = 0

    return output








input = [
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [1, 1, 1, 0],
    [0, 0, 0, 0]
]

print_grid(input)

print("==========================")

input = next(input)

print_grid(input)

print("==========================")

input = next(input)

print_grid(input)

print("==========================")

input = next(input)

print_grid(input)

print("==========================")

input = next(input)


