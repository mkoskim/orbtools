#!/usr/bin/env python3
###############################################################################
#
# Exploring thermal conditions
#
###############################################################################

import os, sys
sys.path.append(os.path.abspath("."))

from orbtools.systems.solsystem import *
from orbtools.systems.exoplanets import *

#------------------------------------------------------------------------------

def show(propellant, E = None, T = None):
  M = propellant
  if T is None:
    T = Esp2T(M, E)
  else:
    E = T2Esp(M, T)

  print(M, "@", T, "=", fmteng(E, "J"))
  print("ve = ", solve_Emv(E, 1.0, None))

def ve2T(ve):
  E = solve_Emv(None, 1.0, ve)
  show("H", E)

# Hydrogen propellant at 2000K
show("H", T = 2000)
ve2T(10e3)
ve2T(50e3)
ve2T(100e3)

#show("H2O", E = 15e6)

exit()

# Test
print("Test:", de_laval(
  22,
  3500,
  1e5 / 70e5,
  1.22
))

# LH2-LOX engine

print("RS-25:",
  de_laval(
    "H2O",
    3300 + 273,
    1.0/69.0,   # ???
    1.33        # ???
  ),
  ("(SL: %.2f)" % (366 * const_g))
)

# NERVA

print("NERVA A2:",
  de_laval(
    "H",
    2119,
    1.0/50.0, # ???
    1.666     # ???
  ),
  ("(SL: %.2f)" % (811 * const_g))
)
