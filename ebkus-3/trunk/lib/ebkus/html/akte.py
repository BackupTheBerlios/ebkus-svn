# coding: latin-1

"""Module für Akte und Fall."""

import string,time

from ebkus.app import Request
from ebkus.config import config
from ebkus.app.ebapi import StrassenkatalogList, Akte, Fall, Zustaendigkeit, today, cc
#from ebkus.app.ebapih import get_codes, mksel,mksel_str,mksel_str_upd
#from ebkus.app_surface.akte_templates import *
#from ebkus.app_surface.standard_templates import *

#from ebkus.app.ebapih import get_codes, make_option_list


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
        anschrift = self.get_anschrift(akte)
        falldaten = leistung = None
        if file in ('akteeinf', 'waufneinf'):
            falldaten = h.FieldsetInputTable(
                legend='Falldaten',
                daten=[[h.SelectItem(label='Bearbeiter',
                                     name='zumitid',
                                     tip='Fallbearbeiter auswählen',
                                     options=self.options.for_mitarbeiter(sel=self.user)),
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
                                     tip='Mitarbeiter auswählen, der die Leistung erbracht hat',
                                     options=self.options.for_mitarbeiter(sel=self.user)),
                        h.SelectItem(label='Leistung',
                                     name='le',
                                     tip='Art der erbrachten Leistung',
                                     options=self.options.for_kat('fsle', akte['fs'])),
                        ],[h.DummyItem(),
                           h.DatumItem(label='Am',
                                       name='lebg',
                                       tip='Datum der Leistung oder des Beginns der Leistung',
                                       date=today()),
                           ]],
                )
        res = h.FormPage(
            title=title,
            name=formname,action="klkarte",method="post",
            hidden=(("akid", akte['id']),
                    ("file", file),
                    ) + hidden,
            rows=(h.Pair(left=klientendaten,
                         right=anschrift,
                         ),
                  notiz,
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
        akte = Akte()
        akte.init(
            id=Akte().getNewId(),
            fs=cc('fsfs', '999'),
            stzbg=self.stelle['id'],
            lage=cc('lage', '999'),
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
    (Tabellen: Akte, Fall, Zuständigkeit, Leistung)."""
    permissions = Request.UPDATE_PERM
    def processForm(self, REQUEST, RESPONSE):
        if self.form.get('akid'):
            akid = self.form.get('akid')
        else:
            self.last_error_message = "Keine ID fuer die Akte erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
        akte = Akte(akid)
        return self._process(
                 title="Wiederaufnahme des Klienten",
                 file='waufneinf',
                 akte=akte,
                 formname='akteform',
                 hidden=(('fallid', Fall().getNewId()),
                         ('status', cc('stand', 'l')),
                         ('stzbg', self.stelle['id']),
                         ),
                 )
        
class updakte(_akte):
    """Akte ändern (Tabelle Akte)."""
    permissions = Request.UPDATE_PERM
    def processForm(self, REQUEST, RESPONSE):
        if self.form.has_key('akid'):
            akid = self.form.get('akid')
            akte = Akte(int(akid))
        else:
            self.last_error_message = "Keine ID fuer die Akte erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
        return self._process(
            title='Akte aktualisieren',
            file='updakte',
            akte=akte,
            formname='akteform',
            hidden=(('stzbg', akte['stzbg']),
                    ('stzak', akte['stzak']))
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
            hidden=(("fallid", fallid),
                    ("file", 'zdaeinf'),
                    ("aktuellzustid", aktuell_zustaendig['id']),
                    ("aktuellmitid", aktuell_zustaendig['mit_id__id']),
                    ),
            rows=(falldaten,
                  self.get_bisherige_zustaendigkeit(aktuell_zustaendig),
                  self.get_zustaendigkeiten(zustaendigkeiten_list),
                  h.SpeichernZuruecksetzenAbbrechen(),
                  ),
            )
        return res.display()
        
class zdar(_akte):
    """Fallabschluss rückgängig machen und neue Zustaendigkeit eintragen
    (Tabellen: Fall und Zuständigkeit)."""
    permissions = Request.UPDATE_PERM
    def processForm(self, REQUEST, RESPONSE):
        if self.form.has_key('fallid'):
            fallid = self.form.get('fallid')
        else:
            self.last_error_message = "Keine ID fuer den Fall erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
        fall = Fall(int(fallid))
        zustid = Zustaendigkeit().getNewId()
        beginndatum = h.FieldsetInputTable(
            daten=[[h.SelectItem(label='Mitarbeiter',
                                 name='zumitid',
                                 tip='Fallbearbeiter auswählen',
                                 options=self.options.for_mitarbeiter(sel=self.user)),
                    h.DatumItem(label='Beginn',
                                name='bg',
                                tip='Datum des Fallbeginns',
                                date=today()),
                    ]],
            )
        res = h.FormPage(
            title='Abschlussdatum rückgängig machen',
            name='zdarform',action="klkarte",method="post",
            hidden=(("fallid", fallid),
                    ("file", 'zdareinf'),
                    ("zustid", Zustaendigkeit().getNewId()),
                    ),
            rows=(beginndatum,
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
            bisherige_zustaendigkeit = self.get_bisherige_zustaendigkeit(aktuell_zustaendig)
        elif file == 'updzust':
            bisherige_zustaendigkeit = None
        res = h.FormPage(
            title=title,
            name='zustform',action="klkarte",method="post",
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
            mit_id=self.user,
            fall_id=fall['id'],
            )
        neue_zust.setDate('bg', today())
        zustaendigkeit = h.FieldsetInputTable(
            legend="Neue Zuständigkeit eintragen",
            daten=[[h.SelectItem(label='Bearbeiter',
                                 name='mitid',
                                 tip='Fallbearbeiter auswählen',
                                 options=self.options.for_mitarbeiter(neue_zust['mit_id'])),
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
                    ('file', 'zusteinf')),
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
                                 options=self.options.for_mitarbeiter(zust['mit_id'])),
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

class rmakten(Request.Request):
    """Abfrageformular zum Löschen von Akten."""
    
    permissions = Request.ADMIN_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        mitarbeiterliste = self.getMitarbeiterliste()
        user = self.user
        
        # Liste der Templates als String
        
        res = []
        res.append(head_normal_ohne_help_t %('Einstellungen f&uuml;r den L&ouml;schvorgang'))
        res.append(rmakten_t % int(config.LOESCHFRIST))
        return string.join(res, '')
        
        
class rmakten2(Request.Request):
    """Löscht die Akten, welche älter als die Löschfrist sind.
    Die Statistiktabellen bleiben erhalten. Die fall_id wird auf NULL gesetzt.
    """
    
    permissions = Request.ADMIN_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        mitarbeiterliste = self.getMitarbeiterliste()
        user = self.user
        if self.form.has_key('frist'):
            frist = self.form.get('frist')
        else:
            self.last_error_message = "Keine Frist erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
            
        jahr = today().year
        monat = today().month
        heute = int(jahr)*12 + int(monat)
        loeschzeitm = int(heute)-int(frist)
        loeschjahr = int(loeschzeitm) / int(12)
        loeschmonat = int(loeschzeitm) - (int(loeschjahr) * int(12))
        
        hidden ={'file': 'removeakten'}
        
        res = []
        res.append(head_normal_ohne_help_t %("Akten und Gruppen löschen"))
        res.append(rmakten2a_t)
        res.append(formhiddenvalues_t % hidden)
        res.append(formhiddennamevalues_t % ({'value': frist, 'name': 'frist'}))
        res.append(formhiddennamevalues_t % ({'value': loeschjahr,
                                              'name': 'loeschjahr'}))
        res.append(formhiddennamevalues_t % ({'value': loeschmonat,
                                              'name': 'loeschmonat'}))
        res.append(rmakten2b_t % (frist, loeschmonat, loeschjahr ))
        return string.join(res, '')
