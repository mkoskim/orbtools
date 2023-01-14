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

ticks_r = [1.0, 10.0, 100.0, 1000.0]
ticks_r_planets = [1.0, 5.0, 10.0]

ticks_m = [0.1, 1.0, 10.0, 100.0, 1000.0, 10_000.0, 100_000, 1_000_000]
ticks_m_planets = [0.1, 1, 10, 100, 500]
ticks_m_stars = [10_000.0, 100_000, 1_000_000]

ticks_density = [1_000, 2_500, 5_000, 10_000]

ticks_flux = [0.001, 0.01, 0.1, 1.0, 10.0]

ticks_L = [0.001, 0.01, 0.1, 1.0, 10.0, 100.0]

ticks_T_stars = [3_000, 5_000, 10_000]

ticks_Mag = [10, 5, 0, -5]

ticks_P = [1, 10, 100, 365, 1000, 10000]

def tick_max(ticks): return max(ticks)
def tick_min(ticks): return min(ticks)
def tick_range(ticks): return 0.5*min(ticks), 2*max(ticks)

#------------------------------------------------------------------------------

def y_Mass(plt, ax, data, ticks = None, append=False):
  if not append:
    if not ticks: ticks = ticks_m

    ymin, ymax = tick_range(ticks)

    ax.set_ylabel("Massa (x Maa)")
    ax.set_ylim(ymin, ymax)
    ax.set_yscale('log')

    set_yticks(ax, ticks)

    ticks2 = [ Moon, Mars, Earth, Neptune, Jupiter, Star.typical["M9"], Sun]
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
    ax.set_xlim(xmin, xmax)
    ax.set_xscale('log')
    set_xticks(ax, ticks)

    ticks2 = [ Mars, Earth, Neptune, Jupiter, Star.typical["M9"], Sun]
    ticks2 = filter(lambda m: MtoEarth(m.GM) > xmin and MtoEarth(m.GM) < xmax, ticks2)
    ticks2 = list(ticks2)

    if len(ticks2):
      ax2 = ax.twiny()
      ax2.set_xscale('log')
      ax2.set_xlim(ax.get_xlim())
      set_xticks(ax2,
        [MtoEarth(x.GM) for x in ticks2],
        [x.name for x in ticks2]
      )

  return [MtoEarth(planet.GM) for planet in data]

#------------------------------------------------------------------------------

def y_Radius(plt, ax, data, ticks, append = False):
  if not append:
    if not ticks: ticks = ticks_r
    ymin, ymax = tick_range(ticks)

    ax.set_ylabel("Halkaisija (x Maa)")
    ax.set_ylim(ymin, ymax)
    ax.set_yscale('log')

    set_yticks(ax, ticks)

    ticks2 = [ Moon, Mars, Earth, Neptune, Jupiter, Sun]
    ticks2 = filter(lambda m: RtoEarth(m.radius) > ymin and RtoEarth(m.radius) < ymax, ticks2)
    ticks2 = list(ticks2)

    if len(ticks2):
      ax2 = ax.twinx()
      ax2.set_yscale('log')
      ax2.set_ylim(ax.get_ylim())
      set_yticks(ax2,
        [RtoEarth(x.radius) for x in ticks2],
        [x.name for x in ticks2]
      )

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

def y_Density(plt, ax, data, ticks = None):
  if not ticks: ticks = ticks_density
  ymin, ymax = tick_range(ticks)

  ax.set_ylabel("Tiheys")
  ax.set_yscale('log')
  ax.set_ylim(ymin, ymax)
  set_yticks(ax, ticks)

  return [planet.density for planet in data]

def x_Density(plt, ax, data, ticks = None):
  if not ticks: ticks = ticks_density
  xmin, xmax = tick_range(ticks)

  ax.set_xlabel("Tiheys")
  ax.set_xscale('log')
  ax.set_xlim(xmin, xmax)
  set_xticks(ax, ticks)
  ax.invert_xaxis()

  return [planet.density for planet in data]

#------------------------------------------------------------------------------

def y_Luminosity(plt, ax, data, ticks = None):
  if ticks is None: ticks = ticks_L
  ymin, ymax = min(ticks)*0.5, max(ticks)*2

  ax.set_ylabel("Säteilyteho")
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

    ax.set_ylabel("Lämpötila")
    #ax.set_yscale('log')
    ax.set_ylim(ymin, ymax)
    set_yticks(ax, ticks)

  return [mass.T for mass in data]

#------------------------------------------------------------------------------

def x_Period(plt, ax, data, ticks):
  if not ticks: ticks = ticks_P
  xmin, xmax = min(ticks)*0.5, max(ticks)*2

  ax.set_xlabel("Kiertoaika (d)")
  ax.set_xlim(xmin, xmax)
  ax.set_xscale('log')
  set_xticks(ax, ticks)

  plt.axvline(x = 365, ls="dashed", color="grey")

  return [TtoDays(planet.orbit.P) for planet in data]

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

#------------------------------------------------------------------------------

def Flux_Radius(plt, ax, data, xticks=None, yticks=None, append = False, N = None):
  data = doFilters(data, hasRadius, hasFlux)
  if not append:
    if not N: N = len(data)
    plt.title("N=%d" % N)

  return (
    x_Flux(plt, ax, data, xticks, append),
    y_Radius(plt, ax, data, yticks, append)
  )

def Flux_Mass(plt, ax, data, xticks=None, yticks=None, append=False, N = None):
  data = doFilters(data, hasMass, hasFlux)
  if not append:
    if not N: N = len(data)
    plt.title("N=%d" % N)

  return (
    x_Flux(plt, ax, data, xticks, append),
    y_Mass(plt, ax, data, yticks, append)
  )

def Flux_Temperature(plt, ax, data, xticks=None, yticks=None, append=False):
  data = doFilters(data, hasFlux, hasTemperature)
  plt.title("N=%d" % len(data))

  return (
    x_Flux(plt, ax, data, xticks, append),
    y_Temperature(plt, ax, data, yticks, append)
  )

def Period_Radius(plt, ax, data, xticks=None, yticks=None):
  data = list(doFilters(data, hasRadius, hasPeriod))
  plt.title("N=%d" % len(data))

  return (
    x_Period(plt, ax, data, xticks),
    y_Radius(plt, ax, data, yticks) # Planets
  )

def Period_Mass(plt, ax, data, xticks=None, yticks=None):
  data = list(doFilters(data, hasMass, hasPeriod))
  plt.title("N=%d" % len(data))

  return (
    x_Period(plt, ax, data, xticks),
    y_Mass(plt, ax, data, yticks) # Planets
  )

def Mass_Radius(plt, ax, data, xticks=None, yticks=None, append=False, N=None):
  data = doFilters(data, hasRadius, hasMass)
  if not append:
    if not N: N = len(data)
    plt.title("N=%d" % N)

  return (
    x_Mass(plt, ax, data, xticks, append),
    y_Radius(plt, ax, data, yticks, append)
  )

def Radius_Mass(plt, ax, data, xticks=None, yticks=None, append=False, N=None):
  data = doFilters(data, hasRadius, hasMass)
  if not append:
    if not N: N = len(data)
    plt.title("N=%d" % N)

  return (
    x_Radius(plt, ax, data, xticks, append),
    y_Mass(plt, ax, data, yticks, append)
  )

def Mass_Density(plt, ax, data, xticks=None, yticks=None):
  data = list(doFilters(data, hasRadius, hasMass))
  plt.title("N=%d" % len(data))

  return (
    x_Mass(plt, ax, data, xticks),
    y_Density(plt, ax, data, yticks)
  )

def Mass_Luminosity(plt, ax, data, xticks=None, yticks=None):
  data = list(doFilters(data, hasMass, hasLuminosity))
  print("Points.:", len(data))

  return (
    x_Mass(plt, ax, data, xticks),
    y_Luminosity(plt, ax, data, yticks)
  )

def Luminosity_Mass(plt, ax, data, xticks=None, yticks=ticks_m_stars):
  data = list(doFilters(data, hasMass, hasLuminosity))
  print("Points.:", len(data))

  return (
    x_Luminosity(plt, ax, data, xticks),
    y_Mass(plt, ax, data, yticks),
  )

def Temperature_Mass(plt, ax, data, xticks=None, yticks=ticks_m_stars):
  data = list(doFilters(data, hasMass, hasTemperature))
  print("Points.:", len(data))

  return (
    x_Temperature(plt, ax, data, xticks),
    y_Mass(plt, ax, data, yticks),
  )

def Temperature_Magnitude(plt, ax, data, xticks=None, yticks=None):
  data = list(doFilters(data, hasMass, hasMagnitude))
  print("Points.:", len(data))

  return (
    x_Temperature(plt, ax, data, xticks),
    y_Magnitude(plt, ax, data, yticks),
  )
