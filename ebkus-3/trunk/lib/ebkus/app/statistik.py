# coding: latin-1

# TODO: die xcount*-Funktionen sollten Methoden der Klassen werden.

from ebkus.app.ebapi import Code, Tabelle, Feld, today, cc, sorted
from ebkus.app.ebapih import get_codes, get_all_codes

# für python2.3, kein set
try:
    s = set
except NameError:
    from sets import Set as set

class _Auszaehlung(object):

    def get_result(self):
        """Liefert das Resultat der Auszählung in Form
        einer Liste von 3-Tupeln:
          (Name, Häufigkeit, Prozent)
        wie sie von den xcount* Funktionen erzeugt werden.

        Die eigentliche Arbeit wird in _compute_result erledigt,
        die in jeder Unterklasse definiert werden muss.
        """
        if not self.result:
            # Ergebnis cachen
            self.result = self._compute_result()
        return self.result

    def _set_attributes(self, kw):
        self.session_key = kw.get('session_key')
        if not hasattr(self, 'feld'):
            self.feld = None
        # die Zahl hat nichts zu sagen, nur damit es nicht
        # genau die Adresse des Objekts ist :-)
        self.id = str(id(self)+785423)
        el0 = self.liste[0] 
        if isinstance(el0, tuple): # Liste kann auch aus Paaren bestehen
            el0 = el0[0]
        class_ = el0.__class__.__name__
        self.auswertungs_ueberschrift = \
                                      kw.get('auswertungs_ueberschrift',
                                             "%sauswertung vom %s" % (
            Tabelle(klasse=class_)['name'],
            "%(day)d.%(month)d.%(year)d." % today()))
        self.kategorie = kw.get('kategorie', self.feld and self.feld['kat']
                                or None)
        self.title = kw.get('title', self.feld and self.feld['name'] or 'Kein Titel')
        self.xtitle = kw.get('xtitle', self.title)
        #self.ytitle = kw.get('ytitle', 'S')
        self.ytitle = kw.get('ytitle', '%')
        self.identname = self.title.lower().replace('/','_').replace(' ', '_')
        self.result = None

    def _get_feld_objekt(self, feld):
        if isinstance(feld, basestring):
            tab_id = Tabelle(klasse=self.liste[0].__class__.__name__)['id']
            return Feld(feld=feld, tab_id=tab_id)
        else:
            # falls schon Objekt
            return feld


class CodeAuszaehlung(_Auszaehlung):
    def __init__(self, liste, feld, **kw):
        self.liste = liste
        # Feldobjekt holen
        self.feld = self._get_feld_objekt(feld)
        if self.feld['verwtyp__code'] == 'm':
            self.__class__ = MultiCodeAuszaehlung
        self._set_attributes(kw)

    def _compute_result(self):
        if self.feld['verwtyp__code'] == 'b':
            return xcountbereich(self.kategorie['code'], self.liste, self.feld['feld'])
        else:
            return xcountitem(self.kategorie['code'], self.liste, self.feld['feld'])
    
class MultiCodeAuszaehlung(CodeAuszaehlung):
    """Für die Felder, wo mehrere Code-Ids als Strings gespeichert werden,
    zB fachstat.eleistungen
    """
    def _compute_result(self):
        return xcountmultiitem(self.kategorie['code'], self.liste, self.feld['feld'])
    
class MehrfachCodeAuszaehlung(_Auszaehlung):
    """Zur Zeit nur für die ba*- Felder in der Jugendhilfestatistik"""
    def __init__(self, liste, felder, title, **kw):
        self.liste = liste
        self.felder = [self._get_feld_objekt(f) for f in felder]
        kw['title'] = title
        self._set_attributes(kw)
        
    def _compute_result(self):
        # TODO: generische Funktion schreiben
        res = []
        for f in self.felder:
            res.append(xcountitem_jgh_ba(f['kat']['code'], self.liste, f['feld'])[0])
        return res

class MehrfachCodeAuszaehlung2(_Auszaehlung):
    """Zur Zeit nur für die gr*- Felder in der Jugendhilfestatistik2007
    Achtung: diese Item funktioniert anders als die ba* Felder in der alten JGH.
    """
    def __init__(self, liste, felder, title, **kw):
        self.liste = liste
        self.felder = [self._get_feld_objekt(f) for f in felder]
        kw['title'] = title
        self._set_attributes(kw)
        
    def _compute_result(self):
        # TODO: generische Funktion schreiben
        return xcountitem_jgh07_gr(self.felder, self.liste)
            
class WertAuszaehlung(_Auszaehlung):
    def __init__(self, liste, feld, **kw):
        self.liste = liste
        # Feldobjekt holen
        self.feld = self._get_feld_objekt(feld)
        self._set_attributes(kw)

    def _compute_result(self):
        return xcountkontakte(self.liste, self.feld['feld'])
    
class RohWertAuszaehlung(_Auszaehlung):
    """Es wird mit feld im Objekt der Wert aufgesucht und die Häufigkeit gezählt.
    Beschriftet wird mit dem Wert selbst.
    """
    def __init__(self, liste, feldname, **kw):
        self.liste = liste
        self.feldname = feldname
        self._set_attributes(kw)

    def _compute_result(self):
        return xcountrohwerte(self.liste, self.feldname)
    
class FunktionsAuszaehlung(_Auszaehlung):
    """Für eine Liste von Paaren (Name, Funktion) wird ausgezählt,
    wie oft die Funktion einen wahren Wert liefert.
    Beschriftet wird mit dem Namen selbst.
    """
    def __init__(self, liste, name_function_pairs, **kw):
        self.liste = liste
        self.name_function_pairs = name_function_pairs
        self._set_attributes(kw)

    def _compute_result(self):
        return xcountfunction(self.liste, self.name_function_pairs)
    
class ObjektAuszaehlung(_Auszaehlung):
    """Zur Zeit funktionieren nur Mitarbeiter in der objekt_liste
    (es werden die Felder 'id' und 'na' für die Auszählung verwendet).
    """
    def __init__(self, liste, feld, objekt_liste, name_feld, **kw):
        self.liste = liste
        self.feld = self._get_feld_objekt(feld)
        self.objekt_liste = objekt_liste
        self.name_feld = name_feld
        self._set_attributes(kw)
        
    def _compute_result(self):
        return xcountnlist(self.objekt_liste, self.liste, self.feld['feld'],
                           count_feld='id', name_feld=self.name_feld)


class BereichsKategorieAuszaehlung(_Auszaehlung):
    def __init__(self, liste, attr, kat_code, **kw):
        self.liste = liste
        self.kat_code = kat_code
        self.attr = attr
        self._set_attributes(kw)
    def _compute_result(self):
        return xcountbereich(self.kat_code, self.liste, self.attr)

class EinzelWertAuszaehlung(_Auszaehlung):
    """Für das Attribut attr werden die Häufigkeiten und Prozentsätze
    der werte berechnet und mit dem entsprechenden Element in namen
    beschriftet.
    """
    def __init__(self, liste, attr, werte, namen=None, **kw):
        self.liste = liste
        self.werte = werte
        if namen == None:
            self.namen = ['']*len(werte)
        self.attr = attr
        self._set_attributes(kw)
        #print werte, namen
        assert len(self.werte) == len(self.namen)
    def _compute_result(self):
        return xcountwerte(self.liste, self.werte, self.namen, self.attr)

# TODO: direkt in _compute_result einarbeiten

def xcountitem(kat_code, d_list, d_item):
    """Liste mit Namen, Anzahl, Prozent fuer die Codefelder in
    der Fach- oder Jugendhilfestatistikdictliste.

    kat_code: die Kategorie, für die die Auszählung gemacht werden soll
    d_list: die Liste der Objekte, über die gezählt werden soll
    d_item: der Name des Attributes, dessen Werte gezählt werden sollen
            (die Werte sind Codes der Kategorie)

    Anwendung:
    zugangsarten = xcountitem('fszm', fachstatliste, 'zm') """
    res = []
    #codelist = get_all_codes(kat_code)
    codelist = get_codes(kat_code) # nur gültige codes (??)
    values = [x[d_item] for x in d_list]
    for c in codelist:
        freq = values.count(c['id'])
        a = (c['name'], freq, ((float(freq)*100)/float(len(d_list))))
        res.append(a)
    return res

def xcountmultiitem(kat_code, d_list, d_item):
    """Liste mit Namen, Anzahl, Prozent fuer die Codefelder in
    der Fach- oder Jugendhilfestatistikdictliste.

    kat_code: die Kategorie, für die die Auszählung gemacht werden soll
    d_list: die Liste der Objekte, über die gezählt werden soll
    d_item: der Name des Attributes, dessen Werte gezählt werden sollen
            (die Werte sind Strings, die ids für Codes der Kategorie enthalten)

    Anwendung:
    zugangsarten = xcountitem('fspbk', fachstatliste, 'kindprobleme') """
    res = []
    #codelist = get_all_codes(kat_code)
    codelist = get_codes(kat_code) # nur gültige codes (??)
    def get_ids():
        """ """
        for x in d_list:
            val = x[d_item]
            #print 'VAL', val
            if val != None:
                for i in val.split():
                    yield int(i)
    values = [i for i in get_ids()]
    size = len(values)
    for c in codelist:
        if size:
            freq = values.count(c['id'])
            a = (c['name'], freq, ((float(freq)*100)/float(len(d_list))))
        else:
            a = (c['name'], 0, 0.0)
        res.append(a)
    return res

def xcountwerte(d_list, werte, namen, attr):
    res = []
    values = [x[attr] for x in d_list]
    for w, n in zip(werte, namen):
        freq = values.count(w)
        a = (n, freq, ((float(freq)*100)/float(len(d_list))))
        res.append(a)
    return res

def xcountrohwerte(d_list, feldname):
    res = []
    values = []
    for x in d_list:
        v = x[feldname]
        if v == None:
            v = ''
        values.append(v)
    werte = sorted(set(values))
    for w in werte:
        freq = values.count(w)
        a = (w, freq, ((float(freq)*100)/float(len(d_list))))
        res.append(a)
    return res

def xcountfunction(d_list, functions):
    """functions ist eine Sequence aus Paaren name, Funktion.
    Für jeden Namen wird ausgezählt, wie häufig die Funktion true
    liefert für jedes Element von d_list"""
    res = []
    for name, func in functions:
        freq = [bool(func(el)) for el in d_list].count(True)
        a = (name, freq, ((float(freq)*100)/float(len(d_list))))
        res.append(a)
    return res
        
def xcountitem_jgh_ba(kat_code, d_list, d_item):
    """Liste mit Namen, Anzahl, Prozent fuer die Tabelle Beratungsanlass
    der Jugendhilfestatistik. Es werden nur die Ankreuzungen (Code 1) gezählt; die
    Leerangaben (Code 0) nicht. (Die Summe der einzelnen Prozentangaben
    ist != 100 %, da mehr als 1 Ankreuzung bei den Beratungsanlässen erlaubt ist.)
    
    Anwendung:
    beratungsanlass1 = xcountitem_jgh_ba(kat_code, jghstatistikliste, 'ba1') """
    res = []
    c1 = Code(kat_code=kat_code, code='1')
    values = [x[d_item] for x in d_list]
    freq = values.count(c1['id'])
    a = [c1['name'], freq, ((float(freq)*100)/float(len(d_list)))]
    res.append(a)
    return res

def xcountitem_jgh07_gr(felder, d_list):
    feldnamen = [f['feld'] for f in felder]
    values_for_each = [[x[f] for x in d_list] for f in feldnamen]
    values = []
    for v in values_for_each:
        values += v
    # Annahme: alle Felder haben denselben kat_code
    codelist = get_all_codes(felder[0]['kat_code'])
    res = []
    for c in codelist:
        freq = values.count(c['id'])
        a = (c['name'], freq, ((float(freq)*100)/float(len(d_list))))
        res.append(a)
    return res
                        
def xcountbereich(kat_code, d_list, d_item):
    """Liste mit Namen, Anzahl, Prozent fuer die Codebereiche
    in der Fach- oder Jugendhilfestatistik.
    
    Anwendung:
    anzahltermine = xcountbereich('fskat', fachstatliste, 'kat') """
    x = []
    res = []
    # TODO get_all_codes hier oder nicht?
    # Ich glaube nicht, da alte Bereiche neue überlappen könnten, etc.
    # das gibt keinen Sinn
    codelist = get_codes(kat_code)
    for d in d_list:
        bereichs_code = None
        value = d[d_item]
        for c in codelist:
            if value >= c['mini'] and value <= c['maxi']:
                bereichs_code = c['id']
                break
        x.append(bereichs_code)
    for c in codelist:
        freq = x.count(c['id'])
        a = [c['name'], freq, ((float(freq)*100)/float(len(d_list)))]
        res.append(a)
    return res

def xcountnlist(nlist, d_list, d_item, count_feld='id', name_feld='na'):
    # die defaults id und na funktionieren für die MitarbeiterList
    """Liste mit Namen, Anzahl, Prozent fuer relat. Dictionarylisten.

    Gezählt werden d_item-Felder der Elemente von d_list, und zwar
    nach Häufigkeit der Werte des count_feld Feldes der Elemente in nlist.
    Für die Benennung in der Ausgabe wird das name_feld des Elements in
    nlist verwendet.
    
    Beispiel:
    anzahlmitarbeiter = xcountnlist(mitarbeiterliste, fachstatliste, 'mit_id',
                                    count_feld='id', name_feld='na')

    Wieviele Elemente (und Prozentsatz) aus d_list entfallen auf jedes Element
    von nlist?
    """
    x = []
    res = []
    for d in d_list:
        x.append(d[d_item])
    for n in nlist:
        freq = x.count(n[count_feld])
        if freq > 0:
            a = [n[name_feld], freq, ((float(freq)*100)/float(len(d_list)))]
            res.append(a)
    return res
    
def xcountkontakte(d_list, d_item):
    """zaehlt die Anzahl der Kontaktzahlen in der Fachstatistik, berechnet die
    Prozente, liefert eine Liste aus: Kontaktzahl, Haeufigkeit, Prozent zurueck.
    """
    values = [x[d_item] for x in d_list]
    values.sort()
    #print 'XCOUNTKONTAKTE', values
    #print d_item
    #print d_list
    res = []
    i = 0
    n = len(values)
    while i < n:
        freq = values.count(values[i])
        res.append(
          [values[i], freq, float(freq)*100/float(n)])
        i += freq
    return res

## _alter_to_group = (1,1,1,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5,6,6,6,7,7,7,7,7,7,8)
## _group_to_name = ('0-2','3-5','6-9','10-13','14-17','18-20','21-26','ab 27')
## def _altersgruppe(jgh):
##     # Alter berechnen:
##     # mindestens 0, höchstens 27
##     # berechnet aus der Differenz zwischen Hilfebeginnjahr und -monat und
##     # Geburtsjahr und -monat
##     alter = min(max(0, ((jgh['bgm'] + 12*jgh['bgy']) - (jgh['gem'] + 12*jgh['gey'])) / 12), 27)
##     # Altersgruppe ist ein Index in _group_to_name
##     return _alter_to_group[alter]

## def xcountaltersgruppe(d_list):
##     """Zählt Altersgruppen aus für die Jugendhilfestatistik2007.
##     Dazu wird die Differenz zwischen Hilfebeginn und Geburtsmonat/jahr
##     herangezogen, die beide Teil der Jugendhilfestatistik2007 sind.
##     Die Altersgruppen werden an die Fachstatistik angelehnt (fsag):
## 1;0-2;fsag
## 2;3-5;fsag
## 3;6-9;fsag
## 4;10-13;fsag
## 5;14-17;fsag
## 6;18-20;fsag
## 7;21-26;fsag
## 8;27-;fsag
##     """
        
##     values = [_altersgruppe(jgh) for jgh in d_list]
##     res = []
##     for i, n in enumerate(_group_to_name):
##         freq = values.count(i+1)
##         a = (n, freq, ((float(freq)*100)/float(len(d_list))))
##         res.append(a)
##     return res

## def xcountaltersgruppe(d_list):
##     return xcountbereich('jghag', self.liste, 'alter')
    
