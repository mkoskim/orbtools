###############################################################################
#
# Testing the new add-on, "engine lab"
#
###############################################################################

import os, sys
sys.path.append(os.path.abspath("."))

from orbtools import *
from sol import *
from testlib  import *

#------------------------------------------------------------------------------
# Check basics of the engines: See
#
#   https://en.wikipedia.org/wiki/Spacecraft_propulsion#Reaction_engines
#
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
#
# Energy efficiency: How much from the energy used can be transferred to a
# kinetic energy of the payload?
#
# With fixed ve, this is achieved when dv/ve ~ 2/3 (energy efficiency ~65%).
# If the engine has variable ve, energy efficiency can be kept high by matching
# the ve to ship speed v.
#
#------------------------------------------------------------------------------

def test_E_eff():

    def energy_efficiency(dv, ve): return Exhaust(ve).E_eff(dv)

    expect(energy_efficiency(3000, 1000)*100, 47.1, 1, "1")
    expect(energy_efficiency(3000, 2000)*100, 64.6, 1, "2")
    expect(energy_efficiency(3000, 3000)*100, 58.2, 1, "3")
    expect(energy_efficiency(3000, 5000)*100, 43.8, 1, "4")
    expect(energy_efficiency(3000, 6000)*100, 38.5, 1, "5")

test_E_eff()

#------------------------------------------------------------------------------
# Burn time depends on (1) input power (the larger, the shorter), (2)
# exhaust velocity (the larger, the longer), and (3) amount of fuel (the
# more the longer). These are examples from Wiki page.
#------------------------------------------------------------------------------

def test_burn_time():

    def burn(P, payload, dv, ve):
        e = Exhaust(ve)
        m = e.fuel(payload, dv)
        return e.t(P, m)

    expect(TtoMonths(burn(1e3, 100, 5e3, 16e3)), 1.8, 0.1, "1")
    expect(TtoMonths(burn(1e3, 100, 5e3, 50e3)), 5.0, 0.1, "2")

test_burn_time()

#------------------------------------------------------------------------------
# Let's create an engine with ve = 5000 m/s. Let's check, how much is the
# mass flow and thrust force with 1 MW power source (100% efficiency).
#------------------------------------------------------------------------------

def test_thrust():
    e = Exhaust(5e3)
    
    expect(e.flow(1e6), 0.08,  0.01, "1")
    expect(e.F(1e6),    400.0, 1.00, "2")

test_thrust()

#------------------------------------------------------------------------------
#
# Print out comparison from Wiki page: when Isp (ve) raises, propellant mass
# decreases, propellant kinetic energy increases, and power per thrust (W/N)
# increases.
#
#------------------------------------------------------------------------------

def comparison(*engines):

    payload = 10e3
    dv = 3000
    
    print("%5s %6s %10s %15s %15s" % ("ve", "fuel", "E", "E/kg", "P/F"))

    for engine in engines:
        fuel  = engine.fuel(payload, dv)
        E     = engine.E(fuel)
        print("%5.0f %6.0f %10s %15s %15s" % (
            engine.ve,
            fuel,
            fmteng(E, "J"),
            fmteng(E/fuel, "J/kg"),
            fmteng(engine.P(), "W/N"),
        ))

    print

#comparison(
#    Exhaust( 1e3),   # Solid rocket
#    Exhaust( 5e3),   # Liquid rocket
#    Exhaust(50e3),   # Ion thruster
#)

#------------------------------------------------------------------------------
# Compare engines from engine database. These are (mainly) existing engines.
#------------------------------------------------------------------------------

def compare_engines():

    names = [
        "F-1", "J-2",
        "SSME", "SSSRB",
        "Merlin 1C", "Merlin 1D", "Raptor",
        "RD-180", "RD-191", "RD-263",
        "P230",
        "HiPEP", "NSTAR", "VASIMR",
        "NERVA",
    ]

    print("%-10s %12s %12s %12s %12s %13s" % ("Name", "v(ex)", "Thrust", "P", "Mass flow", "E(flow)/kg"))

    for engine in sorted([engines[x] for x in names], key = lambda e: e.ve):
        print("%-10s %12s %12s %12s %12s %13s" % (
            engine.name,
            fmteng(ve2Isp(engine.ve), "s"),
            fmteng(engine.F, "N"),
            fmteng(engine.P, "W"),
            fmteng(engine.flow*1e3, "g/s"),
            fmteng(engine.E(), "J/kg"),
        ))

    print()

manual(__name__, compare_engines)

#------------------------------------------------------------------------------
# Fuels
#------------------------------------------------------------------------------

#------------------------------------------------------------------------------
#
# Propellant mixture ratio: LH2/LOX, 100% mixture is 15.999 / (2*1.008).
# Anything above means that not all O2 is burned, anything below means that
# not all H2 is burned. But how much is left unburned?
#
# We leave this out for now. First, the effect is usually not that high: there
# is approx. 3% of propellant mass left unburned. Second, with hydrocarbons it
# results to incomplete burning, which affects to heat values. More information
# would be needed to take those effects in account.
#
# Ratio is meant more for nuclear engines. Most of the speculated open cycle
# nuclear engines have considerable amounts (like 100:1) of inert H2 as
# propellant.
#
#------------------------------------------------------------------------------

def compare_fuels():

    def show(engine, fuel, efficiency, ratio = 1.0):
        engine = engines[engine]
        fuel   = fuels[fuel]
        E = fuel.E * ratio * efficiency
        print("%-10s %15s %12s %10s %15s %6.2f %%" % (
            engine.name,
            fmteng(engine.E(), "J/kg"),
            fmteng(engine.ve, "m/s"),
            fuel.name,
            fmteng(fuel.E, "J/kg"),
            100 * engine.E()/fuel.E
        ))
        
    show("SSME",        "Hydrolox", 0.620)
    show("Raptor",      "Methalox", 0.630)
    show("RD-191",      "Kerolox",  0.529)
    show("Merlin 1D",   "Kerolox",  0.529)
    show("F-1",         "Kerolox",  0.431)
    show("SSSRB",       "APCP",     0.696)

    #--------------------------------------------------------------------------
    # This is strange: computed Isp for gunpowder is ~250 s, but actual
    # gunpowder rockets have Isp around 80 s. It means that the efficiency
    # is just 10%.
    #--------------------------------------------------------------------------

    print("Gunpowder 100%%, Isp = %.2f" % ve2Isp(fuels["Gunpowder"].ve(1.0, 1.00)))
    print("Gunpowder  10%%, Isp = %.2f" % ve2Isp(fuels["Gunpowder"].ve(1.0, 0.10)))
    print("APCP      100%%, Isp = %.2f" % ve2Isp(fuels["APCP"].ve(1.0, 1.0)))
    
manual(__name__, compare_fuels)

#------------------------------------------------------------------------------
# Combust chamber temperatures
#------------------------------------------------------------------------------

def compare_temperatures():
	def show_T(ve, propellant):
		print("%5s: T = %12.2f, v = %12.2f" % (propellant, solve_TMv(None, Fuel.atomic_mass(propellant), ve), ve))
	
	def show_ve(T, propellant):
		print("%5s: T = %12.2f, v = %12.2f" % (propellant, T, solve_TMv(T, Fuel.atomic_mass(propellant), None)))
	
	print("Thermal velocities:")
	show_ve(20, "HH")
	show_ve(20, "HOH")
	
	show_T(2000, "HOH")
	show_T(3000, "HOH")
	show_T(4500, "HOH")
	show_T(100e3, "HH")

	show_ve(2000, "HOH")
	show_ve(2000, "HH")
	show_ve(4000, "HOH")

manual(__name__, compare_temperatures)

#------------------------------------------------------------------------------
#
#------------------------------------------------------------------------------

exit()

#------------------------------------------------------------------------------

def show(engine):
    print("%-10s: E=%15s Isp=%10.1f s (%10.3f km/s)" % (
        engine.name,
        fmteng(engine.E(), "J/kg"),
        ve2Isp(engine.u),
        engine.u * 1e-3
    ))

#------------------------------------------------------------------------------
# Antimatter engine
#------------------------------------------------------------------------------

show(Fuel("!H", ratio = 0.05, efficiency = 1.0))

#------------------------------------------------------------------------------
# Nuclear fusion & fission engines: Notice, that these are calculations where
# the reaction mass results are exhausted. Lowering the ratio means to make
# "mixtures" of reactive fuel and passive propellant.
#------------------------------------------------------------------------------

show(Fuel("D-He3", ratio = 1.0, efficiency = 1.0))
show(Fuel("D-T",   ratio = 1.0, efficiency = 1.0))
show(Fuel("D-D",   ratio = 1.0, efficiency = 1.0))
show(Fuel("U235",  ratio = 1.0, efficiency = 1.0))
show(Fuel("Th232", ratio = 1.0, efficiency = 1.0))

#------------------------------------------------------------------------------
# More "realistic" nuclear engines: these use smaller amounts of nuclear
# fuel to accelerate propellant mass (e.g. H2).
#------------------------------------------------------------------------------

show(Fuel("D-He3",ratio = 11.0 / (11.0 +  861.0), efficiency = 0.025))  # Discovery II
show(Fuel("D-T",  ratio = 41.0 / (41.0 + 4124.0), efficiency = 0.004))  # VISTA

#------------------------------------------------------------------------------
# Ion thruster
#------------------------------------------------------------------------------

show(Engine("Ion", 50e3))

#------------------------------------------------------------------------------
# Liqud rocket engines. 65% efficiency is pretty realistic nozzle efficiency
# in vacuum.
#------------------------------------------------------------------------------

show(Fuel("LH2",      ratio = 1.0, efficiency = 0.65))

show(Fuel("Methane",  ratio = 1.0, efficiency = 0.65))
show(Fuel("Ethane",   ratio = 1.0, efficiency = 0.65))
show(Fuel("Propane",  ratio = 1.0, efficiency = 0.65))
show(Fuel("Butane",   ratio = 1.0, efficiency = 0.65))
show(Fuel("Kerosene", ratio = 1.0, efficiency = 0.65))

show(Fuel("Propanol", ratio = 1.0, efficiency = 0.65))
show(Fuel("Ethanol",  ratio = 1.0, efficiency = 0.65))
show(Fuel("Methanol", ratio = 1.0, efficiency = 0.65))

#------------------------------------------------------------------------------
# Solid rockets. These seem to give too high Isp. Values are taken from
# combustion energy tables.
#------------------------------------------------------------------------------

show(Fuel("TNT",       ratio = 1.0, efficiency = 0.65))
show(Fuel("Gunpowder", ratio = 1.0, efficiency = 0.65))
show(Fuel("Hydrazine", ratio = 1.0, efficiency = 0.65))
