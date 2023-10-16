#!/usr/bin/env python3
###############################################################################
#
# Studying database stars
#
###############################################################################

import os, sys
sys.path.append(os.path.abspath("."))

from orbtools import *
from orbtools.systems.exoplanets import *

snapshot = doFilters(stars.values(), hasMass, hasTemperature, lambda s: s.GM > 0.815*GM_Sun and s.GM < 0.825*GM_Sun)

print(len(snapshot))

for star in sorted(snapshot, key=lambda x: x.T):
  print("%-12s %-5s %.2f %.2f %.1f" % (
    star.name,
    star.sptype or "-",
    MtoSun(star.GM),
    star.L and star.L or 0,
    star.T and star.T or 0,
  ))
