###############################################################################
#
# Flux & temperature calculations
#
###############################################################################

import os, sys
sys.path.append(os.path.abspath("."))

from orbtools.systems.solsystem import *
#from orbtools.systems.exoplanets import *

from testlib import *

#------------------------------------------------------------------------------

print("Solar constant")
print("- Solar constant:", const_solar)
print("- Computed......:", Sun.L * L_Sun / A_sphere(Earth.orbit.a))
print()

#------------------------------------------------------------------------------

print("Stars:")
K0 = Star.typical["K0"]
print("- T(K0)...........:", K0.T)
print("- T(K0) calculated:", Star.LtoT(K0.L, K0.radius))
print("- T(K0) calculated:", Star.fluxToT(Star.L2flux(K0.L, K0.radius)))
print()

#------------------------------------------------------------------------------

print("Sun luminosity & temperature")
print("- T.......:", Sun.T)
print("- T from L:", Star.LtoT(Sun.L, Sun.radius))
print("- L.......:", Sun.L)
print("- L from T:", Star.TtoL(Sun.T, Sun.radius))

print("Flux & temperature at Sun surface:")
SunFlux = Sun.fluxAt(Sun.radius)
print("- Flux.........: %.2f x Earth" % SunFlux)
print("- Temperature..: %.0f K" % Star.fluxToT(SunFlux))

print()

print("Earth flux:")
print("- Flux........:", Earth.flux)
print("- Computed....:", Sun.L * L_Sun / A_sphere(Earth.orbit.a) / const_solar)
#print("- Computed....:", Sun.L * L_Sun / A_sphere(Earth.orbit.a))

print("Earth temperatures:")
Earth_T    = Star.fluxToT(Earth.flux)
Earth_Teff = Star.fluxToT(Earth.flux * 0.25 * (1 - 0.306))
print("- Flux --> T......: %.2f K" % Earth_T)
print("- Flux --> T......: %+.2f C" % T_KtoC(Earth_T))
print("- Flux --> T(eff).: %.2f K" % Earth_Teff)
print("- Flux --> T(eff).: %+.2f C" % T_KtoC(Earth_Teff))

print("Moon temperatures:")
Moon_Teff  = Star.fluxToT(Moon.flux * (1 - 0.136) * 0.25)
print("- Flux --> T......: %+.2f C" % T_KtoC(Moon_Teff))
#print("Moon:", T_KtoC(Star.LtoT(Sun.L * (1-0.12), Earth.orbit.a)))

print()

#------------------------------------------------------------------------------

print("Mercury temperatures:")

Mercury_Tperi = Star.fluxToT(Sun.fluxAt(46e9) * (1 - 0.088))
Mercury_T     = Star.fluxToT(Mercury.flux)
Mercury_Teff  = Star.fluxToT(Mercury.flux * (1 - 0.088) * 0.25)

print("- Flux --> T (peri).: %+.2f C" % T_KtoC(Mercury_Tperi))
print("- Flux --> T........: %+.2f C" % T_KtoC(Mercury_T))
print("- Flux --> Teff.....: %+.2f C" % T_KtoC(Mercury_Teff))
#print("Moon:", T_KtoC(Star.LtoT(Sun.L * (1-0.12), Earth.orbit.a)))

print("Mars temperatures:")

Mars_T     = Star.fluxToT(Mars.flux)
Mars_Teff  = Star.fluxToT(Mars.flux * (1 - 0.250) * 0.25)

print("- Flux --> T......: %+.2f C" % T_KtoC(Mars_T))
print("- Flux --> Teff...: %+.2f C" % T_KtoC(Mars_Teff))
#print("Moon:", T_KtoC(Star.LtoT(Sun.L * (1-0.12), Earth.orbit.a)))

print()

#------------------------------------------------------------------------------

print(Star.LtoT(Sun.L * (1-0.309) * 0.25, Earth.orbit.a))
print(Sun.T_eff(Earth.orbit.a, 0.309))
#print(Star.fluxToTeff(Earth.flux, 0.309))
#print(Earth.fluxToTeff(0.309))

print(Star.fluxToT(Earth.flux))
print(T_KtoC(Star.fluxToT(Earth.flux)))
#print(Earth.fluxToT)

print()

#------------------------------------------------------------------------------
print("Frost line:")
FrostLine_flux = Star.TtoFlux(T_CtoK(0))
FrostLine_r    = Sun.fluxToR(FrostLine_flux)
FrostLine_T    = Star.fluxToT(FrostLine_flux)
print("- flux..: %.2f" % FrostLine_flux)
print("- r.....: %.2f AU" % m2AU(FrostLine_r))
print("- T.....: %.2f K" % FrostLine_T)
print("- T.....: %+.2f C" % T_KtoC(FrostLine_T))

print()

#------------------------------------------------------------------------------

print("Jupiter:")
Jupiter_T = Star.fluxToT(Jupiter.flux)
print("- T.....: %.2f K" % Jupiter_T)
print("- T.....: %+.2f C" % T_KtoC(Jupiter_T))
print("- T(eff):", Star.LtoT(Sun.L * (1-0.503) * 0.25, Jupiter.orbit.a))
print("- T(eff):", Sun.T_eff(Jupiter.orbit.a, 0.503))
