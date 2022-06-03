#!/usr/bin/env python3
###############################################################################
#
# Engine T-ve plot
#
###############################################################################

import os, sys
sys.path.append(os.path.abspath("."))

from orbtools.systems.solsystem import *
from orbtools.systems.exoplanets import *

#------------------------------------------------------------------------------

for e in engines.values():
    print(e.name, "F=", fmteng(e.F, "N"), "ve=", fmteng(e.ve, "m/s"), "P=", fmteng(e.P, "W"))

