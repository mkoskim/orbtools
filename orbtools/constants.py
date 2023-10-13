###############################################################################
#
# Constants
#
###############################################################################

from math import pi

Inf         = float("infinity")

const_G     = 6.67408e-11               # Gravity constant
const_c     = 299.792458e6              # Speed of light
const_g     = 9.80665                   # Standard gravity
const_day   = 24*3600.0                 # Day in seconds
const_year  = 365.25*const_day          # Year in seconds
const_AU    = 149.597870691e9           # Astronomical Unit
const_ly    = const_c*const_year        # Light year
const_solar = 1.361e3                   # Solar constant
const_Lsol  = 3.828e26                  # Solar luminosity
const_h     = 6.62607015e-34		        # Planc constant (Js)
const_kb    = 1.38064852e-23            # Boltzmann constant (J/K)
const_sb    = 5.670374419e-8            # Stefan-Boltzmann constant (W/(m2 K2)
const_NA    = 6.0221409e+23             # Avogadro constant
const_R     = 8.3144598                 # Gas constant (NA * kb)
const_eV    = 1.60218e-19               # eV in Joules

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
GM_Neptune  = 5.79394700000e15

r_Sun       = 695_508e3
r_Jupiter   =  69_911e3
r_Earth     =   6_372.167e3

V_Earth     = 4/3.0*pi*(r_Earth ** 3)
V_Sun       = 4/3.0*pi*(r_Sun ** 3)

#------------------------------------------------------------------------------
# Luminosity

L_Mag0 = 3.0128e28
L_Sun  = 3.828e26

# Solar flux at Frost Line (Sol 2.7AU)

flux_FrostLine = 0.1371742112482853
