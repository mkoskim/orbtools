###############################################################################
#
# Earth LEO - Mars
#
###############################################################################

import os, sys
sys.path.append(os.path.abspath(".."))

from sol import *

#------------------------------------------------------------------------------
#
# Some possibly interesting Earth-Mars trajectories:
#
# - Free return trajectory: periapsis = Earth.orbit.a, P = 2 years: in case
#   you don't want to enter Mars, you will be returned to Earth
#
# - Or, periapsis = Earth.orbit.a, P = 3 years
#
# - Propulsive return trajectory: Use the fuel meant to orbit Mars to
#   take you back to Earth. Also, it could use Mars for gravity assisted sling
#   trajectory.
#
#------------------------------------------------------------------------------

###############################################################################
#
# Timing studies
#
###############################################################################

#------------------------------------------------------------------------------
#
# (Typical?) Mars trip:
# - Earth-Mars: 220 days (180-270)
# - Stay......: 477 days
# - Mars-Earth: 220 days (180-270)
# - Tot.......: 917 days
#
# Computed Mars trip:
#
# - Earth-Mars: 258 days
# - Stay......: 454 days
# - Mars-Earth: 258 days
# - Tot.......: 972 days
#
# See e.g.
#
#	http://www-istp.gsfc.nasa.gov/stargaze/Smars3.htm
#	http://en.wikipedia.org/wiki/List_of_manned_Mars_mission_plans_in_the_20th_century
#
#------------------------------------------------------------------------------
#
# Von Braun Mars trip:
# - Earth-Mars: 270 days
# - Stay......:  80 days
# - Mars-Earth: 290 days
# - Tot.......: 640 days
#
# Uses Venus Flyby return flight; we might implement such orbits...
#
#------------------------------------------------------------------------------

def timing(transfer):

	earth_departure = transfer.launch_angle_up() * (transfer.P_window/360)
	travel_mars     = transfer.T_to_target * transfer.P	
	mars_arrival    = earth_departure + travel_mars
	
	mars_departure  = transfer.launch_angle_down() * (transfer.P_window/360)
	if mars_departure < mars_arrival:
		mars_departure += transfer.P_window
	travel_earth = transfer.T_to_target * transfer.P
	earth_arrival = mars_departure + travel_earth
	
	mars_stay = (mars_departure - mars_arrival)	

	print "Mission timing...:"
	print "- Earth departure: day %4d, delta %4d" % (TtoDays(earth_departure), 0)
	print "- Mars arrival...: day %4d, delta %4d" % (TtoDays(mars_arrival), TtoDays(travel_mars))
	print "- Mars stay......: day %4d, delta %4d" % (TtoDays(mars_arrival), TtoDays(mars_stay))
	print "- Mars departure.: day %4d" % TtoDays(mars_departure)
	print "- Earth arrival..: day %4d, delta %4d" % (TtoDays(earth_arrival), TtoDays(travel_earth))
	print "- Total..........:           delta %4d" % TtoDays(earth_arrival - earth_departure)
	print
	
transfer = Trajectory(Sun, Earth.orbit.a, Mars.orbit.a)

timing(transfer)

###############################################################################
#
# Mission delta v budget
#
###############################################################################

#------------------------------------------------------------------------------
# Create start and end orbits
#------------------------------------------------------------------------------

LEO = Altitude(Earth, 300e3)
LMO = Altitude(Mars, 1000e3)

#------------------------------------------------------------------------------
# Make a mission
#------------------------------------------------------------------------------

Earth2Mars = Mission("Earth - Mars", LEO)

#------------------------------------------------------------------------------
# Burn from start to end
#------------------------------------------------------------------------------

Earth2Mars.exit ("LEO - TMI", LMO.center.orbit)
Earth2Mars.enter("TMI - MOI", LMO)

#------------------------------------------------------------------------------
# Show results
#------------------------------------------------------------------------------

Earth2Mars.show()

