# coding: latin-1

"""Module für die Klientenkarte."""

import string

from ebkus.app import Request
from ebkus.app import ebupd
from ebkus.app import ebapi
from ebkus.app.ebapih import get_all_codes
from ebkus.app_surface.klientenkarte_templates import *
from ebkus.app_surface.standard_templates import *



class klkarte(Request.Request):
    """Klientenkarte."""
    
    permissions = Request.KLKARTE_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        file = self.form.get('file')
        # Fall 1 Klientenkarte direkt darstellen
        if not file or file == 'klkarte':
            fallid = self.form.get('fallid')
            akid = self.form.get('akid')
            mitid = self.mitarbeiter['id']
            if akid: akid = int(akid)
            elif fallid: fallid = int(fallid)
            else:
                res = []
                meldung = {'titel':'Keine Men&uuml;auswahl erhalten!',
                        'legende':'Keine Men&uuml;auswahl erhalten!',
                         'zeile1':'Es wurde nichts aus dem Men&uuml; ausgew&auml;hlt.',
                         'zeile2':''}
                res.append(meldung_t % meldung)
                return string.join(res, '')
            return self.klkarte_display(akid, fallid, mitid)
            
            # Fall 2 erst einfuegen oder updaten, dann Klientenkarte darstellen
        if self.einfuege_oder_update_operationen.get(file):
            akid = self.einfuegen_oder_update(file)
            # damit Klientenkarte nicht als Ergebnis eines POST
            # dargestellt wird
            RESPONSE.redirect('klkarte?akid=%s' % akid)
            return ''
            
            # Fall 3 Dokumenten- Update- oder Einfuegeformular anzeigen
            # Folgende URLs haben denselben Effekt:
            # 1)  http://localhost/efb/ebs/klkarte?file=akteneu
            # 2)  http://localhost/efb/ebs/akteneu
            # Variante 1) nützlich wg. Aufruf aus menu.
            # Könnte auch mit redirect gelöst werden.
            
        if file == 'dokkarte':
            fallid = self.form.get('fallid')
            if fallid: fallid = int(fallid)
            else:
                res = []
                meldung = {'titel':'Keine Men&uuml;auswahl erhalten!',
                        'legende':'Keine Men&uuml;auswahl erhalten!',
                         'zeile1':'Es wurde nichts aus dem Men&uuml; ausgew&auml;hlt.',
                         'zeile2':''}
                res.append(meldung_t % meldung)
                return string.join(res, '')
            RESPONSE.redirect('dokkarte?fallid=%s' % fallid)
            return ''
        if file == 'updjghform' or file == 'updfsform':
            fallid = self.form.get('fallid')
            if not fallid:
                meldung = {'titel':'Keine Men&uuml;auswahl erhalten!',
                        'legende':'Keine Men&uuml;auswahl erhalten!',
                         'zeile1':'Es wurde nichts aus dem Men&uuml; ausgew&auml;hlt.',
                         'zeile2':''}
                return meldung_t % meldung
        return self.ebkus.dispatch(file, REQUEST, RESPONSE)
        
    einfuege_oder_update_operationen = {
      'akteeinf': ('akid', ebapi.Akte),
      'perseinf': ('akid', ebapi.Akte),
      'einreinf': ('akid', ebapi.Akte),
      'anmeinf': ('fallid', ebapi.Fall),
      'leisteinf': ('fallid', ebapi.Fall),
      'zusteinf': ('fallid', ebapi.Fall),
      'zdaeinf': ('fallid', ebapi.Fall),
      #'updfall': ('gfall', ebapi.Fall),
      'updakte': ('akid', ebapi.Akte),
      'updpers': ('bpid', ebapi.Bezugsperson),
      'updeinr': ('einrid', ebapi.Einrichtungskontakt),
      'updanm': ('anmid', ebapi.Anmeldung),
      'updleist': ('leistid', ebapi.Leistung),
      'updzust': ('zustid', ebapi.Zustaendigkeit),
      'updfall': ('fallid', ebapi.Fall),
      'waufneinf': ('fallid', ebapi.Fall),
      'zdareinf': ('fallid', ebapi.Fall),
      'fseinf': ('fsid', ebapi.Fachstatistik),
      'updfs': ('fsid', ebapi.Fachstatistik),
      'jgheinf': ('jghid', ebapi.Jugendhilfestatistik),
      'updjgh': ('jghid', ebapi.Jugendhilfestatistik),
      'fseinf': ('fsid', ebapi.Fachstatistik)
      }
    
    def einfuegen_oder_update(self, file):
        function = getattr(ebupd, file)
        function(self.form)
        id_name, klass = self.einfuege_oder_update_operationen.get(file)
        akid = klass(int(self.form[id_name]))['akte__id']
        return akid
        
    def klkarte_display(self, akid, fallid = None, mitid=None):
        "Darstellung der Klientenkarte."
        
        if not akid and fallid:
            fall = ebapi.Fall(fallid)
            akte = ebapi.Akte(fall['akte_id'])
        else:
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
        res.append(head_normal_t % 'Klientenkarte')
        res.append(body_start)
        if aktueller_fall:
            res.append(menue_t)
            res.append(menue1_t % aktueller_fall)
            res.append(menue2_t % akte)
            res.append(menue3_t % aktueller_fall)
        else:
            if wiederaufnehmbar:
                res.append(menue_t)
                res.append(menuewaufn_t1 % letzter_fall)
            else:
                res.append(menue_t)
                res.append(menuezdar_t1 % letzter_fall)
                ##*************************************************************************
                ## Klientendaten
                ##*************************************************************************
        res.append(klientenkarte_t % akte)
        if aktueller_fall:
            res.append(klientenkarte_t2 % akte)
        else:
            res.append(klientenkarte_t2_keinaktfall)
            ##*************************************************************************
            ## Bezugspersonen des Falles
            ##*************************************************************************
        if aktueller_fall:
            if bezugspersonen:
                res.append(bezugsperson_kopf)
                for e in bezugspersonen:
                    res.append(bezugsperson_t %e)
                res.append(bezugsperson_ende %akte)
            else:
                res.append(keine_bezugsperson_kopf)
                res.append(keine_bezugsperson_ende %akte)
        else:
            if bezugspersonen:
                res.append(bezugsperson_kopf)
                for e in bezugspersonen:
                    res.append(bezugsperson_t_keinaktfall %e)
                res.append(bezugsperson_ende_keinaktfall)
                
                ##*************************************************************************
                ## Leistungen des Falles
                ##*************************************************************************
        if aktueller_fall:
            res.append(leistung_kopf)
            for f in faelle:
                for l in f['leistungen']:
                    if f!=letzter_fall:
                        res.append(leistungs_t1a % l)
                    else:
                        res.append(leistungs_t1 % l)
                    if l['ey'] == 0:
                        res.append(leistungsendeleer_t1)
                    else:
                        res.append(leistungsendedatum_t1 % l)
            res.append(leistung_ende % akte)
        else:
            res.append(leistung_kopf)
            for f in faelle:
                for l in f['leistungen']:
                    res.append(leistungs_t1a_keinaktfall % l)
                    if l['ey'] == 0:
                        res.append(leistungsendeleer_t1)
                    else:
                        res.append(leistungsendedatum_t1 % l)
            res.append(leistung_ende_keinaktfall)
            
            ##*************************************************************************
            ## Status des Falles
            ##*************************************************************************
        res.append(fall_kopf)
        for f in faelle:
            if aktueller_fall:
                if f!=letzter_fall:
                    res.append(fall_t1a % f)
                else:
                    res.append(fall_t1 % f)
            else:
                res.append(fall_t1a_keinaktfall % f)
            if f['aktuell'] == 1:
                res.append(falloffen_t1)
            else:
                res.append(fallendedatum_t1 % f)
        if aktueller_fall:
            res.append(fallende_t_aktfall % akte)
        else:
            if wiederaufnehmbar:
                res.append(fallende_t_waufn % akte)
            else:
                res.append(fallende_t_zdarueck % akte)
                
                ##*************************************************************************
                ## Bearbeiter des Falles
                ##*************************************************************************
        res.append(bearbeiter_kopf_t1)
        for f in faelle:
            for z in f['zustaendigkeiten']:
                if aktueller_fall:
                    if f!=letzter_fall or z!=letzter_fall['zustaendig']:
                        res.append(bearbeiter_t1a % z)
                    else:
                        res.append(bearbeiter_t1 % z)
                else:
                    if f!=letzter_fall or z!=letzter_fall['zustaendig']:
                        res.append(bearbeiter_t1a_keinaktfall % z)
                    else:
                        res.append(bearbeiter_t1_keinaktfall % z)
                if z['ey'] == 0:
                    res.append(bearbeiterendeoffen_t1)
                else:
                    res.append(bearbeiterendedatum_t1 % z)
        if aktueller_fall:
            res.append(bearbeiter_ende_t1 % akte)
        else:
            res.append(bearbeiter_ende_keinaktfall)
            ##*************************************************************************
            ## Anmeldekontakte des Falles
            ##*************************************************************************
            
        anmeldungs_liste = []
        if aktueller_fall:
            for f in faelle:
                for a in f['anmeldung']:
                    if f!=letzter_fall:
                        anmeldungs_liste.append(alt_anmeldung_t % a)
                    else:
                        anmeldungs_liste.append(akt_anmeldung_t % a)
            if anmeldungs_liste:
                res.append(anmeldung_kopf)
                for anmeldung in anmeldungs_liste:
                    res.append(anmeldung)
                if aktueller_fall['anmeldung']:
                    res.append(anmeldung_ende_hatanm)
                else:
                    res.append(anmeldung_ende_keineanm % akte)
            else:
                res.append(keine_anmeldung_kopf)
                if aktueller_fall['anmeldung']:
                    res.append(keine_anmeldung_ende_hatanm)
                else:
                    res.append(keine_anmeldung_ende_keineanm % akte)
        else:
            for f in faelle:
                for a in f['anmeldung']:
                    anmeldungs_liste.append(anmeldung_t1_keinaktfall % a)
            if anmeldungs_liste:
                res.append(anmeldung_kopf)
                for anmeldung in anmeldungs_liste:
                    res.append(anmeldung)
                res.append(anmeldung_ende_keinaktfall)
                
                
                ##*************************************************************************
                ## Einrichtungskontakte des Falles
                ##*************************************************************************
        if aktueller_fall:
            if einrichtungen:
                res.append(einrichtungskontakt_kopf)
                for e in einrichtungen:
                    res.append(einrichtungskontakt_t % e)
                res.append(einrichtungskontakt_ende % akte)
            else:
                res.append(kein_einrichtungskontakt_kopf)
                res.append(kein_einrichtungskontakt_ende % akte)
        else:
            if einrichtungen:
                res.append(einrichtungskontakt_kopf)
                for e in einrichtungen:
                    res.append(einrichtungskontakt_t_keinaktfall % e)
                res.append(einrichtungskontakt_ende_keinaktfall)
                
                ##*************************************************************************
                ## Fachstatistiken des Falles
                ##*************************************************************************
        fachstat_list=[]
        for f in faelle:
            for fs in f['fachstatistiken']:
                fachstat_list.append(fs)
        if aktueller_fall:
            if fachstat_list:
                # alle editierbar
                res.append(fachstatistik_kopf_t)
                for fachstat in fachstat_list:
                    res.append(fachstatistik_t1 % fachstat)
                res.append(fachstatistik_ende % akte)
            else:
                res.append(fachstatistik_kopf_leer)
                res.append(fachstatistik_ende_leer % akte)
        else:
            if fachstat_list:
                # alle editierbar
                res.append(fachstatistik_kopf_t_keinaktfall)
                for fachstat in fachstat_list:
                    res.append(fachstatistik_t1 % fachstat)
                    #res.append(fachstatistik_keinaktfall % fachstat)
                res.append(fachstatistik_ende_keinaktfall)
                ##*************************************************************************
                ## Fall darf eigentlich nicht vorkommen!
                ## mastaleckT msg 19.11.2001
                ##*************************************************************************
            else:
                res.append(fachstatistik_kopf_leer_keinaktfall)
                res.append(fachstatistik_ende_leer_keinaktfall)
                
                
                ##*************************************************************************
                ## Jugendhilfestatistiken des Falles
                ##*************************************************************************
        jgh_list=[]
        for f in faelle:
            for js in f['jgh_statistiken']:
                if js['ey']:
                    jgh_list.append(js)
        if aktueller_fall:
            if jgh_list:
                # alle editierbar
                res.append(jghstatistiken_kopf_t)
                for jghstat in jgh_list:
                    res.append(jghstatistiken_t1 % jghstat)
                res.append(jghstatistiken_ende % akte)
            else:
                res.append(jghstatistiken_kopf_leer)
                res.append(jghstatistiken_ende_leer % akte)
        else:
            if jgh_list:
                # alle editierbar
                res.append(jghstatistiken_kopf_t_keinaktfall)
                for jghstat in jgh_list:
                    res.append(jghstatistiken_t1 % jghstat)
                res.append(jghstatistiken_ende_keinaktfall)
                ##*************************************************************************
                ## Fall darf eigentlich nicht vorkommen!
                ## mastaleckT msg 19.11.2001
                ##*************************************************************************
            else:
                res.append(jghstatistiken_kopf_leer_keinaktfall)
                res.append(jghstatistiken_ende_leer_keinaktfall)
                
                ##*************************************************************************
                ## Notizen zum Fall
                ##*************************************************************************
        notizen_liste=[]
        #notizen_liste.append(notiz_header %("Klient"))
        if akte['no']:
            notizen_liste.append(notiz_akte_t % akte)
            #notizen_liste.append(notiz_header %("Bezugspersonen"))
        for b in bezugspersonen:
            if b['no']:
                notizen_liste.append(notiz_bzpers_t % b)
                #notizen_liste.append(notiz_header %("Einrichtungskontakte"))
        for e in einrichtungen:
            if e['no']:
                notizen_liste.append(notiz_einrichtung_t % e)
                #notizen_liste.append(notiz_header %("Anmeldungskontakte"))
        for f in faelle:
            for a in f['anmeldung']:
                if a['no']:
                    notizen_liste.append(notiz_anmeldung_t % a)
        if notizen_liste:
            res.append(notiz_kopf)
            for notiz in notizen_liste:
                res.append(notiz)
            res.append(notiz_ende)
            
            ##*************************************************************************
            ## Gruppenkarten des Falles
            ##*************************************************************************
        fall_gruppenkarte_list=[]
        for f in faelle:
            fallgruppen = ebapi.FallGruppeList(
              where = 'fall_id = %s' % f['id'])
            for g in fallgruppen:
                if aktueller_fall:
                    fall_gruppenkarte_list.append(fallgruppen_t1 % g)
                else:
                    fall_gruppenkarte_list.append(fallgruppen_t1_keinaktfall % g)
                fall_gruppenkarte_list.append(fallgruppen_t2 % f)
        if fall_gruppenkarte_list:
            res.append(fall_gruppen_kopf)
            for eintrag in fall_gruppenkarte_list:
                res.append(eintrag)
            res.append(fall_gruppen_ende)
        else:
            res.append(fall_gruppen_leer)
            
            ##*************************************************************************
            ## Gruppenkarten der Bezugspersonen des Falles
            ##*************************************************************************
        bzpers_list=[]
        for b in bezugspersonen:
            bezugspersongruppen = ebapi.BezugspersonGruppeList(
              where = 'bezugsp_id = %s' % b["id"])
            for e in bezugspersongruppen:
                if aktueller_fall:
                    bzpers_list.append(bzpersgruppen_t1 % e)
                else:
                    bzpers_list.append(bzpersgruppen_t1_keinaktfall % e)
                bzpers_list.append(bzpersgruppen_t2 % b)
        if bzpers_list:
            res.append(bzpersgruppen_kopf)
            for eintrag in bzpers_list:
                res.append(eintrag)
            res.append(bzpersgruppen_ende)
        else:
            res.append(bzpersgruppen_leer)
        res.append(tabelle_ende)
        return string.join(res, '')
