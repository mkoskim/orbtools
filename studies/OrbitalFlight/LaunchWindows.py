#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
#
# Some planetary systems. Lets try if we can help people making their own
# solar systems.
#
###############################################################################

import os, sys
sys.path.append(os.path.abspath("."))

from orbtools.systems.solsystem import *
from orbtools.systems.exoplanets import *

#------------------------------------------------------------------------------

def synodic(A, B): return abs((A*B) / float(A-B))

def P_synodic(A, B): return synodic(A.P, B.P)

#def P_synodic(A, B):
#  x = (1.0/A.P - 1.0/B.P)
#  x = (A.P - B.P) / (A.P * B.P)
#  #return 1.0 / (1.0/A.P - 1.0/B.P)
#  #return 1 / x
#  return (A.P * B.P) / (A.P - B.P)

#------------------------------------------------------------------------------

def P_launchwindow(A, B):
  A, B = Mass.resolve(A), Mass.resolve(B)

  print(
    "%s -> %s" % (A.name, B.name),
    "days: %.2f" % synodic(TtoDays(A.P), TtoDays(B.P)),
    "years: %.2f" % synodic(TtoYears(A.P), TtoYears(B.P)),
    "P: %.2f" % TtoDays(A.orbit.P_synodic(B.orbit))
  )

def calc(A, B):
  print("%.2f" % (A*B), "%.2f" % abs(A-B), "%.2f" % synodic(A, B))

calc(1.00, 1.88)  # Earth - Mars
calc(365, 687)    # Earth - Mars
calc(150, 450)    # Fictive planets
calc(7.15, 16.69) # Ganymede - Callisto

calc(90, 105)     # Earth 300 km - 1000 km
#print(TtoMinutes(byAltitude(Earth, 300e3).P))
#print(TtoMinutes(byAltitude(Earth, 1000e3).P))

print(630 / 60.0)

#print(synodic(1.00, 1.88))

print()
P_launchwindow("Earth", "Mars")
P_launchwindow("Earth", "Venus")
P_launchwindow("Earth", "Jupiter")
P_launchwindow("Ganymede", "Callisto")

exit()

#------------------------------------------------------------------------------

def sketching():
  A = Earth.orbit
  B = Mars.orbit

  print(TtoDays(A.P), TtoDays(B.P))

  AdegPerSec = 360.0 / A.P
  BdegPerSec = 360.0 / B.P

  print(AdegPerSec, BdegPerSec)

  wDiff = abs(AdegPerSec - BdegPerSec)
  #wDiff = abs(360.0/A.P - 360.0/B.P)
  print(wDiff)

  period = 360 / wDiff
  #period = 360.0 / abs(360.0/A.P - 360.0/B.P)

  print(TtoDays(period))
  print(TtoDays(P_synodic(A, B)))

