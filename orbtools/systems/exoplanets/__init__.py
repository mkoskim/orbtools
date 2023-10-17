#import os, sys
#sys.path.append(os.path.abspath("."))

from orbtools.systems.exoplanets.oec import *
#from orbtools.systems.exoplanets.eu import *

from orbtools.systems.exoplanets.filters import *

print("Stars:")
print("- Total..........:", len(doFilters(stars.values())))
print("- With planets...:", len(doFilters(stars.values(), lambda x: x.hasSatellites)))
print("- Without L......:", len(doFilters(stars.values(), lambda x: not hasLuminosity(x), lambda x: x.hasSatellites)))
print("Exoplanets:")
print("- Total..........:", len(doFilters(planets.values(), isExoplanet)))
print("- With R.........:", len(doFilters(planets.values(), isExoplanet, hasRadius)))
print("- With M.........:", len(doFilters(planets.values(), isExoplanet, hasMass)))
#print("- Only M.........:", len(doFilters(planets.values(), isExoplanet, lambda x: hasMass(x) and not hasRadius(x))))
#print("- Only R.........:", len(doFilters(planets.values(), isExoplanet, lambda x: not hasMass(x) and hasRadius(x))))
print("- With M & R.....:", len(doFilters(planets.values(), isExoplanet, lambda x: hasMass(x) and hasRadius(x))))
#print("- With M + R + L.:", len(doFilters(planets.values(), isExoplanet, hasMass, hasRadius, hasFlux)))
print("- Without L......:", len(doFilters(planets.values(), isExoplanet, isFluxless)))

#------------------------------------------------------------------------------

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

  print("- planets:", len(star.satellites))

#starInfo("Kepler-444 A")
#exit()
