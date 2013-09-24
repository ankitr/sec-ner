#!/usr/bin/env python

import sys
import nltk

def test():
	corpus = nltk.corpus.brown.words()
	del corpus

def setup():
	sys.stdout.write('Seting up NLP systems...\n')