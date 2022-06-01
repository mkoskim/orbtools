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

Sun = Star("Sun", 1.0, 1.0, sptype = "G2", L=1, T=5772, rotate = TasDays(24.6), dist = 0.00)

Star("Proxima Centauri", 1.100, sptype = "M5",  L = 0.0017, dist = 4.244)
Star("Alpha Centauri A", 1.100, sptype = "G2", L = 1.5190, dist = 4.370)
Star("Alpha Centauri B", 0.907, sptype = "K1", L = 0.5002, dist = 4.370)

Star("Sirius A",         2.063, sptype = "A1", L = 25.40, dist = 8.60)
Star("61 Cygni A",       0.700, sptype = "K5", L = 0.153, dist = 11.41)
Star("61 Cygni B",       0.630, sptype = "K7", L = 0.085, dist = 11.41)

Star("Procyon",          1.499, sptype = "F5",  L = 6.93, dist = 11.46)

Star("Tau Ceti",         0.783, sptype = "G8", L = 0.520, dist = 11.905)

#-------------------------------------------------------------------------------
# More stars in exoplanets.py
#-------------------------------------------------------------------------------

################################################################################
#
# Stars by spectral type
#
################################################################################

Star(None, sptype="F0", MxSun=1.61, RxSun=1.728, L=7.24, T=7220, BV=0.30)
Star(None, sptype="F1", MxSun=1.50, RxSun=1.679, L=6.17, T=7020, BV=0.33)
Star(None, sptype="F2", MxSun=1.46, RxSun=1.622, L=5.13, T=6820, BV=0.37)
Star(None, sptype="F3", MxSun=1.44, RxSun=1.578, L=4.68, T=6750, BV=0.39)
Star(None, sptype="F4", MxSun=1.38, RxSun=1.533, L=4.17, T=6670, BV=0.41)
Star(None, sptype="F5", MxSun=1.33, RxSun=1.473, L=3.63, T=6550, BV=0.44)
Star(None, sptype="F6", MxSun=1.25, RxSun=1.359, L=2.69, T=6350, BV=0.49)
Star(None, sptype="F7", MxSun=1.21, RxSun=1.324, L=2.45, T=6280, BV=0.50)
Star(None, sptype="F8", MxSun=1.18, RxSun=1.221, L=1.95, T=6180, BV=0.53)
Star(None, sptype="F9", MxSun=1.13, RxSun=1.167, L=1.66, T=6050, BV=0.56)

Star(None, sptype="G0", MxSun=1.06, RxSun=1.100, L=1.35, T=5930, BV=0.60)
Star(None, sptype="G1", MxSun=1.03, RxSun=1.060, L=1.20, T=5860, BV=0.62)
Star(None, sptype="G2", MxSun=1.00, RxSun=1.012, L=1.02, T=5770, BV=0.65)
Star(None, sptype="G3", MxSun=0.99, RxSun=1.002, L=0.98, T=5720, BV=0.66)
Star(None, sptype="G4", MxSun=0.985, RxSun=0.991, L=0.91, T=5680, BV=0.67)
Star(None, sptype="G5", MxSun=0.98, RxSun=0.977, L=0.89, T=5660, BV=0.68)
Star(None, sptype="G6", MxSun=0.97, RxSun=0.949, L=0.79, T=5600, BV=0.70)
Star(None, sptype="G7", MxSun=0.95, RxSun=0.927, L=0.74, T=5550, BV=0.71)
Star(None, sptype="G8", MxSun=0.94, RxSun=0.914, L=0.68, T=5480, BV=0.73)
Star(None, sptype="G9", MxSun=0.90, RxSun=0.853, L=0.55, T=5380, BV=0.78)

Star(None, sptype="K0", MxSun=0.88, RxSun=0.813, L=0.46, T=5270, BV=0.82)
Star(None, sptype="K1", MxSun=0.86, RxSun=0.797, L=0.41, T=5170, BV=0.86)
Star(None, sptype="K2", MxSun=0.82, RxSun=0.783, L=0.37, T=5100, BV=0.88)
Star(None, sptype="K3", MxSun=0.78, RxSun=0.755, L=0.28, T=4830, BV=0.99)
Star(None, sptype="K4", MxSun=0.73, RxSun=0.713, L=0.20, T=4600, BV=1.09)
Star(None, sptype="K5", MxSun=0.70, RxSun=0.701, L=0.17, T=4440, BV=1.15)
Star(None, sptype="K6", MxSun=0.69, RxSun=0.669, L=0.14, T=4300, BV=1.24)
Star(None, sptype="K7", MxSun=0.64, RxSun=0.630, L=0.10, T=4100, BV=1.34)
Star(None, sptype="K8", MxSun=0.62, RxSun=0.615, L=0.087, T=3990, BV=1.36)
Star(None, sptype="K9", MxSun=0.59, RxSun=0.608, L=0.079, T=3930, BV=1.40)

Star(None, sptype="M0", MxSun=0.57, RxSun=0.588, L=0.069, T=3850, BV=1.42)
Star(None, sptype="M1", MxSun=0.50, RxSun=0.501, L=0.041, T=3660, BV=1.49)
Star(None, sptype="M2", MxSun=0.44, RxSun=0.446, L=0.029, T=3560, BV=1.51)
Star(None, sptype="M3", MxSun=0.37, RxSun=0.361, L=0.016, T=3430, BV=1.53)
Star(None, sptype="M4", MxSun=0.23, RxSun=0.274, L=7.2e-3, T=3210, BV=1.65)
Star(None, sptype="M5", MxSun=0.162, RxSun=0.196, L=3.0e-3, T=3060, BV=1.83)
Star(None, sptype="M6", MxSun=0.102, RxSun=0.137, L=1.0e-3, T=2810, BV=2.01)
Star(None, sptype="M7", MxSun=0.090, RxSun=0.120, L=6.5e-4, T=2680, BV=2.12)
Star(None, sptype="M8", MxSun=0.085, RxSun=0.114, L=5.2e-4, T=2570, BV=2.15)
Star(None, sptype="M9", MxSun=0.079, RxSun=0.102, L=3.0e-4, T=2380, BV=2.17)
