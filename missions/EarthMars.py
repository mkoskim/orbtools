###############################################################################
#
# Earth LEO - Mars
#
###############################################################################

import os, sys
sys.path.append(os.path.abspath("."))

from orbtools import *
from sol import *

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

def timing():

	tra_up = Trajectory(Sun, Earth.orbit.a, Mars.orbit.a, None, None)
	tra_dn = Trajectory(Sun, Earth.orbit.a, Mars.orbit.a, None, None)

	earth_departure = tra_up.launch_angle_up() * (tra_up.P_window/360)
	travel_mars = tra_up.T_to_target() * tra_up.P	
	mars_arrival = earth_departure + travel_mars
	
	mars_departure  = tra_dn.launch_angle_down() * (tra_dn.P_window/360)
	if mars_departure < mars_arrival:
		mars_departure += tra_dn.P_window
	travel_earth = tra_dn.T_to_target() * tra_dn.P
	earth_arrival = mars_departure + travel_earth
	
	mars_stay = (mars_departure - mars_arrival)	

	print "Mission timing"
	print
	print "Earth departure: day %4d" % TtoDays(earth_departure)
	print "Mars arrival...: day %4d" % TtoDays(mars_arrival)
	print "Mars departure.: day %4d" % TtoDays(mars_departure)
	print "Earth arrival..: day %4d" % TtoDays(earth_arrival)
	print
	print "Mission time...: %4d d" % TtoDays(earth_arrival - earth_departure)
	print "- Mars flight..: %4d d" % TtoDays(travel_mars)
	print "- Mars stay....: %4d d" % TtoDays(mars_stay)
	print "- Return.......: %4d d" % TtoDays(travel_earth)	
	print
	
timing()

###############################################################################
#
# Mission delta v budget
#
###############################################################################

LEO = masses["Earth300km"]
LMO = Mass("LMO1000km",0,0,0,Altitude(Mars, 1000e3))

Earth2Mars = Mission("Earth - Mars", LEO.orbit)

Earth2Mars.exit ("TMI", LMO.center.orbit.a)
Earth2Mars.enter("MOI", LMO.orbit)

Earth2Mars.show()


