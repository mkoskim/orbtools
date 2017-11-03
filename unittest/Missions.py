# -*- coding: utf-8 -*-
###############################################################################
#
# Orbtools unit tests: Testing Mission class
#
###############################################################################

import os, sys
sys.path.append(os.path.abspath(".."))

from sol import *

#-----------------------------------------------------------------------------
# Basic testing
#-----------------------------------------------------------------------------

def test_basics():
    leo300  = Altitude(Earth, 300e3)
    leo1000 = Altitude(Earth, 1000e3)

    mission = Mission("300km -> 1000km", leo300)
    mission.burn("1", Trajectory(Earth, leo300.r_initial, leo1000.r_final))
    mission.park("2", leo1000)

    mission.show()

#-----------------------------------------------------------------------------
# Testing system escape and enter calculations
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------
# We are orbiting Moon @ 1000 km. We want to burn to Mars transfer orbit.
# We are escaping from Moon to Earth orbit, and then from Earth to Sun orbit.
#-----------------------------------------------------------------------------

lmo1000km = Altitude(Moon, 1000e3)
print lmo1000km.v()
