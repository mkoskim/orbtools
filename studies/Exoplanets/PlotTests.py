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
  MtoEarth(Saturn.GM),        # Gas giants
  MtoEarth(MasJupiter(78)),   # Stars
]

#------------------------------------------------------------------------------

#stars["TOI-700"].info()
#exit()

#------------------------------------------------------------------------------
# All

def forAll():
  data = masses.values()

  data_x, data_y = (
    #Mass_Radius(plt, ax, data)
    Mass_Density(plt, ax, data)
    #Mass_Density(plt, ax, doFilters(data, lambda x: not(x.GM > MtoEarth(100) and x.orbit and x.orbit.P < TasDays(10))))
  )
  #data_x, data_y = Mass_Radius(plt, ax, planets.values(), xticks=ticks_m_planets, yticks=ticks_r_planets)

  for M_lim in planet_M_lim: plt.axvline(x = M_lim, ls="dashed")

  ax.scatter(data_x, data_y, marker=".", s=1.0)

forAll()

#------------------------------------------------------------------------------
# What kind of stars have planets? Interesting results...

def Stars():

  lim_small = (Star.typical["K5"].GM + Star.typical["K6"].GM) / 2
  lim_large = (Star.typical["F5"].GM + Star.typical["F6"].GM) / 2

  print("lim_small", MtoSun(lim_small))
  print("lim_large", MtoSun(lim_large))

  exoplanets = doFilters(planets.values(), isExoplanet)
  #data = doFilters(stars.values(), lambda x: x.hasSatellites)

  categories = [
    doFilters(exoplanets, lambda x: x.system.GM < lim_small),
    doFilters(exoplanets, lambda x: x.system.GM > lim_small and x.GM < lim_large),
    doFilters(exoplanets, lambda x: x.system.GM > lim_large)
  ]

  print(list(len(x) for x in categories))

  #for star in sorted(categories[1], key=lambda x: x.GM):
  #  print("%-25s" % star.name, "%-7s" % star.sptype, "%5.2f" % MtoSun(star.GM))

  exit()

  #data_x, data_y = Period_Radius(plt, ax, categories[0], yticks=ticks_r_planets)
  #data_x, data_y = Period_Radius(plt, ax, categories[1], yticks=ticks_r_planets)
  #data_x, data_y = Period_Radius(plt, ax, categories[2], yticks=ticks_r_planets)
  #ax.scatter(data_x, data_y, marker=".")

#Stars()

#------------------------------------------------------------------------------
# Exoplanet detection method

def Detection():
  data = doFilters(planets.values(), lambda x: hasattr(x, "detection") and not x.detection is None)

  methods = {}
  for p in data: methods[p.detection] = True
  for m in list(methods.keys()):
    methods[m] = doFilters(data, lambda x: x.detection == m)
  print([(key, len(value)) for key, value in methods.items()])

  #for key, value in methods.items(): print(key, len(value))

  #withM = doFilters(methods["transit"], hasMass)
  #withR = doFilters(methods["RV"], hasRadius)

  #print("Transit: Tot", len(methods["transit"]), "With mass:", len(withM))
  #print("RV:      Tot", len(methods["RV"]), "With radius:", len(withR))

  data_x, data_y = (
    #Period_Radius(plt, ax, methods["transit"], yticks=ticks_r_planets)
    Distance_Radius(plt, ax, methods["transit"], yticks=ticks_r_planets)

    #Period_Mass(plt, ax, methods["RV"], yticks=ticks_m_planets + [10000])
    #Distance_Mass(plt, ax, methods["RV"], yticks=ticks_m_planets + [10000], xticks=[0, 500, 1000, 1500])

    #Period_Mass(plt, ax, methods["microlensing"], yticks=ticks_m_planets)
    #Period_Mass(plt, ax, methods["imaging"], yticks=ticks_m_planets + [1000, 10_000], xticks=ticks_P + [100_000])
  )
  ax.scatter(data_x, data_y, marker=".")

#Detection()

#------------------------------------------------------------------------------
# Exoplanets only

def Exoplanets():
  exoplanets = doFilters(planets.values(), isExoplanet)

  #exoplanets = doFilters(exoplanets, hasMass, lambda x: x.GM < 13*GM_Jupiter)
  #exoplanets = doFilters(exoplanets, hasMass, lambda x: x.GM < 1*GM_Neptune)
  #exoplanets = doFilters(exoplanets, hasMass, hasRadius, isRocky)

  data_x, data_y = (
    #Distance_Radius(plt, ax, exoplanets, yticks=ticks_r_planets)
    #Distance_Period(plt, ax, exoplanets)
    #Period_Radius(plt, ax, exoplanets, yticks=ticks_r_planets)
    #Period_Mass(plt, ax, exoplanets, yticks=ticks_m_planets + [10_000])
    Flux_Radius(plt, ax, exoplanets, yticks=ticks_r_planets, xticks=ticks_flux + [100, 1000])
    #Flux_Mass(plt, ax, exoplanets, yticks=ticks_m_planets, xticks=ticks_flux + [100, 1000])
    #Flux_Temperature(plt, ax, exoplanets, yticks = [-250, 0, 250, 500, 1000], xticks = ticks_flux + [100.0, 1000.0])
    #Mass_Density(plt, ax, exoplanets)
  )

  ax.scatter(data_x, data_y, marker=".")

#Exoplanets()

#------------------------------------------------------------------------------
# Giants

def Giants():
  giants = doFilters(planets.values(), lambda x: x.GM > MasJupiter(0.2))
  data_x, data_y = (
    #Flux_Radius(plt, ax, giants, yticks=ticks_r_planets + [20.0], xticks = ticks_flux + [100.0, 1000.0])
    Flux_Mass(plt, ax, giants, yticks=ticks_m_planets + [5000], xticks = ticks_flux + [100.0, 1000.0])
  )

  ax.scatter(data_x, data_y, marker=".")

#Giants()

#------------------------------------------------------------------------------
# sub-Giants

def subGiants():

  ticks_m = [1, 10, 50]

  data = doFilters(planets.values(), lambda x: x.GM < MasJupiter(0.2))
  #data = doFilters(data, hasFlux, lambda x: x.flux > 10 and x.flux < 20)

  def plotMassDensity():
    for M_lim in [2]: plt.axvline(x = M_lim, ls="dashed")

    return Mass_Density(plt, ax, data, xticks=ticks_m)

  data_x, data_y = (
    #Mass_Radius(plt, ax, data, yticks=ticks_r_planets, xticks=ticks_m_planets)
    #Flux_Radius(plt, ax, data, yticks=ticks_r_planets + [20.0], xticks = ticks_flux + [100.0, 1000.0])
    #Flux_Mass(plt, ax, data, yticks=ticks_m_planets + [5000], xticks = ticks_flux + [100.0, 1000.0])
    #plotMassDensity()
  )

  ax.scatter(data_x, data_y, marker=".")

#subGiants()

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

  data_x, data_y = (
    Flux_Radius(plt, ax, sol_planets, yticks=[0.05, 0.1] + ticks_r_planets)
    #Flux_Mass(plt, ax, sol_planets, yticks=[1e-4, 1e-3, 0.01] + ticks_m_planets)
    #Mass_Density(plt, ax, sol_planets, xticks=[0.01, 0.1] + ticks_m_planets)
  )
  ax.scatter(data_x, data_y, marker="o")

#doSolSystem()

#------------------------------------------------------------------------------
# Super-Earths

def Superearths():

  def doSplit(data, fSplit):
    set1 = doFilters(data, fSplit)
    set2 = doFilters(data, lambda x: not fSplit(x))
    return set1, set2

  def MassRadius2(data1, data2):
    N = len(data1) + len(data2)
    xticks = [1, 2, 3, 4, 8]
    yticks = [1, 1.5, 2]
    data_x, data_y = Mass_Radius(plt, ax, data1, xticks = xticks, yticks=yticks, N = N)
    ax.scatter(data_x, data_y, marker=".")

    data_x, data_y = Mass_Radius(plt, ax, data2, append = True)
    ax.scatter(data_x, data_y, marker="+")

  def RadiusMass2(data1, data2):
    N = len(data1) + len(data2)
    yticks = [1, 2, 3, 4, 8]
    xticks = [1, 1.5, 2, 4]

    data_x, data_y = Radius_Mass(plt, ax, data1, xticks = xticks, yticks=yticks, N = N)
    ax.scatter(data_x, data_y, marker=".")

    data_x, data_y = Radius_Mass(plt, ax, data2, append = True)
    ax.scatter(data_x, data_y, marker="+")

  def FluxRadius2(data1, data2):
    N = len(data1) + len(data2)
    xticks = ticks_flux + [100, 1000]
    yticks = [1, 1.5, 2, 4]

    data_x, data_y = Flux_Radius(plt, ax, data1, xticks = xticks, yticks=yticks, N = N)
    ax.scatter(data_x, data_y, marker=".")

    data_x, data_y = Flux_Radius(plt, ax, data2, append = True)
    ax.scatter(data_x, data_y, marker="+")

  def FluxMass2(data1, data2):
    N = len(data1) + len(data2)
    xticks = ticks_flux + [100, 1000]
    yticks = [1, 2, 3, 4, 8]

    data_x, data_y = Flux_Mass(plt, ax, data1, xticks = xticks, yticks=yticks, N = N)
    ax.scatter(data_x, data_y, marker=".")

    data_x, data_y = Flux_Mass(plt, ax, data2, append = True)
    ax.scatter(data_x, data_y, marker="+")

  def MassDensity(data):
    data_x, data_y = Mass_Density(plt, ax, data, xticks=[1, 2, 4, 8])
    ax.scatter(data_x, data_y, marker=".")
    #plt.axvline(x = 2, ls="dashed")
    #plt.axvline(x = 4, ls="dashed")

  def MassDensity2(data1, data2):
    N = len(data1) + len(data2)
    xticks = [1, 2, 4, 8]
    yticks = None

    data_x, data_y = Mass_Density(plt, ax, data1, xticks=xticks, yticks=yticks, N=N)
    ax.scatter(data_x, data_y, marker=".")

    data_x, data_y = Mass_Density(plt, ax, data2, xticks=xticks, yticks=yticks, append=True)
    ax.scatter(data_x, data_y, marker=".")

  def FluxRadius(data):
    data_x, data_y = Flux_Radius(plt, ax, data, yticks=[1.0, 2.0, 3.0], xticks=ticks_flux + [100, 1000])
    ax.scatter(data_x, data_y, marker=".")
    plt.axhline(y = 2 ** 0.33, ls="dashed")
    plt.axhline(y = 4 ** 0.33, ls="dashed")
    #for m in [Earth, Neptune]:
    #  plt.axhline(y = m.density, ls="dashed", label=m.name)

  def MassRadius(data):
    data_x, data_y = Mass_Radius(plt, ax, data, yticks=[1.0, 2.0], xticks=[1, 2, 3, 4, 8])
    #plt.axvline(x = 2, ls="dashed")
    ax.scatter(data_x, data_y, marker=".")

  superearths = doFilters(planets.values(), isExoplanet, isSuperEarth)

  superearths = doFilters(superearths, hasRadius)
  superearths = doFilters(superearths, hasMass, lambda x: not isUltraDense(x))
  superearths = doFilters(superearths, hasFlux)

  hot, cool = doSplit(superearths, lambda x: x.flux > 100)
  rocky, nonrocky = doSplit(superearths, isRocky)

  #MassRadius2(nonrocky, rocky)
  #RadiusMass2(data2, data1)
  #FluxRadius2(data2, data1)
  #FluxMass2(data2, data1)

  #MassDensity2(cool, hot)

  #MassDensity(hot)
  #MassRadius(cool)

  #MassDensity(superearths)
  #MassRadius(rocky)
  #FluxRadius(rocky)

  r_bins = [(x-0.5)/4 for x in range(16)]
  m_bins = [(x-0.5) for x in range(15)]

  def histRadius(data1, data2, bins = r_bins, N = None):
    if not N: N = len(data1) + len(data2)
    plt.title("N=%d" % N)

    data1 = [RtoEarth(x.radius) for x in data1]
    data2 = [RtoEarth(x.radius) for x in data2]
    ax.hist(data1, bins=bins)
    ax.hist(data2, bins=bins, rwidth=0.5)
    ax.set_xlabel("Halkaisija (x Maa)")

  def histMass(data1, data2, bins = m_bins, N = None):
    if not N: N = len(data1) + len(data2)
    plt.title("N=%d" % N)

    data1 = [MtoEarth(x.GM) for x in data1]
    data2 = [MtoEarth(x.GM) for x in data2]
    ax.hist(data1, bins=bins)
    ax.hist(data2, bins=bins, rwidth=0.5)
    ax.set_xlabel("Massa (x Maa)")

  #histRadius(superearths, rocky, N=len(superearths))
  #histRadius(nonrocky, rocky)
  histRadius(cool, doFilters(cool, isRocky), N = len(cool))

  #histMass(rocky, superearths, N=len(superearths))
  #histMass(rocky, nonrocky)

  #def Mx3(x): return MtoEarth(x.GM) < 3 and 1 or 2
  #histogram2([Mx3(x) for x in data1], [Mx3(x) for x in data2], [1, 2])

#Superearths()

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

#small = doFilters(planets.values(), isExoplanet, hasMass, lambda x: x.GM < 1.25 * GM_Earth)
#small.sort(key=lambda x: x.GM)
#for p in small:
#  print("%-20s %5.2f - %7.2f" % (p.name, MtoEarth(p.GM), m2ly(p.system.dist)))

#exit()

#histExoplanets()

#------------------------------------------------------------------------------

ax.minorticks_off()
#plt.grid()
ax.grid(b=True, which='major', linestyle='-')
plt.show()
