#!/usr/bin/env python3
###############################################################################
#
# Exoplanet database utilities: filtering, checking and so on
#
###############################################################################

import os, sys
sys.path.append(os.path.abspath("."))

from orbtools import *
from orbtools.systems.exoplanets import *

#------------------------------------------------------------------------------
# Reporting
#------------------------------------------------------------------------------

def showStars(data):
  for star in data:
    try:
      print("%-20s %-13s M=%5.2f" % (star.name, star.sptype, MtoSun(star.GM)),
        "L=%7s" % (star.L and "%.2f" % float(star.L)),
        "T=%s" % (star.T and "%.0f" % float(star.T)),
        "Planets: %d" % len(star.satellites)
      )
    except:
      print("ERROR:", star.name)
      exit()

def showPlanets(data):
  print("Points:", len(data))
  for planet in data:
    try:
      print("%-20s M=%7.2f R=%7.2f" % (planet.name, MtoEarth(planet.GM or 0), RtoEarth(planet.radius or 0)),
        #"D=%5.0f" % planet.density,
        #"F=%7.2f" % planet.flux,
        "P=%7.2f" % TtoDays(planet.orbit.P),
        "F=%7.2f" % planet.flux,
      )
    except:
      print("ERROR:", planet.name)
      exit()

#------------------------------------------------------------------------------
# Search stars missing luminosity, and list ones with most planets
#------------------------------------------------------------------------------

# Some systems are (ATM) unfixable, parameters are not yet available
def isFixable(star):
  unfixables = [
    "HD 10180",     # Radii not known
    "Kepler-90",    # Masses not known
    "Gliese 667 C", # Planets not found
    "tau Ceti",     # Radii not known
    "Gliese 581",   # Radii not known
    "HD 34445",     # Radii
    "HD 40307",     # Radii
    "GJ 163",       # Radii
    "HD 158259",    # Radii
    "HD 219134",    # Radii
    "Kepler-122",   # Mass
    "Kepler-169",   # Mass
    "Kepler-238",   # Mass
    "Kepler-292",   # Mass
    "Kepler-296 A", # Mass
    "Kepler-32",    # Mass
    "Kepler-444 A", # Mass
    "Kepler-55",    # Mass
    "Kepler-84",    # Mass
    "55 Cancri A",  # Radii
    "DMPP-1",       # Radii
    "Gliese 221",   # Radii
    "Gliese 676 A", # Radii
    "Gliese 876",   # Radii
    "HD 141399",    # Radii
    "HD 1461",      # Radii
    "HD 20794",     # Radii
    "HD 215152",    # Radii
    "K2-133",       # Mass
    "K2-187",       # Mass
    "K2-72",        # Mass
    "Kepler-107",   # Mass uncertainty
  ]

  return not star.name in unfixables

def topStarsToFix():
  top = doFilters(stars.values(), lambda x: not hasLuminosity(x))
  top.sort(key = lambda x: len(x.satellites), reverse=True)
  showStars(top[:10])

#topStarsToFix()

#------------------------------------------------------------------------------
# Search systems with incomplete star/planets resulting highest gain
#------------------------------------------------------------------------------

def topSystemsToFix():

  print("Top systems to fix:")

  incompletePlanets = doFilters(planets.values(), lambda x: not hasMass(x) or not hasRadius(x) or not hasFlux(x))

  def numIncompleteSatellites(star):
    incomplete = doFilters(incompletePlanets, lambda x: x.system == star)
    return len(incomplete)

  top = doFilters(stars.values(), isFixable)
  top.sort(key = lambda x: numIncompleteSatellites(x), reverse=True)

  showStars(top[:10])

  print("Top pick:")
  showPlanets(top[0].satellites)

topSystemsToFix()

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
