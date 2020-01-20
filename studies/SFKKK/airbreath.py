###############################################################################
#
# Air breathing engines (e.g. Sabre/Skylon)
#
###############################################################################

import os, sys
sys.path.append(os.path.abspath("."))

from orbtools.systems.solsystem import *
from orbtools.systems.exoplanets import *

#------------------------------------------------------------------------------

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

#engine = engines["Merlin 1D"]
engine = engines["SSME"]

engine_info(engine)

#------------------------------------------------------------------------------

rocket1 = Stage("SSTO", engine = engine, payload = 60e3, dv = 9000)

print "Tot. k  =", rocket1.dv / engine.ve
#print "Tot. R  =", exp(rocket.dv / engine.ve)
print "Tot. dv =", rocket1.dv
print "Tot. M  =", fmteng(rocket1.mass / 1e3, "t")
print "Fuel    =", fmteng(rocket1.fuel / 1e3, "t")

rocket2 = Stage("TSTO", engine = engine, payload = 60e3, dv = 9000 - MACH2ms(3))

print "Tot. dv =", rocket2.dv
print "Tot. M  =", fmteng(rocket2.mass / 1e3, "t")
print "Fuel    =", fmteng(rocket2.fuel / 1e3, "t")

print "Mass save:", fmteng((rocket1.mass - rocket2.mass) / 1e3, "t")


