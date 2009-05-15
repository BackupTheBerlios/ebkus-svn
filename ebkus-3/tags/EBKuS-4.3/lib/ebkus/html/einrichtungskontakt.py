# coding: latin-1

"""Module für die Einrichtungskontakte."""

from ebkus.app import Request
from ebkus.app.ebapi import Akte, Fall, Einrichtungskontakt, cc
import ebkus.html.htmlgen as h
from ebkus.html.akte_share import akte_share

class _einr(Request.Request, akte_share):
    def _process(self, REQUEST, RESPONSE,
                 title,
                 einrichtung,
                 file,
                 ):
        akte = Akte(einrichtung['akte_id'])
        letzter_fall = akte['letzter_fall']
        einrichtungskontakte_list = akte['einrichtungen']
        einrichtungskontakt = h.FieldsetInputTable(
            #legend='Einrichtungskontakt',
            legend=title,
            daten=[[h.SelectItem(label='Art',
                               name='insta',
                               options=self.for_kat('klinsta', sel=einrichtung['insta']),
                               class_='listbox120',
                               ),
                    h.CheckItem(label='Aktuell',
                                name='status',
                                value=cc('einrstat', 'ja'),
                                checked=(einrichtung['status'] == cc('einrstat', 'ja')),
                                n_col=4,
                              ),
                    ],
                   [h.TextItem(label='Name',
                             name='na',
                             value=einrichtung['na'],
                             maxlength=80,
                             ),
                    h.TextItem(label='Telefon 1',
                             name='tl1',
                             value=einrichtung['tl1'],
                             ),
                    h.TextItem(label='Telefon 2',
                             name='tl2',
                             value=einrichtung['tl2'],
                             ),
                    ],
                   [h.TextItem(label='Notiz',
                             name='no',
                             value=einrichtung['no'],
                             maxlength=250,
                             class_='textbox310',
                             n_col=4,
                             ),
                    h.CheckItem(label='Wichtig',
                              name='nobed',
                              value=cc('notizbed', 't'),
                              checked=(einrichtung['nobed'] == cc('notizbed', 't'))
                              ),
                    ]
                   ]
            )
        einr_daten = []
        for einr in einrichtungskontakte_list:
            einr_daten.append([
                h.String(string=einr['insta__name']),
                h.String(string=einr['na']),
                h.String(string=einr['tl1']),
                h.String(string=einr['tl2']),
                h.String(string=einr['status__code']),
                ])
            einr_daten.append([
                h.String(string="%(nobed__name)s: %(no)s" % einr,
                       n_col=5,
                       class_=cc('notizbed', 't')==einr['nobed'] and 'tabledatared'
                               or 'tabledata')
                ])
        einrichtungskontakte = h.FieldsetDataTable(
            legend='Einrichtungskontakte',
            headers=('Art', 'Name', 'Telefon 1', 'Telefon 2', 'Aktuell'),
            daten=einr_daten,
            )
        res = h.FormPage(
            title=title,
            name="einrichtungskontakt",action="klkarte",method="post",
            breadcrumbs = (('Hauptmenü', 'menu'),
                           ('Klientenkarte', 'klkarte?akid=%(id)s' % akte),
                           ),
            hidden=(("akid", akte['id']),
                    ("einrid", einrichtung['id']),
                    ("file", file),
                    ),
            rows=(self.get_klientendaten_kurz(letzter_fall),
                  einrichtungskontakt,
                  einrichtungskontakte,
                  h.SpeichernZuruecksetzenAbbrechen(),
                  )
            )
        return res.display()


class einrneu(_einr):
    """Neuen Einrichtungskontakt eintragen. (Tabelle: Einrichtungskontakt.)"""
    permissions = Request.UPDATE_PERM
    def processForm(self, REQUEST, RESPONSE):
        if self.form.has_key('fallid'):
            fallid = self.form.get('fallid')
        else:
            self.last_error_message = "Keine ID für den Fall erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
        fall = Fall(fallid)
        einrichtung = Einrichtungskontakt()
        einrichtung.init(
            id = Einrichtungskontakt().getNewId(),
            no='',
            nobed=cc('notizbed', 't'),
            status=cc('einrstat', 'ja'),
            insta=cc('klinsta', '999'),
            akte_id=fall['akte_id'],
            )
        return self._process(REQUEST, RESPONSE,
                             'Neuen Einrichtungskontakt eintragen',
                             einrichtung,
                             'einreinf',
                             )
        
class updeinr(_einr):
    """Einrichtungskontakt ändern. (Tabelle: Einrichtungskontakt.)"""
    permissions = Request.UPDATE_PERM
    def processForm(self, REQUEST, RESPONSE):
        if self.form.has_key('einrid'):
            id = self.form.get('einrid')
        else:
            self.last_error_message = "Keine ID für die Einrichtung erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
        einrichtung = Einrichtungskontakt(id)
        title = 'Einrichtungskontakt ändern'
        file = 'updeinr'
        return self._process(REQUEST, RESPONSE,
                             title,
                             einrichtung,
                             file,
                             )

class rmeinr(Request.Request):
    permissions = Request.UPDATE_PERM
    def processForm(self, REQUEST, RESPONSE):
        if self.form.has_key('einrid'):
            id = self.form.get('einrid')
        else:
            self.last_error_message = "Keine ID für die Einrichtung erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
        einrichtung = Einrichtungskontakt(id)
        return h.SubmitOrBack(
            legend='Einrichtungskontakt löschen',
            action='klkarte',
            method='post',
            hidden=(('file', 'removeeinr'),
                    ('einrid', einrichtung['id']),
                ),
            zeilen=('Soll der Einrichtungskontakt endgültig gelöscht werden?',
                    ),
            ).display()
