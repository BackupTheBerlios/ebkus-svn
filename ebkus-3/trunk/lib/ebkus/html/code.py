# coding: latin-1

"""Module für den Code und die Kategorieen."""

import string

from ebkus.app import Request
from ebkus.config import config
from ebkus.app.ebapi import Kategorie, KategorieList, \
     Tabelle, TabelleList, FeldList, Code, today, cc
from ebkus.app.ebapih import get_codes, get_all_codes, mksel, mk_ausgabe_codeliste
from ebkus.app_surface.code_templates import *
from ebkus.app_surface.standard_templates import *

import ebkus.html.htmlgen as h
from ebkus.html.akte_share import akte_share

class codelist(Request.Request, akte_share):
    """Tabellarische Liste der Kategorien und Codes. """
    permissions = Request.CODE_PERM
    def processForm(self, REQUEST, RESPONSE):
        # hier gibts eine gewisse Verwirrung zwische Tabelle und Klasse:
        # Tabellen(lang)name und Klassennamen sind meistens identisch,
        # aber Klassennamen enthalten keine Leerzeichen, sind also besser
        # URL-Parameter zu gebrauchen
        klass = self.form.get('tbl')
        if not klass or klass == 'Alle':
            kats = KategorieList(where='')
            title = "Alle Kategorien und Merkmalslisten im &Uuml;berblick"
        else:
            tab_id = Tabelle(klasse=klass)['id']
            kats = KategorieList(
                where='', 
                join=[('feld', 'kategorie.id=feld.kat_id and feld.tab_id=%s' % tab_id)]) 
            title = "Kategorien und Merkmalslisten für %s" % klass

        nicht_anzeigen = ('verwtyp', 'config',)
        zusaetzlich_anzeigen = {
            'Jugendhilfestatistik2007': ['jghag',],
            'Beratungskontakt': ['kdbs',],
            }
        for kl in zusaetzlich_anzeigen:
            if kl == klass:
                kats += [Kategorie(code=k) for k in zusaetzlich_anzeigen[klass]]
        kats = kats.filter(lambda x: x['code'] not in nicht_anzeigen) 
        kats.sort('name')
        for k in kats:
            k['klassen'] = [t['klasse'] for t in TabelleList(
                where='',
                join=[('feld', 'tabelle.id=feld.tab_id and feld.kat_id=%s' % k['id'])])
                            .sorted('klasse')]
        
        uebersicht = h.FieldsetDataTable(
            # Sprungziel sollte eigentlich in 'menu', weil das ganz oben auf der
            # Seite ist. Das hat aber kein legend-text, und IE mag da nicht
            # hinspringen.
            anchor="top",
            legend="Übersicht Kategorien",
            headers=('Kategorie', 'Dokumentation', 'Verwendet in'),
            daten=[[h.Link(string="%(name)s" % k,
                           url="#%(id)s" % k),
                    h.String(string=k['dok'] or ''),
                    h.String(string='<br>'.join([kln for kln in k['klassen']])),
                    ]
                   for k in kats],
            )
        zeile_mit_icon = h.Tr(
            cells=[h.Icon(href="#top",
                          icon= "/ebkus/ebkus_icons/button_go_top.gif",
                          tip="Nach oben",
                          align="left",
                          ),
                   #h.DummyItem(n_col=5),
                   ]
            )
        codetables = [self.get_code_tabelle(k, view="codelist__%s" % klass) for k in kats]
        codelist = []
        for c in codetables:
            codelist.append(c)
            codelist.append(zeile_mit_icon)
        res = h.FormPage(
            title=title,
            help=False,
            name="",action="",method="",
            breadcrumbs = (('Administratorhauptmenü', 'menu'),
                           ),
            rows=(self.get_hauptmenu(),
                  uebersicht,) +
                  tuple(codelist),
            hidden=(),
            )
        return res.display()
        
class oldcodelist(Request.Request):
    """Tabellarische Liste der Kategorien und Codes. """
    
    permissions = Request.CODE_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        user = self.user
        
        katliste = KategorieList(where = "code <> '%s' " % "verwtyp",
                                 order = 'name')
        
        # Headerblock, Menue u. Überschrift fuer das HTML-Template
        
        header = {'titel': 'Kategorielisten',
                  'ueberschrift':
                  '<A name="top"> </A>'}
        
        # Liste der Templates als String
        
        res = []
        res.append(head_normal_ohne_help_t %("Alle Kategorie- und Merkmalslisten im &Uuml;berblick"))
        res.append(katuebersichtstart_t)
        for k in katliste:
            if k['code'] != 'fsag' and k['code'] != 'fsagel' and k['code'] != 'ag':
                k['doku'] = k.get('dok') or ''
                res.append(katuebersichtitem_t % k)
                feldliste = FeldList(where = 'kat_id = %s' %k['id'])
                for f in feldliste:
                    res.append(katuebersichtdbtabellen_t %f)
                res.append(katuebersichtende_t)
        res.append(katuebersichtgesamtende_t)
        
        for k in katliste:
            if k['code'] != 'fsag' and k['code'] != 'fsagel' and k['code'] != 'ag':
                res.append(thkat_t % k)
                res.append(thcodeliste_t)
                cliste = get_all_codes(k['code'])
                mk_ausgabe_codeliste(res, codelisten_t, cliste)
                res.append(code_liste_ende)
                res.append(hreftop_t % "codelist#top")
        res.append(katuebersichtende2_t)
        return string.join(res, '')
        
        
class codetab(Request.Request):
    """1 Code-Tabelle."""
    
    permissions = Request.CODE_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        tabelle = self.form.get('tabelle')
        kat_id = self.form.get('kat_id')
        kat_name = self.form.get('kat_name')
        if not tabelle and not kat_id:
            self.last_error_message = "Keine ID fuer Tabelle bzw. Kategorie erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
        if tabelle:
            tliste = TabelleList(where = "klasse = '%s'" % tabelle)

            if len(tliste) == 1:
                tab = tliste[0]
                felder = tab['felder']
                felder.sort('kat_id__name')

            res = []
            res.append(head_normal_ohne_help_t %('Kategorie- und Merkmalslisten zu: '+ "'%s'" % tabelle))
            res.append(code_tab_start_t)
            x = []
            for f in felder:
                if f['kat_id'] and f['kat_id'] not in x:
                    a = felder.find('kat_id', f['kat_id'])
                    if len(a) >= 1:
                        x.append(f['kat_id'])
                        k = Kategorie(f['kat_id'])
                        res.append(thkat_t % k)
                        res.append(thcodeliste_t)
                        cliste = get_all_codes(k['code'])
                        mk_ausgabe_codeliste(res, codelisten_t, cliste)
                        res.append(code_liste_ende)
                        res.append(hreftop_t % "codetab?tabelle=%s#top" % tabelle)
            res.append(katuebersichtende2_t)
            return string.join(res, '')

class _code(Request.Request, akte_share):
    def _process(self,
                 title,
                 file,
                 code,
                 view,
                 ):
        kat = code['kat']
        # view gibt an, welche Seite nach dem Speicher gezeigt werden soll
        # (siehe administration.py)
        if view == 'updkat': # Aufruf erfolgte von updkat
            view = 'updkat?katid=%(id)s' % kat
        elif view.startswith('codelist__'): # Aufruf erfolgte von codelist
            view = 'codelist?tbl=%s#%s' % (view.split('__')[1], kat['id'])
        new = (file == 'codeeinf')
        bereichskategorie = bool(kat['code']=='dbsite' or FeldList(
            where="kat_id=%s and verwtyp=%s" % (kat['id'], cc('verwtyp', 'b'))))
        legend = (new and "Merkmal hinzufügen für Kategorie '%(name)s'" % kat or
                  "Merkmal bearbeiten aus Kategorie '%(name)s'" % kat)
        code_edit = h.FieldsetInputTable(
            legend=legend,
            daten=[[new and h.TextItem(label="Code",
                                       name="code",
                                       value=code['code'],
                                       tip="Code für das Merkmal",
                                       class_="textboxmid")
                    or h.TextItem(label="Code",
                                  name="code",
                                  value=code['code'],
                                  tip="Code für das Merkmal",
                                  readonly=True,
                                  class_="textboxmid"),
                    h.TextItem(label="Name",
                               name="name",
                               value=code['name'],
                               tip="Name des Merkmals",
                               n_col=4,
                               class_="textbox310"),
                    ],
                   bereichskategorie and
                   [h.TextItem(label="Minimum",
                               name="mini",
                               value=code['mini'] or '',
                               tip="Minimaler Wert des Bereichs (nur für Bereichskategorien, z.B. Anzahl Termine)",
                                                     class_="textboxmid"),
                    h.TextItem(label="Maximum",
                               name="maxi",
                               value=code['maxi'] or '',
                               tip="Maximaler Wert des Bereichs (nur für Bereichskategorien, z.B. Anzahl Termine)",
                               class_="textboxmid"),
                    h.SelectItem(label="Position",
                                 name='sort',
                                 tip='Position in der Liste der Merkmale festlegen',
                                 class_='listbox30',
                                 options=self.for_code_sort(kat, sel=code['sort'])),
                    ] or None,
                   not new and
                   [h.CheckItem(label="Deaktiviert",
                                name='off',
                                value="1",
                                checked=code['off'] == 1,
                                tip='Merkmal deaktivieren'),
                    h.DatumItem(label="Seit",
                                noday=True,
                                name="d",
                                month=code['dm'] or '',
                                year=code['dy'] or '',
                                tip="Monat und Jahr der Deaktivierung"),
                    not bereichskategorie and
                    h.SelectItem(label="Position",
                                 name='sort',
                                 tip='Position in der Liste der Merkmale festlegen',
                                 class_='listbox30',
                                 options=self.for_code_sort(kat, sel=code['sort']))
                    or h.DummyItem(),
                    ] or None,
                   new and not bereichskategorie and
                   [h.DummyItem(),
                    h.DummyItem(),
                    h.SelectItem(label="Position",
                                 name='sort',
                                 tip='Position in der Liste der Merkmale festlegen',
                                 class_='listbox30',
                                 options=self.for_code_sort(kat, sel=code['sort'])),
                    ] or None,
                   [h.TextItem(label="Dokumentation",
                               name="dok",
                               value=code['dok'] or '',
                               tip="Dokumentation für das Merkmals",
                               n_col=6,
                               class_="textboxverylarge"),
                    ],
                   ],
            )

        if view.startswith('updkat'):
            breadcrumbs = (('Administratorhauptmenü', 'menu'),
                           ('Fachstatistik konfigurieren', 'fskonfig'),
                           ('Kategorie bearbeiten', view),
                           )
        elif view.startswith('codelist'):
            breadcrumbs = (('Administratorhauptmenü', 'menu'),
                           ('Kategorien und Merkmalslisten', view),
                           )
        res = h.FormPage(
            title=title,
            help=False,
            name="codeform",action="admin",method="post",
            breadcrumbs = breadcrumbs,
            rows=(code_edit,
                  self.get_code_tabelle(kat, links=False),
                  h.SpeichernZuruecksetzenAbbrechen(),
            ),
            hidden=(('katid', "%(id)s" % kat),
                    ('katcode', "%(code)s" % kat),
                    ('codeid', "%(id)s" % code),
                    ('view', view),
                    ('file', file),
                    ),
            )
        return res.display()


class codeneu(_code):
    """Eingabeformular fuer neuen Code."""
    permissions = Request.ADMIN_PERM
    def processForm(self, REQUEST, RESPONSE):
        katid = self.form.get('katid')
        view = self.form.get('view')
        if not katid:
            self.last_error_message = "Keine ID fuer das Item erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
        kat = Kategorie(katid)
        code = Code()
        code.init(
            id=Code().getNewId(),
            kat_id=kat['id'],
            kat_code=kat['code'],
            code='',
            name='',
            mini=None,
            maxi=None,
            dm=None,
            dy=None,
            sort=max([c['sort'] for c in kat['codes']]) + 1,
            off=0,
            dok='',
            )
        return self._process(title='Merkmal hinzufügen',
                             file='codeeinf',
                             code=code,
                             view=view,
                             )
        

class updcode(_code):
    """Updateformular fuer den Code."""
    permissions = Request.ADMIN_PERM
    def processForm(self, REQUEST, RESPONSE):
        codeid = self.form.get('codeid')
        view = self.form.get('view', '')
        if not codeid:
            self.last_error_message = "Keine ID fuer das Item erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
        code = Code(codeid)
        return self._process(title='Merkmal bearbeiten',
                             file='updcode',
                             code=code,
                             view=view,
                             )

class updkat(Request.Request, akte_share):
    """Wird sowohl mit GET und id als auch mit POST und Daten
    aufgerufen.
    """
    permissions = Request.CODE_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        kat_id = self.form.get('katid')
        if not kat_id:
            self.last_error_message = "Keine ID fuer Kategorie erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
        kat = Kategorie(kat_id)
        kat_name = self.form.get('name')
        if kat_name:
            from ebkus.app.ebupd import updkategorie
            updkategorie(self.form)
        kategorie_edit = h.FieldsetInputTable(
            legend="Kategorie '%(name)s' bearbeiten" % kat,
            daten=[[h.TextItem(label="Kategoriename",
                               name="name",
                               value=kat['name'],
                               tip="Namen der Kategorie ändern",
                               class_="textboxlarge")
                    ],
                   [h.TextItem(label="Dokumentation",
                               name="dok",
                               value=kat['dok'] or '',
                               tip="Dokumentation für die Kategorie",
                               class_="textboxverylarge")
                    ]
                   ],
            )
        res = h.FormPage(
            title='Kategorie bearbeiten',
            help=False,
            name="katform",action="admin",method="post",
            breadcrumbs = (('Administratorhauptmenü', 'menu'),
                           ('Fachstatistik konfigurieren', 'fskonfig'),
                           ),
            rows=(kategorie_edit,
                  self.get_code_tabelle(kat, view='updkat'),
                  h.SpeichernZuruecksetzenAbbrechen(abbrechen='fskonfig'),
                  ),
            hidden=(('katid', "%(id)s" % kat),
                    #('view', 'updkat?katid=%(id)s' % kat),
                    ('view', 'fskonfig'),
                    ('file', 'updkategorie'),
                    ),
            )
        return res.display()

        
