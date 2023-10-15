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

  Mass_Radius(plt, ax, data, s=1)
  #Mass_Density(plt, ax, data, s=1)
  #Mass_Density(plt, ax, doFilters(data, lambda x: not(x.GM > MtoEarth(100) and x.orbit and x.orbit.P < TasDays(10))))

  for M_lim in planet_M_lim: plt.axvline(x = M_lim, ls="dashed")

  #ax.scatter(data_x, data_y, marker=".", s=1.0)

#forAll()

#------------------------------------------------------------------------------
# What kind of stars have planets? Interesting results...

def Stars():

  def MassLuminosity2(data1, data2):
    Mass_Luminosity(plt, ax, data1)
    Mass_Luminosity(plt, ax, data2, append=True, marker='.')

  def MassTemperature2(data1, data2):
    Mass_Temperature(plt, ax, data1)
    Mass_Temperature(plt, ax, data2, append=True, marker='.')

  def MassEE2(data1, data2):
    Mass_EE(plt, ax, data1)
    Mass_EE(plt, ax, data2, append=True, marker='.')

  def EEMass2(data1, data2):
    EE_Mass(plt, ax, data1)
    EE_Mass(plt, ax, data2, append=True, marker='.')

  #K_stars = doFilters(stars.values(), hasSpectralType, lambda star: star.sptype[:2] in ["K0", "K1"])
  #G_stars = doFilters(stars.values(), hasSpectralType, lambda star: star.sptype[:2] in ["G8", "G9"])

  #MassLuminosity2(K_stars, G_stars)
  #MassLuminosity2(stars.values(), Star.typical.values())

  #Temperature_Mass(plt, ax, stars.values())
  #MassTemperature2(stars.values(), Star.typical.values())

  #MassEE2(stars.values(), Star.typical.values())
  EEMass2(stars.values(), Star.typical.values())

  #Temperature_Luminosity(plt, ax, stars.values())
  #Temperature_Luminosity(plt, ax, Star.typical.values(), append=True)

  return

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

Stars()

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

  #Period_Radius(plt, ax, methods["transit"], yticks=ticks_r_planets)
  #Distance_Radius(plt, ax, methods["transit"], yticks=ticks_r_planets)

  #Period_Mass(plt, ax, methods["RV"], yticks=ticks_m_planets + [10000])
  #Distance_Mass(plt, ax, methods["RV"], yticks=ticks_m_planets + [10000], xticks=[0, 500, 1000, 1500])

  #Period_Mass(plt, ax, methods["microlensing"], yticks=ticks_m_planets)
  #Period_Mass(plt, ax, methods["imaging"], yticks=ticks_m_planets + [1000, 10_000], xticks=ticks_P + [100_000])

#Detection()

#------------------------------------------------------------------------------
# Exoplanets only

def Exoplanets():
  exoplanets = doFilters(planets.values(), isExoplanet)

  #exoplanets = doFilters(exoplanets, hasMass, lambda x: x.GM < 13*GM_Jupiter)
  #exoplanets = doFilters(exoplanets, hasMass, lambda x: x.GM < 1*GM_Neptune)
  #exoplanets = doFilters(exoplanets, hasMass, hasRadius, isRocky)

  #Distance_Radius(plt, ax, exoplanets, yticks=ticks_r_planets)
  #Distance_Period(plt, ax, exoplanets)
  #Period_Radius(plt, ax, exoplanets, yticks=ticks_r_planets)
  #Period_Mass(plt, ax, exoplanets, yticks=ticks_m_planets + [10_000])
  Flux_Radius(plt, ax, exoplanets, yticks=ticks_r_planets, xticks=ticks_flux + [100, 1000])
  #Flux_Mass(plt, ax, exoplanets, yticks=ticks_m_planets, xticks=ticks_flux + [100, 1000])
  #Flux_Temperature(plt, ax, exoplanets, yticks = [-250, 0, 250, 500, 1000], xticks = ticks_flux + [100.0, 1000.0])
  #Mass_Density(plt, ax, exoplanets)

#Exoplanets()

#------------------------------------------------------------------------------
# Planet distribution

def histExoplanets():
  exoplanets = doFilters(planets.values(), lambda x: isExoplanet)

  ultrahot = doFilters(exoplanets, hasFlux, lambda x: x.flux > 500)

  def categoryR(planet):
    r = RtoEarth(planet.radius)
    if r <  1.25: return 1
    if r <  2.00: return 2
    if r <  6.00: return 3
    if r < 15.00: return 4
    return 5

  data = [categoryR(x) for x in doFilters(ultrahot, hasRadius)]
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
# Giants

def Giants():
  giants = doFilters(planets.values(), lambda x: x.GM > MasJupiter(0.2))
  #Flux_Radius(plt, ax, giants, yticks=ticks_r_planets + [20.0], xticks = ticks_flux + [100.0, 1000.0])
  Flux_Mass(plt, ax, giants, yticks=ticks_m_planets + [5000], xticks = ticks_flux + [100.0, 1000.0])

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

  #Mass_Radius(plt, ax, data, yticks=ticks_r_planets, xticks=ticks_m_planets)
  #Flux_Radius(plt, ax, data, yticks=ticks_r_planets + [20.0], xticks = ticks_flux + [100.0, 1000.0])
  #Flux_Mass(plt, ax, data, yticks=ticks_m_planets + [5000], xticks = ticks_flux + [100.0, 1000.0])
  #plotMassDensity()

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

  Flux_Radius(plt, ax, sol_planets, yticks=[0.05, 0.1] + ticks_r_planets)
  #Flux_Mass(plt, ax, sol_planets, yticks=[1e-4, 1e-3, 0.01] + ticks_m_planets)
  #Mass_Density(plt, ax, sol_planets, xticks=[0.01, 0.1] + ticks_m_planets)

#doSolSystem()

#------------------------------------------------------------------------------
# Super-Earths

def Superearths():

  ticks_m_super = [1, 2, 3, 4, 8, 16]
  ticks_r_super = [1, 1.5, 2, 3, 4]

  def doSplit(data, fSplit):
    set1 = doFilters(data, fSplit)
    set2 = doFilters(data, lambda x: not fSplit(x))
    return set1, set2

  #----------------------------------------------------------------------------
  # XY plots
  #----------------------------------------------------------------------------

  def MassRadius(data):
    xticks = ticks_m_super
    yticks = ticks_r_super
    Mass_Radius(plt, ax, data, yticks=yticks, xticks=xticks)
    #plt.axvline(x = 2, ls="dashed")

  def MassRadius2(data1, data2):
    N = len(data1) + len(data2)
    xticks = ticks_m_super
    yticks = ticks_r_super

    Mass_Radius(plt, ax, data1, xticks = xticks, yticks=yticks, N = N)
    Mass_Radius(plt, ax, data2, append = True)

  def RadiusMass2(data1, data2):
    N = len(data1) + len(data2)
    yticks = ticks_m_super
    xticks = ticks_r_super

    Radius_Mass(plt, ax, data1, xticks = xticks, yticks=yticks, N = N)
    Radius_Mass(plt, ax, data2, append = True)

  def FluxRadius2(data1, data2):
    N = len(data1) + len(data2)
    xticks = ticks_flux + [100, 1000]
    yticks = ticks_r_super

    Flux_Radius(plt, ax, data1, xticks = xticks, yticks=yticks, N = N)
    Flux_Radius(plt, ax, data2, append = True)

  def FluxMass2(data1, data2):
    N = len(data1) + len(data2)
    xticks = ticks_flux + [100, 1000]
    yticks = ticks_m_super

    Flux_Mass(plt, ax, data1, xticks = xticks, yticks=yticks, N = N)
    Flux_Mass(plt, ax, data2, append = True)

  def MassDensity(data):
    xticks = ticks_m_super
    Mass_Density(plt, ax, data, xticks=xticks)
    #plt.axvline(x = 2, ls="dashed")
    #plt.axvline(x = 4, ls="dashed")

  def MassDensity2(data1, data2):
    N = len(data1) + len(data2)
    xticks = ticks_m_super
    yticks = None

    Mass_Density(plt, ax, data1, xticks=xticks, yticks=yticks, N=N)
    Mass_Density(plt, ax, data2, append=True)

  def FluxRadius(data):
    xticks = ticks_flux + [100, 1000]
    yticks = ticks_r_super

    Flux_Radius(plt, ax, data, yticks=yticks, xticks=xticks)
    #ax.scatter(data_x, data_y, marker=".")

    #plt.axhline(y = 2 ** 0.33, ls="dashed")
    #plt.axhline(y = 4 ** 0.33, ls="dashed")
    #for m in [Earth, Neptune]:
    #  plt.axhline(y = m.density, ls="dashed", label=m.name)

  def FluxMass(data):
    xticks = ticks_flux + [100, 1000]
    yticks = ticks_m_super

    Flux_Mass(plt, ax, data, yticks=yticks, xticks=xticks)

  superearths = planets.values()
  superearths = doFilters(superearths, isExoplanet, isSuperEarth)
  superearths = doFilters(superearths, hasFlux)
  superearths = doFilters(superearths, hasRadius)
  superearths = doFilters(superearths, hasMass, lambda x: not isUltraDense(x))

  #iron, rock = doSplit(rocky, lambda x: x.density > 5000)

  #FluxRadius(superearths)
  #FluxMass(superearths)
  #MassRadius(superearths)

  hot, cool = doSplit(superearths, lambda x: x.flux > 100)
  rocky, nonrocky = doSplit(superearths, isRocky)

  #MassRadius2(nonrocky, rocky)
  #MassRadius2(cool, hot)
  #RadiusMass2(data2, data1)
  #FluxRadius2(data2, data1)
  #FluxMass2(data2, data1)

  #MassDensity(superearths)
  #MassDensity2(cool, hot)
  #MassDensity(hot)
  #MassDensity(cool)

  #MassRadius(rocky)
  #FluxRadius(rocky)

  #----------------------------------------------------------------------------
  # Histograms
  #----------------------------------------------------------------------------

  m_bins = [x+1 for x in range(15)]
  def closest(bins, value):
    return min(bins, key=lambda x: abs(x-value))

  def classify(bins, data, extract):
    classified = [(closest(bins, extract(x)), x) for x in data]
    return [
      [p[1] for p in list(filter(lambda p: p[0] == x, classified))] for x in bins
    ]

  def Bars(data):
    binied = classify(m_bins, data, lambda x: MtoEarth(x.GM))

    total  = [len(x) for x in binied]
    rocky  = [len(list(filter(lambda p: p.density > 3500, x))) for x in binied]
    iron   = [len(list(filter(lambda p: p.density > 5000, x))) for x in binied]

    #print(totals)
    #print(rocky)
    #print(list(zip(rocky, total)))
    #ax.plot(m_bins, totals)

    #ax.plot(m_bins, total)
    #ax.plot(m_bins, rocky)
    #ax.plot(m_bins, iron)

    ax.bar(m_bins, total)
    ax.bar(m_bins, rocky, width=0.4, color="khaki")
    ax.bar(m_bins, iron, width=0.4, color="tab:orange")

    #ax.bar(m_bins, [100.0*x[0]/x[1] for x in zip(rocky, total)], color="khaki")
    #ax.bar(m_bins, [100.0*x[0]/x[1] for x in zip(iron, total)], color="tab:orange")

  #Bars(cool)
  #Bars(hot)

  r_bins = [(x-0.5)/4 for x in range(16)]
  m_bins = [(x-0.5) for x in range(15)]

  def histRadius(data1, data2, data3=[], bins = r_bins, N = None):
    if not N: N = len(data1) + len(data2)
    plt.title("N=%d" % N)
    ax.set_xlabel("Halkaisija (x Maa)")

    data1 = [RtoEarth(x.radius) for x in data1]
    data2 = [RtoEarth(x.radius) for x in data2]
    data3 = [RtoEarth(x.radius) for x in data3]

    ax.hist(data1, bins=bins)
    ax.hist(data2, bins=bins, rwidth=0.5)
    ax.hist(data3, bins=bins, rwidth=0.5)

  def histMass(data1, data2, data3=[], bins = m_bins, N = None):
    if not N: N = len(data1) + len(data2)
    plt.title("N=%d" % N)
    ax.set_xlabel("Massa (x Maa)")

    if not len(data3):
      data3 = data2
      data2 = []

    data1 = [MtoEarth(x.GM) for x in data1]
    data2 = [MtoEarth(x.GM) for x in data2]
    data3 = [MtoEarth(x.GM) for x in data3]

    ax.hist(data1, bins=bins, rwidth=1.0)
    #ax.hist(data2, bins=bins, rwidth=0.6, color="khaki", hatch="..")
    ax.hist(data2, bins=bins, rwidth=0.6, color="khaki")
    ax.hist(data3, bins=bins, rwidth=0.6, color="tab:orange")

  def histMassClass(data):
    rocky = doFilters(data, lambda x: x.density > 3500)
    iron  = doFilters(data, lambda x: x.density > 5000)
    histMass(data, rocky, iron, N = len(data))

  #histRadius(superearths, rocky, N=len(superearths))
  #histRadius(nonrocky, rocky)

  #histRadius(cool, doFilters(cool, isRocky), N = len(cool))
  #histRadius(hot, doFilters(hot, isRocky), N = len(hot))

  #histMass(cool, hot)
  #histMassClass(cool)
  #histMassClass(hot)
  #histMass(hot, doFilters(hot, isRocky), N = len(hot))
  #histMass(rocky, nonrocky)

  #----------------------------------------------------------------------------
  # Flux slices
  #----------------------------------------------------------------------------

  def histSlice(slice):
    rocky, nonrocky = doSplit(slice, isRocky)
    #histMass(nonrocky, rocky, N=len(slice))
    #histMass(slice, rocky, N=len(slice))
    #MassRadius2(nonrocky, rocky)
    #MassDensity(slice)

  hotslice  = doFilters(superearths, lambda x: x.flux > 100 and x.flux < 500)
  coolslice = doFilters(superearths, lambda x: x.flux > 1 and x.flux < 30)
  #histSlice(hotslice)
  #histSlice(coolslice)
  #MassDensity2(coolslice, hotslice)

  #def Mx3(x): return MtoEarth(x.GM) < 3 and 1 or 2
  #histogram2([Mx3(x) for x in data1], [Mx3(x) for x in data2], [1, 2])

#Superearths()

#------------------------------------------------------------------------------

ax.minorticks_off()
#plt.grid()
#ax.grid(b=True, which='major', linestyle='-')
ax.grid(which='major', linestyle='-')
plt.show()
