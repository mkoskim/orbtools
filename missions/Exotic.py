#!/usr/bin/env python
import os, sys
sys.path.append(os.path.abspath(".."))

from sol import *

#------------------------------------------------------------------------------
#
# Mission to Mars: "idea": Use Oberth effect near sun to gain velocity
#
# 1) Start at Earth
# 2) From Earth, lower periapsis to sweep Sun at 30M km
# 3) At periapsis (Sun @ 30M km), burn to reach Mars orbit
# 4) Make Mars Orbit Insertion (MOI)
#
#------------------------------------------------------------------------------

LEO = Altitude(Earth, 300e3)
Sun30Gm = Orbit(Sun, Earth.orbit.a, 30e9)
Sun30Gm2Mars = Orbit(Sun, 30e9, Mars.orbit.a)

mission = Mission("Earth - Sun@30Gm - Mars", LEO)
mission.exit("LEO - Sun@30Gm", Sun30Gm)
mission.burn("Sun@30Gm - Mars", Sun30Gm2Mars)

print Sun30Gm.v(0.00).length
print Sun30Gm.v(0.50)
print Sun30Gm2Mars.v(0.0)

mission.show()

"""
o1 = Earth.orbit
o2 = Orbit(o1.center, o1.apoapsis, 30e9)
o3 = Orbit(o1.center, o2.periapsis, Mars.orbit.r())
o4 = Mars.orbit

deltav = [
    o2.v_initial - o1.v_initial,
    -o3.v_initial - o2.v_final,
    o4.v_initial - -o3.v_final
]

print "p1", o1.v_initial.length, "->", o2.v_initial.length, "=", deltav[0].length
print "p2", o2.v_final.length, "->", o3.v_initial.length, "=", deltav[1].length
print "p3", o3.v_final.length, "->", o4.v_initial.length, "=", deltav[2].length

print sum(map(lambda v: v.length, deltav))

#------------------------------------------------------------------------------

def retro(v): return -Vec2d(v.y, v.x)

print retro(o3.v_by_dist(Earth.orbit.r())), Earth.orbit.v(0), o2.v_initial
print (retro(o3.v_by_dist(Earth.orbit.r())) - o2.v_initial).length

#------------------------------------------------------------------------------

o5 = Orbit(o1.center, Earth.orbit.r(), Mars.orbit.r())

deltav2 = [
    o5.v_initial - o1.v_initial,
    o4.v_initial - -o5.v_final
]

print "p1", o1.v_initial.length, "->", o5.v_initial.length, "=", deltav2[0].length
print "p2", o5.v_final.length, "->", o4.v_initial.length, "=", deltav2[1].length

print sum(map(lambda v: v.length, deltav2))
"""

