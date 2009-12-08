#!/usr/bin/env python
# coding: latin-1

import os, sys, getopt
from os.path import join, split, dirname, basename, exists, isdir, isfile, normpath, abspath
win32 = sys.platform == 'win32'
assert sys.version_info >= (2,3), "Es wird Python 2.3 oder höher benötigt"


def usage():
    s = """\
uninstall.py  <Installationsverzeichnis>
              [<Instanzname>] [mysql | apache | srvstart | openssl | ebkus]

  Deinstalliert die angegebene Komponenten

uninstall.py  --all <Installationsverzeichnis> 

  Deinstalliert die gesamte EBKuS-Installation

Evt. muesse verbliebene Dateien und Verzeichnisse manuell geloescht
werden.

Beispiele:

python uninstall.py .. ebkus
  Aufruf aus dem Home-Verzeichnis, Installationsverzeichnis ist das
  uebergeordnete Verzeichnis.
  Deinstalliert alle Instanzen und ebkus.
python uninstall.py .. demo_berlin muster_efb
  Deinstalliert die Instanzen demo_berlin und muster_efb
python uninstall.py --all C:\ebinst
  Deinstalliert die gesamte EBKuS-Installation
python uninstall.py c:\ebinst apache
  Apache wird aus dem Installationsverzeichnis deinstalliert.
"""
    print s
    sys.exit(1)
    

if __name__ == '__main__':
    dir, fname = split(sys.argv[0])
    if not dir:
        dir = '.'
    dir = abspath(dir)
    EBKUS_DIST = EBKUS_HOME = None
    # ebkus_home oder dist?
    if isfile(join(dir, 'ebkus.conf')):
        EBKUS_HOME = dir
    else:
        EBKUS_DIST = dir
    # nur fuer die Installation 
    sys.path.insert(0, join(dir, 'lib'))
    try:
        optlist, args = getopt.getopt(sys.argv[1:],
                                      'h',
                                      ['help', 'all', 
                                       ])
    except getopt.GetoptError, m:
        print str(m)
        print '------------'
        usage()

    all = False
    for option, value in optlist:
        if option in ('--help', '-h'):
            usage()
        if option in ('--all',):
            all = True

    if len(args) < 1:
        print "zuwenig Argumente"
        print 
        usage()
        sys.exit(1)

    INSTALL_DIR = normpath(abspath(args[0]))
    if not isdir(INSTALL_DIR):
        print "******Fehler: %s ist kein Verzeichnis" % INSTALL_DIR
        usage()
        
    uninstall = args[1:]
    if not (uninstall or all):
        print "******Fehler: Nichts zu deinstallieren"
        usage()

    from ebkus.Install import InstallFromDist, InstallFromHome
    if EBKUS_DIST:
        installer = InstallFromDist(EBKUS_DIST, INSTALL_DIR, INSTALL_DIR,
                                    uninstall_only=True)
    else:
        installer = InstallFromHome(EBKUS_HOME)
    installer.init()
    if all:
        uninstall = installer.config.get_instances() + \
                    ['apache', 'mysql', 'openssl', 'srvstart', 'ebkus']
    for u in uninstall:
        component = installer[u]
        if component:
            installer.apache.stop_service()
            component.uninstall()
        else:
            print "%s ist weder eine bekannte Komponente noch eine konfigurierte EBKuS-Instanz" % u
    sys.exit(0)

