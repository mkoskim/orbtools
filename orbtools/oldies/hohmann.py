################################################################################
#
# Basic Hohmann transfers
#
################################################################################

class Hohmann:

    #----------------------------------------------------------------------
    # This function extracts the circulating bodies. For example:
    # Moon --> Moon, Earth, Sun
    #------------------------------------------------------------------------

	def DoPath(self,orbit):
		if orbit == None: return []
		return self.DoPath(orbit.center.orbit) + [ orbit ]

   	#----------------------------------------------------------------------
   	# Calculate the needed exit velocity, to enter correct trajectory
   	# at the end.
	#----------------------------------------------------------------------

	def exit(self,orbits,dv):
		dv = float(dv)
		if len(orbits) > 1:
			for orbit in orbits[1:]:
				dv = solve_rvrv(
					orbit.center.GM,
					orbit.a(), None,
					Inf, dv)
				dv = dv - orbit.v(orbit.a())
		return dv
		
	#--------------------------------------------------------------------------
	# Calculate the entering velocity from transfer trajectory, caused
	# by the gravity of approaching masses
	#--------------------------------------------------------------------------

	def enter(self,orbits,v_enter):
		v_enter = float(v_enter)
		if len(orbits) < 2: return float(v_enter)
		GM = 0.0
		r  = 0.0
		v  = 0.0
		for orbit in orbits[1:]:
			GM = GM + orbit.center.GM
			r  = r  + orbit.a()
			v  = v  + orbit.v()
		return solve_rvrv(GM,r,None,Inf,abs(v_enter)) - v

	#--------------------------------------------------------------------------
	# Make the Hohmann transfer
	#--------------------------------------------------------------------------

	def __init__(self, orbit_old, orbit_new):
		self.start = orbit_old
		self.end = orbit_new
		#print "Transfer: ", orbit_old.toString(), "->", orbit_new.toString()
		exit_path = self.DoPath(orbit_old)
		enter_path = self.DoPath(orbit_new)

		#print esc_path, " -> ", ent_path
		#for i in esc_path: print "Esc->", i.center.name
		#for i in ent_path: print "Ent<-", i.center.name

		while len(exit_path)>1 and len(enter_path)>1 and (exit_path[1].center == enter_path[1].center):
			del exit_path[0]
			del enter_path[0]

		#print
		#for i in esc_path: print "Esc->", i.center.name
		#for i in ent_path: print "Ent<-", i.center.name
		#print

		# Now, make Hohmann
		r1 = exit_path[0].r1
		r2 = enter_path[0].r1
		hohmann = Trajectory(exit_path[0].center, r1, r2)
		#print "Hohmann: ", hohmann.center.name, fmteng(r1,"m"), fmteng(r2,"m")

		dv1 = self.exit(exit_path, hohmann.v_exit())

		dv2 = self.enter(enter_path, hohmann.v_enter())

		#print "Dv1 =", fmteng(dv1,"m/s")
		#print "Dv2 =", fmteng(dv2,"m/s")

		self.dv1 = dv1
		self.dv2 = dv2
		self.hohmann = hohmann


