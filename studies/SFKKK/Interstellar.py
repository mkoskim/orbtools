###############################################################################
#
# Interstellar traveling studies
#
###############################################################################

import os, sys
sys.path.append(os.path.abspath("."))

from sol import *

#------------------------------------------------------------------------------

ACentauriA = Star("a Centauri A", 1.1)

v_travel = 0.10 * const_c

o_start = Orbit(Sun, AU2m(1.0))
o_end   = Orbit(ACentauriA, AU2m(1.0))

#------------------------------------------------------------------------------

def show_orbit(o):
    print "%s @ %.2f AU, v_escape = %.0f - %.0f = %.0f" % (
        o.center.name,
        m2AU(o.a),
        o.center.v_escape(o.a),
        abs(o.v()),
        o.center.v_escape(o.a) - abs(o.v())
    )

show_orbit(o_start)
show_orbit(o_end)

#------------------------------------------------------------------------------

v_exit  = solve_rvrv(Sun.GM,        AU2m(1.0), None, Inf, v_travel)
v_enter = solve_rvrv(ACentauriA.GM, Inf, v_travel,   AU2m(1.0), None)

v_tot = 2 * v_travel

#------------------------------------------------------------------------------

#print v_travel / 1000, "km/s"
#print v_exit / 1000, "km/s", abs(o_start.v()) / 1000
#print v_enter / 1000, "km/s", abs(o_end.v()) / 1000

print v_travel / 1000, "km/s", v_tot / 1000, "km/s"

#------------------------------------------------------------------------------

def nuclear_fuel(fuel, ratio, dv_tot):
    ve60 = fuel.ve(ratio/100.0, 0.60)
    print "%s %5.1f %% @ %s: R = %.2f" % (
        fuel.name, ratio,
        fmteng(ve60, "m/s"),
        solve_rocket_eq(None, 1.0, dv_tot, ve60),
    )


#nuclear_fuel(fuels["Th232"],    1.0)
#nuclear_fuel(fuels["D-D"],      1.0)
#nuclear_fuel(fuels["D-T"],      1.0)
nuclear_fuel(fuels["D-He3"],    1.0, v_tot)
nuclear_fuel(fuels["D-He3"],    5.0, v_tot)
nuclear_fuel(fuels["D-He3"],   20.0, v_tot)
nuclear_fuel(fuels["!H"],       0.1, v_tot)
nuclear_fuel(fuels["!H"],       1.0, v_tot)

#------------------------------------------------------------------------------
# Computing parameters for selected drive
#------------------------------------------------------------------------------

ve60 = Engine(
    ve   = fuels["!H"].ve(0.01, 0.60),
    P    = 1e12 * 0.60,
    name = "Antimateria 1%",
)

ve60.E_in  = fuels["!H"].E * 0.01
ve60.E_out = ve60.E()

print "v_ex =", ve60.ve/1000, "km/s"
print "P_in =", fmteng(ve60.E_in, "J/kg")

M_dec = ve60.fuel(100e3,         v_travel)
M_acc = ve60.fuel(100e3 + M_dec, v_travel)
M_tot = M_acc + M_dec

print "M(1), M(2), M(tot):", M_acc / 1000, M_dec / 1000, M_tot / 1000
print "t(1), t(2), t(tot):", fmttime(ve60.t(M_acc)), fmttime(ve60.t(M_dec)), fmttime(ve60.t(M_tot))
print "mass flow =", ve60.flow
print "a (1) =", v_travel / ve60.t(M_acc)
print "a (2) =", v_travel / ve60.t(M_dec)

