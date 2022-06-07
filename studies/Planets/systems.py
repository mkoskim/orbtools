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

    T0 = (A.P + B.P)
    T1 = (A.P + B.P) / 4.0
    T2 = solve_aPaP(A.a, A.P, (A.a + B.a) / 2, None) / 2
    T3 = Orbit(A.orbit.center, A.a, B.a).P / 2

    print(A.center.name, ":", A.name, "->", B.name, ":",
        "T0=%.2f" % (T0 / T_unit),
        "T1=%.2f" % (T1 / T_unit),
        "Kepler=%.2f" % (T2 / T_unit),
        "Newton=%.2f" % (T3 / T_unit)
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

#------------------------------------------------------------------------------

import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots()  # Create a figure containing a single axes.

ax.set_ylim(0.5, 4.5)
ax.set_yticks([1, 2, 3, 4])
ax.set_yticklabels(["TRAPPIST-1", "E=120 d", "E=150 d", "Aurinko\nE=365 d"])
plt.axhline(y = 1, linestyle="dashed", color="grey", linewidth=0.5)
plt.axhline(y = 2, linestyle="dashed", color="grey", linewidth=0.5)
plt.axhline(y = 3, linestyle="dashed", color="grey", linewidth=0.5)
plt.axhline(y = 4, linestyle="dashed", color="grey", linewidth=0.5)

ax.invert_xaxis()
ax.set_xscale('log')
xticks = [8.0, 4.0, 2.0, 1.0, 0.5, 0.25, 0.125]
ax.set_xticks(xticks)
ax.set_xticklabels(xticks)
ax.set_xlabel("Säteilyteho (x Maa)")

flux_lim = [2.0, 1.0, 0.396]

ax.fill_between([flux_lim[0], flux_lim[1]], 0, 5, color="lightyellow")
ax.fill_between([flux_lim[1], flux_lim[2]], 0, 5, color="lightgreen")
plt.axvline(x = flux_lim[0], color="red")
plt.axvline(x = flux_lim[1], color="green")
plt.axvline(x = flux_lim[2], color="blue")

#------------------------------------------------------------------------------

def placebodies(bodies, row):
    xy = [(body.flux, row) for body in bodies]
    x = [xy[0] for xy in xy]
    y = [xy[1] for xy in xy]

    ax.scatter(x, y)
    for i, body in enumerate(bodies):
        ax.annotate(
            body.orbit.center.name and body.name.replace(body.orbit.center.name, ""),
            (x[i], y[i]),
            xytext=(0, 5),
            textcoords="offset points"
        )

def bodies(row, center, bodies, moons = []):
    placebodies([Mass.resolve(body) for body in bodies], row)
    placebodies([Mass.resolve(moon) for moon in moons], row - 0.33)
    #for body in bodies:
    #    print("- %10s %7.2f %7.2f" % (body.name, body.flux, m2AU(body.orbit.a)))
    #print()

#------------------------------------------------------------------------------

def EarthEquivalent(row, star, bodies):
    HZ_inner = star.orbitByFlux(flux_lim[0])
    HZ = star.orbitByFlux()
    HZ_outer = star.orbitByFlux(flux_lim[2])
    print(TtoDays(HZ_inner.P), "-", TtoDays(HZ.P), "-", TtoDays(HZ_outer.P))

#------------------------------------------------------------------------------

bodies(4, Sun, [
    Mercury, Venus, Earth, Mars, "Ceres", Jupiter, Saturn
],
#[Moon, "Ganymede", "Titan"]
)

bodies(1, "TRAPPIST-1", [
    "TRAPPIST-1c",
    "TRAPPIST-1d",
    "TRAPPIST-1e",
    "TRAPPIST-1f",
    "TRAPPIST-1g",
])

star = Star.byFluxPeriod(TasDays(150))
bodies(3, star, [
    Mass("A", orbit=byPeriod(star, TasDays(80))),
    Mass("B", orbit=byPeriod(star, TasDays(150))),
    Mass("C", orbit=byPeriod(star, TasDays(300))),
    Mass("D", orbit=byPeriod(star, TasDays(600))),
    Mass("E", orbit=byPeriod(star, TasDays(12 * 150))),
])

star.info()
B, C = masses["B"], masses["C"]
travelTime(TasDays(1), B, C)
print("B a=", fmtdist(B.orbit.a), "v=", fmteng(abs(B.orbit.v()), "m/s"))
print("C a=", fmtdist(C.orbit.a), "v=", fmteng(abs(C.orbit.v()), "m/s"))

star = Star.byFluxPeriod(TasDays(120))
bodies(2, star, [
    Mass("A", orbit=byPeriod(star, TasDays(80))),
    Mass("B", orbit=byPeriod(star, TasDays(150))),
    Mass("C", orbit=byPeriod(star, TasDays(300))),
    Mass("D", orbit=byPeriod(star, TasDays(600))),
])

star.info()
B, C = masses["B"], masses["C"]
travelTime(TasDays(1), B, C)
print("B a=", fmtdist(B.orbit.a), "v=", fmteng(abs(B.orbit.v()), "m/s"))
print("C a=", fmtdist(C.orbit.a), "v=", fmteng(abs(C.orbit.v()), "m/s"))

#------------------------------------------------------------------------------

B = Mass("B", orbit = byPeriod(Sun, TasDays(150)))
C = Mass("C", orbit = byPeriod(Sun, TasDays(300)))
travelTime(TasDays(1), B, C)
print("B a=", fmtdist(B.orbit.a), "v=", fmteng(abs(B.orbit.v()), "m/s"))
print("C a=", fmtdist(C.orbit.a), "v=", fmteng(abs(C.orbit.v()), "m/s"))


#print(150+300 / 4.)
#x_Jupiter = (Jupiter.orbit.P / Earth.orbit.P)
#print("%.2f" % x_Jupiter)
#print("%.2f" % (x_Jupiter * 150))

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
