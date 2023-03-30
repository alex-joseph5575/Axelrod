import random

def fib(n):
    if n in {0, 1}:
        return n
    return fib(n - 2) + fib(n - 1)

def getRandom(n):
    selectedNum = random.randrange(n + 1)
    if int(n) == int(selectedNum):
        return True
    return False