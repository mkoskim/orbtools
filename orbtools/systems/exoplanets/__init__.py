#import os, sys
#sys.path.append(os.path.abspath("."))

from orbtools.systems.exoplanets.oec import *
#from orbtools.systems.exoplanets_eu import *

from orbtools.systems.exoplanets.filters import *

print("Stars:")
print("- Total..........:", len(doFilters(stars.values())))
print("- With L.........:", len(doFilters(stars.values(), hasLuminosity)))
print("Exoplanets:")
print("- Total..........:", len(doFilters(planets.values(), isExoplanet)))
print("- With M + R.....:", len(doFilters(planets.values(), isExoplanet, hasMass, hasRadius)))
print("- With M + R + L.:", len(doFilters(planets.values(), isExoplanet, hasMass, hasRadius, hasFlux)))
