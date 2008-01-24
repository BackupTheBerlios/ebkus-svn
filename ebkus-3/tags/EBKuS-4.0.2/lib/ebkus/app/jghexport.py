# coding: latin-1
"""
Routinen für die Erzeugung des amtlichen Datensatzes
für die Bundesjugendhilfestatistik

Die Funktion jghexport(jahr) gibt zwei Strings zurück:

- den abzugebenden Datensatz ohne Zeilenumbrüche
- den Kontrolldatensatz mit Zeilenumbrüchen und der zusätzlichen
  Angabe der Fallnummer und der Mitarbeiterkennung pro Fall

Die Funktion wird vom Webinterface (html/datenaustausch.py) benutzt, um
dem Anwender zu ermöglichen, den abzugebenen Datensatz und den
Kontrolldatensatz herunterzuladen.

Außerdem kann diese Datei als Skript verwendet werden, um die Datensätze
direkt als Dateien ohne Umweg über das Webinterface zu erzeugen.
Dazu ist diese Datei (jghexport.py) in das Verzeichnis der Instanz
zu kopieren, für die die Statistik erzeugt werden soll.

Aufruf:

python jghexport.py <jahr>

python sollte zum Aufruf desselben Interpreters führen, mit dem EBKuS
installiert wurde.
"""


if __name__ == '__main__':
    import sys
    try:
        import init
    except ImportError:
        print "Dieses Skript zuerst in das Verzeichnis der Instanz kopieren,"
        print "fuer die der JGH-Export durchgefuehrt werden soll."
        sys.exit(1)
        
from ebkus.app.ebapi import JugendhilfestatistikList, Jugendhilfestatistik2007List, today
from ebkus.app.ebupd import jgh_laufende_nummer_setzen

## def jghexport(jahr):
##     """Erzeugt den Datensatz für die Jugendhilfestatistik.

##     Es werden zwei Strings zurückgegeben, der eigentliche Datensatz
##     und ein Kontrolldatensatz mit Zeilenumbrüchen und vorangesteller
##     Fallnummer und Mitarbeiterkennung.
##     """
##     import time
##     from ebkus.app.ebapi import JugendhilfestatistikList
##     from ebkus.app.ebupd import jgh_laufende_nummer_setzen
##     jgh_laufende_nummer_setzen()
##     jghl = JugendhilfestatistikList (where = 'ey =  %s' % jahr, order = 'id')
##     daten_saetze = []
##     log_daten_saetze = []
##     log_header = """Erzeugen der Datei mit den Datensätzen für die Jugendhilfestatistik für %s

## Datum: %s
## Datei: jgh_%s.txt
## Anzahl der Datensätze: %s

## Datensätze (vorangestellt zusätzlich Fallnummer und Mitarbeiterkennung):

## """ % (jahr, time.strftime("%c", time.localtime(time.time())),
##        jahr, len(jghl))
##     for record in jghl:
##         daten_satz, log_daten_satz = get_datensatz(record)
##         daten_saetze.append(daten_satz)
##         log_daten_saetze.append(log_daten_satz)
##     return ''.join(daten_saetze), log_header + ''.join(log_daten_saetze)

def jghexport(jahr, andauernd):
    """Erzeugt den Datensatz für die Jugendhilfestatistik.

    Es werden zwei Strings zurückgegeben, der eigentliche Datensatz
    und ein Kontrolldatensatz mit Zeilenumbrüchen und vorangesteller
    Fallnummer und Mitarbeiterkennung.
    """
    jgh_laufende_nummer_setzen()
    if jahr >= 2007:
        get_datensatz = get_datensatz_ab_2007
        if andauernd:
            #jghl = Jugendhilfestatistik2007List(where = 'ey is NULL and bgy <= %s' % jahr, order = 'lnr')
            jghl = Jugendhilfestatistik2007List(where = 'ey is NULL and jahr = %s' % jahr, order = 'lnr')
        else:
            jghl = Jugendhilfestatistik2007List(where = 'ey=%s' % jahr, order = 'lnr')
    else:
        jghl = JugendhilfestatistikList (where = 'ey =  %s' % jahr, order = 'lnr')
        get_datensatz = get_datensatz_bis_2006
    daten_saetze = []
    log_daten_saetze = []
    log_header = """Erzeugen der Datei mit den Datensätzen für die Jugendhilfestatistik für %s
%s
Erstellt am: %s
Datei: %s
Anzahl der Datensätze: %s

Datensätze (vorangestellt zusätzlich Fallnummer und Mitarbeiterkennung):

""" % (jahr,
       andauernd and "(andauernde Fälle)" or '',
       #time.strftime("%c", time.localtime(time.time())),
       today(),
       get_export_datei_name(jahr, False, andauernd),
       len(jghl))
    for record in jghl:
        daten_satz, log_daten_satz = get_datensatz(record)
        daten_saetze.append(daten_satz)
        log_daten_saetze.append(log_daten_satz)
    return ''.join(daten_saetze), log_header + ''.join(log_daten_saetze)

def get_export_datei_name(jahr, log, andauernd):
    log = log and '_log' or ''
    t = today()
    andauernd = andauernd and (
        "_am_%04d-%02d-%02d_andauernd" % (t.year, t.month, t.day)
        ) or ''
    name = "jgh_%s%s%s.txt" % (jahr, andauernd, log)
    return name

def get_datensatz_bis_2006(r):
    """Erzeugt einen Jugendhilfestatistikdatensatz für einen Fall

    Zurückgegeben wird der eigentliche Datensatz sowie ein Kontrolldatensatz.
    """
    l = [
      check_code(r['rbz__code'], 1),
      check_code(r['kr__code'][1:3], 2),
      check_code(r['gm__code'], 3),
      check_code(r['gmt__code'], 3),
      "%05d" % r['lnr'],
      check_code(r['traeg__code'], 1),
      "%02d" % r['bgm'],
      "%d" % r['bgy'],
      "%02d" % r['em'],
      "%d" % r['ey'],
      check_code(r['bgr__code'], 1),
      check_code(r['gs__code'], 1),
      check_code(r['ag__code'], 1),
      check_code(r['fs__code'], 2),
      check_code(r['hke__code'], 1),
      check_gsa(r['gsa'], r['gsu__code']),
      check_code(r['zm__code'], 1),
      check_code(r['ba0__code'], 1, '0'),
      check_code(r['ba1__code'], 1, '0'),
      check_code(r['ba2__code'], 1, '0'),
      check_code(r['ba3__code'], 1, '0'),
      check_code(r['ba4__code'], 1, '0'),
      check_code(r['ba5__code'], 1, '0'),
      check_code(r['ba6__code'], 1, '0'),
      check_code(r['ba7__code'], 1, '0'),
      check_code(r['ba8__code'], 1, '0'),
      check_code(r['ba9__code'], 1, '0'),
      check_code(r['schw__code'], 1),
      check_code(r['fbe0__code'], 1, '0'),
      check_code(r['fbe1__code'], 1, '0'),
      check_code(r['fbe2__code'], 1, '0'),
      check_code(r['fbe3__code'], 1, '0'),
      ' '*28,
    ]
    daten_satz = ''.join(l)
    assert len(daten_satz) == 80
    log_daten_satz = "%-10s%-10s%s\r\n" % (r['fall_fn'], r['mit_id__ben'], daten_satz[:54])
    return daten_satz, log_daten_satz
    
def get_datensatz_ab_2007(r):
    """Erzeugt einen Jugendhilfestatistikdatensatz für einen Fall

    Zurückgegeben wird der eigentliche Datensatz sowie ein Kontrolldatensatz.
    """
    d = [' ']*157      # Datensatz
    _set(d, 1, 1, 'A')
    _set(d, 2, 3, int(r['land__code']), "%02d")
    #_set(d, 4, 4, '0') # Regierungsbezirk jetzt beim Kreis mit drin
    _set(d, 4, 6, int(r['kr__code']), "%03d")
    _set(d, 7, 9, '0'*3) # Gemeinde bleibt leer
    _set(d, 10, 15, int(r['einrnr__code']), "%06d")
    _set(d, 16, 20, r['lnr'], '%05d')
    _set(d, 21, 22, r['bgm'], '%02d')
    _set(d, 23, 26, r['bgy'], '%04d')
    _set(d, 27, 27, '%1s' % r['zustw'])
    _set(d, 28, 29, r['hilf_art__code'])
    _set(d, 30, 31, r['hilf_ort__code'])
    _set(d, 32, 33, r['traeger__code'])
    _set(d, 34, 34, r['gs__code'])
    _set(d, 35, 36, r['gem'], '%02d')
    _set(d, 37, 40, r['gey'], '%04d')
    _set(d, 41, 112, ' '*(112-41+1)) # keine andere Kinder
    _set(d, 113, 114, r['aort_vor__code'])
    _set(d, 115, 115, r['sit_fam__code'])
    _set(d, 116, 116, r['ausl_her__code'], None, {'0': ' '})
    _set(d, 117, 117, r['vor_dt__code'], None, {'0': ' '})
    _set(d, 118, 118, r['wirt_sit__code'], None, {'0': ' '})
    _set(d, 119, 119, r['aip__code'])
    _set(d, 120, 120, r['ees__code'])
    _set(d, 121, 121, r['va52__code'])
    _set(d, 122, 122, r['rgu__code'])
    _set(d, 123, 123, r['hda__code'])
    _set(d, 124, 126, r['nbkakt'], '%03d', {None: ' '*3})
    _set(d, 127, 130, ' '*4) # irrelevant für Erziehungsberatung
    _set(d, 131, 132, r['gr1__code'])
    _set(d, 133, 134, r['gr2__code'], None, {None: ' '*2})
    _set(d, 135, 136, r['gr3__code'], None, {None: ' '*2})
    _set(d, 137, 138, r['em'], '%02d', {None: ' '*2})
    _set(d, 139, 142, r['ey'], '%04d', {None: ' '*4})
    _set(d, 143, 145, r['nbkges'], '%03d', {None: ' '*3})
    _set(d, 146, 146, r['lbk6m__code'], None, {None: ' '})
    _set(d, 147, 150, ' '*4) # irrelevant für Erziehungsberatung
    _set(d, 151, 152, r['grende__code'], None, {None: ' '*2})
    _set(d, 153, 154, r['aort_nac__code'], None, {None: ' '*2})
    _set(d, 155, 155, r['unh__code'], None, {None: ' '})
    _set(d, 156, 157, '\r\n') # neu: newline zwischen den Datensätzen
    datensatz = ''.join(d)
    assert len(datensatz) == 157
    if datensatz[122] == '1': # Hilfe dauert an
        assert datensatz[137:155] == ' '*18
    else:
        assert datensatz[123:126] == ' '*3
    log_datensatz = "%-14s%-10s%s" % (r['fall_fn'], r['mit_id__ben'], datensatz)
    return datensatz, log_datensatz

def _set(vector, von, bis, val, template=None, substitutions=None):
    res = None
    if substitutions:
        s = substitutions.get(val)
        if s != None:
            res = s
    if res == None:
        if template:
            res = template % val
        else:
            res = val
    #print 'VAL', val
    assert len(res) == (bis + 1 - von), 'Fehler beim Export der Bundesstatistik. Spalte %s-%s' % (von, bis)
    vector[von-1:bis] = list(res)

def check_code(str, length, leer_code = None):
    assert len(str) == length
    if not leer_code is None and str == leer_code:
        str = ' '*length
    return str
    
def check_gsa(gsa, gsu):
    """Falls das gsu-Feld 1 ist (Geschwisteranzahl unbekannt), wird das
    gsa Feld immer mit Leerzeichen gefüllt. Sonst wird die Zahl aus gsa
    übernommen. """
    if gsu == '1':
        return '  1'
    else:
        return "%02d " % gsa
        

if __name__ == '__main__':
    if len(sys.argv) < 2 or sys.argv[1] in ('-h', '-help', '--help'):
        print "Aufruf: python jghexport.py <jahr> [andauernd]"
        sys.exit(1)
    try:
        jahr = sys.argv[1]
        jahr = int(jahr)
        assert jahr > 1995 and jahr < 2500
    except:
        print "***Fehler: Kein gültiges Jahr: '%s'" % jahr
        sys.exit(1)
    try:
        andauernd = sys.argv[2]
        if andauernd.startswith('a'):
            andauernd = True
        else:
            print "***Fehler: Zweiter Parameter muss mit 'a' (fuer andauernd) beginnen"
            sys.exit(1)
    except IndexError:
        andauernd = False
    print
    print "Export der Jugendhilfestatistik fuer Instanz '%s'" % init.INSTANCE_NAME
    print "   (Pfad %s)" % init.INSTANCE_HOME
    print
    print "Jahr: %s  (%s)" % (jahr, andauernd and "andauernde Faelle" or "abgeschlossene Faelle" )
    print
    from ebkus.db.sql import opendb
    opendb()
    daten_saetze, log_daten_saetze = jghexport(jahr, andauernd)

    datei_name = get_export_datei_name(jahr, False, andauernd)
    f = open(datei_name, "w")
    f.write(daten_saetze)
    f.close()
    print "ausgegeben: %s" % datei_name 

    log_datei_name = get_export_datei_name(jahr, True, andauernd)
    f = open(log_datei_name, "w")
    f.write(log_daten_saetze)
    f.close()
    print "ausgegeben: %s" % log_datei_name
    print
    
    
    
    
    
