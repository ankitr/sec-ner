#!/usr/bin/env python

import os
import sys
from ftplib import FTP

import helpers

def test(server):
    connection = FTP(server)
    connection.login()
    connection.retrlines('LIST')
    sys.stdout.write('FTP Server connection made.\n')
    connection.close()

def setup(server):
    connection = FTP(server)
    connection.login()
    sys.stdout.write('Setting up FTP systems...\n')
    sys.stdout.write('\tFTP server connection made.\n')
    sys.stdout.write('\tPassing connection to state.\n')

def collect_indices(connection):
    if os.path.exists('./bin/indexes'):
        if not helpers.query('The \'indexes\' directory already exists. Are you sure you would like to rewrite it?'): sys.exit('Process stopped by user.\n\n')
        else:
            status_code = os.system('rm -rf ./bin/indexes')
            if status_code == 256:
                sys.stdout.write('Permission to delete directory denied. Sudoing the operation. Administrator password may be required.\n')
                status_code = os.system('sudo rm -rf ./bin/indexes') 
            if status_code != 0: sys.exit('Error in creating indexes directory.')
    sys.stdout.write('Creating indexes. You may need to provide an admin username and password.')
    status_code = os.system('mkdir ./bin/indexes')
    if status_code == 256:
        sys.stdout.write('Permission to create directory denied. Sudoing the operation. Administrator password may be required.\n')
        status_code = os.system('sudo mkdir ./bin/indexes') 
    if status_code != 0: sys.exit('Error in creating indexes directory.')
    if status_code != 0: sys.exit('Error in creating indexes directory.')
    connection.cwd
    for filename in ftp.nlst(filematch):
        if os.path.exists('' + filename) == False:
            fhandle = open(os.path.join('C:\my_directory', filename), 'wb')
            print 'Getting ' + filename
            ftp.retrbinary('RETR ' + filename, fhandle.write)
            fhandle.close()
        elif os.path.exists(('C:\my_directory\\' + filename)) == True:
            print 'File ', filename, ' Already Exists, Skipping Download'            


    sys.exit('We\'re working on making indexes. Until then, look up lolcatz on google.')
    # filenames = connection.nlst()
    # for filename in filenames:
    #     local_filename = os.path.join('C:\\test\\', filename)
    #     file = open(local_filename, 'wb')
    #     connection.retrbinary('RETR '+ filename, file.write)
    #     file.close()
    # connection.close()