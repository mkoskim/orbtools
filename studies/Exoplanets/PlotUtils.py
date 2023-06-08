#!/usr/bin/env python3
###############################################################################
#
# Test plots to see that star database seems fine
#
###############################################################################

import os, sys
sys.path.append(os.path.abspath("."))

from orbtools import *
from orbtools.systems.solsystem import *
from orbtools.systems.exoplanets import *

###############################################################################
#
# Plotting
#
###############################################################################

#------------------------------------------------------------------------------
# Setting data to axes
#------------------------------------------------------------------------------

def set_yticks(ax, ticks, labels = None):
  if ticks and not labels: labels = ticks
  if ticks: ax.set_yticks(ticks)
  if labels: ax.set_yticklabels(labels)

def set_xticks(ax, ticks, labels = None):
  if ticks and not labels: labels = ticks
  if ticks: ax.set_xticks(ticks)
  if labels: ax.set_xticklabels(labels)

#------------------------------------------------------------------------------

def set_yticks2(ax, ticks, labels = None):
  if not labels: labels = ticks

  pairs = zip(ticks, labels)
  ymin, ymax = ax.get_ylim()
  pairs = list(filter(lambda x: x[0] > ymin and x[0] < ymax, pairs))
  if not len(pairs): return

  ticks = [x[0] for x in pairs]
  labels = [x[1] for x in pairs]

  ax2 = ax.twinx()
  ax2.set_yscale(ax.get_yscale())
  ax2.set_ylim(ax.get_ylim())
  set_yticks(ax2, ticks, labels)
  ax2.minorticks_off()

def set_xticks2(ax, ticks, labels = None):
  if not labels: labels = ticks

  pairs = zip(ticks, labels)
  xmin, xmax = ax.get_xlim()
  pairs = list(filter(lambda x: x[0] > xmin and x[0] < xmax, pairs))
  if not len(pairs): return

  ticks = [x[0] for x in pairs]
  labels = [x[1] for x in pairs]

  ax2 = ax.twiny()
  ax2.set_xscale(ax.get_xscale())
  ax2.set_xlim(ax.get_xlim())
  set_xticks(ax2, ticks, labels)
  ax2.minorticks_off()

#------------------------------------------------------------------------------

ticks_r = [1.0, 10.0, 100.0, 1000.0]
ticks_r_planets = [0.5, 1.0, 5.0, 10.0, 20.0]

ticks_m = [0.1, 1.0, 10.0, 100.0, 1000.0, 10_000.0, 100_000, 1_000_000]
ticks_m_planets = [0.1, 1, 10, 100, 1000]
ticks_m_stars = [10_000.0, 100_000, 1_000_000]
ticks_m_sol = [0.1, 0.5, 1.0, 2.0]

ticks_density = [0, 1000, 2500, 5000, 7500, 10000]

ticks_flux = [0.001, 0.01, 0.1, 1.0, 10.0]

ticks_L = [0.001, 0.01, 0.1, 1.0, 10.0, 100.0]

ticks_T_stars = [3_000, 5_000, 10_000]

ticks_Mag = [10, 5, 0, -5]

ticks_P = [1, 10, 100, 1000, 10000]

ticks_distance = [0, 1000, 2500, 5000, 10000]

def tick_max(ticks): return max(ticks)
def tick_min(ticks): return min(ticks)
def tick_range(ticks, extend=1.5): return min(ticks)/extend, max(ticks)*extend

#------------------------------------------------------------------------------

def y_Mass(plt, ax, data, ticks = None, append=False):
  if not append:
    if not ticks: ticks = ticks_m

    ymin, ymax = tick_range(ticks)

    ax.set_ylabel("Massa (x Maa)")
    ax.set_yscale('log')
    ax.set_ylim(ymin, ymax)
    set_yticks(ax, ticks)

    ticks2 = [ Moon, Mars, Earth, Neptune, Saturn, Jupiter, Star.typical["M9"], Sun]
    ticks2 = filter(lambda m: MtoEarth(m.GM) > ymin and MtoEarth(m.GM) < ymax, ticks2)
    ticks2 = list(ticks2)

    if len(ticks2):
      ax2 = ax.twinx()
      ax2.set_yscale(ax.get_yscale())
      ax2.set_ylim(ax.get_ylim())
      set_yticks(ax2,
        [MtoEarth(x.GM) for x in ticks2],
        [x.name for x in ticks2]
      )

  return [MtoEarth(planet.GM) for planet in data]

def x_Mass(plt, ax, data, ticks, append=False):
  if not append:
    if not ticks: ticks = ticks_m
    xmin, xmax = tick_range(ticks)

    ax.set_xlabel("Massa (x Maa)")
    ax.set_xscale('log')
    ax.set_xlim(xmin, xmax)
    set_xticks(ax, ticks)

    ticks2 = [ Mars, Earth, Neptune, Jupiter, Star.typical["M9"], Sun]

    set_xticks2(ax, [MtoEarth(x.GM) for x in ticks2], [x.name for x in ticks2])

  return [MtoEarth(planet.GM) for planet in data]

def x_MassStar(plt, ax, data, ticks, append=False):
  if not append:
    if not ticks: ticks = ticks_m_sol
    xmin, xmax = tick_range(ticks)

    ax.set_xlabel("Massa (x Aurinko)")
    ax.set_xscale('log')
    ax.set_xlim(xmin, xmax)
    set_xticks(ax, ticks)

    ticks2 = [ Star.typical["M9"], Star.typical["K9"], Star.typical["G9"], Star.typical["F9"], Star.typical["F0"]]

    set_xticks2(ax, [MtoSun(x.GM) for x in ticks2], [x.name for x in ticks2])
    for startype in ticks2: plt.axvline(x = MtoSun(startype.GM), ls="dashed")

  return [MtoSun(star.GM) for star in data]


#------------------------------------------------------------------------------

def y_Radius(plt, ax, data, ticks, append = False):
  if not append:
    if not ticks: ticks = ticks_r
    ymin, ymax = tick_range(ticks)

    ax.set_ylabel("Halkaisija (x Maa)")
    ax.set_yscale('log')
    set_yticks(ax, ticks)
    ax.set_ylim(ymin, ymax)

    ticks2 = [ Moon, Mars, Earth, Neptune, Jupiter, Sun]
    set_yticks2(ax, [RtoEarth(x.radius) for x in ticks2], [x.name for x in ticks2])

  return [RtoEarth(planet.radius) for planet in data]

def x_Radius(plt, ax, data, ticks, append = False):
  if not append:
    if not ticks: ticks = ticks_r
    xmin, xmax = min(ticks)*0.5, max(ticks)*2

    ax.set_xlabel("Halkaisija (x Maa)")
    ax.set_xlim(xmin, xmax)
    ax.set_xscale('log')
    set_xticks(ax, ticks)

  return [RtoEarth(planet.radius) for planet in data]

#------------------------------------------------------------------------------

def y_Density(plt, ax, data, ticks = None, append=False):
  if not append:
    if not ticks: ticks = ticks_density
    ymin, ymax = tick_range(ticks, extend=1)

    ax.set_ylabel("Tiheys (kg/m³)")
    #ax.set_yscale('log')
    ax.set_ylim(ymin, ymax)
    set_yticks(ax, ticks)

    for m in [Earth, Neptune]:
      plt.axhline(y = m.density, ls="dashed", label=m.name)

    #ticks2 = [Earth, Neptune]
    #set_yticks2(ax, [x.density for x in ticks2], [x.name for x in ticks2])

  return [planet.density for planet in data]

def x_Density(plt, ax, data, ticks = None, append=False):
  if not append:
    if not ticks: ticks = ticks_density
    xmin, xmax = min(ticks), max(ticks)

    ax.set_xlabel("Tiheys")
    #ax.set_xscale('log')
    ax.set_xlim(xmin, xmax)
    set_xticks(ax, ticks)

  return [planet.density for planet in data]

#------------------------------------------------------------------------------

def y_Luminosity(plt, ax, data, ticks = None):
  if ticks is None: ticks = ticks_L
  ymin, ymax = min(ticks)*0.5, max(ticks)*2

  ax.set_ylabel("Säteilyteho (x Aurinko)")
  ax.set_yscale('log')
  ax.set_ylim(ymin, ymax)
  set_yticks(ax, ticks)

  return [star.L for star in data]

def x_Luminosity(plt, ax, data, ticks = None):
  if ticks is None: ticks = ticks_L
  xmin, xmax = min(ticks)*0.5, max(ticks)*2

  ax.set_xlabel("Säteilyteho")
  ax.set_xscale('log')
  ax.set_xlim(xmin, xmax)
  set_xticks(ax, ticks)

  return [star.L for star in data]

#------------------------------------------------------------------------------

def y_Magnitude(plt, ax, data, ticks = None):
  #if ticks is None: ticks = ticks_Mag
  #ymin, ymax = min(ticks)*0.5, max(ticks)*2

  ax.set_ylabel("Magnitudi")
  #ax.set_yscale('log')
  #ax.set_ylim(ymin, ymax)
  #set_yticks(ax, ticks)
  ax.invert_yaxis()

  return [star.mag for star in data]

#------------------------------------------------------------------------------

def x_Temperature(plt, ax, data, ticks = None, append = False):

  if not append:
    if ticks is None: ticks = ticks_T_stars
    xmin, xmax = min(ticks)*0.5, max(ticks)*2

    ax.set_xlabel("Lämpötila")
    ax.set_xscale('log')
    ax.set_xlim(xmin, xmax)
    set_xticks(ax, ticks)

  return [mass.T for mass in data]

def y_Temperature(plt, ax, data, ticks = None, append = False):

  if not append:
    if ticks is None: ticks = ticks_T_stars
    ymin, ymax = min(ticks)*0.5, max(ticks)*2

    ax.set_ylabel("Lämpötila (C)")
    #ax.set_yscale('log')
    ax.set_ylim(ymin, ymax)
    set_yticks(ax, ticks)

  return [mass.T-273.4 for mass in data]

#------------------------------------------------------------------------------

def x_Period(plt, ax, data, ticks, append=False):
  if not append:
    if not ticks: ticks = ticks_P
    xmin, xmax = min(ticks)*0.5, max(ticks)*2

    ax.set_xlabel("Kiertoaika (d)")
    ax.set_xlim(xmin, xmax)
    ax.set_xscale('log')
    set_xticks(ax, ticks)

    plt.axvline(x = 365, ls="dashed")

  return [TtoDays(planet.orbit.P) for planet in data]

def y_Period(plt, ax, data, ticks, append=False):
  if not append:
    if not ticks: ticks = ticks_P
    xmin, xmax = tick_range(ticks)

    ax.set_ylabel("Kiertoaika (d)")
    ax.set_ylim(xmin, xmax)
    ax.set_yscale('log')
    set_yticks(ax, ticks)

    plt.axhline(y = 365, ls="dashed")

  return [TtoDays(planet.orbit.P) for planet in data]

#------------------------------------------------------------------------------

def x_Flux(plt, ax, data, ticks = None, append = False):
  if not append:
    if not ticks: ticks = ticks_flux
    xmin, xmax = min(ticks)*0.5, max(ticks)*2

    ax.set_xlabel("Flux (x Earth)")
    ax.set_xscale('log')

    ax.set_xlim(xmin, xmax)
    set_xticks(ax, ticks)

    ax.invert_xaxis()

    flux_lim = [2.0, 1.0, 0.396, flux_FrostLine]
    plt.axvline(x = flux_lim[0], color="red")
    plt.axvline(x = flux_lim[1], color="green")
    plt.axvline(x = flux_lim[2], color="blue")
    plt.axvline(x = flux_lim[3], ls="dashed")

  return [planet.flux for planet in data]

def x_Distance(plt, ax, data, ticks = None, append = False):
  if not append:
    if not ticks: ticks = ticks_distance
    xmin, xmax = min(ticks), max(ticks)

    ax.set_xlabel("Distance (ly)")
    #ax.set_xscale('log')

    ax.set_xlim(xmin, xmax)
    set_xticks(ax, ticks)

  return [m2ly(planet.system.dist) for planet in data]

#------------------------------------------------------------------------------

def Flux_Radius(plt, ax, data, xticks=None, yticks=None, append = False, N = None, marker="."):
  data = doFilters(data, hasRadius, hasFlux)
  if not append:
    if not N: N = len(data)
    plt.title("N=%d" % N)

  ax.scatter(
    x_Flux(plt, ax, data, xticks, append),
    y_Radius(plt, ax, data, yticks, append),
    marker=marker
  )

def Flux_Mass(plt, ax, data, xticks=None, yticks=None, append=False, N = None, marker="."):
  data = doFilters(data, hasMass, hasFlux)
  if not append:
    if not N: N = len(data)
    plt.title("N=%d" % N)

  ax.scatter(
    x_Flux(plt, ax, data, xticks, append),
    y_Mass(plt, ax, data, yticks, append),
    marker=marker
  )

def Flux_Temperature(plt, ax, data, xticks=None, yticks=None, append=False, marker="."):
  data = doFilters(data, hasFlux, hasTemperature)
  plt.title("N=%d" % len(data))

  ax.scatter(
    x_Flux(plt, ax, data, xticks, append),
    y_Temperature(plt, ax, data, yticks, append),
    marker=marker
  )

def Period_Radius(plt, ax, data, xticks=None, yticks=None, marker="."):
  data = list(doFilters(data, hasRadius, hasPeriod))
  plt.title("N=%d" % len(data))

  ax.scatter(
    x_Period(plt, ax, data, xticks),
    y_Radius(plt, ax, data, yticks),
    marker=marker
  )

def Period_Mass(plt, ax, data, xticks=None, yticks=None, marker=".", **kw):
  data = list(doFilters(data, hasMass, hasPeriod))
  plt.title("N=%d" % len(data))

  ax.scatter(
    x_Period(plt, ax, data, xticks),
    y_Mass(plt, ax, data, yticks),
    marker=marker,
    **kw
  )

def Mass_Radius(plt, ax, data, xticks=None, yticks=None, append=False, N=None, marker=".", **kw):
  data = doFilters(data, hasRadius, hasMass)
  if not append:
    if not N: N = len(data)
    plt.title("N=%d" % N)

  ax.scatter(
    x_Mass(plt, ax, data, xticks, append),
    y_Radius(plt, ax, data, yticks, append),
    marker=marker,
    **kw
  )

def Radius_Mass(plt, ax, data, xticks=None, yticks=None, append=False, N=None, marker=".", **kw):
  data = doFilters(data, hasRadius, hasMass)
  if not append: plt.title("N=%d" % (N or len(data)))

  ax.scatter(
    x_Radius(plt, ax, data, xticks, append),
    y_Mass(plt, ax, data, yticks, append),
    marker=marker,
    **kw
  )

def Mass_Density(plt, ax, data, xticks=None, yticks=None, N=None, append=None, marker=".", **kw):
  data = list(doFilters(data, hasRadius, hasMass))
  if not append: plt.title("N=%d" % (N or len(data)))

  ax.scatter(
    x_Mass(plt, ax, data, xticks, append),
    y_Density(plt, ax, data, yticks, append),
    marker=marker,
    **kw
  )

def Mass_Luminosity(plt, ax, data, xticks=None, yticks=None, N=None, append=None, marker=".", **kw):
  data = list(doFilters(data, hasMass, hasLuminosity))
  if not append: plt.title("N=%d" % (N or len(data)))

  ax.scatter(
    x_MassStar(plt, ax, data, xticks),
    y_Luminosity(plt, ax, data, yticks),
    marker=marker,
    **kw
  )

def Luminosity_Mass(plt, ax, data, xticks=None, yticks=ticks_m_stars, N=None, append=None, marker=".", **kw):
  data = list(doFilters(data, hasMass, hasLuminosity))
  if not append: plt.title("N=%d" % (N or len(data)))

  ax.scatter(
    x_Luminosity(plt, ax, data, xticks),
    y_Mass(plt, ax, data, yticks),
    marker=".",
    **kw
  )

def Temperature_Mass(plt, ax, data, xticks=None, yticks=ticks_m_stars, N=None, marker=".", **kw):
  data = list(doFilters(data, hasMass, hasTemperature))
  if not append: plt.title("N=%d" % (N or len(data)))

  ax.scatter(
    x_Temperature(plt, ax, data, xticks),
    y_Mass(plt, ax, data, yticks),
    marker=".",
    **kw
  )

def Temperature_Magnitude(plt, ax, data, xticks=None, yticks=None, N=None, marker=".", **kw):
  data = list(doFilters(data, hasMass, hasMagnitude))
  if not append: plt.title("N=%d" % (N or len(data)))

  ax.scatter(
    x_Temperature(plt, ax, data, xticks),
    y_Magnitude(plt, ax, data, yticks),
    marker=marker,
    **kw
  )

def Distance_Radius(plt, ax, data, xticks=None, yticks=None, N=None, append=None, marker=".", **kw):
  data = doFilters(data, hasRadius, hasDistance)
  if not append: plt.title("N=%d" % (N or len(data)))

  ax.scatter(
    x_Distance(plt, ax, data, xticks, append),
    y_Radius(plt, ax, data, yticks, append),
    marker=marker,
    **kw
  )

def Distance_Mass(plt, ax, data, xticks=None, yticks=None, N=None, append=None, marker=".", **kw):
  data = doFilters(data, hasMass, hasDistance)
  if not append: plt.title("N=%d" % (N or len(data)))

  ax.scatter(
    x_Distance(plt, ax, data, xticks, append),
    y_Mass(plt, ax, data, yticks, append),
    marker=marker,
    **kw
  )

def Distance_Period(plt, ax, data, xticks=None, yticks=None, N=None, append=None, marker=".", **kw):
  data = doFilters(data, hasPeriod, hasDistance)
  if not append: plt.title("N=%d" % (N or len(data)))

  ax.scatter(
    x_Distance(plt, ax, data, xticks, append),
    y_Period(plt, ax, data, yticks, append),
    marker=marker,
    **kw
  )

