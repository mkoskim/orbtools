################################################################################
#
# Unit tests: Orbital calculation toolbox
#
################################################################################

from orbits import *

#-------------------------------------------------------------------------------
# Testing printing
#-------------------------------------------------------------------------------

def test_TimePrints():
    print timefmt( time_hms(0,0,43.5) )
    print timefmt( time_hms(0,32,43.5) )
    print timefmt( time_hms(1,13,12) )
    print timefmt( time_hms(28,13,12) )
    print timefmt( time_hms(3*24+7,13,12) )
    print timefmt( time_hms(38*24+7,13,12) )
    print timefmt( time_hms(523*24+7,13,12) )
    print timefmt( time_hms(700*24+7,13,12) )
    print timefmt( time_hms(1523*24+7,13,12) )
    print timefmt( time_hms(11523*24+7,13,12) )
    print timefmt( time_hms(1211523*24+7,13,12) )

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

#-------------------------------------------------------------------------------
# Testing energy equation
#-------------------------------------------------------------------------------

def test_EnergyEq():
    print "--------------------------------------------------"
    print "Testing energy equation solving:"
    print
    print "esc=", v_escape(GM_Sun, AU2m(1))
    print "v2=", solve_v2(GM_Sun,v_escape(GM_Sun,AU2m(1))+200,AU2m(1), None, ly2m(2))

#-------------------------------------------------------------------------------
# Testing GM solving from orbital radius & period
# Calculate Mars mass using Phobos orbit: r = 9380km, P=7h 39.5m
#-------------------------------------------------------------------------------

def test_GMsolving():
    print "--------------------------------------------------"
    print "Testing GM solving from orbital parameters:"
    print

    # Calculate Mars mass ~ 6.42e23 kg (from Phobos orbit parameters)

    print "m(Mars): %.3g" % GM2kg( solve_GM_from_aP(9380e3, time_hms(7,39.5,0))), "== 6.42e23 kg?"
    print

#-------------------------------------------------------------------------------
# Testing circular & escape velocity calculation
#-------------------------------------------------------------------------------

def test_Vcirc():
    print "--------------------------------------------------"
    print "Testing circular & escape velocity calculation:"
    print
    print "Earth +300km: v(circ) = %5.0f  (7558) m/s" % v_circular(GM_Earth, 6678e3+300e3)
    print "Earth +300km: v(esc)  = %5.0f (10689) m/s" % v_escape(GM_Earth, 6678e3+300e3)
    print

    #o = Orbit_circular(GM_Sun, 150e9)
    #print o.period()/(365*24*60*60)
    #print o.v(100e9)

    #o = Orbit_from_circular(GM_Earth, 6378e3 + 300e3, -200)
    #print o.periapsis, "-", o.apoapsis

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

import solsystem

def test_MassDB():
    print "--------------------------------------------------"
    print "Testing mass database:"
    print
    Sun = masses["Sun"]
    Earth = masses["Earth"]
    print "Density:"
    print "   Earth.: %7.2f kg/m^3" % Earth.density()
    print "   Sun...: %7.2f kg/m^3" % Sun.density()
    print "Surface g:"
    print "   Earth.: %7.2f g" % (Earth.surface_g()/const_g)
    print "   Sun...: %7.2f g" % (Sun.surface_g()/const_g)
    print "Surface escape velocity:"
    print "   Earth.: %7.2f km/s" % (Earth.surface_v_esc()*1e-3)
    print "   Sun...: %7.2f km/s" % (Sun.surface_v_esc()*1e-3)
    print
    print "Earth:"
    print "   orbits= ", Earth.center.name
    print "   Laplace=", engfmt(Earth.dist_Laplace(),"m")
    print "   dist=   ", engfmt(Earth.orbit.a(), "m")
    print "   P(a)=   ", timefmt(Earth.orbit.P())
    print "   v   =   ", engfmt(Earth.orbit.v(Earth.orbit.a()),"m/s")
    print "LEO (300km):"
    LEO = masses["LEO"]
    print "   dist=", engfmt(LEO.orbit.a(), "m")
    print "   P(a)=", timefmt(LEO.orbit.P())
    print "   v   =", engfmt(LEO.orbit.v(LEO.orbit.a()),"m/s")
    print

#-------------------------------------------------------------------------------
# Testing mission setup
#-------------------------------------------------------------------------------

#from mission_mars import *

#print "Stage1:"
#print "   orbits=",   s1.orbit.center.name
#print "   altitude=", engfmt(s1.orbit.altitude(), "m")

