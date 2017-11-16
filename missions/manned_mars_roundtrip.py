################################################################################
#
# Orbital toolbox: Mission to Mars
#
################################################################################

import sys, os
sys.path.append(os.path.abspath(".."))

from sol import *

import ApolloMission

#-------------------------------------------------------------------------------
# Designing roundtrip: Earth (LEO) - Mars - Earth
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
# Orbits involved to mission
#-------------------------------------------------------------------------------

EarthLEO = Altitude(Earth,300e3)

MarsLMO = Altitude(Mars,1000e3)
MarsSurface = Surface(Mars)

#-------------------------------------------------------------------------------
# Transfers
#-------------------------------------------------------------------------------

Mars_Takeoff = Mission("Mars Takeoff", MarsSurface)
Mars_Takeoff.burn("Ascent/1", Trajectory(Mars, MarsSurface.r(0), MarsLMO.r(0.5)))
Mars_Takeoff.park("Ascent/2", MarsLMO)

#-------------------------------------------------------------------------------
# Apollo Lunar Ascent stage: dry mass = 2,150 kg
# APS engine, Isp 311 s
#-------------------------------------------------------------------------------

APS = Exhaust(Isp2ve(311))
Moon_Takeoff = ApolloMission.phase42

Mars_Takeoff.show()
Moon_Takeoff.show()

print "Ascent vehicle, dry mass 2150 kg"
print "Moon: fuel=", APS.fuel(2150, Moon_Takeoff.dv), "tot=", APS.solve(None, 2150, Moon_Takeoff.dv)
print "Mars: fuel=", APS.fuel(2150, Mars_Takeoff.dv), "tot=", APS.solve(None, 2150, Mars_Takeoff.dv)
print "Earth: fuel=", APS.fuel(2150, 9000), "tot=", APS.solve(None, 2150, 9000)

exit()

Earth_Surface2LEO = Transfer(EarthSurface, EarthLEO)

TMI_ToLMO     = Transfer(EarthLEO, MarsLMO)
TMI_ToSurface = Transfer(EarthLEO, MarsSurface)

Mars_Surface2LMO = Transfer(MarsSurface, MarsLMO)

TEI = Transfer(MarsLMO,EarthSurface)

#-------------------------------------------------------------------------------
# Payloads
#-------------------------------------------------------------------------------

SpaceHab = Payload(30e3)
MarsHab = Payload(30e3)
MarsLauncher = Payload(10e3)
EarthReturnVehicle = Payload(10e3)

#-------------------------------------------------------------------------------
# Engines
#-------------------------------------------------------------------------------

LH2Engine   = Engine(4400)
SolidEngine = Engine(2500)
IonEngine   = Engine(10000)

#-------------------------------------------------------------------------------
# Stages (from last to first)
#-------------------------------------------------------------------------------

Stage1 = Stage(
    "Earth Return..",
    SpaceHab.mass + EarthReturnVehicle.mass,
    IonEngine,
    abs(TEI.dv1))

Stage2 = Stage(
    "Mars Launcher.",
    MarsLauncher.mass,
    SolidEngine,
    abs(Mars_Surface2LMO.dv1) + abs(Mars_Surface2LMO.dv2))

Stage3 = Stage(
    "Mars Surface..",
    MarsHab.mass + Stage2.mass,
    IonEngine,
    abs(TMI_ToSurface.dv2))

Stage4 = Stage(
    "Mars orbiter..",
    Stage1.mass,
    IonEngine,
    abs(TMI_ToLMO.dv2))

Stage5 = Stage(
    "Trans-Mars....",
    Stage3.mass + Stage4.mass,
    IonEngine,
    abs(TMI_ToLMO.dv1))

Stage6 = Stage(
    "LEO Launcher..",
    Stage5.mass,
    LH2Engine,
    abs(Earth_Surface2LEO.dv1) + abs(Earth_Surface2LEO.dv2))

#-------------------------------------------------------------------------------
# Show rocket stage statistics
#-------------------------------------------------------------------------------

#Stage6.printOut()
#Stage5.printOut()
#Stage4.printOut()
#Stage3.printOut()
#Stage2.printOut()
#Stage1.printOut()

print
t = Transfer(Altitude("Earth",300e3), Altitude("Mars", 1000e3))
print "Earth-Mars...: dv1=",fmteng(t.dv1,"m/s"), "dv2=", fmteng(t.dv2,"m/s"), "T=", fmttime(t.hohmann.P()/2)
t = Transfer(Altitude("Earth",300e3), Altitude("Venus", 1000e3))
print "Earth-Venus..: dv1=",fmteng(t.dv1,"m/s"), "dv2=", fmteng(t.dv2,"m/s"), "T=", fmttime(t.hohmann.P()/2)
t = Transfer(Altitude("Earth",300e3), Altitude("Europa", 1000e3))
print "Earth-Europa.: dv1=",fmteng(t.dv1,"m/s"), "dv2=", fmteng(t.dv2,"m/s"), "T=", fmttime(t.hohmann.P()/2)
t = Transfer(Altitude("Earth",300e3), Altitude("Neptune", 1000e3))
print "Earth-Neptune: dv1=",fmteng(t.dv1,"m/s"), "dv2=", fmteng(t.dv2,"m/s"), "T=", fmttime(t.hohmann.P()/2)
print

print
print "P(Earth)...:", fmteng(Earth.orbit.P()/(24*60*60), "d")
print "o(Earth)...: %.3f o/d" % (Earth.orbit.w()*24*60*60)
print "P(Mars)....:", fmteng(Mars.orbit.P()/(24*60*60), "d")
print "o(Earth)...: %.3f o/d" % (Mars.orbit.w()*24*60*60)
print "o(diff)....: %.3f o/d" % ((Earth.orbit.w() - Mars.orbit.w())*24*60*60)

t = Transfer(
    Altitude(Earth, 300e3),
    #Altitude("Moon", 300e3),
    #Altitude("Phobos", 2e3)	
    Altitude(Mars, 1000e3)
	#Altitude("Venus",1000e3)
    )

hohmann = t.hohmann
Tref = 0
print
print "Earth-Mars...:"
print "   Department: T = %.2f" % (Tref)
print "   Arrive....: T = %.2f" % (Tref + TtoYears(hohmann.P()/2))
print "Mars-Earth...:"
print "   Department: T = %.2f" % (Tref + TtoYears(hohmann.P()/2 + hohmann.T_up2dn()))
print "   Arrive....: T = %.2f" % (Tref + TtoYears(hohmann.P() + hohmann.T_up2dn()))
print
print "P(Earth).....: P = %.2f d" % TtoDays(Earth.orbit.P())
print "P(Mars)......: P = %.2f d" % TtoDays(Mars.orbit.P())
print "Window.......: P = %.2f m" % TtoMonths(hohmann.P_window())
print "Angle up.....: a = ", hohmann.launch_angle_up()
print "Angle @ Mars.: a = ", hohmann.launch_angle_up() - hohmann.w_diff()*hohmann.P()/2
print "Angle down...: a = ", hohmann.launch_angle_down()
print
print "dv(1) = ", t.dv1
print "dv(2) = ", t.dv2

#t = Transfer(Earth.orbit, Venus.orbit)
#print
#print "Earth-Jupiter: T = ", fmttime(t.hohmann.P()/2)
#print "Window.......: P = ", fmttime(t.hohmann.P_window())
#print "Launch angle.: Up = ", t.hohmann.launch_angle_up()
#print "Launch angle.: Dn = ", t.hohmann.launch_angle_down()
#t.hohmann.T_up_to_down()

#-------------------------------------------------------------------------------
# High Energy Transfers, Earth-Mars
#-------------------------------------------------------------------------------

Earth = masses["Earth"]
Mars = masses["Mars"]

for mult in [
	(1.0, 1.0),
	(1.0, 2.0),
	(1.0, 4.0),
	(1.0, 8.0),
	(0.5, 2.0),
	(0.5, 4.0)
	]:
	mlo, mhi = mult
	t = Trajectory("Sun", Earth.orbit.a(), Mars.orbit.a(),
		mlo*Earth.orbit.a(), mhi*Mars.orbit.a())
	T = t.T_to_target()
	print "dv=%14s" % fmteng(abs(t.v_exit()) + abs(t.v_enter()), "m/s"), "AU:%7.2f - %7.2f" % (m2AU(t.r1), m2AU(t.r2)), "T=", fmttime(T), "(r=%s)" % fmteng(t.pos_fr(T)[1],"m")



