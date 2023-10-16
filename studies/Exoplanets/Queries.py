#!/usr/bin/env python3
###############################################################################
#
# Test plots to see that star database seems fine
#
###############################################################################

import os, sys
sys.path.append(os.path.abspath("."))

from orbtools import *
from orbtools.systems.exoplanets import *

#------------------------------------------------------------------------------

def EarthFlux():
  earthlike = doFilters(planets.values(), hasFlux, lambda x: x.flux > 0.85 and x.flux < 1.15)

  print("Planets:", len(earthlike))

  for planet in earthlike:
    print("%-18s %7.2f %.2f" % (
      planet.name,
      MtoEarth(planet.GM),
      planet.flux,
    ))

EarthFlux()

#------------------------------------------------------------------------------

def EarthDistance():
  earthlike = doFilters(planets.values(), hasFlux, lambda x: x.orbit.a > AU2m(0.9) and x.orbit.a < AU2m(1.1))

  print("Planets:", len(earthlike))

  for planet in earthlike:
    print("%-18s %8.2f %4.2f %7.2f" % (
      planet.name,
      MtoEarth(planet.GM),
      m2AU(planet.orbit.a),
      planet.flux,
    ))

#EarthDistance()
