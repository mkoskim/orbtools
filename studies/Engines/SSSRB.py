#!/usr/bin/env python3
###############################################################################
#
# Engine T-ve plot
#
###############################################################################

import os, sys
sys.path.append(os.path.abspath("."))

from orbtools import *
from orbtools.systems.solsystem import *

engine = engines["SSSRB"]
engine.info()

def SSSRB_Payload(orbit):
    dv = abs(orbit.v(0))

    Mf = 90e3
    Mp = 500e3

    k = dv / engine.ve
    R = exp(k)

    print(orbit.center.name, dv)
    print("k=", k, "R=", R, "Payload=", Mp/(R-1)-Mf)


MoonOrbit = Orbit(Moon, Moon.radius, Moon.radius + 300e3)
MarsOrbit = Orbit(Mars, Mars.radius, Mars.radius + 300e3)
EarthOrbit = Orbit(Earth, Earth.radius, Earth.radius + 300e3)

SSSRB_Payload(MoonOrbit)
SSSRB_Payload(MarsOrbit)
SSSRB_Payload(EarthOrbit)
