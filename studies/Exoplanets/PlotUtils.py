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

print("Stars...:", len(stars.keys()))
print("Planets.:", len(planets.keys()))

###############################################################################
#
# Database utils
#
###############################################################################

#------------------------------------------------------------------------------
# Database info: show missing values
#
# Many database objects are incomplete. Examples:
#
# - Many planets miss either radius or mass
# - Many stars miss either radius or mass
# - Many Kepler stars miss spectral type
#
# This needs to be taken into account when making plots.
#
#------------------------------------------------------------------------------

def checkMissing():

  def isIncompleteStar(star):
    if not len(star.satellites): return False
    if not star.radius: return True
    if not star.L: return True
    return False

  def isIncompletePlanet(planet):
    if not planet.GM: return True
    if not planet.radius: return True
    return False

  incomplete_stars = list(sorted(filter(isIncompleteStar, stars.values()), key=lambda x: x.name))
  incomplete_planets = list(sorted(filter(isIncompletePlanet, planets.values()), key=lambda x: x.name))

  print("Incomplete stars...:", len(incomplete_stars))
  print("Incomplete planets.:", len(incomplete_planets))

  print("Checking stars...")
  for star in incomplete_stars:
    print("    ", star.name, ": SP=", star.sptype, "R=", star.radius and RtoSun(star.radius), "L=", star.L, "(planets: %d)" % len(star.satellites))

  print("Checking planets...")
  for planet in incomplete_planets:
    print("    ", planet.name, "M=", MtoEarth(planet.GM), "R=", planet.radius and RtoEarth(planet.radius))

#stars["Kepler-22"].info()
#stars["Kepler-62"].info()
#stars["Kepler-186"].info()
#stars["Kepler-442"].info()
#stars["Kepler-452"].info()
#stars["TRAPPIST-1"].info()

#stars["Proxima Centauri"].info()
#stars["Alpha Centauri A"].info()
#stars["Alpha Centauri B"].info()

#stars["Sirius A"].info()
#stars["61 Cygni A"].info()
#stars["61 Cygni B"].info()

#stars["Procyon"].info()

#stars["Tau Ceti"].info()

#checkMissing()
#exit()

###############################################################################
#
# Data filters
#
###############################################################################

def doFilters(data, *filters):
  return len(filters) and filter(filters[0], doFilters(data, *filters[1:])) or data

def isStar(mass): return mass.type == "star"

def isPlanet(mass): return mass.type == "planet"

def hasMass(mass):
  if not mass.GM: return False
  if GM2kg(mass.GM) < 1: return False
  return True

def hasRadius(mass):
  if not mass.radius: return False
  if mass.radius < 1.0: return False
  return True

def hasLuminosity(mass):
  return hasattr(mass, "L") and mass.L

def hasTemperature(mass):
  return hasattr(mass, "T") and mass.T

def hasMagnitude(mass):
  return hasattr(mass, "mag") and mass.mag

def hasFlux(planet):
  return not planet.flux is None

def hasPeriod(mass):
  return not mass.orbit is None

def isExoplanet(mass):
  if mass.type != "planet": return False
  if mass.system.name == "Sun": return False
  return True

def isJovian(planet):
  return planet.GM > MasJupiter(0.2) and planet.GM < MasJupiter(78)

def isNotJovian(planet):
  return planet.GM < MasJupiter(0.2)

def isUltraDense(planet):
  return planet.density > 10000

def isSuperEarth(planet):
  return planet.GM < MasEarth(15)

def isRocky(planet):
  # Densities over 10000 kg/m3 on small planets are probably incertainties in
  # physical parameters
  return planet.density > 5000 and planet.density < 10000

def isHot(planet):
  if not planet.flux: return False
  return planet.flux > 2.5

def isCold(planet):
  if not planet.flux: return False
  return planet.flux < flux_FrostLine

def isInHZ(planet):
  #if not FilterPlanet(planet): return False
  if not planet.flux: return False
  if isHot(planet): return False
  if isCold(planet): return False
  return True

def isSpectralClass(star, *sptypes): return star.sptype and star.sptype[:1] in sptypes
def isSpectralType(star, sptype): return star.sptype and star.sptype[:len(sptype)] == sptype

###############################################################################
#
# Plotting
#
###############################################################################

#------------------------------------------------------------------------------
# Setting data to axes
#------------------------------------------------------------------------------

def set_yticks(ax, ticks, labels = None):
  if ticks and not labels: labels = ticks
  if ticks: ax.set_yticks(ticks)
  if labels: ax.set_yticklabels(labels)

def set_xticks(ax, ticks, labels = None):
  if ticks and not labels: labels = ticks
  if ticks: ax.set_xticks(ticks)
  if labels: ax.set_xticklabels(labels)

#------------------------------------------------------------------------------

ticks_r = [1.0, 10.0, 100.0, 1000.0]
ticks_r_planets = [1.0, 5.0, 10.0]

ticks_m = [0.1, 1.0, 10.0, 100.0, 1000.0, 10_000.0, 100_000, 1_000_000]
ticks_m_planets = [0.1, 1.0, 10.0, 100.0, 500.0]
ticks_m_stars = [10_000.0, 100_000, 1_000_000]

ticks_density = [1_000, 2_500, 5_000, 10_000]

ticks_flux = [0.001, 0.01, 0.1, 1.0, 10.0]

ticks_L = [0.001, 0.01, 0.1, 1.0, 10.0, 100.0]

ticks_T_stars = [3_000, 5_000, 10_000]

ticks_Mag = [10, 5, 0, -5]

ticks_P = [1, 10, 100, 365, 1000]

def tick_max(ticks): return max(ticks)
def tick_min(ticks): return min(ticks)
def tick_range(ticks): return 0.5*min(ticks), 2*max(ticks)

#------------------------------------------------------------------------------

def y_Mass(plt, ax, data, ticks = None, append=False):
  if not append:
    if not ticks: ticks = ticks_m

    ymin, ymax = tick_range(ticks)

    ax.set_ylabel("Massa (x Maa)")
    ax.set_ylim(ymin, ymax)
    ax.set_yscale('log')

    set_yticks(ax, ticks)

    ticks2 = [ Moon, Mars, Earth, Neptune, Jupiter, stars["M9"], Sun]
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

def x_Mass(plt, ax, data, ticks):
  if not ticks: ticks = ticks_m
  xmin, xmax = tick_range(ticks)

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

  #M_lim = [2.0, MtoEarth(MasJupiter(0.2)), MtoEarth(MasJupiter(78))]
  #plt.axvline(x = M_lim[0], ls="dashed")
  #plt.axvline(x = M_lim[1], ls="dashed")
  #plt.axvline(x = M_lim[2], ls="dashed")

  return [MtoEarth(planet.GM) for planet in data]

#------------------------------------------------------------------------------

def y_Radius(plt, ax, data, ticks):
  if not ticks: ticks = ticks_r
  ymin, ymax = tick_range(ticks)

  ax.set_ylabel("Halkaisija (x Maa)")
  ax.set_ylim(ymin, ymax)
  ax.set_yscale('log')

  set_yticks(ax, ticks)

  ticks2 = [ Moon, Mars, Earth, Neptune, Jupiter, Sun]
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

def x_Radius(plt, ax, data, ticks):
  if not ticks: ticks = ticks_r
  xmin, xmax = min(ticks)*0.5, max(ticks)*2

  ax.set_xlabel("Säde (x Maa)")
  ax.set_xlim(xmin, xmax)
  set_xticks(ax, ticks)
  ax.set_xscale('log')

  #ax2 = ax.twiny()
  #ax2.set_xscale('log')
  #ax2.set_xlim(ax.get_xlim())
  #set_xticks(ax,
  #  [1.0, MtoEarth(GM_Neptune), MtoEarth(GM_Jupiter), MtoEarth(GM_Jupiter)*80, MtoEarth(GM_Sun)],
  #  ["Earth", "Neptunus", "Jupiter", "Star", "Sun"]
  #)

  return [RtoEarth(planet.radius) for planet in data]

#------------------------------------------------------------------------------

def y_Density(plt, ax, data, ticks = None):
  if not ticks: ticks = ticks_density
  ymin, ymax = tick_range(ticks)

  ax.set_ylabel("Tiheys")
  ax.set_yscale('log')
  ax.set_ylim(ymin, ymax)
  set_yticks(ax, ticks)

  return [planet.density for planet in data]

def x_Density(plt, ax, data, ticks = None):
  if not ticks: ticks = ticks_density
  xmin, xmax = tick_range(ticks)

  ax.set_xlabel("Tiheys")
  ax.set_xscale('log')
  ax.set_xlim(xmin, xmax)
  set_xticks(ax, ticks)
  ax.invert_xaxis()

  return [planet.density for planet in data]

#------------------------------------------------------------------------------

def y_Luminosity(plt, ax, data, ticks = None):
  if ticks is None: ticks = ticks_L
  ymin, ymax = min(ticks)*0.5, max(ticks)*2

  ax.set_ylabel("Säteilyteho")
  ax.set_yscale('log')
  ax.set_ylim(ymin, ymax)
  set_yticks(ax, ticks)

  return [star.L for star in data]

def x_Luminosity(plt, ax, data, ticks = None):
  if ticks is None: ticks = ticks_L
  xmin, xmax = min(ticks)*0.5, max(ticks)*2

  ax.set_xlabel("Säteilyteho")
  ax.set_xscale('log')
  ax.set_xlim(xmin, xmax)
  set_xticks(ax, ticks)

  return [star.L for star in data]

#------------------------------------------------------------------------------

def y_Magnitude(plt, ax, data, ticks = None):
  #if ticks is None: ticks = ticks_Mag
  #ymin, ymax = min(ticks)*0.5, max(ticks)*2

  ax.set_ylabel("Magnitudi")
  #ax.set_yscale('log')
  #ax.set_ylim(ymin, ymax)
  #set_yticks(ax, ticks)
  ax.invert_yaxis()

  return [star.mag for star in data]

#------------------------------------------------------------------------------

def x_Temperature(plt, ax, data, ticks = None):
  if ticks is None: ticks = ticks_T_stars
  xmin, xmax = min(ticks)*0.5, max(ticks)*2

  ax.set_xlabel("Lämpötila")
  ax.set_xscale('log')
  ax.set_xlim(xmin, xmax)
  set_xticks(ax, ticks)
  ax.invert_xaxis()

  return [star.T for star in data]

#------------------------------------------------------------------------------

def x_Period(plt, ax, data, ticks):
  if not ticks: ticks = ticks_P
  xmin, xmax = min(ticks)*0.5, max(ticks)*2

  ax.set_xlabel("Kiertoaika (d)")
  ax.set_xlim(xmin, xmax)
  ax.set_xscale('log')
  set_xticks(ax, ticks)

  plt.axvline(x = 365, ls="dashed", color="grey")

  return [TtoDays(planet.orbit.P) for planet in data]

def x_Flux(plt, ax, data, ticks = None, append = False):
  if not append:
    if not ticks: ticks = ticks_flux
    xmin, xmax = min(ticks)*0.5, max(ticks)*2

    ax.set_xlabel("Flux (x Earth)")
    ax.set_xscale('log')

    ax.set_xlim(xmin, xmax)
    set_xticks(ax, ticks)

    ax.invert_xaxis()

    flux_lim = [2.0, 1.0, 0.396, flux_FrostLine]
    plt.axvline(x = flux_lim[0], color="red")
    plt.axvline(x = flux_lim[1], color="green")
    plt.axvline(x = flux_lim[2], color="blue")
    plt.axvline(x = flux_lim[3], ls="dashed")

  return [planet.flux for planet in data]

#------------------------------------------------------------------------------

def Flux_Radius(plt, ax, data, xticks=None, yticks=None):
  data = list(doFilters(data, hasRadius, hasFlux))
  print("Points.:", len(data))

  return (
    x_Flux(plt, ax, data, xticks),
    y_Radius(plt, ax, data, yticks)
  )

def Flux_Mass(plt, ax, data, xticks=None, yticks=None, append=False):
  data = list(doFilters(data, hasMass, hasFlux))
  print("Points.:", len(data))

  return (
    x_Flux(plt, ax, data, xticks, append),
    y_Mass(plt, ax, data, yticks, append)
  )

def Period_Radius(plt, ax, data, xticks=None, yticks=None):
  data = list(doFilters(data, hasRadius, hasPeriod))
  print("Points.:", len(data))

  return (
    x_Period(plt, ax, data, xticks),
    y_Radius(plt, ax, data, yticks) # Planets
  )

def Mass_Radius(plt, ax, data, xticks=None, yticks=None):
  data = list(doFilters(data, hasRadius, hasMass))
  print("Points.:", len(data))

  return (
    x_Mass(plt, ax, data, xticks),
    y_Radius(plt, ax, data, yticks)
  )

def Mass_Density(plt, ax, data, xticks=None, yticks=None):
  data = list(doFilters(data, hasRadius, hasMass))
  print("Points.:", len(data))

  return (
    x_Mass(plt, ax, data, xticks),
    y_Density(plt, ax, data, yticks)
  )

def Mass_Luminosity(plt, ax, data, xticks=None, yticks=None):
  data = list(doFilters(data, hasMass, hasLuminosity))
  print("Points.:", len(data))

  return (
    x_Mass(plt, ax, data, xticks),
    y_Luminosity(plt, ax, data, yticks)
  )

def Luminosity_Mass(plt, ax, data, xticks=None, yticks=ticks_m_stars):
  data = list(doFilters(data, hasMass, hasLuminosity))
  print("Points.:", len(data))

  return (
    x_Luminosity(plt, ax, data, xticks),
    y_Mass(plt, ax, data, yticks),
  )

def Temperature_Mass(plt, ax, data, xticks=None, yticks=ticks_m_stars):
  data = list(doFilters(data, hasMass, hasTemperature))
  print("Points.:", len(data))

  return (
    x_Temperature(plt, ax, data, xticks),
    y_Mass(plt, ax, data, yticks),
  )

def Temperature_Magnitude(plt, ax, data, xticks=None, yticks=None):
  data = list(doFilters(data, hasMass, hasMagnitude))
  print("Points.:", len(data))

  return (
    x_Temperature(plt, ax, data, xticks),
    y_Magnitude(plt, ax, data, yticks),
  )
