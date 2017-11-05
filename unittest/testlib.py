# -*- coding: utf-8 -*-
################################################################################
#
# Functions for making test cases
#
################################################################################

def expect(computed, correct, error, name = None):
	diff = abs(computed-correct)
	if diff > error:
		raise Exception("Case '%s' failed: %s != %s" % (
		    name,
		    str(computed),
		    str(correct)
		))

