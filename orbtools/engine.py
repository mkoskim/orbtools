###############################################################################
#
#
#
###############################################################################

from orbtools import *

#-------------------------------------------------------------------------------
# Solving rocket equation: give the unknown value as None for solving.
#-------------------------------------------------------------------------------

def solve_rocket_eq(M0, M1, dv, ve):

    def Rv(dv, ve): return exp(float(dv)/ve)
    def Rm(M0, M1): return log(float(M0)/M1)

    if M0 == None: return M1 * Rv(dv, ve)
    if M1 == None: return M0 / Rv(dv, ve)
    if dv == None: return ve * Rm(M0, M1)
    return dv / Rm(M0, M1)

def solve_Emv(E, m, v = None):
    if m == None: return E/(0.5*(v**2))
    if v == None: return sqrt(E/(0.5*m))
    return 0.5*m*(v**2)
    
def solve_Emc(E, m):
    if m == None: return E/(const_c**2)
    return m*(const_c**2)

def solve_Fma(F, m, a):
    if F == None: return m * a
    if m == None: return float(F) / a
    return float(F) / m

###############################################################################
#
# Fixed-Isp reaction engines
#
###############################################################################

class Exhaust(object):

    def __init__(self, ve): self.ve = float(ve)

    def solve(self, M0, M1, dv): return solve_rocket_eq(M0, M1, dv, self.ve)

    def dv(self, payload, fuel): return self.solve(payload + fuel, payload, None)
    def fuel(self, payload, dv): return self.solve(None, payload, dv) - payload

    def P(self, F = 1): return F * (0.5 * self.ve)
    def F(self, P):     return P / (0.5 * self.ve)      # = flux * ve
    def E(self, m = 1): return solve_Emv(None, m, self.ve)
    def flux(self, P):  return solve_Emv(P, None, self.ve)
    def E_eff(self, dv):return solve_Emv(None, 1, dv) / self.E(self.fuel(1, dv))
    
    def t(self, P, m):  return self.E(m) / P

class Engine(object):

    def __init__(self, ve, P = None, F = None):
        self.exhaust = Exhaust(ve)
        self.P = P and P or self.exhaust.P(F)

    @property
    def ve(self): return self.exhaust.ve

    @property
    def flux(self): return self.exhaust.flux(self.P)
    
    @property
    def F(self):    return self.exhaust.F(self.P)

    def solve(self, M0, M1, dv): return self.exhaust.solve(M0, M1, dv)
    def dv(self, payload, fuel): return self.exhaust.dv(payload, fuel)
    def fuel(self, payload, dv): return self.exhaust.fuel(payload, dv)
    
    def E(self, m = 1):     return self.exhaust.E(m)
    def E_eff(self, dv):    return self.exhaust.E_eff(dv)
    
    def t(self, m): return self.exhaust.t(self.P, m)    



#------------------------------------------------------------------------------
# Engine database: parameters are vacuum parameters
#------------------------------------------------------------------------------

def Engine_veP(ve, P):      return Engine(ve, P = P)
def Engine_IspP(isp, P):    return Engine(Isp2ve(isp), P = P)
def Engine_veF(ve, F):      return Engine(ve, F = F)
def Engine_IspF(isp, F):    return Engine(Isp2ve(isp), F = F)

engines = {
    "F-1":          Engine_IspF(304.0,  7770000),   # Saturn first stage
    "J-2":          Engine_IspF(421.0,  1033000),   # Saturn upper stage

    "RS-25":        Engine_IspF(452.3,  2279000),   # Shuttle main engine
    "SSSRB":        Engine_IspF(268.0, 14000000),   # Shuttle solid rocket booster (PBAN/APCP)
    
    "Merlin 1C":    Engine_IspF(336.0,  413644),    # SpaceX Falcon 1, 9 (vac)
    "Merlin 1D":    Engine_IspF(348.0,  934000),    # SpaceX Falcon 9 v1.1 (vac)
    "Raptor":       Engine_IspF(382.0, 3500000),    # SpaceX Raptor (vac)

    "RD-180":       Engine_IspF(338.4, 4152136),    # RP-1 engine
    "RD-263":       Engine_IspF(318.0, 1130000),    # N2O2/UDMH engine
        
    "P230":         Engine_IspF(286.0, 6472300),    # Ariane 5 HTPB booster

    "HiPEP":        Engine_IspF(9620.0, 0.670),     # Ion thruster: 39.3 kW
    "NSTAR":        Engine_IspF(3100.0, 0.092),     # Ion thruster:  2.3 kW
    "VASIMR":       Engine_IspF(5000.0, 5.700),     # VASIMR: 200 kW
}

engines["SSME"]  = engines["RS-25"]
engines["RS-24"] = engines["RS-25"]

###############################################################################
#
# Tools for making experimental engines
#
###############################################################################

#------------------------------------------------------------------------------
#
# Nuclear rockets: These rockets burn part of their fuel mass to energy,
# which is then used to accelerate the rest of the mass. NOTE: These
# calculations assume that the reaction mass is exhausted.
#
#------------------------------------------------------------------------------

def Fuel(fuel, ratio = 1.0, efficiency = 1.0):

    def E2dm(energy):       return solve_Emc(energy, None)
    def dm2E(mass_loss):    return solve_Emc(None, mass_loss)
    
    #--------------------------------------------------------------------------
    
    def Burn(energy, fuel, oxidizer):
        atomic_mass = {
            "H":  1.008,
            "C": 12.011,
            "N": 14.007,
            "O": 15.999,
        }
        m_fuel     = sum([atomic_mass[x] for x in fuel])
        m_oxidizer = sum([atomic_mass[x] for x in oxidizer])
        m_tot = m_fuel + m_oxidizer

        return energy * m_fuel / m_tot
    
    def CH(energy, C, H, O = 0, N = 0):
        return Burn(
            energy,
            C*["C"] + H*["H"] + O*["O"] + N*["N"],
            (2*C + H/2 - O)*["O"]
        )
    
    #--------------------------------------------------------------------------
    
    energy = {
        "!H":       lambda: dm2E(1.0000000),
        "D-He3":    lambda: dm2E(0.0040423),
        "D-T":      lambda: dm2E(0.0037681),
        
        "D-D":      lambda: 87900000.00e6,
        "U235":     lambda: 80620000.00e6,
        "Th232":    lambda: 79420000.00e6,
        "Pu239":    lambda:    83610.00e6,
        
        "LH2":      lambda: CH(  141.86e6,  0,  2),

        "Methane":  lambda: CH(   55.6e6,  1,  4),
        "Ethane":   lambda: CH(   51.8e6,  2,  6),
        "Propane":  lambda: CH(   50.3e6,  3,  8),
        "Butane":   lambda: CH(   49.5e6,  4, 10),
        "Kerosene": lambda: CH(   46.2e6, 12, 26),

        "Methanol": lambda: CH(   22.7e6,  1,  4,  1),
        "Ethanol" : lambda: CH(   29.7e6,  2,  6,  1),
        "Propanol": lambda: CH(   33.6e6,  3,  8,  1),

        "TNT":      lambda:        4.6e6,
        "Gunpowder":lambda:        3.0e6,
        "Hydrazine":lambda:        1.6e6,
    }

    return energy[fuel]()

    #--------------------------------------------------------------------------
    
    E  = energy[fuel]() * ratio
    dv = solve_Emv(E * efficiency, 1 - E2dm(E), None)
    
    return Engine(fuel, dv)

