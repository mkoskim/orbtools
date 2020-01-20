###############################################################################
#
# Approximating habitable zones
#
###############################################################################

import os, sys
sys.path.append(os.path.abspath("."))

from orbtools.systems.solsystem import *
from orbtools.systems.exoplanets import *

examples = [
    Star("Gamma Virginis",       1.7,  L = 6.0,  sptype = "F0"),
    Star("Eta Arietis",          1.3,  L = 2.5,  sptype = "F5"),
    Star("Beta Comae Berenices", 1.1,  L = 1.26, sptype = "G0"),
    Sun,
    Star("Alpha Mensae",         0.93, L = 0.79, sptype = "G5"),
    Star("70 Ophiuchi A",        0.78, L = 0.40, sptype = "K0"),
    Star("61 Cygni A",           0.69, L = 0.16, sptype = "K5"),
]

flux_Venus = Venus.flux
flux_Earth = Earth.flux
flux_Mars  = Mars.flux

print flux_Venus, flux_Mars * const_solar
print m2AU(Mars.orbit.a), TtoDays(Mars.orbit.P)
print m2AU(Venus.orbit.a), TtoDays(Venus.orbit.P)

for star in examples:
    HZ_inner = star.orbitByFlux(flux_Venus)
    HZ_earth = star.orbitByFlux(flux_Earth)
    HZ_outer = star.orbitByFlux(flux_Mars)

    #print("%3s\t%4.1f\t%8s\t%.1f\t%8s\t%.1f\t%8s\t%.1f" % (
    #    star.sptype,
    #    TtoYears(Star.TMS(star.GM / GM_Sun)) / 1e9,
    #    fmttime(HZ_inner.P), m2AU(HZ_inner.a),
    #    fmttime(HZ_earth.P), m2AU(HZ_earth.a),
    #    fmttime(HZ_outer.P), m2AU(HZ_outer.a),
    #))

    print("%3s\t%.0f\t%.0f\t%.1f" % (
        star.sptype,
        TtoDays(HZ_inner.P),
        TtoDays(HZ_earth.P),
        TtoDays(HZ_outer.P),
    ))


