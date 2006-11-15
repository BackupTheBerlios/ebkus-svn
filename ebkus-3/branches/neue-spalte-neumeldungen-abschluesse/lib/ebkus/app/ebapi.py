# coding: latin-1
"""Anwendungsschnittstelle für die EB Klientenverwaltung.

Die eigentlichen Objektklassen liegen im automatisch generierten Modul
ebapigen.py und werden hier nur importiert. Weiter manuelle
Ergänzungen, Subklassendefinitionen, Methodendefinitionen, etc. können
in diesem Modul abgelegt werden.

"""

import sys, string, math, os
import datetime
from ebkus.app.ebapigen import *
from ebkus.db import dbapp, sql
from ebkus.config import config


####################
# utility Funktionen
####################

def nfc(code_nr):
    try:
        name=Code(code_nr)['name']
    except:
        return ''
        pass
    return name
    
def is_binary(mimecode):
    if mimecode == cc('mimetyp','txt')or mimecode == cc('mimetyp','asc')or mimecode == cc('mimetyp','html')or mimecode == cc('mimetyp','htm')or mimecode == cc('mimetyp','ps')or mimecode == cc('mimetyp','rtf')or mimecode == cc('mimetyp','rtx'):
        return 0
    else:
        return 1
        
def ist_gruppen_mitarbeiter(gruppen_id,mit_id):
    gruppex = Gruppe(int(gruppen_id))
    mitarbeitergruppe = gruppex['mitarbeiter']
    is_gr_mit = 0
    for mg in mitarbeitergruppe:
        if int(mit_id) == int(mg['mit_id']):
            is_gr_mit = 1
    return is_gr_mit
    
def getDBSite():
    return config.SITE
    
def cc(kat_code, code):
    """Liefert die code id für eine kat_code/code Kombination.
    Bsp:  cc('stzei', 'B') liefert die Zahl 230"""
    try: id = Code(kat_code = kat_code, code =  code)['id']
    except:
        raise dbapp.DBAppError("Code '%s' für Kategorie '%s' existiert nicht" % (code, kat_code))
    return id
def cn(kat_code, name):
    """Liefert die code id für eine kat_code/codename Kombination.
    Bsp:  cn('stzei', 'EFB-Wienerstr.') liefert die Zahl 230"""
    try: id = Code(kat_code = kat_code, name =  name)['id']
    except:
        raise dbapp.DBAppError("Code '%s' für Kategorie '%s' existiert nicht" % (name, kat_code))
    return id
    
    
class Date(object):
    def __init__(self, year = None, month = None, day = None):
        """No error checking. Use the check method."""
        if year is month is day is None: # assume today
            import time
            year, month, day = time.localtime(time.time())[:3]
        if month is None: month = 1
        if day is None: day = 1
        self.year, self.month, self.day = year, month, day
        
    def to_py_date(self):
        """Throws an exception if its not a correct date."""
        return datetime.date(self.year, self.month, self.day)

    def is_zero(self):
        return self.year == self.month == self.day == 0

    def totuple(self):
        return self.year, self.month, self.day
        
    def __getitem__(self, key):
        if key == 'day': return self.day
        elif key == 'month': return self.month
        elif key == 'year': return self.year
        else:
            raise KeyError, key
            
    def diff(self, other):
        """Unterschied in Monaten, positiv und negativ:
        other - self
        Tage werden nicht berücksichtigt.
        """
        diff = other.year*12 + other.month - (self.year*12 + self.month)
        return diff
        
    def add_month(self, months):
        """Liefert ein neues Datum, indem months Monate
        addiert werden. Tage werden nicht berücksichtigt,
        aber wenn nötig korrigiert, d.h. Date(2000, 7, 31).add_month(2)
        ergibte Date(2000, 9, 30).
        """
        d_years = months / 12
        d_months = months % 12
        year = self.year + d_years
        month = self.month + d_months
        day = self.day
        if month > 12:
            month -= 12
            year += 1
        elif month < 1:
            month += 12
            year -= 1
        new_date = Date(year, month, day)
        if not new_date.check():
            # liegts am zu grossen Tag für den neuen Monat?
            if month == 2 and day > 28:
                new_date = Date(year, 2, 28)
            elif day > 30:
                new_date = Date(year, month, 30)
            assert new_date.check(), "Addition von Monaten misslungen"
        return new_date

    def check(self):
        """Liefert true, falls Datum (0,0,0) ist, oder ein korrektes Datum.
        TODO: ACHTUNG: ZWEISTELLIGE DATEN SIND ZULÄSSIG!
        Folgende Jahreszahlen sind gültig:
             -   -1: Fehler
           0 -   30: 2000 - 2030
          31 -   69: Fehler
          70 -   99: 1970 - 1999
         100 - 1969: Fehler
        1970 - 2030: 1970 - 2030
        2031 -     : Fehler
        """

        y = self.year
        m = self.month
        d = self.day
        if y == m == d == 0:
            return True
        if 0 <= y <= 30: # zwei-stellige Jahresangabe
            y += 2000
        elif 30 < y < 100:
            y += 1900
        self.year = y
        if y < 1970 or y > 2030:
            return False
        try:
            self.to_py_date()
            return True
        except:
            return False

    def __cmp__(self, other):
        """Works only if dates have been checked true. If a date is all zero,
        it compares greater than any other date."""
        if not isinstance(other, Date):
            raise TypeError("Kein Date-Objekt: %s" % repr(other))
        try:
            return cmp(self.to_py_date(), other.to_py_date())
        except:
            # mindestens ein Argument ist 0,0,0
            if self.is_zero():
                if other.is_zero():
                    return 0
                return 1
            else:
                return -1
            
    def __str__(self):
        return "%02d.%02d.%04d" % (self.day, self.month, self.year)
    __repr__ = __str__
    
today = Date

#print today()


#########################################################
# getDate, setDate
#
# Achtung!
# Beruht auf der Konvention, daß Datum immer mit Feldnamen
# angegeben ist, die wie folgt aufgebaut sind:
#   <key>y   (bgy)
#   <key>m   (bgm)
#   <key>d   (bgd)
##########################################################

def getDate(self, key):
    y,m,d = key + 'y', key + 'm', key + 'd'
    return Date(self[y], self[m], self[d])
    
def setDate(self, key, date):
    y,m,d = key + 'y', key + 'm', key + 'd'
    self[y], self[m], self[d] = date.totuple()
    
dbapp.DBObjekt.getDate = getDate
dbapp.DBObjekt.setDate = setDate


def getQuartal(monat):
    """Gibt das Quartal für einen bestimmten Monat aus."""
    if int(monat) > 0 and int(monat) < 13:
        q = ((int(monat) - 1) / 3) + 1
        return int(q)
    else:
        raise EE("Keine Monatszahl zwischen 1 und 12")
        
        
def getNewId(self):
    """Standardmethode, um neue Werte für Schlüsselfelder zu erzeugen.
    
    Verwendet die Tabelle tabid (Klasse TabellenID), um eine neue id zu
    generieren abhängig von der Datenbankinstallation, die durch
    die Datenbanksite definiert ist. Die Datenbankinstallation ist in
    der Konfiguration unter dem Namen config.SITE definiert und kann mit der
    Funktion getDBSite() ermittelt werden.
    
    Mit der Zeile
    
         DBObjekt.getNewId = getNewId
    
    wird diese Funktion als Methode der Klasse DBObjekt installiert und
    damit auf alle Unterklassen von DBObjekt, die in 'ebapigen'
    definiert werden, vererbt.
    
    Da die 'new' Methode von DBObjekt getNewId verwendet, kann z.B. eine
    neuer Mitarbeiter wie folgt erzeugt werden:
    
           m = Mitarbeiter()
           m.new()
           m['vn'] = 'Tom'
           m['na'] = 'Friedrich'
           m.insert()
    
    """
    
    if not self.primarykey:
        raise dbapp.DBAppError("Cannot getNewId without primarykey")
        
    tid = TabellenID(table_name = self.table, dbsite = cc('dbsite',  getDBSite()))
    maxist = tid['maxist']
    max = tid['maxid']
    min = tid['minid']
    if maxist:
        newid = maxist + 1
    else:
        newid = 1
    if newid > max:
        raise dbapp.DBAppError("No more ids availabe for table '%s'" % self.table)
    tid.update({'maxist' : newid})
    return newid
    
dbapp.DBObjekt.getNewId = getNewId


def getNewFallnummer(stz_code, jahr):
    """Neue Fallnummer erzeugen."""
    jahresfallliste = FallList(
      where = "bgy = %s and fn like '%%%s%%'" % (jahr, stz_code))
    return "%s-%s%s" % (len(jahresfallliste) + 1, jahr, stz_code)
    
def getNewGruppennummer(stz_code):
    """Neue Gruppennummer erzeugen."""
    jahresgruppenl = GruppeList(where = 'bgy = %(year)d' % today() +
             " and gn like '%%%s%%'" % stz_code)
    
    return str(len(jahresgruppenl) + 1) + '-' + str(today().year) + stz_code
    
    
    ##############################
    # Berechnete Felder für Akte
    ##############################
    
    ##*************************************************************************
    ##
    ##def _wiederaufnehmbar(self, key):
    ##  letzter_fall = self['letzter_fall']
    ##  if letzter_fall and letzter_fall['zday'] != 0:
    ##    zdazeit_in_monaten = letzter_fall['zday']*12 + letzter_fall['zdam']
    ##    heute_in_monaten =   today().year*12 + today().month
    ##    wiederaufnehmbar =  (heute_in_monaten - zdazeit_in_monaten) > 0
    ##  else: wiederaufnehmbar = 0
    ##  self._cache_field('wiederaufnehmbar', wiederaufnehmbar)
    ##  return wiederaufnehmbar
    ##
    ## Bisher logisch falsch.
    ## Korrektur
    ## Datum: 22.11.2001 msg systems ag mastaleckT
    ## Schaltjahre und unterschiedliche Monatslängen müssen nicht berücksichtigt
    ## werden, da eine derartige Genauigkeit hier nicht notwendig ist.
    ##*************************************************************************
    
def _wiederaufnehmbar(self, key):
    letzter_fall = self['letzter_fall']
    if letzter_fall and letzter_fall['zday'] != 0:
        zdazeit_in_tagen = letzter_fall['zday']*365 + letzter_fall['zdam']*30 + letzter_fall['zdad']
        heute_in_tagen = today().year*365 + today().month*30 + today().day
        wiederaufnehmbar = (heute_in_tagen - zdazeit_in_tagen) > 30
    else: wiederaufnehmbar = 0
    #self.data['wiederaufnehmbar'] = wiederaufnehmbar # data cache
    self._cache_field('wiederaufnehmbar', wiederaufnehmbar)
    return wiederaufnehmbar
    
def _letzter_fall(self, key):
    faelle = self['faelle']
    if faelle:
        faelle.sort('bgy', 'bgm', 'bgd')
        letzter_fall = faelle[-1]
    else:
        letzter_fall = None
        #self.data['letzter_fall'] = letzter_fall # data cache
    self._cache_field('letzter_fall', letzter_fall)
    return letzter_fall
    
    
def _aktueller_fall(self, key):
    letzter_fall = self['letzter_fall']
    aktueller_fall = None
    if letzter_fall:
        if letzter_fall['zday'] == 0:
            aktueller_fall = letzter_fall
            #self.data['aktueller_fall'] = aktueller_fall # data cache
    self._cache_field('aktueller_fall', aktueller_fall)
    return aktueller_fall
    
def _aktuell_akte(self, key):
    res = not self['aktueller_fall'] is None
    #self.data['aktuell'] = res # data cache
    self._cache_field('aktuell', res)
    return res
    
def _str_inner(self, key):
    if int(self['lage']) == Code(cc('lage', '0'))['id']:
      # in Berlin
        return self['str']
    else:
        return ''
        
def _str_ausser(self, key):
    if int(self['lage']) == Code(cc('lage', '1'))['id']:
      # ausserhalb Berlins
        return self['str']
    else:
        return ''
        
Akte.attributemethods['wiederaufnehmbar'] = _wiederaufnehmbar
Akte.attributemethods['letzter_fall'] = _letzter_fall
Akte.attributemethods['aktueller_fall'] = _aktueller_fall
Akte.attributemethods['aktuell'] = _aktuell_akte
Akte.attributemethods['str_inner'] = _str_inner
Akte.attributemethods['str_ausser'] = _str_ausser

Bezugsperson.attributemethods['str_inner'] = _str_inner
Bezugsperson.attributemethods['str_ausser'] = _str_ausser

############################
# Berechnete Felder für Fall
############################

def _aktuell_fall(self, key):
    return self['zday'] == 0
    
def _zustaendig_fall(self, key):
    found = 0
    for z in self['zustaendigkeiten']:
        if z['ed'] == 0:
            found = 1
            break
    if found: res =  z
    else: res =  None
    self._cache_field('zustaendig', res)
    return res
    
def _zuletzt_zustaendig_fall(self, key):
    zs = self['zustaendigkeiten']
    zs.sort('bgy', 'bgm', 'bgd')
    res = zs[0]
    self._cache_field('zuletzt_zustaendig', res)
    return res
    
Fall.attributemethods['aktuell'] = _aktuell_fall
Fall.attributemethods['zustaendig'] = _zustaendig_fall
Fall.attributemethods['zuletzt_zustaendig'] = _zuletzt_zustaendig_fall


############################
# Pfaddefinitionen
############################


Akte.pathdefinitions = {
  'akte': 'self'
}
Anmeldung.pathdefinitions = {
  'akte': 'fall_id__akte'
}

Leistung.pathdefinitions = {
  'akte': 'fall_id__akte'
}
Zustaendigkeit.pathdefinitions = {
  'akte': 'fall_id__akte'
}
Fachstatistik.pathdefinitions = {
  'akte': 'fall_id__akte'
}
Jugendhilfestatistik.pathdefinitions = {
  'akte': 'fall_id__akte'
}

Dokument.pathdefinitions = {
  'akte': 'fall_id__akte'
}

Gruppe.pathdefinitions = {
  'gruppe': 'self'
}

MitarbeiterGruppe.pathdefinitions = {
  'gruppe': 'gruppe_id__gruppe'
}

Gruppendokument.pathdefinitions = {
  "gruppe": "gruppe_id__gruppe"
}

FallGruppe.pathdefinitions = {
  'gruppe': 'gruppe_id__gruppe', 'akte': 'fall_id__akte'
}

BezugspersonGruppe.pathdefinitions = {
  'gruppe': 'gruppe_id__gruppe', 'akte': 'bezugsp_id__akte'
}

def akte_undo_cached_fields(self):
    """Zieht alle gecachten Feldwerte zurück, aus allen Objekten,
    die mit einer Akte zusammenhängen. Nach jedem insert oder update
    aufzurufen, damit keine falschen gecachten Werte auftreten."""
    
    for f in self['faelle']:
        for l in f['leistungen']: l.undo_cached_fields()
        for z in f['zustaendigkeiten']: z.undo_cached_fields()
        for a in f['anmeldung']: a.undo_cached_fields()
        for fs in f['fachstatistiken']: fs.undo_cached_fields()
        for jgh in f['jgh_statistiken']: jgh.undo_cached_fields()
        for d in f['dokumente']: d.undo_cached_fields()
        for g in f['gruppen']: g.undo_cached_fields()
        f.undo_cached_fields()
    for b in self['bezugspersonen']:
        for gr in b['gruppen']: gr.undo_cached_fields()
        b.undo_cached_fields()
    for e in self['einrichtungen']: e.undo_cached_fields()
    self.undo_cached_fields()
    
Akte.akte_undo_cached_fields = akte_undo_cached_fields

def gruppe_undo_cached_fields(self):
    """Zieht alle gecachten Feldwerte zurück, aus allen Objekten,
    die mit einer Gruppe zusammenhängen. Nach jedem insert oder update
    aufzurufen, damit keine falschen gecachten Werte auftreten."""
    
    for m in self['mitarbeiter']: m.undo_cached_fields()
    for b in self['bezugspersonen']: b.undo_cached_fields()
    for f in self['faelle']: f.undo_cached_fields()
    for d in self['gruppendokumente']: d.undo_cached_fields()
    self.undo_cached_fields()
    
Gruppe.gruppe_undo_cached_fields = gruppe_undo_cached_fields

## Allgemein Stringüberrüfung
## Datumsüberprüfung
## Codeüberprüfung
## Foreignkeyüberprüfung


#############################################################################
##
## Allgemeines für die folgenen Prüffunktionen (check_*)
## =====================================================

## 1. und 2. Argument ist eine dictionary und ein key, wodurch der
## zu prüfende Wert definiert ist (in unserem Beispiel die form).

## Der Wert kann immer (muß aber nicht) ein String sein, der je nach
## Prüffunktion umgewandelt wird. Falls die Umwandlung mißlingt, wird
## eine Exception geworfen.

## Falls ein Fehler auftritt, wird eine EBUpdateError Exception geworfen mit
## dem errorstring als Argument.

## Falls das default Argument belegt ist (d.h. nicht None ist), wird es
## zurückgegeben falls
## - die dictionary keinen Eintrag unter key hat
## - ein Eintrag existiert, dieser aber None oder '' ist

## Die default Werte werden *nicht* weiter überprüft.

## Falls kein default Wert angegeben ist (default = None), führt das Fehlen
## eines gültigen Wertes zu einem Fehler.
##
## Gültige Werte:
##  check_str_not_empty: ein nicht-leerer String
##  check_int_not_empty: ein Integer, kann auch 0 sein
##  check_fk: eine id, für die ein Objekt der entsprechenden Klasse existiert
##  check_code: ein code, für das ein Code Objekt der entsprechenden Kategorie
##              existiert
##  check_date: ein gültiges Datum zwischen 1980 und today()
##              falls maybezero true ist, ist auch (0,0,0) zulässig
##              falls maybefuture true ist, kann das Datum in der Zukunft liegen
##                (bis 2030)
##              falls nodayallowed true ist, kann der Tag weggelassen werden (d=None)
##                Er wird dann auf 1 gesetzt.
##
#############################################################################

# Hilfsfunktion, damit das default Argument auch ein Objekt sein kann,
# aus dem der Wert geholt wird
def k_or_val(key, default):
    try: val = default[key]
    except: val = default
    return val
    
    # Garantiert einen nicht-leeren String
def check_str_not_empty(dict, key, errorstring, default = None):
    val = dict.get(key)
    if val is None or val == '':
        if not default is None: return k_or_val(key, default)
    if not val or type(val) != type(''): raise EE(errorstring)
    return val
    
    
    ##****************************************************************
    ## Hsnr und Plz aus Tabelle Strassenkatalog auslesen
    ##
    ## HeS 25.10.2001
    ## ABR 31.12.2002
    ##****************************************************************
    
def read_hsnr(stra, plz):
    res = []
    res.append("<br>")
    
    for el in plz:
        res.append("<br><b>Plz. " +  str(el[0]) + " : </b><br>")
        sql_query = "SELECT DISTINCT hausnr FROM strassenkat WHERE str_name = '%s' and plz = '%s'" % (stra,str(el[0]))
        hsnr = sql.execute(sql_query)
        n=0
        g=0
        for el in hsnr:
            if n == 11:
                res.append("<br>")
                n = 0
            res.append(str(el[0]))
            if g != (len(hsnr)-1):
                res.append(", ")
            n = n + 1
            g = g + 1
        res.append("<br>")
    return string.join(res, '')
    
    
def read_plz(stra):
    sql_query = "SELECT DISTINCT plz FROM strassenkat WHERE str_name = '%s'" % stra
    Plz = sql.execute(sql_query)
    return Plz
    ##****************************************************************
    ## Check ob Strasse mit Hsnr und Plz im Strassenkatalog vorhanden
    ##
    ## HeS 25.10.2001
    ## ABR 31.12.2002
    ##****************************************************************
def check_strasse(dict, key1, key2, key3):
    stra = dict.get(key1)
    if dict.get(key2) == '':
        hsnr = '"---"'
    else:
        hsnr = dict.get(key2)
    if dict.get(key3) == '':
        Plz = '"00000"'
    else:
        Plz = dict.get(key3)
        
    strasse = StrassenkatalogList(where = 'str_name = "%s"' % stra
                           + 'and hausnr = "%s"' % hsnr + ' and plz = %s ' % Plz)
    if len(strasse) == 0:
        plz_liste = read_plz(stra)
        hsnr_liste = read_hsnr(stra, plz_liste)
        errorstring = "Angabe zur Strasse <b>(" + str(stra) + ")</b> nicht korrekt: <br> Es sind folgende Postleitzahlen mit den dazu genannten Hausnummern verf&uuml;gbar:  " +  str(hsnr_liste)
        raise  EE(errorstring)
    else:
        return stra
        
        ##****************************************************************
        ## Planungsraum zuweisen
        ##
        ## HeS 29.10.2001
        ##****************************************************************
        
def plraum_zuweisen(dict, key1, key2, key3, errorstring):
    stra = dict.get(key1)
    if dict.get(key2) == '':
        hsnr = '"---"'
    else:
        hsnr = dict.get(key2)
    Plz = dict.get(key3)
    
    strasse = StrassenkatalogList(where = 'str_name = "%s"' % stra
                           + ' and hausnr = "%s" ' % hsnr + ' and plz = %s ' % Plz)
    
    if len(strasse) == 0:
        raise EE(errorstring)
    else:
        for i in strasse:
            plr = i['Plraum']
            return plr
            
            
            ##*****************************************************************
            ## Wohnbezirk zuordnen
            ##
            ## HeS
            ##*****************************************************************
            
def wohnbez_zuordnen(dict, key1, key2, key3, errorstring):
    stra = dict.get(key1)
    if dict.get(key2) == '':
        hsnr = '"---"'
    else:
        hsnr = dict.get(key2)
    Plz = dict.get(key3)
    
    strasse = StrassenkatalogList(where = 'str_name = "%s"' % stra
                           + ' and hausnr = "%s" ' % hsnr + ' and plz = %s ' % Plz)
    
    if len(strasse) == 0:
        raise EE(errorstring)
    else:
        for i in strasse:
            bezirk = i['bezirk']
            if bezirk == 1:
                wohnbezirk = cc('wohnbez', '01')
            elif bezirk == 2:
                wohnbezirk = cc('wohnbez', '02')
            elif bezirk == 3:
                wohnbezirk = cc('wohnbez', '03')
            elif bezirk == 4:
                wohnbezirk = cc('wohnbez', '04')
            elif bezirk == 5:
                wohnbezirk = cc('wohnbez', '05')
            elif bezirk == 6:
                wohnbezirk = cc('wohnbez', '06')
            elif bezirk == 7:
                wohnbezirk = cc('wohnbez', '07')
            elif bezirk == 8:
                wohnbezirk = cc('wohnbez', '08')
            elif bezirk == 9:
                wohnbezirk = cc('wohnbez', '09')
            elif bezirk == 10:
                wohnbezirk = cc('wohnbez', '10')
            elif bezirk == 11:
                wohnbezirk = cc('wohnbez', '11')
            elif bezirk == 12:
                wohnbezirk = cc('wohnbez', '12')
            elif bezirk == 13:
                wohnbezirk = cc('wohnbez', '13')
            return wohnbezirk
            
            
            
def check_int_not_empty(dict, key, errorstring, default = None):
    val = dict.get(key)
    if val is None or val == '':
        if not default is None: return k_or_val(key, default)
    if type(val) == type(1): return val
    try: val = int(val)
    except:  raise EE(errorstring)
    return val
    
    
def check_fk(dict, key, klass, errorstring, default = None):
    fk = dict.get(key)
    if fk is None or fk == '':
        if not default is None: return k_or_val(key, default)
    try: fk = int(fk)
    except: raise EE(errorstring)
    try:
      #print 'FK', type(fk), fk
        obj = klass(fk)
    except Exception, e:
        raise EE("%s: %s" % (errorstring, e))
    return fk
    
    
    
def check_date(dict, key, errorstring, default = None,
               maybezero = None, maybefuture = None, nodayallowed = None):

    if type(key) == type(()):
        d, m, y = key[0], key[1], key[2]
    else:
        d, m, y = key + 'd', key + 'm', key + 'y'
    d, m, y = dict.get(d), dict.get(m), dict.get(y)
    if d is m is y is None or d == m == y == '':
        if not default is None:
            if isinstance(default, Date): return default
            if isinstance(default, DBObjekt): return default.getDate(key)
            if type(default) == type(()): return apply(Date, default)
    if nodayallowed and d is None or d == '':
        d = '1'
    try:
        d,m,y = int(d), int(m), int(y)
    except:
        raise EE(errorstring)
    datum = Date(y,m,d)
    if (not datum.check()  or
        (not maybefuture and datum.year != 0 and today() < datum) or
        (not maybezero and datum.year == 0)):
        raise EE("%s: %s" % (errorstring, str(datum)))
    return datum
    
def check_code(dict, key, kat_code, errorstring, default = None):
    code = dict.get(key)
    #print key, kat_code, code
    if code is None or code == '':
        if not default is None:
            if type(default) == type(''): return cc(kat_code, default)
            else: return k_or_val(key, default)
    try: code = int(code)
    except: raise EE(errorstring)
    try:
        codeobj = Code(code)
        assert codeobj['kat_code'] == kat_code
        # print 'Code:' ,code
    except Exception, e:
        raise EE("%s: %s" % (errorstring, e))
    return code
    
    
def get_string_fields(object, form, formnames, default = None, objectnames = None):
    if not objectnames:
        objectnames = formnames
    pairs = map(None, formnames, objectnames)
    for fname, objname in pairs:
        val = form.get(fname)
        if val is None:
            if not default is None:
                val = k_or_val(objname, default)
        elif type(val) != type(''): raise TypeError(fname)
        object[objname] = val
        
        
        # Falls der Wert eines Feldes in der form None oder '' ist und kein Default-
        # wert angegeben ist,  wird der Wert auf None gesetzt.
        # Ansonsten wird überprüft, ob es sich um ein Integer handelt,
        # sonst Fehler.
        
def get_int_fields(object, form, formnames, default = None, objectnames = None):
    if not objectnames:
        objectnames = formnames
    pairs = map(None, formnames, objectnames)
    for fname, objname in pairs:
        val = form.get(fname)
        if val is None or val == '':
            if not default is None:
                val = k_or_val(objname, default)
            else: val = None
        else:
            try: val = int(val)
            except: raise TypeError(fname)
        object[objname] = val
        
        
        # Gibt das existierende Objekt zurück.
        # Hier gibt es keine defaults, da das Objekt existieren muß.
def check_exists(dict, key, klass, errorstring):
    """Raise an error if an instance of klass with id id doesn't exists."""
    try:
        id = int(dict[key])
        obj = klass(id)
    except:
        raise EE(errorstring)
    return obj
    
    #######################
    # Weiter Prüffunktionen
    #######################
    
    # geaenderte check_unique. huber
    
def check_unique(value, klassList, field, errorstring):
    """Raise an error if value already exists for field for any instance of klass."""
    query = "%s = '%s'" % (field,value)
    liste = klassList(where = query)
    if len(liste) > 0:
        raise EE(errorstring)
    else:
        return value
        
        
        # Alte check_unique
        
        #def check_unique(value, klass, field, errorstring):
        #  """Raise an error if value already exists for field for any instance of klass."""
        #  try:
        #    obj = klass(field, val)
        #    raise EE(errorstring % obj)
        #  except: pass
        #  return value
        
def check_not_exists(id, klass, errorstring):
    """Raise an error if an instance of klass with id id already exists."""
    try:
        obj = klass(id)
    except: pass
    else:
        raise EE(errorstring % obj)
        
        
        ########################
        # Exceptions
        ########################
        
class EBUpdateError(Exception):
    """Ein Fehler, der normalerweise nicht passieren sollte und daher
    als ERROR geloggt werden sollte"""
    pass
    
class EBUpdateDataError(Exception):
    """Ein Fehler, der in der Regel durch falsche Eingaben des Benutzers
    entsteht und daher auch von diesem selber zu korrigieren ist.
    Sollte nicht geloggt werden."""
    pass
    
EE = EBUpdateDataError

# Es könnte auch Warnungen geben, die aber nicht einen Eintrag
# verhindern, z.B.zu alte Datumsangaben (mehr als zwei Jahre zurück)

class EBUpdateWarning(Exception):
    pass
    
    
def mk_daten_dirs(n=None):
    """Erstellt die Datenverzeichnispfade bei der Installation fuer die Akten
       und das Exportverzeichnis."""
    
    daten_path = os.path.join(config.INSTANCE_HOME, 'daten')
    akten_path = os.path.join(daten_path, 'akten')
    gruppen_path = os.path.join(daten_path, 'gruppen')
    export_path = os.path.join(daten_path, 'export')
    try:
        os.mkdir(daten_path, 0700)
    except: pass
    try:
        os.mkdir(akten_path, 0700)
    except: pass
    try:
        os.mkdir(gruppen_path, 0700)
    except: pass
    try:
        os.mkdir(export_path, 0700)
    except: pass

## NICHT MEHR NOETIG! Wird von mk_akte_dir mit erledigt.
##     if not n:
##         n = int(AK_DIRS_MAX)
##     print 'Lege Aktenverzeichnisse an (insg. %s )' % n
##     for a in range(n):
##         try:
##             os.mkdir(os.path.join(akten_path, str(a)), 0700)
##         except Exception, e:
##             raise ('Keine Aktenverzeichnisse angelegt: %s' %(e))
##     print 'Aktenverzeichnisse angelegt'
    
def get_akte_path(akid):
    """Ermittelt den Pfad für die Dokumente 1 Akte anhand der Aktenid."""
    
    n = int(config.AK_DIRS_MAX) # max. je n Akten in n Verzeichnissen
    akdirs = akid/n
    try:
        akte_path = os.path.join(config.INSTANCE_HOME, 'daten', 'akten', str(akdirs), str(akid))
    except Exception, e:
        raise ('Kein Aktenverzeichnis. %s' %(e))
    return akte_path
    
    
def mk_akte_dir(akid):
    """Erstellt 1 Verzeichnis fuer 1 Akte anhand der Aktenid;
       gibt Pfad der Akte zurueck."""
    
    n = int(config.AK_DIRS_MAX) # max. je n Akten in n Verzeichnissen
    akdir = akid/n

    akdir_path = os.path.join(config.INSTANCE_HOME, 'daten', 'akten', str(akdir))
    try:
        os.mkdir(akdir_path, 0700)
    except: pass
    
    akte_path = os.path.join(config.INSTANCE_HOME, 'daten', 'akten', str(akdir), str(akid))
    try:
        os.mkdir(akte_path, 0700)
    except: pass
    return akte_path
    
def mk_gruppe_dir(gruppeid):
    """Erstellt 1 Verzeichnis fuer 1 Gruppe anhand der Gruppenid;
       gibt Pfad der Gruppe zurueck. """
    
    gruppe_path = os.path.join(config.INSTANCE_HOME, 'daten', 'gruppen', str(gruppeid))
    try:
        os.mkdir(gruppe_path, 0700)
    except: pass
    return gruppe_path
    
def get_gruppe_path(gruppeid):
    """Ermittelt den Pfad für die Dokumente 1 Gruppe anhand der Gruppenid. """
    
    try:
        gruppe_path = os.path.join(config.INSTANCE_HOME, 'daten', 'gruppen', str(gruppeid))
    except Exception, e:
        raise ('Kein Gruppenverzeichnis. %s' %(e))
    return gruppe_path
    
    
def get_rm_datum(frist=None):
    """Ermittelt anhand der Loeschfrist (Aufbewahrungsfrist) das Loeschdatum. """
    
    if frist is None or frist == '':
        frist = config.LOESCHFRIST
    jahr = today().year
    monat = today().month
    heute = int(jahr)*12 + int(monat)
    loeschzeitm = int(heute)-int(frist)
    loeschjahr = int(loeschzeitm) / int(12)
    loeschmonat = int(loeschzeitm) - (int(loeschjahr) * int(12))
    loeschdatum = {'loeschjahr' : loeschjahr, 'loeschmonat' : loeschmonat}
    return loeschdatum
    
    
def convert_pstoascii():
    """Konvertiert die PDF-Dokumente in schlechtes Ascii. Unixspezifisch,
       verwendet Systemaufruf fuer das Programm: pstoascii. """
    
    import ebkus.db.sql
    sql.opendb()
    
    dokl = DokumentList(where = 'mtyp = %s'
                        % cc('mimetyp', 'pdf'), order = 'fall_id,id')
    grdokl = GruppendokumentList(where = 'mtyp = %s'
                                 % cc('mimetyp', 'pdf'), order = 'gruppe_id,id')
    
    for d in grdokl:
        gruppe_path = get_gruppe_path(d['gruppe_id'])
        dateil = os.listdir('%s' % gruppe_path)
        if '%s.txt' % d['id'] not in dateil and '%s.pdf' % d['id'] in dateil:
            os.system('ps2ascii %s/%s.pdf %s/%s.txt'
                      % (gruppe_path,d['id'],gruppe_path,d['id']))
            
    for d in dokl:
        fall = Fall(d['fall_id'])
        akte_path = get_akte_path(fall['akte_id'])
        dateil = os.listdir('%s' % akte_path)
        if '%s.txt' % d['id'] not in dateil and '%s.pdf' % d['id'] in dateil:
            os.system('ps2ascii %s/%s.pdf %s/%s.txt'
                      % (akte_path,d['id'],akte_path,d['id']))
            
    sql.closedb()
    
    
    
