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

sys.exit()

#Sun.info()
#Earth.info()
#Mars.info()

#plotter.center(Earth)

#------------------------------------------------------------------------------

plotter.orbit(A)
plotter.orbit(B)
plotter.orbit(C)

t = 0.5 * C.P / B.P
print(fmttime(B.P/2))
print(fmttime(t * B.P))

B.arg = 360*(0.5 - t)

print(B.arg)

plotter.travel(C, 0, 0.5, "blue")
plotter.travel(B, 0, t, "green")
plotter.pos(B, 0, "red")
plotter.pos(C, 0, "red")

t = 0.5 * C.P / A.P
plotter.travel(A, 0, t, "green")

#    plotter.travel(A, -0.33, 0.00, color="green")
#    plotter.travel(A,  0.00, 0.25, color="grey")
#    plotter.event(C, 0.0, "A")
#    plotter.travel(C, 0.00, 0.50, color="blue")
#    plotter.travel(C, 0.50, 0.75, color="grey")
#    plotter.event(C, 0.5, "A")
#    plotter.travel(B, 0.50, 0.83, color="green")

#plot1()

#------------------------------------------------------------------------------

def plot2():

    D = Orbit(Earth, C.r1 - 2000e3, C.r2 - 2000e3)
    E = Orbit(Earth, C.r1 - 4000e3, C.r2 - 4000e3)

    def speedmark(orbit, t, color):
        plotter.mark(orbit, t, color=color)
        plotter.speed(orbit, t, scale = 500, color=color)

    plotter.orbit(C)
    plotter.orbit(D)
    plotter.orbit(E)

    #plotter.event(C, 0.0, "Periapsis", offset = (-20, 15))
    #plotter.event(C, 0.5, "Apoapsis", offset=(-20, -15))
    #plotter.travel(C,  0.00, 0.25, color="green")
    speedmark(C, 0.00, color="green")
    speedmark(C, 0.25, color="green")
    speedmark(C, 0.50, color="green")
    speedmark(C, 0.85, color="green")

    speedmark(D, 0.00, color="green")
    speedmark(E, 0.00, color="green")

    #plotter.travel(C,  0.50, 0.75, color="green")

#plot2()

#------------------------------------------------------------------------------

plotter.plt.grid()
plotter.show()
