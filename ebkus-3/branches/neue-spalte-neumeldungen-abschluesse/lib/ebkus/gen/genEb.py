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
import string
import sys
from ebkus.db.sql import opendb, closedb, getDBHandle
from ebkus.gen import schemagen


template = \
"""
#####################################
# %(lname)s  (Tabelle '%(table)s')
#####################################


class %(lname)s(DBObjekt):
  table = '%(table)s'
  fields =  %(dbfields)s
  fieldtypes = {}
  foreignfieldtypes = {}
  inversefieldtypes = {}
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
"""#!/usr/local/bin/python
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
        index = string.rfind(str, ', ', 0, maxlen)
        index = index + 2
        result = result + str[0:index] + '\\\n' + ' '*indent
        str = str[index:]
        if len(str) < maxlen:
            return result  + str
            
            
def getFields(table):
    fs = getDBHandle().listfields(table)
    dbfields = []
    dbfields_prefix = []
    for f in fs:
      # print f
        if f[0] == 'idx1':
            continue
            ## Nicht kompatibel fuer MySQLdb [('feld', 'int(11)',),(..)] und 
            ## MySQL [['feld','tabelle', 'int', 11, ],[..]]
            ##
            ##    if   f[2] in ['int', 'char', 'long', 'string', 'blob', 'mediumblob', 'longblob','varchar']:
        dbfields.append(f[0])
        dbfields_prefix.append("%s.%s" % (table, f[0]))
        #    else:
        #      raise "Unknown database datatype: %s" % f[2]
    return dbfields, dbfields_prefix
    
def getNewTablesPairs():
    """Aus der Datenbank generiert."""
    res = getDBHandle().query("SELECT tabelle, klasse FROM tabelle")
    # print res
    return res
    
    
def generateForeignKeyInfo(schemadata_tables):
    ifkeys = []
    fkeys = []
    for t in schemadata_tables:
        for f in t.fields:
            if f.verwtyp == 'f': # sei akte_id der Klasse Fall, inverse ist faelle für Akte
                klass = f.table.Tables[f.ftable].classname
                ifkeys.append((klass, f.inverse, t.classname, f.fieldname))
                fkeys.append((t.classname, f.fieldname, klass, repr(f.inverse)))
            if f.verwtyp == 'k':
                klass = 'Code'
                fkeys.append((t.classname, f.fieldname, klass, None))
    return fkeys, ifkeys
    
def gen_api(schema_str):
    import StringIO
    file = StringIO.StringIO()
    newtables = getNewTablesPairs()
    tables = newtables
    #  print tables
    file.write(header)
    # hier geht es durcheinander, weil noch nicht einheitlich von schemadata
    # generiert wird.
    schemadata_tables = schemagen.get_schema_info(schema_str)
    tabledict = schemadata_tables[0].Tables
    for elem in tables:
        table, lname = elem
        dbfieldsl, dbfields_prefixl = getFields(table)
        dbfields = formatFields(repr(dbfieldsl), MAXL, IND)
        dbfields_prefix = formatFields(repr(dbfields_prefixl), MAXL, IND)
        if tabledict.has_key(table):
            primarykey = repr(tabledict[table].primarykey)
            keys =  tabledict[table].keys
        else: # alte Tabelle, Heuristik
            primarykey = 'None'
            keys = []
            ##       if 'id' in dbfieldsl:
            ##      primarykey = "'id'"
            ##       else:
            ##      primarykey = 'None'
        file.write(template % { 'dbfields' : dbfields, 'dbfields_prefix' : dbfields_prefix, 
                           'lname' : lname, 'table' : table,
                           'keys' : keys, 'primarykey' : primarykey})
        print 'Klassendefinition generiert: %s' % lname
        
    fkeys, ifkeys = generateForeignKeyInfo(schemadata_tables)
    file.write(
    """
    
    # Die folgenden Einträge ermöglichen die automatische Navigation über
    # Fremdschlüssel. Wird insbesondere von DBObjekt.__getitem__ verwendet.
    #   fall['akte_id__vn'] kann damit automatisch evaluiert werden.
    
    """)
    for f in fkeys:
        file.write("%s.foreignfieldtypes['%s'] = (%s, %s)\n" % f)
    file.write(
    """
    
    # Die folgenden Einträge ermöglichen die automatische Navigation über
    # inverse Fremdschlüssel. Wird insbesondere von DBObjekt.__getitem__ 
    # verwendet.
    #   fall['leistungen'] kann damit automatisch evaluiert werden.
    
    """)
    for f in ifkeys:
        file.write("%s.inversefieldtypes['%s'] = (%sList, '%s')\n" % f)
    return file
    
    
def generate_ebapi(schema_str):
    opendb()
    f = gen_api(schema_str)
    closedb()
    # f ist StringIO Objekt
    return f
    
    
# funktioniert so nicht

## if __name__ == '__main__':
##     filename = 'ebapigen.py'
##     f = generate_ebapi(schemadata.schemainfo)
##     file = open('../app/%s' % filename, 'w')
##     file.write(f.getvalue())
##     f.close()
##     file.close()
##     print '----> ', filename, 'generiert'  
    
    
    
