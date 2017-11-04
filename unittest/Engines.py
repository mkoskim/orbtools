###############################################################################
#
# Testing the new add-on, "engine lab"
#
###############################################################################

from orbtools import *

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

