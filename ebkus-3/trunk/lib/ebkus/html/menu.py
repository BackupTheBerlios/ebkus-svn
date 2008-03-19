# coding: latin-1
import string
from ebkus.app import Request
from ebkus.app.ebapi import today, ZustaendigkeitList, TabelleList, \
     register_set, register_get
from ebkus.app_surface.menu_templates import *
from ebkus.app_surface.standard_templates import *
from ebkus.config import config

import ebkus.html.htmlgen as h
from ebkus.html.akte_share import akte_share

class menu(Request.Request, akte_share):
    permissions = Request.MENU_PERM

    def get_abmelden_pw(self):
        return h.FieldsetInputTable(
            daten=[[h.Button(value='Abmelden',
                             onClick="go_to_url('logout')",
                             tip="Logout",
                             ),
                    h.Button(value='Passwort ändern',
                             onClick="go_to_url('pwchange')",
                             tip="Passwort ändern",
                             ),
                    ]]
            )
    def _hauptmenu_klienten(self):
        logo_mitarbeiter_uhr = h.Table(
            rows=(
##                        (h.Icon(href="/ebkus/%s/index.html" % config.INSTANCE_NAME,
##                                      icon="/ebkus/ebkus_icons/ebkus_logo.gif",
##                                      tip='Zur Zugangsseite und dem Handbuch',
##                                      align='center',
##                                      n_col=2),
##                               ),
                       
            h.Tr(cells=(h.String(string=("%(vn)s, %(na)s (%(ben)s, %(benr__name)s)<br />%%s" %
                                         self.mitarbeiter) % config.INSTANCE_TITLE,
                                 class_='normaltext',
                                 align='left',
                                 ),
                              h.Icon(href="/ebkus/%s/index.html" % config.INSTANCE_NAME,
                                     icon="/ebkus/ebkus_icons/ebkus_logo.gif",
                                     tip='Zur Zugangsseite und dem Handbuch',
                                     align='center',
                                     n_col=2),
                              h.String(string='<div id="Uhr">&nbsp;</div>',
                                       class_='normaltext',
                                       align="right",
                                       ),
                              ),
                       ),
                  
            ),
            )
        gruppenmenu = h.FieldsetInputTable(
            daten=[[h.Button(value='Gruppenmenü',
                             onClick="go_to_url('menugruppe')",
                             tip="Zum Gruppenmenü",
                             ),
                    config.FALLUNABHAENGIGE_AKTIVITAETEN_BS and
                    h.Button(value='Fallunabh. Aktivitäten',
                             onClick="go_to_url('fua')",
                             tip="Zu den fallunabhängigen Aktivitäten",
                             class_='buttonbig',
                             ) or None,
                    ]]
            )
        auswertungen = h.FieldsetFormInputTable(
            legend='Auswertungen',
            daten=[[h.String(string='&nbsp;'*13,
                             class_='labeltext'),
                    h.SelectGoto(name='Auswahl1',
                                 class_='listbox',
                                 align='center',
                                 tip='Wählen Sie die gewünschte Auswertung',
                                 options=self.for_auswertungen(),
                                 ),
                    ]]
            )

        suche = h.FieldsetFormInputTable(
            action='abfr3',
            name='suchform',
            method='post',
            legend='Suche',
            daten=[[h.SelectItem(label='Nach',
                                 name='table',
                                 tip='Wählen Sie aus, wonach Sie suchen wollen',
                                 class_='listbox170',
                                 n_col=3,
                                 options="""
                            <option value="akte" selected> Vor- oder Nachname, Klient</option>
                            <option value="bezugsperson"> Vor- oder Nachname, Bezugsperson</option>
                            <option value="fall"> Beratungsfallnummer, Fall</option>
                            <option value="gruppe"> Name oder Thema, Gruppe</option>"""),
                    ],
                   [h.TextItem(label='Ausdruck',
                               name='expr',
                               class_='textbox120',
                               tip='Zeichenkette, nach der gesucht werden soll'),
                    h.Button(type='submit',
                             align='left',
                             #width='1%',
                             class_='buttonsmall',
                             value='Go'),
                    ],
                   ]
            )
        
        klient = h.FieldsetFormInputTable(
            action='klkarte',
            name='klkarteform',
            method='post',
            legend='Klientenauswahl', 
            daten=[
##             [
##                     h.Button(value='Neuaufnahme',
##                              type='button',
##                              onClick="go_to_url('akteneu')",
##                              n_col=6,
##                              ),
##                     ],
                   [h.SelectItem(name='fallid',
                                 size="18",
                                 class_="listbox280",
                                 tip="Alle Fälle, für die Sie Zugriffsrechte haben",
                                 options=self.for_klienten(),
                                 n_col=6,
                                 nolabel=True,
                                 ),
                    ],
                   [h.RadioItem(label='Klientenkarte',
                                name='file',
                                value='klkarte',
                                checked=True,
                                tip='Klientenkarte für ausgewählten Klienten ansehen',
                                ),
                    h.RadioItem(label='Klientendokumente',
                                name='file',
                                value='kldok',
                                tip='Dokumente für ausgewählten Klienten ansehen',
                                ),
                    h.RadioItem(label='Aktenvorblatt',
                                name='file',
                                value='vorblatt',
                                tip='Aktenvorblatt für ausgewählten Klienten ansehen',
                                ),
                    ],
##                    [h.String(string='Fachstatistik:',
##                              class_='labeltext',
##                              n_col=2,
##                              ),
##                     h.RadioItem(label='Neu',
##                                 name='file',
##                                 value='fsneu',
##                                 tip='Fachstatistik für ausgewählten Fall neu anlegen',
##                                 ),
##                     h.RadioItem(label='Ändern',
##                                 name='file',
##                                 value='updfsform',
##                                 tip='Fachstatistik für ausgewählten Fall ändern',
##                                 ),
##                     ],
                   [h.RadioItem(label='Bundesstatistik',
                                name='file',
                                value='updjghform', # wird in klientenkarte.py differenziert ausgewertet
                                tip='Bundesstatistik für ausgewählten Fall bearbeiten',
                                ),
                    h.RadioItem(label='Fachstatistik',
                                name='file',
                                value='updfsform', # wird in klientenkarte.py differenziert ausgewertet
                                tip='Fachstatistik für ausgewählten Fall bearbeiten',
                                ),
                    h.DummyItem(),
                    ],
                   [h.DummyItem(n_col=6)],
                   [h.Button(value='Ok',
                             type='submit',
                             n_col=3,
                             ),
                    h.Button(value='Neuaufnahme',
                             type='button',
                             onClick="go_to_url('akteneu')",
                             n_col=3,
                             ),
                    #h.DummyItem(n_col=2),
                    ],
                   ],
            )

        res = h.Page(
            title='Hauptmenü',
            help="das-hauptmen",
            onload="window.setTimeout('ZeitAnzeigen()',0)",
            rows=(logo_mitarbeiter_uhr,
                  h.Pair(left=(gruppenmenu,
                               auswertungen,
                               self.get_suche(),
                               self.get_abmelden_pw(),
                               ),
                         right=(klient,
                                ),
                         ),
                  ),
            )
        return res.display()
            


    def _hauptmenu_admin(self):
        mitarbeiter = h.FieldsetInputTable(
            legend='Mitarbeiter',
            daten=[[h.Button(value='Bearbeiten',
                             onClick="go_to_url('mitausw')",
                             tip="Merkmale von Mitarbeitern bearbeiten",
                             ),
                    h.Button(value='Neu',
                             onClick="go_to_url('mitneu')",
                             tip="Neuen Mitarbeiter eintragen",
                             ),
                    ]],
            )
        akten = h.FieldsetInputTable(
            legend='Akten',
            daten=[[h.Button(value='Löschen/Datenschutz',
                             onClick="go_to_url('rmakten')",
                             tip="Löschen von Akten nach Ablauf der Löschfrist",
                             class_="buttonbig",
                             ),
                    h.Button(value='Altdaten importieren',
                             onClick="go_to_url('altimport')",
                             tip="Importieren von Klientendaten aus früheren Systemen",
                             class_="buttonbig",
                             ),
                    ],
                   [h.Button(value='Löschen/Fehlerkorrektur',
                             onClick="go_to_url('rmaktenf')",
                             tip="Löschen von fehlerhaften Fällen und Akten",
                             class_="buttonbig",
                             ),
                    h.DummyItem(),
                    ]],
            )
        bundesstatistik = h.FieldsetInputTable(
            legend='Bundesstatistik',
            daten=[[h.Button(value='Exportieren',
                             onClick="go_to_url('formabfrjghexport')",
                             tip="Bundesstatistik im amtlichen Format erstellen",
                             ),
                    h.Button(value='Download',
                             onClick="go_to_url('jghexportlist')",
                             tip="Bundesstatistik herunterladen",
                             ),
                    ]],
            )
        fachstatistik = h.FieldsetInputTable(
            legend='Fachstatistik',
            daten=[[h.Button(value='Konfigurieren',
                             onClick="go_to_url('fskonfig')",
                             tip="Fachstatistik konfigurieren",
                             ),
                    ]],
            )
        # Tabellen, die Kategorien verwenden
        klassen = [t['klasse'] for t in
                   TabelleList(where='feld.kat_id IS NOT NULL',
                               join=[('feld', 'tabelle.id=feld.tab_id')]).sorted('klasse')]
        options = '<option value="nothing">[Tabelle auswählen]</option>\n'
        options += '<option value="codelist?tbl=Alle">Alle Tabellen</option>\n'
        options += '\n'.join(['<option value="codelist?tbl=%s">%s</option>' % (kln,kln)
                              for kln in klassen])
        tip = "Merkmalskataloge der gewählten Tabelle bearbeiten"
        merkmalskataloge = h.FieldsetFormInputTable(
            legend='Merkmalskataloge bearbeiten',
            daten=[[h.String(string="der Tabelle:",
                             class_="labeltext",
                             tip=tip,
                             ),
                    h.SelectGoto(name='tbl',
                                 tip=tip,
                                 options=options),
                    ]],
            )
        strassenkatalog = h.FieldsetInputTable(
            legend='Straßenkatalog',
            daten=[[h.Button(value='Importieren',
                             onClick="go_to_url('strkatimport')",
                             tip="Straßenkatalog aus einer CSV-Datei importieren",
                             ),
                    h.Button(value='Exportieren',
                             onClick="go_to_url('strkatexport')",
                             tip="Straßenkatalog als CSV-Datei exportieren",
                             ),
                    ]],
            )

        if config.SQL_ABFRAGE:
            sql_abfrage = h.FieldsetInputTable(
                legend='SQL Abfragen',
                daten=[[h.Button(value='Abfragen',
                                 onClick="go_to_url('sql_abfrage')",
                                 tip="Ergebnis einer SQL-Abfrage als CSV-Datei herunterladen",
                                 ),
                        ]],
                )
        else:
            sql_abfrage = None
        from ebkus.app.protocol import is_on
        if is_on():
            from ebkus.app.protocol import get_protocol_limit
            grenze = get_protocol_limit()
            protokoll = h.FieldsetFormInputTable(
                legend='Protokoll',
                name="fuellgrenze",
                action="admin_protocol",
                method="post",
                hidden = (('auswahl', 'pgrenze'),
                          ),
                daten=[[h.Button(value='Archivieren',
                                 onClick="go_to_url('admin_protocol?auswahl=archiv')",
                                 tip="Protokolldatensätze archivieren",
                                 ),
                        h.DummyItem(),
                        h.TextItem(label='Füllgrenze',
                                   tip="Max. Größe der Protokolltabelle vor automatischer Archivierung",
                                   name='grenze',
                                   value=grenze,
                                   maxlength=9,
                                   class_='textbox52',
                                   ),
                        h.Button(value='Speichern',
                                 type='submit',
                                 tip="Füllgrenze speichern",
                                 ),
                        ]],
                )
        else:
            protokoll = None
        res = h.Page(
            title='Administratorhauptmenü',
            help="das-hauptmen",
            breadcrumbs = ((),),
            rows=(self.get_abmelden_pw(),
                  h.Pair(left=mitarbeiter,
                         right=akten,
                         ),
                  h.Pair(left=bundesstatistik,
                         right=fachstatistik,
                         ),
                  h.Pair(left=merkmalskataloge,
                         right=strassenkatalog,
                         ),
                  h.Pair(left=sql_abfrage,
                         right='',
                         ),
                  protokoll,
                  ),
            )
        return res.display()

    def processForm(self, REQUEST, RESPONSE):
        #if True: return self._hauptmenu_klienten()
        mitarbeiterliste = self.getMitarbeiterliste()
        user = self.user
        stelle = self.stelle
        mitarbeiter = self.mitarbeiter
        # damit das logo auf dem Hauptmenü auf die Eingangsseite der Instanz
        # verlinken kann
        mitarbeiter['index_url'] = "/ebkus/%s/index.html" % config.INSTANCE_NAME
        res = []
        if mitarbeiter['benr__code'] == 'bearb':
            return self._hauptmenu_klienten()
##             res.append(head_normal_t % ('Hauptmen&uuml;'))
##             zustaendigkeiten = ZustaendigkeitList(where = 'ed = 0 and mit_id = %s'
##                                                   % mitarbeiter['id'] )
##             zustaendigkeiten.sort('mit_id__na', 'fall_id__akte_id__na',
##                                   'fall_id__akte_id__vn')
##             res.append(main_menu_t % mitarbeiter)
##             for z in zustaendigkeiten:
##                 if z['fall_id__akte_id__stzak'] == stelle['id']:
##                     res.append(klientauswahl_t % z)
##             res.append(menusubmit_t )
        elif mitarbeiter['benr__code'] == 'verw':
            return self._hauptmenu_klienten()
##             res.append(head_normal_t % ('Hauptmen&uuml;'))
##             zustaendigkeiten = ZustaendigkeitList(where = 'ed = 0', order = 'id')
##             zustaendigkeiten.sort('mit_id__na', 'fall_id__akte_id__na',
##                                   'fall_id__akte_id__vn')
##             res.append(main_menu_t % mitarbeiter)
##             for z in zustaendigkeiten:
##                 if z['fall_id__akte_id__stzak'] == stelle['id']:
##                     res.append(klientauswahl_t % z)
##             res.append(menusubmit_t )
            # Admin soll keine Klientennamen erhalten, er braucht nur das Admin-Menu.
        elif mitarbeiter['benr__code'] == 'admin':
            return self._hauptmenu_admin()
##             res.append(head_normal_ohne_help_t % ('Hauptmen&uuml;'))
##             prottabid = TabellenID(table_name = 'protokoll')
##             # Tabellen, die Kategorien verwenden
##             klassen = [t['klasse'] for t in
##                        TabelleList(where='feld.kat_id IS NOT NULL',
##                                    join=[('feld', 'tabelle.id=feld.tab_id')]).sorted('klasse')]
##             options = '<option value="nothing">[Tabelle auswählen]</option>\n'
##             options += '<option value="codelist?tbl=Alle">Alle Tabellen</option>\n'
##             options += '\n'.join(['<option value="codelist?tbl=%s">%s</option>' % (kln,kln)
##                                   for kln in klassen])
##             label = h.String(string="Verwendet für:",
##                              class_="labeltext")
##             to_codelist = h.SelectGoto(name='tbl',
##                                        options=options)
            
##             grenze = prottabid['maxid']
##             res.append(administration_t % ("%s%s" % (label, to_codelist), grenze))
            
        elif mitarbeiter['benr__code'] == 'protokol':
            res2 = []
            meldung = {'titel':'Gesicherter Bereich!',
                      'legende':'Achtung!',
                      'zeile1':'Sie betreten einen Hochsicherheitsbereich',
                      'zeile2':'Sie werden zur Protokoll - Anmeldung weitergeleitet.','url':'login_formular'}
            res2.append(meldung_weiterleitung_t % meldung)
            return string.join(res2, '')
        return string.join(res, '')
        
        
        
        
        
        
        
        
