#!/usr/bin/env python

import commands
import logging
import os
import subprocess
import sys
import time

import config
import data
import helpers
import nlp
import scraping

logging.basicConfig(filename='./secner/main.log', level=logging.DEBUG)

def test():
    try:
        data.test(config.NEO4J_SERVER)
        nlp.test()
        scraping.test(config.SEC_SERVER)
        sys.stdout.write('\n\n\nTests returned positive. All systems ready to go.\n\n\n\n')
    except Exception as e:
        sys.exit('\n\n\nTests returned negative. Check logs for more details. Here\'s the last error:\n"%s"\n\n' % sys.exc_value)

def setup():
    os.chdir('./secner')
    graph = data.setup(config.NEO4J_SERVER)
    ftp_server = scraping.setup(config.SEC_SERVER)
    nlp.setup()
    return graph, ftp_server


def initialize():
    test()
    if not helpers.query('Would you like to initiate the process?'): sys.exit('Process stopped by user.')
    if not helpers.query('This action will erase all content on your Neo4j server. Are you sure you would like to continue?'): sys.exit('Process stopped by user.')
    sys.stdout.write('Starting')
    for i in range(5):
        sys.stdout.write('.')
        sys.stdout.flush()
        time.sleep(0.75 )
    sys.stdout.write('\n\n')
    graph, ftp_server = setup()
    sys.stdout.write('Setup complete.\n\n\n\n')
    scraping.collect_indices(ftp_server)

def refresh(): #TODO
    test()
    if not helpers.query('Would you like to initiate the process?'): sys.exit('Process stopped by user')
    sys.exit('Refresh unprepared for usage.')


def debug():
    logging.debug('oyouoaufdof') #TODO setup logging
    # status, temp = commands.getstatusoutput('touch ./secner/completetest')
    sys.stdout.write(temp[::-1]+'yolo\n')