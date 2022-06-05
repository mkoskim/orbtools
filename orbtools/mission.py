###############################################################################
###############################################################################
#
# Building missions
#
###############################################################################
###############################################################################

from orbtools import *

#------------------------------------------------------------------------------
# Lets rethink this. We do burns that result to new orbits.
#------------------------------------------------------------------------------

#def Hohmann(A, B):
#    assert A.center == B.center, "Orbits need to have same center."
#    return Orbit(A.center, A.r(0), B.r(0.5))

class Transfer:

    def __init__(self, name, orbit):
        self.name = name
        self.burns = [ Transfer.Burn(orbit)]

    #--------------------------------------------------------------------------
    # Properties
    #--------------------------------------------------------------------------

    @property
    def latest(self): return self.burns[-1]

    @property
    def orbit(self): return self.latest.orbit

    @property
    def dv(self):
        return sum([abs(burn.dv) for burn in self.burns])

    @property
    def t(self):
        return sum([burn.t for burn in self.burns])

    @property
    def initial(self):
        return self.burns[0].orbit

    @property
    def final(self):
        return self.latest.orbit

    #--------------------------------------------------------------------------
    # Transfer operations
    #--------------------------------------------------------------------------

    def liftTo(self, dist, t = 0):
        A = self.orbit
        f, r = A.fr(t)
        orbit = Orbit(A.center, r, dist, arg = f)
        dv = orbit.v(0) - A.v(t)
        self.latest.stay = t
        self.burns.append(Transfer.Burn(orbit, dv))
        return orbit, dv

    def lift(self, height, t = 0):
        A = self.orbit
        return self.liftTo(A.r(t) + height, t)

    def circulate(self, t = 0):
        A = self.orbit
        return self.liftTo(A.r(t), t)

    #--------------------------------------------------------------------------

    class Burn:
        def __init__(self, orbit, dv = Vec2d()):
            self.orbit = orbit
            self.dv = dv
            self.stay = 0.0

        @property
        def t(self): return self.stay * self.orbit.P

    #--------------------------------------------------------------------------

    @staticmethod
    def TakeOff(name, mass, altitude):
        T = Transfer(name, Surface(mass))
        T.lift(altitude)
        T.circulate(t=0.5)
        return T

    #--------------------------------------------------------------------------

    def info(self):
        print("Transfer..:", self.name)
        print("- DV......:", fmteng(self.dv, "m/s"))
        print("- Time....:", fmttime(self.t))

        print("- Burns:")
        for burn in self.burns:
            print("  - DV:", abs(burn.dv))

#def Burn(orbFrom, orbTo):

#    assert orbFrom.center == orbTo.center, "Orbits have different central masses"

    #if initial:
    #    self.dv = abs(orbTo.v_initial - orbFrom.v_initial)
    #else:
    #    self.dv = abs(orbTo.v_final - orbFrom.v_final)

    #self.dt = orbTo.T_to_target * orbTo.P
    #self.name = name
    #self.orbit = orbTo

#------------------------------------------------------------------------------
# Loss (friction, gravity) estimations
#------------------------------------------------------------------------------

class Loss:
    def __init__(self, name, orbit, loss):
        self.name = name
        self.orbit = orbit
        self.dv = loss
        self.dt = 0

#------------------------------------------------------------------------------
# Entering system to given orbit
#------------------------------------------------------------------------------

class EnterSystem:

    def __init__(self, name, orbFrom, orbTo):

        if orbTo.center.orbit.center != orbFrom.center:
            raise Exception("Target center != orbit center")

        if abs(orbFrom.r_final - orbTo.center.orbit.a) > orbTo.center.SOI():
            raise Exception("Orbit does not reach system")

        v_inf   = abs(abs(orbFrom.v_final) - abs(orbTo.center.orbit.v()))
        v_enter = solve_rvrv(
            orbTo.center.GM,
            Inf, v_inf,
            orbTo.r_initial, None
        )
        #print "Enter: v_fin: %s, v_body.: %s" % (fmteng(v_final, "m/s"), fmteng(v_body, "m/s"))
        #print "Enter: v_inf: %s, v_enter: %s" % (fmteng(v_inf, "m/s"), fmteng(v_enter, "m/s"))

        self.dv = abs(v_enter - abs(orbTo.v(0)))
        self.dt = 0
        self.name = name
        self.orbit = orbTo

#------------------------------------------------------------------------------
# Escape from system to orbit its central mass
#------------------------------------------------------------------------------

class ExitSystem:
    def __init__(self, name, orbit, target_r, r1 = None, r2 = None):
        oldcenter = orbit.center
        newcenter = orbit.center.orbit.center

        exit_orbit = Trajectory(
            newcenter,
            oldcenter.orbit.a,
            target_r,
            r1, r2
        )
        v_inf  = abs(exit_orbit.v_initial.length - oldcenter.orbit.v_initial.length)
        v_exit = solve_rvrv(
            oldcenter.GM,
            orbit.r_initial, None,
            Inf, v_inf
        )

        #print "Exit: v_inf: %s, v_exit: %s" % (fmteng(v_inf, "m/s"), fmteng(v_exit, "m/s"))

        self.dv = abs(abs(v_exit) - abs(orbit.v_initial))
        self.dt = exit_orbit.T_to_target * exit_orbit.P
        self.name = name
        self.orbit = exit_orbit

#------------------------------------------------------------------------------
# "Virtual" burn for mission initial orbit
#------------------------------------------------------------------------------

class Initial:
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

class MissionX:

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
            print("Mission:", self.name)
            for burn in self.burns[1:]:
                    print("    Burn: %-15s dv=%8.2f dt=%10s" % (burn.name, burn.dv, fmttime(burn.dt)))
            print("    ---")
            print("    Tot.: %15s dv=%8.2f dt=%10s" % ("", self.dv, fmttime(self.dt)))


