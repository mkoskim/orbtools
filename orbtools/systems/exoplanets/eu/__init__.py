################################################################################
#
# Exoplanets imported from EU Exoplanet Catalog, see:
#
# https://exoplanet.eu/catalog/#downloads-section
#
################################################################################

from orbtools import *

from orbtools.systems.exoplanets.eu.eu import getRows, extractRow, fixes
#from orbtools.systems.exoplanets.eu.nasa import getRows, extractRow, fixes

#-------------------------------------------------------------------------------
# Use fixes table to do data fixes
#-------------------------------------------------------------------------------

def doFix(data, verbose = False):

  name = data["name"]

  def fix(field, value, current):
    #if not quiet and current: print("Fix: %-20s %s = %s --> %s" % (name, field, current, value))
    #if verbose: print("Fix: %s %s = %s --> %s" % (name, field, current, value))
    return value

  if name not in fixes: return
  fields = fixes[name]

  for field, value in fields.items():
    data[field] = fix(field, value, data[field])

#-------------------------------------------------------------------------------
# Process CSV row
#-------------------------------------------------------------------------------

def createPlanet(planet_data, star_data, verbose = True):

  #print(row)

  #-----------------------------------------------------------------------------
  # Extract planet data
  #-----------------------------------------------------------------------------

  #-----------------------------------------------------------------------------
  # Find/create star
  #-----------------------------------------------------------------------------

  def doStarMR(mass, radius):
    return (
      mass and float(mass) or 0,
      radius and float(radius) or None
    )

  def doStarL(L, T, RxSun):
    if(L): return float(L)
    if(RxSun and T): return Star.TtoL(float(T), RasSun(RxSun))
    return None

  def doStar(name, MxSun, RxSun):
    #print(MxSun, RxSun)

    dist   = star_data["distance"]
    sptype = star_data["sp_type"]
    T      = star_data["T"]
    L      = star_data["L"]
    #print(L)

    #print(name, sptype, mass, radius, T, dist)

    return Star(name,
      MxSun = MxSun,
      RxSun = RxSun,
      sptype = sptype,
      T = T,
      L = doStarL(L, T, RxSun),
      dist = dist and parsec2m(dist) or None
    )

  #-----------------------------------------------------------------------------
  # Find/create planet
  #-----------------------------------------------------------------------------

  def doPlanetOrbit(star, P, a):
    P = P and TasDays(P) or None
    a = a and AU2m(a) or None

    if P: return byPeriod(star, P)
    if a: return Orbit(star, a)
    return None

  def doPlanetMR(mass, radius):
    return (
      mass and MasJupiter(mass) or 0,
      radius and RasJupiter(radius) or None,
    )

  def doPlanet(star):
    #print(planet_data)
    #star.info()

    name = planet_data["name"]

    if name in masses:
      if verbose: print("Skipping:", name, "- duplicate")
      return

    #if not star.L:
    #  if verbose: print("Fluxless:", name, "@", star.name)

    doFix(planet_data, verbose)

    orbit = doPlanetOrbit(star, planet_data["orbital_period"], planet_data["semi_major_axis"])

    if not orbit:
      if verbose: print("Skipping:", name, "- no orbital parameters")
      return

    #print(TtoDays(orbit.P))
    #print(m2AU(orbit.a))

    GM, radius = doPlanetMR(planet_data["mass"], planet_data["radius"])

    planet = Planet(name, GM = GM, radius = radius, orbit = orbit)

    T = planet_data["T"]
    detection = planet_data["detection_type"]

    planet.T = T and float(T) or None
    planet.detection = detection or None

    return planet

  #-----------------------------------------------------------------------------
  # Add a planet
  #-----------------------------------------------------------------------------

  star_name = star_data["name"]
  planet_name = planet_data["name"]

  if(not star_name):
    #if verbose: print("Unfixable", planet_data["name"], "# nameless host star")
    return

  if(star_name in fixes and fixes[star_name] is None):
    #if verbose: print("Unfixable", star_name)
    return

  if(not planet_name):
    #if verbose: print("Unfixable:", planet_data["name"], "# nameless planet")
    return

  if(planet_data["status"] != "Confirmed"):
    if verbose: print("Skipping:", planet_name, "- not confirmed")
    return

  if(planet_name in fixes and fixes[planet_name] is None):
    #if verbose: print("Unfixable", planet_name)
    return

  if star_name in stars:
    star = stars[star_name]
  else:
    doFix(star_data, verbose)

    MxSun, RxSun = doStarMR(star_data["mass"], star_data["radius"])

    if not MxSun:
      if verbose: print("Skipping:", planet_data["name"], "@", star_data["name"], "- massless star")
      return

    star = doStar(star_name, MxSun, RxSun)

  planet = doPlanet(star)

  #star.info()
  #planet.info()

  #exit()

  #print(star_data["name"], ":", planet_data["name"], ":", star_data["alternate_names"])

rows = getRows()

print("Planets (total):", len(rows))
for row in rows[1:]:
  planet_data, star_data = extractRow(row)
  #print(planet_data, star_data)
  createPlanet(planet_data, star_data)

def starInfo(name):
  star = stars[name]

  print("Star:")
  print("- Name...:", name)
  print("- SP.....:", star.sptype)
  print("- Mass...:", star.GM and ("%.2f" % MtoSun(star.GM)) or None)
  print("- Radius.:", star.radius and ("%.2f" % RtoSun(star.radius)) or None)
  print("- T......:", star.T and ("%.2f" % star.T) or None)
  print("- L......:", star.L and ("%.2f" % star.L) or None)

  if star.radius and star.T:
    print("- L(calc): %.2f" % Star.TtoL(star.T, star.radius))

#starInfo("HD 96700")

#exit()
