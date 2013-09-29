#!/usr/bin/env python

import commands
import logging
import os
import subprocess
import sys
import time

import __main__
import config
import data
import debug
import helpers
import nlp
import scraping

logging.basicConfig(filename='./secner/main.log', level=logging.DEBUG)


# Process Tools
def test():
    logging.debug('Running system tests.')
    try:
        data.test(config.NEO4J_SERVER)
        nlp.test()
        scraping.test(config.SEC_SERVER)
        logging.debug('Tests cleared.')
        sys.stdout.write('\n\n\nTests returned positive. All systems ready to go.\n\n\n\n')
    except Exception as e:
        logging.error('System tests returned negative.')
        sys.exit('\n\n\nTests returned negative. Check logs for more details. Here\'s the last error:\n"%s"\n\n' % sys.exc_value)

def setup():
    logging.debug('Running process setup.')
    logging.debug('Changing working directory.')
    os.chdir('./secner')
    graph = data.setup(config.NEO4J_SERVER)
    ftp_server = scraping.setup(config.SEC_SERVER)
    nlp.setup()
    return graph, ftp_server


# Commands
def initialize():
    logging.info('Initializing system.')
    test()
    logging.debug('Requesting init permissions')
    if not helpers.query('Would you like to initiate the process?'): sys.exit('Process stopped by user.')
    if not helpers.query('This action will erase all content on your Neo4j server. Are you sure you would like to continue?'): sys.exit('Process stopped by user.')
    logging.debug('Recieved permission to continue. Running emergency shutdown buffer.')
    sys.stdout.write('Starting')
    for i in range(5):
        sys.stdout.write('.')
        sys.stdout.flush()
        time.sleep(0.75)
    sys.stdout.write('\n\n')
    graph, ftp_server = setup()
    logging.debug('Setup complete.')
    sys.stdout.write('Setup complete.\n\n\n\n')
    scraping.collect_indices(ftp_server)

def refresh(): #TODO
    test()
    if not helpers.query('Would you like to initiate the process?'): sys.exit('Process stopped by user')
    sys.exit('Refresh unprepared for usage.')

def cleanup():
    """For use when an emergency problem causes an unsafe shutdown. Clears out system files and returns to a stable state."""
    logging.info('Cleaning up system.')
    logging.debug('Changing working directory.')
    os.chdir('./secner')
    status = os.system('rm -rf ./bin/indexes/*')

def debugger():
    __main__.flags.append(1234)
    logging.debug('different')
    debug.debug()
    # status, temp = commands.getstatusoutput('touch ./secner/completetest')
    # sys.stdout.write(temp[::-1]+'yolo\n')