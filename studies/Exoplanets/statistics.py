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

print("Planets:", len(planets))

withPlanets = [x for x in stars.values() if x.hasSatellites]

print("Stars with planets:", len(withPlanets))

withSptype = [x for x in withPlanets if x.sptype != None]

print("Stars with sptype:", len(withSptype))

print("- M:", len([x for x in withSptype if x.sptype[0] == "M"]))
print("- K:", len([x for x in withSptype if x.sptype[0] == "K"]))
print("- G:", len([x for x in withSptype if x.sptype[0] == "G"]))
print("- F:", len([x for x in withSptype if x.sptype[0] == "F"]))

exit()

dwarfs = [x for x in withPlanets if x.GM < Star.typical["M0"].GM]
mid    = [x for x in withPlanets if x.GM > Star.typical["M0"].GM and x.GM < Star.typical["F0"].GM]

print("M < M0:", len(dwarfs))
print("M = [M0 ... F0]:", len(mid))

print([x.sptype for x in mid])
exit()

def byStar(planets, m_min, m_max):
    return [
        x for x in planets.values() if x.orbit.center.GM > m_min and x.orbit.center.GM < m_max
    ]

dwarfs = byStar(planets, 0, Star.typical["M0"].GM)

print("   ... M0:", len(dwarfs))
print("M0 ... F0:", len(byStar(planets, Star.typical["M0"].GM, Star.typical["F0"].GM)))
print("F0 ...   :", len(byStar(planets, Star.typical["F0"].GM, Inf)))
