#!/usr/bin/python2
# -*- coding: utf-8 -*-
###############################################################################
#
# Launch window periods between different planets
#
###############################################################################

from sol import *
import string

#------------------------------------------------------------------------------
# What table to do?
#------------------------------------------------------------------------------

def launch_window_period(A, B):
	if A == B: return None
	return P_window(A.center.GM, A.orbit.a, B.orbit.a)

def travel_time(A, B):
	if A == B: return None
	trajectory = Trajectory(A.center, A.orbit.a, B.orbit.a)
	return trajectory.P * trajectory.T_to_target()

#------------------------------------------------------------------------------
# Do table
#------------------------------------------------------------------------------

def maketable(f, *planets):
	maxlen = max(map(lambda p: len(p.name), planets))
	
	table = []

	for A in planets:
		table.append(map(lambda B: f(A, B), planets))
	
	print " " * maxlen, string.join(
		map(lambda planet: planet.name.rjust(maxlen), planets),
		" "
	)
	
	for planet, line in zip(planets, table):
		print planet.name.ljust(maxlen),
		for value in line:
			if value != None:
				print "%*.2f" % (maxlen, TtoYears(value)),
			else:
				print "-".rjust(maxlen),
		print
	
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

Ceres = masses["Ceres"]

maketable(launch_window_period, Venus, Earth, Mars, Ceres, Jupiter, Saturn, Uranus, Neptune)
print

maketable(travel_time, Venus, Earth, Mars, Ceres, Jupiter, Saturn, Uranus, Neptune)
print

