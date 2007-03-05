# coding: latin-1

"""Module für die Zuständigkeiten."""

import string

from ebkus.app import Request
from ebkus.app.ebapi import Akte, Fall, Zustaendigkeit, today
from ebkus.app.ebapih import mksel
from ebkus.app_surface.zustaendigkeit_templates import *
from ebkus.app_surface.standard_templates import *

class zustneu(Request.Request):
    """Neue Zuständigkeit eintragen. (Tabelle: Zuständigkeit.)"""
    
    permissions = Request.UPDATE_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        mitarbeiterliste = self.getMitarbeiterliste()
        user = self.user
        if self.form.has_key('fallid'):
            fallid = self.form.get('fallid')
        else:
            self.last_error_message = "Keine ID für den Fall erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
        fall = Fall(int(fallid))
        akte = Akte(fall['akte_id'])
        zustaendigkeiten = fall['zustaendigkeiten']
        zustaendigkeiten.sort('bgy', 'bgm', 'bgd')
        
        hidden ={'file': 'zusteinf'}
        zustid = Zustaendigkeit().getNewId()
        hiddenid ={'name': 'zustid', 'value': zustid}
        
        # Liste der Templates als String
        
        res = []
        res.append(head_normal_t %("Neue Zust&auml;ndigkeit eintragen"))
        res.append(thzustneu_t %fall)
        mksel(res, mitarbeiterliste_t, mitarbeiterliste, 'na', user)
        res.append(zustneudatum_t % today())
        res.append(formhiddenvalues_t % hidden)
        res.append(formhiddennamevalues_t % hiddenid)
        res.append(zustende_t % fall['zustaendig'])
        if len(zustaendigkeiten) > 0:
            res.append(thzustaendigkeiten_t)
            for z in zustaendigkeiten:
                res.append(zustaendigkeiten_t % z)
            res.append(zustaendigkeiten_ende_t)
            
        return string.join(res, '')
        
        
class updzust(Request.Request):
    """Neue Zuständigkeit eintragen. (Tabelle: Zuständigkeit.)"""
    
    permissions = Request.UPDATE_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        mitarbeiterliste = self.getMitarbeiterliste()
        user = self.user
        if self.form.has_key('zustid'):
            id  = self.form.get('zustid')
        else:
            self.last_error_message = "Keine ID für die Zuständigkeit erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
        zustaendigkeit = Zustaendigkeit(int(id))
        fall = Fall(zustaendigkeit['fall_id'])
        akte = Akte(fall['akte_id'])
        zustaendigkeiten = fall['zustaendigkeiten']
        zustaendigkeiten.sort('bgd', 'bgm', 'bgy')
        
        hidden ={'file': 'updzust'}
        # Liste der Templates als String
        
        res = []
        res.append(head_normal_t %("Eintrag zur Zust&auml;ndigkeit bearbeiten"))
        ########
        res.append(thzustupd_ta)
        res.append(thzustupd_t_zustid %id)
        res.append(thzustupd_tb %fall)
        mksel(res, mitarbeiterliste_t, mitarbeiterliste, 'id',
                zustaendigkeit['mit_id'])
        res.append(updzustdatum_t % zustaendigkeit)
        res.append(formhiddenvalues_t % hidden)
        if len(zustaendigkeiten) > 0:
            res.append(thzustaendigkeiten_t)
            for z in zustaendigkeiten:
                res.append(zustaendigkeiten_t % z)
            res.append(zustaendigkeiten_ende_t)
        return string.join(res, '')
        
        
        
