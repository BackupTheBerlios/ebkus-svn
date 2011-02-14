# coding: latin-1
import os, sys, logging
from os.path import join, exists
from time import time
from itertools import chain
from ebkus.config import config
from ebkus.db.sql import opendb, closedb, getDBHandle, SQL, SQLError
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
    # hack: k�nstlich auf 4.2 setzen, nur f�r demo_test
    #from ebkus.app.ebapi import register_set
    #register_set("Version", "4.2")
    #u.ist = u.get_version()
    u.keep_alive_anpassen()
    u.fallnummer_pruefen_und_reparieren()
    u.fsqualij_code_reparieren()
    if u.update_noetig():
        u.update()
        
class UpdateDB(object):
    """Zum Update einer EBKuS-Datenbank von einer Version auf eine h�here.
    Die Software der h�heren Version muss bereits eingespielt sein.
    """

    # Die Software kann auch immer eine dreistellige Version sein (4.3.1).
    # Die zugeh�rige DB-Version ist immer zweistellig. 
    # Wenn das Schema ge�ndert wird, muss sich die zweistellige Versionszahl
    # erh�hen.

    # Die Datenbank muss mindestens auf diesem Niveau sein, damit 
    # ein Update m�glich ist.
    # ist_moeglich_db = ['4.2']
    # ist_moeglich_db = ['4.3']
    ist_moeglich_db = ['4.2', '4.3']
    # Die Update Software kann die Datenbankversion auf dieses Niveau
    # heben (d.h. es gibt eine update_<ist_m�glich>_nach_<soll_m�glich>
    # soll_moeglich_db = ['4.3']
    soll_moeglich_db = ['4.4']

    def __init__(self):
        # Protokoll stoert
        from ebkus.app.protocol import temp_off
        temp_off()
        # Sollversion ist immer die Major-Version der Software (4.1, 4.4, ...)
        from ebkus import Version
        self.ist_sw = Version
        # Minor-Version spielt keine Rolle
        vt = Version.split('.')
        self.soll_db = "%s.%s" % (vt[0], vt[1])
        try:
            opendb()
        except:
            # Zum Update muss die Datenbank verf�gbar sein.
            # Daher:
            self.abort("Fuer das Update muss die Datenbank verfuegbar sein!",
                       exc_info=True)
        # Ist-Version der Datenbank feststellen
        self.tables = getDBHandle().listtables()
        try:
            ist_db = self.get_version()
            vt = ist_db.split('.')
            self.ist_db = "%s.%s" % (vt[0], vt[1])
        except:
            self.ist_db = None

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
            try:
                version = register_get('Version')
                if version:
                    return version
            except SQLError:
                pass
            try:
                # Neues Schema ab 4.4, DB ist �lter, also Versionsinfo direkt mit SQL holen
                werte = SQL("SELECT value FROM register where regkey='Version'").execute()
                if werte:
                    from cPickle import loads
                    s = werte[0][0]
                    try: s = s.tostring() # kommt manchmal als array.array raus
                    except: pass # war schon string
                    res = loads(s)
                    return res
            except:
                pass
            # register-Tabelle vorhanden aber keine Version gefunden, also 4.0 oder 4.0.1
            return '4.0'
        else:
            return None

    def update_noetig(self):
        if not self.ist_db:
            logging.error("Version der Datenbank nicht feststellbar, Update nicht m�glich.")
            return False
        elif self.ist_db == self.ist_sw:
            logging.info("Datenbankversion und Softwareversion stimmen ueberein.")
            logging.info("Keine Update erforderlich")
            return False
        elif self.ist_db == self.soll_db:
            logging.info("Datenbankversion und Softwareversion sind kompatibel.")
            logging.info("Keine Update erforderlich")
            return False
        else:
            logging.info("Datenbankversion: %s" % self.ist_db)
            logging.info("Softwareversion:  %s" % self.ist_sw)
            logging.info("Update der Datenbank erforderlich")
        if self.soll_db not in self.soll_moeglich_db:
            self.abort("Update auf Version %s nicht moeglich" % self.ist_sw)
        if not self.ist_db in self.ist_moeglich_db:
            self.abort("Update von Version %s nicht moeglich" % self.ist_db)
        logging.info("Datenbank wird auf Version %s updatet" % self.soll_db)
        return True

    def update(self):
        method = "update_%s_nach_%s" % (self.ist_db, self.soll_db)
        method = method.replace('.', '_')
        res = getattr(self, method)()
        from ebkus import Version
        from ebkus.app.ebapi import register_set
        register_set("Version", self.soll_db)
        logging.info("Datenbank von Version %s auf Version %s erfolgreich updatet" %
                     (self.ist_db, self.soll_db))

    def update_4_1_nach_4_1_1(self):
        self.fsqualij_code_reparieren()

    def update_4_1_1_nach_4_2(self):
        self.mehrfach_joker_felder_reparieren()

    def update_4_1_nach_4_2(self):
        self.fsqualij_code_reparieren()
        self.mehrfach_joker_felder_reparieren()

    def update_4_2_nach_4_3(self):
        self.wartezeit_bereichskategorie_eintragen()
        self.fua_bs_neue_tabelle_fuer_mitarbeiter_zuordnung()

    def update_4_2_nach_4_3_1(self):
        self.wartezeit_bereichskategorie_eintragen()
        self.fua_bs_neue_tabelle_fuer_mitarbeiter_zuordnung()

    def update_4_3_nach_4_4(self):
        self.add_field_to_register()
        self.add_mail_fields_to_akte_bezugsperson()
        self.neue_tabelle_fuer_gemeindeschluessel()
        from ebkus.app.gemeindeschluessel import get_gemeindeschluessel
        get_gemeindeschluessel('Berlin', '12047')

    def update_4_2_nach_4_4(self):
        self.update_4_2_nach_4_3()
        self.update_4_3_nach_4_4()

    def add_field_to_register(self):
        SQL("ALTER TABLE register ADD valuestr TEXT").execute()
        t = Tabelle(tabelle='register')
        f = Feld()
        f.init(
            tab_id=t['id'],
            feld='valuestr',
            name='Wert als String',
            inverse=None,
            typ='TEXT',
            verwtyp=cc('verwtyp', 'p'),
            ftab_id=None,
            flag=0,
            )
        f.new()
        f.insert()
        # Nicht unbedingt n�tig, aber es ist klarer, wenn das Feld k�nftig leer ist.
        SQL("UPDATE register set value=NULL,valuestr='%s' where regkey='Version'" % self.ist_db).execute()
        logging.info("Feld 'valuestr' fuer Tabelle 'register' eingefuehrt")

    def add_mail_fields_to_akte_bezugsperson(self):
        tabellen = ('akte', 'bezugsperson', 'einrichtung')
        for tn in tabellen:
            SQL("ALTER TABLE %s ADD mail VARCHAR(80)" % tn).execute()
            t = Tabelle(tabelle=tn)
            f = Feld()
            f.init(
                tab_id=t['id'],
                feld='mail',
                name='E-Mail',
                inverse=None,
                typ='VARCHAR(80)',
                verwtyp=cc('verwtyp', 'p'),
                ftab_id=None,
                flag=0,
                )
            f.new()
            f.insert()
            logging.info("Feld 'mail' fuer Tabelle '%s' eingefuehrt" % t['tabelle'])

    def wartezeit_bereichskategorie_eintragen(self):
        kat_code = 'wartez'
        try:
            k = Kategorie(code=kat_code)
            return
        except:
            pass # Kategorie gibts noch nicht
        k = Kategorie()
        k.new()
        k.init(
            code=kat_code,
            name='Wartezeit zwischen Anmeldung und erster Leistung',
            flag=1,  # ist Bereichskategorie
            zeit=int(time()),
            )
        k.insert()
        kat_id = k['id']
        logging.info("Bereichskategorie 'wartez' hinzugefuegt")
        assert isinstance(kat_id, (int, long))
        code_data = (
            ('1', 'am selben Tag', 0, 0, ),
            ('2', 'bis 1 Woche', 1, 7, ),
            ('3', 'bis 2 Wochen', 8, 14, ),
            ('4', 'bis 3 Wochen', 15, 21, ),
            ('5', 'bis 1 Monat', 22, 30, ),
            ('6', 'bis 3 Monate', 31, 91, ),
            ('7', 'bis 6 Monate', 92, 183, ),
            ('6', 'mehr als 6 Monate', 184, 9999, ),
            )
        sort = 0
        for code, name, mini, maxi in code_data:
            sort += 1
            c = Code()
            c.new()
            c.init(
                code=code,
                name=name,
                kat_id=kat_id,
                kat_code=kat_code,
                sort=sort,
                off=0,
                zeit=int(time()),
                mini=mini,
                maxi=maxi,
                )
            assert c['kat_code'] == kat_code == k['code'] == 'wartez'
            c.insert()
            logging.info("Code fuer 'wartez' hinzugefuegt: code=%s name=%s" % (code, name))

    def neue_tabelle_fuer_gemeindeschluessel(self):
        if 'ags' in self.tables:
            logging.info("Tabelle 'ags' existiert bereits")
            return
        try:
            SQL("""CREATE TABLE ags (
id int NOT NULL,
plz CHAR(5),
ags CHAR(12),
ort VARCHAR(60),
PRIMARY KEY (id),
KEY(ort(10))
)""").execute()

            t = Tabelle()
            t.init(
                tabelle="ags",
                name="Amtliche Gemeindeschl�ssel",
                klasse="AGS",
                flag=0,
                maxist=0
                )
            t.new()
            t.insert()
            felder = (
                ('id', 'id', None, 'INT', cc('verwtyp', 's'), None,),
                ('plz', 'Postleitzahl', None, 'CHAR(5)', cc('verwtyp', 'p'), None,),
                ('ags', 'Gemeindeschl�ssel', None, 'CHAR(12)', cc('verwtyp', 'p'), None,),
                ('ort', 'Ort', None, 'VARCHAR(60)', cc('verwtyp', 'p'), None,),
                )
            for feld, name, inverse, typ, verwtyp, ftab_id in felder:
                f = Feld()
                f.init(
                    tab_id=t['id'],
                    feld=feld,
                    name=name,
                    inverse=inverse,
                    typ=typ,
                    verwtyp=verwtyp,
                    ftab_id=ftab_id,
                    flag=0,
                    )
                f.new()
                f.insert()
            logging.info("Neue Tabelle 'ags' fuer Gemeindeschluessel eingefuehrt")
        except:
            #raise
            logging.error("************ Fehler beim Anlegen der Tabelle 'ags'")

    def fua_bs_neue_tabelle_fuer_mitarbeiter_zuordnung(self):
        if 'mitarbeiterfua_bs' in self.tables:
            logging.info("Tabelle 'mitarbeiterfua_bs' existiert bereits")
            return
        try:
            SQL("""CREATE TABLE mitarbeiterfua_bs (
id int NOT NULL,
mit_id int,
fua_bs_id  int,
zeit int,
PRIMARY KEY (id)
)""").execute()

            t = Tabelle()
            t.init(
                tabelle="mitarbeiterfua_bs",
                name="Zuordnung Mitarbeiter-fallunabh�ngige Aktivit�ten",
                klasse="Mitarbeiterfua_bs",
                flag=0,
                maxist=0
                )
            t.new()
            t.insert()
            felder = (
                ('id', 'id', None, cc('verwtyp', 's'), None,),
                ('mit_id', 'Mitarbeiterid', 'mitarbeiterfuaktivitaeten',
                 cc('verwtyp', 'f'), Tabelle(tabelle='mitarbeiter')['id']),
                ('fua_bs_id', 'Fua_bsid', 'mitarbeiterfuaktivitaeten',
                 cc('verwtyp', 'f'), Tabelle(tabelle='fua_bs')['id']),
                ('zeit', '�nderungszeit', None, cc('verwtyp', 'p'), None),
                )
            for feld, name, inverse, verwtyp, ftab_id in felder:
                f = Feld()
                f.init(
                    tab_id=t['id'],
                    feld=feld,
                    name=name,
                    inverse=inverse,
                    typ='INT',
                    verwtyp=verwtyp,
                    ftab_id=ftab_id,
                    flag=0,
                    )
                f.new()
                f.insert()
            logging.info("Neue Tabelle 'mitarbeiterfua_bs' eingefuehrt")
        except:
            #raise
            logging.error("************ Fehler beim Anlegen der Tabelle 'mitarbeiterfua_bs'")

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
            
