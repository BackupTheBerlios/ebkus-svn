# coding: latin-1

"""Module für die Leistung."""

from ebkus.app import Request
from ebkus.app.ebapi import cc, Fall, Leistung, today, EE
from ebkus.config import config

import ebkus.html.htmlgen as h
from ebkus.html.akte_share import akte_share

class _leist(Request.Request, akte_share):
    def _process(self, REQUEST, RESPONSE,
                 title,
                 legend,
                 leistung,
                 file,
                 ):
        fall = leistung['fall']
        leistungen_list = fall['leistungen']
        leistungen_list.sort('bgy', 'bgm', 'bgd')
        mitarbeiter_leistung = h.FieldsetInputTable(
            legend = '%s %s %s' % (legend, fall['akte__vn'], fall['akte__na']),
            daten = [[h.SelectItem(label='Mitarbeiter',
                                   name='mitid',
                                   options=self.for_mitarbeiter(leistung['mit_id'])),
                      h.SelectItem(label='Leistung',
                                   name='le',
                                   class_='listbox220',
                                   options=self.for_kat('fsle', leistung['le'])),
            ]]
            )
        leistungszeitraum = h.FieldsetInputTable(
            legend = 'Leistungszeitraum',
            daten = [[h.DatumItem(label='Am',
                                  name='bg',
                                  date = leistung.getDate('bg'),
                                  ),
                      h.DatumItem(label='Bis',
                                  name='e',
                                  date = leistung.getDate('e'),
                                  ),
                      ]]
            )
        leistungen = h.FieldsetDataTable(
            legend= 'Leistungen',
            headers= ('Mitarbeiter', 'Leistung', 'Am', 'Bis'),
            daten= [[h.String(string= leist['mit_id__na']),
                     h.String(string= leist['le__name']),
                     h.Datum(date=leist.getDate('bg')),
                     h.Datum(date=leist.getDate('e')),
                     ]
                    for leist in leistungen_list],
            )
        res = h.FormPage(
            title=title,
            name="leistung",action="klkarte",method="post",
            breadcrumbs = (('Hauptmenü', 'menu'),
                           ('Klientenkarte', 'klkarte?akid=%(akte_id)s' % fall),
                           ),
            hidden=(("fallid", fall['id']),
                    ("stz", leistung['stz']),
                    ("leistid", leistung['id']),
                    ("file", file),
                    ),
            rows=(mitarbeiter_leistung,
                  leistungszeitraum,
                  leistungen,
                  h.SpeichernZuruecksetzenAbbrechen(),
                  )
            )
        return res.display()
    
class leistneu(_leist):
    """Neue Leistung eintragen. (Tabelle: Leistung.)"""
    permissions = Request.UPDATE_PERM
    def processForm(self, REQUEST, RESPONSE):
        if self.form.has_key('fallid'):
            fallid = self.form.get('fallid')
        else:
            self.last_error_message = "Keine ID für den Fall erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
        fall = Fall(int(fallid))
        benr = self.mitarbeiter['benr__code']
        if benr in ('verw',):
            # Verwaltungskraft kann Einträge für andere Mitarbeiter machen
            mit_id = fall['zustaendig__mit_id']
        else:
            mit_id = self.mitarbeiter['id']
        leistung = Leistung()
        leistung.init(
            id=Leistung().getNewId(),
            ey='',
            em='',
            ed='',
            stz=self.stelle['id'],
            fall_id=fall['id'],
            mit_id=mit_id,
            le=cc('fsle', '1'),
            )
        leistung.setDate('bg', today())
        return self._process(REQUEST, RESPONSE,
                             title="Neue Leistung eintragen",
                             legend="Neue Leistung eintragen für",
                             leistung=leistung,
                             file='leisteinf',
                             )
        
class updleist(_leist):
    """Leistung ändern. (Tabelle: Leistung.)"""
    permissions = Request.UPDATE_PERM
    def processForm(self, REQUEST, RESPONSE):
        if self.form.has_key('leistid'):
            id = self.form.get('leistid')
        else:
            self.last_error_message = "Keine ID für die Leistung erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
        leistung = Leistung(id)
        fall = Fall(leistung['fall_id'])
        return self._process(REQUEST, RESPONSE,
                             title="Leistung bearbeiten",
                             legend="Leistung bearbeiten von",
                             leistung=leistung,
                             file='updleist',
                             )

class rmleist(Request.Request):
    """Beratungskontakt löschen."""
    permissions = Request.UPDATE_PERM
    def processForm(self, REQUEST, RESPONSE):
        if self.form.has_key('leistid'):
            id = self.form.get('leistid')
        else:
            self.last_error_message = "Keine ID für die Leistung erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
        leistung = Leistung(id)
        if len(leistung['fall']['leistungen']) < 2:
            raise EE('Es muss immer mindestens eine Leistung geben')
        if leistung['beratungskontakte']:
            raise EE('Leistung in einem Beratungskontakt kann nicht gelöscht werden')
        return h.SubmitOrBack(
            legend='Leistung löschen',
            action='klkarte',
            method='post',
            hidden=(('file', 'removeleist'),
                    ('leistid', leistung['id']),
                    ),
            zeilen=('Soll die Leistung vom %s endgültig gelöscht werden?' % leistung.getDate('bg'),
                    ),
            ).display()

