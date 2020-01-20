################################################################################
#
# Orbital toolbox: Payloads, delta-v and propellant calculations
#
# Equations:
#
# - dv           = ve * ln(mtot/payload)
# - dv / ve      =      ln(mtot/payload)
# - exp(dv / ve) =         mtot/payload
#
# - ve = dv / ln(mtot/payload)
#
# 2) mtot = payload + mfuel
#
# R = ratio of masses = Mtot / Mpayload
#
################################################################################

from orbtools import *

################################################################################
#
#
#
################################################################################

class Payload(object):

    def __init__(self, name, mass):
        self.name = name
        self.mass = float(mass)
        self.dv   = 0
        self.engine = None

    @property
    def payload(self): return self.mass
    
    @property
    def fuel(self):    return 0

    def show(self):
        print("Payload")
        print("   ", "Mass: %.2f kg" % self.mass)

################################################################################
#
#
#
################################################################################

class Stage(object):

    #--------------------------------------------------------------------------
    # mass = payload + fuel
    #
    # - payload = mass / R <=> mass = R * payload
    #
    # - payload = mass / R
    #   mass - fuel = mass / R
    #   - fuel = mass / R - mass
    #   fuel = mass - mass / R
    #   fuel = mass * (1 - 1/R)
    #   fuel/(1-1/R) = mass
    #   
    # R = (payload + fuel) / payload = mass / payload
    #
    #--------------------------------------------------------------------------

    @property
    def mass(self): return self.payload + self.fuel

    #--------------------------------------------------------------------------
    # mass (tot), payload, mf (fuel mass), dv:
    # - Give two of them, and others None to solve the rest
    # - Engine u is always known
    #--------------------------------------------------------------------------

    def __init__(self, name, mass = None, payload = None, fuel = None, engine = None, dv = None, mission = None):

        if mission != None: dv = mission.dv

        #----------------------------------------------------------------------
        # dv and ve given, compute masses
        #----------------------------------------------------------------------
        
        if dv != None and engine != None:
            R = engine.R(dv)
            print dv, engine.ve
            print R, log(R), dv / engine.ve
            if mass != None:
                payload = mass / R
                fuel = mass - payload
            elif payload != None:
                mass = R * payload
                fuel = mass - payload
            else:
                fuel = mass - payload

        #----------------------------------------------------------------------
        # dv or ve missing, compute masses, solve missing
        #----------------------------------------------------------------------

        else:
            if mass != None:
                if payload != None: fuel = mass - payload
                else: payload = mass - fuel
            else:
                mass = payload + fuel
            
            if dv == None:
                dv = engine.dv(payload, fuel)
            else:
                engine = Engine(solve_rocket_eq(mass, payload, dv, None))

        #----------------------------------------------------------------------
        # Fill info
        #----------------------------------------------------------------------

        self.name = name
        self.engine = engine
        self.mission = mission
        self.dv = dv
        self.payload = payload
        self.fuel = fuel
            
    def show(self):
        print(self.name)
        print("   ", "Mass.......: %.2f kg" % self.mass)    
        print("   ", "- Payload..: %.2f kg" % self.payload)
        print("   ", "- Fuel.....: %.2f kg" % self.fuel)
        print("   ", "Engine.....: %.2f m/s" % self.engine.ve)
        print("   ", "DV.........: %.2f m/s" % self.dv)
        if self.mission != None:
            phase = self.mission
            print("   ", "Mission DV.: %.2f m/s" % phase.dv)
            print("   ", "DV diff....: %.2f m/s" % (self.dv - phase.dv))
			
################################################################################

class Rocket(object):

    #---------------------------------------------------------------------------
    # Staged rocket: we create it from top to bottom, creating new objects
    # to include masses of upper stages.
    #---------------------------------------------------------------------------

    def __init__(self, name, *stages, **kw):
        self.name = name
        self.stages = []
        if "mission" in kw:
            self.mission = kw["mission"]
        else:
            self.mission = None
        
        totmass = 0
        for stage in stages:
            if stage.engine:
                solvedstage = Stage(
                    stage.name,
                    engine = stage.engine,
                    payload = stage.payload + totmass,
                    fuel    = stage.fuel,
                    mission = stage.mission
                )
            else:
                solvedstage = Payload(
                    stage.name,
                    stage.mass
                )
            self.stages.append(solvedstage)
            totmass = totmass + stage.mass
    
    @property
    def payload(self):
        return self.stages[0].payload

    @property
    def dv(self):
        return sum(map(lambda s: s.dv, self.stages))

    @property
    def mass(self):
        return self.stages[-1].mass

    @property
    def fuel(self):
        return sum(map(lambda s: s.fuel, self.stages))

    def show(self):
        print("Rocket:", self.name)
        print("- Payload........: %.2f kg"  % self.payload)
        print("- Tot. mass......: %.2f kg"  % self.mass)
        print("- Tot. propellant: %.2f kg"  % self.fuel)
        print("- Tot. DV........: %.2f m/s" % self.dv)
        if self.mission != None:
            phase = self.mission
            print("- Mission DV.....: %.2f m/s" % phase.dv)
            print("- DV diff........: %.2f m/s" % (self.dv - phase.dv))
        print("Stages:")
        for stage in self.stages:
            stage.show()
