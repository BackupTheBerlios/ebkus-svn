# coding: latin-1
##***************************************************************************
## Projekt:     Kobit/EBKuS-neu
## Datei:       ebkus/html/wordexp.py
##
## Beschreibung:Klasse für den Export von Klientendatein in MS Wordvorlagen
##
## Basisklasse: Request
##
## Typen:       -
##
## Klassenname: wordexp
## Klassenart:  -
##
##---------------------------------------------------------------------------
##
## REVISIONEN:
##
## DATUM        AUTOR           BESCHREIBUNG
## 10.11.2001   brehmea(msg)    Ersterstellung
## 22.11.2001   brehmea(msg)    Aenderungen
##
##***************************************************************************

## Standardimporte
import string
import re

## EBKuSimporte
from ebkus.app import Request
from ebkus.app import ebupd
from ebkus.app import ebapi
from ebkus.app.ebapih import get_all_codes

from ebkus.app_surface.wordexp_templates import *
from ebkus.app_surface.standard_templates import *
from ebkus.app_surface.klientenkarte_templates import *



class wordexport(Request.Request):
##***************************************************************************
## Instanzvariablen
##***************************************************************************
    permissions = Request.KLKARTE_PERM
    
    ##***************************************************************************
    ## Methoden - CTOR / DTOR
    ##***************************************************************************
    
    ##***************************************************************************
    ## Methoden - eigene Funktionalität
    ##***************************************************************************
    ##***************************************************************************
    ## Methode:     processForm
    ## Parameter:   (REQUEST, RESPONSE)
    ## Return:      string, der ein HTML-Gerüst darstellt.
    ##
    ## Beschreibung:Die Klasse bietet folgende Funktionalitäten an
    ##              - Auswahl einer Worddokumentenvorlage
    ##              - Buttons zum Abbrechen
    ##              - Erstellen eines JavaScripts Respone, welches die Vorlage
    ##                öffnet und Variablen mit KKarteinhalten ersetzt.
    ##
    ## Vorbed.:     -
    ## Nebenwirk.:  -
    ##***************************************************************************
    def processForm(self, REQUEST, RESPONSE):
    
        akid = self.form.get('akid')
        wordvorlage = self.form.get('wordvorlage')
        
        if akid: akid = int(akid)
        else:
            self.last_error_message = "Keine AktenID erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
            
        if wordvorlage:
            pat = re.escape(wordvorlage)
            return self.make_export(akid, pat)
        else:
            return self.word_auswahl(akid)
            
        RESPONSE.redirect('wordexp?akid=%s' % akid)
        return ''
        
    def word_auswahl(self, akid):
        res = []
        res.append(head_normal_t %('Wordauswahl'))
        res.append(wordauswahl_t % (akid,akid))
        return string.join(res, '')
        
        
    def make_export(self, akid, wordvorlage):
    
        akte = ebapi.Akte(akid)
        bezugspersonen = akte['bezugspersonen']
        einrichtungen = akte['einrichtungen']
        faelle = akte['faelle']
        
        faelle.sort('bgy', 'bgm', 'bgd')
        bezugspersonen.sort('verw__sort')
        einrichtungen.sort('status', 'na')
        
        # Aktueller bzw. letzter Fall, Wiederaufnehmbarkeit
        
        letzter_fall = akte['letzter_fall']
        aktueller_fall = akte['aktueller_fall']
        wiederaufnehmbar =  akte['wiederaufnehmbar']
        
        
        res = []
        ###########
        header = "Export der Akte " + str(akid) + " in eine MS-Word Vorlage"
        #res.append(head_normal_t % header)
        #res.append(body_start)
        res.append(wordexport_top_t % (akid, wordvorlage))
        
        res.append(wordexport_kldaten_t % akte)
        #return string.join(res, '')
        #
        if bezugspersonen:
            n = 0
            for e in bezugspersonen:
                e['lfdnr'] = n
                res.append(wordexport_bzperson_t % (e))
                n = n + 1
                
                
                
        for f in faelle:
            n = 0
            for l in f['leistungen']:
                l['lfdnr'] = n
                res.append(wordexport_leistungen_t % l)
                n = n + 1
                
        n = 0
        for f in faelle:
            f['lfdnr'] = n
            res.append(wordexport_stand_t % f)
            n = n + 1
            
        for f in faelle:
            n = 0
            for z in f['zustaendigkeiten']:
                z['lfdnr'] = n
                res.append(wordexport_bearbeiter_t % z)
                n = n + 1
                
        for f in faelle:
            n = 0
            for a in f['anmeldung']:
                a['lfdnr'] = n
                res.append(wordexport_anmkontakte_t % a)
                n = n + 1
                
                
        if einrichtungen:
            n = 0
            for e in einrichtungen:
                e['lfdnr'] = n
                res.append(wordexport_einkontakte_t % e)
                
        fachstat_list=[]
        for f in faelle:
            for fs in f['fachstatistiken']:
                if fs['jahr']:
                    fachstat_list.append(fs)
        if fachstat_list:
            n = 0
            for fachstat in fachstat_list:
                fachstat['lfdnr'] = n
                res.append(wordexport_fachstat_t % fachstat)
                n = n + 1
                
                
        jgh_list=[]
        for f in faelle:
            for js in f['jgh_statistiken']:
                if js['ey']:
                    jgh_list.append(js)
        if jgh_list:
            n = 0
            for jghstat in jgh_list:
                jghstat['lfdnr'] = n
                res.append(wordexport_jghstat_t % jghstat)
                n = n + 1
                
        notizen_liste=[]
        n = 0
        if akte['no']:
            notizen_liste.append(wordexport_notiz_kldaten_t % akte)
            n = n + 1
        for b in bezugspersonen:
            if b['no']:
                b['lfdnr'] = n
                notizen_liste.append(wordexport_notiz_bzperson_t % b)
                n = n + 1
        for e in einrichtungen:
            if e['no']:
                e['lfdnr'] = n
                notizen_liste.append(wordexport_notiz_einkontakte_t % e)
                n = n + 1
        for f in faelle:
            for a in f['anmeldung']:
                if a['no']:
                    a['lfdnr'] = n
                    notizen_liste.append(wordexport_notiz_anmkontakte_t % a)
                    n = n + 1
        if notizen_liste:
            for notiz in notizen_liste:
                res.append(notiz)
                
        n = 0
        fall_gruppenkarte_list=[]
        for f in faelle:
            fallgruppen = ebapi.FallGruppeList(
              where = 'fall_id = %s' % f['id'])
            for g in fallgruppen:
                g['lfdnr'] = n
                f['lfdnr'] = n
                fall_gruppenkarte_list.append(wordexport_gkfall_t1 % g)
                fall_gruppenkarte_list.append(wordexport_gkfall_t2 % f)
                n = n + 1
        if fall_gruppenkarte_list:
            for eintrag in fall_gruppenkarte_list:
                res.append(eintrag)
                
        n = 0
        bzpers_list=[]
        for b in bezugspersonen:
            bezugspersongruppen = ebapi.BezugspersonGruppeList(
              where = 'bezugsp_id = %s' % b["id"])
            for e in bezugspersongruppen:
                e['lfdnr'] = n
                b['lfdnr'] = n
                bzpers_list.append(wordexport_gkbzp_t1 % e)
                bzpers_list.append(wordexport_gkbzp_t2 % b)
                n = n + 1
        if bzpers_list:
            for eintrag in bzpers_list:
                res.append(eintrag)
                
        res.append(wordexport_bot_t)
        return string.join(res, '')