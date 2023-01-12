###############################################################################
#
# Data filters
#
###############################################################################

from orbtools import *

def doFilters(data, *filters):
  def recurse(data, filters):
    return len(filters) and filter(filters[-1], doFilters(data, *filters[:-1])) or data
  return list(recurse(data, filters))

def isStar(mass): return mass.type == "star"

def isPlanet(mass): return mass.type == "planet"

def hasMass(mass):
  if not mass.GM: return False
  if GM2kg(mass.GM) < 1: return False
  return True

def hasRadius(mass):
  if not mass.radius: return False
  if mass.radius < 1.0: return False
  return True

def hasLuminosity(mass):
  return hasattr(mass, "L") and mass.L

def hasTemperature(mass):
  return hasattr(mass, "T") and mass.T

def hasMagnitude(mass):
  return hasattr(mass, "mag") and mass.mag

def hasFlux(planet):
  return not planet.flux is None

def hasPeriod(mass):
  return not mass.orbit is None

def isExoplanet(mass):
  if mass.type != "planet": return False
  if mass.system.name == "Sun": return False
  return True

def isJovian(planet):
  return planet.GM > MasJupiter(0.2) and planet.GM < MasJupiter(78)

def isNotJovian(planet):
  return planet.GM < MasJupiter(0.2)

def isUltraDense(planet):
  return planet.density > 10000

def isSuperEarth(planet):
  return planet.GM < MasEarth(15)

def isRocky(planet):
  # Densities over 10000 kg/m3 on small planets are probably incertainties in
  # physical parameters
  return planet.density > 5000 and planet.density < 10000

def isHot(planet):
  if not planet.flux: return False
  return planet.flux > 2.5

def isCold(planet):
  if not planet.flux: return False
  return planet.flux < flux_FrostLine

def isInHZ(planet):
  #if not FilterPlanet(planet): return False
  if not planet.flux: return False
  if isHot(planet): return False
  if isCold(planet): return False
  return True

def isSpectralClass(star, *sptypes): return star.sptype and star.sptype[:1] in sptypes
def isSpectralType(star, sptype): return star.sptype and star.sptype[:len(sptype)] == sptype

