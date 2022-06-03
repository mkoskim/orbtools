#!/usr/bin/env python3
###############################################################################
#
# Fictive engine SSE-2 for moving cargo between Earth and Mars
#
# SSE, Speculative Space Engines
#
###############################################################################

import os, sys
sys.path.append(os.path.abspath("."))

from orbtools.systems.solsystem import *
from orbtools.systems.exoplanets import *

#------------------------------------------------------------------------------
# Lifting up to LEO, orbiting + losses:
#------------------------------------------------------------------------------

m_ship = 6000.0
m_propellant = 6000.0
m_tot = m_ship + m_propellant
#dv = 10e3
#a = 1.5 * 9.81
#F = m_tot * a
ve = solve_rocket_eq(m_tot, m_ship, dv, None)

ship = Stage("Learspace",
    payload=m_ship,
    fuel=m_propellant,
    engine = Engine(name="SSE-1", ve = ve, F = F)
)

#print(ship.a_initial)
#print(fmttime(ship.t_burn))
ship.show()
ship.engine.show()

sys.exit()

#------------------------------------------------------------------------------
# Fuels for engines
#------------------------------------------------------------------------------

selected = map(lambda name: fuels[name], [
    "U235", "Pu239",
    "D-He3", "T-T",
    "AM",
])

def SSE1_fuel(fuel):
    #Esp = ship.engine.Esp
    ship_P = ship.engine.P
    fuel_per_second = ship_P / fuel.E
    fuel_tot = ship.fuel * ship.engine.Esp / fuel.E
    print(fuel.name, "flow:", fmtmass(fuel_per_second, "g/s"), "tot:", fmtmass(fuel_tot))

for fuel in selected:
    #print("%10s Esp=%6.2f TJ/kg" %(fuel.name, fuel.E * 1e-12))
    #fuel.show()
    SSE1_fuel(fuel)

sys.exit()

#------------------------------------------------------------------------------
# Reaction chamber temperature
#------------------------------------------------------------------------------

def show_T_ve(T, ve):
    print("T=%.2f K" % (T), "ve=%s" % (fmteng(ve, "m/s")))

def T_to_ve(T):
    ve = solve_MTv("H", T, None)
    return (T, ve)

def ve_to_T(ve):
    T = solve_MTv("H", None, ve)
    return (T, ve)

for T in [2000, 3000, 4000, 5000, 6000, 7000, 8000]:
    show_T_ve(*T_to_ve(T))

for ve in [4000, 8000, 10000, 15000, 20000]:
    show_T_ve(*ve_to_T(ve))

#sys.exit()

#print("a initial (g):", a / 9.81)
#print("a final.. (g):", F / m_ship / 9.81)
#print("Flow:", engine.F / engine.ve)
#print("Burn:", engine.t(m_propellant))
#print("T (H):", solve_MTv("H", None, ve))
#print("T (O):", solve_MTv("O", None, ve))

#------------------------------------------------------------------------------
# Engine comparison
#------------------------------------------------------------------------------

#engines["Merlin 1D"].show()
#engines["RS-25"].show()
#engines["F-1"].show()
#engines["NERVA"].show()
