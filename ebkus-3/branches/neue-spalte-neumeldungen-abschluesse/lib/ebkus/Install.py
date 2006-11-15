# coding: latin-1
import os, sys, getopt, errno, popen2, time
assert sys.version_info >= (2,3), "Es wird Python 2.3 oder höher benötigt"
from traceback import format_exception
from os.path import join, split, dirname, basename, exists, \
     isdir, isfile, normpath, normcase, abspath
from os import rename, remove
from shutil import rmtree, copy2
from urllib import urlretrieve
import zipfile
import re

# Abkuerzung
win32 = sys.platform == 'win32'

def readable(path):
    return os.access(path, os.R_OK)

def assert_readable(path):
    if not os.access(path, os.R_OK):
        raise InstallException("keine Leseberechtigung für %s" % path)

class InstallException(Exception):
    pass

def create_cd(dist_dir, cd_dir, for_linux, for_win32):
    global win32
    saved_win32 = win32
    # Windows Sachen runterladen
    if for_win32:
        win32 = True
        download_dir = join(cd_dir, 'win32')
        install_dir = join(cd_dir, 'ebkus_win32')
        create_directory(install_dir)
        create_directory(download_dir)
        installer = InstallFromDist(dist_dir, install_dir, download_dir)
        installer.init()
        installer.close_log()
        installer.python._download()
        installer.mysql_python._download()
        installer.mysql._download()
        installer.apache._download()
        installer.openssl._download()
        installer.pygdchart._download()
        installer.reportlab._download()
        installer.srvstart._download()
        myrmtree(install_dir, logf=installer.log)
    
    # Linux Sachen runterladen
    if for_linux:
        win32 = False
        download_dir = join(cd_dir, 'linux')
        install_dir = join(cd_dir, 'ebkus_linux')
        create_directory(install_dir)
        create_directory(download_dir)
        installer = InstallFromDist(dist_dir, install_dir, download_dir)
        installer.init()
        installer.close_log()
        installer.python._download()
        installer.mysql_python._download()
        installer.mysql._download()
        installer.apache._download()
        installer.modssl._download()
        installer.openssl._download()
        installer.pygdchart._download()
        installer.reportlab._download()
        myrmtree(install_dir, logf=installer.log)

    # EBKuS Dateien kopieren
    ebkus_dir = join(cd_dir, 'ebkus-3.2')
    create_directory(ebkus_dir)
    for f in os.listdir(dist_dir):
        src = join(dist_dir, f)
        mycopytree(src, ebkus_dir, exclude_dirs=['CVS'],
                   overwrite=True, logf=installer.log)
    os.chmod(join(ebkus_dir, 'install.py'), 0700)
    os.chmod(join(ebkus_dir, 'create_cd.py'), 0700)

    # Doku bauen
    try:
        cwd = os.getcwd()
        os.chdir(join(ebkus_dir, 'doc'))
        res = os.system('./make.py')
        if res == 0:
            aux = ['manual.aux', 'manual.out', 'manual.log']
            for f in aux:
                try: os.remove(f)
                except: pass
            installer.log('Dokumentation erfolgreich erzeugt')
    finally:
        os.chdir(cwd)
    win32 = saved_win32

class Installer(object):
    # hier tragen sich die Komponenten mit Namen und Objekt ein
    components = {}
    def __getitem__(self, name):
        try:
            return self.components[name]
        except:
            return None

    def _init_log(self, dir):
        #self.log = open(join(dir, 'install.log'))
        try:
            self._log = open(join(dir, 'install.log'), 'a')
            self._log.write(time.strftime("\n%Y-%m-%d %H:%M:%S\n",
                                          time.localtime(time.time())))
        except: pass
        
    def close_log(self):
        try:
            self._log.close()
        except: pass
        
    def log(self, msg, push=False, pop=False, reset=False):
        assert not (push and pop)
        if not hasattr(self, '_nesting_depth') or reset:
            self._nesting_depth = 0
        indent = '    '*self._nesting_depth
        sys.stdout.write("%s%s\n" % (indent, msg))
        try: self._log.write("%s%s\n" % (indent, msg))
        except: pass
        if push:
            self._nesting_depth += 1
        elif pop:
            self._nesting_depth -= 1

    def assert_true(self, predicate, msg):
        try:
            if not predicate:
                raise InstallException(msg)
        except InstallException, m:
            self.log(''.join(format_exception(*sys.exc_info())),
                     reset=True)
            sys.exit(1)
                     
    def _get_database_admin_passwort(self):
        pw = self.config.DATABASE_ADMIN_PASSWORD
        if pw == 'ASK':
            try: return self._cached_pw
            except: pass
            import getpass
            print
            pw = getpass.getpass("Datenbankadministrator-Passwort: ")
            print
            self._cached_pw = pw
        return pw
    
    def find_ebkus_conf(self, where):
        """Gibt es bereits eine ebkus.conf in einem der in 'where'
        aufgelisteten Verzeichnissen?
        """
        for dir in where:
            ebkus_conf = join(dir, 'ebkus.conf')
            if exists(ebkus_conf):
                self._ebkus_conf = ebkus_conf
                self.log("Konfigurationsdatei: %s" % ebkus_conf)
                assert_readable(ebkus_conf)
                return ebkus_conf
        self.log("keine Konfigurationsdatei gefunden")
        return None

    def init_config(self, instance=None, instance_conf=None):
        """liest ebkus.conf ein und gibt config-Objekt zurueck
        Falls ein Instanzname uebergeben wird, wird die Konfiguration
        fuer diese Instanz erzeugt.
        
        self.config wird nicht gesetzt, kann daher auch von Instanzen
        genutzt werden.
        """
        assert_readable(self._ebkus_conf)
        conf_files = [self._ebkus_conf]
        if instance and instance_conf:
            assert_readable(instance_conf)
            conf_files.append(instance_conf)
        import ebkus.config
        ebkus.config.init(instance, conf_files)
        return ebkus.config.config


# http://prdownloads.sourceforge.net/mysql-python/MySQL-python.exe-0.9.2.win32-py2.3.exe
# http://prdownloads.sourceforge.net/mysql-python/MySQL-python-0.9.2.tar.gz

    def init_components(self):
        # Klassenvariablen werden von allen Instanzen von Component geerbt.
        Component.config = self.config
        Component.installer = self

        # die download URLs sind ausgelagert in download.py
        from ebkus import download as d
        def spl(url):
            i = url.rindex('/')
            return url[:i], url[i+1:]

        # archive_dir: der Name des obersten Verzeichnisses eines Archivs in dem
        #              alle Dateien direkt oder in Unterverzeichnissen stehen
        #              Falls dieses Feld leer ist, gibt es in diesem Archiv kein
        #              gemeinsames Oberberzeichnis
        # target_dir:  der Name des obersten Verzeichnisses nach der Installation.
        #              Bleibt leer, falls durch die Installation kein oberstes
        #              Verzeichnis fuer die Komponente angelegt wird.

        python = Component('python')
        if win32:
            python.url = spl(d.python_win32)[0]
            python.archive = spl(d.python_win32)[1]
        else:
            python.url = spl(d.python_linux)[0]
            python.archive = spl(d.python_linux)[1]
        self.python = python

        mysql_python = ComponentMySQLPython('mysql_python')
        mysql_python.url = spl(d.mysql_python_win32)[0]
        if win32:
            mysql_python.url = spl(d.mysql_python_win32)[0]
            mysql_python.archive = spl(d.mysql_python_win32)[1]
            mysql_python.archive_dir = 'mysql-python-1.0.0.win32-py2.3'
            mysql_python.target_dir = ''
        else:
            mysql_python.url = spl(d.mysql_python_linux)[0]
            mysql_python.archive = spl(d.mysql_python_linux)[1]
        self.mysql_python = mysql_python

        mysql = ComponentMySQL('mysql')
        mysql.url =  spl(d.mysql_win32)[0]
        if win32:
            mysql.url =  spl(d.mysql_win32)[0]
            mysql.archive = spl(d.mysql_win32)[1]
            mysql.archive_dir = 'mysql-4.0.18'
            mysql.target_dir = 'mysql'
            mysql.service_install_cmd = r"%s\bin\mysqld-nt --install" % mysql.install_path
            mysql.service_install_success_string = 'successfully installed'
            mysql.service_uninstall_cmd = r"%s\bin\mysqld-nt --remove" % mysql.install_path
            mysql.service_uninstall_success_string = 'successfully removed'
            mysql.service_name = 'MySQL'
        else:
            mysql.url =  spl(d.mysql_linux)[0]
            mysql.archive = spl(d.mysql_linux)[1]
        self.mysql = mysql

        reportlab = ComponentReportlab('reportlab')
        reportlab.url = spl(d.reportlab)[0]
        reportlab.archive = spl(d.reportlab)[1]
        reportlab.archive_dir = 'reportlab-1_19'
        reportlab.target_dir = ''
        self.reportlab = reportlab

        pygdchart = ComponentPygdchart('pygdchart')
        if win32:
            pygdchart.url = spl(d.pygdchart_win32)[0]
            pygdchart.archive = spl(d.pygdchart_win32)[1]
        else:
            pygdchart.url = spl(d.pygdchart_linux)[0]
            pygdchart.archive = spl(d.pygdchart_linux)[1]
        pygdchart.archive_dir = ''
        pygdchart.target_dir = ''
        self.pygdchart = pygdchart

        openssl = ComponentOpenssl('openssl')
        if win32:
            openssl.url = spl(d.openssl_win32)[0]
            openssl.archive = spl(d.openssl_win32)[1]
            openssl.archive_dir = ''
            openssl.target_dir = 'openssl'
        else:
            openssl.url = spl(d.openssl_linux)[0]
            openssl.archive = spl(d.openssl_linux)[1]
        self.openssl = openssl

        modssl = Component('modssl')
        if not win32:
            modssl.url = spl(d.modssl_linux)[0]
            modssl.archive = spl(d.modssl_linux)[1]
        self.modssl = modssl

        apache = ComponentApache('apache')
        if win32:
            apache.url = spl(d.apache_win32)[0]
            apache.archive = spl(d.apache_win32)[1]
            apache.archive_dir = ''
            apache.target_dir = 'apache'
            apache.service_install_cmd = r"%s\apache -n Apache -k install" %  apache.install_path
            apache.service_install_success_string = 'installed successfully'
            apache.service_uninstall_cmd = r"%s\apache -n Apache -k uninstall" % apache.install_path
            apache.service_uninstall_success_string = 'removed successfully'
            apache.service_name = 'Apache'
        else:
            apache.url = spl(d.apache_linux)[0]
            apache.archive = spl(d.apache_linux)[1]
        self.apache = apache

        srvstart = ComponentSrvstart('srvstart')
        if win32:
            srvstart.url = spl(d.srvstart_win32)[0]
            srvstart.archive = spl(d.srvstart_win32)[1]
            srvstart.archive_dir = ''
            srvstart.target_dir = 'srvstart'
        self.srvstart = srvstart

        ebkus = ComponentEbkus('ebkus')
        ebkus.url = ''
        ebkus.archive = ''
        ebkus.archive_dir = ''
        ebkus.target_dir = 'ebkus'
        ebkus.files = [
            'CHANGES.txt',
            'LICENSE.txt',
            'README.txt',
            'TODO.txt',
            'ebkus.conf',
            'configure.py',
            'uninstall.py',
            'doc',
            'lib',
            'htdocs',
            'sql',
            'templates',
            'vorlagen'
            ]
        self.ebkus = ebkus
        

class InstallFromDist(Installer):
    def __init__(self, dist_dir, install_dir, download_dir, uninstall_only=False):
        self._dist_dir = dist_dir
        self._install_dir = install_dir
        self._download_dir = download_dir
        self._uninstall_only = uninstall_only
        self._init_log(self._install_dir)
        
    def init(self):
        self.assert_true( exists(self._dist_dir), "Kein Distributionsverzeichnis")
        if not self._install_dir:
            raise InstallException("kein Installationsverzeichnis angegeben")
        if not exists(self._install_dir):
            raise InstallException("Installationsverzeichnis existiert nicht: %s" % self._install_dir)
        self.log("Installationsverzeichnis: %s" % self._install_dir)
        if not exists(self._download_dir):
            raise InstallException("Download-Verzeichnis existiert nicht: %s" % self._download_dir)
        self.log("Downloadverzeichnis: %s" % self._download_dir)
        ebkus_home = join(self._install_dir, 'ebkus')
        if self._uninstall_only:
            # Fuers deinstallieren wird auch eine ebkus.conf aus ebkus_home genommen
            #dirs = [ebkus_home, self._dist_dir]
            dirs = [ebkus_home]
        else:
            #dirs = [self._dist_dir]
            dirs = [ebkus_home]
        if not self.find_ebkus_conf(dirs):
            self.generate_default_ebkus_conf()
        self.config = self.init_config()
        self.config.EBKUS_DIST = self._dist_dir
        if not equalpath(self.config.DOWNLOAD_DIR, self._download_dir) \
           and not self._uninstall_only: # beim deinstallieren spielt
                                         # Downloadverzeichnis keine Rolle
            raise InstallException("Angegebenes Downloadverzeichnis nicht identisch mit dem in ebkus.conf")
        if not equalpath(self.config.INSTALL_DIR, self._install_dir):
            raise InstallException("Angegebenes Installationsverzeichnis nicht identisch mit dem in ebkus.conf")
            
        #self.config.show()
        self.init_components()

    def generate_default_ebkus_conf(self):
        """generiert eine default ebkus.conf in EBKUS_HOME"""
        ebkus_home = join(self._install_dir, 'ebkus')
        create_directory(ebkus_home)
        #ebkus_conf = join(self._dist_dir, 'ebkus.conf')
        ebkus_conf = join(ebkus_home, 'ebkus.conf')
        template = join(self._dist_dir, 'templates', 'ebkus.conf.template')
        # python auf windows immer mit '-u' aufrufen, sonst geht gar nichts ...
        if win32:
            minus_u = ' -u'
            OPENSSL_EXECUTABLE = join(self._install_dir, 'openssl', 'openssl.exe')
            MYSQL_DIR = join(self._install_dir, 'mysql', 'bin')
        else:
            minus_u = ''
            OPENSSL_EXECUTABLE = 'openssl'
            MYSQL_DIR = ''
        params = {'INSTALL_DIR': self._install_dir,
                  'DOWNLOAD_DIR': self._download_dir, 
                  'MYSQL_DIR': MYSQL_DIR, 
                  'EBKUS_PYTHON_PATH': join(ebkus_home, 'lib'),
                  'PYTHON_EXECUTABLE': sys.executable + minus_u,
                  'SERVER_NAME': 'localhost',
                  'SERVER_ADMIN': 'admin@localhost',
                  'OPENSSL_EXECUTABLE': OPENSSL_EXECUTABLE
                  }
        data = open(template, 'rU').read() % params
        file = open(ebkus_conf, 'w')
        file.write(data)
        file.close()
        os.chmod(ebkus_conf, 0600)
        self._ebkus_conf = ebkus_conf
        self.log("Konfigurationsdatei mit default-Werten erzeugt: %s" % ebkus_conf)


class InstallFromHome(Installer):
    def __init__(self, ebkus_home):
        self._ebkus_home = ebkus_home
        self._init_log(ebkus_home)
        
    def init(self):
        assert exists(self._ebkus_home)
        if not self.find_ebkus_conf([self._ebkus_home]):
            raise InstallException("Keine Konfigurationsdatei")
        self.config = self.init_config()
        assert equalpath(self.config.EBKUS_HOME, self._ebkus_home)
        #config.show()
        self.init_components()

    
class InstallFromInstance(Installer):
    """es wird vorausgesetzt, dass 'import init' ausgefuehrt wurde,
    es also eine gueltige config bereits gibt"""
    
    def __init__(self, config):
        self.config = config
        self._init_log(config.INSTANCE_HOME)

    def init(self):
        assert self.config
        self.log("Konfigurationsdatei: %s" % self.config.ebkus_conf)
        self._ebkus_conf = self.config.ebkus_conf
        if self.config.instance_conf:
            self.log("Zusaetzliche Konfigurationsdatei der Instanz: %s" %
                     self.config.instance_conf)
        self.init_components()
            
        
class Component(object):
    config = None
    installer = None

    def __init__(self, name):
        self.name = name
        self.service_name = name # wird fuer Instanzen ueberschrieben: ebkus-<name>
        self.installer.components[name] = self

    def _get_database_admin_passwort(self):
        return self.installer._get_database_admin_passwort()
        
    def log(self, msg, push=False, pop=False):
        self.installer.log(msg, push, pop)

    def get_install_path(self):
        return self._get_install_path()
    # wird evt. in Unterklassen ueberschrieben
    def _get_install_path(self):
        return join(self.config.INSTALL_DIR, self.target_dir)
    install_path = property(get_install_path, None, None)


    def install(self):
        if not self.installable():
            return
        self.log("%s installieren" % self.name, push=True)
        if self.is_installed():
            self.log('%s ist bereits installiert' % self.name, pop=True)
            return
        self._install()
        self.log("%s erfolgreich installiert" % self.name, pop=True)

    def configure(self):
        if not self.installable():
            return
        self.log("%s konfigurieren" % self.name, push=True)
        self._configure()
        self.log("%s erfolgreich konfiguriert" % self.name, pop=True)

    def _install(self):
        self.log("nichts zu installieren")
    def _configure(self):
        self.log("nichts zu konfigurieren")
        
    def uninstall(self):
        if not self.installable():
            return
        self.log("%s deinstallieren" % self.name, push=True)
        if not self.is_installed():
            self.log("%s war nicht installiert" % self.name, pop=True)
            return
        if not self.safe_to_remove():
            self.log("nicht deinstalliert", pop=True)
            return
        self._uninstall()
        self.log("%s deinstalliert" % self.name, pop=True)

    def _uninstall(self):
        if self.runs_as_service():
            self.stop_service()
            self.uninstall_service()
        ip = self.install_path
        if isdir(ip):
            #rmtree(ip, True)
            myrmtree(ip, logf=self.log)
        elif isfile(ip):
            remove(ip)

    def _download(self):
        if equalpath(self.config.DOWNLOAD_DIR, self.config.INSTALL_DIR):
            # nur wenn nicht explizit ein download-Verzeichnis
            # angegeben wurde suche wir in ../linux bzw ../win32
            # nach Software-Archiven (zB auf eine Distributions-CD)
            try:
                target = normpath(join(self.installer._dist_dir, '..',
                                       win32 and 'win32' or 'linux',
                                       self.archive))
                if exists(target):
                    self.archive_path = target
                    self.log('vorhanden: %s' % target)
                    return
            except:
                pass

        target = join(self.config.DOWNLOAD_DIR, self.archive)
        if exists(target):
            self.log('vorhanden: %s' % target)
        else:
            url = '%s/%s' % (self.url, self.archive)
            self.log('herunterladen: %s  ... ' % url, push=True)
            urlretrieve(url, target)
            self.log('erfolgreich heruntergeladen', pop=True)
        self.archive_path = target
        
    def is_installed(self):
        try:
            return exists(self.install_path)
        except:
            return False
    

    # wird fuer entsprechende Unterklassen ueberschrieben
    def installable(self):
        """kann die Komponente ueber dieses Skript
        installiert und konfiguriert werden?
        """
        return False

    # wird ueberschrieben in Unterklassen
    def safe_to_remove(self):
        """darf die Komponente ueber dieses Skript
        deinstalliert werden?
        """
        return True

    def _no_instances_configured(self):
        """darf die Komponente ueber dieses Skript
        deinstalliert werden? Nur wenn keine Instanzen mehr da sind.
        """
        # nicht wenn es noch ebkus Instanzen gibt
        ebkus_conf = join(self.config.EBKUS_HOME, 'ebkus.conf')
        for i in self.installer.ebkus.instances:
            if isdir(i.config.INSTANCE_HOME):
                self.log("Instanz %s existiert noch" % i.name)
                self.log("bitte erst deinstallieren")
                return False
        return True

    # wird fuer entsprechende Unterklassen ueberschrieben
    def runs_as_service(self):
        """kann die Komponente als Windows Dienst
        eingerichtet werden?
        """
        return False
    
    def popen(self, cmd, teststring=None):
        out_and_error, inp = popen2.popen4(cmd)
        res = out_and_error.read()
        out_and_error.close()
        inp.close()
        if not teststring:
            return res
        if res.find(teststring) > -1:
            return True
        else:
            return False
        
    def _unpack(self, tempdir=None):
        archive_path = self.archive_path
        if tempdir:
            add_to_path = tempdir
        elif self.archive_dir:
            # in diesem Fall habe alle Dateien im Archiv ein
            # gemeinsames Oberverzeichnis
            add_to_path = ''
        elif self.target_dir:
            # hier nicht
            add_to_path = self.target_dir
        else:
            raise IOError("Kein Verzeichnis zum Auspacken")
        unpack_dir = self.archive_dir or add_to_path
        self.unpack_path = join(self.config.INSTALL_DIR, unpack_dir)
        if exists(self.unpack_path):
            self.log('bereits entpackt: %s' % archive_path)
        else:
            self.log('entpacke: %s' % archive_path)
            z = zipfile.ZipFile(archive_path, 'r')
            z.extract(join(self.config.INSTALL_DIR, add_to_path))
        
    def _copy_to_python(self, src, lib=None):
        """Datei oder Verzeichnis src wird nach EBKUS_PYTHON_PATH
        kopiert und steht damit automatisch im Python Pfad.
        Falls src eine Liste ist, jedes Element der Liste kopieren"""
        if not lib:
            lib = self.config.EBKUS_PYTHON_PATH
            create_directory(lib)
        assert isdir(lib)
        #self.log('lib: ', lib)
        #self.log('src: ', src)
        if not isinstance(src, list):
            src = [src]
        assert isinstance(src, list)
        for el in src:
            self.log("kopieren:  %s  -->  %s" % (el, lib))
            mycopytree(el, lib)


    def install_service(self):
        if self.runs_as_service():
            self.log("%s Dienst installieren (Name des Dienstes: %s)" %
                     (self.name, self.service_name), push=True)
            if self.popen(self.service_install_cmd, self.service_install_success_string):
                self.log("erfolgreich installiert", pop=True)
            else:
                self.log("konnte nicht installiert werden", pop=True)

    def is_installed_service(self):
        if self.runs_as_service():
            if self.is_started_service():
                return True
            self.start_service()
            if self.is_started_service():
                self.stop_service()
                return True
        return False

    def is_started_service(self):
        if self.runs_as_service():
            return self.popen('net start', self.service_name)

    def uninstall_service(self):
        if self.runs_as_service():
            self.log("%s Dienst deinstallieren" % self.name, push=True)
            if self.popen(self.service_uninstall_cmd, self.service_uninstall_success_string):
                self.log("erfolgreich deinstalliert", pop=True)
            else:
                self.log("konnte nicht deinstalliert werden", pop=True)

    def start_service(self):
        if self.runs_as_service():
            if self.popen("net start %s" % self.service_name, "wurde erfolgreich gestartet"):
                self.log("%s Dienst gestartet" % self.name)
            else:
                self.log("%s Dienst konnte nicht gestartet werden" % self.name)

    def stop_service(self):
        if self.runs_as_service():
            if not self.is_started_service():
                return
            if self.popen("net stop %s" % self.service_name, "wurde erfolgreich beendet"):
                self.log("%s Dienst beendet" % self.name)
            else:
                self.log("%s Dienst konnte nicht beendet werden " % self.name)

class ComponentReportlab(Component):
    def installable(self):
        return True
    def _get_install_path(self):
        return join(self.config.EBKUS_PYTHON_PATH, 'reportlab')
    def _install(self):
        self._download()
        self._unpack()
        self._copy_to_python(join(self.unpack_path, 'reportlab'))

    def is_installed(self):
        return exists(join(self.config.EBKUS_PYTHON_PATH, 'reportlab'))

class ComponentPygdchart(Component):
    dll_name = win32 and 'gdchart.pyd' or 'gdchart.so'
    def installable(self):
        return True
    def _get_install_path(self):
        return join(self.config.EBKUS_PYTHON_PATH, self.dll_name)
    def _install(self):
        self._download()
        tempdir = join(self.config.INSTALL_DIR, self.archive + 'TMP')
        self._unpack(tempdir=tempdir)
        self._copy_to_python(join(tempdir, self.dll_name))
        rmtree(tempdir, True)


class ComponentMySQLPython(Component):
    def installable(self):
        """nur unter win32 installierbar"""
        return win32
    def _get_install_path(self):
        return join(self.config.EBKUS_PYTHON_PATH, 'MySQLdb')
    def _install(self):
        self._download()
        self._unpack()
        site = join(dirname(os.__file__), "site-packages")
        self._copy_to_python(join(self.unpack_path, 'MySQLdb'), site)
        self._copy_to_python(join(self.unpack_path, 'CompatMysqldb.py'), site)
        self._copy_to_python(join(self.unpack_path, '_mysql.pyd'), site)
        self._copy_to_python(join(self.unpack_path, '_mysql_exceptions.py'), site)
    def _uninstall(self):
        site = join(dirname(os.__file__, "site-packages"))
        for ip in [
            join(site, 'MySQLdb'),
            join(site, 'CompatMysqldb.py'),
            join(site, '_mysql.pyd'),
            join(site, '_mysql_exceptions.py'),
            ]:
            if isdir(ip):
                #rmtree(ip, True)
                myrmtree(ip, logf=self.log)
            elif isfile(ip):
                remove(ip)

class ComponentMySQL(Component):


    def setup(self):
        if self.is_ready_for_admin_connect():
            self.log("mysql ist betriebsbereit")
            return
        try:
            self.log("setup fuer mysql", push=True)
            self.install()
            self.configure()
            self.install_service()
            self.start_service()
            self.set_admin_password()
            self.log("mysql ist betriebsbereit", pop=True)
        except Exception, e:
            self.log("***** Fehler: mysql konnte nicht installiert werden.")
            self.log("***** Grund: %s" % str(e), pop=True)

    def installable(self):
        return win32
    def runs_as_service(self):
        return win32

    def _install(self):
        """
        - falls mysql dir in install_dir existiert [und
          c:\windows\my.init existiert, nichts machen]
        - runterladen, falls noch nicht in install_dir
        - auspacken
        - umbenennen
        - my.ini erzeugen
        - Datenbankrechte setzen: nur root von localhost mit passwort aus
          config.DATABASE_ADMIN_PASSWORD
        - als Dienst installieren
        - starten
        """
        self._download()
        self._unpack()
        rename(self.unpack_path, self.install_path)


    def safe_to_remove(self):
        """darf die Komponente ueber dieses Skript
        deinstalliert werden?
        """
        return self._no_instances_configured()
            

    def _configure(self):
        mysql_conf_path = join(os.getenv('SystemRoot'), 'my.ini')
        self.log("mysql Konfiguration erzeugen: %s" % mysql_conf_path)
        create_file(join(self.config.EBKUS_DIST, 'templates', 'my.ini.template'),
                   mysql_conf_path,
                   params = {'MYSQL_DIR': self.install_path,
                             'MYSQL_DATA_DIR': join(self.install_path, 'data')})
        # remove my.cnf
        mysql_cnf = join(os.getenv('SystemRoot'), 'my.cnf')
        if exists(mysql_cnf):
            remove(mysql_cnf)

    def is_ready_for_admin_connect(self):
        from MySQLdb import connect
        try:
            db = connect(host=self.config.DATABASE_ADMIN_HOST,
                     user=self.config.DATABASE_ADMIN_USER,
                     passwd=self._get_database_admin_passwort(),
                     db='mysql')
            return True
        except:
            return False
        

    def set_admin_password(self):
        if self.is_ready_for_admin_connect():
            self.log("Datenbankadministrator ist bereits eingerichtet.")
            return
        from MySQLdb import connect
        db = connect(host='localhost',
                     user='root',
                     passwd='',
                     db='mysql')
        cursor = db.cursor()
        self.log("Datenbankadministrator einrichten:  user=root  passwort=%s  host=localhost" % \
              self._get_database_admin_passwort())
        cursor.execute("DELETE FROM user WHERE host != 'localhost'")
        cursor.execute("DELETE FROM user WHERE user != 'root'")
        cursor.execute("UPDATE user SET password=" +
                       "PASSWORD('%s') WHERE user='root'" %
                       self._get_database_admin_passwort())
        cursor.execute("FLUSH PRIVILEGES")
        
class ComponentOpenssl(Component):
    def installable(self):
        return win32
    def _install(self):
        """
        - falls apache dir in install_dir existiert nichts machen
        - runterladen, falls noch nicht in install_dir
        - auspacken
        """
        self._download()
        self._unpack()

class ComponentApache(Component):
    def installable(self):
        return win32
    def runs_as_service(self):
        return win32

    def _install(self):
        """
        - falls apache dir in install_dir existiert nichts machen
        - runterladen, falls noch nicht in install_dir
        - dasselbe fuer openssl
        - auspacken
        - ssl libs kopieren
        - httpd.conf erzeugen
        - geht noch nicht: als Dienst installieren
        - geht noch nicht: starten
        """
        self._download()
        self._unpack()
        ip = self.install_path
        ssleay32_path = join(self.config.INSTALL_DIR, 'openssl', 'ssleay32.dll')
        libeay32_path = join(self.config.INSTALL_DIR, 'openssl', 'libeay32.dll')
        self.log("kopieren:  %s  -->  %s" % (ssleay32_path, ip))
        copy2(ssleay32_path, ip)
        self.log("kopieren:  %s  -->  %s" % (libeay32_path, ip))
        copy2(libeay32_path, ip)

    def _configure(self):
        ip = self.install_path
        apache_conf = join(ip, 'conf', 'httpd.conf')
        self.log("apache Konfiguration erzeugen: %s" % apache_conf)
        create_file(join(self.config.EBKUS_DIST, 'templates', 'httpd.conf.template'),
                   apache_conf,
                   params = {'SERVER_ROOT': ip,
                             'EBKUS_HTTPD_CONF': join(self.config.EBKUS_HOME, 'ebkus_httpd.conf')})

    def safe_to_remove(self):
        """nicht entfernen wenn noch Instanzen da sind, so wie für mysql."""
        return self._no_instances_configured()
    
class ComponentSrvstart(Component):
    def installable(self):
        return win32
    def _install(self):
        """
        - falls apache dir in install_dir existiert nichts machen
        - runterladen, falls noch nicht in install_dir
        - auspacken
        """
        self._download()
        self._unpack()

class ComponentEbkus(Component):
    # Liste der Instanzen aus ebkus.conf
    # Jedes Element ist Instanz von ComponentEbkusInstance.
    instances = []

    def __getitem__(self, name):
        try:
            if name.startswith('EBKuS-'):
                name = name[6:]
            instance = getattr(self, name)
        except:
            instance = None
        if not instance or instance not in self.instances:
            return None
        else:
            return instance
            

    def __init__(self, name):
        #Component.__init__(self, name)
        super(ComponentEbkus, self).__init__(name)
        for i in self.config.get_instances():
            self._create_instance(i)

    def is_installed(self):
        already_installed = True
        for f in self.files:
            target = join(self.config.EBKUS_HOME, f)
            if not exists(target):
                already_installed = False
                break
        return already_installed
            
        
    def installable(self):
        return True

    def _install(self):
        self.log("Verzeichnis erzeugen: %s" % self.config.EBKUS_HOME)
        create_directory(self.config.EBKUS_HOME)
        for f in self.files:
            src = join(self.config.EBKUS_DIST, f)
            mycopytree(src, self.config.EBKUS_HOME, exclude_dirs=['CVS'],
                       overwrite=True, logf=self.log)

    def uninstall(self):
        # erst alle Instanzen
        for i in self.instances:
            i.uninstall()
        # dann selbst
        #Component.uninstall(self)
        super(ComponentEbkus, self).uninstall()

    def safe_to_remove(self):
        for i in self.instances:
            if i.is_installed():
                self.log("Instanz %s muss zuerst deinstalliert werden" % i.name)
                return False
        return True

    def _configure(self):
        dirs, files = self._get_ebkus_dirs_and_files()
        for path, mode in dirs:
            self.log("Verzeichnis erzeugen: %s" % path)
            create_directory(path, mode)
        for tmpl, path, mode in files:
            self.log("Datei erzeugen: %s" % path)
            create_file(tmpl, path, vars(self.config), mode=mode)
        self.makeCertificates()
## Ich dachte ein funktionierender httpd.conf für Linux wäre auch sinnvoll,
## aber so geht es nicht, das das template windows- und installationsspezifisch ist            
##         path =  join(self.config.EBKUS_HOME, 'httpd.conf')
##         self.log("Datei erzeugen: %s" % path)
##         create_file(join(self.config.EBKUS_HOME, 'templates', 'httpd.conf.template'),
##                     path,
##                     params = {'SERVER_ROOT': '/srv/www/htdoc',
##                               'EBKUS_HTTPD_CONF': join(self.config.EBKUS_HOME, 'ebkus_httpd.conf')})

    def _get_ebkus_dirs_and_files(self):
        TEMPLATES = join(self.config.EBKUS_HOME, 'templates')
        dirs = (
            (self.config.APACHE_LOG_DIR, 0755),
            )

        files = (
            (join(TEMPLATES, 'openssl.cnf.template'),
             join(self.config.EBKUS_HOME, 'openssl.cnf'), 0644),
            (join(TEMPLATES, 'ebkus_httpd.conf.template'),
             join(self.config.EBKUS_HOME, 'ebkus_httpd.conf'), 0644),
            (join(TEMPLATES, 'configure.py.template'),
             join(self.config.EBKUS_HOME, 'configure.py'), 0700),
        )
        return dirs, files

    def makeCertificates(self):
        self.log("SSL Zertifikate erzeugen", push=True)
        config = self.config
        certificates_path = join(config.EBKUS_HOME, 'ebkus_ssl_certificates')
        certificate_file = join(certificates_path, 'ebkusserver.cert')
        if not equalpath(config.SSL_CERTIFICATE_FILE, certificate_file):
            self.log('*** ACHTUNG: Es sind nicht die Standard-SSL-Zertifikate konfiguriert.')
            self.log('             Stellen Sie selber sicher, dass die entsprechenden Dateien')
            self.log('             existieren und korrekt sind.', pop=True)
        openssl_cnf_path = os.path.join(config.EBKUS_HOME, 'openssl.cnf')
        if isfile(certificate_file):
            # keine Erzeugung falls Verzeichnis existiert
            self.log('Zertifikate existieren bereits', pop=True)
            return
        create_directory(certificates_path, 0755)
        try:
            cwd = os.getcwd()
            os.chdir(certificates_path)
            self.popen("%s req -config %s -new -out ebkusserver.csr" %
                      (config.OPENSSL_EXECUTABLE, openssl_cnf_path))
            self.popen("%s rsa -in privkey.pem -passin pass:%s -out ebkusserver.key" %
                      (config.OPENSSL_EXECUTABLE, config.OUTPUT_PASSWORD))
            self.popen("%s x509 -in ebkusserver.csr -out ebkusserver.cert \
            -req -signkey ebkusserver.key -days 3650" % config.OPENSSL_EXECUTABLE)
            self.log("erfolgreich erzeugt", pop=True)
        finally:
            os.chdir(cwd)
    
    def _create_instance(self, instance_name):
        assert instance_name in self.config.get_instances()
        if hasattr(self, instance_name):
            raise InstallException("nicht zulaessing als Instanzname: %s" % instance_name)
        config = self.config.copy(instance_name)
        instance_home = config.INSTANCE_HOME
        instance_conf = join(instance_home, instance_name + '.conf')
        # falls eine eigene .conf existiert
        if exists(instance_conf):
            assert_readable(instance_conf)
            config = self.installer.init_config(instance_name, instance_conf)
        
        instance = ComponentEbkusInstance(instance_name)
        instance.config = config
        assert instance.name == instance_name
        instance.service_name = "EBKuS-%s" % instance.name
        srv_conf = normpath("%s\srvstart.conf" % config.INSTANCE_HOME)
        instance.service_install_cmd = r"%s\srvstart\srvstart.exe install %s -c %s" % \
                                       (config.INSTALL_DIR, instance.service_name,
                                        srv_conf)
        instance.service_install_success_string = 'created non-desktop service'
        instance.service_uninstall_cmd = r"%s\srvstart\srvstart.exe remove %s" % \
                                         (config.INSTALL_DIR, instance.service_name)
        instance.service_uninstall_success_string = 'Deletion of service'
        self.instances.append(instance)
        setattr(self, instance_name, instance)

class ComponentEbkusInstance(Component):
    # diese Methoden machen hier keinen Sinn
    _download = _unpack = lambda self: None

    def _get_install_path(self):
        return self.config.INSTANCE_HOME

    def is_installed(self):
        home = self.config.INSTANCE_HOME
        if exists(join(home, 'start.py')) and \
               exists(join(home, 'init.py')):
            return True
        return False

    def installable(self):
        return True
    def runs_as_service(self):
        return win32

    def _configure(self):
        assert self.name == self.config.INSTANCE_NAME
        dirs, files = self._get_instance_dirs_and_files()
        self.log("Verzeichnis erzeugen: %s" % self.config.INSTANCE_HOME)
        create_directory(self.config.INSTANCE_HOME, 0755)
        for path, mode in dirs:
            self.log("Verzeichnis erzeugen: %s" % path)
            create_directory(path, mode)
        params = vars(self.config)
        if not win32:
            # wird für das ebkus_server template gebraucht (sudo -u $EBKUS_USER)
            import getpass
            params['EBKUS_USER'] = getpass.getuser()
        for tmpl, path, mode in files:
            # bloeder hack, damit dienst.py nicht unter linux auftaucht:
            if not win32 and path.endswith('dienst.py'):
                continue
            if win32 and path.endswith('ebkus_%s' % self.config.INSTANCE_NAME):
                continue
            self.log("Datei erzeugen: %s" % path)
            create_file(tmpl, path, params, mode=mode)
        
            
        self._add_instance_to_ebkus_httpd_config()
        # falls Datenbank fuer die Instanz noch nicht existiert, einrichten
        if self.check_instance_database():
            self.log("Datenbank betriebsbereit: name=%s" % self.config.DATABASE_NAME)
        else:
            self.create_database()
        if win32:
            srv_conf = join(self.config.INSTANCE_HOME, 'srvstart.conf')
            self.log("Datei erzeugen: %s" % srv_conf)
            create_file(
                join(self.config.EBKUS_HOME, 'templates', 'srvstart.conf.template'),
                srv_conf,
                params = {'INSTANCE_HOME': self.config.INSTANCE_HOME,
                          'SERVICE_NAME': self.service_name,
                          'PYTHON_EXECUTABLE': self.config.PYTHON_EXECUTABLE
                          })

    def _uninstall(self):
        self._remove_instance_from_ebkus_httpd_config()
        # dump nach Installationsverzeichnis, da EBKUS_HOME
        # und INSTANCE_HOME evt. geloescht werden sollen
        if not self.dump_database(dir=self.config.INSTALL_DIR):
            self.log("Fehler beim Datenbank-Dump")
        # muss hier bereits gedumpt sein!
        self.drop_database()
        super(ComponentEbkusInstance, self)._uninstall()
        
    def safe_to_remove(self):
        daten_dir = join(self.config.INSTANCE_HOME, 'daten')
        protocol_dir = self.config.PROTOCOL_DIR
        if dir_and_subdirs_contain_files(daten_dir):
            self.log("Datenverzeichnis enthaelt noch Dateien")
            return False
        if dir_and_subdirs_contain_files(protocol_dir):
            self.log("Protokollverzeichnis enthaelt noch Dateien")
            return False
        return True
    
    def check_instance_database(self):
        import traceback
        from MySQLdb.constants.ER import BAD_DB_ERROR
        from MySQLdb import OperationalError
        from MySQLdb import connect
        try:
            db = connect(host=self.config.DATABASE_HOST,
                         user=self.config.DATABASE_USER,
                         passwd=self.config.DATABASE_PASSWORD,
                         db=self.config.DATABASE_NAME)
        except Exception, e:
##             print "Die Datenbank '%s' konnte nicht geoeffnet werden." % self.config.DATABASE_NAME
##             print "Grund: %s" % str(e)
##             traceback.print_exc()
            return False
        return True

    def create_database(self, sql_file=None):
        self.log("Datenbank fuer %s einrichten" % self.name, push=True)
        from MySQLdb import connect
        db = connect(host=self.config.DATABASE_ADMIN_HOST,
                     user=self.config.DATABASE_ADMIN_USER,
                     passwd=self._get_database_admin_passwort()
                     )
        cursor = db.cursor()
        try:
            cursor.execute("DROP DATABASE %s" % self.config.DATABASE_NAME)
        except:
            pass
        grant_statement = ("GRANT ALL PRIVILEGES ON %(DATABASE_NAME)s.* " + 
                          "TO %(DATABASE_USER)s@'%(DATABASE_HOST)s' " + 
                          "IDENTIFIED BY '%(DATABASE_PASSWORD)s'") % vars(self.config)
        #print grant_statement
        cursor.execute(grant_statement)
        cursor.execute("FLUSH PRIVILEGES")    
        self.log(("name=%(DATABASE_NAME)s  user=%(DATABASE_USER)s  " + 
              "passwort=%(DATABASE_PASSWORD)s  host=%(DATABASE_HOST)s") % vars(self.config))
        try:
            cursor.execute("CREATE DATABASE %s" % self.config.DATABASE_NAME)
            cursor.execute("USE %s" % self.config.DATABASE_NAME)
            #mysql_bin_path = join(INSTALL_DIR, 'mysql', 'bin')
            if not sql_file:
                # berlin.sql
                # standard.sql
                # demo_berlin.sql
                # demo_standard.sql
                if self.config.BERLINER_VERSION:
                    sql_file = 'berlin'
                else:
                    sql_file = 'standard'
                if self.config.INSTANCE_NAME.startswith('demo'):
                    sql_file = 'demo_%s' % sql_file
                sql_file = join(self.config.EBKUS_HOME, 'sql', '%s.sql' % sql_file)
            if not exists(sql_file):
                if exists(sql_file + '.gz'):
                    sql_file += '.gz'
                else:
                    # muss erzeugt werden aus migrate_*, strkat_*, demo_daten
                    self.log("keine initiale Datenbank vorhanden")
                    str_kat = demo_daten = None
                    if self.config.INSTANCE_NAME.startswith('demo'):
                        demo_daten = 'demo_daten.py'
                    if self.config.BERLINER_VERSION:
                        merkmale_file_in = 'merkmale_berlin.py'
                        if self.config.INSTANCE_NAME.startswith('demo'):
                            str_kat = 'strassen_katalog_berlin_ausschnitt.txt.gz'
##                             demo_daten = 'demo_daten.py'
                        else:
                            str_kat = 'strassen_katalog_berlin.txt.gz'
                        str_kat = join(self.config.EBKUS_HOME, 'sql', str_kat)
                    else:
                        merkmale_file_in = 'merkmale_standard.py'
##                         if self.config.INSTANCE_NAME.startswith('demo'):
##                             demo_daten = 'demo_daten.py'
                    merkmale_file_in = join(self.config.EBKUS_HOME, 'sql', merkmale_file_in)
##                     if demo_daten:
##                         demo_daten = join(self.config.EBKUS_HOME, 'sql', demo_daten)
                    self.generate_initial_database(merkmale_file_in,
                                                   sql_file,
                                                   str_kat=str_kat,
                                                   demo_daten=demo_daten)

            self.log("initialisieren mit %s" % sql_file)
            for c in sql_split(sql_file):
                #print c
                cursor.execute(c)
            assert self.check_instance_database()
            self.log("Datenbank fuer %s erfolgreich eingrichtet" % self.name, pop=True)
        except:
            cursor.execute("DROP DATABASE %s" % self.config.DATABASE_NAME)
            self.log("Datenbank fuer %s konnte nicht eingerichtet werden" % self.name, pop=True)
            raise

    def backup_instance(self, dir=None):
        """erstellt eine ZIP-Datei, die alle Daten einer Instanz enthält.

        Daten einer Instanz sind:
        - daten/akten
        - daten/gruppe
        - dump...sql

        ZIP-Datei wird nach dir geschrieben mit einem eindeutigen Namen.
        Default-dir ist EBKUS_HOME.
        """
        if not dir:
            dir = self.config.EBKUS_HOME
        from ebkus import Version
        zip_archive = "%s_backup_v%s_%s.zip" % (self.config.INSTANCE_NAME,
                                                Version,
                                                time.strftime("%Y-%m-%d_%H-%M-%S",
                                                              time.localtime(time.time())))
        zip_archive = join(dir, zip_archive)
        self.log("Backup nach %s" % zip_archive)
        assert isdir(dir), "Backup-Verzeichnis existiert nicht: %s" % dir
        sql_file = self.dump_database(dir)
        if not sql_file:
            self.log("Fehler beim Backup von %s" % self.config.INSTANCE_NAME)
            return False
        cwd = os.getcwd()
        try:
            try:
                os.chdir(self.config.INSTANCE_HOME)
                zip = zipfile.ZipFile(zip_archive, 'w', zipfile.ZIP_DEFLATED)
                zip.write(sql_file, basename(sql_file))
                self.log("Archivieren von daten/akten und daten/gruppen")
                for root,dirs,files in os.walk('daten'):
                    if 'export' in dirs:
                        dirs.remove('export')
                    for f in files:
                        zip.write(join(root, f))
                self.log("Backup erfolgreich: %s" % zip_archive)
                return zip_archive
            except Exception, msg:
                try: os.remove(zip_archive)
                except: pass
                self.log(msg)
                self.log("Fehler beim Backup von %s" % self.config.INSTANCE_NAME)
                return False
        finally:
            try: os.remove(sql_file)
            except: pass
            os.chdir(cwd)
        
    def restore_instance(self, zip_archive):
        """Stellt eine Instanz wieder her aus einem ZIP-File"""
        self.log("Instanz wiederherstellen aus %s" % zip_archive, push=True)
        try:
            if dir_and_subdirs_contain_files(
                join(self.config.INSTANCE_HOME, 'daten', 'akten')) or \
                dir_and_subdirs_contain_files(
                join(self.config.INSTANCE_HOME, 'daten', 'gruppen')):
                raise Exception("daten/akten bzw. daten/gruppen muessen leer sein")
            zip = zipfile.ZipFile(zip_archive, 'r')
            sql_file = None
            sql_files = [f.filename for f in zip.infolist()
                         if re.match("%s_dump.+sql" % self.config.INSTANCE_NAME,
                                     f.filename)]
            if len(sql_files) != 1:
                raise Exception("Archiv muss genau eine SQL-Dump-Datei fuer diese Instanz haben.")
            sql_file = sql_files[0]
            for finfo in zip.infolist():
                name = finfo.filename
                if not(name == sql_file or
                       re.match("daten.(akten|gruppen)", name)):
                    raise Exception("Falsche Datei in Archiv: %s" % name)
            for finfo in zip.infolist():
                path = join(self.config.INSTANCE_HOME, finfo.filename)
                dirs = dirname(path)
                if dirs:
                    create_directory(dirs, 0700)
                f = open(path, 'w')
                f.write(zip.read(finfo.filename))
                f.close()
                os.chmod(path, 0600)
                Y,M,D,h,m,s = finfo.date_time
                t = time.mktime((Y,M,D,h,m,s,0,1,-1))
                os.utime(path, (t,t))
                self.log("wiederhergestellt: %s" % path)
            sql_file = join(self.config.INSTANCE_HOME, sql_file)
            self.create_database(sql_file)
            os.remove(sql_file)
            self.log("Wiederherstellung erfolgreich", pop=True)
        except Exception, msg:
            #self.log(''.join(format_exception(*sys.exc_info())))
            self.log(msg)
            self.log("Fehler beim Wiederherstellen von %s" %
                     self.config.INSTANCE_NAME, pop=True)
            return False
            
                
            
        
    def dump_database(self, dir=None):
        """macht einen Dump der Datenbank der Instanz im Verzeichnis dir.

        Falls dir None ist, wird der dump in EBKUS_HOME abgelegt.
        """
        if not dir:
            dir = self.config.EBKUS_HOME
        self.log("Datenbank-Dump erzeugen", push=True)
        self.log("Datenbankname: %s" % self.config.DATABASE_NAME)
        if not exists(dir):
            raise InstallException("Verzeichnis %s existiert nicht" % dir)
        from ebkus import Version
        file_name = "%s_dump_v%s_%s.sql" % (self.config.INSTANCE_NAME,
                                            Version,
                                            time.strftime("%Y-%m-%d_%H-%M-%S",
                                                          time.localtime(time.time())))
        file_name = join(dir, file_name)
        self.log("SQL-Datei: %s" % file_name)
        pw = self.config.DATABASE_PASSWORD
        pw_arg = pw and "-p%s" % pw or ''
        self.log("SQL-Datei ausgeben")
        cmd = "%s -c -u%s %s %s > %s" % \
                  (join(self.config.MYSQL_DIR, 'mysqldump'),
                   self.config.DATABASE_USER,
                   pw_arg,
                   self.config.DATABASE_NAME,
                   file_name)
        #print cmd
        res = os.system(cmd)
        if res == 0:
            self.log("Datenbank-Dump erfolgt", pop=True)
            return file_name
        else:
            self.log("Fehler beim Datenbank-Dump", pop=True)
            return False
            

    def drop_database(self):
        self.log("Datenbank fuer %s loeschen" % self.name, push=True)
        from MySQLdb import connect
        db = connect(host=self.config.DATABASE_ADMIN_HOST,
                     user=self.config.DATABASE_ADMIN_USER,
                     passwd=self._get_database_admin_passwort()
                     )
        cursor = db.cursor()
        try:
            cursor.execute("DROP DATABASE %s" % self.config.DATABASE_NAME)
            self.log("erfolgreich geloescht", pop=True)
        except:
            self.log("konnte nicht geloescht werden", pop=True)
        
    def generate_initial_database(self, merkmale_file_in, sql_file_out,
                                  str_kat=None, demo_daten=None):
        """Initiale Datenbank erzeugen und als SQL-Dump sichern.
        
        merkmale_file_in: migrdata-artige Datei als Eingabe
        sql_file_out: mit mysqldump erzeugte sql Datei als Ausgabe
        str_kat: Strassenkatalog als Textdatei. Kann None sein, dann wird
        keiner eingelesen.

        Die Datenbank wird nach dem Dump aus mysql geloescht.
        """
        # rein kosmetisch
        import warnings
        warnings.filterwarnings('ignore', '', DeprecationWarning, 'ebkus\.app\.protocol', 11)

        self.log("leere Datenbank aus Merkmaldatei erzeugen", push=True)
        self.log("Eingabe Merkmaldatei: %s" % merkmale_file_in)
        database_name = self.name + '_XX_init_XX'
        import ebkus.config
        ebkus.config.config = self.config
        from ebkus.gen.schemagen import init_new_db
        from ebkus.gen.schemadata import schemainfo
        from ebkus.gen.migrate import migrate
        from ebkus.gen.migrate_strkat import read_strkat
        from ebkus.db.sql import opendb, closedb, getDBHandle
        opendb(host=self.config.DATABASE_ADMIN_HOST, user=self.config.DATABASE_ADMIN_USER,
           passwd=self._get_database_admin_passwort())
        # direkt die MySQLdb ohne Adapter
        cursor = getDBHandle().dbhandle.cursor()
        try:
            cursor.execute("DROP DATABASE %s" % database_name)
        except:
            pass
        try:
            cursor.execute("CREATE DATABASE %s" % database_name)
            cursor.execute("USE %s" % database_name)
            self.log("Schema generieren ...")
            init_new_db(schemainfo, False)
            self.log("Kategorien/Codes anlegen ...")
            migrate(merkmale_file_in)
            if str_kat:
                self.log("Strassenkatalog einlesen (kann lange dauern!) ...")
                read_strkat(str_kat)
            if demo_daten:
                self.log("Demo-Daten einfuegen")
                from ebkus.gen.demo_daten import create_demo_daten
                create_demo_daten()
##                 globals = {}
##                 execfile(demo_daten, globals)
##                 globals['create_demo_daten']()
            pw = self._get_database_admin_passwort()
            pw_arg = pw and "-p%s" % pw or ''
            self.log("SQL-Datei ausgeben: %s" % sql_file_out)
            os.system("%s -c -u%s %s %s > %s" %
                      (join(self.config.MYSQL_DIR, 'mysqldump'),
                       self.config.DATABASE_ADMIN_USER,
                       pw_arg,
                       database_name,
                       sql_file_out)
                      )
        finally:
            cursor.execute("DROP DATABASE %s" % database_name)
            closedb()
        self.log("erfolgreich erzeugt", pop=True)

    def _add_instance_to_ebkus_httpd_config(self):
        script_alias = "ScriptAlias /ebkus/%(INSTANCE_NAME)s/cgi/ %(DOCUMENT_ROOT)s/cgi/" \
                       % vars(self.config)
        alias = "Alias /ebkus/%(INSTANCE_NAME)s/ %(DOCUMENT_ROOT)s/" \
                % vars(self.config)
        assert self.config.INSTANCE_NAME == self.name
        ebkus_httpd_conf = join(self.config.EBKUS_HOME, 'ebkus_httpd.conf')
        f = open(ebkus_httpd_conf, 'rU')
        text = f.read()
        f.close()
        i = text.find(script_alias)
        if i > -1:
            # schon drin, pruefen, ob der andere auch drin ist
            if not text.find(alias) > 1:
                raise InstallException("Fehler in %s ; bitte manuell reparieren" % ebkus_httpd_conf)
            else:
                return
        text = text.replace('#INSTANCE_SCRIPT_ALIAS', script_alias)
        text = text.replace('#INSTANCE_ALIAS', alias +
                            # Platzhalter fuer weitere Instanzenx
                            '\n\n#INSTANCE_SCRIPT_ALIAS\n#INSTANCE_ALIAS')
        f = open(ebkus_httpd_conf, 'w')
        f.write(text)
        f.close()
        self.log("ebkus_httpd.conf erfolgreich fuer %s angepasst" % self.name)
    
    def _remove_instance_from_ebkus_httpd_config(self):
        script_alias = "ScriptAlias /ebkus/%(INSTANCE_NAME)s/cgi/ %(DOCUMENT_ROOT)s/cgi/" \
                       % vars(self.config)
        alias = "Alias /ebkus/%(INSTANCE_NAME)s/ %(DOCUMENT_ROOT)s/" \
                % vars(self.config)
        assert self.config.INSTANCE_NAME == self.name
        ebkus_httpd_conf = join(self.config.EBKUS_HOME, 'ebkus_httpd.conf')
        f = open(ebkus_httpd_conf, 'rU')
        text = f.read()
        f.close()
        i = text.find(script_alias)
        if i > -1:
            if not text.find(alias) > 1:
                raise InstallException("Fehler in %s ; bitte manuell reparieren" % ebkus_httpd_conf)
            else:
                text = text.replace(script_alias + '\n', '')
                text = text.replace(alias + '\n\n', '')
                f = open(ebkus_httpd_conf, 'w')
                f.write(text)
                f.close()
                self.log("Eintraege aus ebkus_httpd.conf fuer %s entfernt" % self.name)

    def _get_instance_dirs_and_files(self):
        config = self.config
        TEMPLATES = join(config.EBKUS_HOME, 'templates')
        dirs = (
            (join(config.INSTANCE_HOME, 'daten'), 0700),
            (join(config.INSTANCE_HOME, 'daten', 'export'), 0700),
            (join(config.INSTANCE_HOME, 'daten', 'akten'), 0700),
            (join(config.INSTANCE_HOME, 'daten', 'gruppen'), 0700),
            (join(config.DOCUMENT_ROOT, 'daten', 'export'), 0755),
            (join(config.DOCUMENT_ROOT, 'cgi'), 0755),
            (config.PROTOCOL_DIR, 0700)
            )

        files = (
            (join(TEMPLATES, 'init.py.template'),
             join(config.INSTANCE_HOME, 'init.py'), 0700),
            (join(TEMPLATES, 'start.py.template'),
             join(config.INSTANCE_HOME, 'start.py'), 0700),
            (join(TEMPLATES, 'stop.py.template'),
             join(config.INSTANCE_HOME, 'stop.py'), 0700),
            (join(TEMPLATES, 'status.py.template'),
             join(config.INSTANCE_HOME, 'status.py'), 0700),
            (join(TEMPLATES, 'ebkus_server.template'),
             join(config.INSTANCE_HOME,
                  'ebkus_%s' % config.INSTANCE_NAME), 0700),
            (join(TEMPLATES, 'datenbank_initialisieren.py.template'),
             join(config.INSTANCE_HOME, 'datenbank_initialisieren.py'), 0700),
            (join(TEMPLATES, 'datenbank_sichern.py.template'),
             join(config.INSTANCE_HOME, 'datenbank_sichern.py'), 0700),
            (join(TEMPLATES, 'dienst.py.template'),
             join(config.INSTANCE_HOME, 'dienst.py'), 0700),
            (join(TEMPLATES, 'index.html.template'),
             join(config.DOCUMENT_ROOT, 'index.html'), 0644),
            (join(TEMPLATES, 'ebcgi.py.template'),
             join(config.DOCUMENT_ROOT, 'cgi', 'do'), 0755)
        )
        return dirs, files

def _extract(self, todir='', matching=None):
    """monkey-patch fuer die ZipFile Klasse"""
    for name in self.namelist():
        if matching and not re.match(matching, name):
            continue
        path = join(todir, name)
        dir, fname = split(path)
        if dir:
            try:
                os.makedirs(dir, 0755)
                #print "created: %s" % dir
            except:
                #print "not created: %s" % dir
                pass
        #print "PATH %s" % path
        if fname:
            f = open(path, 'wb')
            f.write(self.read(name))
            f.close()

zipfile.ZipFile.extract = _extract

# Hilfsfunktionen

def sql_split(filename):
    """Generator der eine mysqldump-Datei in eine Liste von
    SQL-Statements zerlegt.

    Jedes Statement lässt sich mit
       db.cursor().execute(sql_statement)
    ausfuehren.

    Setzt voraus, dass jedes SQL-Statement in der Datei mit ';\n'
    abgeschlossen ist und dass alle Kommentarzeilen mit '--'
    beginnen.

    Es wird auch eine gzip komprimiert Datei akzeptiert.
    """
    if filename.lower().endswith('.gz'):
        import gzip
        f = gzip.GzipFile(filename)
    else:
        f = open(filename, 'rU')
    cmd = []
    while True:
        l = f.readline()
        if not l:
            break
        l = l.strip()
        if not l or l.startswith('--'):
            continue
        cmd.append(l)
        if l.endswith(';'):
            yield ''.join(cmd)
            cmd = []

def create_directory(path, mode=0755):
    try:
        os.makedirs(path, mode)
    except OSError, e:
        # ok wenn schon da
        if e.errno != errno.EEXIST:
            raise
            
def create_file(template, outfile, params, mode=0644):
    #print 'create_file', template, outfile
    #print params
    data = open(template, 'rU').read()
    #print data
    data = data % params
    file = open(outfile, 'w')
    file.write(data)
    file.close()
    os.chmod(outfile, mode)
    
def equalpath(p1, p2):
    return normcase(normpath(p1)) == normcase(normpath(p2))

def check_MySQLdb():
    print "gefunden:  Python Version %-10s" % sys.version
    try:
        import MySQLdb
        print "gefunden:  MySQLdb Version %-10s" % MySQLdb.__version__
        return True
    except ImportError:
        print "fehlt:  MySQLdb"
        print "******  Fehler: Bitte erst MySQLdb installieren"
        return False


def dir_and_subdirs_contain_files(dir):
    """Prueft, ob in dem Verzeichnis direkt oder in
    Unterverzeichnissen noch Dateien enthalten sind.
    """
    if not exists(dir):
        return False
    if isfile(dir):
        return True
    if not isdir(dir):
        return False
    els = os.listdir(dir)
    for e in els:
        f = join(dir, e)
        if isfile(f):
            return True
        elif isdir(f):
            res = dir_and_subdirs_contain_files(f)
            if res:
                return True
    return False

def myrmtree(path, logf=None):
    def onerror(func, arg, exc):
        if logf:
            logf("Konnte nicht geloescht werden: %s" % arg)
##         print "FUNC: %s" % func
##         print "ARG : %s" % str(arg)
##         print "EXC : %s" % str(exc)
    if logf:
        logf("Verzeichnisbaum loeschen: %s" % path, push=True)
    rmtree(path, onerror=onerror)
    if logf:
        logf("Verzeichnisbaum geloescht: %s" % path, pop=True)


def mycopytree(src, dst_dir, exclude_dirs=[], overwrite=True, logf=None):
    """kopiert src (entweder Datei oder Verzeichnis) in das
    Verzeichnis dst_dir, das existieren muss."""
    #print src, dst_dir
    if not isdir(dst_dir):
        raise IOError("%s ist kein existierendes Verzeichnis." % dst_dir)
    name = basename(src)
    if not name:
        name = basename(dirname(src))
        if not name:
            raise IOError("%s kann nicht kopiert werden." % src)
    if isdir(src):
        #print name, exclude_dirs
        if name in exclude_dirs:
            #print 'exclude %s --> %s' % (src, dst_dir)
            return
        else:
            #print 'dir %s --> %s' % (src, dst_dir)
            pass
        dst  = join(dst_dir, name)
        if not exists(dst):
            os.mkdir(dst, 0755)
        names = os.listdir(src)
        for n in names:
            src_name = join(src, n)
            mycopytree(src_name, dst, exclude_dirs, overwrite, logf)
    elif isfile(src):
        #print 'datei %s --> %s' % (src, dst_dir)
        file = join(dst_dir, name)
        if not exists(file) or overwrite:
            if logf:
                logf("kopieren: %s --> %s" % (src, dst_dir))
            copy2(src, dst_dir)
    else:
        #print 'nicht kopierbar %s --> %s' % (src, dst_dir)
        pass
        
def download(url, target):
    self.log('herunterladen: %s  ... ' % url, push=True)
    urlretrieve(url, target)
    self.log('erfolgreich heruntergeladen', pop=True)
