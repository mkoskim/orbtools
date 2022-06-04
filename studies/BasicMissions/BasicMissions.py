#!/usr/bin/env python3
###############################################################################
#
# Some basic missions
#
###############################################################################

import os, sys
sys.path.append(os.path.abspath("."))

from orbtools.systems.solsystem import *
from orbtools.systems.exoplanets import *

#------------------------------------------------------------------------------
# Create orbit shorcuts
#------------------------------------------------------------------------------

LEO = byAltitude(Earth, 300e3)
LMO = byAltitude(Mars,  300e3)
LJO = byAltitude(Jupiter, 1_070_412e3)

#------------------------------------------------------------------------------

EarthLEO = Mission("Earth-LEO", Surface(Earth))
EarthLEO.transfer("Earth-LEO", LEO)

EarthLEO.show()

#------------------------------------------------------------------------------

EarthMars = Mission("Earth-Mars", Surface(Earth))
EarthMars.exit("TMI", LMO.center.orbit)
EarthMars.enter("MOI", LMO)

EarthMars.show()

#------------------------------------------------------------------------------

LEOMars = Mission("LEO-Mars", LEO)
LEOMars.exit("TMI", LMO.center.orbit)
LEOMars.enter("MOI", LMO)

LEOMars.show()

#------------------------------------------------------------------------------

EarthJupiter = Mission("Earth-Jupiter", Surface(Earth))
EarthJupiter.exit("TJI", LJO.center.orbit)
EarthJupiter.enter("JOI", LJO)

EarthJupiter.show()

#------------------------------------------------------------------------------

LEOJupiter = Mission("LEO-Jupiter", LEO)
LEOJupiter.exit("TJI", LJO.center.orbit)
LEOJupiter.enter("JOI", LJO)

LEOJupiter.show()

#------------------------------------------------------------------------------
# LEO - Interstellar space

v_SunEscape = Sun.v_escape(Earth.orbit.a)
v_inf = v_SunEscape - Earth.orbit.v().length
dv_Interstellar = solve_rvrv(
  LEO.center.GM,
  LEO.a, None,
  Inf, v_inf
)


#class Interstellar:
#
#  def __init__(self, from):
#    Sun = from.center

print(fmteng(v_SunEscape, "m/s"))
print(fmteng(v_inf, "m/s"))
#print(Interstellar.dv)

#------------------------------------------------------------------------------

def propellant(dv, ve):
  return solve_rocket_eq(None, 1, dv, ve) - 1

missions = [EarthLEO, LEOMars, LEOJupiter, EarthMars, EarthJupiter]
engines = [4000, 8000, 15000]

for mission in missions:
  for ve in engines:
    print("%-15s ve=%.0f p=%.1f" % (mission.name, ve, propellant(mission.dv, ve)))
  print()

print("Interstellar dv=%.0f" % (dv_Interstellar))
for ve in engines:
  print("%-15s ve=%.0f p=%.1f" % ("LEO-Interstellar", ve, propellant(dv_Interstellar, ve)))

#------------------------------------------------------------------------------

#EarthJupiter = Orbit(Sun, Earth.orbit.a, Jupiter.orbit.a)
#print(fmttime(EarthJupiter.P/2.0))
#print(TtoDays(Jupiter.orbit.P), TtoDays(Earth.orbit.P))
#print(fmttime((Jupiter.orbit.P + Earth.orbit.P) / 4))

