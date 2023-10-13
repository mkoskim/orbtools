# -*- coding: utf-8 -*-
################################################################################
#
# Running unit test to package, comparing results to known calculations
#
################################################################################

import os, sys
sys.path.append(os.path.abspath(".."))

#from sol import *
from testlib import *

################################################################################
#
# Tähtitieteen perusteet (Fundamentals of Astronomy)
#
################################################################################

# s. 164
expect( v_elliptical(GM_Sun, AU2m(1.568), AU2m(1.17)), 30800, 50)

expect( P_orbit(kg2GM(5+5), 1.0), 243000, 500 )
expect( Orbit(Mass("Bricks", kg2GM(5+5), 0, 0), 1.0).P, 243000, 500 )

################################################################################
#
# Miscellaneous: sanity checks etc
#
################################################################################

expect( Earth.g_surface, 9.81, 0.02 )
expect( Earth.v_escape(), 11100, 100)

################################################################################
#
# Taivaanmekaniikan materiaali (Juhani Kaukoranta)
#
################################################################################

#------------------------------------------------------------------------------
# LEO 300 km -> LMO 1000 km
#------------------------------------------------------------------------------

def Kaukoranta_EarthMars():
	LEO = masses["Earth300km"]
	LMO = Mass("LMO1000km", orbit = Altitude(Mars, 1000e3))

	Earth2Mars = Mission("Earth - Mars", LEO.orbit)

	Earth2Mars.exit ("TMI", Mars.orbit)
	Earth2Mars.enter("MOI", LMO.orbit)

	expect(Earth2Mars.burns[1].dv, 3590, 5)
	expect(Earth2Mars.burns[2].dv, 2028, 5)

Kaukoranta_EarthMars()

#------------------------------------------------------------------------------
# LEO 300 km -> LVO 1000 km
#------------------------------------------------------------------------------

def Kaukoranta_EarthVenus():
	LEO = masses["Earth300km"]
	LVO = Mass("LVO1000km",0,0,0,Altitude(Venus, 1000e3))

	Earth2Venus = Mission("Earth - Venus", LEO.orbit)
	Earth2Venus.exit("TVI", Venus.orbit)
	Earth2Venus.enter("VOI", LVO.orbit)

	expect(Earth2Venus.burns[1].dv, 3481, 5)
	expect(Earth2Venus.burns[2].dv, 3186, 5)

Kaukoranta_EarthVenus()

