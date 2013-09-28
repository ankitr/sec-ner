#!/usr/bin/env python

import commands
import logging
import os
import sys

from ftplib import FTP

import __main__
import helpers

logging.basicConfig(filename='./secner/main.log', level=logging.DEBUG)

def test(server):
    logging.debug('Running scraping test.')
    connection = FTP(server)
    logging.debug('Connected to server. Testing connection...')
    logging.debug(connection.retrlines('LIST'))
    sys.stdout.write('FTP Server connection made.\n')
    logging.debug('Closing connection.')
    connection.close()

def setup(server):
    connection = FTP(server)
    connection.login()
    sys.stdout.write('Setting up FTP systems...\n')
    sys.stdout.write('\tFTP server connection made.\n')
    sys.stdout.write('\tPassing connection to state.\n')

def collect_indices(connection):
    os.cwd('./secner/bin/indexes')
    status, output = commands.getstatusoutput('wget')
    if status == 32512: sys.exit('wget (a prerequisite of this program) is not installed. Please install before running again.')
    sys.stdout.write('Preparing to download the indexes for the server. Depending on your connection this may take a couple hours. DO NOT SEVER THE CONNECTION DURING THIS TIME PERIOD. LEAVE THE MACHINE RUNNING FOR THIS TIME.')
    logging.info('Starting server initiation.')
    if __main__.inspect: status = os.system('wget -r ftp://ftp.sec.gov/edgar/daily-index/*')
    else:
        status, output = commands.getstatusoutput('wget -r ftp://ftp.sec.gov/edgar/daily-index/*')
        logging.debug(status)
        logging.debug(output)
    if status == 32512:
        logging.error('wget not installed.')
        sys.exit('Please install wget before rerunning this process.')
    elif status == 1024
    elif status != 0:
        logging.error('wget failed. Need to clean up indexes.')
        sys.exit('Critical failure. Run clean before attempting to download again.')

    sys.exit('We\'re working on making indexes. Until then, look up lolcatz on google.')
    # filenames = connection.nlst()
    # for filename in filenames:
    #     local_filename = os.path.join('C:\\test\\', filename)
    #     file = open(local_filename, 'wb')
    #     connection.retrbinary('RETR '+ filename, file.write)
    #     file.close()
    # connection.close()