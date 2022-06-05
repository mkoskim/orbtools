#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
#
# Flight profiles from surfaces to low orbits
#
###############################################################################

import os, sys
sys.path.append(os.path.abspath("."))

from orbtools.systems.solsystem import *
from orbtools.systems.exoplanets import *

#------------------------------------------------------------------------------
# How we want to make surface to orbit transfers?

def plot():

    T = Transfer.TakeOff("Earth-LEO", Earth, 300e3)
    A = T.initial
    B = T.final

    T.info()
    A.info()
    B.info()

    import plotter

    plotter.orbit(A)
    plotter.orbit(B)

    for burn in T.burns:
        if burn.stay: plotter.travel(burn.orbit, 0.0, burn.stay)

    #plotter.travel(B, 0.0, 0.5)
    #plotter.travel(C, 0.0, 0.66)
    #plotter.orbit(C)

    plotter.show()

#T1 = Burn(A)

plot()
exit()

#------------------------------------------------------------------------------

def info():
    SuperEarth = Mass("Super", GM_Earth*4, Mass.rFromV(GM2kg(GM_Earth*4) / Earth.density), 0)

    SuperLEO = byAltitude(SuperEarth, 0, 300e3)
    EarthLEO = byAltitude(Earth, 0, 300e3)
    MarsLMO = byAltitude(Mars, 0, 300e3)
    MoonLMO = byAltitude(Moon, 0, 300e3)

    for orbit in [SuperLEO, EarthLEO, MarsLMO, MoonLMO]:
        dv1 = abs(orbit.v(0))
        v2 = abs(orbit.v(0.5))
        vf = v_circular(orbit.center.GM, orbit.r2)
        dv2 = vf - v2
        g = orbit.center.g_surface

        print(orbit.center.name,
            ("%.2f g" % (g / const_g)),
            ("%.2f m/s" % dv1),
            ("%.2f min" % (solve_vat(dv1, g + 0.7*9.81, None)/60)),
            #fmteng(v2, "m/s"),
            #fmteng(vf, "m/s"),
            ("%.2f min" % ((orbit.P/2)/60)),
            fmteng(dv2, "m/s"),
        )
    exit()

#info()

#------------------------------------------------------------------------------
# Example rocket: Falcon-9 v1.2 / Block 5 TSTO
#------------------------------------------------------------------------------

Falcon9_I = Stage(
    "Falcon-9/I",
    engine = Engine.Stack(9, engines["Merlin 1D/sea"]),
    drymass =  25_600,
    fuel    = 395_700
)

Falcon9_II = Stage(
    "Falcon-9/II",
    engine = engines["Merlin 1D"], # vacuum
    drymass =  3_900,
    fuel    = 92_670
)

Falcon9_toLEO = Payload("Payload", 22_000)
Falcon9_toGEO = Payload("Payload",  8_300)

Falcon9 = Rocket("Falcon-9",
    Falcon9_I,
    Falcon9_II,
    Falcon9_toLEO,
    #Falcon9_toGEO,
)

Falcon9.info()

#exit()

#------------------------------------------------------------------------------
# "Learspace"
#------------------------------------------------------------------------------

Learspace = Rocket("Learspace",
    Stage(
        "Learspace/I",
        engine = Engine.veF("SSE-1", 12_400, 176_600),
        drymass=6000,
        fuel=6000
    )
)

#------------------------------------------------------------------------------
# Plot acceleration & velocity diagram
#------------------------------------------------------------------------------

def plotAccVel(rocket):

    import matplotlib.pyplot as plt
    import numpy as np

    #--------------------------------------------------------------------------

    stages = [s for s in rocket.stages if s.engine]
    burns  = [0] + [s.t_burn + 15 for s in stages]
    start = np.cumsum(burns)

    def burn(stage):
        return [
            (start[stage] + t, rocket.a(stage, t))
            for t
            in np.arange(0, burns[stage+1], 1.0)
        ]

    xy = [(t, 0.0) for t in np.arange(-15, 0, 1)] + list(np.concatenate([burn(i) for i, stage in enumerate(stages)]))

    #--------------------------------------------------------------------------

    x   = [p[0]/60.0 for p in xy]
    acc = [p[1] for p in xy]
    vel = np.cumsum(acc)

    print("Rocket........:", rocket.name)
    print("- Acc average.: %.2f g" % (sum(acc)/len(acc) / const_g))
    print("- Final v.....: %.2f m/s" % (vel[-1]))
    print("- Burn time...: %.2f min" % (solve_vat(vel[-1], sum(acc)/len(acc), None) / 60.0))

    #--------------------------------------------------------------------------

    fig, ax = plt.subplots()
    plt.grid()
    ax.set_ylabel("Acceleration (g)")
    ax.set_xlabel("Time (min)")

    line1, = ax.plot(
        x,
        [a/const_g for a in acc],
        color="orange",
        label="Acceleration"
    )

    ax2 = ax.twinx()
    ax2.set_ylabel("Velocity [km/s]")
    line2, = ax2.plot(
        x,
        [v*1e-3 for v in vel],
        color="green",
        label="Velocity"
    )

    plt.legend(
        bbox_to_anchor=(0., 1.02, 1., .102), loc='lower left', ncol=2,
        handles = [line1, line2]
    )
    plt.show()

plotAccVel(Falcon9)
#plotAccVel(Learspace)
