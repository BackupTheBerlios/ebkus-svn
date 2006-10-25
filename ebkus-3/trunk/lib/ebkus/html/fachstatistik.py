# coding: latin-1
##*************************************************************************
## Projekt:       EBKuS
##
## Datei:         fachstatistik.py
##
## Beschreibung:  ...
##
## Klassen:       fsneu
##                updfs
##                updfsausw
##*************************************************************************
##
## Revisionen:
##
## Datum:                 Autor:          Beschreibung:
##
## 01.10.2001             mastaleckT      Entfernen der verwaisten Klassen-
##                                        elemente nach Integration migrate_
##                                        berlin.py
##
##*************************************************************************

import string
from ebkus.app import ebapi
from ebkus.app import Request,date
from ebkus.app.ebapi import Akte, Fall, Fachstatistik, FachstatistikList, LeistungList,cc,today,Code
from ebkus.app.ebapih import get_codes, mksel, get_all_codes
from ebkus.app_surface.fachstatistik_templates import *
from ebkus.app_surface.standard_templates import *


##*************************************************************************
##
## Erstellen einer neuen Fachstatistik
##
## 01.10.2001 mastaleckT(msg)
##*************************************************************************
class fsneu(Request.Request):
    """Neue Fachstatistik eintragen. (Tabelle: Fachstatistik)"""
    
    permissions = Request.STAT_PERM
    def processForm(self, REQUEST, RESPONSE):
        mitarbeiterliste = self.getMitarbeiterliste()
        user = self.user
        fallid = self.form.get('fallid')
        ##*************************************************************************
        ##
        ## Prüft ob eine Fall_ID vorhanden ist. Wenn nicht, kann keine Fachstat
        ## erstellt werden.
        ##
        ## 01.10.2001 mastaleckT(msg)
        ##*************************************************************************
        if not fallid:
            res = []
            meldung = {'titel':'Fehler',
                     'legende':'Fehlerbeschreibung',
                     'zeile1':'Erstellen einer Fachstatistik nur f&uuml;r einen Fall moeglich!',
                     'zeile2':''}
            res.append(meldung_t % meldung)
            return string.join(res, '')
            
            
            ##*************************************************************************
            ##
            ## Weiteres Prüfen der Fallzugehörigkeit (Mit Fall - ID oder ohne Fall - ID)
            ## nicht mehr notwendig, da nur noch bei vorhandener Fall ID eine
            ## Statistik erstellt werden kann
            ##
            ## mastaleckT(msg)02.10.2001
            ##*************************************************************************
        fall = Fall(int(fallid))
        anmeldungl = fall['anmeldung']
        akte = fall['akte']
        letzter_fall = akte['letzter_fall']
        leistungen = fall['leistungen']
        jahr = '%(year)s' % today()
        vorjahr = int(jahr) - 1
        
        jahresl = ebapi.FachstatistikList(where = "fall_fn = '%s'" % letzter_fall['fn'])
        if jahresl:
            res = []
            meldung = {'titel':'Hinweis',
                     'legende':'Hinweis',
                     'zeile1':'Es ist bereits eine Fachstatistik f&uuml;r die Fallnummer vorhanden!',
                     'zeile2':''}
            res.append(meldung_t % meldung)
            return string.join(res, '')
            
            ##*************************************************************************
            ##
            ## Funktion berechnet das Alter des Klienten
            ##
            ## mastaleckT(msg) 04.10.2001
            ##
            ##*************************************************************************
        alter_klient = date.calc_age(akte['gb'],letzter_fall['bgd'],letzter_fall['bgm'],letzter_fall['bgy'])
        
        #fstatliste = FachstatistikList(where = 'fall_id = %(id)d' % fall
        #                                 + " and jahr = %d" % vorjahr,
        #                                 order = 'jahr')
        stellenzeichen = get_codes('stzei')
        geschlechter = get_codes('gs')
        altersgruppen = get_codes('fsag')
        altersgruppeneltern = get_codes('fsagel')
        familienarten = get_codes('fsfs')
        zugangsarten = get_codes('fszm')
        herkunftelternl = get_codes('fshe')
        berufelternl = get_codes('fsbe')
        beratungsanlaesse = get_codes('fsba')
        problembereicheeltern = get_codes('fspbe')
        problembereichekinder = get_codes('fspbk')
        qualifikationen_mutter_vater = get_codes('fsquali')
        qualifikationen_kind = get_codes('fsqualij')
        massnahmen = get_codes('fsle')
        hidden ={'file': 'fseinf'}
        fsid = Fachstatistik().getNewId()
        hiddenid ={'name': 'fsid', 'value': fsid}
        res = []
        ##*************************************************************************
        ##
        ## Formular: Erstellen einer neuen Fachstatistik
        ##
        ##*************************************************************************
        res.append(head_normal_t %('Neue Fachstatistik erstellen'))
        res.append(fsneu_t1)
        res.append(fsneu_fn_t % fall)
        mitarb_data = {'mit_id': self.mitarbeiter['id'],'mit_name' : self.mitarbeiter['ben']}
        res.append(fsneu_mit_t % mitarb_data)
        res.append(fsneu_jahr_t % today())
        res.append(fsneu_region_t % akte)
        
        res.append(fsneu_geschlecht_t)
        mksel(res, codeliste_t, geschlechter)
        res.append(fsneu_altersgr_t)
        if(alter_klient >= 0 and alter_klient <= 2):
            altersgruppe_kat = cc('fsag','1')
        elif(alter_klient >= 3 and alter_klient <= 5):
            altersgruppe_kat = cc('fsag','2')
        elif(alter_klient >= 6 and alter_klient <= 9):
            altersgruppe_kat = cc('fsag','3')
        elif(alter_klient >= 10 and alter_klient <= 13):
            altersgruppe_kat = cc('fsag','4')
        elif(alter_klient >= 14 and alter_klient <= 17):
            altersgruppe_kat = cc('fsag','5')
        elif(alter_klient >= 18 and alter_klient <= 20):
            altersgruppe_kat = cc('fsag','6')
        elif(alter_klient >= 21 and alter_klient <= 26):
            altersgruppe_kat = cc('fsag','7')
        else:
            altersgruppe_kat = cc('fsag','999')
        mksel(res, codeliste_t, altersgruppen, 'id', altersgruppe_kat)
        res.append(fsneu_famstatus_t)
        for f in familienarten:
            if fallid and fall['akte_id__fs'] == f['id']:
                f['sel'] = 'selected'
            else:
                f['sel'] = ''
            res.append(codeliste_t % f)
        res.append(fsneu_zugangsmodus_t)
        mksel(res, codeliste_t, zugangsarten)
        res.append(fsneu_qualikind_t)
        mksel(res, codeliste_t, qualifikationen_kind)
        res.append(fsneu_qualimutter_t)
        mksel(res, codeliste_t, qualifikationen_mutter_vater)
        res.append(fsneu_qualivater_t)
        mksel(res, codeliste_t, qualifikationen_mutter_vater)
        res.append(fsneu_berufmutter_t)
        mksel(res, codeliste_t, berufelternl)
        res.append(fsneu_berufvater_t)
        mksel(res, codeliste_t, berufelternl)
        res.append(fsneu_hkmutter_t)
        mksel(res, codeliste_t, herkunftelternl)
        res.append(fsneu_hkvater_t)
        mksel(res, codeliste_t, herkunftelternl)
        res.append(fsneu_altermutter_t)
        mksel(res, codeliste_t, altersgruppeneltern)
        res.append(fsneu_altervater_t)
        mksel(res, codeliste_t, altersgruppeneltern)
        res.append(fsneu_beratungsanlass1_t)
        mksel(res, codeliste_t, beratungsanlaesse)
        res.append(fsneu_beratungsanlass2_t)
        mksel(res, codeliste_t, beratungsanlaesse)
        res.append(fsneu_problemkind_t)
        mksel(res, codeliste_t, problembereichekinder)
        res.append(fsneu_problemeltern_t)
        mksel(res, codeliste_t, problembereicheeltern)
        res.append(fsneu_problemspektrumkind_t )
        mksel(res, codeliste_t, problembereichekinder)
        res.append(fsneu_problemkindnot_t)
        res.append(fsneu_problemspektrumeltern_t)
        mksel(res, codeliste_t, problembereicheeltern)
        res.append(fsneu_problemelternnot_t)
        res.append(fsneu_massnahmen_t)
        fsleistungen = LeistungList(where = 'fall_id = %s' % letzter_fall['id'])
        leistungs_liste = []
        for s in fsleistungen:
            leistungs_liste.append(s['le'])
        mksel(res, codeliste_t, massnahmen,'id',leistungs_liste)
        
        res.append(fsneu_zahlkontakte_t)
        res.append(formhiddenvalues_t % hidden)
        res.append(formhiddennamevalues_t % hiddenid)
        res.append(fsneu_notizsubmit_t)
        return string.join(res, '')
        
        ##*************************************************************************
        ##
        ## Updaten einer Fachstatistik
        ##
        ## 01.10.2001 mastaleckT(msg)
        ##*************************************************************************
# kann auch als updfsform angesprochen werden (siehe EBKuS.py)
# wird in menu_templates.py verwendet
class updfs(Request.Request):
    permissions = Request.STAT_PERM
    def processForm(self, REQUEST, RESPONSE):
        mitarbeiterliste = self.getMitarbeiterliste()
        mitarbeiter = self.mitarbeiter
        user = self.user
        if self.form.has_key('fsid'):
            id = self.form.get('fsid')
            fstat = Fachstatistik(int(id))
        elif self.form.has_key('fallid'):
            fallid = self.form.get('fallid')
            fall = Fall(fallid)
            fs = fall['fachstatistiken']
            if not fs:
                meldung = {'titel':'Hinweis',
                           'legende':'Hinweis',
                           'zeile1':'Es ist noch keine Fachstatistik f&uuml;r den Fall vorhanden!',
                           'zeile2':''}
                return meldung_t % meldung
            else:
                fstat = fs[-1] # müsste eigentlich immer nur eine sein ...
        else:
            self.last_error_message = "Keine ID für die Fachstatistik erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
        fsleistungen = fstat['leistungen']
        fskindprobleme = fstat['fachstatkindprobleme']
        fselternprobleme = fstat['fachstatelternprobleme']
        fallid = fstat.get('fall_id')
        fall = Fall(int(fstat['fall_id']))
        akte = fall['akte']
        stellenzeichen = get_codes('stzei')
        geschlechter = get_codes('gs')
        altersgruppen = get_codes('fsag')
        altersgruppeneltern = get_codes('fsagel')
        familienarten = get_codes('fsfs')
        zugangsarten = get_codes('fszm')
        herkunftelternl = get_codes('fshe')
        berufelternl = get_codes('fsbe')
        beratungsanlaesse = get_codes('fsba')
        problembereicheeltern = get_codes('fspbe')
        problembereichekinder = get_codes('fspbk')
        qualifikationen_mutter_vater = get_codes('fsquali')
        qualifikationen_kind = get_codes('fsqualij')
        massnahmen = get_codes('fsle')
        hidden ={'file': 'updfs'}
        res = []
        res.append(head_normal_t %('Fachstatistik &auml;ndern'))
        res.append(fsupd_t1)
        res.append(fsupd_fn_t % fstat)
        res.append(fsupd_mit_t % {'mit_id': fstat['mit_id'],'mit_name' : fstat['mit_id__ben']})
        res.append(fsupd_jahr_t % ({'year' : fstat['jahr']}))
        res.append(fsupd_region_t % fstat['bz'])
        
        res.append(fsupd_geschlecht_t)
        mksel(res, codeliste_t, geschlechter, 'id', fstat['gs'])
        res.append(fsupd_altersgr_t)
        mksel(res, codeliste_t, altersgruppen, 'id', fstat['ag'])
        res.append(fsupd_famstatus_t)
        mksel(res, codeliste_t, familienarten, 'id', fstat['fs'])
        res.append(fsupd_zugangsmodus_t)
        mksel(res, codeliste_t, zugangsarten, 'id', fstat['zm'])
        res.append(fsneu_qualikind_t)
        mksel(res, codeliste_t, qualifikationen_kind,'id', fstat['qualij'])
        res.append(fsneu_qualimutter_t)
        mksel(res, codeliste_t, qualifikationen_mutter_vater, 'id', fstat['qualikm'])
        res.append(fsneu_qualivater_t)
        mksel(res, codeliste_t, qualifikationen_mutter_vater, 'id', fstat['qualikv'])
        res.append(fsupd_berufmutter_t)
        mksel(res, codeliste_t, berufelternl, 'id', fstat['bkm'])
        res.append(fsupd_berufvater_t)
        mksel(res, codeliste_t, berufelternl, 'id', fstat['bkv'])
        res.append(fsupd_hkmutter_t)
        mksel(res, codeliste_t, herkunftelternl, 'id', fstat['hkm'])
        res.append(fsupd_hkvater_t)
        mksel(res, codeliste_t, herkunftelternl, 'id', fstat['hkv'])
        res.append(fsupd_altermutter_t)
        mksel(res, codeliste_t, altersgruppeneltern, 'id', fstat['agkm'])
        res.append(fsupd_altervater_t)
        mksel(res, codeliste_t, altersgruppeneltern, 'id', fstat['agkv'])
        res.append(fsupd_beratungsanlass1_t)
        mksel(res, codeliste_t, beratungsanlaesse, 'id', fstat['ba1'])
        res.append(fsupd_beratungsanlass2_t)
        mksel(res, codeliste_t, beratungsanlaesse, 'id', fstat['ba2'])
        res.append(fsupd_problemkind_t)
        mksel(res, codeliste_t, problembereichekinder, 'id', fstat['pbk'])
        res.append(fsupd_problemeltern_t)
        mksel(res, codeliste_t, problembereicheeltern, 'id', fstat['pbe'])
        res.append(fsupd_problemspektrumkind_t)
        pbkids = []
        for f in fskindprobleme:
            pbkids.append(f['pbk'])
        mksel(res, codeliste_t, problembereichekinder, 'id', pbkids)
        res.append(fsupd_problemkindnot_t % fstat['no2'])
        res.append(fsupd_problemspektrumeltern_t)
        pbeids = []
        for f in fselternprobleme:
            pbeids.append(f['pbe'])
        mksel(res, codeliste_t, problembereicheeltern, 'id', pbeids)
        res.append(fsupd_problemelternnot_t % fstat['no3'])
        res.append(fsupd_massnahmen_t)
        fsleiids = []
        for f in fsleistungen:
            fsleiids.append(f['le'])
        mksel(res, codeliste_t, massnahmen, 'id', fsleiids)
        res.append(fsupd_zahlkontakte_t % fstat)
        res.append(formhiddenvalues_t % hidden)
        res.append(fsupd_notizsubmit_t % fstat )
        return string.join(res, '')
        
        ##*************************************************************************
        ##
        ## Auswahlformular zum Wählen einer zu editierenden Fachstatistik
        ##
        ## 01.10.2001 mastaleckT(msg)
        ##*************************************************************************

# wird nicht mehr verwendet
class updfsausw(Request.Request):
    permissions = Request.STAT_PERM
    def processForm(self, REQUEST, RESPONSE):
        mitarbeiterliste = self.getMitarbeiterliste()
        user = self.user
        mitarbeiter = self.mitarbeiter
        stelle = self.stelle
        stellenzeichen = get_all_codes('stzei')
        ##*************************************************************************
        ##
        ## Prüfen der Fallzugehörigkeit (Mit Fall - ID oder ohne Fall - ID)
        ##
        ## 01.10.2001 mastaleckT(msg)
        ##*************************************************************************
        if self.form.has_key('fallid'):
            fallid = self.form.get('fallid')
            try:
                fsl = FachstatistikList(where = 'fall_id = %s and mit_id = %s and stz = %s'
                                        % (fallid, mitarbeiter['id'], stelle['id']),
                                      order = 'jahr,fall_fn')
            except:
                meldung = {'titel':'Fehler',
                         'legende':'Fehlerbeschreibung',
                         'zeile1': 'Keine Fachstatistik vorhanden',
                         'zeile2':'Versuchen Sie es bitte erneut.'}
                return (meldung_t %meldung)
            fall = Fall(int(fallid))
            akte = Akte(fall['akte_id'])
            letzter_fall = akte['letzter_fall']
        else:
            if mitarbeiter['benr'] == cc('benr','bearb'):
                fsl = FachstatistikList(where = 'mit_id = %s and stz = %s'
                                        % (mitarbeiter['id'], stelle['id']),
                                        order = 'jahr,fall_fn')
            elif mitarbeiter['benr'] == cc('benr','verw'):
                fsl = FachstatistikList(where = 'stz = %s' % (stelle['id']), order = 'jahr,fall_fn')
                
        res = []
        res.append(head_normal_t %('Auswahl einer Fachstatistik'))
        res.append(thupdstausw_t)
        ges=0
        for el in fsl:
            fall = ebapi.Fall(el['fall_id'])
            akte = ebapi.Akte(fall['akte_id'])
            letzter_fall = akte['letzter_fall']
            if el['fall_fn'] == letzter_fall['fn']:
                res.append(updfsausw1_t % el)
                ges=ges+1
            else:
                pass
        if ges == 0:
            meldung = {'titel':'Fehler',
                     'legende':'Fehlerbeschreibung',
                     'zeile1': 'Keine aktuelle Fachstatistik vorhanden',
                     'zeile2': 'Versuchen Sie es bitte erneut.'}
            return (meldung_t %meldung)
            #res = []
            #res.append(head_normal_t %('Auswahl einer Fachstatistik'))
            #res.append(thupdstausw_t)
            #mksel(res, updfsausw1_t, fsl )
        res.append(updstausw2_t)
        return string.join(res, '')
        
        
        
        
        
        
        
        
        
        
        
