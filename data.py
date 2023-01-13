def dyel(n, m):
    return n % m == 0


def f(x, A):
    return x & 51 == 0 or ((x & 41 == 0) <= (x & A == 0))


for A in range(0, 500):
    tf = True
    for x in range(0, 500):
        if f(x, A) == False:
            tf = False
            break
    if tf:
        print(A)
