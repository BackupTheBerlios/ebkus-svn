# coding: latin-1
"""Verschiedenes was zur HTML-basierten Anwendung gehört, aber sonst nirgends
hineinpaßt"""

from ebkus.db import dbapp
from ebkus.app import ebapi
from ebkus.app_surface.abfragen_templates import *
from ebkus.app_surface.standard_templates import *

def mksel(result, template, List, field=None, value=None):
    """Automatisiert die Belegung des 'sel'-Feldes.
    
    Anwendung:
    mksel(res, codeliste_t, zugangsarten, 'id', anmeldung['zm'])"""
    if value is None: value = []
    else:
        if type(value) != type([]):
            value = [value]
    for elem in List:
        if field and elem[field] in value:
            elem['sel'] = 'selected'
        else:
            elem['sel'] = ''
        result.append(template % elem)
        del elem['sel']
        
def mksel_str_upd(result, template, List,wert):
    test = {'strvalue' : '-Nicht in Strassenkatalog enthalten-','sel' : ''}
    result.append(template % test)
    for name in List:
        sel_wert = ''
        if name[0] == wert:
            sel_wert = 'selected'
        strassen = {'strvalue' : name[0], 'sel' : sel_wert}
        result.append(template % strassen)
        
def mksel_str(result, template, List):
    test = {'strvalue' : '-Nicht in Strassenkatalog enthalten-'}
    result.append(template % test)
    for name in List:
        strassen = {'strvalue' : name[0]}
        result.append(template %strassen)
        
        ##*************************************************************************
        ##  Besondere Form des mksel mit zusätzlicher "Login" Überprüfung
        ##  Diese Unterdrückt das Anzeigen des Login - Benutzerrechtes
        ##*************************************************************************
def mksel_benr(result, template, List, field=None, value=None):
    if value is None: value = []
    else:
        if type(value) != type([]):
            value = [value]
    for elem in List:
        if field and elem[field] in value:
            elem['sel'] = 'selected'
        else:
            elem['sel'] = ''
        if elem['name'] != 'login':
            result.append(template % elem)
        del elem['sel']
        
def get_all_codes(kat_code):
    """Anwendung:
    stellenzeichen = get_all_codes('stzei')"""
    li =  ebapi.Kategorie(code = kat_code)['codes']
    li.sort('sort')
    return li
    
    
def get_codes(kat_code):
    """Anwendung:
    stellenzeichen = get_codes('stzei')"""
    li =  (ebapi.Kategorie(code = kat_code)['codes']).filter(lambda x: x['off'] != 1)
    li.sort('sort')
    return li
    
    
    ## def get_bereich(code_list, value):
    ##   code = filter(lambda x, v = value: x['mini'] <= v <= x['maxi'],
    ##                 code_list)
    
    
    #############################################################
    # HREFs berechnen
    # Diese Felder werden über den conditialfields Mechanismus
    # berechnet, brauchen also bei Updates nicht verändert zu werden.
    # Die Bedingungen, von denen sie abhängen, müssen aber gegebenenfalls
    # aktualisiert werden.
    #############################################################
    
ac = ebapi.Akte.conditionalfields

ac['href_thbperson'] = ('aktuell', """
<A HREF="persneu?akid=%(id)d&fallid=%(aktueller_fall__id)d&klerv=1">Eltern</A>,
<A HREF="persneu?akid=%(id)d&fallid=%(aktueller_fall__id)d&klerv=3">Geschwister</A>,
<A HREF="persneu?akid=%(id)d&fallid=%(aktueller_fall__id)d&klerv=8">Verwandte</A>""",
'Eltern, Geschwister, Verwandte')

ac['href_theinrichtung'] = ('aktuell', """
<A HREF="einrneu?akid=%(id)d&fallid=%(aktueller_fall__id)d">Einrichtungskontakt</A>""",
'Einrichtungskontakt')

ac['href_thanmeldung'] = (('aktueller_fall__anmeldung', 'aktuell') ,
'Anmeldung',
 """
<A HREF="anmneu?akid=%(id)d&fallid=%(aktueller_fall__id)d">Anmeldung</A>""",
'Anmeldung')

ac['href_thleistung'] = ('aktuell', """
<A HREF="leistneu?akid=%(id)d&fallid=%(aktueller_fall__id)d">Leistung</A>""",
'Leistung')

ac['href_thzustaendig'] = ('aktuell', """
<A HREF="zustneu?akid=%(id)d&fallid=%(aktueller_fall__id)d">Bearbeiter</A>""",
'Bearbeiter')

ac['href_fstatistik'] = ('aktuell', """
<A HREF="fsneu?akid=%(id)d&fallid=%(aktueller_fall__id)d"> Fachstatistik</A>""",
'Fachstatistik')


ac['href_jghstatistik'] = ('aktuell', """
<A HREF="jghneu?akid=%(id)d&fallid=%(aktueller_fall__id)d"> Bundesstatistik</A>""",
'Bundesstatistik')

ac['href_updakte'] = ('aktuell', """
<A HREF="updakte?akid=%(id)d">%(na)s</A>""",
"%(na)s")

ac['stfarbe'] = (('aktuell', 'wiederaufnehmbar') , '#FFFFFF', '#FAF0E6', '#FFF5EE',)
ac['staktion'] = (('aktuell', 'wiederaufnehmbar') , 'zda',  'W', 'R')

ac['href_thstand'] = (('aktuell', 'wiederaufnehmbar') , """
<A HREF="zda?akid=%(id)d&fallid=%(aktueller_fall__id)d">Stand</A>""",
"""
<A HREF="waufnneu?akid=%(id)d&fallid=%(letzter_fall__id)d">Stand</A>""",
"""
<A HREF="zdar?akid=%(id)d&fallid=%(letzter_fall__id)d">Stand</A>""")


ac['href_no'] = ('no', """
<A HREF="klkarte?akid=%(id)d#notiz"> Notiz</A>""", '')


bc = ebapi.Bezugsperson.conditionalfields

bc['href_updpersvn'] = ('akte_id__aktuell', """
<A HREF="updpers?akid=%(akte_id)d&bpid=%(id)d"> %(vn)s</A>""",
'%(vn)s')

bc['href_updpersna'] = ('akte_id__aktuell', """
<A HREF="updpers?akid=%(akte_id)d&bpid=%(id)d"> %(na)s</A>""",
'%(na)s')

bc['href_no'] =  ('no', """
<A HREF="klkarte?akid=%(akte_id)d#notiz"> %(nobed__name)s</A>""", '')

ec = ebapi.Einrichtungskontakt.conditionalfields

ec['href_updeinrna'] = ('akte_id__aktuell', """
<A HREF="updeinr?akid=%(akte_id)d&einrid=%(id)d"> %(na)s</A>""",
'%(na)s')

ec['href_no'] =  ('no', """
<A HREF="klkarte?akid=%(akte_id)d#notiz"> %(nobed__name)s</A>""", '')


ac = ebapi.Anmeldung.conditionalfields

ac['href_updanm'] = ('fall_id__aktuell', """
<A HREF="updanm?fallid=%(fall_id)d&anmid=%(id)d"> gemeldet von</A>""",
' gemeldet von ')

ac['href_no'] =  ('no', """
<A HREF="klkarte?akid=%(fall_id__akte_id)d#notiz"> Notiz</A>""", '')



lc = ebapi.Leistung.conditionalfields

lc['href_updleist'] = ('fall_id__aktuell', """
<A HREF="updleist?fallid=%(fall_id)d&leistid=%(id)d"> %(mit_id__na)s</A>""",
' %(mit_id__na)s ')

zc = ebapi.Zustaendigkeit.conditionalfields

zc['href_updzust'] = ('fall_id__aktuell', """
<A HREF="updzust?fallid=%(fall_id)d&zustid=%(id)d"> %(mit_id__na)s</A>""",
' %(mit_id__na)s ' )

fc = ebapi.Fall.conditionalfields

fc['href_updfall'] = ('aktuell', """
<A HREF="updfall?akid=%(akte_id)d&fallid=%(id)d"> %(fn)s</A>""",
' %(fn)s ')

sc = ebapi.Fachstatistik.conditionalfields

sc['href_updfs'] = ('fall_id__aktuell', """
<A HREF="updfs?fallid=%(fall_id)d&fsid=%(id)d"> %(jahr)d</A> """,
' %(jahr)d' )

jc = ebapi.Jugendhilfestatistik.conditionalfields

jc['href_updjgh'] = ('fall_id__aktuell', """
<A HREF="updjgh?akid=%(fall_id__akte_id)d&fallid=%(fall_id)d&jghid=%(id)d"> %(em)d.%(ey)d</A> """,
'%(em)d.%(ey)d' )

dc = ebapi.Dokument.conditionalfields

dc['href_dokkarte'] = ('fall_id__aktuell', """
<A HREF="dokkarte?fallid=%(fall_id)d&dokid=%(id)d">%(vd)d.%(vm)d.%(vy)d</A>""",
'Dokument')

dc['href_vermneu'] = ('fall_id__aktuell', """
<A HREF="vermneu?fallid%(fall_id)d">Vermerk""",
'Dokument')

dc['href_upload'] = ('fall_id__aktuell', """
<A HREF="upload?fallid%(fall_id)d">Import""",
'Dokument')

dc['href_updverm'] = ('fall_id__aktuell', """
<A HREF="updverm?fallid%(fall_id)d&dokid=%(id)d">Text ändern""",
'Dokument')

dc['href_updvermausw'] = ('fall_id__aktuell', """
<A HREF="updvermausw?fallid%(fall_id)d">Text ändern""",
'Dokument')

dc['href_rmdok'] = ('fall_id__aktuell', """
<A HREF="rmdok?fallid%(fall_id)d">Löschen""",
'Dokument')


    
def mk_ausgabe_codeliste(res, templatel, dlist):
    """Macht die Codelistenausgaben etwas freundlicher.
    """
    
    if isinstance(dlist, dbapp.DBObjekt):
        if dlist['dm'] == None:
            sep = ''
        else:
            sep = '.'
        if dlist['off'] == 1:
            off = 'x'
        else:
            off = ''
        d1 = {'id' : dlist['id'], 'kat_id' : dlist['kat_id'],
              'code': dlist['code'], 'name' : dlist['name'],
              'sort' : dlist['sort'],
              'mini' : dlist['mini'], 'maxi' : dlist['maxi'],
              'off' : off, 'dm' : dlist['dm'], 'dy' : dlist['dy'],
              'dok' : dlist['dok'], 'sep' : sep}
        keys = d1.keys()
        for k in keys:
            if d1[k] == None:
                d1[k] = ''
        res.append(templatel % d1)
        del d1
    else:
        for d in dlist:
            if d['dm'] == None:
                sep = ''
            else:
                sep = '.'
            if d['off'] == 1:
                off = 'x'
            else:
                off = ''
            d1 = {'id' : d['id'], 'kat_id' : d['kat_id'],
                'code': d['code'], 'name' : d['name'],
                'sort' : d['sort'], 'mini' : d['mini'], 'maxi' : d['maxi'],
                'off' : off, 'dm' : d['dm'], 'dy' : d['dy'],
                'dok' : d['dok'], 'sep' : sep}
            keys = d1.keys()
            for k in keys:
                if d1[k] == None:
                    d1[k] = ''
            res.append(templatel % d1)
            del d1
            
    
def mk_columns(text, width):
    """Zeilenumbruch fuer Ascii-Texte zur Plain-Text Ausgabe im Browser
    """
    t = text.strip()
    words = t.split(' ')
    new = ''
    c = 0
    for w in words:
        new = new + w + ' '
        if len(new) > c + width:
            new = new + '\n'
            c = c + width + 1
    return new
    
def mk_text(dokumentliste, path):
    """Formatiert einen Ascii Text zur Anzeige im Browser"""
    
    out = ''
    for d in dokumentliste:
        try:
            f = open('%s/%s'
                     % (path, d['fname']), 'r')
            datei = f.read()
        except ebapi.EBUpdateDataError, e:
            raise ebapi.EE("Datei nicht gefunden: %s" % str(args))
            
        kopfzeile = '%(vd)d.%(vm)d.%(vy)d: %(art__name)s' % d
        fuss = '\n%(mit_id__vn)s %(mit_id__na)s' % d
        betreff = mk_columns(d['betr'],65)
        zeilen = betreff.split('\n')
        betr = ''
        for z in zeilen:
            betr = betr + '%s\n' % z
        out = '%s\n%s\nBetr.: %s\n\n%s\n%s\n\n'\
              % (out, kopfzeile, betreff, datei, fuss)
        f.close()
        
    return out
    
    
    
    
    
    
    
    
    
