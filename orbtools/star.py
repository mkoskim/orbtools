###############################################################################
#
# Stars
#
###############################################################################

from orbtools import *

#-------------------------------------------------------------------------------
# Stars: 
#-------------------------------------------------------------------------------

stars = {}

class Star(Mass):

    def __init__(self, name, MxSun, RxSun = 0, sptype = None, L = None, rotate = 0, orbit = None, dist = None):
        super(Star, self).__init__(
            name,
            GM     = MxSun * GM_Sun,
            radius = RxSun * r_Sun,
            rotate = rotate,
            orbit  = orbit
        )

        self.sptype = sptype
        self.L      = (L is None) and Star.MLR(MxSun) or L
        if dist is None:
            self.dist = None
        else:
            self.dist = ly2m(dist)
        
        stars[name] = self
        
    #--------------------------------------------------------------------------
    # Flux (in solar constant units) at given distance
    #--------------------------------------------------------------------------
    
    def flux(self, distance = AU2m(1.0)):
        return self.L / (m2AU(distance) ** 2)

    #--------------------------------------------------------------------------
    # Habitable Zone distance: in fact, distance at given flux.
    #--------------------------------------------------------------------------

    def orbitByFlux(self, flux = 1.0):
        return Orbit(self, AU2m(sqrt(self.L) / flux))

    def HZ(self, flux = 1.0):
        return AU2m(sqrt(self.L) / flux)
        
    #---------------------------------------------------------------------------
    # MLR, Mass-Luminosity Relation.
    # Luminosity approxmation from star mass (as Sun mass)
    # https://en.wikipedia.org/wiki/Mass%E2%80%93luminosity_relation
    #---------------------------------------------------------------------------

    @staticmethod
    def MLR(MxSun):
        if MxSun < 0.43:
            k, a = 0.23, 2.3
        elif MxSun < 2.00:
            k, a = 1.0, 4.0
        elif MxSun < 20.00:
            k, a = 1.4, 3.5
        else:
            k, a = 32e3, 1.0
        
        return k * (MxSun ** a)

    #---------------------------------------------------------------------------
    # MRR, Mass-Radius Relation.
    # Radius approxmation from star mass (as Sun mass)
    # ???
    #---------------------------------------------------------------------------



