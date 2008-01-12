#!/usr/bin/env python
# coding: latin-1
"""
Struktur der CD:

README.txt
/linux
  Python?
  mysql?
  MySQLdb
  ReportLab_1_19.zip
  pygdchart0.6.1-linux-py23.zip
/win32
  Python
  MySQLdb
  Apache_1.3.31-Mod_SSL_2.8.17-Openssl_0.9.7d-Win32.zip
  Openssl-0.9.7d-Win32.zip
  mysql-4.0.17-win-noinstall.zip
  ReportLab_1_19.zip
  pygdchart0.6.1-w32-py23.zip
  srvstart_run.v110.zip
/ebkus-3.2
  /doc
  /lib
  /sql
  /templates
  /htdocs
  README.txt
  TODO.txt
  install.py
  create_cd.py
  ...
  
"""
import os, sys, getopt
assert sys.version_info >= (2,3), "Es wird Python 2.3 oder höher benötigt"
from os.path import join, split, dirname, basename, exists, isdir, isfile, normpath, abspath

def usage():
    s = """\
create_cd.py  [Optionen] <Verzeichnis>

  Erstellt in dem Verzeichnis alle für die EBKuS-Distributions-CD
  benötigten Dateien und Verzeichnisse, die dann nur noch
  gebrannt werden müssen.

  Das Verzeichnis darf kein Unterverzeichnis des
  aktuellen Verzeichnisses (wo dieses Skript sich befindet) sein.

  Die nötige Software wird automatisch heruntergeladen. Dazu muss
  natürlich eine Internetverbindung aktiv sein.

  Optionen:

  --linux        Nur die für Linux benötigte Software holen
  --win32        Nur die für Windows benötigte Software holen

Beispiel:

   python create_cd.py --linux /home/user/tmp/ebkus-cd
   
"""
    print s
    sys.exit(1)
    

if __name__ == '__main__':
    dir, fname = split(sys.argv[0])
    if not dir:
        dir = '.'
    dir = normpath(abspath(dir))
    EBKUS_DIST = dir
    sys.path.insert(0, join(EBKUS_DIST, 'lib'))

    try:
        optlist, args = getopt.getopt(sys.argv[1:],
                                      'h',
                                      ['help', 'linux', 'win32'])
    except:
        usage()

    try:
        CD_DIR = normpath(abspath(args[0]))
    except:
        usage()

    linux = win32 = True # default
    for option, value in optlist:
        if option in ('--help', '-h'):
            usage()
        elif option in ('--linux',):
             win32 = False            
        elif option in ('--win32',):
             linux = False
        else:
            usage()

    assert exists(CD_DIR), "Verzeichnis '%s' existiert nicht" % CD_DIR
    assert not CD_DIR.startswith(EBKUS_DIST), \
           "CD-Verzeichnis '%s' darf kein Unterverzeichnis von '%s' sein" % (CD_DIR, EBKUS_DIST)
    from ebkus.Install import create_cd
    create_cd(EBKUS_DIST, CD_DIR, for_linux=linux, for_win32=win32)
