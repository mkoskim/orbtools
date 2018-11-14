###############################################################################
#
# Orbital calculation toolbox
#
###############################################################################

from orbtools import *

###############################################################################
#
# Solving Kepler's equation:
#
#    a1^3 * P1^2  =  a2^3 * P2^2
#
# Usage:
#
#	solve_aPaP( a1,p1, a2,p2 ) - place "None" for argument to solve
#
###############################################################################

def solve_aPaP(a1, P1, a2, P2):

    def solve_a_aPaP(a1, p1, _, p2):
        return ((a1 ** 3.0) * (p2 ** 2.0) / (p1 ** 2.0)) ** (1/3.0)

    def solve_P_aPaP(a1, p1, a2, _):
        return ((p1 ** 2.0) * (a2 ** 3.0) / (a1 ** 3.0)) ** 0.5

    if a1 == None: return solve_a_aPaP(a2, P2, None, P1)
    if a2 == None: return solve_a_aPaP(a1, P1, None, P2)
    if P1 == None: return solve_P_aPaP(a2, P2, a1, None)
    if P2 == None: return solve_P_aPaP(a1, P1, a2, None)
    return None

################################################################################
#
# Solve GM from (1) circular orbit parameters, (2) gravitational acceleration
# at given distance.
#
################################################################################

def solve_GM_from_aP(a, P): return a * ((2*pi*a/P) ** 2)
def solve_GM_from_rg(r, g): return g * (r ** 2.0)

################################################################################
#
# Solving energy equation:
#
#   E  = Ekin + Epot 
#   E1 = E2
#
#   ==> m*v1^2/2 - GM*m/r1 = m*v2^2/2 - GM*m/r2  || /m
#   ==> v1^2/2 - GM/r1 = v2^2/2 - GM/r2
#
################################################################################

def solve_rvrv(GM, r1, v1, r2, v2):

    def solve_v2(GM, r1, v1, r2, _):
        return sqrt(v1**2.0 + 2.0*GM*(1.0/r2-1.0/r1));

    def solve_r2(GM, r1, v1, _, v2):
        return 1.0/( 1.0/r1 + (v2**2.0-v1**2.0)/(2.0*GM) );

    if r1 == None: return solve_r2(GM, r2, v2, None, v1)
    if r2 == None: return solve_r2(GM, r1, v1, None, v2)
    if v1 == None: return solve_v2(GM, r2, v2, r1, None)
    if v2 == None: return solve_v2(GM, r1, v1, r2, None)
    return None

################################################################################
#
# Conservation of impulse momentum
#
################################################################################

def solve_vro_v2(v1, r1, o1, _ , r2, o2): return float(v1)*r1*o1/(r2*o2)
def solve_vro_r2(v1, r1, o1, v2, _ , o2): return float(v1)*r1*o1/(v2*o2)
def solve_vro_o2(v1, r1, o1, v2, r2, _ ): return float(v1)*r1*o1/(v2*r2)

def solve_vrcos(v1, r1, o1, v2, r2, o2):
    if v1 == None: return solve_vro_v2(v2,r2,cos(deg2rad(o2)),None,r1,cos(deg2rad(o1)))
    if r1 == None: return solve_vro_r2(v2,r2,cos(deg2rad(o2)),v1,None,cos(deg2rad(o1)))
    if o1 == None: return rad2deg(acos(solve_vro_o2(v2,r2,cos(deg2rad(o2)),v1,r1,None)))
    if v2 == None: return solve_vro_v2(v1,r1,cos(deg2rad(o1)),None,r2,cos(deg2rad(o2)))
    if r2 == None: return solve_vro_r2(v1,r1,cos(deg2rad(o1)),v2,None,cos(deg2rad(o2)))
    if o2 == None: return rad2deg(acos(solve_vro_o2(v1,r1,cos(deg2rad(o1)),v2,r2,None)))
    return None
	
def solve_vrsin(v1, r1, o1, v2, r2, o2):
    if v1 == None: return solve_vro_v2(v2,r2,sin(deg2rad(o2)),None,r1,sin(deg2rad(o1)))
    if r1 == None: return solve_vro_r2(v2,r2,sin(deg2rad(o2)),v1,None,sin(deg2rad(o1)))
    if o1 == None: return rad2deg(asin(solve_vro_o2(v2,r2,sin(deg2rad(o2)),v1,r1,None)))
    if v2 == None: return solve_vro_v2(v1,r1,sin(deg2rad(o1)),None,r2,sin(deg2rad(o2)))
    if r2 == None: return solve_vro_r2(v1,r1,sin(deg2rad(o1)),v2,None,sin(deg2rad(o2)))
    if o2 == None: return rad2deg(asin(solve_vro_o2(v1,r1,sin(deg2rad(o1)),v2,r2,None)))
    return None

################################################################################
#
# Masses, for mass database
#
################################################################################

masses = { }

class Mass(object):
    
    def __init__(self, name, GM = 0, radius = 0, rotate = 0, orbit = None):
        self.name = name
        self.GM = float(GM)
        self.radius = float(radius)
        if rotate == "S":
            self.rotate = orbit.P;
        else:
            self.rotate = float(rotate)
        self.orbit = orbit
        if orbit != None: self.center = orbit.center
        masses[name] = self

    #--------------------------------------------------------------------------
    #
    #--------------------------------------------------------------------------
    
    @staticmethod
    def resolve(mass):
        if isinstance(mass, str): return masses[mass]
        return mass

    @staticmethod
    def rFromV(V):
        return (V / (4/3.0*pi)) ** (1/3.0)

    #--------------------------------------------------------------------------
    # Basic properties
    #--------------------------------------------------------------------------
    
    @property
    def diam(self): return self.radius*2

    @property
    def kg(self): return GM2kg(self.GM)
    
    @property
    def isMassless(self): return self.GM < kg2GM(0.1)
    
    @property
    def V(self): return 4/3.0*pi*(self.radius ** 3)

    @property
    def density(self): return self.kg / self.V

    def g(self,r): return self.GM/(r ** 2.0)

    @property
    def g_surface(self): return self.g(self.radius)

    def v_escape(self, r = None):
        if r == None:
            return v_escape(self.GM, self.radius)
        else:
            return v_escape(self.GM, r)

    def altitude(self, a): return self.radius + float(a)

    #--------------------------------------------------------------------------
    # Finding satellites
    #--------------------------------------------------------------------------
    
    def satellites(self):
        s = []
        for m in masses.values():
            if m.orbit != None and m.orbit.center == self:
                s.append(m)
        return s

    #--------------------------------------------------------------------------
    # Lagrangian distances (e.g. SOI, Sphere of Influence)
    #--------------------------------------------------------------------------
    
    def Lagrangian(self):
        return self.orbit.a*pow(self.GM/(3*self.center.GM),1/3.0)
    
    def HillSphere(self):
        return self.Lagrangian()*(1-self.orbit.e)

    def SOI(self):
        return self.orbit.a*pow(self.GM/self.center.GM, 2/5.0)

    #--------------------------------------------------------------------------
    # Radiation flux from star
    #--------------------------------------------------------------------------
    
    @property
    def flux(self):
        if not hasattr(self.orbit.center, "L"): return None
        return self.orbit.center.flux(self.orbit.altitude())
    
    #--------------------------------------------------------------------------
    # Info dump
    #--------------------------------------------------------------------------
    
    def info(self):
        print("-------------------")
        print("Name..............:", self.name)
        if not self.isMassless:
            print("Mass..............: %.4g kg (%.4g x M_earth)" % (self.kg, self.GM/GM_Earth))
            if hasattr(self, "L"):
                print("Luminosity........: %.4f x Sun" % (self.L))
                HZ = Orbit(self, self.HZ())
                print("Habitable zone....: ")
                print("    - Distance....: %.4f AU" % m2AU(HZ.a))
                print("    - Period......: %.0f d (%.1f a)" % (TtoDays(HZ.P), TtoYears(HZ.P)))
            if self.radius:
                print("Radius............: %s (%.4g x R_earth)" % (fmtdist(self.radius), self.radius/r_Earth))
                print("Volume............: %.4g m3 (%.4g x V_earth)" % (self.V, self.V/V_Earth))
                print("Density...........: %.3f kg/m3" % (self.density))
                print("Surface gravity...: %.2f g (%.2f m/s^2)" % (self.g_surface/const_g, self.g_surface))
                print("Escape velocity...: %s" % fmteng(self.v_escape(), "m/s"))
            print("Rotating period...: %s" % fmttime(self.rotate))
        if self.orbit:
            print("Orbits............:", self.orbit.center.name)
            print("   Distance.......:", fmtdist(self.orbit.a))
            print("   Period.........:", fmttime(self.orbit.P))
            print("   L1/L2 distance.:", fmtdist(self.Lagrangian()))
            print("   Hill Sphere....:", fmtdist(self.HillSphere()))
            print("   SOI............:", fmtdist(self.SOI()))
            if hasattr(self.orbit.center, "L"):
                print("   Flux...........: %.3f x Earth (%s)" % (
                    self.flux,
                    fmteng(self.flux * const_solar, "W/m2"),
                ))
        s = self.satellites()
        if len(s):
            print("Satellites........:")
            s.sort(key=lambda x: x.orbit.a)
            for num, satellite in enumerate(s):
                print("   %2d - %-20s %15s %15s %s" % (
                    num+1,
                    satellite.name,
                    fmtdist(satellite.orbit.altitude()),
                    fmttime(satellite.orbit.P),
                    hasattr(self, "L") and ("%7.3f" % satellite.flux) or "",
                ))
                    
	
################################################################################
#
# General orbit equations
#
################################################################################

def eccentricity(r1, r2):   return 1 - 2.0*min(r1, r2)/float(r1 + r2)
def solve_a(r1, r2):        return (r1 + r2)/2.0
def solve_b(r1, r2):        return solve_a(r1, r2) * sqrt(1-eccentricity(r1, r2)**2)

#------------------------------------------------------------------------------

def v_escape(GM, r):        return sqrt(2.0*GM/r)
def v_circular(GM, r):      return sqrt(GM/float(r))
def v_elliptical(GM, a, r): return sqrt(GM*(2.0/r - 1.0/a))

def P_orbit(GM, a):         return 2*pi*sqrt((a ** 3.0)/GM)
def a_from_P(GM, P):        return (P**2.0 * GM / (4*pi**2)) ** (1/3.0)

#------------------------------------------------------------------------------
# Angular velocities to solve launch window periods
#------------------------------------------------------------------------------

def w_circular(GM, a):      return 1.0/P_orbit(GM, a)
def w_diff(GM, a, b):       return 360*abs(w_circular(GM, a) - w_circular(GM, b))
def P_window(GM, a, b):     return abs(360/w_diff(GM, a, b))

################################################################################
#
# 2D vectors
#
################################################################################

class Vec2d:

    def __init__(self, x = 0, y = 0): self.set(x, y)

    def set(self, x, y): self.x, self.y = float(x), float(y)

    def __add__(self, a): return Vec2d(self.x + a.x, self.y + a.y)
    def __sub__(self, a): return Vec2d(self.x - a.x, self.y - a.y)
    def __mul__(self, a): return Vec2d(self.x * a, self.y * a)
    def __div__(self, a): return Vec2d(self.x / a, self.y / a)

    def __neg__(self): return Vec2d(-self.x, -self.y)
    def __abs__(self): return self.length

    @property
    def length2(self): return self.x**2 + self.y**2
    
    @property
    def length(self):  return sqrt(self.length2)
    
    def normalize(self): self /= self.length
    def normalized(self): return self.__div__(self.length)

    def __str__(self): return "(%f,%f)" % (self.x, self.y)

    @property
    def fr(self):
        return (
            360 * (atan2( self.y, self.x )/(2*pi) % 1),
            self.length
        )

    def rotate(self, a):
        rad = radians(a)
        return Vec2d(
            self.x * cos(rad) - self.y * sin(rad),
            self.x * sin(rad) + self.y * cos(rad)
        )

#------------------------------------------------------------------------------
#
# Determining position (x, y) at orbital ellipse(r1, r2), by normalized
# T = [0..1].
#
#   r1 = distance at T=0
#   r2 = distance at T=0.5
#
# Algorithm always positions periapsis at angle = 0.
#
#------------------------------------------------------------------------------

def pos_xy(r1, r2, T):

    if r1 > r2: T = T + 0.5
    T = T % 1.0

    e  = eccentricity(r1, r2)
    M  = 2*pi*T
    E0 = M
    E  = M + e * sin(E0)

    while abs(E0-E) > 1e-10:
        E0 = E
        E = M + e * sin(E0)

    a = solve_a(r1, r2)
    b = solve_b(r1, r2)
    p = Vec2d(
        a*(cos(E)-e),
        b*sin(E)
    )

    return (r1 > r2) and -p or p

################################################################################
#
# Basic elliptical orbits
#
################################################################################

class Orbit(object):

    #--------------------------------------------------------------------------
    #
    # Orbit elements:
    #
    #   r1  = distance at T0
    #   r2  = distance at T0 + 0.5
    #   T0  = T at r1
    #   arg = angle of r1
    #
    #--------------------------------------------------------------------------
    
    def __init__(self, center, r1, r2 = None, T0 = 0, arg = 0):
        self.set(center, r1, r2, T0, arg)

    def set(self, center, r1, r2, T0, arg):
        center = Mass.resolve(center)
        if center.isMassless:
            raise Exception("Cannot orbit massless particle.")
        self.center = center
        self.r1 = float(r1)
        self.r2 = (r2 == None) and float(r1) or float(r2)
        self.T0 = T0
        self.arg = arg

    #--------------------------------------------------------------------------
    # Basic properties
    #--------------------------------------------------------------------------

    @property
    def periapsis(self): return min(self.r1, self.r2)

    @property
    def apoapsis(self): return max(self.r1,self.r2)

    @property
    def diam(self): return self.r1 + self.r2

    @property
    def a(self): return solve_a(self.r1, self.r2)

    @property
    def b(self): return solve_b(self.r1, self.r2)

    @property
    def e(self): return eccentricity(self.r1, self.r2)

    @property
    def P(self): return P_orbit(self.center.GM, self.a)

    #--------------------------------------------------------------------------
    # Initial and final altitudes and speeds, for mission building
    #--------------------------------------------------------------------------
    
    @property
    def r_initial(self): return self.r(0.0)

    @property
    def r_final(self): return self.r(0.5)

    @property
    def v_initial(self): return self.v(0)

    @property
    def v_final(self): return self.v(0.5)

    def altitude(self, t = 0): return self.r(t) - self.center.radius

    @property
    def alt_initial(self): return self.altitude(0.0)
    
    @property
    def alt_final(self): return self.altitude(0.5)
    
    #--------------------------------------------------------------------------
    # Position (x,y) or (f,r) at given moment t = [0...1]
    #--------------------------------------------------------------------------

    def xy(self, t = 0): return pos_xy(self.r1, self.r2, t - self.T0).rotate(self.arg)
    def fr(self, t = 0): return self.xy(t).fr

    #--------------------------------------------------------------------------
    # Orbital velocity vector at given moment t = [0 ... 1]
    #--------------------------------------------------------------------------

    def v(self, t = 0):
        h = 1/self.P
        return (self.xy(t+h) - self.xy(t-h)) / 2.0

    #--------------------------------------------------------------------------
    # Orbital distance / angle at given moment t = [0 ... 1]
    #--------------------------------------------------------------------------

    def r(self, t = 0):
            f, r = self.fr(t)
            return r

    def f(self, t = 0):
            f, r = self.fr(t)
            return f

    #--------------------------------------------------------------------------

    def isReachable(self, r): return r >= self.periapsis and r <= self.apoapsis

    @property
    def isCircular(self): return abs(self.r1 - self.r2) < 1e-6 * self.r1

    @property
    def isUpwards(self): return self.r1 < self.r2

    #--------------------------------------------------------------------------
    # Solve T at given distance
    #--------------------------------------------------------------------------

    def time(self, dist):
        dist = float(dist)
        
        if not self.isReachable(dist):
            raise Exception("Distance out of orbit parameters.")

        if self.isCircular: return 0

        #----------------------------------------------------------------------
        # If orbit is upwards, distance increases from 0 ... 0.5
        # If orbit is downwards, distance decreases from 0 ... 0.5
        #----------------------------------------------------------------------
        
        if self.isUpwards:
            low, high = 0, 0.5
            while abs(low-high) > (1/self.P):
                mid = (low + high)/2
                if self.r(mid) > dist:
                        high = mid
                else:
                        low = mid
        else:
            low, high = 0, 0.5
            while abs(low-high) > (1/self.P):
                mid = (low + high)/2
                if self.r(mid) > dist:
                        low = mid
                else:
                        high = mid

        return (low + high)/2

    #--------------------------------------------------------------------------
    # Orbital velocity vector at given distance r
    #--------------------------------------------------------------------------

    def v_by_dist(self, r):
        return self.v(self.time(r))

    #--------------------------------------------------------------------------
    # Velocity difference between ellipse and circular orbit at given altitude
    #--------------------------------------------------------------------------

    def dv_circular(self, r):
        t = self.time(r)
        p = self.xy(t)
        v_circ = Vec2d(-p.y, p.x).normalized() * v_circular(self.center.GM, r)
        return self.v(t) - v_circ

    #--------------------------------------------------------------------------
    # Mean angular velocity
    #--------------------------------------------------------------------------

    def w(self): return 360.0/self.P()

    #--------------------------------------------------------------------------
    # This is used by Trajectory class below
    #--------------------------------------------------------------------------
    
    @property
    def T_to_target(self):
        if self.isCircular: return 0.0
        return 0.5

################################################################################
#
# Helper functions to create orbits
#
################################################################################

#------------------------------------------------------------------------------
# Surface "orbit", to simplify landings & takeoffs
#------------------------------------------------------------------------------

class Surface(object):
    def __init__(self, center):
        center = Mass.resolve(center)
        self.center = center

    #--------------------------------------------------------------------------
    
    @property
    def P(self): return self.center.rotate

    @property
    def a(self): return self.center.radius

    #--------------------------------------------------------------------------
    
    def r(self, t = 0.0): return self.a

    def xy(self, t = 0.0):
        return Vec2d(
            cos(2*pi*t),
            sin(2*pi*t)
        ) * self.center.radius

    def v(self, t = 0.0):
        if self.center.rotate:
            w = 2*pi/self.center.rotate
            return Vec2d(
                cos(2*pi*t),
                sin(2*pi*t)
            ).rotate(90) * w * self.center.radius
        else:
            return Vec2d(0, 0)

    #--------------------------------------------------------------------------
    
    @property
    def r_initial(self): return self.r(0.0)

    @property
    def r_final(self): return self.r(0.5)

    @property
    def v_initial(self): return self.v(0)

    @property
    def v_final(self): return self.v(0.5)

    def altitude(self, t = 0): return self.r(t) - self.center.radius

    @property
    def alt_initial(self): return self.altitude(0.0)
    
    @property
    def alt_final(self): return self.altitude(0.5)
    
    #--------------------------------------------------------------------------
    
    @property
    def T_to_target(self): return 0.0
    
#------------------------------------------------------------------------------
# Creating orbit from altitudes (adding central body radius)
#------------------------------------------------------------------------------

def Altitude(center, r1, r2 = None):
    center = Mass.resolve(center)
    if r2 == None:
        return Orbit(center, center.radius + r1)
    else:
        return Orbit(center, center.radius + r1, center.radius + r2)

#------------------------------------------------------------------------------
# Creating orbit with given period
#------------------------------------------------------------------------------

def Period(center, P, r1 = None):
    center = Mass.resolve(center)
    a = a_from_P(center.GM,P)
    if r1 == None:
        r1 = r2 = a
    else:
        r2 = 2*a - r1
    return Orbit(center, r1, r2)

#------------------------------------------------------------------------------
# Creating orbit with given eccentricity
#------------------------------------------------------------------------------

def Eccentric(center, a, e):
    return Orbit(center, a*(1-e), a*(1+e))

#------------------------------------------------------------------------------
# Creating orbit with given distance and orbital speed at that distance
#------------------------------------------------------------------------------

def OrbitRV(center, r, v):
    center = Mass.resolve(center)

    if(v >= v_escape(center.GM,r)):
        raise Exception("Apoapsis = infinite.")
            
    vc = v_circular(center.GM,r)
    a = center.GM/(2*pow(vc,2) - pow(v,2))
    return Orbit(center, r, 2*a - r)

################################################################################
#
# Trajectory is an arc of an ellipse (r1, r2), from altitude r3 to r4.
#
#   r3 = transfer initial altitude
#   r4 = transfer final altitude
#
#   r1 = ellipse periapsis (or apoapsis downwards)
#   r2 = ellipse apoapsis  (or periapsis downwards)
#
# Most often, you use Hohmann trajectories, where r3=r1 and r4=r2. But if you
# want to try faster transfers, you have an option to either lower periapsis,
# or raise apoapsis.
#
################################################################################

class Trajectory(Orbit):

    def __init__(self, center, r3, r4, r1 = None, r2 = None, T0 = 0, arg = 0):
        if r1 == None: r1 = r3
        if r2 == None: r2 = r4
        self.set(center, r1, r2, T0, arg)
        self.r3 = r3
        self.r4 = r4

    #--------------------------------------------------------------------------
    # Initial and final altitudes, for mission building
    #--------------------------------------------------------------------------

    @property
    def r_initial(self): return self.r3

    @property
    def r_final(self): return self.r4

    @property
    def v_initial(self): return self.v(self.time(self.r3))

    @property
    def v_final(self): return self.v(self.time(self.r4))

    #--------------------------------------------------------------------------
    # Solve time to reach final altitude from initial altitude: Time is
    # relative [0 ... 1] to trajectory period.
    #--------------------------------------------------------------------------

    @property
    def T_initial(self): return self.time(self.r3)
    
    @property
    def T_final(self): return self.time(self.r4)

    @property
    def T_to_target(self): return self.T_final - self.T_initial

    ###########################################################################
    #
    # Launch window calculations
    #
    ###########################################################################

    #--------------------------------------------------------------------------
    # Difference of angular speeds (degrees) at initial and final altitude
    #--------------------------------------------------------------------------

    @property
    def w_diff(self):  return w_diff(self.center.GM, self.r3, self.r4)

    #--------------------------------------------------------------------------
    # Period of launch window, based on initial and final altitudes
    #--------------------------------------------------------------------------

    @property
    def P_window(self): return P_window(self.center.GM, self.r3, self.r4)

    #--------------------------------------------------------------------------
    # Launch angles (r3 -> r4 and vice versa), so that planet at r3 is at
    # 0 degrees. Seems to be correct according to:
    #
    #	http://www-istp.gsfc.nasa.gov/stargaze/Smars3.htm
    #
    #--------------------------------------------------------------------------

    def launch_angle_up(self):
            w_r3 = self.P / P_orbit(self.center.GM, self.r3)
            w_r4 = self.P / P_orbit(self.center.GM, self.r4)
            
            t_arrival = self.time(self.r4)			# Time to arrival
            t_departure = self.time(self.r3)		# Time to departure
            t_travel = t_arrival - t_departure		# Traveling time

            f_arrival   = self.f(t_arrival)			# Angle at arrival
            f_departure = self.f(t_departure)		# Angle at departure

            f_r3_at_departure = f_departure
            f_r4_at_departure = f_arrival - 360*w_r4*t_travel
            
            return -(f_r4_at_departure - f_r3_at_departure)

    def launch_angle_down(self):
            w_r3 = self.P / P_orbit(self.center.GM, self.r3)
            w_r4 = self.P / P_orbit(self.center.GM, self.r4)
            
            t_arrival   = 1.0 - self.time(self.r3)	# Time to arrival
            t_departure = 1.0 - self.time(self.r4)	# Time to departure
            t_travel = t_arrival - t_departure		# Traveling time

            f_departure = self.f(t_departure)		# Angle at departure
            f_arrival   = self.f(t_arrival)			# Angle at arrival

            f_r3_at_departure = f_arrival - 360*w_r3*t_travel
            f_r4_at_departure = f_departure

            return -(f_r4_at_departure - f_r3_at_departure)

    def launch_angle(self): return self.launch_angle_up()

    ###########################################################################
    #
    # Delta-v required to enter and exit to trajectory
    #
    ###########################################################################

    @property
    def dv_enter(self): return abs(self.dv_circular(self.r3))

    @property
    def dv_exit(self):  return abs(self.dv_circular(self.r4))

    @property
    def dv_total(self): return self.dv_enter + self.dv_exit

    #--------------------------------------------------------------------------
    # Computational dv for Hohmann transfer (r3 - r4)
    #--------------------------------------------------------------------------

    @property
    def hohmann_P(self):
        a = solve_a(self.r3, self.r4)
        return P_orbit(self.center.GM, a) / 2        

    @property
    def hohmann_dv_enter(self):
        a = solve_a(self.r3, self.r4)
        return abs(v_elliptical(self.center.GM, a, self.r3) - v_circular(self.center.GM, self.r3))
            
    @property
    def hohmann_dv_exit(self):
        a = solve_a(self.r3, self.r4)
        return abs(v_elliptical(self.center.GM, a, self.r4) - v_circular(self.center.GM, self.r4))
            
    @property
    def hohmann_dv_total(self):
        return self.hohmann_dv_enter + self.hohmann_dv_exit

