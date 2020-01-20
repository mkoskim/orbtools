################################################################################
#
# Some exoplanet systems
#
################################################################################

from orbtools import *

################################################################################
#
# Gliese 581 (M3V type red dwarf) & planets
#
################################################################################

Mass("Gliese 581e",      1.70 * GM_Earth, orbit = Orbit("Gliese 581", AU2m(0.02815)))
Mass("Gliese 581b",     15.80 * GM_Earth, orbit = Orbit("Gliese 581", AU2m(0.04061)))
Mass("Gliese 581c",      5.50 * GM_Earth, orbit = Orbit("Gliese 581", AU2m(0.07210)))
Mass("Gliese 581g (?)",  2.20 * GM_Earth, orbit = Orbit("Gliese 581", AU2m(0.13000)))
Mass("Gliese 581d (?)",  6.98 * GM_Earth, orbit = Orbit("Gliese 581", AU2m(0.21847)))

################################################################################
#
# TRAPPIST-1 (M8 type dwarf star) & planets
#
################################################################################

Mass("TRAPPIST-1b",  1.017 * GM_Earth, radius = 1.121 * r_Earth, orbit = Orbit("TRAPPIST-1", AU2m(0.01154775)))
Mass("TRAPPIST-1c",  1.156 * GM_Earth, radius = 1.095 * r_Earth, orbit = Orbit("TRAPPIST-1", AU2m(0.01581512)))
Mass("TRAPPIST-1d",  0.297 * GM_Earth, radius = 0.784 * r_Earth, orbit = Orbit("TRAPPIST-1", AU2m(0.02228038)))
Mass("TRAPPIST-1e",  0.772 * GM_Earth, radius = 0.910 * r_Earth, orbit = Orbit("TRAPPIST-1", AU2m(0.02928285)))
Mass("TRAPPIST-1f",  0.934 * GM_Earth, radius = 1.046 * r_Earth, orbit = Orbit("TRAPPIST-1", AU2m(0.03853361)))
Mass("TRAPPIST-1g",  1.148 * GM_Earth, radius = 1.148 * r_Earth, orbit = Orbit("TRAPPIST-1", AU2m(0.04687692)))
Mass("TRAPPIST-1h",  0.331 * GM_Earth, radius = 0.773 * r_Earth, orbit = Orbit("TRAPPIST-1", AU2m(0.06193488)))

################################################################################
#
# 61 Virginis (G7V type star) & planets
#
################################################################################

Mass("61 Virginis b",      5.3 * GM_Earth, orbit = Orbit("61 Virginis", AU2m(0.050201)))
Mass("61 Virginis c",     18.8 * GM_Earth, orbit = Orbit("61 Virginis", AU2m(0.2175)))
Mass("61 Virginis d (?)", 23.7 * GM_Earth, orbit = Orbit("61 Virginis", AU2m(0.476)))

################################################################################

Mass("Gliese 876d", 6.83 * GM_Earth, radius = 1.65 * r_Earth)
Mass("Test", 2 * GM_Earth, radius = 1 * r_Earth)

