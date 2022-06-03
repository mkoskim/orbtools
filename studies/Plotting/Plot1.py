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

A = byAltitude(Earth, 1000e3)
B = byAltitude(Earth, 10000e3)
C = Orbit(Earth, A.a, B.a)

#plotter.center(Earth)

#------------------------------------------------------------------------------

def plot1():
    plotter.orbit(A)
    plotter.orbit(B)
    plotter.orbit(C)

    plotter.travel(A, -0.33, 0.00, color="green")
    plotter.travel(A,  0.00, 0.25, color="grey")
    plotter.event(C, 0.0, "A")
    plotter.travel(C, 0.00, 0.50, color="blue")
    plotter.travel(C, 0.50, 0.75, color="grey")
    plotter.event(C, 0.5, "A")
    plotter.travel(B, 0.50, 0.83, color="green")

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

plot2()

#------------------------------------------------------------------------------

plotter.plt.grid()
plotter.show()
