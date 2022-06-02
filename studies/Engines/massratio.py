#!/usr/bin/env python3
###############################################################################
#
# Mass ratio (R) related to delta-v and ve
#
###############################################################################

import os, sys
sys.path.append(os.path.abspath("."))

from orbtools.systems.solsystem import *
from orbtools.systems.exoplanets import *

#------------------------------------------------------------------------------

def calc(k):
  if not k:
    print("%7s %12s" % ("k", "R-1"))
    return
  print("%7.2f %12.2f" % (k, exp(k)-1))

for k in [None, 0.25, 0.5, 1.0, 2.0, 3.0, 5.0, 10.0, 20.0]:
  calc(k)

F9_payload = 22.8
F9_dry = 22 + 4 + F9_payload
F9_full = 400 + 100 + F9_dry

print("Falcon-9: dry=%.2f full=%.2f R=%.2f" % (F9_dry, F9_full, F9_full / F9_dry))
