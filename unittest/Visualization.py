# -*- coding: utf-8 -*-
###############################################################################
#
# Testing visualizations
#
###############################################################################

import os, sys
sys.path.append(os.path.abspath(".."))

from sol import *

low  = Altitude(Earth, 300e3)
high = Altitude(Earth, 1000e3)
    
o1 = Orbit(Earth, low.r(), high.r())
o2 = Orbit(Earth, high.r(), low.r(), arg = 180, T0 = 0.5)

window = gui.window()

gui.run()
