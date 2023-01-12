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
    orbit = None

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
oec = ET.fromstring(open("./orbtools/systems/catalogs/systems.xml").read())

for system in oec: doSystem(system)

#------------------------------------------------------------------------------
# Fixes for data in catalogue (2023/01/11)
#------------------------------------------------------------------------------

stars["HD 80869"].T = 5837 # Fix: 58
planets["HD 110113 b"].GM = MasEarth(4.55) # Fix: 1446.12

#------------------------------------------------------------------------------
# Some missing data in catalogue (2023/01/11)
#------------------------------------------------------------------------------

stars["Rigel A"].T = 12100
stars["Betelgeuse"].T = 3600

#------------------------------------------------------------------------------

#stars["16 Cygni C"].radius =
#stars["16 Cygni C"].T =
#stars["16 Cygni C"].L =

stars["61 Cygni A"].radius = RasSun(0.665)
stars["61 Cygni A"].T = 4526
stars["61 Cygni A"].L = 0.095

stars["61 Cygni B"].radius = RasSun(0.595)
stars["61 Cygni B"].T = 4077
stars["61 Cygni B"].L = 0.085

stars["GJ 163"].radius = RasSun(0.409)
stars["GJ 163"].T = 3460
stars["GJ 163"].L = 0.02163

stars["GJ 180"].radius = RasSun(0.4229)
stars["GJ 180"].T = 3634
stars["GJ 180"].L = 0.02427

#stars["GJ 2056"].radius = RasSun(0.6715)
#stars["GJ 2056"].T =
#stars["GJ 2056"].L =

stars["GJ 229"].radius = RasSun(0.69)
stars["GJ 229"].T = 3700
stars["GJ 229"].L = 0.0430

stars["GJ 27.1"].radius = RasSun(0.5188870)
stars["GJ 27.1"].T = 3687.0
stars["GJ 27.1"].L = Star.LasLog10(-1.34847)

stars["GJ 3082"].radius = RasSun(0.4652160)
stars["GJ 3082"].T = 3910.0
stars["GJ 3082"].L = Star.LasLog10(-1.46273)

stars["GJ 3090"].sptype = "M2V"

stars["GJ 317"].radius = RasSun(0.4170)
stars["GJ 317"].T = 3510
stars["GJ 317"].L = 0.02175

stars["GJ 433"].radius = RasSun(0.529)
stars["GJ 433"].T = 3445
stars["GJ 433"].L = 0.034

stars["GJ 687"].radius = RasSun(0.492)
stars["GJ 687"].T = 3095
stars["GJ 687"].L = 0.0213

stars["GJ 9066"].radius = RasSun(0.164)
stars["GJ 9066"].T = 3154
stars["GJ 9066"].L = Star.LasLog10(-2.60)

stars["GJ 96"].radius = RasSun(0.5806120)
stars["GJ 96"].T = 3782.0
stars["GJ 96"].L = Star.LasLog10(-1.20665)

stars["Gliese 1002"].radius = RasSun(0.137)
stars["Gliese 1002"].T = 3024
stars["Gliese 1002"].L = 0.001406
Mass("Gliese 1002 a", MasEarth(1.08), orbit = Orbit("Gliese 1002", AU2m(0.0457)))
Mass("Gliese 1002 b", MasEarth(1.36), orbit = Orbit("Gliese 1002", AU2m(0.0738)))

stars["Gliese 221"].radius = RasSun(0.613)
stars["Gliese 221"].T = 4324
stars["Gliese 221"].L = 0.001406

#stars["Gliese 328"].radius = RasSun(?)
stars["Gliese 328"].T = 3989
stars["Gliese 328"].L = 0.10

stars["Gliese 649"].radius = RasSun(0.531)
stars["Gliese 649"].T = 3621
stars["Gliese 649"].L = 0.04373

stars["Gliese 674"].radius = RasSun(0.361)
stars["Gliese 674"].T = 3404
stars["Gliese 674"].L = 0.01575

stars["Gliese 676 A"].radius = RasSun(0.617)
stars["Gliese 676 A"].T = 4014
stars["Gliese 676 A"].L = 0.08892

#stars["HD 158259"].radius = RasSun(0.617)
stars["HD 158259"].T = 6068
stars["HD 158259"].L = 1.6

stars["HD 159868"].radius = RasSun(1.97)
stars["HD 159868"].T = 5558
stars["HD 159868"].L = 3.59

#stars["HD 163296"].radius = RasSun()
#stars["HD 163296"].T =
#stars["HD 163296"].L =

stars["HD 181433"].radius = RasSun(0.8108410)
stars["HD 181433"].T = 4929.630
stars["HD 181433"].L = Star.LasLog10(-0.4561762)

stars["HD 204313"].radius = RasSun(1.08)
stars["HD 204313"].T = 5783
stars["HD 204313"].L = 1.18

stars["HD 20794"].radius = RasSun(0.92)
stars["HD 20794"].T = 5401
stars["HD 20794"].L = 0.74

stars["HD 40307"].radius = RasSun(0.716)
stars["HD 40307"].T = 4977
stars["HD 40307"].L = 0.23

stars["K2-16"].radius = RasSun(0.703181)
stars["K2-16"].T = 4627.07
stars["K2-16"].L = Star.LasLog10(-0.689946)

stars["K2-165"].radius = RasSun(0.8376060)
stars["K2-165"].T = 5141.6700
stars["K2-165"].L = Star.LasLog10(-0.3548089)

stars["K2-183"].radius = RasSun(0.87)
stars["K2-183"].T = 5482
stars["K2-183"].L = Star.LasLog10(-0.1317863)

stars["K2-187"].radius = RasSun(0.894913)
stars["K2-187"].T = 5477
stars["K2-187"].L = Star.LasLog10(-0.1960678)

stars["K2-219"].radius = RasSun(1.2561700)
stars["K2-219"].T = 5712.000
stars["K2-219"].L = Star.LasLog10(0.17994742)

stars["K2-32"].radius = RasSun(0.233767)
stars["K2-32"].T = 3190.0
stars["K2-32"].L = Star.LasLog10(-2.2926)

stars["K2-58"].radius = RasSun(0.8364240)
stars["K2-58"].T = 5020.000
stars["K2-58"].L = Star.LasLog10(-0.3976375)

stars["K2-80"].radius = RasSun(0.8680660)
stars["K2-80"].T = 5203.000
stars["K2-80"].L = Star.LasLog10(-0.3031848)

#stars["Kepler-108 B"].radius = RasSun(0.955127)
#stars["Kepler-108 B"].T = 5309.190
#stars["Kepler-108 B"].L = Star.LasLog10(-0.1850697)

stars["Kepler-411"].radius = RasSun(0.76)
stars["Kepler-411"].T = 4773
stars["Kepler-411"].L = 0.27

stars["Kepler-42"].radius = RasSun(0.175)
stars["Kepler-42"].T = 3269
stars["Kepler-42"].L = 3.08e-3

stars["Kepler-450 A"].radius = RasSun(1.600)
stars["Kepler-450 A"].T = 6298
stars["Kepler-450 A"].L = Star.LasLog10(0.53147524)

stars["Kepler-595"].radius = RasSun(1.600)
stars["Kepler-595"].T = 5138.50
stars["Kepler-595"].L = Star.LasLog10(-0.3476832)

stars["Kepler-82"].radius = RasSun(0.955127)
stars["Kepler-82"].T = 5309.190
stars["Kepler-82"].L = Star.LasLog10(-0.1850697)

stars["KOI-1860"].radius = RasSun(1.08916)
stars["KOI-1860"].T = 5620.270
stars["KOI-1860"].L = Star.LasLog10(0.02790548)

#------------------------------------------------------------------------------

planets["Kepler-22 b"].GM = MasJupiter(0.11)

planets["Kepler-186 b"].GM = MasEarth(1.24)
planets["Kepler-186 c"].GM = MasEarth(2.1)
planets["Kepler-186 d"].GM = MasEarth(2.54)
planets["Kepler-186 e"].GM = MasEarth(2.15)
planets["Kepler-186 f"].GM = MasEarth(1.71)

planets["Kepler-442 b"].GM = MasEarth(2.3)

planets["Kepler-452 b"].GM = MasEarth(5)

planets["Kepler-62 b"].GM = MasEarth(2.1)
planets["Kepler-62 c"].GM = MasEarth(0.1)
planets["Kepler-62 d"].GM = MasEarth(5.5)
planets["Kepler-62 e"].GM = MasEarth(4.5)
planets["Kepler-62 f"].GM = MasEarth(2.8)

