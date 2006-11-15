#!/usr/bin/env python -i

usage = """\
Usage:

1. in das Verzeichnis einer konfigurierten Instanz kopieren
2. mit 'python -i interaktiv.py' aufrufen

Nur unter Linux getestet!
"""

import sys,os,string,re

import sys, os, re
# ich finde das immer ganz praktisch
from os.path import join, split, dirname, basename, exists, isdir, \
                    isfile, normpath, normcase, abspath, splitext, \
                    expanduser

# mit dem folgenden hat man eine persistente command history
# und autocompletion mit der Tab-Taste
import os, rlcompleter, readline, atexit
readline.parse_and_bind('tab: complete')
historyPath = expanduser("~/.python_history")
#print historyPath
readline.set_history_length(1000)
def save_history(historyPath=historyPath):
   import readline
   # why can't the next line see the global readline?
   readline.write_history_file(historyPath)
   #print 'saving history'
if os.path.exists(historyPath):
   readline.read_history_file(historyPath)
atexit.register(save_history)
# clean up the namespace
del atexit, readline, save_history, historyPath, rlcompleter

try:
    import init
    import ebkus.ebs
    # aufgrund der ganzen scheiss-'import *' hat man nun die ganze
    # EBKuS Schnittstelle im Namesraum von e
    # vielleicht hat's hier ja was Gutes ...
    import ebkus.app.ebupd as e
except Exception, msg:
   print '**********  Fehler:', msg
   print usage
   sys.exit(1)

    
print
print """\
EBKuS %s interaktiv

Autocompletion mit der Tab-Taste
History wie in der Shell

Die EBKuS-API findet sich im Namensraum 'e', z.B.
>>> l = e.MitarbeiterList(where='')
>>> e.xcountitem('stzei', l, 'stz')
>>> dir(e) # gibt alles aus

"""  % ebkus.Version






