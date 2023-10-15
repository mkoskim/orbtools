###############################################################################
#
# Stars
#
###############################################################################

from orbtools import *

stars = {}
planets = {}

#-------------------------------------------------------------------------------
#
# Planet: Just a big object.
#
#-------------------------------------------------------------------------------

class Planet(Mass):
    def __init__(self, name, GM, radius = None, rotate = 0, orbit = None):

        self.type = "planet"

        super(Planet, self).__init__(
            name,
            GM     = float(GM),
            radius = radius and float(radius) or None,
            rotate = rotate,
            orbit  = orbit
        )

        if name: planets[name] = self

#-------------------------------------------------------------------------------
#
# Stars:
#
#   GM = mass
#   L  = Luminosity (Sun = 1.0)
#   T  = Surface temperature
#
#-------------------------------------------------------------------------------

class Star(Mass):

    def __init__(self, name, MxSun, RxSun = None, sptype = None, L = None, mag = None, T = None, rotate = 0, dist = None, orbit = None):

        self.type = "star"

        super(Star, self).__init__(
            name,
            GM     = MasSun(float(MxSun)),
            radius = RxSun and RasSun(float(RxSun)) or None,
            rotate = rotate,
            orbit  = orbit
        )

        self.L = L and float(L) or None
        self.T = T and float(T) or None

        self.mag = mag and float(mag) or None
        self.dist = dist and float(dist) or None
        self.sptype = sptype

        if name:
            stars[name] = self
        else:
            self.name = sptype

    #--------------------------------------------------------------------------
    # Stefan-Boltzmann law: the relation between radiation power (W) per
    # area unit and temperature.
    #
    #   L = Luminosity (x Sun), total amount of energy emitted per second
    #   T = Temperature (K)
    #   r = distance
    #   flux = W/m2 (x Earth)
    #
    #--------------------------------------------------------------------------

    @staticmethod
    def L2flux(L, r):
        r2 = m2AU(r) ** 2
        return L / r2
        #return L * L_Sun / A_sphere(r)

    @staticmethod
    def flux2L(flux, r):
        r2 = m2AU(r) ** 2
        return flux * r2
        #return flux * (A_sphere(r) / L_Sun)

    @staticmethod
    def LtoT(L, r):
        flux = Star.L2flux(L, r)
        return solve_fluxT(flux, None)
        #return solve_StefanBoltzmann(flux * const_solar, None)

    @staticmethod
    def TtoL(T, r):
        #flux = solve_StefanBoltzmann(None, T) / const_solar
        flux = solve_fluxT(None, T)
        return Star.flux2L(flux, r)

    @staticmethod
    def fluxToT(flux = 1.0):
        return solve_fluxT(flux, None)
        #return solve_StefanBoltzmann(flux * const_solar, None)

    @staticmethod
    def TtoFlux(T):
        return solve_fluxT(None, T)

    @staticmethod
    def fluxToTeff(flux = 1.0, albedo = 0.0):
        return Star.fluxToT(0.25 * (1 - albedo) * flux)

    #--------------------------------------------------------------------------
    # Effective temperature at given distance
    #--------------------------------------------------------------------------

    def T_eff(self, r, albedo = 0.0):
        return Star.LtoT(0.25 * (1-albedo) * self.L, r)

    #--------------------------------------------------------------------------
    # Radiation at given distance, relative to flux received by Earth:
    #--------------------------------------------------------------------------

    def fluxAt(self, distance = AU2m(1.0)):
        if not self.L: return None
        return Star.L2flux(self.L, distance)
        #return self.L / (m2AU(distance) ** 2)

    def fluxToR(self, flux = 1.0):
        return AU2m(sqrt(self.L / flux))

    def orbitByFlux(self, flux = 1.0):
        return Orbit(self, self.fluxToR(flux))

    def EarthEquivalence(self):
        return self.orbitByFlux(1.0)

    #-------------------------------------------------------------------------------
    # Visual magnitude to absolute
    #-------------------------------------------------------------------------------

    @staticmethod
    def magVtoAbs(mag, dist):
        return mag - 5*(log10(m2parsec(dist/10)))

    #-------------------------------------------------------------------------------
    # Absolute magnitude to luminosity (x Sun) conversion (Do not work)
    #-------------------------------------------------------------------------------

    @staticmethod
    def mag2L(mag):
        return 10 ** ((4.85 - mag) / 2.5)
        #return 10 ** (0.4*(4.85 - mag))

    #-------------------------------------------------------------------------------
    # Luminosity as log10(L_Sun)
    #-------------------------------------------------------------------------------

    @staticmethod
    def LasLog10(L):
        return 10 ** L

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
        S_max, S_min = Star.typical["F0"], Star.typical["M9"]

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

#------------------------------------------------------------------------------

Star.typical = {
    "F0": Star(None, sptype="F0", MxSun=1.61, RxSun=1.728, L=7.24, T=7220),
    "F1": Star(None, sptype="F1", MxSun=1.50, RxSun=1.679, L=6.17, T=7020),
    "F2": Star(None, sptype="F2", MxSun=1.46, RxSun=1.622, L=5.13, T=6820),
    "F3": Star(None, sptype="F3", MxSun=1.44, RxSun=1.578, L=4.68, T=6750),
    "F4": Star(None, sptype="F4", MxSun=1.38, RxSun=1.533, L=4.17, T=6670),
    "F5": Star(None, sptype="F5", MxSun=1.33, RxSun=1.473, L=3.63, T=6550),
    "F6": Star(None, sptype="F6", MxSun=1.25, RxSun=1.359, L=2.69, T=6350),
    "F7": Star(None, sptype="F7", MxSun=1.21, RxSun=1.324, L=2.45, T=6280),
    "F8": Star(None, sptype="F8", MxSun=1.18, RxSun=1.221, L=1.95, T=6180),
    "F9": Star(None, sptype="F9", MxSun=1.13, RxSun=1.167, L=1.66, T=6050),

    "G0": Star(None, sptype="G0", MxSun=1.06, RxSun=1.100, L=1.35, T=5930),
    "G1": Star(None, sptype="G1", MxSun=1.03, RxSun=1.060, L=1.20, T=5860),
    "G2": Star(None, sptype="G2", MxSun=1.00, RxSun=1.012, L=1.02, T=5770),
    "G3": Star(None, sptype="G3", MxSun=0.99, RxSun=1.002, L=0.98, T=5720),
    "G4": Star(None, sptype="G4", MxSun=0.985, RxSun=0.991, L=0.91, T=5680),
    "G5": Star(None, sptype="G5", MxSun=0.98, RxSun=0.977, L=0.89, T=5660),
    "G6": Star(None, sptype="G6", MxSun=0.97, RxSun=0.949, L=0.79, T=5600),
    "G7": Star(None, sptype="G7", MxSun=0.95, RxSun=0.927, L=0.74, T=5550),
    "G8": Star(None, sptype="G8", MxSun=0.94, RxSun=0.914, L=0.68, T=5480),
    "G9": Star(None, sptype="G9", MxSun=0.90, RxSun=0.853, L=0.55, T=5380),

    "K0": Star(None, sptype="K0", MxSun=0.88, RxSun=0.813, L=0.46, T=5270),
    "K1": Star(None, sptype="K1", MxSun=0.86, RxSun=0.797, L=0.41, T=5170),
    "K2": Star(None, sptype="K2", MxSun=0.82, RxSun=0.783, L=0.37, T=5100),
    "K3": Star(None, sptype="K3", MxSun=0.78, RxSun=0.755, L=0.28, T=4830),
    "K4": Star(None, sptype="K4", MxSun=0.73, RxSun=0.713, L=0.20, T=4600),
    "K5": Star(None, sptype="K5", MxSun=0.70, RxSun=0.701, L=0.17, T=4440),
    "K6": Star(None, sptype="K6", MxSun=0.69, RxSun=0.669, L=0.14, T=4300),
    "K7": Star(None, sptype="K7", MxSun=0.64, RxSun=0.630, L=0.10, T=4100),
    "K8": Star(None, sptype="K8", MxSun=0.62, RxSun=0.615, L=0.087, T=3990),
    "K9": Star(None, sptype="K9", MxSun=0.59, RxSun=0.608, L=0.079, T=3930),

    "M0": Star(None, sptype="M0", MxSun=0.57, RxSun=0.588, L=0.069, T=3850),
    "M1": Star(None, sptype="M1", MxSun=0.50, RxSun=0.501, L=0.041, T=3660),
    "M2": Star(None, sptype="M2", MxSun=0.44, RxSun=0.446, L=0.029, T=3560),
    "M3": Star(None, sptype="M3", MxSun=0.37, RxSun=0.361, L=0.016, T=3430),
    "M4": Star(None, sptype="M4", MxSun=0.23, RxSun=0.274, L=7.2e-3, T=3210),
    "M5": Star(None, sptype="M5", MxSun=0.162, RxSun=0.196, L=3.0e-3, T=3060),
    "M6": Star(None, sptype="M6", MxSun=0.102, RxSun=0.137, L=1.0e-3, T=2810),
    "M7": Star(None, sptype="M7", MxSun=0.090, RxSun=0.120, L=6.5e-4, T=2680),
    "M8": Star(None, sptype="M8", MxSun=0.085, RxSun=0.114, L=5.2e-4, T=2570),
    "M9": Star(None, sptype="M9", MxSun=0.079, RxSun=0.102, L=3.0e-4, T=2380),
}
