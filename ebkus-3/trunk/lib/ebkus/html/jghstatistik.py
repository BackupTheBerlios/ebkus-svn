# coding: latin-1
##*************************************************************************
## Projekt:       EBKuS
##
## Datei:         jghstatistik.py
##
## Beschreibung:  ...
##
## Klassen:       jghneu
##                updjgh
##                updjghausw
##*************************************************************************
##
## Revisionen:
##
## Datum:                 Autor:          Beschreibung:
##
##
##*************************************************************************

"""Module für die Jugendhilfestatistik."""

import logging
import string
from ebkus.config import config
from ebkus.app import ebapi
from ebkus.app import Request,date
from ebkus.app.ebapi import Akte, Fall, Jugendhilfestatistik, Code, \
     JugendhilfestatistikList, cc, today, check_date, Wrapper, \
     Jugendhilfestatistik2007List, Jugendhilfestatistik2007
from ebkus.app.ebupd import upgrade_jgh
from ebkus.app.ebapih import get_codes, mksel, get_all_codes
from ebkus.app_surface.standard_templates import *
from ebkus.app_surface.jgh_templates import *
from ebkus.app_surface.jgh07_templates import *



# kann auch als updjghform angesprochen werden (siehe EBKuS.py)
# wird in menu_templates.py verwendet
class jghneu(Request.Request):
    """Neue Jugendhilfestatistik eintragen. (Tabelle: Jugendhilfestatistik.)"""
    permissions = Request.STAT_PERM
    def processForm(self, REQUEST, RESPONSE):
        fallid = self.form.get('fallid')
        jghiddel = self.form.get('jghiddel')
        typ = self.form.get('typ')
        logging.info('JGHNEU %s %s %s' % (fallid, jghiddel, typ))
        if jghiddel and typ == 'jgh07' and fallid:
            logging.info('JGHNEU upgrading %s %s %s' % (fallid, jghiddel, typ))
            # neue Statistik auf alte 'upgraden'
            upgrade_jgh(jghiddel, old2new=False)
##             fall = Fall(fallid)
##             # diese Fall ist noch unzureichend initialisiert
##             jghstat = fall['jgh']
        
        if not fallid:
            meldung = {'titel':'Fehler',
                      'legende':'Fehlerbeschreibung',
                       'zeile1':'Sie d&uuml;rfen eine Bundesstatistik nur f&uuml;r einen g&uuml;ltigen Fall erstellen.',
                       'zeile2':''}
            return meldung_t % meldung
        fall = Fall(fallid)
        akte = fall['akte']
        fn = fall['fn']
        bgd = fall['bgd']
        bgm = fall['bgm']
        bgy = fall['bgy']
        ex_jgh = fall['jgh']
        if ex_jgh:
            meldung = {'titel':'Hinweis',
                     'legende':'Hinweis',
                     'zeile1':'Es ist bereits eine Jugendhilfestatistik f&uuml;r die Fallnummer vorhanden!',
                     'zeile2':''}
            return meldung_t % meldung

        alter_klient = date.calc_age(akte['gb'],fall['bgd'],fall['bgm'],fall['bgy'])
        geschwisterfaelle = get_codes('gfall')
        stellenzeichen = get_codes('stzei')
        bezirke = get_codes('rbz')
        kreise = get_codes('kr')
        gemeinde = get_codes('gm')
        gemeindeteile = get_codes('gmt')
        if config.BERLINER_VERSION:
            wohnbezirk =  get_codes('wohnbez')
        traeger = get_codes('traeg')
        beendigungsgruende = get_codes('bgr')
        geschlechter = get_codes('gs')
        altersgruppen = get_codes('ag')
        lebtbeipersonen = get_codes('fs')
        staatsangehoerigkeiten = get_codes('hke')
        erstekontaktaufnahmel = get_codes('zm')
        berschwerpunkte = get_codes('schw')
        geschwister = get_codes('gsa')
        
        hidden ={'file': 'jgheinf'}
        jghid = Jugendhilfestatistik().getNewId()
        hiddenid ={'name': 'jghid', 'value': jghid}
        hiddenid2 ={'name': 'stz', 'value': self.stelle['id']}
        mitarb_data = {'mit_id': self.mitarbeiter['id'],'mit_name' : self.mitarbeiter['ben']}
        res = []
        res.append(head_normal_t % 'Neue Bundesstatistik erstellen')
        res.append(jghstatneu_t % ({'id':fallid}))
        res.append(jghstatneufn_t  %({'fall_fn' : fn} ))
        res.append(jghstatneugemeinde_t %(Code(cc('gm','000'))['id']))
        res.append(jghstatneugemeindeteil_t %(Code(cc('gmt','000'))['id']))
        res.append(formhiddenvalues_t % hidden)
        res.append(formhiddennamevalues_t % hiddenid)
        res.append(formhiddennamevalues_t % hiddenid2)
        res.append(jghstatneumit_t % mitarb_data)
        res.append(jghstatneubeginn_t  % ({'bgd': bgd, 'bgm': bgm , 'bgy' : bgy} ))
        mksel(res, codeliste_t, bezirke)
        res.append(jghstatneuende_t %(today()))
        res.append(jghstatneukreis_t)
        mksel(res, codeliste_t, kreise)
        if config.BERLINER_VERSION:
            res.append(jghstatneuwbz_berlin_t)
            mksel(res,codeliste_t,wohnbezirk,'id',akte['wohnbez'])
            res.append(jghstatneugfall_berlin_t)
        else:
            res.append(jghstatneuwbz_t % akte['wohnbez'])
            res.append(jghstatneugfall_t)
        mksel(res,codeliste_t, geschwisterfaelle, 'name', 'Nein')
        res.append(jghstatneutraeger_t)
        mksel(res, codeliste_t, traeger)
        res.append(jghstatneukontakt_t)
        mksel(res, codeliste_t, erstekontaktaufnahmel)
        res.append(jghstatneuendegrund_t)
        mksel(res, codeliste_t, beendigungsgruende)
        res.append(jghstatneuanlass_t)
        res.append(codelisteos_t % Code(cc('ba0', '1')) )
        res.append(codelisteos_t % Code(cc('ba1', '1')) )
        res.append(codelisteos_t % Code(cc('ba2', '1')) )
        res.append(codelisteos_t % Code(cc('ba3', '1')) )
        res.append(codelisteos_t % Code(cc('ba4', '1')) )
        res.append(codelisteos_t % Code(cc('ba5', '1')) )
        res.append(codelisteos_t % Code(cc('ba6', '1')) )
        res.append(codelisteos_t % Code(cc('ba7', '1')) )
        res.append(codelisteos_t % Code(cc('ba8', '1')) )
        res.append(codelisteos_t % Code(cc('ba9', '1')) )
        res.append(jgstatneuschwerpunkt_t)
        mksel(res, codeliste_t, berschwerpunkte)
        res.append(jghstatneulebtbei_t)
        mksel(res, codeliste_t, lebtbeipersonen)
        res.append(jghstatneugeschlecht_t)
        mksel(res, codeliste_t, geschlechter)
        res.append(jghstatneualter_t)
        if(alter_klient < 3):
            altersgruppe_kat = cc('ag', '1')
        elif(alter_klient >= 3 and alter_klient < 6):
            altersgruppe_kat = cc('ag', '2')
        elif(alter_klient >= 6 and alter_klient < 9):
            altersgruppe_kat = cc('ag', '3')
        elif(alter_klient >= 9 and alter_klient < 12):
            altersgruppe_kat = cc('ag', '4')
        elif(alter_klient >= 12 and alter_klient < 15):
            altersgruppe_kat = cc('ag', '5')
        elif(alter_klient >= 15 and alter_klient < 18):
            altersgruppe_kat = cc('ag', '6')
        elif(alter_klient >= 18 and alter_klient < 21):
            altersgruppe_kat = cc('ag', '7')
        elif(alter_klient >= 21 and alter_klient < 24):
            altersgruppe_kat = cc('ag', '8')
        elif(alter_klient >= 24 and alter_klient < 27):
            altersgruppe_kat = cc('ag', '9')
        else:
            altersgruppe_kat = " "
        mksel(res, codeliste_t, altersgruppen, 'id', altersgruppe_kat)
        res.append(jghstatneu_t2a)
        res.append(jghstatneu_t2b)
        mksel(res, codeliste_t, staatsangehoerigkeiten)
        res.append(jghstatneu_t3  % Code(cc('gsu', '1')))
        res.append(radio_t % Code(cc('fbe0', '1' )) )
        res.append(jghstatneu_t4)
        res.append(radio_t % Code(cc('fbe0', '2' )) )
        res.append(jghstatneu_t5)
        res.append(radio_t % Code(cc('fbe1', '1')) )
        res.append(jghstatneu_t6)
        res.append(radio_t % Code(cc('fbe1', '2')) )
        res.append(jghstatneu_t7)
        res.append(jghansaetzefamilie_t % Code(cc('fbe2', '1')) )
        res.append(jghstatneu_t8)
        res.append(jghansaetzeumfeld_t % Code(cc('fbe3', '1')) )
        res.append(jghstatneu_t9)
        return string.join(res, '')
        
        
class updjgh(Request.Request):
    """Jugendhilfestatistik ändern. (Tabelle: Jugendhilfestatistik)"""
    
    permissions = Request.STAT_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        # Pro Fall kann es nur 1 Jugendhilfestatistik geben.
##         jghiddel = self.form.get('jghiddel')
        fallid = self.form.get('fallid')
        id = self.form.get('jghid')
##         typ = self.form.get('typ')
##         if jghiddel and typ == 'jhg07' and fallid:
##             # neue Statistik auf alte 'upgraden'
##             upgrade_jgh(jghiddel, old2new=False)
##             fall = Fall(fallid)
##             # diese Fall ist noch unzureichend initialisiert
##             jghstat = fall['jgh']
        if fallid:
            fall = Fall(fallid)
            jghstat = fall['jgh']
            if not jghstat:
                meldung = {'titel':'Hinweis',
                           'legende':'Hinweis',
                           'zeile1':'Es ist noch keine Bundesstatistik f&uuml;r den Fall vorhanden!',
                           'zeile2':''}
                return meldung_t % meldung
        elif id:
            jghstat = Jugendhilfestatistik(id)
            fallid = jghstat.get('fall_id')
            if fallid:
                fall = Fall(int(fallid))
                akte = fall['akte']
        else:
            self.last_error_message = "Keine Bundesstatistik-ID erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
            
        geschwisterfaelle = get_codes('gfall')
        stellenzeichen = get_codes('stzei')
        bezirke = get_codes('rbz')
        kreise = get_codes('kr')
        gemeinde = get_codes('gm')
        gemeindeteile = get_codes('gmt')
        if config.BERLINER_VERSION:
            wohnbezirk = get_codes('wohnbez')
        traeger = get_codes('traeg')
        beendigungsgruende = get_codes('bgr')
        geschlechter = get_codes('gs')
        altersgruppen = get_codes('ag')
        lebtbeipersonen = get_codes('fs')
        staatsangehoerigkeiten = get_codes('hke')
        erstekontaktaufnahmel = get_codes('zm')
        berschwerpunkte = get_codes('schw')
        ansaetzekind = get_codes('fbe0')
        ansaetzeeltern = get_codes('fbe1')
        ansaetzefamilie = get_codes('fbe2')
        ansaetzeumfeld = get_codes('fbe3')
        geschwister = get_codes('gsa')
        hidden ={'file': 'updjgh'}
        hiddenid ={'name': 'jghid', 'value': '%(id)d' %jghstat }
        hiddenid2 ={'name': 'stz', 'value': self.stelle['id']}
        
        res = []
        res.append(head_normal_t % 'Alte Bundesstatistik bearbeiten (bis 2006)')
        res.append(jghstatedit_t % ({'id':fallid}))
        res.append(jghstateditfn_t  %({'fall_fn' : jghstat['fall_fn']}))
        res.append(jghstateditgemeinde_t %(Code(cc('gm','000'))['id']))
        res.append(jghstateditgemeindeteil_t %(Code(cc('gmt','000'))['id']))
        res.append(formhiddenvalues_t % hidden)
        res.append(formhiddennamevalues_t % hiddenid)
        res.append(formhiddennamevalues_t % hiddenid2)
        res.append(jghstateditmit_t %{'mit_id': jghstat['mit_id'],'mit_name' : jghstat['mit_id__ben']})
        res.append(jghstateditbeginn_t  % jghstat)
        mksel(res, codeliste_t, bezirke, 'id', jghstat['rbz'])
        res.append(jghstateditende_t % jghstat )
        res.append(jghstateditkreis_t)
        mksel(res, codeliste_t, kreise, 'id', jghstat['kr'])
        if config.BERLINER_VERSION:
            res.append(jghstateditwbz_berlin_t)
            mksel(res,codeliste_t,wohnbezirk,'id',jghstat['bezirksnr'])
            res.append(jghstateditgfall_berlin_t)
        else:
            res.append(jghstateditwbz_t)
            res.append(jghstateditgfall_t)
        mksel(res,codeliste_t, geschwisterfaelle, 'id', jghstat['gfall'])
        res.append(jghstatedittraeger_t)
        mksel(res, codeliste_t, traeger, 'id', jghstat['traeg'])
        res.append(jghstateditkontakt_t)
        mksel(res, codeliste_t, erstekontaktaufnahmel, 'id', jghstat['zm'])
        res.append(jghstateditendegrund_t)
        mksel(res, codeliste_t, beendigungsgruende, 'id', jghstat['bgr'])
        res.append(jghstateditanlass_t)
        d = Code(cc('ba0', '1') )
        if jghstat['ba0'] == cc('ba0', '1'):
            d['sel'] = 'selected'
        else:
            d['sel'] = ''
        res.append(codeliste_t % d)
        d = Code(cc('ba1', '1') )
        if jghstat['ba1'] == cc('ba1', '1'):
            d['sel'] = 'selected'
        else:
            d['sel'] = ''
        res.append(codeliste_t % d)
        d = Code(cc('ba2', '1') )
        if jghstat['ba2'] == cc('ba2', '1'):
            d['sel'] = 'selected'
        else:
            d['sel'] = ''
        res.append(codeliste_t % d)
        d = Code(cc('ba3', '1') )
        if jghstat['ba3'] == cc('ba3', '1'):
            d['sel'] = 'selected'
        else:
            d['sel'] = ''
        res.append(codeliste_t % d)
        d = Code(cc('ba4', '1') )
        if jghstat['ba4'] == cc('ba4', '1'):
            d['sel'] = 'selected'
        else:
            d['sel'] = ''
        res.append(codeliste_t % d)
        d = Code(cc('ba5', '1') )
        if jghstat['ba5'] == cc('ba5', '1'):
            d['sel'] = 'selected'
        else:
            d['sel'] = ''
        res.append(codeliste_t % d)
        d = Code(cc('ba6', '1') )
        if jghstat['ba6'] == cc('ba6', '1'):
            d['sel'] = 'selected'
        else:
            d['sel'] = ''
        res.append(codeliste_t % d)
        d = Code(cc('ba7', '1') )
        if jghstat['ba7'] == cc('ba7', '1'):
            d['sel'] = 'selected'
        else:
            d['sel'] = ''
        res.append(codeliste_t % d)
        d = Code(cc('ba8', '1') )
        if jghstat['ba8'] == cc('ba8', '1'):
            d['sel'] = 'selected'
        else:
            d['sel'] = ''
        res.append(codeliste_t % d)
        d = Code(cc('ba9', '1') )
        if jghstat['ba9'] == cc('ba9', '1'):
            d['sel'] = 'selected'
        else:
            d['sel'] = ''
        res.append(codeliste_t % d)
        res.append(jgstateditschwerpunkt_t)
        mksel(res, codeliste_t, berschwerpunkte, 'id', jghstat['schw'])
        res.append(jghstateditlebtbei_t)
        mksel(res, codeliste_t, lebtbeipersonen, 'id', jghstat['fs'])
        res.append(jghstateditgeschlecht_t)
        mksel(res, codeliste_t, geschlechter, 'id', jghstat['gs'])
        res.append(jghstateditalter_t)
        mksel(res, codeliste_t, altersgruppen, 'id', jghstat['ag'] )
        if jghstat['gsu'] == cc('gsu', '1'):
            check = 'checked'
        else:
            check = ''
        if jghstat['gsa'] == None:
            gsa = ''
        else:
            gsa = jghstat['gsa']
            # msgsystems 02.07.2002
        res.append(jghstatedit_t2a %gsa)
        #mksel(res, codeliste_t, geschwister, 'id', gsa)
        res.append(jghstatedit_t2b % ({'gsa': gsa ,'gsu': cc('gsu', '1'), 'check': check }))
        mksel(res, codeliste_t, staatsangehoerigkeiten, 'id', jghstat['hke'])
        res.append(jghstatedit_t3 % ({'gsa': gsa ,'gsu': cc('gsu', '1'), 'check': check }))
        #####
        if jghstat['fbe0'] == cc('fbe0', '1'):
            res.append(radiocheck_t % Code(cc('fbe0', '1')) )
        else:
            res.append(radio_t % Code(cc('fbe0', '1')) )
        res.append(jghstatedit_t4)
        if jghstat['fbe0'] == cc('fbe0', '2'):
            res.append(radiocheck_t % Code(cc('fbe0', '2')) )
        else:
            res.append(radio_t % Code(cc('fbe0', '2')) )
        res.append(jghstatedit_t5)
        if jghstat['fbe1'] == cc('fbe1', '1'):
            res.append(radiocheck_t % Code(cc('fbe1', '1')) )
        else:
            res.append(radio_t % Code(cc('fbe1', '1')) )
        res.append(jghstatedit_t6)
        if jghstat['fbe1'] == cc('fbe1', '2'):
            res.append(radiocheck_t % Code(cc('fbe1', '2')) )
        else:
            res.append(radio_t % Code(cc('fbe1', '2')) )
        res.append(jghstatedit_t7)
        if jghstat['fbe2'] == cc('fbe2', '1'):
            res.append(jghansaetzefamiliecheck_t % Code(cc('fbe2', '1')) )
        else:
            res.append(jghansaetzefamilie_t % Code(cc('fbe2', '1')) )
        res.append(jghstatedit_t8)
        if jghstat['fbe3'] == cc('fbe3', '1'):
            res.append(jghansaetzeumfeldcheck_t % Code(cc('fbe3', '1')) )
        else:
            res.append(jghansaetzeumfeld_t % Code(cc('fbe3', '1')) )
        res.append(jghstatedit_t9)
        return string.join(res, '')

def mkselstr(template, liste, field, value=None):
    res = []
    mksel(res, template, liste, field, value)
    return ''.join(res)

class _jgh07(Request.Request):
    """Gemeinsame Klasse für die neue Bundesstatistik"""
    def _formular(self, jgh):
        """Bringt Templates und Daten zusammen sowohl für die Neueinführung
        als auch für das Update.
        """
        jgh['gm'] = ''
        jgh['gmt'] = ''
        jgh['rbz_sel'] = ''#mkselstr(codeliste_t, get_codes('rbz'), 'id', jgh['rbz'])
        jgh['kr_sel'] = ''#mkselstr(codeliste_t, get_codes('kr'), 'id', jgh['kr'])
        jgh['gfall_sel'] = ''#mkselstr(codeliste_t, get_codes('gfall'), 'id', jgh['gfall'])
        jgh['shf_sel'] = mkselstr(codeliste_t, get_codes('shf'), 'id', jgh['sit_fam'])
        #jgh['jghid'] = 
        #jgh['stz'] =         
        #jgh['file'] =
##         for k,v in jgh.items():
##             print k, v
##         print jgh.data
##         print '_______________________________'
##         print jgh.obj.data
        res = []
        res.append(head_normal_t % 'Bundesstatistik bearbeiten')
        res.append(jghhead_t % jgh)
        res.append(jghfalldaten_t % jgh)
        res.append(jghpersonendaten_t % jgh)
        res.append(jghbuttons_t) 
        res.append(jghfoot_t) 
        return ''.join(res)




class updjgh07(_jgh07):
    """Jugendhilfestatistik ändern. (Tabelle: Jugendhilfestatistik)"""
    
    permissions = Request.STAT_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        # Pro Fall kann es nur 1 Jugendhilfestatistik geben.
##         jghiddel = self.form.get('jghiddel')
        fallid = self.form.get('fallid')
        id = self.form.get('jghid')
##         typ = self.form.get('typ')
##         if jghiddel and typ == 'jhg' and fallid:
##             # alte Statistik auf neue upgraden
##             upgrade_jgh(jghiddel, old2new=True)
##             fall = Fall(fallid)
##             jghstat = fall['jgh']
        if fallid:
            fall = Fall(fallid)
            jghstat = fall['jgh']
            if not jghstat:
                meldung = {'titel':'Hinweis',
                           'legende':'Hinweis',
                           'zeile1':'Es ist noch keine Bundesstatistik f&uuml;r den Fall vorhanden!',
                           'zeile2':''}
                return meldung_t % meldung
        elif id:
            jghstat = Jugendhilfestatistik2007(id)
            fallid = jghstat.get('fall_id')
            if fallid:
                fall = Fall(int(fallid))
                akte = fall['akte']
        else:
            self.last_error_message = "Keine Bundesstatistik-ID erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
        jghstat['jghid'] = jghstat['id']
        jghstat['file'] = 'updjgh07'
        return self._formular(jghstat)
        
class jgh07neu(_jgh07):
    """Neue Jugendhilfestatistik eintragen. (Tabelle: Jugendhilfestatistik.)"""
    permissions = Request.STAT_PERM
    def processForm(self, REQUEST, RESPONSE):
        fallid = self.form.get('fallid')
        jghiddel = self.form.get('jghiddel')
        typ = self.form.get('typ')
        if jghiddel and typ == 'jgh' and fallid:
            # alte Statistik auf neue upgraden
            upgrade_jgh(jghiddel, old2new=True)
        if not fallid:
            meldung = {'titel':'Fehler',
                      'legende':'Fehlerbeschreibung',
                       'zeile1':'Sie d&uuml;rfen eine Bundesstatistik nur f&uuml;r einen g&uuml;ltigen Fall erstellen.',
                       'zeile2':''}
            return meldung_t % meldung
        fall = Fall(fallid)
        ex_jgh = fall['jgh']
        if ex_jgh:
            meldung = {'titel':'Hinweis',
                     'legende':'Hinweis',
                     'zeile1':
                       'Es ist bereits eine Jugendhilfestatistik f&uuml;r die Fallnummer vorhanden!',
                     'zeile2':''}
            return meldung_t % meldung
        jgh = Jugendhilfestatistik2007()
        jgh['jghid'] = Jugendhilfestatistik2007().getNewId()
        jgh['stz'] = self.stelle['id']
        jgh['file'] = 'jgh07einf'
        jgh['mit_id'] = self.mitarbeiter['id']
        jgh.setDate('bg', fall.getDate('bg'))
        jgh['fall_fn'] = fall['fn']
        jgh['fall_id'] = fall['id']
        # defaults
        jgh.setDate('e', today())
        jgh['sit_fam'] = cc('shf', '5') # unbekannt
        return self._formular(jgh)
        

class jgh_check(Request.Request):
    """Ziel aller "Speichern"-Vorgänge für JGH-Statistiken.
    """
    permissions = Request.STAT_PERM
    def processForm(self, REQUEST, RESPONSE):
        fallid = self.form.get('fallid')
        fall = Fall(fallid)
        file = self.form.get('file')
        # diese Statistik wird evt. gelöscht falls das Endedatum
        # nicht passt
        jghiddel = ''
        jgh = fall['jgh']
        if jgh:
            jghiddel = jgh['id']
            
        beginn = check_date(self.form, 'bg', "Fehler im Datum für den Beginn",
                                nodayallowed=True)
        ende = check_date(self.form, 'e', "Fehler im Datum für das Ende",
                                nodayallowed=True)
        # uns interessieren zwei Zustände:
        # für beide gilt Beginn ist 2006 oder früher
        # 1. alte Statistik und Ende 2007 oder später
        # 2. neue Statistik und Ende 2006 oder früher
        # In allen anderen Fällen wird direkt an die Klientenkarte weitergereicht.
        if beginn.year <= 2006 and fall['aktuell']:
            if ende.year <= 2006 and file in ('jgh07einf', 'updjgh07'):
                assert (file == 'updjgh07' and jghiddel or
                        file == 'jgh07einf' and not jghiddel)
                return self._ask(fallid, 'jghneu', jghiddel, 'jgh07', ende.year)
            if ende.year >= 2007 and file in ('jgheinf', 'updjgh'):
                assert (file == 'updjgh' and jghiddel or
                        file == 'jgheinf' and not jghiddel)
                return self._ask(fallid, 'jgh07neu', jghiddel, 'jgh', ende.year)
        # es handelt sich um einen POST-Request, mit redirect
        # kommen wir hier nicht weiter
        from ebkus.html.klientenkarte import klkarte
        self.__class__ = klkarte
        return klkarte.processForm(self, REQUEST, RESPONSE)

    def _ask(self, fallid, welche, jghiddel, typ, jahr):
        if typ == 'jgh07':
            z1 = "Das Endedatum %s passt nicht zur neuen Bundesstatistik (ab 2007)." % jahr
            z2 = "Wollen Sie die neue Bundesstatistik durch die alte ersetzen?"
        else:
            z1 = "Das Endedatum %s passt nicht zur alten Bundesstatistik (bis 2006)." % jahr
            z2 = "Wollen Sie die alte Bundesstatistik durch die neue ersetzen?"
            
        # alte Statistik vorhanden
        d = {
            'titel': 'Bundesstatistik ersetzen',
            'legende': 'Bundesstatistik ersetzen?',
            'action': welche,
            'zeile1': z1,
            'zeile2': z2,
            'n1': 'fallid', 'v1': fallid,
            'n2': 'jghiddel', 'v2': jghiddel,
            'n3': 'typ', 'v3': typ,
            }
        meldung = jgh_ueberschreiben_ja_nein_t % d
        return meldung

# Wird nicht mehr verwendet        
class updjghausw(Request.Request):
    """Auswahl der Jugendhilfestatistik zum Ändern.
    (Tabelle: Jugendhilfestatistik)"""
    
    permissions = Request.STAT_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        user = self.user
        stelle = self.stelle
        stellenzeichen = get_all_codes('stzei')
        fallid = self.form.get('fallid')
        mitarbeiter = self.mitarbeiter
        
        if fallid:
            jgh = JugendhilfestatistikList(where = 'fall_id = %s and mit_id = %s and stz = %s'
                                           % (fallid, mitarbeiter['id'], stelle['id']),
                                     order = 'ey,fall_fn')
            if len(jgh) != 1:
                meldung = {'titel':'Fehler',
                         'legende':'Fehlerbeschreibung',
                         'zeile1': "%s Jugendhilfestatistik(en) f&uuml; diesen Fall erhalten" % len(jgh),
                         'zeile2':'Versuchen Sie es bitte erneut.'}
                return (meldung_t % meldung)
            fall = Fall(int(fallid))
            akte = Akte(fall['akte_id'])
            letzter_fall = akte['letzter_fall']
            
        else:
            if mitarbeiter['benr'] == cc('benr','bearb'):
                jgh = JugendhilfestatistikList(where = 'mit_id = %s and stz = %s'
                                       % (mitarbeiter['id'], stelle['id']),
                                       order = 'ey,fall_fn')
            elif mitarbeiter['benr'] == cc('benr','verw'):
                jgh = JugendhilfestatistikList(where = 'stz = %s' % (stelle['id']), order = 'ey,fall_fn')
                
                # Headerblock, Menue u. Uberschrift fuer das HTML-Template
                
        if fallid:
            legendtext = {'legendtext':
                      "Bundesstatistik f&uuml;r Fallnr.: %(fn)s / Klient: %(akte_id__vn)s, %(akte_id__na)s ausw&auml;hlen"
                      % fall}
        else:
            legendtext = {'legendtext': "Bundesstatistik zum &Auml;ndern ausw&auml;hlen"}
            
            # Liste der Templates als String
        res = []
        res.append(head_normal_t % 'Auswahl einer Bundesstatistik')
        res.append(thupdstausw_t % legendtext)
        ges=0
        for el in jgh:
            fall = ebapi.Fall(el['fall_id'])
            akte = ebapi.Akte(fall['akte_id'])
            letzter_fall = akte['letzter_fall']
            if el['fall_fn'] == letzter_fall['fn']:
                res.append(updjghausw1_t % el)
                ges=ges+1
            else:
                pass
        if ges == 0:
            meldung = {'titel':'Fehler',
                     'legende':'Fehlerbeschreibung',
                     'zeile1': 'Keine aktuelle Jghstatistik vorhanden',
                     'zeile2': 'Versuchen Sie es bitte erneut.'}
            return meldung_t % meldung
            
            #res = []
            #res.append(head_normal_t % 'Auswahl einer Bundesstatistik')
            #res.append(thupdstausw_t % legendtext)
            #mksel(res, updjghausw1_t, jgh )
        res.append(updstausw2_t)
        return string.join(res, '')
        
        
        
        
        
        
        
