# coding: latin-1

"""Module für die Anmeldung."""

from ebkus.app import Request
from ebkus.app.ebapi import Akte, Fall, Anmeldung, cc


import ebkus.html.htmlgen as h
from ebkus.html.akte_share import akte_share


class _anm(Request.Request, akte_share):
    def _process(self,
                 title,
                 anm,
                 hidden,
                 ):
        anmeldekontakt = h.FieldsetInputTable(
            legend='Anmeldekontakt',
            daten=[[h.TextItem(label='Gemeldet von',
                               name='von',
                               value=anm['von'],
                               ),
                    h.TextItem(label='Telefon',
                               name='mtl',
                               value=anm['mtl'],
                               ),
                    ],
                   [h.SelectItem(label='Zugangsart',
                                 name='zm',
                                 options=self.for_kat('fszm', anm['zm']),
                                 ),
                    h.TextItem(label='Empfehlung von',
                               name='me',
                               value=anm['me'],
                               ),
                    ],
                   [h.DatumItem(label='Gemeldet am',
                                 name='a',
                                 date=anm.getDate('a'),
                                 ),
                    h.DummyItem(),
                    ],
                   [h.TextItem(label='Anmeldegrund',
                               name='mg',
                               value=anm['mg'],
                               class_='textboxverylarge',
                               maxlength=250,
                               n_col=4
                               ),
                    ],
                   [h.TextItem(label='Notiz',
                               name='no',
                               value=anm['no'],
                               class_='textboxverylarge',
                               maxlength=250,
                               n_col=4
                               ),
                    ],
            ]
            )
        res = h.FormPage(
            title=title,
            name='anmform',action="klkarte",method="post",
            breadcrumbs = (('Hauptmenü', 'menu'),
                           ('Klientenkarte', 'klkarte?akid=%(fall__akte_id)s' % anm),
                           ),
            hidden=hidden,
            rows=(anmeldekontakt,
                  h.SpeichernZuruecksetzenAbbrechen(),
                  ),
            )
        return res.display()



class anmneu(_anm):
    """Neue Anmeldung eintragen. (Tabelle: Anmeldung)"""
    permissions = Request.UPDATE_PERM
    def processForm(self, REQUEST, RESPONSE):
        if self.form.has_key('fallid'):
            fallid = self.form.get('fallid')
        else:
            self.last_error_message = "Keine ID für den Fall erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
        fall = Fall(fallid)
        akte = Akte(fall['akte_id'])
        bezugspersonen = akte['bezugspersonen']
        bezugspersonen.sort('verw__sort')
        anm = Anmeldung()
        anm.init(
            id=Anmeldung().getNewId(),
            fall_id=fall['id'],
            zm=cc('fszm', '999'),
            )
        # Datum des Fallbeginns und Nachname der 1 Bezugspers. zur Übernahme
        # im Formular anbieten.
        anm.setDate('a', fall.getDate('bg'))
        if bezugspersonen:
            b1 = bezugspersonen[0]
            anm['von'] = b1['na']
            anm['mtl'] = b1['tl1']
                    
        return self._process(
            title="Neue Anmeldeinformation eintragen",
            anm=anm,
            hidden=(('anmid', anm['id']),
                    ('file', 'anmeinf'),
                    ('fallid', anm['fall_id']),
                    )
            )
        
class updanm(_anm):
    """Anmeldung ändern. (Tabelle: Anmeldung)"""
    permissions = Request.UPDATE_PERM
    def processForm(self, REQUEST, RESPONSE):
        if self.form.has_key('anmid'):
            id = self.form.get('anmid')
        else:
            self.last_error_message = "Keine ID für die Anmeldung erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
        anm = Anmeldung(id)
        return self._process(
            title="Anmeldeinformation &auml;ndern",
            anm=anm,
            hidden=(('anmid', anm['id']),
                    ('file', 'updanm'),
                    ),
            )

class viewanm(Request.Request):
    """Anmeldung ändern. (Tabelle: Anmeldung)"""
    permissions = Request.UPDATE_PERM
    def processForm(self, REQUEST, RESPONSE):
        if self.form.has_key('anmid'):
            id = self.form.get('anmid')
        else:
            self.last_error_message = "Keine ID für die Anmeldung erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
        anm = Anmeldung(id)
        anmeldekontakt = h.FieldsetInputTable(
            legend='Anmeldekontakt',
            daten=[[h.TextItem(label='Gemeldet von',
                               name='von',
                               value=anm['von'],
                               readonly=True,
                               ),
                    h.TextItem(label='Anmeldegrund',
                               name='mg',
                               value=anm['mg'],
                               maxlength=250,
                               readonly=True,
                               ),
                    ],
                   [h.TextItem(label='Gemeldet am',
                               name='a',
                               value=str(anm.getDate('a')),
                               readonly=True,
                                 ),
                    h.TextItem(label='Empfehlung von',
                               name='me',
                               value=anm['me'],
                               readonly=True,
                               ),
                    ],
                   [h.TextItem(label='Telefon',
                               name='mtl',
                               value=anm['mtl'],
                               readonly=True,
                               ),
                    h.TextItem(label='Zugangsmodus',
                               name='zm',
                               value=anm['zm__name'],
                               readonly=True,
                               ),
                    ],
            ],
            button=h.Button(value="Schließen",
                            onClick="javascript:window.close()",
                            tip="Fenster schließen",
                            ),
            )
        res = h.FormPage(
            title="Detailansicht: Anmeldekontakt von %(fall__akte__vn)s  %(fall__akte__na)s" % anm,
            rows=(anmeldekontakt,),
            )
        return res.display()
        

