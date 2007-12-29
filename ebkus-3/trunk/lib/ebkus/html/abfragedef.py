# coding: latin-1
import re
import time
from ebkus.db.sql import SQL
from ebkus.app import Request
from ebkus.app import ebapi
from ebkus.app.ebapih import get_codes
from ebkus.config import config
from ebkus.html.strkat import get_strasse
import ebkus.html.htmlgen as h
from ebkus.html.fskonfig import fs_customize as fsc

"""
Eine Query wird durch eine Liste von strings repräsentiert.
"""

class abfragedef(Request.Request):
    permissions = Request.ABFR_PERM
    def _process(self,
                 abfr,
                 cgi_name,
                 ):
        #print 'ABFRAGEDEF', cgi_name, abfr
        q = Query(abfr)
        definition = q.get_anzeige()
        daten = q.gen_html()
        abfr_id = abfr.get('id') # muss keine haben
        meta = h.FieldsetInputTable(
            legend='Name und Beschreibung',
            daten=[[h.TextItem(label='Name',
                               name='name',
                               value=abfr['name'],
                               ),
                    # Mitarbeiter und Zeit des letzten Updates anzeigen
                    h.String(string='Letzte Änderung: %s %s' %
                             (time.strftime('%d.%m.%Y', time.localtime(abfr['zeit'])),
                              abfr['mit__na']),
                             class_='normaltext',
                             ),
                    ],
                   [h.TextItem(label='Beschreibung',
                               name='dok',
                               value=abfr['dok'],
                               class_='textboxverylarge',
                               n_col=3,
                               ),
                    ],
                   ],
            )
        anzeige = h.FieldsetDataTable(
            legend = 'Definition der Teilmenge',
            daten=[[h.String(string=definition)]],
            )
        define_query = h.FieldsetInputTable(
            legend='Definition bearbeiten',
            daten=daten
            )
        buttons = h.FieldsetInputTable(daten=[[
            h.Button(value="Speichern",
                     name='op',
                     tip="Teilmengendefinition speichern",
                     type='submit',
                     ),
            h.Button(value="Weiter",
                     name='op',
                     tip="Weiter bearbeiten ohne zu speichern",
                     type='submit'
                     ),
            h.Button(value="Abbrechen",
                     name='op',
                     tip="Zurück zur Statistikabfrage ohne zu speichern",
                     type='submit',
                     ),
            ]])
        res = h.FormPage(
            title='Teilmenge für Statistikabfrage definieren',
            name="abfragedef",
            #action="abfragedef",
            action="statabfr", # wird über file gesteuert wie bei klkarte
                               # file=='abfragedef' and op=='Speichern' -->
                               # ebupd.upd_or_einf_abfr
            method="post",
            hidden = (('abfrid', abfr_id and abfr_id or ''),
                      ('file', 'abfragedef'),
                      # Mit diesem Mitarbeiter wird das update durchgeführt
                      ('mitid', self.mitarbeiter['id']),
                      ),
            rows=(meta,
                  anzeige,
                  define_query,
                  buttons,
##                   h.SpeichernZuruecksetzenAbbrechen(name='op',
##                                                     value='Speichern',
##                                                     onclick_abbrechen=
##                                                     "opener.location.reload();window.close();",
##                                                     ),
                  ),
            )
        return res.display()

    def processForm(self, REQUEST, RESPONSE):
        #print 'FORM abfragedef', self.form
        op = self.form.get('op')
        cgi_name = 'query1'
        assert op in (None, 'new', 'edit', 'del', 'Weiter')
        abfr_id = self.form.get('abfrid')
        if abfr_id:
            abfrold = ebapi.Abfrage(abfr_id)
        else:
            abfrold = None
        if op in ('edit', 'del'):
            # altes Objekt ist vorhanden, nur das wird dargestellt
            if not abfr_id:
                raise ebapi.EE('Keine ID für Abfrage')
            name = abfrold['name']
            if op == 'del':
                return h.SubmitOrBack(
                    legend='Teilmengendefinition löschen',
                    action='statabfr',
                    #onclick_abbrechen="window.close()",
                    method='post',
                    hidden=(('abfrid', abfr_id),
                            ('file', 'rmabfr'), # wird in statabfr abgefragt -->
                                                # ebupd.rmabfr
                            ),
                    zeilen=("Soll Teilmengendefinition '%s' gelöscht werden?" % name,
                            )
                    ).display()
##             elif op == 'del_immed':
##                 abfrold.delete()
##                 return h.Meldung(legend='Teilmengendefinition gelöscht',
##                                  zeilen=("Die Teilmengendefinition '%s' wurde gelöscht." % name,),
##                                  onClick="opener.location.reload();history.back();",
##                                  ).display()
            else:
                #op == 'edit':
                return self._process(abfrold, cgi_name)
        elif op == 'new':
            # default Objekt bauen, in Form steht nichts
            abfr = ebapi.Abfrage()
            abfr.init(zeit=time.time(),
                      mit_id=self.mitarbeiter['id'],
                      name='',
                      dok='',
                      value='',
                      typ='statistik_teilmengen_definition',
                      )
        else:
            # Objekt aus den Form-Parametern bauen
            query_list = ebapi.check_list(self.form,
                                          cgi_name,
                                          'Keine Query',
                                          [])
            #print 'QUERY_LIST for q', query_list
            q = Query(query_list)
            #print 'QUERY_STRING from q', q.get_query_string(),
            name=self.form.get('name', '')
            # name nicht prüfen, darf leer sein, solange nicht gespeichert wird
            if abfrold:
                # Solange nicht gespeichert, immer die alten Daten anzeigen
                zeit = abfrold['zeit']
                mit_id = abfrold['mit_id']
            else:
                zeit = time.time()
                mit_id = self.mitarbeiter['id']
            abfr = ebapi.Abfrage()
            abfr.init(id=abfr_id,
                      zeit=zeit,
                      mit_id=mit_id,
                      name=name,
                      dok=self.form.get('dok', ''),
                      value=q.get_query_string(),
                      typ='statistik_teilmengen_definition',
                      )
##         if op == 'Speichern':
##             if abfrold:
##                 file = 'updabfr'
## ##                 abfrold.update(abfr)
## ##                 abfr = abfrold
##             else:
##                 file = 'abfreinf'
## ##                 abfr.new()
## ##                 abfr.insert()
        #print 'ABFR vor HTML', abfr
        return self._process(abfr, cgi_name)

class Query(object):
    """Baum.
    CGI-Namen: 0 Root, 00 erstes Kind, 010 erstes Kind des zweiten Kindes von root
    f id von einem Feld
    o Ort
    i int
    s 
    """
    def __init__(self, 
                 arg=None,          # Abfrage-DB-Instanz
                                    # Liste, z.B. von CGI
                                    # String, zB aus der Abfrage-Instanz
                 name=None,
                 cgi_name='query1', # nur für HTML Generierung

##                  query_list=None,   # Liste von form, evt. nur ein String, evt. leere
##                                     # Strings als Elemente
##                  query_string=None, # Gespeicherter String, syntaktisch korrekt, kann leer sein
##                  abfrage=None,      # Abfrage-Datenbankobjekt
        ):
        if not arg:
            arg = []
        self.cgi_name = cgi_name
        self.name = '' # kann überschrieben werden, s.u.
        if isinstance(arg, ebapi.Abfrage):
            query_string = arg['value']
            self.name =  arg['name']
            query_list = query_string.split()
        elif isinstance(arg, list):
            query_list = [q for q in arg if q]
        elif isinstance(arg, basestring):
            query_list = arg.split()
        else:
            raise ebapi.EE("Falsche Argumente für Query") # sollte nie passieren
        if not query_list:
            query_list = ['00_ALL']
            self.name = 'Alle'
        if name != None:
            self.name = name
        try:
            self.raw_query_map = dict([(s.split('_')[0],
                                        s.split('_')[1])
                                       for s in query_list if s])
        except Exception, e:
            raise # ebapi.EE("Fehler in Parameter für Abfrage: %s" % e)
        # Wird von Primitivknoten gesetzt um zu registrieren, ob Fachstatistik.
        # Bundesstatistik oder Ortsangaben in der Query verwendet werden.
        self.uses = [False,False,False] 
        #self.maxdepth = max([len(k) for k in self.raw_query_map.keys()]) / 2
        #print 'QUERY MAP vor dem build', self.raw_query_map
        #self.root = Condition.build_query(self, '00')
        self.root = build_query(self, '00')
        if not self.root:
            # wurde abgwählt
            self.root = All(self, '00')
        self.fs = self.uses[0]
        self.jgh = self.uses[1]
        self.ort = self.uses[2]
    def get_query_list(self):
        return ['%s_%s' % (i,v) for i,v in self.raw_query_map.items()]
    def get_query_string(self):
        return ' '.join(self.get_query_list())
    def gen_html(self):
        data = []
        row = []
        self.root.gen(data, row)
        self._fill(data)
        #self._test(data)
        return data
    def _fill(self, data):
        "n_col bei items setzten, so dass jede Zeile die gleich Anzahl Zellen überspannt."
        max_colspan = max([sum([item.n_col for item in row]) for row in data])
        for row in data:
            n_cells = sum([item.n_col for item in row])
            row[-1].n_col = max_colspan - n_cells + row[-1].n_col
##     def _test(self, data):
##         "Jede Zeile überspannt max_colspan Zellen"
##         max_colspan = max([sum([item.n_col for item in row]) for row in data])
##         print 'ZELLEN NACH:', max_colspan
##         for row in data:
##             n_cells = sum([item.n_col for item in row])
##             assert n_cells == max_colspan
    def get_anzeige(self):
        anzeige = self.root.get_anzeige().strip()
        #print 'QUERY anzeige', anzeige
        if anzeige:
            return anzeige
        else:
            return '&lt;keine Bedingungen&gt;'
    def test(self, element):
        #print element
        #print self.root
        return self.root.test(element)
    def always_true(self):
        return isinstance(self.root, All)


# @classmethod # geht nicht wg. python2.3
# def build_query(cls, query, index):
def build_query(query, index):
    """Factory für die Objekte im Baum außer den Values der
    primitiven Objekten, den eigentlichen Blättern.
    """
    str = query.raw_query_map.get(index)
    #print 'BUILD_QUERY str', str
    if str == None:
        return None
    elif str == 'ALL':
        cond = All(query, index)
    elif str == 'UND':
        cond = And(query, index)
    elif str == 'ODER':
        cond = Or(query, index)
    elif str == 'NICHT':
        cond = Not(query, index)
    elif str.startswith('f'):
        field = ebapi.Feld(str[1:])
        #print 'BUILD_QUERY field', field
        verwtyp = field['verwtyp__code']
        if verwtyp == 'k':
            cond = SingleKatFeld(query, index, field)
        elif  verwtyp == 'm':
            cond = MultiKatFeld(query, index, field)
        elif  verwtyp == 'f':
            cond = ObjFeld(query, index, field)
    elif str.startswith('o'):
        feldname = str[1:]
        cond = Ortsangabe(query, index, feldname)
    else:
        raise ebapi.EE('build_query: unkown value: %s' % str)
    cond.build_query_children()
    return cond

class Condition(object):
    "Abstract super class"
    index_size = 2 # maximal 100 Kinder eines Knotens
    def build_query_children(self):
        pass
    def index_code(self):
        """Aufgrund dieses Strings, der als CGI-Wert verwendet wird,
        kann das Objekt als Teil der Query rekonstruiert werden.
        Der Index verweist auf einen Knoten im Query-Baum, der Code
        auf das Objekt.
        """
        return "%s_%s" % (self.index, self.code())
    def get_anzeige(self):
        #print 'CONDITION anzeige', ''
        return ''
    def get_children_values(self):
        """Liste von Kindern:  nur die Wert"""
        map = self.query.raw_query_map
##         keys_for_values = [k for k in map.keys()
##                            if k.startswith(self.index) and k != self.index]
        return [map[k] for k in self.get_children_indexes()]
    def get_children_indexes(self):
        """Liste von Kindern:  nur die Indexe"""
        map = self.query.raw_query_map
        size = len(self.index) + self.index_size # um nur die Kinder zu kriegen, nicht die Kindeskinder
        keys_for_values = [k for k in map.keys()
                           if k.startswith(self.index) and len(k) == size]
        return keys_for_values
    def gen_more(self, data, row, index):
        row.append(h.SelectItem(name=self.query.cgi_name,
                                n_col=3,
                                nolabel=True,
                                onChange="submit()",
                                tip='Bedingung hinzufügen',
                                options=self.get_options(index)))
        data.append(row)
    def get_options(self, index):
        "Optionen für die Bedingungswahl für benutzerdefinierte Teilmengen"
        tmpl = '<option value="%s">%s</option>'
        options = [tmpl % ('', '[Neue Bedingung]')]
        for op in ('UND', 'ODER', 'NICHT'):
            qstr = "%s_%s" % (index, op)
            options.append(tmpl % (qstr, op))
        options += [tmpl % ('', '[Regionen]')]
        for f in ([('plraum', 'Planungsraum'),
                  ('ort', 'Ort'),
                  ('plz', 'PLZ')] +
                  [(f, f.capitalize())
                   for f in config.STRASSENSUCHE.split() if f != 'ort']):
            qstr = "%s_o%s" % (index, f[0])
            options.append(tmpl % (qstr, f[1]))
        options += [tmpl % ('', '[Fachstatistik]')]
        for f in fsc.standard_felder + fsc.joker_felder:
            # nur Kategorien
            if not fsc.deaktiviert(f):
                feld = fsc.get(f)
                qstr = "%s_f%s" % (index, feld['id'])
                options.append(tmpl % (qstr, feld['name']))
        options += [tmpl % ('', '[Bundesstatistik]')]
        for f in ('hilf_art', 
                  'hilf_ort', 
                  'traeger', 
                  'gs', 
                  'aort_vor', 
                  'sit_fam', 
                  'ausl_her', 
                  'vor_dt', 
                  'wirt_sit', 
                  'aip', 
                  'ees', 
                  'va52', 
                  'rgu', 
                  'gr1', 
                  'gr2', 
                  'gr3', 
                  'nbkges', 
                  'lbk6m', 
                  'grende', 
                  'aort_nac', 
                  'unh', 
                  ):
            feld = ebapi.get_feld(f, klasse='Jugendhilfestatistik2007')
            qstr = "%s_f%s" % (index, feld['id'])
            options.append(tmpl % (qstr, feld['name']))
        return '\n'.join(options)
class All(Condition):
    def __init__(self, query, index=None):
        self.query = query
        self.index = index
        self.conditions = []
    def test(self, element):
        return True
    def code(self):
        return 'ALL'
    def gen(self, data, row):
        self.gen_more(data, row, self.index)
class _AndOrNOT(Condition):
    def __init__(self, query, index):
        self.query = query
        self.index = index
        self.conditions = []
    def get_anzeige(self):
        anzeige = (' %s ' % self.code()).join(
            [c.get_anzeige() for c in self.conditions
             if c.get_anzeige()])
        #print '_AndOrNOT anzeige', anzeige
        if anzeige:
            return '(%s)' % anzeige
        else:
            return ''
    def code(self):
        return self.op
    def build_query_children(self):
        for k in self.get_children_indexes():
            #c = self.build_query(self.query, k)
            c = build_query(self.query, k)
            if c:
                self.conditions.append(c)
    def get_conditions_with_joker(self):
        n_subs = len(self.conditions)
        # self.index der wird vom Aufrufer gesetzt
        all1 = All(self.query)
        all2 = All(self.query)
        # immer ein Selektor am Ende
        extras = [all1]
        if n_subs == 0:
            # 2 Selektoren, wenn noch gar keine Bedinungen da sind
            extras.append(all2)
        return self.conditions + extras
    def gen(self, data, row):
        """Nur eine Auswahlbox am Ende, außer:
        Wenn keine Bedinungen da sind, zwei Auswahlboxen.
        """
        first = True
        for i,c in enumerate(self.get_conditions_with_joker()):
            c.index = "%s%02d" % (self.index, i)
            if i == 0:
                row.append(h.CheckItem(label=self.op,
                                       checked=True,
                                       label_class='tabledatabold',
                                       name=self.query.cgi_name,
                                       value=self.index_code(),
                                       class_='tabledatabold',
                                       tip2='Bedingung entfernen',
                                       onClick='submit()',
                                       n_col=3,
                                       ))
            else:
                row = [h.DummyItem(n_col=3)]*(len(self.index)/2-1)
                row.append(h.String(string=self.op,
                                    n_col=3,
                                    class_='tabledatabold',
                                    ))
            c.gen(data, row)
class And(_AndOrNOT):
    op = 'UND'
    def build_query_children(self):
        "Bei der Konjunktion prüfen, ob Ortsangaben mit drin sind."
        "Die möglich Werte können sich gegenseitig einschränken"
        for k in self.get_children_indexes():
            #c = self.build_query(self.query, k)
            c = build_query(self.query, k)
            if c:
                self.conditions.append(c)
        ort_c = [c for c in self.conditions
                 if isinstance(c, Ortsangabe)]
        for c in ort_c:
            # Ortsangaben kennen nun ihre Ortsgeschwister
            c.ort_siblings = ort_c
                
    def test(self, element):
        for c in self.conditions:
            if not c.test(element):
                return False
        return True
class Or(_AndOrNOT):
    op = 'ODER'
    def test(self, element):
        for c in self.conditions:
            if c.test(element):
                return True
        return False
class Not(_AndOrNOT):
    op = 'NICHT'
    def get_anzeige(self):
        if self.conditions:
            anzeige = self.conditions[0].get_anzeige()
            if anzeige:
                return ' %s %s ' % (self.code(), anzeige)
        return ''
    def test(self, element):
        if self.conditions and self.conditions[0].test(element):
            return False
        return True
    def get_conditions_with_joker(self):
        if self.conditions:
            return self.conditions
        else:
            # ein Selektor ('joker') wenn keine Bedingung da ist
            all1 = All(self.query)
            return [all1]
class Primitive(Condition):
    index_size = 3 # maximal 1000 Kinder
    def build_query_children(self):
        self.values = [self.value_conv(v) for v in self.get_children_values()]
        #print 'BUILD_QUERY_CHILDREN', self.values
    def get_anzeige(self):
        anzeige_values = self.get_anzeige_values()
        if anzeige_values:
            return ' %s = %s ' % (self.name(),anzeige_values)
        else:
            return ''
    def get_anzeige_values(self):
        anzeige = ' oder '.join(["'%s'" % self.value_name(v) for v in self.values])
        return anzeige
    def gen(self, data, row):
        row.append(h.CheckItem(label=self.name(),
                               label_class='tabledatabold',
                               class_='tabledatabold',
                               name=self.query.cgi_name,
                               onClick='submit()',
                               value=self.index_code(),
                               tip2='Bedingung entfernen',
                               checked=True,
                               ))
        row.append(h.String(string='ist',
                            ))
        data.append(row)
        self.gen_values(data)
    def gen_values(self, data):
        first = True
        for i,v in enumerate(self.possible_values()):
            row = [h.DummyItem(n_col=3)]*(len(self.index)/2-1)
            row += [h.String(string='oder'),
                    h.CheckItem(label=self.value_name(v),
                                name=self.query.cgi_name,
                                value=self.value_index_code(i, v),
                                checked=(v in self.values),
                                )
                    ]
            data.append(row)
    def test(self, pair_or_instance):
        if isinstance(pair_or_instance, tuple):
            return self._test(pair_or_instance[self.ref])
        else:
            return self._test(pair_or_instance)
class Feld(Primitive):
    value_conv = int
    tab2ref = {'fachstat': 0, 'jghstat07': 1}
    def __init__(self, query, index, feld):
        self.query = query
        self.index = index
        self.feld = feld
        tabelle = self.feld['tab__tabelle']
        self.ref = self.tab2ref[tabelle]
        self.query.uses[self.ref] = True
        self.values = []
    def code(self):
        return 'f%s' % self.feld['id']
    def name(self):
        return self.feld['name']
    def value_index_code(self, index, value):
        # 03 == index_size
        return "%s%03d_%s" % (self.index, index, value)
class KatFeld(Feld):
    def possible_values(self):
        return [c['id'] for c in get_codes(self.feld['kat_code'])]
    def value_name(self, value):
        return ebapi.Code(value)['name']
class SingleKatFeld(KatFeld):
    def _test(self, element):
        return element[self.feld['feld']] in self.values
class MultiKatFeld(SingleKatFeld):
    def _test(self, element):
        # Felder mit oder verknüpft
        for id in element[self.feld['feld']].split():
            if int(id) in self.values:
                return True
        return False
# TBD fehlt noch einiges für Mitarbeiter zB
# später. Erst mal nur Kat und Ort Bedingungen
class ObjFeld(Feld):
    def _test(self, element):
        return element[self.feld['feld']] in self.values
    def possible_values(self):
        pass
class Ortsangabe(Primitive):
    value_conv = str
    def __init__(self, query, index, feldname):
        self.query = query
        self.index = index
        # feldname: ort, ortsteil, bezirk, plz, samtgemeinde, plraum
        # true_values: Berlin, Mitte, Friedenau, 12067, Baddenstedt
        self.feldname = feldname
        self.values = []
        self.ort_siblings = []
        self.ref = 0 # immer Fachstatistik
        self.query.uses[2] = True
    def name(self):
        return self.feldname
    def value_name(self, value):
        return value
    def value_index_code(self, index, value):
        # 03 == index_size
        return "%s%03d_%s" % (self.index, index, value)
    def possible_values(self):
        # DONE TODO evt. einschränken wenn auch andere Felder des
        # Straßenkatalogs eingeschränkt sind (PLZ, Planungsräume, Bezirk)
        # --> sind noch andere in der gleich Konjunktion?
        #self.ort_siblings
        # Einschränkungen: wenn bezirk,ort,samtgemeinde ---> planungsraum, plz
        # nicht einschränken: planungsr,plz --> ort, bezirk,
        # Falls innerhalb desselben 'UND' eine der Ortsangaben ort, bezirk, samtgemeinde
        # als Bedingung vorhanden ist, werden die Auswahlmöglichkeiten für planungsr, plz
        # eingschränkt auf die mit der Bedinung kompatiblen.
        if config.STRASSENKATALOG:
            where = ''
            if self.feldname in ('plz', 'planungsr'):
                sibls = [s for s in self.ort_siblings
                         if s.feldname in ('ort', 'bezirk', 'samtgemeinde') and
                         s.feldname != self.feldname and
                         s.values]
                where = ' and '.join(["%s in (%s)" %
                                      (s.feldname, ', '.join(["'%s'" % v
                                                              for v in s.values]))
                                      for s in sibls])
                if where:
                    where = 'where %s' % where
            if self.feldname == 'planungsr':
                feld = 'plraum'
            else:
                feld = self.feldname
            return [t[0] for t in SQL(
                "select distinct %s from strkatalog %s order by %s" %
                (feld, where, feld)).execute()]
        else:
            # Einschränkungen ohne Strkat: nein
            assert self.feldname in ('ort', 'plz', 'planungsr')
            return [t[0] for t in SQL(
                "select distinct %s from akte order by %s" %
                (self.feldname, self.feldname)).execute()]
            
    def _test(self, element):
        #aktewert = element['fall__akte__' + self.feldname]
        fswert = element[self.feldname]
        #akteid = element['fall__akte_id']
        #print 'ORTSANGABE _test', akteid, aktewert, self.values
        return fswert in self.values
        #return aktewert in self.values
    def code(self):
        return 'o%s' % self.feldname
