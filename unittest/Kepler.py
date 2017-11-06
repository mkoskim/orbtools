###############################################################################
#
# Orbtools unit tests: Testing Kepler's equations
#
###############################################################################

import os, sys
sys.path.append(os.path.abspath(".."))

from sol import *
from testlib import *

#-------------------------------------------------------------------------------
# Solving Earth & Jupiter axis (AU) and period (a), with Kepler's eq.
#-------------------------------------------------------------------------------

def test_Kepler():
    runcase()
    expect(solve_aPaP(None, 1.0,  5.2,  11.86),   1.0, 1e-2, "1")
    expect(solve_aPaP(1.0,  None, 5.2,  11.86),   1.0, 1e-2, "2")
    expect(solve_aPaP(1.0,  1.0,  None, 11.86),   5.2, 1e-2, "3")
    expect(solve_aPaP(1.0,  1.0,  5.2,   None), 11.86, 1e-2, "4")

test_Kepler()

#------------------------------------------------------------------------------
# Solving GM
#------------------------------------------------------------------------------

def test_SolveGM():
    runcase()

    # Solve Sun mass from Earth orbit parameters
    expect(solve_GM_from_aP(AU2m(1), TasYears(1.0)) / GM_Sun,     1.0, 1e-2, "1")

    # Calculate Mars mass ~ 6.42e23 kg from Phobos orbit parameters
    expect(GM2kg(solve_GM_from_aP(9380e3, TasDHMS(0, 7, 39.5, 0))), 6.42e23, 0.01e23, "2")

    Phobos = masses["Phobos"].orbit
    expect(solve_GM_from_aP(Phobos.a, Phobos.P) / GM_Mars, 1.0, 1e-3, "3")

    # Solve Earth/Jupiter mass from radius and surface g
    expect(solve_GM_from_rg(Earth.radius, const_g)  / GM_Earth,   1.0, 1e-2, "4")
    expect(solve_GM_from_rg(Jupiter.radius, 24.79)  / GM_Jupiter, 1.0, 1e-2, "5")

test_SolveGM()
