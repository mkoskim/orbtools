###############################################################################
#
# Apollo-style Earth-Moon roundtrip mission
#
###############################################################################

import os, sys
sys.path.append(os.path.abspath(".."))

from sol import *

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
phase1.transfer("LEO Lift", LEO.orbit)
phase1.loss("Losses", 750)

#------------------------------------------------------------------------------
# Phase 2: Park to LEO + TLI (Trans Lunar Injection)
#------------------------------------------------------------------------------

phase2 = Mission("Trans-Lunar Injection", phase1.orbit)
phase2.lift("TLI", Moon.orbit)

#------------------------------------------------------------------------------
# Phase 3: Lunar Orbit Insertion
#------------------------------------------------------------------------------

phase3 = Mission("Lunar Orbit Insertion", phase2.orbit)
phase3.enter("LOI 100 km", LLO.orbit)

#------------------------------------------------------------------------------
# Phase 4.1: Lunar landing
#------------------------------------------------------------------------------

phase41 = Mission("Lunar Landing", phase3.orbit)
phase41.transfer("Descent", Surface(Moon))

#------------------------------------------------------------------------------
# Phase 4.2: Lunar takeoff
#------------------------------------------------------------------------------

phase42 = Mission("Lunar Takeoff", phase41.orbit)
phase42.transfer("Ascent", LLO.orbit)

#------------------------------------------------------------------------------
# Phase 5: TEI (Trans Earth Injection)
#------------------------------------------------------------------------------

phase5 = Mission("Trans-Earth Injection", phase42.orbit)
phase5.exit("TEI @LLO", Earth.radius)

#------------------------------------------------------------------------------
# Phase 6: Earth landing
#------------------------------------------------------------------------------

phase6 = Mission("Earth Landing", phase5.orbit)
phase6.park("Landing", Surface(Earth))

if __name__ == "__main__":
    phases = [phase1, phase2, phase3, phase41, phase42, phase5, phase6]
    for phase in phases: phase.show()

    print
    print "Total dv:", sum([phase.dv for phase in phases])
