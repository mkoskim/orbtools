###############################################################################
#
# Print formats
#
###############################################################################

from orbtools import *

#------------------------------------------------------------------------------
# Engineering prints (exp = multiply of three)
#------------------------------------------------------------------------------

def fmteng(val, unit):
    a = abs(val)
    if(a >= 1e+18): return "%.3f E%s" % (val/1e+18, unit)
    if(a >= 1e+15): return "%.3f P%s" % (val/1e+15, unit)
    if(a >= 1e+12): return "%.3f T%s" % (val/1e+12, unit)
    if(a >= 1e+09): return "%.3f G%s" % (val/1e+09, unit)
    if(a >= 1e+06): return "%.3f M%s" % (val/1e+06, unit)
    if(a >= 1e+03): return "%.3f k%s" % (val/1e+03, unit)
    if(a >= 1e+00): return "%.3f %s" % (val/1e+00, unit)
    if(a >= 1e-03): return "%.3f m%s" % (val/1e-03, unit)
    if(a >= 1e-06): return "%.3f u%s" % (val/1e-06, unit)
    if(a >= 1e-09): return "%.3f n%s" % (val/1e-09, unit)
    if(a >= 1e-12): return "%.3f p%s" % (val/1e-12, unit)
    if(a >= 1e-15): return "%.3f f%s" % (val/1e-15, unit)
    return "%.3f a%s" % (val/1e-18, unit)

#------------------------------------------------------------------------------
# Distance prints
#------------------------------------------------------------------------------

def fmtdist(val):
	if(val < AU2m(0.1)): return "%.2f km" % (val*1e-3)
	return "%.2f AU" % m2AU(val)

#------------------------------------------------------------------------------
# Time prints
#------------------------------------------------------------------------------

def fmttime(val):
	if(val <         	1): return "0.00 s"
	if(val <           90): return fmteng(val,"s")
	if(val <       120*60): return "%.2f m" % (val/60)
	if(val <   3*24*60*60): return "%.2f h" % (val/3600)
	if(val < 600*24*60*60): return "%.2f d" % TtoDays(val)
	return fmteng(TtoYears(val), "a")

