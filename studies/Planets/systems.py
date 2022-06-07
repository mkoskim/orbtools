#!/usr/bin/env python3
# -*- coding: utf-8 -*-
###############################################################################
#
# Some planetary systems. Lets try if we can help people making their own
# solar systems.
#
###############################################################################

import os, sys
sys.path.append(os.path.abspath("."))

from orbtools.systems.solsystem import *
from orbtools.systems.exoplanets import *

#------------------------------------------------------------------------------

def table(T_unit, *bodies):
    for body in bodies:
        body = Mass.resolve(body)
        print(body.name, fmteng(body.orbit.a, "m"), "%.2f" % (body.orbit.P / T_unit))

def travelTime(T_unit, A, B):
    A = Mass.resolve(A)
    B = Mass.resolve(B)

    T0 = (A.orbit.P + B.orbit.P)
    T1 = (A.orbit.P + B.orbit.P) / 4.0
    T2 = solve_aPaP(A.orbit.a, A.orbit.P, (A.orbit.a + B.orbit.a) / 2, None) / 2
    T3 = Orbit(A.orbit.center, A.orbit.a, B.orbit.a).P / 2

    print(A.name, "->", B.name, ":",
        "T0=%.2f" % (T0 / T_unit),
        "T1=%.2f" % (T1 / T_unit),
        "T2=%.2f" % (T2 / T_unit),
        "T3=%.2f" % (T3 / T_unit)
    )

def travelTimes():
    table(TasDays(1), "Io", "Europa", "Ganymede", "Callisto")
    travelTime(TasDays(1), "Europa", "Ganymede")
    travelTime(TasDays(1), "Callisto", "Europa")
    travelTime(TasDays(1), "Ganymede", "Callisto")

    print("---")
    table(TasYears(1), Venus, Earth, Mars, "Ceres", Jupiter)
    travelTime(TasDays(1), Earth, Mars)
    travelTime(TasYears(1), Earth, Mars)
    travelTime(TasYears(1), Mars, "Ceres")
    travelTime(TasDays(1), Venus, Mars)

    print("---")
    #print(fmteng(masses["TRAPPIST-1"].GM / GM_Jupiter, ""))
    table(TasDays(1),
        "TRAPPIST-1d",
        "TRAPPIST-1e",
        "TRAPPIST-1f",
        "TRAPPIST-1g",
    )
    travelTime(TasDays(1), "TRAPPIST-1d", "TRAPPIST-1f")
    travelTime(TasDays(1), "TRAPPIST-1e", "TRAPPIST-1g")

    exit()

#------------------------------------------------------------------------------

def flux2P(flux):
    r = 1 / sqrt(flux)
    return solve_aPaP(1.0, 1.0, r, None)

def kepler():
    # Flux to period

    def solve_P(a):
        return sqrt(a ** 3.0)

    for flux in [4.0, 2.0, 1.0, 0.5, 0.25, 0.125]:
    #for r in [0.25, 0.5, 1.0, 2.0, 4.0, 8.0]:
        r = 1/(flux ** 0.5)
        #flux = 1/(r ** 2)
        P = solve_P(r)
        print(r ** 3)
        print("%.2f %.2f %.2f" % (flux, r, P))
        #P = solve_aPaP(1.0, 1.0, i, None)
        #a = solve_aPaP(1.0, 1.0, None, i)

        #print(i, "a -> P", i, P)
        #print(i, "P -> a", i, a)
    exit()

#kepler()

#------------------------------------------------------------------------------

import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots()  # Create a figure containing a single axes.

ax.set_ylim(0.5, 3.5)
ax.set_yticks([1, 2, 3])
ax.set_yticklabels(["TRAPPIST-1", "Esimerkki", "Aurinko"])
plt.axhline(y = 1, linestyle="dashed", color="grey", linewidth=0.5)
plt.axhline(y = 2, linestyle="dashed", color="grey", linewidth=0.5)
plt.axhline(y = 3, linestyle="dashed", color="grey", linewidth=0.5)

ax.invert_xaxis()
ax.set_xscale('log')
xticks = [4.0, 2.0, 1.0, 0.5, 0.25, 0.125]
ax.set_xticks(xticks)
ax.set_xticklabels(xticks)
ax.set_xlabel("Säteilyteho (x Maa)")

flux_lim = [2.0, 1.0, 0.396]

ax.fill_between([flux_lim[0], flux_lim[1]], 0, 4, color="lightyellow")
ax.fill_between([flux_lim[1], flux_lim[2]], 0, 4, color="lightgreen")
plt.axvline(x = flux_lim[0], color="red")
plt.axvline(x = flux_lim[1], color="green")
plt.axvline(x = flux_lim[2], color="blue")

#------------------------------------------------------------------------------

def bodies(row, bodies):
    xy = [(body.flux, row) for body in bodies]
    x = [xy[0] for xy in xy]
    y = [xy[1] for xy in xy]

    ax.scatter(x, y)
    for i, body in enumerate(bodies):
        ax.annotate(
            body.name.replace(body.orbit.center.name, ""),
            (x[i], y[i]),
            xytext=(0, 5),
            textcoords="offset points"
        )
    #for body in bodies:
    #    print("- %10s %7.2f %7.2f" % (body.name, body.flux, m2AU(body.orbit.a)))
    #print()

#------------------------------------------------------------------------------

bodies(3, [
    Mercury, Venus, Earth, Mars, masses["Ceres"], Jupiter, Saturn
])

bodies(1, [
    masses["TRAPPIST-1c"],
    masses["TRAPPIST-1d"],
    masses["TRAPPIST-1e"],
    masses["TRAPPIST-1f"],
    masses["TRAPPIST-1g"],
])

star = stars["K3"]

HZ_inner = star.orbitByFlux(flux_lim[0])
HZ = star.orbitByFlux()
HZ_outer = star.orbitByFlux(flux_lim[2])
print(TtoDays(HZ_inner.P), "-", TtoDays(HZ.P), "-", TtoDays(HZ_outer.P))

bodies(2, [
    Mass("A", orbit=byPeriod(star, TasDays(80))),
    Mass("B", orbit=byPeriod(star, TasDays(150))),
    Mass("C", orbit=byPeriod(star, TasDays(300))),
    Mass("D", orbit=byPeriod(star, TasDays(600))),
    Mass("E", orbit=byPeriod(star, TasDays(1780))),
])

#print(150+300 / 4.)
x_Jupiter = (Jupiter.orbit.P / Earth.orbit.P)
print("%.2f" % x_Jupiter)
print("%.2f" % (x_Jupiter * 150))

#------------------------------------------------------------------------------

ax2 = ax.twiny()
ax2.set_xscale('log')
ax2.set_xlim(ax.get_xlim())
ax2.set_xticks(flux_lim)
ax2.set_xticklabels([("x%.1f" % flux2P(flow)) for flow in flux_lim])
ax2.set_xlabel("Kiertoaika")

#print(flux2P(Venus.flux) * 365)
#print(flux2P(Mars.flux) * 365)

plt.grid()
plt.show()
