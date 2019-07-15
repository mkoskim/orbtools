###############################################################################
#
# Different solar routes
#
###############################################################################

import os, sys
sys.path.append(os.path.abspath(".."))
sys.path.append(os.path.abspath("."))

from sol import *

#------------------------------------------------------------------------------
# LaGrange points (Earth, Mars, ...)
#------------------------------------------------------------------------------

def LaGrange(body, angle):
    body = Mass.resolve(body)
    a = a_from_P(body.orbit.center.GM, body.orbit.P * (360 + angle)/360.0)
    o = Orbit(body.orbit.center, body.orbit.r(), 2*a - body.orbit.r())

    dv = abs(o.v() - body.orbit.v())

    print(body.name, angle, fmttime(o.P), fmteng(dv, "m/s"), fmteng(dv, "m/s"))

LaGrange("Earth", +60.0)
LaGrange("Earth", -60.0)
LaGrange("Mars", +60.0)
LaGrange("Mars", -60.0)
LaGrange("Ceres", +60.0)
LaGrange("Ceres", -60.0)

