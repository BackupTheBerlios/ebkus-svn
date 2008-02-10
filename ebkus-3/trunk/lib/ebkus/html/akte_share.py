# coding: latin-1

"""Gemeinsame HTML Elemente."""

from ebkus.config import config
from ebkus.db.sql import escape
from ebkus.app.ebapi import today, str2date, cc, bcode, \
     Akte, Bezugsperson, BeratungskontaktList, Code, FallList
from ebkus.app.ebapih import get_codes, make_option_list
import ebkus.html.htmlgen as h
from ebkus.html.options import options

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
""" % aktueller_fall)
             or
             h.SelectGoto(name='Auswahl2', options =
"""<option value="nothing">[ Anzeige ]</option>
<option value="vorblatt?akid=%(akte_id)d&fallid=%(id)d">- Vorblatt</option>
<option value="kldok?akid=%(akte_id)d&fallid=%(id)d">- Klientendokumente</option>
""" % letzter_fall ))

# Im aktuellen Fall gab es den Wordexport, der aber unseres Wissens nie
# verwendet wurde. Ich verstehe es auch nicht. Soll raus.
# <option value="wordexport?akid=%(akte_id)d">- Word-Export</option>

    def _get_ort_zusatz_items(self, data):
        "Optionale, konfigurierbare Felder für Klientendaten readonly"
        from ebkus.html.strkat import get_strasse
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
                    h.TextItem(label='Straße',
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
                               class_='textbox13',
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
                   [isinstance(data, Akte) and
                    h.TextItem(label='Aufbewahrungs-<br />kategorie',
                               name='aufbew',
                               value=data['aufbew__name'],
                               readonly=True,
                               tip="Bestimmt den Zeitraum, für den die Akte aufbewahrt werden muss",
                               n_col=4,
                               ) or h.DummyItem(n_col=4),
                    h.DummyItem(),
                    h.DummyItem(),
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
            gs_tip = 'Geschlecht %s' % bezug
        elif isinstance(data, Bezugsperson):
            bezug = 'der Bezugsperson'
            bezug_n = 'die Bezugsperson'
            legend = 'Bezugspersondaten'
            gs_tip = 'Geschlecht %s (Nicht nötig bei -mutter bzw. -vater in Verwandtschaftsart)' % bezug
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
                                 tip=gs_tip,
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
                   isinstance(data, Akte) and
                   [h.SelectItem(label='Aufbewahrungs-<br />kategorie',
                                 name='aufbew',
                                 options=self.for_kat('aufbew', sel=data['aufbew']),
                                 tip="Bestimmt den Zeitraum, für den die Akte aufbewahrt werden muss",
                                 )] or None,
                   ],
            )
        return klientendaten

    def get_anschrift(self, data, force_strkat=None):
        from ebkus.html.strkat import get_strasse
        if force_strkat != None:
            strkat_on = force_strkat
        else:
            strkat_on = (data.get('lage') == cc('lage', '0'))
        n_col = 3 # eine Spalte mehr wg. icons
        such_icon = h.Icon(href="javascript:view_strkat()",
                           #href="javascript:open('strkat','Strassensuche')",
                           tip="Passende Einträge im Straßenkatalog suchen",
                           icon="/ebkus/ebkus_icons/strkatview_button.jpg",
                           )
        strkat_ein_aus = h.CheckItem(label='Straßenkatalog verwenden',
                                     tip='Häkchen entfernen, um Adresse ohne Abgleich mit dem Straßenkatalog einzugeben',
                                     name='strkat_on',
                                     value=1,
                                     checked=strkat_on,
                                     n_label=2,
                                     n_col=n_col,
                                     )
        reset_icon = h.Icon(#href="strkat",
                          href="javascript:reset_strkat()",
                          #href="javascript:open('strkat','Strassensuche')",
                          tip="Adressfelder leeren",
                          icon="/ebkus/ebkus_icons/neu_button.gif",
                          )
        str = h.TextItem(label='Straße',
                         name='str',
                         value=data['str'],
                         tip='Straße',
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
        if strkat_on:
            strasse = get_strasse(data)
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
        # TODO klären, ob die 0 nicht ganz weg kann.
        # wird in setAdresse eingesetzt, wenn kein planungsr angegeben wurde
        planungsr_value = data.get('plraum', '')
        if planungsr_value == '0':
            planungsr_value = ''

        if isinstance(data, Akte):
            planungsr = h.TextItem(label='Planungsraum',
                                   name='plraum',
                                   value=planungsr_value,
                                   tip="Der Planungsraum des Klienten",
                                   n_col=n_col,
                                   )
        else:
            planungsr = h.DummyItem(n_col=n_col,)
        if config.STRASSENKATALOG:
            items = (strkat_ein_aus,)
        else:
            items = ()
        items += (str, hsnr, plz, ort,)
        if config.STRASSENKATALOG and strkat_on:
            zusatzfelder = [f for f in config.STRASSENSUCHE.split() if f != 'ort']
            for f in zusatzfelder:
                if f == 'bezirk':
                    items += (bezirk,)
                if f == 'ortsteil':
                    items += (ortsteil,)
                if f == 'samtgemeinde':
                    items += (samtgemeinde,)
        else:
            items += (planungsr,)
        # Suche hinter das letzte item
        if config.STRASSENKATALOG:
            items[-1].icon = such_icon
            items[-1].n_col = 2
        anschrift = h.FieldsetInputTable(
            # tip überdeckt die tips der einzelnen Elemente in der Statuszeile
##             tip="Anfangsbuchstaben in einem oder "
##             "mehreren Feldern genügen für eine Suche!",
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
            legend='Zuständigkeiten',
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

    def get_bisherige_zustaendigkeit(self, aktuell_zustaendig, legend):
        bisherige_zustaendigkeit = h.FieldsetDataTable(
            legend=legend,
            headers= ('Bearbeiter', 'Beginn'),
            daten=[[h.String(string= "%(mit__vn)s %(mit__na)s" % aktuell_zustaendig),
                    h.Datum(date=aktuell_zustaendig.getDate('bg')),
                    ]],
            )
        return bisherige_zustaendigkeit


    def get_bezugspersonen(self, bezugspersonen_list,
                           aktueller_fall, # falls False, kein Hinzufügen-Button, inaktive edit/view buttons
                           edit_button, # falls False, kein edit button
                           view_button, # falls False, kein view button
                           hinzufuegen_button, # falls False, kein hinzufügen button
                           ):
        bezugspersonen = h.FieldsetDataTable(
            legend= 'Bezugspersonen',
            headers= ('Art', 'Vorname', 'Nachname', 'Telefon 1', 'Telefon 2'),
            noheaders=3,
            daten= [[aktueller_fall and
                     h.Icon(href='updpers?akid=%(akte_id)d&bpid=%(id)d' % b,
                            icon="/ebkus/ebkus_icons/edit_button.gif",
                            tip= 'Bezugsperson bearbeiten')
                     or
                     h.Dummy(),
                     aktueller_fall and
                     h.Icon(href='rmpers?bpid=%(id)d' % b,
                            icon= "/ebkus/ebkus_icons/del_button.gif",
                            tip= 'Daten für Bezugsperson löschen')
                     or
                     h.Dummy(),
                     aktueller_fall and
                     h.Icon(href= '#',
                            onClick= "view_details('viewpers?akid=%(akte_id)d&bpid=%(id)d')" % b,
                            icon= "/ebkus/ebkus_icons/view_details.gif",
                            tip= 'Bezugsperson ansehen')
                     or
                     h.Dummy(),
                     h.String(string= b['verw__name']),
                     h.String(string= b['vn']),
                     h.String(string= b['na']),
                     h.String(string= b['tl1']),
                     h.String(string= b['tl2']),
                     ]
                    for b in bezugspersonen_list],
            button= (aktueller_fall and hinzufuegen_button and
                     h.Button(value="Hinzufügen",
                            tip="Bezugsperson hinzufügen",
                            onClick=
                       "go_to_url('persneu?akid=%(akte_id)d&fallid=%(id)d&klerv=1')" %
                              aktueller_fall,
                            ) or None),
            )
        # Löschen unerwünschter icons aus den Tabellenitems.
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


        bisherige_kontakte = h.FieldsetDataTable(
            legend = 'Liste der bisherigen Kontakte',
            empty_msg = "Bisher keine Kontakte eingetragen.",
            headers = ('Mitarbeiter', 'Art', 'Datum', 'Dauer', 'Notiz'),
            daten =  [[h.String(string = b['mit_id__na']),
                       h.String(string = b['art__name']),
                       h.Datum(date =  b.getDate('k')),
                       h.String(string = b['dauer__name']),
                       h.String(string = b['no']),]
                      for b in beratungskontakte],
            )
    def get_beratungskontakte(self, beratungskontakte,
                                 aktueller_fall=None, # falls False, kein Hinzufügen-Button, inaktive edit/view buttons
                                 edit_button=False, # falls False, kein edit button
                                 hinzufuegen_button=False, # falls False, kein hinzufügen button
                                 ):
        BS = config.BERATUNGSKONTAKTE_BS
        if BS:
            art_feld = 'art_bs'
            headers=('Datum', 'Mitarbeiter', 'Klienten', 'Art',
                       'Teilnehmer', 'Dauer in Minuten', 'BS', 'Notiz')
        else:
            art_feld = 'art'
            headers=('Datum', 'Mitarbeiter', 'Klienten', 'Art',
                     'Dauer', 'BS', 'Notiz')
        beratungskontakte.sort('ky', 'km', 'kd')
        if aktueller_fall:
            updurl = 'updbkont?bkontid=%%(id)d&fallid=%s' % aktueller_fall['id']
            rmurl =   'rmbkont?bkontid=%%(id)d&fallid=%s' % aktueller_fall['id']
        bisherige_kontakte = h.FieldsetDataTable(
            legend='Beratungskontakte',
            empty_msg="Bisher keine Kontakte eingetragen.",
            noheaders=2,
            headers=headers,
            daten=[[(edit_button and (aktueller_fall and 
                                      h.Icon(href= updurl % b,
                                             icon= "/ebkus/ebkus_icons/edit_button.gif",
                                             tip= 'Beratungskontakt bearbeiten')
                                      or h.Dummy())) or None,
                    (edit_button and (aktueller_fall and
                                      h.Icon(href=rmurl % b,
                                             icon="/ebkus/ebkus_icons/del_button.gif",
                                             tip='Beratungskontakt endgültig löschen')
                                      or h.Dummy())) or None,
                    h.Datum(date=b.getDate('k'),
                            time=b.getTime('k')),
                    h.String(string=', '.join([m['na']
                                               for m in b['mitarbeiter']]),
                             ),
                    h.String(string=', '.join([f['akte__na']
                                               for f in b['faelle']]),
                             ),
                    h.String(string=b['%s__name'% art_feld]),
                    BS and h.String(string=', '.join([Code(i)['name']
                                                      for i in b['teilnehmer_bs'].split()]),
                                    ) or None,
                    BS and h.String(string="%(dauer)s / %(brutto)s" % b,
                                    tip='Netto/Brutto') or
                    h.String(string=bcode('fskd', b['dauer'])['name']),
                    h.String(string=b['jghkontakte'] or '',
                             tip='Anzahl der Kontakte im Sinne der Bundesjugendstatistik'),
                    h.String(string=b['no']),
                    ]
                   for b in beratungskontakte],
            button=(aktueller_fall and hinzufuegen_button and
                    h.Button(value="Hinzufügen",
                             tip="Beratungskontakt hinzufügen",
                             onClick=
                             "go_to_url('bkontneu?akid=%(akte_id)s&fallid=%(id)s')" %
                             aktueller_fall,
                             ) or None),
            )
        return bisherige_kontakte

##     def get_beratungskontakte_bs(self, beratungskontakte,
##                                  aktueller_fall=None, # falls False, kein Hinzufügen-Button, inaktive edit/view buttons
##                                  edit_button=False, # falls False, kein edit button
##                                  hinzufuegen_button=False, # falls False, kein hinzufügen button
##                                  ):
##         beratungskontakte.sort('ky', 'km', 'kd')
##         if aktueller_fall:
##             updurl = 'updbkont?bkontid=%%(id)d&fallid=%s' % aktueller_fall['id']
##         bisherige_kontakte = h.FieldsetDataTable(
##             legend='Beratungskontakte',
##             empty_msg="Bisher keine Kontakte eingetragen.",
##             headers=('Datum', 'Mitarbeiter', 'Klienten', 'Art',
##                        'Teilnehmer', 'Dauer in Minuten', 'Notiz'),
##             daten=[[(edit_button and (aktueller_fall and 
##                                       h.Icon(href= updurl % b,
##                                              icon= "/ebkus/ebkus_icons/edit_button.gif",
##                                              tip= 'Beratungskontakt bearbeiten')
##                                       or
##                                       h.IconDead(icon= "/ebkus/ebkus_icons/edit_button_inaktiv_locked.gif",
##                                                  tip= 'Funktion gesperrt'))) or None,
##                     h.Datum(date =  b.getDate('k')),
##                     h.String(string=', '.join([m['na']
##                                                for m in b['mitarbeiter']]),
##                              ),
##                     h.String(string=', '.join([f['akte__na']
##                                                for f in b['faelle']]),
##                              ),
##                     h.String(string=b['art_bs__name']),
##                     h.String(string=', '.join([Code(i)['name']
##                                                for i in b['teilnehmer'].split()]),
##                              ),
##                     h.String(string=b['dauer']),
##                     h.String(string=b['no']),
##                     ]
##                    for b in beratungskontakte],
##             button=(aktueller_fall and hinzufuegen_button and
##                     h.Button(value="Hinzufügen",
##                              tip="Beratungskontakt hinzufügen",
##                              onClick=
##                              "go_to_url('bkontneu?akid=%(akte_id)s&fallid=%(id)s')" %
##                              aktueller_fall,
##                              ) or None),
##             )
##         return bisherige_kontakte
    


    def get_code_tabelle(self, kat, links=True, view=''):
        codes = kat['codes'].sorted('sort')
        bereichskat = kat['flag']
        if bereichskat:
            headers=('Code', 'Merkmal', 'Sort', 'Min', 'Max', 'Off', 'Ab', 'Dokumentation')
        else:
            headers=('Code', 'Merkmal', 'Sort', 'Off', 'Ab', 'Dokumentation')
        code_tabelle = h.FieldsetDataTable(
            legend="Alle Merkmale der Kategorie '%s'" % kat['name'],
            anchor="%(id)s" % kat,
            daten_before_headers = links and
            [[h.Icon(href="codeneu?katid=%s&view=%s" % (kat['id'], view),
                     icon= "/ebkus/ebkus_icons/neu_button.gif",
                     tip="Merkmal zur Antwortkategorie hinzufügen",
                     ),
              h.DummyItem(n_col=5),
              ]] or (),
            headers=headers,
            daten=[[links and h.Link(string="%(code)s" % code,
                                     tip="Merkmal bearbeiten",
                                     url="updcode?codeid=%s&view=%s" % (code['id'], view))
                    or h.String(string="%(code)s" % code),
                    h.String(string="%(name)s" % code),
                    h.String(string="%(sort)s" % code),
                    bereichskat and h.String(string="%(mini)s" % code) or None,
                    bereichskat and h.String(string="%(maxi)s" % code) or None,
                    h.String(string="%(off)s" % code),
                    h.String(string=code['dy'] and "%(dm)s<b>.</b>%(dy)s" % code or ''),
                    h.String(string=code['dok'] or '')]
                   for code in codes],
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
                   [h.TextItem(label='Gruppennummer',
                               name='xxx',
                               value="%(gn)s" % gruppe,
                               readonly=True,
                               tip='Gruppennummer',
                               ),
                    h.DatumItem(label='Beginn',
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
                    ],
                   [readonly and
                    h.TextItem(label='Gruppenart',
                               name='xxx',
                               value="%(grtyp__name)s" % gruppe,
                               readonly=True,
                               tip='Art der Gruppe',
                               ) or
                    h.SelectItem(label='Gruppenart',
                                 name='grtyp',
                                 tip='Art der Gruppe',
                                 readonly=readonly,
                                 options=self.for_kat('grtyp', sel=gruppe['grtyp']),
                                 ),
                    readonly and 
                    h.TextareaItem(label='Mitarbeiter',
                                   name='xxx',
                                   value="%(mitarbeiternamen)s" % gruppe,
                                   readonly=True,
                                   #rows="2",
                                   rowspan="2",
                                   tip='Teilnehmende Mitarbeiter',
                                   ) or
##                     h.TextItem(label='Mitarbeiter',
##                                name='xxx',
##                                value="%(mitarbeiternamen)s" % gruppe,
##                                readonly=True,
##                                rowspan="2",
##                                tip='Teilnehmende Mitarbeiter',
##                                ) or
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
                   [readonly and h.TextItem(label='Teilnehmer',
                               name='xxx',
                               value="%(teiln__name)s" % gruppe,
                               readonly=True,
                               tip='Art der Teilnehmer',
                               ) or
                    h.SelectItem(label='Teilnehmer',
                                 name='teiln',
                                 tip='Art der Teilnehmer',
                                 readonly=readonly,
                                 options=self.for_kat('teiln', sel=gruppe['teiln']),
                                 ),
                    h.TextItem(label='Stundenzahl',
                               name='stzahl',
                               readonly=readonly,
                               value=gruppe['stzahl'] or '',
                               tip='Geplante Stundenzahl insgesamt über die Dauer der Gruppe',
                               class_='textboxmid',
                               ),
                    ],
                   ],
            button=button,
            )
        return gruppendaten

    def grundgesamtheit(self, bis_jahr=None, von_jahr=None, quartal=None,
                        stellen_ids=None,
                        legend='Grundgesamtheit',
                        submit_value=None,
                        show_quartal=True,
                        show_welche=False,
                        welche=None):
        "Für Auswertungen. Legt Jahre und Stellen fest."
        #print 'GG', von_jahr, bis_jahr
        if not bis_jahr:
            bis_jahr = today().year
        if von_jahr == bis_jahr or not von_jahr:
            erster_eintrag = ' '
            von_jahr = None
        else:
            erster_eintrag = None
        if not stellen_ids:
            stellen_ids = [self.stelle['id']]
        tmpl = '<option value="%s"%s>%s</option>'
        sel = ' selected="selected"'
        welche_options = '\n'.join([tmpl % (v,
                                            v==welche and sel or '',
                                            v.capitalize())
                                    for v in ('laufend', 'abgeschlossen', 'alle')])
        res = h.FieldsetInputTable(
            legend=legend,
            daten=[[show_welche and h.SelectItem(label='Welche',
                                 name='w',
                                 options=welche_options,
                                 tip='Auszählung nur für laufende, abgeschlossene oder alle Fälle',
                                 ) or
                    show_quartal and h.SelectItem(label='Quartal',
                                 name='quartal',
                                 class_='listbox30',
                                 tip='Wählen Sie das Quartal, für das eine Auszählung erfolgen soll',
                                 options=self.for_quartal(sel=quartal, erster_eintrag=' '),
                                 ) or h.DummyItem(),
                    h.SelectItem(label='Jahr',
                                 name='bis_jahr',
                                 class_='listbox45',
                                 tip='Wählen Sie das Jahr, für das eine Auszählung erfolgen soll',
                                 options=self.for_jahre(sel=bis_jahr),
                                 ),
                    h.SelectItem(label='Stelle',
                                 name='stz',
                                 multiple=True,
                                 rowspan=2,
                                 tip='Eine oder mehrere Stellen auswählen',
                                 size=3,
                                 options=self.for_kat('stzei', sel=stellen_ids),
                                 ),
                    ],
                   [h.SelectItem(label='Frühere Jahre einbeziehen ab',
                                 name='von_jahr',
                                 class_='listbox45',
                                 n_label=3,
                                 n_col=4,
                                 tip='Nur für Auswertungen über mehrere Jahre hinweg',
                                 options=self.for_jahre(sel=von_jahr,
                                                        erster_eintrag=erster_eintrag),
                                 ),
                    ],
                   [h.Dummy(n_col=4)],
                   ],
            button=submit_value and h.Button(value=submit_value,
                                             name='op',
                                             tip=submit_value,
                                             type='submit',
                                             n_col=4,
                                             ) or None,

            )
        return res

    def get_hauptmenu(self):
        return h.FieldsetInputTable(
            daten=[[h.Button(value='Hauptmenü',
                             onClick="go_to_url('menu')",
                             tip="Hauptmenü",
                             ),
            ]]
            )

    def get_zurueck(self):
        return h.FieldsetInputTable(
            daten=[[h.Button(value='Zurück',
                             onClick="history.back()",
                             tip="Zurück",
                             ),
            ]]
            )

    def get_auswertungs_menu(self):
        menu = h.FieldsetInputTable(
            daten=[[h.Button(value="Hauptmenü",
                             tip="Zum Hauptmenü",
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
                                 tip='Wählen Sie die gewünschte andere Auswertung',
                                 options=self.for_auswertungen(),
                                 ),
                    ]])
        return menu

    def beratungen(self, welche, mitarbeiter=None,
                   stelle=None,
                   ab_jahr=None,
                   ab_fallnummer=None,
                   sort=()):
        assert welche in ('laufend', 'abgeschlossen', 'alle')
        assert ab_jahr and ab_fallnummer or not ab_fallnummer
        where = 'fall.zday %s 0' % (welche=='laufend' and '=' or
                                    welche=='abgeschlossen' and '>' or
                                    welche=='alle' and '>='
                                    )
        # nur die letzte Zuständigkeit deren Endedatum gleich dem ZDA-Datum ist
        where += """ and fall.zday = zustaendigkeit.ey and 
        fall.zdam = zustaendigkeit.em and 
        fall.zdad = zustaendigkeit.ed"""
        
        if mitarbeiter:
            where += ' and mitarbeiter.id=%s' % mitarbeiter['id']
        if stelle:
            where += ' and akte.stzbg=%s' % stelle['id']
        if ab_jahr:
            where += ' and fall.bgy >= %s' % ab_jahr
        fall_list = FallList(
            where=where,
            join=[('zustaendigkeit', 'zustaendigkeit.fall_id=fall.id'),
                  ('akte', 'fall.akte_id=akte.id'),
                  ('mitarbeiter', 'zustaendigkeit.mit_id=mitarbeiter.id')])
        if ab_jahr and ab_fallnummer:
            def ab_fn(fall):
                j = fall['bgy']
                c = fall['fn_count'] # Fallnummerzähler, definiert in ebapi.py
                return  j > ab_jahr or (j == ab_jahr and c >= ab_fallnummer)
            fall_list = fall_list.filter(ab_fn)
        fall_list.sort(*sort)
        return fall_list

    def beratungen_fall(self, mitarbeiter=None,
                        klname=None,
                        klvorname=None,
                        klnachname=None,
                        fn=None,
                        sort=()):
        join=[('zustaendigkeit', 'zustaendigkeit.fall_id=fall.id'),
              ('akte', 'fall.akte_id=akte.id'),
              ('mitarbeiter', 'zustaendigkeit.mit_id=mitarbeiter.id')]
        # nur die eigene Stelle
        where = "akte.stzbg=%s" % self.stelle['id']
        # nur die letzte Zuständigkeit deren Endedatum gleich dem ZDA-Datum ist
        where += """ and fall.zday = zustaendigkeit.ey and 
        fall.zdam = zustaendigkeit.em and 
        fall.zdad = zustaendigkeit.ed"""
        if klname:
            expr = escape('%' + klname + '%')
            where += " and (akte.vn like %s or akte.na like %s)" % \
            (expr, expr)
        if klvorname:
            expr = escape('%' + klvorname + '%')
            where += " and (akte.vn like %s)" % (expr,)
        if klnachname:
            expr = escape('%' + klnachname + '%')
            where += " and (akte.na like %s)" % (klnachname,)
        if klname or klvorname or klnachname:
            sort = ('akte__na', 'akte__vn', 'bgy', 'bgm', 'bgd')
        if fn:
            expr = escape('%' + fn + '%')
            where += " and fall.fn like %s" % expr
            sort = ('bgy', 'fn_count')
        if mitarbeiter:
            where += " and mitarbeiter.id = %s" % mitarbeiter['id']
        fall_list = FallList(
            where=where,
            join=join,
            )
        fall_list.sort(*sort)
        return fall_list
