################################################################################
#
# Some exoplanet systems
#
################################################################################

from orbtools import *

################################################################################
#
# Example main sequence stars
#
################################################################################

A_star = Star("A-class star", 2.0) # 1.40 - 2.10 solar masses (example: Sirius A)
F_star = Star("F-class star", 1.2) # 1.04 - 1.40 solar masses
G_star = Star("G-class star", 1.0) # 0.80 - 1.04 solar masses (example: Sun)
K_star = Star("K-class star", 0.7) # 0.45 - 0.80 solar masses (example: 61 Cygni A)
M_star = Star("M-class star", 0.2) # 0.08 - 0.45 solar masses (example: M4V class star)

################################################################################
#
# Gliese 581 (M3V type red dwarf) & planets
#
################################################################################

Gliese581  = Star("Gliese 581", 0.31, 0.299, TasDays(132.5), L = 0.013)		

Gliese581e = Mass("Gliese 581e",      1.70 * GM_Earth, orbit = Orbit(Gliese581, AU2m(0.02815)))
Gliese581b = Mass("Gliese 581b",     15.80 * GM_Earth, orbit = Orbit(Gliese581, AU2m(0.04061)))
Gliese581c = Mass("Gliese 581c",      5.50 * GM_Earth, orbit = Orbit(Gliese581, AU2m(0.07210)))
Gliese581g = Mass("Gliese 581g (?)",  2.20 * GM_Earth, orbit = Orbit(Gliese581, AU2m(0.13000)))
Gliese581d = Mass("Gliese 581d (?)",  6.98 * GM_Earth, orbit = Orbit(Gliese581, AU2m(0.21847)))

################################################################################
#
# TRAPPIST-1 (M8 type dwarf star) & planets
#
################################################################################

TRAPPIST1  = Star("TRAPPIST-1", 0.089, 0.121, TasDays(3.295), L = 0.000522)		

TRAPPIST1b = Mass("TRAPPIST-1b",  1.017 * GM_Earth, radius = 1.121 * r_Earth, orbit = Orbit(TRAPPIST1, AU2m(0.01154775)))
TRAPPIST1c = Mass("TRAPPIST-1c",  1.156 * GM_Earth, radius = 1.095 * r_Earth, orbit = Orbit(TRAPPIST1, AU2m(0.01581512)))
TRAPPIST1d = Mass("TRAPPIST-1d",  0.297 * GM_Earth, radius = 0.784 * r_Earth, orbit = Orbit(TRAPPIST1, AU2m(0.02228038)))
TRAPPIST1e = Mass("TRAPPIST-1e",  0.772 * GM_Earth, radius = 0.910 * r_Earth, orbit = Orbit(TRAPPIST1, AU2m(0.02928285)))
TRAPPIST1f = Mass("TRAPPIST-1f",  0.934 * GM_Earth, radius = 1.046 * r_Earth, orbit = Orbit(TRAPPIST1, AU2m(0.03853361)))
TRAPPIST1g = Mass("TRAPPIST-1g",  1.148 * GM_Earth, radius = 1.148 * r_Earth, orbit = Orbit(TRAPPIST1, AU2m(0.04687692)))
TRAPPIST1h = Mass("TRAPPIST-1h",  0.331 * GM_Earth, radius = 0.773 * r_Earth, orbit = Orbit(TRAPPIST1, AU2m(0.06193488)))

################################################################################
#
# 61 Virginis (G7V type star) & planets
#
################################################################################

Virginis61  = Star("61 Virginis", 0.93, 0.9867, L = 0.8222)		

Virginis61b = Mass("61 Virginis b",      5.3 * GM_Earth, orbit = Orbit(Virginis61, AU2m(0.050201)))
Virginis61c = Mass("61 Virginis c",     18.8 * GM_Earth, orbit = Orbit(Virginis61, AU2m(0.2175)))
Virginis61d = Mass("61 Virginis d (?)", 23.7 * GM_Earth, orbit = Orbit(Virginis61, AU2m(0.476)))


