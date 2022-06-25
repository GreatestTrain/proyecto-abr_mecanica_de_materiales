import matplotlib.pyplot as plt
from sympy import lambdify
from numpy import linspace
from .symbols import _x


def plot_beam(beam, res=1000, division_ticks=8):
    x = linspace(0,beam.current,res)
    func1 = lambdify(_x, beam.sfd)
    func2 = lambdify(_x, beam.bmd)
    y1 = func1(x)
    y2 = func2(x)
    x_ticks = linspace(0,beam.current,division_ticks-1)

    fig, ax = plt.subplots(1,2,figsize=(12,4),subplot_kw={'axisbelow': False})
    ax[0].set_title("SFD")
    ax[0].plot(x,y1, "g-.")
    ax[0].axhline(0, color="k", linewidth=0.5)
    ax[0].fill_between(x,y1,0, color="yellow")
    ax[0].grid(c="k", alpha=0.33)
    ax[1].set_title("BMD")
    ax[1].plot(x,y2, "r-.")
    ax[1].axhline(0, color="k", linewidth=0.5)
    ax[1].fill_between(x,y2,0, color="limegreen")
    ax[1].grid(c="k", alpha=0.33)

    for plot in ax:
        plot.spines.left.set_position(('data', 0))
        plot.spines.right.set_color('none')
        plot.spines.bottom.set_position(('data', 0))
        plot.spines.top.set_color('none')
        plot.set_xticks(x_ticks)
        plot.set_xlabel("distancia (x)", loc="right")
    plt.show()