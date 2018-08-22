###############################################################################
#
#
#
###############################################################################

from orbtools import *

#-------------------------------------------------------------------------------
# MLR, Mass-Luminosity Relation.
# Luminosity approxmation from star mass (as Sun mass)
# https://en.wikipedia.org/wiki/Mass%E2%80%93luminosity_relation
#-------------------------------------------------------------------------------

def _MLR(MxSun):
    if MxSun < 0.43:
        k, a = 0.23, 2.3
    elif MxSun < 2.00:
        k, a = 1.0, 4.0
    elif MxSun < 20.00:
        k, a = 1.4, 3.5
    else:
        k, a = 32e3, 1.0
    
    return k * (MxSun ** a)

#-------------------------------------------------------------------------------
# MRR, Mass-Radius Relation.
# Radius approxmation from star mass (as Sun mass)
# ???
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# Stars: 
#-------------------------------------------------------------------------------

class Star(Mass):

    def __init__(self, name, MxSun, RxSun = 0, rotate = 0, orbit = None, L = None):
        super(Star, self).__init__(
            name,
            GM     = MxSun * GM_Sun,
            radius = RxSun * r_Sun,
            rotate = rotate,
            orbit  = orbit
        )

        self.L = (L is None) and _MLR(MxSun) or L
        
    #--------------------------------------------------------------------------
    # Flux (in solar constant units) at given distance
    #--------------------------------------------------------------------------
    
    def flux(self, distance = AU2m(1.0)):
        return self.L / (m2AU(distance) ** 2)

    #--------------------------------------------------------------------------
    # Habitable Zone distance: in fact, distance at given flux.
    #--------------------------------------------------------------------------

    def HZ(self, flux = 1.0):
        return AU2m(sqrt(self.L) / flux)

