#!/usr/bin/env python3
###############################################################################
#
# Laser Thermal Engine
#
###############################################################################

import os, sys
sys.path.append(os.path.abspath("."))

from orbtools.systems.solsystem import *
from orbtools.systems.exoplanets import *

#------------------------------------------------------------------------------
# See: https://arxiv.org/pdf/2201.00244.pdf
#------------------------------------------------------------------------------

LTE = Engine(Isp2ve(3000), P = 100e6)

LTE.info()
