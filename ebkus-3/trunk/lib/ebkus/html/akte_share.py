# coding: latin-1

"""Gemeinsame HTML Elemente."""

from ebkus.config import config
from ebkus.app.ebapi import today, str2date, cc, Akte, Bezugsperson, Beratungskontakt_BSList, Code
from ebkus.app.ebapih import get_codes, make_option_list
import ebkus.html.htmlgen as h
from ebkus.html.options import options
from ebkus.html.strkat import get_strassen_list, get_strasse

class akte_share(options):
    """Html-Elemente, die an verschiedenen Stellen gebraucht werden
    und hier nur einmal definiert werden.
    """
    def get_button_klienten_neu(self, aktueller_fall, wiederaufnehmbar, letzter_fall):
            return (aktueller_fall and
             h.SelectGoto(name='Auswahl1', options =
"""<option value="nothing">[ Neu ]</option>
<option value="akteneu?file=akteneu">- Neuaufnahme</option>
<option value="persneu?akid=%(akte_id)s&fallid=%(id)s">- Bezugsperson</option>
<option value="einrneu?akid=%(akte_id)s&fallid=%(id)s">- Einrichtung</option>
<option value="anmneu?akid=%(akte_id)s&fallid=%(id)s">- Anmeldung</option>
<option value="leistneu?akid=%(akte_id)s&fallid=%(id)s">- Leistung</option>
<option value="bkontneu?akid=%(akte_id)s&fallid=%(id)s">- Beratungskontakt</option>
<option value="zustneu?akid=%(akte_id)s&fallid=%(id)s">- Bearbeiter</option>
<option value="vermneu?akid=%(akte_id)s&fallid=%(id)s">- Dokument erstellen</option>
<option value="upload?akid=%(akte_id)s&fallid=%(id)s">- Dokument importieren</option>
<option value="fsneu?akid=%(akte_id)s&fallid=%(id)s">- Fachstatistik</option>
<option value="jgh07neu?akid=%(akte_id)s&fallid=%(id)s">- Bundesstatistik</option>
<option value="zda?akid=%(akte_id)s&fallid=%(id)s">- zu den Akten</option>
""" % aktueller_fall)
                  or wiederaufnehmbar and
                  h.SelectGoto(name='Auswahl1', options =
"""<option value="nothing">[ Neu ]</option>
<option value="akteneu?file=akteneu">- Neuaufnahme</option>
<option value="waufnneu?akid=%(akte_id)d&fallid=%(id)d">- Wiederaufnahme</option>
""" % letzter_fall)
                  or
                  h.SelectGoto(name='Auswahl1', options =
"""<option value="nothing">[ Neu ]</option>
<option value="akteneu?file=akteneu">- Neuaufnahme</option>
<option value="zdar?akid=%(akte_id)d&fallid=%(id)d">- zdA R&uuml;ckg&auml;ngig</option>
""" % letzter_fall))

    def get_button_klienten_anzeige(self, aktueller_fall, letzter_fall):
            return (aktueller_fall and
             h.SelectGoto(name='Auswahl2', options =
"""<option value="nothing">[ Anzeige ]</option>
<option value="newXX vorblatt?akid=%(akte_id)d&fallid=%(id)d">- Vorblatt</option>
<option value="kldok?akid=%(akte_id)d&fallid=%(id)d">- Klientendokumente</option>
<option value="wordexport?akid=%(akte_id)d">- Word-Export</option>
""" % aktueller_fall)
             or
             h.SelectGoto(name='Auswahl2', options =
"""<option value="nothing">[ Anzeige ]</option>
<option value="vorblatt?akid=%(akte_id)d&fallid=%(id)d">- Vorblatt</option>
<option value="kldok?akid=%(akte_id)d&fallid=%(id)d">- Klientendokumente</option>
""" % letzter_fall ))
            

    def _get_ort_zusatz_items(self, data):
        "Optionale, konfigurierbare Felder f�r Klientendaten readonly"
        items = [h.DummyItem(), h.DummyItem()]
        strasse = get_strasse(data)
        if strasse:
            items_dict = {'bezirk': h.TextItem(label='Bezirk',
                                               tip='Bezirk',
                                               value=strasse.get('bezirk',''),
                                               readonly=True,
                                               ),
                          'ortsteil': h.TextItem(label='OT',
                                                 tip='Ortsteil',
                                                 value=strasse.get('ortsteil', ''),
                                                 readonly=True,
                                                 ),
                          'samtgemeinde': h.TextItem(label='SG',
                                                     tip='Samtgemeinde',
                                                     value=strasse.get('samtgemeinde', ''),
                                                     readonly=True,
                                                     ),
                          }
            zusatzfelder = [k for k in config.STRASSENSUCHE.split() if k != 'ort']
            if strasse.get('samtgemeinde') == strasse['ort']:
                if 'samtgemeinde' in zusatzfelder:
                    zusatzfelder.remove('samtgemeinde')
            if len(zusatzfelder) == 1:
                items[0] = items_dict[zusatzfelder[0]]
            elif len(zusatzfelder) > 1:
                items[0] = items_dict[zusatzfelder[0]]
                items[1] = items_dict[zusatzfelder[1]]
        return items


    def get_klientendaten_readonly(self, data, button=None):
        if isinstance(data, Akte):
            bezug = 'des Klienten'
            legend = 'Klientendaten'
        elif isinstance(data, Bezugsperson):
            bezug = 'der Bezugsperson'
            legend = 'Bezugsperson %s' % data['verw__name']
        klientendaten = h.FieldsetInputTable(
            legend=legend,
            daten=[[h.TextItem(label='Vorname',
                              name='vn',
                              value=data['vn'],
                              readonly=True,
                               n_col=4,
                              ),
                    h.TextItem(label='Stra�e',
                              name='str',
                              value="%(str)s %(hsnr)s" % data,
                              readonly=True,
                              ),
                    h.TextItem(label='Wohnt bei',
                              name='fs__name',
                              value=data['fs__name'],
                              readonly=True,
                              ),
                    ],
                   [h.TextItem(label='Nachname',
                              name='na',
                              value=data['na'],
                              readonly=True,
                               n_col=4,
                              ),
                    h.TextItem(label='PLZ',
                               name='plz',
                               class_='textboxmid',
                               value=data['plz'],
                               readonly=True,
                               ),
                    h.TextItem(label='Ort',
                               name='ort',
                               value=data['ort'],
                               readonly=True,
                              ),
                    ],
                   [h.TextItem(label='Geburtstag',
                              name='gb',
                              value=data['gb'],
                               class_='textbox52',
                              readonly=True,
                              ),
                    h.TextItem(label='Geschl.',
                               name='gs',
                               value=data['gs'] and data['gs__name'] or '',
                               class_='textbox12',
                              readonly=True,
                              )] +
                   self._get_ort_zusatz_items(data),
                   [h.TextItem(label='Ausbildung',
                               name='ber',
                               value=data['ber'],
                               readonly=True,
                               n_col=4,
                               ),
                    h.TextItem(label='Telefon 1',
                              name='tl1',
                              value=data['tl1'],
                              readonly=True,
                              ),
                    h.TextItem(label='Telefon 2',
                              name='tl2',
                              value=data['tl2'],
                              readonly=True,
                              ),
                    ],
                   ],
            button=button,
            )
        return klientendaten


    def get_klientendaten(self, data):
        if isinstance(data, Akte):
            bezug = 'des Klienten'
            bezug_n = 'der Klient'
            legend = 'Klientendaten'
        elif isinstance(data, Bezugsperson):
            bezug = 'der Bezugsperson'
            bezug_n = 'die Bezugsperson'
            legend = 'Bezugspersondaten'
        klientendaten = h.FieldsetInputTable(
            legend=legend,
            daten=[[h.TextItem(label='Vorname',
                               name='vn',
                               value=data['vn'],
                               tip='Vorname %s' % bezug,
                               )],
                   [h.TextItem(label='Nachname',
                               name='na',
                               value=data['na'],
                               tip='Nachname %s' % bezug,
                               )],
                   [h.DatumItem(label='Geburtstag',
                               name='gb',
                               date=str2date(data['gb']),
                               tip="Geburtstag %s" % bezug,
                               )],
                   [h.SelectItem(label='Geschlecht',
                                 name='gs',
                                 options=self.for_kat('gs', sel=(not data['gs'] and ' '
                                                                 or data['gs'])),
                                 tip='Geschlecht %s' % bezug,
                                 class_='listbox30',
                                 )],
                   [h.SelectItem(label='Wohnt bei',
                                 name='fs',
                                 options=self.for_kat('fsfs', sel=data['fs']),
                                 tip='Bei wem %s lebt' % bezug_n,
                                 )],
                   [h.TextItem(label='Telefon1',
                               name='tl1',
                               value=data['tl1'],
                               )],
                   [h.TextItem(label='Telefon2',
                               name='tl2',
                               value=data['tl2'],
                               )],
                   [h.TextItem(label='Ausbildung',
                               name='ber',
                               value=data['ber'],
                               tip='Die Ausbildung %s' % bezug,
                               )],
                   ],
            )
        return klientendaten

    def get_anschrift(self, data):
        if config.STRASSENKATALOG:
            n_col = 3 # eine Spalte mehr wg. icon
            such_icon = h.Icon(href="javascript:view_strkat()",
                               #href="javascript:open('strkat','Strassensuche')",
                               tip="Passende Eintr�ge im Stra�enkatalog suchen",
                               icon="/ebkus/ebkus_icons/strkatview_button.jpg",
                               )
            strkat_ein_aus = h.CheckItem(label='Stra�enkatalog verwenden',
                                         tip='H�kchen entfernen, um Adresse ohne Abgleich mit dem Stra�enkatalog einzugeben',
                                         name='strkat_on',
                                         value=1,
                                         checked=(data.get('lage') == cc('lage', '0')),
                                         n_label=2,
                                         n_col=n_col,
                                         )
        else:
            icon = None
            n_col = 2
        reset_icon = h.Icon(#href="strkat",
                          href="javascript:reset_strkat()",
                          #href="javascript:open('strkat','Strassensuche')",
                          tip="Adressfelder leeren",
                          icon="/ebkus/ebkus_icons/neu_button.gif",
            )

        strasse = get_strasse(data)
        str = h.TextItem(label='Stra�e',
                         name='str',
                         value=data['str'],
                         tip='Stra�e',
                         icon=reset_icon,
                         )
        hsnr = h.TextItem(label='Hausnummer',
                          name='hsnr',
                          value=data['hsnr'],
                          tip='Hausnummer',
                          n_col=n_col,
                        )
        plz = h.TextItem(label='Postleitzahl',
                       name='plz',
                       value=data['plz'],
                       tip="Postleitzahl",
                       n_col=n_col,
                       )
        ort = h.TextItem(label='Ort',
                       name='ort',
                       value=data['ort'],
                       tip="Wohnort",
                       n_col=n_col,
                       )
        ortsteil = h.TextItem(label='Ortsteil',
                       name='ortsteil',
                       value=strasse.get('ortsteil', ''),
                       tip="Ortsteil",
                       n_col=n_col,
                       )
        bezirk = h.TextItem(label='Bezirk',
                       name='bezirk',
                       value=strasse.get('bezirk', ''),
                       n_col=n_col,
                       )
        samtgemeinde = h.TextItem(label='Samtgemeinde',
                       name='samtgemeinde',
                       tip="Samtgemeinde",
                       value=strasse.get('samtgemeinde', ''),
                       n_col=n_col,
                       )
        planungsr = h.TextItem(label='Planungsraum',
                               name='planungsr',
                               value=data.get('planungsr', ''),
                               tip="Der Planungsraum des Klienten",
                               n_col=n_col,
                               )
        if config.STRASSENKATALOG:
            items = (strkat_ein_aus, str, hsnr, plz, ort,)
            #items = (strkat, str_ausser, hsnr, plz, ort, fs)
            zusatzfelder = [f for f in config.STRASSENSUCHE.split() if f != 'ort']
            for f in zusatzfelder:
                if f == 'bezirk':
                    items += (bezirk,)
                if f == 'ortsteil':
                    items += (ortsteil,)
                if f == 'samtgemeinde':
                    items += (samtgemeinde,)
        else:
            items = (str, hsnr, plz, ort, planungsr,)
        # Suche hinter das letzte item
        items[-1].icon = such_icon
        items[-1].n_col = 2
        anschrift = h.FieldsetInputTable(
            # tip �berdeckt die tips der einzelnen Elemente in der Statuszeile
##             tip="Anfangsbuchstaben in einem oder "
##             "mehreren Feldern gen�gen f�r eine Suche!",
            legend = 'Anschrift',
            daten = [[i] for i in items])
        return anschrift

    def get_klientendaten_kurz(self, fall):
        akte = fall['akte']
        klientendaten = h.FieldsetDataTable(
            legend='Klient',
            headers= ('Name', 'Geburtsdatum', 'Fallnummer', 'zdA'),
            daten=[[h.String(string="%(vn)s %(na)s" % akte),
                    h.String(string="%(gb)s" % akte),
                    h.String(string="%(fn)s" % fall),
                    h.Datum(date=fall.getDate('zda')),
                    ]]
            )
        return klientendaten
        
    def get_gruppendaten_kurz(self, gruppe):
        gruppendaten = h.FieldsetDataTable(
            legend='Gruppe',
            headers= ('Name', 'Gruppennummer', 'Von', 'Bis'),
            daten=[[h.String(string="%(name)s" % gruppe),
                    h.String(string="%(gn)s" % gruppe),
                    h.Datum(date=gruppe.getDate('bg')),
                    h.Datum(date=gruppe.getDate('e')),
                    ]]
            )
        return gruppendaten

    def get_zustaendigkeiten(self, zustaendigkeiten_list):
        zustaendigkeiten = h.FieldsetDataTable(
            legend='Zust�ndigkeiten',
            headers= ('Bearbeiter', 'Beginn', 'Ende'),
            daten=[[h.String(string= zust['mit_id__na']),
                    h.Datum(day=zust['bgd'],
                            month=zust['bgm'],
                            year=zust['bgy']),
                    h.Datum(day=zust['ed'],
                            month=zust['em'],
                            year=zust['ey'])]
                   for zust in zustaendigkeiten_list],
            )
        return zustaendigkeiten

    def get_bisherige_zustaendigkeit(self, aktuell_zustaendig):
        bisherige_zustaendigkeit = h.FieldsetDataTable(
            legend='Bisherige Zust�ndigkeit wird ausgetragen',
            headers= ('Bearbeiter', 'Beginn'),
            daten=[[h.String(string= "%(mit__vn)s %(mit__na)s" % aktuell_zustaendig),
                    h.Datum(date=aktuell_zustaendig.getDate('bg')),
                    ]],
            )
        return bisherige_zustaendigkeit


    def get_bezugspersonen(self, bezugspersonen_list,
                           aktueller_fall, # falls False, kein Hinzuf�gen-Button, inaktive edit/view buttons
                           edit_button, # falls False, kein edit button
                           view_button, # falls False, kein view button
                           hinzufuegen_button, # falls False, kein hinzuf�gen button
                           ):
        bezugspersonen = h.FieldsetDataTable(
            legend= 'Bezugspersonen',
            headers= ('Art', 'Vorname', 'Nachname', 'Telefon 1', 'Telefon 2'),
            daten= [[(aktueller_fall and
                      h.Icon(href= 'updpers?akid=%(akte_id)d&bpid=%(id)d' % b,
                           icon= "/ebkus/ebkus_icons/edit_button.gif",
                           tip= 'Bezugsperson bearbeiten')
                      or
                      h.IconDead(icon= "/ebkus/ebkus_icons/edit_button_inaktiv_locked.gif",
                               tip= 'Funktion gesperrt')),

                       (aktueller_fall and
                        h.Icon(href= '#',
                             onClick= "view_details('viewpers?akid=%(akte_id)d&bpid=%(id)d')" % b,
                             icon= "/ebkus/ebkus_icons/view_details.gif",
                             tip= 'Bezugsperson ansehen')
                        or
                        h.IconDead(icon= "/ebkus/ebkus_icons/view_details_inaktiv.gif",
                                 tip= 'Funktion gesperrt')),

                       h.String(string= b['verw__name']),
                       h.String(string= b['vn']),
                       h.String(string= b['na']),
                       h.String(string= b['tl1']),
                       h.String(string= b['tl2'])]
                      for b in bezugspersonen_list],
            button= (aktueller_fall and hinzufuegen_button and
                     h.Button(value="Hinzuf�gen",
                            tip="Bezugsperson hinzuf�gen",
                            onClick=
                       "go_to_url('persneu?akid=%(akte_id)d&fallid=%(id)d&klerv=1')" %
                              aktueller_fall,
                            ) or None),
            )
        # L�schen unerw�nschter icons aus den Tabellenitems.
        # Erscheint mir einfacher, als die Generierung weiter zu verschachteln.
        daten = bezugspersonen.daten
        if edit_button:
            if not view_button:
                for zeile in daten:
                    del zeile[1]
        else:
            for zeile in daten:
                del zeile[0]
            if not view_button:
                for zeile in daten:
                    del zeile[0]
        return bezugspersonen


    def get_beratungskontakte_bs(self, beratungskontakte,
                                 aktueller_fall=None, # falls False, kein Hinzuf�gen-Button, inaktive edit/view buttons
                                 edit_button=False, # falls False, kein edit button
                                 hinzufuegen_button=False, # falls False, kein hinzuf�gen button
                                 ):
        beratungskontakte.sort('ky', 'km', 'kd')
        bisherige_kontakte = h.FieldsetDataTable(
            legend='Beratungskontakte',
            empty_msg="Bisher keine Kontakte eingetragen.",
            headers=('Datum', 'Mitarbeiter', 'Klienten', 'Art',
                       'Teilnehmer', 'Dauer (x10min)', 'Notiz'),
            daten=[[(edit_button and (aktueller_fall and 
                                      h.Icon(href= 'updbkont?bkontid=%(id)d' % b,
                                             icon= "/ebkus/ebkus_icons/edit_button.gif",
                                             tip= 'Beratungskontakt bearbeiten')
                                      or
                                      h.IconDead(icon= "/ebkus/ebkus_icons/edit_button_inaktiv_locked.gif",
                                                 tip= 'Funktion gesperrt'))) or None,
                    h.Datum(date =  b.getDate('k')),
                    h.String(string=', '.join([b['mit%s__na' % i] 
                                               for i in ('', '1', '2')
                                               if b['mit%s_id' % i]]),
                             ),
                    h.String(string=', '.join([b['fall%s__name' % i]
                                               for i in ('', '1', '2')
                                               if b['fall%s_id' % i]]),
                             ),
                    h.String(string=b['art__name']),
                    h.String(string=', '.join([Code(i)['name']
                                               for i in b['teilnehmer'].split()]),
                             ),
                    h.String(string=b['dauer']),
                    h.String(string=b['no']),
                    ]
                   for b in beratungskontakte],
            button=(aktueller_fall and hinzufuegen_button and
                    h.Button(value="Hinzuf�gen",
                             tip="Beratungskontakt hinzuf�gen",
                             onClick=
                             "go_to_url('bkontneu?akid=%(akte_id)s&fallid=%(id)s')" %
                             aktueller_fall,
                             ) or None),
            )
        return bisherige_kontakte
    


    def get_code_tabelle(self, kat, links=True, view=''):
        code_tabelle = h.FieldsetDataTable(
            legend="Alle Merkmale der Kategorie '%s'" % kat['name'],
            anchor="%(id)s" % kat,
            daten_before_headers = links and
            [[h.Icon(href="codeneu?katid=%s&view=%s" % (kat['id'], view),
                     icon= "/ebkus/ebkus_icons/neu_button.gif",
                     tip="Merkmal zur Antwortkategorie hinzuf�gen",
                     ),
              h.DummyItem(n_col=5),
              ]] or (),
            headers=('Code', 'Merkmal', 'Sort', 'Off', 'Ab', 'Dokumentation'),
            daten=[[links and h.Link(string="%(code)s" % code,
                                     tip="Merkmal bearbeiten",
                                     url="updcode?codeid=%s&view=%s" % (code['id'], view))
                    or h.String(string="%(code)s" % code),
                    h.String(string="%(name)s" % code),
                    h.String(string="%(sort)s" % code),
                    h.String(string="%(off)s" % code),
                    h.String(string=code['dy'] and "%(dm)s<b>.</b>%(dy)s" % code or ''),
                    h.String(string=code['dok'] or '')]
                   for code in kat['codes'].sorted('sort')],
            )
        return code_tabelle

    def get_suche(self):
        return h.FieldsetFormInputTable(
            action='abfr3',
            name='suchform',
            method='post',
            legend='Suche',
            daten=[[h.SelectItem(label='Nach',
                                 name='table',
                                 tip='W�hlen Sie aus, wonach Sie suchen wollen',
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


    def get_gruppendaten(self, gruppe, readonly=True):
        if readonly:
            button = h.Button(value="Bearbeiten",
                              tip="Gruppendaten bearbeiten",
                              onClick= "go_to_url('updgruppe?gruppeid=%(id)s')" % gruppe)
        else:
            button=None
##         print 'SEL', [m['mit_id'] for m in gruppe['mitarbeiter']]
##         print gruppe['mitarbeiter']
        gruppendaten = h.FieldsetInputTable(
            legend='Gruppendaten',
            daten=[[h.TextItem(label='Name',
                               name='name',
                               value="%(name)s" % gruppe,
                               readonly=readonly,
                               tip='Name der Gruppe',
                               ),
                    h.TextItem(label='Thema',
                               name='thema',
                               readonly=readonly,
                               value="%(thema)s" % gruppe,
                               tip='Thema der Gruppe',
                               class_='textbox280',
                               n_col=4,
                               ),
                    ],
                   [h.DatumItem(label='Beginn',
                                 name='bg',
                                 date=gruppe.getDate('bg'),
                                 readonly=readonly,
                                 tip='Beginndatum',
                                 ),
                    h.DatumItem(label='Ende',
                                 name='e',
                                 date=gruppe.getDate('e'),
                                 readonly=readonly,
                                 tip='Endedatum',
                                 ),
                    h.DummyItem(),
                    ],
                   [h.SelectItem(label='Gruppenart',
                                 name='grtyp',
                                 tip='Art der Gruppe',
                                 readonly=readonly,
                                 options=self.for_kat('grtyp', sel=gruppe['grtyp']),
                                 ),
                    h.SelectItem(label='Mitarbeiter',
                                 name='mitid',
                                 size="4",
                                 multiple=True,
                                 tip='Teilnehmende Mitarbeiter',
                                 rowspan="2",
                                 readonly=readonly,
                                 options=self.for_mitarbeiter(sel=[m['mit_id'] for m in gruppe['mitarbeiter']])),
                    h.TextItem(label='Maximale Teilnehmerzahl',
                               name='tzahl',
                               readonly=readonly,
                               value=gruppe['tzahl'] or '',
                               tip='Geplante maximale Teilnehmerzahl der Gruppe',
                               class_='textboxmid'
                               ),
                    ],
                   [h.SelectItem(label='Teilnehmer',
                                 name='teiln',
                                 tip='Art der Teilnehmer',
                                 readonly=readonly,
                                 options=self.for_kat('teiln', sel=gruppe['teiln']),
                                 ),
                    h.TextItem(label='Stundenzahl',
                               name='stzahl',
                               readonly=readonly,
                               value=gruppe['stzahl'] or '',
                               tip='Geplante Stundenzahl insgesamt �ber die Dauer der Gruppe',
                               class_='textboxmid',
                               ),
                    ],
                   ],
            button=button,
            )
        return gruppendaten

    def grundgesamtheit(self, legend='Grundgesamtheit'):
        "F�r Auswertungen. Legt Jahre und Stellen fest."
        res = h.FieldsetInputTable(
            legend='Grundgesamtheit',
            daten=[[h.SelectItem(label='Jahr',
                                 name='bis_jahr',
                                 class_='listbox45',
                                 tip='W�hlen Sie das Jahr, f�r das eine Ausz�hlung erfolgen soll',
                                 options=self.for_jahre(sel=today()['year']-1),
                                 ),
                    h.SelectItem(label='Stelle',
                                 name='stz',
                                 multiple=True,
                                 rowspan=2,
                                 tip='Eine oder mehrere Stellen ausw�hlen',
                                 size=3,
                                 options=self.for_kat('stzei', sel=self.stelle['id']),
                                 ),
                    ],
                   [h.SelectItem(label='Fr�here Jahre einbeziehen ab',
                                 name='von_jahr',
                                 class_='listbox45',
                                 tip='Nur f�r Auswertungen �ber mehrere Jahre hinweg',
                                 options=self.for_jahre(erster_eintrag=' '),
                                 ),
                    ],
                   ],
            )
        return res

    def get_auswertungs_menu(self):
        menu = h.FieldsetInputTable(
            daten=[[h.Button(value="Hauptmen�",
                             tip="Zum Hauptmen�",
                             onClick="go_to_url('menu')",
                             ),
                    h.String(string='Andere Auswertungen:',
                             align='right', 
                             class_='labeltext'),
                    # SelectGoto sollte mit SelectItem zusammengelegt werden
                    # (hat sonst kein label)
                    h.SelectGoto(name='Auswahl1',
                                 class_='listbox',
                                 align='left',
                                 tip='W�hlen Sie die gew�nschte andere Auswertung',
                                 options=self.for_auswertungen(),
                                 ),
                    ]])
        return menu
