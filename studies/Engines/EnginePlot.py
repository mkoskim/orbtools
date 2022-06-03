#!/usr/bin/env python3
###############################################################################
#
# Engine T-ve plot
#
###############################################################################

import os, sys
sys.path.append(os.path.abspath("."))

from orbtools.systems.solsystem import *
from orbtools.systems.exoplanets import *

#------------------------------------------------------------------------------

def getEngines(*selected):
    return [engines[name] for name in selected]

chemical = getEngines(
    "RS-25",        # LH2/LOX
    # "Vulcain",    # LH2/LOX
    # "Merlin 1C"   # RP1/LOX
    "Merlin 1D",    # RP1/LOX
    #"Raptor",       # CH4/LOX
    #"RD-263",
    "SSSRB",
)

electric = getEngines(
    "HiPEP",
    "NSTAR",
    "NEXT",
    "X3",
    "MPD",
)

#for e in electric: e.show()

nuclear  = getEngines("NERVA")

speculative = [
    Engine(name="SSE-1", ve = 14.43e3, F = 176e3)
]

#------------------------------------------------------------------------------
# Plot
#------------------------------------------------------------------------------

import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots()  # Create a figure containing a single axes.

#------------------------------------------------------------------------------

def get_y(e):
    return e.ve

ax.set_ylabel("Ve [km/s]")
ax.set_yscale('log')

yticks = [1_000, 2_500, 5_000, 10_000, 25_000, 50_000, 100_000]

ax.set_yticks(yticks)
ax.set_yticklabels([x*1e-3 for x in yticks])

#plt.axhline(y=4500, linestyle="dashed", linewidth=1, color="grey")

#------------------------------------------------------------------------------

def get_x(e):
    return e.F

ax.set_xlabel("Työntövoima [N]")
ax.set_xscale('log')
#ax.set_xlim(1000, 10_000_000_000)

xticks = [
    (       0.01, "10 mN"),
    (        0.1, "100 mN"),
    (          1, "1 N"),
    (         10, "10 N"),
    (        100, "100 N"),
    (      1_000, "1 kN"),
    (     10_000, "10 kN"),
    (    100_000, "100 kN"),
    (  1_000_000, "1 MN"),
    ( 10_000_000, "10 MN"),
    (100_000_000, "100 MN"),
]

ax.set_xticks([x[0] for x in xticks])
ax.set_xticklabels([x[1] for x in xticks])

#plt.title("Moottorit")
plt.minorticks_off()

#------------------------------------------------------------------------------

def plotEngines(selected, color = None):
    data_x = [get_x(e) for e in selected]
    data_y = [get_y(e) for e in selected]

    ax.scatter(data_x, data_y, color = color)

    for e in selected:
        txt, x, y = e.name, get_x(e), get_y(e)
        #print(x, y)
        ax.annotate(txt, xy = (x, y), xytext=(5, 0), textcoords="offset points")

plotEngines(chemical, "green")
plotEngines(electric, "blue")
plotEngines(nuclear, "yellow")
plotEngines(speculative, "red")

#------------------------------------------------------------------------------

plt.grid()
plt.show()
