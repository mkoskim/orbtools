#!/usr/bin/env python3

###############################################################################
#
# What if Sun looses half its mass suddenly?
#
###############################################################################

import os, sys
sys.path.append(os.path.abspath("."))

from orbtools.systems.solsystem import *
from orbtools.systems.exoplanets import *

#------------------------------------------------------------------------------

HalfSun = Star.typical["M1"]
print("Mass: %.2f x Sun" % MtoSun(HalfSun.GM))
print("Circular @ 1 AU:", fmteng(v_circular(HalfSun.GM, AU2m(1)), "m/s"))
print("Escape @ 1 AU:", fmteng(v_escape(HalfSun.GM, AU2m(1)), "m/s"))

Earth.orbit.info()

orbit = Orbit(HalfSun, Earth.orbit.r(0), Earth.orbit.r(0) * 50)
#orbit = byRV(HalfSun, Earth.orbit.r(0), abs(Earth.orbit.v(0)))
orbit.info()
