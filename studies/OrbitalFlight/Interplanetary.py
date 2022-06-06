#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
#
# Interplanetary flights
#
###############################################################################

import os, sys
sys.path.append(os.path.abspath("."))

from orbtools.systems.solsystem import *
from orbtools.systems.exoplanets import *

#------------------------------------------------------------------------------

# Earth-Mars w/o gravity

T1 = Transfer.Hohmann("Earth-Mars", Sun, Earth.a, Mars.a)
T1.info()
#T.initial.info()
#T.final.info()
#T.burns[1].orbit.info()

print("---")
T2 = Transfer("Earth-Mars", byAltitude(Earth, 300e3))
T2.exit(Mars.a)
T2.enter(byAltitude(Mars, 1000e3), 0.5)
T2.info()

print("---")
T3 = Transfer.Hohmann("Earth-Venus", Sun, Earth.a, Venus.a)
T3.info()

T4 = Transfer("Earth-Venus", byAltitude(Earth, 300e3))
T4.exit(Venus.a)
T4.enter(byAltitude(Venus, 1000e3), 0.5)
T4.info()

exit()

v_0 = T1.burns[0].orbit.v()
v_target = T1.burns[1].orbit.v()
print(v_target)
print("v(target): %.2f m/s" % abs(v_target))
print("v(target): %.2f m/s" % abs(v_target - v_0))

A = byAltitude(Earth, 300e3)
#A.info()
v_initial = A.v()
print("v(init): %.2f m/s" % abs(v_initial))

v_escape = solve_rvrv(A.center.GM, A.r(), None, Inf, abs(v_target - v_0))
#v_escape = solve_rvrv(A.center.GM, A.r(), None, Inf, 0)
print(v_escape, Earth.v_escape(Earth.radius + 300e3))
#print("v(escape): %.2f m/s" % v_escape)
v_burn = v_escape - abs(v_initial)
print("burn: %.2f m/s" % v_burn)

def plot():
    import plotter

    A = byAltitude(Earth, 3000e3, 10000e3)
    B = byAltitude(Earth, 10000e3, 3000e3)

    plotter.orbit(A)
    plotter.orbit(B)

    plotter.show()
