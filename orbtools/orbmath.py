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
      return (a1 ** 3.0) * (p2 ** 2.0) / (p1 ** (2.0/3.0))

  def solve_P_aPaP(a1, p1, a2, _):
      return (p1 ** 2.0) * (a2 ** 3.0) / (a1 ** (3.0/2.0))

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

  def __init__(self, name = None, GM = 0, radius = 0, rotate = 0, orbit = None):
    self.name = name
    self.GM = float(GM)
    self.radius = radius and float(radius) or None
    if rotate == "S":
      self.rotate = orbit.P;
    else:
      self.rotate = float(rotate)
    self.orbit = orbit

    if name:
      assert name not in masses, "Mass '%s' already exists." % name
      masses[name] = self

    self.hasSatellites = False

  @staticmethod
  def fromGM(GM): return Mass(GM = GM)

  @staticmethod
  def fromKg(kg): return Mass(GM = kg2GM(kg))

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
  def V(self): return V_sphere(self.radius)
  #def V(self): return 4/3.0*pi*(self.radius ** 3)

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

  def v_circular(self, r):
    return v_circular(self.GM, r)

  def altitude(self, a): return self.radius + float(a)

  #--------------------------------------------------------------------------
  # Orbital parameters
  #--------------------------------------------------------------------------

  @property
  def center(self):
    if not self.orbit: return None
    return self.orbit.center

  @property
  def a(self):
    return self.orbit and self.orbit.a or None

  @property
  def v(self):
    return self.orbit and self.orbit.v(0) or None

  @property
  def P(self):
    return self.orbit and self.orbit.P or None

  #--------------------------------------------------------------------------
  # Finding satellites
  #--------------------------------------------------------------------------

  #@property
  #def hasSatellites(self):
  #  return any(True for _ in self.satellites)

  @property
  def satellites(self):
    return list(filter(lambda m: m.orbit != None and m.orbit.center == self, masses.values()))

  #--------------------------------------------------------------------------
  # Finding system
  #--------------------------------------------------------------------------

  @property
  def system(self):
    if not self.orbit: return self
    return self.orbit.center.system

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
  # Radiation flux (x Earth) from star
  #--------------------------------------------------------------------------

  @property
  def flux(self):
    if not self.center: return None
    if not hasattr(self.center, "fluxAt"): return self.center.flux
    return self.center.fluxAt(self.orbit.a)

  #@property
  #def fluxToT(self):
  #  if not self.flux: return None
  #  return Star.fluxToT(self.flux)

  #def fluxToTeff(self, albedo):
  #  if not self.flux: return None
  #  return Star.fluxToTeff(self.flux, albedo)

  #--------------------------------------------------------------------------
  # Info dump
  #--------------------------------------------------------------------------

  def info(self):
    print("-------------------")
    print("Name..............:", self.name)
    if not self.isMassless:
      print("Mass..............: %s" % (fmtmass(self.kg)))
    if self.type == "star":
      print("Spectral type.....: %s" % self.sptype)
      print("Temperature.......:", self.T and "%.0f K" % self.T or "N/A")
      print("Distance..........:", self.dist and "%.2f ly" % m2ly(self.dist) or "N/A")
      if self.L:
        print("Luminosity........: %.5f x Sun" % (self.L))
        HZ = Orbit(self, self.HZ())
        print("Habitable zone....: ")
        print("    - Distance....: %.4f AU" % m2AU(HZ.a))
        print("    - Period......: %.0f d (%.1f a)" % (TtoDays(HZ.P), TtoYears(HZ.P)))
    if not self.radius is None:
      if self.type == "star":
        print("Radius............: %s (%.4g x R_sun)" % (fmtdist(self.radius), self.radius/r_Sun))
        print("Volume............: %.4g m3 (%.4g x V_sun)" % (self.V, self.V/V_Sun))
      else:
        print("Radius............: %s (%.4g x R_earth)" % (fmtdist(self.radius), self.radius/r_Earth))
        print("Volume............: %.4g m3 (%.4g x V_earth)" % (self.V, self.V/V_Earth))
      print("Density...........: %.3f kg/m3" % (self.density))
      print("Surface gravity...: %.2f g (%.2f m/s^2)" % (self.g_surface/const_g, self.g_surface))
      print("Escape velocity...: %s" % fmteng(self.v_escape(), "m/s"))
    print("Rotating period...: %s" % fmttime(self.rotate))
    if self.orbit:
      print("Orbits............:", self.center.name)
      print("   Distance.......:", fmtdist(self.a))
      print("   Period.........:", fmttime(self.P))
      print("   Flux...........: %.3f x Earth (%s)" % (
          self.flux,
          fmteng(self.flux * const_solar, "W/m2"),
      ))
      #print("   L1/L2 distance.:", fmtdist(self.Lagrangian()))
      #print("   Hill Sphere....:", fmtdist(self.HillSphere()))
      #print("   SOI............:", fmtdist(self.SOI()))
    if self.hasSatellites:
      s = self.satellites
      s.sort(key=lambda x: x.orbit.a)

      print("Satellites........:")

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

  def normalize(self, l = 1.0): self *= l / self.length
  def normalized(self, l = 1.0): return self.__mul__(l / self.length)

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

  def __init__(self, center, r1, r2 = None, arg=None):
    r2 = r2 == None and r1 or r2
    assert r1 > 0
    assert r2 > 0
    center = Mass.resolve(center)
    assert not center.isMassless, "Cannot orbit massless object"
    self.center = center
    self.r1  = float(r1)            # Periapsis
    self.r2  = float(r2)            # Apoapsis
    self.arg = arg and arg or 0.0   # Argument of periapsis

    center.hasSatellites = True

  #--------------------------------------------------------------------------
  # Basic properties
  #--------------------------------------------------------------------------

  @property
  def periapsis(self): return min(self.r1, self.r2)

  @property
  def apoapsis(self): return max(self.r1, self.r2)

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
  # Synodic period to given orbit
  #--------------------------------------------------------------------------

  def P_synodic(self, B):
      A, B = self.P, B.P
      return abs((A * B) / float(A - B))

  #--------------------------------------------------------------------------
  # Position (x,y) or (f,r) at given moment t = [0...1]
  #--------------------------------------------------------------------------

  def xy(self, t = 0):
      return pos_xy(self.r1, self.r2, t).rotate(self.arg)

  #--------------------------------------------------------------------------
  # Orbital distance / angle at given moment t = [0 ... 1]
  #--------------------------------------------------------------------------

  def fr(self, t = 0): return self.xy(t).fr

  def r(self, t = 0):
          f, r = self.fr(t)
          return r

  def f(self, t = 0):
          f, r = self.fr(t)
          return f

  def altitude(self, t = 0): return self.r(t) - self.center.radius

  #--------------------------------------------------------------------------
  # Orbital velocity vector at given moment t = [0 ... 1]
  #--------------------------------------------------------------------------

  def v(self, t = 0):
    l = v_elliptical(self.center.GM, self.a, self.r(t))
    h = 1e-6
    #return Vec2d.__div__(self.xy(t+h) - self.xy(t-h), 2.0 * (h * self.P))
    return (self.xy(t+h) - self.xy(t-h)).normalized(l)

  def v_escape(self, t = 0):
      return self.center.v_escape(self.r(t))

  def v_circular(self, t = 0):
      return self.center.v_circular(self.r(t))

  #--------------------------------------------------------------------------
  # Orbital energy: E = Ekin - Epot
  #--------------------------------------------------------------------------

  def Epot(self, t = 0): return -self.center.GM/self.r(t)

  def Ekin(self, t = 0): return solve_Emv(None, 1.0, abs(self.v(t)))

  def E(self, t = 0): return self.Ekin(t) + self.Epot(t)

  #--------------------------------------------------------------------------
  # C3, characteristic energy for interplanetary exit & entry trajectories
  #--------------------------------------------------------------------------

  def C3(self, v, t = 0):
      return solve_rvrv(self.center.GM, self.r(t), None, Inf, v)

  #--------------------------------------------------------------------------
  # Orbit info dump
  #--------------------------------------------------------------------------

  def info(self):

      def info_by_t(t, prefix=""):
          r, v = (self.r(t), abs(self.v(t)))
          E, Ekin, Epot = (self.E(t), self.Ekin(t), self.Epot(t))

          print(prefix + "- r.....:", fmtdist(r), "alt:", fmtdist(r - self.center.radius))
          print(prefix + "- v.....: %.2f m/s" % v)
          print(prefix + "- E.....:", fmteng(E, "J"), "(%s %s)" % (fmteng(Ekin, "J"), fmteng(Epot, "J")))

      print("Orbit")

      print("- Center:", self.center.name)
      print("- A.....:", fmtdist(self.a))
      print("- P.....:", fmttime(self.P))

      # Circular orbits
      if(self.r1 == self.r2):
          info_by_t(0.0)
      # Elliptical orbits
      else:
          print("- Periapsis")
          info_by_t(0.0, "  ")
          print("- Apoapsis")
          info_by_t(0.5, "  ")

#------------------------------------------------------------------------------
# Surface "orbit", to simplify landings & takeoffs
#------------------------------------------------------------------------------

class Surface(Orbit):

    def __init__(self, center, arg = None):
        center = Mass.resolve(center)
        self.center = center
        self.r1 = center.radius
        self.r2 = center.radius
        self.arg = arg and arg or 0.0

    #--------------------------------------------------------------------------

    @property
    def P(self): return self.center.rotate

    @property
    def a(self): return self.center.radius

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

#------------------------------------------------------------------------------
# Creating orbit from altitudes (adding central body radius)
#------------------------------------------------------------------------------

def byAltitude(center, r1, r2 = None, arg=None):
    center = Mass.resolve(center)

    if r2 == None:
        return Orbit(center, center.radius + r1, arg)
    else:
        return Orbit(center, center.radius + r1, center.radius + r2, arg)

#------------------------------------------------------------------------------
# Creating orbit with given period
#------------------------------------------------------------------------------

def byPeriod(center, P, r1 = None):
    center = Mass.resolve(center)

    a = a_from_P(center.GM, P)
    if r1 == None:
        r1 = r2 = a
    else:
        r2 = 2*a - r1

    return Orbit(center, r1, r2)

#------------------------------------------------------------------------------
# Creating orbit with given eccentricity
#------------------------------------------------------------------------------

def byEccentricity(center, a, e):
    return Orbit(center, a*(1-e), a*(1+e))

#------------------------------------------------------------------------------
# Creating orbit with given distance and orbital speed at that distance
#------------------------------------------------------------------------------

def byRV(center, r, v):
  center = Mass.resolve(center)
  GM = center.GM

  #print(r, v)

  vesc = v_escape(GM, r)
  vc = v_circular(GM, r)
  #print(vc, vesc)

  assert v < vesc, "Apoapsis = infinite"

  a = GM*r / (2*GM - r*(v**2))

  return Orbit(center, r, 2*a - r)


################################################################################
#
# Trajectory
#
################################################################################

#------------------------------------------------------------------------------
# Let's think this better this time. Trajectory is path in any orbit. It
# has its own parameters, like the point where we entered the orbit, and
# when we leave
#------------------------------------------------------------------------------

class Trajectory:

    def __init__(self):
        pass

