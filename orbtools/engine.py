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

    def P(self, F = 1): return solve_PFv(None, F, self.ve)
    def F(self, P):     return solve_PFv(P, None, self.ve)
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

    #--------------------------------------------------------------------------

    @property
    def ve(self): return self.exhaust.ve

    @property
    def F(self):    return self.exhaust.F(self.P)

    @property
    def flow(self): return self.exhaust.flow(self.P)

    @property
    def Esp(self):  return 0.5 * self.ve ** 2

    def solve(self, M0, M1, dv): return self.exhaust.solve(M0, M1, dv)
    def dv(self, payload, fuel): return self.exhaust.dv(payload, fuel)
    def fuel(self, payload, dv): return self.exhaust.fuel(payload, dv)

    def E(self, m = 1):     return self.exhaust.E(m)
    def E_eff(self, dv):    return self.exhaust.E_eff(dv)

    def t(self, m): return self.exhaust.t(self.P, m)

    def R(self, dv): return self.exhaust.R(dv)

    #--------------------------------------------------------------------------

    @staticmethod
    def veP(name, ve, P):   return Engine(ve, P = P, name = name)

    @staticmethod
    def IspP(name, isp, P): return Engine(Isp2ve(isp), P = P, name = name)

    @staticmethod
    def veF(name, ve, F):   return Engine(ve, F = F, name = name)

    @staticmethod
    def IspF(name, isp, F):    return Engine(Isp2ve(isp), F = F, name = name)

    #--------------------------------------------------------------------------

    def info(self):
        print("Engine....:", self.name)
        print("- v_e.....:", fmteng(self.ve, "m/s"))
        print("- Thrust..:", fmteng(self.F, "N"))
        print("- Power...:", fmteng(self.P, "W"))
        print("- Flow....:", fmtmass(self.flow))
        print("- Esp.....:", fmteng(self.Esp, "J/kg"))

#------------------------------------------------------------------------------
# Engine database: parameters are vacuum parameters... TODO: Add fuels.
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
# Chemical rocket engines
#------------------------------------------------------------------------------

Engine.IspF("F-1",          304.0,  7_770_000)    # Saturn first stage
Engine.IspF("J-2",          421.0,  1_033_000)    # Saturn upper stage
Engine.IspF("RS-25",        452.3,  2_279_000)    # Shuttle main engine (vac)
Engine.IspF("Vulcain",      431.0,  1_140_000)    # Ariane 5 main engine (vac)
Engine.IspF("SSSRB",        268.0, 14_000_000)    # Shuttle solid rocket booster (PBAN/APCP)

Engine.IspF("Merlin 1C",    336.0,    413_644)     # SpaceX Falcon 1, 9 (vac)
Engine.IspF("Merlin 1D",    348.0,    934_000)     # SpaceX Falcon 9 v1.1 (vac)
Engine.IspF("Raptor",       363.0,  2_300_000)     # SpaceX Raptor 1 (vac)

Engine.IspF("RD-180",       338.4,  4_152_136)     # RP-1 engine
Engine.IspF("RD-191",       337.0,  2_090_000)     # RP-1 engine
Engine.IspF("RD-263",       318.0,  1_130_000)     # N2O2/UDMH engine

Engine.IspF("P230",         286.0,  6_472_300)     # Ariane 5 HTPB booster

#------------------------------------------------------------------------------
# Electric rocket engines
#------------------------------------------------------------------------------

Engine.IspF("HiPEP",       9620.0, 0.670)       # Ion thruster:  39.3 kW
Engine.IspF("NSTAR",       3100.0, 0.092)       # Ion thruster:   2.3 kW
Engine.IspF("NEXT",        4170.0, 0.237)       # Ion thruster:   6.9 kW
Engine.IspF("X3",          2650.0, 5.400)       # Ion thruster: 102.0 kW
Engine.IspF("MPD",         4665.0, 2.750)       # MPD thruster: 100.0 kW

#Engine.IspF("VASIMR",      5000.0, 5.700)       # VASIMR: 200 kW

#------------------------------------------------------------------------------
# Thermonuclear rocket engines
#------------------------------------------------------------------------------

Engine.IspF("NERVA",        841.0, 246_663)      # NERVA nuclear thermal engine

#------------------------------------------------------------------------------
# A.K.A.
#------------------------------------------------------------------------------

#engines["SSME"]  = engines["RS-25"]

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

    def ve(self, ratio = 0.0, efficiency = 1.0):
        return sqrt(2 * self.E)
        #return solve_Emv(
        #    self.E * ratio * efficiency,
        #    1.0, # - self.dm(ratio, efficiency),
        #    None
        #)

    def show(self):
        print("Name...:", self.name);
        print("- Esp..:", fmteng(self.E, "J"))
        print("- ve...:", fmteng(self.ve(), "m/s"))

    #--------------------------------------------------------------------------
    # NOTE: g/mol, not kg/mol
    #--------------------------------------------------------------------------

    mole_mass = {
        "Pu239": 239.05216,
        "U235": 235.04393,
        "T": 3.0160492813,  # Tritium
        "D": 4.0282035557,  # Deuterium
        "He3": 3.0160293220,

        "H":  1.008,
        "C": 12.011,
        "N": 14.007,
        "O": 15.999,

        "H2O": 18.01528,
        "CO2": 44.01,
    }

    @staticmethod
    def atomic_mass(particles):
        if isinstance(particles, str): return Fuel.mole_mass[particles]
        return sum([Fuel.mole_mass[x] for x in particles])

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

    #--------------------------------------------------------------------------
    # Nuclear fuel
    #--------------------------------------------------------------------------

    @staticmethod
    def Nuclear(name, eV, *particles):
        E_mol = eV * const_eV * const_NA
        #print("E = %.2f TJ/mol" % (E_mol * 1e-12))

        m = Fuel.atomic_mass(particles) * 1e-3
        #print("m(mol):", m)

        Esp = E_mol / m
        #print(name, "E = %.2f TJ/kg" % (Esp * 1e-12))

        return Fuel(name, Esp)

#------------------------------------------------------------------------------
# Nuclear fuels
#------------------------------------------------------------------------------

Fuel.Nuclear("Pu239", 207.1e6, "Pu239")
Fuel.Nuclear("U235",  202.5e6, "U235")
Fuel.Nuclear("T-T",    11.3e6, "T", "T")
Fuel.Nuclear("D-He3",  14.7e5 + 3.6e6, "D", "He3")
#Fuel.Nuclear("D-T",    14.1e6 + 3.5e6, "D", "T")
#Fuel.Nuclear("D-T",)

Fuel("AM_1ug", dm=1e-9)
Fuel("AM_1mg", dm=1e-6)
Fuel("AM_1g",  dm=1e-3)
Fuel("AM_10g", dm=1e-2)
Fuel("AM",     dm=1.0)

#Fuel("D-He3",    dm = 0.0040423)
#Fuel("D-T",      dm = 0.0037681)
#Fuel("D-D",      E  = 87900.00e9)
#Fuel("U235",     E  = 83.14e12)
#Fuel("Pu239",    E  = 83.61e12)

#Fuel("Th232",    E  = 79420.00e9)     # Unconfirmed

#------------------------------------------------------------------------------
# Liquid chemical fuels
#------------------------------------------------------------------------------

Fuel.CH("LH2/LOX",       141.86e6,  0,  2)
Fuel.CH("CH4/LOX",        55.60e6,  1,  4)
Fuel.CH("C2H6/LOX",       51.80e6,  2,  6)
Fuel.CH("C3H8/LOX",       50.30e6,  3,  8)
Fuel.CH("C4H10/LOX",      49.50e6,  4, 10)
Fuel.CH("C12H26/LOX",     46.20e6, 12, 26)

Fuel.CH("CH3OH/LOX",      22.70e6,  1,  4,  1)
Fuel.CH("C2H5OH/LOX",     29.70e6,  2,  6,  1)
Fuel.CH("C3H7OH/LOX",     33.60e6,  3,  8,  1)

#Fuel.alias("Methane",       "CH4/LOX")
#Fuel.alias("Ethane",        "C2H6/LOX")
#Fuel.alias("Propane",       "C3H8/LOX")
#Fuel.alias("Butane",        "C4H10/LOX")
#Fuel.alias("Kerosene",      "C12H26/LOX")
#Fuel.alias("RP-1",          "C12H26/LOX")
#Fuel.alias("Methanol",      "CH3OH/LOX")
#Fuel.alias("Ethanol",       "C2H5OH/LOX")
#Fuel.alias("Propanol",      "C3H7OH/LOX")

#Fuel.alias("Hydrolox",      "LH2/LOX")
#Fuel.alias("Methalox",      "CH4/LOX")
#Fuel.alias("Kerolox",       "C12H26/LOX")

#------------------------------------------------------------------------------
# Solid chemical fuels
#------------------------------------------------------------------------------

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
