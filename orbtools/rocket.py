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
    def payload(self):  return self.mass / self.R
    
    @property
    def fuel(self):     return self.mass - self.payload

    #--------------------------------------------------------------------------
    # mass (tot), payload, mf (fuel mass), dv:
    # - Give two of them, and others None to solve the rest
    # - Engine u is always known
    #--------------------------------------------------------------------------

    def __init__(self, name, engine, mass = None, payload = None, fuel = None, dv = None, mission = None):
        self.name = name
        self.engine = engine
        self.mission = mission

        if mass == None:
            if payload != None and fuel != None: mass = fuel + payload

        if mass != None:
            if payload != None:
                self.dv = self.engine.dv(payload, mass -payload)
            elif fuel != None:
                self.dv = self.engine.dv(mass - fuel, fuel)
            else:
                if dv == None: dv = mission.dv
                self.dv = dv
            self.mass = float(mass)
            self.R = self.engine.R(self.dv)
        else:
            if dv == None: dv = mission.dv
            
            self.dv = dv
            self.R  = engine.R(dv)

            if payload != None:
                self.mass = self.R * float(payload)
            else:
                self.mass = fuel/(1 - 1.0/self.R)

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
                    stage.engine,
                    None,
                    stage.payload + totmass,
                    stage.fuel,
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
