#!/usr/bin/env python

#import ftplib
#import ftputil
import logging
import sys

logging.basicConfig(filename='./secner/main.log', level=logging.DEBUG)

def query(question, default="no"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".
    """
    valid = {"yes":True,   "y":True,  "ye":True,
             "no":False,     "n":False}
    if default == None: prompt = " [y/n] "
    elif default == "yes": prompt = " [Y/n] "
    elif default == "no": prompt = " [y/N] "
    else: raise ValueError("invalid default answer: '%s'" % default)
    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '': return valid[default]
        elif choice in valid: return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "\
                             "(or 'y' or 'n').\n")

# """
# ftpwalk -- Walk a hierarchy of files using FTP (Adapted from os.walk()).
# """

# def ftpwalk(ftp, top, topdown=True, onerror=None):
#     """
#     Generator that yields tuples of (root, dirs, nondirs).
#     """
#     ftp.login()
#     # Make the FTP object's current directory to the top dir.
#     ftp.cwd(top)
#     # We may not have read permission for top, in which case we can't
#     # get a list of the files the directory contains.  os.path.walk
#     # always suppressed the exception then, rather than blow up for a
#     # minor reason when (say) a thousand readable directories are still
#     # left to visit.  That logic is copied here.
#     try:
#         dirs, nondirs = _ftp_listdir(ftp)
#     except os.error, err:
#         if onerror is not None:
#             onerror(err)
#         return
#     if topdown:
#         yield top, dirs, nondirs
#     for entry in dirs:
#         dname = entry[0]
#         path = posixjoin(top, dname)
#         if entry[-1] is None: # not a link
#             for x in ftpwalk(ftp, path, topdown, onerror):
#                 yield x
#     if not topdown:
#         yield top, dirs, nondirs

# _calmonths = dict( (x, i+1) for i, x in
#                    enumerate(('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
#                               'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')) )

# def _ftp_listdir(ftp):
#     """
#     List the contents of the FTP opbject's cwd and return two tuples of

#        (filename, size, mtime, mode, link)

#     one for subdirectories, and one for non-directories (normal files and other
#     stuff).  If the path is a symbolic link, 'link' is set to the target of the
#     link (note that both files and directories can be symbolic links).

#     Note: we only parse Linux/UNIX style listings; this could easily be
#     extended.
#     """
#     dirs, nondirs = [], []
#     listing = []
#     ftp.retrlines('LIST', listing.append)
#     for line in listing:
#         # Parse, assuming a UNIX listing
#         words = line.split(None, 8)
#         if len(words) < 6:
#             print >> sys.stderr, 'Warning: Error reading short line', line
#             continue
#         # Get the filename.
#         filename = words[-1].lstrip()
#         if filename in ('.', '..'):
#             continue
#         # Get the link target, if the file is a symlink.
#         extra = None
#         i = filename.find(" -> ")
#         if i >= 0:
#             # words[0] had better start with 'l'...
#             extra = filename[i+4:]
#             filename = filename[:i]
#         # Get the file size.
#         size = int(words[4])
#         # Get the date.
#         year = datetime.today().year
#         month = _calmonths[words[5]]
#         day = int(words[6])
#         mo = re.match('(\d+):(\d+)', words[7])
#         if mo:
#             hour, min = map(int, mo.groups())
#         else:
#             mo = re.match('(\d\d\d\d)', words[7])
#             if mo:
#                 year = int(mo.group(1))
#                 hour, min = 0, 0
#             else:
#                 raise ValueError("Could not parse time/year in line: '%s'" % line)
#         dt = datetime(year, month, day, hour, min)
#         mtime = time.mktime(dt.timetuple())
#         # Get the type and mode.
#         mode = words[0]
#         entry = (filename, size, mtime, mode, extra)
#         if mode[0] == 'd':
#             dirs.append(entry)
#         else:
#             nondirs.append(entry)
#     return dirs, nondirs