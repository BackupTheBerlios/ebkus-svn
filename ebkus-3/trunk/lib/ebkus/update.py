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
     getNewFallnummer, cc, today, calc_age, Fall, StrassenkatalogNeuList


#str_kat = join(config.EBKUS_HOME, 'sql', STRASSENKATALOG) 
#STRASSENKATALOG = 'strkatalog_berlin_ausschnitt.sql.gz'
STRASSENKATALOG = '/home/atms/dev/ebkus/strassen_katalog/berlin/strkatalog_berlin_jk.sql.gz'
# für python2.3, kein set
try:
    s = set
except NameError:
    from sets import Set as set


# public
def update():
    u = UpdateDB()
    if u.update_noetig():
        u.update()
        
class UpdateDB(object):
    """Zum Update einer EBKuS-Datenbank von einer Version auf eine höhere.
    Die Software der höheren Version muss bereits eingespielt sein.
    """
    # diese Listen definieren für welche Datenbankversionen diese Klasse funktioniert
    ist_moeglich = ['3.3', '4.0', '4.0.2', '4.1'] # TODO: 4.0.1 und 4.0.2 integrieren
    soll_moeglich = ['4.1']

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
            # Zum Update muss die Datenbank verfügbar sein.
            # Daher:
            self.abort("Für das Update muss die Datenbank verfügbar sein!",
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
            logging.info("Datenbankversion und Softwareversion stimmen überein.")
            logging.info("Keine Update erforderlich")
            return False
        else:
            logging.info("Datenbankversion: %s" % self.ist)
            logging.info("Softwareversion:  %s" % self.soll)
            logging.info("Update der Datenbank erforderlich")
        if self.soll not in self.soll_moeglich:
            self.abort("Update auf Version %s nicht möglich" % self.soll)
        if not self.ist in self.ist_moeglich:
            self.abort("Update von Version %s nicht möglich" % self.ist)
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

    def update_4_0_nach_4_1(self):
        if not self.has_field('jghstat07', 'jahr'):
            SQL('ALTER TABLE jghstat07 ADD COLUMN jahr INT').execute()
            logging.info("Feld 'jahr' zur Bundesstatistik hinzugefügt")
        tab_id = Tabelle(tabelle='jghstat07')['id']
        if not FeldList(where="tab_id=%s and feld='jahr'" % tab_id):
            feld = Feld()
            feld.init(tab_id=tab_id,
                      feld='jahr',
                      name='Jahr',
                      typ='INT',
                      verwtyp=cc('verwtyp', 'p'),
                      flag=0,
                )
            feld.new()
            feld.insert()
            logging.info("Metadaten für Feld 'jahr' hinzugefügt")
        self.jahr_in_bundesstatistik()
        Kategorie(code='kr').update({
            'dok': "amtlicher Gemeindeschlüssel (AGS, Ziffer 3-5)"})
        Kategorie(code='rbz').update({
            'dok': "amtlicher Gemeindeschlüssel (AGS) obsolet, in Kreis mit drin"})
        self.kreis_dreistellig_umstellen()
        self.einrichtungsnummer_sechsstellig_umstellen()
        self.keep_alive_anpassen()
        self.strassenkatalog_reparieren()

    def update_4_0_2_nach_4_1(self):
        # kann nichts schaden
        self.update_4_0_nach_4_1()

    def update_3_3_nach_4_1(self):
        self.rename_tables()
        self.init_new_db()
        self.set_diff()
        self.masse_kopieren()
        self.planungsr_ort_plz_kopieren()
        self.maxist_berechnen()
        self.neue_kataloge()
        self.fehlende_codes()
        self.update_feld()
##         self.diff_merkmalskataloge(
##             "/home/atms/dev/ebkus/source-dist/tmp/EBKuS-3.3/sql/merkmale_standard.py",
##             "/home/atms/dev/ebkus/source-dist/tmp/EBKuS-4.0.2/sql/merkmale_standard.py",
##             )
        self.update_fachstatistik_merkmale()
        self.fachstatistik_items_abschalten()
        self.fachstatistik_multi()
        self.fachstatistik_beschaeftigung_unter_14()
        self.jahr_in_bundesstatistik()
        self.geschlecht_aus_statistik_nach_akte()
        self.add_mime_types()
        self.kreis_dreistellig_umstellen()
        self.strassenkatalog_einlesen()
        self.stellenzeichen_reparieren()
        self.akte_aufbew_initialisieren()
        self.fallnummer_pruefen_und_reparieren()
        self.regional_abgleich()
        self.alte_tabellen_loeschen()
        self.keep_alive_anpassen()


    def strassenkatalog_reparieren(self):
        strassen_list = StrassenkatalogNeuList(where='von IS NOT NULL')
        from ebkus.html.strkat import split_hausnummer
        count = 0
        for s in strassen_list:
            try:
                vn, vb, vg = split_hausnummer(s['von'])
                bn, bb, bg = split_hausnummer(s['bis'])
                s.update({'von': "%03d%s" % (vn, vb.upper()),
                          'bis': "%03d%s" % (bn, bb.upper()),
                    })
                count += 1
            except:
                pass
        logging.info("%s Eintraege des Strassenkatalogs repariert" % count)

    def keep_alive_anpassen(self):
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
        else:
            logging.info("Apache-Server 'KeepAlive' nicht veraendert")
                
            

    def alte_tabellen_loeschen(self):
        for t in getDBHandle().listtables():
            if t.endswith('_old'):
                SQL("DROP TABLE %s" % t).execute()
        logging.info("Alte Tabellen geloescht")
        
    def regional_abgleich(self):
        if config.STRASSENKATALOG:
            akte_list = AkteList(where='')
            from ebkus.html.strkat import get_strasse
            count = 0
            def fs_iter(akte):
                for fall in akte['faelle']:
                    for fs in fall['fachstatistiken']:
                        yield fs
            for a in akte_list:
                strasse = get_strasse(a)
                if strasse:
                    count += 1
                    upd = {}
                    for f in ('ort', 'plz', 'ortsteil',
                              'bezirk', 'samtgemeinde', 'plraum'):
                        upd[f]= strasse[f]
                    for fs in fs_iter(a):
                        fs.update(upd) 
                    a.update({'plraum': strasse['plraum']})
                else:
                    # dieser Fall ist schon durch planungsr_ort_plz_kopieren() geregelt
                    pass
            logging.info("Abgleich mit dem Strassenkatalog %s mal (aus %s) gelungen" %
                         (count, len(akte_list)))
        

    def akte_aufbew_initialisieren(self):
        aufbew_id = cc('aufbew', '1')
        SQL("UPDATE akte SET aufbew=%s" % aufbew_id).execute()
##         akte_list = AkteList(where='')
##         for a in akte_list:
##             a.update({'aufbew': cc('aufbew', '1')}) # alles auf Beratung
        logging.info("Aufbewahrungskategorie fuer alle Akten auf 'Beratung' gesetzt")
        
    def stellenzeichen_reparieren(self):
        akte_list = AkteList(where='')
        count = 0
        for a in akte_list:
            if a['stzbg'] != a['stzak']:
                count += 1
                a.update({'stzbg': a['stzak']})
        logging.info("akte.stzbg war %s mal verschieden von akte.stzak" % count)

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
            
    def geschlecht_aus_statistik_nach_akte(self):
        fs_list = FachstatistikList(where='')
        for fs in fs_list:
            try:
                fs['fall__akte'].update({'gs': fs['gs']})
            except:
                pass
        logging.info("Geschlecht aus Fachstatistik in die Klientenakte uebernommen")

    def strassenkatalog_einlesen(self):
        if config.STRASSENKATALOG:
            SQL('DROP TABLE IF EXISTS strkatalog').execute()
            user = config.DATABASE_USER
            pw = config.DATABASE_PASSWORD
            pw_arg = pw and "-p%s" % pw or ''
            db = config.DATABASE_NAME
            str_kat = STRASSENKATALOG
            cat = str_kat.endswith('.gz') and 'zcat' or 'cat'
            os.system("%s %s | mysql -u%s %s %s" % (cat, str_kat, user, pw_arg, db))
            logging.info('Strassenkatalog eingelesen: %s' % STRASSENKATALOG)
        
    def kreis_dreistellig_umstellen(self):
        from ebkus.app.ebapih import get_all_codes
        kreise = get_all_codes('kr')
        for k in kreise:
            code = k['code']
            if code in ('01', '02', '03', '04', '05', '06',
                        '07', '08', '09', '10', '11', '12',
                        ):
                code = '0' + code # Berlin 0
            elif len(code) == 2:
                code = '1' + code # sonst 1
            k.update({'code': code})
        logging.info('Kreis-Code dreistellig gemacht')
        
    def einrichtungsnummer_sechsstellig_umstellen(self):
        from ebkus.app.ebapih import get_all_codes
        codes = get_all_codes('einrnr')
        for c in codes:
            code = c['code']
            if not code.isdigit():
                logging.error("Einrichungsnummer gefunden, die keine Zahl ist: %s" % code)
            elif len(code) != 6:
                code = "%06d" % int(code[:6])
                c.update({'code': code})
                logging.info("Einrichungsnummer mit 0 aufgefuellt: %s" % code)
        logging.info('Einrichtungsnummern sechsstellig gemacht')

    def rename_tables(self):
        for t in self.tables:
            SQL('ALTER TABLE %s RENAME %s_old' % (t, t)).execute()
        logging.info('Tabellen umbenannt')
    def init_new_db(self):
        from ebkus.gen.schemadata import schemainfo
        from ebkus.gen.schemagen import get_schema_info, create_schema_in_db, \
             insert_tables_fields_in_db, insert_version
        newtables = get_schema_info(schemainfo)
        test = False
        create_schema_in_db(newtables, test)
        insert_tables_fields_in_db(newtables, test)
        insert_version()
        logging.info('Neue Datenbank erzeugt')
        
    def set_diff(self):
        tables = getDBHandle().listtables()
        self.tables_old = [t[:-4] for t in tables if t.endswith('_old')]
        self.tables_new = [t for t in tables if not t.endswith('_old')]
        self.tables_both = [t for t in self.tables_new if t in self.tables_old]
##         print self.tables_old
##         print self.tables_new
##         print self.tables_both
        #print 'obsolete Tabellen: ', [t for t in self.tables_old if t not in self.tables_new]
        #print 'neue Tabellen:     ', [t for t in self.tables_new if t not in self.tables_old]
        #print 'gemeins. Tabellen: ', self.tables_both
        for t in self.tables_both:
            common, obsolet, neu = self.diff_felder(t)
            #print t, obsolet, neu
    def diff_felder(self, tabelle):
        alte = [f[0] for f in getDBHandle().listfields(tabelle + '_old')]
        neue = [f[0] for f in getDBHandle().listfields(tabelle)]
        return (
            [f for f in alte if f in neue],
            [f for f in alte if f not in neue],
            [f for f in neue if f not in alte],
            )
    def masse_kopieren(self):
        for table in self.tables_both:
            if table not in ('tabelle', 'feld'):
                common, obsolet, neu = self.diff_felder(table)
                felder = ', '.join(common)
                SQL("""INSERT INTO %(table)s (%(felder)s)
                       SELECT  %(felder)s
                       FROM %(table)s_old
                       """ % locals()).execute()
        logging.info("Gleichgebliebene Daten kopiert")
    def planungsr_ort_plz_kopieren(self):
        SQL("""UPDATE akte_old, akte
               SET akte.plraum=akte_old.planungsr
               WHERE akte_old.id=akte.id
        """).execute()
        SQL("""UPDATE akte, fall, fachstat
               SET fachstat.plraum=akte.plraum,
                   fachstat.ort=akte.ort,
                   fachstat.plz=akte.plz
               WHERE akte.id=fall.akte_id and fall.id=fachstat.fall_id
        """).execute()
        logging.info("Planungsraum, Ort, PLZ aus Akte nach Fachstatistik uebernommen")
    def maxist_berechnen(self):
        for table in self.tables_new:
            maxist = SQL("SELECT COUNT(*) FROM %s" % table).execute()[0][0]
            #print table, maxist
            SQL("UPDATE tabelle SET maxist = %s WHERE tabelle = '%s'" %
                (maxist, table)).execute()
        logging.info("Maxist berechnet")
    def neue_kataloge(self):
        merkmals_datei = join(config.EBKUS_HOME, 'sql', 'merkmale_standard.py')
        mk = MerkmalsKatalog(merkmals_datei)
        self.katalog = mk.katalog
        neue = [k for k in self.katalog
                if not KategorieList(where="code='%s'" % k)]
        neue.sort()
        for k in neue:
            self.insert_katalog(k)
        logging.info("Merkmalskataloge eingelesen")
        self.bereichskategorien_markieren(mk)
    def insert_katalog(self, kat_code):
        k = self.katalog[kat_code]
        codes = k['codes']
        k['zeit'] = int(time())
        k.new()
        k.insert()
        id = k['id']
        for c in codes:
            c.new()
            c['zeit'] = int(time())
            c['kat_id'] = id
            c.insert()
        logging.info('Katalog eingeführt: %s' % kat_code)
    def bereichskategorien_markieren(self, merkmalskatalog):
        for k in KategorieList(where=''):
            if k['code'] in merkmalskatalog.bereichskategorien:
                flag = 1
            else:
                flag = 0
            k.update({'flag':flag})
        for c in CodeList(where=''):
            c.update({'flag':0})
        logging.info("Kategorie/Code flag gesetzt")
    def update_feld(self):
        from ebkus.gen.migrate import update_feld
        # verwtyp, kat_id, kat_code, inverse
        update_feld()
        logging.info("Tabelle feld updatet")
    def fehlende_codes(self):
        self.add_code('verwtyp', 'm', 'Mehrfachkategorie')
        logging.info("Code hinzugefügt: %s.%s" % ('verwtyp', 'm'))
    def add_code(self, kat_code, code, name,
                 sort=1, mini=None, maxi=None, dok=None,
                 ):
        kat_id = Kategorie(code=kat_code)['id']
        from ebkus.app.ebupd import codeeinf
        codeeinf({'codeid': Code().getNewId(),
                  'katcode': kat_code,
                  'katid': kat_id,
                  'code': code,
                  'name': name,
                  'sort': sort,
                  'mini': mini,
                  'maxi': maxi,
                  'dok': dok,
                  'flag': 0,
                  })
    def upd_code(self, kat_code, code, name=None,
                 sort=None, mini=None, maxi=None, dok=None,
                 ):
        kat_id = Kategorie(code=kat_code)['id']
        code = Code(code=code, kat_code=kat_code)
        from ebkus.app.ebupd import updcode
        updcode({'codeid': code['id'],
                 'katcode': kat_code,
                 'katid': kat_id,
                 'code': code['code'],
                 'name': name or code['name'],
                  'sort': sort or code['sort'],
                 'mini': mini or code['mini'],
                 'maxi': maxi or code['maxi'],
                 'dok': dok or code['dok'],
                 'dm': '',
                 'dy': '',
                 })
    def exists_code(self, kat_code, code):
        try:
            Code(code=code, kat_code=kat_code)
            return True
        except:
            return False
    def diff_merkmalskataloge(self, old, new):
        k1 = MerkmalsKatalog(old).katalog
        k2 = MerkmalsKatalog(new).katalog
        common = [k for k in k1 if k in k2]
        common.sort()
        obsolet = [k for k in k1 if k not in common]
        obsolet.sort()
        neu = [k for k in k2 if k not in common]
        neu.sort()
        print 'OBSOLET: ', obsolet
        print 'NEU:     ', neu
        for k in common:
            self.diff_kat(k1[k], k2[k])
    def diff_kat(self, old, new):
        if old == new:
            #print 'gleich:     ', old['code'], old['name']
            assert old['codes'] == new['codes'] 
        else:
            print '*** differ: ', old['code'], old['name'], new['name']
            old_codes = dict([(c['code'], c) for c in old['codes']])
            new_codes = dict([(c['code'], c) for c in new['codes']])
##             print old_codes
##             print new_codes
            codes = list(set([c for c in chain(old_codes, new_codes)]))
            codes.sort()
            print codes
            for c in codes:
                old_code = old_codes.get(c)
                new_code = new_codes.get(c)
                if old_code == new_code:
                    print '  %08s' % (c,)
                elif not old_code or not new_code:
                    print '  %08s  %s  %s' % (c,
                                              old_code and c or 'fehlt',
                                              new_code and c or 'fehlt')
                else:
                    attrs = set(old_code.data)|set(new_code.data)
                    diffs = ' '.join(["%s{%s,%s}" % (a, old_code.data.get(a), new_code.data.get(a))
                                      for a in attrs
                                      if old_code.data.get(a) !=  new_code.data.get(a)])
                    print '  %08s %s' % (c, diffs)
    def update_fachstatistik_merkmale(self):
         self.upd_code('fsag', '1', mini='0', maxi=2)
         self.upd_code('fsag', '2', mini=3, maxi=5)
         self.upd_code('fsag', '3', mini=6, maxi=9)
         self.upd_code('fsag', '4', mini=10, maxi=13)
         self.upd_code('fsag', '5', mini=14, maxi=17)
         self.upd_code('fsag', '6', mini=18, maxi=20)
         self.upd_code('fsag', '7', mini=21, maxi=26)

         self.upd_code('fsagel', '1', mini=1, maxi=20)
         self.upd_code('fsagel', '2', mini=21, maxi=26)
         self.upd_code('fsagel', '3', mini=27, maxi=44)
         self.upd_code('fsagel', '4', mini=45, maxi=54)
         self.upd_code('fsagel', '5', mini=55, maxi=64)
         self.upd_code('fsagel', '6', mini=65, maxi=74)
         self.upd_code('fsagel', '7', mini=75, maxi=150)

         Kategorie(code='fsbe').update({'name': 'Beschäftigungsverhältnis der Eltern'})
         self.upd_code('fsbe', '2', name='Vollzeit angestellt')
         self.upd_code('fsbe', '3', name='Teilzeit angestellt')
         self.upd_code('fsbe', '6', name='arbeitslos (ALGI/II)')

         self.upd_code('fskat', '8', maxi=99999)

         if not self.exists_code('fspbe', '11'):
             self.add_code('fspbe', '11', name='Trennung, Scheidung, Sorge-/Umgangsrecht', sort=8)
         if not self.exists_code('fspbe', '12'):
             self.add_code('fspbe', '12', name='Beziehungskonflikte', sort=9)
                       
         Kategorie(code='fsqualij').update({'dok': 'Beschäftigung Jugendlicher'})
         if not self.exists_code('fsqualij', '7'):
             self.add_code('fsqualij', '7', name='entfällt (unter 14)', sort=7)
         
         self.upd_code('klerv', '1', dok='Wird zur Berechnung der Altersgruppe der Mutter verwendet')
         self.upd_code('klerv', '2', dok='Wird zur Berechnung der Altersgruppe des Vaters verwendet')

         logging.info('Fachstatistik-Merkmale updatet')

    def fachstatistik_items_abschalten(self):
        from ebkus.html.fskonfig import fs_customize as fsc
        abzuschaltende_items = ('ba1', 'ba2', 'pbe', 'pbk', 'no2', 'no3') + \
                               fsc.joker_felder
        for f in abzuschaltende_items:
            f_obj = fsc.get(f)
            flag = f_obj['flag']
            f_obj.update({'flag': flag|1})
        logging.info("Einige Fachstatistik-Items abgeschaltet")


    def fachstatistik_multi(self):
        fs_list = FachstatistikList(where='')
        for fs in fs_list:
            fs_id = fs['id']
            upd = {
                'anmprobleme': "%(ba1)s %(ba2)s" % fs,
                'kindprobleme': "%(pbk)s " % fs + self.get_multi_id_string(
                'fachstatkindproblem_old', 'pbk', fs_id),

                'elternprobleme': "%(pbe)s " % fs + self.get_multi_id_string(
                'fachstatelternproblem_old', 'pbe', fs_id),

                'eleistungen': self.get_multi_id_string(
                'fachstatlei_old', 'le', fs_id),
                }
            fs.update(upd)
        logging.info("Fachstatistik Anmelde- und Problempektrum %s mal updated" % len(fs_list))
            
    def fachstatistik_beschaeftigung_unter_14(self):
        fs_list = FachstatistikList(where='')
        count = 0
        for fs in fs_list:
            upd = {}
            try:
                fall = Fall(fs['fall_id'])
                alter = calc_age(fall['akte__gb'], fall.getDate('bg'))
                if alter < 14:
                    upd['qualij'] = cc('fsqualij', '7')
            except:
                pass
            if upd:
                count += 1
                fs.update(upd)
        logging.info("Fachstatistik Beschaeftigung Jugendlicher %s mal auf 'entfaellt (unter 14)'"
                     % count)
        
    def get_multi_id_string(self, table, feld, fs_id):
        res = SQL("SELECT distinct %s from %s where fstat_id=%s" %
                  (feld,table,fs_id)).execute()
        return ' '.join([str(e[0]) for e in res])
    def jahr_in_bundesstatistik(self):
        "geschlossene Fälle: Ende-Jahr"
        "offene Fälle: bis Mai Vorjahr, sonst dieses Jahr"
        SQL("UPDATE jghstat07 SET jahr=ey WHERE ey IS NOT NULL").execute()
        logging.info("Bundesstatistiken von abgeschlossenen Faellen auf Ende-Jahr gesetzt")
        jahr = today().year
        if today().month < 10:
            jahr -= 1
        SQL("UPDATE jghstat07 SET jahr=%s WHERE ey IS NULL" % jahr).execute()
        logging.info("Bundesstatistiken von andauernden Faellen auf %s gesetzt" % jahr)
    def add_mime_types(self):
         self.add_code('mimetyp', 'odt', name='application/vnd.oasis.opendocument.text')
         self.add_code('mimetyp', 'ods', name='application/vnd.oasis.opendocument.spreadsheet')
         self.add_code('mimetyp', 'odp', name='application/vnd.oasis.opendocument.presentation')
         self.add_code('mimetyp', 'odg', name='application/vnd.oasis.opendocument.graphics')
         self.add_code('mimetyp', 'odc', name='application/vnd.oasis.opendocument.chart')
         self.add_code('mimetyp', 'odf', name='application/vnd.oasis.opendocument.formula')
         self.add_code('mimetyp', 'odi', name='application/vnd.oasis.opendocument.image')
         self.add_code('mimetyp', 'odm', name='application/vnd.oasis.opendocument.text-master')
         logging.info('Mimetypes ergänzt')
         
# fsqualij sozialer Status Jugendlicher, 14-27 Besch%Gï¿½%@tigung Jugendlicher
"""
OBSOLET:  ['dbsite', 'wohnbez']
NEU:      ['aufbew', 'fsjoka1', 'fsjoka2', 'fsjoka3', 'fsjoka4', 'fsjokf5', 'fsjokf6', 'fsjokf7', 'fsjokf8', 'fska', 'fskd', 'fuabs', 'fuadbs', 'kabs', 'kdbs', 'teilnbs']
*** differ:  fsag Altersgruppe Kind/Jugendliche Altersgruppe Kind/Jugendliche
['1', '2', '3', '4', '5', '6', '7', '8', '9', '999']
         1 mini{None,0} maxi{None,2}
         2 mini{None,3} maxi{None,5}
         3 mini{None,6} maxi{None,9}
         4 mini{None,10} maxi{None,13}
         5 mini{None,14} maxi{None,17}
         6 mini{None,18} maxi{None,20}
         7 mini{None,21} maxi{None,26}
         8
         9
       999
*** differ:  fsagel Altersgruppe Eltern Altersgruppe Eltern
['1', '2', '3', '4', '5', '6', '7', '999']
         1 mini{None,1} maxi{None,20}
         2 mini{None,21} maxi{None,26}
         3 mini{None,27} maxi{None,44}
         4 mini{None,45} maxi{None,54}
         5 mini{None,55} maxi{None,64}
         6 mini{None,65} maxi{None,74}
         7 mini{None,75} maxi{None,150}
       999
*** differ:  fsbe Beruf der Eltern Besch%Gï¿½%@tigungsverh%Gï¿½%@tnis der Eltern
['1', '10', '2', '3', '4', '5', '6', '7', '8', '9', '999']
         1
        10
         2 name{Vollzeit angestellt / ABM,Vollzeit angestellt}
         3 name{Teilzeit angestellt / ABM,Teilzeit angestellt}
         4
         5
         6 name{arbeitslos,arbeitslos (ALGI/II)}
         7
         8
         9
       999
*** differ:  fskat Anzahl der Termine Anzahl der Termine
['0', '1', '2', '3', '4', '5', '6', '7', '8']
         0
         1
         2
         3
         4
         5
         6
         7
         8 maxi{None,99999}
*** differ:  fspbe Problemspektrum Eltern Problemspektrum Eltern
['1', '10', '11', '12', '2', '3', '4', '5', '6', '7', '8', '9', '999']
         1
        10 sort{10,12}
        11  fehlt  11
        12  fehlt  12
         2
         3
         4
         5
         6
         7
         8 sort{8,10}
         9 sort{9,11}
       999 sort{11,13}
*** differ:  fsqualij sozialer Status Jugendlicher, 14-27 Besch%Gï¿½%@tigung Jugendlicher
['1', '2', '3', '4', '5', '6', '7', '999']
         1
         2
         3
         4
         5
         6
         7  fehlt  7
       999 sort{8,9}
*** differ:  gm Gemeinde Gemeinde
['000']
       000
*** differ:  gmt Gemeindeteil Gemeindeteil
['000']
       000
*** differ:  klerv Verwandtschaftsgrad Verwandtschaftsgrad
['1', '10', '11', '12', '13', '2', '3', '4', '5', '6', '7', '8', '9', '999']
         1 dok{,Wird zur Berechnung der Altersgruppe der Mutter verwendet}
        10
        11
        12
        13
         2 dok{,Wird zur Berechnung der Altersgruppe des Vaters verwendet}
         3
         4
         5
         6
         7
         8
         9
       999
*** differ:  kr Kreis Kreis
['01', '101', '103', '151', '158']
        01  01  fehlt
       101  fehlt  101
       103  fehlt  103
       151  fehlt  151
       158  fehlt  158
*** differ:  land Land (Feld 2-3) Land (Feld 2-3)
['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16']
        01  fehlt  01
        02  fehlt  02
        03  fehlt  03
        04  fehlt  04
        05  fehlt  05
        06  fehlt  06
        07  fehlt  07
        08  fehlt  08
        09  fehlt  09
        10  fehlt  10
        11  fehlt  11
        12 sort{1,12} name{Muster-Land,Brandenburg}
        13  fehlt  13
        14  fehlt  14
        15  fehlt  15
        16  fehlt  16
*** differ:  mimetyp Mime Typ Mime Typ
['asc', 'bmp', 'doc', 'dot', 'gif', 'gtar', 'gz', 'htm', 'html', 'jpe', 'jpeg', 'jpg', 'odc', 'odf', 'odg', 'odi', 'odm', 'odp', 'ods', 'odt', 'pdf', 'png', 'ps', 'rtf', 'rtx', 'sdc', 'sdw', 'sxw', 'tar', 'tgz', 'tif', 'tiff', 'txt', 'wrd', 'xls', 'zip']
       asc
       bmp sort{28,36}
       doc
       dot
       gif sort{21,29}
      gtar sort{16,24}
        gz sort{18,26}
       htm
      html
       jpe sort{24,32}
      jpeg sort{23,31}
       jpg sort{22,30}
       odc  fehlt  odc
       odf  fehlt  odf
       odg  fehlt  odg
       odi  fehlt  odi
       odm  fehlt  odm
       odp  fehlt  odp
       ods  fehlt  ods
       odt  fehlt  odt
       pdf
       png sort{27,35}
        ps
       rtf
       rtx sort{20,28}
       sdc
       sdw
       sxw
       tar sort{19,27}
       tgz sort{17,25}
       tif sort{26,34}
      tiff sort{25,33}
       txt
       wrd
       xls
       zip sort{15,23}
*** differ:  rbz Regierungsbezirk Regierungsbezirk
['0']
         0
*** differ:  verwtyp Feldverwendungstyp Feldverwendungstyp
['b', 'f', 'k', 'm', 'p', 's']
         b
         f
         k
         m  fehlt  m
         p
         s
"""



    
class MerkmalsKatalog(object):
    def __init__(self, datei):
        merkmale = {}
        execfile(datei, merkmale)
        kategorie_zeilen = merkmale['kategorie_list_str'].strip().split('\n')
        kategorien = [k.strip().split(';') for k in kategorie_zeilen if k]
        code_zeilen = merkmale['code_list_str'].strip().split('\n')
        codes = [c.strip().split(';') for c in code_zeilen if c]
        self.bereichskategorien = merkmale['bereichs_kategorien_str'].split()
        self.init_katalog(kategorien)
        self.init_codes(codes)
        #self.test()

    def test(self):
        for kat_code in self.katalog:
            k = self.katalog[kat_code]
            print k['code'], k['name'], k['dok']
            for c in k['codes']:
                print '  ', c['code'], c['name'], c['sort'], c['dok']

    def init_katalog(self, kategorien):
        self.katalog = {}
        for kdata in kategorien:
            #print 'KDATA', kdata
            k = Kategorie()
            code = kdata[0]
            k.init(code=code,
                   name=kdata[1],
                   dok=len(kdata) > 2 and kdata[2] or '',
                   flag=code in self.bereichskategorien and 1 or 0,
                   codes=[]
                   )
            self.katalog[code] = k
    def init_codes(self, codes_data):
        for cdata in codes_data:
            c = Code()
            code, name, kat_code = cdata[:3]
            kat = self.katalog[kat_code]
            codes = kat['codes']
            bereichs_kat = bool(kat['flag'])
            sort = len(codes) > 0 and codes[-1]['sort'] + 1 or 1
            c.init(code=code,
                   name=name,
                   kat_code=kat_code,
                   sort=sort,
                   off=0,
                   flag=0,
                   )
            
            if bereichs_kat and len(cdata) > 3 and cdata[3]:
                c['mini'] = int(cdata[3])
            if bereichs_kat and len(cdata) > 4 and cdata[4]:
                c['maxi'] = int(cdata[4])
            if len(cdata) > 5 and cdata[5]:
                c['dok'] = cdata[5]
            codes.append(c)

def create_new_kategorien(new_table, merkmals_datei):
    """Erstelle eine Liste der Kategorien und eine Liste der Codes,
    die für new_table benötigt werden, aber noch nicht in der Datenbank
    sind.
    """
    
    needed = [f.kat_code for f in new_table.fields if f.kat_code]
    needed.append('jghag') # Altersgruppe in keinem Feld
    existing = [k['code'] for k in KategorieList(where='')]
    needed_and_not_existing = [k for k in needed if k not in existing]
    
    merkmale = {}
    execfile(merkmals_datei, merkmale)
    kategorie_zeilen = merkmale['kategorie_list_str'].strip().split('\n')
    kategorien = [k.strip().split(';') for k in kategorie_zeilen]
    code_zeilen = merkmale['code_list_str'].strip().split('\n')
    codes = [c.strip().split(';') for c in code_zeilen]
    #print kategorien
    #print codes
    needed_kategorien = [k for k in kategorien if k[0] in needed_and_not_existing]
    needed_codes = [c for c in codes if c[2] in needed_and_not_existing]
    #print 'KATEGORIEN', needed_kategorien
    #print 'CODES:', needed_codes

    for kat_code, kat_name in needed_kategorien:
        k = Kategorie()
        k.new()
        k['code'] = kat_code
        k['name'] = kat_name
        k['zeit'] = int(time())
        k.insert()
        logging.debug("Neue Kategorie für %s: %s" % (kat_name, kat_code))
    logging.info("Neue Kategorien hinzugefügt")

    last_kat_code = None
    for code_data in needed_codes:
        code, name, kat_code = code_data[:3]
        if kat_code != last_kat_code:
            k = Kategorie(code=kat_code)
            sort = 1
        c = Code()
        c.new()
        c['code'] = code
        c['name'] = name
        c['kat_id'] = k['id']
        c['kat_code'] = kat_code
        c['sort'] = sort
        c['off'] = 0
        c['zeit'] = int(time())
        if len(code_data) > 3 and code_data[3]:
            c['mini'] = int(code_data[3])
        if len(code_data) > 4 and code_data[4]:
            c['maxi'] = int(code_data[4])
        c.insert()
        sort += 1
        logging.debug("Neue Code für %s: %s" % (name, code))
    logging.info("Neue Codes hinzugefügt")

    """
mitarbeiter
protokoll
strassenkat_old, strkatalog !!!
akte
    akte.gs
    akte.aufbew
    akte.plraum
    -akte.wohnbez
    -akte.planungsr
    akte.stzak --> akte.stzbg
fall
anmeldung
    -anmeldung.ad,am,ay
bezugsperson
    bezugsperson.gs
einrichtung
leistung
[beratungskontakt, mitarbeiterberatungskontakt, fallberatungskontakt, fua_bs]
zustaendigkeit
dokument
gruppendokument
gruppe
fallgruppe
bezugspersongruppe
mitarbeitergruppe
fachstat
    fachstat.plz
    fachstat.ort
    fachstat.ortsteil
    fachstat.samtgemeinde
    fachstat.bezirk
    fachstat.plraum
    -fachstat.bz
    fachstat.anmprobleme
    fachstat.kindprobleme     füllen
    fachstat.elternprobleme   füllen
    fachstat.eleistungen      füllen
    fachstat.joka1
    fachstat.joka2
    fachstat.joka3
    fachstat.joka4
    fachstat.jokf5
    fachstat.jokf6
    fachstat.jokf7
    fachstat.jokf8
    
    jghstat07.jahr

    kategorie.flag

    code.flag

    tabelle.maxist
    
    """
# code.flag, kategorie.flag einführen, Bereichskategorien auf 1 setzen

"""
OBSOLETE TABELLEN:  ['exportprotokoll', 'fachstatelternproblem', 'fachstatkindproblem', 'fachstatlei', 'importprotokoll', 'mitstelle', 'schluessel', 'sessions', 'strassenkat', 'tabid']

NEUE TABELLEN:      ['abfrage', 'altdaten', 'beratungskontakt', 'fallberatungskontakt', 'fua_bs', 'mitarbeiterberatungskontakt', 'register', 'strkatalog']

GEMEINS. TABELLEN:  ['akte', 'anmeldung', 'bezugsperson', 'bezugspersongruppe', 'code', 'dokument', 'einrichtung', 'fachstat', 'fall', 'fallgruppe', 'feld', 'gruppe', 'gruppendokument', 'jghstat', 'jghstat07', 'kategorie', 'leistung', 'mitarbeiter', 'mitarbeitergruppe', 'protokoll', 'tabelle', 'zustaendigkeit']

akte ['planungsr', 'wohnbez'] ['gs', 'aufbew', 'plraum']
anmeldung ['ad', 'am', 'ay'] []
bezugsperson [] ['gs']
bezugspersongruppe [] []
code [] ['flag']
dokument [] []
einrichtung [] []
fachstat ['bz'] ['plz', 'ort', 'ortsteil', 'samtgemeinde', 'bezirk', 'plraum', 'anmprobleme', 'kindprobleme', 'elternprobleme', 'eleistungen', 'joka1', 'joka2', 'joka3', 'joka4', 'jokf5', 'jokf6', 'jokf7', 'jokf8']
fall [] []
fallgruppe [] []
feld [] []
gruppe [] []
gruppendokument [] []
jghstat ['bezirksnr'] []
jghstat07 ['bezirksnr'] ['jahr']
kategorie [] ['flag']
leistung [] []
mitarbeiter [] []
mitarbeitergruppe [] []
protokoll [] []
tabelle [] ['maxist']
zustaendigkeit [] []
"""

def write_success_file(version):
    name = 'update_auf_%s_war_erfolgreich' % version
    filename = join(config.EBKUS_HOME, name)
    open(filename, 'w').write(filename)

# jahr in jgh07
# fsqualij
# kr, rbz KategorieDoku 

def ist_version_3_3():
    tables = getDBHandle().listtables()
    if ('jghstat07' in tables and
        not 'strkatalog' in tables and
        'fachstatlei' in tables):
        return True
    return False
        

## def update_is_possible():
##     from ebkus import Version
##     if Version.startswith('4.0'):
##         logging.info("Diese EBKuS-Version (%s) kann mit diesem Patch updatet werden" % Version)
##         return True
##     logging.critical("Diese EBKuS-Version (%s) kann nicht mit diesem Patch updatet werden" % Version)
##     return False

# ab hier private
def needs_update(ziel_version):
    name = 'update_auf_%s_war_erfolgreich' % ziel_version
    filename = join(config.EBKUS_HOME, name)
    #if exists(
    db = getDBHandle()
    if 'jghstat07' in db.listtables():
        felder = db.listfields('jghstat07')
        for f in felder:
            if f[0] == 'jahr':
                return False
    return True

def do_update():
    # Protokoll abschalten
    from ebkus.app.protocol import temp_off
    temp_off()
    from ebkus import Version
    from ebkus.app.ebapi import register_set
    register_set('Version', Version)
    Kategorie(code='kr').update({
        'dok': "amtlicher Gemeindeschlüssel (AGS, Ziffer 3-5)"})
    Kategorie(code='rbz').update({
        'dok': "amtlicher Gemeindeschlüssel (AGS) obsolet, in Kreis mit drin"})


def neue_tabellen():
    'strkatalog'
    'beratungskontakt'
    'mitarbeiterberatungskontakt'
    'fallberatungskontakt'
    'fua_bs'
    'register'
    'abfrage'
    'altdaten'


def neue_felder():
    SQL('ALTER TABLE jghstat07 ADD COLUMN jahr INT').execute()
    logging.info('Feld jahr zu jghstat07 hinzugefuegt')
    SQL('ALTER TABLE kategorie ADD COLUMN flag INT DEFAULT 0').execute()
    SQL('ALTER TABLE code ADD COLUMN flag INT DEFAULT 0').execute()

