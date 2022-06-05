################################################################################
#
# Multistage rockets
#
################################################################################

from orbtools import *

################################################################################
#
#
#
################################################################################

class Stage:

    #--------------------------------------------------------------------------
    # mass (tot), payload, mf (fuel mass), dv:
    # - Give two of them, and others None to solve the rest
    # - Engine u is always known
    #--------------------------------------------------------------------------

    def __init__(self, name, drymass, fuel = None, engine = None):
        self.name = name
        self.engine = engine
        self.drymass = float(drymass)
        self.fuel = float(fuel)

    @property
    def R(self): return 1 + self.fuel / self.drymass

    def m_final(self, payload = 0): return self.drymass + payload
    def m_initial(self, payload = 0): return self.m_final(payload) + self.fuel

    #--------------------------------------------------------------------------

    def dv(self, payload):
        if self.engine == None: return 0.0

        return solve_rocket_eq(
            self.m_initial(payload),
            self.m_final(payload),
            None,
            self.engine.ve
        )

    #--------------------------------------------------------------------------

    @property
    def t_burn(self): return self.engine.t(self.fuel)

    def a(self, payload, t):
        mf = self.fuel - self.engine.flow * t
        if mf < 0: return 0.0
        return solve_Fma(
            self.engine.F,
            self.m_final(payload) + mf,
            None
        )

    def a_initial(self, payload): return solve_Fma(self.engine.F, self.m_initial(payload), None)
    def a_final(self, payload): return solve_Fma(self.engine.F, self.m_final(payload), None)

    #--------------------------------------------------------------------------

    def info(self, payload = None):
        print("Stage:", self.name)
        print("   Mass.........: %.2f kg" % self.m_initial())
        print("   - Payload....: %.2f kg" % self.drymass)
        print("   - Fuel.......: %.2f kg" % self.fuel)
        print("   - R..........: %.2f" % self.R)

        if self.engine == None: return

        print("   Engine.......:", self.engine.name)
        print("   - Ve.........:", fmteng(self.engine.ve, "m/s"))
        print("   - Thrust.....:", fmteng(self.engine.F, "N"))
        print("   - Burn time..: %.2f s" % self.t_burn)

        if payload == None: return

        print("   DV...........:", fmteng(self.dv(payload), "m/s"))
        print("   Acceleration.:")
        print("   - Initial....: %.2f g" % (self.a_initial(payload) / const_g))
        print("   - Final......: %.2f g" % (self.a_final(payload) / const_g))

#------------------------------------------------------------------------------

def Payload(name, mass):
    return Stage(name, drymass = mass, fuel=0.0)

################################################################################

class Rocket:

    def __init__(self, name, *stages):
        self.name = name
        self.stages = stages

    def payload(self, stage):
        return sum(stage.m_initial() for stage in self.stages[stage+1:])

    def t_burn(self, stage): return self.stages[stage].t_burn

    def a(self, stage, t): return self.stages[stage].a(self.payload(stage), t)

    #def a_initial(self, stage):
    #    return solve_Fma(self.stage[stage].engine.F, payload(stage))

    #@property
    #def payload(self):
    #    return self.stages[0].payload

    #@property
    #def dv(self):
    #    return sum(map(lambda s: s.dv, self.stages))

    #@property
    #def mass(self):
    #   return self.stages[-1].mass

    @property
    def m_initial(self):
        return sum([stage.m_initial() for stage in self.stages])

    @property
    def fuel(self):
        return sum([stage.fuel for stage in self.stages])

    @property
    def drymass(self):
        return sum([stage.drymass for stage in self.stages])

    #@property
    #def R(self):
    #    return 1 + self.fuel/self.drymass

    @property
    def dv_tot(self):
        return sum([stage.dv(self.payload(i)) for i, stage in enumerate(self.stages)])

    #--------------------------------------------------------------------------

    def info(self):
        print("Rocket:", self.name)
        print("- Total mass....: %.2f kg" % self.m_initial)
        print("  - Dry mass....: %.2f kg" % self.drymass)
        print("  - Fuel........: %.2f kg" % self.fuel)
        print("  - R...........: %.2f" % (self.m_initial / self.drymass))
        print("- Tot. DV.......: %.2f m/s" % self.dv_tot)

        #print("- Payload........: %.2f kg"  % self.payload)
        print("Stages:")
        for i, stage in enumerate(self.stages):
            stage.info(self.payload(i))

#------------------------------------------------------------------------------
# Ready made rockets
#------------------------------------------------------------------------------
