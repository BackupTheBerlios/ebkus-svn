# coding: latin-1

"""
Stellt den amtlichen Gemeindeschlüssel für die Bundesstatistik zur Verfügung.

Voraussetzungen:
================

Es existiert 

A. eine csv-Datei mit den Gemeindeschlüsseln unter

$EBKUS_HOME/sql/gemeindeschluessel_in_deutschland.csv

Ist in der Distribution mit dabei, kann aber auch erzeugt werden, indem aus der Excel-Datei, die unter

http://www.destatis.de/jetspeed/portal/cms/Sites/destatis/Internet/DE/Content/Statistiken/Regionales/Gemeindeverzeichnis/Administrativ/Archiv/GV2000VJ/4Q__31122010__Auszug,property=file.xls

zur Verfügung steht, eine csv-Datei abgespeichert wird mit mit folgenden Parametern:

Zeichensatz: Western, ISO-8869-15
Feldtrenner: ,
Texttrenner: "

Ich habe das mit Openoffice gemacht, ob das auch mit MS Excel mit diesen Parametern geht, weiß ich nicht.

oder B. eine csv-Datei $EBKUS_HOME/sql/gemeindeschluessel.csv, die nur die benötigten Werte enthält.

Das sind: plz ort ags, also z.B.
"38518","Gifhorn","03151009"

(Parameter wie oben) 

Diese Datei wird genommen, wenn sie vorhanden ist. Wenn sie nicht vorhanden ist, wird sie erzeugt aus der 
offiziellen Datei (siehe A. erzeugt) und kann dann weiter editiert werden.


Konfigurationsvariable GEMEINDESCHLUESSEL_VON_PLZ

Falls diese Variable nicht belegt ist, werden keine Gemeindeschlüssel in die Bundesstatistik eingetragen.

"""

import csv, re, os, sys, logging
from ebkus.config import config
from ebkus.db.sql import SQL, SQLError
from ebkus.db.dbapp import cache_clear_if_gt
from ebkus.app.ebapi import AGS, AGSList
from os.path import join, split, dirname, basename, exists, \
     isdir, isfile, normpath, normcase, abspath

_agscontainer = None

# Diese Zusätze aus den Ortsbezeichnungen sollen alle weg.
# Z.B. Aus "Gießen, Universitätsstadt" wird "Gießen"
_zusaetze = (
  "Stadt",
  "Kreisstadt",
  "Landeshauptstadt",
  "Bergstadt",
  "Lutherstadt",
  "Universitätsstadt",
  "Goethestadt",
  "Hansestadt",
  "Freie und Hansestadt",
  "M",
  "Marktflecken",
  "St",
  "Flecken",
  "Kirchspiel",
  "Kurort",
  "Höhenkurort",
  "Höhenluftkurort",
  "Nordseebad",
  "Wissenschaftsstadt",
  "GKSt",
  "gemeindefreies Gebiet",
  "gemfr. Gebiet",
  "gemfr. Geb.",
  "gemfr. Bezirk",
  "Brüder-Grimm-Stadt",
  "Karolingerstadt",
  "Schöfferstadt",
  "Barbarossast., Krst.",
  "Konrad-Zuse-Stadt",
  "Dom- und Kaiserstadt",
  "Loreleystadt",
  "Sickingenstadt",
  "Reuterstadt",
  "Gneisenaustadt",
  "Liebenbachstadt",
  "documenta-Stadt",
)

class AGSContainer(object):
    def __init__(self):
        if self.data_in_db(): # Datenbank ist bereits gefüllt, der Normalfall
            return
        spec = config.GEMEINDESCHLUESSEL_VON_PLZ
        if spec:
            self.restrict_plz = [p.strip() for p in spec.split(';') if p.strip()]
        else:
            self.restrict_plz = [] # Default ohne Konfiguration: keine Restriktion, alle nehmen
        self.csv_datei_orig =  join(config.EBKUS_HOME, 'sql', 'gemeindeschluessel_in_deutschland.csv.gz')
        self.generate_db()
    def data_in_db(self):
        count = SQL("select count(*) from ags").execute()
        return count[0][0];
    def generate_db(self):
        import gzip
        f_in = gzip.open(self.csv_datei_orig)
        SQL("ALTER TABLE ags DISABLE KEYS;").execute()
        for line in self.get_data(f_in):
            res = self.handle_line(line)
            #print 'INIT', line, res
            if not res:
                continue
            plz, ort, ags = res
            self.add2db(plz, ort, ags)
        SQL("ALTER TABLE ags ENABLE KEYS;").execute()
    def handle_line(self, liste):
        """Gibt ein tuple plz, ort, ags zurück, das aufgenommen werden soll,
        sonst None.
        """
        typ = liste[0]
        if typ != '60': # Nur Gemeinden
            return None
        plz = liste[13]
        if not plz: # keine Gemeinde ohne PLZ
            return None
        if self.restrict_plz: # nur Gemeinden, deren PLZ mit bestimmten Ziffern beginnt
            include = False
            for prefix in self.restrict_plz:
                if plz.startswith(prefix):
                    include = True
                    break
            if not include:
                return None
        ort = liste[7]
        for z in _zusaetze:  # Zusätze entfernen
            ort = ort.replace(', %s' % z, '')
        ags = ''.join(liste[2:5]+liste[6:7])
        return plz, ort, ags

    def get_data(self, f):
        reader = csv.reader(f.readlines(),
                            delimiter=',',
                            doublequote=True,
                            quotechar='"',
                            lineterminator='\r\n',
                            )
        size = None
        for l in reader:
            if l[0] != '60':
                continue
            assert len(l) == size or size == None
            size = len(l)
            yield l
    def add2db(self, plz, ort, ags):
        ag = AGS()
        ag.init(plz=plz, ort=ort, ags=ags)
        ag.new()
        ag.insert()
    def get_gemeindeschluessel(self, gem_name, gem_plz):
        """Falls der Name eindeutig ist, den assoziierten AGS zurückgeben.
        Falls mehrere Einträge, die PLZ heranziehen.
        Falls ein Eintrag dieselbe PLZ hat, dessen AGS zurückgeben.
        In allen anderen Fällen None zurückgeben.
        """
        if not gem_name:
            return None
        matches = AGSList(where="ort like '%s'" % (gem_name+'%',))
        if not matches: # kein Treffer
            return None
        exakt = [m for m in matches if m['ort'] == gem_name]
        if len(exakt) == 1:
            return exakt[0]['ags'] # ein exakter Treffer
        else:
            for m in exakt:
                if m['plz'] == gem_plz: # exakter Treffer mit korrekter PLZ
                    return m['ags']
        for m in matches:
            if m['plz'] == gem_plz: # nicht-exakter Treffer mit korrekter PLZ
                return m['ags']     # unterscheidet z.B. 'Müden (Aller)' von 'Müden (...)'
        # Wenn keine der nicht-exakten Treffer die korrekte PLZ hat,
        # können wir keine Aussage machen.
        return None


    # def __init__(self):
    #     self.ort2ags = {} # ortsname --> [(plz, ags), ...]
    #     spec = config.GEMEINDESCHLUESSEL_VON_PLZ
    #     if spec:
    #         self.restrict_plz = [p.strip() for p in spec.split(';') if p.strip()]
    #     else:
    #         return
    #     self.csv_datei_orig =  join(config.EBKUS_HOME, 'sql', 'gemeindeschluessel_in_deutschland.csv.gz')
    #     self.csv_datei_cache = join(config.EBKUS_HOME, 'sql', 'gemeindeschluessel_cache.csv')
    #     self.csv_datei_eigen = join(config.EBKUS_HOME, 'sql', 'gemeindeschluessel.csv')
    #     if exists(self.csv_datei_eigen):
    #         self.csv_datei = self.csv_datei_eigen
    #     else:
    #         if not exists(self.csv_datei_cache):
    #             self.generate_csv_datei()
    #         self.csv_datei = self.csv_datei_cache
    #     f = open(self.csv_datei)
    #     reader = csv.reader(f.readlines(),
    #                         delimiter=',',
    #                         doublequote=True,
    #                         quotechar='"',
    #                         lineterminator='\r\n',
    #                         )
    #     for plz, ort, ags in reader:
    #         self.add2dict(plz, ort, ags)

    # def get_gemeindeschluessel(self, gem_name, gem_plz):
    #     """Falls der Name eindeutig ist, den assoziierten AGS zurückgeben.
    #     Falls mehrere Einträge, die PLZ heranziehen.
    #     Falls ein Eintrag dieselbe PLZ hat, dessen AGS zurückgeben.
    #     In allen anderen Fällen None zurückgeben.
    #     """
    #     ags = None
    #     value = self.ort2ags.get(gem_name)
    #     if value:
    #         if len(value) == 1:
    #             ags = value[0][1]
    #         else:
    #             for v in value:
    #                 plz, ags = v
    #                 if plz == gem_plz:
    #                     break
    #     else:
    #         # Name kommt direkt nicht vor, z.B. weil nach Müden gesucht wird,
    #         # es gibt aber nur den Eintrag Müden (Aller)
    #         values = [self.ort2ags[k] for k in self.ort2ags if k.startswith(gem_name)]
    #         for value in values:
    #             for v in value:
    #                 plz, ags = v
    #                 if plz == gem_plz:
    #                     break
    #     return ags

    # def generate_csv_datei(self):
    #     import gzip
    #     f_in = gzip.open(self.csv_datei_orig)
    #     f_out = open(self.csv_datei_cache, "wb")
    #     writer = csv.writer(f_out,
    #                         delimiter=',',
    #                         doublequote=True,
    #                         quotechar='"',
    #                         lineterminator='\r\n',
    #                         )
    #     for line in self.get_data(f_in):
    #         res = self.handle_line(line)
    #         #print 'INIT', line, res
    #         if not res:
    #             continue
    #         plz, ort, ags = res
    #         writer.writerow((plz,ort,ags))
    # def add2dict(self, plz, ort, ags):
    #     value = self.ort2ags.get(ort)
    #     if value:
    #         value.append((plz,ags))
    #     else:
    #         self.ort2ags[ort] = [(plz,ags)]

def get_gemeindeschluessel(ort, plz):
    """Falls der Name eindeutig ist, den assoziierten AGS zurückgeben.
    Falls mehrere Einträge, die PLZ heranziehen.
    Falls ein Eintrag dieselbe PLZ hat, dessen AGS zurückgeben.
    In allen anderen Fällen None zurückgeben.
    """
    global _agscontainer
    if not _agscontainer:
        try:
            _agscontainer = AGSContainer()
            logging.info("Gemeindeschluessel erfolgreich initialisiert (n=%s)." % _agscontainer.data_in_db())
        except Exception, e:
            t = sys.exc_info()[0]
            logging.exception("%s: %s", t, e)
            logging.error("Gemeindeschluessel konnten nicht eingelesen werden.")
            return None
    return _agscontainer.get_gemeindeschluessel(ort, plz)

def delete_cache():
    global _agscontainer
    _agscontainer = None
    try:
        SQL("delete from ags").execute()
    except:
        pass
    cache_clear_if_gt(0) # Ganz sicher gehen, dass keine AGS mehr im Cache sind.
# def delete_cache():
#     global _agscontainer
#     _agscontainer = None
#     try:
#         os.unlink(join(config.EBKUS_HOME, 'sql', 'gemeindeschluessel_cache.csv'))
#     except:
#         pass
