# coding: latin-1

"""Modul Beratungskontakte."""

from ebkus.app import Request
from ebkus.app.ebapi import Fall, Beratungskontakt, today
from ebkus.config import config

import ebkus.html.htmlgen as h
from ebkus.html.akte_share import akte_share

class _bkont(Request.Request, akte_share):
    # bkontneu und updbkont mit derselben Routine,
    # nur anders parametrisiert
    def _process(self, REQUEST, RESPONSE,
                 title,
                 legendtext,
                 fall,
                 bkont,
                 file,
                 ):
        beratungskontakte = fall['beratungskontakte']
        beratungskontakte.sort('ky', 'km', 'kd')
        beratungs_kontakt_bearbeiten = h.FieldsetInputTable(
            legend = '%s %s %s' % (legendtext, fall['akte__vn'], fall['akte__na']),
            daten = [[h.SelectItem(label='Mitarbeiter',
                                 name='mitid',
                                 options=self.for_mitarbeiter(sel=bkont['mit_id'])),
                      h.SelectItem(label='Art des Kontaktes',
                                 name='art',
                                 options=self.for_kat('fska', sel=bkont['art'])),
                      ],
                     [h.DatumItem(label='Datum',
                                name='k',
                                date =  bkont.getDate('k')),
                      h.SelectItem(label='Dauer',
                                 name='dauer',
                                 options=self.for_kat('fskd', sel=bkont['dauer'])),
                      ],
                     [h.TextItem(label='Notiz',
                               name='no',
                               value=bkont['no'],
                               class_='textboxverylarge',
                               maxlength=1024,
                               n_col=4,)
                      ],
                     ],
            )
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
        res = h.FormPage(
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
                  h.SpeichernZuruecksetzenAbbrechen(),
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
            stz=self.stelle['id'],
            mit_id=self.mitarbeiter['id'],
            art=None,
            dauer=None,
            )
        bkont.setDate('k', today())
        return self._process(REQUEST, RESPONSE,
                             title="Neuen Beratungskontakt eintragen",
                             legendtext="Neuen Beratungskontakt eintragen für",
                             fall=fall,
                             bkont=bkont,
                             file='bkonteinf',
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
        bkont = Beratungskontakt(id)
        fall = Fall(bkont['fall_id'])
        return self._process(REQUEST, RESPONSE,
                             title="Beratungskontakt bearbeiten",
                             legendtext="Beratungskontakt bearbeiten von",
                             fall=fall,
                             bkont=bkont,
                             file='updbkont',
                             )
