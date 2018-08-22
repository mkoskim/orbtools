###############################################################################
#
# Travelling in TRAPPIST-1 system
#
###############################################################################

import os, sys
sys.path.append(os.path.abspath(".."))

from orbtools.systems.solsystem import *
from orbtools.systems.exoplanets import *

#------------------------------------------------------------------------------

LO_d = Altitude(TRAPPIST1d, 300e3)
LO_e = Altitude(TRAPPIST1e, 300e3)

#------------------------------------------------------------------------------
# Reaching 300 km orbit at TRAPPIST-1d
#------------------------------------------------------------------------------

to_LO_d = Mission("TRAPPIST-1d lift", Surface(TRAPPIST1d))
to_LO_d.transfer("1", LO_d)
to_LO_d.show()
print "    P(orbit):", fmttime(to_LO_d.orbit.P)

#------------------------------------------------------------------------------
# Reaching 300 km orbit at TRAPPIST-1e
#------------------------------------------------------------------------------

to_LO_e = Mission("TRAPPIST-1e lift", Surface(TRAPPIST1e))
to_LO_e.transfer("1", LO_e)
to_LO_e.show()
print "    P(orbit):", fmttime(to_LO_e.orbit.P)

#------------------------------------------------------------------------------
# Transfer from d to e
#------------------------------------------------------------------------------

d_to_e = Mission("TRAPPIST-1: d -> e", LO_d)
d_to_e.exit("1", LO_e.center.orbit)
d_to_e.enter("2", LO_e)

d_to_e.show()

print fmttime(Trajectory(TRAPPIST1, TRAPPIST1d.orbit.a, TRAPPIST1e.orbit.a).P_window)

LEO  = Altitude(Earth, 300e3)
LMO  = Altitude(Mars,  300e3)

###############################################################################
#
# Reference calculations
#
###############################################################################

Ceres  = masses["Ceres"]
Pallas = masses["Pallas"]

CeresPallas = Mission("Reference: Ceres-Pallas", Ceres.orbit)
CeresPallas.transfer("1", Pallas.orbit)

CeresPallas.show()

print "Ceres, P.............: %.2f y" % TtoYears(Ceres.orbit.P)
print "Pallas, P............: %.2f y" % TtoYears(Pallas.orbit.P)
print "Ceres-Pallas, window.: %.2f y" % TtoYears(Trajectory(Sun, Ceres.orbit.a, Pallas.orbit.a).P_window)

#------------------------------------------------------------------------------
# Earth-LEO (300 km) transfer for reference
#------------------------------------------------------------------------------

to_LEO = Mission("LEO", Surface(Earth))
to_LEO.transfer("1", LEO)
to_LEO.show()
print "    P(orbit):", fmttime(to_LEO.orbit.P)

#------------------------------------------------------------------------------
# Earth-Mars transfer for reference
#------------------------------------------------------------------------------

EarthMars = Mission("Reference: Earth-Mars", LEO)
EarthMars.exit("1", LMO.center.orbit)
EarthMars.enter("2", LMO)
EarthMars.show()

print fmttime(Trajectory(Sun, Earth.orbit.a, Mars.orbit.a).P_window)

