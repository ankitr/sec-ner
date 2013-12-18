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
import nlp
import scraping

from helpers import *

logging.basicConfig(filename='./secner/main.log', level=logging.DEBUG)


# Process Tools
def test():
    logging.debug('Running system tests.')
    try:
        data.test(config.NEO4J_SERVER)
        nlp.test()
        scraping.test(config.SEC_SERVER)
        logging.debug('Tests cleared.')
        print('\n\n\nTests returned positive. All systems ready to go.\n\n\n')
    except:
        logging.error('System tests returned negative.')
        logging.debug(type(sys.exc_type))
        logging.debug(str(sys.exc_type))
        logging.error('%s:%s' % (sys.exc_type, sys.exc_value))
        sys.exit('Tests returned negative. Check logs for more details.')

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
    permit('Would you like to initiate the process?')
    permit('This action will erase all content on your Neo4j server. Would you like to continue?')
    out('Starting setup.')
    graph, ftp_server = setup()
    out('Setup complete.')
    scraping.initiate_indexes(ftp_server)
    #TODO: Run NLP

def reinitialize():
    out('REINITIALIZING SYSTEM\n\n')
    test()
    logging.debug('Requesting init permissions')
    permit('This action will erase all content on your Neo4j server. Are you sure you would like to continue?')

def refresh(): #TODO
    # logging.info('Refreshing.')
    # test()
    sys.exit('Refresh unprepared for usage.')

def clean_up():
    """For use when an emergency problem causes an unsafe shutdown. Clears out system files and returns to a stable state."""
    logging.info('Cleaning up system.')
    logging.debug('Changing working directory.')
    os.chdir('./secner/bin/')
    logging.debug('Requesting permission to continue.')
    permission = helpers.query('Note that running this proccess will result in deletion of potentially valuable content. Are you absolutely sure you would wish to proceed?')
    if not permission:
        logging.debug('User did not permit running the service.')
        sys.exit('Process stopped by user.')
    logging.debug('Permission recieved. Continuing with process.')
    if os.path.exists('./indexes/'):
        logging.debug('Clearing indexes.')
        status = os.system('rm -rf ./indexes/')
        if status == 256:
            error('Permission denied.')
        elif status != 0:
            error('Something went wrong.')
    if os.path.exists('./tests/'):
        logging.debug('Clearing tests.')
        status = os.system('rm -rf ./tests/*')
        if status == 256:
            error('Permission denied.')
        elif status != 0:
            error('Something went wrong.')
    if os.path.exists('./.secner-helpers/'):
        logging.debug('Clearing secner-helpers.')
        status = os.system('rm -rf ./secner-helpers/*')
        if status == 256:
            error('Permission denied.')
        elif status != 0:
            error('Something went wrong.')
    try:
        logging.debug('Clearing Neo4j Server.')
        data.clean(config.NEO4J_SERVER)
    except:
        logging.error('Something went wrong while clearing the Neo4j server.')
        logging.exception(sys.exc_type+':'+sys.exc_value)
        sys.exit('Something went wrong while clearing the Neo4j server. Check logs for details.')
    logging.debug('Clearing complete.')
    sys.exit('System cleaned. Factory state returned.')

def clear_logs():
    """Clears the logs to open up space"""
    logging.info('Clearing logs.')
    print('Clearing logs.')
    status = os.system('rm ./secner/main.log')
    if status == 256:
        logging.error('User is not authorized to delete logs.')
        sys.exit('Permission denied.')
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
    # print(temp[::-1]+'yolo\n')