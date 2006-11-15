# coding: latin-1
"""

Tabellen fuer die EB-Klientenverwaltung
der bezirklichen Familienberatungsstellen Berlins.

Daten als string für das Schema der EB Klientenverwaltung.

Aufbau:
 Für jede Tabelle eine Headerzeile und eine Folge von Zeilen für jedes Feld.
 Zwischen jeder Tabelle steht eine Leerzeile.
 Jede Zeile ist eine Folge von Feldern, die durch Komma getrennt sind.

 Jede Tabelle beginnt mit einer Zeile mit den folgenden Feldern:
 1. table      immer gleich
 2. <tabellenname>
 3. <feld>.<feld>.../<feld>.<feld>.../... Schlüssel für die Tabelle (s.u.)
 4. <Langname> ausführlicher Name für die Tabelle, der auch eine Phrase mit
               Leerzeichen sein darf.
 5. <Klassenname> Ein Identifier, der verwendet wird, um eine der Tabelle
                  enstprechenden Objektklasse für das ebapi zu generieren

Jeder Schlüssel identifiziert eine Zeile in der Tabelle.  Ein
Schlüssel kann aus einem Feldnamen oder aus mehreren durch '.'
getrennten Feldnamen bestehen.  Der Primärschlüssel wird hier nicht
aufgeführt, da er durch die Existenz eines Feldes des Verwendungstyps
's' gegeben ist.

Beispiel für Schlüssel für Tabelle code:
   code.kat_id/code.kat_code/name.kat_id/name.kat_code
Eine Zeile der Tabelle code kann also durch je zwei Werte der Felder
  code, kat_id bzw.
  code, kat_code bzw.
  name, kat_id bzw.
  name, kat_code
identifiziert werden.

Feldzeilen
1. <Feldname>
2. <Feldtyp>    der Typ des Feldes in der Datenbank, also 'INT', 'CHAR(70)'
3. <Langname>   langer Name für das Feld, der auch eine Phrase mit Leerzeichen
                sein kann. Kann im Interface für die Kennzeichnung des Feldes
                verwendet werden.
4. <Verwendungstyp> ein Buchstabe aus {s,f,k,b,p}
                    s = Primär(s)chlüssel für die Tabelle
                    f = (F)remdschlüssel
                    k = (k)odiertes Feld, Wert verweist in die Tabelle code
                    b = Zahlenfeld, für das aber Werte(b)ereiche in der Tabelle code
                        definert sind
                    p = primitives Feld
5. <Tabelle oder Codekategorie> Falls der Verwendungstyp 'f' ist, steht hier die
                                Tabelle, auf die der Fremdschlüssel verweist.
                                Falls der Verwendungstyp 'k' ist, steht
                                hier der code für die Kategorie, deren Instanzen
                                das Feld als Werte haben kann.
                                Falls der Verwendungstyp 'b' ist, steht hier
                                der code für eine Bereichskategorie, aufgrund derer
                                die Werte des Feldes gruppiert werden können.
6. <Name für inverse Relation> Falls der Verwendungstyp 'f' ist, kann hier ein Name
                               für die inverse Beziehung, die dann eine 1:n Beziehung
                               ist, eingetragen werden.
"""

# Was fehlt:
# Defaultwerte für Kategorien, evt. auch für andere Feldarten
# notnull ganz allgemein für Felder, insbesondere für Fremdschlüssel


schemainfo = \
"""
table, mitarbeiter, , Mitarbeiter, Mitarbeiter
id, INT, id, s,
vn, CHAR(35), Vorname, p,
na, CHAR(35), Name, p,
ben, CHAR(25), Benutzer, p,
anr, CHAR(20), Anrede, p
tl1, CHAR(25), Diensttelefon, p
fax, CHAR(25), Fax, p
mail, CHAR(50), Mail, p
stat, INT, Status, k, status
benr, INT, Benutzungsrecht, k, benr
stz, INT, Hauptdienststelle, k, stzei
zeit, INT, Änderungszeit, p,
pass, CHAR(50), Passwort, p,

table, protokoll, , Protokoll, Protokoll
nr, INT(11), nr, s,
zeit, VARCHAR(17), zeit, p,
artdeszugriffs, longtext, artdeszugriffs, p,
benutzerkennung, VARCHAR(25), benutzerkennung, p,
ipadresse, CHAR(25), ipadresse, p

table, strassenkat, ,Strassenkatalog
str_nummer, CHAR(5), Str_nummer, p,
str_name, CHAR(60), Str_name, p,
hausnr, CHAR(4), Hausnr, p,
bezirk, INT, Bezirk, p,
plz, INT, Plz, p,
Plraum, CHAR(4), Planungsraum, p

table, sessions, ,Session
session_id, CHAR(50), SessionID, s,
time, CHAR(16), Time, p,
user_name, CHAR(25), UserName, p,

table, mitstelle, mit_id.stz, Zuordnung Mitarbeiter-Dienststelle, MitarbeiterDienststelle
mit_id, INT, Mitarbeiterid, f, mitarbeiter, neben_stz
stz, INT, Nebendienststelle, k, stzei

table, akte, , Akte, Akte
id, INT, id, s
vn, CHAR(35), Vorname, p,
na, CHAR(35), Name, p,
gb, CHAR(10), Geburtsdatum, p,
ber, CHAR(30), Ausbildung, p,
str, CHAR(35), Strasse, p,
hsnr, CHAR(5), Hausnummer, p,
plz, CHAR(9), Postleitzahl, p,
planungsr, CHAR(4), Planungsraum, p, wird in das fachstat.bz Feld übernommen
wohnbez, INT, Wohnbezirk, p,
lage, INT, inBerlin, p,
ort, CHAR(35), Ort, p,
tl1, CHAR(25), Telefon, p,
tl2, CHAR(25), Diensttelefon, p,
fs, INT, Familienstatus (lebt bei), k, fsfs,
no, CHAR(255), Notiz, p,
stzbg, INT, Aufnahmedienststelle, k, stzei
stzak, INT, Aktuelle Dienststelle, k, stzei
zeit, INT, Änderungszeit, p,

table, fall, , Fall, Fall
id, INT, id, s,
akte_id, INT, Aktenid, f, akte, faelle
fn, CHAR(30), Fallnummer, p,
bgd, INT, Beginn Tag, p,
bgm, INT, Beginn Monat, p,
bgy, INT, Beginn Jahr, p,
zdad, INT, Abschluss Tag, p,
zdam, INT, Abschluss Monat, p,
zday, INT, Abschluss Jahr, p,
status, INT, Fallstand, k, stand

table, anmeldung, , Anmeldung, Anmeldung
id, INT, id, s,
fall_id, INT, Fall_id, f, fall, anmeldung
von, CHAR(35), angemeldet von, p,
ad, INT, Anmeldetag, p,
am, INT, Anmeldemonat, p,
ay, INT, Anmeldejahr, p,
mtl, CHAR(25), Telefon, p,
me, CHAR(35), auf Empfehlung von, p,
zm, INT, Zugangsart, k, fszm
mg, CHAR(255), Anmeldegrund, p,
no, CHAR(255), Notiz, p,

table, bezugsperson, , Bezugsperson, Bezugsperson
id, INT, id, s,
akte_id, INT, Aktenid, f, akte, bezugspersonen
vn, CHAR(35), Vorname, p,
na, CHAR(35), Name, p,
gb, CHAR(10), Geburtsdatum, p,
ber, CHAR(30), Beruf, p,
str, CHAR(35), Strasse, p,
hsnr, CHAR(5), Hausnummer, p,
lage, INT, inBerlin, p,
plz, CHAR(9), Postleitzahl, p,
ort, CHAR(35), Ort, p,
tl1, CHAR(25), Telefon, p,
tl2, CHAR(25), Diensttelefon, p,
fs, INT, Familienstatus (lebt bei), k, fsfs
verw, INT, Verwandschaftsgrad, k, klerv
no, CHAR(255), Notiz, p,
nobed, INT, Notizbedeutung, k, notizbed
vrt, INT, im Verteiler, k, vert

table, einrichtung, , Kontakt mit Einrichtung, Einrichtungskontakt
id, INT, id, s,
akte_id, INT, Aktenid, f, akte, einrichtungen
na, CHAR(80), Name, p,
tl1, CHAR(25), Telefon1, p,
tl2, CHAR(25), Telefon2, p,
insta, INT, Einrichtungsart, k, klinsta
no, CHAR(255), Notiz, p,
nobed, INT, Notizbedeutung, k, notizbed
status, INT, Aktueller Kontakt, k, einrstat

table, leistung, , Leistung, Leistung
id, INT, id, s,
fall_id, INT, Fallid, f, fall, leistungen
mit_id, INT, Mitarbeiterid, f, mitarbeiter, leistungen
le, INT, Leistungsart, k, fsle
bgd, INT, Beginn Tag, p,
bgm, INT, Beginn Monat, p,
bgy, INT, Beginn Jahr, p,
ed, INT, Ende Tag, p,
em, INT, Ende Monat, p,
ey, INT, Ende Jahr, p,
stz, INT, Dienststelle, k, stzei

table, zustaendigkeit, , Zuständigkeit, Zustaendigkeit
id, INT, id, s,
fall_id, INT, Fallid, f, fall, zustaendigkeiten
mit_id, INT, Mitarbeiterid, f, mitarbeiter, zustaendigkeiten
bgd, INT, Beginn Tag, p,
bgm, INT, Beginn Monat, p,
bgy, INT, Beginn Jahr, p,
ed, INT, Ende Tag, p,
em, INT, Ende Monat, p,
ey, INT, Ende Jahr, p,

table, dokument, , Dokument, Dokument
id, INT, id, s,
fall_id, INT, Fallid, f, fall, dokumente
mit_id, INT, Mitarbeiterid, f, mitarbeiter, dokumente
betr, CHAR(255), Betrifft, p,
fname, CHAR(255), Dateiname, p,
art, INT, Text ist, k, dokart
vd, INT, Tag, p,
vm, INT, Monat, p,
vy, INT, Jahr, p,
mtyp, INT, Mime Typ, k, mimetyp
dok, BLOB, Dokument, p,
zeit, INT, Änderungszeit, p,

table, gruppendokument, , Zuordnung Gruppe-Dokument, Gruppendokument
id, INT, id, s,
gruppe_id, INT, Gruppeid, f, gruppe, gruppendokumente
mit_id, INT, Mitarbeiterid, f, mitarbeiter, gruppendokumente
betr, CHAR(254), Betrifft, p,
fname, CHAR(254), Dateiname, p,
art, INT, Text ist, k, dokart
vd, INT, Tag, p,
vm, INT, Monat, p,
vy, INT, Jahr, p,
mtyp, INT, Mime Typ, k, mimetyp
dok, BLOB, Dokument, p,
zeit, INT, Änderungszeit, p,

table, gruppe, , Gruppe, Gruppe
id, INT, id, s,
gn, CHAR(20), Gruppennummer, p,
name, CHAR(255), Name, p,
thema, CHAR(255), Thema, p,
tzahl, INT, Anzahl der Termine, p,
stzahl, INT, Anzahl der Stunden, p,
bgd, INT, Tag, p,
bgm, INT, Monat, p,
bgy, INT, Jahr, p,
ed, INT, Tag, p,
em, INT, Monat, p,
ey, INT, Jahr, p,
teiln, INT, Teilnehmer, k, teiln
grtyp, INT, Gruppentyp, k, grtyp
stz, INT, Dienststelle, k, stzei
zeit, INT, Änderungszeit, p,

table, fallgruppe, /fall_id.gruppe_id/gruppe_id.fall_id,\
       Zuordnung Fall-Gruppe, FallGruppe
id, INT, id, s
fall_id, INT, Fallid, f, fall, gruppen
gruppe_id, INT, Gruppeid, f, gruppe, faelle
bgd, INT, Tag, p,
bgm, INT, Monat, p,
bgy, INT, Jahr, p,
ed, INT, Tag, p,
em, INT, Monat, p,
ey, INT, Jahr, p,
zeit, INT, Änderungszeit, p,

table, bezugspersongruppe, /bezugsp_id.gruppe_id/gruppe_id.bezugsp_id,\
       Zuordnung Bezugsperson-Gruppe, BezugspersonGruppe
id, INT, id, s
bezugsp_id, INT, Bezugspersonid, f, bezugsperson, gruppen
gruppe_id, INT, Gruppeid, f, gruppe, bezugspersonen
bgd, INT, Tag, p,
bgm, INT, Monat, p,
bgy, INT, Jahr, p,
ed, INT, Tag, p,
em, INT, Monat, p,
ey, INT, Jahr, p,
zeit, INT, Änderungszeit, p,

table, mitarbeitergruppe, mit_id.gruppe_id/gruppe_id.mit_id,\
       Zuordnung Mitarbeiter-Gruppe, MitarbeiterGruppe
id, INT, id, s
mit_id, INT, Mitarbeiterid, f, mitarbeiter, gruppen
gruppe_id, INT, Gruppeid, f, gruppe, mitarbeiter
bgd, INT, Tag, p,
bgm, INT, Monat, p,
bgy, INT, Jahr, p,
ed, INT, Tag, p,
em, INT, Monat, p,
ey, INT, Jahr, p,
zeit, INT, Änderungszeit, p,

table, fachstat, , Fachstatistik, Fachstatistik
id, INT, id, s,
mit_id, INT, Mitarbeiterid, f, mitarbeiter, fachstatistiken
fall_id, INT, Fallid, f, fall, fachstatistiken
fall_fn, CHAR(20), Fallnummer, p,
jahr, INT, Jahr, p,
stz, INT, Dienststelle, k, stzei, default ist aktuelle Dst. des Falles, wird benötigt wegen standalone Funktion der Fachstatistik
bz, CHAR(4), Region, p, berlinspezifisch - das ist der Planungsraum
gs, INT, Geschlecht, k, gs
ag, INT, Altersgruppe Kind, k, fsag
fs, INT, Familienstatus (lebt bei), k, fsfs
zm, INT, Zugangsart, k, fszm
qualij, INT, Qualifikation des/r Jugendlicher/n, k, fsqualij
hkm, INT, Herkunft der Mutter, k, fshe
hkv, INT, Herkunft des Vaters, k, fshe
bkm, INT, Beruf der Mutter, k, fsbe
bkv, INT, Beruf des Vaters, k, fsbe
qualikm, INT, Qualifikation der Mutter, k, fsquali
qualikv, INT, Qualifikation des Vater, k, fsquali
agkm, INT, Altersgruppe der Mutter, k, fsagel
agkv, INT, Altersgruppe des Vaters, k, fsagel
ba1, INT, Vorstellungsanlass 1 bei der Anmeldung, k, fsba
ba2, INT, Vorstellungsanlass 2 bei der Anmeldung, k, fsba
pbe, INT, Hauptproblematik Eltern, k,fspbe
pbk, INT, Hauptproblematik Kind/Jugendliche, k, fspbk
kat, INT, Summe der Konsultationen insgesamt (a 50 Min.), b, fskat
kkm, INT, Anzahl der Konsultationen Mutter, b, fskat
kkv, INT, Anzahl der Konsultationen Vater, b, fskat
kki, INT, Anzahl der Konsultationen Kind / Jugendlicher, b, fskat
kpa, INT, Anzahl der Konsultationen Paar, b, fskat
kfa, INT, Anzahl der Konsultationen Familie, b, fskat
ksoz, INT, Anzahl der Konsultationen Sozialarbeiter, b, fskat
kleh, INT, Anzahl der Konsultationen Lehrer, b, fskat
kerz, INT, Anzahl der Konsultationen Erzieher, b, fskat
kkonf, INT, Anzahl der Konsultationen Hilfebesprechung, b, fskat
kson, INT, Kontaktanzahl Sonstige, b, fskat
no, CHAR(255), Notiz, p,
no2, CHAR(255), anders geartete Problemlagen Kind, p,
no3, CHAR(255), anders geartete Problemlagen Eltern, p,
zeit, INT, Änderungszeit, p,

table, fachstatlei, , Zuordnung Fachstatistik-Leistung, Fachstatistikleistung
id, INT, id, s,
fstat_id, INT, Fachstatistikid, f, fachstat, leistungen
le, INT, Leistungsart, k, fsle

table, fachstatkindproblem, , Zuordnung Fachstatistik-Problemspektrum Kind, Fachstatistikkindproblem
id, INT, id, s,
fstat_id, INT, Fachstatistikid, f, fachstat, fachstatkindprobleme
pbk, INT, Problemspektrum Kind, k, fspbk

table, fachstatelternproblem, , Zuordnung Fachstatistik-Problemspektrum Eltern, Fachstatistikelternproblem
id, INT, id, s,
fstat_id, INT, Fachstatistikid, f, fachstat, fachstatelternprobleme
pbe, INT, Problemspektrum Eltern, k, fspbe

table, jghstat, , Jugendhilfestatistik, Jugendhilfestatistik
id, INT, id, s,
fall_id, INT, Fallid, f, fall, jgh_statistiken
mit_id, INT, Mitarbeiterid, f, mitarbeiter, jgh_statistiken
fall_fn, CHAR(20), Fallnummer, p,
gfall, INT, Geschwisterfall, k, gfall
bezirksnr, INT, Wohnbezirksnummer des Klienten, k, wohnbez, berlinspezifisch
stz, INT, Dienststelle, k, stzei, default ist aktuelle Dst. des Falles
rbz, INT, Regierungsbezirk, k, rbz, bundesweite Statistik - stellen- nicht klientenbezogen
kr, INT, Kreis, k, kr, bundesweite Statistik - stellen- nicht klientenbezogen
gm, INT, Gemeinde, k, gm, bundesweite Statistik - stellen- nicht klientenbezogen
gmt, INT, Gemeindeteil, k, gmt, bundesweite Statistik - stellen- nicht klientenbezogen
lnr, INT, laufendeNummer, p,
traeg, INT, Träger, k, traeg
bgm, INT, Beginn Monat, p,
bgy, INT, Beginn Jahr, p,
em, INT, Ende Monat, p,
ey, INT, Ende Jahr, p,
bgr, INT, Beendigungsgrund, k, bgr
gs, INT, Geschlecht, k, gs
ag, INT, Altersgruppe, k, ag
fs, INT, lebt bei, k, fs
hke, INT, Herkunft Eltern, k, hke
gsa, INT, Geschwisterzahl, b, gsa,     *Bereich* fuer die Abfrage wie fska
gsu, INT, Geschwisterzahl unbekannt, k, gsu
zm, INT, Kontaktaufnahme, k, zm
ba0, INT, Beratungsanlass 0, k, ba0
ba1, INT, Beratungsanlass 1, k, ba1
ba2, INT, Beratungsanlass 2, k, ba2
ba3, INT, Beratungsanlass 3, k, ba3
ba4, INT, Beratungsanlass 4, k, ba4
ba5, INT, Beratungsanlass 5, k, ba5
ba6, INT, Beratungsanlass 6, k, ba6
ba7, INT, Beratungsanlass 7, k, ba7
ba8, INT, Beratungsanlass 8, k, ba8
ba9, INT, Beratungsanlass 9, k, ba9
schw, INT, Beratungsschwerpunkt, k, schw
fbe0, INT, Beratung Kind, k, fbe0
fbe1, INT, Beratung Eltern, k, fbe1
fbe2, INT, Beratung Familie, k, fbe2
fbe3, INT, Beratung Umfeld, k, fbe3
zeit, INT, Änderungszeit, p,

table, code, code.kat_id/code.kat_code/name.kat_id/name.kat_code, Code, Code
id, INT, id, s,
kat_id, INT, Kategorienid, f, kategorie, codes
kat_code, CHAR(8), Kategoriencode, p,
code, CHAR(8), Code, p, , kann auch als Abkürzung im Interface verwendet werden
name, CHAR(160), Name, p,
sort, INT, Sortierreihenfolge, p,
mini, INT, Bereichsminimum, p,
maxi, INT, Bereichsmaximum, p,
off, INT, Ungültig, p,
dm, INT, Ungültig ab Monat, p,
dy, INT, Ungültig ab Jahr, p,
dok, CHAR(255), Erläuterung, p,
zeit, INT, Änderungszeit, p,

table, kategorie, code/name, Kategorie, Kategorie
id, INT, id, s,
code, CHAR(8), Code, p,
name, CHAR(60), Name, p,
kat_id, INT, Kategorienart, f, kategorie, kategorien
dok, CHAR(255), Erläuterung, p,
zeit, INT, Änderungszeit, p,

table, exportprotokoll, , DB Exportprotokoll, Exportprotokoll
id, INT, id, s,
mit_id, INT, Mitarbeiterid, f, mitarbeiter,
zeit, INT, Exportzeitpunkt, p,
dbsite, INT, Datenbanksite, k, dbsite,

table, importprotokoll, , DB Importprotokoll, Importprotokoll
id, INT, id, s,
exp_id, INT, Exportprotokollid, f, exportprotokoll, importprotokolle
mit_id, INT, Mitarbeiterid, f, mitarbeiter,
zeit, INT, Importzeitpunkt, p,
dbsite, INT, Datenbanksite, k, dbsite,

table, feld, tab_id.feld, Feld, Feld
id, INT, id, s,
tab_id, INT, Tabelle, f, tabelle, felder
feld, CHAR(30), Feldname, p,
name, CHAR(60), Langname des Feldes, p,
inverse, CHAR(60), Name für inverse Beziehung, p,
typ, CHAR(20), Datenbanktyp, p,
laenge, INT, Feldlänge, p,
notnull, INT, Nicht NULL, p,
verwtyp, INT, Verwendungstyp, k, verwtyp,
ftab_id, INT, Fremdtabelle, f, tabelle, inverse,
kat_id, INT, Kategorienid, f, kategorie
kat_code, CHAR(8), Kategoriencode, p,
flag, INT, Flags, p,
dok, CHAR(255), Erläuterung, p,

table, tabelle, tabelle/name/klasse, Tabelle, Tabelle
id, INT, id, s,
tabelle, CHAR(30), Tabellenname, p,
name, CHAR(60), Langname der Tabelle, p,
klasse, CHAR(60), Klassenname, p,
flag, INT, Flags, p,
dok, CHAR(255), Erläuterung, p,

table, tabid, table_id.dbsite/table_name.dbsite, Zuordnung Tabelle-ID-Bereiche, TabellenID
table_id, INT, Tabellenid, f, tabelle, iddaten
table_name, CHAR(30), Tabellenname, p,
dbsite, INT, Datenbanksite, k, dbsite,
minid, INT, Minimale ID, p,
maxid, INT, Maximale ID, p,
maxist, INT, Maximale verwendete ID, p,

table, schluessel, tab_id.feld_id.seq, Schlüssel, Schluessel
tab_id, INT, Tabelle, f, tabelle, schluessel
feld_id, INT, Feld, f, feld, schluessel
seq, INT, Laufende Nummer, p,
"""

#fname, fdbtype, lname, vtyp =  {s,f,k,b,p}, { , tablename, kat_code, kat_code, }
#tname, fn1/fn3.fn3/fn5.fn6, lname, classname













