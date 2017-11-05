###############################################################################
#
# Testing the new add-on, "engine lab"
#
###############################################################################

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

def test_energy_efficiency():

    def energy_efficiency(dv, ve): return Exhaust(ve).E_eff(dv)

    expect(energy_efficiency(3000, 1000)*100, 47.1, 1, "E_eff 1")
    expect(energy_efficiency(3000, 2000)*100, 64.6, 1, "E_eff 2")
    expect(energy_efficiency(3000, 3000)*100, 58.2, 1, "E_eff 3")
    expect(energy_efficiency(3000, 5000)*100, 43.8, 1, "E_eff 4")
    expect(energy_efficiency(3000, 6000)*100, 38.5, 1, "E_eff 5")

test_energy_efficiency()

def test_burn_time():

    def burn(P, payload, dv, ve):
        e = Exhaust(ve)
        m = e.fuel(payload, dv)
        return e.t(P, m)

    expect(TtoMonths(burn(1e3, 100, 5e3, 16e3)), 1.8, 0.1, "Burn time 1")
    expect(TtoMonths(burn(1e3, 100, 5e3, 50e3)), 5.0, 0.1, "Burn time 2")

test_burn_time()

def test_thrust():
    e = Exhaust(5e3)
    
    expect(e.flux(1e6), 0.08,  0.01, "Thrust 1")
    expect(e.F(1e6),    400.0, 1.00, "Thrust 2")

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
    
    print "%5s %6s %10s %15s %15s" % ("ve", "fuel", "E", "E/kg", "P/F")

    for engine in engines:
        fuel  = engine.fuel(payload, dv)
        E     = engine.E(fuel)
        print "%5.0f %6.0f %10s %15s %15s" % (
            engine.ve,
            fuel,
            fmteng(E, "J"),
            fmteng(E/fuel, "J/kg"),
            fmteng(engine.P(), "W/N"),
        )

    print

#comparison(
#    Exhaust( 1e3),   # Solid rocket
#    Exhaust( 5e3),   # Liquid rocket
#    Exhaust(50e3),   # Ion thruster
#)

#------------------------------------------------------------------------------
# Compare engines from engine database. These are (mainly) existing engines.
#------------------------------------------------------------------------------

def compare_engines(*names):

    print "%-10s %12s %12s %12s %12s %13s" % ("Name", "v(ex)", "Thrust", "P", "Mass flow", "E(flow)/kg")

    for name in names:
        engine = engines[name]
        print "%-10s %12s %12s %12s %12s %13s" % (
            name,
            fmteng(engine.ve, "m/s"),
            fmteng(engine.F, "N"),
            fmteng(engine.P, "W"),
            fmteng(engine.flux*1e3, "g/s"),
            fmteng(engine.E(), "J/kg"),
        )

    print

compare_engines(
    "F-1", "J-2",
    "SSME", "SSSRB",
    "Merlin 1C", "Merlin 1D", "Raptor",
    "RD-180", "RD-263",
    "P230",
    "HiPEP", "NSTAR", "VASIMR",
    "NERVA",
)

#------------------------------------------------------------------------------
# Fuels
#------------------------------------------------------------------------------

print "RP-1:", fmteng(Fuel("Kerosene"), "J/kg")
print "CH4.:", fmteng(Fuel("Methane"), "J/kg")
print "LH2.:", fmteng(Fuel("LH2"), "J/kg")

#------------------------------------------------------------------------------
#
#------------------------------------------------------------------------------

exit()

#------------------------------------------------------------------------------

def show(engine):
    print "%-10s: E=%15s Isp=%10.1f s (%10.3f km/s)" % (
        engine.name,
        fmteng(engine.E(), "J/kg"),
        ve2Isp(engine.u),
        engine.u * 1e-3
    )

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

