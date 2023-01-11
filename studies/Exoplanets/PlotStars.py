#!/usr/bin/env python3
###############################################################################
#
# Test plots to see that star database seems fine
#
###############################################################################

import os, sys
sys.path.append(os.path.abspath("."))

from orbtools import *
from orbtools.systems.solsystem import *
import orbtools.systems.stars
import orbtools.systems.exoplanets

def FilterMass(mass):
  if not mass.GM: return False
  if not mass.radius: return False
  if mass.GM < 0.01 * GM_Earth: return False
  return True

def FilterStar(star):
  if not FilterMass(star): return False

  if not hasattr(star, "L"): return False
  if not star.L: return False

  #if star.sptype[:1] != "G": return False

  #if not star.GM: return False
  #if MtoSun(star.GM) > 2: return False

  #if not star.mag: return False

  #if not star.dist: return False
  #if m2ly(star.dist) > 1000: return False

  #if not star.radius: return False
  #if RtoSun(star.radius) > 5: return False

  #if star.L > 5: return False
  #refL = Star.MLR(MtoSun(star.GM))
  #if star.L > 1.5*refL: return False

  #if not star.T: return False
  #if star.T > 10000: return False

  return True

def FilterPlanet(planet):
  if not FilterMass(planet): return False
  if not planet.orbit: return False

  def FilterSystem(planet):
    star = planet.system
    if star.sptype[0] not in ["F", "G", "K"]: return False
    return True

  #if not FilterSystem(planet): return False
  #if not StarFilter(planet.orbit.center): return False

  if not planet.flux: return False
  #if planet.flux > 20: return False
  return True

def FilterSuperEarth(planet):
  if not FilterPlanet(planet): return False
  #if planet.GM < 0.5 * GM_Earth: return False
  if planet.GM > 40  * GM_Earth: return False
  return True

def FilterHabitable(planet):
  #if not FilterPlanet(planet): return False
  if not planet.flux: return False
  if planet.flux > 2.5: return False
  if planet.flux < 0.2: return False
  #if planet.GM < 0.3 * GM_Earth: return False
  #if planet.GM > 4.0 * GM_Earth: return False
  return True

#data = list(stars.values())
data = masses.values()

#stars["Gliese 1002"].info()
#stars["TRAPPIST-1"].info()

#data = list(filter(FilterMass, data))
#data = list(filter(FilterStar, data))
#data = list(filter(FilterPlanet, data))
#data = list(filter(FilterSuperEarth, data))
data = list(filter(FilterHabitable, data))

#TRAPPIST1 = stars["TRAPPIST-1"]
#TRAPPIST1.info()
#print(Star.RT2L(Sun.radius, Sun.T))
#print(Star.RT2L(TRAPPIST1.radius, TRAPPIST1.T))

print("Points:", len(data))

#data.sort(key=lambda s: s.flux)

#print([x.name for x in data])
for mass in data:
  print(mass.system.name, mass.system.sptype, "%.2f" % mass.system.T, "%.4f" % mass.system.L, mass.name, "%.2f" % MtoEarth(mass.GM), mass.flux)
  #print(mass.name, MtoJupiter(mass.GM), RtoEarth(mass.radius), mass.density)
  pass

#exit()

#for star in data:
#  print(star.name, RtoSun(star.radius), MtoSun(star.GM))

#------------------------------------------------------------------------------
#
# Plotting
#
#------------------------------------------------------------------------------

import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots()  # Create a figure containing a single axes.

#plt.subplots_adjust(left=0.15, right=0.85)  # adjust plot area

def set_yticks(ax, ticks, labels = None):
  if ticks and not labels: labels = ticks
  if ticks: ax.set_yticks(ticks)
  if labels: ax.set_yticklabels(labels)

def set_xticks(ax, ticks, labels = None):
  if ticks and not labels: labels = ticks
  if ticks: ax.set_xticks(ticks)
  if labels: ax.set_xticklabels(labels)

#------------------------------------------------------------------------------

def y_Mass(ticks = [0.1, 1.0, 10.0, 100.0, 500.0]):
  ymin = ticks[0]*0.5
  ymax = ticks[-1] * 2
  ax.set_ylabel("Massa (x Maa)")
  ax.set_ylim(ymin, ymax)
  ax.set_yscale('log')

  set_yticks(ax, ticks)

  ticks2 = [ Mars, Earth, Neptune, Jupiter, Sun]
  ticks2 = filter(lambda m: MtoEarth(m.GM) > ymin and MtoEarth(m.GM) < ymax, ticks2)
  ticks2 = list(ticks2)

  if len(ticks2):
    ax2 = ax.twinx()
    ax2.set_yscale('log')
    ax2.set_ylim(ax.get_ylim())
    set_yticks(ax2,
      [MtoEarth(x.GM) for x in ticks2],
      [x.name for x in ticks2]
    )


  return [MtoEarth(planet.GM) for planet in data]

def y_Radius(ticks):
  ymin = ticks[0]*0.5
  ymax = ticks[-1] * 2

  ax.set_ylabel("Säde (x Maa)")
  ax.set_ylim(ymin, ymax)
  ax.set_yscale('log')

  set_yticks(ax, ticks)

  ticks2 = [ Mars, Earth, Neptune, Jupiter, Sun]
  ticks2 = filter(lambda m: RtoEarth(m.radius) > ymin and RtoEarth(m.radius) < ymax, ticks2)
  ticks2 = list(ticks2)

  if len(ticks2):
    ax2 = ax.twinx()
    ax2.set_yscale('log')
    ax2.set_ylim(ax.get_ylim())
    set_yticks(ax2,
      [RtoEarth(x.radius) for x in ticks2],
      [x.name for x in ticks2]
    )

  return [RtoEarth(planet.radius) for planet in data]

def y_Density():
  ax.set_ylabel("Tiheys")
  ax.set_yscale('log')
  ax.set_ylim(ymin = 500, ymax = 12_000)

  set_yticks(ax, [1_000, 2_500, 5_000, 10_000])

  return [planet.density for planet in data]

#data_y = [MtoEarth(planet.GM) for planet in data]
#data_y = [planet.density for planet in data]
#data_y = [RtoSun(star.radius) for star in data]
#data_y = [float(star.L) for star in data]
#data_y = [float(star.mag) for star in data]

#------------------------------------------------------------------------------

def x_Mass(ticks = [0.1, 1.0, 10.0, 100.0, 1000.0, 10_000.0, 100_000, 1_000_000]):
  xmin = ticks[0]*0.5
  xmax = ticks[-1] * 2

  ax.set_xlabel("Massa (x Maa)")
  ax.set_xlim(xmin, xmax)
  ax.set_xscale('log')
  set_xticks(ax, ticks)

  ticks2 = [ Mars, Earth, Neptune, Jupiter, stars["M9"], Sun]
  ticks2 = filter(lambda m: MtoEarth(m.GM) > xmin and MtoEarth(m.GM) < xmax, ticks2)
  ticks2 = list(ticks2)

  if len(ticks2):
    ax2 = ax.twiny()
    ax2.set_xscale('log')
    ax2.set_xlim(ax.get_xlim())
    set_xticks(ax2,
      [MtoEarth(x.GM) for x in ticks2],
      [x.name for x in ticks2]
    )

  return [MtoEarth(planet.GM) for planet in data]

def x_Radius():
  ax.set_xlabel("Säde (x Maa)")
  ax.set_xlim(xmin = 0.1, xmax = RtoEarth(Jupiter.radius * 2))
  set_xticks(ax, [0.1, 1.0, 10.0, 100.0])
  ax.set_xscale('log')

  #ax2 = ax.twiny()
  #ax2.set_xscale('log')
  #ax2.set_xlim(ax.get_xlim())
  #set_xticks(ax,
  #  [1.0, MtoEarth(GM_Neptune), MtoEarth(GM_Jupiter), MtoEarth(GM_Jupiter)*80, MtoEarth(GM_Sun)],
  #  ["Earth", "Neptunus", "Jupiter", "Star", "Sun"]
  #)

  return [RtoEarth(planet.radius) for planet in data]

def x_Density():
  ax.set_xlabel("Tiheys")
  ax.set_xscale('log')
  ax.set_xlim(xmin = 500, xmax = 12_000)

  set_xticks(ax, [1_000, 2_500, 5_000, 10_000])
  ax.invert_xaxis()

  return [planet.density for planet in data]

def x_Period():
  ax.set_xlabel("Period (days)")
  ax.set_xlim(0.1, 5000)
  ax.set_xscale('log')

  set_xticks(ax, [1, 10, 100, 1000])

  return [TtoDays(planet.orbit.P) for planet in data]

def x_Flux():
  ax.set_xlabel("Flux (x Earth)")
  ax.set_xscale('log')
  ax.set_xlim(xmax = 20.0, xmin = 0.01)
  ax.set_xticks([10, 1.0, 0.1, 0.01])
  ax.set_xticklabels([10, 1.0, 0.1, 0.01])
  ax.invert_xaxis()

  flux_lim = [2.0, 1.0, 0.396]
  plt.axvline(x = flux_lim[0], color="red")
  plt.axvline(x = flux_lim[1], color="green")
  plt.axvline(x = flux_lim[2], color="blue")

  return [planet.flux for planet in data]

#data_x = [TtoDays(planet.orbit.P) for planet in data]
#data_x = [m2ly(star.dist) for star in data]
#data_x = [MtoSun(star.GM) for star in data]

#------------------------------------------------------------------------------

#data_y = y_Radius([1.0, 10.0, 100.0, 1000.0]) # Stars + planets
#data_y = y_Radius([1.0, 10.0, 20.0]) # Planets
#data_y = y_Mass()
data_y = y_Mass([0.1, 1.0, 2.0, 4.0, 10.0, 25.0, 100.0, 250.0]) # Planets
#data_y = y_Mass([1.0, 5.0, 10.0, 20.0]) # Superearths
#data_y = y_Density()

#data_x = x_Mass() # Planets and stars
#data_x = x_Mass([0.05, 1.0, 4.0, 10.0, 20.0, 100.0, 1000.0])
#data_x = x_Mass([1.0, 2.0, 5.0, 10.0, 20.0]) # Superearths
#data_x = x_Radius()
#data_x = x_Period()
data_x = x_Flux()
#data_x = x_Density()

#print(data_x)
#print(data_y)

#------------------------------------------------------------------------------

#ax.scatter(data_x, data_y, marker=".", s = 1.0)
ax.scatter(data_x, data_y, marker=".")

#ax.set_xlim(-0.5, len(stars)-0.5)
#ax.set_xticks(range(len(stars)))
#ax.set_xticklabels(stars)

#for x in range(len(stars)):
#    plt.axvline(x, linestyle="dashed", color="grey", linewidth=0.5)

#ax.invert_yaxis()
#ax.set_yscale('log')
#yticks = [8.0, 4.0, 2.0, 1.0, 0.5, 0.25, 0.125]
#ax.set_yticks(yticks)
#ax.set_yticklabels(yticks)
#ax.set_ylabel("Säteilyteho (x Maa)")

#flux_lim = [2.0, 1.0, 0.396]

#plt.axhline(y = flux_lim[0], color="red")
#plt.axhline(y = flux_lim[1], color="green")
#plt.axhline(y = flux_lim[2], color="blue")

#ax.fill_between(ax.get_xlim(), flux_lim[1], flux_lim[2], color="lightgreen")
#ax.fill_between(ax.get_xlim(), flux_lim[0], flux_lim[1], color="lightyellow")

#ax2 = ax.twinx()
#ax2.set_yscale('log')
#ax2.set_ylim(ax.get_ylim())
#ax2.set_yticks(flux_lim)
#ax2.set_yticklabels([("%.1f" % flux2P(flow)) for flow in flux_lim])
#ax2.set_ylabel("Kiertoaika (x E)")

#print(flux2P(Venus.flux) * 365)
#print(flux2P(Mars.flux) * 365)

plt.grid()
plt.show()
