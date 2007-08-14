# coding: latin-1

"""Module für die Leistung."""

from ebkus.app import Request
from ebkus.app.ebapi import Fall, Leistung, today
from ebkus.app.ebapih import get_codes, make_option_list
from ebkus.config import config

from ebkus.html.htmlgen import Base, Form, FormPage, Fieldset, FieldsetDataTable, \
     FieldsetInputTable, Tr, Pair, \
     Button, Datum, String, Icon, IconDead, SelectGoto, Klientendaten, \
     SelectItem, DatumItem, TextItem, \
     SpeichernZuruecksetzenAbbrechen


class _leist(Request.Request):
    # leistneu und updleist mit derselben Routine,
    # nur anders parametrisiert
    def _process(self, REQUEST, RESPONSE,
                 title,
                 legend,
                 fall,
                 leistung,
                 file,
                 mitarbeiter_selected,
                 leistung_selected,
                 ):
        leistungen_list = fall['leistungen']
        leistungen_list.sort('bgy', 'bgm', 'bgd')
        leistungsarten = get_codes('fsle')
        # hier kommt alles rein, was das template braucht
        mitarbeiter_options = make_option_list(self.getMitarbeiterliste(),
                                               'id', 'na',
                                               selected=mitarbeiter_selected),
        leistungsart_options = make_option_list(leistungsarten,
                                                'id', 'name',
                                                selected=leistung_selected),

        mitarbeiter_leistung = FieldsetInputTable(
            legend = '%s %s %s' % (legend, fall['akte__vn'], fall['akte__na']),
            daten = [[SelectItem(label='Mitarbeiter',
                                 name='mitid',
                                 options=mitarbeiter_options),
                      SelectItem(label='Leistung',
                                 name='le',
                                 options=leistungsart_options),
            ]]
            )
        leistungszeitraum = FieldsetInputTable(
            legend = 'Leistungszeitraum',
            daten = [[DatumItem(label='Am',
                                name='bg',
                                date = leistung.getDate('bg'),
                                ),
                      DatumItem(label='Bis',
                                name='e',
                                date = leistung.getDate('e'),
                                ),
            ]]
            )
        leistungen = FieldsetDataTable(
            legend= 'Leistungen',
            headers= ('Mitarbeiter', 'Leistung', 'Am', 'Bis'),
            daten= [[String(string= leist['mit_id__na']),
                     String(string= leist['le__name']),
                     Datum(date=leist.getDate('bg')),
                     Datum(date=leist.getDate('e')),
                     ]
                    for leist in leistungen_list],
            )
        res = FormPage(
            title=title,
            name="leistung",action="klkarte",method="post",
            hidden=(("akid", fall['akte_id']),
                    ("fallid", fall['id']),
                    ("stz", leistung['stz']),
                    ("leistid", leistung['id']),
                    ("file", file),
                    ),
            rows=(mitarbeiter_leistung,
                  leistungszeitraum,
                  leistungen,
                  SpeichernZuruecksetzenAbbrechen(),
                  )
            )
        return res.display()
        return self.render('leistung.html', context_dict)
    
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
        leistung = Leistung()
        leistung.init(
            id=Leistung().getNewId(),
            bgy=today().year,
            bgm=today().month,
            bgd=today().day,
            ey='',
            em='',
            ed='',
            stz=self.stelle['id'],
            )
        return self._process(REQUEST, RESPONSE,
                             "Neue Leistung eintragen",
                             "Neue Leistung eintragen für",
                             fall,
                             leistung,
                             'leisteinf',
                             self.mitarbeiter['id'],
                             None,
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
        leistung = Leistung(int(id))
        fall = Fall(leistung['fall_id'])
        return self._process(REQUEST, RESPONSE,
                             "Leistung bearbeiten",
                             "Leistung bearbeiten von",
                             fall,
                             leistung,
                             'updleist',
                             leistung['mit_id'],
                             leistung['le']
                             )

