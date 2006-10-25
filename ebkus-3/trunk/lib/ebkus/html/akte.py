# coding: latin-1

"""Module für Akte und Fall."""

import string,time

from ebkus.app import Request
from ebkus.config import config
from ebkus.app.ebapi import StrassenkatalogList,Akte, Fall, Zustaendigkeit, today, cc,Code
from ebkus.app.ebapih import get_codes, mksel,mksel_str,mksel_str_upd
from ebkus.app_surface.akte_templates import *
from ebkus.app_surface.standard_templates import *

class akteneu(Request.Request):
    """Neue Fallakte anlegen (Tabellen: Akte, Fall, Zuständigkeit, Leistung)."""
    
    permissions = Request.UPDATE_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        mitarbeiterliste = self.getMitarbeiterliste()
        user = self.user
        familienarten = get_codes('fsfs')
        leistungsarten = get_codes('fsle')
        
        # Für FORM-HIDDEN-VALUES
        
        hidden ={'file': 'akteeinf'}
        akid = Akte().getNewId()
        hiddenid ={'name': 'akid', 'value': akid}
        hiddenid2={'name': 'stzbg', 'value': self.stelle['id']}
        
        # Liste der Templates als String
        res = []
        res.append(head_normal_t %('Neue Akte anlegen'))
        res.append(akte_neu_t1)
        mksel(res, codeliste_t, familienarten, 'code', '999')
        res.append(akte_neu_t3)
        mksel(res, mitarbeiterliste_t, mitarbeiterliste, 'ben', user)
        res.append(akte_neu_t4  % today())
        mksel(res, mitarbeiterliste_t, mitarbeiterliste, 'ben', user)
        res.append(akte_neu_t5)
        mksel(res, codeliste_t, leistungsarten, 'code', '1')
        res.append(akte_neu_t6 % today())
        res.append(formhiddenvalues_t % hidden)
        res.append(formhiddennamevalues_t % hiddenid)
        res.append(formhiddennamevalues_t % hiddenid2)
        res.append(akte_neu_t7 % today())
        return string.join(res, '')
        
        
class waufnneu(Request.Request):
    """Wiederaufnahme einer vorhandener  Fallakte
    (Tabellen: Akte, Fall, Zuständigkeit, Leistung)."""
    
    permissions = Request.UPDATE_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        mitarbeiterliste = self.getMitarbeiterliste()
        user = self.user
        if self.form.get('akid'):
            akid = self.form.get('akid')
        else:
            self.last_error_message = "Keine ID fuer die Akte erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
        akte = Akte(int(akid))
        letzter_fall = akte['letzter_fall']
        familienarten = get_codes('fsfs')
        leistungsarten = get_codes('fsle')
        
        # Für FORM-HIDDEN-VALUES
        
        hidden ={'file': 'waufneinf'}
        fallid = Fall().getNewId()
        hiddenid ={'name': 'fallid', 'value': fallid}
        hiddenstatus ={'name': 'status', 'value': cc('stand', 'l')}
        hiddenid2={'name': 'stzbg', 'value': self.stelle['id']}
        
        # Liste der Templates als String
        
        akte_kopie = akte
        res = []
        res.append(head_normal_t %("Wiederaufnahme des Klienten"))
        akte['legend'] = "Klientendaten von %(vn)s %(na)s" % akte
        akte['bezug_nominativ'] = 'der Klient'
        akte['bezug_genitiv'] = 'des Klienten'
        res.append(wiederaufnahme_t1 % akte)
        mksel(res, codeliste_t, familienarten, 'id', akte['fs'])
        res.append(wiederaufnahme_t3 %akte)
        mksel(res, mitarbeiterliste_t, mitarbeiterliste, 'ben', user)
        res.append(wiederaufnahme_t4  % today())
        mksel(res, mitarbeiterliste_t, mitarbeiterliste, 'ben', user)
        res.append(wiederaufnahme_t5)
        mksel(res, codeliste_t, leistungsarten)
        res.append(wiederaufnahme_t6 % today())
        res.append(formhiddenvalues_t % hidden)
        res.append(formhiddennamevalues_t % hiddenid)
        res.append(formhiddennamevalues_t % hiddenid2)
        res.append(formhiddennamevalues_t % hiddenstatus)
        res.append(wiederaufnahme_t7 % today())
        res.append(hiddenakte_id % letzter_fall)
        return string.join(res, '')
        
        
class updakte(Request.Request):
    """Akte ändern (Tabelle Akte)."""
    permissions = Request.UPDATE_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        mitarbeiterliste = self.getMitarbeiterliste()
        user = self.user
        if self.form.has_key('akid'):
            akid = self.form.get('akid')
            akte = Akte(int(akid))
        else:
            self.last_error_message = "Keine ID fuer die Akte erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
        letzter_fall = akte['letzter_fall']
        bezugspersonen = akte['bezugspersonen']
        bezugspersonen.sort('verw__sort')
        familienarten = get_codes('fsfs')
        verwandtschaftsarten = get_codes('klerv')
        
        hidden ={'file': 'updakte'}
        hiddenid2={'name': 'stzbg', 'value': akte['stzbg']}
        hiddenid3={'name': 'stzak', 'value': akte['stzak']}
        
        # Liste der Templates als String
        
        res = []
        res.append(head_normal_t % ('Akte aktualisieren'))
        akte['legend'] = 'Klientendaten'
        akte['bezug_nominativ'] = 'der Klient'
        akte['bezug_genitiv'] = 'des Klienten'
        res.append(akte_update_t1 % akte)
        mksel(res, codeliste_t, familienarten, 'id', akte['fs'])
        res.append(akte_update_t3 % akte)
        res.append(hiddenakte_id % letzter_fall)
        res.append(formhiddenvalues_t % hidden)
        res.append(formhiddennamevalues_t % hiddenid2)
        res.append(formhiddennamevalues_t % hiddenid3)
        res.append(akte_update_t7)
        return string.join(res, '')
        
        
class updfall(Request.Request):
    """Fall updaten (Tabelle: Fall)."""
    
    permissions = Request.UPDATE_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        mitarbeiterliste = self.getMitarbeiterliste()
        user = self.user
        if self.form.has_key('fallid'):
            fallid = self.form.get('fallid')
        else:
            self.last_error_message = "Keine ID fuer den Fall erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
        fall = Fall(int(fallid))
        akte = Akte(fall['akte_id'])
        zustaendigkeiten = fall['zustaendigkeiten']
        hidden ={'file': 'updfall'}
        
        # Liste der Templates als String
        
        res = []
        res.append(head_normal_t %("Beginndatum &auml;ndern"))
        res.append(updzda_t % fall)
        if len(zustaendigkeiten) > 0:
            res.append(thzustaendigkeiten_t)
            for z in zustaendigkeiten:
                res.append(zustaendigkeiten_t % z)
            res.append(zustaendigkeiten_ende_t)
        res.append(hiddenakte_id % fall)
        res.append(formhiddenvalues_t % hidden)
        res.append(updzda_t2 % fall)
        return string.join(res, '')
        
        
class zda(Request.Request):
    """Fallakte abschliessen (Tabellen: Fall und Zuständigkeit)."""
    
    permissions = Request.UPDATE_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        mitarbeiterliste = self.getMitarbeiterliste()
        user = self.user
        if self.form.has_key('fallid'):
            fallid = self.form.get('fallid')
        else:
            self.last_error_message = "Keine ID fuer den Fall erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
        fall = Fall(int(fallid))
        akte = Akte(fall['akte_id'])
        zustaendigkeiten = fall['zustaendigkeiten']
        zustaendigkeiten.sort('bgd', 'bgm', 'bgy')
        aktuell_zustaendig = fall['zustaendig']
        
        hidden ={'file': 'zdaeinf'}
        
        # Liste der Templates als String
        
        res = []
        res.append(head_normal_t %("Abschlu&szlig;datum eintragen"))
        res.append(zda_t % fall)
        res.append(zda_t2 % today())
        res.append(zda_t3 % aktuell_zustaendig)
        if len(zustaendigkeiten) > 0:
            res.append(thzustaendigkeiten_t)
            for z in zustaendigkeiten:
                res.append(zustaendigkeiten_t % z)
            res.append(zustaendigkeiten_ende_t)
        res.append(hiddenakte_id % fall)
        res.append(formhiddenvalues_t % hidden)
        res.append(zda_t4 % fall)
        return string.join(res, '')
        
        
class zdar(Request.Request):
    """Fallabschluss rückgängig machen und neue Zustaendigkeit eintragen
    (Tabellen: Fall und Zuständigkeit)."""
    
    permissions = Request.UPDATE_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        mitarbeiterliste = self.getMitarbeiterliste()
        user = self.user
        if self.form.has_key('fallid'):
            fallid = self.form.get('fallid')
        else:
            self.last_error_message = "Keine ID fuer den Fall erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
        fall = Fall(int(fallid))
        akte = Akte(fall['akte_id'])
        zustaendigkeiten = fall['zustaendigkeiten']
        letzte_zustaendigkeit = zustaendigkeiten[-1]
        zustaendigkeiten.sort('bgd', 'bgm', 'bgy')
        
        zustid = Zustaendigkeit().getNewId()
        hiddenid ={'name': 'zustid', 'value': zustid}
        hidden ={'file': 'zdareinf'}
        
        # Liste der Templates als String
        
        res = []
        res.append(head_normal_t %("Abschlussdatum r&uuml;ckg&auml;ngig machen"))
        res.append(zdarzust1_t)
        mksel(res, mitarbeiterliste_t, mitarbeiterliste, 'id',
              letzte_zustaendigkeit['mit_id'])
        res.append(zdarzust2_t % today())
        res.append(hiddenakte_id % fall)
        res.append(formhiddenvalues_t % hidden)
        res.append(formhiddennamevalues_t % hiddenid)
        res.append(zdarzust3_t %fall)
        return string.join(res, '')
        
        
class rmakten(Request.Request):
    """Abfrageformular zum Löschen von Akten."""
    
    permissions = Request.ADMIN_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        mitarbeiterliste = self.getMitarbeiterliste()
        user = self.user
        
        # Liste der Templates als String
        
        res = []
        res.append(head_normal_ohne_help_t %('Einstellungen f&uuml;r den L&ouml;schvorgang'))
        res.append(rmakten_t % int(config.LOESCHFRIST))
        return string.join(res, '')
        
        
class rmakten2(Request.Request):
    """Löscht die Akten, welche älter als die Löschfrist sind.
    Die Statistiktabellen bleiben erhalten. Die fall_id wird auf NULL gesetzt.
    """
    
    permissions = Request.ADMIN_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        mitarbeiterliste = self.getMitarbeiterliste()
        user = self.user
        if self.form.has_key('frist'):
            frist = self.form.get('frist')
        else:
            self.last_error_message = "Keine Frist erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
            
        jahr = today().year
        monat = today().month
        heute = int(jahr)*12 + int(monat)
        loeschzeitm = int(heute)-int(frist)
        loeschjahr = int(loeschzeitm) / int(12)
        loeschmonat = int(loeschzeitm) - (int(loeschjahr) * int(12))
        
        hidden ={'file': 'removeakten'}
        
        res = []
        res.append(head_normal_ohne_help_t %("Akten und Gruppen löschen"))
        res.append(rmakten2a_t)
        res.append(formhiddenvalues_t % hidden)
        res.append(formhiddennamevalues_t % ({'value': frist, 'name': 'frist'}))
        res.append(formhiddennamevalues_t % ({'value': loeschjahr,
                                              'name': 'loeschjahr'}))
        res.append(formhiddennamevalues_t % ({'value': loeschmonat,
                                              'name': 'loeschmonat'}))
        res.append(rmakten2b_t % (frist, loeschmonat, loeschjahr ))
        return string.join(res, '')
        
        
        
        
        
        
