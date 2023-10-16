#!/usr/bin/env python3
###############################################################################
#
# Info from solar system
#
###############################################################################

import os, sys
sys.path.append(os.path.abspath("."))

from orbtools import *
from orbtools.systems.solsystem import *

import functools

#------------------------------------------------------------------------------
# How much moons weight compared to their host planet?

planets = [Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto]

for planet in planets:
  GM_moons = functools.reduce(lambda a, b: a+b.GM, planet.satellites, 0)

  print("%-10s %.2f" % (planet.name, GM_moons and planet.GM / GM_moons or 0))
