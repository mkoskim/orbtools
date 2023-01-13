#!/usr/bin/env python3
###############################################################################
#
# Test plots to see that star database seems fine
#
###############################################################################

import os, sys
sys.path.append(os.path.abspath("."))

from orbtools import *
from PlotUtils import *

#------------------------------------------------------------------------------
# Filter and plot
#------------------------------------------------------------------------------

import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(9, 6))  # Create a figure containing a single axes.
#plt.subplots_adjust(left=0.15, right=0.85)  # adjust plot area

#------------------------------------------------------------------------------

planet_M_lim = [
  2.0,                        # Earth-like
  MtoEarth(GM_Neptune),       # Neptune
  MtoEarth(MasJupiter(0.2)),  # Saturn etc
  MtoEarth(MasJupiter(13)),   # Brown dwarfs
  MtoEarth(MasJupiter(78)),   # Stars
]

#------------------------------------------------------------------------------

#stars["TOI-700"].info()
#exit()

#------------------------------------------------------------------------------
# All

def forAll():
  data_x, data_y = Mass_Radius(plt, ax, masses.values())
  #data_x, data_y = Mass_Radius(plt, ax, planets.values(), xticks=ticks_m_planets, yticks=ticks_r_planets)

  for M_lim in planet_M_lim: plt.axvline(x = M_lim, ls="dashed")

  ax.scatter(data_x, data_y, marker=".", s=1.0)

#forAll()

#------------------------------------------------------------------------------
# Giants

def Giants():
  giants = doFilters(planets.values(), lambda x: x.GM > MasJupiter(0.2))
  data_x, data_y = Flux_Radius(plt, ax, giants, yticks=ticks_r_planets + [20.0], xticks = ticks_flux + [20.0, 100.0, 1000.0])

  ax.scatter(data_x, data_y, marker=".")

#Giants()

#------------------------------------------------------------------------------
# Exoplanets only

def Exoplanets():
  exoplanets = doFilters(planets.values(), isExoplanet)

  data_x, data_y = (
    #Period_Radius(plt, ax, exoplanets, yticks=ticks_r_planets, xticks=ticks_P + [10_000])
    Period_Mass(plt, ax, exoplanets, yticks=ticks_m_planets + [5000], xticks=ticks_P + [10_000])
  #data_x, data_y = Flux_Radius(plt, ax, exoplanets, yticks=ticks_r_planets)
  #data_x, data_y = Flux_Mass(plt, ax, doFilters(exoplanets, hasMass, hasRadius), yticks=ticks_m_planets)
  )

  ax.scatter(data_x, data_y, marker=".")

#Exoplanets()

#------------------------------------------------------------------------------
# Planets

#data_x, data_y = Flux_Radius(plt, ax, sol_planets, yticks=[0.05, 0.1] + ticks_r_planets, xticks=ticks_flux)
#data_x, data_y = Flux_Radius(plt, ax, planets.values(), yticks=ticks_r_planets)

# Super-Earths
#data_x, data_y = Flux_Mass(plt, ax, doFilters(planets.values(), isSuperEarth), yticks=[1.0, 2.0, 4.0, 8.0], xticks=ticks_flux+[25.0])

# Rocky worlds
#data_x, data_y = Flux_Mass(plt, ax, doFilters(planets.values(), isRocky, hasMass, hasRadius), yticks=ticks_m_planets)

# Stars
#data_x, data_y = Mass_Luminosity(plt, ax, stars.values(), xticks=ticks_m_stars)
#data_x, data_y = Luminosity_Mass(plt, ax, stars.values(), yticks=ticks_m_stars)
#data_x, data_y = Temperature_Mass(plt, ax, stars.values(), yticks=ticks_m_stars)
#data_x, data_y = Temperature_Magnitude(plt, ax, stars.values())

#ax.scatter(data_x, data_y, marker=".", s = 1.0)
#ax.scatter(data_x, data_y, marker=".", color="lightgrey")
#ax.scatter(data_x, data_y, marker="o")

# Secondary plot
#data_x, data_y = Flux_Mass(plt, ax, doFilters(planets.values(), isRocky, isSuperEarth, hasMass, hasRadius), yticks=[1.0, 2.0, 4.0, 8.0], xticks=ticks_flux+[25.0], append=True)
#ax.scatter(data_x, data_y, marker="+", color="red")

# Tertiary plot
#data_x, data_y = Flux_Mass(plt, ax, doFilters(planets.values(), isJovian, hasMass, hasRadius), yticks=ticks_m_planets, append=True)
#ax.scatter(data_x, data_y, marker=".", color="green")

# Planets in HZ (Habitable Zone)
#data_x, data_y = Mass_Radius(plt, ax, doFilters(planets.values(), isInHZ), xticks=ticks_m_planets, yticks=ticks_r_planets)
#data2_x, data2_y = Mass_Radius(plt, ax, doFilters(planets.values(), isHot), xticks=ticks_m_planets, yticks=ticks_r_planets)
#data3_x, data3_y = Mass_Radius(plt, ax, doFilters(planets.values(), isCold), xticks=ticks_m_planets, yticks=ticks_r_planets)

#ax.scatter(data2_x, data2_y, marker=".", s=1.0, color="red")
#ax.scatter(data3_x, data3_y, marker=".", color="blue")
#ax.scatter(data_x, data_y, marker=".")

#------------------------------------------------------------------------------
# Solar system with hand-picked objects

sol_planets = [
  Mercury, Venus, Earth, Mars, Moon,
  masses["Ceres"], masses["Pallas"], masses["Vesta"],
  Jupiter, Saturn,
  masses["Io"], masses["Europa"], masses["Ganymede"], masses["Callisto"],
  masses["Titan"],
  Uranus, Neptune,
]

def doSolSystem():

  #data_x, data_y = Flux_Radius(plt, ax, sol_planets, yticks=[0.05, 0.1] + ticks_r_planets)
  #data_x, data_y = Flux_Mass(plt, ax, sol_planets, yticks=[1e-4, 1e-3, 0.01] + ticks_m_planets)

  data_x, data_y = Mass_Density(plt, ax, sol_planets, xticks=[0.01, 0.1] + ticks_m_planets)

  ax.scatter(data_x, data_y, marker=".")

#doSolSystem()

#------------------------------------------------------------------------------
# Super-Earths

def histSuperearths():
  superearths = doFilters(planets.values(), isExoplanet, hasRadius, hasMass, hasFlux, isSuperEarth, lambda x: not isUltraDense(x))
  #superearths = doFilters(superearths, lambda x: x.flux < 10, hasFlux)

  data1 = doFilters(superearths, lambda x: x.flux < 60, hasFlux)
  data2 = doFilters(superearths, lambda x: x.flux > 60, hasFlux)

  #data1 = [MtoEarth(x.GM) for x in data1]
  #data2 = [MtoEarth(x.GM) for x in data2]
  #bins = [x-0.5 for x in range(16)]
  #ax.set_xlabel("Massa (x Maa)")

  #data1 = [RtoEarth(x.radius) for x in doFilters(data1, lambda x: not isRocky(x))]
  data1 = [RtoEarth(x.radius) for x in data1]
  data2 = [RtoEarth(x.radius) for x in data2]
  bins = [(x-0.5)/4 for x in range(16)]

  # We can set the number of bins with the *bins* keyword argument.
  ax.hist(data1, bins=bins)
  ax.hist(data2, bins=bins, rwidth=0.5)
  plt.title("N=%d" % (len(data1) + len(data2)))

#histSuperearths()

#------------------------------------------------------------------------------
# Planet distribution

def histExoplanets():
  exoplanets = doFilters(planets.values(), lambda x: isExoplanet)

  def categoryR(planet):
    r = RtoEarth(planet.radius)
    if r <  1.25: return 1
    if r <  2.00: return 2
    if r <  6.00: return 3
    if r < 15.00: return 4
    return 5

  data = [categoryR(x) for x in doFilters(exoplanets, hasRadius)]
  bins = 6

  #data = [RtoEarth(x.radius) for x in doFilters(exoplanets, hasRadius)]
  #bins = [1.25, 2, 6, 15]
  #ax.set_xlabel("Halkaisija (x Maa)")

  # We can set the number of bins with the *bins* keyword argument.
  ax.hist(data, bins=bins, rwidth=0.6)

  print("Points:", len(data))

small = doFilters(planets.values(), isExoplanet, hasMass, lambda x: x.GM < 1.25 * GM_Earth)
small.sort(key=lambda x: x.GM)
for p in small:
  print("%-20s %5.2f - %7.2f" % (p.name, MtoEarth(p.GM), m2ly(p.system.dist)))

exit()

histExoplanets()

plt.grid()
plt.show()
