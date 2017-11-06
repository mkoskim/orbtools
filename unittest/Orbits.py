# -*- coding: utf-8 -*-
###############################################################################
#
# Orbtools unit tests: Testing Orbit() class
#
###############################################################################

import os, sys
sys.path.append(os.path.abspath(".."))

from sol import *

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

#------------------------------------------------------------------------------
# This shows error in mass database, because orbit is only calculated
# by central mass (not including satellite mass). It is highest with
# Earth-Moon like systems, where satellite has considerable mass compared
# to central object.
#------------------------------------------------------------------------------

def test_moon():
    print "Given............:", fmttime(TasDays(27.321661))
    print "GM(Earth + Moon).:", fmttime(P_orbit(Earth.GM + Moon.GM, Moon.orbit.a))
    print "GM(Earth)........:", fmttime(P_orbit(Earth.GM, Moon.orbit.a))
    print "Database.........:", fmttime(Moon.orbit.P)
    print

test_moon()

#------------------------------------------------------------------------------
# Tähtitieteen perusteet (1984), example 7.3: Two 5 kg bricks are orbiting
# each other in empty space. Their distance is 1 m. What is the period of the
# orbit? Answer: 243000 s (2.8 d)
#------------------------------------------------------------------------------

def test_brick():
    bricks = Mass("Bricks", kg2GM(2 * 5))
    o = Orbit(bricks, 1.0)

    print "Bricks:"
    print "- Period (given)....:", 243000
    print "- Period (method 1).:", P_orbit(bricks.GM, 1.0)
    print "- Period (method 2).:", o.P
    print "- Velocity..........:", fmteng(abs(o.v()), "m/s")
    print

test_brick()

#------------------------------------------------------------------------------
# Create circular orbit around Earth
#------------------------------------------------------------------------------

def test_circular():
    #o = Orbit(Earth, Earth.radius + 300e3)
    o = Altitude(Earth, 300e3)

    print o.xy(0.00), o.v(0.00)
    print o.xy(0.25), o.v(0.25)
    print o.xy(0.50), o.v(0.50)
    print o.xy(0.75), o.v(0.75)
    print

    print o.v().rotate(90), o.v(0.25)
    print

#test_circular()

#------------------------------------------------------------------------------
# Test "Surface" orbits: These are pseudo-orbits used in missions
#------------------------------------------------------------------------------

def test_surface():
    o = Surface(Earth)

    print o.xy(0),    o.v(0)
    print o.xy(0.25), o.v(0.25)
    print fmttime(o.P)

#test_surface()

#------------------------------------------------------------------------------
# Testing orbit creations from different parameters
#------------------------------------------------------------------------------

def test_orbits():
    geo = Period(Earth, Earth.rotate)
    print fmttime(geo.P), geo.altitude() * 1e-3

#test_orbits()

#------------------------------------------------------------------------------
#
# Create pair of elliptical orbits around Earth: first one lifts
# 300 -> 1000 km, another drops from apogeum back to 300 km. Not that
# surprising, that these orbits should be equal: Their position at 1000 km
# should match.
#
#------------------------------------------------------------------------------

def test_transfers():

    low  = Altitude(Earth, 300e3)
    high = Altitude(Earth, 1000e3)
    
    o1 = Orbit(Earth, low.r(), high.r())
    o2 = Orbit(Earth, high.r(), low.r(), arg = 180, T0 = 0.5)

    print o1.xy(0.00).fr, o1.v(0.00)
    print o2.xy(0.00).fr, o2.v(0.00)
    print

    print o1.xy(0.50).fr, o1.v(0.50)
    print o2.xy(0.50).fr, o2.v(0.50)
    print

test_transfers()

#------------------------------------------------------------------------------
# Test elliptical trajectory velocity differences to given circular ones
#------------------------------------------------------------------------------

def test_vdiff():
    o1 = Orbit(Earth, Earth.radius + 500e3)
    o2 = Orbit(Earth, Earth.radius + 1000e3)
    o3 = Orbit(Earth, Earth.radius + 1500e3)

    ot = Orbit(Earth, o1.r(), o3.r())

    print ot.v(0),   o1.v(0)
    print ot.v(0.5), o3.v(0.5)

#test_vdiff()

    
