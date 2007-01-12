# coding: latin-1
import os, sys, logging
from os.path import join
from time import time

from ebkus.config import config
from ebkus.db.sql import opendb, closedb, getDBHandle, SQL
from ebkus.gen.schemagen import get_schema_info
from ebkus.gen.schemadata import schemainfo
from ebkus.gen.genEb import generate_ebapi
from ebkus.app.ebapi import Tabelle, Feld, FeldList, TabellenID, Kategorie, KategorieList, Code
    
# public
def update():
    try:
        opendb()
    except:
        # Zum Update muss die Datenbank verfügbar sein.
        # Daher:
        logging.critical("Für das Update muss die Datenbank verfügbar sein!",
                         exc_info=True)
        logging.shutdown()
        sys.exit(1)
    if needs_update():
        logging.info("Update von EBKuS 3.2 auf 3.3 (neue gesetzliche Statistik) beginnt")
        try:
            do_update()
            logging.info("Update von EBKuS 3.2 auf 3.3 erfolgreich")
        except Exception, e:
            t = sys.exc_info()[0]
            logging.exception("%s: %s", t, e)
            logging.critical("Update von EBKuS 3.2 auf 3.3 misslungen")
            logging.shutdown()
            sys.exit(1)
            
    else:
        logging.info("Kein Update erforderlich")

# ab hier private
def needs_update():
    db = getDBHandle()
    if 'jghstat07' in db.listtables():
        return False
    else:
        return True
##     name = 'update_auf_3.3_war_erfolgreich'
##     filename = join(config.EBKUS_HOME, name)
##     try:
##         if open(filename).read(100) == name:
##             return False
##         else:
##             return True
##     except:
##         return True
    
def do_update():
    alter_plraum_fields()
    if config.BERLINER_VERSION:
        replace_strassenkat()
    create_index_strassenkat()
    update_planungs_raeume()
    delete_old_strassenkat()
    create_new_table()
    # zum Testen
    import ebkus.app.ebapi
    jgh07 = ebkus.app.ebapi.Jugendhilfestatistik2007()
    #create_new_kategorien()
    create_primary_keys()
    name = 'update_auf_3.3_war_erfolgreich'
    filename = join(config.EBKUS_HOME, name)
    open(filename, 'w').write(filename)
    return True


def create_index_strassenkat():
    if config.BERLINER_VERSION:
        for t in ('strassenkat', 'strassenold'):
            for f in ('str_nummer', 'plz', 'hausnr'):
                SQL('ALTER TABLE %s ADD KEY (%s)' % (t,f)).execute()
                logging.info("Index fuer Feld %s in Tabelle %s" % (f, t))

def delete_old_strassenkat():
    if config.BERLINER_VERSION:
        SQL('DROP TABLE strassenold').execute()
    logging.info("Alter Strassenkatalog gelöscht")

def alter_plraum_fields():
    d = (('akte', 'planungsr'),('fachstat', 'bz'))
    for t, f in d:
        SQL('ALTER TABLE %s MODIFY %s CHAR(8)' % (t, f)).execute()
        tab = Tabelle(tabelle=t)
        f = Feld(tab_id=tab['id'], feld=f)
        f.update({'typ': 'CHAR(8)'})
        logging.info("Feldlänge auf CHAR(8) gesetzt in Tabelle %s Feld %s" % (t, f['feld']))
        
def replace_strassenkat():
    if not config.BERLINER_VERSION:
        return
    SQL('ALTER TABLE strassenkat RENAME strassenold').execute()
    logging.info("Tabelle strassenkat umbenannt in strassenold")
    from ebkus.Install import sql_split
    if config.INSTANCE_NAME.startswith('demo'):
        str_kat = 'strassenkat_berlin_ausschnitt.sql.gz'
        # TODO rückgangi
        #str_kat = 'strassenkat_berlin.sql.gz'
    else:
        str_kat = 'strassenkat_berlin.sql.gz'
    filename = join(config.EBKUS_HOME, 'sql', str_kat)
    if sys.platform == 'win32':
        for c in sql_split(filename):
            SQL(c).execute()
    else:
        # viel schneller
        user = config.DATABASE_USER
        pw = config.DATABASE_PASSWORD
        pw_arg = pw and "-p%s" % pw or ''
        db = config.DATABASE_NAME
        os.system("zcat %s | mysql -u%s %s %s" % (filename, user, pw_arg, db))
    logging.info("Neuer Strassenkatalog importiert von %s" % filename)
    

def update_planungs_raeume():
    if config.BERLINER_VERSION:
        lage_innerhalb = Code(kat_code='lage', code='0')['id']
        s = SQL("""\
UPDATE akte a, fall f, fachstat fs,
     strassenold o, strassenkat i
SET a.planungsr=i.Plraum, fs.bz=i.Plraum
WHERE a.lage=%s AND
      o.str_nummer=i.str_nummer AND
      a.str=o.str_name and a.hsnr=o.hausnr AND
      a.plz=o.plz AND o.hausnr=i.hausnr AND
      f.akte_id=a.id AND fs.fall_id=f.id
        """ % lage_innerhalb).execute()
        s = SQL("""\
UPDATE akte a, fall f, fachstat fs
SET a.planungsr='0', fs.bz='0'
WHERE a.lage!=%s AND
      f.akte_id=a.id AND fs.fall_id=f.id
        """ % lage_innerhalb).execute()
        logging.info("Planungsräume in akte und fachstat updated")
    else:
        SQL("""\
UPDATE akte a
SET a.planungsr='0'
WHERE a.planungsr='9999'
        """).execute()
        SQL("""\
UPDATE fachstat fs
SET fs.bz='0'
WHERE fs.bz='9999'
        """).execute()
        logging.info("Planungsräume '9999' in akte und fachstat durch '0' ersetzt")

def create_new_table():
    tables = get_schema_info(schemainfo)
    jghstat07 = [t for t in tables if t.tablename == 'jghstat07'][0]
    db = getDBHandle()
    #print jghstat07.sql_create()
    db.query(jghstat07.sql_create())
    #table_id = 32
    #field_id = 333
    table_id = Tabelle().getNewId()
    #print jghstat07.sql_insert(table_id)
    db.query(jghstat07.sql_insert(table_id))
    for f in jghstat07.fields:
        field_id = Feld().getNewId()
        #print f.sql_insert(field_id)
        db.query(f.sql_insert(field_id))
    j07 = Tabelle(tabelle='jghstat07')
    logging.info("Neue Tabelle für %s: %s" % (j07['name'], 'jghstat07'))
    create_new_kategorien(jghstat07,
                          join(config.EBKUS_HOME, 'sql',
                               'merkmale_standard.py'))
#                               'merkmale_berlin.py'))
    for f in jghstat07.fields:
        fupd = Feld()
        v = Code(code=f.verwtyp, kat_code='verwtyp')
        fupd['verwtyp'] = v['id']
        if f.verwtyp in 'kb':
            kat = Kategorie(code=f.kat_code)
            fupd['kat_id'] = kat['id']
            fupd['kat_code'] = kat['code']
        if f.verwtyp in 'fk':    # kodierte Felder sind Fremdschlüssel nach code
            fupd['ftab_id'] = Tabelle(tabelle=f.ftable)['id']
            if f.verwtyp in 'f':    # Name für inverse Beziehung
                fupd['inverse'] = f.inverse
        feld = Feld(feld=f.fieldname, tab_id=j07['id'])
        feld.update(fupd)

    site = Code(kat_code='dbsite', code=config.SITE)
    t = TabellenID()
    t['table_id'] = j07['id']
    t['table_name'] = j07['tabelle']
    t['dbsite'] = site['id']
    t['minid'] = site['mini']
    t['maxid'] = site['maxi']
    t['maxist'] = 1
    t.insert()
    return True

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


def create_primary_keys():
    kid = Code(kat_code='verwtyp', code='s')['id']
    primary_key_felder = FeldList(where='verwtyp=%s' % kid)
    for f in primary_key_felder:
        fname = f['feld']
        tname = f['tab__tabelle']
        try:
            res = SQL('ALTER TABLE %s ADD PRIMARY KEY (%s)' % (tname, fname)).execute()
        except:
            # if index already exists we don't care
            pass
    logging.info("Primärschlüsselindex für Tabellen hinzugefügt")
    
