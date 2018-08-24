###############################################################################
#
# Multistage rocket studies
#
###############################################################################

import os, sys
sys.path.append(os.path.abspath("."))

from sol import *

#------------------------------------------------------------------------------

engine = Exhaust(5000)

stages = []
for i in range(5):
    stages.append(Stage(str(i+1), engine, payload = 20, fuel = 80))

rocket = Rocket("R", *stages)

print "Tot. dv =", rocket.dv
print "Tot. k  =", rocket.dv / engine.ve
print "Tot. R  =", exp(rocket.dv / engine.ve)

#rocket.show()

