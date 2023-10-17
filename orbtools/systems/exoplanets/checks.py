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

#masses["K2-16"].info()
#exit()

#------------------------------------------------------------------------------
# Testing Luminosity calculation: we have certain set of stars with manually
# added Luminosity, and we can compare the results of calculations
#------------------------------------------------------------------------------

def testLuminosityCalc():
  data = doFilters(stars.values(), hasLuminosity)
  data.sort(key=lambda x: x.GM, reverse=True)

  for star in data:
    if star.radius:
      star.L1 = Star.RT2L(star.radius, star.T)
    else:
      star.L1 = None

    #if star.mag:
    #  star.L2 = Star.mag2L(star.mag)
    #else:
    #  star.L2 = None
    star.L2 = Star.MLR(star.GM / GM_Sun)

    print("%-15s" % (star.name),
      "M=%5s" % (star.GM and "%.2f" % MtoSun(star.GM)),
      "R=%5s" % (star.radius and "%.2f" % RtoSun(star.radius)),
      "T=%s" % (star.T and "%.0f" % float(star.T)),
      "mag=%6s" % (star.mag and "%.2f" % float(star.mag)),
      "L=%7s" % (star.L and "%.4f" % float(star.L)),
      "L1=%7s" % (star.L1 and "%.4f" % float(star.L1)),
      "L2=%7s" % (star.L2 and "%.4f" % float(star.L2)),
    )

#testLuminosityCalc()

#print(Star.magVtoAbs(0.12, ly2m(860))) # Rigel
#print(Star.magVtoAbs(0.12, ly2m(860))) # 61 Cygni A
#print(stars["HD 158259"].elem.findtext("distance"))
#stars["EPIC 211089792"].info()

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
  print("Planets:", len(data))
  for planet in data:
    try:
      print("%-20s M=%7.2f R=%7.2f" % (planet.name, MtoEarth(planet.GM or 0), RtoEarth(planet.radius or 0)),
        #"D=%5.0f" % planet.density,
        #"P=%7.2f" % TtoDays(planet.orbit.P),
        #planet.flux and "F=%7.2f" % planet.flux or None,
        #planet.system.name,
      )
    except:
      print("ERROR:", planet.name)
      exit()

#------------------------------------------------------------------------------
# Search stars missing luminosity, and list ones with most planets
#------------------------------------------------------------------------------

def showMissing(star):
  print("Name:", star.name)
  print("Sp..:", star.sptype)
  for planet in star.satellites:
    print("- ",
      planet.name,
      "M=%s" % planet.elem.findtext("mass"),
      "R=%s" % planet.elem.findtext("radius"),
      planet.elem.findtext("discoverymethod"),
    )

#showMissing(masses["HD 10180"])
#showMissing(masses["Kepler-90"])
#masses["EPIC 22881391 b"].info()
#showMissing(masses["EPIC 228813918"])
#exit()

#------------------------------------------------------------------------------
# These systems are (ATM) unfixable, planet parameters (M & R) are not yet
# available in any source (Wikipedia, NASA catalogue etc).
#------------------------------------------------------------------------------

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

    "PSR 1257+12",  # Pulsar
  ]

  return not star.name in unfixables

#------------------------------------------------------------------------------

def topStarsToFix():
  print("Top stars to fix")
  top = doFilters(stars.values(), lambda x: not hasLuminosity(x), isFixable)
  top.sort(key = lambda x: len(x.satellites), reverse=True)
  showStars(top[:10])

#topStarsToFix()

#stars["Kepler-82"].info()

#------------------------------------------------------------------------------
# Search systems with incomplete star/planets resulting highest gain
#------------------------------------------------------------------------------

def topSystemsToFix():

  print("Top systems to fix:")

  incompletePlanets = doFilters(planets.values(), isFixable, lambda x: not hasMass(x) or not hasRadius(x) or not hasFlux(x))

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
# Planets, which main star misses luminosity
#------------------------------------------------------------------------------

def planetsMissingFlux():

  print("Planets missing flux:")

  fluxless = doFilters(planets.values(), isFluxless)
  #fluxless = doFilters(planets.values(), hasMass, hasRadius, isFluxless)
  fluxless.sort(key=lambda x: x.GM)

  showPlanets(fluxless)

#planetsMissingFlux()

#------------------------------------------------------------------------------
# Planets which density > 10 000 kg/m3 (possible error in either mass or radius)
#------------------------------------------------------------------------------

def ultradensePlanets():

  print("Very dense planets:")

  ultradense = doFilters(planets.values(), hasMass, hasRadius, isUltraDense)
  ultradense.sort(key=lambda x: x.density, reverse=True)

  showPlanets(ultradense)

#ultradensePlanets()
