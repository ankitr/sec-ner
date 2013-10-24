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
    except:
        logging.error('System tests returned negative.')
        logging.debug(type(sys.exc_type))
        logging.debug(str(sys.exc_type))
        logging.error('%s:%s' % (sys.exc_type, sys.exc_value))
        sys.exit('\n\n\nTests returned negative. Check logs for more details. Here\'s the last error:\n"%s:%s"\n\n' % (sys.exc_type, sys.exc_value))

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
    if not helpers.query('Would you like to initiate the process?'):
        logging.debug('User did not permit running the service.')
        sys.exit('Process stopped by user.')
    if not helpers.query('This action will erase all content on your Neo4j server. Are you sure you would like to continue?'):
        logging.debug('User did not give permission to delete Neo4j content.')
        sys.exit('Process stopped by user.')
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
    scraping.initiate_indexes(ftp_server)
    #TODO: Run NLP

def reinitialize():
    logging.info('Reinitializing system.')
    stdout('REINITIALIZING SYSTEM\n\n\n')
    test()
    logging.debug('Requesting init permissions')
    if not helpers.query('Would you like to initiate the process?'):
        logging.debug('User did not permit running the service.')
        sys.exit('Process stopped by user.')
    if not helpers.query('This action will erase all content on your Neo4j server. Are you sure you would like to continue?'):
        logging.debug('User did not give permission to delete Neo4j content.')
        sys.exit('Process stopped by user.')

def refresh(): #TODO
    logging.info('Refreshing.')
    test()
    sys.exit('Refresh unprepared for usage.')

def clean_up():
    """For use when an emergency problem causes an unsafe shutdown. Clears out system files and returns to a stable state."""
    logging.info('Cleaning up system.')
    logging.debug('Changing working directory.')
    os.chdir('./secner/bin/')
    logging.debug('Requesting permission to continue.')
    if not helpers.query('Note that running this proccess will result in deletion of potentially valuable content. Are you absolutely sure you would wish to proceed?'):
        logging.debug('User did not permit running the service.')
        sys.exit('Process stopped by user.')
    logging.debug('Permission recieved. Continuing with process.')
    if os.path.exists('./indexes/'):
        logging.debug('Clearing indexes.')
        status = os.system('rm -rf ./indexes/')
        if status == 256:
            logging.error('User is not authorized to clear indexes.')
            sys.exit('Permission denied. Please run from a super user state. (Maybe sudo python secner [command]%s if you\'re an admin)\n' % (' inspect' if __main__.inspect else str()))
        elif status != 0:
            logging.error('Something went wrong while clearing the indexes directory.')
            sys.exit('Something went wrong while clearing the indexes directory.\n')
    if os.path.exists('./tests/'):
        logging.debug('Clearing tests.')
        status = os.system('rm -rf ./tests/*')
        if status == 256:
            logging.error('User is not authorized to clear tests.')
            sys.exit('Permission denied. Please run from a super user state. (Maybe sudo python secner [command]%s if you\'re an admin)\n' % (' inspect' if __main__.inspect else str()))
        elif status != 0:
            logging.error('Something went wrong while clearing the tests directory.')
            sys.exit('Something went wrong while clearing the tests directory.\n')
    if os.path.exists('./.secner-helpers/'):
        logging.debug('Clearing secner-helpers.')
        status = os.system('rm -rf ./secner-helpers/*')
        if status == 256:
            logging.error('User is not authorized to clear secner-helpers.')
            sys.exit('Permission denied. Please run from a super user state. (Maybe sudo python secner [command]%s if you\'re an admin)\n' % (' inspect' if __main__.inspect else str()))
        elif status != 0:
            logging.error('Something went wrong while clearing the secner-helpers directory.')
            sys.exit('Something went wrong while clearing the secner-helpers directory.\n')
    try: data.clean(config.NEO4J_SERVER)
    except:
        logging.error('Something went wrong while clearing the Neo4j server.')
        logging.exception(sys.exc_type+':'+sys.exc_value)
        sys.exit('Something went wrong while clearing the Neo4j server. Check logs for details.')
    logging.debug('Clearing complete.')
    sys.exit('System cleaned. Factory state returned.')

def clear_logs():
    """Clears the logs to open up space"""
    logging.info('Clearing logs.')
    sys.stdout.write('Clearing logs.')
    status = os.system('rm ./secner/main.log')
    if status == 256:
        logging.error('User is not authorized to delete logs.')
        sys.exit('Permission denied. Please run from a super user state. (Maybe sudo python secner [command]%s if you\'re an admin)\n' % (' inspect' if __main__.inspect else str()))
    elif status != 0:
        logging.error('Something went wrong while creating the indexes directory.')
        sys.exit('Something went wrong while creating the indexes directory.\n')
    logging.debug('Logs successfully deleted.')
    sys.exit('Logs successfully deleted.')

def debugger():
    """Can be used for any tests of the system. This is NOT intended for production use."""
    __main__.flags.append(1234)
    logging.debug('different')
    # status, temp = commands.getstatusoutput('touch ./secner/completetest')
    # sys.stdout.write(temp[::-1]+'yolo\n')