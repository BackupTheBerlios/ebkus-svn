# coding: latin-1

# TODO: die xcount*-Funktionen sollten Methoden der Klassen werden.

from ebkus.app.ebapi import Code, Tabelle, Feld, today, cc
from ebkus.app.ebapih import get_codes, get_all_codes


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
        self.file = kw.get('file')
        if not hasattr(self, 'feld'):
            self.feld = None
        # die Zahl hat nichts zu sagen, nur damit es nicht
        # genau die Adresse des Objekts ist :-)
        self.id = str(id(self)+785423) 
        self.auswertungs_ueberschrift = \
                                      kw.get('auswertungs_ueberschrift',
                                             "%sauswertung vom %s" % (
            Tabelle(klasse=self.liste[0].__class__.__name__)['name'],
            "%(day)d.%(month)d.%(year)d." % today()))
        self.kategorie = kw.get('kategorie', self.feld and self.feld['kat']
                                or None)
        self.title = kw.get('title', self.feld and self.feld['name'] or 'Kein Titel')
        self.xtitle = kw.get('xtitle', self.title)
        self.ytitle = kw.get('ytitle', 'S')
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
        self._set_attributes(kw)

    def _compute_result(self):
        if self.feld['verwtyp__code'] == 'b':
            return xcountbereich(self.kategorie['code'], self.liste, self.feld['feld'])
        else:
            return xcountitem(self.kategorie['code'], self.liste, self.feld['feld'])
    
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
            
class WertAuszaehlung(_Auszaehlung):
    def __init__(self, liste, feld, **kw):
        self.liste = liste
        # Feldobjekt holen
        self.feld = self._get_feld_objekt(feld)
        self._set_attributes(kw)

    def _compute_result(self):
        return xcountkontakte(self.liste, self.feld['feld'])
    
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
    codelist = get_all_codes(kat_code)
    values = [x[d_item] for x in d_list]
    for c in codelist:
        freq = values.count(c['id'])
        a = (c['name'], freq, ((float(freq)*100)/float(len(d_list))))
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
    
    
def xcountbereich(kat_code, d_list, d_item):
    """Liste mit Namen, Anzahl, Prozent fuer die Codebereiche
    in der Fach- oder Jugendhilfestatistik.
    
    Anwendung:
    anzahltermine = xcountbereich('fskat', fachstatliste, 'kat') """
    x = []
    res = []
    codelist = get_all_codes(kat_code)
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
        a = [n[name_feld], freq, ((float(freq)*100)/float(len(d_list)))]
        res.append(a)
    return res
    
def xcountkontakte(d_list, d_item):
    """zaehlt die Anzahl der Kontaktzahlen in der Fachstatistik, berechnet die
    Prozente, liefert eine Liste aus: Kontaktzahl, Haeufigkeit, Prozent zurueck.
    """
    values = [x[d_item] for x in d_list]
    values.sort()
    res = []
    i = 0
    n = len(values)
    while i < n:
        freq = values.count(values[i])
        res.append(
          [values[i], freq, float(freq)*100/float(n)])
        i += freq
    return res
