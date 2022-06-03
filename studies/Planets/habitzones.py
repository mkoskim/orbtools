#!/usr/bin/env python3
###############################################################################
#
# Approximating habitable zones
#
###############################################################################

import os, sys
sys.path.append(os.path.abspath("."))

from orbtools.systems.solsystem import *
from orbtools.systems.exoplanets import *

#------------------------------------------------------------------------------
# Example stars to generate table
#------------------------------------------------------------------------------

examples = [
    #stars["F0"],
    stars["F4"],
    stars["F5"],
    stars["G0"],
    stars["G2"],
    stars["G5"],
    stars["K0"],
    stars["K5"],
    stars["M0"],
    stars["M1"],
    #stars["M5"],
    #stars["M9"],
]

#------------------------------------------------------------------------------
# Check prints
#------------------------------------------------------------------------------

def get_xlegend(): return "Vuoden pituus (d)"

def get_x(orbit):
    return TtoDays(orbit.P)

def get_ylegend(): return "Kirkkaus"

def get_y(star):
    #return log10(MtoSun(star.GM))
    return log10(star.L)
    #return star.L
    #return star.T

#------------------------------------------------------------------------------
# Check prints
#------------------------------------------------------------------------------

flux_Earth = Earth.flux
flux_Inner = flux_Earth * 2.00
flux_Outer = flux_Earth * 0.40

#------------------------------------------------------------------------------
# Generate table from example stars
#------------------------------------------------------------------------------

class HZ:

    def __init__(self, star):
        self.star = star
        self.inner = star.orbitByFlux(flux_Inner)
        self.earth = star.orbitByFlux(flux_Earth)
        self.outer = star.orbitByFlux(flux_Outer)

HZ_orbits = map(lambda star: HZ(star), examples)

#------------------------------------------------------------------------------

def printOut():
    print("Flux:",
        flux_Inner * const_solar,
        flux_Earth * const_solar,
        flux_Outer * const_solar
    )
    for zone in HZ_orbits:
        print("%3s\t%.0f\t%.0f\t%.1f" % (
            zone.star.sptype,
            TtoDays(zone.inner.P),
            TtoDays(zone.earth.P),
            TtoDays(zone.outer.P),
        ))

#printOut()

#------------------------------------------------------------------------------
# Plot
#------------------------------------------------------------------------------

import matplotlib.pyplot as plt
import numpy as np

from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)

fig, ax = plt.subplots()  # Create a figure containing a single axes.

data_y = []
data_x1 = []
data_x2 = []
data_x3 = []

#plt.title("Vuoden pituus")
#plt.ylabel(get_ylegend())
plt.xlabel(get_xlegend())

for index, zone in enumerate(HZ_orbits):
    #print(index, T_earth)
    data_y.append(get_y(zone.star))
    #data_y.append(zone.star.sptype)
    data_x1.append(get_x(zone.inner))
    data_x2.append(get_x(zone.earth))
    data_x3.append(get_x(zone.outer))

ax.fill_betweenx(data_y, data_x1, data_x2, alpha=.40, color="yellow")
ax.fill_betweenx(data_y, data_x2, data_x3, alpha=.25, color="green")
ax.plot(data_x1, data_y, color="orange")
ax.plot(data_x2, data_y, color="green")
ax.plot(data_x3, data_y, color="blue")

ax.set_xlim(0, 1000)
ax.xaxis.set_major_locator(MultipleLocator(100))
#ax.xaxis.set_minor_locator(MultipleLocator(100))

#------------------------------------------------------------------------------
# Spectral types
#------------------------------------------------------------------------------

spticks = list(
    map(lambda sp: [
        sp,
        get_y(stars[sp])
    ],
    ["F5", "G0", "K0", "K5", "M0"]
    )
)

ax.set_yticks(list(map(lambda sp: sp[1], spticks)))
ax.set_yticklabels(list(map(lambda sp: sp[0], spticks)))

#------------------------------------------------------------------------------
# Interesting points
#------------------------------------------------------------------------------

PoI = list(map(lambda name: [
        name,
        get_x(masses[name].orbit),
        get_y(masses[name].orbit.center),
    ],
    [
        "Venus", "Earth", "Mars",
        "Kepler-442b",
        "Kepler-62e", # "Kepler-62f",
        #"HD 192310b", "HD 192310c",
        #"61 Virginis d",
        #"54 Piscium b",
    ]
))

ax.scatter(
    list(map(lambda p: p[1], PoI)),
    list(map(lambda p: p[2], PoI)),
)

for point in PoI:
    txt, x, y = point[0], point[1], point[2]
    #ax.scatter(x, y)
    ax.annotate(txt, xy = (x, y), xytext=(5, 0), textcoords="offset points")

#ax.invert_yaxis()

plt.grid()
plt.show()
