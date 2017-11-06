# -*- coding: utf-8 -*-
################################################################################
#
# Functions for making test cases
#
################################################################################

import os
import traceback

#------------------------------------------------------------------------------

def _getcaller():
    return traceback.extract_stack(None, 3)[0]

#------------------------------------------------------------------------------

def runcase():
    print "Running: %s..." % (_getcaller()[2])

def manual(name, f):
    if name == "__main__": f()

#------------------------------------------------------------------------------

def expect(computed, correct, error, name = None):
    caller   = _getcaller()
    filename = os.path.basename(caller[0])
    line     = caller[1]
    func     = caller[2]
    
    if abs(computed - correct) > error:
        raise Exception("%s:%d: Case '%s %s' failed: %s != %s" % (
            filename, line,
            func, name,
            str(computed),
            str(correct)
        ))
    else:
        print "%s:%d: Case '%s %s' ok." % (filename, line, func, name)

#------------------------------------------------------------------------------

def expectd(diff, error, name = None):
    if diff > error:
        raise Exception("Case '%s' failed: %s != %s" % (
            name,
            str(diff),
            str(error)
        ))

#------------------------------------------------------------------------------
# Relative error as percentage
#------------------------------------------------------------------------------

def error(computed, correct):
    return (abs(correct - computed) / correct) * 100.0

