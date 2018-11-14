###############################################################################
#
# Approximating travel times
#
###############################################################################

import os, sys
sys.path.append(os.path.abspath("."))

from orbtools.systems.solsystem import *
from orbtools.systems.exoplanets import *

for m in [Moon, Mars, Earth, masses["SuperEarth"], masses["GiantEarth"]]:
    print "Name..........:", m.name
    print "- Mass........:", m.GM / GM_Earth
    print "- Radius......:", m.radius / Earth.radius
    print "- Density.....:", m.density
    print "- g...........:", m.g_surface / Earth.g_surface

    o = Altitude(m, 300e3)
    print "- v (300 km)..:", abs(o.v())
    print "- P (300 km)..:", fmttime(o.P)

