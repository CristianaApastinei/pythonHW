def compute_pow(x, y):
    return x ** y


def compute_fact(n):
    if n == 0:
        return 1
    return n * compute_fact(n - 1)


def compute_fib(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a
