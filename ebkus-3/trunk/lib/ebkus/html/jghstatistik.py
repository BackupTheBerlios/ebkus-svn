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

import re
import logging
import string
from ebkus.config import config
from ebkus.app import ebapi
from ebkus.app import Request
from ebkus.app.ebapi import Akte, Fall, Jugendhilfestatistik, Code, \
     JugendhilfestatistikList, cc, cn, today, EE, check_date, calc_age, \
     Jugendhilfestatistik2007List, Jugendhilfestatistik2007, \
     BezugspersonList
from ebkus.app.ebupd import upgrade_jgh
from ebkus.app.ebapih import get_codes, mksel, get_all_codes
from ebkus.app.gemeindeschluessel import get_gemeindeschluessel
from ebkus.app_surface.standard_templates import *
from ebkus.app_surface.jgh_templates import *
from ebkus.app_surface.jgh07_templates import *

import ebkus.html.htmlgen as h
from ebkus.html.akte_share import akte_share


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
            raise EE('Bundesstatistik nur f&uuml;r einen g&uuml;ltigen Fall')
        fall = Fall(fallid)
        akte = fall['akte']
        fn = fall['fn']
        bgd = fall['bgd']
        bgm = fall['bgm']
        bgy = fall['bgy']
        ex_jgh = fall['jgh']
        if ex_jgh:
            raise EE('Bundesstatistik bereits vorhanden')
        alter_klient = calc_age(akte['gb'],fall.getDate('bg'))
        geschwisterfaelle = get_codes('gfall')
        stellenzeichen = get_codes('stzei')
        bezirke = get_codes('rbz')
        kreise = get_codes('kr')
        gemeinde = get_codes('gm')
        gemeindeteile = get_codes('gmt')
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
        res.append(head_normal_ohne_help_t % 'Neue Bundesstatistik erstellen')
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
            res.append(jghstatneugfall_berlin_t)
        else:
            res.append(jghstatneuwbz_t)
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
        
        
# kann auch als updjghform angesprochen werden (siehe EBKuS.py)
# wird in menu_templates.py verwendet
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
            if jghstat:
                # Von menu aus kann ein update der Bundesstatistik angefordert
                # werden, ohne zu spezifizieren ob alte oder neue.
                # Das wird hier abgefangen.
                if isinstance(jghstat, Jugendhilfestatistik2007):
                    return self.ebkus.dispatch('updjgh07', REQUEST, RESPONSE)
            else:
                raise EE('Noch keine Bundesstatistik f&uuml;r den Fall vorhanden.')
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
        res.append(head_normal_ohne_help_t % 'Alte Bundesstatistik bearbeiten (bis 2006)')
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
    """value entscheidet, welcher Wert selected ist.
    Falls value nicht None ist und in liste vorkommt, ist er selected.
    Falls value None ist, ist kein Wert selected.
    Falls value ' ' ist, wird eine leere Option als erstes in die Optionliste
    eingefügt.
    """
    if value not in (None, ' ', ''):
        #print value, [code['code'] for code in liste]
        assert value in [code['id'] for code in liste]
    res = []
    if value in (' ', ''):
        res.append('<option value=" " selected> </option>')
    mksel(res, template, liste, field, value)
    return ''.join(res)

def split_option_name(name, size):
    """Return list of strings smaller than size.

    Alle Strings außer dem ersten sind mit &nbsp; eingerückt.
    """
    assert size > 10 # sonst nicht sinnvoll
    if len(name) <= size:
        return [name]
    words = name.split()
    res = []
    curr_size = 0
    curr_el = []
    first = True
    for w in words:
        new_size = curr_size + len(w)
        if new_size <= size:
            curr_el.append(w)
            curr_size = new_size
        else:
            res.append(' '.join(curr_el))
            curr_size = len(w)
            curr_el = [('&nbsp;'*4) + w] # einrücken
            if first:
                # damit eingerückt werden kann
                size -= 4
                first = False
    res.append(' '.join(curr_el))
    return res
                
    
def make_option_list(code_list, selected=None, no_empty_option=False):
    """Liefert eine Liste von Option-Elementen (Liste von Strings).
    
    selected entscheidet, welcher Wert selected ist.
    Falls selected die id eines Wertes in code_list ist, ist der selected.
    Falls selected None ist, ist kein Wert selected.
    Falls selected ' ' ist, ist die leere Option selected.
    Falls selected 'first' ist, ist der erste code selected.
    Falls add_empty False ist, wird keine leere Option eingefügt.
    """
    max_size = 60
    option = '\n<option value="%(id)s" %(sel)s >%(name)s</option>'
    res = []
    selected_values = ()

    if not no_empty_option:
        if selected in ('', ' '):
            res.append('<option value=" " selected> </option>')
        else:
            res.append('<option value=" "> </option>')
    if selected:
        if selected == 'first' and code_list:
            selected = code_list[0]['id']
        if not isinstance(selected, (tuple, list)):
            selected_values = (selected,)
    for c in code_list:
        sel = c['id'] in selected_values and 'selected' or ''
        if len(c['name']) > max_size:
            name_list = split_option_name(c['name'], max_size)
            for n in name_list:
                res.append(option % {'name': n, 'id': c['id'], 'sel': sel})
                # nur erste option selektieren
                if sel:
                    sel = ''
        else:
            c['sel'] = sel
            res.append(option % c)
            del c['sel']
    return res

_fb_data = (
    {'abschnitt': 'A',
     'title': 'Beginn der Hilfegewährung',
     'items_data': ({'frage': 'Monat (der Einleitung der Hilfe)',
                     'typ': ('int', 1, 12,),
                     'name': 'bgm',
                     'readonly': True,
                     },
                    {'frage': 'Jahr',
                     'typ': ('int', 1970, 2030,),
                     'name': 'bgy',
                     'readonly': True,
                     },
                    {'frage': 'Übernahme von einem anderen Jugendamt wegen Zuständigkeitswechsels',
                     'typ': ('checkbox','1', ' '),
                     'name': 'zustw',
                     },
                    ),
     }, 
    {'abschnitt': 'B',
     'title': 'Art der Hilfe',
     'items_data': ({'frage': 'Art der Hilfe',
                'typ': ('kat', 'hilf_art',),
                'name': 'hilf_art',
                'default': ' '
                },
               ),
     }, 
    {'abschnitt': 'C',
     'title': 'Ort der Durchführung',
     'items_data': ({'frage': '(Hauptsächlicher) Ort der Durchführung',
                'typ': ('kat', 'hilf_ort',),
                'name': 'hilf_ort',
                'default': '06',
                'no_empty_option': True,     
                },
               ),
     },
    {'abschnitt': 'D',
     'title': 'Träger',
     'items_data': ({'frage': 'Träger der Einrichtung oder des Dienstes, die/der die Hilfe/Beratung durchführt',
                'typ': ('kat', 'traeger',),
                'name': 'traeger',
                'default': '10',
                'no_empty_option': True,     
                },
               ),
     }, 
    {'abschnitt': 'E',
     'title': 'Geschlecht und Alter',
     'items_data': ({'frage': 'Geschlecht',
                     'typ': ('kat', 'gs',),
                     'name': 'gs',
                     'size': '3',
                     'readonly': True,
                     'default': ' '
                },
##     {'frage': 'Geschlecht',
##                 'typ': ('kat', 'gs',),
##                 'name': 'gs',
##                 'default': ' '
##                 },
               {'frage': 'Geburtsmonat',
                'typ': ('int', 1, 12,),
                'name': 'gem',
                'default': ' '
                },
               {'frage': 'Geburtsjahr',
                'typ': ('int', 1970, 2030,),
                'name': 'gey',
                'default': ' '
                },
               ),
     }, 
    {'abschnitt': 'F',
     'title': 'Lebenssituation bei Beginn der Hilfe',
     'items_data': ({'frage': 'Aufenthaltsort vor der Hilfe',
                'typ': ('kat', 'auf_ort',),
                'name': 'aort_vor',
                'default': ' '
                },
               {'frage': 'Situation in der Herkunftsfamilie',
                'typ': ('kat', 'shf',),
                'name': 'sit_fam',
                'default': ' '
                },
               'Migrationshintergrund',
               {'frage': 'Ausländische Herkunft mindestens eines Elternteils (nicht: Staatsangehörigkeit)',
                'typ': ('kat', 'ja_ne_un',),
                'name': 'ausl_her',
                'default': ' '
                },
               {'frage': 'In der Familie wird vorrangig deutsch gesprochen',
                'typ': ('kat', 'ja_ne_un',),
                'name': 'vor_dt',
                'default': ' '
                },
               'Wirtschaftliche Situation',
               {'frage': 'Die Herkunftsfamilie bzw. der/die junge Volljährige \
lebt teilweise oder ganz von Arbeitslosengeld II (SGB II), bedarfsorientierter \
Grundsicherung im Alter und bei Erwerbsminderung oder Sozialhilfe (SGB XII)',
                'typ': ('kat', 'ja_ne_un',),
                'name': 'wirt_sit',
                'default': ' '
                },
               ),
     }, 
    {'abschnitt': 'G',
     'title': 'Anregende Institution oder Person',
     'items_data': ({'frage': 'Diese aktuelle Hilfe/Beratung anregende(n) Institution(en) oder Person(en)',
                     'typ': ('kat', 'aip',),
                     'name': 'aip',
                     'default': ' '
                     },
                    ),
     }, 
    {'abschnitt': 'H',
     'title': 'Familien- und vormundschafts-richterliche Entscheidungen',
     'items_data': ({'frage': 'Teilweiser oder vollständiger Entzug der elterlichen Sorge (nach §1666 BGB)',
                     'typ': ('kat', 'ja_nein',),
                     'name': 'ees',
                     'default': '2',
                     'no_empty_option': True,     
                     },
                    {'frage': 'Verfahrensaussetzung nach §52 FGG',
                     'typ': ('kat', 'ja_nein',),
                     'name': 'va52',
                     'default': '2',
                     'no_empty_option': True,     
                     },
                    {'frage': 'Richterliche Genehmigung für eine Unterbringung, die mit einem Freiheitsentzug verbunden ist (nach §1631b BGB)',
                     'typ': ('kat', 'ja_nein',),
                     'name': 'rgu',
                     'default': '2',
                     'no_empty_option': True,     
                     },
                    ),
     },
    {'abschnitt': 'I',
     'title': 'Hilfe dauert an',
     'items_data': ({'frage': 'Hilfe/Beratung dauert am Jahresende an',
                     'typ': ('kat', 'ja_nein',),
                     'name': 'hda',
                     'default': ' '
                     },
                    ),
     }, 
    {'abschnitt': 'J',
     'title': 'Intensität der andauernden Hilfe',
     'items_data': ('(Nur ausfüllen, falls die Hilfe/Beratung am Jahresende andauert)',
                    {'frage': 'Zahl der Beratungskontakte im abgelaufenen Kalenderjahr',
                     'typ': ('int', 1, 999,),
                     'name': 'nbkakt',
                     'default': ' ',
                     'extra': (config.BERATUNGSKONTAKTE and 
                               'Falls leer, wird die aus den Beratungskontakten berechnete Anzahl eingesetzt.' or 
                               'Mindestens 1 Kontakt angeben'),
                     },
                    ),
     }, 
    {'abschnitt': 'K',
     'title': 'Gründe für die Hilfegewährung',
     # Die Beispiele für die Gründe stehen hier, weil im Datenbankschema für die Tabelle code,
     # wo sie eigentlich stehen sollen, für das Feld name nur 160 Zeichen vorgesehen sind.
     'gruende_bsp': {'10':"(z.B. Ausfall der Bezugspersonen wegen Krankheit, stationärer Unterbringung, Inhaftierung, Tod; unbegleitet eingereiste Minderjährige)",
                 '11':"(z.B. soziale, gesundheitliche, wirtschaftliche Probleme)",
                 '12':"(z.B. Vernachlässigung, körperliche, psychische, sexuelle Gewalt in der Familie)",
                 '13':"(z.B. Erziehungsunsicherheit, pädagogische Überforderung, unangemessene Verwöhnung)",
                 '14':"(z.B. psychische Erkrankung, Suchtverhalten, geistige oder seelische Behinderung)",
                 '15':"(z.B. Partnerkonflikte, Trennung und Scheidung, Umgangs-/Sorgerechtsstreitigkeiten, Eltern-/Stiefeltern-Kind-Konflikte, migrationsbedingte Konfliktlagen)",
                 '16':"(z.B. Gehemmtheit, Isolation, Geschwisterrivalität, Weglaufen, Aggressivität, Drogen-/Alkoholkonsum, Delinquenz/Straftat)",
                 '17':"(z.B. Entwicklungsrückstand, Ängste, Zwänge, selbst verletzendes Verhalten, suizidale Tendenzen)",
                 '18':"(z.B. Schwierigkeiten mit Leistungsanforderungen, Konzentrationsprobleme (ADS, Hyperaktivität), schulvermeidendes Verhalten (Schwänzen), Hochbegabung)",
                 '19':"",
                 },

     },
    'Ab hier bitte nur dann ausfüllen, falls die Hilfe/Beratung beendet ist.',
    {'abschnitt': 'L',
     'title': 'Ende der Hilfe/Beratung',
     'items_data': ({'frage': 'Monat',
                     'typ': ('int', 1, 12,),
                     'name': 'em',
                     },
                    {'frage': 'Jahr',
                     'typ': ('int', 1970, 2030,),
                     'name': 'ey',
                     },
                    ),
     }, 
    {'abschnitt': 'M',
     'title': 'Betreuungsintensität der beendeten Hilfe/Beratung',
     'items_data': ({'frage': 'Zahl der Beratungskontakte während der gesamten Beratungsdauer',
                     'typ': ('int', 1, 999,),
                     'name': 'nbkges',
                     'default': ' ',
                     'extra': (config.BERATUNGSKONTAKTE and 
                               'Falls leer, wird die aus den Beratungskontakten berechnete Anzahl eingesetzt.' or 
                               'Mindestens 1 Kontakt angeben'),
                     },
                    {'frage': 'Letzter Beratungskontakt liegt mehr als sechs Monate zurück',
                     'typ': ('kat', 'ja_nein',),
                     'name': 'lbk6m',
                     'default': ' '
                     },
                    ),
     },
    {'abschnitt': 'N',
     'title': 'Grund für die Beendigung der Hilfe/Beratung',
     'items_data': ({'frage': 'Grund für die Beendigung der Hilfe/Beratung',
                     'typ': ('kat', 'grende',),
                     'name': 'grende',
                     'default': ' '
                     },
                    ),
     }, 
    {'abschnitt': 'O',
     'title': 'Anschließender Aufenthalt',
     'items_data': ({'frage': 'Anschließender Aufenthalt',
                     'typ': ('kat', 'auf_ort',),
                     'name': 'aort_nac',
                     'default': ' '
                     },
                    ),
     }, 
    {'abschnitt': 'P',
     'title': 'Unmittelbar nachfolgende Hilfe',
     'items_data': ({'frage': 'Unmittelbar nachfolgende Hilfe',
                     'typ': ('kat', 'unh',),
                     'name': 'unh',
                     'default': ' '
                     },
                    ),
     }, 
    )

class _jgh07(Request.Request, akte_share):
    """Gemeinsame Klasse für die neue Bundesstatistik"""
    def _formular(self, jgh):
        """Bringt Templates und Daten zusammen sowohl für die Neueinführung
        als auch für das Update.
        """
        jgh['land_sel'] = self.for_land_kr_einrnr('land')
        jgh['kr_sel'] = self.for_land_kr_einrnr('kr')
        jgh['einrnr_sel'] = self.for_land_kr_einrnr('einrnr')
##         jgh['land_sel'] = ''.join(make_option_list(get_codes('land'), 'first', True))
##         jgh['kr_sel'] = ''.join(make_option_list(get_codes('kr'), 'first', True))
##         jgh['einrnr_sel'] = ''.join(make_option_list(get_codes('einrnr'), 'first', True))
        jgh['gfall_sel'] = ''.join(make_option_list(get_codes('gfall'), 'first', True))
        if jgh.get('lnr'):
            jgh['laufendenr'] = jgh['lnr']
        else:
            jgh['laufendenr'] = 'noch nicht vergeben'
        # wohnung außerhalb
        plz = ort = ags = ''
        ags_plz_ort = get_ags_plz_ort_if_wohnort_ausserhalb(jgh)
        if ags_plz_ort:
            ags, plz, ort = ags_plz_ort
        if ags:
            jgh['ags'] = "(AGS: %s)" % ags
        else:
            jgh['ags'] = ''
        jgh['plz'], jgh['ort'] = plz, ort
        res = []
        res.append(jghhead_t % jgh)
        res.append(jghfalldaten_t % jgh)
        res.append(fb_abschnitt_trenner_t)
        res.append(fb_abschnitt_trenner_t.join(
            [self._abschnitt(a, jgh) for a in _fb_data]))
        res.append(fb_abschnitt_trenner_t)
        res.append(jghbuttons_t) 
        res.append(jghfoot_t)
        fall = jgh['fall']
        if fall:
            klkarte_url = 'klkarte?akid=%(akte_id)s' % fall
        else:
            klkarte_url = ''
        return h.Page(
            title='Bundesstatistik bearbeiten',
            help=False,
            breadcrumbs = (('Hauptmenü', 'menu'),
                           ('Klientenkarte', klkarte_url),
                           ),
            rows=res
            ).display()

    def _abschnitt(self, data, jgh):
        if isinstance(data, basestring):
            return fb_zwischenueberschrift_t % data
        abschnitt = data.copy()
        if abschnitt['abschnitt'] == 'K':
            # besondere Behandlung
            items = self._items_fuer_K(jgh, abschnitt['gruende_bsp'])
        else:
            items = [self._item(i, jgh) for i in data['items_data']]
        abschnitt['items'] = fb_item_trenner_t.join(items)
        return fb_abschnitt_t % abschnitt

    def _items_fuer_K(self, jgh, gruende_bsp):
        res = []
        res.append(fb_k_header_t)
        codes = get_codes('gruende')
        for c in codes:
            id = c['id']
            code = c['code']
            bsp = gruende_bsp[code]
            name = c['name']
            if bsp:
                frage = "%s<br>%s" % (name, bsp)
            else:
                frage = name
            item = {'frage': frage,
                    'id': id,
                    'ch1': jgh.get('gr1') == id and 'checked' or '',
                    'ch2': jgh.get('gr2') == id and 'checked' or '',
                    'ch3': jgh.get('gr3') == id and 'checked' or '',
                    }
            if code == '19':
                res.append(fb_k_last_item_t % item)
            else:
                res.append(fb_k_item_t % item)
        return res
    def _item(self, data, jgh):
        if isinstance(data, basestring):
            return fb_zwischenueberschrift_t % data
        assert isinstance(data, dict)
        item = data.copy()
        label = item['typ'][0]
        if label == 'kat':
            kat_code = item['typ'][1]
            name = item['name']
            default = jgh.get(name)
            if name == 'gs': # Geschlecht readonly
                # Wert muss da sein! Nur für Geschlecht gedacht.
                item['value'] = Code(jgh[name])['name']
                item['name'] = '' # readonly feld
                item['ro'] = 'readonly'
                item['tip'] = ''
                return fb_text_item_t % item
            if default == None:
                default = item.get('default')
                if default and default != ' ':
                    default = cc(kat_code, default)
            codes = get_codes(kat_code)
            #item['options'] = mkselstr(fb_option_t, codes, 'id', default)
            no_empty_option = item.get('no_empty_option')
            item['options'] = ''.join(make_option_list(codes, default, no_empty_option))
            maxl = max([len(c['name']) for c in codes])
            if maxl < 60:
                w = "%sem" % max(maxl, 3)
            else:
                w = "100%"
            item['width'] = w
            if name == 'hda':
                item['onChange'] = """onChange="del_anzahl_kontakte('%s', '%s')" """ % \
                                   (cn('ja_nein', 'ja'), cn('ja_nein', 'nein'))
            else:
                item['onChange'] = ''
            return fb_select_one_item_t % item
        elif label == 'int':
            minl, maxl = item['typ'][1:3]
            item['size'] = len(str(maxl))
            name = item['name']
            default = jgh.get(name)
            if default == None:
                default = item.get('default')
                if default == None:
                    default = ''
            item['value'] = default
            if item.get('readonly'):
                item['ro'] = 'readonly'
            else:
                item['ro'] = ''
            extra = item.get('extra')
            if extra:
                item['tip'] = tip_t % {'tip': extra}
            else:
                item['tip'] = ''
            return fb_int_item_t % item
        elif label == 'checkbox':
            name = item['name']
            value = jgh.get(name)
            item['value'] = '1'
            item['checked'] = (value == '1' and 'checked' or '')
            return fb_checkbox_item_t % item
        else:
            return ''

class updjgh07(_jgh07):
    """Jugendhilfestatistik ändern. (Tabelle: Jugendhilfestatistik)"""
    
    permissions = Request.STAT_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        # Pro Fall kann es nur 1 Jugendhilfestatistik geben.
        fallid = self.form.get('fallid')
        id = self.form.get('jghid')
        if id:
            jgh = Jugendhilfestatistik2007(id)
        elif fallid:
            fall = Fall(fallid)
            jgh = fall['jgh']
            if not jgh:
                raise EE('Noch keine Bundesstatistik f&uuml;r den Fall vorhanden.')
        else:
            self.last_error_message = "Keine Bundesstatistik-ID erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
        jgh['jghid'] = jgh['id']
        jgh['file'] = 'updjgh07'
        return self._formular(jgh)
        
class jgh07neu(_jgh07):
    """Neue Jugendhilfestatistik eintragen. (Tabelle: Jugendhilfestatistik.)"""
    permissions = Request.STAT_PERM
    def processForm(self, REQUEST, RESPONSE):
        fallid = self.form.get('fallid')
        jahr = today().year
        jghiddel = self.form.get('jghiddel')
        typ = self.form.get('typ')
        if jghiddel and typ == 'jgh' and fallid:
            # alte Statistik auf neue upgraden
            upgrade_jgh(jghiddel, old2new=True)
        if not fallid:
            raise EE('Bundesstatistik nur f&uuml;r einen g&uuml;ltigen Fall')
        fall = Fall(fallid)
        ex_jgh = fall['jgh']
        if ex_jgh:
            raise EE('Bundesstatistik bereits vorhanden.')
        jgh = Jugendhilfestatistik2007()
        jgh['jghid'] = Jugendhilfestatistik2007().getNewId()
        jgh['stz'] = self.stelle['id']
        jgh['file'] = 'jgh07einf'
        jgh['mit_id'] = fall['zustaendig__mit_id']
        #jgh.setDate('bg', fall.getDate('bg'))
        jgh.setDate('bg', fall['leistungsbeginn'])
        jgh['fall_fn'] = fall['fn']
        jgh['fall_id'] = fall['id']
        jgh['jahr'] = jahr
        dmy = [int(e) for e in fall['akte__gb'].split('.')]
        dmy.reverse()
        geburtsdatum = ebapi.Date(*dmy)
        jgh['gey'] = geburtsdatum.year
        jgh['gem'] = geburtsdatum.month
        geschlecht = fall['akte__gs']
        if not geschlecht:
            raise EE("Bitte zuerst das Geschlecht in die Klientenkarte eintragen!")
        jgh['gs'] = geschlecht
        assert isinstance(jgh['gs'], (int, long))
        if config.BERATUNGSKONTAKTE:
            from ebkus.html.beratungskontakt import get_jgh_kontakte
            jgh['nbkakt'], jgh['nbkges'] = get_jgh_kontakte(fall, jahr)
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

##         em, ey = self.form.get('em'), self.form.get('ey')
        
        ende = check_date(self.form, 'e', "Fehler im Datum für das Ende",
                                nodayallowed=True, maybezero=True, default=(0,0,0))
        if ende.is_zero():
            # kein Ende ausgefüllt, es ist mindestens 2007
            ende_jahr = max(2007, today().year)
        else:
            ende_jahr = ende.year
            
        # uns interessieren zwei Zustände:
        # für beide gilt Beginn ist 2006 oder früher
        # 1. alte Statistik und Ende 2007 oder später
        # 2. neue Statistik und Ende 2006 oder früher
        # In allen anderen Fällen wird direkt an die Klientenkarte weitergereicht.
        if beginn.year <= 2006 and fall['aktuell']:
            if ende_jahr <= 2006 and file in ('jgh07einf', 'updjgh07'):
                assert (file == 'updjgh07' and jghiddel or
                        file == 'jgh07einf' and not jghiddel)
                return self._ask(fallid, 'jghneu', jghiddel, 'jgh07', ende_jahr)
            if ende_jahr >= 2007 and file in ('jgheinf', 'updjgh'):
                assert (file == 'updjgh' and jghiddel or
                        file == 'jgheinf' and not jghiddel)
                return self._ask(fallid, 'jgh07neu', jghiddel, 'jgh', ende_jahr)
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
        meldung = submit_or_back_t % d
        return meldung


from ebkus.html.jgh_wohnt_ausserhalb import wohnt_ausserhalb
from ebkus.html.strkat import get_strasse

def _get_adress_data(jgh):
    """Holt Adressdaten ergänzt um Info aus dem Strassenkatalog falls vorhanden.
    Zur Zeit nur aus Akte, also Klient selber.
    Evt. auch aus Bezugsperson, aber nicht klar wie.
    Klient könnte allein wohnen, oä.

    Es werden nur Adressen herangezogen, wenn es eine 5-stellige PLZ und 
    einen Eintrag für den Ort gibt.
    """
    # def daten_ausreichend(data):
    #     if not re.match(r'^\d{5,5}$', data['plz']): # Nur korrekt geformte plz verwenden.
    #         data['plz'] = ''
    #         if not data['plz'] or not data['ort']: # Ohne korrekte plz und ort kann 'wohnt ausserhalb' nicht bestätigt werden.
    #             return False
    def data_from_obj(obj):
        data = dict(
            hsnr=obj.get('hsnr', ''), 
            str=obj.get('str', ''), 
            plz=obj.get('plz', ''),
            ort=obj.get('ort', ''),
            ortsteil=obj.get('ortsteil', ''),
            samtgemeinde=obj.get('samtgemeinde', ''),
            bezirk=obj.get('bezirk', ''),
            plraum=obj.get('plraum', ''),
            )
        return data
        # update nimmt keine keyword-Argumente in python 2.3:
        # data.update(hsnr=obj['hsnr'], str=obj['str'], plz=obj['plz'], ort=obj['ort'], plraum=obj['plraum'])
        # data.update(d)

        # d = (hsnr=obj['hsnr'], str=obj['str'], plz=obj['plz'], ort=obj['ort'], plraum=obj['plraum'])
        # for k in data.keys():
        #     v = obj.get(k)
        #     if v:
        #         data[k] = v

    akte = jgh['fall__akte']
    if akte:
        adressquelle = akte
        data = data_from_obj(adressquelle)
        # passiert alles später:
        # if not daten_ausreichend(data):
        #     return None
            # for art in ('Mutter', 'Vater',):
            #     for bp in akte['bezugspersonen']:
            #         if bp['verw__name'] == art:
        if config.STRASSENKATALOG:
            strasse = get_strasse(adressquelle)
            data.update(strasse)
        data['fall_fn'] = jgh['fall_fn']
        return data
    return None

def get_ags_plz_ort_if_wohnort_ausserhalb(jgh):
    data = _get_adress_data(jgh)
    if wohnt_ausserhalb(data, config):
        plz, ort = data['plz'], data['ort']
        ags = get_gemeindeschluessel(ort, plz)
        return ags, plz, ort
    else:
        return None

class jgh_wohnt_ausserhalb_check(Request.Request, akte_share):
    """Liefert Liste von Adressen & ob wohnt_ausserhalb detektiert wird mit aktueller Konfiguration.
    Wird nur benötigt zur Prüfung der Konfiguration. 
    """
    permissions = Request.ADMIN_PERM

    def get_daten(self, jahr=None):
        """Adressdaten für alle Bundesstatistikdatensätze für jahr.
        Liefert Liste von dicts mit Feldern:
        felder = 'str','hsnr','plz','ort',
                 'ortsteil','samtgemeinde','bezirk' # je nach config.STRASSENSUCHE
                 'plz_ausser', 'ort_ausser'
        damit man prüfen kann, für welche Adressen "wohnt außerhalb" generiert wird.
        """
        if jahr:
            jahr = int(jahr)
            where = 'jahr = %s' % jahr
        else:
            where = ''
        jghlist = Jugendhilfestatistik2007List(where=where)
        def get_data(jgh):
            data = _get_adress_data(jgh)
            if not data:
                return None
            res = get_ags_plz_ort_if_wohnort_ausserhalb(jgh)
            if not res:
                res = '','',''
            data['ags_ausser'], data['plz_ausser'], data['ort_ausser']  = res
            return data
        daten = [data for data in [get_data(jgh) for jgh in jghlist] if data]
        return daten

    def get_felder_und_daten_zeilen(self, jahr):
        """Liefert Liste von Listen von StringItems für FieldsetDataTable"""
        felder = 'fall_fn', 'str','hsnr','plz','ort'
        zusatzfelder = config.STRASSENSUCHE.split()
        if 'ort' in zusatzfelder:
            zusatzfelder.remove('ort')
        felder += tuple(zusatzfelder)
        if 'plraum' not in felder:
            felder += ('plraum',)
        felder += ('plz_ausser', 'ort_ausser', 'ags_ausser')
        daten_zeilen = []
        for data in self.get_daten(jahr):
            res = []
            for f in felder:
                res.append(h.String(string=data[f]))
            daten_zeilen.append(res)
        return felder, daten_zeilen

    def processForm(self, REQUEST, RESPONSE):
        jahr = self.form.get('jahr')
        felder, daten_zeilen = self.get_felder_und_daten_zeilen(jahr)
        adress_table = h.FieldsetDataTable(
            legend="Adressen zur Prüfung der Konfiguration",
            headers=felder,
            daten=daten_zeilen,
            )
        konfig_table = h.FieldsetDataTable(
            legend="Konfiguration für Adressen 'wohnt ausserhalb'",
            headers=('Variable', 'Wert'),
            daten=[[h.String(string="%s:" % var.lower(),
                             class_='labeltext',
                             align='right',
                             ),
                    h.String(string=getattr(config, var)),]
                   for var in (
                    'WOHNT_NICHT_AUSSERHALB',
                    # 'GEMEINDESCHLUESSEL_VON_PLZ',
                    )],
            )
        res = h.Page(
            title='Adressen zur Prüfung der Bundesstatistik',
            rows=(self.get_hauptmenu(),
                  konfig_table,
                  adress_table,
                  ),
            )
        return res.display()

