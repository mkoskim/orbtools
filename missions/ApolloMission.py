###############################################################################
#
# Apollo-style Earth-Moon roundtrip mission
#
###############################################################################

import os, sys
sys.path.append(os.path.abspath("."))

from orbtools import *
from orbtools.systems.solsystem import *

#------------------------------------------------------------------------------
# Create shortcuts and LLO (Low Lunar Orbit) @ 110 km
#------------------------------------------------------------------------------

Moon = masses["Moon"]
LEO  = masses["LEO"]
LLO  = Mass("LLO", 0, 0, 0, Altitude("Moon", 110e3))

#------------------------------------------------------------------------------
# Phase 1: Launch towards LEO
#------------------------------------------------------------------------------

phase1 = Mission("Earth-LEO", Surface(Earth))
phase1.burn("Surface 2 LEO", Orbit(Earth, Earth.radius, LEO.orbit.a))
phase1.loss("Losses", 750)
phase1.show()

#------------------------------------------------------------------------------
# Phase 2: Park to LEO + TLI (Trans Lunar Injection)
#------------------------------------------------------------------------------

phase2 = Mission("Trans-Lunar Injection", phase1.orbit)
phase2.park("LEO park", LEO.orbit)
phase2.burn("TLI @LEO", Trajectory(Earth, phase2.orbit.a, Moon.orbit.a))
phase2.show()

#------------------------------------------------------------------------------
# Phase 3: Lunar Orbit Insertion
#------------------------------------------------------------------------------

phase3 = Mission("Lunar Orbit Insertion", phase2.orbit)
phase3.enter("LOI 100 km", Orbit(Moon, LLO.orbit.a))
phase3.show()

#------------------------------------------------------------------------------
# Phase 4.1: Lunar landing
#------------------------------------------------------------------------------

phase41 = Mission("Lunar Landing", phase3.orbit)
phase41.burn("Descent/1", Altitude(Moon, LLO.orbit.alt_initial, 0))
phase41.park("Descent/2", Surface(Moon))
phase41.show()

#------------------------------------------------------------------------------
# Phase 4.2: Lunar takeoff
#------------------------------------------------------------------------------

phase42 = Mission("Lunar Takeoff", phase41.orbit)
phase42.burn("Ascent/1", Altitude(Moon, 0, LLO.orbit.alt_initial))
phase42.park("Ascent/2", LLO.orbit)
phase42.show()

#------------------------------------------------------------------------------
# Phase 5: TEI (Trans Earth Injection)
#------------------------------------------------------------------------------

phase5 = Mission("Trans-Earth Injection", phase42.orbit)
phase5.exit("TEI @LLO", Earth.radius)
phase5.show()

#------------------------------------------------------------------------------
# Phase 6: Earth landing
#------------------------------------------------------------------------------

phase6 = Mission("Earth Landing", phase5.orbit)
phase6.park("Landing 1", Altitude(Earth,0))
phase6.park("Landing 2", Surface(Earth))
phase6.show()

