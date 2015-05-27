################################################################################
#
# Kerbal System Database: Orbital calculation toolbox
#
################################################################################

from orbtools.orbmath import *
from orbtools.general import *

################################################################################
#
# Sun & planets
#
################################################################################

#-------------------------------------------------------------------------------
#    Name       Mass        	Radius      Sid. P		Orbit			Distance
Mass("Sun",		kg2GM(1.76e28),	261600e3,	432000)
Mass("Moho",	kg2GM(2.53e21),	250e3,		1210000,	Orbit("Sun", 	5263138304))
Mass("Eve",		kg2GM(1.23e23),	700e3,		80500,		Orbit("Sun", 	9832684544))
Mass("Gilly",	kg2GM(1.24e17),	13e3,		28255,		Orbit("Eve", 	31500000))
Mass("Kerbin",	kg2GM(5.29e22),	600e3,		21600,		Orbit("Sun", 	13599840256))
Mass("Mun",		kg2GM(9.77e20),	200e3,		"S",		Orbit("Kerbin",	12000000))
Mass("Minmus",	kg2GM(2.65e19),	60e3,		40400,		Orbit("Kerbin",	47000000))
Mass("Duna",	kg2GM(4.52e21),	320e3,		65518,		Orbit("Sun", 	20726155264))
Mass("Ike",		kg2GM(2.78e20),	130e3,		"S",		Orbit("Duna", 	3200000))
Mass("Dres",	kg2GM(3.22e20),	138e3,		34800,		Orbit("Sun", 	40839348203))
Mass("Jool",	kg2GM(4.24e24),	6000e3,		36000,		Orbit("Sun", 	68773560320))
Mass("Laythe",	kg2GM(2.94e22),	500e3,		"S",		Orbit("Jool", 	27184000))
Mass("Vall",	kg2GM(3.11e21),	300e3,		"S",		Orbit("Jool", 	43152000))
Mass("Tylo",	kg2GM(4.24e22),	600e3,		"S",		Orbit("Jool", 	68500000))
Mass("Bop",		kg2GM(3.73e19),	65e3,		"S",		Orbit("Jool", 	128500000))
Mass("Pol",		kg2GM(1.08e19),	44e3,		"S",		Orbit("Jool", 	179890000))
Mass("Eeloo",	kg2GM(1.12e21),	210e3,		19460,		Orbit("Sun", 	90118820000))

Sun = masses["Sun"]
Moho = masses["Moho"]
Eve = masses["Eve"]
Kerbin = masses["Kerbin"]
Mun = masses["Mun"]
Duna = masses["Duna"]
Dres = masses["Dres"]
Jool = masses["Jool"]
Eeloo = masses["Eeloo"]

