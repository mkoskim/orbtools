#!/usr/bin/env python3
###############################################################################
#
# Search for bodies in database and plot radiation intensities
#
###############################################################################

import os, sys
sys.path.append(os.path.abspath("."))

from orbtools.systems.solsystem import *
from orbtools.systems.exoplanets import *

#------------------------------------------------------------------------------

def get_xlegend(): return "Vuoden pituus (d)"

def get_x(planet):
    return planet.flux

def get_ylegend(): return "Kirkkaus"

def get_y(planet):
  return MtoEarth(planet.GM)

def isRadiatedPlanet(mass):
  if not mass.GM: return False
  if mass.GM < 0.005*GM_Earth: return False
  if not mass.flux: return False
  if mass.flux > 3.5: return False
  return True

#------------------------------------------------------------------------------

planets = list(filter(isRadiatedPlanet, masses.values()))
#planets = list(map(lambda name: masses[name], ["Earth", "Venus", "Mars", "Mercury"]))

#print("\n".join(list(map(lambda p: "%s: (%.2f, %.2f)" % (p.name, get_x(p), get_y(p)), planets))))

#sys.exit()

#------------------------------------------------------------------------------
# Plot
#------------------------------------------------------------------------------

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)

fig, ax = plt.subplots()  # Create a figure containing a single axes.

#ax.set_ylim(0, 20)
ax.set_yscale('log')
plt.axhline(y=0.25, color="grey", linestyle="dashed")
plt.axhline(y=4.00, color="grey", linestyle="dashed")

ax.set_xscale('log')
ax.set_xlim(1e-2, 5.15)
ax.invert_xaxis()
plt.axvline(x=2.00, color="green", linestyle="dashed")
plt.axvline(x=0.25, color="green", linestyle="dashed")

#ax.set_xticks([300, 200, 100, 50, 25, 10, 5])
#ax.set_xticks([5, 10, 25, 50, 100, 200, 300])
#ax.set_xticklabels([5, 10, 25, 50, 100, 200, 300])

data = list(
  map(
    lambda p: [p.name, get_x(p), get_y(p)],
    planets
  )
)

ax.scatter(
    list(map(lambda p: p[1], data)),
    list(map(lambda p: p[2], data)),
)

plt.grid()
plt.show()
