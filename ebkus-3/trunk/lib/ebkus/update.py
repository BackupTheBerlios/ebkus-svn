# coding: latin-1
import logging
from os.path import join
from time import time

from ebkus.config import config
from ebkus.db.sql import opendb, closedb, getDBHandle, SQL
from ebkus.gen.schemagen import get_schema_info
from ebkus.gen.schemadata import schemainfo
from ebkus.gen.genEb import generate_ebapi
from ebkus.app.ebapi import Tabelle, Feld, FeldList, Kategorie, KategorieList, Code
    
# public
def needs_update():
    db = getDBHandle()
    if 'jghstat07' in db.listtables():
        return False
    else:
        return True

def xneeds_update():
    #return True
    return False

def do_update():
    create_new_table()
    # das kommt später wieder raus
    # ebapigen.py wird fertig mitgeliefert
    regenerate_ebapi()
    # zum Testen
    import ebkus.app.ebapi
    jgh07 = ebkus.app.ebapi.Jugendhilfestatistik2007()
    #create_new_kategorien()
    create_primary_keys()
    return True


# ab hier private
def check_new_table():
    return False

def check_new_version():
    return False

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
                               'merkmale_berlin.py'))
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
    return True

def create_new_kategorien(new_table, merkmals_datei):
    """Erstelle eine Liste der Kategorien und eine Liste der Codes,
    die für new_table benötigt werden, aber noch nicht in der Datenbank
    sind.
    """
    
    needed = [f.kat_code for f in new_table.fields if f.kat_code]
    existing = [k['code'] for k in KategorieList(where='')]
    needed_and_not_existing = [k for k in needed if k not in existing]
    
    merkmale = {}
    execfile(merkmals_datei, merkmale)
    kategorie_zeilen = merkmale['kategorie_list_str'].strip().split('\n')
    kategorien = [k.strip().split(';') for k in kategorie_zeilen]
    code_zeilen = merkmale['code_list_str'].strip().split('\n')
    codes = [c.strip().split(';') for c in code_zeilen]

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
        logging.info("Neue Kategorie für %s: %s" % (kat_name, kat_code))

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
        logging.info("Neuer Code für %s: %s" % (name, code))

def regenerate_ebapi():
    import ebkus.app.ebapigen
    f = generate_ebapi(schemainfo)
    ebapigen_fn = join(config.EBKUS_PYTHON_PATH, 'ebkus', 'app', 'ebapigen.py')
    open(ebapigen_fn, 'w').write(f.getvalue())
    reload(ebkus.app.ebapigen)
    reload(ebkus.app.ebapi)
    


def create_primary_keys():
    kid = Code(kat_code='verwtyp', code='s')['id']
    primary_key_felder = FeldList(where='verwtyp=%s' % kid)
    for f in primary_key_felder:
        fname = f['feld']
        tname = f['tab__tabelle']
        try:
            res = SQL('ALTER TABLE %s ADD PRIMARY KEY (%s)' % (tname, fname)).execute()
            logging.info("Primärschlüsselindex für Tabelle %s hinzugefügt" % tname)
        except:
            # if index already exists we don't care
            pass
    
def update_version():
    return False
