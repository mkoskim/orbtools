###############################################################################
###############################################################################
#
# Building missions
#
###############################################################################
###############################################################################

from orbtools import *

###############################################################################
#
# Burn: transfer from one orbit to another.
#
###############################################################################

class Burn(object):
    def __init__(self, name, orbFrom, orbTo, initial = True):

        if orbFrom.center != orbTo.center:
            raise Exception("Orbits have different central masses!")
        if abs(orbFrom.r_final - orbTo.r_initial) > 0.05*orbTo.r_initial:
            raise Exception("Orbit does not reach target")

        if initial:
            self.dv = abs(orbTo.v_initial - orbFrom.v_initial)
        else:
            self.dv = abs(orbTo.v_final - orbFrom.v_final)
        
        self.dt = orbTo.T_to_target * orbTo.P
        self.name = name
        self.orbit = orbTo

#------------------------------------------------------------------------------
# Loss (friction, gravity) estimations
#------------------------------------------------------------------------------

class Loss(object):
    def __init__(self, name, orbit, loss):
        self.name = name
        self.orbit = orbit
        self.dv = loss
        self.dt = 0

#------------------------------------------------------------------------------
# Entering system to given orbit
#------------------------------------------------------------------------------

class EnterSystem(object):

    def __init__(self, name, orbFrom, orbTo):

        if orbTo.center.orbit.center != orbFrom.center:
            raise Exception("Target center != orbit center")

        if abs(orbFrom.r_final - orbTo.center.orbit.a) > orbTo.center.SOI():
            raise Exception("Orbit does not reach system")

        v_inf   = orbFrom.dv_circular(orbFrom.r_final).length
        v_enter = solve_rvrv(
            orbTo.center.GM,
            Inf, v_inf,
            orbTo.r_initial, None
        )
            
        self.dv = abs(v_enter - abs(orbTo.v(0)))
        self.dt = 0
        self.name = name
        self.orbit = orbTo
	
#------------------------------------------------------------------------------
# Escape from system to orbit its central mass
#------------------------------------------------------------------------------

class ExitSystem(object):
    def __init__(self, name, orbit, target_r, r1 = None, r2 = None):
        oldcenter = orbit.center
        newcenter = orbit.center.orbit.center

        exit_orbit = Trajectory(
                newcenter,
                oldcenter.orbit.a,
                target_r,
                r1, r2
        )
        v_inf  = abs(exit_orbit.v_initial - oldcenter.orbit.v_initial)
        v_exit = solve_rvrv(
            oldcenter.GM,
            oldcenter.orbit.r_initial, None,
            Inf, v_inf
        )

        self.dv = abs(v_exit - abs(orbit.v_initial))
        self.dt = exit_orbit.T_to_target * exit_orbit.P
        self.name = name
        self.orbit = exit_orbit

#------------------------------------------------------------------------------
# "Virtual" burn for mission initial orbit
#------------------------------------------------------------------------------

class Initial(object):
    def __init__(self, orbit):
        self.name = "Start"
        self.dv = 0
        self.dt = 0
        self.orbit = orbit

###############################################################################
#
# Mission: A sequence of burns
#
###############################################################################

class Mission(object):
    
    def __init__(self, name, initial_orbit):
        self.name = name
        self.burns = [ Initial(initial_orbit) ]

    def burn(self, name, to_orbit):
        if isinstance(to_orbit, float):
            to_orbit = Trajectory(self.orbit.center, self.orbit.r_initial, to_orbit)
        self.burns.append(Burn(name, self.orbit, to_orbit))

    def park(self, name, to_orbit):
        self.burns.append(Burn(name, self.orbit, to_orbit, False))

    def lift(self, name, to_orbit):
        self.burn(name, to_orbit.a)
    
    def transfer(self, name, to_orbit):
        self.lift(name + "/1", to_orbit)
        self.park(name + "/2", to_orbit)

    def loss(self, name, dv):
        self.burns.append(Loss(name, self.orbit, dv))

    def enter(self, name, orbit):
        self.burns.append(EnterSystem(name, self.orbit, orbit))

    def exit(self, name, orbit):
        if isinstance(orbit, float):
            r_final = orbit
        else:
            r_final = orbit.r_final
        self.burns.append(ExitSystem(name, self.orbit, r_final))

    @property
    def orbit(self): return self.burns[-1].orbit
    
    @property
    def dt(self): return sum(map(lambda b: b.dt, self.burns))
                    
    @property
    def dv(self): return sum(map(lambda b: b.dv, self.burns[1:]))

    def show(self):
            print "Mission:", self.name
            for burn in self.burns[1:]:
                    print "    Burn: %-15s dv=%8.2f dt=%10s" % (burn.name, burn.dv, fmttime(burn.dt))
            print "    ---"
            print "    Tot.: %15s dv=%8.2f dt=%10s" % ("", self.dv, fmttime(self.dt))


