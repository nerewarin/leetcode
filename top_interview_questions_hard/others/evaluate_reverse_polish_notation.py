from collections import deque


def do(tokens):
    stack = deque()

    for t in tokens:
        try:
            res = int(t)
        except:
            right = stack.pop()
            left = stack.pop()
            res = eval(f'{left} {t} {right}')
            res = int(res)

        stack.append(res)

    return stack.pop()

assert do(["2","1","+","3","*"]) == 9
assert do(["4","13","5","/","+"]) == 6
assert do(["10","6","9","3","+","-11","*","/","*",в об"17","+","5","+"]) == 22