###############################################################################
#
# Delta-v calculations for Apollo-Saturn hardware
#
###############################################################################

import os, sys
sys.path.append(os.path.abspath(".."))

from sol import *

import ApolloMission as Mission

###############################################################################
#
# Apollo LM
#
# http://en.wikipedia.org/wiki/Apollo_Lunar_Module
#
# 	Ascent Stage		 4,700 kg
#	Descent Stage		10,334 kg
#
###############################################################################

APS_engine = Exhaust(Isp2ve(311))
DPS_engine = Exhaust(Isp2ve(311))

LM = Rocket(
    "LM Descent",
    Stage("LM Ascent",  APS_engine, mass =  4700, fuel = 2353, mission = Mission.phase42),
    Stage("LM Descent", DPS_engine, mass = 10334, fuel = 8200, mission = Mission.phase41)
)

###############################################################################
#
# Apollo CSM
#
# http://en.wikipedia.org/wiki/Apollo_Command/Service_Module
# http://en.wikipedia.org/wiki/Trans-Earth_injection
#
# 	Command Module CM-107		 5,560 kg (no dv)
# 	Service Module SM-107		24,520 kg (18,410 kg prop)
#
###############################################################################

AJ10_engine = Exhaust(Isp2ve(319))	# CSM

#------------------------------------------------------------------------------
# CSM TEI: CM + SM structural mass + propellant for TEI
#------------------------------------------------------------------------------

CSM_TEI = Stage(
    "CSM TEI",
    AJ10_engine,
    payload = (					
        5560 +		# - Command Module
        (24520-18410)	# - SM (empty)
    ),
    dv = 1076,
    mission = Mission.phase5
)

#------------------------------------------------------------------------------
# CSM LOI: CSM TEI + LM + rest CSM propellant (i.e. CSM + LM)
#------------------------------------------------------------------------------

CSM_LOI = Stage(
	"CSM LOI",
	AJ10_engine,
	payload = CSM_TEI.mass + LM.mass,
	fuel    = 18410 - CSM_TEI.fuel,
	mission = Mission.phase3
)	

CSM = CSM_LOI

###############################################################################
#
#        F1            J2
# ISP    263           421.00
# mass   8,353 kg      1,788 kg
#
###############################################################################

F1_engine = Exhaust(Isp2ve(264.72))
J2_engine = Exhaust(Isp2ve(421.00))

S_IVB = Stage("S-IVB", J2_engine, mass =  120.80e3, payload =  10e3)
S_II  = Stage("S-II",  J2_engine, mass =  480.00e3, payload =  36e3)
S_IC  = Stage("S-IC",  F1_engine, mass = 2300.00e3, payload = 131e3)

SaturnV_upper = Rocket(
	"Saturn V (upper)",
	Payload("CSM+LM", CSM.mass),
	S_IVB,
	mission = Mission.phase2
)

SaturnV_lower = Rocket(
	"Saturn V (lower)",
	Payload("Saturn V (upper)", SaturnV_upper.mass),
	S_II,
	S_IC,
	mission = Mission.phase1
)

if __name__ == "__main__":
    SaturnV_lower.show()
    print "***"
    SaturnV_upper.show()
    print "***"
    CSM_LOI.show()
    print "***"
    CSM_TEI.show()
    print "***"
    LM.show()

