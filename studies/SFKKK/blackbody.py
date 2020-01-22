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

def makebb(T):
    bb = []
    for wl in spectrum:
        bb.append(blackbody(T, wl * 1e-9))

    s = sum(bb)
    return list(map(lambda p: p/s, bb))

G2V = makebb(5780)
K0  = makebb(5240)

#for p in G2V: print(p)
for p in K0: print(p)
#for wl in spectrum: print wl

