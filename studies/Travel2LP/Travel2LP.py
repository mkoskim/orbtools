#!/usr/bin/env python2
###############################################################################
#
# Traveling to Lagrangian points, times and delta-vs. The idea: assume that
# future interplanetary travels are mainly done by "ITN cruisers". How long
# it will take to go to one of these cruisers, and back?
#
###############################################################################

from sol import *

#------------------------------------------------------------------------------
#
# Lagrangian points:
# - L1:
# - L2:
# - L3: opposite side of the planet
# - L4: +60 degrees
# - L5: -60 degrees
#
#------------------------------------------------------------------------------

def Travel_L45(name, A, initial, transfer):
	#print TtoDays(transfer.P), m2AU(transfer.r1), m2AU(transfer.r2)
	
	dv_exit  = ExitSystem("Exit", initial, transfer.r2).dv
	dv_enter = abs(A.orbit.v() - transfer.v())
	print "- %s: T=%-5.2f dv=%.2f (%.2f + %.2f)" % (
		#"%s (%d km)" % (A.name, initial.altitude() * 1e-3),
		name,
		TtoYears(transfer.P),
		dv_exit + dv_enter,
		dv_exit,
		dv_enter
	)

def Travel_L4(A, initial):
	Travel_L45(
		"L4", A,
		initial,
		Period(
			A.orbit.center,
			((360-60)/360.0) * A.orbit.P,
			A.orbit.a
		)
	)

def Travel_L5(A, initial):
	Travel_L45(
		"L5", A,
		initial,
		Period(
			A.orbit.center,
			((360+60)/360.0) * A.orbit.P,
			A.orbit.a
		)
	)

def Travel_L3(A, initial):
	Travel_L45(
		"L3", A,
		initial,
		Period(
			A.orbit.center,
			((360+180)/360.0) * A.orbit.P,
			A.orbit.a
		)
	)


def Travel2Lagrangian(A, altitude):
	initial = Altitude(A, altitude)
	print A.name, "(%d km)" % (altitude*1e-3), "P=%.2f" % TtoYears(A.orbit.P)
	Travel_L3(A, initial)
	Travel_L4(A, initial)
	Travel_L5(A, initial)
	print

Travel2Lagrangian(Venus, 1000e3)
Travel2Lagrangian(Earth, 1000e3)
Travel2Lagrangian(Mars,  1000e3)
Travel2Lagrangian(Jupiter, masses["Ganymede"].orbit.altitude())

