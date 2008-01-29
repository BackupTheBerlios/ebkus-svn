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
import traceback

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
    
def is_binary(arg):
    code = None
    if isinstance(arg, (Dokument, Gruppendokument)):
        code = arg['mtyp__code']
    elif isinstance(arg, Code):
        code = arg['code']
    elif isinstance(arg, (basestring, int, long)):
        # ist id
        code = Code(arg)['code']
    assert code
    # Nun muss es Objekt sein
    if code in ('txt', 'asc', 'html', 'htm', 'ps', 'rtf', 'rtx',):
        return False
    return True
        
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

def bcode(kat_code, value,
          default=None # default für value!
          ):
    "liefert das Code-Objekt der Bereichskategorie, in deren "
    "Bereich value fällt."
    from ebkus.app.ebapih import get_codes
    if value or value==0:
        value = int(value)
    else:
        if default != None:
            value = default
        else:
            raise EE('Kein Wert für Bereichskategorie')
    code_list = get_codes(kat_code)
    for c in code_list:
        try:
            if value >= int(c['mini']) and value <= int(c['maxi']):
                return c
        except:
            pass
    raise EE('Keine Bereich für Wert gefunden')
    
    


def get_feld(feldname, tabelle=None, klasse=None):
    "Liefert das entsprechende Feldobjekt."
    if tabelle:
        return Feld(feld=feldname,
                    tab_id=Tabelle(tabelle=tabelle)['id'])
    elif klasse:
        return Feld(feld=feldname,
                    tab_id=Tabelle(klasse=klasse)['id'])

    
class Date(object):
    def __init__(self, year = None, month = None, day = None):
        """No error checking. Use the check method."""
        if year is month is day is None: # assume today
            import time
            year, month, day = time.localtime(time.time())[:3]
        if month is None: month = 1
        if day is None: day = 1
        self.year, self.month, self.day = year, month, day
        self.years = self.months = self.days = ''
        for a in ('month', 'day'):
            v = getattr(self, a)
            if isinstance(v, (int, long)):
                setattr(self, a+'s', "%02d" % v)
        if isinstance(self.year, (int, long)):
                self.years = "%04d" % self.year
        
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

    def check(self, alle_jahrgaenge_akzeptieren=False):
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
        if alle_jahrgaenge_akzeptieren:
            if y < 1890 or y > today().year:
                return False
        else:
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

def str2date(str):
    "3.4.1999 -> Date"
    try:
        if str:
            nums = [int(i) for i in str.split('.')]
        else:
            nums = [0,0,0]
    except:
        raise EE('Fehler in Datumsstring: %s' %str)
    nums.reverse()
    return Date(*nums)

def calc_age(gb_datum_als_string, aktuelles_datum_als_date):
    d,m,y = [int(x) for x in gb_datum_als_string.split('.')]
    assert y > 1900
    gb = Date(y, m, d)
    diff = gb.diff(aktuelles_datum_als_date)
    return diff/12

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
    return Date(self[y], self[m], self.get(d))
    
def setDate(self, key, date):
    y,m,d = key + 'y', key + 'm', key + 'd'
    self[y], self[m], self[d] = date.totuple()
    
dbapp.DBObjekt.getDate = getDate
dbapp.DBObjekt.setDate = setDate


class Time(object):
    def __init__(self, hour=None, minute=None):
        "Ohne hour und minute --> leeres Zeitobjekt"
        "Falls hour einen Wert hat und minute nicht, wird minute auf 0"
        "gesetzt"
        if hour or hour == 0: # muss Ziffer sein
            if not minute:    # wenn leer --> 0
                minute = 0
            self.hour = int(hour)
            self.hours = "%02d" % self.hour
            self.minute = int(minute)
            self.minutes = "%02d" % self.minute
        else:
            self.hours = self.minutes = ''
            self.hour = self.minute = None
        self.empty = (self.hour == None)
    def __str__(self):
        if self.empty:
            return ''
        else:
            return "%s:%s" % (self.hours, self.minutes)
    def check(self):
        if self.empty or ((0 <= self.hour <= 23) and (0 <= self.minute <= 59)):
            return True
        return False
        
            
def getTime(self, key):
    h,min = key + 'h', key + 'min'
    return Time(self.get(h), self.get(min))
    
def setTime(self, key, time):
    h,min = key + 'h', key + 'min'
    self[h], self[min] = time.hour, time.minute
    
dbapp.DBObjekt.getTime = getTime
dbapp.DBObjekt.setTime = setTime


def getQuartal(monat):
    """Gibt das Quartal für einen bestimmten Monat aus."""
    if int(monat) > 0 and int(monat) < 13:
        q = ((int(monat) - 1) / 3) + 1
        return int(q)
    else:
        raise EE("Keine Monatszahl zwischen 1 und 12")

def getNewId(self):
    """Standardmethode, um neue Werte für Schlüsselfelder zu erzeugen.
    
    Verwendet maxist-Feld von Tabelle, um eine neue id zu
    generieren.
    
    Es genügt nicht, das Maximum der Spalte zu nehmen, da mehrere Benutzer
    das gleiche tun können und hinterher alle versuchen, ein Objekt mit derselben
    ID einzufügen.

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
    maxid = sql.SQL("select max(%s) from %s" % (self.primarykey, self.table)).execute()[0][0]
    if not maxid:
        maxid = 0
    tab = Tabelle(tabelle=self.table)
    maxist = tab['maxist']
    newid = max(maxid, maxist) + 1
    tab.update({'maxist': newid})
    return newid
    
dbapp.DBObjekt.getNewId = getNewId


def getNewFallnummer(stz_code, jahr):
    """Neue Fallnummer erzeugen."""
    return _getNewNummer(stz_code, jahr, FallList, 'fn')
def getNewGruppennummer(stz_code, jahr):
    """Neue Gruppennummer erzeugen."""
    return _getNewNummer(stz_code, jahr, GruppeList, 'gn')
def _getNewNummer(stz_code, jahr, klass, feld):
    """Neue Fall- oder Gruppennummer erzeugen."""
    jahresfallliste = klass(
      where="bgy = %s and %s like '%%%s%%'" % (jahr, feld, stz_code))
    if jahresfallliste:
        groesste_fallnummer = max([ int(f[feld].split('-')[0]) for f in jahresfallliste])
    else:
        groesste_fallnummer = 1
    return "%s-%s%s" % (groesste_fallnummer + 1, jahr, stz_code)
    
    
    
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
    
def _akte_name(self, key):
    return "%(vn)s %(na)s" % self

def _wiederaufnehmbar(self, key):
    """Ein Fall ist wiederaufnehmbar, wenn der Abschluss *länger* zurückliegt,
    als die konfigurierte Wiederaufnahmefrist.
    Ansonsten (nämlich innerhalb der Wiederaufnahmefrist) wird
    der einfach aktiviert, dh 'Zda Rückgängig'
    """
    letzter_fall = self['letzter_fall']
    if letzter_fall and letzter_fall['zday'] != 0:
        zda_date = letzter_fall.getDate('zda')
        zda_rueck_bis = zda_date.add_month(config.WIEDERAUFNAHMEFRIST)
        return today() > zda_rueck_bis
    return False
    
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
    res = ''
    try:
        if int(self['lage']) == Code(cc('lage', '0'))['id']:
          # in Berlin
            res = self['str']
    except:
        pass
    return res
        
def _str_ausser(self, key):
    res = ''
    try:
        if int(self['lage']) == Code(cc('lage', '1'))['id']:
          # ausserhalb Berlins
            res = self['str']
    except:
        pass
    return res

def _get_strkat_ortsangabe(self, key):
    strasse = self.get('strasse')
    if strasse == None:
        from ebkus.html.strkat import get_strasse
        strasse = self['strasse'] = get_strasse(self)
    return strasse.get(key)

        
Akte.attributemethods['name'] = _akte_name
Akte.attributemethods['wiederaufnehmbar'] = _wiederaufnehmbar
Akte.attributemethods['letzter_fall'] = _letzter_fall
Akte.attributemethods['aktueller_fall'] = _aktueller_fall
Akte.attributemethods['aktuell'] = _aktuell_akte
Akte.attributemethods['str_inner'] = _str_inner
Akte.attributemethods['str_ausser'] = _str_ausser
Akte.attributemethods['bezirk'] = _get_strkat_ortsangabe
Akte.attributemethods['ortsteil'] = _get_strkat_ortsangabe
Akte.attributemethods['samtgemeinde'] = _get_strkat_ortsangabe
# Achtung ganz doof: Akte hat eigenes Feld planungsr
Akte.attributemethods['plraum'] = _get_strkat_ortsangabe

Bezugsperson.attributemethods['str_inner'] = _str_inner
Bezugsperson.attributemethods['str_ausser'] = _str_ausser
Bezugsperson.attributemethods['bezirk'] = _get_strkat_ortsangabe
Bezugsperson.attributemethods['ortsteil'] = _get_strkat_ortsangabe
Bezugsperson.attributemethods['samtgemeinde'] = _get_strkat_ortsangabe

############################
# Berechnete Felder für Fall
############################

def _fall_name(self, key):
    return self['akte__name']

def _aktuell_fall(self, key):
    return self['zday'] == 0
    
def _zustaendig_fall(self, key):
    "die aktuelle Zuständigkeit (*nicht* der Mitarbeiter)"
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
    zs = self['zustaendigkeiten'].sorted('bgy', 'bgm', 'bgd')
    res = zs[-1]
    self._cache_field('zuletzt_zustaendig', res)
    return res
    
def _get_jgh(self, key):
    where_cl = "fall_id=%s" % self['id']
    jghs = []
    jghs += JugendhilfestatistikList(where=where_cl)
    jghs += Jugendhilfestatistik2007List(where=where_cl)
    assert len(jghs) <= 1, "Mehr als eine Bundesstatistik für Fall %s" % fall['fn']
    if jghs:
        return jghs[0]
    else:
        return None

def _fn_count(self, key):
    fn = self['fn']
    return int(fn.split('-')[0])

## def _has_fachstatistik(self, key):
##     if self['aktuell']:
##         if self['fachstatistiken']:
##             return str(self['fachstatistiken'][0]['jahr'])[2:]
##         else:
##             return 'nv'
##     else:
##         return '-'
## def _has_jghstatistik(self, key):
##     if self['aktuell']:
##         if self['jgh07_statistiken']:
##             return str(self['jgh07_statistiken'][0]['jahr'])[2:]
##         else:
##             return 'nv'
##     else:
##         return '-'
def _has_statistik(self, key):
    if key == 'has_fachstatistik':
        k = 'fachstatistiken'
    elif key == 'has_jghstatistik':
        k = 'jgh07_statistiken'
    if self['aktuell']:
        if self[k]:
            return str(self[k][0]['jahr'])[2:]
        else:
            return 'nv'
    else:
        return '-'

def _fall_beratungskontakte(self, key):
    bkont_list = BeratungskontaktList(
        where='fallberatungskontakt.fall_id=%s' % self['id'],
        join=[('fallberatungskontakt',
               'fallberatungskontakt.bkont_id=beratungskontakt.id')])
    bkont_list.sort('ky', 'km', 'kd')
    return bkont_list
def _fall_leistungsbeginn(self, key):
    leistungen = self['leistungen']
    leistungen.sort('bgy', 'bgm', 'bgd')
    return leistungen[0].getDate('bg')

Fall.attributemethods['name'] = _fall_name
Fall.attributemethods['aktuell'] = _aktuell_fall
Fall.attributemethods['zustaendig'] = _zustaendig_fall
Fall.attributemethods['zuletzt_zustaendig'] = _zuletzt_zustaendig_fall
Fall.attributemethods['jgh'] = _get_jgh
Fall.attributemethods['fn_count'] = _fn_count
Fall.attributemethods['has_fachstatistik'] = _has_statistik
Fall.attributemethods['has_jghstatistik'] = _has_statistik
Fall.attributemethods['bg'] = getDate
Fall.attributemethods['zda'] = getDate
Fall.attributemethods['beratungskontakte'] = _fall_beratungskontakte
Fall.attributemethods['leistungsbeginn'] = _fall_leistungsbeginn


def _prev_zust(self, key):
    zustaendigkeiten = self['fall__zustaendigkeiten'].sorted('bgy', 'bgm', 'bgd')
    i = zustaendigkeiten.index(self)
    if i > 0:
        return zustaendigkeiten[i-1]
    else:
        return None
def _next_zust(self, key):
    zustaendigkeiten = self['fall__zustaendigkeiten'].sorted('bgy', 'bgm', 'bgd')
    i = zustaendigkeiten.index(self)
    if i+1 < len(zustaendigkeiten):
        return zustaendigkeiten[i+1]
    else:
        return None
    

Zustaendigkeit.attributemethods['prev'] = _prev_zust
Zustaendigkeit.attributemethods['next'] = _next_zust



def _alter(self, key):
    # Alter berechnen:
    # mindestens 0, höchstens 27
    # berechnet aus der Differenz zwischen Hilfebeginnjahr und -monat und
    # Geburtsjahr und -monat
    alter = min(27,
                max(0, ((self['bgm'] + 12*self['bgy']) -
                        (self['gem'] + 12*self['gey'])) / 12))
    return alter
        
Jugendhilfestatistik2007.attributemethods['alter'] = _alter

# Felder vn, na wie bei Akter
Mitarbeiter.attributemethods['name'] = _akte_name

def _gruppe_mitarbeiternamen(self, key):
    """Ein String mit komma-getrennten Nachnamen der Mitarbeiter einer Gruppe."""
    mitarbeiter = self['mitarbeiter'].sorted('mit__na')
    return ', '.join([m['mit__na'] for m in mitarbeiter])
Gruppe.attributemethods['mitarbeiternamen'] = _gruppe_mitarbeiternamen
Gruppe.attributemethods['bg'] = getDate
Gruppe.attributemethods['e'] = getDate


def _bkont_mitarbeiter(self, key):
    mitarbeiter_list = MitarbeiterList(
        where='mitarbeiterberatungskontakt.bkont_id=%s' % self['id'],
        join=[('mitarbeiterberatungskontakt',
               'mitarbeiterberatungskontakt.mit_id=mitarbeiter.id')])
    mitarbeiter_list.sort('na')
    return mitarbeiter_list
def _bkont_faelle(self, key):
    fall_list = FallList(
        where='fallberatungskontakt.bkont_id=%s' % self['id'],
        join=[('fallberatungskontakt',
               'fallberatungskontakt.fall_id=fall.id')])
    fall_list.sort('akte__na')
    return fall_list
## def _brutto_dauer_bkont_bs(self, key):
##     """Eval'ed den dok-String der Kategorie art_bs aus,
##     so dass man dort eintragen kann, wie aus der Netto-Dauer
##     die Brutto-Dauer berechnet wird.
##     """
##     if config.BERATUNGSKONTAKTE_BS:
##         dauer = self.get('dauer', 0)
##         term = self['art_bs__dok']
##         try:
##             brutto = int(round(eval(term)))
##         except:
##             brutto = 0
##         return brutto
def _brutto_dauer_bkont_bs(self, key):
    """Brutto-Dauer für die Kontaktanzahl der Bundesstatistik.
    
    Eval'ed den dok-String der Kategorie art_bs aus,
    so dass man dort eintragen kann, wie aus der Netto-Dauer
    die Brutto-Dauer berechnet wird.
    Speziell für die Brutto-Dauer im Sinne der Bundesstatistik
    kann man nach dem Trenner || eine zweite Formel eingeben, die nur
    für die Berechnung der Kontaktzeit für die Bundesstatistik
    genommen wird:

    dauer * 1.8 || dauer*1.2 # bs:ja
    """
    if config.BERATUNGSKONTAKTE_BS:
        dauer = self.get('dauer', 0)
        term = self['art_bs__dok']
        # Kommentar absplitten
        try:
            term, comment = term.split('#')
        except:
            pass
        # zweite Formal absplitten
        try:
            brutto_term, brutto_bs_term = term.split('||')
        except:
            # falls nicht vorhanden, die erste nehmen
            brutto_term = brutto_bs_term = term
        if key == 'brutto':
            term = brutto_term
        elif key == 'brutto_bs':
            term = brutto_bs_term
        try:
            brutto = int(round(eval(term)))
        except:
            brutto = 0
        return brutto
        
def _jghkontakte(self, key):
    try:
        if config.BERATUNGSKONTAKTE_BS:
            if 'bs:ja' in self['art_bs__dok'].lower():
                # als Grundlage für die Berechnung der Anzahl der Kontakte
                # wird das oben berechnete brutto_bs genommen
                return int(bcode('kdbs', self['brutto_bs'])['code'])
            else:
                return 0
        elif config.BERATUNGSKONTAKTE:
            return int(bcode('fskd', self['dauer'])['code'])
    except:
        pass
    
Beratungskontakt.attributemethods['mitarbeiter'] = _bkont_mitarbeiter
Beratungskontakt.attributemethods['faelle'] = _bkont_faelle
Beratungskontakt.attributemethods['brutto'] = _brutto_dauer_bkont_bs
# brutto für die Bundesstatistik
Beratungskontakt.attributemethods['brutto_bs'] = _brutto_dauer_bkont_bs
Beratungskontakt.attributemethods['jghkontakte'] = _jghkontakte


def _brutto_dauer_fua_bs(self, key):
    dauer = self.get('dauer', 0)
    term = self['art__dok']
    try:
        brutto = int(round(eval(term)))
    except:
        brutto = 0
    return brutto

Fua_BS.attributemethods['brutto'] = _brutto_dauer_fua_bs

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
Beratungskontakt.pathdefinitions = {
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
Jugendhilfestatistik2007.pathdefinitions = {
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
        for b in f['beratungskontakte']: b.undo_cached_fields()
        for b in f['fallberatungskontakte']: b.undo_cached_fields()
        for z in f['zustaendigkeiten']: z.undo_cached_fields()
        for a in f['anmeldung']: a.undo_cached_fields()
        for fs in f['fachstatistiken']: fs.undo_cached_fields()
        for jgh in f['jgh_statistiken']: jgh.undo_cached_fields()
        for jgh07 in f['jgh07_statistiken']: jgh07.undo_cached_fields()
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
    
def check_list(dict, key, errorstring, default=None):
    "garantiert eine Liste mit nicht-leeren Elementen"
    "Falls default == [], auch eine leere Liste"
    val = dict.get(key)
    if val:
        if isinstance(val, basestring):
            val = [val]
        else:
            # TODO: das muss man nicht immer prüfen
            assert isinstance(val, list)
        # keine leeren strings
        val = [v for v in val if v]
        #print 'VAL', val
        return val
    else:
        #print 'VAL EMPTY', val
        if default == None:
            raise EE(errorstring)
        else:
            return default
    
            
def check_int_not_empty(dict, key, errorstring, default = None):
    val = dict.get(key)
    if isinstance(val, (int, long)):
        return val
    if val is None or val.strip() == '':
        if not default is None:
            return k_or_val(key, default)
    try:
        val = int(val)
    except:
        raise EE(errorstring)
    return val
    
    
def check_fk(dict, key, klass, errorstring, default = None):
    fk = dict.get(key)
    if fk in (None, '', ' '):
        if not default is None: return k_or_val(key, default)
    try: fk = int(fk)
    except: raise EE(errorstring)
    try:
      #print 'FK', type(fk), fk
        obj = klass(fk)
    except Exception, e:
        raise EE("%s: %s" % (errorstring, e))
    return fk
    
    

def check_time(dict, key, errorstring, default=None):
    if type(key) == type(()):
        h, min = key[0], key[1]
    else:
        h, min = key + 'h', key + 'min'
    h, min = dict.get(h), dict.get(min)
    try:
        t = Time(h, min)
        assert t.check()
    except:
        traceback.print_exc()
        raise EE(errorstring)
    if t.empty:
        if default != None:
            return default
        else:
            traceback.print_exc()
            raise EE(errorstring)
    return t
    
def check_date(dict, key, errorstring, default = None,
               maybezero = None,    # darf 0 sein
               maybefuture = None,  # darf in der Zukunft liegen
               nodayallowed = None, # Tag darf fehlen
               alle_jahrgaenge_akzeptieren=False,
               # falls True, nur Jahre zwischen 1890 und heute akzeptieren
               ):

    if type(key) == type(()):
        d, m, y = key[0], key[1], key[2]
    else:
        d, m, y = key + 'd', key + 'm', key + 'y'
    d, m, y = dict.get(d), dict.get(m), dict.get(y)
    empty = (None, '', ' ')
    if d in empty and m in empty and y in empty:
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
    if (not datum.check(alle_jahrgaenge_akzeptieren)  or
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

def check_multi_code(dict, key, kat_code, errorstring, default = None):
    """mehrere code ids als string in einem Feld"""
    code = dict.get(key)
    #print key, kat_code, code
    if code is None or code == '':
        if not default is None:
            if type(default) == type(''):
                return cc(kat_code, default)
            else:
                return k_or_val(key, default)
    if not isinstance(code, list):
        code = [code]
    try:
        code = [int(c) for c in code]
    except:
        raise EE(errorstring)
    try:
        codes = CodeList(code)
    except Exception, e:
        raise EE("%s: %s" % (errorstring, e))
    return ' '.join([str(i) for i in codes.getIds()])
    
    
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
    
ER = EBUpdateError


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
    
# TODO beseitigen, ist verzockt. Besser Date.add_month benutzen. Funktioniert
# auch mit negativen Werten.
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
    


# Ein Register in der Datenbank, wo man beliebige Python-Objekte
# mit einem Schlüssel persistent ablegen kann
def register_set(key, value=None):
    from cPickle import dumps
    r = None
    try:
        r = Register(regkey=key)
    except dbapp.DBAppError:
        pass
    if value == None:
        if r:
            r.delete()
        return
    p = dumps(value)
    if r:
        r.update({'value': p})
    else:
        r = Register()
        r.init(id=Register().getNewId(),
               regkey=key,
               value=p,)
        r.insert()
def register_get(key, default=None):
    from cPickle import loads
    try:
        r = Register(regkey=key)
    except dbapp.DBAppError:
        return default
    s = r['value']
    return loads(s)


# TBD wieder wegnehmen beim Umstieg auf höhrere Version
def sorted(seq):
    "da wir python2.3 verwenden, leider kein eingebautes sorted"
    try:
        copy = list(seq)
        copy.sort()
        return copy
    except:
        return seq
