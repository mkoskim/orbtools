################################################################################
#
# Some exoplanet systems
#
################################################################################

from orbtools import *

import os, sys
sys.path.append(os.path.abspath("."))

from orbtools import *
#import orbtools.systems.stars

import xml.etree.ElementTree as ET, urllib.request, gzip, io
url = "https://github.com/OpenExoplanetCatalogue/oec_gzip/raw/master/systems.xml.gz"
oec = ET.parse(gzip.GzipFile(fileobj=io.BytesIO(urllib.request.urlopen(url).read())))

#------------------------------------------------------------------------------

def doPlanet(planet, star):
  name = planet.findtext("name")
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

  #if not radius or not orbit: print(name, mass, radius, P, A)

  if not mass: return

  Mass(name, GM = MasJupiter(mass), radius = radius and RasJupiter(radius), orbit = orbit)

#------------------------------------------------------------------------------

def doStar(star, dist):
  name = star.findtext("name")
  if not name: return
  if name == "Sun": return

  sptype = star.findtext("spectraltype") or None
  mass = star.findtext("mass") or None
  radius = star.findtext("radius") or None
  T = star.findtext("temperature") or None
  magV = star.findtext("magV") or None

  #if not radius or not T: print(name, mass, radius, T)

  if not mass: return
  if sptype is None: return
  if sptype[0] not in ["F", "G", "K", "M"]: return

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

for system in oec.getroot():
  doSystem(system)

#------------------------------------------------------------------------------
# Missing data in catalogue
#------------------------------------------------------------------------------

stars["GJ 163"].radius = RasSun(0.409)
stars["GJ 163"].T = 3_460
stars["GJ 163"].L = 0.02163

stars["GJ 180"].radius = RasSun(0.4229)
stars["GJ 180"].T = 3_634
stars["GJ 180"].L = 0.02427

stars["GJ 229"].radius = RasSun(0.69)
stars["GJ 229"].T = 3_700
stars["GJ 229"].L = 0.0430

stars["GJ 433"].radius = RasSun(0.529)
stars["GJ 433"].T = 3_445
stars["GJ 433"].L = 0.034

stars["Gliese 1002"].radius = RasSun(0.137)
stars["Gliese 1002"].T = 3_024
stars["Gliese 1002"].L = 0.001406
Mass("Gliese 1002 a", MasEarth(1.08), orbit = Orbit("Gliese 1002", AU2m(0.0457)))
Mass("Gliese 1002 b", MasEarth(1.36), orbit = Orbit("Gliese 1002", AU2m(0.0738)))

#------------------------------------------------------------------------------
# Missing in catalogue
#------------------------------------------------------------------------------

Star("Gliese 163", MxSun=0.405, RxSun=0.409, T=3460, L=0.02163, sptype="M3.5V", dist = ly2m(49.36), mag=10.91)
#Mass("Gliese 163 b", MasEarth(9.9), orbit=Orbit("Gliese 163", AU2m(0.060)))

"""
################################################################################

Star("Epsilon Eridani",  0.820, sptype = "K2", L = 0.340, dist = 10.475)

################################################################################

Star("HD 192310", MxSun=0.78, RxSun=0.79, sptype = "K2", L = 0.385, T=5069, BV=0.88, dist = 10.475)
Mass("HD 192310b", MasEarth(16.9), orbit = Orbit("HD 192310", AU2m(0.32)))
Mass("HD 192310c", MasEarth(24.0), orbit = Orbit("HD 192310", AU2m(1.18)))

################################################################################

Star("Kepler-62", 0.690, 0.640, sptype="K2", L=0.21, T=4925, BV=0.832, rotate=TasDays(38.3), dist=990)
Mass("Kepler-62b", MasEarth(2.1), RasEarth(1.31), orbit=Orbit("Kepler-62", AU2m(0.0553)))
Mass("Kepler-62c", MasEarth(0.1), RasEarth(0.54), orbit=Orbit("Kepler-62", AU2m(0.0930)))
Mass("Kepler-62d", MasEarth(5.5), RasEarth(1.95), orbit=Orbit("Kepler-62", AU2m(0.1200)))
Mass("Kepler-62e", MasEarth(4.5), RasEarth(1.61), orbit=Orbit("Kepler-62", AU2m(0.4270)))
Mass("Kepler-62f", MasEarth(2.8), RasEarth(1.41), orbit=Orbit("Kepler-62", AU2m(0.7180)))

################################################################################

Star("Kepler-442", 0.610, 0.600, sptype="K5", L=0.117, T=4402, dist=1206)
Mass("Kepler-442b", 2.30 * GM_Earth, orbit = Orbit("Kepler-442", AU2m(0.409)))

################################################################################

Star("54 Piscium", 0.76, 0.944, sptype = "K0", L = 0.52, T = 5062, BV=0.85, rotate= TasDays(40.2), dist = 36.32)
#Mass("54 Piscium B", MasJupiter(50.0), RasSun(0.082), orbit = Orbit("54 Piscium"))
Mass("54 Piscium b", MasJupiter(0.228), orbit = Orbit("54 Piscium", AU2m(0.295)))

################################################################################
#
# Gliese 581 (M3V type red dwarf) & planets
#
################################################################################

Star("Gliese 581", 0.310, 0.299,  sptype = "M3", L = 0.013000, dist = 20.56, rotate = TasDays(132.5))
Mass("Gliese 581e",      1.70 * GM_Earth, orbit = Orbit("Gliese 581", AU2m(0.02815)))
Mass("Gliese 581b",     15.80 * GM_Earth, orbit = Orbit("Gliese 581", AU2m(0.04061)))
Mass("Gliese 581c",      5.50 * GM_Earth, orbit = Orbit("Gliese 581", AU2m(0.07210)))
Mass("Gliese 581g (?)",  2.20 * GM_Earth, orbit = Orbit("Gliese 581", AU2m(0.13000)))
Mass("Gliese 581d (?)",  6.98 * GM_Earth, orbit = Orbit("Gliese 581", AU2m(0.21847)))

################################################################################

Mass("Gliese 876d", 6.83 * GM_Earth, radius = 1.65 * r_Earth)
#Mass("Test", 2 * GM_Earth, radius = 1 * r_Earth)

################################################################################
#
# TRAPPIST-1 (M8 type dwarf star) & planets
#
################################################################################

Star("TRAPPIST-1", 0.089, 0.121,  sptype = "M8", L = 0.000522, dist = 39.60, rotate = TasDays(3.295))
Mass("TRAPPIST-1b",  1.3771 * GM_Earth, radius = 1.116 * r_Earth, orbit = Orbit("TRAPPIST-1", AU2m(0.01154)))
Mass("TRAPPIST-1c",  1.3105 * GM_Earth, radius = 1.097 * r_Earth, orbit = Orbit("TRAPPIST-1", AU2m(0.01580)))
Mass("TRAPPIST-1d",  0.3885 * GM_Earth, radius = 0.778 * r_Earth, orbit = Orbit("TRAPPIST-1", AU2m(0.02227)))
Mass("TRAPPIST-1e",  0.6932 * GM_Earth, radius = 0.920 * r_Earth, orbit = Orbit("TRAPPIST-1", AU2m(0.02925)))
Mass("TRAPPIST-1f",  1.0411 * GM_Earth, radius = 1.045 * r_Earth, orbit = Orbit("TRAPPIST-1", AU2m(0.03849)))
Mass("TRAPPIST-1g",  1.3238 * GM_Earth, radius = 1.129 * r_Earth, orbit = Orbit("TRAPPIST-1", AU2m(0.04683)))
Mass("TRAPPIST-1h",  0.3261 * GM_Earth, radius = 0.775 * r_Earth, orbit = Orbit("TRAPPIST-1", AU2m(0.06189)))

################################################################################
#
# 61 Virginis (G7V type star) & planets
#
################################################################################

Star("61 Virginis", 0.93, 0.9867, sptype = "G7", L = 0.822200, dist = 27.90)
Mass("61 Virginis b", MasEarth(5.3), orbit = Orbit("61 Virginis", AU2m(0.050201)))
Mass("61 Virginis c", MasEarth(18.8), orbit = Orbit("61 Virginis", AU2m(0.2175)))
Mass("61 Virginis d", MasEarth(23.7), orbit = Orbit("61 Virginis", AU2m(0.476)))
"""