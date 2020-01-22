###############################################################################
#
# Blackbody calculations
#
###############################################################################

import os, sys
sys.path.append(os.path.abspath("."))

from orbtools.systems.solsystem import *
from orbtools.systems.exoplanets import *

spectrum = range(50, 2000, 50)

def makebb(T, W):
    bb = []
    for wl in spectrum:
        bb.append(blackbody(T, wl * 1e-9))

    E = sum(bb)
    return list(map(lambda x: W * x/E, bb))

G2 = makebb(5780, 1300)
K0 = makebb(5240, 1300)
F5 = makebb(6540, 1300)

#for p in G2: print(p)
#for p in K0: print(p)
for p in F5: print(p)
#for wl in spectrum: print wl

