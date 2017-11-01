#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
#
# Misc. tests
#
###############################################################################

import os, sys
sys.path.append(os.path.abspath("."))

from orbtools import *
from sol import *

#------------------------------------------------------------------------------
# Testing escape velocities (velocities at infinite)
#------------------------------------------------------------------------------

import math

def Earth_escape(altitude, v_inf):
	r     = Earth.radius + altitude
	v_esc = Earth.v_escape(r)
	dv    = solve_rvrv(Earth.GM, r, None, Inf, v_inf)
	print "v_esc=%.2f v_inf=%7.2f dv=%.2f (d=%7.2f)" % (v_esc, v_inf, dv, dv - v_esc)
	return dv

Earth_escape(300e3, 0e3)
Earth_escape(300e3, 1e3)
Earth_escape(300e3, 3e3)
Earth_escape(300e3, 5e3)

exit()

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

# print solve_rocket_eq(None, 1, 9000, 4500)
# print solve_rocket_eq(1, None, 9000, 4500)
# print solve_rocket_eq(7.38, 1, None, 4500)
# print solve_rocket_eq(7.38, 1, 9000, None)

#------------------------------------------------------------------------------
# With rocket backpack to orbit, what's ve and kinetic energy?
#------------------------------------------------------------------------------

dv = solve_rocket_eq(250, 200, 9000, None)
Ekin = 0.5 * 50 * (dv ** 2)

print dv, Ekin*1e-9, Ekin/50*1e-6

