################################################################################
#
# Star Database
#
################################################################################

from orbtools import *

#-------------------------------------------------------------------------------
# Magnitude to luminosity (x Sun) conversion
#-------------------------------------------------------------------------------

def mag2L(mag): return 10 ** ((4.85 - mag) / 2.5)

################################################################################
#
# Real stars
#
################################################################################

Sun = Star("Sun", 1.0, 1.0, sptype = "G2V", rotate = TasDays(24.6), dist = 0.00)

Star("Proxima Centauri", 1.100, sptype = "M5",  L = 0.0017, dist = 4.244)
Star("Alpha Centauri A", 1.100, sptype = "G2V", L = 1.5190, dist = 4.370)
Star("Alpha Centauri B", 0.907, sptype = "K1V", L = 0.5002, dist = 4.370)

Star("Sirius A",         2.063, sptype = "A1V", L = 25.40, dist = 8.60)
Star("Epsilon Eridani",  0.820, sptype = "K2V", L = 0.340, dist = 10.475)
Star("61 Cygni A",       0.700, sptype = "K5V", L = 0.153, dist = 11.41)
Star("61 Cygni B",       0.630, sptype = "K7V", L = 0.085, dist = 11.41)

Star("Procyon",          1.499, sptype = "F5",  L = 6.93, dist = 11.46)

Star("Tau Ceti",         0.783, sptype = "G8V", L = 0.520, dist = 11.905)

Star("Gliese 581", 0.310, 0.299,  sptype = "M3V", L = 0.013000, dist = 20.56, rotate = TasDays(132.5))
Star("TRAPPIST-1", 0.089, 0.121,  sptype = "M8V", L = 0.000522, dist = 39.60, rotate = TasDays(3.295))		
Star("61 Virginis", 0.93, 0.9867, sptype = "G7V", L = 0.822200, dist = 27.90)		

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


