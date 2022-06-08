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

def placebodies(bodies, col):
    xy = [(col, body.flux) for body in bodies]
    x = [xy[0] for xy in xy]
    y = [xy[1] for xy in xy]

    ax.scatter(x, y)
    for i, body in enumerate(bodies):
        ax.annotate(
            body.orbit.center.name and body.name.replace(body.orbit.center.name, "") or body.name,
            (x[i], y[i]),
            xytext=(7, -2.5),
            textcoords="offset points"
        )

def bodies(row, center, bodies):
    placebodies([Mass.resolve(body) for body in bodies], row)

#------------------------------------------------------------------------------

def EarthEquivalent(row, star, bodies):
    HZ_inner = star.orbitByFlux(flux_lim[0])
    HZ = star.orbitByFlux()
    HZ_outer = star.orbitByFlux(flux_lim[2])
    print(TtoDays(HZ_inner.P), "-", TtoDays(HZ.P), "-", TtoDays(HZ_outer.P))

#------------------------------------------------------------------------------

E365 = Star.byFluxPeriod(TasDays(365))
E150 = Star.byFluxPeriod(TasDays(150))
E120 = Star.byFluxPeriod(TasDays(120))

Sun.info()
E150.info()
E120.info()

systems = [
    [Sun, [
        Mercury,
        Venus,
        Earth,
        Mars,
        "Ceres",
        Jupiter,
    ]],
    [E365, [
        Mass("A", orbit=byPeriod(E365, TasDays(80))),
        Mass("B", orbit=byPeriod(E365, TasDays(150))),
        Mass("C", orbit=byPeriod(E365, TasDays(300))),
    ]],
    [E150, [
        Mass("A", orbit=byPeriod(E150, TasDays(80))),
        Mass("B", orbit=byPeriod(E150, TasDays(150))),
        Mass("C", orbit=byPeriod(E150, TasDays(300))),
        Mass("D", orbit=byPeriod(E150, TasDays(600))),
        Mass("E", orbit=byPeriod(E150, TasDays(12 * 150))),
    ]],
    [E120, [
        Mass("A", orbit=byPeriod(E120, TasDays(80))),
        Mass("B", orbit=byPeriod(E120, TasDays(150))),
        Mass("C", orbit=byPeriod(E120, TasDays(300))),
        Mass("D", orbit=byPeriod(E120, TasDays(600))),
    ]],
    ["TRAPPIST-1", [
        "TRAPPIST-1c",
        "TRAPPIST-1d",
        "TRAPPIST-1e",
        "TRAPPIST-1f",
        "TRAPPIST-1g",
    ]],
]

#------------------------------------------------------------------------------

A = byPeriod(Sun,  TasDays(150))
B = byPeriod(E150, TasDays(150))
C = byPeriod(E120, TasDays(150))

for orbit in [A, B, C]:
    print(
        orbit.center.name,
        fmttime(orbit.P),
        fmtdist(orbit.a),
        fmteng(abs(orbit.v()), "m/s")
    )

#B, C = masses["B"], masses["C"]
#travelTime(TasDays(1), B, C)
#B, C = masses["B"], masses["C"]
#travelTime(TasDays(1), B, C)

#print("B a=", fmtdist(B.orbit.a), "v=", fmteng(abs(B.orbit.v()), "m/s"))
#print("C a=", fmtdist(C.orbit.a), "v=", fmteng(abs(C.orbit.v()), "m/s"))

#print("B a=", fmtdist(B.orbit.a), "v=", fmteng(abs(B.orbit.v()), "m/s"))
#print("C a=", fmtdist(C.orbit.a), "v=", fmteng(abs(C.orbit.v()), "m/s"))

#B = Mass("B", orbit = byPeriod(Sun, TasDays(150)))
#C = Mass("C", orbit = byPeriod(Sun, TasDays(300)))
#travelTime(TasDays(1), B, C)
#print("B a=", fmtdist(B.orbit.a), "v=", fmteng(abs(B.orbit.v()), "m/s"))
#print("C a=", fmtdist(C.orbit.a), "v=", fmteng(abs(C.orbit.v()), "m/s"))

#------------------------------------------------------------------------------

def equivalence(star1, star2):
    a, b = [TtoDays(Mass.resolve(s).EarthEquivalence().P) for s in [star1, star2]]

    print("%s - %s: %.1f - %.1f d" % (star1, star2, a, b))

equivalence("F5", "F9")
equivalence("G0", "G9")
equivalence("K0", "K9")
equivalence("M0", "M9")

#exit()

#------------------------------------------------------------------------------

import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots()  # Create a figure containing a single axes.

#------------------------------------------------------------------------------

def starLabel(star):
    star = Mass.resolve(star)
    name, eq = star.name, star.EarthEquivalence().P
    if eq > TasDays(50):
        eq = "E=%.0f d" % TtoDays(eq)
    else:
        eq = "E=%.1f d" % TtoDays(eq)
    if star.name:
        return "%s\n%s" % (eq, name)
    return "%s" % (eq)

stars = [starLabel(star) for star, planets in systems]

ax.set_xlim(-0.5, len(stars)-0.5)
ax.set_xticks(range(len(stars)))
ax.set_xticklabels(stars)

for x in range(len(stars)):
    plt.axvline(x, linestyle="dashed", color="grey", linewidth=0.5)

ax.invert_yaxis()
ax.set_yscale('log')
yticks = [8.0, 4.0, 2.0, 1.0, 0.5, 0.25, 0.125]
ax.set_yticks(yticks)
ax.set_yticklabels(yticks)
ax.set_ylabel("Säteilyteho (x Maa)")

flux_lim = [2.0, 1.0, 0.396]

ax.fill_between(ax.get_xlim(), flux_lim[0], flux_lim[1], color="lightyellow")
ax.fill_between(ax.get_xlim(), flux_lim[1], flux_lim[2], color="lightgreen")
plt.axhline(y = flux_lim[0], color="red")
plt.axhline(y = flux_lim[1], color="green")
plt.axhline(y = flux_lim[2], color="blue")

for i, system in enumerate(systems):
    star, planets = system
    bodies(i, star, planets)

ax2 = ax.twinx()
ax2.set_yscale('log')
ax2.set_ylim(ax.get_ylim())
ax2.set_yticks(flux_lim)
ax2.set_yticklabels([("x%.1f" % flux2P(flow)) for flow in flux_lim])
ax2.set_ylabel("Kiertoaika")

#print(flux2P(Venus.flux) * 365)
#print(flux2P(Mars.flux) * 365)

plt.grid()
plt.show()
