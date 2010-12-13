#!/usr/local/bin/python
# coding: latin-1

"""
  Parsen der Code-, Kategorien-, Mitarbeiter-,TabellenId-Liste.

  Kategorien eintragen
    aus der vollst�ndigen Liste
  Codes eintragen
    aus der vollst�ndigen Liste
  Administrator und Mitarbeiter eintragen
    aus der Liste
  (die Daten stehen in migrdata)

Tabelle feld mit den Kategoriecodes/ids aktualisieren
  die Daten stehen in schemagen (Table/Field Instanzen)

Tabelle tabid initialisieren

"""
import sys, string
from ebkus.app.ebapi import *
from ebkus.db import sql
from ebkus.db import dbapp
from ebkus.gen import schemagen
from ebkus.gen import schemadata
from ebkus.config import config
from time import time



#class MigrError(Exception):
#  pass


## class IdGen:
##     def __init__(self):
##         self.A = 1
##         self.B = 3000001
        
##     def get(self, dbsite):
##         if dbsite == 'A': return self.getA()
##         if dbsite == 'B': return self.getB()
##         raise 'FALSCHE DBSITE'
        
##     def getA(self):
##         res = self.A
##         self.A = self.A + 1
##         return res
        
##     def getB(self):
##         res = self.B
##         self.B = self.B + 1
##         return res
        
        
def parse_code_list(str):
    import string
    import re
    codes = []
    lines  = string.split(str, '\n')
    for lstr in lines:
        lstr = string.strip(lstr)
        if not lstr:
            continue
        l = re.split('[\s]*;[\s]*', lstr)
        if len(l) < 3:
            print lstr
            raise 'Error in codelist'
        codes.append(l)
    return codes
    
    ## print parse_code_list(code_list_str)
    ## print
    
def parse_kategorie_list(str):
    import string
    import re
    kategories = []
    lines  = string.split(str, '\n')
    for lstr in lines:
        lstr = string.strip(lstr)
        if not lstr:
            continue
        l = re.split('[\s]*;[\s]*', lstr)
        if len(l) < 2:
            print lstr
            raise 'Error in kategorielist %s' % lstr
        kategories.append(l)
    return kategories
    
    
    ## print parse_kategorie_list(kategorie_list_str)
    ## print
    
def parse_mitarbeiter_list(str):
    import string
    import re
    mitarbeiter = []
    lines  = string.split(str, '\n')
    for lstr in lines:
        lstr = string.strip(lstr)
        if not lstr:
            continue
        l = re.split('[\s]*;[\s]*', lstr)
        if len(l) < 6:
            print lstr
            raise 'Error in codelist'
        mitarbeiter.append(l)
    return mitarbeiter
    
def parse_tab_id(str):
    import string
    import re
    codes = []
    lines  = string.split(str, '\n')
    for lstr in lines:
        lstr = string.strip(lstr)
        if not lstr:
            continue
        l = re.split('[\s]*,[\s]*', lstr)
        if len(l) < 5:
            print lstr
            raise 'Error in codelist'
        codes.append(l)
    return codes
    
    
def insert_kategorien(merkmale):
    kl = KategorieList(where = '')
    if kl:
        #print 'Kategorien schon definiert, werden gel�scht'
        kl.deleteall()
    #print 'Kategorien einf�gen'
    klistdata = parse_kategorie_list(merkmale['kategorie_list_str'])
    bereichslist = string.split(merkmale['bereichs_kategorien_str'])
    aenderungszeit = int(time())
    for kd in klistdata:
        k = Kategorie()
        #k.new(idgen.getA())
        k.new()
        k['code'] = kd[0]
        k['name'] = kd[1]
        try:
            k['dok'] = kd[2]
        except:
            pass # kein dok-string
        bereichskat = (kd[0] in bereichslist) and 1 or 0
        k['flag'] = bereichskat
        k['zeit'] = aenderungszeit
        k.insert()
        
def insert_kategorie_codes(merkmale):
    cl = CodeList(where = '')
    if cl:
        #print 'Codes schon definiert, werden gel�scht'
        cl.deleteall()
    #print 'Codes einf�gen'
    clistdata = parse_code_list(merkmale['code_list_str'])
    bereichslist = string.split(merkmale['bereichs_kategorien_str'])
    #idgen = IdGen()
    katcode = None
    aenderungszeit = int(time())
    for cd in clistdata:
        if katcode != cd[2]:
            #print 'KATCODE', katcode
            # Neue Kategorie
            katl = KategorieList(where = "code = '%s'" % cd[2])
            #print 'KATL', katl
            if len(katl) != 1:
                raise 'Keine eindeutige Kategorie f�r code: %s' % cd
            kat = katl[0]
            katcode = cd[2]
            sort = 1
            #print "Code f�r '%s' einf�gen" % kat['name']
        c = Code()
        #c.new(idgen.getA())
        c.new()
        c['code'] = cd[0]
        c['name'] = cd[1]
        c['kat_id'] = kat['id']
        c['kat_code'] = kat['code']
        c['sort'] = sort
        c['off'] = 0
        c['zeit'] = aenderungszeit
        assert c['kat_code'] == katcode == kat['code'] == cd[2]
        sort = sort + 1
        #print 'BBB', cd
        if katcode in bereichslist and len(cd) > 4:
            c['mini'] = int(cd[3])
            c['maxi'] = int(cd[4])
        if len(cd) > 5:
            c['dok'] = cd[5].strip()
        c.insert()
        
def update_feld():
    #print 'Feld tabelle erg�nzen'
    tables = schemagen.get_schema_info(schemadata.schemainfo)
    verwtlist = CodeList(where = "kat_code = 'verwtyp'")
    katlist = KategorieList(where = '')
    dbtlist = TabelleList(where = '')
    for t in tables:
        dbt = dbtlist.findu("tabelle", t.tablename)
        assert dbt['tabelle'] == t.tablename
        #print "Tabelle '%s'" % t.tablename
        dbfields = FeldList(where = "tab_id = %s" % dbt['id'])
        for f in t.fields:
            dbf = dbfields.findu('feld', f.fieldname)
            assert dbf['feld'] == f.fieldname
            verwtyp = verwtlist.findu('code', f.verwtyp)
            dbfupd = Feld()
            dbfupd['verwtyp'] = verwtyp['id']
            #print "  Feld '%s' (%s %s)" % (f.fieldname, f.verwtyp, f.ref)
            if f.verwtyp in 'kmb':
                kat = katlist.findu('code', f.kat_code)
                dbfupd['kat_id'] = kat['id']
                dbfupd['kat_code'] = kat['code']
            if f.verwtyp in 'fkm':    # kodierte Felder sind Fremdschl�ssel nach code
                dbfupd['ftab_id'] = dbtlist.findu('tabelle', f.ftable)['id']
                if f.verwtyp in 'f':    # Name f�r inverse Beziehung
                    dbfupd['inverse'] = f.inverse
            dbf.update(dbfupd)
            
def insert_mitarbeiter(merkmale):
    mitl = MitarbeiterList(where = '')
    if mitl:
        #print 'Mitarbeiter schon eingetragen, werden gel�scht'
        mitl.deleteall()
    #print 'Mitarbeiter einf�gen'
    mlistdata = parse_mitarbeiter_list(merkmale['mitarbeiter_list_str'])
    #idgen = IdGen()
    aenderungszeit = int(time())
    for ml in mlistdata:
        m = Mitarbeiter()
        #m.new(idgen.getA())
        m.new()
        m['vn'] = ml[0]
        m['na'] = ml[1]
        m['ben'] = ml[2]
        m['stat'] = cc('status', '%s' % ml[3])
        m['benr'] = cc('benr', '%s' % ml[4])
        m['stz'] = cc('stzei', '%s' % ml[5])
        m['zeit'] = aenderungszeit
        m['pass'] = ml[6]
        m.insert()
        
def init_maxist():
    for tab in TabelleList(where='', order='id'):
        feld_list = FeldList(where='tab_id=%d and verwtyp=%d'
                             % (tab['id'], cc('verwtyp', 's')))
        if feld_list:
            primarykey = feld_list[0]['feld']
            maxid = sql.SQL("select max(%s) from %s" %
                            (primarykey, tab['tabelle'])).execute()[0][0]
            if not maxid:
                maxid = 0
            tab.update({'maxist': maxid})
            
def migrate(file_name):
    import ebkus.app.protocol
    try:
        dbapp.cache_off() # tbd muss das sein?
        ebkus.app.protocol.temp_off()
        merkmale = {}
        execfile(file_name, merkmale)
        assert merkmale.has_key('code_list_str')
        assert merkmale.has_key('bereichs_kategorien_str')
        assert merkmale.has_key('kategorie_list_str')
        assert merkmale.has_key('mitarbeiter_list_str')
        insert_kategorien(merkmale)
        insert_kategorie_codes(merkmale)
        insert_mitarbeiter(merkmale)
        update_feld()
        init_maxist()
    finally:
        ebkus.app.protocol.temp_on()
    
    
if __name__ == '__main__':
    if len(sys.argv) > 1:
        merkmals_def = sys.argv[1]
    else:
        raise Exception("keine Merkmalsdefinition")
    dbapp.cache_off()
    opendb()
    migrate(merkmals_def)
    closedb()
    mk_daten_dirs(config.AK_DIRS_MAX)



