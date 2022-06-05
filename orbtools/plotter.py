# -*- coding: utf-8 -*-
###############################################################################
#
# Orbit plotter
#
###############################################################################

from orbtools.misc import *
from math import *

import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots()

#------------------------------------------------------------------------------

ax.set_aspect('equal')
ax.scatter([0], [0])

#------------------------------------------------------------------------------

rot = -90

#------------------------------------------------------------------------------

scaling = 0

def arrow_args(): return {
	"length_includes_head": True,
	"head_length": scaling * 0.075,
	"head_width":  scaling * 0.1 * 0.5,
}

#------------------------------------------------------------------------------

def getXY(orbit, t):
	return orbit.xy(t).rotate(rot)

def getV(orbit, t):
	return orbit.v(t).rotate(rot)

def getPath(orbit, t1=0.0, t2=1.0):
	xy = [getXY(orbit, t) for t in np.linspace(t1, t2, 50, endpoint=True)]
	x  = [p.x for p in xy]
	y  = [p.y for p in xy]
	return x, y

#------------------------------------------------------------------------------

def annotate(txt, x, y, offset = (0, 5)):
	ax.annotate(txt, xy=(x, y), xytext=offset, textcoords="offset points")

def center(center):
	annotate(center.name, 0, 0)

def linep(x1, y1, x2, y2, color = None, style=None, width=None):
	return plt.plot([x1, x2], [y1, y2],
		color = color,
		linestyle = style,
		linewidth = width,
	)

def lined(x, y, dx, dy, color = None, style = None):
	return linep(x, y, x + dx, x + dy,
		color=color,
		style=style,
	)

def arrowd(x, y, dx, dy, color = None):
	return plt.arrow(x, y, dx, dy,
		color=color,
		**arrow_args(),
	)

def arrowp(x1, y1, x2, y2, color = None):
	return arrowd(x1, y1, x2 - x1, y2 - y1,
		color = color
	)

#------------------------------------------------------------------------------

def orbit(orbit, color="grey", style="dashed", width=1):
	global scaling
	scaling = max(scaling, orbit.a)
	x, y = getPath(orbit)
	ax.plot(x, y, color = color, linestyle = style, linewidth = width)

def travel(orbit, t1, t2, color=None, style=None):
	x, y = getPath(orbit, t1, t2)
	ax.plot(x[:-1], y[:-1], color=color, linestyle=style)

	arrowp(x[-2], y[-2], x[-1], y[-1], color=color)

def mark(orbit, t, color=None):
	p = getXY(orbit, t)
	ax.scatter(p.x, p.y,
		color=color
	)

def event(orbit, t, txt, offset=(0, 5)):
	p = getXY(orbit, t)
	#ax.scatter(p.x, p.y)
	annotate(txt, p.x, p.y, offset)

def speed(orbit, t, scale = 1.0, color=None):
	p = getXY(orbit, t)
	v = getV(orbit, t) * scale

	arrowd(p.x, p.y, v.x, v.y,
		color=color
	)

def speedmark(orbit, t, scale=1.0, color=None):
	mark(orbit, t, color=color)
	speed(orbit, t, scale=scale, color=color)

def pos(orbit, t, color=None, style=None):
	p = getXY(orbit, t)
	linep(0, 0, p.x, p.y, color=color,style=style)

def slice(orbit, t1, t2, color=None):
	pos(orbit, t1, color)
	pos(orbit, t2, color)
	travel(orbit, t1, t2, color)

#------------------------------------------------------------------------------

def show():
	plt.show()
