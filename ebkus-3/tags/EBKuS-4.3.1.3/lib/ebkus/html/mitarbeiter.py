# coding: latin-1

"""Module für die Mitarbeiter-Daten."""

import string

from ebkus.app import Request
from ebkus.config import config
from ebkus.app.ebapi import Mitarbeiter, MitarbeiterList, Code, today, cc, EE
from ebkus.app.ebapih import get_codes, get_all_codes, mksel,mksel_benr
from ebkus.app_surface.mitarbeiter_templates import *
from ebkus.app_surface.standard_templates import *

import ebkus.html.htmlgen as h
from ebkus.html.akte_share import akte_share

class _mitarbeiter(Request.Request, akte_share):
    def get_mitarbeiter(self, 
                        edit_button=False, # falls False, kein edit button
                        hinzufuegen_button=False, # falls False, kein hinzufügen button
                        ):
        mitarbeiter_list = MitarbeiterList(where='')
        mitarbeiter_list.sort('stz__code', 'na')
        mitarbeiter_table = h.FieldsetDataTable(
            legend='Mitarbeiter',
            headers=('Benutzer', 'Name', 'Vorname', 'Status', 'Rechte', 'Stelle'),
            daten=[[edit_button and h.Icon(href= 'updmit?mitid=%(id)d' % mit,
                                            icon= "/ebkus/ebkus_icons/edit_button.gif",
                                            tip= 'Mitarbeiter bearbeiten')
                                      or None,
                    h.String(string=mit['ben']),
                    h.String(string=mit['na']),
                    h.String(string=mit['vn']),
                    h.String(string=mit['stat__name']),
                    h.String(string=mit['benr__name']),
                    h.String(string=mit['stz__name']),
                    ]
                    for mit in mitarbeiter_list],
            button=(hinzufuegen_button and
                    h.Button(value="Hinzufügen",
                             tip="Mitarbeiter hinzufügen",
                             onClick=
                             "go_to_url('mitneu')"
                             ) or None),
            )
        return mitarbeiter_table

    def _process(self, 
                 title,
                 file,
                 mit,
                 ):
        edit = h.FieldsetInputTable(
            legend=title,
            daten=[[h.TextItem(label='Vorname',
                               name='vn',
                               value=mit['vn'],
                               tip='Vorname des Mitarbeiters'
                               ),
                    h.TextItem(label='Nachname',
                               name='na',
                               value=mit['na'],
                               tip='Nachname des Mitarbeiters'
                               ),
                    h.TextItem(label='Benutzerkennung',
                               name='ben',
                               value=mit['ben'],
                               tip='Benutzerkennung des Mitarbeiters'
                               ),
                    ],
                   [h.SelectItem(label='Status',
                                 name='stat',
                                 options=self.for_kat('status',
                                                      sel=mit['stat'], all=True),
                                 ),
                    h.SelectItem(label='Rechte',
                                 name='benr',
                                 options=self.for_kat('benr',
                                                      sel=mit['benr'], all=True),
                                 ),
                    h.SelectItem(label='Stelle',
                                 name='stz',
                                 options=self.for_kat('stzei',
                                                      sel=mit['stz'], all=True),
                                 ),
                    ],
                   file in ('updmit',) and
                   [h.CheckItem(label='Passwort zurücksetzen',
                                name='changepassword',
                                value='1',
                                checked=False,
                                tip='Neues Passwort ist identisch mit der Benutzerkennung'
                               ),
                    h.DummyItem(),
                    ] or None,
                   ],
##             daten=[[h.TextItem(label='Vorname',
##                                name='vn',
##                                value=mit['vn'],
##                                tip='Vorname des Mitarbeiters'
##                                ),
##                     h.SelectItem(label='Status',
##                                  name='stat',
##                                  options=self.for_kat('status',
##                                                       sel=mit['stat'], all=True),
##                                  ),
##                     ],
##                    [h.TextItem(label='Nachname',
##                                name='na',
##                                value=mit['na'],
##                                tip='Nachname des Mitarbeiters'
##                                ),
##                     h.SelectItem(label='Rechte',
##                                  name='benr',
##                                  options=self.for_kat('benr',
##                                                       sel=mit['benr'], all=True),
##                                  ),
##                     ],
##                    [h.TextItem(label='Benutzerkennung',
##                                name='ben',
##                                value=mit['ben'],
##                                tip='Benutzerkennung des Mitarbeiters'
##                                ),
##                     h.SelectItem(label='Stelle',
##                                  name='stz',
##                                  options=self.for_kat('stzei',
##                                                       sel=mit['stz'], all=True),
##                                  ),
##                     ],
##                    file in ('updmit',) and
##                    [h.CheckItem(label='Passwort zurücksetzen',
##                                 name='changepassword',
##                                 value='1',
##                                 checked=False,
##                                 tip='Neues Passwort ist identisch mit der Benutzerkennung'
##                                ),
##                     h.DummyItem(),
##                     ] or None,
##                    ],
            )
        res = h.FormPage(
            title=title,
            name='mitedit',action="mitausw",method="post",
            breadcrumbs = (('Hauptmenü', 'menu'),
                           ('Mitarbeiter', 'mitausw'),
                           ),
            hidden=(("mitid", mit['id']),
                    ("file", file),
                    ),
            rows=(edit,
                  h.SpeichernZuruecksetzenAbbrechen(),
                  #self.get_mitarbeiter(),
                  ),
            )
        return res.display()

class mitausw(_mitarbeiter):
    """Auswahlformular zum Ändern der Mitarbeiterdaten. """
    permissions = Request.ADMIN_PERM
    def processForm(self, REQUEST, RESPONSE):
        file = self.form.get('file')
        if file:
            from ebkus.app import ebupd
            function = getattr(ebupd, file)
            function(self.form)
        res = h.Page(
            title='Mitarbeiter',
            breadcrumbs = (('Aministratorhauptmenü', 'menu'),
                           ),
            rows=(self.get_hauptmenu(),
                  self.get_mitarbeiter(edit_button=True,
                                       hinzufuegen_button=True),
                  ),
            )
        return res.display()

class mitneu(_mitarbeiter):
    """Mitarbeiterstammdatenformular."""
    permissions = Request.ADMIN_PERM
    def processForm(self, REQUEST, RESPONSE):
        mit = Mitarbeiter()
        mit.init(
            id=Mitarbeiter().getNewId(),
            vn='',
            na='',
            ben='',
            benr=cc('benr', 'bearb'),
            stat=cc('status', 'i'),
            stz=get_codes('stzei')[0],
            )
        return self._process('Neuer Mitarbeiter',
                             'miteinf',
                             mit)
    
##         bearbeiterliste = self.getMitarbeiterliste()
##         user = self.user
##         stelle = self.stelle
##         mitarbeiterliste = MitarbeiterList(where = '', order = 'na')
##         stellenzeichen = get_all_codes('stzei')
##         masterdb = Code(kat_code = 'dbsite', code = '%s' % config.MASTER_SITE)
##         benutzerarten = get_all_codes('benr')
##         dienststatusl = get_all_codes('status')
        
        
##         # Form-Hidden-Values
        
##         hidden ={'file': 'miteinf'}
##         mitid = Mitarbeiter().getNewId()
##         hiddenid ={'name': 'mitid', 'value': mitid}
        
##         # Liste der Templates als String
        
##         res = []
##         res.append(head_normal_ohne_help_t %("Neuen Mitarbeiter eintragen"))
##         res.append(mitarbeiter_neu_t1)
##         mksel(res, codelistecode_t, dienststatusl, 'code', 'i')
##         res.append(mitarbeiter_neu_t2)
##         mksel_benr(res, codelistecode_t, benutzerarten, 'code', 'bearb')
##         res.append(mitarbeiter_neu_t3)
##         mksel(res, codelistecode_t, stellenzeichen, 'code', stelle['code'])
##         res.append(mitarbeiter_neu_t4)
##         for m in mitarbeiterliste:
##             res.append(mitliste_t % m)
##         res.append(formhiddenvalues_t % hidden)
##         res.append(formhiddennamevalues_t % hiddenid)
##         res.append(mitarbeiter_neu_t5)
##         return string.join(res, '')
        
        
class updmit(_mitarbeiter):
    """Updateformular für die Stammdaten der Mitarbeiter. """
    permissions = Request.ADMIN_PERM
    def processForm(self, REQUEST, RESPONSE):
        mit_id = self.form.get('mitid')
        if not mit_id:
            EE('Keine Mitarbeiter-Id')
        mit = Mitarbeiter(mit_id)
        return self._process('Mitarbeiter bearbeiten',
                             'updmit',
                             mit)

##         bearbeiterliste = self.getMitarbeiterliste()
##         user = self.user
##         stelle = self.stelle
##         stellenzeichen = get_codes('stzei')
##         benutzerarten = get_codes('benr')
##         dienststatusl = get_codes('status')
##         mitarbeiterliste = MitarbeiterList(where = '', order = 'na')
##         if self.form.has_key('mitid'):
##             mitid = self.form.get('mitid')
##             mit = Mitarbeiter(int(mitid))
##         else:
##             self.last_error_message = "Keine ID fuer den Mitarbeiter erhalten"
##             return self.EBKuSError(REQUEST, RESPONSE)
            
##         hidden ={'file': 'updmit'}
##         hiddenid ={'name': 'mitid', 'value': mitid}
        
##         # Liste der Templates als String
        
##         res = []
##         res.append(head_normal_ohne_help_t %("Mitarbeitereintrag für '%(vn)s %(na)s' &auml;ndern" % mit))
##         res.append(mitarbeiter_upd_t1 %mit)
##         mksel(res, codelistecode_t, dienststatusl, 'id', mit['stat'])
##         res.append(mitarbeiter_upd_t2 %mit)
##         mksel_benr(res, codelistecode_t, benutzerarten, 'id', mit['benr'])
##         res.append(mitarbeiter_upd_t3 %mit)
##         mksel(res, codelistecode_t, stellenzeichen, 'id', mit['stz'])
##         res.append(mitarbeiter_upd_t4)
##         for m in mitarbeiterliste:
##             res.append(mitlistehrefs_t % m)
##         res.append(formhiddenvalues_t % hidden)
##         res.append(formhiddennamevalues_t % hiddenid)
##         res.append(mitarbeiter_upd_t5)
##         return string.join(res, '')
        
        
        
