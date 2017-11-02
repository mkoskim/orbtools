###############################################################################
#
# Orbtools unit tests: Testing Kepler's equations
#
###############################################################################

import os, sys
sys.path.append(os.path.abspath(".."))

from sol import *

#------------------------------------------------------------------------------
# Showing relative error as percentage
#------------------------------------------------------------------------------

def error(computed, correct):
    return (abs(correct - computed) / correct) * 100.0

#------------------------------------------------------------------------------
# Solving Jupiter's period (11.8 years)
#------------------------------------------------------------------------------

print "Jupiter period..: diff = %.3f %%" % error(solve_aPaP(1, 1, 5.2, None), 11.862)
print "Jupiter distance: diff = %.3f %%" % error(solve_aPaP(1, 1, None, 11.86), 5.2044)

#------------------------------------------------------------------------------
# Solving GM from circular orbit paramters
#------------------------------------------------------------------------------

print "Sun mass:         diff = %.3f %%" % error(solve_GM_from_aP(AU2m(1), TasYears(1.0)), GM_Sun)

#------------------------------------------------------------------------------
# Solving GM from gravity acceleration
#------------------------------------------------------------------------------

print "Earth mass:       diff = %.3f %%" % error(solve_GM_from_rg(Earth.radius, const_g), GM_Earth)
print "Jupiter mass:     diff = %.3f %%" % error(solve_GM_from_rg(Jupiter.radius, 24.79), GM_Jupiter)
                                            
#------------------------------------------------------------------------------
# Solving escape velocities from different bodies
#------------------------------------------------------------------------------

print "Earth v_esc:      diff = %.3f %%" % error(solve_rvrv(Earth.GM, Inf, 0, Earth.radius, None), 11.186e3)
print "Jupiter v_esc:    diff = %.3f %%" % error(solve_rvrv(Jupiter.GM, Inf, 0, Jupiter.radius, None), 59.5e3)

#------------------------------------------------------------------------------
# Mass info is partly computed, it is possible to check if there are errors
#------------------------------------------------------------------------------

Earth.info()
