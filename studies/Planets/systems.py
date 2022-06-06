#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
#
# Some planetary systems. Lets try if we can help people making their own
# solar systems.
#
###############################################################################

import os, sys
sys.path.append(os.path.abspath("."))

from orbtools.systems.solsystem import *
from orbtools.systems.exoplanets import *

#------------------------------------------------------------------------------

def kepler():
    # Flux to period

    def solve_P(a):
        return sqrt(a ** 3.0)

    for flux in [4.0, 2.0, 1.0, 0.5, 0.25, 0.125]:
    #for r in [0.25, 0.5, 1.0, 2.0, 4.0, 8.0]:
        r = 1/(flux ** 0.5)
        #flux = 1/(r ** 2)
        P = solve_P(r)
        print(r ** 3)
        print("%.2f %.2f %.2f" % (flux, r, P))
        #P = solve_aPaP(1.0, 1.0, i, None)
        #a = solve_aPaP(1.0, 1.0, None, i)

        #print(i, "a -> P", i, P)
        #print(i, "P -> a", i, a)
    exit()

#kepler()

#------------------------------------------------------------------------------

import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots()  # Create a figure containing a single axes.

ax.set_ylim(0, 3)

def bodies(row, bodies):
    xy = [(1.0/body.flux, row) for body in bodies]
    x = [xy[0] for xy in xy]
    y = [xy[1] for xy in xy]

    ax.scatter(x, y)
    #for body in bodies:
    #    print("- %10s %7.2f %7.2f" % (body.name, body.flux, m2AU(body.orbit.a)))
    #print()

bodies(1, [
    Mercury, Venus, Earth, Mars
])

bodies(2, [
    masses["TRAPPIST-1c"],
    masses["TRAPPIST-1d"],
    masses["TRAPPIST-1e"],
    masses["TRAPPIST-1f"],
    masses["TRAPPIST-1g"],
])

plt.show()
