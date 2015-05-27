###############################################################################
#
# Orbtools unit test, using J. Kaukoranta's calculations
#
###############################################################################

from orbtools.systems.solsystem import *

#------------------------------------------------------------------------------
# LEO 300 km -> LMO 1000 km
#------------------------------------------------------------------------------

LEO = masses["Earth300km"]
LMO = Mass("LMO1000km",0,0,0,Altitude(Mars, 1000e3))

Earth2Mars = Mission("Earth - Mars", LEO.orbit)

Earth2Mars.exit ("TMI", Mars.orbit.a)
Earth2Mars.enter("MOI", LMO.orbit)

print "Earth - Mars"
print "    %.0f" % Earth2Mars.burns[1].dv, "==", 3590
print "    %.0f" % Earth2Mars.burns[2].dv, "==", 2028

#------------------------------------------------------------------------------
# LEO 300 km -> LVO 1000 km
#------------------------------------------------------------------------------

LVO = Mass("LVO1000km",0,0,0,Altitude(Venus, 1000e3))
Earth2Venus = Mission("Earth - Venus", LEO.orbit)
Earth2Venus.exit("TVI", Venus.orbit.a)
Earth2Venus.enter("VOI", LVO.orbit)

print "Earth - Venus"
print "    %.0f" % Earth2Venus.burns[1].dv, "==", 3481
print "    %.0f" % Earth2Venus.burns[2].dv, "==", 3186


