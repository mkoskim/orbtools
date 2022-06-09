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

#------------------------------------------------------------------------------

class Energy:

  def __init__(self, name, orbit = None, center = None, dv=None):
    self.name = name
    if dv != None:
      self.dv = dv
      self.center = center
    else:
      self.orbit = orbit
      self.center = orbit.center

  def v_surface(self):
    return self.center.v_circular(self.center.radius)

  def getv(self):
    if self.dv >= 0:
      return self.center.v_escape() + self.dv
    else:
      return abs(self.orbit.v())

  def getE(self):
    if hasattr(self, "orbit"):
      return self.orbit.E()
    return self.dv ** 2

  def getEdv(self):
    E = self.getE()
    if E < 0:
      return -sqrt(abs(E))
    return sqrt(E)

  def getdv(self):

    surface = byAltitude(self.center, 0)

    if hasattr(self, "orbit"):
      transfer = Orbit(self.center, self.center.radius, self.orbit.r())
      dv = abs(transfer.v())
    else:
      dv = self.center.v_escape() + self.dv

    return dv - abs(surface.v())

  def getalt(self):
    if not hasattr(self, "orbit"): return None
    return self.orbit.altitude() * 1e-3

  def getP(self):
    if not hasattr(self, "orbit"): return None
    return self.orbit.P

  def gety(self):
    #return self.getdv()
    return self.getEdv()
    #return self.getE()
    #return self.getP()
    #return self.getv()
    #return self.getalt()

  def plot(self, ax, x):
    x, y = x, self.gety()

    if y != None:
      print("%s %.2f" % (self.name, y))
      ax.scatter(x, y)
      ax.annotate(
        self.name,
        (x, y),
        xytext=(7, -3),
        textcoords="offset points"
      )

#------------------------------------------------------------------------------

orbits = [
  #Energy("Surface", orbit = byAltitude(Earth, 0)),
  #Energy("LEO", orbit = byAltitude(Earth, 150e3)),
  Energy("ISS", orbit = byAltitude(Earth, 450e3)),
  Energy("GEO", orbit = byPeriod(Earth, Earth.rotate)),
  Energy("Moon", orbit = Moon.orbit),
]

orbitlines = [
  #Energy("1 h",  orbit = byPeriod(Earth, TasHours(1))),
  Energy("2 h",  orbit = byPeriod(Earth, TasHours(2))),
  Energy("12 h",  orbit = byPeriod(Earth, TasHours(12))),
  Energy("1 d",  orbit = byPeriod(Earth, TasDays(1))),
  Energy("30 d", orbit = byPeriod(Earth, TasDays(30))),
]

C3 = Energy("C3", center = Earth, dv=0)

energies = [
  Energy("MTO", center = Earth, dv=389.02),
  Energy("JTO", center = Earth, dv=3065.26)
]

#------------------------------------------------------------------------------

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.axes_grid1 import make_axes_locatable

fig, axOrbit = plt.subplots()  # Create a figure containing a single axes.

#fig, (axEnergy, axOrbit)=plt.subplots(2, sharex=True)

#fig = plt.figure()
#gs  = fig.add_gridspec(2, hspace=0, height_ratios=[1, 4])
#axEnergy, axOrbit = gs.subplots(sharex = True)

plt.subplots_adjust(left=0.2, right=0.8)  # adjust plot area

#------------------------------------------------------------------------------
# orbit axes

for orbit in orbits:
  orbit.plot(axOrbit, 0)

for e in energies:
  e.plot(axOrbit, 0)

for line in orbitlines:
  #line.plot(ax, 1)
  plt.axhline(line.gety(), linestyle="dashed", color="grey", linewidth=0.5)

axOrbit.set_xticks([])
axOrbit.set_yticks([line.gety() for line in orbitlines])
axOrbit.set_yticklabels([line.name for line in orbitlines])

#------------------------------------------------------------------------------
# energy axis

#axEnergy.yaxis.set_ticks_position("right")
#axEnergy.set_xlim(axOrbit.get_xlim())
#axEnergy.set_xticks([])
#axEnergy.spines["bottom"].set_visible(False)
#axOrbit.spines["top"].set_visible(False)

#for e in energies:
#  e.plot(axEnergy, 0)

#------------------------------------------------------------------------------

#print(axOrbit.get_ylim())
#axOrbit.set_ylim(axOrbit.get_ylim()[0], C3.gety())
#axEnergy.set_ylim(C3.gety(), axEnergy.get_ylim()[1]*1.001)

#print(axEnergy.get_ylim())
#print(axEnergy.get_yticks())
#ticks = [C3.gety()] + [x for x in axEnergy.get_yticks() if x > C3.gety()]
#axEnergy.set_yticks([int(x) for x in ticks])
#axEnergy.set_yticklabels([int(x) for x in ticks])
#axEnergy.set_yticks(list(axEnergy.get_yticks()) + [C3.gety()])
#axEnergy.set_yticks(np.linspace(*axEnergy.get_ylim(), 3, dtype="int"))

plt.axhline(C3.gety(), color="grey", linestyle="dashed")

#axOrbit.set_ylim(0, axOrbit.get_ylim()[1])
lmin, lmax = axOrbit.get_ylim()

axDV = axOrbit.twinx()
axDV.set_ylim((lmin, lmax))
axDV.set_yscale(axOrbit.get_yscale())
#ticks = sorted([x for x in axDV.get_yticks()] + [C3.gety()])
#axDV.set_yticks([int(x) for x in ticks])
#axDV.set_yticklabels([int(x) for x in ticks])
#axDV.set_ylim((lmin, lmax))

print(axOrbit.get_ylim())
print(axDV.get_ylim())
#print(ticks)

#------------------------------------------------------------------------------

#plt.grid()
plt.show()
