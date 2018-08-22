###############################################################################
#
# Approximating travel times
#
###############################################################################

import os, sys
sys.path.append(os.path.abspath("."))

from orbtools.systems.solsystem import *
from orbtools.systems.exoplanets import *

def approx(A, B, fmt):

    print "%s %.2f %s %.2f %.2f %.2f" % (
        A.name, fmt(A.orbit.P),
        B.name, fmt(B.orbit.P),
        fmt((A.orbit.P + B.orbit.P) / 4),
        fmt(Trajectory(A.orbit.center, A.orbit.a, B.orbit.a).P / 2)
    )

approx(masses["LEO"], Moon, TtoDays)
approx(Earth, Mars, TtoMonths)
approx(Earth, Venus, TtoMonths)
approx(Earth, Jupiter, TtoYears)
approx(Jupiter, Saturn, TtoYears)

