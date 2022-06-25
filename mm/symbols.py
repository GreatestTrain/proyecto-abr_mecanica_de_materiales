from sympy import Symbol, integrate
# from symengine import Symbol

_x = Symbol("x")

def integrate_c(*args, **other):
    _C = Symbol("C_1")
    N = 1
    _C = Symbol('C_{' + f"{N}" + '}')
    while _C in (to_return := integrate(*args, **other)).free_symbols:
        N += 1
        _C = Symbol('C_{' + f"{N}" + '}')
    return to_return + _C


def flex(n, array, *args, **other):
    to_return = []
    for function, limits in array:
        if n==1:
            to_add = integrate_c(function, *args, **other)
        elif n==2:
            to_add = integrate_c(integrate_c(function, *args, **other))
        to_return.append(to_add, limits)
    return to_return