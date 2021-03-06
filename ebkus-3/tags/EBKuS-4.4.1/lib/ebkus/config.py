# coding: latin-1
from __future__ import generators

import sys, re, ConfigParser
from os.path import exists, normpath

class ConfigError(Exception):
    pass

config = None

import ebkus
_ebkus_version = ebkus.Version

from ebkus.config_doku import param_doks

class KonfigVar(object):
    def __init__(self, data, dok, value):
        self.section = data[0]
        self.NAME = data[1]
        self.name = data[2]
        self.typ = data[3]
        self.default = data[4]
        if dok:
            self.fachlich = dok[0]
            self.valid_pattern = dok[1]
            self.beschreibung = dok[2]
            try: self.doku = dok[3]
            except: self.doku = ''
        else:
            self.fachlich = False
            self.valid_pattern = ''
            self.beschreibung = ''
            self.doku = ''
        self.value = value
    def print_value(self, key):
        v = getattr(self, key)
        if isinstance(v, bool):
            return v and 'true' or 'false'
        return v
    def __getitem__(self, key):
        return getattr(self, key)
    def is_boolean(self):
        return self.typ == 'b'
    def is_int(self):
        return self.typ == 'i'

# (section, Name fuer config Nutzer, Name in config Datei, typ, Default)  
# typ: p path, s string, i int, b boolean
# default modifier: i interpolate, e eval, s literal

_params = (
    ('ebkus', 'INSTALL_DIR', 'install_dir', 'p', None),
    ('ebkus', 'DOWNLOAD_DIR', 'download_dir', 'p', 'i:%(install_dir)s/download'),
##     ('ebkus', 'SW_LINUX_DIR', 'sw_linux_dir', 'p', 'i:%(install_dir)s/../linux'),
##     ('ebkus', 'SW_WIN32_DIR', 'sw_win32_dir', 'p', 'i:%(install_dir)s/../win32'),
    ('ebkus', 'EBKUS_HOME', 'ebkus_home', 'p', 'i:%(install_dir)s/ebkus'),
    ('ebkus', 'PYTHON_EXECUTABLE', 'python_executable', 'p', 'e:sys.executable'),
    ('ebkus', 'EBKUS_VERSION', 'ebkus_version', 's', 'e:_ebkus_version'),
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
    ('apache', 'SERVER_HTTPS_PORT', 'server_https_port', 'i', 's:443'),
    ('apache', 'SERVER_HTTP_PORT', 'server_http_port', 'i', 's:80'),
    ('openssl', 'STAAT', 'staat', 's', 's:DE'),
    ('openssl', 'LAND', 'land', 's', 's:Berlin'),
    ('openssl', 'ORT', 'ort', 's', 's:Berlin'),
    ('openssl', 'ORGANISATION', 'organisation', 's', 's:EFB'),
    ('openssl', 'ORGANISATIONSEINHEIT', 'organisationseinheit', 's', 's:EFB'),
    ('openssl', 'OUTPUT_PASSWORD', 'output_password', 's', 's:polo'),
    ('openssl', 'OPENSSL_EXECUTABLE', 'openssl_executable', 'p', 's:openssl'),
    ('instance', 'INSTANCE_NAME', 'instance_name', 's', None),
    ('instance', 'INSTANCE_TITLE', 'instance_title', 's', 'e:self.get_instance_title(instance_name)'),
    ('instance', 'INSTANCE_HOME', 'instance_home', 'p', 'i:%(ebkus_home)s/%(instance_name)s'),
    ('instance', 'DATABASE_NAME', 'database_name', 's', 'i:%(instance_name)s'),
    ('instance', 'DATABASE_HOST', 'database_host', 's', 's:localhost'),
    ('instance', 'DATABASE_USER', 'database_user', 's', 'i:%(instance_name)s'),
    ('instance', 'DATABASE_PASSWORD', 'database_password', 's', 'i:%(instance_name)s'),
    ('instance', 'DATABASE_TYPE', 'database_type', 's', 's:MySQLdb'),
    ('instance', 'DOCUMENT_ROOT', 'document_root', 'p', 'i:%(instance_home)s/htdocs'),
    ('instance', 'INITIAL_CONTENT', 'initial_content', 'p', 'i:'),
    ('instance', 'PORT', 'port', 'i', None),
    ('instance', 'HOST', 'host', 's', 's:localhost'),
    ('instance','LOG_FILE',  'log_file', 'p', 'i:%(instance_home)s/%(instance_name)s.log'),
    ('instance','LOG_LEVEL',  'log_level', 's', 's:INFO'),
    ('instance', 'SITE', 'site', 's', 's:A'),
    ('instance', 'MASTER_SITE', 'master_site', 's', 's:A'),
    ('instance', 'LOESCHFRIST', 'loeschfrist', 'i', 's:36'),
    ('instance', 'WIEDERAUFNAHMEFRIST', 'wiederaufnahmefrist', 'i', 's:1'),
    ('instance', 'SESSION_TIME', 'session_time', 'i', 's:120'),
    ('instance', 'PROTOCOL_DIR', 'protocol_dir', 'p', 'i:%(instance_home)s/protokolle'),
    ('instance', 'AK_DIRS_MAX', 'ak_dirs_max', 's', 's:100'),
    ('instance', 'ADMIN_NAME', 'admin_name', 's', 's:Keine Angabe'),
    ('instance', 'ADMIN_TEL', 'admin_tel', 's', 's:Keine Angabe'),
    ('instance', 'ADMIN_EMAIL', 'admin_email', 's', 's:Keine Angabe'),
    ('instance', 'BERLINER_VERSION', 'berliner_version', 'b', 'e:False'),
    ('instance', 'BERATUNGSKONTAKTE', 'beratungskontakte', 'b', 'e:False'),
    ('instance', 'BERATUNGSKONTAKTE_BS', 'beratungskontakte_bs', 'b', 'e:False'),
    ('instance', 'FALLUNABHAENGIGE_AKTIVITAETEN_BS', 'fallunabhaengige_aktivitaeten_bs', 'b', 'e:False'),
    ('instance', 'STRASSENKATALOG', 'strassenkatalog', 's', 's:'),
    ('instance', 'STRASSENKATALOG_VOLLSTAENDIG', 'strassenkatalog_vollstaendig', 'b', 'e:False'),
    ('instance', 'STRASSENSUCHE', 'strassensuche', 's', 's:'), # ort ortsteil bezirk samtgemeinde
    ('instance', 'SQL_ABFRAGE', 'sql_abfrage', 'b', 'e:False'),
    ('instance', 'ANMELDUNGSDATEN_OBLIGATORISCH', 'anmeldungsdaten_obligatorisch', 'b', 'e:False'),
#    ('instance', 'FEHLER_BEI_FACHSTATISTIK_AKTE_DISKREPANZ', 'fehler_bei_fachstatistik_akte_diskrepanz', 'b', 'e:False'),
    ('instance', 'WARNUNG_BEI_FACHSTATISTIK_AKTE_DISKREPANZ', 'warnung_bei_fachstatistik_akte_diskrepanz', 'b', 'e:False'),
    ('instance', 'FACHSTATISTIK_AKTE_DISKREPANZ_NICHT_ZULASSEN', 'fachstatistik_akte_diskrepanz_nicht_zulassen', 'b', 'e:False'),
    ('instance', 'EXTERN_FIELDSET_LABEL', 'extern_fieldset_label', 's', 's:'),
    ('instance', 'EXTERN_FIELDSET_POSITION', 'extern_fieldset_position', 'i', 's:2'),
    ('instance', 'EXTERN_BUTTON1_LABEL', 'extern_button1_label', 's', 's:'),
    ('instance', 'EXTERN_BUTTON1_URL', 'extern_button1_url', 's', 's:'),
    ('instance', 'EXTERN_BUTTON2_LABEL', 'extern_button2_label', 's', 's:'),
    ('instance', 'EXTERN_BUTTON2_URL', 'extern_button2_url', 's', 's:'),
    ('instance', 'EXTERN_BUTTON3_LABEL', 'extern_button3_label', 's', 's:'),
    ('instance', 'EXTERN_BUTTON3_URL', 'extern_button3_url', 's', 's:'),
    ('instance', 'EXTERN_BUTTON4_LABEL', 'extern_button4_label', 's', 's:'),
    ('instance', 'EXTERN_BUTTON4_URL', 'extern_button4_url', 's', 's:'),
    ('instance', 'WOHNT_NICHT_AUSSERHALB', 'wohnt_nicht_ausserhalb', 's', 's:'),
    ('instance', 'GEMEINDESCHLUESSEL_VON_PLZ', 'gemeindeschluessel_von_plz', 's', 's:'),
    ('instance', 'NEUMELDUNGEN_NACH_REGION', 'neumeldungen_nach_region', 's', 's:'),
    ('instance', 'MELDUNG_VOM_ADMIN', 'meldung_vom_admin', 's', 's:'),
    ('instance', 'KEINE_BUNDESSTATISTIK', 'keine_bundesstatistik', 'b', 'e:False'),
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
                if c.has_option(s, 'strassenkatalog'):
                    if c.get(s, 'strassenkatalog') == 'berlin':
                        c.set(s, 'berliner_version', 'true')
##                 if c.get(s, 'berliner_version'):
##                         self._error("Berliner Version muss Strassenkatalog 'berlin' haben.")
##                 if c.get(s, 'strassenkatalog') == 'berlin':
##                     if not c.get(s, ):
##                         self._error("Strassenkatalog 'berlin' nur in Berliner Version moeglich.")

    def _error(self, msg):
        self._errors.append(msg)

    def get(self, section, option):
        return self._conf.get(section, option)

    def get_instance_title(self, instance_name):
        return ' '.join([e.capitalize() for e in instance_name.split('_')])

    def _proc_default(self, default, pdict, param):
        if not default:
            self._error("Kein Wert fuer %s" % param)
            return
        instance_name = pdict.get('instance_name')
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
            except ConfigParser.NoOptionError:
                #print t
                value = self._proc_default(t[4], param_dict, param)
                if typ == 'i':
                    value = int(value)
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
        from ebkus.app.ebapi import register_get
        l = []
        for s, P, p, v, t in self._param_iterator(_params):
            v_ebkus_conf = v
            # Fachliche Konfigurationsvariable k�nnen im Admin-Men� editiert werden
            # und werden in der Datenbank abgelegt.
            v_db = None
            try:
                v_db = register_get(p)
            except:
                pass
            if v_db and v_db != v_ebkus_conf:
                v_out = "%s (in ebkus.conf: %s)" % (v_db, v_ebkus_conf)
            else:
                v_out = v_ebkus_conf
            l.append("%s: %s" % (p, v_out))
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

    def iter(self):
        """Iterator �ber alle Konfigurationsvariablen.
        Es wird f�r jede Variable eine Instanz der Klasse KonfigVar
        zur�ckgegeben.
        """
        for p in _params:
            NAME = p[1]
            name = p[2]
            dok = param_doks.get(name)
            p = KonfigVar(p, dok, getattr(self, NAME))
            yield p

    def prtable(self):
        sections = self._conf.sections()
        for s in sections:
            pass

if __name__ == '__main__':
    #init('demo', '/home/atms/dev/ebkus/ebkus-2/ebkus.conf')
    init(None, '/home/atms/dev/ebkus/ebkus-2/ebkus.conf')
    config.pp_PARAMS()
