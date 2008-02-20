# coding: latin-1

KEIN_PROTOKOLL = ('feld', 'tabelle' 'protokoll', 'sessions')
KEIN_PROTOKOLL_VON_SELECT = ('code', 'kategorie')

## Standardimporte
import string
import time
import os
import re
import rotor

from ebkus.db.dbapp import DBObjekt
from ebkus.app.ebapi import cc, EE, Protokoll, ProtokollList, Code, \
     register_get, register_set, Tabelle

from ebkus.app.Request import getRequest
from ebkus.config import config

class ProtokolltabelleVoll(Exception):
    pass

# damit man das Protokoll vor�bergehend ausstellen kann, zB.
# f�er das Initialisieren der Datenbank
_protocol_on = True
def temp_on():
    global _protocol_on
    _protocol_on = True
def temp_off():
    global _protocol_on
    _protocol_on = False
def is_temp_on():
    return _protocol_on
    
# mit diesem sehr merkw�rdigem Hack wird in der Datenbank kodiert
# ob protokolliert werden soll :-)
# diese drei Funktionen, damit der Irrsinn sich hier konzentriert
def on():
    protokoll_code = Code(kat_code='config', code='protocol')
    protokoll_code.update({'name': 'on'})
def off():
    protokoll_code = Code(kat_code='config', code='protocol')
    protokoll_code.update({'name': 'off'})
def is_on():    
    protokoll_code = Code(kat_code='config', code='protocol')
    return protokoll_code['name'] == 'on'

def write_sql_protocol(artdeszugriffs=None, sql=None, username=None, ip=None):
    """Einen Eintrag in die Protokolltabelle vornehmen"""
    if not is_temp_on():
        return
    try:
        temp_off()
        # das darf erst hier stehen sonst kommt es zu Rekursion
        if not is_on():
            return
        req = getRequest()
        if not username:
            if req:
                username = req.user
            else:
                username = 'unbekannt'
        if not ip:
            if req:
                ip = req.ip
            else:
                ip = 'unbekannt'
        if not artdeszugriffs:
            artdeszugriffs = _analyse(sql)
            if not artdeszugriffs:
                return
        zeitstempel = time.strftime("%d.%m.%y %H:%M:%S",
                                    time.localtime(time.time()))
        # Protokolltabelle automatisch archivieren
        # h�ngt ab von dem mit set_protocol_limit gesetzten Wert
        try:
            new_id = Protokoll().getNewId()
        except ProtokolltabelleVoll, e:
            archive_sql_protocol(username)
            new_id = Protokoll().getNewId()
        protokoll = Protokoll()
        protokoll['zeit'] = zeitstempel
        protokoll['artdeszugriffs'] = artdeszugriffs
        protokoll['benutzerkennung'] = username
        protokoll['ipadresse'] = ip
        protokoll.new(new_id)
        protokoll.insert()
    finally:
        temp_on()


def _analyse(sql_string):
    """SQL String f�r Eintrag in die Protokolltabelle aufbereiten
    
    Beruht auf dem alten schrecklichen Code.
    """
    if not sql_string or sql_string.startswith('DROP TABLE'):
        return ''
    # obwohl grausam, habe ich diesen Code erst mal weitgehend so gelassen,
    # weil am Ende eine so sch�ne Tabelle raus kommt :-)
    if sql_string[:6] == 'SELECT':
        art = 'SELECT'
        sqlsttmtlist = string.split(sql_string)
        tabelle = (sqlsttmtlist.index('FROM')) + 1
        spaltenstart = (sqlsttmtlist.index('SELECT')) + 1
        spaltenende = (sqlsttmtlist.index('FROM'))
        spalten = ''
        while ((spaltenstart > 0 ) and (spaltenstart < spaltenende)):
            pat = str(sqlsttmtlist[spaltenstart])
            #pat = re.sub(r'\'', '\\\'', teststring)
            spalten = spalten + " " + pat
            spaltenstart = spaltenstart + 1
        wherestr = ''
        try:
            wherestart = (sqlsttmtlist.index('WHERE')) + 1
        except:
            wherestart = len(sqlsttmtlist)
            wherestr = 'keine'
        whereende = len(sqlsttmtlist)
        while ((wherestart > 0) and (wherestart < whereende)):
            pat = str(sqlsttmtlist[wherestart])
            #pat = re.sub(r'\'', '\\\'', teststring)
            wherestr = wherestr + " " + pat
            wherestart = wherestart + 1
        artdeszugriffs = "SELECT auf Tabelle: %s \n Spalten : %s \n Bedingung: %s" % \
                         (sqlsttmtlist[tabelle], spalten, wherestr)
    elif sql_string[:6] == 'UPDATE':
        art = 'UPDATE'
        sqlsttmtlist = string.split(sql_string)
        tabelle = (sqlsttmtlist.index('UPDATE')) + 1
        spaltenstart = (sqlsttmtlist.index('SET')) + 1
        spaltenende = (sqlsttmtlist.index('WHERE'))
        spalten = ''
        while ((spaltenstart > 0 ) and (spaltenstart < spaltenende)):
            pat = str(sqlsttmtlist[spaltenstart])
            #pat = re.sub(r'\'', '\\\'', teststring)
            spalten = spalten + " " + pat
            spaltenstart = spaltenstart + 1
        wherestr = ''
        wherestart = (sqlsttmtlist.index('WHERE')) + 1
        whereende = len(sqlsttmtlist)
        while ((wherestart > 0) and (wherestart < whereende)):
            pat = str(sqlsttmtlist[wherestart])
            #pat = re.sub(r'\'', '\\\'', teststring)
            wherestr = wherestr + " " + pat
            wherestart = wherestart + 1
        artdeszugriffs = "UPDATE der Tabelle: %s \n Spalte-Wert : %s \n Bedingung: %s" % \
                         (sqlsttmtlist[tabelle], spalten, wherestr)
    elif sql_string[:6] == 'INSERT':
        art = 'INSERT'
        sqlsttmtlist = string.split(sql_string)
        tabelle = (sqlsttmtlist.index('INTO')) + 1
        spaltenstart = (sqlsttmtlist.index('INTO')) + 2
        spaltenende = (sqlsttmtlist.index('VALUES'))
        spalten = ''
        while ((spaltenstart > 0 ) and (spaltenstart < spaltenende)):
            pat = str(sqlsttmtlist[spaltenstart])
            #pat = re.sub(r'\'', '\\\'', teststring)
            spalten = spalten + " " + pat
            spaltenstart = spaltenstart + 1
        wherestr = ''
        wherestart = (sqlsttmtlist.index('VALUES')) + 1
        whereende = len(sqlsttmtlist)
        while ((wherestart > 0) and (wherestart < whereende)):
            pat = str(sqlsttmtlist[wherestart])
            #pat = re.sub(r'\'', '\\\'', teststring)
            wherestr = wherestr + " " + pat
            wherestart = wherestart + 1
        artdeszugriffs = "INSERT in Tabelle: %s \n Spalten : %s \n Werte: %s" % \
                         (sqlsttmtlist[tabelle], spalten, wherestr)
    elif sql_string[:6] == 'DELETE':
        art = 'DELETE'
        sqlsttmtlist = string.split(sql_string)
        tabelle = (sqlsttmtlist.index('FROM')) + 1
        wherestr = ''
        try:
            wherestart = sqlsttmtlist.index('WHERE') + 1
        except:
            wherestart = len(sqlsttmtlist)
            wherestr = 'keine'
            pass
        whereend = len(sqlsttmtlist)
        while ((wherestart > 0) and (wherestart < whereend)):
            pat = str(sqlsttmtlist[wherestart])
            #pat = re.sub(r'\'', '\\\'', teststring)
            wherestr = wherestr + " " + pat
            wherestart = wherestart + 1
        artdeszugriffs = "DELETE in Tabelle: %s \n Bedingung: %s" % \
                         (sqlsttmtlist[tabelle], wherestr)
    else:
        artdeszugriffs = "Zugriff konnte nicht analysiert werden"
    try:
        # inhaltlich irrelevantes etwas stutzen ...
        art = sqlsttmtlist[0] # SELECT, UPDATE, ...
        tab = sqlsttmtlist[tabelle] # Name der Tabelle
        if tab in KEIN_PROTOKOLL:
            artdeszugriffs = ''
        if art in ('SELECT',):
            if tab in KEIN_PROTOKOLL_VON_SELECT:
                artdeszugriffs = ''
    except:
        logging.exception('FF')
        pass
    return artdeszugriffs


def archive_sql_protocol(user):
    """L�scht die Daten aus der Protokolltabelle und schreibt
    sie in eine Archivdatei.
    Code weitestgehend von MSG �bernommen."""
    tmp_yek = "2001.12.31" # ?? :-)
    # diesen abschnitt. hier wird zu erst in eine datei archiviert, dann gel�scht
    # zeit generieren und fileobjekt erstellen.
    local_time_insec = time.time()
    local_time_tupel = time.localtime(local_time_insec)
    zeitstempel = time.strftime("%d%m%y%H%M%S", local_time_tupel)
    zeitstempel2 =time.strftime("%d.%m.%y um %H:%M:%S", local_time_tupel)
    pfad = os.path.join(config.PROTOCOL_DIR, zeitstempel + ".txt")
    #if os.exists(PROTOCOL_DIR) != true:
    #mkdir(PROTOCOL_DIR)
    fdatei = open(pfad, "wb")
    # jede zeile aus der protokolltabelle wird in die datei geschrieben
    protokolleintraege = ProtokollList(where = '', order='nr')
    rot = rotor.newrotor(tmp_yek)
    from ebkus.app_surface.protokoll_templates import datei_t
    for p in protokolleintraege:
        fdatei.write(rot.encryptmore(datei_t % p))
        fdatei.write(rot.encryptmore('<br>'))
    fdatei.write(rot.encryptmore("""<br>****************************<br>
Die Protokolltabellen wurden am %s von %s geloescht
und in die Datei %s archiviert.
<br>****************************<br>""" % (zeitstempel2, user, pfad)))
    fdatei.close()
    # Maxist protokolltabelle wird gesetzt
    tab = Tabelle(tabelle='protokoll')
    tab.update({'maxist': 0})
    # protokolltabelle wird gel�scht
    protokolleintraege2 = ProtokollList(where = '')
    protokolleintraege2.deleteall()


def set_protocol_limit(limit):
    """Setzte die maximale Anzahl der Eintr�ge in die Protokolltabelle.
    Wenn diese Anzal �berschritten wird, wird automatisch archiviert.
    """
    limit = int(limit)
    if limit < 100000 or limit > 100000000:
        raise EE('F�llgrenze muss zwischen 100.000 und 100.000.000 liegen')
    register_set('protokoll_fuellgrenze', limit)

def get_protocol_limit():
    """Holt die maximale Anzahl der Eintr�ge in die Protokolltabelle.
    Wenn diese Anzal �berschritten wird, wird automatisch archiviert.
    """
    return register_get('protokoll_fuellgrenze', default=200000)

def _getNewId(self):
    """�berschreibt die Standardmethode, um neue Werte f�r
    Schl�sselfelder zu erzeugen, f�r die Protokolltabelle.
    """
    newid = DBObjekt.getNewId(self)
    if newid > get_protocol_limit():
        raise ProtokolltabelleVoll(
            "Die Protokolltabelle hat den gesetzten F�llstand erreicht: %s" % max)
    return newid

Protokoll.getNewId = _getNewId
