#!/usr/bin/env python

import logging
import sys

from py2neo import neo4j

logging.basicConfig(filename='./secner/main.log', level=logging.DEBUG)

def test(server):
	graph = neo4j.GraphDatabaseService(server)
	sys.stdout.write('Neo4j connection established.\n')

def setup(server):
	sys.stdout.write('Preparing Neo4j server...\n')
	graph = neo4j.GraphDatabaseService(server)
	sys.stdout.write('\tNeo4j connection established.\n')
	graph.clear()
	sys.stdout.write('\tServer cleared.\n')