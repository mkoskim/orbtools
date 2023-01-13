################################################################################
#
# Exoplanets imported from Open Exoplanet Catalog, see:
#
# https://github.com/OpenExoplanetCatalogue/oec_gzip/
#
################################################################################

from orbtools import *

#------------------------------------------------------------------------------

def doPlanet(planet, star):
  name = planet.findtext("name")

  if not name: return
  if name in masses: return

  mass = planet.findtext("mass")

  radius = planet.findtext("radius") or None

  P = planet.findtext("period")
  A = planet.findtext("semimajoraxis")

  if P:
    orbit = byPeriod(star, float(TasDays(P)))
  elif A:
    orbit = Orbit(star, float(AU2m(A)))
  else:
    return None

  #if not radius or not orbit: print("Planet:", name, mass, radius, P, A)

  # Allow massless planets
  # if not mass: return

  p = Planet(name, GM = mass and MasJupiter(mass) or 0, radius = radius and RasJupiter(radius), orbit = orbit)

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
  magV = star.findtext("magV") or None

  #if not radius or not T: print("Star:", name, sptype, mass, radius, T)

  if not mass: return
  #if sptype is None: return
  #if sptype[0] not in ["F", "G", "K", "M"]: return

  s = Star(name, MxSun = mass, RxSun = radius, sptype = sptype, T = T, magV = magV, dist = dist)

  for planet in star.findall(".//planet"):
    doPlanet(planet, s)

#------------------------------------------------------------------------------

def doSystem(system):
  dist = system.findtext("distance")
  if dist: dist = parsec2m(dist)

  for star in system.findall(".//star"):
    doStar(star, dist)

#------------------------------------------------------------------------------

#import xml.etree.ElementTree as ET, urllib.request, gzip, io
#url = "https://github.com/OpenExoplanetCatalogue/oec_gzip/raw/master/systems.xml.gz"
#oec = ET.parse(gzip.GzipFile(fileobj=io.BytesIO(urllib.request.urlopen(url).read()))).getroot()

import xml.etree.ElementTree as ET, gzip
oec = ET.fromstring(open("./orbtools/systems/exoplanets/oec/systems.xml").read())

for system in oec: doSystem(system)

from orbtools.systems.exoplanets.oec.fixes import doFixes
doFixes(quiet = True)
#exit()
