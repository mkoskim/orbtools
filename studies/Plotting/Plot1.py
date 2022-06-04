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

S = Surface(Earth)

A = byAltitude(Earth, 1000e3)
B = byAltitude(Earth, 10000e3)
C = Orbit(Earth, A.a, B.a)

#A.info()
#B.info()
#C.info()
#exit()

#plotter.center(Earth)

#------------------------------------------------------------------------------

def plot(orbit):

    #plotter.orbit(S, style="solid")
    plotter.orbit(orbit)
    orbit.info()

    if(orbit.r1 == orbit.r2):
        plotter.pos(orbit, 0.00, color="green")
    else:
        plotter.event(orbit, 0.0, "Periapsis", offset = (-50, -10))
        plotter.event(orbit, 0.5, "Apoapsis", offset=(15, 0))
        plotter.pos(orbit, 0.00, color="red")
        plotter.pos(orbit, 0.50, color="green")

    plotter.speedmark(orbit, 0.00, color="green", scale=500)
    plotter.speedmark(orbit, 0.25, color="green", scale=500)
    plotter.speedmark(orbit, 0.50, color="green", scale=500)
    plotter.speedmark(orbit, 0.85, color="green", scale=500)

    plotter.slice(orbit, -0.03 - 0.05, -0.03, color="lightgrey")
    plotter.slice(orbit, 0.40, 0.40 + 0.05, color="lightgrey")
    #plotter.slice(C, 0.525, 0.6, color="lightgrey")
    #plotter.pos(C, 0.05)
    #plotter.pos(C, 0.55)

    #plotter.travel(C,  0.00, 0.25, color="green")
    #plotter.travel(C,  0.50, 0.75, color="green")

plot(B)
#plot(C)

#------------------------------------------------------------------------------

def plot():
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

#plot()

#------------------------------------------------------------------------------

def plot():

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

#plot()

#------------------------------------------------------------------------------

plotter.plt.grid()
plotter.show()
