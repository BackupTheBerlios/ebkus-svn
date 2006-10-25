# coding: latin-1
from __future__ import generators

import sys, re, ConfigParser
from os.path import exists, normpath

class ConfigError(Exception):
    pass

config = None

# (section, Name fuer config Nutzer, Name in config Datei, typ, Default)  
# typ: p path, s string, i int, b boolean
# default modifier: i interpolate, e eval, s literal

_params = (
    ('ebkus', 'INSTALL_DIR', 'install_dir', 'p', None),
    ('ebkus', 'DOWNLOAD_DIR', 'download_dir', 'p', 'i:%(install_dir)s'),
##     ('ebkus', 'SW_LINUX_DIR', 'sw_linux_dir', 'p', 'i:%(install_dir)s/../linux'),
##     ('ebkus', 'SW_WIN32_DIR', 'sw_win32_dir', 'p', 'i:%(install_dir)s/../win32'),
    ('ebkus', 'EBKUS_HOME', 'ebkus_home', 'p', 'i:%(install_dir)s/ebkus'),
    ('ebkus', 'PYTHON_EXECUTABLE', 'python_executable', 'p', 'e:sys.executable'),
    ('ebkus', 'MYSQL_DIR', 'mysql_dir', 'p', 's:'),
    ('ebkus', 'EBKUS_PYTHON_PATH', 'ebkus_python_path', 'p', 'i:%(ebkus_home)s/lib'),
    ('ebkus', 'EBKUS_DOCUMENT_ROOT', 'ebkus_document_root', 'p', 'i:%(ebkus_home)s/htdocs/ebkus'),
    ('ebkus', 'DATABASE_ADMIN_HOST', 'database_admin_host', 's', 's:localhost'),
    ('ebkus', 'DATABASE_ADMIN_USER', 'database_admin_user', 's', 's:root'),
    ('ebkus', 'DATABASE_ADMIN_PASSWORD', 'database_admin_password', 's', 's:'),
    ('apache', 'SSL_CERTIFICATE_FILE', 'ssl_certificate_file', 'p',
     'i:%(ebkus_home)s/ebkus_ssl_certificates/ebkusserver.cert'),
    ('apache', 'SSL_CERTIFICATE_KEY_FILE', 'ssl_certificate_key_file', 'p',
     'i:%(ebkus_home)s/ebkus_ssl_certificates/ebkusserver.key'),
    ('apache', 'APACHE_LOG_DIR', 'apache_log_dir', 'p', 'i:%(ebkus_home)s/log'),
    ('apache', 'SERVER_ADMIN', 'server_admin', 's', 's:admin@localhost'),
    ('apache', 'SERVER_NAME', 'server_name', 's', 's:localhost'),
    ('openssl', 'STAAT', 'staat', 's', 's:DE'),
    ('openssl', 'LAND', 'land', 's', 's:Berlin'),
    ('openssl', 'ORT', 'ort', 's', 's:Berlin'),
    ('openssl', 'ORGANISATION', 'organisation', 's', 's:EFB'),
    ('openssl', 'ORGANISATIONSEINHEIT', 'organisationseinheit', 's', 's:EFB'),
    ('openssl', 'OUTPUT_PASSWORD', 'output_password', 's', 's:polo'),
    ('openssl', 'OPENSSL_EXECUTABLE', 'openssl_executable', 'p', 's:openssl'),
    ('instance', 'INSTANCE_NAME', 'instance_name', 's', None),
    ('instance', 'INSTANCE_HOME', 'instance_home', 'p', 'i:%(ebkus_home)s/%(instance_name)s'),
    ('instance', 'DATABASE_NAME', 'database_name', 's', 'i:%(instance_name)s'),
    ('instance', 'DATABASE_HOST', 'database_host', 's', 's:localhost'),
    ('instance', 'DATABASE_USER', 'database_user', 's', 'i:%(instance_name)s'),
    ('instance', 'DATABASE_PASSWORD', 'database_password', 's', 'i:%(instance_name)s'),
    ('instance', 'DATABASE_TYPE', 'database_type', 's', 's:MySQLdb'),
    ('instance', 'DOCUMENT_ROOT', 'document_root', 'p', 'i:%(instance_home)s/htdocs'),
    ('instance', 'PORT', 'port', 'i', None),
    ('instance', 'HOST', 'host', 's', 's:localhost'),
    ('instance','LOG_FILE',  'log_file', 'p', 'i:%(instance_home)s/%(instance_name)s.log'),
    ('instance','LOG_LEVEL',  'log_level', 's', 's:INFO'),
    ('instance', 'SITE', 'site', 's', 's:A'),
    ('instance', 'MASTER_SITE', 'master_site', 's', 's:A'),
    ('instance', 'LOESCHFRIST', 'loeschfrist', 'i', 's:36'),
    ('instance', 'SESSION_TIME', 'session_time', 'i', 's:120'),
    ('instance', 'PROTOCOL_DIR', 'protocol_dir', 'p', 'i:%(instance_home)s/protokolle'),
    ('instance', 'AK_DIRS_MAX', 'ak_dirs_max', 's', 's:100'),
    ('instance', 'ADMIN_NAME', 'admin_name', 's', 's:Keine Angabe'),
    ('instance', 'ADMIN_TEL', 'admin_tel', 's', 's:Keine Angabe'),
    ('instance', 'ADMIN_EMAIL', 'admin_email', 's', 's:Keine Angabe'),
    ('instance', 'BERLINER_VERSION', 'berliner_version', 'b', 'b:False')
    )

# werden von show/dump nicht angezeigt
_hide = (
##     'SW_LINUX_DIR', 'SW_WIN32_DIR',
    'EBKUS_PYTHON_PATH', 'EBKUS_DOCUMENT_ROOT',
    'DATABASE_TYPE', 'DOCUMENT_ROOT',
    'SITE', 'MASTER_SITE',
    'PROTOCOL_DIR', 'AK_DIRS_MAX'
         )

def init(instance_name, config_files, defaults={}):
    global config
    config = _Config(instance_name, config_files, defaults)
    return config

class _Config(object):
    def __init__(self, instance_name, config_files, defaults):
        self.instance_name = instance_name
        # ab python 2.3: self._conf = ConfigParser.SafeConfigParser()
        self._conf = ConfigParser.ConfigParser(defaults)
        self._conf.read(config_files)
        self._errors = []
        self._check_consistency()
        if self._errors:
            for e in self._errors:
                print
                print "Fehler in Konfiguration:\n%s" % e
                print
            raise ConfigError("Fehler in Konfiguration")
        self._init_PARAMS()
        # die Pfade von ebkus.conf und einer evt. <instance>.conf
        # werden an das config-Objekt drangepappt, obwohl es keine
        # richtigen Config-Variablen sind.
        # Ist aber nuetzlich im Programm.
        self.ebkus_conf = config_files[0]
        try:
            self.instance_conf = config_files[1]
            if not exists(self.instance_conf):
                self.instance_conf = None
        except:
            self.instance_conf = None
            
    def copy(self, instance_name=None):
        """erzeugt eine Kopie von sich selbst fuer instance_name
        """
        import copy
        cp = copy.copy(self)
        if instance_name:
            cp.set_instance(instance_name)
        return cp

    def get_instances(self):
        c = self._conf
        sections = c.sections()
        instances = [c.get(s, 'instance_name')
                     for s in sections
                     if c.has_option(s, 'instance_name')]
        self.all_instances = instances
        return instances
        
    def _is_ident(self, name):
        return re.match(r'^[a-z][a-z0-9_]*$', name)
    
    def _check_consistency(self):
        non_instance_sections = ['DEFAULT', 'ebkus', 'apache', 'openssl', 'mysql']
        c = self._conf
        ports = {}
        for s in c.sections():
            if s in non_instance_sections:
                if c.has_option(s, 'instance_name'):
                    self._error("Sektion '%s' darf keine Option 'instance_name' haben" % s)
            else:
                if not c.has_option(s, 'instance_name'):
                    self._error("Sektion '%s' muss eine Option 'instance_name' haben" % s)
                elif not s == c.get(s, 'instance_name'):
                    self._error("Option 'instance_name' in Sektion '%s' muss den Wert %s haben" % (s,s))
                elif not c.has_option(s, 'port'):
                    self._error("Option 'port' in Sektion '%s' fehlt" % s)
                elif c.getint(s, 'port') in ports:
                    self._error("Wert fuer 'port' in '%s' bereits vergeben" % s)
                else:
                    ports[c.getint(s, 'port')] = 1
                for o in ('instance_name', 'database_name',
                          #'database_user', 'database_password'):
                          # database_password kann auch grosse Buchstaben enthalten
                          'database_user'):
                    if c.has_option(s, o):
                        val = c.get(s, o)
                        if not self._is_ident(val):
                            self._error("""Wert '%s' fuer Option '%s' ungueltig.
Bitte nur kleine Buchstaben (keine Umlaute) und Unterstrich verwenden.""" % (val, o))
                            

           
    def _error(self, msg):
        self._errors.append(msg)

    def get(self, section, option):
        return self._conf.get(section, option)

    def _proc_default(self, default, pdict, param):
        if not default:
            self._error("Kein Wert fuer %s" % param)
            return 
        typ, val = default.split(':')
        if typ == 's':
            return val
        elif typ == 'i':
            return val % pdict
        elif typ == 'e':
            return eval(val)
        
    def _param_iterator(self, params):
        param_dict = {}
        for t in params:
            section = t[0]
            PARAM = t[1]
            param = t[2]
            assert PARAM.lower() == param
            typ = t[3]
            if typ in ('s', 'p'):
                f = self._conf.get
            elif typ == 'b':
                f = self._conf.getboolean
            elif typ == 'i':
                f = self._conf.getint
            if section == 'instance':
                section = self.instance_name
                if not section:
                    continue
            try:
                value = f(section, param)
##                 try:
##                     value = value.replace('\\', '/')
##                 except: pass
            except ConfigParser.NoOptionError:
                #print param
                value = self._proc_default(t[4], param_dict, param)
            # value darf nicht leer sein, sonst macht normpath '.' draus
            if value and typ in ('p',): 
                value = normpath(value)
            param_dict[param] = value
            yield section, PARAM, param, value, typ
        
    def _init_PARAMS(self):
        for s, P, p, v, t in self._param_iterator(_params):
            setattr(self, P, v)

    def set_instance(self, instance_name):
        assert instance_name is None or instance_name in self.get_instances()
        self.instance_name = instance_name
        self._init_PARAMS()

    def dump(self):
        l = []
        for s, P, p, v, t in self._param_iterator(_params):
            l.append("%s: %s" % (p, v))
        return '\n'.join(l)
        
    def show_section(self, sections):
        for section in sections:
            if section == 'DEFAULT':
                print "%-32s %s" % ('ebkus_conf', self.ebkus_conf)
                print "%-32s %s" % ('instance_conf', self.instance_conf or '')
            for s, P, p, v, t in self._param_iterator(_params):
                #print s, section
                if s == section and not P in _hide:
                    print "%-32s %s" % (p, v)
                    assert v == getattr(self, P)
            print

    def show(self, current=True, all=False):
        """current==True: zeigt Werte fuer die gesetzte Instanz
           current==False: zeigt Werte fuer alle Instanzen"""
        non_instance_sections = ['DEFAULT', 'ebkus', 'apache', 'openssl']
        if current and not all:
            sections = non_instance_sections
            sections.append(self.instance_name)
            self.show_section(sections)
            return
        instances = self.get_instances()
        save_instance_setting = self.instance_name
        self.show_section(non_instance_sections)
        for i in instances:
            self.set_instance(i)
            self.show_section([i])
        self.set_instance(save_instance_setting)

    def pp_PARAMS(self):
        for s, P, p, v, t in self._param_iterator(_params):
            print "%-15s %-32s %-25s %-3s  %s" % (s, P, p, t, v)
            assert v == getattr(self, P)


if __name__ == '__main__':
    #init('demo', '/home/atms/dev/ebkus/ebkus-2/ebkus.conf')
    init(None, '/home/atms/dev/ebkus/ebkus-2/ebkus.conf')
    config.pp_PARAMS()
