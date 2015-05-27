################################################################################
#
# Orbital toolbox: Solving launch windows for Mars missions
#
################################################################################

import sys

from orbtools import *
from orbtools.systems.solsystem import *
from orbtools.spaceships import *

print>>sys.stderr, "Launch windows for Mars missions"

print "0 0"

for lower in [0.0, 0.1, 0.2, 0.3]:
#for lower in [0.0]:
    for higher in [0.00, 0.25, 0.50, 0.75, 1.00, 1.25, 1.50, 1.75, 2.00]:
    #for higher in [0.00]:
        initial   = Earth.orbit.periapsis()
        final     = Mars.orbit.apoapsis()
        periapsis = initial - AU2m(lower)
        apoapsis  = final + AU2m(higher)
        t = Trajectory(Sun, initial, final, periapsis, apoapsis)
        
        dv = abs(t.v_enter()) + abs(t.v_exit())
        
        # Initial angle
        print TtoDays(t.P_window()*(t.launch_angle_up()/360.0)), dv

print TtoDays(t.P_window()), 0

