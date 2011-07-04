#!/usr/bin/env python
# coding: latin-1

import os, sys, getopt
from os.path import join, split, dirname, basename, exists, isdir, isfile, normpath, abspath
win32 = sys.platform == 'win32'
assert sys.version_info >= (2,3), "Es wird Python 2.3 oder hoeher benoetigt"
win32new = win32 and sys.version_info >= (2,7)


def usage():
    s = """\
install.py [Optionen] <Installationsverzeichnis>

  Installiert alle Komponenten im Installationsverzeichnis.

  Komponenten sind
  - ebkus 
  - alle in der Konfigurationsdatei  definierten Instanzen
    (defaultmaessig gibt es die Instanzen 'demo' und 'muster_efb')
  - reportlab

  Unter Windows darueberhinaus
  - mysql
  - apache

  Die letzten beiden sowie reportlab werden bei Bedarf vom EBKuS-FTP-Server
  in das Downloadverzeichnis heruntergeladen und im Installationsverzeichnis 
  installiert und konfiguriert.

  Unter Linux sollten mysql und apache bereits
  installiert und konfiguriert sein und die noetigen Konfigurationsdaten
  in ebkus.conf enthalten sein.
  
  Optionen:

    --config, -c

      Liest eine vorhandene 'ebkus.conf' oder erstellt eine neue, falls
      keine vorhanden ist, und bricht dann die Installation ab.
      Die Konfiguration kann dann modifiziert und ergaenzt werden.

      Ausserdem wird die Konfiguration auf der Konsole
      ausgegeben.

      Die Konfigurationsdatei ebkus.conf befindet sich im Homeverzeichnis
      <Installationsverzeichnis>/ebkus.

    --preconfig_dir, -p

      Dateien aus diesem Verzeichnis werden vor der Installation 
      in das EBKuS-Homeverzeichnis kopiert. Liegt dort eine gueltige
      'ebkus.conf' und eine Menge von Datenbankdumps der zugehoerigen
      Instanzen, laesst sich damit eine vollautomatische Neuinstallation 
      durchfuehren. 

    --download_dir,-d <Downloadverzeichnis>

      Verzeichnis, in dem die zu installierenden
      Software erwartet wird. Falls vom Internet herunter-
      geladen wird, landen die Dateien hier.
      Falls nicht angegeben, ist das Downloadverzeichnis
      <Installationsverzeichnis>/download.

    --no_mysql
    --no_apache

      Die jeweilige Komponente wird unter Windows nicht installiert
      (unter Linux sowieso nicht).

    --update, -u

      Die EBKuS-Dateien werden auf jeden Fall aus der Distribution in die
      Installation kopiert. Damit ist also ein Update moeglich. 
      Evt. gestartete Instanzen sollten vorher beendet werden! 

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
    PRECONFIG_DIR = None
    config_only = no_mysql = no_apache = no_srvstart = update = needs_confirmation = False
    try:
        optlist, args = getopt.getopt(sys.argv[1:],
                                      'hd:cup:',
                                      ['help', 'no_mysql', 'no_apache', 'no_srvstart',
                                       'config', 'update', 
                                       'download_dir=', 'preconfig_dir='])
    except getopt.GetoptError, m:
        print str(m)
        print '------------'
        usage()
        
    for option, value in optlist:
        if option in ('--help', '-h'):
            usage()
        if option in ('--config', '-c'):
            config_only = True
        if option in ('--update', '-u'):
            update = True
        if option in ('--no_mysql',):
            no_mysql = True
        if option in ('--no_apache',):
            no_apache = True
        if option in ('--no_srvstart',):
            no_srvstart = True
        if option in ('--download_dir', '-d'):
            DOWNLOAD_DIR = abspath(value)
        if option in ('--preconfig_dir', '-p'):
            PRECONFIG_DIR = abspath(value)

    if  len(args) > 1:
        print "******Fehler: Zu viele Argumente"
        print 
        usage()
        sys.exit(1)
    elif len(args) == 1:
        INSTALL_DIR = normpath(abspath(args[0]))
    else:
        print "******Fehler: Kein Installationsverzeichnis angegeben"
        print 
        usage()
        sys.exit(1)
    if INSTALL_DIR and not exists(INSTALL_DIR):
        needs_confirmation = True
        os.makedirs(INSTALL_DIR, 0755)

    if needs_confirmation:
        if config_only:
            prompt = r"EBKuS-Konfiguration (ebkus.conf) in '%s' erzeugen? [ja/nein]:"
        else:
            prompt = r"EBKuS in '%s' installieren? [ja/nein]:"
        res = raw_input(prompt % INSTALL_DIR)
        if not res or not res[0].lower() in ('j', 'y'):
            sys.exit(1)

    from ebkus.Install import InstallFromDist
    installer = InstallFromDist(EBKUS_DIST, INSTALL_DIR, DOWNLOAD_DIR, preconfig_dir=PRECONFIG_DIR)

    installer.init()
    if config_only:
        installer.config.show(all=True)
        sys.exit(0)

    # Falls MySQLdb noch nicht installiert ist
    try:
        import MySQLdb
    except ImportError:
        if win32new:
            print '"Python-MySQL Adapter" ist noch nicht installiert.'
            print 'Bitte erst die Datei "MySQL-python-1.2.3.win32-py2.7.exe" installieren.'
            sys.exit(1)
        elif win32:
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

    # Falls pywin32 noch nicht installiert ist
    if win32new:
        try:
            import win32service
        except ImportError:
            print '"Python for Windows extensions" ist noch nicht installiert.'
            print 'Bitte erst die Datei "pywin32-216.win32-py2.7.exe" installieren.'
            sys.exit(1)

    if installer.mysql.is_ready_for_admin_connect():
        print "mysql ist betriebsbereit"
    else:
        print "mysql ist nicht betriebsbereit"
        if win32 and not no_mysql:
            installer.mysql.setup()


    if win32 and not no_apache:
        if not win32new:
            installer.openssl.install()
        installer.apache.install()
    if win32 and not win32new and not no_srvstart:
        installer.srvstart.install()


    installer.ebkus.install(update)
    installer.ebkus.configure()
    installer.reportlab.install()
    if sys.version_info < (2,4):
        installer.pygdchart.install()

    if win32 and not no_apache:
        installer.apache.configure()
        if not installer.apache.is_started_service():
            installer.apache.install_service()
            installer.apache.start_service()

#    sys.exit(0)

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

        
