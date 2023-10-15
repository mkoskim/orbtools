# -*- coding: utf-8 -*-
###############################################################################
#
# Basic physics & math equations and solving for orbital calculations
#
###############################################################################

from math import *
from constants import *

#-------------------------------------------------------------------------------
# Geometry
#-------------------------------------------------------------------------------

def arcsec(dist, diam):
  return atan(diam / dist)/(2*pi)*360*60*60

def A_circle(r): return pi * r**2
def A_sphere(r): return 4 * pi * r**2
def V_sphere(r): return 4/3 * pi * r**3

#-------------------------------------------------------------------------------
# Solve quadratic equations
#-------------------------------------------------------------------------------

def solve_quadratic(a, b, c):
    D = sqrt(b**2 - 4*a*c)
    return (
        (-b + D) / (2 * a),
        (-b - D) / (2 * a)
    )

#-------------------------------------------------------------------------------
# time, distance, acceleration
#-------------------------------------------------------------------------------

# v = a*t

def solve_vat(v, a, t):
    if a == None: return v/float(t)
    if t == None: return v/float(a)
    return a*t

# s = v*t + ½at²
# ½at² + vt - s = 0

def solve_svat(s, v, a, t):
    if t == None: return solve_quadratic(0.5*a, v, -s)[0]
    assert a != None
    assert v != None
    return v*t + a*(t**2) / 2.0

#-------------------------------------------------------------------------------
# Power and Force equations
#-------------------------------------------------------------------------------

def solve_Fma(F, m, a):
    if F == None: return m * a
    if m == None: return float(F) / a
    return float(F) / m

def solve_PFv(P, F, ve):
    if P == None: return F * (0.5 * ve)
    if F == None: return P / (0.5 * ve) # = flow * ve
    return 2.0 * P/F

#-------------------------------------------------------------------------------
# Energy equations
#-------------------------------------------------------------------------------

def solve_Emv(E, m, v = None):
    if m == None: return E/(0.5*(v**2))
    if v == None: return sqrt(2 * E/m)
    return 0.5*m*(v**2)

def solve_Emc(E, m):
    if m == None: return E/(const_c**2)
    return m*(const_c**2)

#-------------------------------------------------------------------------------
# Energy and temperature:
#-------------------------------------------------------------------------------

def solve_StefanBoltzmann(flux, T):
    if(T): return const_sb * (T ** 4)
    return (flux / const_sb) ** (1/4)

#-------------------------------------------------------------------------------
# Solve temperature (K) from flux (x Earth): simplifies calculations with
# stars, where units are based on Sun and Earth.
#-------------------------------------------------------------------------------

def solve_fluxT(flux, T):
    C = const_solar / const_sb
    if(T): return (T ** 4) / C
    return (flux * C) ** (1/4)
