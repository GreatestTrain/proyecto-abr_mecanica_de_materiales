from sympy import sympify, Piecewise, solve, Eq, Symbol
from .symbols import _x, flex
from .forces import PointLoad, DistributedLoad, Moment, Force
from typing import Union
from IPython.display import Latex

class Structure:
    def __init__(self, kind):
        self.kind = kind
    
    def __str__(self) -> str:
        return "== Structure ==\n"

class Beam(Structure):
    def __init__(self, section=False):
        super().__init__(kind = "Beam")
        if section:
            self.section = section
        self._forces = []
        self._limits = []
        self._convention = 1
        # self.v_0 = 0
        # self.vd_0 = 0

    @property
    def convention(self) -> int:
        return self._convention
    @convention.setter
    def convention(self, value):
        if value in (1,2):
            self._convention = value
        else:
            raise TypeError("Avaible conventions (1 or 2)")

    @property
    def loads(self) -> list:
        return list(filter(lambda x: (x[0].load, x[1]) if isinstance(x[0],(PointLoad,DistributedLoad)) else None, zip(self._forces,self._limits)))

    @property
    def moments(self) -> list:
        return list(filter(lambda x: (x[0].moment, x[1]) if isinstance(x[0],Force) else None, zip(self._forces,self._limits)))
    
    @property
    def current(self) -> float:
        if self._limits:
            return self._limits[-1][1]
        else:
            return 0.0
    
    def addZero(self, to: Union[int, float]):
        self._forces.append(DistributedLoad(0))
        self._limits.append((self.current, to))

    def addPointLoad(self, load, point):
        if point > self.current:
            self.addZero(point)
        self._forces.append(load)
        self._limits.append((point, point))

    def addDistributedLoad(self, load, limits: Union[tuple, list]):
        if isinstance(limits, (tuple, list)) and limits[0] != limits[1]:
            if limits[0] > self.current:
                self.addZero(limits[0])
            self._forces.append(load)
            self._limits.append(limits)
        else:
            raise TypeError("limits must be tuple or a list with 2 elements")
    
    def addMoment(self, moment, point):
        if point > self.current:
            self.addZero(point)
        self._forces.append(moment)
        self._limits.append((point, point))

    def addForce(self, force, limits):
        if isinstance(force, PointLoad):
            self.addPointLoad(force, limits)
        elif isinstance(force, DistributedLoad):
            self.addDistributedLoad(force, limits)
        elif isinstance(force, Moment):
            self.addMoment(force, limits)

    @property
    def sfd(self, type: str = "Piecewise"):
        to_return = []
        ans = sympify(0)
        for load, limits in self.loads:
            if limits[0] == limits[1]:
                to_add = sympify(load.load + sympify(ans.subs(_x, _x-limits[0])))
            else:
                to_add = sympify(load.load.subs(_x, _x-limits[0]) + ans.subs(_x, _x-limits[0]))
                if limits[1] == self.current:
                    lm = (limits[0]<=_x) & (_x<=limits[1])
                else:
                    lm = (limits[0]<=_x) & (_x<limits[1])
                to_return.append((to_add.simplify(), lm))
            ans = to_add.simplify()
        # to_return.append((sympify(0), (self.current<=_x) & (_x<=self.current)))
        if self.convention == 1:
            to_return = [(-element[0], element[1]) for element in to_return]
        elif self.convention == 2:
            to_return = to_return
        if type == "Piecewise":
            return Piecewise(*to_return)
        elif type == "List":
            return to_return
        if type == "Piecewise":
            return Piecewise(*to_return)
        elif type == "List":
            return to_return
    
    @property
    def bmd(self, type: str = "Piecewise"):
        to_return = []
        ans = sympify(0)
        for load, limits in self.moments:
            if limits[0] == limits[1]:
                if isinstance(load, Moment):
                    to_add = sympify(load.moment + ans)
                elif isinstance(load, PointLoad):
                    to_add = sympify(load.moment.subs(_x, _x-limits[0]) + ans)
            else:
                to_add = sympify(load.moment.subs(_x, _x-limits[0]) + ans)
                if limits[1] == self.current:
                    lm = (limits[0]<=_x) & (_x<=limits[1])
                else:
                    lm = (limits[0]<=_x) & (_x<limits[1])
                to_return.append((to_add.simplify(), lm))
            
            ans = to_add.simplify()
        # to_return.append((sympify(0), (self.current<=_x) & (_x<=self.current)))
        if self.convention == 1:
            to_return = [(-element[0], element[1]) for element in to_return]
        elif self.convention == 2:
            to_return = to_return
        if type == "Piecewise":
            return Piecewise(*to_return)
        elif type == "List":
            return to_return
    
    # def deflex(self, convention:bool = True, type: str = "Piecewise"):
    #     ## solo voladizo
    #     to_return = []
    #     functions_2 = flex(2, self.bmd(convention = True, type="List"),_x)
    #     c2 = solve(Eq(0, functions_2[0][0].subs(_x, 0)))[0]
    #     functions = flex(1, self.bmd(convention = True, type="List"),_x)
    #     c1 = solve(Eq(0, functions[0][0].subs(_x, 0)))[0]
    #     return functions_2.subs({
    #         Symbol("C_1"): c1,
    #         Symbol("C_2"): c2
    #     })

    def zeros(self, kind:str="sfd", precision=0):
        if kind == "sfd":
            to_return = solve(Eq(self.sfd,0))
            to_return.append(self.sfd.subs(_x, 0))
            to_return.append(self.current)
        elif kind == "bmd":
            to_return = solve(Eq(self.bmd(),0))
        return to_return
    @property
    def bm_max(self):
        to_return: list = []
        for zero in self.zeros("sfd"):
            to_return.append(float(self.bmd.subs(_x, zero)))
        return max(to_return)
    @property
    def bm_min(self):
        to_return: list = []
        for zero in self.zeros("sfd"):
            to_return.append(float(self.bmd.subs(_x, zero)))
        return min(to_return)
    @property
    def sigma_max(self):
        return (self.bm_max * self.section.max_c) / self.section.I
    @property
    def sigma_min(self):
        return (self.bm_min * self.section.max_c) / self.section.I

    def sigma_report(self) -> str:
        s1 = str(round(self.sigma_max,3))
        s2 = str(round(solve(Eq(self.bmd, self.bm_max))[0],3))
        s3 = str(round(self.sigma_min,3))
        s4 = str(round(solve(Eq(self.bmd, self.bm_min))[0],3))
        return Latex(r"$\sigma_{\text{max}} = " + s1 + " \quad\longrightarrow x  = " + s2 + "$\n\n" + r"$\sigma_{\text{min}} = " +  s3 + " \quad\longrightarrow x  = " + s4 + "$")

    def __str__(self):
        return f"id: {hex(id(self))}\n== Structure ==\n- Beam -\nnº of loads: {len(self.loads)}\nnº of moments: {len(self.moments)}"

class Support:
    pass

class PinSupport(Support):
    pass
class RolledSupprot(Support):
    pass
class FixedSupport(Support):
    pass
class SpringSupport(Support):
    pass