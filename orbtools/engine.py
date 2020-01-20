###############################################################################
#
# Engine equations
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

#-------------------------------------------------------------------------------
# Energy equations
#-------------------------------------------------------------------------------

def solve_Emv(E, m, v = None):
    if m == None: return E/(0.5*(v**2))
    if v == None: return sqrt(2 * E/m)
    return 0.5*m*(v**2)
    
def solve_Emc(E, m):
    if m == None: return E/(const_c**2)
    return m*(const_c**2)

#-------------------------------------------------------------------------------
# Power and Force equations
#-------------------------------------------------------------------------------

def solve_Fma(F, m, a):
    if F == None: return m * a
    if m == None: return float(F) / a
    return float(F) / m

def solve_PFve(P, F, ve):
    if P == None: return F * (0.5 * ve)
    if F == None: return P / (0.5 * ve) # = flow * ve
    return 2.0 * P/F
    
#-------------------------------------------------------------------------------
# Temperature equations:
# T = temperature (Kelvin)
# M = Molar mass (g/mol)
# v = speed
#-------------------------------------------------------------------------------

def solve_MTv(M, T, v = None):
    if isinstance(M, str): M = Fuel.atomic_mass(M)
    if T == None: return (M*1e-3 * v**2 / (3*const_R))
    if M == None: return (2.5*const_R*T / (v**2)) * 1e3
    return 1.6 * sqrt(T * const_R/M*1e3)

def de_laval(M, T, p, r_exp, gamma):
    if isinstance(M, str): M = Fuel.atomic_mass(M)

    p_ex = p / r_exp
    f = gamma / (gamma - 1)
    
    return sqrt(
        T * (const_R/M*1e3)*
        2*f *
        (1 - (p_ex / p) ** (1 / f))
    )

###############################################################################
#
# Fixed-Isp rocket engines
#
###############################################################################

class Exhaust(object):

    def __init__(self, ve): self.ve = float(ve)

    def solve(self, M0, M1, dv): return solve_rocket_eq(M0, M1, dv, self.ve)

    def R(self, dv): return self.solve(None, 1, dv)

    def dv(self, payload, fuel): return self.solve(payload + fuel, payload, None)
    def M0(self, payload, dv):   return payload * self.R(dv)
    def fuel(self, payload, dv): return payload * (self.R(dv) - 1)

    def P(self, F = 1): return solve_PFve(None, F, self.ve)
    def F(self, P):     return solve_PFve(P, None, self.ve)
    def E(self, m = 1): return solve_Emv(None, m, self.ve)
    def flow(self, P):  return solve_Emv(P, None, self.ve)
    def E_eff(self, dv):return solve_Emv(None, 1, dv) / self.E(self.fuel(1, dv))
    
    def t(self, P, m):  return self.E(m) / P

#------------------------------------------------------------------------------

engines = { }

class Engine(object):

    def __init__(self, ve, P = None, F = None, name = None, propellant = None):
        self.exhaust = Exhaust(ve)
        self.P = P and P or self.exhaust.P(F)
        self.name = name
        self.propellant = propellant
        if name: engines[name] = self

    @property
    def ve(self): return self.exhaust.ve

    @property
    def flow(self): return self.exhaust.flow(self.P)
    
    @property
    def F(self):    return self.exhaust.F(self.P)

    def solve(self, M0, M1, dv): return self.exhaust.solve(M0, M1, dv)
    def dv(self, payload, fuel): return self.exhaust.dv(payload, fuel)
    def fuel(self, payload, dv): return self.exhaust.fuel(payload, dv)
    
    def E(self, m = 1):     return self.exhaust.E(m)
    def E_eff(self, dv):    return self.exhaust.E_eff(dv)
    
    def t(self, m): return self.exhaust.t(self.P, m)    

    def R(self, dv): return self.exhaust.R(dv)

#------------------------------------------------------------------------------
# Engine database: parameters are vacuum parameters
#------------------------------------------------------------------------------

def Engine_veP(name, ve, P):      return Engine(ve, P = P, name = name)
def Engine_IspP(name, isp, P):    return Engine(Isp2ve(isp), P = P, name = name)
def Engine_veF(name, ve, F):      return Engine(ve, F = F, name = name)
def Engine_IspF(name, isp, F):    return Engine(Isp2ve(isp), F = F, name = name)

Engine_IspF("F-1",          304.0,  7770000)    # Saturn first stage
Engine_IspF("J-2",          421.0,  1033000)    # Saturn upper stage

Engine_IspF("RS-25",        452.3,  2279000)    # Shuttle main engine
Engine_IspF("SSSRB",        268.0, 14000000)    # Shuttle solid rocket booster (PBAN/APCP)

Engine_IspF("Merlin 1C",    336.0,  413644)     # SpaceX Falcon 1, 9 (vac)
Engine_IspF("Merlin 1D",    348.0,  934000)     # SpaceX Falcon 9 v1.1 (vac)
Engine_IspF("Raptor",       382.0, 3500000)     # SpaceX Raptor (vac)

Engine_IspF("RD-180",       338.4, 4152136)     # RP-1 engine
Engine_IspF("RD-191",       337.0, 2090000)     # RP-1 engine
Engine_IspF("RD-263",       318.0, 1130000)     # N2O2/UDMH engine
        
Engine_IspF("P230",         286.0, 6472300)     # Ariane 5 HTPB booster

Engine_IspF("HiPEP",       9620.0, 0.670)       # Ion thruster: 39.3 kW
Engine_IspF("NSTAR",       3100.0, 0.092)       # Ion thruster:  2.3 kW
Engine_IspF("VASIMR",      5000.0, 5.700)       # VASIMR: 200 kW

Engine_IspF("NERVA",        850.0, 333600)      # NERVA nuclear thermal engine

#------------------------------------------------------------------------------
# A.K.A.
#------------------------------------------------------------------------------

engines["SSME"]  = engines["RS-25"]

###############################################################################
#
# Tools for making experimental engines
#
###############################################################################

#------------------------------------------------------------------------------
# Different fuels as energy source.
#------------------------------------------------------------------------------

fuels = {}

class Fuel:

    def __init__(self, name, E = None, dm = None):
        self.E = E and E or solve_Emc(None, dm)
        self.name = name
        if name: fuels[name] = self

    #--------------------------------------------------------------------------

    def dm(self, ratio = 1.0, efficiency = 1.0):
        return solve_Emc(self.E * ratio * efficiency, None)

    #--------------------------------------------------------------------------

    def ve(self, ratio, efficiency):
        return solve_Emv(
            self.E * ratio * efficiency,
            1.0 - self.dm(ratio, efficiency),
            None
        )
        
    #--------------------------------------------------------------------------

    @staticmethod
    def atomic_mass(molecule):
        am = {
            "H":  1.008,
            "C": 12.011,
            "N": 14.007,
            "O": 15.999,
        }
        return sum([am[x] for x in molecule])
		
    #--------------------------------------------------------------------------

    @staticmethod
    def alias(name, to): return Fuel(name, E = fuels[to].E)

    #--------------------------------------------------------------------------
    # Chemical burning: giving in energy by fuel unit, atoms in fuel and
    # oxidizer, it computes specific energy.
    #--------------------------------------------------------------------------
    
    @staticmethod
    def Burn(name, energy, fuel, oxidizer):
        m_fuel     = Fuel.atomic_mass(fuel)
        m_oxidizer = Fuel.atomic_mass(oxidizer)
        m_tot      = m_fuel + m_oxidizer

        return Fuel(name, E = energy * m_fuel / m_tot)
    
    #--------------------------------------------------------------------------
    # Burning hydrocarbons
    #--------------------------------------------------------------------------

    @staticmethod
    def CH(name, energy, C, H, O = 0, N = 0):
        return Fuel.Burn(
            name,
            energy,
            C*["C"] + H*["H"] + O*["O"] + N*["N"],
            int(2*C + H/2 - O)*["O"]
        )

#------------------------------------------------------------------------------

Fuel("!H",       dm = 1.0000000)
Fuel("D-He3",    dm = 0.0040423)
Fuel("D-T",      dm = 0.0037681)
Fuel("D-D",      E  = 87900000.00e6)
Fuel("U235",     E  = 80620000.00e6)
Fuel("Th232",    E  = 79420000.00e6)
Fuel("Pu239",    E  =    83610.00e6)

Fuel.CH("LH2/LOX",       141.86e6,  0,  2)
Fuel.CH("CH4/LOX",        55.60e6,  1,  4)
Fuel.CH("C2H6/LOX",       51.80e6,  2,  6)
Fuel.CH("C3H8/LOX",       50.30e6,  3,  8)
Fuel.CH("C4H10/LOX",      49.50e6,  4, 10)
Fuel.CH("C12H26/LOX",     46.20e6, 12, 26)

Fuel.CH("CH3OH/LOX",      22.70e6,  1,  4,  1)
Fuel.CH("C2H5OH/LOX",     29.70e6,  2,  6,  1)
Fuel.CH("C3H7OH/LOX",     33.60e6,  3,  8,  1)

#Fuel("N2O4/UDMH", E = None)

Fuel("TNT",       E = 4.610e6)
Fuel("Gunpowder", E = 3.000e6)
Fuel("Hydrazine", E = 1.600e6)

#------------------------------------------------------------------------------
# APCP is a mixture of reagents, used in various forms in solid rocket
# boosters. It's main fuel is aluminium which energy density is 31.0 MJ/kg.
# Space Shuttle SRB APCP mixture:
#
# Ammonium Perchlorate (AP) NH4ClO4: 69.6% (oxidizer)
# Aluminium (Al)                   : 16.0% (main fuel)
# Rest                             : 14.4%
# - PBAN (binder)                    12.0% (also fuel)
# - Epoxy curing                      2.0%
# - Iron oxide catalyst               0.4%
# 
#------------------------------------------------------------------------------

Fuel("APCP", E = 31.0e6 * 0.16)  # Guessed

#------------------------------------------------------------------------------
# A.K.A.
#------------------------------------------------------------------------------

Fuel.alias("Antimatter",    "!H")
Fuel.alias("Methane",       "CH4/LOX")
Fuel.alias("Ethane",        "C2H6/LOX")
Fuel.alias("Propane",       "C3H8/LOX")
Fuel.alias("Butane",        "C4H10/LOX")
Fuel.alias("Kerosene",      "C12H26/LOX")
Fuel.alias("RP-1",          "C12H26/LOX")
Fuel.alias("Methanol",      "CH3OH/LOX")
Fuel.alias("Ethanol",       "C2H5OH/LOX")
Fuel.alias("Propanol",      "C3H7OH/LOX")

Fuel.alias("Hydrolox",      "LH2/LOX")
Fuel.alias("Methalox",      "CH4/LOX")
Fuel.alias("Kerolox",       "C12H26/LOX")
