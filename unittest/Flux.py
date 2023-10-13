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

print(Earth.flux)

print(Star.LtoT(Sun.L, Sun.radius))
print(Sun.T)

print(Star.TtoL(Sun.T, Sun.radius))
print(Sun.L)

print("Moon:", T_KtoC(Star.LtoT(Sun.L * (1-0.12), Earth.orbit.a)))

print(Star.LtoT(Sun.L * (1-0.309) * 0.25, Earth.orbit.a))
print(Sun.T_eff(Earth.orbit.a, 0.309))

print(Star.LtoT(Sun.L * (1-0.503) * 0.25, Jupiter.orbit.a))
print(Sun.T_eff(Jupiter.orbit.a, 0.503))
