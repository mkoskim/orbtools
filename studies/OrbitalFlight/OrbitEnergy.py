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
      return -solve_Emv(abs(E), 1.0, None)
    return sqrt(E)

  def getdv(self):
    if hasattr(self, "orbit"):
      return -(self.orbit.v_escape() - abs(self.orbit.v()))
    else:
      return +self.dv

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

ISS = byAltitude(Earth, 450e3)
GPS = byAltitude(Earth, 20_000e3)
GEO = byPeriod(Earth, Earth.rotate)

orbits = [
  #Energy("Surface", orbit = byAltitude(Earth, 0)),
  #Energy("LEO", orbit = byAltitude(Earth, 150e3)),
  Energy("Surface", orbit = Surface(Earth)),
  Energy("ISS", orbit = ISS),
  Energy("GPS", orbit = GPS),
  Energy("GEO", orbit = GEO),
  Energy("Moon", orbit = Moon.orbit),
]

orbitlines = [
  #Energy("1 h",  orbit = byPeriod(Earth, TasHours(1))),
  Energy("Surface", orbit = Surface(Earth)),
  Energy("2 h",  orbit = byPeriod(Earth, TasHours(2))),
  Energy("12 h",  orbit = byPeriod(Earth, TasHours(12))),
  Energy("1 d",  orbit = byPeriod(Earth, TasDays(1))),
  Energy("30 d", orbit = byPeriod(Earth, TasDays(30))),
  Energy("C3=0", center=Earth, dv=0),
]

C3 = Energy("C3", center = Earth, dv=0)

energies = [
  Energy("MTO", center = Earth, dv=389.02),
  Energy("JTO", center = Earth, dv=3065.26)
]

def printParams(name, orbit):
  print(name)
  print("   ", "E     =", fmteng(orbit.E(), "J"))
  print("   ", "- Ekin=", fmteng(orbit.Ekin(), "J"))
  print("   ", "- Epot=", fmteng(orbit.Epot(), "J"))
  print("   ", "v(Ekin)=", fmteng(solve_Emv(orbit.Ekin(), 1.0, None), "m/s"))
  print("   ", "v      =", fmteng(abs(orbit.v()), "m/s"))
  #print("   ", "r=", fmteng(orbit.r(), "m"))
  print("   ", "v(Epot)=", fmteng(solve_Emv(abs(orbit.Epot()), 1.0, None), "m/s"))
  print("   ", "v(esc) =", fmteng(orbit.v_escape(), "m/s"))
  print("   ", "v(diff)=", fmteng(solve_Emv(abs(orbit.E()), 1.0, None), "m/s"))
  print("   ", "dv(esc)=", orbit.v_escape() - abs(orbit.v()))

printParams("Earth surface", Surface(Earth))
printParams("ISS", ISS)
printParams("GEO", GEO)
#exit()

#------------------------------------------------------------------------------

import matplotlib.pyplot as plt
import numpy as np
#from mpl_toolkits.axes_grid1 import make_axes_locatable

fig, axOrbit = plt.subplots()  # Create a figure containing a single axes.

#fig, (axEnergy, axOrbit)=plt.subplots(2, sharex=True)

#fig = plt.figure()
#gs  = fig.add_gridspec(2, hspace=0, height_ratios=[1, 4])
#axEnergy, axOrbit = gs.subplots(sharex = True)

plt.subplots_adjust(left=0.3, right=0.7)  # adjust plot area

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

import matplotlib.ticker as ticker

axDV.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: "%+.0f km/s" % (x*1e-3)))

print(axOrbit.get_ylim())
print(axDV.get_ylim())
#print(ticks)

#------------------------------------------------------------------------------

#plt.grid()
plt.show()
