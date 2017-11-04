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

    if M0 == None:      return M1 * Rv(dv, ve)
    elif M1 == None:    return M0 / Rv(dv, ve)
    elif dv == None:    return ve * Rm(M0, M1)
    else:               return dv / Rm(M0, M1)

def solve_Emv(E, m, v = None):
    if m == None: return E/(0.5*(v**2))
    if v == None: return sqrt(E/(0.5*m))
    return 0.5*m*(v**2)
    
def solve_Emc(E, m):
    if m == None: return E/(const_c**2)
    return m*(const_c**2)

###############################################################################
#
#
#
###############################################################################

class Engine(object):

    def __init__(self, name, u):
        self.name = name
        self.u    = float(u)

    def R(self, dv):        return exp(float(dv)/self.u)
    def dvR(self, R):       return self.u*log(R)
    def dv(self, m0, m1):   return self.dvR(m0/m1)

    def E(self, m = 1): return solve_Emv(None, m, self.u)

    def F(self, flux): return flux * self.u
    def flux(self, P): return solve_Emv(P, None, self.u)

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

    #--------------------------------------------------------------------------
    
    E  = energy[fuel]() * ratio
    dv = solve_Emv(E * efficiency, 1 - E2dm(E), None)

    return Engine(fuel, dv)

