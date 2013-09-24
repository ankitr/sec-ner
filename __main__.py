#!/usr/bin/env python

import sys

from processes import *

__author__ = 'Ankit Ranjan (me@ankit.io)'
__version__ = 'v0.0.1'

COMMANDS = {
    'init':'initialize',
    'refresh':'refresh',
    'debug':'debug'
}

#TODO: Make this more robust an initialization

try:
    eval(COMMANDS[sys.argv[1]])()
except IndexError:
    sys.exit('usage: python secner <command>\n\nThe most common commands are:\n\tinit\t\tInitialize the network. This is a long process that is memory and time intensive.\n\trefresh\t\tStarts a refresh loop, and runs the process every 24 hours. Should be run as a cron job on a server.\n')
except KeyError:
    sys.exit('\'%s\' is an invalid command.\n\nusage: python secner <command>\n\nThe most common commands are:\n\tinit\t\tInitialize the network. This is a long process that is memory and time intensive.\n\trefresh\t\tStarts a refresh loop, and runs the process every 24 hours. Should be run as a cron job on a server.\n' % sys.argv[1])