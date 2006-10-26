# coding: latin-1

"""Module für die Bezugspersonen."""

import string

from ebkus.app import Request
from ebkus.app.ebapi import StrassenkatalogList,Akte, Fall, Bezugsperson, cc, Code
from ebkus.app.ebapih import get_codes, mksel,mksel_str, mksel_str_upd
from ebkus.app_surface.klientenkarte_templates import detail_view_bezugsperson_t
from ebkus.app_surface.standard_templates import *
from ebkus.app_surface.bezugsperson_templates import *
from ebkus.app_surface.akte_templates import anschrift_bezugsperson_t

class persneu(Request.Request):
    """Neue Bezugsperson eintragen. (Tabelle: Bezugsperson)"""
    
    permissions = Request.UPDATE_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        mitarbeiterliste = self.getMitarbeiterliste()
        user = self.user
        if self.form.has_key('fallid'):
            fallid = self.form.get('fallid')
        else:
            res = []
            meldung = {'titel':'Keine ID für die Bezugsperson erhalten!',
                     'legende':'Keine ID für die Bezugsperson erhalten!',
                     'zeile1':'Keine ID für die Bezugsperson erhalten',
                     'zeile2':'Sie werden zum Hauptmen&uuml; weitergeleitet.'}
            res.append(meldung_t % meldung)
            return string.join(res, '')
        fall = Fall(fallid)
        akte = Akte(fall['akte_id'])
        letzter_fall = akte['letzter_fall']
        bezugspersonen = akte['bezugspersonen']
        bezugspersonen.sort('verw__sort')
        verwandtschaftsarten = get_codes('klerv')
        familienarten = get_codes('fsfs')
        
        hidden ={'file': 'perseinf'}
        bpid = Bezugsperson().getNewId()
        hiddenid ={'name': 'bpid', 'value': bpid}
        
        # Liste der Templates als String
        
        res = []
        res.append(head_normal_t %('Neue Bezugsperson eintragen'))
        # Personendaten bleiben leer
        res.append(bzpers_neu_t1)
        # Anschrift wird von Klientenakte uebernommen
        akte['bezug_nominativ'] = 'die Bezugsperson'
        akte['bezug_genitiv'] = 'der Bezugsperson'
        res.append(anschrift_bezugsperson_t % akte)
        mksel(res, codeliste_t, familienarten, 'id', cc('fsfs','999'))
        res.append(bzpers_neu_t3 % {'nobed': cc('notizbed', 't'),'vrt' : cc('vert', 'f') })
        res.append(bzpers_neu_t4a)
        mksel(res, codeliste_t, verwandtschaftsarten, 'id',cc('klerv', '999'))
        res.append(bzpers_neu_t4b)
        bezugspersonenliste = []
        for bz in bezugspersonen:
            bezugspersonenliste.append(bz)
        if bezugspersonenliste:
            res.append(bezugsperson_kopf)
            for bz in bezugspersonenliste:
                res.append(bezugsperson_t % bz)
            res.append(bezugsperson_ende)
        res.append(bzpers_neu_t5)
        res.append(formhiddenvalues_t % hidden)
        res.append(formhiddennamevalues_t % hiddenid)
        res.append(bzpers_neu_t6 % letzter_fall)
        
        return string.join(res, '')
        
class updpers(Request.Request):
    """Bezugsperson ändern. (Tabelle: Bezugsperson)"""
    
    permissions = Request.UPDATE_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        mitarbeiterliste = self.getMitarbeiterliste()
        user = self.user
        if self.form.has_key('bpid'):
            id = self.form.get('bpid')
        else:
            self.last_error_message = "Keine ID für die Bezugsperson erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
        bezugsperson = Bezugsperson(int(id))
        akte = bezugsperson['akte']
        letzter_fall = akte['letzter_fall']
        bezugspersonen = akte['bezugspersonen']
        bezugspersonen.sort('verw__sort')
        verwandtschaftsarten = get_codes('klerv')
        familienarten = get_codes('fsfs')
        
        hidden ={'file': 'updpers'}
        
        # Liste der Templates als String
        
        res = []
        res.append(head_normal_t %('Bezugsperson bearbeiten'))
        bezugsperson['legend'] = 'Bezugspersonendaten'
        bezugsperson['bezug_nominativ'] = 'die Bezugsperson'
        bezugsperson['bezug_genitiv'] = 'der Bezugsperson'
        res.append(bzpers_edit_t1 % bezugsperson)
        mksel(res, codeliste_t, familienarten, 'id', bezugsperson['fs'])
        if bezugsperson['nobed'] == cc('notizbed', 't'):
            check = 'checked'
        else:
            check = ''
        res.append(bzpers_edit_t3 % {'nobed': cc('notizbed', 't'),
                                   'check' : check,
                                   'no': bezugsperson['no'],
                                   'vrt': bezugsperson['vrt']})
        res.append(bzpers_edit_t4a)
        mksel(res, codeliste_t, verwandtschaftsarten, 'id', bezugsperson['verw'])
        res.append(bzpers_edit_t4b)
        bezugspersonenliste = []
        for bz in bezugspersonen:
            bezugspersonenliste.append(bz)
        if bezugspersonenliste:
            res.append(bezugsperson_kopf)
            for bz in bezugspersonenliste:
                res.append(bezugsperson_t % bz)
            res.append(bezugsperson_ende)
        res.append(bzpers_edit_t5)
        res.append(formhiddenvalues_t % hidden)
        res.append(bzpers_edit_t6 % bezugsperson)
        res.append(bzpers_edit_t6b % letzter_fall)
        return string.join(res, '')
        
class viewpers(Request.Request):
    """Bezugsperson ändern. (Tabelle: Bezugsperson)"""
    
    permissions = Request.UPDATE_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        mitarbeiterliste = self.getMitarbeiterliste()
        user = self.user
        if self.form.has_key('bpid'):
            id = self.form.get('bpid')
        else:
            self.last_error_message = "Keine ID für die Bezugsperson erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
        bezugsperson = Bezugsperson(int(id))
        akte = bezugsperson['akte']
        letzter_fall = akte['letzter_fall']
        bezugspersonen = akte['bezugspersonen']
        bezugspersonen.sort('verw__sort')
        verwandtschaftsarten = get_codes('klerv')
        familienarten = get_codes('fsfs')
        
        hidden ={'file': 'updpers'}
        
        # Liste der Templates als String
        
        res = []
        titel = ("Detailansicht: " + bezugsperson['verw__name'] + " von " + akte['vn'] + " " + akte['na'])
        res.append(head_normal_ohne_help_t %(titel))
        res.append(detail_view_bezugsperson_t % bezugsperson)
        return string.join(res, '')
        
        
