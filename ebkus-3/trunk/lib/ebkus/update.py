# coding: latin-1
import os, sys, logging
from os.path import join
from time import time

from ebkus.config import config
from ebkus.db.sql import opendb, closedb, getDBHandle, SQL
from ebkus.gen.schemagen import get_schema_info
from ebkus.gen.schemadata import schemainfo
from ebkus.gen.genEb import generate_ebapi
from ebkus.app.ebapi import Tabelle, Feld, FeldList, Kategorie, KategorieList, Code
    
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
    if not update_is_possible():
        sys.exit(1)
    if needs_update():
        logging.info("Update von EBKuS 4.0 auf 4.0.2 beginnt")
        try:
            do_update()
            logging.info("Update von EBKuS 4.0 auf 4.0.2 erfolgreich")
        except Exception, e:
            t = sys.exc_info()[0]
            logging.exception("%s: %s", t, e)
            logging.critical("Update von EBKuS 4.0 auf 4.0.2 misslungen")
            logging.shutdown()
            sys.exit(1)
            
    else:
        logging.info("Kein Update erforderlich")

# jahr in jgh07
# fsqualij
# kr, rbz KategorieDoku 

def update_is_possible():
    from ebkus import Version
    if Version.startswith('4.0'):
        return True
    logging.critical("Diese EBKuS-Version (%s) kann nicht mit diesem Patch updatet werden" % Version)
    return False

# ab hier private
def needs_update():
    db = getDBHandle()
    felder = db.listfields('jghstat07')
    for f in felder:
        if f[0] == 'jahr':
            return False
    return True

def do_update():
    SQL('ALTER TABLE jghstat07 ADD COLUMN jahr INT')
    from ebkus import Version
    from ebkus.app.ebapi import register_set
    register_set('Version', Version)
    Kategorie(code='kr').update({
        'dok': "amtlicher Gemeindeschlüssel (AGS, Ziffer 3-5)"})
    Kategorie(code='rbz').update({
        'dok': "amtlicher Gemeindeschlüssel (AGS) obsolet, in Kreis mit drin"})
    
