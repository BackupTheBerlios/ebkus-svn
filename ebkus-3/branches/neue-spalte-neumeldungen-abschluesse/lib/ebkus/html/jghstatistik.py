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

import string
from ebkus.config import config
from ebkus.app import ebapi
from ebkus.app import Request,date
from ebkus.app.ebapi import Akte, Fall, Jugendhilfestatistik, Code, JugendhilfestatistikList, cc, today
from ebkus.app.ebapih import get_codes, mksel, get_all_codes
from ebkus.app_surface.standard_templates import *
from ebkus.app_surface.jgh_templates import *

# kann auch als updjghform angesprochen werden (siehe EBKuS.py)
# wird in menu_templates.py verwendet
class jghneu(Request.Request):
    """Neue Jugendhilfestatistik eintragen. (Tabelle: Jugendhilfestatistik.)"""
    permissions = Request.STAT_PERM
    def processForm(self, REQUEST, RESPONSE):
        mitarbeiterliste = self.getMitarbeiterliste()
        user = self.user
        fallid = self.form.get('fallid')
        
        if not fallid:
            res = []
            meldung = {'titel':'Fehler',
                      'legende':'Fehlerbeschreibung',
                       'zeile1':'Sie d&uuml;rfen eine Bundesstatistik nur f&uuml;r einen g&uuml;ltigen Fall erstellen.',
                       'zeile2':''}
            res.append(meldung_t % meldung)
            return string.join(res, '')
            
        fall = Fall(int(fallid))
        akte = fall['akte']
        letzter_fall = akte['letzter_fall']
        fn = fall['fn']
        bgd = fall['bgd']
        bgm = fall['bgm']
        bgy = fall['bgy']
        alter_klient = date.calc_age(akte['gb'],letzter_fall['bgd'],letzter_fall['bgm'],letzter_fall['bgy'])
        
        jahresl = ebapi.JugendhilfestatistikList(where = "fall_fn = '%s'" % letzter_fall['fn'])
        if jahresl:
            res = []
            meldung = {'titel':'Hinweis',
                     'legende':'Hinweis',
                     'zeile1':'Es ist bereits eine Jugendhilfestatistik f&uuml;r die Fallnummer vorhanden!',
                     'zeile2':''}
            res.append(meldung_t % meldung)
            return string.join(res, '')
            
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
        mitarbeiterliste = self.getMitarbeiterliste()
        user = self.user
        fallid = self.form.get('fallid')
        id = self.form.get('jghid')
        
        # Pro Fall kann es nur 1 Jugendhilfestatistik geben.
        if fallid:
            fall = Fall(int(fallid))
            akte = fall['akte']
            jghstatl = fall['jgh_statistiken']
            letzter_fall = akte['letzter_fall']
            if not jghstatl:
                meldung = {'titel':'Hinweis',
                           'legende':'Hinweis',
                           'zeile1':'Es ist noch keine Bundesstatistik f&uuml;r den Fall vorhanden!',
                           'zeile2':''}
                return meldung_t % meldung
            jghstat = jghstatl[0]
        elif id:
            jghstat = Jugendhilfestatistik(int(id))
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
        res.append(head_normal_t % 'Bundesstatistik bearbeiten')
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
        
# Wird nicht mehr verwendet        
class updjghausw(Request.Request):
    """Auswahl der Jugendhilfestatistik zum Ändern.
    (Tabelle: Jugendhilfestatistik)"""
    
    permissions = Request.STAT_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        mitarbeiterliste = self.getMitarbeiterliste()
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
                return (meldung_t %meldung)
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
            return (meldung_t %meldung)
            
            #res = []
            #res.append(head_normal_t % 'Auswahl einer Bundesstatistik')
            #res.append(thupdstausw_t % legendtext)
            #mksel(res, updjghausw1_t, jgh )
        res.append(updstausw2_t)
        return string.join(res, '')
        
        
        
        
        
        
        
