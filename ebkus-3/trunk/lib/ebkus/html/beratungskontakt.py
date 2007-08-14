# coding: latin-1

"""Modul Beratungskontakte."""

from ebkus.app import Request
from ebkus.app.ebapi import Fall, Beratungskontakt, today
from ebkus.app.ebapih import get_codes, make_option_list
from ebkus.config import config


from ebkus.html.htmlgen import Base, Form, FormPage, Fieldset, FieldsetDataTable, \
     FieldsetInputTable, Tr, Pair, \
     Button, Datum, String, Icon, IconDead, SelectGoto, Klientendaten, \
     SelectItem, DatumItem, TextItem, \
     SpeichernZuruecksetzenAbbrechen

class _bkont(Request.Request):
    # bkontneu und updbkont mit derselben Routine,
    # nur anders parametrisiert
    def _process(self, REQUEST, RESPONSE,
                 title,
                 legendtext,
                 fall,
                 bkont,
                 file,
                 mitarbeiter_selected,
                 beratungskontakt_selected,
                 beratungskontaktdauer_selected,
                 ):
        beratungskontakte = fall['beratungskontakte']
        beratungskontakte.sort('ky', 'km', 'kd')
        mitarbeiter_options = make_option_list(self.getMitarbeiterliste(),
                                               'id', 'na',
                                               selected=mitarbeiter_selected),
        beratungskontaktdauer_options =  make_option_list(get_codes('fskd'),
                                                          'id', 'name',
                                                          selected=beratungskontaktdauer_selected),
        beratungskontaktart_options =  make_option_list(get_codes('fska'),
                                                        'id', 'name',
                                                        selected=beratungskontakt_selected),
        beratungs_kontakt_bearbeiten = FieldsetInputTable(
            legend = '%s %s %s' % (legendtext, fall['akte__vn'], fall['akte__na']),
            daten = [[SelectItem(label='Mitarbeiter',
                                 name='mitid',
                                 options=mitarbeiter_options),
                      SelectItem(label='Art des Kontaktes',
                                 name='art',
                                 options=beratungskontaktart_options),
                      ],
                     [DatumItem(label='Datum',
                                name='k',
                                date =  bkont.getDate('k')),
                      SelectItem(label='Dauer',
                                 name='dauer',
                                 options=beratungskontaktdauer_options),
                      ],
                     [TextItem(label='Notiz',
                               name='no',
                               value=bkont['no'],
                               class_='textboxverylarge',
                               maxlength=1024,
                               n_col=4,)
                      ],
                     ],
            )
        bisherige_kontakte = FieldsetDataTable(
            legend = 'Liste der bisherigen Kontakte',
            empty_msg = "Bisher keine Kontakte eingetragen.",
            headers = ('Mitarbeiter', 'Art', 'Datum', 'Dauer', 'Notiz'),
            daten =  [[String(string = b['mit_id__na']),
                       String(string = b['art__name']),
                       Datum(date =  b.getDate('k')),
                       String(string = b['dauer__name']),
                       String(string = b['no']),]
                      for b in beratungskontakte],
            )

    
        res = FormPage(
            title=title,
            name="beratungskontakt",action="klkarte",method="post",
            hidden=(("akid", fall['akte_id']),
                    ("stz", bkont['stz']),
                    ("bkontid", bkont['id']),
                    ("fallid", fall['id']),
                    ("file", file),
                    ),
            rows=(beratungs_kontakt_bearbeiten,
                  bisherige_kontakte,
                  SpeichernZuruecksetzenAbbrechen(),
                  )
            )
        return res.display()
    
class bkontneu(_bkont):
    """Neue Beratungskontakt eintragen. (Tabelle: Beratungskontakt.)"""
    
    permissions = Request.UPDATE_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        if self.form.has_key('fallid'):
            fallid = self.form.get('fallid')
        else:
            self.last_error_message = "Keine ID für den Fall erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
        fall = Fall(fallid)
        bkont = Beratungskontakt()
        bkont.init(
            id=Beratungskontakt().getNewId(),
            ky=today().year,
            km=today().month,
            kd=today().day,
            stz=self.stelle['id'],
            )
        return self._process(REQUEST, RESPONSE,
                             "Neuen Beratungskontakt eintragen",
                             "Neuen Beratungskontakt eintragen für",
                             fall,
                             bkont,
                             'bkonteinf',
                             self.mitarbeiter['id'],
                             None,
                             None,
                             )
        
class updbkont(_bkont):
    """Beratungskontakt ändern. (Tabelle: Beratungskontakt.)"""
    
    permissions = Request.UPDATE_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        if self.form.has_key('bkontid'):
            id = self.form.get('bkontid')
        else:
            self.last_error_message = "Keine ID für den Beratungskontakt erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
        beratungskontakt = Beratungskontakt(int(id))
        fall = Fall(beratungskontakt['fall_id'])
        return self._process(REQUEST, RESPONSE,
                             "Beratungskontakt bearbeiten",
                             "Beratungskontakt bearbeiten von",
                             fall,
                             beratungskontakt,
                             'updbkont',
                             beratungskontakt['mit_id'],
                             beratungskontakt['art'],
                             beratungskontakt['dauer'],
                             )

