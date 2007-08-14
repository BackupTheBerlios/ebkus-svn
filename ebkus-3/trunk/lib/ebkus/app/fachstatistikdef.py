# coding: latin-1

# Feldtypen: k kat
#            b integer mit Bereichskategorien
#            m multikat   Mehrfachauswahl aus Kategorie
#            s string
#            i integer
#            o Objekt

# Verwendung: fsdef.<gruppenkuerzel>.<itemkuerzel>.<attr>
# Kuerzel immer im Attribut key abgelegt
# gruppenkuerzel: falldaten, angabenklient, termine
#                 bei einitem-Gruppen identisch mit itemkuerzel
# itemkuerzel:    attribut key, normalerweise von feld übernommen

from ebkus.app.ebapih import get_codes, make_option_list


class FachstatistikItem(object):
    def __init__(self, **kw):
        self.name = kw.get('name')
        self.feld = kw.get('feld')
        self.typ = kw.get('typ')
        self.kat = kw.get('kat')
##         self.empty_option = kw.get('empty_option')
        self.aktiviert = kw.get('aktiviert', True)
        self.key = kw.get('key', self.feld)
        assert self.key
        tc = {
            'm': FachstatistikItemMultiKat,
            'k': FachstatistikItemSingleKat,
            's': FachstatistikItemString,
            'i': FachstatistikItemInteger,
            }
        try: self.__class__ = tc[self.typ]
        except: pass
    def get_fs_data(self):
        return self._group._fsdef._fs_data
    def value(self):
        val = self.get_fs_data().get(self.feld)
        return val
    
class FachstatistikItemString(FachstatistikItem):
    def value(self):
        val = self.get_fs_data().get(self.feld)
        if not val:
            val = ''
        return val
class FachstatistikItemInteger(FachstatistikItem):
    def value(self):
        val = self.get_fs_data().get(self.feld)
        if not val:
            val = '0'
        return val
class FachstatistikItemKat(FachstatistikItem):
    pass
class FachstatistikItemSingleKat(FachstatistikItemKat):
    """Falls im fs_data-Objekt kein Wert gefunden wird, kommt eine leere
    Option rein, die auch selektiert ist.
    Falls ein Wert gegeben ist, kommt keine leere Option hinein.
    """
    def options(self):
        codes = get_codes(self.kat)
        selected = self.get_fs_data().get(self.feld)
        if selected == None:
            empty_option = True
            select_first = True
            selected = ''
        else:
            empty_option = False
            select_first = False
        return make_option_list(codes, 'id', 'name',
                                empty_option=empty_option,
                                select_first=select_first,
                                selected=selected)
class FachstatistikItemMultiKat(FachstatistikItemKat):
    """Es werden genau immer diejenigen Optionen selektiert,
    die im fs_data-Objekt angegeben sind.
    """
    def options(self):
        codes = get_codes(self.kat)
        selected = self.get_fs_data().get(self.feld)
        if selected != None:
            #selected = selected.getIds()
            selected = [int(i) for i in selected.split()]
        return make_option_list(codes, 'id', 'name',
                                selected=selected)

    
class FachstatistikGruppe(object):
    def __init__(self, **kw):
        self.legend = kw.get('legend', '')
        self.items = kw.get('items', [])
        self._keys = {}
        for i in self.items:
            self._keys[i.key] = i
        assert self.key
        self.aktiviert = False
        for i in self.items:
            i._group = self
            if i.aktiviert:
                self.aktiviert = True
    def __getitem__(self, key):
        return self._keys[key]
        
class FachstatistikGruppeFalldaten(FachstatistikGruppe):
    def __init__(self):
        self.key = 'falldaten'
        items = [
            FachstatistikItem(name='Fallnummer',
                              feld='fall_fn',
                              typ='s',
                              ),
            FachstatistikItem(name='Mitarbeiter',
                              feld='mit_id',
                              typ='o',
                              ),
            FachstatistikItem(name='Jahr',
                              feld='jahr',
                              typ='i',
                              ),
            ]
        FachstatistikGruppe.__init__(self,
                                     legend='Falldaten',
                                     items=items)
                                     
class FachstatistikGruppeAngabenKlient(FachstatistikGruppe):
    def __init__(self):
        self.key = 'angabenklient'
        FI = FachstatistikItem
        items = [
            FI(name='Planungsraum',
               feld='bz',
               typ='s',
               ),
            FI(name='Geschlecht',
               feld='gs',
               typ='k',
               kat='gs',
               aktiviert=True,
               ),
            FI(name='Alter Kind',
               feld='ag',
               typ='k',
               kat='fsag',
               aktiviert=True,
               ),
            FI(name='Lebensmittelpunkt des Kindes',
               feld='fs',
               typ='k',
               kat='fsfs',
               ),
            FI(name='Empfohlen von',
               feld='zm',
               typ='k',
               kat='fszm',
               ),
            FI(name='Qualifikation Jugendlicher',
               feld='qualij',
               typ='k',
               kat='fsqualij',
               ),
            FI(name='Qualifikation Mutter',
               feld='qualikm',
               typ='k',
               kat='fsquali',
               ),
            FI(name='Qualifikation Vater',
               feld='qualikv',
               typ='k',
               kat='fsquali',
               ),
            FI(name='Beruf Mutter',
               feld='bkm',
               typ='k',
               kat='fsbe',
               ),
            FI(name='Beruf Vater',
               feld='bkv',
               typ='k',
               kat='fsbe',
               ),
            FI(name='Herkunftsland Mutter',
               feld='hkm',
               typ='k',
               kat='fshe',
               ),
            FI(name='Herkunftsland Vater',
               feld='hkv',
               typ='k',
               kat='fshe',
               ),
            FI(name='Alter Mutter',
               feld='agkm',
                              typ='k',
               kat='fsagel',
               ),
            FI(name='Alter Vater',
               feld='agkv',
               typ='k',
               kat='fsagel',
               ),

            ]
        FachstatistikGruppe.__init__(self,
                                     legend='Angaben zum Klienten und dessen Angehörige',
                                     items=items)
class FachstatistikGruppeEinItem(FachstatistikGruppe):
    def __init__(self, item):
        self.key = item.key
        self.item = item
        self.notiz = None
        FachstatistikGruppe.__init__(self,
                                     legend=item.name,
                                     items=[item])
class FachstatistikGruppeEinItemNotiz(FachstatistikGruppe):
    def __init__(self, item, notiz):
        self.key = item.key
        self.item = item
        self.notiz = notiz
        FachstatistikGruppe.__init__(self,
                                     legend=item.name,
                                     items=[item, notiz])
class FachstatistikGruppeEinItemEineNotiz(FachstatistikGruppe):
    def __init__(self, item=None, notiz=None, legend=None):
        assert item or notiz
        self.key = item and item.key or notiz.key
        legend = legend or item and item.name or notiz.name
        self.item = item
        self.notiz = notiz
        FachstatistikGruppe.__init__(self,
                                     legend=legend,
                                     items=[i for i in (item, notiz) if i])
class FachstatistikGruppeTermine(FachstatistikGruppe):
    felder = ['kat', 'kkm', 'kkv', 'kki', 'kpa', 'kfa',
              'ksoz', 'kleh', 'kerz', 'kkonf', 'kson']
    namen = ['Summe', 'KiMu', 'KiVa', 'Kind', 'Paar', 'Familie',
             'Soz.', 'Lehrer', 'Erz.', 'Hilfebespr.', 'Sonst.']
    def __init__(self):
        self.key = 'termine'
        items = [FachstatistikItem(name=fn[1],
                                   feld=fn[0],
                                   typ='i')
                 for fn in zip(self.felder, self.namen)]
        FachstatistikGruppe.__init__(self,
                                     legend='Terminsumme',
                                     items=items)

class FachstatistikDefinition(object):
    """Alle Infos zur Fachstatistik,
    steuert das Formular zur Abfrage der Daten,
    die Darstellung der Ergebnisse und die Konfiguration
    der Fachstatistik.

    Der Fragebogen besteht aus eine Folge von Gruppen.
    Jede Gruppe kommt in einen Kasten (fieldset).
    Jede Gruppe besteht aus einer Folge von Items.
    Gruppen und Items werden jeweils durch eigene Klassen
    dargestellt.


    """
    def __init__(self):
        FI = FachstatistikItem
        FGIN = FachstatistikGruppeEinItemEineNotiz
        _groups = [
            FachstatistikGruppeFalldaten(),
            FachstatistikGruppeAngabenKlient(),
            FGIN(FI(name='Problem 1 bei der Anmeldung',
                    feld='ba1',
                    typ='k',
                    kat='fsba',
                    )
                 ),
            FGIN(FI(name='Problem 2 bei der Anmeldung',
                    feld='ba2',
                    typ='k',
                    kat='fsba',
                    )
                 ),
            FGIN(FI(name='Hauptproblematik Kind / Jugenliche',
                    feld='pbk',
                    typ='k',
                    kat='fspbk',
                    )
                 ),
            FGIN(FI(name='Hauptproblematik der Eltern',
                    feld='pbe',
                    typ='k',
                    kat='fspbe',
                    )
                 ),
            FGIN(FI(name='Problemspektrum Kind / Jugenliche',
                    feld='kindprobleme',
                    typ='m',
                    kat='fspbk',
                    ),
                 FI(name='Andersgeartete Problemlage',
                    feld='no2',
                    typ='s',
                    ),
                 ),
            FGIN(FI(name='Problemspektrum Eltern',
                    feld='elternprobleme',
                    typ='m',
                    kat='fspbe',
                                               ),
                 FI(name='Andersgeartete Problemlage',
                    feld='no3',
                    typ='s',
                    ),
                 ),
            FGIN(FI(name='Erbrachte Leistungen',
                    feld='eleistungen',
                    typ='m',
                    kat='fsle',
                    )
                 ),
            FachstatistikGruppeTermine(),
            FGIN(notiz=FI(name='Notiz',
                          feld='no',
                          typ='s',
                          )
                 ),
            ]
        self._keys = {}
        for g in _groups:
            self._keys[g.key] = g
            g._fsdef = self
        self._keys['dummy_item'] = FachstatistikItem(
            name='', feld='', key='dummy_item', aktiviert=False,)
    def __getitem__(self, key):
        return self._keys[key]
    def _get_items(self):
        for g in groups:
            for i in g:
                yield i
    def _get_groups(self):
        for g in _groups:
            yield g
    items = property(_get_items, None, None)
    groups = property(_get_groups, None, None)
    def set_fs_data(self, fs_data):
        """Bevor die options-Methode eines FachstatistikItem-Objekts
        aufgerufen werden kann, muessen mit dieser Methode die
        Options initialisiert werden.
        """
        self._fs_data = fs_data

fsdef = FachstatistikDefinition()
