################################################################################
#
# Unit tests: Orbital calculation toolbox
#
################################################################################

import os, sys
sys.path.append(os.path.abspath(".."))

from sol import *
from testlib import *

#-------------------------------------------------------------------------------
# Testing printing
#-------------------------------------------------------------------------------

def test_TimePrints():
    print fmttime( TasDHMS(        0,  0, 0,   2.543e-5) )
    print fmttime( TasDHMS(        0,  0, 0,   2.543e-2) )
    print fmttime( TasDHMS(        0,  0, 0,  43.5) )
    print fmttime( TasDHMS(        0,  0, 32, 43.5) )
    print fmttime( TasDHMS(        0,  1, 13, 12) )
    print fmttime( TasDHMS(        0, 28, 13, 12) )
    print fmttime( TasDHMS(        3,  7, 13, 12) )
    print fmttime( TasDHMS(       38,  7, 13, 12) )
    print fmttime( TasDHMS(      523,  7, 13, 12) )
    print fmttime( TasDHMS(      700,  7, 13, 12) )
    print fmttime( TasDHMS(    5*365,  7, 13, 12) )
    print fmttime( TasDHMS(   35*365,  7, 13, 12) )
    print fmttime( TasDHMS(  145*365,  7, 13, 12) )
    print fmttime( TasDHMS( 4145*365,  7, 13, 12) )
    print fmttime( TasDHMS(56732*365,  7, 13, 12) )
    print

manual(__name__, test_TimePrints)

#-------------------------------------------------------------------------------
# Testing circular & escape velocity calculation
#-------------------------------------------------------------------------------

def test_Vcirc():
    runcase()

    # Velocities around Earth @ 300 km
    expect(v_circular(Earth.GM, Earth.radius + 300e3), 7729, 1, "1")
    expect(v_escape(Earth.GM, Earth.radius + 300e3), 10931, 1, "2")

    # Create orbit around sun @ 1AU (Earth orbit)
    o = Orbit(Sun, AU2m(1.0))
    expect(TtoYears(o.P),     1.0, 1e-3, "3")
    expect(o.v(0).length, 29784.0, 1,    "4")

test_Vcirc()

#-------------------------------------------------------------------------------
# Testing energy equation (by solving escape velocities)
#-------------------------------------------------------------------------------

def test_EnergyEq():
    runcase()
    expect(solve_rvrv(Earth.GM,   Inf, 0, Earth.radius,   None), 11.186e3, 1, "1")
    expect(solve_rvrv(Jupiter.GM, Inf, 0, Jupiter.radius, None), 59.532e3,   1, "2")

    expect(v_escape(GM_Sun, AU2m(1)),                   42121.9, 1, "3")
    expect(solve_rvrv(GM_Sun, AU2m(1), None, Inf, 0),   42121.9, 1, "4")

test_EnergyEq()

#-------------------------------------------------------------------------------
# Testing solar system mass database
#-------------------------------------------------------------------------------

def test_MassDB():
    print "--------------------------------------------------"
    print "Testing mass database:"
    print
    print "Density:"
    print "   Earth.: %7.2f kg/m^3" % Earth.density
    print "   Sun...: %7.2f kg/m^3" % Sun.density
    print "Surface g:"
    print "   Earth.: %7.2f g" % (Earth.g_surface/const_g)
    print "   Sun...: %7.2f g" % (Sun.g_surface/const_g)
    print "Surface escape velocity:"
    print "   Earth.: %7.2f km/s" % (Earth.v_escape()*1e-3)
    print "   Sun...: %7.2f km/s" % (Sun.v_escape()*1e-3)
    print "Earth:"
    print "   orbits= ", Earth.center.name
    print "   dist=   ", fmteng(Earth.orbit.a, "m")
    print "   P   =   ", fmttime(Earth.orbit.P)
    print "   v   =   ", fmteng(Earth.orbit.v(0).length,"m/s")
    print "LEO (300km):"
    LEO = masses["LEO"]
    print "   dist=", fmteng(LEO.orbit.a, "m")
    print "   P   =", fmttime(LEO.orbit.P)
    print "   v   =", fmteng(LEO.orbit.v(0).length,"m/s")
    print

manual(__name__, Earth.info)
manual(__name__, test_MassDB)
