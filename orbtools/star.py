###############################################################################
#
# Stars
#
###############################################################################

from orbtools import *

#-------------------------------------------------------------------------------
#
# Stars:
# GM = mass
# L  = Luminosity relative to Sun
#
#-------------------------------------------------------------------------------

stars = {}

class Star(Mass):

    def __init__(self, name, MxSun, RxSun = 0, sptype = None, L = None, T = None, BV = None, rotate = 0, orbit = None, dist = None):

        self.sptype = sptype
        if not name: name = sptype

        super(Star, self).__init__(
            name,
            GM     = MasSun(MxSun),
            radius = RasSun(RxSun),
            rotate = rotate,
            orbit  = orbit
        )

        self.L      = (L is None) and Star.MLR(MxSun) or L
        self.T      = T
        self.BV     = BV

        if dist is None:
            self.dist = None
        else:
            self.dist = ly2m(dist)

        if name: stars[name] = self

    #--------------------------------------------------------------------------
    # Radiation at given distance, relative to flux received by Earth:
    #--------------------------------------------------------------------------

    def radiation(self, distance = AU2m(1.0)):
        return self.L / (m2AU(distance) ** 2)

    #--------------------------------------------------------------------------
    # Habitable Zone distance: in fact, distance at given flux.
    #--------------------------------------------------------------------------

    def HZ(self, flux = 1.0):
        return AU2m(sqrt(self.L / flux))

    def orbitByFlux(self, flux = 1.0):
        return Orbit(self, self.HZ(flux))

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
    # Create star with specific flux at certain orbital period
    #---------------------------------------------------------------------------

    @staticmethod
    def byFluxPeriod(P_target, flux = 1.0):
        S_max, S_min = Mass.resolve("F0"), Mass.resolve("M9")

        def P_max(): return S_max.orbitByFlux(flux).P
        def P_min(): return S_min.orbitByFlux(flux).P

        assert P_target > P_min(), "Period too small"
        assert P_target < P_max(), "Period too large"

        while P_max() - P_min() > TasDays(0.5):
            MxSun = 0.5 * (S_max.GM + S_min.GM) / GM_Sun
            star = Star(None, MxSun = MxSun, L = Star.MLR(MxSun))
            P = star.orbitByFlux().P
            #print(fmtGM(star.GM), "L=%.2f" % star.L, "P=", fmttime(P))

            if(P > P_target):
                S_max = star
            else:
                S_min = star

        return star

    #--------------------------------------------------------------------------
    # Lifetime approx
    #--------------------------------------------------------------------------

    @staticmethod
    def TMS(MxSun):
        return TasYears(1e10 * (MxSun ** -2.5))

    #---------------------------------------------------------------------------
    # MRR, Mass-Radius Relation.
    # Radius approxmation from star mass (as Sun mass)
    # ???
    #---------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#
# Black Body Radiation
#
#-------------------------------------------------------------------------------

def blackbody(T, wavelength):
    #a = 2 * const_h * (const_c ** 2) / (wavelength ** 5)
    a = 8 * pi * const_h * const_c / (wavelength ** 5)
    b = const_h * const_c / (wavelength * const_kb * T)

    return a / (exp(b) - 1)

