#!/usr/bin/env python

import logging
import sys

from py2neo import neo4j

import __main__
import helpers

logging.basicConfig(filename='./secner/main.log', level=logging.DEBUG)

def test(server):
	logging.debug('Testing Neo4j connection.')
	graph = neo4j.GraphDatabaseService(server)
	logging.debug('Connection established.')
	sys.stdout.write('Neo4j connection established.\n')

def setup(server):
	logging.debug('Setting up Neo4j systems.')
	sys.stdout.write('Preparing Neo4j server...\n')
	graph = neo4j.GraphDatabaseService(server)
	logging.debug('Connection established.')
	sys.stdout.write('\tNeo4j connection established.\n')
	clean(server)
	sys.stdout.write('\tServer cleared.\n')

def clean(server):
	logging.debug('Clearing graph.')
	logging.debug('Connecting to Neo4j server.')
	graph = neo4j.GraphDatabaseService(server)
	logging.debug('Connected. Preparing to clear.')
	graph.clear()
	logging.debug('Server successfully cleared.')