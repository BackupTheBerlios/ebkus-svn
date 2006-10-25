#!/usr/local/bin/python
# coding: latin-1

"""
Modul zur Erzeugung des neuen Schemas der EB Klientenverwaltung in der Datenbank.

Der Aufruf erfolgt über
           init_new_db()
bzw. aus einem anderen Modul
           import schemagen
           schemagen.init_new_db()

Die Datenbank, auf die operiert wird, ergibt sich durch aus dem Modul sql
importierten Funktionen.

Bei wiederholtem Aufruf von init_new_db() werden die bei früheren Durchläufen
erzeugten Tabellen sowie evt. bereits darin befindliche Daten gelöscht.

Außerdem werden die Metatabellen 'tabelle' und 'feld' partiell gefüllt,
mit einem Datensatz für jede Tabelle und jedes Feld.

Die Daten zur Erzeugung des Schemas stehen in schemadata.py, das hier importiert
wird.

Funktionsweise:
Aus Daten in schemadata.py werden eine Menge von Instanzen der hier definierten
Klassen 'Table' und 'Field' erzeugt, die dann zu Generierung des Schemas
(Methode Table.sql_create()) und zum Auffüllen der Tabellen 'tabelle' und 'feld'
(Methode sql_insert()) verwendet werden.
"""

import string
import re
from ebkus.db.sql import opendb, closedb, getDBHandle


class Table:
    Tables = {}
    #tname, fn1/fn3.fn3/fn5.fn6, lname, classname
    def __init__(self, list):
        self.fields = []
        list[len(list):] = ['']*(4-len(list))
        self.tablename, keys, self.lname, self.classname = list
        if not self.classname:
            self.classname = self.lname
        self.primarykey = None
        self.keys = []
        if keys:
            keys = string.split(keys, '/')
            for i in range(len(keys)):
                keys[i] = tuple(string.split(keys[i], '.'))
                #if len(keys[i]) == 1: keys[i] = keys[i][0]
            self.keys = keys
        self.flag = 0
        Table.Tables[self.tablename] = self
        
        
    def sql_create(self):
        return "CREATE TABLE %s (\n  %s\n)\n" % (self.tablename,
                string.join(
                  map(lambda x: "%s %s" % (x.fieldname, x.dbtype),
                      self.fields),
                  ',\n  '))
        
    def sql_insert(self, id):
        self.id = id
        return "INSERT INTO tabelle values \
              (%d,'%s','%s','%s',%d,NULL)" % \
              (self.id, self.tablename, self.lname, self.classname, self.flag)
        
    def __str__(self):
        return "Tabelle: %s [%s %s %s]\n  %s" % \
               (self.tablename, self.keys, self.lname, self.classname,
                string.join(map(str, self.fields), '\n  '))
        
    def __repr__(self):
        return self.tablename
        
class Field:
    Fields = {}
    #fname, fdbtype, lname,
    #vtyp =  {s,f,k,b,p}, { , tablename, kat_code, kat_code, }, inversename
    def __init__(self, table, list):
        self.table = table
        list[len(list):] = ['']*(6-len(list))
        self.fieldname, self.dbtype, self.lname, self.verwtyp, self.ref, self.inverse = list[:6]
        if not self.verwtyp: self.verwtyp = 'p'
        if len(self.verwtyp) != 1 or self.verwtyp not in 'sfkbp':
            raise 'Error in field definition'
        if self.verwtyp == 's':  # Schluesselfeld
            self.table.primarykey = self.fieldname
        self.kat_code = ''
        self.ftable = ''
        self.flag = 0
        if self.verwtyp in 'fkb' and not self.ref:
            raise 'Error in field definition'
        else:
            if self.verwtyp in 'kb':
                self.kat_code = self.ref
                if self.verwtyp in 'k':
                    self.ftable = 'code'   # kodierte Felder sind Fremdschlüssel nach code
            if  self.verwtyp in 'f':
                self.ftable = self.ref
        Field.Fields[(self.table.tablename, self.fieldname)] = self
        
    def sql_insert(self, id):
        self.id = id
        return "INSERT INTO feld values \
              (%d, %d, '%s','%s',NULL,'%s',NULL,NULL,NULL,NULL,NULL,NULL,%d,NULL)" % \
              (self.id, self.table.id, self.fieldname, self.lname,
               self.dbtype, 0)
        
    def __str__(self):
        return "%s, %s, %s, %s, %s" % \
               (self.fieldname, self.dbtype, self.lname, self.verwtyp, self.ref)
        
    def __repr__(self):
        return self.__str__()
        
        
        
def get_schema_info(str):
    newtables = []
    lines  = string.split(str, '\n')
    newtable = 1
    for lstr in lines:
        lstr = string.strip(lstr)
        if not lstr:
            newtable = 1
            table = None
            continue
        l = re.split('[\s]*,[\s]*', lstr)
        try:
            if newtable:
                if l[0] == 'table':
                    table = Table(l[1:])
                    newtables.append(table)
                    newtable = 0
                else:
                    raise 'Error in schemadata'
            else:
                table.fields.append(Field(table,l))
        except OverflowError:
            print '******ERROR***:  ' + lstr
            raise 'Error in schemadata'
    return newtables
    
    
def delete_tables_in_db(test = 0):
    """Löscht alle Tabellen."""
    db = getDBHandle()
    #print db
    alltables = db.listtables()
    #print alltables
    for t in alltables:
        #print 'Lösche ', t
        if not test:
            # protokollieren abgestellt, da es um die Einrichtung
            # der Datenbank selber geht
            db.query("DROP TABLE %s" % t)
        else:
            print "DROP TABLE %s" % t
            pass
        
        
def create_schema_in_db(newtables, test = 0):
    db = getDBHandle()
    #print db
    for t in newtables:
        if not test:
            # protokollieren abgestellt, da es um die Einrichtung
            # der Datenbank selber geht
            db.query(t.sql_create())
        else:
            print t.sql_create()
        
def insert_tables_fields_in_db(newtables, test = 0):
    db = getDBHandle()
    tid = 1
    fid = 1
    for t in newtables:
        sql = t.sql_insert(tid)
        if not test:
            # protokollieren abgestellt, da es um die Einrichtung
            # der Datenbank selber geht
            db.query(sql)
        else:
            print sql
        tid = tid + 1
        for f in t.fields:
            sql = f.sql_insert(fid)
            if not test:
                # protokollieren abgestellt, da es um die Einrichtung
                # der Datenbank selber geht
                db.query(sql)
            else:
                print sql
            fid = fid + 1
            
            
def init_new_db(schema_str, test):
    import ebkus.app.protocol
    try:
        ebkus.app.protocol.temp_off()
        newtables = get_schema_info(schema_str)
        delete_tables_in_db(test)
        create_schema_in_db(newtables, test)
        insert_tables_fields_in_db(newtables, test)
    finally:
        ebkus.app.protocol.temp_on()
    
    
def generate_schema(schema_str, test):
    opendb()
    init_new_db(schema_str, test)
    closedb()
    
if __name__ == '__main__':
  # Falls test = 1, werden real keine Einträge in die Datenbank gemacht
    test = 1
    
    if test:
        print "***************************************"
        print "TEST LAUF"
        print "***************************************"
        print
    else:
        print "***************************************"
        print "PRODUKTIV LAUF"
        print "***************************************"
        print
        
        # Um auf die Liste der alten Tabellen zuzugreifen
        
        # Hier stehen die Daten für das neue Schema
    import ebkus.gen.genEb
    import ebkus.gen.schemadata
    schema_str = schemadata.schemainfo
    generate_schema(schema_str, test)
    
    
