#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
#
# Make a plot about escape velocity - object entering a system has its
# speed always over escape velocity
#
###############################################################################

import os, sys
sys.path.append(os.path.abspath("."))

from orbtools.systems.solsystem import *
from orbtools.systems.exoplanets import *

#------------------------------------------------------------------------------

orbits = [
    byAltitude(Earth, 300e3)
]