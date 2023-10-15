#import os, sys
#sys.path.append(os.path.abspath("."))

from orbtools.systems.exoplanets.oec import *

from orbtools.systems.exoplanets.filters import *

print("Stars:")
print("- Total..........:", len(doFilters(stars.values())))
print("- With planets...:", len(doFilters(stars.values(), lambda x: x.hasSatellites)))
print("- With L.........:", len(doFilters(stars.values(), hasLuminosity)))
print("Exoplanets:")
print("- Total..........:", len(doFilters(planets.values(), isExoplanet)))
print("- With M.........:", len(doFilters(planets.values(), isExoplanet, hasMass)))
print("- With R.........:", len(doFilters(planets.values(), isExoplanet, hasRadius)))
#print("- Only M.........:", len(doFilters(planets.values(), isExoplanet, lambda x: hasMass(x) and not hasRadius(x))))
#print("- Only R.........:", len(doFilters(planets.values(), isExoplanet, lambda x: not hasMass(x) and hasRadius(x))))
print("- With M & R.....:", len(doFilters(planets.values(), isExoplanet, lambda x: hasMass(x) and hasRadius(x))))
#print("- With M + R + L.:", len(doFilters(planets.values(), isExoplanet, hasMass, hasRadius, hasFlux)))
print("- Without L......:", len(doFilters(planets.values(), isExoplanet, isFluxless)))

#exit()