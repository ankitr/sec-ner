#!/usr/bin/env python

import logging
import sys
import nltk

logging.basicConfig(filename='./secner/main.log', level=logging.DEBUG)

def test():
	corpus = nltk.corpus.brown.words()
	del corpus

def setup():
	sys.stdout.write('Seting up NLP systems...\n')