#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
#
# Orbtools unit tests: Testing Orbit() class
#
###############################################################################

import os, sys
sys.path.append(os.path.abspath("."))

from orbtools.systems.solsystem import *
from orbtools.systems.exoplanets import *

#------------------------------------------------------------------------------

A = Earth.orbit
B = Mars.orbit
C = Orbit(Sun, Earth.a, Mars.a)

#print("A", fmteng(A.E(), "J"))
#print("B", fmteng(B.E(), "J"))
#print("C(0.0):", fmteng(C.E(0), "J"), ":", fmteng(C.Epot(0), "J"), fmteng(C.Ekin(0), "J"))
#print("C(0.5):", fmteng(C.E(0.5), "J"), ":", fmteng(C.Epot(0.5), "J"), fmteng(C.Ekin(0.5), "J"))

#Sun.info()
#Earth.info()
#Mars.info()

#plotter.center(Earth)

#------------------------------------------------------------------------------

def plot():
    plotter.orbit(A)
    plotter.orbit(B)
    plotter.orbit(C)

    t = 0.5 * C.P / B.P
    print(fmttime(B.P/2))
    print(fmttime(t * B.P))

    B.arg = 360*(0.5 - t)

    print("Arg=", B.arg)

    plotter.travel(C, 0, 0.5, "blue")
    plotter.travel(B, 0, t, "green")
    plotter.pos(B, 0, "red")
    plotter.pos(C, 0, "red")

    t = 0.5 * C.P / A.P
    plotter.travel(A, 0, t, "green")

    plotter.event(A, 0.0, "A", offset=(-2.5, -12))
    plotter.event(C, 0.5, "R", offset=(-2.5, -12))

    plotter.event(B, 0.200, "T2")
    plotter.event(C, 0.125, "T1", offset=(10, 0))

plot()

#------------------------------------------------------------------------------

plotter.plt.grid()
plotter.show()
