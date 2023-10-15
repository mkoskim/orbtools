################################################################################
#
# Exoplanets imported from Open Exoplanet Catalog, see:
#
# https://github.com/OpenExoplanetCatalogue/oec_gzip/
#
################################################################################

from orbtools import *

################################################################################
#
# Filling in data from XML file
#
################################################################################

def doPlanet(planet, star):
  name = planet.findtext("name")

  if not name: return
  if name in masses: return

  mass = planet.findtext("mass")
  radius = planet.findtext("radius") or None
  T = planet.findtext("temperature") or None
  detection = planet.findtext("discoverymethod") or None

  P = planet.findtext("period")
  A = planet.findtext("semimajoraxis")

  if P:
    orbit = byPeriod(star, float(TasDays(P)))
  elif A:
    orbit = Orbit(star, float(AU2m(A)))
  else:
    return None

  GM     = mass and MasJupiter(mass) or 0
  radius = radius and RasJupiter(radius) or None

  p = Planet(name, GM = GM, radius = radius, orbit = orbit)

  p.elem = planet
  p.T = T and float(T) or None
  p.detection = detection or None

#------------------------------------------------------------------------------

def doStar(star, dist):
  name = star.findtext("name")
  if not name: return
  if name in masses: return
  if name == "Sun": return

  sptype = star.findtext("spectraltype") or None
  mass = star.findtext("mass") or None
  radius = star.findtext("radius") or None
  T = star.findtext("temperature") or None

  #if dist:
  #  mag = star.findtext("magV")
  #  if mag: mag = Star.magVtoAbs(float(mag), dist)
  #else:
  #  mag = None

  #if not radius or not T: print("Star:", name, sptype, mass, radius, T)

  if not mass: return

  #if sptype is None: return
  #if sptype[0] not in ["F", "G", "K", "M"]: return

  s = Star(name, MxSun = mass, RxSun = radius, sptype = sptype, T = T, dist = dist)

  s.elem = star

  for planet in star.findall(".//planet"):
    doPlanet(planet, s)

#------------------------------------------------------------------------------

def doSystem(system):
  dist = system.findtext("distance")
  if dist:
    dist = parsec2m(dist)

  for star in system.findall(".//star"):
    doStar(star, dist)

#------------------------------------------------------------------------------

#import xml.etree.ElementTree as ET, urllib.request, gzip, io
#url = "https://github.com/OpenExoplanetCatalogue/oec_gzip/raw/master/systems.xml.gz"
#oec = ET.parse(gzip.GzipFile(fileobj=io.BytesIO(urllib.request.urlopen(url).read()))).getroot()

import xml.etree.ElementTree as ET, gzip
oec = ET.fromstring(open("./orbtools/systems/exoplanets/oec/systems.xml").read())

for system in oec: doSystem(system)

################################################################################
#
# Running fixes (fix some missing / incorrect data)
#
################################################################################

from orbtools.systems.exoplanets.oec.fixes import doFixes
doFixes(quiet = True)
#doFixes(quiet = False)
#exit()

################################################################################
#
# Adding data from equations (not used atm) - after fixes!
#
################################################################################

from orbtools.systems.exoplanets.filters import *
from scipy.interpolate import LinearNDInterpolator
#import numpy as np

#------------------------------------------------------------------------------
# Fill in luminosity from temperature and radius

def doRTtoL():
  starsWOL = doFilters(stars.values(), lambda x: not hasLuminosity(x), hasRadius, hasTemperature)

  for star in starsWOL:
    star.L = Star.TtoL(star.T, star.radius)

#------------------------------------------------------------------------------
# Use stars with mass, temperature and luminosity to interpolate luminosities
# to stars without radius. Sadly, this is not as effective as it sounds. We
# need to wait scientists to fill up masses and temperatures for stars with
# planets.

def doInterpolateL():

  #----------------------------------------------------------------------------
  # Make 2D interpolation from computed L

  starsL = doFilters(stars.values(), hasLuminosity)

  points = [(MtoSun(star.GM), star.T) for star in starsL]
  values = [star.L for star in starsL]

  interp = LinearNDInterpolator(points, values)

  #----------------------------------------------------------------------------
  # Stars with T but without L yet

  starsMT = doFilters(stars.values(), hasTemperature, lambda x: not hasLuminosity(x))
  print("MT:", len(starsMT))

  #for star in starsMT:
  #  print(star.name)

  for star in starsMT: star.L = interp(MtoSun(star.GM), star.T)

doRTtoL()
#doInterpolateL()

#exit()
