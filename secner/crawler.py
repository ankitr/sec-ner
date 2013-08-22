#!/usr/bin/env python

import os
import nltk

from ftplib import FTP
from neo4jrestclient.client import GraphDatabase

#Base Variables
FTP_SERVER_LOCATION = 'ftp.sec.gov'
NEO4J_SERVER_LOCATION = 'http://54.221.198.99:7474/db/data/'

#Set up server connections
sec = FTP(FTP_SERVER_LOCATION)
sec.login()
neo4j = GraphDatabase(NEO4J_SERVER_LOCATION)

