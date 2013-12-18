#!/usr/bin/env python

#import ftplib
#import ftputil
import logging
import os
import re
import sys

logging.basicConfig(filename='./secner/main.log', level=logging.DEBUG)

def query(question, default='yes'):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".
    """
    valid = {'yes':True,
             'y':True,
             'ye':True,
             'no':False,
             'n':False}
    if default == None: prompt = ' [y/n] '
    elif default == 'yes': prompt = ' [Y/n] '
    elif default == 'no': prompt = ' [y/N] '
    else: raise ValueError('Invalid default answer: \'%s\'' % default)
    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '': return valid[default]
        elif choice in valid: return valid[choice]
        else:
            print('Please respond with \'yes\' or \'no\' (or \'y\' or \'n\').')

def find(dregex, fregex, top='.'):
    dmatcher = re.compile(dregex)
    fmatcher = re.compile(fregex)
    for dirpath, dirnames, filenames in os.walk(top):
        d = os.path.relpath(dirpath, top)
        if not dmatcher.match(d): continue
        for f in filenames:
            if fmatcher.match(f):
                yield os.path.join(d, f)

def error(message):
    logging.error(message)
    sys.exit(message+'\n')

def out(message):
    logging.debug(message)
    print(message)

def permit(permission):
    if not query(permission):
        error('User stopped process.')