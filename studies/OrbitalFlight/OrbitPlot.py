#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
#
# Make a plot about escape velocity - object entering a system has its
# speed always over escape velocity
#
###############################################################################

import os, sys
sys.path.append(os.path.abspath("."))

from orbtools.systems.solsystem import *
from orbtools.systems.exoplanets import *
import matplotlib.ticker as ticker

#------------------------------------------------------------------------------

orbits = [
    (0, byAltitude(Earth, 500e3), "blue"),
    (0, byAltitude(Earth, 1000e3), "red"),
    (0, byAltitude(Earth, 2000e3), "green"),
    (1, byAltitude(Earth, 1000e3, 2000e3), "orange"),
]

def plotStatic(ax, orbit, x, color):
    ax.scatter(x, orbit.a - orbit.center.radius, color=color)
    if abs((orbit.r1-orbit.r2)/orbit.a) > 0.001:
        ax.plot(
            [x, x],
            [orbit.altitude(0), orbit.altitude(0.5)],
            color = color
        )

def plotTime(ax, orbit, color):
    t = np.linspace(0, 2, 2*100)
    alt = [orbit.altitude(t) for t in t]
    ax.plot(t, alt, color = color)

def solve(A, B):
    #rA³/rB³ = PA²/PB²
    #rA³ = PA²/PB² * rB³
    #PA² = (rA³/rB³) * PB³

    print("A=", A)
    print("B=", B)

    Ar = 1.0
    Br = (((B**2) / (A**2)) * (Ar ** 3)) ** (1/3.)

    print("Br=", Br)

    Tr = (Ar + Br)/2

    print("Tr=", Tr)

    TP = ((Tr**3) * (A**2)) ** (1/2.)

    print("TP     =", TP)
    print("Ttime  =", TP / 2.)
    print("(A+B)/4=", (A+B) / 4.)
    #print(Rb, A, P, P/2, (150+200)/4.)
    exit()

#solve(90, 23*60 + 56)
#solve(10, 5*90)

import matplotlib.pyplot as plt
import numpy as np
#from mpl_toolkits.axes_grid1 import make_axes_locatable

#fig, (axEnergy, axOrbit)=plt.subplots(2, sharex=True)

#fig, axStatic = plt.subplots()  # Create a figure containing a single axes.
#plt.subplots_adjust(left=0.2, right=0.8)  # adjust plot area

fig = plt.figure()
gs  = fig.add_gridspec(ncols=2, wspace=0.1, width_ratios=[1,3])
#axAlt, axStatic = gs.subplots(sharey = True)
axStatic, axAlt = gs.subplots()

plt.subplots_adjust(left=0.15, right=0.8)  # adjust plot area

for x, orbit, color in orbits:
    plotTime(axAlt, orbit, color)
    plotStatic(axStatic, orbit, x, color)

axAlt.yaxis.set_label_position("right")
axAlt.yaxis.tick_right()
axAlt.set_ylabel("Altitude [km]")
axAlt.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: "%.0f" % (x*1e-3)))
axAlt.set_ylim(0, axAlt.get_ylim()[1])
axAlt.set_xlim(0, 2)
axAlt.set_xticks([])
axAlt.set_xlabel("Time")
axAlt.grid()

axStatic.yaxis.set_label_position("left")
axStatic.yaxis.tick_left()
axStatic.set_ylabel("Period [min]")
axStatic.set_xticks([])
axStatic.set_yticks(axAlt.get_yticks())
axStatic.set_ylim(axAlt.get_ylim())
axStatic.yaxis.set_major_formatter(ticker.FuncFormatter(
    lambda x, pos: (x > 10e3) and "%.0f" % TtoMinutes(byAltitude(Earth, x).P) or ""
))
axStatic.grid()

lmin, lmax = axStatic.get_xlim()
axStatic.set_xlim(lmin-0.5, lmax+0.5)

#axAlt = axStatic.twinx()
#axAlt.yaxis.set_label_position("right")
#axAlt.yaxis.tick_right()
#axAlt.set_ylim(axStatic.get_ylim())
#axAlt.set_xlim(axStatic.get_xlim())

plt.show()
