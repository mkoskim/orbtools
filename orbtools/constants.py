###############################################################################
#
# Constants
#
###############################################################################

from math import pi

const_G   = 6.67408e-11
const_c   = 299.792458e6
const_g   = 9.80665
const_day = 24*3600.0
const_year = 365.25*const_day
const_AU = 149.597870691e9
const_ly = const_c*const_year

Inf = float("infinity")

#------------------------------------------------------------------------------
#
# GM table for Solar System: Useful for creating own solar systems, using
# masses of Sun, Earth and Jupiter to define star/planet masses.
#
#------------------------------------------------------------------------------

GM_Sun      = 1.32712440018e20
GM_Mercury  = 2.20320000000e13
GM_Venus    = 3.24859000000e14
GM_Earth    = 3.98600441800e14
GM_Mars     = 4.28280000000e13
GM_Jupiter  = 1.26686534000e17
GM_Saturnus = 3.79311870000e16
GM_Uranus   = 6.83652900000e15
GM_Neptunus = 5.79394700000e15

r_Earth     = 6372.167e3
V_Earth     = 4/3.0*pi*(r_Earth ** 3)
