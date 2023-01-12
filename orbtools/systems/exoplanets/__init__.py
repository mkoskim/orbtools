#import os, sys
#sys.path.append(os.path.abspath("."))

from orbtools.systems.exoplanets.oec import *
#from orbtools.systems.exoplanets_eu import *

from orbtools.systems.exoplanets.filters import *

print("Exoplanets imported:")
print("- Total..........:", len(doFilters(planets.values(), isExoplanet)))
print("- With M + R.....:", len(doFilters(planets.values(), isExoplanet, hasMass, hasRadius)))
print("- With M + R + L.:", len(doFilters(planets.values(), isExoplanet, hasMass, hasRadius, hasFlux)))
#print("Stars...:", len(stars.keys()))
#print("Planets.:", len(planets.keys()))
