# -*- coding: utf-8 -*-
###############################################################################
#
# Support for data plotting (GNUplot)
#
###############################################################################

import string
from orbtools.misc import *

#------------------------------------------------------------------------------
# Dump data (two-dimensional list of values) to a file for plotting
#------------------------------------------------------------------------------

def dumpdata(filename, data, separator = " "):
	f = open(filename, "w")
	for record in data:
		print>>f, string.join(map(lambda d: str(d), record), separator)
	f.close()

#------------------------------------------------------------------------------
# Plot data files
#------------------------------------------------------------------------------

def plot(directory, cmdfile):
	system("cd %s; gnuplot %s" % (directory, cmdfile))

#def plotPNG(directory, cmdfile):
#	system("cd %s; gnuplot %s" % (directory, cmdfile))

