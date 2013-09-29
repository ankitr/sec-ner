#!/usr/bin/env python

import commands
import logging
import os
import sys
import time

from ftplib import FTP

import __main__
import helpers

logging.basicConfig(filename='./secner/main.log', level=logging.DEBUG)

def test(server):
    logging.debug('Running scraping test.')
    connection = FTP(server)
    connection.login()
    logging.debug('Connected to server. Testing connection...')
    logging.debug(connection.retrlines('LIST'))
    sys.stdout.write('FTP Server connection made.\n')
    logging.debug('Closing connection.')
    connection.close()

def setup(server):
    logging.debug('Setting up FTP connections.')
    sys.stdout.write('Setting up FTP systems...\n')
    connection = FTP(server)
    connection.login()
    logging.debug('Connected to server.')
    sys.stdout.write('\tFTP server connection made.\n')
    sys.stdout.write('\tPassing connection to state.\n')

def collect_indexes(connection):
    """Collects the indexes from the SEC server for processing over. Should be used for initialization."""
    logging.debug('Collecting indexes.')
    logging.debug('Checking if indexes directory exists.')
    if os.path.exists('./bin/indexes'):
        logging.debug('indexes directory exists. Asking for permission to remove.')
        if helpers.query('The indexes directory already exists. Would you like to remove it?'):
            sys.stdout.write('Deleting...\n\n')
            status = os.system('rm -rf ./bin/indexes')
            if status == 256:
                logging.error('User is not authorized to delete indexes.')
                sys.exit('Permission denied. Please run from a super user state. (Maybe sudo python secner [command]%s if you\'re an admin)\n' % (' inspect' if __main__.inspect else str()))
            elif status != 0:
                logging.error('Something went wrong while removing the indexes directory.')
                sys.exit('Something went wrong while removing the indexes directory.\n')
            logging.debug('indexes directory removed successfully.')
        else:
            logging.error('User permission not granted to remove indexes directory.')
            sys.exit('Process stopped by user.\n')
    else: logging.debug('indexes directory does not exist. Proceeding normally.')
    logging.debug('Making indexes directory.')
    sys.stdout.write('Setting up for index download.\n')
    status = os.system('mkdir ./bin/indexes')
    if status == 256:
        logging.error('User is not authorized to create an indexes directory.')
        sys.exit('Permission denied. Please run from a super user state. (Maybe sudo python secner [command]%s if you\'re an admin)\n' % (' inspect' if __main__.inspect else str()))
    elif status != 0:
        logging.error('Something went wrong while creating the indexes directory.')
        sys.exit('Something went wrong while creating the indexes directory.\n')
    logging.debug('New indexes directory created successfully.')
    logging.debug('Moving to indexes directory.')
    os.chdir('./bin/indexes')
    logging.debug('Checking for wget...')
    status, output = commands.getstatusoutput('wget')
    if status == 32512:
        logging.debug('wget is not installed.')
        sys.exit('wget (a prerequisite of this program) is not installed. Please install before running again.\n')
    logging.debug('wget is installed.')
    sys.stdout.write('Preparing to download the indexes for the server. Depending on your connection this may take a couple hours.\nDO NOT SEVER THE CONNECTION DURING THIS TIME PERIOD. LEAVE THE MACHINE RUNNING FOR THIS TIME.\n\n\n')
    if not helpers.query('Are you ready to begin?', default='yes'):
        logging.debug('Process ceased by user. Download not started')
        sys.exit('Process stopped by user.\n')
    sys.stdout.write('\n\n\n')
    sys.stdout.write('Starting')
    for i in range(3):
        sys.stdout.write('.')
        sys.stdout.flush()
        time.sleep(0.75)
    sys.stdout.write('\n\n')
    logging.info('Starting server initiation.')
    if __main__.inspect: status = os.system('wget -r ftp://ftp.sec.gov/edgar/full-index/*')
    else:
        status, output = commands.getstatusoutput('wget -r ftp://ftp.sec.gov/edgar/full-index/*')
        logging.debug(status)
        logging.debug(output)
    if status == 1024:
        logging.error('Unable to connect to the server from wget.')
        sys.exit('wget failed to connect with the server. Please check your network connection or try again later.\n')
    elif status == 256:
        logging.error('Permission denied to copy indexes.')
        sys.exit('Permission denied. Please run from a super user state. (Maybe sudo python secner [command]%s if you\'re an admin)\n' % (' inspect' if __main__.inspect else str()))
    elif status != 0:
        logging.critical('wget failed. Need to clean up indexes.')
        sys.exit('\nCritical failure. Run clean before attempting to download again.\n')

    sys.exit('We\'re working on making indexes. Until then, look up lolcatz on google.\n')
    # filenames = connection.nlst()
    # for filename in filenames:
    #     local_filename = os.path.join('C:\\test\\', filename)
    #     file = open(local_filename, 'wb')
    #     connection.retrbinary('RETR '+ filename, file.write)
    #     file.close()
    # connection.close()