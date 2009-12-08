#!/usr/local/bin/python
# coding: latin-1

"""Modul zur Generierung der Anwendungsschnittstelle für die EB
Klientenverwaltung.

Die in diesem Modul definierte Funktion

                  gen_api()

erzeugt die Objektklassen in der Datei ebapigen.py.

Voraussetzung für die Generierung ist, daß schemagen.init_new_db()
bereits gelaufen sein muß, da auf die (Meta-) Datenbanktabllen
'tabelle' und 'feld' zurückgegriffen wird.

gen_api() verwendet folgende Quellen für die Generierung:

Neues Schema:
 - schemagen.get_schema_info() (siehe Modul schemagen.py)

 - Feldname und -typen sowie Klassennamen werden direkt aus der
   Datenbank abgefragt.

TODO:

- die Generierung alleine von schemagen.get_schema_info() abhängig machen.
  Das wäre viel übersichtlicher und einfacher.

"""
import sys
import logging


template = \
"""
#####################################
# %(lname)s  (Tabelle '%(table)s')
#####################################


class %(lname)s(DBObjekt):
    table = '%(table)s'
    fields =  %(dbfields)s
    fieldlengths = %(dbfieldlengths)s
    fieldtypes = {}
    foreignfieldtypes = {}
    inversefieldtypes = {}
    multikatfieldtypes = {}
    attributemethods = {}
    conditionalfields = {}
    pathdefinitions = {}
    attributehandler = None
    primarykey = %(primarykey)s
    otherkeys = %(keys)s
    querySQL  = SimpleSQL(table = table, fields = fields)
    updateSQL = querySQL

class %(lname)sList(Container):
    resultClass = %(lname)s
    querySQL = resultClass.querySQL
"""    

header = \
"""# coding: latin-1
\"\"\"
AUTOMATISCH GENERIERTE DATEI! NICHT EDITIEREN!

Automatisch generierte Anwendungsschnittstelle für die EB Klientenverwaltung.

Generiert von genEb.py

\"\"\"

from ebkus.db.dbapp import DBObjekt, Container, DBAppError
from ebkus.db.sql import SQLError, SQL, SimpleSQL, \\
                opendb, closedb, getDBHandle
"""


IND = 23   # einrücken von Feldstrings
MAXL = 57  # Länge von Feldstrings ohne Einrücken

def formatFields(str, maxlen, indent):
    if len(str) <= maxlen:
        return str
    result = ''
    while 1:
        index = str.rfind(', ', 0, maxlen)
        index = index + 2
        result = result + str[0:index] + '\\\n' + ' '*indent
        str = str[index:]
        if len(str) < maxlen:
            return result  + str
            
            
    
def generateForeignKeyInfo(schemadata_tables):
    ifkeys = []
    fkeys = []
    mkeys = []
    for t in schemadata_tables:
        for f in t.fields:
            if f.verwtyp == 'f': # sei akte_id der Klasse Fall, inverse ist faelle für Akte
                klass = f.table.Tables[f.ftable].classname
                ifkeys.append((klass, f.inverse, t.classname, f.fieldname))
                fkeys.append((t.classname, f.fieldname, klass, repr(f.inverse)))
            if f.verwtyp == 'k':
                klass = 'Code'
                fkeys.append((t.classname, f.fieldname, klass, None))
            if f.verwtyp == 'm':
                klass = 'Code'
                mkeys.append((t.classname, f.fieldname, klass))
    return fkeys, ifkeys, mkeys
    
def generate_ebapi(filename):
    from ebkus.gen.schemagen import get_schema_info
    from ebkus.gen.schemadata import schemainfo
    file = open(filename, 'wb')
    #  print tables
    file.write(header)
    schemadata_tables = get_schema_info(schemainfo)
    for t in schemadata_tables:
        table, lname = t.tablename, t.classname
        dbfieldsl = [f.fieldname for f in t.fields]
        dbfieldlengths = [f.max_len for f in t.fields]
        dbfields = formatFields(repr(dbfieldsl), MAXL, IND)
        primarykey = repr(t.primarykey)
        keys =  t.keys
        file.write(template % { 'dbfields' : dbfields,
                                'dbfieldlengths' : dbfieldlengths,
                           'lname' : lname, 'table' : table,
                           'keys' : keys, 'primarykey' : primarykey})
        logging.info('Klassendefinition generiert: %s' % lname)
        
    fkeys, ifkeys, mkeys = generateForeignKeyInfo(schemadata_tables)
    file.write("""
    
# Die folgenden Einträge ermöglichen die automatische Navigation über
# Fremdschlüssel. Wird insbesondere von DBObjekt.__getitem__ verwendet.
#   fall['akte_id__vn'] kann damit automatisch evaluiert werden.
    
""")
    for f in fkeys:
        file.write("%s.foreignfieldtypes['%s'] = (%s, %s)\n" % f)
    file.write("""
    
# Die folgenden Einträge ermöglichen die automatische Navigation über
# inverse Fremdschlüssel. Wird insbesondere von DBObjekt.__getitem__ 
# verwendet.
#   fall['leistungen'] kann damit automatisch evaluiert werden.
    
""")
    for f in ifkeys:
        file.write("%s.inversefieldtypes['%s'] = (%sList, '%s')\n" % f)
    file.write("""
    
# Die folgenden Einträge ermöglichen Mehrfachauswahlfelder.
# In das Feld werden die IDs von Code-Instanzen als Strings
# geschrieben. Beim Aufruf über __getitem__ werden die durch
# Code-Instanzen ersetzt.
    
""")
    for f in mkeys:
        file.write("%s.multikatfieldtypes['%s'] = %sList\n" % f)

    file.close()


if __name__ == '__main__':
    import sys
    sys.path.insert(0, "/home/atms/dev/ebkus/install/ebkus/lib")
    filename = 'ebapigen.py'
    generate_ebapi(filename)
    print '----> ', filename, 'generiert'  
    
    
    
