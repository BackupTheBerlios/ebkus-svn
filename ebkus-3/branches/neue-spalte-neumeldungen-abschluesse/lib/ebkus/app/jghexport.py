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
    

def jghexport(jahr):
    """Erzeugt den Datensatz für die Jugendhilfestatistik.

    Es werden zwei Strings zurückgegeben, der eigentliche Datensatz
    und ein Kontrolldatensatz mit Zeilenumbrüchen und vorangesteller
    Fallnummer und Mitarbeiterkennung.
    """
    import time
    import ebkus.ebs # Warnings abstellen
    from ebkus.app.ebapi import JugendhilfestatistikList
    from ebkus.app.ebupd import jgh_laufende_nummer_setzen
    jgh_laufende_nummer_setzen()
    jghl = JugendhilfestatistikList (where = 'ey =  %s' % jahr, order = 'id')
    daten_saetze = []
    log_daten_saetze = []
    log_header = """Erzeugen der Datei mit den Datensätzen für die Jugendhilfestatistik für %s

Datum: %s
Datei: jgh_%s.txt
Anzahl der Datensätze: %s

Datensätze (vorangestellt zusätzlich Fallnummer und Mitarbeiterkennung):

""" % (jahr, time.strftime("%c", time.localtime(time.time())),
       jahr, len(jghl))
    for record in jghl:
        daten_satz, log_daten_satz = get_datensatz(record)
        daten_saetze.append(daten_satz)
        log_daten_saetze.append(log_daten_satz)
    return ''.join(daten_saetze), log_header + ''.join(log_daten_saetze)


def get_datensatz(r):
    """Erzeugt einen Jugendhilfestatistikdatensatz für einen Fall

    Zurückgegeben wird der eigentliche Datensatz sowie ein Kontrolldatensatz.
    """
    l = [
      check_code(r['rbz__code'], 1),
      check_code(r['kr__code'], 2),
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
    log_daten_satz = "%-10s%-10s%s\n" % (r['fall_fn'], r['mit_id__ben'], daten_satz[:54])
    return daten_satz, log_daten_satz
    

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
    import sys
    try:
        import init
        print "Export der Jugendhilfestatistik für Instanz '%s'" % init.INSTANCE_NAME
        print "   (Pfad %s)" % init.INSTANCE_HOME
        print
    except ImportError:
        print "Dieses Skript zuerst in das Verzeichnis der Instanz kopieren,"
        print "fuer die der JGH-Export durchgefuehrt werden soll."
    if len(sys.argv) < 2:
        print "***Fehler: Bitte Jahr angeben"
        sys.exit(1)
    jahr = sys.argv[1]
    try:
        jahr = int(jahr)
        assert jahr > 1995 and jahr < 2500
    except:
        print "***Fehler: Kein gültiges Jahr: '%s'" % jahr
        sys.exit(1)
    from ebkus.db.sql import opendb
    opendb()
    daten_saetze, log_daten_saetze = jghexport(jahr)

    f = open("jgh_%s.txt" % jahr, "w")
    f.write(daten_saetze)
    f.close()

    f = open("jgh_log_%s.txt" % jahr, "w")
    f.write(log_daten_saetze)
    f.close()

    sys.stdout.write(log_daten_saetze)
    print
    
    
    
    
    
