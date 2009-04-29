# coding: latin-1
""" Alle Funktionen, die zu einer Veränderung der Datenbank führen, stehen
hier. """

import time
import sha
import os
from ebkus.app.ebapi import *
from ebkus.app.ebapih import *
from ebkus.config import config
from ebkus.db.dbapp import cache_on, cache_off, cache_is_on, undo_cached_fields


def akteeinf(form):
    """Neue Akte, Fall, Zustaendigkeit"""
    
    akid = check_int_not_empty(form, 'akid', "Aktenid fehlt")
    check_not_exists(akid, Akte,
      "Akte (id: %(id)s, Name: %(na)s, %(vn)s, Geburtsdatum %(gb)s) existiert bereits")
    akte = Akte()
    get_string_fields(akte, form,
          ['vn', 'na', 'ber', 'tl1', 'tl2', 'no'],'')
    setAdresse(akte, form)
    akte['na'] = check_str_not_empty(form, 'na', "Kein Name")

    akte['gs'] = check_code(form,'gs', 'gs',
                            "Keine Geschlechtsangabe")
    akte['aufbew'] = check_code(form,'aufbew', 'aufbew',
                            "Keine Aufbewahrungskategorie")
    akte['gb'] = str(check_date(form, 'gb', 'Fehler im Geburtsdatum'))
##     akte['gb'] = check_str_not_empty(form, 'gb', "Kein Geburtsdatum")
    akte['fs'] = check_code(form,'fs', 'fsfs',
                            "Fehler im Familienstatus", '999')
    akte['stzbg'] = check_code(form, 'stzbg',
                               'stzei', "Kein Stellenzeichen für die Akte")
    stelle = Code(akte['stzbg'])
    akte['zeit'] = int(time.time())
    
    fall = Fall()
    # Fallbeginn ist identisch mit Zuständigkeitsbeginn
    fall.setDate('bg',
                 check_date(form, 'zubg',
                            "Fehler im Anmeldedatum"))
    fall.setDate('zda', Date(0,0,0))
    fall['fn'] = getNewFallnummer(stelle['code'], fall['bgy'])
    fall['status'] = cc('stand', 'l')

    zust = Zustaendigkeit()
    zust['mit_id'] = check_fk(form, 'zumitid', Mitarbeiter,
                              "Kein zuständiger Mitarbeiter für Fall")
    zust.setDate('bg', fall.getDate('bg'))
    zust.setDate('e', Date(0,0,0))
    
    leist = Leistung()
    leist['mit_id'] = check_fk(form, 'lemitid', Mitarbeiter,
                              "Kein zuständiger Mitarbeiter für Leistung")
    leist['le'] = check_code(form, 'le', 'fsle', "Keine Leistungsart")
    leist.setDate('bg',
                  check_date(form, 'lebg',
                             "Fehler im Datum für den Leistungsbeginn"))
    if leist.getDate('bg') < fall.getDate('bg'):
        raise EE("Datum des Leistungsbeginn vor Fallbeginn")
    leist.setDate('e', Date(0,0,0))
    leist['stz'] = check_code(form, 'lestz', 'stzei',
                              "Kein Stellenzeichen für die Leistung",
                              stelle['id'])

    if config.ANMELDUNGSDATEN_OBLIGATORISCH:
        anm = _check_anmeinf(form)
    try:
        akte.insert(akid)
        fall['akte_id'] = akte['id']
        fall.new()
        fall.insert()
        if config.ANMELDUNGSDATEN_OBLIGATORISCH:
            anm['fall_id'] = fall['id']
            anm.insert()
        zust['fall_id'] = fall['id']
        zust.new()
        zust.insert()
        leist['fall_id'] = fall['id']
        leist.new()
        leist.insert()
    except Exception, args:
        try: akte.delete()
        except: pass
        try: fall.delete()
        except: pass
        try: zust.delete()
        except: pass
        try: leist.delete()
        except: pass
        raise EBUpdateError("Fehler beim Einfügen in die Datenbank: %s" % str(args))
        
def updakte(form):

    akteold = check_exists(form, 'akid', Akte, "Aktenid fehlt")
    akte = Akte()
    akte['na'] = check_str_not_empty(form, 'na', "Kein Name", akteold)
    akte['gs'] = check_code(form,'gs', 'gs',
                            "Keine Geschlechtsangabe")
    akte['aufbew'] = check_code(form,'aufbew', 'aufbew',
                            "Keine Aufbewahrungskategorie")
    akte['gb'] = str(check_date(form, 'gb', 'Fehler im Geburtsdatum'))
##     akte['gb'] = check_str_not_empty(form, 'gb', "Kein Geburtsdatum", akteold)
    get_string_fields(akte, form,
                      ['vn', 'ber',
                       'tl1', 'tl2', 'no'], akteold)
    
    setAdresse(akte, form)
    akte['fs'] = check_code(form,'fs', 'fsfs',
                            "Fehler im Familienstatus", akteold)
    # Werte erst dann übernehmen, wenn keine Fehler aufgetreten sind
    akteold.update(akte)
    _stamp_akte(akteold)
    
def perseinf(form):
    """Neue Bezugsperson."""
    
    bpid = check_int_not_empty(form, 'bpid', "Bezugspersonenid fehlt")
    check_not_exists(bpid, Bezugsperson,
      "Bezugsperson (id: %(id)s, Name: %(na)s, %(vn)s Geburtsdatum %(gb)s) existiert bereits")
    pers = Bezugsperson()
    pers['akte_id'] = check_fk(form, 'akid', Akte, "Keine Akte")
    get_string_fields(pers, form,
                      ['vn', 'na', 'ber', 'tl1', 'tl2', 'no'],'')
    if pers['vn'] == '' and pers['na'] == '':
        raise EE("Kein Name")
    pers['verw'] = check_code(form, 'verw', 'klerv',
                              "Fehler im Verwandtschaftsgrad", '999')
    gs = form.get('gs')
    if gs and not gs == ' ':
        gs = check_code(form,'gs', 'gs',
                        "Keine Geschlechtsangabe", '')
    else:
        verwname = Code(pers['verw'])['name'].lower()
        if 'vater' in verwname:
            gs = cc('gs', '1')
        elif 'mutter' in verwname:
            gs = cc('gs', '2')
        else:
            gs = None
    pers['gs'] = gs
    gb = check_date(form, 'gb', 'Fehler im Geburtsdatum', (0,0,0),
                    alle_jahrgaenge_akzeptieren=True)
    pers['gb'] = gb.year != 0 and str(gb) or ''
    setAdresse(pers, form)
    pers['fs'] = check_code(form,'fs', 'fsfs',
                            "Fehler im Familienstatus", '999')
    pers['nobed'] = check_code(form, 'nobed', 'notizbed',
                               "Fehler in Notizbedeutung", cc('notizbed', 'f'))
    pers['vrt'] = check_code(form, 'vrt', 'vert',
                             "Fehler in Verteiler", 'f')
    try:
        pers.insert(bpid)
    except Exception, args:
        try: pers.delete()
        except: pass
        raise EBUpdateError("Fehler beim Einfügen in die Datenbank: %s" % str(args))
    _stamp_akte(pers['akte'])
    
    
def updpers(form):
    """Update der Bezugsperson."""
    
##     # unsystematische HACK!!
##     fs = form.get('nobed')
##     if not fs:
##         form['nobed'] = cc('notizbed', 'f')
        
    persold = check_exists(form, 'bpid', Bezugsperson, "Bezugspersonid fehlt")
    pers = Bezugsperson()
    get_string_fields(pers, form,
                      ['vn', 'na', 'ber', 'tl1', 'tl2', 'no','hsnr'],
                      persold)
    if pers['vn'] == '' and pers['na'] == '':
        raise EE("Kein Name")
    pers['verw'] = check_code(form, 'verw', 'klerv',
                              "Fehler im Verwandtschaftsgrad", persold)
    gs = form.get('gs').strip()
    if gs:
        gs = check_code(form,'gs', 'gs',
                        "Keine Geschlechtsangabe", '')
    else:
        verwname = Code(pers['verw'])['name'].lower()
        if 'vater' in verwname:
            gs = cc('gs', '1')
        elif 'mutter' in verwname:
            gs = cc('gs', '2')
        else:
            gs = None
    pers['gs'] = gs
    gb = check_date(form, 'gb', 'Fehler im Geburtsdatum', (0,0,0),
                    alle_jahrgaenge_akzeptieren=True)
    pers['gb'] = gb.year != 0 and str(gb) or ''
    setAdresse(pers, form)
    pers['fs'] = check_code(form,'fs', 'fsfs',
                            "Fehler im Familienstatus", persold)
    pers['nobed'] = check_code(form, 'nobed', 'notizbed',
                               "Fehler in Notizbedeutung", cc('notizbed', 'f'))
    pers['vrt'] = check_code(form, 'vrt', 'vert',
                             "Fehler in Verteiler", persold)
    
    persold.update(pers)
    _stamp_akte(persold['akte'])
    

def removepers(form):
    pers = check_exists(form, 'bpid', Bezugsperson, "Bezugspersonid fehlt")
    if pers['gruppen']:
        raise EE('Mitglied einer Gruppe kann nicht gelöscht werden')
    if pers['fallberatungskontakte']:
        raise EE('Teilnehmer/in an Beratungskontakt kann nicht gelöscht werden')
    pers.delete()

    
def einreinf(form):
    """Neuer Einrichtungskontakt."""
    
    einrid = check_int_not_empty(form, 'einrid', "Einrichtungskontaktid fehlt")
    check_not_exists(einrid, Einrichtungskontakt,
      "Einrichtungskontakt (id: %(id)s, Name: %(na)s) existiert bereits")
    einr = Einrichtungskontakt()
    einr['akte_id'] = check_fk(form, 'akid', Akte, "Keine Akte")
    get_string_fields(einr, form, ['na','tl1','tl2', 'no'],'')
    if einr['na'] == '':
        raise EE("Kein Name")
    einr['insta'] = check_code(form, 'insta', 'klinsta',
                               "Fehler in Institution", '999')
    einr['nobed'] = check_code(form, 'nobed', 'notizbed',
                               "Fehler in Notizbedeutung", cc('notizbed', 'f'))
    einr['status'] = check_code(form, 'status', 'einrstat',
                                "Fehler in Einrichtungsstatus", cc('einrstat', 'nein'))
    
    einr.insert(einrid)
    _stamp_akte(einr['akte'])
    
    
def updeinr(form):
    """Update eines Einrichtungskontaktes."""
    
##     # unsystematische HACK!!
##     fs = form.get('nobed')
##     if not fs:
##         form['nobed'] = cc('notizbed', 'f')
        
    einrold = check_exists(form, 'einrid', Einrichtungskontakt, "Einrichtungskontaktid fehlt")
    einr = Einrichtungskontakt()
    get_string_fields(einr, form, ['na','tl1','tl2', 'no'], einrold)
    if einr['na'] == '':
        raise EE("Kein Name")
    einr['insta'] = check_code(form, 'insta', 'klinsta',
                               "Fehler in Institution", einrold)
    einr['nobed'] = check_code(form, 'nobed', 'notizbed',
                               "Fehler in Notizbedeutung", cc('notizbed', 'f'))
    einr['status'] = check_code(form, 'status', 'einrstat',
                                "Fehler in Einrichtungsstatus", cc('einrstat', 'nein'))
    
    einrold.update(einr)
    _stamp_akte(einrold['akte'])
    

def removeeinr(form):
    einr = check_exists(form, 'einrid', Einrichtungskontakt, "Einrichtungskontaktid fehlt")
    einr.delete()


def _check_anmeinf(form):
    anmid = check_int_not_empty(form, 'anmid', "Anmeldungsid fehlt")
    check_not_exists(anmid, Anmeldung,
      "Anmeldung (id: %(id)s, Von: %(von)s) existiert bereits")
    anm = Anmeldung()
    anm['id'] = anmid
    get_string_fields(anm, form, ['von','mtl','me', 'mg', 'anm_no'],'')
    if anm['von'] == '':
        raise EE("Kein Feld 'Gemeldet von'")
    anm['no'] = anm['anm_no']
    del anm['anm_no']
    anm['zm'] = check_code(form, 'zm', 'fszm', "Fehler im Zugangsmodus")
    return anm

def anmeinf(form):
    """Neue Anmeldung."""
    anm = _check_anmeinf(form)
    anm['fall_id'] = check_fk(form, 'fallid', Fall, "Kein Fall")
    fall = Fall(anm['fall_id'])
    vorhandene_anmeldung = fall['anmeldung']
    if len(vorhandene_anmeldung) > 0:
        raise EE("Anmeldung für Fall %(fn)s schon vorhanden" % fall)
    try:
        anm.insert()
    except:
        try: anm.delete()
        except: pass
    _stamp_akte(anm['akte'])
    
    
def updanm(form):
    """Update der Anmeldung."""
    anmold = check_exists(form, 'anmid', Anmeldung, "Keine Anmeldungsid")
    anm = Anmeldung()
    get_string_fields(anm, form, ['von','mtl','me', 'mg', 'anm_no'], anmold)
    if anm['von'] == '':
        raise EE("Kein Feld 'von wem gemeldet'")
    anm['zm'] = check_code(form, 'zm', 'fszm', "Fehler im Zugangsmodus", anmold)
    anm['no'] = anm['anm_no']
    del anm['anm_no']
    anmold.update(anm)
    _stamp_akte(anmold['akte'])
    
def leisteinf(form):
    """Neue Leistung."""
    
    leistid = check_int_not_empty(form, 'leistid', "Leistungsid fehlt")
    check_not_exists(leistid, Leistung,
      "Leistung (id: %(id)s) existiert bereits")
    leist = Leistung()
    leist['fall_id'] = check_fk(form, 'fallid', Fall, "Kein Fall")
    leist['mit_id'] = check_fk(form, 'mitid', Mitarbeiter, "Kein Mitarbeiter")
    leist['le'] = check_code(form, 'le', 'fsle', "Fehler in Leistungsart")
    
    
    beginndatum = check_date(form, 'bg', "Fehler im Leistungsbeginndatum")
    endedatum = check_date(form, 'e', "Fehler im Leistungsendedatum", Date(0,0,0),
                           maybezero = 1)
    
    if endedatum < beginndatum:
        raise EE("Endedatum vor Beginndatum")
        
    fall = Fall(leist['fall_id'])
    if beginndatum < fall.getDate('bg'):
        raise EE("Beginndatum vor Fallbeginn")
        
    leist.setDate('bg', beginndatum)
    leist.setDate('e', endedatum)
    
    
    leist['stz'] = check_code(form, 'stz', 'stzei',
                              "Kein Stellenzeichen für die Leistung")
    try:
        leist.insert(leistid)
    except:
        try: leist.delete()
        except: pass
    _stamp_akte(leist['akte'])
    
    
def updleist(form):
    """Update der Leistung."""
    
    leistold = check_exists(form,'leistid', Leistung, "Keine Leistungsid")
    fall = leistold['fall']
    
    leist = Leistung()
    
    leist['mit_id'] = check_fk(form, 'mitid', Mitarbeiter, "Fehler in Mitarbeiter", leistold)
    leist['le'] = check_code(form, 'le', 'fsle', "Fehler in Leistungsart", leistold)
    
    beginndatum = check_date(form, 'bg', "Fehler im Leistungsbeginndatum", leistold)
    endedatum = check_date(form, 'e', "Fehler im Leistungsendedatum", leistold,
                           maybezero = 1)
    # Überprüfungen?
    if endedatum < beginndatum:
        raise EE("Endedatum vor Beginndatum")
        
    if beginndatum < fall.getDate('bg'):
        raise EE("Beginndatum vor Fallbeginn")
        
    leist.setDate('bg', beginndatum)
    leist.setDate('e', endedatum)
    
    leist['stz'] = check_code(form, 'stz', 'stzei',
                              "Kein Stellenzeichen für die Leistung",
                              leistold)
    leistold.update(leist)
    _stamp_akte(leistold['akte'])

## def _bkont_check(form, bkont):
##     bkont['fall_id'] = check_fk(form, 'fallid', Fall, "Kein Fall")
##     bkont['mit_id'] = check_fk(form, 'mitid', Mitarbeiter, "Kein Mitarbeiter")
##     bkont['art'] = check_code(form, 'art', 'fska', "Fehler in Beratungskontaktart")
##     bkont['no'] = check_str_not_empty(form, 'no', 'Keine Notiz', '')
##     if config.BERATUNGSKONTAKTE_MINUTEN:
##         bkont['f2f_min'] = check_int_not_empty(form, 'f2f_min', "Fehler in Face-2-Face Minuten")
##         bkont['vn_min'] = check_int_not_empty(form, 'vn_min', "Fehler in Vor/Nachbereitung Minuten")
##     else:
##         bkont['dauer'] = check_code(form, 'dauer', 'fskd', "Fehler in Beratungskontaktdauer")
##     datum = check_date(form, 'k', "Fehler im Beratungskontaktdatum")
##     fall = Fall(bkont['fall_id'])
##     if datum < fall.getDate('bg'):
##         raise EE("Datum vor Fallbeginn")
##     if fall.get('ey') and datum > fall.getDate('e'):
##         raise EE("Datum nach Fallende")
##     bkont.setDate('k', datum)
##     bkont['stz'] = check_code(form, 'stz', 'stzei',
##                             "Kein Stellenzeichen für den Beratungskontakt")

def removeleist(form):
    """Löschen der Leistung."""
    leist = check_exists(form,'leistid', Leistung, "Keine Leistungsid")
    if len(leist['fall']['leistungen']) < 2:
        raise EE('Es muss immer mindestens eine Leistung geben')
    if leist['beratungskontakte']:
        raise EE('Leistung in einem Beratungskontakt kann nicht gelöscht werden')
    leist.delete()
        
def _bkont_check(form, bkont):
    #print '_bkont_bs_check', form
    fall_ids = check_list(form, 'bkfallid', 'Keine Fälle')
    mit_ids = check_list(form, 'mitid', 'Keine Mitarbeiter')
    faelle = [Fall(id) for id in fall_ids]
    mitarbeiter = [Mitarbeiter(id) for id in mit_ids]
    if config.BERATUNGSKONTAKTE_BS:
        zeit = check_time(form, 'k', "Fehler in Uhrzeit", Time())
        bkont.setTime('k', zeit)
        bkont['art_bs'] = check_code(form, 'art_bs', 'kabs', "Fehler in Beratungskontaktart")
        mc = check_multi_code(form, 'teilnehmer_bs', 'teilnbs',
                              "Fehler in Teilnehmer",
                              #default=[cc('teilnbs', '0')]) # falsch!
                              default=[Code(kat_code='teilnbs', code='0')])
        #print 'MULTICODE', mc, type(mc)
        bkont['teilnehmer_bs'] = mc
        bkont['offenespr'] = check_code(form, 'offenespr', 'ja_nein', "", cn('ja_nein', 'nein'))
        bkont['dauer'] = check_int_not_empty(form, 'dauer', "Fehler in Dauer", 0)
        if Code(bkont['art_bs'])['code'] == '5':
            # ausgefallener Kontakt automatisch 20 Minuten
            bkont['dauer'] = 20
        if not (bkont['dauer'] % 10) == 0:
            raise EE("Bitte Kontaktdauer nur in 10-er Schritten angeben, z.B. 20, 30, 60.")
        bkont['anzahl'] = check_int_not_empty(form, 'anzahl', "Fehler in Anzahl der Teilnehmer", 0)
    else:
        bkont['art'] = check_code(form, 'art', 'fska', "Fehler in Beratungskontaktart")
        dauer_kat = check_code(form, 'dauer_kat', 'fskd', "Fehler in Kontaktdauer")
        # wir tragen einfach den Mittelwert zwischen den Bereichsgrenzen ein
        bkont['dauer'] = int((Code(dauer_kat)['mini'] + Code(dauer_kat)['maxi'])/2.)
    bkont['no'] = check_str_not_empty(form, 'no', 'Keine Notiz', '')
    datum = check_date(form, 'k', "Fehler im Beratungskontaktdatum")
    for fall in faelle:
        if datum < fall.getDate('bg'):
            raise EE("Datum vor Fallbeginn von %(akte__vn)s %(akte__na)s" % fall )
        if fall.get('ey') and datum > fall.getDate('e'):
            raise EE("Datum nach Fallende von %(akte__vn)s %(akte__na)s" % fall)
    bkont.setDate('k', datum)
    bkont['stz'] = check_code(form, 'stz', 'stzei',
                              "Kein Stellenzeichen für den Beratungskontakt")
    return mitarbeiter, faelle

def _bkont_upd_mitarbeiter_faelle(bkont, mitarbeiter, faelle):
    MitarbeiterberatungskontaktList(where='bkont_id=%(id)s' % bkont).deleteall()
    FallberatungskontaktList(where='bkont_id=%(id)s' % bkont).deleteall()
    for m in mitarbeiter:
        mb = Mitarbeiterberatungskontakt()
        mb.init(
            mit_id=m['id'],
            bkont_id=bkont['id'],
            )
        mb.new()
        mb.insert()
    for f in faelle:
        fb = Fallberatungskontakt()
        fb.init(
            fall_id=f['id'],
            bkont_id=bkont['id'],
            )
        fb.new()
        fb.insert()

## def bkonteinf(form):
##     """Neuer Beratungskontakt."""
##     if not config.BERATUNGSKONTAKTE:
##         raise EBUpdateError("Aufruf von bkonteinf ohne config.BERATUNGSKONTAKTE")
##     bkontid = check_int_not_empty(form, 'bkontid', "Beratungskontaktid fehlt")
##     check_not_exists(bkontid, Beratungskontakt,
##                      "Beratungskontakt (id: %(id)s) existiert bereits")
##     bkont = Beratungskontakt()
##     _bkont_check(form, bkont)
##     try:
##         bkont.insert(bkontid)
##     except:
##         try: bkont.delete()
##         except: pass
##     _stamp_akte(bkont['fall__akte'])

def bkonteinf(form):
    """Neuer Beratungskontakt."""
    bkontid = check_int_not_empty(form, 'bkontid', "Beratungskontaktid fehlt")
    check_not_exists(bkontid, Beratungskontakt,
                     "Beratungskontakt (id: %(id)s) existiert bereits")
    bkont = Beratungskontakt()
    mitarbeiter, faelle = _bkont_check(form, bkont)
    try:
        bkont.insert(bkontid)
        _bkont_upd_mitarbeiter_faelle(bkont, mitarbeiter, faelle)
    except:
        try: bkont.delete()
        except: pass
    for f in bkont['faelle']:
        _stamp_akte(f['akte'])
    
## def updbkont(form):
##     """Update des Beratungskontakts."""
##     if not config.BERATUNGSKONTAKTE:
##         raise EBUpdateError("Aufruf von updbkont ohne config.BERATUNGSKONTAKTE")
##     bkontold = check_exists(form,'bkontid', Beratungskontakt, "Keine Beratungskontaktid")
##     bkont = Beratungskontakt()
##     _bkont_check(form, bkont)
##     bkontold.update(bkont)
##     _stamp_akte(bkontold['fall__akte'])
    
def updbkont(form):
    """Update des Beratungskontakts."""
    bkontold = check_exists(form,'bkontid', Beratungskontakt, "Keine Beratungskontaktid")
    bkont = Beratungskontakt()
    mitarbeiter, faelle = _bkont_check(form, bkont)
    bkontold.update(bkont)
    _bkont_upd_mitarbeiter_faelle(bkontold, mitarbeiter, faelle)
    for f in bkontold['faelle']:
        _stamp_akte(f['akte'])
    

def removebkont(form):
    bkont = check_exists(form,'bkontid', Beratungskontakt, "Keine Beratungskontaktid")
    faelle = bkont['faelle']
    MitarbeiterberatungskontaktList(where='bkont_id=%(id)s' % bkont).deleteall()
    FallberatungskontaktList(where='bkont_id=%(id)s' % bkont).deleteall()
    #print 'BKONT ID', bkont['id']
    bkont.delete()
    for f in faelle:
        _stamp_akte(f['akte'])
    
# Fallunabhängige Aktivitäten Braunschweig
def _fua_bs_check(form, fua):
    #print '_fua_bs_check', form
    fua['mit_id'] = check_fk(form, 'mitid', Mitarbeiter, "Kein Mitarbeiter")
    fua['art'] = check_code(form, 'art', 'fuabs', "Fehler in Aktivitätstart")
    fua['no'] = check_str_not_empty(form, 'no', 'Keine Notiz', '')
    if fua['art'] == cc('fuabs', '1'):
        fua['dauer'] = 20
    else:
        fua['dauer'] = check_int_not_empty(form, 'dauer', "Fehler in Dauer")
        if not (fua['dauer'] % 10) == 0:
            raise EE("Bitte Aktivitätsdauer nur in 10-er Schritten angeben, z.B. 20, 30, 60, etc.")
    datum = check_date(form, 'k', "Fehler im Aktivitätsdatum")
    fua.setDate('k', datum)
    fua['stz'] = check_code(form, 'stz', 'stzei',
                              "Kein Stellenzeichen für die Aktivität")

def fuabseinf(form):
    """Neue Aktivität."""
    if not config.FALLUNABHAENGIGE_AKTIVITAETEN_BS:
        raise EBUpdateError("Aufruf von fuabseinf ohne config.FALLUNABHAENGIGE_AKTIVITAETEN_BS")
    fuaid = check_int_not_empty(form, 'fuaid', "Aktivitäts-ID fehlt")
    check_not_exists(fuaid, Fua_BS,
                     "Aktivität (id: %(id)s) existiert bereits")
    # Bei neuen Fua sind mehrere Mitarbeiter erlaubt
    # Es werden dann identische Einträge für jeden Mitarbeiter getrennt
    # vorgenommen.
    mit_ids = check_list(form, 'mitid', 'Keine Mitarbeiter')
    fua_ids = [fuaid] + [None for i in mit_ids[1:]]
    #print 'MITIDS', mit_ids
    for mit_id, fua_id in zip(mit_ids,fua_ids):
        form['mitid'] = mit_id
        if fua_id == None:
            fua_id = Fua_BS().getNewId()
        fua = Fua_BS()
        _fua_bs_check(form, fua)
        try:
            fua.insert(fua_id)
        except:
            try: fua.delete()
            except: pass
    
def updfuabs(form):
    """Update der fallunabhängigen Aktivität."""
    if not config.FALLUNABHAENGIGE_AKTIVITAETEN_BS:
        raise EBUpdateError("Aufruf von updfuabs ohne config.FALLUNABHAENGIGE_AKTIVITAETEN_BS")
    fuaold = check_exists(form,'fuaid', Fua_BS, "Keine Aktivitäts-ID")
    fua = Fua_BS()
    _fua_bs_check(form, fua)
    fuaold.update(fua)

def removefuabs(form):
    if not config.FALLUNABHAENGIGE_AKTIVITAETEN_BS:
        raise EBUpdateError("Aufruf von updfuabs ohne config.FALLUNABHAENGIGE_AKTIVITAETEN_BS")
    fua = check_exists(form,'fuaid', Fua_BS, "Keine Aktivitäts-ID")
    fua.delete()
    
def zusteinf(form):
    """Neue Zuständigkeit."""

    # nicht am selben Tag beginnen wie der vorige
    zustid = check_int_not_empty(form, 'zustid', "Zuständigkeitsid fehlt")
    check_not_exists(zustid, Zustaendigkeit,
      "Zuständigkeit (id: %(id)s) existiert bereits")
    zust = Zustaendigkeit()
    zust['fall_id'] = check_fk(form, 'fallid', Fall, "Kein Fall")
    zust['mit_id'] = check_fk(form, 'mitid', Mitarbeiter, "Kein Mitarbeiter")
    beginndatum =  check_date(form, 'bg',
                                "Fehler im Zuständigkeitsbeginndatum")
    zust.setDate('bg',
                 beginndatum)
    # Kann 0 sein, 0 als Default
    endedatum = check_date(form, 'e',
                           "Fehler im Zuständigkeitsendedatum", Date(0,0,0),
                           maybezero = 1)
    zust.setDate('e', endedatum)
    if endedatum < beginndatum:
        raise EE("Zuständigkeitsende vor Beginn")
    aktzustold = check_exists(form, 'aktuellzustid' ,
                              Zustaendigkeit, "Kein aktueller Zustand")
    aktzust_endedatum = aktzustold.getDate('e')
    if beginndatum < aktzustold.getDate('bg'):
        raise EE("Zuständigkeitsbeginn vor Beginn der aktuellen Zuständigkeit")
    aktzust = Zustaendigkeit()
    aktzust.setDate('e', beginndatum)
    try:
        zust.insert(zustid)
        aktzustold.update(aktzust)
    except:
        try: zust.delete()
        except: pass
        
    _stamp_akte(zust['akte'])
    
    ##
    ## Es ist immer genau ein Mitarbeiter pro Zeiteinheit zustaendig.
    ## 1. Ueberschneidungen (groesser 1 Tag, weil Ende u. Beginndatum
    ## identisch ist) Fehler ebenso wenn 2 Mitarbeiter gleichzeitig
    ##  aktuell zustaendig sind.
    ## 3. Aelteste Zustaendigkeit sollte mit Fallbeginn identisch sein
    ##    (Rueckmelden).
    


    
def updzust(form):
    """Update der Zuständigkeit."""
    
    zustold  = check_exists(form, 'zustid', Zustaendigkeit,
                            "Keine Zustaendigksid")
    prevold = zustold['prev']
    nextold = zustold['next']
    fall = zustold['fall']
    zust = Zustaendigkeit()
    prev = Zustaendigkeit()
    next = Zustaendigkeit()
    # Soll tatsächlich der Mitarbeiter für eine Zuständigkeit wechseln können?
    zust['mit_id'] = check_fk(form, 'mitid', Mitarbeiter, "Fehler in Mitarbeiter", zustold)
    beginndatum = check_date(form, 'bg', "Fehler im Beginndatum", zustold)
    if prevold:
        if beginndatum <= prevold.getDate('bg'):
            raise EE('Beginndatum muss nach dem Beginn der letzten Zuständigkeit sein')
    else:
        # erste Zuständigkeit
        if beginndatum != fall.getDate('bg'):
            raise EE('Erste Zuständigkeit muss mit dem Fall beginnen')
    prev.setDate('e', beginndatum)
    zust.setDate('bg', beginndatum)
    endedatum = check_date(form, 'e', "Fehler im Enddatum",
                           zustold, maybezero = 1)
    if endedatum <= beginndatum:
        raise EE("Zuständigkeitsende muss nach dem Beginn sein")
        # msg-systems ag , brehmea 2002 23.01
        # nicht updatebale, weil sonst grobe fehler passieren koennen. keine zustid
        #zust.setDate('bg', beginndatum)
        #zust.setDate('e', endedatum)
        
    if nextold:
        if endedatum >= nextold.getDate('e'):
            raise EE('Endedatum muss vor dem Ende der folgenden Zuständigkeit sein')
    else:
        # erste Zuständigkeit
        if endedatum != fall.getDate('zda'):
            raise EE('Letzte Zuständigkeit muss mit dem Fall enden')
    next.setDate('bg', endedatum)
    zust.setDate('e', endedatum)
    zustold.update(zust)
    if prevold:
        prevold.update(prev)
    if nextold:
        nextold.update(next)
    _stamp_akte(zustold['akte'])
    
    
def dokeinf(form):
    """Neues Dokument."""
    
    import os
    
    dokid = check_int_not_empty(form, 'dokid', "dokid fehlt")
    check_not_exists(dokid, Dokument,
      "Dokument-ID (id: %(id)s) existiert bereits")
    dok = Dokument()
    dok['fall_id'] = check_fk(form, 'fallid', Fall, "Kein Fall")
    fall = dok['fall']
    akteold = fall['akte']
    dok['mit_id'] = check_fk(form, 'mitid', Mitarbeiter, "Kein Mitarbeiter")
    dok['betr'] = check_str_not_empty(form, 'betr', "Kein Betreff")
    dok['art'] = check_code(form, 'art', 'dokart', "Text ist: fehlt")
    dok['mtyp'] = cc('mimetyp','txt')
    dok['fname'] = '%s.txt' % dokid
    dok['zeit'] = int(time.time())
    dok.setDate('v',
                  check_date(form, 'v',
                             "Fehler im Datum"))
    text = check_str_not_empty(form, 'text', "Kein Text")
    akte_path = mk_akte_dir(akteold['id'])
    
    try:
        f = open('%s/%s' % (akte_path, dok['fname']), 'w')
        f.write(text)
        f.close()
        akte_path = get_akte_path(akteold['id'])
        os.chmod('%s/%s' % (akte_path, dok['fname']), 0600)
    except Exception, args:
        raise EBUpdateError("Fehler beim Anlegen der Datei: %s" % str(args))
    try:
        dok.insert(dokid)
    except Exception, args:
        try: dok.delete()
        except: pass
        raise EBUpdateError("Fehler beim Einfügen in die Datenbank: %s" % str(args))
        
    _stamp_akte(dok['akte'])
    
    
def updvermeinf(form):
    """Text ändern."""
    
    import os
    dokold = check_exists(form, 'dokid', Dokument, "Dokument-Id fehlt")
    dok = Dokument()
    dok['fall_id'] = check_fk(form, 'fallid', Fall, "Kein Fall", dokold)
    dok['mit_id'] = check_fk(form, 'mitid', Mitarbeiter,
                             "Kein Mitarbeiter", dokold)
    dok['betr'] = check_str_not_empty(form, 'betr', "Kein Betreff", dokold)
    dok['art'] = check_code(form, 'art', 'dokart', "Text ist: fehlt", dokold)
    dok['zeit'] = int(time.time())
    dok.setDate('v',
                check_date(form, 'v',
                           "Fehler im Datum"))
    if not is_binary(dokold):
        dok['mtyp'] = cc('mimetyp','txt')
        dok['fname'] = '%s.txt' % dokold['id']
        text = check_str_not_empty(form, 'text', "Kein Text")
        fall = Fall(dok['fall_id'])
        akteold = fall['akte']
        fname = os.path.join(get_akte_path(akteold['id']),
                             dok['fname'])
        try:
            f = open(fname, 'w+')
            f.write(text)
            f.close()
            os.chmod(fname,0600)
        except Exception, args:
            raise EBUpdateError("Fehler beim Anlegen der Datei: %s" % str(args))
    dokold.update(dok)
    _stamp_akte(dokold['akte'])
    
    
def removedoks(form):
    """Dokument löschen."""
    
    import os
    dokids = check_list(form, 'dokids', "Keinen Eintrag markiert?")
    for d in dokids:
        try:
            dok = Dokument(int(d))
            fall = Fall(dok['fall_id'])
            akteold = fall['akte']
            akte_path = get_akte_path(akteold['id'])
            os.remove('%s/%s' % (akte_path, dok['fname']))
            akte = Akte()
            akte['zeit'] = int(time.time())
            akteold.update(akte)
            dok.delete()
        except Exception, args:
            raise EBUpdateError("Fehler beim Loeschen, id: %s" % str(args))
            
            
def uploadeinf(form):
    """Upload eines Dokumentes."""
    
    import os
    
    if form.has_key('datei'):
        #print form.items()
        dokid = check_int_not_empty(form, 'dokid', "Dokumentenid fehlt")
        check_not_exists(dokid, Dokument,
                         "Dokument (id: %(id)s) existiert bereits")
        dok = Dokument()
        dok['fall_id'] = check_fk(form, 'fallid', Fall, "Kein Fall")
        fall = Fall(dok['fall_id'])
        akteold = fall['akte']
        dok['mit_id'] = check_fk(form, 'mitid', Mitarbeiter, "Kein Mitarbeiter")
        dok['betr'] = check_str_not_empty(form, 'betr', "Kein Betreff")
        dok['art'] = check_code(form, 'art', 'dokart', "Text ist: fehlt")
        dok.setDate('v',
                      check_date(form, 'v',
                               "Fehler im Datum"))
        dok['zeit'] = int(time.time())
        
        try:
            headers = form['datei'].headers
            if headers.has_key('Content-Type'):
                ctype = headers['Content-Type']
        except Exception, args:
            raise EE("Keine Dateiheaders erhalten: %s" % str(args))
            
        try:
            fname_orig = form['datei'].filename
        except Exception, args:
            raise EE("Kein Dateiname erhalten: %s" % str(args))
            
            #
            # Netscape sendet: Content-Type: application/xxx
            # Opera sendet: Content-Type: application/xxx; name="filename.ext"
            # Der Mime Typ wird hier nur von der .ext abgeleitetet !
            #
            
        try:
            i = string.rindex(fname_orig, '.')
            ext = fname_orig[i+1:]
            dok['mtyp'] = cc('mimetyp', '%s' % ext)
            ##       content_type = form['datei'].headers['Content-Type']
            ##       dok['mtyp'] = cn('mimetyp', content_type)
            dok['fname'] = '%s.%s' % (dokid, ext)
        except Exception, args:
            raise EE("Kein passendes Dateiformat (Mime Typ). %s" % str(args))
            
        try:
            f = open('%s/%s' % (mk_akte_dir(akteold['id']), dok['fname']), 'wb')
        except Exception, args:
            raise EBUpdateError("Fehler beim Oeffnen der Datei. %s" % str(args))
        try:
            f.write(form['datei'].read())
        except Exception, args:
            raise EBUpdateError("Fehler beim Speichern der Datei. %s" % str(args))
        try:
            f.close()
        except Exception, args:
            raise EBUpdateError("Fehler beim Schliessen der Datei. %s" % str(args))
        try:
            akte_path = get_akte_path(akteold['id'])
        except Exception, args:
            raise EBUpdateError("Fehler beim Finden des Dateipfades. %s" % str(args))
        try:
            os.chmod('%s/%s' % (akte_path, dok['fname']) ,0600)
        except Exception, args:
            raise EBUpdateError("Fehler beim Anlegen der Datei: %s" % str(args))
        try:
            dok.insert(dokid)
        except Exception, args:
            try: dok.delete()
            except: pass
            raise EBUpdateError("Fehler beim Einfügen in die Datenbank: %s" % str(args))
            
        _stamp_akte(dok['akte'])
        
        
def zdaeinf(form):
    """Neu z.d.A., Aktenabschluss."""
    
    fallold = check_exists(form, 'fallid', Fall, "Kein Fall")
    zustold = check_exists(form, 'aktuellzustid', Zustaendigkeit,
                        "Keine aktuelle Zuständigkeit")
    zdadatum =  check_date(form, 'zda',
                                "Fehler im zdA-Datum")
    fallende = fallold.getDate('zda')
    if fallende != Date(0,0,0):
        raise EE("Fall ist bereits zdA")
    zustende = zustold.getDate('e')
    if zustende != Date(0,0,0):
        raise EE("Zuständigkeit für Fall ist bereits beendet")
    if zdadatum < zustold.getDate('bg'):
        raise EE("z.d.A.-Datum liegt vor Zuständigkeitsbeginn")
        
    fall = Fall()
    fall.setDate('zda', zdadatum)
    fall['status'] = cc('stand', 'zdA')
    zust = Zustaendigkeit()
    zust.setDate('e', zdadatum)
    fstatl = FachstatistikList(where = 'fall_id = %d' % fallold['id'])
    
    if len(fstatl) == 1:
        fs = fstatl[0]
        if fs['jahr'] != zdadatum.year:
            raise EE("Jahr der Fachstatistik entspricht nicht dem Jahr des Fallabschlusses")
    elif len(fstatl) > 1:
        raise EE("Mehr als 1 Fachstatistik für Fallnummer '%s', " % fallold['fn']
                 + "'%d' vorhanden." % fall['zday'] )
    else:
        raise EE("Keine Fachstatistik für Fallnummer '%s', " % fallold['fn'])
        
##     jghstatl = JugendhilfestatistikList(where = 'fall_id = % d' % fallold['id'] )
##     if len(jghstatl) == 1:
##         pass
##     elif len(jghstatl) > 1:
##         raise EE("Mehr als eine Jugendhilfestatistik für Fallnummer '%(fn)s' vorhanden." % fallold )
##     else:
##         raise EE("Keine Jugendhilfestatistik für Fallnummer '%(fn)s' vorhanden" % fallold )
    jgh = fallold['jgh']
    if jgh and isinstance(jgh, Jugendhilfestatistik2007):
        if jgh['hda'] == cc('ja_nein', '1'):
            raise EE("Die vorhandene Jugendhilfestatistik ist nicht für einen abgeschlossenen Fall.")
        if jgh['jahr'] != zdadatum.year:
            raise EE("Jahr der Bundesstatistik entspricht nicht dem Jahr des Fallabschlusses")
    if not jgh:
        raise EE("Keine Jugendhilfestatistik für Fallnummer '%(fn)s' vorhanden" % fallold )
    akteold = fallold['akte']
    letzter_fall = akteold['letzter_fall']
    leistungen = LeistungList(where = 'fall_id = %s and ed=0 and em=0 and ey=0' % letzter_fall['id'])
    for s in leistungen:
        leist = Leistung()
        leist.setDate('e', zdadatum)
        s.update(leist)
        
    zustold.update(zust)
    fallold.update(fall)
    _stamp_akte(fallold['akte'])
    


def _check_fallbeginn(fall, fallbeginn):
    faelle = fall['akte__faelle'].sorted('bgy', 'bgm', 'bgd')
    i = faelle.index(fall)
    if i > 0:
        # nicht der erste Fall
        if fallbeginn < faelle[i-1].getDate('zda'):
            raise EE('Fallbeginn vor Ende des vorherigen Falls')
    zustaendigkeiten = fall['zustaendigkeiten'].sorted('bgy', 'bgm', 'bgd')
    if fallbeginn > zustaendigkeiten[0].getDate('e'):
            raise EE('Fallbeginn nach Ende der ersten Zuständigkeit')
    for leist in fall['leistungen']:
        if leist.getDate('bg') < fallbeginn:
            raise EE('Fallbeginn nach Beginn der ersten Leistung')
            
            
    
def updfall(form):
    """Update Fall."""
    fallold = check_exists(form, 'fallid', Fall, "Keine Fallid")
    erste_zustold = fallold['zustaendigkeiten'].sorted('bgy', 'bgm', 'bgd')[0]
    fall = Fall()
    zust = Zustaendigkeit()
    fallbeginn = check_date(form, 'bg', "Fehler im Fallbeginndatum", fallold)
    _check_fallbeginn(fallold, fallbeginn)
    fall.setDate('bg', fallbeginn)
    zust.setDate('bg', fallbeginn)
    # Das soll wohl hier nicht geändert werden
    # fall['status'] = 236
    
    fallold.update(fall)
    erste_zustold.update(zust)
    _stamp_akte(fallold['akte'])
    
    
def zdareinf(form):
    """z.d.A. rückgängig machen."""
    
    # es werden nur das Fallendedatum und das Zuständigkeitsende wieder auf offen
    # gesetzt. Keine neue Zuständigkeit.
    fallold = check_exists(form, 'fallid', Fall, "Keine Fallid")
    zustold = fallold['zuletzt_zustaendig']
    fall = Fall()
    zust = Zustaendigkeit()
    fall.setDate('zda', Date(0,0,0))
    zust.setDate('e', Date(0,0,0))
    fall['status'] = cc('stand', 'l')
    fallold.update(fall)
    zustold.update(zust)
    _stamp_akte(fallold['akte'])
    
    
def waufneinf(form):
    """Wiederaufnahme der Akte."""
    
    akteold = check_exists(form, 'akid', Akte, "Aktenid fehlt")
    stelle = Code(akteold['stzbg'])
    akte = Akte()
    akte['na'] = check_str_not_empty(form, 'na', "Kein Name", akteold)
    akte['gs'] = check_code(form,'gs', 'gs',
                            "Keine Geschlechtsangabe")
    akte['gb'] = str(check_date(form, 'gb', 'Fehler im Geburtsdatum'))
##     akte['gb'] = check_str_not_empty(form, 'gb',
##                                      "Kein Geburtsdatum", akteold)
    get_string_fields(akte, form,
                      ['vn', 'ber', 'tl1', 'tl2', 'no'], akteold)
    akte['fs'] = check_code(form,'fs', 'fsfs',
                            "Fehler im Familienstatus", akteold)
    setAdresse(akte, form)
    fallid = check_int_not_empty(form, 'fallid', "Fallid fehlt")
    
    letzter_fall = akteold['letzter_fall']
    fall = Fall()
    fall['akte_id'] = check_fk(form, 'akid', Akte,
                              "Keine Aktenid für Fall")
    # Fallbeginn ist identisch mit Zuständigkeitsbeginn
    fall.setDate('bg',
                 check_date(form, 'zubg',
                            "Fehler im Datum für den Zuständigkeitsbeginn"))
    if fall.getDate('bg') <= letzter_fall.getDate('zda'):
        raise EE('Fallbeginn muss nach Abschluss des letzten Falls liegen')
    fall.setDate('zda', Date(0,0,0))
    fall['fn'] = getNewFallnummer(stelle['code'], fall['bgy'])
    fall['status'] = cc('stand', 'l')
    
    zust = Zustaendigkeit()
    zust['mit_id'] = check_fk(form, 'zumitid', Mitarbeiter,
                              "Kein zuständiger Mitarbeiter für Fall")
    zust.setDate('bg', fall.getDate('bg'))
    zust.setDate('e', Date(0,0,0))
    
    leist = Leistung()
    leist['mit_id'] = check_fk(form, 'lemitid', Mitarbeiter,
                              "Kein zuständiger Mitarbeiter für Leistung")
    leist['le'] = check_code(form, 'le', 'fsle', "Keine Leistungsart")
    leist.setDate('bg',
                  check_date(form, 'lebg',
                             "Fehler im Datum für den Leistungsbeginn"))
    if leist.getDate('bg') < fall.getDate('bg'):
        raise EE("Datum des Leistungs- vor Zustaendigkeitsbeginn")
    leist.setDate('e', Date(0,0,0))
    leist['stz'] = check_code(form, 'lestz', 'stzei',
                              "Kein Stellenzeichen für die Leistung",
                              stelle['id'])
    if config.ANMELDUNGSDATEN_OBLIGATORISCH:
        anm = _check_anmeinf(form)
    
    try:
        akteold.update(akte)
        fall.insert(fallid)
        if config.ANMELDUNGSDATEN_OBLIGATORISCH:
            anm['fall_id'] = fall['id']
            anm.insert()
        zust['fall_id'] = fall['id']
        zust.new()
        zust.insert()
        leist['fall_id'] = fall['id']
        leist.new()
        leist.insert()
    except Exception, args:
        try: fall.delete()
        except: pass
        try: zust.delete()
        except: pass
        try: leist.delete()
        except: pass
        raise EBUpdateError("Fehler beim Einfügen in die Datenbank: %s" % str(args))
    _stamp_akte(akteold)
    

def _fs_check(form, fstat, fstatold=None):
    fstat['mit_id'] = check_fk(form, 'mitid', Mitarbeiter, "Kein Mitarbeiter")
    fstat['jahr'] = check_int_not_empty(form, 'jahr', "Jahr fehlt")
    fstat['stz'] = check_code(form, 'stz', 'stzei',
                              "Kein Stellenzeichen für die Fachstatistik")
    # Regionalinfos übernehmen
    fall_id = fstat['fall_id']
    fall = None
    if fall_id:
        fall = Fall(fall_id)
        akte = fall['akte']
        if (fstatold and not fstatold['ort']) or not fstatold:
            # nicht mehrmals übernehmen, Akte kann sich später geändert habe
            # nur übernehmen, wenn noch nichts eingetragen ist
            for a in ('ort', 'plz', 'plraum'):
                fstat[a] = akte[a]
            if config.STRASSENKATALOG:
                from ebkus.html.strkat import get_strasse
                str = get_strasse(akte)
            else:
                str = {}
            for a in ('ortsteil', 'bezirk', 'samtgemeinde'):
                fstat[a] = str.get(a, '')
    # ab hier abschaltbar
    from ebkus.html.fskonfig import fs_customize as fsc
    multicode = cc('verwtyp', 'm')
    singlecode = cc('verwtyp', 'k')
    for fname in fsc.abschaltbare_items:
        if not fsc.deaktiviert(fname):
            feld = fsc.get(fname) # das Feldobjekt
            verwtyp = feld['verwtyp']
            if verwtyp == singlecode:
                fstat[fname] = check_code(form, fname,
                                          feld['kat_code'],
                                          "Fehlt: %s" % feld['name'])
            elif verwtyp == multicode:
                fstat[fname] = check_multi_code(form, fname,
                                                feld['kat_code'],
                                                "Fehlt: %s" % feld['name'])
            elif fname in ('no', 'no2', 'no3'):
                fstat[fname] = check_str_not_empty(form, fname, "Keine Notiz", '')
            elif fname in ('kat',):
                uebernehmen = form.get('uebernehmen')
                if uebernehmen == '1' and config.BERATUNGSKONTAKTE and not config.BERATUNGSKONTAKTE_BS:
                    # aus Beratungskontakten übernehmen
                    from ebkus.html.beratungskontakt import get_fs_kontakte
                    get_fs_kontakte(fall, fstat)
                else:
                    fstat[fname] = check_int_not_empty(form, fname, "Terminsumme fehlt")
                    for f in fsc.termin_felder:
                        fobj = fsc.get(f)
                        fstat[f] = check_int_not_empty(form, f, "Fehlt: %s" % fobj['name'])
##             elif fname in fsc.termin_felder:
##                 fstat[fname] = check_int_not_empty(form, fname, "Keine Terminanzahl", 0)
    if fall_id and akte:
        akte.akte_undo_cached_fields()

        

def fseinf(form):
    """Neue Fachstatistik."""
    
    fsid = check_int_not_empty(form, 'fsid', "FachstatistikID fehlt")
    
    check_not_exists(fsid, Fachstatistik,
      "Fachstatistik (id: %(id)s, Fallnummer: %(fall_fn)s, Mitarbeiter: %(mit_id__na)s) existiert bereits")
    fstat = Fachstatistik()
    if form['fallid'] != None and form['fallid'] != '':
        fstat['fall_id'] = check_fk(form, 'fallid', Fall, "Kein Fall")
    fstat['fall_fn'] = check_str_not_empty(form, 'fall_fn', "Fallnummer fehlt")
    jahresl = FachstatistikList(where = "fall_fn = '%s'" % fstat['fall_fn'])
    if len(jahresl) >= 1:
        raise EE("Fachstatistik für Fallnummer: '%s' vorhanden" % fstat['fall_fn'])
    _fs_check(form, fstat)
    fstat['zeit'] = int(time.time())
    try:
        fstat.insert(fsid)
    except Exception, args:
        try: fstat.delete()
        except: pass
        raise EBUpdateError("Fehler beim Einfügen in die Datenbank: %s" % str(args))
        
        
def updfs(form):
    """Update der Fachstatistik."""
    
    fstatold = check_exists(form, 'fsid', Fachstatistik, "Fachstatistikid fehlt")
    fstat = Fachstatistik()
    fallid = form.get('fallid')
    if fallid == None or fallid == '' or fallid == 'None':
        fstat['fall_id'] = None
    else:
        fstat['fall_id'] = check_fk(form, 'fallid', Fall, "Kein Fall")
    fstat['fall_fn'] = check_str_not_empty(form, 'fall_fn', "Fallnummer fehlt")
    #fstat['bz'] kann nicht updatet werden
    _fs_check(form, fstat, fstatold=fstatold)
    fstat['zeit'] = int(time.time())
    fstatold.update(fstat)
    ## vgl. Kommentar bei updjgh
    ##
    if fstatold['fall_id'] != None:
        _stamp_akte(fstatold['akte'])
        

def updfskonfig(form):
    """Fachstatistikformular konfigurieren."""
    def set_aktiviert(f_obj, status):
        flag = f_obj['flag']
        if status:
            f_obj.update({'flag': flag&~1})
        else:
            f_obj.update({'flag': flag|1})
    from ebkus.html.fskonfig import fs_customize as fsc
    for f in fsc.abschaltbare_items:
        f_obj = fsc.get(f)
        status = form.get('%s_a' % f)
        set_aktiviert(f_obj, status)
        if f == 'kat':
            # alle Terminfelder richten sich nach kat, der Summe
            for t in fsc.termin_felder:
                t_obj = fsc.get(t)
                set_aktiviert(t_obj, status)
        if f in fsc.joker_felder:
            label = form.get('%s_l' % f)
            f_obj.update({'name': label})
            kat_id = form.get('%s_k' % f)
            kat = Kategorie(kat_id)
            f_obj.update({'kat_code': kat['code']})
            f_obj.update({'kat_id': kat['id']})
#         if f in fsc.joker_frei:
#             mehrfach = form.get('%s_m' % f)
#             if mehrfach:
#                 f_obj.update({'verwtyp': cc('verwtyp', 'm')})
#             else:
#                 f_obj.update({'verwtyp': cc('verwtyp', 'k')})
        if f in fsc.joker_frei:
            mehrfach = form.get('%s_m' % f)
            flag = f_obj['flag']
            # Präsenz von bit 2 signalisiert einfach
            if mehrfach:
                f_obj.update({'flag': flag&~2})
            else:
                f_obj.update({'flag': flag|2})

    
def jgheinf(form):
    """Jugendhilfestatistik."""
    
    jghid = check_int_not_empty(form, 'jghid', "JugendhilfestatistikID fehlt")
    check_not_exists(jghid, Jugendhilfestatistik,
        "Jugendhilfestatistik (id: %(id)s, Fallnummer: %(fall_fn)s, Mitarbeiter: %(mit_id__na)s, Fall: %(fall_id)s ) existiert bereits")
    
    jghstat = Jugendhilfestatistik()
    fallid = form.get('fallid')
    if fallid == None or fallid == '' or fallid == 'None':
        jghstat['fall_id'] = None
    else:
        jghstat['fall_id'] = check_fk(form, 'fallid', Fall, "Kein Fall")
        check_unique(jghstat['fall_id'], JugendhilfestatistikList, 'fall_id',"Fallid gibt es bereits")

    jghstat['mit_id'] = check_fk(form, 'mitid', Mitarbeiter,
                                 "Kein Mitarbeiter")
    jghstat['fall_fn'] = check_str_not_empty(form, 'fall_fn',
                                             "Fallnummer fehlt")
    check_unique(jghstat['fall_fn'], JugendhilfestatistikList, 'fall_fn',"Fallnummer gibt es bereits")

    jghl = JugendhilfestatistikList(where =
                                    "fall_fn = '%s'" % jghstat['fall_fn'])
    if len(jghl) >= 1:
        raise EE("Jugendhilfestatistik für Fallnummer: '%s'" % jghstat['fall_fn']
                  + " existiert bereits.")
    jghstat['stz'] = check_code(form, 'stz', 'stzei',
                              "Kein Stellenzeichen für die Jugendhilfestatistik")
    jghstat['gfall'] = check_code(form, 'gfall', 'gfall',
                                  "Angabe, ob der Fall ein Geschwisterfall ist, fehlt")
    jghstat.setDate('bg',
                 check_date(form, 'bg',
                            "Fehler im Datum für den Beginn", nodayallowed = 1 ) )
    if form['fallid'] != None and form['fallid'] != '':
        fall = Fall(jghstat['fall_id'])
        if fall['bgm'] != jghstat['bgm'] or fall['bgy'] != jghstat['bgy']:
            raise EE("Beginndatum in der Jugendhilfestatistik stimmt mit dem Fallbeginn nicht überein")
    jghstat.setDate('e',
                 check_date(form, 'e',
                            "Fehler im Datum für das Ende", nodayallowed = 1 ) )
    if jghstat.getDate('e') < jghstat.getDate('bg'):
        raise EE("Fallende in der Jugendhilfestatistik liegt vor Fallbeginn")
    if jghstat.getDate('e').year > 2006:
        raise EE("Alte Bundesstatistik für Fallende nach 2006 nicht erlaubt")
    del jghstat['bgd']
    del jghstat['ed']
    jghstat['rbz'] = check_code(form, 'rbz', 'rbz',
                              "Kein Regierungsbezirk" )
    jghstat['kr'] = check_code(form, 'kr', 'kr',
                              "Kein Kreis" )
    jghstat['gm'] = check_code(form, 'gm', 'gm',
                              "Keine Gemeinde")
    jghstat['gmt'] = check_code(form, 'gmt', 'gmt',
                              "Kein Gemeindeteil")
    jghstat['traeg'] = check_code(form, 'traeg', 'traeg',
                              "Kein Traeger" )
    jghstat['bgr'] = check_code(form, 'bgr', 'bgr',
                              "Kein Beendigungsgrund" )
    jghstat['gs'] = check_code(form, 'gs', 'gs',
                              "Kein Geschlecht" )
    jghstat['ag'] = check_code(form, 'ag', 'ag',
                              "Keine Altersgruppe Kind" )
    jghstat['fs'] = check_code(form, 'fs', 'fs',
                              "Feld: 'Junger Mensch lebt bei', fehlt" )
    jghstat['hke'] = check_code(form, 'hke', 'hke',
                              "Keine Staatsangehörigkeit" )
    jghstat['gsu'] = check_code(form, 'gsu', 'gsu',
                              "Feld: 'Geschwister unbekannt', fehlt", '0')
    if form['gsa'] == '' and jghstat['gsu'] == cc('gsu', '0'):
        raise EE("Keine Geschwisterzahl und nicht 'unbekannt' angegeben")
    elif form['gsa'] != '' and jghstat['gsu'] == cc('gsu', '1'):
        raise EE("Geschwisterzahl und 'unbekannt' angegeben")
    if jghstat['gsu'] == cc('gsu', '1'):
        jghstat['gsa'] = None
    else:
        jghstat['gsa'] = check_int_not_empty(form, 'gsa',
                                           "Geschwisterzahl leer")
    jghstat['zm'] = check_code(form, 'zm', 'zm',
                              "Feld: '1. Kontaktaufnahme', fehlt", )
    jghstat['schw'] = check_code(form, 'schw', 'schw',
                              "'Beratungsschwerpunkt' fehlt" )
    if form.get('fbe0') and form.get('fbe1') and (form.get('fbe2') or form.get('fbe3')):
        raise EE("Ingesamt mehr als 2 Ankreuzungen bei 'Beratungsansatz' vorhanden")
    elif not form.get('fbe0') and not form.get('fbe1') and not (form.get('fbe2') or form.get('fbe3')):
        raise EE("Keine Ankreuzung bei 'Beratungsansatz'")
    else:
        jghstat['fbe0'] = check_code(form, 'fbe0', 'fbe0',
                                 "Beratungsansatz 'Kind' leer", '0')
        jghstat['fbe1'] = check_code(form, 'fbe1', 'fbe1',
                                 "Beratungsansatz 'Eltern' leer", '0')
        jghstat['fbe2'] = check_code(form, 'fbe2', 'fbe2',
                                 "Beratungsansatz 'Familie' leer", '0')
        jghstat['fbe3'] = check_code(form, 'fbe3', 'fbe3',
                                 "Beratungsansatz 'soziales Umfeld' leer", '0')
        
    ba = check_list(form, 'ba', "Keinen Beratunganlass angegeben")
    if len(ba) > 2:
        raise EE("Mehr als 2 Beratungsanlässe markiert")
    for b in ba:
        jghstat['ba0'] = int(b)
        if jghstat['ba0'] == cc('ba0', '1'):
            break
        else: jghstat['ba0'] = cc('ba0', '0')
    for b in ba:
        jghstat['ba1'] = int(b)
        if jghstat['ba1'] == cc('ba1', '1'):
            break
        else: jghstat['ba1'] = cc('ba1', '0')
    for b in ba:
        jghstat['ba2'] = int(b)
        if jghstat['ba2'] == cc('ba2', '1'):
            break
        else: jghstat['ba2'] = cc('ba2', '0')
    for b in ba:
        jghstat['ba3'] = int(b)
        if jghstat['ba3'] == cc('ba3', '1'):
            break
        else: jghstat['ba3'] = cc('ba3', '0')
    for b in ba:
        jghstat['ba4'] = int(b)
        if jghstat['ba4'] == cc('ba4', '1'):
            break
        else: jghstat['ba4'] = cc('ba4', '0')
    for b in ba:
        jghstat['ba5'] = int(b)
        if jghstat['ba5'] == cc('ba5', '1'):
            break
        else: jghstat['ba5'] = cc('ba5', '0')
    for b in ba:
        jghstat['ba6'] = int(b)
        if jghstat['ba6'] == cc('ba6', '1'):
            break
        else: jghstat['ba6'] = cc('ba6', '0')
    for b in ba:
        jghstat['ba7'] = int(b)
        if jghstat['ba7'] == cc('ba7', '1'):
            break
        else: jghstat['ba7'] = cc('ba7', '0')
    for b in ba:
        jghstat['ba8'] = int(b)
        if jghstat['ba8'] == cc('ba8', '1'):
            break
        else: jghstat['ba8'] = cc('ba8', '0')
    for b in ba:
        jghstat['ba9'] = int(b)
        if jghstat['ba9'] == cc('ba9', '1'):
            break
        else: jghstat['ba9'] = cc('ba9', '0')
        


    jghstat['zeit'] = int(time.time())
    
    try:
        jghstat.insert(jghid)
    except Exception, args:
        try: jghstat.delete()
        except: pass
        raise EBUpdateError("Fehler beim Einfügen in die Datenbank: %s" % str(args))
        

def raise_if_int(form, keys, error_message):
    for k in keys:
        v = form.get(k)
        found = False
        try:
            vi = int(v)
            found = True
        except (ValueError, TypeError):
            pass
        if found:
            raise EE(error_message)

def _jgh07_check(form, jgh):
    """Jugendhilfestatistik prüfen sowohl für Einführung als auch für Update."""
    from ebkus.html.jghstatistik import _fb_data
    try:
        fall_id = check_fk(form, 'fallid', Fall, "Kein Fall")
        fall = Fall(fall_id)
    except:
        # es muss keinen Fall geben, z.B. falls dieser schon gelöscht wurde
        fall = None
    jgh['jahr'] = jahr = check_int_not_empty(form, 'jahr', 'Kein Jahr')
    if jahr > today().year:
        raise EE('Fehler im Jahr: zu weit in der Zukunft')
    jgh['stz'] = check_code(form, 'stz', 'stzei',
                            "Kein Stellenzeichen für die Jugendhilfestatistik")
    jgh['mit_id'] = check_fk(form, 'mitid', Mitarbeiter,
                                 "Kein Mitarbeiter")
    jgh['land'] = check_code(form, 'land', 'land',
                            "Kein Land")
    jgh['kr'] = check_code(form, 'kr', 'kr',
                            "Kein Kreis")
    jgh['einrnr'] = check_code(form, 'einrnr', 'einrnr',
                            "Keine Einrichtungsnummer")
    jgh['gfall'] = check_code(form, 'gfall', 'gfall',
                                  "Angabe, ob der Fall ein Geschwisterfall ist, fehlt")
    # wird auf True gesetzt, wenn das entsprechende item mit ja beantwortet wurde    
    hilfe_dauert_an = False 
    # Kategorienitems werden über die Daten in jghstatistik._fb_data abgehandelt
    for a in _fb_data:
        if isinstance(a, basestring):
            continue
        lfb = a['abschnitt']
        title = a['title']
        if lfb == 'K':
            _jgh07_check_abschnitt_K(form, jgh)
        else:
            for i in a['items_data']:
                if isinstance(i, basestring):
                    continue
                typ = i['typ'][0]
                name = i['name']
                frage = i['frage']
                if typ == 'kat':
                    kat_code = i['typ'][1]
                    item_kennzeichung = "%s / %s / %s" % (lfb, title, frage)
                    if name == 'hda' and str(form.get('hda')) == str(cn('ja_nein', 'ja')):
                        hilfe_dauert_an = True
                    if hilfe_dauert_an and name in ('lbk6m', 'grende', 'aort_nac', 'unh'):
                        raise_if_int(form, (name,),
                                     "Nur bei beendeter Hilfe ausfüllen: %s" %
                                     item_kennzeichung)
                        jgh[name] = None
                    else:
                        jgh[name] = check_code(form, name, kat_code,
                                   "Fehlt: %s" % item_kennzeichung)
    jgh['zustw'] = form.get('zustw') or ' '
    # Datumsangaben direkt abhandeln
    jgh.setDate('ge',
                check_date(form, 'ge',
                           "Fehler in E / Geburtsdatum", nodayallowed = 1 ) )
    del jgh['ged']
    jgh.setDate('bg',
                check_date(form, 'bg',
                           "Fehler im Datum für den Beginn", nodayallowed = 1 ) )
    if fall and (fall['bgy'] > jgh['bgy'] or
                 (fall['bgy'] == jgh['bgy'] and fall['bgm'] > jgh['bgm'])):
        raise EE("Beginndatum in der Jugendhilfestatistik vor Fallbeginn")
    if jahr < jgh['bgy']:
        raise EE("Fehler im Jahr: liegt vor Fallbeginn")
    if hilfe_dauert_an:
        raise_if_int(form, ('ey', 'em'),
                     "Nur bei beendeter Hilfe ausfüllen: L / Ende der Hilfe / Datum")
        jgh['ey'] = jgh['em'] = None
    else:
        jgh.setDate('e',
                    check_date(form, 'e',
                               "Fehler in L / Ende der Hilfe / Datum", nodayallowed = 1 ) )
        if jgh.getDate('e') < jgh.getDate('bg'):
            raise EE("Fallende in der Jugendhilfestatistik liegt vor Fallbeginn")
        if jgh.getDate('e') < Date(2007):
            raise EE("Neue Bundesstatistik für Fallende vor 2007 nicht erlaubt")
        if jgh.getDate('e').year != jahr:
            raise EE("Jahr des Endes der Beratung nicht gleich dem Jahr")
            
        del jgh['ed']
    del jgh['bgd']
    # Beratungskontakte direkt abhandeln
    item_J = "J / Intensität / Zahl der Beratungskontakte"
    item_M = "M / Betreuungsintensität / Zahl der Beratungskontakte"
    nbkakt = nbkges = None
    if config.BERATUNGSKONTAKTE:
        from ebkus.html.beratungskontakt import get_jgh_kontakte
        nbkakt, nbkges = get_jgh_kontakte(fall, jahr)
    #print 'DEFAULTS', nbkakt, nbkges
    if hilfe_dauert_an:
        jgh['nbkakt'] = check_int_not_empty(form, 'nbkakt',
                            "Fehlt: %s" % item_J, default=nbkakt)
        raise_if_int(form, ('nbkges',),
                     "Nur bei beendeter Hilfe ausfüllen: %s" % item_M)
        jgh['nbkges'] = None
        assert isinstance(jgh['nbkakt'], (int, long))
        if jgh['nbkakt'] < 1:
            raise EE("Es muss mindestens 1 Beratungskontakt geben: %s" % item_J)
    else:
        jgh['nbkges'] = check_int_not_empty(form, 'nbkges',
                            "Fehlt: %s" % item_M, default=nbkges)
        raise_if_int(form, ('nbkakt',),
                     "Nur bei andauernder Hilfe ausfüllen: %s" % item_J)
        jgh['nbkakt'] = None
        assert isinstance(jgh['nbkges'], (int, long))
        if jgh['nbkges'] < 1:
            raise EE("Es muss mindestens 1 Beratungskontakt geben: %s" % item_M)
    if fall:
        fall['akte'].akte_undo_cached_fields()

def _jgh07_check_abschnitt_K(form, jgh):
    item_K = "K / Gründe für die Hilfegewährung"
    m1 = "Mehr als ein Hauptgrund"
    m2 = "Mehr als ein 2. Grund"
    m3 = "Mehr als ein 3. Grund"
    k1 = "Kein Hauptgrund"
    k2 = "Kein 2. Grund"
    v = "Hauptgrund, 2. Grund und 3. Grund müssen unterschiedlich sein"
    found = True # falls das auf False gesetzt wird und danach wieder auf True --> Fehler
    for g, m in zip(('gr1', 'gr2', 'gr3'), (m1, m2, m3)):
        g_val = form.get(g)
        if isinstance(g_val, list):
            if len(g_val) > 1:
                raise EE("%s in %s" % (m, item_K))
            if g_val:
                g_val = g_val[0]
        if g_val:
            if not found:
                raise EE("%s in %s" % (k2, item_K))
            jgh[g] = check_code(form, g, 'gruende', "Fehler in %s" % item_K)
            found = jgh[g]
        else:
            if g == 'gr1':
                raise EE("%s in %s" % (k1, item_K))
            found = False
    v1, v2, v3 = jgh.get('gr1'), jgh.get('gr2'), jgh.get('gr3')
    if (v1 and (v1 == v2 or v1 == v3)) or (v2 and v2 == v3):
        raise EE("%s in %s" % (v, item_K))
    

def jgh07einf(form):
    """Jugendhilfestatistik 2007."""
    
    jghid = check_int_not_empty(form, 'jghid', "JugendhilfestatistikID fehlt")
    check_not_exists(jghid, Jugendhilfestatistik2007,
        "Jugendhilfestatistik (id: %(id)s, Fallnummer: %(fall_fn)s, Mitarbeiter: %(mit_id__na)s, Fall: %(fall_id)s ) existiert bereits")
    jgh = Jugendhilfestatistik2007()
    # Zur Einführung muss ein Fall vorhanden sein.
    # Evt. kann dieser später gelöscht werden, ohne dass die Statistik
    # selbst gelöscht wird.
    # Der Fall (fall_id und fall_fn) kann später nicht mehr verändert werden.
    jgh['fall_id'] = check_fk(form, 'fallid', Fall, "Kein Fall")
    jgh['fall_fn'] = check_str_not_empty(form, 'fall_fn',
                                         "Fallnummer fehlt")
    check_unique(jgh['fall_fn'], Jugendhilfestatistik2007List,
                 'fall_fn',
                 "Jugendhilfestatistik für Fallnummer '%s'" % jgh['fall_fn']
                  + " existiert bereits.")
    check_unique(jgh['fall_id'], Jugendhilfestatistik2007List,
                 'fall_id',
                 "Jugendhilfestatistik für Fall-ID '%s'" % jgh['fall_id']
                 + " existiert bereits.")
##     print 'EBUPD VOR _jgh07_check form', form
##     print 'EBUPD VOR _jgh07_check jgh', jgh
    _jgh07_check(form, jgh)
##     print 'EBUPD NACH _jgh07_check form', form
##     print 'EBUPD NACH _jgh07_check jgh', jgh
    jgh['zeit'] = int(time.time())
    try:
        jgh.insert(jghid)
        #print 'EBUPD INSERT erfolgreich'
        from ebkus.db.sql import SQL
        #print SQL("select * from jghstat07 order by ey").execute()
    except Exception, args:
        try: jgh.delete()
        except: pass
        raise EBUpdateError("Fehler beim Einfügen in die Datenbank: %s" % str(args))
        


def _jgh_get_letzte_laufende_nummer():
    letzte = letzte2007 = 0
    jghstatliste2007 = Jugendhilfestatistik2007List(where = 'lnr > 0', order = 'lnr')
    jghstatliste = JugendhilfestatistikList(where = 'lnr > 0', order = 'lnr')
    if jghstatliste:
        letzte = jghstatliste[-1]['lnr']
    if jghstatliste2007:
        letzte2007 = jghstatliste2007[-1]['lnr']
    return max(letzte, letzte2007)

def jgh_laufende_nummer_setzen():
    """Erteilt jeder Jugendhilfestatistik eine laufende Nummer.
    Im Prinzip kann in einer alten Statistik eine höhere Nummer stehen
    als in einer neuen, was aber selten vorkommen dürfte.
    """

    letzte = _jgh_get_letzte_laufende_nummer()
    jghstatliste = JugendhilfestatistikList(where = 'lnr IS NULL', order = 'id')
    for j in jghstatliste:
        letzte += 1
        j.update({'lnr': letzte})
    jghstatliste = Jugendhilfestatistik2007List(where = 'lnr IS NULL', order = 'id')
    for j in jghstatliste:
        letzte += 1
        j.update({'lnr': letzte})
    return letzte

def upgrade_jgh(id, old2new):
    """Alte/neue Jugendhilfestatistik durch neue/alte ersetzen.
    Eine vorhandene Jugendstatistik wird durch die alte bzw. neue
    ersetzt, die vom Anwender ausgefüllt werden muss.
    Die neue wird mit jgheinf bzw. jgh07einf angelegt.
    Falls old2new True ist, wird eine alte Bundesstatistik (bis 2006) durch
    eine neue (ab 2007) ersetzt, sonst umgekehrt.

    Das ganze kann ab 2008 auf jeden Fall gestrichen werden, da dann solche
    Fälle nicht vorkommen dürften.
    """
    import logging
    logging.debug("upgrade_jgh: id=%s old2new=%s" % (id,old2new))
    try:
        if old2new:
            jgh = Jugendhilfestatistik(id)
        else:
            jgh = Jugendhilfestatistik2007(id)
    except:
        # nichts zu upgraden
        return
    fall_id = jgh.get('fall_id')
    fall = None
    if fall_id:
        fall = Fall(fall_id)
        if not fall['aktuell']:
            adj = old2new and 'neue' or 'alte'
            raise EE(
                "Ersatz duch %s Bundesstatistik nur möglich für offene Fälle." %
                adj)
        fall_beginn = fall.getDate('bg')
        if not fall_beginn.year <= 2006:
            raise EE("Ersatz duch %s Bundesstatistik nur möglich \
für Fälle von 2006 oder früher." % adj)
    else:
        raise EE(
            "Kein Fall vorhanden. Ersatz durch %s  Bundesstatistik nicht möglich." %
            adj)
    jgh.delete()
    logging.info("upgrade_jgh: %s Jugendhilfestatistik für Fall-Nr. %s gelöscht" %
                 (old2new, fall['fn']))

def updjgh07(form):
    """Update der Jugendhilfestatistik."""
    jghold = check_exists(form, 'jghid', Jugendhilfestatistik2007,
                              "JugendhilfestatistikID fehlt")
    jgh = Jugendhilfestatistik2007()
    _jgh07_check(form, jgh)
    jgh['zeit'] = int(time.time())
    jghold.update(jgh)
    try:
        ## akte_undo_cached_fields() fuehrt zu einem Error, wenn
        ## jgh['fall_id'] = None ist. Daher try-except
        _stamp_akte(jghold['akte'])
    except:
        # kann schief gehen, wenn es keinen Fall gibt
        pass
        
def updjgh(form):
    """Update der Jugendhilfestatistik."""
    
    jghstatold = check_exists(form, 'jghid', Jugendhilfestatistik,
                              "JugendhilfestatistikID fehlt")
    jghstat = Jugendhilfestatistik()
    fallid = form.get('fallid')
    if fallid == None or fallid == '' or fallid == 'None':
        jghstat['fall_id'] = None
    else:
        jghstat['fall_id'] = check_fk(form, 'fallid', Fall, "Kein Fall")

    jghstat['fall_fn'] = check_str_not_empty(form, 'fall_fn',
                                             "Fallnummer fehlt")

    jghstat['stz'] = check_code(form, 'stz', 'stzei',
                              "Kein Stellenzeichen für die Jugendhilfestatistik")
    jghstat['gfall'] = check_code(form, 'gfall', 'gfall',
                                  "Angabe, ob der Fall ein Geschwisterfall ist, fehlt")
    jghstat.setDate('bg', check_date(form, 'bg',
                            "Fehler im Datum für den Beginn", nodayallowed = 1 ) )
    if form['fallid'] != None and form['fallid'] != '':
        fall = Fall(jghstat['fall_id'])
        if fall['bgm'] != jghstat['bgm'] or fall['bgy'] != jghstat['bgy']:
            raise EE("Beginndatum in der Jugendhilfestatistik stimmt mit dem Fallbeginn nicht überein")
    jghstat.setDate('e',
                 check_date(form, 'e',
                            "Fehler im Datum für das Ende", nodayallowed = 1 ) )
    if jghstat.getDate('e') < jghstat.getDate('bg'):
        raise EE("Fallende in der Jugendhilfestatistik liegt vor Fallbeginn")
    if jghstat.getDate('e').year > 2006:
        raise EE("Alte Bundesstatistik für Fallende nach 2006 nicht erlaubt")
    del jghstat['bgd']
    del jghstat['ed']
    jghstat['rbz'] = check_code(form, 'rbz', 'rbz',
                              "Kein Regierungsbezirk", jghstatold)
    jghstat['kr'] = check_code(form, 'kr', 'kr',
                              "Kein Kreis", jghstatold)
    jghstat['gm'] = check_code(form, 'gm', 'gm',
                              "Keine Gemeinde", jghstatold)
    jghstat['gmt'] = check_code(form, 'gmt', 'gmt',
                              "Kein Gemeindeteil", jghstatold)
    jghstat['traeg'] = check_code(form, 'traeg', 'traeg',
                              "Kein Traeger", jghstatold)
    jghstat['bgr'] = check_code(form, 'bgr', 'bgr',
                              "Kein Beendigungsgrund", jghstatold)
    jghstat['gs'] = check_code(form, 'gs', 'gs',
                              "Kein Geschlecht", jghstatold)
    jghstat['ag'] = check_code(form, 'ag', 'ag',
                              "Keine Altersgruppe Kind", jghstatold)
    jghstat['fs'] = check_code(form, 'fs', 'fs',
                              "Feld: 'Junger Mensch lebt bei', fehlt", jghstatold)
    jghstat['hke'] = check_code(form, 'hke', 'hke',
                              "Keine Staatsangehörigkeit", jghstatold)
    
    jghstat['gsu'] = check_code(form, 'gsu', 'gsu',
                              "Feld: 'Geschwister unbekannt', fehlt", '0')
    if form['gsa'] == '' and jghstat['gsu'] == cc('gsu', '0'):
        raise EE("Keine Geschwisterzahl und nicht 'unbekannt' angegeben")
    elif form['gsa'] != '' and jghstat['gsu'] == cc('gsu', '1'):
        raise EE("Geschwisterzahl und 'unbekannt' angegeben")
    if jghstat['gsu'] == cc('gsu', '1'):
        jghstat['gsa'] = None
    else:
        jghstat['gsa'] = check_int_not_empty(form, 'gsa',
                                           "Geschwisterzahl leer")
    jghstat['zm'] = check_code(form, 'zm', 'zm',
                              "Feld: '1. Kontaktaufnahme', fehlt", )
    jghstat['schw'] = check_code(form, 'schw', 'schw',
                              "'Beratungsschwerpunkt' fehlt", )
    if form.get('fbe0') and form.get('fbe1') and (form.get('fbe2') or form.get('fbe3')):
        raise EE("Ingesamt mehr als 2 Ankreuzungen bei 'Beratungsansatz' vorhanden")
    elif not form.get('fbe0') and not form.get('fbe1') and not (form.get('fbe2') or form.get('fbe3')):
        raise EE("Keine Ankreuzung bei 'Beratungsansatz'")
    else:
        jghstat['fbe0'] = check_code(form, 'fbe0', 'fbe0',
                                 "Beratungsansatz 'Kind' leer", '0')
        jghstat['fbe1'] = check_code(form, 'fbe1', 'fbe1',
                                 "Beratungsansatz 'Eltern' leer", '0')
        jghstat['fbe2'] = check_code(form, 'fbe2', 'fbe2',
                                 "Beratungsansatz 'Familie' leer", '0')
        jghstat['fbe3'] = check_code(form, 'fbe3', 'fbe3',
                                 "Beratungsansatz 'soziales Umfeld' leer", '0')
        
##     if form.has_key('ba'):
##         ba = form.get('ba')
##     else: raise EE("Keinen Beratunganlass angegeben")
##     #  print "BERATUNGSANLÄSSE:",ba
##     if type(ba) is type(''):
##         ba = [ba]
    ba = check_list(form, 'ba', "Keinen Beratunganlass angegeben")
    if len(ba) > 2:
        raise EE("Mehr als 2 Beratungsanlässe markiert")
    for b in ba:
        jghstat['ba0'] = int(b)
        if jghstat['ba0'] == cc('ba0', '1'):
            break
        else: jghstat['ba0'] = cc('ba0', '0')
    for b in ba:
        jghstat['ba1'] = int(b)
        if jghstat['ba1'] == cc('ba1', '1'):
            break
        else: jghstat['ba1'] = cc('ba1', '0')
    for b in ba:
        jghstat['ba2'] = int(b)
        if jghstat['ba2'] == cc('ba2', '1'):
            break
        else: jghstat['ba2'] = cc('ba2', '0')
    for b in ba:
        jghstat['ba3'] = int(b)
        if jghstat['ba3'] == cc('ba3', '1'):
            break
        else: jghstat['ba3'] = cc('ba3', '0')
    for b in ba:
        jghstat['ba4'] = int(b)
        if jghstat['ba4'] == cc('ba4', '1'):
            break
        else: jghstat['ba4'] = cc('ba4', '0')
    for b in ba:
        jghstat['ba5'] = int(b)
        if jghstat['ba5'] == cc('ba5', '1'):
            break
        else: jghstat['ba5'] = cc('ba5', '0')
    for b in ba:
        jghstat['ba6'] = int(b)
        if jghstat['ba6'] == cc('ba6', '1'):
            break
        else: jghstat['ba6'] = cc('ba6', '0')
    for b in ba:
        jghstat['ba7'] = int(b)
        if jghstat['ba7'] == cc('ba7', '1'):
            break
        else: jghstat['ba7'] = cc('ba7', '0')
    for b in ba:
        jghstat['ba8'] = int(b)
        if jghstat['ba8'] == cc('ba8', '1'):
            break
        else: jghstat['ba8'] = cc('ba8', '0')
    for b in ba:
        jghstat['ba9'] = int(b)
        if jghstat['ba9'] == cc('ba9', '1'):
            break
        else: jghstat['ba9'] = cc('ba9', '0')
        
    jghstat['zeit'] = int(time.time())
    
    jghstatold.update(jghstat)
    
    ## akte_undo_cached_fields() fuehrt zu einem Error, wenn
    ## jghstat['fall_id'] = None ist.
    ##
    
    fallid = jghstatold.get('fall_id')
    if fallid:
        _stamp_akte(jghstatold['akte'])
        


## def abfreinf(form):
##     from ebkus.html.abfragedef import Query
##     abfr_id =  check_int_not_empty(form, 'abfrid', "ID fehlt")
##     name=check_str_not_empty(form, 'name', "Kein Name")
##     mit_id = check_fk(form, 'mitid', Mitarbeiter, "Kein Mitarbeiter")
##     cgi_name = 'query1' 
##     q = Query(cgi_name, form.get(cgi_name, []))
##     abfr = Abfrage()
##     abfr.init(id=abfr_id,
##               zeit=time.time(),
##               mit_id=mit_id,
##               name=name,
##               dok=self.form.get('dok', ''),
##               value=q.get_query_string(),
##               typ='statistik_teilmengen_definition',
##               )
##     abfr.new()
##     abfr.insert()


def upd_or_einf_abfr(form):
    from ebkus.html.abfragedef import Query
    abfr_id =  form.get('abfrid')
    name=check_str_not_empty(form, 'name', "Kein Name")
    abfrage_list = AbfrageList(where="name = '%s'" % name)
    if len(abfrage_list) > 1:
        raise EE(("Es existieren mehrere Teilmengendefinitionen mit dem Namen '%s'." % name) +
                 "Bitte erst löschen.")
    elif abfrage_list:
        abfrold = abfrage_list[0]
        if abfr_id and int(abfr_id) != abfrold['id']:
            raise EE("Es existiert bereits eine Definition mit dem Namen '%s'." % name)
    else:
        abfrold = None
    mit_id = check_fk(form, 'mitid', Mitarbeiter, "Kein Mitarbeiter")
    cgi_name = 'query1' 
    query1 = check_list(form, cgi_name, 'Keine Query', [])
    q = Query(query1, cgi_name=cgi_name)
    abfr = Abfrage()
    abfr.init(zeit=time.time(),
              mit_id=mit_id,
              name=name,
              dok=form.get('dok', ''),
              value=q.get_query_string(),
              typ='statistik_teilmengen_definition',
              )
    if abfrold:
        abfrold.update(abfr)
    else:
        abfr.new()
        abfr.insert()

## def updabfr(form):
##     from ebkus.html.abfragedef import Query
##     abfr_id =  check_int_not_empty(form, 'abfrid', "ID fehlt")
##     abfrold = Abfrage(abfr_id)
##     name=check_str_not_empty(form, 'name', "Kein Name")
##     mit_id = check_fk(form, 'mitid', Mitarbeiter, "Kein Mitarbeiter")
##     cgi_name = 'query1' 
##     q = Query(cgi_name, form.get(cgi_name, []))
##     abfr = Abfrage()
##     abfr.init(id=abfr_id,
##               zeit=time.time(),
##               mit_id=mit_id,
##               name=name,
##               dok=self.form.get('dok', ''),
##               value=q.get_query_string(),
##               typ='statistik_teilmengen_definition',
##               )
##     abfrold.update(abfr)

def rmabfr(form):
    abfr_id =  check_int_not_empty(form, 'abfrid', "ID fehlt")
    abfrold = Abfrage(abfr_id)
    abfrold.delete()
        
def gruppeeinf(form):
    """Neue Gruppe."""
    
    gruppeid = check_int_not_empty(form, 'gruppeid', "Gruppeid fehlt")
    check_not_exists(gruppeid, Gruppe,
                     "Gruppe (id: %(id)s, Name: %(name)s gibt es in der Datenbank bereits")
    gruppe = Gruppe()
    get_string_fields(gruppe, form, ['gn', 'name', 'thema'], '')
    gruppe['name'] = check_str_not_empty(form, 'name', "Kein Gruppenname")
    gruppe['thema'] = check_str_not_empty(form, 'thema', "Kein Thema")
    gruppe['teiln'] = check_code(form, 'teiln', 'teiln',
                                 "Fehler bei Teilnehmer")
    gruppe['grtyp'] = check_code(form, 'grtyp', 'grtyp',
                                 "Fehler beim Gruppentyp")
    gruppe['stz'] = check_code(form, 'stz', 'stzei',
                               "Kein Stellenzeichen für die Grupp")
    get_int_fields(gruppe, form, ['tzahl', 'stzahl'], None)
    
##     if form.has_key('mitid'):
##         mitid = form.get('mitid')
##     else: raise EE("Keine Mitarbeiter angegeben")
##     #  print "Mitarbeiter:",mitid
##     if type(mitid) is type(''):
##         mitid = [mitid]
    mitid = check_list(form, 'mitid', "Keine Mitarbeiter angegeben")
    # TBD: stimmt das? dürfen beide Daten 0 sein oder in der Zukunft liegen?
    gruppe.setDate('bg', check_date(form, 'bg',
                                    "Fehler im Datum für den Beginn", Date(0,0,0), maybezero = 1, maybefuture=1 ))
    gruppe.setDate('e', check_date(form, 'e',
                                   "Fehler im Datum für das Ende", Date(0,0,0), maybezero = 1, maybefuture=1 ))
    if gruppe.getDate('bg') > gruppe.getDate('e'):
        raise EE('Beginndatum liegt vor Endedatum')
    gruppe['gn'] = getNewGruppennummer(Code(gruppe['stz'])['code'], gruppe['bgy'])
    check_unique(gruppe['gn'], GruppeList, 'gn',
                 "Gruppennummer ist bereits vergeben")
    for m in mitid:
        mitgruppe = MitarbeiterGruppe()
        mitgruppe['mit_id'] = int(m)
        mitgruppe['gruppe_id'] = gruppeid
        mitgruppe.setDate('bg', gruppe.getDate('bg'))
        mitgruppe.setDate('e', gruppe.getDate('e'))
        mitgruppe['zeit'] = int(time.time())
        try:
            mitgruppe.new()
            mitgruppe.insert()
        except Exception, args:
            raise EBUpdateError("Fehler beim Einfügen in die Datenbank: %s" % str(args))
            
    gruppe['zeit'] = int(time.time())
    
    try:
        gruppe.insert(gruppeid)
    except Exception, args:
        try: gruppe.delete()
        except: pass
        raise EBUpdateError("Fehler beim Einfügen in die Datenbank: %s" % str(args))
        
        
def updgr(form):
    """Update der Gruppe."""
    
    gruppeold = check_exists(form, 'gruppeid', Gruppe, "Gruppe-Id fehlt")
##     if form.has_key('mitid'):
##         mitid = form.get('mitid')
##     else:
##         raise EE("Keine Mitarbeiter angegeben")
##     if type(mitid) is type(''):
##         mitid = [mitid]
    mitid = check_list(form, 'mitid', "Keine Mitarbeiter angegeben")
    gruppe = Gruppe()
    get_string_fields(gruppe, form, ['gn', 'name', 'thema'], '')
    gruppe['gn'] = check_str_not_empty(form, 'gn',
                                       "Keine Gruppennummer", gruppeold)
    gruppe['name'] = check_str_not_empty(form, 'name', "Kein Gruppenname")
    gruppe['thema'] = check_str_not_empty(form, 'thema', "Kein Thema")
    gruppe['teiln'] = check_code(form, 'teiln', 'teiln',
                                 "Fehler bei Teilnehmer")
    gruppe['grtyp'] = check_code(form, 'grtyp', 'grtyp',
                                 "Fehler beim Gruppentyp")
    gruppe['stz'] = check_code(form, 'stz', 'stzei',
                               "Kein Stellenzeichen für die Gruppe")
    get_int_fields(gruppe, form, ['tzahl', 'stzahl'], None)
    
    gruppe.setDate('bg', check_date(form, 'bg',
                                    "Fehler im Datum für den Beginn",
                                    Date(0,0,0), maybezero = 1, maybefuture=1 ))
    gruppe.setDate('e', check_date(form, 'e',
                                   "Fehler im Datum für das Ende",
                                   Date(0,0,0), maybezero = 1, maybefuture=1 ))
    
    if gruppe.getDate('bg') > gruppe.getDate('e'):
        raise EE('Beginndatum liegt vor Endedatum')
    gruppe['zeit'] = int(time.time())
    
    ##*************************************************************************
    ##
    ##  MastaleckT 07.03.2002
    ##
    ##  Update der Mitarbeiter einer Gruppe
    ##
    ##*************************************************************************
    
    ## Alle alten Mitarbeiter der Gruppe loeschen
    gr_mit_hinzuliste = []
    grp_mitarbeiterliste = MitarbeiterGruppeList(where = 'gruppe_id=%d' %gruppeold['id'])
    for mloesch in grp_mitarbeiterliste:
        mloesch.delete()
    for m in mitid:
        mitgruppe = MitarbeiterGruppe()
        mitgruppe['mit_id'] = int(m)
        mitgruppe['gruppe_id'] = gruppeold['id']
        ## Sollte unterschieden werden bei Mitzuständigkeit später als Gruppenbeginn?
        mitgruppe.setDate('bg', gruppeold.getDate('bg'))
        mitgruppe.setDate('e', gruppeold.getDate('e'))
        mitgruppe['zeit'] = int(time.time())
        try:
            mitgruppe.new()
            mitgruppe.insert()
        except Exception, args:
            raise EBUpdateError("Fehler beim Einfügen in die Datenbank: %s" % str(args))
    try:
        gruppeold.update(gruppe)
    except Exception, args:
        try: gruppe.delete()
        except: pass
        raise EBUpdateError("Fehler beim Einfügen in die Datenbank: %s" % str(args))
    gruppeold.gruppe_undo_cached_fields()
    
    
def dokgreinf(form):
    """Gruppendokument (Text) einfügen."""
    
    import os
    dokid = check_int_not_empty(form, 'dokid', "dokid fehlt")
    check_not_exists(dokid, Gruppendokument,
      "Dokument-ID (id: %(id)s) existiert bereits")
    dok = Gruppendokument()
    dok['gruppe_id'] = check_fk(form, 'gruppeid', Gruppe, "Keine Gruppe")
    gruppeold = Gruppe(dok['gruppe_id'])
    dok['mit_id'] = check_fk(form, 'mitid', Mitarbeiter, "Kein Mitarbeiter")
    dok['betr'] = check_str_not_empty(form, 'betr', "Kein Betreff")
    dok['art'] = check_code(form, 'art', 'dokart', "Text ist: fehlt")
    dok['mtyp'] = cc('mimetyp','txt')
    dok['fname'] = '%s.txt' % dokid
    dok['zeit'] = int(time.time())
    dok.setDate('v',
                  check_date(form, 'v',
                             "Fehler im Datum"))
    text = check_str_not_empty(form, 'text', "Kein Text")
    gruppe_path = mk_gruppe_dir(gruppeold['id'])
    
    try:
        f = open('%s/%s' % (gruppe_path, dok['fname']), 'w')
        f.write(text)
        f.close()
        gruppe_path = get_gruppe_path(gruppeold['id'])
        os.chmod('%s/%s' % (gruppe_path, dok['fname']) ,0600)
    except Exception, args:
        raise EBUpdateError("Fehler beim Anlegen der Datei: %s" % str(args))
        
    gruppe = Gruppe()
    gruppe['zeit'] = int(time.time())
    
    try:
        dok.insert(dokid)
        gruppeold.update(gruppe)
    except Exception, args:
        try: dok.delete()
        except: pass
        raise EBUpdateError("Fehler beim Einfügen in die Datenbank: %s" % str(args))
        
    dok['gruppe'].gruppe_undo_cached_fields()
    
    
def updgrvermeinf(form):
    """Update der Gruppe."""
    
    import os
    dokold = check_exists(form, 'dokid', Gruppendokument,
                          "Dokument-Id fehlt")
    dok = Gruppendokument()
    dok['gruppe_id'] = check_fk(form, 'gruppeid', Gruppe,
                                "Keine Gruppe", dokold)
    dok['mit_id'] = check_fk(form, 'mitid', Mitarbeiter,
                             "Kein Mitarbeiter", dokold)
    dok['betr'] = check_str_not_empty(form, 'betr',
                                      "Kein Betreff", dokold)
    dok['art'] = check_code(form, 'art', 'dokart',
                            "Text ist: fehlt", dokold)
    dok.setDate('v',
                  check_date(form, 'v',
                             "Fehler im Datum"))
    dok['zeit'] = int(time.time())
    gruppeold = Gruppe(dok['gruppe_id'])
    if not is_binary(dokold):
        dok['mtyp'] = cc('mimetyp','txt')
        dok['fname'] = '%s.txt' % dokold['id']
        text = check_str_not_empty(form, 'text', "Kein Text")
        gruppe_path = get_gruppe_path(gruppeold['id'])
        fname = os.path.join(gruppe_path, dok['fname'])
        try:
            f = open(fname, 'w+')
            f.write(text)
            f.close()
            os.chmod(fname,0600)
        except Exception, args:
            raise EBUpdateError("Fehler beim Anlegen der Datei: %s" % str(args))
        
    dokold.update(dok)
    gruppe = Gruppe()
    gruppe['zeit'] = int(time.time())
    gruppeold.update(gruppe)
    dokold['gruppe'].gruppe_undo_cached_fields()
    
    
def uploadgreinf(form):
    """Upload eines Gruppendokumentes."""
    
    #  import mimetypes
    import os
    
    if form.has_key('datei'):
        dokid = check_int_not_empty(form, 'dokid', "Dokumentenid fehlt")
        check_not_exists(dokid, Gruppendokument,
        "Dokument (id: %(id)s) existiert bereits")
        dok = Gruppendokument()
        dok['gruppe_id'] = check_fk(form, 'gruppeid', Gruppe, "Keine Gruppe")
        gruppeold = Gruppe(dok['gruppe_id'])
        dok['mit_id'] = check_fk(form, 'mitid', Mitarbeiter, "Kein Mitarbeiter")
        dok['betr'] = check_str_not_empty(form, 'betr', "Kein Betreff")
        dok['art'] = check_code(form, 'art', 'dokart', "Text ist: fehlt")
        dok.setDate('v',
                      check_date(form, 'v',
                               "Fehler im Datum"))
        dok['zeit'] = int(time.time())
        
        try:
            headers = form['datei'].headers
            if headers.has_key('Content-Type'):
                ctype = headers['Content-Type']
        except Exception, args:
            raise EE("Keine Dateiheaders erhalten: %s" % str(args))
            
            # Netscape sendet: Content-Type: application/xxx
            # Opera sendet: Content-Type: application/xxx; name="filename.ext"
            # Der Mime Typ wird hier nur von der .ext abgeleitetet !
            
        try:
            fname_orig = form['datei'].filename
        except Exception, args:
            raise EE("Kein Dateiname erhalten: %s" % str(args))
            
        try:
            i = string.rindex(fname_orig, '.')
            ext = fname_orig[i+1:]
            dok['mtyp'] = cc('mimetyp', '%s' % ext)
            ##      content_type = form['datei'].headers['Content-Type']
            ##      dok['mtyp'] = cn('mimetyp', content_type)
            dok['fname'] = '%s.%s' % (dokid, ext)
        except Exception, args:
            raise EE("Kein passendes Dateiformat (Mime Typ). %s" % str(args))
            
        try:
            f = open('%s/%s' % (mk_gruppe_dir(gruppeold['id']), dok['fname']), 'wb')
        except Exception, args:
            raise EBUpdateError("Fehler beim Oeffnen der Datei. %s" % str(args))
        try:
            f.write(form['datei'].read())
        except Exception, args:
            raise EBUpdateError("Fehler beim Speichern der Datei. %s" % str(args))
        try:
            f.close()
        except Exception, args:
            raise EBUpdateError("Fehler beim Schliessen der Datei. %s" % str(args))
        try:
            gruppe_path = get_gruppe_path(gruppeold['id'])
        except Exception, args:
            raise EBUpdateError("Fehler beim Finden des Dateipfades. %s" % str(args))
        try:
            os.chmod('%s/%s' % (gruppe_path, dok['fname']) ,0600)
        except Exception, args:
            raise EBUpdateError("Fehler beim Setzen der Dateirechte: %s" % str(args))
            
        gruppe = Gruppe()
        gruppe['zeit'] = int(time.time())
        
        try:
            dok.insert(dokid)
            gruppeold.update(gruppe)
        except Exception, args:
            try: dok.delete()
            except: pass
            raise EBUpdateError("Fehler beim Einfügen in die Datenbank: %s" % str(args))
            
        dok['gruppe'].gruppe_undo_cached_fields()
        
        
def gruppeteilneinf(form):
    """Neuer Gruppenteilnehmer."""
    
    mitid = check_int_not_empty(form, 'mitid', "Mitarbeiterid fehlt")
    gruppeid = check_int_not_empty(form, 'gruppeid', "Gruppeid fehlt")
    gruppeold = Gruppe(gruppeid)
    
    fallid = check_list(form, 'fallid', '', [])
    bezugspid = check_list(form, 'bezugspid', '', [])
    if not fallid and not bezugspid:
        raise EE("Keine TeilnehmerIn angegeben")
    for f in fallid:
        fallgruppel = FallGruppeList(where = 'gruppe_id = %s and fall_id = %s'
                                     % (gruppeid, f))
        if len(fallgruppel) > 0:
            # das muss nicht gemeldet werden
            #raise EE("Klient wird schon als Teilnehmer geführt")
            continue
        fallgruppe = FallGruppe()
        fallgruppe['fall_id'] = f
        fallgruppe['gruppe_id'] = gruppeid
        fallgruppe.setDate('bg', check_date(form, 'bg',
            "Fehler im Datum für den Beginn", Date(0,0,0), maybezero = 1, maybefuture = 1 ))
        fallgruppe.setDate('e', check_date(form, 'e',
          "Fehler im Datum für das Ende", Date(0,0,0), maybezero = 1, maybefuture = 1 ))
        if fallgruppe.getDate('bg') > fallgruppe.getDate('e'):
            raise EE('Beginndatum liegt vor Endedatum')

        fallgruppe['zeit'] = int(time.time())
        try:
            fallgruppe.new()
            fallgruppe.insert()
        except Exception, args:
            raise EBUpdateError("Fehler beim Einfügen in die Datenbank: %s" % str(args))
                
    for b in bezugspid:
        bezugspgruppel = BezugspersonGruppeList(where =                                               'gruppe_id = %s and bezugsp_id = %s' % (gruppeid, b))
        if len(bezugspgruppel) > 0:
            # das muss nicht gemeldet werden
            #raise EE("Bezugsperson wird schon als Teilnehmer geführt")
            continue
        bezugspgruppe = BezugspersonGruppe()
        bezugspgruppe['bezugsp_id'] = b
        bezugspgruppe['gruppe_id'] = gruppeid
        bezugspgruppe.setDate('bg', check_date(form, 'bg',
           "Fehler im Datum für den Beginn", Date(0,0,0), maybezero = 1 ))
        bezugspgruppe.setDate('e', check_date(form, 'e',
           "Fehler im Datum für das Ende", Date(0,0,0), maybezero = 1 ))
        bezugspgruppe['zeit'] = int(time.time())
        if bezugspgruppe.getDate('bg') > bezugspgruppe.getDate('e'):
            raise EE('Beginndatum liegt vor Endedatum')
        try:
            bezugspgruppe.new()
            bezugspgruppe.insert()
        except Exception, args:
            raise EBUpdateError("Fehler beim Einfügen in die Datenbank: %s" % str(args))
                
    gruppe = Gruppe()
    gruppe['zeit'] = int(time.time())
    gruppeold.update(gruppe)
    
    gruppeold.gruppe_undo_cached_fields()
    
    
def removeteiln(form):
    """Gruppenteilnehmer löschen."""
    
    gruppeid = check_int_not_empty(form, 'gruppeid', "Gruppe-Id fehlt")
    fallgr_id = check_list(form, 'fallgrid', '', [])
    bzpgr_id = check_list(form, 'bzpgrid', '', [])
    if not (fallgr_id or bzpgr_id):
        raise EE("Keine TeilnehmerIn zum Löschen markiert")
    for f in fallgr_id:
        fallgr = FallGruppe(f)
        fallgr.delete()
    for b in bzpgr_id:
        bzpgr = BezugspersonGruppe(b)
        bzpgr.delete()
    gruppeold = Gruppe(gruppeid)
    gruppe = Gruppe()
    gruppe['zeit'] = int(time.time())
    gruppeold.update(gruppe)

## def removeteiln(form):
##     """Gruppenteilnehmer löschen."""
    
##     gruppeid = check_int_not_empty(form, 'gruppeid', "Gruppe-Id fehlt")
##     fallgr_id = form.get('fallgrid')
##     bzpgr_id = form.get('bzpgrid')
##     if not (fallgr_id or bzpgr_id):
##         raise EE("Keine TeilnehmerIn zum Löschen markiert")
##     if fallgr_id:
##         if type(fallgr_id) is type(''):
##             fallgr_id = [fallgr_id]
##         for f in fallgr_id:
##             try:
##                 fallgr = FallGruppe(f)
##                 fallgr.delete()
##             except Exception, args:
##                 raise EBUpdateError("Fehler beim Löschen in der Datenbank: %s" % str(args))
                
##     if bzpgr_id:
##         if type(bzpgr_id) is type(''):
##             bzpgr_id = [bzpgr_id]
##         for b in bzpgr_id:
##             try:
##                 bzpgr = BezugspersonGruppe(b)
##                 bzpgr.delete()
##             except Exception, args:
##                 raise EBUpdateError("Fehler beim Löschen in der Datenbank: %s" % str(args))
                
##     gruppeold = Gruppe(gruppeid)
##     gruppe = Gruppe()
##     gruppe['zeit'] = int(time.time())
    
##     gruppeold.update(gruppe)
    
    
def updgrteiln(form):
    """Update des Gruppenteilnehmers."""
    
    if form.has_key('fallgrid'):
        fallgrold = check_exists(form, 'fallgrid', FallGruppe, "Kein Teilnehmer")
        gruppeold = fallgrold['gruppe']
        fallgr = FallGruppe()
        fallgr.setDate('bg', check_date(form, 'bg',
                                        "Fehler im Datum für den Beginn",
                                        (0,0,0), # Datum darf leer sein
                                        maybezero = 1, maybefuture = 1 ))
        fallgr.setDate('e', check_date(form, 'e',
                                       "Fehler im Datum für das Ende",
                                       (0,0,0), maybezero = 1,
                                       maybefuture = 1 ))
        fallgr['zeit'] = int(time.time())
        if fallgr.getDate('bg') > fallgr.getDate('e'):
            raise EE('Beginndatum liegt vor Endedatum')
        fallgrold.update(fallgr)
        gruppe = Gruppe()
        gruppe['zeit'] = int(time.time())
        gruppeold.update(gruppe)
        gruppeold.gruppe_undo_cached_fields()
        
    elif form.has_key('bzpgrid'):
        bezpgrold = check_exists(form, 'bzpgrid',
                                 BezugspersonGruppe, "Kein Teilnehmer")
        bezp = Bezugsperson(bezpgrold['bezugsp_id'])
        gruppeold = bezpgrold['gruppe']
        bezpgr = BezugspersonGruppe()
        bezpgr.setDate('bg', check_date(form, 'bg',
                                        "Fehler im Datum für den Beginn",
                                        (0,0,0), maybezero = 1,
                                        maybefuture = 1 ))
        bezpgr.setDate('e', check_date(form, 'e',
                                       "Fehler im Datum für das Ende",
                                       (0,0,0), maybezero = 1,
                                       maybefuture = 1 ))
        if bezpgr.getDate('bg') > bezpgr.getDate('e'):
            raise EE('Beginndatum liegt vor Endedatum')
        bezpgr['zeit'] = int(time.time())
        
        bezpgrold.update(bezpgr)
        gruppe = Gruppe()
        gruppe['zeit'] = int(time.time())
        gruppeold.update(gruppe)
        gruppeold.gruppe_undo_cached_fields()
    else:
        raise EE("keine Teilnehmer-ID erhalten.")
        
        
def removegrdoks(form):
    """Gruppendokument löschen."""
    
    import os
    dokids = check_list(form, 'dokids', "Keinen Eintrag markiert?")
    for d in dokids:
        try:
            dok = Gruppendokument(int(d))
            gruppeold = Gruppe(dok['gruppe_id'])
            gruppe_path = get_gruppe_path(gruppeold['id'])
            os.remove('%s/%s' % (gruppe_path, dok['fname']))
            gruppe = Gruppe()
            gruppe['zeit'] = int(time.time())
            gruppeold.update(gruppe)
            dok.delete()
        except Exception, args:
            raise EBUpdateError("Fehler beim Loeschen, id: %s" % str(args))
            
            #refresh des Cache?
            #Duplikat der Geloeschten Datensaetze und Dateien?
            #
            
            
def miteinf(form):
    """Neuer Mitarbeiter."""
    
    mitid = check_int_not_empty(form, 'mitid', "Mitarbeiterid fehlt")
    check_not_exists(mitid,
                     Mitarbeiter,
                     "Mitarbeiter (id: %(id)s, Vorname: %(vn)s, Name: %(na)s) gibt es in der DB bereits")
    
    mit = Mitarbeiter()
    get_string_fields(mit, form, ['vn', 'na'],'')
    mit['na'] = check_str_not_empty(form, 'na', "Kein Name")
    mit['ben'] = check_str_not_empty(form, 'ben', "Kein Benutzername")
    mit['ben'] = check_unique(mit['ben'], MitarbeiterList, 'ben',
                      "Benutzername ist schon vorhanden. Muss einmalig sein")
    mit['vn'] = check_str_not_empty(form, 'vn', "Kein Vorname")
    mit['stat'] = check_code(form, 'stat', 'status', "Fehler beim Status")
    mit['stz'] =  check_code(form, 'stz', 'stzei',
                             "Fehler beim Stellenzeichen")
    mit['benr'] =  check_code(form, 'benr', 'benr',
                              "Fehler bei den Benutzerrechten")
    mit['zeit'] = int(time.time())
    ##########################################################################################
    #
    # 13.09.2001 msg, TM
    #
    # Beim Anlegen eines Benutzers wird von nun an standardmaessig der benutzername als
    # default - Passwort in die Datenbank geschrieben. Die Benutzer muessen ihr Passwort
    # nach dem ersten Anmelden selbst aendern.
    # brehmea(msg) 13.09.2001 mit sha-encodierung
    ##########################################################################################
    s = sha.new(check_str_not_empty(form, 'ben', "Kein Benutzername"))
    mit['pass'] = s.hexdigest()
    
    try:
        mit.insert(mitid)
    except Exception, args:
        try: pers.delete()
        except: pass
        raise EBUpdateError("Fehler beim Einfügen in die Datenbank: %s" % str(args))
        
        
def updmit(form):
    """Update Mitarbeiter."""
    
    mitold = check_exists(form, 'mitid', Mitarbeiter, "Mitarbeiterid fehlt")
    mit = Mitarbeiter()
    
    get_string_fields(mit, form, ['vn', 'na'],'')
    mit['na'] = check_str_not_empty(form, 'na', "Kein Name")
    mit['ben'] = check_str_not_empty(form, 'ben', "Kein Benutzer")
    if mitold['ben'] != mit['ben']:
        mit['ben'] = check_unique(mit['ben'], MitarbeiterList, 'ben',
                        "Benutzername ist schon vorhanden. Muss einmalig sein")
    mit['vn'] = check_str_not_empty(form, 'vn', "Kein Vorname", mitold)
    mit['stat'] = check_code(form, 'stat', 'status',
                             "Fehler beim Status", mitold)
    mit['stz'] =  check_code(form, 'stz', 'stzei',
                             "Fehler beim Stellenzeichen", mitold)
    # TODO: Stellenzeichenänderung nur als Fehlerkorrektur zulassen
    if mit['stz'] != mitold['stz']:
        from ebkus.app import ebapi
        for klassname in (
            'LeistungList',
            'MitarbeiterberatungskontaktList',
            'Fua_BSList',
            'ZustaendigkeitList',
            'DokumentList',
            'GruppendokumentList',
            'MitarbeiterGruppeList',
            'FachstatistikList',
            'JugendhilfestatistikList',
            'Jugendhilfestatistik2007List',
            'AbfrageList',
            ):
            res = getattr(ebapi, klassname)(where='mit_id = %(id)s' % mitold)
            if res:
                raise EE(
                    'Es sind bereits Daten mit diesem Mitarbeiter vorhanden.<br />'
                    'Ein Stellenwechsel ist nur möglich zur Fehlerkorrektur '
                    'direkt nachdem der Mitarbeiter in EBKuS angelegt wurde.')
    if (str(form.get('changepassword')) == '1'):
        s = sha.new(check_str_not_empty(form, 'ben', "Kein Benutzername"))
        mit['pass'] = s.hexdigest()
        
    mit['benr'] =  check_code(form, 'benr', 'benr',
                              "Fehler bei den Benutzerrechten", mitold)
    mit['zeit'] = int(time.time())
    
    mitold.update(mit)
    undo_cached_fields()
    
    
def codeeinf(form):
    """Neuer Code."""
    
    codeid = check_int_not_empty(form, 'codeid', "Merkmalsid fehlt")
    check_not_exists(codeid, Code,
                     "Code (id: %(id)s, Code: %(code)s, Kategoriencode: %(kat_code)s, Name: %(name)s) gibt es bereits")
    code = Code()
    code['code'] = check_str_not_empty(form, 'code', "Merkmalscode fehlt")
    code['kat_code'] = check_str_not_empty(form, 'katcode',
                                           "Kategoriencode fehlt")

    try:
        c = Code(code=code['code'], kat_code=code['kat_code'])
        raise EBUpdateDataError("Code %(code)s existiert bereits" % c)
    except dbapp.DBAppError:
        # Ok, existiert nicht
        pass
    #code['kat_id'] = Kategorie(code=code['kat_code'])['id']
    code['kat_id'] = check_fk(form, 'katid', Kategorie, 
                              "Kategorienid fehlt",
                              Kategorie(code=code['kat_code'])['id'])
    code['name'] = check_str_not_empty(form, 'name', "Merkmalsname fehlt")
    if form.get('mini') or form.get('maxi') or code['kat_code'] == 'dbsite':
        code['mini'] = check_int_not_empty(form, 'mini',
                                         "Fehler bei Bereichsminimum")
        code['maxi'] = check_int_not_empty(form, 'maxi',
                                         "Fehler bei Bereichsmaximum")
        if code['mini'] > code['maxi']:
            raise EE("Maximum ist kleiner als Minimum")
    else:
        code['mini'] = None
        code['maxi'] = None
    code['off'] = check_int_not_empty(form, 'off', 'Item off leer', 0)
    code['dok'] = check_str_not_empty(form, 'dok', "Dokumentation fehlt", '')
    code['sort'] = check_int_not_empty(form, 'sort', "Sortierangabe fehlt")
    code['dm'] = None
    code['dy'] = None
    _check_code(code)
    codeliste = CodeList(where = "kat_code = '%s'" % code['kat_code']
                         + 'and sort >= %d' % code['sort'], order = 'sort')
    if codeliste:
    
        for c in codeliste:
            cneu = Code()
            x = c['sort']
            cneu['sort'] = x + 1
            c.update(cneu)
            
    code['zeit'] = int(time.time())
    
    try:
        code.insert(codeid)
    except Exception, args:
        try: code.delete()
        except: pass
        raise EBUpdateError("Fehler beim Einfügen in die Datenbank: %s" % str(args))
        

def _check_code(code):
    # kr 3-stellig
    kat_code = code['kat_code']
    code = code['code']
    if kat_code in ('kr', 'land', 'einrnr') and not code.isdigit():
        raise EE("Code muss aus Ziffern bestehen")
    if kat_code == 'kr' and len(code) != 3:
        raise EE("Code für Kreis muss dreistellig sein (Ziffer 3-5 des amtlichen Gemeindeschlüssel (AGS)")
    elif kat_code == 'land' and len(code) != 2:
        raise EE("Code für Land muss zweistellig sein (Ziffer 1-2 des amtlichen Gemeindeschlüssel (AGS)")
    elif kat_code == 'einrnr' and len(code) != 6:
        raise EE("Code für Einrichtungsnummer muss sechsstellig sein")

def updcode(form):
    """Update des Code."""
    
    codeold = check_exists(form, 'codeid', Code, "Merkmalsid fehlt")
    code = Code()
    code['code'] = check_str_not_empty(form, 'code',
                                       "Merkmalscode fehlt", codeold['code'])
    code['kat_code'] = check_str_not_empty(form, 'katcode',
                                           "Kategoriencode fehlt", codeold['kat_code'])
# orig
    code['kat_id'] = check_fk(form, 'katid', Kategorie,
                              "Kategorienid fehlt", codeold['kat_id'])
#    code['kat_id'] = codeold
    code['name'] = check_str_not_empty(form, 'name',
                                       "Merkmalsname fehlt", codeold)
    if form.get('mini') or form.get('maxi') or code['kat_code'] == 'dbsite':
        code['mini'] = check_int_not_empty(form, 'mini',
                                         "Minimum des Bereichs fehlt")
        code['maxi'] = check_int_not_empty(form, 'maxi',
                                         "Maximum des Bereichs fehlt")
        if code['mini'] > code['maxi']:
            raise EE("Minimum ist grösser als Maximum")
    else:
        code['mini'] = None
        code['maxi'] = None
    code['off'] = check_int_not_empty(form, 'off', 'Item off leer', 0)
    code['sort'] = check_int_not_empty(form, 'sort',
                                       "Sortierangabe fehlt", codeold)
    code['dok'] = check_str_not_empty(form, 'dok', "Dokumentation fehlt",
                                      codeold)
    if form['dm'] != '':
        code['dm'] = check_int_not_empty(form, 'dm',
                                       "Fehler beim Ungültigkeitsdatum",)
        if code['dm'] < 1 or code['dm'] > 12:
            raise EE("Fehler beim Monat")
    else:
        code['dm'] = None
    if form['dy'] != '':
        code['dy'] = check_int_not_empty(form, 'dy',
                                       "Fehler beim Ungültigkeitsdatum", )
        if code['dy'] < 1000:
            raise EE("Keine 4 Ziffern beim Jahr")
    else:
        code['dy'] = None
        
    _check_code(code)
    x = code['sort']
    y = codeold['sort']
    
    code['zeit'] = int(time.time())
    codeold.update(code)
    
    # Korrektur der Sortierreihenfolge der Codes nach Aenderungen
    if x != y:
        codeliste = CodeList(where = "kat_id = %d" % codeold['kat_id']
                             + ' and sort = %d' % x , order = 'sort')
        for c in codeliste:
            if x > y and c['id'] != codeold['id']:
                cneu = Code()
                cneu['sort'] = c['sort'] - 1
                c.update(cneu)
            elif x < y  and c['id'] != codeold['id']:
                cneu = Code()
                cneu['sort'] = c['sort'] + 1
                c.update(cneu)
                
        codeliste = CodeList(where = "kat_id = %d" % codeold['kat_id'], order = 'sort')
        i = 0;
        for c in codeliste:
            i = i + 1
            cneu = Code()
            if c['sort'] == i:
                pass
            else:
                cneu['sort'] = i
                c.update(cneu)
    flush_cache()
            

def updkategorie(form):
    kat = check_exists(form, 'katid', Kategorie, "Kategorienid fehlt")
    name = check_str_not_empty(form, 'name', 'Kein Name', '')
    dok  = check_str_not_empty(form, 'dok', 'Keine Doku', '')
    kat.update({'name': name, 'dok': dok})
    from ebkus.db.dbapp import undo_cached_fields
    undo_cached_fields()
    


def remove_akte(akte, statistik_auch=False, aktuell_auch=False):
    akte_id = akte['id']
    for fall in akte['faelle']:
        remove_fall(fall, statistik_auch, aktuell_auch)
    einrl = EinrichtungskontaktList(where = 'akte_id = %s' % akte_id)
    einrl.deleteall()
    bezugspl = BezugspersonList(where = 'akte_id = %s' % akte_id)
    for  b in bezugspl:
        bezugspgrl = BezugspersonGruppeList(where = 'bezugsp_id = %s' % b['id'])
        bezugspgrl.deleteall()
    bezugspl.deleteall()
    akte_path = get_akte_path(akte_id)
    try:
        os.rmdir('%s' % akte_path)
    except: pass
    akte.delete()
    undo_cached_fields()
    try:
        a = Akte(akte_id)
        assert False, 'Akte wurde nicht gelöscht'
    except:
        pass # alles OK
    return True


def remove_fall(fall, statistik_auch=False, aktuell_auch=False):
    if not aktuell_auch:
        assert not fall['aktuell'], 'Aktueller Fall kann nicht gelöscht werden'
    fall_id = fall['id']
    #print "********* LOESCHEN: %(id)s;%(akte_id)s;%(fn)s" % fall
    jghstatl = JugendhilfestatistikList(where = 'fall_id = %s' % fall_id)
    jgh07statl = Jugendhilfestatistik2007List(where = 'fall_id = %s' % fall_id)
    fachstatl = FachstatistikList(where = 'fall_id = %s' % fall_id)
    dokl = DokumentList(where = 'fall_id = %s' % fall_id)
    zustaendigl = ZustaendigkeitList(where = 'fall_id = %s' % fall_id)
    anmeldungl = AnmeldungList(where = 'fall_id = %s' % fall_id)
    leistungl = LeistungList(where = 'fall_id = %s' % fall_id)
    fallberl = FallberatungskontaktList(where='fall_id = %s' % fall_id)
    fallgrl = FallGruppeList(where = 'fall_id = %s' % fall_id)
    akte_path = get_akte_path(fall['akte_id'])
    for j in jghstatl:
        if statistik_auch:
            j.delete()
        else:
            jghstatold = Jugendhilfestatistik(j['id'])
            jghstat = Jugendhilfestatistik()
            jghstat['fall_id'] = None
            jghstat['zeit'] = int(time.time())
            jghstatold.update(jghstat)
    for j in jgh07statl:
        if statistik_auch:
            j.delete()
        else:
            jghstatold = Jugendhilfestatistik2007(j['id'])
            jghstat = Jugendhilfestatistik2007()
            jghstat['fall_id'] = None
            jghstat['zeit'] = int(time.time())
            jghstatold.update(jghstat)
    for a in fachstatl:
        if statistik_auch:
            a.delete()
        else:
            fachstatold = Fachstatistik(a['id'])
            fachstat = Fachstatistik()
            fachstat['fall_id'] = None
            fachstat['zeit'] = int(time.time())
            fachstatold.update(fachstat)
    for d in dokl:
        try:
            os.remove('%s/%s' % (akte_path, d['fname']))
        except:
            pass
    anmeldungl.deleteall()
    leistungl.deleteall()
    dokl.deleteall()
    fallgrl.deleteall()
    zustaendigl.deleteall()
    # Beratungskontakte werden nur dann gelöscht, wenn sie sich ausschließlich
    # auf den zu löschenden Fall beziehen. Ansonsten wird nur die Beteiligung
    # dieses Falls am Beratungskontakt gelöscht.
    for f in fallberl:
        bkont = f['bkont']
        # alle Beratungskontakte löschen, die sich *nur* auf diesen Fall beziehen
        if len(bkont['fallberatungskontakte']) == 1:
            assert f['id'] == bkont['fallberatungskontakte'][0]['id']
            # für diese auch die Mitarbeiterberatungskontakte löschen
            bkont['mitarbeiterberatungskontakte'].deleteall()
            bkont.delete()
        try: f.delete()
        except: pass # wg. Fehler früherem Fehler kann er sich hier mal verschlucken
    fall.delete()
    undo_cached_fields()
    return True
    

def remove_gruppe(gruppe):
    #print "%(id)s;;%(gn)s" % g
    gruppe_id = gruppe['id']
    gruppe_path = get_gruppe_path(gruppe_id)
    fallgrl = FallGruppeList(where = 'gruppe_id = %s' % gruppe_id)
    bezugspgrl = BezugspersonGruppeList(where = 'gruppe_id = %s' % gruppe_id)
    dokl = GruppendokumentList(where = 'gruppe_id = %s' % gruppe_id)
    mitgrl = MitarbeiterGruppeList(where = 'gruppe_id = %s' % gruppe_id)
    fallgrl.deleteall()
    bezugspgrl.deleteall()
    mitgrl.deleteall()
    for d in dokl:
        try:
            os.remove('%s/%s' % (gruppe_path, d['fname']))
        except:
            pass
    try:
        os.rmdir('%s' % gruppe_path)
    except:
        pass
    dokl.deleteall()
    gruppe.delete()
    return True
    
def removeakten(form):
    """Akten und Gruppen löschen."""
    akten_ids = check_list(form, 'rmak', 'Fehler in zu löschenden Akten', [])
    gruppen_ids = check_list(form, 'rmgr', 'Fehler in zu löschenden Gruppen', [])
    akten = [Akte(id) for id in akten_ids]
    gruppen = [Gruppe(id) for id in gruppen_ids]
    cacheon = cache_is_on()
    try:
        if cache_on:
            cache_off()
        for a in akten:
            remove_akte(a, statistik_auch=False)
        for g in gruppen:
            remove_gruppe(g)
    finally:
        if cacheon:
            cache_on()
    return len(akten), len(gruppen)
    
def _stamp_akte(akteold):
    """Zeitstempel in der Akte setzen und cache zurücksetzen"""
    akte = Akte()
    akte['zeit'] = int(time.time())
    akteold.update(akte)
    akteold.akte_undo_cached_fields()
    

def flush_cache():
    if cache_is_on():
        cache_off()
        cache_on()

def setAdresse(obj, form):
    """Wenn strkat_on gesetzt ist, wird die Ueberpruefung durch den Strassenkatalog
    getriggert.

    Kann auch fuer Bezugspersonenadressen verwendet werden,
    plraum wird dann nicht beruecksichtigt
    """
    #print 'SETADRESSE', form
    from ebkus.html.strkat import fuehrende_nullen_ersetzen
    strkat_on = form.get('strkat_on')
    if strkat_on and config.STRASSENKATALOG:
        from ebkus.html.strkat import get_strassen_list
        try:
            strassen_list = get_strassen_list(form, exact=False)
            if strassen_list != None and len(strassen_list) > 1:
                strassen_list = get_strassen_list(form, exact=True)
        except Exception, e:
            raise EE(str(e))
        #print 'SETADRESSE', strassen_list
        if strassen_list == None:
            raise EE("Keine Adresse.<br /><br />"
                     "Falls Sie ausdrücklich keine Adresse angeben wollen, "
                     "deaktivieren Sie den Abgleich mit dem Straßenkatalog.")
        elif len(strassen_list) < 1:
            raise EE("Kein passender Eintrag für die Adresse "
                     "im Straßenkatalog gefunden.<br /><br />"
                     "Bitte verwenden Sie die Straßensuche,"
                     "oder deaktivieren Sie den Abgleich "
                     "mit dem Straßenkatalog.""")
        elif len(strassen_list) > 1:
            raise EE("Mehrere passende Einträge "
                     "im Straßenkatalog gefunden.<br /><br />"
                     "Bitte wählen Sie mit der Straßensuche "
                     "einen eindeutigen Eintrag aus.""")
        hsnr = form.get('hsnr')
        strasse = strassen_list[0]
        obj['lage'] = cc('lage', '0') 
        obj['ort'] = strasse['ort']
        obj['plz'] = strasse['plz']
        obj['str'] = strasse['name']
        von = strasse['von']
        if von and von == strasse['bis']:
            hsnr = fuehrende_nullen_ersetzen(von)
        if not hsnr:
            raise EE("Keine Hausnummer.<br /><br />"
                     "Falls Sie ausdrücklich keine Hausnummer angeben wollen, <br />"
                     "tragen Sie '---' anstelle der Hausnummer ein.")
        elif hsnr.startswith('-'):
            obj['hsnr'] = '' # erfolgreicher Abgleich ohne Hausnummer
        else:
            obj['hsnr'] = hsnr
        if 'plraum' in obj.fields:
##             # Übernahme des Planungsraums aus dem Straßenkatalogs
##             # Was übernommen wird, ist config-abhängig
##             obj['planungsr'] = strasse[config.PLANUNGSRAUMFELD]
            obj['plraum'] = strasse['plraum']
    else:
        # Ohne Abgleich mit Straßenkatalog
        obj['lage'] = cc('lage', '1')
        ort = form.get('ort', '')
        obj['ort'] = ort
        obj['str'] = form.get('str', '')
        obj['hsnr'] = form.get('hsnr', '')
        obj['plz'] = form.get('plz', '')
        if 'plraum' in obj.fields:
            planungs_raum = form.get('plraum')
            if planungs_raum in ('0',):
                raise EBUpdateDataError("Kein gültiger Planungsraum")
            obj['plraum'] =  planungs_raum or '0'

