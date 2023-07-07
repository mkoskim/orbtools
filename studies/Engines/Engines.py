#!/usr/bin/env python3
###############################################################################
#
# Engine studies
#
###############################################################################

import os, sys
sys.path.append(os.path.abspath("."))

from orbtools import *

#------------------------------------------------------------------------------

SSE2 = Engine(engines["HiPEP"].ve, P=1000*1e6)

def showInfo(engine):

    print(engine.name)
    print("- Pout=", engine.P * 1e-6)
    print("- F=", engine.F * 1e-3)
    print("- dm=", engine.flow)
    print("- ve=", engine.ve)
    print("- Esp=", engine.E() * 1e-6)

showInfo(engines["Merlin 1D"])
showInfo(engines["NERVA"])
showInfo(engines["NSTAR"])
showInfo(engines["HiPEP"])
showInfo(SSE2)

#------------------------------------------------------------------------------
"""
def fuel_info(fuel):
    ve60 = fuel.ve(1.0, 0.60)
    print "%s: %s %s %s : %s %s %s %s" % (
        fuel.name,
        fmteng(fuel.E, "J/kg"),
        fmteng(fuel.ve(1.0, 1.00), "m/s"),
        fmteng(ve60, "m/s"),
        #fmteng(solve_rocket_eq(1.0 +  0.5, 1.0, None, ve60), "m/s"),
        fmteng(solve_rocket_eq(1.0 +  1.0, 1.0, None, ve60), "m/s"),
        fmteng(solve_rocket_eq(1.0 +  2.0, 1.0, None, ve60), "m/s"),
        fmteng(solve_rocket_eq(1.0 +  5.0, 1.0, None, ve60), "m/s"),
        fmteng(solve_rocket_eq(1.0 + 10.0, 1.0, None, ve60), "m/s"),
        #fmteng(solve_rocket_eq(1.0 + 20.0, 1.0, None, ve60), "m/s"),
    )

print "Chemical"

fuel_info(fuels["TNT"])
fuel_info(fuels["APCP"])
fuel_info(fuels["Kerolox"])
fuel_info(fuels["Methalox"])
fuel_info(fuels["Hydrolox"])

def engine_info(engine):
    print "%s: %s %s %s %s : %s %s %s %s" % (
        engine.name,
        fmteng(engine.ve, "m/s"),
        fmteng(engine.P, "W"),
        fmteng(engine.flow * 1000, "g/s"),
        fmteng(engine.F, "N"),
        fmteng(engine.dv(1.0,  1.0), "m/s"),
        fmteng(engine.dv(1.0,  2.0), "m/s"),
        fmteng(engine.dv(1.0,  5.0), "m/s"),
        fmteng(engine.dv(1.0, 10.0), "m/s"),
    )

print "Electric"

engine_info(engines["NSTAR"])
engine_info(engines["HiPEP"])
engine_info(engines["VASIMR"])
engine_info(engines["SSSRB"])
engine_info(engines["F-1"])

def nuclear_engine(engine):
    #ve60 = fuel.ve(1.0, 0.60)
    print "%s --- -: %s %s : %s %s %s %s" % (
        engine.name,
        "N/A",
        fmteng(engine.ve, "m/s"),
        fmteng(engine.dv(1.0,  1.0), "m/s"),
        fmteng(engine.dv(1.0,  2.0), "m/s"),
        fmteng(engine.dv(1.0,  5.0), "m/s"),
        fmteng(engine.dv(1.0, 10.0), "m/s"),
    )

def nuclear_fuel(fuel, ratio):
    ve60 = fuel.ve(ratio/100.0, 0.60)
    print "%s %5.1f %%: %s %s : %s %s %s %s" % (
        fuel.name, ratio,
        fmteng(fuel.ve(ratio/100.0, 1.00), "m/s"),
        fmteng(ve60, "m/s"),
        fmteng(solve_rocket_eq(1.0 +  1.0, 1.0, None, ve60), "m/s"),
        fmteng(solve_rocket_eq(1.0 +  2.0, 1.0, None, ve60), "m/s"),
        fmteng(solve_rocket_eq(1.0 +  5.0, 1.0, None, ve60), "m/s"),
        fmteng(solve_rocket_eq(1.0 + 10.0, 1.0, None, ve60), "m/s"),
    )


print "Nuclear"

nuclear_engine(engines["NERVA"])

nuclear_fuel(fuels["Th232"],    1.0)
nuclear_fuel(fuels["D-D"],      1.0)
nuclear_fuel(fuels["D-T"],      1.0)
nuclear_fuel(fuels["D-He3"],    1.0)
nuclear_fuel(fuels["D-He3"],    5.0)

nuclear_fuel(fuels["!H"],       0.1)

"""