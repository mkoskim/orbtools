################################################################################
#
# Some exoplanet systems
#
################################################################################

import os, sys
sys.path.append(os.path.abspath("."))

from sol import *
from testlib  import *

#-------------------------------------------------------------------------------

#print mag2L(11.6),  0.013    # Gliese 581
#print Star.MLR(1.1),   mag2L(4.38), 1.519    # Alpha Centauri A
#print Star.MLR(0.907), mag2L(5.71), 0.5002   # Alpha Centauri B

for name in sorted(stars, key = lambda name: -stars[name].L):
    if stars[name].dist is None: continue
    star = stars[name]
    HZ = star.orbitByFlux()
    print "%-20s %3s %5.2f %5.2f %5.2f %.2f %10s" % (
        star.name,
        star.sptype,
        m2ly(star.dist),
        star.GM / GM_Sun,
        star.L,
        m2AU(HZ.a),
        fmttime(HZ.P),
    )

