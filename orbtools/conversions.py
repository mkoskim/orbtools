###############################################################################
#
# Unit conversions. Internally, orbtools uses:
#
# - Mass: 	GM (G*kg)
# - Distance:	m
# - Time: 	s
# - Speed:	m/s
#
###############################################################################

from math import *
from constants import *

#------------------------------------------------------------------------------
# Time
#------------------------------------------------------------------------------

def TasDHMS(d, h, m, s):    return d*24*3600.0 + h*60*60.0 + m*60.0 + s
def TasDays(d):             return float(d)*24*3600
def TasYears(a):            return float(a)*const_year

def TtoMinutes(secs):   return secs/(60.0)
def TtoHours(secs):     return secs/(3600.0)
def TtoDays(secs):      return secs/(24*3600.0)
def TtoWeeks(secs):     return TtoDays(secs)/7
def TtoMonths(secs):    return TtoDays(secs)/30
def TtoYears(secs):     return TtoDays(secs)/365.25

#------------------------------------------------------------------------------
# Mass
#------------------------------------------------------------------------------

def GM2kg(GM): return float(GM)/const_G
def kg2GM(kg): return float(kg)*const_G

def MtoSun(GM): return float(GM)/GM_Sun
def MtoEarth(GM): return float(GM)/GM_Earth

def MasSun(m): return float(m) * GM_Sun
def MasJupiter(m): return float(m) * GM_Jupiter
def MasEarth(m): return float(m) * GM_Earth

#------------------------------------------------------------------------------
# Radius
#------------------------------------------------------------------------------

def RtoSun(R): return float(R) / r_Sun
def RtoEarth(R): return float(R) / r_Earth

def RasSun(R): return float(R) * r_Sun
def RasEarth(R): return float(R) * r_Earth

#------------------------------------------------------------------------------
# Distance
#------------------------------------------------------------------------------

def AU2m(AU):   return float(AU)*const_AU
def m2AU(m):    return float(m)/const_AU
def ly2m(ly):   return float(ly)*const_ly
def m2ly(m):    return float(m)/const_ly

#------------------------------------------------------------------------------
# Speed
#------------------------------------------------------------------------------

def MACH2ms(mach): return mach*343.0
def ms2MACH(ms):   return ms/343.0
def fts2ms(fts):   return fts*0.3048
def ms2fts(ms):    return ms/0.3048

#------------------------------------------------------------------------------
# Angles
#------------------------------------------------------------------------------

def deg2rad(d): return radians(d)
def rad2deg(r): return degrees(r)

#------------------------------------------------------------------------------
# ISP <-> ve
#------------------------------------------------------------------------------

def Isp2ve(isp): return const_g * float(isp)
def ve2Isp(ve):  return float(ve) / const_g

