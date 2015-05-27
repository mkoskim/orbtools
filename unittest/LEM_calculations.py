from orbtools import *
from orbtools.systems.solsystem import *
from orbtools.spaceships import *

LEM_engine = Engine(3050)
LEM1 = Stage("LEM ascend", LEM_engine, 4700, None, 2353)				# 2220
LEM2 = Stage("LEM descent", LEM_engine, 10334 + LEM1.mass, None, 8200)	# 2500

LEM1.printOut()
LEM2.printOut()

Moon = masses["Moon"]
LLO = Altitude(Moon, 100e3)
SLO = Surface(Moon)

print "LLO 100 km, v =", LLO.v().length()

