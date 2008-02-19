#!/usr/local/bin/python
# coding: latin-1

import re
from ebkus.db import sql

##*************************************************************************
## schreiben der Strassen in Tabelle strassenkat
##
##*************************************************************************

def write_strassen_to_db(str_nr, str_name, hsnr, bez, plz, planungsr):
    sql_query = "INSERT INTO strassenkat (str_nummer,str_name,hausnr,bezirk,plz,plraum) VALUES (" \
                + str_nr + "," + str_name + "," + hsnr + "," + bez + "," + plz + "," + planungsr + ")"
    #print sql_query
    sql.execute(sql_query)
    
def del_old_strkat():
    #print "Loesche alten Strassenkatalog"
    try:
        sql_query = "DELETE FROM strassenkat"
        sql.execute(sql_query)
        #print "Strassenkatalog geloescht"
    except:
        #print "Konnte alten Strassenkatalog nicht entfernen!"
        pass
    
    
def read_strkat(file_name, opendb=False):
    dyn_pos = 0
    gesamt_pos = 0
    if opendb:
        sql.opendb()
    line = None
    neuliste = []
    if file_name.lower().endswith('.gz'):
        import gzip
        f = gzip.GzipFile(file_name)
    else:
        f = open(file_name)
    del_old_strkat()
    while line != '':
        line = f.readline()
        line = re.sub(r'\'', '\\\'', line)
        line = re.sub(r'\"', '\'', line)
        if line != '':
            neuliste = schreibe_daten(line)
            str_nr = neuliste[0]
            str_name = neuliste[1]
            hsnr = neuliste[2]
            if hsnr == '':
                hsnr = '\'---\''
            bez = neuliste[4]
            plz = neuliste[9]
            planungsr = neuliste[20]
            write_strassen_to_db(str_nr, str_name, hsnr, bez, plz, planungsr)
            dyn_pos = dyn_pos + 1
            if dyn_pos == 10000:
                gesamt_pos = gesamt_pos + 10000
                print "      Status: " + str(gesamt_pos) + " von ca. 385000 Datensaetzen fertig importiert."
                dyn_pos = 0
    #print "Strassenkatalog wurde erfolgreich importiert."
    ##*************************************************************************
    ## Anlegen eines Indexes für die schnellere Suche im Strassenkat
    ## Index wird über 10 Zeichen des Strassennamens angelegt. Wunsch von Huber.
    ## brehmea 15.08.2002
    ##*************************************************************************
    #print "Lege Index fuer Strassenkatalog an."
    sql_query = "ALTER TABLE strassenkat ADD INDEX (str_name(10))"
    sql.execute(sql_query)
    #print "Index fuer Strassenkatalog wurde erfolgreich angelegt."
    f.close()
    if opendb:
        sql.closedb()
    
    ##*************************************************************************
    ## Schreiben der ausgelesenen Zeile des Strassenkataloges in eine neue
    ## Liste ohne Trennzeichen
    ##
    ## hellers 19.10.2001
    ##*************************************************************************
    
def schreibe_daten(line):
    neuliste = []
    neuliste = line.split(';')
    return neuliste
    


if __name__ == '__main__':
    if len(sys.argv) > 1:
        strkat = sys.argv[1]
    else:
        # default
        strkat = 'strkat.txt'
    import init
    read_strkat(strkat, opendb=True)
