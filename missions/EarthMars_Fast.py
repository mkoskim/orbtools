###############################################################################
#
# Earth LEO - Mars: Fast trajectories.
#
###############################################################################

import os, sys
sys.path.append(os.path.abspath(".."))

from sol import *

#------------------------------------------------------------------------------

def trajectory(periapsis = None, apoapsis = None, arg = 0):
    return Trajectory(
        Sun,
        Earth.orbit.a,
        Mars.orbit.a,
        periapsis,
        apoapsis,
        arg = arg
    )
    
#------------------------------------------------------------------------------

t = trajectory(
    periapsis = Earth.orbit.a - AU2m(0.0),
    apoapsis  = Mars.orbit.a  + AU2m(0.0),
)

#------------------------------------------------------------------------------

print "Periapsis......:", m2AU(t.periapsis)
print "R (initial)....:", m2AU(t.r_initial)
print
print "Apoapsis.......:", m2AU(t.apoapsis)
print "R (final)......:", m2AU(t.r_final)
print

print "t (Hohmann)....: %s" % fmttime(t.hohmann_P)
print "t (transfer)...: %s (%s - %s)" % (fmttime(t.T_to_target * t.P), fmttime(t.T_initial * t.P), fmttime(t.T_final * t.P))

f_initial = t.fr(t.T_initial)[0]
E_initial = Earth.orbit.v().rotate(f_initial)

print "p_initial:", t.fr(t.T_initial)
print "f_initial:", f_initial

print "v_initial:", t.v_initial, t.v_initial.length
print "E_initial:", E_initial, E_initial.length
#print m2AU(Earth.orbit.a), Earth.orbit.v().length

print (t.v_initial - E_initial)
print (t.v_initial - E_initial).length
print t.hohmann_dv_enter

