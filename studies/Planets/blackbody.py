#!/usr/bin/env python3
###############################################################################
#
# Blackbody calculations
#
###############################################################################

import os, sys
sys.path.append(os.path.abspath("."))

from orbtools.systems.solsystem import *
from orbtools.systems.exoplanets import *

#------------------------------------------------------------------------------

for name in ["F5", "Sun", "K2"]:
    o = stars[name].orbitByFlux()
    print("%s: r=%.2f AU, P=%.2f d" % (name, m2AU(o.a), TtoDays(o.P)))

sys.exit()

#------------------------------------------------------------------------------

step = 10
spectrum = range(step, 2000, step)

def makebb(txt, T, W):
    bb = []
    for wavelength in spectrum:
        bb.append(blackbody(T, wavelength * 1e-9))

    E = W / (step * sum(bb))
    return [txt] + list(map(lambda x: x * E, bb))

#T5000 = makebb(5000, 1300)
#K5 = makebb(stars["K2"].T, 1300)
#G2 = makebb(stars["G2"].T, 1300)
#F5 = makebb(stars["F5"].T, 1300)

data = zip(
    ["Aallonpituus (nm)"] + list(spectrum),
    #makebb("Sun", 5777, 1367),
    #makebb("4000K", 4000, 1367),
    #makebb("3000K", 3000, 1367),
    makebb("K2", stars["K2"].T, 1367),
    makebb("G2", stars["G2"].T, 1367),
    makebb("F5", stars["F5"].T, 1367),
)

#for p in G2: print(p)
#for p in K0: print(p)
#for p in F5: print(p)
#for wl in spectrum: print wl
for d in data: print("\t".join(map(str, d)))
