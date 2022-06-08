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

  def __init__(self, name, E=None, center = None, orbit = None):
    self.name = name
    if E != None:
      self.E = E
      self.center = center
    else:
      self.E = orbit.E()
      self.orbit = orbit
      self.center = orbit.center

  def v_surface(self):
    return self.center.v_circular(self.center.radius)

  def getv(self):
    if self.E >= 0:
      return self.center.v_escape() + sqrt(self.E)
    else:
      return abs(self.orbit.v())

  def getdv(self):
    surface = byAltitude(self.center, 0)
    if self.E < 0:
      transfer = Orbit(self.center, self.center.radius, self.orbit.r())
      return abs(transfer.v() - surface.v())
    return self.center.v_escape() + sqrt(self.E) - abs(surface.v())

  def getalt(self):
    if self.E >= 0: return None
    return self.orbit.altitude() * 1e-3

  def getE(self):
    E = self.E * 1e-6
    if E < 0:
      return -log(1 + abs(E))
    if E == 0:
      return 0
    return log(1 + E*1e4)

  def getP(self):
    if self.E >= 0: return None
    return self.orbit.P

  def gety(self):
    return self.getE()
    #return self.getP()
    #return self.getv()
    #return self.getdv()
    #return self.getalt()

  def plot(self, ax, x):
    x, y = x, self.gety()

    if y != None:
      print("%s %.2f" % (self.name, y))
      ax.scatter(x, y)
      ax.annotate(self.name, (x, y))

#------------------------------------------------------------------------------

orbits = [
  #Energy("Surface", orbit = byAltitude(Earth, 0)),
  #Energy("LEO", orbit = byAltitude(Earth, 150e3)),
  Energy("ISS", orbit = byAltitude(Earth, 450e3)),
  Energy("GEO", orbit = byPeriod(Earth, Earth.rotate)),
  Energy("Moon", orbit = Moon.orbit),
  Energy("MTO", center = Earth, E=12),
  Energy("JTO", center = Earth, E=80)
]

lines = [
  Energy("1 h",  orbit = byPeriod(Earth, TasHours(1))),
  Energy("1 d",  orbit = byPeriod(Earth, TasDays(1))),
  Energy("30 d", orbit = byPeriod(Earth, TasDays(30))),
  Energy("C3", center = Earth, E=0),
]

#------------------------------------------------------------------------------

import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots()  # Create a figure containing a single axes.

#------------------------------------------------------------------------------

#ax.set_yscale('log')

#------------------------------------------------------------------------------

for orbit in orbits:
  orbit.plot(ax, 0)

ax2 = ax.twinx()
ax2.set_ylim(ax.get_ylim())
ax.set_yticks([line.gety() for line in lines])
ax.set_yticklabels([line.name for line in lines])

for line in lines:
  #line.plot(ax, 1)
  plt.axhline(line.gety(), linestyle="dashed", color="grey", linewidth=0.5)

#------------------------------------------------------------------------------

#plt.grid()
plt.show()
