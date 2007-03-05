# coding: latin-1

"""Module für die Dokumente."""

import string

from ebkus.app import Request
from ebkus.app.ebapi import Fall, Akte, Dokument, Gruppendokument, DokumentList, GruppendokumentList, Gruppe, today, cc, get_akte_path, get_gruppe_path
from ebkus.app.ebapih import get_codes, mksel
from ebkus.app_surface.dokument_templates import *
from ebkus.app_surface.standard_templates import *


class vermneu(Request.Request):
    """Neuen Text  eintragen (Tabelle: Dokument, Gruppendokument)."""
    
    permissions = Request.VERM_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        mitarbeiterliste = self.getMitarbeiterliste()
        user = self.user
        
        # Das Formular ist 1 Fall oder 1 Gruppe zugeordnet.
        
        if self.form.has_key('gruppeid'):
            gruppeid = self.form.get('gruppeid')
            gruppe = Gruppe(int(gruppeid))
            action = "gruppenkarte"
            hidden = {'file': 'dokgreinf'}
            dokid = Gruppendokument().getNewId()
            hiddendokid ={'name': 'dokid', 'value': dokid}
            header = "Neuen Texteintrag zur Gruppe hinzuf&uuml;gen"
            tabkopf = formkopfdokgrneu_t % gruppe
            
        elif self.form.has_key('fallid'):
            fallid = self.form.get('fallid')
            fall = Fall(int(fallid))
            akte = Akte(fall['akte_id'])
            hidden ={'file': 'dokeinf'}
            dokid = Dokument().getNewId()
            hiddendokid ={'name': 'dokid', 'value': dokid}
            header = "Neuen Texteintrag zur Akte hinzuf&uuml;gen"
            tabkopf = formkopfdokneu_t % fall
            
        else:
            self.last_error_message = "Keine ID fuer den Fall erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
            
        dokarten = get_codes('dokart')
        dokarten.sort('name')
        
        # Liste der Templates als String
        
        res = []
        res.append(head_normal_t % header)
        res.append(tabkopf)
        res.append(formhiddenvalues_t % hidden)
        res.append(formhiddennamevalues_t % hiddendokid)
        res.append(vermneu_t % today() )
        res.append(vermneu2_t % self.mitarbeiter)
        mksel(res, codeliste_t, dokarten, 'name', 'Beraternotiz')
        res.append(vermneu3_t)
        return string.join(res, '')
        
        
class updverm(Request.Request):
    """Text ändern (Tabelle: Dokument, Gruppendokument)."""
    
    permissions = Request.VERM_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        mitarbeiterliste = self.getMitarbeiterliste()
        user = self.user
        
        # Das Formular ist 1 Fall oder 1 Gruppe zugeordnet.
        
        if self.form.has_key('dokid'):
            dokid = self.form.get('dokid')
            dok = Dokument(int(dokid))
        else:
            self.last_error_message = "Keine ID fuer Dokument erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
            
        fall = Fall(dok['fall_id'])
        akte = Akte(fall['akte_id'])
        dokarten = get_codes('dokart')
        dokarten.sort('name')
        
        try:
            akte_path = get_akte_path(akte['id'])
            f = open('%s/%s'
                     % (akte_path,dok['fname']), 'r')
            text = f.read()
            f.close()
        except Exception, e:
            meldung = {'titel':'Fehler',
                       'legende':'Fehlerbeschreibung',
                       'zeile1': str(e),
                       'zeile2':'Versuchen Sie es bitte erneut.'}
            return (meldung_t %meldung)
            
        dok['text'] = text
        
        # Fuer FORM-HIDDEN-VALUES
        
        hidden ={'file': 'updvermeinf'}
        hiddendokid ={'name': 'dokid', 'value': dokid}
        
        # Liste der Templates als String
        
        res = []
        res.append(head_normal_t %("Texteintrag der Akte &auml;ndern"))
        res.append(formkopfdokneu_t % fall)
        res.append(formhiddenvalues_t % hidden)
        res.append(formhiddennamevalues_t % hiddendokid)
        res.append(vermupd_t % dok )
        res.append(vermneu2_t % self.mitarbeiter)
        del dok['text']
        mksel(res, codeliste_t, dokarten, 'id', dok['art'])
        res.append(vermneu3_t)
        return string.join(res, '')
        
        
class updvermausw(Request.Request):
    """Auswahlbox zum Öffnen eines Textes
    (Tabellen: Dokument, Gruppendokument)."""
    
    permissions = Request.VERM_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        mitarbeiterliste = self.getMitarbeiterliste()
        user = self.user
        
        # Das Dokument ist 1 Fall oder 1 Gruppe zugeordnet.
        
        if self.form.has_key('fallid'):
            fallid = self.form.get('fallid')
            fall = Fall(int(fallid))
            akte = Akte(fall['akte_id'])
            dokliste = DokumentList(where = 'fall_id = %s and mit_id = %s and mtyp = %s'
                                        % (fall['id'], self.mitarbeiter['id'],
                                           cc('mimetyp', 'txt')), order = 'vy,vm,vd')
            
            header = "Texteintrag der Akte zum &Auml;ndern ausw&auml;hlen"
            hidden ={'file': 'updverm'}
            formkopf = formkopfdokneu_t % fall
            
        elif self.form.has_key('gruppeid'):
            gruppeid = self.form.get('gruppeid')
            gruppe = Gruppe(int(gruppeid))
            dokliste = GruppendokumentList(where = 'gruppe_id = %s and mit_id = %s and mtyp = %s'
                                        % (gruppe['id'], self.mitarbeiter['id'],
                                           cc('mimetyp', 'txt')), order = 'vy,vm,vd')
            
            header = "Texteintrag der Gruppe zum &Auml;ndern ausw&auml;hlen"
            hidden ={'file': 'updgrverm'}
            formkopf = formkopfdokgrneu_t % gruppe
            
        else:
            self.last_error_message = "Keine ID fuer Fall oder Gruppe erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
            
            # Liste der Templates als String
            
        res = []
        res.append(head_normal_t % header)
        res.append(formkopf)
        res.append(formhiddenvalues_t % hidden)
        res.append(vermausw_t)
        for d in dokliste:
            res.append(vermausw2_t % d)
        res.append(vermausw3_t)
        return string.join(res, '')
        
        
class upload(Request.Request):
    """Dokument uploaden (Tabellen: Dokument, Gruppendokument)."""
    
    permissions = Request.VERM_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        mitarbeiterliste = self.getMitarbeiterliste()
        user = self.user
        
        if self.form.has_key('gruppeid'):
            gruppeid = self.form.get('gruppeid')
            gruppe = Gruppe(int(gruppeid))
            action = "gruppenkarte"
            hidden = {'file': 'uploadgreinf'}
            dokid = Gruppendokument().getNewId()
            hiddendokid ={'name': 'dokid', 'value': dokid}
            header = "Datei zur Gruppe importieren"
            tabkopf = formulargrh_t % gruppe
        elif self.form.has_key('fallid'):
            fallid = self.form.get('fallid')
            fall = Fall(int(fallid))
            akte = Akte(fall['akte_id'])
            action = "dokkarte"
            hidden = {'file': 'uploadeinf'}
            dokid = Dokument().getNewId()
            hiddendokid ={'name': 'dokid', 'value': dokid}
            header = "Datei in die Akte aufnehmen"
            tabkopf = formularh_t % fall
        else:
            self.last_error_message = "Keine ID fuer Fall oder Gruppe erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
            
        dokartl = get_codes('dokart')
        dokartl.sort('name')
        
        # Liste der Templates als String
        
        res = []
        res.append(head_normal_t % header)
        res.append(uploadformh_t % action)
        res.append(formhiddenvalues_t % hidden)
        res.append(formhiddennamevalues_t % hiddendokid)
        res.append(tabkopf)
        res.append(uploadform_t % today())
        res.append(uploadform2_t % self.mitarbeiter)
        mksel(res, codeliste_t, dokartl, 'name', 'Bericht')
        res.append(uploadform3_t)
        page = string.join(res, '')
        #print "UPLOADPAGE: "
        #print page
        return page
        
        
class updgrverm(Request.Request):
    """Update Gruppendokument (Tabelle: Gruppendokument)."""
    
    permissions = Request.VERM_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        mitarbeiterliste = self.getMitarbeiterliste()
        user = self.user
        if self.form.has_key('dokid'):
            dokid = self.form.get('dokid')
        else:
            self.last_error_message = "Keine ID fuer Dokument erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
        dok = Gruppendokument(int(dokid))
        gruppe = Gruppe(dok['gruppe_id'])
        dokarten = get_codes('dokart')
        dokarten.sort('name')
        
        try:
            gruppe_path = get_gruppe_path(gruppe['id'])
            f = open('%s/%s'
                     % (gruppe_path,dok['fname']), 'r')
            text = f.read()
            f.close()
        except Exception, e:
            meldung = {'titel':'Fehler',
                       'legende':'Fehlerbeschreibung',
                       'zeile1': str(e),
                       'zeile2':'Versuchen Sie es bitte erneut.'}
            return (meldung_t %meldung)
            
        dok['text'] = text
        
        header = "Texteintrag der Gruppe &auml;ndern"
        
        # Fuer FORM-HIDDEN-VALUES
        
        hidden ={'file': 'updgrvermeinf'}
        hiddendokid ={'name': 'dokid', 'value': dokid}
        
        # Liste der Templates als String
        
        res = []
        res.append(head_normal_t % header)
        res.append(formkopfdokgrneu_t % gruppe)
        res.append(formhiddenvalues_t % hidden)
        res.append(formhiddennamevalues_t % hiddendokid)
        res.append(vermupd_t % dok )
        res.append(vermneu2_t %self.mitarbeiter)
        del dok['text']
        mksel(res, codeliste_t, dokarten, 'id', dok['art'])
        res.append(vermneu3_t)
        return string.join(res, '')
        
        
class rmdok(Request.Request):
    """Lösche Dokument (Tabellen: Dokument, Gruppendokument)."""
    
    permissions = Request.RMDOK_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        mitarbeiterliste = self.getMitarbeiterliste()
        user = self.user
        
        if self.form.has_key('fallid'):
            fallid = self.form.get('fallid')
            fall = Fall(int(fallid))
            akte = Akte(fall['akte_id'])
            dokliste = DokumentList(where = 'fall_id = %s and mit_id = %s'
                                        % (fall['id'], self.mitarbeiter['id']))
            header = "Dokumente und Texteintr&auml;ge der Akte löschen"
            hidden ={'file': 'removedoks'}
            formkopf = formkopfdokneu_t % fall
        elif self.form.has_key('gruppeid'):
            gruppeid = self.form.get('gruppeid')
            gruppe = Gruppe(gruppeid)
            dokliste = GruppendokumentList(where = 'gruppe_id = %s and mit_id = %s'
                                        % (gruppe['id'], self.mitarbeiter['id']))
            header = "Dokumente und Texteintr&auml;ge der Gruppe löschen"
            hidden ={'file': 'removegrdoks'}
            formkopf = formkopfdokgrneu_t % gruppe
        else:
            self.last_error_message = "Keine ID fuer Fall oder Gruppe erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
            
        dokliste.sort('art__name','vy','vm','vd')
        
        # Liste der Templates als String
        
        res = []
        res.append(head_normal_t % header)
        res.append(formkopf)
        res.append(formhiddenvalues_t % hidden)
        res.append(rmverm_t )
        for d in dokliste:
            res.append(rmverm2_t % d)
        res.append(rmverm3_t)
        return string.join(res, '')
        
        
        
