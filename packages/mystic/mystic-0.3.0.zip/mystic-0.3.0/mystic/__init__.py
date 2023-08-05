#!/usr/bin/env python
#
# Author: Mike McKerns (mmckerns @caltech and @uqfoundation)
# Author: Alta Fang (altafang @caltech and alta @princeton)
# Author: Patrick Hung (patrickh @caltech)
# Copyright (c) 1997-2016 California Institute of Technology.
# License: 3-clause BSD.  The full license text is available at:
#  - http://trac.mystic.cacr.caltech.edu/project/mystic/browser/mystic/LICENSE

# get version numbers, license, and long description
try:
    from info import this_version as __version__
    from info import readme as __doc__, license as __license__
except ImportError:
    msg = """First run 'python setup.py build' to build mystic."""
    raise ImportError(msg)

__author__ = 'Mike McKerns'

__doc__ = """
""" + __doc__

__license__ = """
""" + __license__

__all__ = ['solvers', 'termination', 'strategy', 'munge', 'tools', \
           'constraints', 'penalty', 'coupler', 'symbolic', 'monitors', \
           'support', 'model_plotter', 'log_reader', 'collapse_plotter']

# solvers
import solvers

# strategies, termination conditions
import termination
import strategy

# constraints and penalties
import constraints
import penalty
import coupler
import symbolic

# monitors, function wrappers, and other tools
import monitors
import munge
import tools

# scripts
from scripts import model_plotter, log_reader, collapse_plotter
import support

# backward compatibility
from tools import *


def license():
    """print license"""
    print __license__
    return

def citation():
    """print citation"""
    print __doc__[-526:-123]
    return

# end of file
