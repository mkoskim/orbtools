#!/usr/bin/env python2
# -*- coding: utf-8 -*-
###############################################################################
#
# How much delta-v is required to a rock, to travel from Mercury surface
# to Earth surface?
#
###############################################################################

from sol import *

def onImpact(name, body, orbit_height):
	mission = Mission(name, Surface(body))
	mission.exit("Impact", orbit_height)
	mission.show()

onImpact("Mars-Earth", "Mars", Earth.orbit.a)
onImpact("Mercury-Earth", "Mercury", Earth.orbit.a)
onImpact("Mercury-Venus", "Mercury", Venus.orbit.a)
onImpact("Mercury exit", "Mercury", Mercury.orbit.a)

