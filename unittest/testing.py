#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
#
# Misc. tests
#
###############################################################################

from orbtools import *

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

