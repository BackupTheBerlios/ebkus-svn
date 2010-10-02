# coding: latin-1

"""Module für Akte und Fall."""

import string,time,sys
import logging

from ebkus.db.sql import SQL
from ebkus.app import Request
from ebkus.config import config
from ebkus.app.ebapi import Akte, Fall, Gruppe, FallList, GruppeList, Altdaten, Anmeldung, \
     Zustaendigkeit, today, cc, check_list, check_code, check_int_not_empty, EE
from ebkus.app_surface.standard_templates import *
from ebkus.app_surface.akte_templates import *

import ebkus.html.htmlgen as h
from ebkus.html.akte_share import akte_share

class _akte(Request.Request, akte_share):
    """Gemeinsame Methode zur Anzeige der Aktenformulare.
    """
    def _process(self,
                 title,
                 file,
                 akte,
                 anmeldung,
                 formname,
                 hidden,
                 force_strkat=None,
                 ):
        notiz = h.FieldsetInputTable(
            legend='Notiz',
            daten=[[h.TextItem(label='Notiz',
                             name='no',
                             value=akte['no'],
                             class_='textboxverylarge',
                             tip="Freies Feld für Notizen",
                             )],
                   ]
            )
        klientendaten = self.get_klientendaten(akte)
        anschrift = self.get_anschrift(akte, force_strkat)
        falldaten = leistung = altdaten = None
        if file in ('akteeinf', 'waufneinf'):
            falldaten = h.FieldsetInputTable(
                legend='Falldaten',
                daten=[[h.SelectItem(label='Bearbeiter',
                                     name='zumitid',
                                     tip='Fallbearbeiter auswählen',
                                     options=self.for_mitarbeiter(sel=self.mitarbeiter['id'])),
                        h.DatumItem(label='Anmeldedatum',
                                    name='zubg',
                                    tip='Anmeldedatum',
                                    year=today().year,
                                    month=today().month),
                        ]],
                )
            leistung = h.FieldsetInputTable(
                legend='Leistung',
                daten=[[h.SelectItem(label='Mitarbeiter',
                                     name='lemitid',
                                     tip='Mitarbeiter auswählen, der die Leistung erbracht hat',
                                     options=self.for_mitarbeiter(sel=self.mitarbeiter['id'])),
                        h.SelectItem(label='Leistung',
                                     name='le',
                                     tip='Art der erbrachten Leistung',
                                     class_='listbox250',
                                     options=self.for_kat('fsle', akte['fs'])),
                        ],[h.DummyItem(),
                           h.DatumItem(label='Am',
                                       name='lebg',
                                       tip='Datum der Leistung oder des Beginns der Leistung',
                                       date=today()),
                           ]],
                )

        if file=='akteeinf' and \
               SQL("select count(*) from altdaten").execute()[0][0] > 0:
            # Altdaten vorhanden
            altdaten = h.FieldsetInputTable(
                legend='Nach Altdaten suchen',
                tip="Bitte zuerst nach Altdaten suchen, dann erst weitere Daten eingeben",
                button=h.Button(value='Altdaten',
                                name='xxx',
                                onClick="go_to_url('altlist')",
                                tip="Suche in den Altdaten aus früheren EDV-Systemen",
                                ),
                )
        if config.ANMELDUNGSDATEN_OBLIGATORISCH and file in ('akteeinf', 'waufneinf'):
            anmeldungf = self.get_anmeldekontakt(anmeldung)
        else:
            anmeldungf = None
        res = h.FormPage(
            title=title,
            name=formname,action="klkarte",method="post",
            breadcrumbs = (('Hauptmenü', 'menu'),
                          (not file=='akteeinf') and
                           ('Klientenkarte', 'klkarte?akid=%s' % akte['id'])
                           or None,
                           ),
            hidden=(("akid", akte['id']),
                    ("file", file),
                    ("strid", ""), # wird nur von strkat mit javascript gesetzt
                    ) + hidden,
            rows=(h.Pair(left=klientendaten,
                         right=(altdaten, anschrift),
                         ),
                  notiz,
                  anmeldungf,
                  falldaten,
                  leistung,
                  h.SpeichernZuruecksetzenAbbrechen(),
                  ),
            )
        return res.display()

class akteneu(_akte):
    """Neue Fallakte anlegen (Tabellen: Akte, Fall, Zuständigkeit, Leistung)."""
    permissions = Request.UPDATE_PERM
    def processForm(self, REQUEST, RESPONSE):
        alt_ids = check_list(self.form, 'uebern', 'Fehler in Altdaten', [])
        if len(alt_ids) > 1:
            raise EE("Bitte nur einen Eintrag zur Übernahme markieren!")
        if alt_ids:
            alt = Altdaten(alt_ids[0])
        else:
            alt = {}
        gs_alt = alt.get('geschlecht')
        if gs_alt:
            gs = (gs_alt=='w' and cc('gs', '2')) or (gs_alt=='m' and cc('gs', '1'))
        else:
            gs = ' '
        if alt:
            no = "Alte Fallnummer: %(fallnummer)s, Jahr: %(jahr)s, Früherer Mitarbeiter: %(mitarbeiter)s" % alt
        else:
            no = ''
        str = alt.get('strasse', '')
        if str:
            for end in ('trasse', 'traße'):
                if str.endswith(end):
                    i = str.index(end)
                    str = str[:i] + 'tr.'
        akte = Akte()
        akte.init(
            id=Akte().getNewId(),
            fs=cc('fsfs', '999'),
            vn=alt.get('vorname', ''),
            na=alt.get('name', ''),
            gb=alt.get('geburtsdatum', ''),
            ort=alt.get('ort', ''),
            plz=alt.get('plz', ''),
            str=str,
            hsnr=alt.get('hausnummer', '').upper(),
            gs=gs,
            tl1=alt.get('telefon1', ''),
            tl2=alt.get('telefon2', ''),
            no=no,
            aufbew=cc('aufbew', '1'),
            stzbg=self.stelle['id'],
            lage=(config.STRASSENKATALOG and  cc('lage', '0') or
                  cc('lage', '1')),
            )
        hidden = (('stzbg', akte['stzbg']),
                  )
        anm = None
        if config.ANMELDUNGSDATEN_OBLIGATORISCH:
            anm = Anmeldung()
            anm.init(
                id=Anmeldung().getNewId(),
                zm=cc('fszm', '999'),
                )
            # Nachname und Telefon des Klienten
            # im Formular anbieten.
            anm['von'] = akte['na']
            anm['mtl'] = akte['tl1']
            hidden += (('anmid', anm['id']),)
        
        return self._process(
            title='Neue Akte anlegen',
            file='akteeinf',
            akte=akte,
            anmeldung=anm,
            formname='akteform',
            hidden=hidden,
            )

class waufnneu(_akte):
    """Wiederaufnahme einer vorhandener  Fallakte
    (Tabellen: Akte, Fall, Zuständigkeit, Leistung)."""
    permissions = Request.UPDATE_PERM
    def processForm(self, REQUEST, RESPONSE):
        akid = self.form.get('akid')
        if not akid:
            raise EE("Keine ID fuer die Akte erhalten")
        akte = Akte(akid)
        hidden=(('fallid', Fall().getNewId()),
                ('status', cc('stand', 'l')),
                )
        anm = None
        if config.ANMELDUNGSDATEN_OBLIGATORISCH:
            anm = Anmeldung()
            anm.init(
                id=Anmeldung().getNewId(),
                zm=cc('fszm', '999'),
                )
            # Nachname und Telefon des Klienten
            # im Formular anbieten.
            anm['von'] = akte['na']
            anm['mtl'] = akte['tl1']
            hidden += (('anmid', anm['id']),)
        return self._process(
                 title="Wiederaufnahme des Klienten",
                 file='waufneinf',
                 akte=akte,
                 anmeldung=anm,
                 formname='akteform',
                 hidden=hidden,
                 )
        
class updakte(_akte):
    """Akte ändern (Tabelle Akte)."""
    permissions = Request.UPDATE_PERM
    def processForm(self, REQUEST, RESPONSE):
        strkat = self.form.get('strkat')
        if strkat == '0':
            force_strkat = False
        elif strkat == '1':
            force_strkat = True
        else:
            force_strkat = None
        if self.form.has_key('akid'):
            akid = self.form.get('akid')
            akte = Akte(akid)
        else:
            self.last_error_message = "Keine ID fuer die Akte erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
        return self._process(
            title='Akte aktualisieren',
            file='updakte',
            akte=akte,
            anmeldung=None,
            formname='akteform',
            hidden=(),
            force_strkat=force_strkat,
            )

class updfall(_akte):
    """Fall updaten (Tabelle: Fall)."""
    permissions = Request.UPDATE_PERM
    def processForm(self, REQUEST, RESPONSE):
        if self.form.has_key('fallid'):
            fallid = self.form.get('fallid')
        else:
            self.last_error_message = "Keine ID fuer den Fall erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
        fall = Fall(fallid)
        zustaendigkeiten_list = fall['zustaendigkeiten']
        beginndatum = h.FieldsetInputTable(
            legend='Beginndatum',
            daten=[[h.DatumItem(label='Fallbeginn',
                                name='bg',
                                tip='Fallbeginn',
                                date=fall.getDate('bg')),
            ]],
            )
        res = h.FormPage(
            title='Beginndatum ändern',
            name='akteform',action="klkarte",method="post",
            breadcrumbs = (('Hauptmenü', 'menu'),
                           ('Klientenkarte', 'klkarte?akid=%(akte_id)s' % fall),
                           ),
            hidden=(("fallid", fallid),
                    ("file", 'updfall'),
                    ),
            rows=(beginndatum,
                  self.get_zustaendigkeiten(zustaendigkeiten_list),
                  h.SpeichernZuruecksetzenAbbrechen(),
                  ),
            )
        return res.display()
        
class zda(_akte):
    """Fallakte abschliessen (Tabellen: Fall und Zuständigkeit)."""
    permissions = Request.UPDATE_PERM
    def processForm(self, REQUEST, RESPONSE):
        if self.form.has_key('fallid'):
            fallid = self.form.get('fallid')
        else:
            self.last_error_message = "Keine ID fuer den Fall erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
        fall = Fall(fallid)
        zustaendigkeiten_list = fall['zustaendigkeiten']
        zustaendigkeiten_list.sort('bgd', 'bgm', 'bgy')
        aktuell_zustaendig = fall['zustaendig']
        falldaten = h.FieldsetInputTable(
            legend='Falldaten',
            daten=[[h.DatumItem(label='Beginndatum',
                                name='bg',
                                tip='Fallbeginn',
                                date=fall.getDate('bg')),
                    h.DatumItem(label='Abschlussdatum',
                                name='zda',
                                tip='Fallabschlussdatum',
                                date=today()),
            ]],
            )
        res = h.FormPage(
            title='Abschlussdatum eintragen',
            name='akteform',action="klkarte",method="post",
            breadcrumbs = (('Hauptmenü', 'menu'),
                           ('Klientenkarte', 'klkarte?akid=%(akte_id)s' % fall),
                           ),
            hidden=(("fallid", fallid),
                    ("file", 'zdaeinf'),
                    ("aktuellzustid", aktuell_zustaendig['id']),
                    ("aktuellmitid", aktuell_zustaendig['mit_id__id']),
                    ),
            rows=(falldaten,
                  self.get_bisherige_zustaendigkeit(
            aktuell_zustaendig,
            legend='Bisherige Zuständigkeit wird ausgetragen'),
                  self.get_zustaendigkeiten(zustaendigkeiten_list),
                  h.SpeichernZuruecksetzenAbbrechen(),
                  ),
            )
        return res.display()
        
class zdar(_akte):
    """Fallabschluss rückgängig machen und letzte Zustaendigkeit wiederherstellen
    (Tabellen: Fall und Zuständigkeit)."""
    permissions = Request.UPDATE_PERM
    def processForm(self, REQUEST, RESPONSE):
        fallid = self.form.get('fallid')
        if not fallid:
            raise EE("Keine ID fuer den Fall erhalten")
        fall = Fall(fallid)
        zuletzt_zustaendig = fall['zuletzt_zustaendig']
        res = h.FormPage(
            title='Abschlussdatum rückgängig machen',
            name='zdarform',action="klkarte",method="post",
            breadcrumbs = (('Hauptmenü', 'menu'),
                           ('Klientenkarte', 'klkarte?akid=%(akte_id)s' % fall),
                           ),
            hidden=(("fallid", fallid),
                    ("file", 'zdareinf'),
                    ),
            rows=(self.get_bisherige_zustaendigkeit(
            zuletzt_zustaendig,
            legend='Letzte Zuständigkeit wird wiederhergestellt',
            ),
                  h.SpeichernZuruecksetzenAbbrechen(),
                  ),
            )
        return res.display()

class _zust(_akte):
    def _process(self,
                 title,
                 file,
                 fall,
                 zustaendigkeit, # Form schon fertig, da unterschiedlich upd/neu
                 hidden,
                 ):
        aktuell_zustaendig = fall['zustaendig']
        zustaendigkeiten_list = fall['zustaendigkeiten']
        zustaendigkeiten_list.sort('bgy', 'bgm', 'bgd')
        if file == 'zusteinf':
            bisherige_zustaendigkeit = self.get_bisherige_zustaendigkeit(
                aktuell_zustaendig,
                legend='Bisherige Zuständigkeit wird ausgetragen',
                )
        elif file == 'updzust':
            bisherige_zustaendigkeit = None
        res = h.FormPage(
            title=title,
            name='zustform',action="klkarte",method="post",
            breadcrumbs = (('Hauptmenü', 'menu'),
                           ('Klientenkarte', 'klkarte?akid=%(akte_id)s' % fall),
                           ),
            hidden=hidden,
            rows=(self.get_klientendaten_kurz(fall),
                  zustaendigkeit,
                  bisherige_zustaendigkeit,
                  self.get_zustaendigkeiten(zustaendigkeiten_list),
                  h.SpeichernZuruecksetzenAbbrechen(),
                  ),
            )
        return res.display()

class zustneu(_zust):
    """Neue Zuständigkeit eintragen. (Tabelle: Zuständigkeit.)"""
    permissions = Request.UPDATE_PERM
    def processForm(self, REQUEST, RESPONSE):
        if self.form.has_key('fallid'):
            fallid = self.form.get('fallid')
        else:
            self.last_error_message = "Keine ID für den Fall erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
        fall = Fall(fallid)
        aktuell_zustaendig = fall['zustaendig']
        neue_zust = Zustaendigkeit()
        neue_zust.init(
            id=Zustaendigkeit().getNewId(),
            mit_id=self.mitarbeiter['id'],
            fall_id=fall['id'],
            )
        neue_zust.setDate('bg', today())
        zustaendigkeit = h.FieldsetInputTable(
            legend="Neue Zuständigkeit eintragen",
            daten=[[h.SelectItem(label='Bearbeiter',
                                 name='mitid',
                                 tip='Fallbearbeiter auswählen',
                                 options=self.for_mitarbeiter(neue_zust['mit_id'])),
                    h.DatumItem(label='Beginn',
                                name='bg',
                                tip='Datum des Zuständigkeitbeginns',
                                date=neue_zust.getDate('bg')),
                    # keine Endedataum
                    ]],
            )
        return self._process(
            title="Neue Zust&auml;ndigkeit eintragen",
            file='zusteinf',
            fall=fall,
            zustaendigkeit=zustaendigkeit,
            hidden=(('zustid', neue_zust['id']),
                    ("aktuellzustid", aktuell_zustaendig['id']),
                    ('file', 'zusteinf'),
                    ('fallid', fall['id']),
                    ),
            )
        
class updzust(_zust):
    """Neue Zuständigkeit eintragen. (Tabelle: Zuständigkeit.)"""
    permissions = Request.UPDATE_PERM
    def processForm(self, REQUEST, RESPONSE):
        if self.form.has_key('zustid'):
            id  = self.form.get('zustid')
        else:
            self.last_error_message = "Keine ID für die Zuständigkeit erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
        zust = Zustaendigkeit(id)
        fall = Fall(zust['fall_id'])
        zustaendigkeit = h.FieldsetInputTable(
            legend="Zuständigkeit bearbeiten",
            daten=[[h.SelectItem(label='Bearbeiter',
                                 name='mitid',
                                 tip='Fallbearbeiter auswählen',
                                 options=self.for_mitarbeiter(zust['mit_id'])),
                    h.DatumItem(label='Beginn',
                                name='bg',
                                tip='Datum des Zuständigkeitbeginns',
                                date=zust.getDate('bg')),
                    h.DatumItem(label='Ende',
                                name='e',
                                tip='Datum des Zuständigkeitendes',
                                date=zust.getDate('e')),
                    ]],
            )

        return self._process(
            title="Zust&auml;ndigkeit bearbeiten",
            file='updzust',
            fall=fall,
            zustaendigkeit=zustaendigkeit,
            hidden=(('zustid', zust['id']),
                    ('file', 'updzust'),
                    ),
            )


class rmaktenf(Request.Request, akte_share):
    """Einzelnen Fall löschen."""
    permissions = Request.ADMIN_PERM
    def processForm(self, REQUEST, RESPONSE):
        fn = self.form.get('fn')
        gn = self.form.get('gn')
        if fn and gn:
            raise EE("Es kann entweder ein Fall oder eine Gruppe gelöscht werden, nicht beides zugleich")
        statistik_auch = (self.form.get('statistik_auch') == '1')
        ok = self.form.get('ok')
        fall_id = self.form.get('fallid')
        gruppe_id = self.form.get('gruppeid')
        if fn and not ok and not fall_id:
            faelle = FallList(where="fn = '%s'" % fn)
            if len(faelle) < 1:
                raise EE("Kein Fall mit dieser Fallnummer gefunden.")
            elif len(faelle) > 1:
                # darf nicht passieren
                raise EE("Mehrere passende Fälle gefunden.")
            else:
                fall = faelle[0]
            if not fall['aktuell']:
                raise EE("Fall <em>%s</em> ist abgeschlossen. Es können nur aktuelle Fälle gelöscht werden."
                         % fn)
            akte = fall['akte']
            statistik_vorhanden = bool(fall['fachstatistiken'] or
                                       fall['jgh_statistiken'] or
                                       fall['jgh07_statistiken'])
            stattext = ''
            if statistik_vorhanden:
                if statistik_auch:
                    stattext = "(Die zugehörige Bundes- und Fachstatistik wird ebenfalls gelöscht.)"
                else:
                    stattext = "(Die zugehörige Bundes- und Fachstatistik bleibt erhalten.)"
            if len(akte['faelle']) == 1:
                letzter_fall = True
                legend = 'Akte endgültig löschen'
                zeilen=("Der Fall <em>%(fn)s</em> ist der einzige in der Akte <em>%(name)s</em>." % fall,
                        "Da eine Akte immer mindestens einen Fall haben muss, wird die "
                        "Akte inklusive aller Stammdaten ebenfalls gelöscht.",
                        stattext,
                        "Soll der Fall <em>%(fn)s</em> mitsamt der gesamten Akte <em>%(name)s</em> "
                        "endgültig gelöscht werden?" % fall,
                        )
            else:
                letzter_fall = False
                legend = 'Fall endgültig löschen'
                zeilen=("Soll der Fall <em>%(fn)s (%(name)s)</em> endgültig gelöscht werden?" % fall,
                        stattext,
                        )
            hidden = (('fallid', fall['id']),
                      ('statistik_auch', statistik_auch and '1' or ''),
                      ('ok', '1'),
                )
            return h.SubmitOrBack(
                legend=legend,
                action='rmaktenf',
                method='post',
                hidden=hidden,
                zeilen=zeilen,
                ).display()
        elif gn and not ok and not gruppe_id:
            gruppen = GruppeList(where="gn = '%s'" % gn)
            if len(gruppen) < 1:
                raise EE("Kein Gruppe mit dieser Gruppennummer gefunden.")
            elif len(gruppen) > 1:
                # darf nicht passieren
                raise EE("Mehrere passende Gruppen gefunden.")
            else:
                gruppe = gruppen[0]
            if gruppe['ey']:
                raise EE(("Gruppe <em>%s</em> hat eine Endedatum, ist also abgeschlossen. " +
                         "Es können nur laufende Gruppen gelöscht werden.")
                         % gn)
            if gruppe['faelle'] or gruppe['bezugspersonen']:
                raise EE(("Die Gruppe <em>%s</em> hat Teilnehmer. " +
                         "Es können nur Gruppen ohne Teilnehmer gelöscht werden.")
                         % gn)
            legend = 'Gruppe endgültig löschen'
            zeilen=("Soll die Gruppe <em>%(gn)s (%(name)s)</em> endgültig gelöscht werden?" % gruppe,
                        )
            hidden = (('gruppeid', gruppe['id']),
                      ('ok', '1'),
                )
            return h.SubmitOrBack(
                legend=legend,
                action='rmaktenf',
                method='post',
                hidden=hidden,
                zeilen=zeilen,
                ).display()
        elif fall_id and ok == '1':
            fall = Fall(fall_id)
            akte = fall['akte']
            akten = [akte]
            name = akte['name']
            fn = fall['fn']
            from ebkus.app.ebupd import remove_fall, remove_akte
            if len(akte['faelle']) == 1:
                ganze_akte_loeschen = True
                remove_akte(akte,
                            statistik_auch=statistik_auch,
                            aktuell_auch=True)
                legend = "Ganze Akte gelöscht"
            else:
                ganze_akte_loeschen = False
                remove_fall(fall,
                            statistik_auch=statistik_auch,
                            aktuell_auch=True)
                legend = "Fall gelöscht"
            geloeschter_fall = h.FieldsetDataTable(
                legend=legend,
                headers=('Fallnummer', 'Name'),
                daten=[[h.String(string=fn),
                        h.String(string=name),
                        ]],
                )
            res = h.Page(
                title=legend,
                breadcrumbs = (('Aministratorhauptmenü', 'menu'),
                               ('Einzelnen Fall löschen', None),
                               ),
                rows=(self.get_hauptmenu(),
                      geloeschter_fall,
                      ),
                )
            return res.display()
        elif gruppe_id and ok == '1':
            gruppe = Gruppe(gruppe_id)
            gn = gruppe['gn']
            name = gruppe['name']
            from ebkus.app.ebupd import remove_fall, remove_akte, remove_gruppe
            remove_gruppe(gruppe)
            legend = "Gruppe gelöscht"
            geloeschte_gruppe = h.FieldsetDataTable(
                legend=legend,
                headers=('Gruppennummer', 'Name'),
                daten=[[h.String(string=gn),
                        h.String(string=name),
                        ]],
                )
            res = h.Page(
                title=legend,
                breadcrumbs = (('Aministratorhauptmenü', 'menu'),
                               ('Einzelne Gruppe löschen', None),
                               ),
                rows=(self.get_hauptmenu(),
                      geloeschte_gruppe,
                      ),
                )
            return res.display()
            
        auswahl = h.FieldsetFormInputTable(
            name="rmfallanzeigen",
            action="rmaktenf",
            method="post",
            legend='Fallnummer des zu löschenden Falls',
            daten=[[h.TextItem(label='Fallnummer',
                               name='fn',
                               value='',
                               tip='Fallnummer des zu löschenden Falls'
                               ),
                    h.CheckItem(label="Statistik auch löschen",
                                name="statistik_auch",
                                value="1",
                                checked=True,
                                tip="Ankreuzen, um auch die zugehörige Bundes- und Fachstatistik zu löschen",
                                ),
                    ],
                   [h.Dummy(n_col=4)],
                   ],
            button=h.Button(value="Löschen",
                            name='op',
                            tip="Fall mit der angegebenen Nummer endgültig löschen",
                            type='submit',
                            n_col=4,
                            ),
            )
        auswahl_gruppe = h.FieldsetFormInputTable(
            name="rmgruppeanzeigen",
            action="rmaktenf",
            method="post",
            legend='Gruppennummer der zu löschenden Gruppe',
            daten=[[h.TextItem(label='Gruppennummer',
                               name='gn',
                               value='',
                               tip='Gruppennummer der zu löschenden Gruppe'
                               ),
                    h.DummyItem(label_width="50%", class_="textbox280"), # breites Dummy aus optischen Gründen
                    ],
                   [h.Dummy(n_col=4)],
                   ],
            button=h.Button(value="Löschen",
                            name='op',
                            tip="Gruppe mit der angegebenen Nummer endgültig löschen",
                            type='submit',
                            n_col=4,
                            ),
            )
        res = h.Page(
            title='Einzelnen Fall löschen',
            breadcrumbs = (('Aministratorhauptmenü', 'menu'),
                           ),
            rows=(self.get_hauptmenu(),
                  auswahl,
                  auswahl_gruppe,
                  ),
            )
        return res.display()


class rmakten(Request.Request, akte_share):
    """Abfrageformular zum Löschen von Akten."""
    permissions = Request.ADMIN_PERM
    def processForm(self, REQUEST, RESPONSE):
        #print self.form
        alter = self.form.get('alter')
        if alter == None:
            alter = config.LOESCHFRIST
        else:
            alter = check_int_not_empty(
            self.form, 'alter', 'Fehler im Alter in Monaten')
            if alter < config.LOESCHFRIST:
                raise EE('Löschfrist beträgt mindestens %s Monate' % config.LOESCHFRIST)
        aufbew = self.form.get('aufbew')
        if aufbew == None:
            aufbew = cc('aufbew', '1')
        else:
            aufbew = check_code(self.form, 'aufbew', 'aufbew',
                                'Fehler in Aufbewahrungskategorie')
        op = self.form.get('op')
        rm = check_list(self.form, 'rmak', 'Fehler in markierten Akten', '')
        if op == 'Endgültig löschen' and rm:
            hidden = [('rmak', r) for r in rm] + [('op', 'loeschen_confirmed')]
            return h.SubmitOrBack(
                legend='Endgültig löschen',
                action='rmakten2',
                method='post',
                hidden=hidden,
                zeilen=("Sollen die markierten Akten endgültig gelöscht werden?",
                        )
                ).display()
        alter_und_kategorie = h.FieldsetFormInputTable(
            name="rmaktenanzeigen",
            action="rmakten",
            method="post",
            hidden = (),
            legend='Alter und Kategorie der zu löschenden Akten wählen',
            daten=[[h.SelectItem(label='Aufbewahrungskategorie',
                                 name='aufbew',
                                 options=self.for_kat('aufbew',
                                                      sel=aufbew or cc('aufbew', '1')),
                                 ),
                    h.TextItem(label='Monate seit Abschluss des letzten Falls',
                               name='alter',
                               value=alter or '',
                               class_='textboxsmall',
                               maxlength=3,
                               tip='Mindesanzahl der Monate seit Abschluss des letzten Falls'
                               ),
                    ],
                   [h.Dummy(n_col=4)],
                   [h.Button(value="Anzeigen",
                             name='op',
                             tip="Akten der gewählten Kategorie und des gewählten Alters anzeigen",
                             type='submit',
                             n_col=4,
                             ),
                    ],
                   ],
            )
        if alter and aufbew:
            rmdatum = today().add_month(-(alter+1)) # damit immer mindestens die Anzahl Monate
                                                    # dazwischen liegt
            #print 'LOESCHDATUM', rmdatum
            #alle_faelle = FallList(
            #    where = 'zday <= %(year)s and zdam <= %(month)s and zday > 0'
            #    % rmdatum)
            alle_faelle = FallList(
                where = '(zday < %(year)s or (zday = %(year)s and zdam <= %(month)s)) and zday > 0'
                   % rmdatum, 
                order = 'zday, zdam, zdad')
            # Hier gab es einen Fehler (in Reinickendorf):
            # AttributeError: Could not resolve field 'akte__letzter_fall' for instance of 'Fall'
            # Daher wurde nichts zum löschen angezeigt
            # faelle = [f for f in alle_faelle
            #           if f == f['akte__letzter_fall'] and aufbew == f['akte__aufbew']]
            faelle = []
            for f in alle_faelle:
                try:
                    if f == f['akte__letzter_fall'] and aufbew == f['akte__aufbew']:
                        faelle.append(f)
                except Exception, e:
                    t = sys.exc_info()[0]
                    logging.exception("Interner Fehler: %s: %s", t, e)
                    logging.exception("  Falle ohne Akte? fall_id=%s" % f['id'])
            akten = h.FieldsetFormDataTable(
                name="rmakten",
                #action="abfragedef",
                action="rmakten",
                method="post",
                hidden = (),
                legend='Akten zum löschen auswählen (Statistiken bleiben erhalten)',
                headers=('Fallnummer', 'Name', 'Vorname', 'Geburtsdatum', 'Letzter Fallabschluss', '', 'Löschen'),
                daten=[[h.String(string=fall['fn']),
                        h.String(string=fall['akte__na']),
                        h.String(string=fall['akte__vn']),
                        h.String(string=fall['akte__gb']),
                        h.Datum(date=fall.getDate('zda')),
                        h.CheckItem(label='',
                                    name='rmak',
                                    value=fall['akte_id'],
                                    checked=False,
                                    tip='Hier markieren, um die Akte endgültig zu löschen',
                                    ),
                        ] for fall in faelle],
                no_button_if_empty=True,
                button=h.Button(value="Endgültig löschen",
                           name='op',
                           tip="Markierte endgültig Akten löschen",
                           type='submit',
                           class_='buttonbig',
                           n_col=6,
                     ),
                empty_msg="Keine Akten gefunden.",
                )
            
        else:
            akten = None
        res = h.Page(
            title='Akten löschen nach Ablauf der Löschfrist',
            breadcrumbs = (('Aministratorhauptmenü', 'menu'),
                           ),
            rows=(self.get_hauptmenu(),
                  alter_und_kategorie,
                  akten,
                  ),
            )
        return res.display()
        
class rmakten2(Request.Request, akte_share):
    """Löscht die Akten, deren ID im Parameter rmak steht.
    """
    permissions = Request.ADMIN_PERM
    def processForm(self, REQUEST, RESPONSE):
        from ebkus.app.ebapi import check_list
        #print self.form
        op = self.form.get('op')
        rm = check_list(self.form, 'rmak', 'Fehler in markierten Akten', '')
        if op == 'loeschen_confirmed' and rm:
            if rm:
                akten = [Akte(r) for r in rm]
                for a in akten:
                    # vor dem Löschen holen!
                    a['zda'] = a['letzter_fall'].getDate('zda')
                    assert not a['aktueller_fall']
                from ebkus.app.ebupd import removeakten
                anzahl_akten_geloescht, anzahl_gruppen_geloescht = removeakten(self.form)
                assert anzahl_akten_geloescht == len(akten), 'Fehler beim Löschen von Akten'
            else:
                raise EE('Keine Akten zum löschen markiert')
            geloeschte_akten = h.FieldsetDataTable(
                legend='Endgültig gelöschte Akten (Statistik bleibt erhalten)',
                headers=('Name', 'Vorname', 'Geburtsdatum', 'Letzter Fallabschluss'),
                daten=[[h.String(string=akte['na']),
                        h.String(string=akte['vn']),
                        h.String(string=akte['gb']),
                        h.Datum(date=akte['zda']),
                        ] for akte in akten],
                )
            
        else:
            geloeschte_akten = None
        res = h.Page(
            title='Akten gelöscht',
            breadcrumbs = (('Aministratorhauptmenü', 'menu'),
                           ('Akten löschen', None),
                           ),
            rows=(self.get_hauptmenu(),
                  geloeschte_akten,
                  ),
            )
        return res.display()

