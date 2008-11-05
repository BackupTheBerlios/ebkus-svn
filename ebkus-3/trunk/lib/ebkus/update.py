# coding: latin-1
import os, sys, logging
from os.path import join, exists
from time import time
from itertools import chain
from ebkus.config import config
from ebkus.db.sql import opendb, closedb, getDBHandle, SQL
from ebkus.gen.schemagen import get_schema_info
from ebkus.gen.schemadata import schemainfo
from ebkus.gen.genEb import generate_ebapi
from ebkus.app.ebapi import Tabelle, Feld, FeldList, \
     Kategorie, KategorieList, Code, CodeList, FachstatistikList, \
     FallList, AkteList, JugendhilfestatistikList, Jugendhilfestatistik2007List, \
     getNewFallnummer, cc, today, calc_age, Fall

try:
    s = set
except NameError:
    from sets import Set as set


# public
def update():
    u = UpdateDB()
    u.keep_alive_anpassen()
    u.fallnummer_pruefen_und_reparieren()
    u.fsqualij_code_reparieren()
    if u.update_noetig():
        u.update()
        
class UpdateDB(object):
    """Zum Update einer EBKuS-Datenbank von einer Version auf eine h�here.
    Die Software der h�heren Version muss bereits eingespielt sein.
    """
    # diese Listen definieren f�r welche Datenbankversionen diese Klasse funktioniert
    ist_moeglich = ['4.1', '4.1.1']
    soll_moeglich = ['4.2']

    def __init__(self):
        # Protokoll stoert
        from ebkus.app.protocol import temp_off
        temp_off()
        # Sollversion ist immer die Version der Software
        from ebkus import Version
        self.soll = Version
        try:
            opendb()
        except:
            # Zum Update muss die Datenbank verf�gbar sein.
            # Daher:
            self.abort("F�r das Update muss die Datenbank verf�gbar sein!",
                       exc_info=True)
        # Ist-Version feststellen
        self.tables = getDBHandle().listtables()
        self.ist = self.get_version()

    def abort(self, message, exc_info=False):
        logging.critical(message, exc_info=exc_info)
        logging.shutdown()
        sys.exit(1)

    def has_field(self, table, field):
        return bool([t for t in getDBHandle().listfields(table) if t[0] == field])

    def get_version(self):
        tables = self.tables
        if ('jghstat07' in tables and
            not 'strkatalog' in tables and
            'fachstatlei' in tables):
            return '3.3'
        elif 'register' in tables:
            from ebkus.app.ebapi import register_get
            version = register_get('Version')
            if version:
                return version
            else:
                # 4.0 oder 4.0.1
                return '4.0'
        else:
            return None

    def update_noetig(self):
        if self.ist == self.soll:
            logging.info("Datenbankversion und Softwareversion stimmen �berein.")
            logging.info("Keine Update erforderlich")
            return False
        else:
            logging.info("Datenbankversion: %s" % self.ist)
            logging.info("Softwareversion:  %s" % self.soll)
            logging.info("Update der Datenbank erforderlich")
        if self.soll not in self.soll_moeglich:
            self.abort("Update auf Version %s nicht m�glich" % self.soll)
        if not self.ist in self.ist_moeglich:
            self.abort("Update von Version %s nicht m�glich" % self.ist)
        logging.info("Datenbank wird auf Version %s updatet" % self.soll)
        return True

    def update(self):
        method = "update_%s_nach_%s" % (self.ist, self.soll)
        method = method.replace('.', '_')
        res = getattr(self, method)()
        from ebkus import Version
        from ebkus.app.ebapi import register_set
        register_set("Version", self.soll)
        logging.info("Datenbank von Version %s auf Version %s erfolgreich updatet" %
                     (self.ist, self.soll))

    def update_4_1_nach_4_1_1(self):
        self.fsqualij_code_reparieren()

    def update_4_1_1_nach_4_2(self):
        self.mehrfach_joker_felder_reparieren()

    def update_4_1_nach_4_2(self):
        self.fsqualij_code_reparieren()
        self.mehrfach_joker_felder_reparieren()

    def fsqualij_code_reparieren(self):
        try:
            # Code '5' kommt zweimal vor, durch '9' ersetzen, falls noch frei
            # War aber nicht schlimm, da Ausz�hlungen �ber die id, nicht den code
            # erfolgen.
            codes5 = CodeList(where="kat_code='fsqualij' and code='5'")
            codes9 = CodeList(where="kat_code='fsqualij' and code='9'")
            if len(codes5) == 2 and len(codes9) == 0:
                codes5[1].update({'code': '9'})
                logging.info("Doppelter fsqualij-Code ersetzt")
        except:
            pass

    def keep_alive_anpassen(self):
        try:
            changed = False
            if sys.platform == 'win32':
                httpd_conf = join(config.INSTALL_DIR, 'apache', 'conf', 'httpd.conf')
                if exists(httpd_conf):
                    f = open(httpd_conf, 'rb')
                    text = f.read()
                    f.close()
                    if text.find('\nKeepAlive On') > -1:
                        text = text.replace('\nKeepAlive On', '\nKeepAlive Off')
                        open(httpd_conf, 'wb').write(text)
                        changed = True
            if changed:
                logging.info("Apache-Server auf 'KeepAlive Off' eingestellt")
        except:
            pass # sollte nie scheitern
            
    def fallnummer_pruefen_und_reparieren(self):
        faelle = FallList(where='')
        fn_dict = {}
        doubletten = []
        for f in faelle:
            fn = f['fn']
            count = fn_dict.setdefault(fn, 0)
            if count > 0:
                doubletten.append(fn)
            fn_dict[fn] += 1
        if doubletten:
            for fn in doubletten:
                n = fn_dict[fn]
                logging.error("****Fallnummer mehrfach vergeben: %s (%sx)" % (fn, n))
                self.fallnummer_reparieren(fn)
        else:
            logging.info("Keine doppelten Fallnummer")
            

    def fallnummer_reparieren(self, fn):
        faelle = FallList(where="fn='%s'" % fn)
        for f in faelle[1:]:
            stz_code = f['akte__stzbg__code']
            jahr = f['bgy']
            new_fn = getNewFallnummer(stz_code, jahr)
            f.update({'fn': new_fn})
            fall_id = f['id'] 
            where = 'fall_id=%s' % fall_id
            for s in chain(JugendhilfestatistikList(where=where),
                           Jugendhilfestatistik2007List(where=where),
                           FachstatistikList(where=where),
                           ):
                s.update({'fall_fn': new_fn})
            logging.info("Fallnummer repariert: fall_id=%s: %s --> %s" %
                         (fall_id, fn, new_fn))



    def _get_jokf_int_felder(self):
        res = []
        cols = SQL("SHOW COLUMNS FROM fachstat LIKE 'jokf%%'").execute()
        for c in cols:
            if c[1].startswith('int'):
                res.append(c[0])
        logging.info("Fachstatistik INT-jokf<n>-Felder: %s" % res)
        return res

    def mehrfach_joker_felder_reparieren(self):
        # werte sichern
        # auf string umstellen
        # werte schreiben
        # feld anpassen
        felder = self._get_jokf_int_felder()
        for f in felder:
            werte = SQL("SELECT id, %s FROM fachstat" % f).execute()
            SQL("ALTER TABLE fachstat MODIFY %s VARCHAR(255)" % f).execute()
            for id, val in werte:
                if val == None:
                    SQL("""UPDATE fachstat SET %s=NULL WHERE id=%s""" % (f,id)).execute()
                else:
                    val = str(val)
                    SQL("""UPDATE fachstat SET %s='%s' WHERE id=%s""" % (f,val,id)).execute()
            feld = Feld(tab_id=Tabelle(tabelle='fachstat')['id'], feld=f)
            if feld['verwtyp__code'] == 'k':
                # war single vorher, soll so bleiben, wird in flag als bit 2 kodiert
                feld.update({'flag': feld['flag']|2})
            # Trotzdem alle auf 'm' stellen, da nur so die strings im Feld
            # richtig interpretiert werden.
            feld.update({'verwtyp': cc('verwtyp', 'm')})
            logging.info("Fachstatistik Feld %s umgestellt" % f)
            
