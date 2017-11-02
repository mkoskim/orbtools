###############################################################################
###############################################################################
#
# Building missions
#
###############################################################################
###############################################################################

from orbtools import *

###############################################################################
#
# Burn: transfer from one orbit to another.
#
###############################################################################

class Burn(object):
	def __init__(self, name, orbFrom, orbTo, initial = True):

		if orbFrom.center != orbTo.center:
			raise Exception("Orbits have different central masses!")
		if abs(orbFrom.r_final - orbTo.r_initial) > 0.05*orbTo.r_initial:
			raise Exception("Orbit does not reach target")

		if initial:
			self.dv = abs(orbTo.v_initial - orbFrom.v_initial)
		else:
			self.dv = abs(orbTo.v_final - orbFrom.v_final)
		self.dt = orbTo.T_to_target * orbTo.P
		self.name = name
		self.orbit = orbTo

#------------------------------------------------------------------------------
# Loss (friction, gravity) estimations
#------------------------------------------------------------------------------

class Loss(object):
	def __init__(self, name, orbit, loss):
		self.name = name
		self.orbit = orbit
		self.dv = loss
		self.dt = 0

#------------------------------------------------------------------------------
# Entering system to given orbit
#------------------------------------------------------------------------------

class EnterSystem(object):

	def __init__(self, name, orbFrom, orbTo):

		if orbTo.center.orbit.center != orbFrom.center:
			raise Exception("Target center != orbit center")

		if abs(orbFrom.r_final - orbTo.center.orbit.a) > orbTo.center.SOI():
			raise Exception("Orbit does not reach system")

		r_enter = orbTo.center.orbit.r2
		v_enter = abs(orbFrom.dv_circular(r_enter))
		v_enter = sqrt(v_enter ** 2 + 2*orbTo.center.GM/orbTo.r1)

		self.dv = abs(v_enter - abs(orbTo.v(0)))
		self.dt = 0
		self.name = name
		self.orbit = orbTo
	
#------------------------------------------------------------------------------
# Escape from system to orbit its central mass
#------------------------------------------------------------------------------

class ExitSystem(object):
	def __init__(self, name, orbit, target_r, r1 = None, r2 = None):
		oldcenter = orbit.center
		newcenter = orbit.center.orbit.center

		exit_orbit = Trajectory(
			newcenter,
			oldcenter.orbit.a,
			target_r,
			r1, r2
		)
		v_exit = abs(exit_orbit.v(0) - oldcenter.orbit.v(0))
		v_exit = sqrt(v_exit ** 2 + oldcenter.v_escape(orbit.r1) ** 2)

		self.dv = abs(v_exit - abs(orbit.v()))
		self.dt = exit_orbit.T_to_target * exit_orbit.P
		self.name = name
		self.orbit = exit_orbit

#------------------------------------------------------------------------------
# "Virtual" burn for mission initial orbit
#------------------------------------------------------------------------------

class Initial(object):
	def __init__(self, orbit):
		self.name = "Start"
		self.dv = 0
		self.dt = 0
		self.orbit = orbit

###############################################################################
#
# Mission: A sequence of burns
#
###############################################################################

class Mission(object):
	def __init__(self, name, initial_orbit):
		self.name = name
		self.burns = [ Initial(initial_orbit) ]

	def burn(self, name, to_orbit):
		self.burns.append(Burn(name, self.orbit, to_orbit))

	def park(self, name, to_orbit):
		self.burns.append(Burn(name, self.orbit, to_orbit, False))

	def loss(self, name, dv):
		self.burns.append(Loss(name, self.orbit, dv))

	def enter(self, name, orbit):
		self.burns.append(EnterSystem(name, self.orbit, orbit))

	def exit(self, name, orbit):
		self.burns.append(ExitSystem(name, self.orbit, orbit.r_final))

	@property
	def orbit(self): return self.burns[-1].orbit
	
	@property
	def dt(self): return sum(map(lambda b: b.dt, self.burns))
			
	@property
	def dv(self): return sum(map(lambda b: b.dv, self.burns[1:]))

	def show(self):
		print "Mission:", self.name
		for burn in self.burns[1:]:
			print "    Burn: %-15s dv=%8.2f dt=%10s" % (burn.name, burn.dv, fmttime(burn.dt))
		print "    ---"
		print "    Tot.: %15s dv=%8.2f dt=%10s" % ("", self.dv, fmttime(self.dt))


