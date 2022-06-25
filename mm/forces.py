from sympy import sympify, integrate
from .symbols import _x

class Force:
    def __init__(self, kind):
        self.kind = kind
        self.load = 0
        self.moment = 0
    def __str__(self) -> str:
        if self.kind == 0:
            kind = "Point Load"
        elif self.kind == 1:
            kind = "Distributed Load"
        elif self.kind == 2:
            kind = "Moment"
        return f"id: {hex(id(self))}\n== Force ==\n - {kind} -\nload => {self.load}\nmoment => {self.moment}"
class PointLoad(Force):
    def __init__(self, load):
        super().__init__(kind = 0)
        if load == 0:
            self.load = 0
        else:
            self.load = sympify(load)
        self.moment = - integrate(self.load, _x)
class DistributedLoad(Force):
    def __init__(self, expr):
        super().__init__(kind = 1)
        self.load = integrate(expr, _x)
        self.moment = - integrate(self.load, _x)
class Moment(Force):
    def __init__(self, moment):
        super().__init__(kind = 2)
        self.moment = sympify(moment)