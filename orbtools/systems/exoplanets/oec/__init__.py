################################################################################
#
# Exoplanets imported from Open Exoplanet Catalog, see:
#
# https://github.com/OpenExoplanetCatalogue/oec_gzip/
#
################################################################################

from orbtools import *
from orbtools.systems.exoplanets.oec.fixes import fixes

#-------------------------------------------------------------------------------
# Use fixes table to do data fixes
#-------------------------------------------------------------------------------

verbose = False      # True/false if you want reports when reading catalogue
verbosefix = False   # True/false if you want to see what values are changed

def doFix(data):

  name = data["name"]

  def fix(field, value, current):
    if verbosefix:
      if current:
        print("- Fix: %-20s %s = %s --> %s" % (name, field, current, value))
      else:
        print("- Add: %-20s %s = %s" % (name, field, value))
    return value

  if name not in fixes: return

  for field, value in fixes[name].items():
    data[field] = fix(field, value, data[field])

################################################################################
#
# Filling in data from XML file
#
################################################################################

def doPlanet(planet, star):

  data = {
    "name": planet.findtext("name"),
    "detection_type": planet.findtext("discoverymethod"),
    #"discovered": row[5],
    "orbital_period": planet.findtext("period"),
    "semi_major_axis": planet.findtext("semimajoraxis"),
    "radius": planet.findtext("radius"),
    "mass": planet.findtext("mass"),
    "T": planet.findtext("temperature"),
    "status": "Confirmed",
  }

  name = data["name"]

  if not name: return
  if name in masses: return

  incomplete = name in fixes and fixes[name] is None

  mass = data["mass"]
  radius =  data["radius"]
  T =  data["T"]
  detection = data["detection_type"]

  # Make orbit: We prefer period, as it is commonly more reliable than
  # semi-major axis.

  P = data["orbital_period"]
  A = data["semi_major_axis"]

  if P:
    orbit = byPeriod(star, float(TasDays(P)))
  elif A:
    orbit = Orbit(star, float(AU2m(A)))
  else:
    if verbose and not incomplete: print(name, "No orbit")
    return None

  GM     = mass and MasJupiter(mass) or 0
  radius = radius and RasJupiter(radius) or None

  p = Planet(name, GM = GM, radius = radius, orbit = orbit)

  p.T = T and float(T) or None
  p.detection = detection or None

#------------------------------------------------------------------------------

def doStar(star, dist):

  data = {
    "name": star.findtext("name"),
    "sp_type": star.findtext("spectraltype"),
    "T": star.findtext("temperature"),
    "radius": star.findtext("radius"),
    "mass": star.findtext("mass"),
    "L": "",
    "distance": dist
  }

  name = data["name"]
  if not name: return
  if name in masses: return

  incomplete = name in fixes and fixes[name] is None

  if not incomplete: doFix(data)

  sptype = data["sp_type"]
  mass = data["mass"]
  radius = data["radius"]

  planets = star.findall(".//planet")

  # Stars without mass are excluded: it is not possible to make orbits
  # around them.

  if not mass:
    if verbose and not incomplete and len(planets): print(name, "# Massless, planets", len(planets))
    return

  def doStarL(L, T, RxSun):
    if(L): return float(L)
    if(RxSun and T): return Star.TtoL(float(T), RasSun(RxSun))
    return None

  T = data["T"]
  L = doStarL(data["L"], T, radius)

  # Warn if star has planets, but its luminosity can't be determined; add star
  # and planets anyways.

  if (not L):
    if verbose and not incomplete and len(planets): print(name, "# Fluxless, planets:", len(planets))

  s = Star(
    name,
    sptype = sptype,
    MxSun = mass,
    RxSun = radius,
    T = T,
    L = L,
    dist = dist
  )

  for planet in planets:
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
