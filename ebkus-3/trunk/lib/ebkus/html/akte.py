# coding: latin-1

"""Module f�r Akte und Fall."""

import string,time

from ebkus.db.sql import SQL
from ebkus.app import Request
from ebkus.config import config
from ebkus.app.ebapi import Akte, Fall, FallList, Altdaten, \
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
                             tip="Freies Feld f�r Notizen",
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
                                     tip='Fallbearbeiter ausw�hlen',
                                     options=self.for_mitarbeiter(sel=self.mitarbeiter['id'])),
                        h.DatumItem(label='Fallbeginn',
                                    name='zubg',
                                    tip='Monat des Fallbeginns',
                                    year=today().year,
                                    month=today().month),
                        ]],
                )
            leistung = h.FieldsetInputTable(
                legend='Leistung',
                daten=[[h.SelectItem(label='Mitarbeiter',
                                     name='lemitid',
                                     tip='Mitarbeiter ausw�hlen, der die Leistung erbracht hat',
                                     options=self.for_mitarbeiter(sel=self.mitarbeiter['id'])),
                        h.SelectItem(label='Leistung',
                                     name='le',
                                     tip='Art der erbrachten Leistung',
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
                                tip="Suche in den Altdaten aus fr�heren EDV-Systemen",
                                ),
                )
        res = h.FormPage(
            title=title,
            name=formname,action="klkarte",method="post",
            breadcrumbs = (('Hauptmen�', 'menu'),
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
                  falldaten,
                  leistung,
                  h.SpeichernZuruecksetzenAbbrechen(),
                  ),
            )
        return res.display()

class akteneu(_akte):
    """Neue Fallakte anlegen (Tabellen: Akte, Fall, Zust�ndigkeit, Leistung)."""
    permissions = Request.UPDATE_PERM
    def processForm(self, REQUEST, RESPONSE):
        alt_ids = check_list(self.form, 'uebern', 'Fehler in Altdaten', [])
        if len(alt_ids) > 1:
            raise EE("Bitte nur einen Eintrag zur �bernahme markieren!")
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
            no = "Alte Fallnummer: %(fallnummer)s, Jahr: %(jahr)s, Fr�herer Mitarbeiter: %(mitarbeiter)s" % alt
        else:
            no = ''
        str = alt.get('strasse', '')
        if str:
            for end in ('trasse', 'tra�e'):
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
        return self._process(
            title='Neue Akte anlegen',
            file='akteeinf',
            akte=akte,
            formname='akteform',
            hidden=(('stzbg', akte['stzbg']),
                    )
            )

class waufnneu(_akte):
    """Wiederaufnahme einer vorhandener  Fallakte
    (Tabellen: Akte, Fall, Zust�ndigkeit, Leistung)."""
    permissions = Request.UPDATE_PERM
    def processForm(self, REQUEST, RESPONSE):
        akid = self.form.get('akid')
        if not akid:
            raise EE("Keine ID fuer die Akte erhalten")
        akte = Akte(akid)
        return self._process(
                 title="Wiederaufnahme des Klienten",
                 file='waufneinf',
                 akte=akte,
                 formname='akteform',
                 hidden=(('fallid', Fall().getNewId()),
                         ('status', cc('stand', 'l')),
                         ),
                 )
        
class updakte(_akte):
    """Akte �ndern (Tabelle Akte)."""
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
            title='Beginndatum �ndern',
            name='akteform',action="klkarte",method="post",
            breadcrumbs = (('Hauptmen�', 'menu'),
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
    """Fallakte abschliessen (Tabellen: Fall und Zust�ndigkeit)."""
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
            breadcrumbs = (('Hauptmen�', 'menu'),
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
            legend='Bisherige Zust�ndigkeit wird ausgetragen'),
                  self.get_zustaendigkeiten(zustaendigkeiten_list),
                  h.SpeichernZuruecksetzenAbbrechen(),
                  ),
            )
        return res.display()
        
class zdar(_akte):
    """Fallabschluss r�ckg�ngig machen und letzte Zustaendigkeit wiederherstellen
    (Tabellen: Fall und Zust�ndigkeit)."""
    permissions = Request.UPDATE_PERM
    def processForm(self, REQUEST, RESPONSE):
        fallid = self.form.get('fallid')
        if not fallid:
            raise EE("Keine ID fuer den Fall erhalten")
        fall = Fall(fallid)
        zuletzt_zustaendig = fall['zuletzt_zustaendig']
        res = h.FormPage(
            title='Abschlussdatum r�ckg�ngig machen',
            name='zdarform',action="klkarte",method="post",
            breadcrumbs = (('Hauptmen�', 'menu'),
                           ('Klientenkarte', 'klkarte?akid=%(akte_id)s' % fall),
                           ),
            hidden=(("fallid", fallid),
                    ("file", 'zdareinf'),
                    ),
            rows=(self.get_bisherige_zustaendigkeit(
            zuletzt_zustaendig,
            legend='Letzte Zust�ndigkeit wird wiederhergestellt',
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
                legend='Bisherige Zust�ndigkeit wird ausgetragen',
                )
        elif file == 'updzust':
            bisherige_zustaendigkeit = None
        res = h.FormPage(
            title=title,
            name='zustform',action="klkarte",method="post",
            breadcrumbs = (('Hauptmen�', 'menu'),
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
    """Neue Zust�ndigkeit eintragen. (Tabelle: Zust�ndigkeit.)"""
    permissions = Request.UPDATE_PERM
    def processForm(self, REQUEST, RESPONSE):
        if self.form.has_key('fallid'):
            fallid = self.form.get('fallid')
        else:
            self.last_error_message = "Keine ID f�r den Fall erhalten"
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
            legend="Neue Zust�ndigkeit eintragen",
            daten=[[h.SelectItem(label='Bearbeiter',
                                 name='mitid',
                                 tip='Fallbearbeiter ausw�hlen',
                                 options=self.for_mitarbeiter(neue_zust['mit_id'])),
                    h.DatumItem(label='Beginn',
                                name='bg',
                                tip='Datum des Zust�ndigkeitbeginns',
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
    """Neue Zust�ndigkeit eintragen. (Tabelle: Zust�ndigkeit.)"""
    permissions = Request.UPDATE_PERM
    def processForm(self, REQUEST, RESPONSE):
        if self.form.has_key('zustid'):
            id  = self.form.get('zustid')
        else:
            self.last_error_message = "Keine ID f�r die Zust�ndigkeit erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
        zust = Zustaendigkeit(id)
        fall = Fall(zust['fall_id'])
        zustaendigkeit = h.FieldsetInputTable(
            legend="Zust�ndigkeit bearbeiten",
            daten=[[h.SelectItem(label='Bearbeiter',
                                 name='mitid',
                                 tip='Fallbearbeiter ausw�hlen',
                                 options=self.for_mitarbeiter(zust['mit_id'])),
                    h.DatumItem(label='Beginn',
                                name='bg',
                                tip='Datum des Zust�ndigkeitbeginns',
                                date=zust.getDate('bg')),
                    h.DatumItem(label='Ende',
                                name='e',
                                tip='Datum des Zust�ndigkeitendes',
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
    """Abfrageformular zum L�schen von Akten."""
    permissions = Request.ADMIN_PERM
    def processForm(self, REQUEST, RESPONSE):
        return "Noch nicht implementiert"


class rmakten(Request.Request, akte_share):
    """Abfrageformular zum L�schen von Akten."""
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
                raise EE('L�schfrist betr�gt mindestens %s Monate' % config.LOESCHFRIST)
        aufbew = self.form.get('aufbew')
        if aufbew == None:
            aufbew = cc('aufbew', '1')
        else:
            aufbew = check_code(self.form, 'aufbew', 'aufbew',
                                'Fehler in Aufbewahrungskategorie')
        op = self.form.get('op')
        rm = check_list(self.form, 'rmak', 'Fehler in markierten Akten', '')
        if op == 'Endg�ltig l�schen' and rm:
            hidden = [('rmak', r) for r in rm] + [('op', 'loeschen_confirmed')]
            return h.SubmitOrBack(
                legend='Endg�ltig l�schen',
                action='rmakten2',
                method='post',
                hidden=hidden,
                zeilen=("Sollen die markierten Akten endg�ltig gel�scht werden?",
                        )
                ).display()
        alter_und_kategorie = h.FieldsetFormInputTable(
            name="rmaktenanzeigen",
            action="rmakten",
            method="post",
            hidden = (),
            legend='Alter und Kategorie der zu l�schenden Akten w�hlen',
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
                             tip="Akten der gew�hlten Kategorie und des gew�hlten Alters anzeigen",
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
            alle_faelle = FallList(
                where = 'zday <= %(year)s and zdam <= %(month)s and zday > 0'
                % rmdatum)
            faelle = [f for f in alle_faelle
                      if f == f['akte__letzter_fall'] and aufbew == f['akte__aufbew']]
            akten = h.FieldsetFormDataTable(
                name="rmakten",
                #action="abfragedef",
                action="rmakten",
                method="post",
                hidden = (),
                legend='Akten zum l�schen ausw�hlen (Statistiken bleiben erhalten)',
                headers=('Name', 'Vorname', 'Geburtsdatum', 'Letzter Fallabschluss', '', 'L�schen'),
                daten=[[h.String(string=fall['akte__na']),
                        h.String(string=fall['akte__vn']),
                        h.String(string=fall['akte__gb']),
                        h.Datum(date=fall.getDate('zda')),
                        h.CheckItem(label='',
                                    name='rmak',
                                    value=fall['akte_id'],
                                    checked=False,
                                    tip='Hier markieren, um die Akte endg�ltig zu l�schen',
                                    ),
                        ] for fall in faelle],
                no_button_if_empty=True,
                button=h.Button(value="Endg�ltig l�schen",
                           name='op',
                           tip="Markierte endg�ltig Akten l�schen",
                           type='submit',
                           class_='buttonbig',
                           n_col=6,
                     ),
                empty_msg="Keine Akten gefunden.",
                )
            
        else:
            akten = None
    
##         buttons = h.FieldsetInputTable(
##             daten=[[
##             h.Button(value="Endg�ltig l�schen",
##                      name='op',
##                      tip="Markierte Akten l�schen",
##                      type='button',
##                      onClick="confirm_submit('Markierte Akten endg�ltig l�schen?', 'rmakten')",
##                      class_='buttonbig',
##                      ),
##             h.Button(value="Abbrechen",
##                      name='op',
##                      tip="Zur�ck zum Hauptmen� ohne zu l�schen",
##                      type='button',
##                      onClick="go_to_url('menu')",
##                      ),
##             ]])
        res = h.Page(
            title='Akten l�schen',
            breadcrumbs = (('Aministratorhauptmen�', 'menu'),
                           ),
            rows=(self.get_hauptmenu(),
                  alter_und_kategorie,
                  akten,
                  ),
            )
        return res.display()
        
class rmakten2(Request.Request, akte_share):
    """L�scht die Akten, deren ID im Parameter rmak steht.
    """
    permissions = Request.ADMIN_PERM
    def processForm(self, REQUEST, RESPONSE):
        from ebkus.app.ebapi import check_list
        print self.form
        op = self.form.get('op')
        rm = check_list(self.form, 'rmak', 'Fehler in markierten Akten', '')
        if op == 'loeschen_confirmed' and rm:
            if rm:
                akten = [Akte(r) for r in rm]
                for a in akten:
                    # vor dem L�schen holen!
                    a['zda'] = a['letzter_fall'].getDate('zda')
                    assert not a['aktueller_fall']
                from ebkus.app.ebupd import removeakten
                anzahl_akten_geloescht, anzahl_gruppen_geloescht = removeakten(self.form)
                assert anzahl_akten_geloescht == len(akten), 'Fehler beim L�schen von Akten'
            else:
                raise EE('Keine Akten zum l�schen markiert')
            geloeschte_akten = h.FieldsetDataTable(
                legend='Endg�ltig gel�schte Akten (Statistik bleibt erhalten)',
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
            title='Akten gel�scht',
            breadcrumbs = (('Aministratorhauptmen�', 'menu'),
                           ('Akten l�schen', None),
                           ),
            rows=(self.get_hauptmenu(),
                  geloeschte_akten,
                  ),
            )
        return res.display()
##     def processForm(self, REQUEST, RESPONSE):
##         mitarbeiterliste = self.getMitarbeiterliste()
##         user = self.user
##         if self.form.has_key('frist'):
##             frist = self.form.get('frist')
##         else:
##             self.last_error_message = "Keine Frist erhalten"
##             return self.EBKuSError(REQUEST, RESPONSE)
            
##         jahr = today().year
##         monat = today().month
##         heute = int(jahr)*12 + int(monat)
##         loeschzeitm = int(heute)-int(frist)
##         loeschjahr = int(loeschzeitm) / int(12)
##         loeschmonat = int(loeschzeitm) - (int(loeschjahr) * int(12))
        
##         hidden ={'file': 'removeakten'}
        
##         res = []
##         res.append(head_normal_ohne_help_t %("Akten und Gruppen l�schen"))
##         res.append(rmakten2a_t)
##         res.append(formhiddenvalues_t % hidden)
##         res.append(formhiddennamevalues_t % ({'value': frist, 'name': 'frist'}))
##         res.append(formhiddennamevalues_t % ({'value': loeschjahr,
##                                               'name': 'loeschjahr'}))
##         res.append(formhiddennamevalues_t % ({'value': loeschmonat,
##                                               'name': 'loeschmonat'}))
##         res.append(rmakten2b_t % (frist, loeschmonat, loeschjahr ))
##         return string.join(res, '')
