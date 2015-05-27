#!/usr/bin/env python2
# -*- coding: utf-8 -*-
################################################################################
#
# Study about amount of travelers in space stations. That is, studying
# the launch windows and travel times to see departures and arrivals.
#
################################################################################

import sys

from orbtools.systems.solsystem import *

#-------------------------------------------------------------------------------
# Do a trajectory from A to B, lifting apoapsis/periapsis at given values.
# Print out departure & arrival times to both directions.
#-------------------------------------------------------------------------------

def doTrajectory(
	A, B,								# Bodies to travel between
	offset = 0.0,						# "offset" for plots
	liftDown = None, liftUp = None,		# Lifting trajectory up/down
	swingby_up = False,					# Swing-by via apoapsis
	swingby_down = False,				# Swing-by via periapsis
	):

	assert A.orbit.center == B.orbit.center
	
	t = Trajectory(
		A.orbit.center,
		A.orbit.a,
		B.orbit.a,
		liftDown,
		liftUp
	)
	
	travel_time  = t.P * t.T_to_target()

	up_dv        = t.dv_enter
	up_launch    = t.launch_angle_up()
	up_departure = t.P_window * (up_launch/360)
	up_arrival   = up_departure + travel_time

	dn_dv        = t.dv_exit
	dn_launch    = t.launch_angle_down()
	dn_departure = t.P_window * (dn_launch/360)
	dn_arrival   = dn_departure + travel_time

	def fmtDay(d): return TtoDays(d)

	print fmtDay(up_departure), 1 + offset, fmtDay(dn_arrival), 1 + offset
	print fmtDay(dn_departure), 2 + offset, fmtDay(up_arrival), 2 + offset

"""	
	print
	print "Travel.....:", A.name, "->", B.name
	print "P_window...:", TtoDays(t.P_window)
	print "Travel time:", TtoDays(travel_time)

	print "Angle up...:", "%+.2f" % up_launch
	print "- Departure: d = ", TtoDays(up_departure)
	print "- Arrival..: d = ", TtoDays(up_arrival)
	print "- DV enter.: %.2f", up_dv

	print "Angle down.:", "%+.2f" % dn_launch
	print "- Departure: d = ", TtoDays(dn_departure)
	print "- Arrival..: d = ", TtoDays(dn_arrival)
	print "- DV enter.: %.2f", dn_dv
"""

#-------------------------------------------------------------------------------
# Launch plots
#-------------------------------------------------------------------------------

def doLaunchPlot():
	print>>sys.stderr, "P(window):", TtoDays(P_window(Sun.GM, Earth.orbit.a, Mars.orbit.a))

	for higher in [0.0, 0.25, 0.5, 0.75, 1.0]:
		for lower in [0.0, 0.1, 0.2, 0.3, 0.4]:

			if higher == 0 and lower == 0:
				continue
			elif higher != 0 and lower != 0:
				offset = 0.2
			elif higher != 0:
				offset = 0.1
			else:
				offset = -0.1
		
			doTrajectory(Earth, Mars,
				offset,
				Earth.orbit.a - AU2m(lower),
				Mars.orbit.a + AU2m(higher)
			)

#-------------------------------------------------------------------------------
# Orbit plots
#-------------------------------------------------------------------------------

def distScale( v ):
	return \
		10 * m2AU(v.x), \
		10 * m2AU(v.y), \
	
def doPlanetPlot(filename = "plots/MarsEarthOrbits.dat"):
	tra = Trajectory(
		Sun,
		Earth.orbit.a, Mars.orbit.a,
		Earth.orbit.a - AU2m(0.3),
		Mars.orbit.a + AU2m(0.5)
	)

	data = []
	
	for t in range(50 + 1):
		x1, y1 = distScale(Earth.orbit.pos_xy(t/50.0))
		x2, y2 = distScale(Mars.orbit.pos_xy(t/50.0))
		x3, y3 = distScale(tra.pos_xy(t/50.0))
		data.append( [x1, y1, x2, y2, x3, y3] )

	plotter.dumpdata(filename, data)
	plotter.plot("plots/", "MarsEarthTrajectory.gnuplot")

doPlanetPlot()
exit()

def doTrajectoryPlot():
	tra = Trajectory(Earth, Mars,
		Earth.orbit.a - AU2m(0.3),
		Mars.orbit.a + AU2m(0.5)
	)
	t_start = tra.time(Earth.orbit.a)
	t_stop  = tra.time(Mars.orbit.a)
	t_len   = t_stop - t_start
	
	for t in range(50):
		x, y = distScale(tra.pos_xy(t_start + t_len * t/50.0))
		print x, y
		
#-------------------------------------------------------------------------------
# Testing etc.
#-------------------------------------------------------------------------------

tra1 = Trajectory(
		Sun,
		Earth.orbit.a, Mars.orbit.a,
		Earth.orbit.a - AU2m(0.3),
		Mars.orbit.a + AU2m(0.5)
)
tra2 = Trajectory(
		Sun,
		Earth.orbit.a, Mars.orbit.a,
)

print "Hohmann", tra2.dv_enter, tra2.dv_exit, tra2.dv_total
print "Example", tra1.dv_enter, tra1.dv_exit, tra1.dv_total

#doPlanetPlot()
#doTrajectoryPlot()

#doTrajectory(Earth, Mars, None, AU2m(1.6))
#doTrajectory(Earth, Mars, AU2m(0.9), None)

################################################################################
#
# Older tests... Notice sys.exit()
#
################################################################################

sys.exit()

o  = Trajectory(Sun, Earth.orbit.r1, Mars.orbit.r1)
e  = Engine(4000)
R1 = e.R(o.dv_hohmann_total())

for alt in [1.6, 1.8, 2.0, 2.5, 3.0, 4.0, 5.0]:
    t = Trajectory(
        Sun, Earth.orbit.r1, Mars.orbit.r1,
        Earth.orbit.r1,
        AU2m(alt))
    print "%.1f %3.0f %4.1f %4.1f" % (
        alt, TtoDays(t.T_to_target()),
        t.dv_total()/1000, e.R(t.dv_total())/R1
    )

sys.exit(0)
        
#print TtoDays(o.T_to_target()), o.dv_enter(), o.dv_exit(), o.dv_total()

#print TtoDays(o.P_hohmann()), o.dv_hohmann_enter(), o.dv_hohmann_exit(), o.dv_hohmann_total()

for higher in [0.0, 0.25, 0.5, 0.75, 1.0]:
    for lower in [0.0, 0.1, 0.2, 0.3, 0.4]:
        t = Trajectory(Sun, Earth.orbit.r1, Mars.orbit.r1,
            Earth.orbit.r1 - AU2m(lower),
            Mars.orbit.r1 + AU2m(higher))
        print "%.2f - %.2f: %3.0f %5.1f" % (
            lower, higher,
            TtoDays(t.T_to_target()), e.R(t.dv_total())/R1
        ) #t.dv_total(), "(", t.dv_enter(), t.dv_exit(), ")"
