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
#from orbtools.systems.solsystem import *
#import orbtools.systems.stars
#import orbtools.systems.exoplanets

#------------------------------------------------------------------------------

def showStars(data):
  for star in data:
    try:
      print("%-20s %-13s M=%5.2f x Sun" % (star.name, star.sptype, MtoSun(star.GM)),
        "L=%7s" % (star.L and "%.2f" % float(star.L)),
        "T=%s" % (star.T and "%.0f" % float(star.T))
      )
    except:
      print("ERROR:", star.name)
      exit()
  exit()

def showPlanets(data):
  print("Points:", len(data))
  for planet in data:
    try:
      print("%-20s M=%7.2f R=%7.2f" % (planet.name, MtoEarth(planet.GM), RtoEarth(planet.radius)),
        "D=%5.0f" % planet.density,
        #"F=%7.2f" % planet.flux,
        "P=%7.2f" % TtoDays(planet.orbit.P),
        "F=%7.2f" % planet.flux,
      )
    except:
      print("ERROR:", planet.name)
      exit()
  exit()

#------------------------------------------------------------------------------

#data = doFilters(planets.values(), hasMass, hasRadius, isInHZ, lambda x: x.GM > 0.01 * GM_Earth)
#data = doFilters(planets.values(), isRocky, hasFlux, lambda x: x.GM < MasJupiter(0.2), hasMass, hasRadius)
#data = sorted(data, key=lambda x: x.flux)
#showPlanets(data)

#data = doFilters(stars.values(), isStar, hasTemperature, lambda x: isSpectralClass(x, "B"))
#data = sorted(data, key=lambda x: x.T)
#showStars(data)

#data = reversed(sorted(stars.values(), key=lambda x: x.GM))
#showStars(list(data)[:30])

#print(Sun.fluxAt(AU2m(2.7)))
#print(MtoEarth(GM_Sun))
#print(MtoEarth(MasJupiter(0.2)))
#print(MtoEarth(MasJupiter(78)))
#exit()

#Jupiter.info()
#Saturn.info()
#exit()

#------------------------------------------------------------------------------
# Filter and plot
#------------------------------------------------------------------------------

import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots()  # Create a figure containing a single axes.
#plt.subplots_adjust(left=0.15, right=0.85)  # adjust plot area

# All
#data_x, data_y = Mass_Radius(plt, ax, masses.values())

# Planets

#data_x, data_y = Mass_Radius(plt, ax, planets.values(), xticks=ticks_m_planets, yticks=ticks_r_planets)

#data_x, data_y = Flux_Radius(plt, ax, sol_planets, yticks=[0.05, 0.1] + ticks_r_planets, xticks=ticks_flux)
#data_x, data_y = Flux_Radius(plt, ax, planets.values(), yticks=ticks_r_planets)
#data_x, data_y = Flux_Mass(plt, ax, doFilters(planets.values(), hasMass, hasRadius), yticks=ticks_m_planets)
#data_x, data_y = Period_Radius(plt, ax, planets.values(), yticks=ticks_r_planets)

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

doSolSystem()

#------------------------------------------------------------------------------
# Histograms

def doHistorgam():
  data1 = doFilters(planets.values(), lambda x: not isUltraDense(x), isSuperEarth, isExoplanet, hasRadius, hasMass)
  data2 = doFilters(planets.values(), isRocky, lambda x: not isUltraDense(x), isSuperEarth, isExoplanet, hasRadius, hasMass)

  #data1 = [MtoEarth(x.GM) for x in data1]
  #data2 = [MtoEarth(x.GM) for x in data2]
  #bins = [x-0.5 for x in range(16)]
  #ax.set_xlabel("Massa (x Maa)")

  data1 = [RtoEarth(x.radius) for x in doFilters(data1, lambda x: not isRocky(x))]
  data2 = [RtoEarth(x.radius) for x in data2]
  bins = [(x-0.5)/4 for x in range(16)]
  #ax.set_xlabel("Halkaisija (x Maa)")

  # We can set the number of bins with the *bins* keyword argument.
  ax.hist(data1, bins=bins)
  ax.hist(data2, bins=bins, rwidth=0.7)

  print("Points:", len(data1))
  print("Points:", len(data2))

#doHistorgam()

plt.grid()
plt.show()
