# coding: latin-1

"""Module f�r die Bezugspersonen."""

import string

from ebkus.app import Request
from ebkus.config import config
from ebkus.app.ebapi import Akte, Fall, Bezugsperson, cc, Code, EE
from ebkus.app.ebapih import get_codes, mksel,mksel_str, mksel_str_upd
from ebkus.app_surface.klientenkarte_templates import detail_view_bezugsperson_t
from ebkus.app_surface.standard_templates import *
from ebkus.app_surface.bezugsperson_templates import *
from ebkus.app_surface.akte_templates import anschrift_bezugsperson_t

import ebkus.html.htmlgen as h
from ebkus.html.akte_share import akte_share

class _pers(Request.Request, akte_share):
    def _process(self,
                 title,
                 bzp,
                 hidden,
                 ):
        akte = bzp['akte']
        aktueller_fall = akte['aktueller_fall']
        bezugspersonen_list = akte['bezugspersonen']
        bezugspersonen_list.sort('verw__sort')
        notiz_wichtig = h.FieldsetInputTable(
            legend='Notiz',
            daten=[[h.TextItem(label='Notiz',
                               name='no',
                               value=bzp['no'],
                               maxlength=250,
                               class_='textbox310',
                               n_col=4,
                               ),
                    h.CheckItem(label='Wichtig',
                                name='nobed',
                                value=cc('notizbed', 't'),
                                checked=(bzp['nobed'] == cc('notizbed', 't'))
                                ),
                    ]],
            )
        verwandtschaftsart = h.FieldsetInputTable(
            legend='Verwandschaftsart',
            daten=[[h.SelectItem(label='Verwandschaftsart',
                                 name='verw',
                                 options=self.for_kat('klerv', bzp['verw'])),
            ]]
            )
        res = h.FormPage(
            title=title,
            name='persform',action="klkarte",method="post",
            breadcrumbs = (('Hauptmen�', 'menu'),
                           ('Klientenkarte', 'klkarte?akid=%s' % bzp['akte_id']),
                           ),
            hidden=hidden,
            rows=(h.Pair(left=self.get_klientendaten(bzp),
                         right=self.get_anschrift(bzp),
                         ),
                  verwandtschaftsart,
                  notiz_wichtig,
                  self.get_bezugspersonen(bezugspersonen_list, aktueller_fall,
                                          edit_button=False, view_button=True,
                                          hinzufuegen_button=False),
                  h.SpeichernZuruecksetzenAbbrechen(),
                  ),
            )
        return res.display()

class persneu(_pers):
    """Neue Bezugsperson eintragen. (Tabelle: Bezugsperson)"""
    permissions = Request.UPDATE_PERM
    def processForm(self, REQUEST, RESPONSE):
        if self.form.has_key('fallid'):
            fallid = self.form.get('fallid')
        else:
            return h.Meldung(legend='Keine ID f�r den Fall erhalten',
                             zeilen=('Keine ID f�r den Fall erhalten!',
                                     'Sie werden zum Hauptmen&uuml; weitergeleitet.'),
                             ).display()
        fall = Fall(fallid)
        akte = fall['akte']
        bzp = Bezugsperson()
        bzp.init(
            id=Bezugsperson().getNewId(),
            akte_id=fall['akte_id'],
            no='',
            nobed=cc('notizbed', 't'),
            vrt=cc('vert', 'f'),
            fs=cc('fsfs', '999'),
            verw=cc('klerv', '999'),
            gs=' ',
            )
        for f in ('na', 'plz', 'ort', 'str', 'hsnr', 'lage', 'tl1', 'tl2'):
            bzp[f] = akte[f]
        return self._process(title='Neue Bezugsperson eintragen',
                             bzp=bzp,
                             hidden=(('bpid', bzp['id']),
                                     ('file', 'perseinf'),
                                     ("strid", ""), # wird nur von strkat mit javascript gesetzt
                                     ('akid', bzp['akte_id']),
                                     ('vrt', bzp['vrt']),
                                     ),
                             )
        
class updpers(_pers):
    """Bezugsperson �ndern. (Tabelle: Bezugsperson)"""
    
    permissions = Request.UPDATE_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        if self.form.has_key('bpid'):
            id = self.form.get('bpid')
        else:
            self.last_error_message = "Keine ID f�r die Bezugsperson erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
        bzp = Bezugsperson(id)
        return self._process(title='Bezugsperson bearbeiten',
                             bzp=bzp,
                             hidden=(('bpid', bzp['id']),
                                     ('file', 'updpers'),
                                     ("strid", ""), # wird nur von strkat mit javascript gesetzt
                                     ('vrt', bzp['vrt']),
                                     )
                             )

class rmpers(Request.Request):
    permissions = Request.UPDATE_PERM
    def processForm(self, REQUEST, RESPONSE):
        if self.form.has_key('bpid'):
            id = self.form.get('bpid')
        else:
            self.last_error_message = "Keine ID f�r die Bezugsperson erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
        bzp = Bezugsperson(id)
        if bzp['gruppen']:
            raise EE('Mitglied einer Gruppe kann nicht gel�scht werden')
        if bzp['fallberatungskontakte']:
            raise EE('Teilnehmer/in an Beratungskontakt kann nicht gel�scht werden')
        return h.SubmitOrBack(
            legend='Daten f�r Bezugsperson l�schen',
            action='klkarte',
            method='post',
            hidden=(('file', 'removepers'),
                    ('bpid', bzp['id']),
                    ),
            zeilen=('Soll die Daten f�r Bezugsperson %(vn)s %(na)s endg�ltig gel�scht werden?' % bzp,
                    ),
            ).display()

    
class viewpers(Request.Request, akte_share):
    """Daten (Addresse, etc.) des Klienten bzw. einer Bezugsperson ansehen"""
    permissions = Request.UPDATE_PERM
    def processForm(self, REQUEST, RESPONSE):
        if self.form.has_key('bpid'):
            id = self.form.get('bpid')
            obj = Bezugsperson(id)
            title="Detailansicht: %(verw__name)s von  %(akte__vn)s  %(akte__na)s" % obj
        elif self.form.has_key('akid'):
            id = self.form.get('akid')
            obj = Akte(id)
            title="Detailansicht: Klient %(vn)s  %(na)s" % obj,
        else:
            self.last_error_message = "Keine ID f�r die Person erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
        res = h.FormPage(
            title=title,
            rows=(self.get_klientendaten_readonly(obj,
                                                  button=h.Button(value="Schlie�en",
                                                                  onClick="javascript:window.close()",
                                                                  tip="Fenster schlie�en",
                                                                  ),
                                                  ),
                  ),
            )
        return res.display()
        
