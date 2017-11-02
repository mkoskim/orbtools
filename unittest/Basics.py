################################################################################
#
# Unit tests: Orbital calculation toolbox
#
################################################################################

import os, sys
sys.path.append(os.path.abspath(".."))

from sol import *

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

test_TimePrints()

#-------------------------------------------------------------------------------
# Solving Earth & Jupiter axis (AU) and period (a), with Kepler's eq.
#-------------------------------------------------------------------------------

def test_Kepler():
    print "--------------------------------------------------"
    print "Testing Kepler's equation solving:"
    print
    print "Kepler: %.2f" % solve_aPaP(None,1,5.2,11.857824421), "== 1.00?"
    print "Kepler: %.2f" % solve_aPaP(1,None,5.2,11.857824421), "== 1.00?"
    print "Kepler: %.2f" % solve_aPaP(1,1,None,11.857824421), "== 5.20?"
    print "Kepler: %.2f" % solve_aPaP(1,1,5.2,None), "== 11.86?"
    print

test_Kepler()

#-------------------------------------------------------------------------------
# Testing GM solving from orbital radius & period
# Calculate Mars mass using Phobos orbit: r = 9380km, P=7h 39.5m
#-------------------------------------------------------------------------------

def test_GMsolving():
    print "--------------------------------------------------"
    print "Testing GM solving from orbital parameters:"
    print

    # Calculate Mars mass ~ 6.42e23 kg (from Phobos orbit parameters)

    print "m(Mars): %.3g" % GM2kg( solve_GM_from_aP(9380e3, TasDHMS(0, 7, 39.5, 0))), "== 6.42e23 kg?"
    print

test_GMsolving()

#-------------------------------------------------------------------------------
# Testing circular & escape velocity calculation
#-------------------------------------------------------------------------------

def test_Vcirc():
    print "--------------------------------------------------"
    print "Testing circular & escape velocity calculation:"
    print
    print "Earth +300km: v(circ) = %5.0f  (7558) m/s" % v_circular(Earth.GM, Earth.radius + 300e3)
    print "Earth +300km: v(esc)  = %5.0f (10689) m/s" % v_escape(Earth.GM, Earth.radius + 300e3)
    print

    o = Orbit(Sun, AU2m(1.0))
    print "Sun @ 1AU, period =", fmttime(o.P)
    print "Sun @ 1AU, v_circ =", o.v(0).length
    print

test_Vcirc()

#-------------------------------------------------------------------------------
# Testing energy equation
#-------------------------------------------------------------------------------

def test_EnergyEq():
    print "--------------------------------------------------"
    print "Testing energy equation solving:"
    print
    print "Sun @ 1AU, esc=", v_escape(GM_Sun, AU2m(1))
    print "Sun @ 1AU, esc=", solve_rvrv(GM_Sun, AU2m(1), None, Inf, 0)
    print

test_EnergyEq()

#-------------------------------------------------------------------------------
# Heitto Deimoksella: M=1.8e15, r0=7490m, v0=4.5m/s
# Solution: apoapsis = 12830 m, nopeus = 2.62 m/s, periodi=5.157 h
#-------------------------------------------------------------------------------

#o = Orbit_from_v(kg2GM(1.8e15), 7490, 4.5)
#print "Apoapsis=", o.apoapsis, "v(ap)=", o.v(o.apoapsis)
#print "P=", o.period()/3600

#-------------------------------------------------------------------------------
# Heitto Deimoksella: M=1.8e15, r0=7490m, r1=r0+50
# Solution: v0 =
#-------------------------------------------------------------------------------

#o = Orbit_elliptical(kg2GM(1.8e15),7490+50,7490)
#print "v0=", o.v(o.periapsis)
#print "v1=", o.v(o.apoapsis)
#print "P=", o.period()/3600

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

test_MassDB()

#-------------------------------------------------------------------------------
# Testing mission setup
#-------------------------------------------------------------------------------

#from mission_mars import *

#print "Stage1:"
#print "   orbits=",   s1.orbit.center.name
#print "   altitude=", engfmt(s1.orbit.altitude(), "m")

