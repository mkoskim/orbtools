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
# The planned mission is following:
#
# 1) Mars base (MarsHab) is launched and landed to Mars at previous launch
#    window: This has also Mars ascent vechile to return crew to Mars orbit.
#
# 2) Manned SpaceHab, with Mars lander is launched to low Mars orbit: For
#    safety reasons, Mars lander is also parked to orbit first.
#
# 3) Crew lands to Mars from LMO using lander
#
# 4) At next Mars-Earth launch window, crew uses Mars ascent vehicle to
#    take them to SpaceHab parked at LMO
#
# 5) SpaceHab is launched to Earth
#
# 6) Separate CRW is used to land on Earth, SpaceHab itself is left to
#    interplanetary trajectory.
#
# Only the TMI uses LH2/LOX engines. To be sure, that rocket fuel can be
# stored for entire mission, other parts use hypergolic / solid fuels.
#
###############################################################################

#------------------------------------------------------------------------------
# Create orbit shorcuts
#------------------------------------------------------------------------------

LEO = Altitude(Earth, 300e3)
LMO = Altitude(Mars,  250e3)

#------------------------------------------------------------------------------
# Make a mission
#------------------------------------------------------------------------------

LEO2TMI = Mission("TMI @ LEO", LEO)
LEO2TMI.exit("LEO - TMI", LMO.center.orbit)

TMI2Surface = Mission("TMI Landing", LEO2TMI.orbit)
TMI2Surface.enter("Landing", Surface(Mars))

TMI2LMO = Mission("MOI", LEO2TMI.orbit)
TMI2LMO.enter("TMI - LMO", LMO)

LMO2Surface = Mission("Mars Landing", LMO)
LMO2Surface.transfer("Descent", Surface(Mars))

Surface2LMO = Mission("Mars - LMO", Surface(Mars))
Surface2LMO.transfer("Ascent", LMO)

#------------------------------------------------------------------------------
# Show results
#------------------------------------------------------------------------------

LEO2TMI.show()
TMI2Surface.show()
TMI2LMO.show()

LMO2Surface.show()
Surface2LMO.show()

#------------------------------------------------------------------------------
# Rockets to perform operations
# MAV = Mars Ascent Vehicle
#------------------------------------------------------------------------------

MAV = Stage("MAV Ascent", engine = Exhaust(Isp2ve(311)), payload = 2000, mission = Surface2LMO)

MAV.show()

