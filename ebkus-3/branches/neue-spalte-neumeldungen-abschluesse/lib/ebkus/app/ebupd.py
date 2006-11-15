# coding: latin-1
""" Alle Funktionen, die zu einer Veränderung der Datenbank führen, stehen
hier. """

import time
import sha

from ebkus.app.ebapi import *
from ebkus.app.ebapih import *
from ebkus.config import config


def akteeinf(form):
    """Neue Akte, Fall, Zustaendigkeit"""
    
    akid = check_int_not_empty(form, 'akid', "Aktenid fehlt")
    check_not_exists(akid, Akte,
      "Akte (id: %(id)s, Name: %(na)s, %(vn)s, Geburtsdatum %(gb)s) existiert bereits")
    akte = Akte()
    get_string_fields(akte, form,
          ['vn', 'na', 'gb', 'ber', 'str','hsnr','plz', 'ort', 'tl1', 'tl2', 'no'],'')
    setAdresse(akte, form)
    akte['na'] = check_str_not_empty(form, 'na', "Kein Name")
    akte['gb'] = check_str_not_empty(form, 'gb', "Kein Geburtsdatum")
    akte['fs'] = check_code(form,'fs', 'fsfs',
                            "Fehler im Familienstatus", '999')
    akte['stzbg'] = check_code(form, 'stzbg',
                               'stzei', "Kein Stellenzeichen für die Akte")
    akte['stzak'] = akte['stzbg']
    stelle = Code(akte['stzbg'])
    akte['zeit'] = int(time.time())
    
    fall = Fall()
    # Fallbeginn ist identisch mit Zuständigkeitsbeginn
    fall.setDate('bg',
                 check_date(form, 'zubg',
                            "Fehler im Datum für den Zuständigkeitsbeginn"))
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
        raise EE("Datum des Leistungsbeginn vor Zustaendigkeitsbeginn")
    leist.setDate('e', Date(0,0,0))
    leist['stz'] = check_code(form, 'lestz', 'stzei',
                              "Kein Stellenzeichen für die Leistung",
                              akte['stzbg'])
    
    try:
        akte.insert(akid)
        fall['akte_id'] = akte['id']
        fall.new()
        fall.insert()
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
    akte['gb'] = check_str_not_empty(form, 'gb', "Kein Geburtsdatum", akteold)
    get_string_fields(akte, form,
                      ['vn', 'ber', 'str', 'plz', 'ort',
                       'tl1', 'tl2', 'no'], akteold)
    
    setAdresse(akte, form)
    akte['fs'] = check_code(form,'fs', 'fsfs',
                            "Fehler im Familienstatus", akteold)
    akte['stzbg'] = check_code(form, 'stzbg', 'stzei',
                               "Kein Stellenzeichen für die Akte")
    akte['stzak'] = check_code(form, 'stzak', 'stzei',
                               "Kein aktuelles Stellenzeichen für die Akte")
    akte['zeit'] = int(time.time())
    
    # Werte erst dann übernehmen, wenn keine Fehler aufgetreten sind
    akteold.update(akte)
    akteold.akte_undo_cached_fields()
    
    
def perseinf(form):
    """Neue Bezugsperson."""
    
    bpid = check_int_not_empty(form, 'bpid', "Bezugspersonenid fehlt")
    check_not_exists(bpid, Bezugsperson,
      "Bezugsperson (id: %(id)s, Name: %(na)s, %(vn)s Geburtsdatum %(gb)s) existiert bereits")
    pers = Bezugsperson()
    pers['akte_id'] = check_fk(form, 'akid', Akte, "Keine Akte")
    get_string_fields(pers, form,
                      ['vn', 'na', 'gb', 'ber', 'str',
                       'plz', 'ort', 'tl1', 'tl2', 'no'],'')
    if pers['vn'] == '' and pers['na'] == '':
        raise EE("Kein Name")
        
    setAdresse(pers, form)
    pers['verw'] = check_code(form, 'verw', 'klerv',
                              "Fehler im Verwandtschaftsgrad", '999')
    pers['fs'] = check_code(form,'fs', 'fsfs',
                            "Fehler im Familienstatus", '999')
    pers['nobed'] = check_code(form, 'nobed', 'notizbed',
                               "Fehler in Notizbedeutung", 'f')
    pers['vrt'] = check_code(form, 'vrt', 'vert',
                             "Fehler in Verteiler", 'f')
    
    akteold = pers['akte']
    akte = Akte()
    akte['zeit'] = int(time.time())
    
    try:
        pers.insert(bpid)
        akteold.update(akte)
    except Exception, args:
        try: pers.delete()
        except: pass
        raise EBUpdateError("Fehler beim Einfügen in die Datenbank: %s" % str(args))
        
    pers['akte'].akte_undo_cached_fields()
    
    
def updpers(form):
    """Update der Bezugsperson."""
    
    # unsystematische HACK!!
    fs = form.get('nobed')
    if not fs:
        form['nobed'] = cc('notizbed', 'f')
        
    persold = check_exists(form, 'bpid', Bezugsperson, "Bezugspersonid fehlt")
    pers = Bezugsperson()
    get_string_fields(pers, form,
                      ['vn', 'na', 'gb', 'ber', 'str', 'plz',
                       'ort', 'tl1', 'tl2', 'no','hsnr'],
                      persold)
    if pers['vn'] == '' and pers['na'] == '':
        raise EE("Kein Name")
        
    setAdresse(pers, form)
    pers['verw'] = check_code(form, 'verw', 'klerv',
                              "Fehler im Verwandtschaftsgrad", persold)
    pers['fs'] = check_code(form,'fs', 'fsfs',
                            "Fehler im Familienstatus", persold)
    pers['nobed'] = check_code(form, 'nobed', 'notizbed',
                               "Fehler in Notizbedeutung", persold)
    pers['vrt'] = check_code(form, 'vrt', 'vert',
                             "Fehler in Verteiler", persold)
    
    persold.update(pers)
    akteold = persold['akte']
    akte = Akte()
    akte['zeit'] = int(time.time())
    akteold.update(akte)
    persold['akte'].akte_undo_cached_fields()
    
    
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
                               "Fehler in Notizbedeutung", 'f')
    einr['status'] = check_code(form, 'status', 'einrstat',
                                "Fehler in Einrichtungsstatus", 'ja')
    
    einr.insert(einrid)
    akteold = einr['akte']
    akte = Akte()
    akte['zeit'] = int(time.time())
    akteold.update(akte)
    
    einr['akte'].akte_undo_cached_fields()
    
    
def updeinr(form):
    """Update eines Einrichtungskontaktes."""
    
    # unsystematische HACK!!
    fs = form.get('nobed')
    if not fs:
        form['nobed'] = cc('notizbed', 'f')
        
    einrold = check_exists(form, 'einrid', Einrichtungskontakt, "Einrichtungskontaktid fehlt")
    einr = Einrichtungskontakt()
    get_string_fields(einr, form, ['na','tl1','tl2', 'no'], einrold)
    if einr['na'] == '':
        raise EE("Kein Name")
    einr['insta'] = check_code(form, 'insta', 'klinsta',
                               "Fehler in Institution", einrold)
    einr['nobed'] = check_code(form, 'nobed', 'notizbed',
                               "Fehler in Notizbedeutung", einrold)
    einr['status'] = check_code(form, 'status', 'einrstat',
                                "Fehler in Einrichtungsstatus", einrold)
    
    einrold.update(einr)
    akteold = einrold['akte']
    akte = Akte()
    akte['zeit'] = int(time.time())
    akteold.update(akte)
    
    einrold['akte'].akte_undo_cached_fields()
    
    
def anmeinf(form):
    """Neue Anmeldung."""
    
    anmid = check_int_not_empty(form, 'anmid', "Anmeldungsid fehlt")
    check_not_exists(anmid, Anmeldung,
      "Anmeldung (id: %(id)s, Von: %(von)s) existiert bereits")
    anm = Anmeldung()
    anm['fall_id'] = check_fk(form, 'fallid', Fall, "Kein Fall")
    fall = Fall(anm['fall_id'])
    vorhandene_anmeldung = fall['anmeldung']
    if len(vorhandene_anmeldung) > 0:
        raise EE("Anmeldung für Fall %(fn)s schon vorhanden" % fall)
    get_string_fields(anm, form, ['von','mtl','me', 'mg', 'no'],'')
    
    if anm['von'] == '':
        raise EE("Kein Feld 'von wem gemeldet'")
    anm.setDate('a',
                check_date(form, 'a', "Fehler im Anmeldedatum"))
    anm['zm'] = check_code(form, 'zm', 'fszm', "Fehler im Zugangsmodus")
    
    akteold = anm['akte']
    akte = Akte()
    akte['zeit'] = int(time.time())
    
    try:
        akteold.update(akte)
        anm.insert(anmid)
    except:
        try: anm.delete()
        except: pass
        
    anm['akte'].akte_undo_cached_fields()
    
    
def updanm(form):
    """Update der Anmeldung."""
    
    anmold = check_exists(form, 'anmid', Anmeldung, "Keine Anmeldungsid")
    anm = Anmeldung()
    get_string_fields(anm, form, ['von','mtl','me', 'mg', 'no'], anmold)
    if anm['von'] == '':
        raise EE("Kein Feld 'von wem gemeldet'")
    anmeldedatum = check_date(form, 'a', "Fehler im Anmeldedatum")
    anm.setDate('a', anmeldedatum)
    anm['zm'] = check_code(form, 'zm', 'fszm', "Fehler im Zugangsmodus", anmold)
    
    akteold = anmold['akte']
    akte = Akte()
    akte['zeit'] = int(time.time())
    
    anmold.update(anm)
    akteold.update(akte)
    anmold['akte'].akte_undo_cached_fields()
    
    
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
    
    akteold = fall['akte']
    akte = Akte()
    akte['zeit'] = int(time.time())
    
    try:
        leist.insert(leistid)
        akteold.update(akte)
    except:
        try: leist.delete()
        except: pass
    leist['akte'].akte_undo_cached_fields()
    
    
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
    akteold = fall['akte']
    akte = Akte()
    akte['zeit'] = int(time.time())
    akteold.update(akte)
    
    leistold['akte'].akte_undo_cached_fields()
    
    
def zusteinf(form):
    """Neue Zuständigkeit."""
    
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
    
    aktzust = Zustaendigkeit()
    aktzust.setDate('e', beginndatum)
    akteold = Akte(zust['fall_id__akte_id'])
    akte = Akte()
    akte['zeit'] = int(time.time())
    
    try:
        zust.insert(zustid)
        aktzustold.update(aktzust)
        akteold.update(akte)
    except:
        try: zust.delete()
        except: pass
        
    zust['akte'].akte_undo_cached_fields()
    
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
    zust = Zustaendigkeit()
    
    # Soll tatsächlich der Mitarbeiter für eine Zuständigkeit wechseln können?
    zust['mit_id'] = check_fk(form, 'mitid', Mitarbeiter, "Fehler in Mitarbeiter", zustold)
    beginndatum = check_date(form, 'bg', "Fehler im Beginndatum", zustold)
    endedatum = check_date(form, 'e', "Fehler im Enddatum",
                           zustold, maybezero = 1)
    if endedatum < beginndatum:
        raise EE("Zuständigkeitsende vor Beginn")
        # msg-systems ag , brehmea 2002 23.01
        # nicht updatebale, weil sonst grobe fehler passieren koennen. keine zustid
        #zust.setDate('bg', beginndatum)
        #zust.setDate('e', endedatum)
        
    zustold.update(zust)
    akteold = Akte(zustold['fall_id__akte_id'])
    akte = Akte()
    akte['zeit'] = int(time.time())
    
    akteold.update(akte)
    zustold['akte'].akte_undo_cached_fields()
    
    
def dokeinf(form):
    """Neues Dokument."""
    
    import os
    
    dokid = check_int_not_empty(form, 'dokid', "dokid fehlt")
    check_not_exists(dokid, Dokument,
      "Dokument-ID (id: %(id)s) existiert bereits")
    dok = Dokument()
    dok['fall_id'] = check_fk(form, 'fallid', Fall, "Kein Fall")
    fall = Fall(dok['fall_id'])
    akteold = Akte(fall['akte_id'])
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
        
    akte = Akte()
    akte['zeit'] = int(time.time())
    
    try:
        dok.insert(dokid)
        akteold.update(akte)
    except Exception, args:
        try: dok.delete()
        except: pass
        raise EBUpdateError("Fehler beim Einfügen in die Datenbank: %s" % str(args))
        
    dok['akte'].akte_undo_cached_fields()
    
    
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
    dok['mtyp'] = cc('mimetyp','txt')
    dok['fname'] = '%s.txt' % dokold['id']
    dok.setDate('v',
                  check_date(form, 'v',
                             "Fehler im Datum"))
    text = check_str_not_empty(form, 'text', "Kein Text")
    fall = Fall(dok['fall_id'])
    akteold = Akte(fall['akte_id'])
    akte_path = get_akte_path(akteold['id'])
    
    try:
        f = open('%s/%s' % (akte_path, dok['fname']), 'w+')
        f.write(text)
        f.close()
        os.chmod('%s/%s' % (akte_path, dok['fname']),0600)
    except Exception, args:
        raise EBUpdateError("Fehler beim Anlegen der Datei: %s" % str(args))
        
    dokold.update(dok)
    akte = Akte()
    akte['zeit'] = int(time.time())
    akteold.update(akte)
    dokold['akte'].akte_undo_cached_fields()
    
    
def removedoks(form):
    """Dokument löschen."""
    
    import os
    if form.has_key('dokids'):
        dokids = form.get('dokids')
    else:
        raise EE("Keinen Eintrag markiert?")
        
    if type(dokids) is type(''):
        dokids = [dokids]
    for d in dokids:
        try:
            dok = Dokument(int(d))
            fall = Fall(dok['fall_id'])
            akteold = Akte(fall['akte_id'])
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
        print form.items()
        dokid = check_int_not_empty(form, 'dokid', "Dokumentenid fehlt")
        check_not_exists(dokid, Dokument,
                         "Dokument (id: %(id)s) existiert bereits")
        dok = Dokument()
        dok['fall_id'] = check_fk(form, 'fallid', Fall, "Kein Fall")
        fall = Fall(dok['fall_id'])
        akteold = Akte(fall['akte_id'])
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
            
        akte = Akte()
        akte['zeit'] = int(time.time())
        
        try:
            dok.insert(dokid)
            akteold.update(akte)
        except Exception, args:
            try: dok.delete()
            except: pass
            raise EBUpdateError("Fehler beim Einfügen in die Datenbank: %s" % str(args))
            
        dok['akte'].akte_undo_cached_fields()
        
        
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
        pass
    elif len(fstatl) > 1:
        raise EE("Mehr als 1 Fachstatistik für Fallnummer '%s', " % fallold['fn']
                 + "'%d' vorhanden." % fall['zday'] )
    else:
        raise EE("Keine Fachstatistik für Fallnummer '%s', " % fallold['fn'])
        
    jghstatl = JugendhilfestatistikList(where = 'fall_id = % d' % fallold['id'] )
    if len(jghstatl) == 1:
        pass
    elif len(jghstatl) > 1:
        raise EE("Mehr als eine Jugendhilfestatistik für Fallnummer '%(fn)s' vorhanden." % fallold )
    else:
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
    akteold = fallold['akte']
    akte = Akte()
    akte['zeit'] = int(time.time())
    akteold.update(akte)
    
    fallold['akte'].akte_undo_cached_fields()
    
    
def updfall(form):
    """Update Fall."""
    
    
    fallold = check_exists(form, 'fallid', Fall, "Keine Fallid")
    fall = Fall()
    fallbeginn = check_date(form, 'bg', "Fehler im Fallbeginndatum", fallold)
    fall.setDate('bg', fallbeginn)
    
    # Das soll wohl hier nicht geändert werden
    # fall['status'] = 236
    
    fallold.update(fall)
    akteold = fallold['akte']
    akte = Akte()
    akte['zeit'] = int(time.time())
    akteold.update(akte)
    
    fallold['akte'].akte_undo_cached_fields()
    
    
def zdareinf(form):
    """z.d.A. rückgängig machen."""
    
    fallold = check_exists(form, 'fallid', Fall, "Keine Fallid")
    fall = Fall()
    fall.setDate('zda', Date(0,0,0))
    fall['status'] = cc('stand', 'l')
    zustid = check_int_not_empty(form, 'zustid', "Zuständigkeitsid fehlt")
    check_not_exists(zustid, Zustaendigkeit,
      "Zuständigkeit (id: %(id)s) existiert bereits")
    zust = Zustaendigkeit()
    zust['fall_id'] = check_fk(form, 'fallid', Fall, "Kein Fall")
    zust['mit_id'] = check_fk(form, 'zumitid', Mitarbeiter, "Kein Mitarbeiter")
    beginndatum =  check_date(form, 'bg',
                                "Fehler im Zuständigkeitsbeginndatum")
    zust.setDate('bg', beginndatum)
    zust.setDate('e', Date(0,0,0))
    if fallold.getDate('bg') > zust.getDate('bg'):
        raise EE("Zustaendigkeitsbeginn liegt vor Fallbeginn")
        
    fallold.update(fall)
    zust.insert(zustid)
    akteold = fallold['akte']
    akte = Akte()
    akte['zeit'] = int(time.time())
    akteold.update(akte)
    
    fallold['akte'].akte_undo_cached_fields()
    
    
def waufneinf(form):
    """Wiederaufnahme der Akte."""
    
    akteold = check_exists(form, 'akid', Akte, "Aktenid fehlt")
    akte = Akte()
    akte['na'] = check_str_not_empty(form, 'na', "Kein Name", akteold)
    akte['gb'] = check_str_not_empty(form, 'gb',
                                     "Kein Geburtsdatum", akteold)
    get_string_fields(akte, form,
                      ['vn', 'ber', 'str', 'plz', 'ort',
                       'tl1', 'tl2', 'no'], akteold)
    akte['fs'] = check_code(form,'fs', 'fsfs',
                            "Fehler im Familienstatus", akteold)
    setAdresse(akte, form)
    akte['stzbg'] = check_code(form, 'stzbg', 'stzei', "Kein Stellenzeichen für die Akte")
    akte['stzak'] = akte['stzbg']
    stelle = Code(akte['stzbg'])
    fallid = check_int_not_empty(form, 'fallid', "Fallid fehlt")
    
    fall = Fall()
    fall['akte_id'] = check_fk(form, 'akid', Akte,
                              "Keine Aktenid für Fall")
    # Fallbeginn ist identisch mit Zuständigkeitsbeginn
    fall.setDate('bg',
                 check_date(form, 'zubg',
                            "Fehler im Datum für den Zuständigkeitsbeginn"))
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
                              akte['stzbg'])
    
    akte['zeit'] = int(time.time())
    try:
        akteold.update(akte)
        fall.insert(fallid)
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
    akteold.akte_undo_cached_fields()
    
    
def fseinf(form):
    """Neue Fachstatistik."""
    
    fsid = check_int_not_empty(form, 'fsid', "FachstatistikID fehlt")
    
    check_not_exists(fsid, Fachstatistik,
      "Fachstatistik (id: %(id)s, Fallnummer: %(fall_fn)s, Mitarbeiter: %(mit_id__na)s) existiert bereits")
    fstat = Fachstatistik()
    if form['fallid'] != None and form['fallid'] != '':
        fstat['fall_id'] = check_fk(form, 'fallid', Fall, "Kein Fall")
    fstat['mit_id'] = check_fk(form, 'mitid', Mitarbeiter,
                               "Kein Mitarbeiter")
    fstat['kat'] = check_int_not_empty(form, 'kat',
                                       "Terminsumme fehlt")
    fstat['fall_fn'] = check_str_not_empty(form, 'fall_fn',
                                           "Fallnummer fehlt")
    fstat['jahr'] = check_int_not_empty(form, 'jahr', "Jahr fehlt")
    
    jahresl = FachstatistikList(where = "fall_fn = '%s'" % fstat['fall_fn'])
    
    if len(jahresl) >= 1:
        raise EE("Fachstatistik für Fallnummer: '%s'" % fstat['fall_fn'])
        
    fstat['stz'] = check_code(form, 'stz', 'stzei',
                              "Kein Stellenzeichen für die Fachstatistik")
    fstat['bz'] = form.get('plr')

    fstat['gs'] = check_code(form, 'gs', 'gs',
                              "Kein Geschlecht")
    fstat['ag'] = check_code(form, 'ag', 'fsag',
                              "Keine Altersgruppe Kind")
    fstat['agkm'] = check_code(form, 'agkm', 'fsagel',
                              "Keine Altersgruppe Mutter")
    fstat['agkv'] = check_code(form, 'agkv', 'fsagel',
                              "Keine Altersgruppe Vater")
    fstat['fs'] = check_code(form, 'fs', 'fsfs',
                              "Kein Familienstatus")
    fstat['zm'] = check_code(form, 'zm', 'fszm',
                              "Keine Zugangsart")
    fstat['hkm'] = check_code(form, 'hkm', 'fshe',
                              "Keine Herkunft, Mutter")
    fstat['hkv'] = check_code(form, 'hkv', 'fshe',
                              "Keine Herkunft, Vater" )
    fstat['qualij'] = check_code(form, 'qualij', 'fsqualij',
                              "Keine Qualifikation f&uuml;r Jugendlichen gew&auml;hlt")
    fstat['qualikm'] = check_code(form, 'qualikm', 'fsquali',
                              "Keine Qualifikation f&uuml;r Vater gew&auml;hlt")
    fstat['qualikv'] = check_code(form, 'qualikv', 'fsquali',
                              "Keine Qualifikation f&uuml;r Vater gew&auml;hlt")
    fstat['bkm'] = check_code(form, 'bkm', 'fsbe',
                              "Kein Beruf, Mutter")
    fstat['bkv'] = check_code(form, 'bkv', 'fsbe',
                              "Kein Beruf, Vater fehlt")
    fstat['ba1'] = check_code(form, 'ba1', 'fsba',
                              "Keine Problemlage 1 bei der Anmeldung" )
    fstat['ba2'] = check_code(form, 'ba2', 'fsba',
                              "Keine Problemlage 2 bei der Anmeldung" )
    fstat['pbe'] = check_code(form, 'pbe', 'fspbe',
                              "Keine Hauptproblematik der Eltern" )
    fstat['pbk'] = check_code(form, 'pbk', 'fspbk',
                              "Keine Hauptproblematik Kind" )
    fstat['no'] = check_str_not_empty(form, 'no', "Keine Notiz", '')
    fstat['no2'] = check_str_not_empty(form, 'no2', "Keine Notiz andersgeartete Problemlage Kind", '')
    fstat['no3'] = check_str_not_empty(form, 'no3', "Keine Notiz andersgeartete Problemlage Eltern", '')
    
    #get_int_fields(fstat, form, ['ka'], )
    get_int_fields(fstat, form,
                   ['kkm', 'kkv',
                   'kki', 'kpa', 'kfa', 'ksoz', 'kleh', 'kerz', 'kson','kkonf' ], 0)
    
    if form.has_key('le'):
        le = form.get('le')
    else: raise EE("Keine Massnahme angegeben")
    
    if form.has_key('pbkind'):
        pbk = form.get('pbkind')
    else: raise EE("Kein Problemspektrum für das Kind angegeben")
    
    if form.has_key('pbeltern'):
        pbe = form.get('pbeltern')
    else: raise EE("Kein Problemspektrum für die Eltern angegeben")
    
    #print "LEISTUNGSART:",le
    if type(le) is type(''):
        le = [le]
    for l in le:
        fstatlei = Fachstatistikleistung()
        fstatlei['fstat_id'] = fsid
        fstatlei['le'] = check_code({'le':l},'le', 'fsle', "Keine Leistungsart")
        try:
            fstatlei.new()
            fstatlei.insert()
        except Exception, args:
            raise EBUpdateError("Fehler beim Einfügen in die Datenbank: %s" % str(args))
            
            #print "Problemspektrum:",pbkind
    if type(pbk) is type(''):
        pbk = [pbk]
    for p in pbk:
        fstatpbk = Fachstatistikkindproblem()
        fstatpbk['fstat_id'] = fsid
        fstatpbk['pbk'] = check_code({'pbk':p},'pbk', 'fspbk', "Kein Problemspektrum Kind")
        try:
            fstatpbk.new()
            fstatpbk.insert()
        except Exception, args:
            raise EBUpdateError("Fehler beim Einfügen in die Datenbank: %s" % str(args))
            
            #print "Problemspektrum:",pbeltern
    if type(pbe) is type(''):
        pbe = [pbe]
    for p in pbe:
        fstatpbe = Fachstatistikelternproblem()
        fstatpbe['fstat_id'] = fsid
        fstatpbe['pbe'] = check_code({'pbe':p},'pbe', 'fspbe', "Kein Problemspektrum Eltern")
        try:
            fstatpbe.new()
            fstatpbe.insert()
        except Exception, args:
            raise EBUpdateError("Fehler beim Einfügen in die Datenbank: %s" % str(args))
            
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
    fstat['mit_id'] = check_fk(form, 'mitid', Mitarbeiter, "Kein Mitarbeiter")
    fstat['kat'] = check_int_not_empty(form, 'kat', "Terminsumme fehlt")
    fstat['fall_fn'] = check_str_not_empty(form, 'fall_fn', "Fallnummer fehlt")
    fstat['jahr'] = check_int_not_empty(form, 'jahr', "Jahr fehlt")
    fstat['stz'] = check_code(form, 'stz', 'stzei',
                              "Kein Stellenzeichen für die Fachstatistik")
    fstat['bz'] = check_code(form, 'bz', 'fsbz',
                              "Kein Bezirk", fstatold)
    fstat['gs'] = check_code(form, 'gs', 'gs',
                              "Kein Geschlecht", fstatold)
    fstat['ag'] = check_code(form, 'ag', 'fsag',
                              "Keine Altersgruppe Kind", fstatold)
    fstat['agkm'] = check_code(form, 'agkm', 'fsagel',
                              "Keine Altersgruppe Mutter", fstatold)
    fstat['agkv'] = check_code(form, 'agkv', 'fsagel',
                              "Keine Altersgruppe Vater", fstatold)
    fstat['fs'] = check_code(form, 'fs', 'fsfs',
                              "Kein Familienstatus", fstatold )
    fstat['zm'] = check_code(form, 'zm', 'fszm',
                              "Keine Zugangsart", fstatold)
    fstat['qualij'] = check_code(form, 'qualij', 'fsqualij',
                              "Keine Qualifikation f&uuml;r Jugendlichen gew&auml;hlt")
    fstat['qualikm'] = check_code(form, 'qualikm', 'fsquali',
                              "Keine Qualifikation f&uuml;r Vater gew&auml;hlt")
    fstat['qualikv'] = check_code(form, 'qualikv', 'fsquali',
                              "Keine Qualifikation f&uuml;r Vater gew&auml;hlt")
    fstat['hkm'] = check_code(form, 'hkm', 'fshe',
                              "Keine Herkunft, Mutter", fstatold)
    fstat['hkv'] = check_code(form, 'hkv', 'fshe',
                              "Keine Herkunft, Vater", fstatold)
    fstat['bkm'] = check_code(form, 'bkm', 'fsbe',
                              "Kein Beruf, Mutter", fstatold)
    fstat['bkv'] = check_code(form, 'bkv', 'fsbe',
                              "Kein Beruf, Vater fehlt", fstatold)
    fstat['ba1'] = check_code(form, 'ba1', 'fsba',
                              "Keine Problemlage 1 bei der Anmeldung", fstatold)
    fstat['ba2'] = check_code(form, 'ba2', 'fsba',
                              "Keine Problemlage 1 bei der Anmeldung", fstatold)
    fstat['pbe'] = check_code(form, 'pbe', 'fspbe',
                              "Keine Hauptproblematik der Eltern", fstatold)
    fstat['pbk'] = check_code(form, 'pbk', 'fspbk',
                              "Keine Hauptproblematik Kind", fstatold)
    fstat['no2'] = check_str_not_empty(form, 'no2',
                                       "Keine Notiz andersgeartete Problemlage Kind", fstatold)
    fstat['no3'] = check_str_not_empty(form, 'no3',
                                       "Keine Notiz andersgeartete Problemlage Eltern", fstatold)
    fstat['no'] = check_str_not_empty(form, 'no', "Keine Notiz", fstatold)
    
    #get_int_fields(fstat, form, ['ka'], )
    get_int_fields(fstat, form,
                   [ 'kkm', 'kkv',
                   'kki', 'kpa', 'kfa', 'ksoz', 'kleh', 'kerz', 'kson','kkonf' ], 0)
    
    if form.has_key('le'):
        le = form.get('le')
    else: raise EE("Keine Massnahme angegeben")
    
    if form.has_key('pbkind'):
        pbk = form.get('pbkind')
    else: raise EE("Kein Problemspektrum für das Kind angegeben")
    
    if form.has_key('pbeltern'):
        pbe = form.get('pbeltern')
    else: raise EE("Kein Problemspektrum für die Eltern angegeben")
    
    fsid = fstatold['id']
    if not le is None:
        fsleilist = FachstatistikleistungList(where='fstat_id = %s' % fsid)
        fsleilist.deleteall()
        if type(le) is type(''):
            le = [le]
        codelist =  []
        for l in le:
            codelist.append(check_code({'le':l},'le', 'fsle',
                                       "Fehler in Leistungsart"))
        for l in codelist:
            fstatlei = Fachstatistikleistung()
            fstatlei['fstat_id'] = fsid
            fstatlei['le'] = l
            try:
                fstatlei.new()
                fstatlei.insert()
                fstatold.update(fstat)
            except Exception, args:
                raise EBUpdateError("Fehler beim Einfügen in die Datenbank: %s" % str(args))
                
    if not pbk is None:
        pbkl = FachstatistikkindproblemList(where='fstat_id = %s' % fsid)
        pbkl.deleteall()
        if type(pbk) is type(''):
            pbk = [pbk]
        codelist =  []
        for p in pbk:
            codelist.append(check_code({'pbk':p},'pbk', 'fspbk', "Fehler Problemspektrum Kind"))
        for p in codelist:
            fstatpbk = Fachstatistikkindproblem()
            fstatpbk['fstat_id'] = fsid
            fstatpbk['pbk'] = p
            try:
                fstatpbk.new()
                fstatpbk.insert()
                fstatold.update(fstat)
            except Exception, args:
                raise EBUpdateError("Fehler beim Einfügen in die Datenbank: %s" % str(args))
                
    if not pbe is None:
        pbelist = FachstatistikelternproblemList(where='fstat_id = %s' % fsid)
        pbelist.deleteall()
        if type(pbe) is type(''):
            pbe = [pbe]
        codelist =  []
        for p in pbe:
            codelist.append(check_code({'pbe':p},'pbe', 'fspbe', "Fehler Problemspektrum Eltern"))
        for p in codelist:
            fstatpbe = Fachstatistikelternproblem()
            fstatpbe['fstat_id'] = fsid
            fstatpbe['pbe'] = p
            try:
                fstatpbe.new()
                fstatpbe.insert()
                fstatold.update(fstat)
            except Exception, args:
                raise EBUpdateError("Fehler beim Einfügen in die Datenbank: %s" % str(args))
                
    fstat['zeit'] = int(time.time())
    fstatold.update(fstat)
    
    ## vgl. Kommentar bei updjgh
    ##
    
    if fstatold['fall_id'] != None:
        akteold = Akte(fstatold['fall_id__akte_id'])
        akte = Akte()
        akte['zeit'] = int(time.time())
        akteold.update(akte)
        fstatold['akte'].akte_undo_cached_fields()
        
        
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
    jghstat['bezirksnr'] = check_code(form, 'wohnbez', 'wohnbez',
                                          "Kein Wohnbezirk")
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
        
    if form.has_key('ba'):
        ba = form.get('ba')
    else: raise EE("Keinen Beratunganlass angegeben")
    ##  print "BERATUNGSANLÄSSE:",ba
    if type(ba) is type(''):
        ba = [ba]
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
        

def jgh_laufende_nummer_setzen():
    """Erteilt jeder Jugenhilfestatistik eine laufende Nummer"""
    # höchste vorhandene laufende Nummer ermitteln
    jghstatliste = JugendhilfestatistikList(where = 'lnr > 0', order = 'lnr')
    if jghstatliste:
        letzte = jghstatliste[-1]['lnr']
    else:
        letzte = 0
    # laufende Nummer setzen wo noch keine vorhanden ist
    jghstatliste = JugendhilfestatistikList(where = 'lnr IS NULL', order = 'id')
    for j in jghstatliste:
        letzte += 1
        j.update({'lnr': letzte})


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
    if config.BERLINER_VERSION:
        jghstat['bezirksnr'] = check_code(form, 'wohnbez', 'wohnbez',
                                          "Kein Wohnbezirk")
    
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
        
    if form.has_key('ba'):
        ba = form.get('ba')
    else: raise EE("Keinen Beratunganlass angegeben")
    #  print "BERATUNGSANLÄSSE:",ba
    if type(ba) is type(''):
        ba = [ba]
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
        akteold = Akte(jghstatold['fall_id__akte_id'])
        akte = Akte()
        akte['zeit'] = int(time.time())
        akteold.update(akte)
        jghstatold['akte'].akte_undo_cached_fields()
        
        
def gruppeeinf(form):
    """Neue Gruppe."""
    
    gruppeid = check_int_not_empty(form, 'gruppeid', "Gruppeid fehlt")
    check_not_exists(gruppeid, Gruppe,
                     "Gruppe (id: %(id)s, Name: %(name)s gibt es in der Datenbank bereits")
    gruppe = Gruppe()
    get_string_fields(gruppe, form, ['gn', 'name', 'thema'], '')
    gruppe['gn'] = check_str_not_empty(form, 'gn', "Keine Gruppennummer")
    check_unique(gruppe['gn'], GruppeList, 'gn',
                 "Gruppennummer ist bereits vergeben")
    gruppe['name'] = check_str_not_empty(form, 'name', "Kein Gruppenname")
    gruppe['thema'] = check_str_not_empty(form, 'thema', "Kein Thema")
    gruppe['teiln'] = check_code(form, 'teiln', 'teiln',
                                 "Fehler bei Teilnehmer")
    gruppe['grtyp'] = check_code(form, 'grtyp', 'grtyp',
                                 "Fehler beim Gruppentyp")
    gruppe['stz'] = check_code(form, 'stz', 'stzei',
                               "Kein Stellenzeichen für die Grupp")
    get_int_fields(gruppe, form, ['tzahl', 'stzahl'], 0)
    
    if form.has_key('mitid'):
        mitid = form.get('mitid')
    else: raise EE("Keine Mitarbeiter angegeben")
    #  print "Mitarbeiter:",mitid
    if type(mitid) is type(''):
        mitid = [mitid]

    # TODO: stimmt das? dürfen beide Daten 0 sein oder in der Zukunft liegen?
    gruppe.setDate('bg', check_date(form, 'bg',
                                    "Fehler im Datum für den Beginn", Date(0,0,0), maybezero = 1, maybefuture=1 ))
    gruppe.setDate('e', check_date(form, 'e',
                                   "Fehler im Datum für das Ende", Date(0,0,0), maybezero = 1, maybefuture=1 ))
    if gruppe.getDate('bg') > gruppe.getDate('e'):
        raise EE('Beginndatum liegt vor Endedatum')
    for m in mitid:
        mitgruppe = MitarbeiterGruppe()
        mitgruppe['mit_id'] = m
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
    if form.has_key('mitid'):
        mitid = form.get('mitid')
    else:
        raise EE("Keine Mitarbeiter angegeben")
    if type(mitid) is type(''):
        mitid = [mitid]
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
    get_int_fields(gruppe, form, ['tzahl', 'stzahl'], gruppeold)
    
    gruppe.setDate('bg', check_date(form, 'bg',
                                    "Fehler im Datum für den Beginn", Date(0,0,0), maybezero = 1, maybefuture=1 ))
    gruppe.setDate('e', check_date(form, 'e',
                                   "Fehler im Datum für das Ende", Date(0,0,0), maybezero = 1, maybefuture=1 ))
    
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
        mitgruppe['mit_id'] = m
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
    dok['zeit'] = int(time.time())
    dok['mtyp'] = cc('mimetyp','txt')
    dok['fname'] = '%s.txt' % dokold['id']
    dok.setDate('v',
                  check_date(form, 'v',
                             "Fehler im Datum"))
    text = check_str_not_empty(form, 'text', "Kein Text")
    dok['zeit'] = int(time.time())
    gruppeold = Gruppe(dok['gruppe_id'])
    gruppe_path = get_gruppe_path(gruppeold['id'])
    
    try:
        f = open('%s/%s' % (gruppe_path, dok['fname']), 'w+')
        f.write(text)
        f.close()
        os.chmod('%s/%s' % (gruppe_path, dok['fname']),0600)
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
    
    if form.has_key('fallid'):
        fallid = form.get('fallid')
    elif form.has_key('bezugspid'):
        bezugspid = form.get('bezugspid')
    else:
        raise EE("Keine TeilnehmerIn angegeben")
        
    if form.has_key('fallid'):
        if type(fallid) is type(''):
            fallid = [fallid]
        for f in fallid:
            fallgruppel = FallGruppeList(where = 'gruppe_id = %s and fall_id = %s'
                                         % (gruppeid, f))
            if len(fallgruppel) > 0:
                raise EE("Klient wird schon als Teilnehmer geführt")
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
                
    if form.has_key('bezugspid'):
        bezugspid = form.get('bezugspid')
        if type(bezugspid) is type(''):
            bezugspid = [bezugspid]
        for b in bezugspid:
            bezugspgruppel = BezugspersonGruppeList(where =                                               'gruppe_id = %s and bezugsp_id = %s' % (gruppeid, b))
            if len(bezugspgruppel) > 0:
                raise EE("Klient wird schon als Teilnehmer geführt")
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
    if form.has_key('fallid'):
        fallid = form.get('fallid')
    elif form.has_key('bezugspid'):
        bezugspid = form.get('bezugsid')
    else:
        raise EE("Keine TeilnehmerIn zum Löschen markiert")
    if form.has_key('fallid'):
        fallid = form.get('fallid')
        if type(fallid) is type(''):
            fallid = [fallid]
        for f in fallid:
            try:
                fallgr = FallGruppe(int(f))
                fallgr.delete()
            except Exception, args:
                raise EBUpdateError("Fehler beim Löschen in der Datenbank: %s" % str(args))
                
    if form.has_key('bezugspid'):
        bezugspid = form.get('bezugspid')
        if type(bezugspid) is type(''):
            bezugspid = [bezugspid]
        for b in bezugspid:
            try:
                bezugspgr = BezugspersonGruppe(int(b))
                bezugspgr.delete()
            except Exception, args:
                raise EBUpdateError("Fehler beim Löschen in der Datenbank: %s" % str(args))
                
    gruppeold = Gruppe(gruppeid)
    gruppe = Gruppe()
    gruppe['zeit'] = int(time.time())
    
    gruppeold.update(gruppe)
    
    
def updgrteiln(form):
    """Update des Gruppenteilnehmers."""
    
    if form.has_key('fallgrid'):
        fallgrold = check_exists(form, 'fallgrid', FallGruppe, "Kein Teilnehmer")
        fall = Fall(fallgrold['fall_id'])
        gruppeold = fallgrold['gruppe']
        fallgr = FallGruppe()
        fallgr.setDate('bg', check_date(form, 'bg',
                                        "Fehler im Datum für den Beginn",
                                        fallgrold,
                                        maybezero = 1, maybefuture = 1 ))
        fallgr.setDate('e', check_date(form, 'e',
                                       "Fehler im Datum für das Ende",
                                       fallgrold, maybezero = 1,
                                       maybefuture = 1 ))
        fallgr['zeit'] = int(time.time())
        if fallgr.getDate('bg') > fallgr.getDate('e'):
            raise EE('Beginndatum liegt vor Endedatum')
        fallgrold.update(fallgr)
        gruppe = Gruppe()
        gruppe['zeit'] = int(time.time())
        gruppeold.update(gruppe)
        gruppeold.gruppe_undo_cached_fields()
        
    elif form.has_key('bezugspgrid'):
        bezpgrold = check_exists(form, 'bezugspgrid',
                                 BezugspersonGruppe, "Kein Teilnehmer")
        bezp = Bezugsperson(bezpgrold['bezugsp_id'])
        gruppeold = bezpgrold['gruppe']
        bezpgr = BezugspersonGruppe()
        bezpgr.setDate('bg', check_date(form, 'bg',
                                        "Fehler im Datum für den Beginn",
                                        bezpgrold, maybezero = 1,
                                        maybefuture = 1 ))
        bezpgr.setDate('e', check_date(form, 'e',
                                       "Fehler im Datum für das Ende",
                                       bezpgrold, maybezero = 1,
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
    if form.has_key('dokids'):
        dokids = form.get('dokids')
    else:
        raise EE("Keinen Eintrag markiert?")
        
    if type(dokids) is type(''):
        dokids = [dokids]
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
    
    if (str(form.get('changepassword')) == '1'):
        s = sha.new(check_str_not_empty(form, 'ben', "Kein Benutzername"))
        mit['pass'] = s.hexdigest()
        
    mit['benr'] =  check_code(form, 'benr', 'benr',
                              "Fehler bei den Benutzerrechten", mitold)
    mit['zeit'] = int(time.time())
    
    mitold.update(mit)
    
    
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
    code['kat_id'] = check_fk(form, 'katid', Kategorie, "Kategorienid fehlt")
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
    codeliste = CodeList(where = "kat_code = '%s'" % code['kat_code']
                         + 'and sort >= %d' % code['sort'], order = 'sort')
    if codeliste:
    
        for c in codeliste:
            cneu = Code()
            x = c['sort']
            cneu['sort'] = x + 1
            c.update(cneu)
            
    code['zeit'] = int(time.time())
    
    if code['kat_code'] == 'dbsite':
        tl = TabellenIDList(where = '', order = 'minid desc'  )
        minid = int('%(minid)d' % tl[0])
        if minid > code['mini']:
            raise EE("Das Bereichsminimum  ist kleiner als bei der Site %(dbsite__name)s"
                     % tl[0])
        maxliste = TabellenIDList(where = 'minid = %d' % minid)
        for m in maxliste:
            t = TabellenID()
            t['table_id'] = m['table_id']
            t['table_name'] = m['table_name']
            t['dbsite'] = codeid
            t['minid'] = code['mini']
            t['maxid'] = code['maxi']
            t['maxist'] = int(t['minid']) -1
            try:
                t.insert()
            except Exception, args:
                try: t.delete()
                except: pass
                raise EBUpdateError("Fehler beim Einfügen in die Datenbank: %s" % str(args))
                
    try:
        code.insert(codeid)
    except Exception, args:
        try: code.delete()
        except: pass
        raise EBUpdateError("Fehler beim Einfügen in die Datenbank: %s" % str(args))
        
        
def updcode(form):
    """Update des Code."""
    
    codeold = check_exists(form, 'codeid', Code, "Merkmalsid fehlt")
    code = Code()
    code['code'] = check_str_not_empty(form, 'code',
                                       "Merkmalscode fehlt", codeold)
    code['kat_code'] = check_str_not_empty(form, 'katcode',
                                           "Kategoriencode fehlt", codeold)
    code['kat_id'] = check_fk(form, 'katid', Kategorie,
                              "Kategorienid fehlt", codeold)
    code['name'] = check_str_not_empty(form, 'name',
                                       "Merkmalsname fehlt", codeold)
    if form['mini'] != '' or form['maxi'] != '' or codeold['kat_code'] == 'dbsite':
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
                
    if codeold['kat_code'] == 'dbsite':
        tl = TabellenIDList(where = 'dbsite = %s' % codeold['id'] )
        for m in tl:
            t = TabellenID()
            t['minid'] = codeold['mini']
            t['maxid'] = codeold['maxi']
            t['maxist'] = int(t['minid']) -1
            m.update(t)
            
            
def removeakten(form):
    """Akten und Gruppen löschen."""
    
    import os
    
    frist = check_int_not_empty(form, 'frist',
                                'Keine Monate', config.LOESCHFRIST)
    
    rmdatum = get_rm_datum(frist)
    alle_faelle = FallList(where = 'zday <= %(loeschjahr)s and zdam <= %(loeschmonat)s and zday > 1'
                           % rmdatum )
    
    # Alle Fälle entfernen, die *nicht* der letzte Fall der jeweiligen Akte sind
    faelle = [f for f in alle_faelle if f == f['akte_id__letzter_fall']]

    #print "## Schema: fallid;akte_id;Fallnummer"
    zeit = int(time.time())
    #print "## Unix-Zeit: %s" % zeit
    
    #print "## %s Faelle sind " % len(faelle) + "aelter als %(loeschmonat)s.%(loeschjahr)s"  % rmdatum

    # kann sein, dass es weniger Akten sind als Fällte, da eine Akte
    # mehrere Fälle haben kann, daher ein dict mit akte_id zum Zählen
    anzahl_akten_geloescht = {}    
    for f in faelle:
        #print "********* LOESCHEN: %(id)s;%(akte_id)s;%(fn)s" % f
        jghstatl = JugendhilfestatistikList(where = 'fall_id = %s' % f['id'])
        fachstatl = FachstatistikList(where = 'fall_id = %s' % f['id'])
        dokl = DokumentList(where = 'fall_id = %s' % f['id'])
        zustaendigl = ZustaendigkeitList(where = 'fall_id = %s' % f['id'])
        anmeldungl = AnmeldungList(where = 'fall_id = %s' % f['id'])
        leistungl = LeistungList(where = 'fall_id = %s' % f['id'])
        einrl = EinrichtungskontaktList(where = 'akte_id = %s' % f['akte_id'])
        bezugspl = BezugspersonList(where = 'akte_id = %s' % f['akte_id'])
        fallgrl = FallGruppeList(where = 'fall_id = %s' % f['id'])
        akte_path = get_akte_path(f['akte_id'])
        
        for j in jghstatl:
            jghstatold = Jugendhilfestatistik(j['id'])
            jghstat = Jugendhilfestatistik()
            jghstat['fall_id'] = None
            jghstat['zeit'] = int(time.time())
            jghstatold.update(jghstat)
        for a in fachstatl:
            fachstatold = Fachstatistik(a['id'])
            fachstat = Fachstatistik()
            fachstat['fall_id'] = None
            fachstat['zeit'] = int(time.time())
            fachstatold.update(fachstat)
        for d in dokl:
            try:
                os.remove('%s/%s' % (akte_path, d['fname']))
            except: pass
        try:
            os.rmdir('%s' % akte_path)
        except: pass
        anmeldungl.deleteall()
        leistungl.deleteall()
        einrl.deleteall()
        dokl.deleteall()
        fallgrl.deleteall()
        zustaendigl.deleteall()
        for  b in bezugspl:
            bezugspgrl = BezugspersonGruppeList(where = 'bezugsp_id = %s' % b['id'])
            bezugspgrl.deleteall()
        bezugspl.deleteall()
        fall = Fall(f['id'])
        try:
            akte = Akte(f['akte_id'])
        except: pass
        try:
            fall.delete()
        except: pass
        try:
            akte.delete()
            anzahl_akten_geloescht[akte['id']] = True
        except: pass
        #print "Loeschen der Faelle Okay"

    # wir brauch nur die Länge der dict
    anzahl_akten_geloescht = len(anzahl_akten_geloescht)
    gruppen = GruppeList(where = 'ey <= %(loeschjahr)s and em <= %(loeschmonat)s and ey > 1'
                      % rmdatum )
    
    #print "## Schema: gruppeid;leer;Gruppenummer"
    zeit = int(time.time())
    #print "## Unix-Zeit: %s" % zeit
    
    #print "## %s Gruppen sind " % len(gruppen) + "aelter als %(loeschmonat)s.%(loeschjahr)s"  % rmdatum

    anzahl_gruppen_geloescht = 0
    for g in gruppen:
        #print "%(id)s;;%(gn)s" % g
        gruppe_path = get_gruppe_path(g['id'])
        fallgrl = FallGruppeList(where = 'gruppe_id = %s' % g['id'])
        bezugspgrl = BezugspersonGruppeList(where = 'gruppe_id = %s' % g['id'])
        dokl = GruppendokumentList(where = 'gruppe_id = %s' % g['id'])
        mitgrl = MitarbeiterGruppeList(where = 'gruppe_id = %s' % g['id'])
        fallgrl.deleteall()
        bezugspgrl.deleteall()
        mitgrl.deleteall()
        for d in dokl:
            try:
                os.remove('%s/%s' % (gruppe_path, d['fname']))
            except: pass
        try:
            os.rmdir('%s' % gruppe_path)
        except: pass
        dokl.deleteall()
        gruppeold = Gruppe(g['id'])
        gruppeold.delete()
        anzahl_gruppen_geloescht += 1
    #print "Loeschen der Gruppen Okay"
    return anzahl_akten_geloescht, anzahl_gruppen_geloescht
    
    
def setAdresse(obj, form):
    """Wenn strkat einen Wert hat, wird die Ueberpruefung durch den Strassenkatalog
    getriggert. Dies ist z.Z. nur in der Berliner Version der Fall.

    Kann auch fuer Bezugspersonenadressen verwendet werden,
    planungsr und wohnbez werden dann nicht beruecksichtigt
    """
    strasse = form.get('str')
    strkat = form.get('strkat')
    if strkat:
        # Straßenkatalog, nur Berliner Version
        if check_strasse(form, 'strkat', 'hsnr', 'plz') != '':
            obj['str'] = strkat
            if form.get('hsnr') == '':
                obj['hsnr'] = '---'
            else:
                obj['hsnr'] = form.get('hsnr')
            obj['plz'] = form.get('plz')
        # innerhalb der Gültigkeit des Straßenkatalogs
        obj['lage'] = cc('lage', '0') 
        if 'planungsr' in obj.fields:
            # Übernahme des Planungsraums aus dem Straßenkatalogs
            # falls Objekt ein planungsr-Feld hat
            obj['planungsr'] = plraum_zuweisen(form, 'strkat', 'hsnr',
                                               'plz', "Kein Planungsraum gefunden")
        if 'wohnbez' in obj.fields:
            # wohnbez aus dem Straßenkatalog übernehmen
            obj['wohnbez'] = wohnbez_zuordnen(form, 'strkat', 'hsnr',
                                              'plz', "Kein Wohnbezirk gefunden")
    else:
        # Für nicht-Berliner Version kommen wir immer hier durch
        # Für Berliner Version nur dann, wenn gar keine Straße angegeben wurde
        # oder eine außerhalb Berlins.
        if strasse:
            # Strassenangabe (immer für nicht-Berliner Version, nur Straßen
            # außerhalb von Berlin für Berliner Version)
            obj['str'] = strasse
            obj['hsnr'] = form.get('hsnr')
            obj['plz'] = form.get('plz')
            # außerhalb der Gültigkeit des Straßenkatalogs
            obj['lage'] = cc('lage', '1')
            if 'planungsr' in obj.fields:
                planungs_raum = form.get('planungsr')
                if planungs_raum in ('0', '9999'):
                    raise EBUpdateDataError("Kein gültiger Planungsraum")
                obj['planungsr'] =  planungs_raum or 0
            if 'wohnbez' in obj.fields:
                # außerhalb Berlins
                obj['wohnbez'] = cc('wohnbez', '13')
        else:
            # keine Strassenangabe (für Berliner und nicht-Berliner Version)
            obj['str'] = strasse
            obj['hsnr'] = form.get('hsnr')
            obj['plz'] = form.get('plz')
            obj['lage'] = cc('lage', '999')
            if 'planungsr' in obj.fields:
                planungs_raum = form.get('planungsr')
                if planungs_raum in ('0', '9999'):
                    raise EBUpdateDataError("Kein gültiger Planungsraum")
                obj['planungsr'] =  planungs_raum or 9999
            if 'wohnbez' in obj.fields:
                obj['wohnbez'] = cc('wohnbez', '999')


