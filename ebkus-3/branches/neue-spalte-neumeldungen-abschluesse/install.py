#!/usr/bin/env python
# coding: latin-1

import os, sys, getopt
from os.path import join, split, dirname, basename, exists, isdir, isfile, normpath, abspath
win32 = sys.platform == 'win32'
assert sys.version_info >= (2,3), "Es wird Python 2.3 oder höher benötigt"


def usage():
    s = """\
install.py --config <Installationsverzeichnis>
install.py -c <Installationsverzeichnis>

  Erstellt eine default Konfigurationsdatei ebkus.conf
  in <Installationsverzeichnis>/ebkus, falls noch keine
  vorhanden ist.
  Diese kann dann modifiziert und ergaenzt werden.

  Ausserdem wird die Konfiguration auf der Konsole
  ausgegeben.

install.py [--download <Downloadverzeichnis>] <Installationsverzeichnis>
install.py [-d <Downloadverzeichnis>] <Installationsverzeichnis>

  Installiert alle Komponenten im Installationsverzeichnis,
  das bereits existieren muss.

  Komponenten sind
  - ebkus 
  - alle in der Konfigurationsdatei  definierten Instanzen
    (defaultmaessig gibt es eine Instanz 'demo')
  - reportlab
  - pygdchart

  Unter Windows 2000 darueberhinaus
  - mysql
  - mysql_python
  - apache
  - openssl

  Diese werden bei Bedarf vom Internet heruntergeladen und im
  Installationsverzeichnis installiert und konfiguriert.

  Unter Linux sollten mysql, apache, openssl, pygdchart bereits
  installiert sein und die noetigen Konfigurationsdaten
  in ebkus.conf enthalten sein.
  
  Optionen:
    --download_dir,-d <Downloadverzeichnis>

      Verzeichnis, in dem ZIP-Archive der zu installierenden
      Komponenten erwartet werden. Falls vom Internet herunter-
      geladen wird, landen die Dateien hier.
      Falls nicht angegeben, wird das Installationsverzeichnis
      verwendet.

"""
    print s
    sys.exit(1)
    

if __name__ == '__main__':
    dir, fname = split(sys.argv[0])
    if not dir:
        dir = '.'
    dir = abspath(dir)
    EBKUS_DIST = dir
    # nur fuer die Installation 
    sys.path.insert(0, join(EBKUS_DIST, 'lib'))
    INSTALL_DIR = None
    DOWNLOAD_DIR = None
    config_only = no_mysql = no_apache = no_srvstart = False
    try:
        optlist, args = getopt.getopt(sys.argv[1:],
                                      'hi:d:c',
                                      ['help', 'no_mysql', 'no_apache', 'no_srvstart',
                                       'config', 
                                       'install_dir=', 'download_dir='])
    except getopt.GetoptError, m:
        print str(m)
        print '------------'
        usage()
        
    for option, value in optlist:
        if option in ('--help', '-h'):
            usage()
        if option in ('--config', '-c'):
            config_only = True
        if option in ('--no_mysql',):
            no_mysql = True
        if option in ('--no_apache',):
            no_apache = True
        if option in ('--no_srvstart',):
            no_srvstart = True
        if option in ('--download_dir', '-d'):
            DOWNLOAD_DIR = abspath(value)

    if len(args) < 1 or len(args) > 1:
        print "falsche Anzahl von Argumenten"
        print 
        usage()
        sys.exit(1)
    INSTALL_DIR = normpath(abspath(args[0]))
    if not DOWNLOAD_DIR:
        DOWNLOAD_DIR = INSTALL_DIR

    from ebkus.Install import InstallFromDist
    installer = InstallFromDist(EBKUS_DIST, INSTALL_DIR, DOWNLOAD_DIR)

    installer.init()
    if config_only:
        installer.config.show(all=True)
        sys.exit(0)

    # Falls MySQLdb noch nicht installiert ist
    try:
        import MySQLdb
    except ImportError:
        if win32:
            installer.mysql_python.install()
            sys.path.append(installer.config.EBKUS_PYTHON_PATH)
            try:
                import MySQLdb
            except:
                print 'MySQL-python konnte nicht installiert werden'
                sys.exit(1)
        else:
            print 'MySQL-python ist nicht installiert'
            sys.exit(1)
            

    if installer.mysql.is_ready_for_admin_connect():
        print "mysql ist betriebsbereit"
    else:
        print "mysql ist nicht betriebsbereit"
        if win32 and not no_mysql:
            installer.mysql.setup()

    if win32 and not no_apache:
        installer.openssl.install()
        installer.apache.install()
        if not no_srvstart:
            installer.srvstart.install()

    installer.ebkus.install()
    installer.ebkus.configure()
    installer.reportlab.install()
    installer.pygdchart.install()

    if win32 and not no_apache:
        installer.apache.configure()
        if not installer.apache.is_started_service():
            installer.apache.install_service()
            installer.apache.start_service()

    for i in installer.ebkus.instances:
        i.configure()
        if win32:
            if i.is_started_service():
                i.stop_service()
            else:
                i.install_service()
            i.start_service()

    if win32 and not no_apache:
        installer.apache.stop_service()
        installer.apache.start_service()

    sys.exit(0)

        
