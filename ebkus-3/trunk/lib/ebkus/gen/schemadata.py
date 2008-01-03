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
                    m = (m)ultikat kodiertes Feld, Liste von ids als String,
                        Werte verweisen in die Tabelle code
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
vn, VARCHAR(35), Vorname, p,
na, VARCHAR(35), Name, p,
ben, VARCHAR(25), Benutzer, p,
anr, VARCHAR(20), Anrede, p
tl1, VARCHAR(25), Diensttelefon, p
fax, VARCHAR(25), Fax, p
mail, VARCHAR(50), Mail, p
stat, INT, Status, k, status
benr, INT, Benutzungsrecht, k, benr
stz, INT, Hauptdienststelle, k, stzei
zeit, INT, Änderungszeit, p,
pass, VARCHAR(50), Passwort, p,

table, protokoll, , Protokoll, Protokoll
nr, INT(11), nr, s,
zeit, VARCHAR(17), zeit, p,
artdeszugriffs, longtext, artdeszugriffs, p,
benutzerkennung, VARCHAR(25), benutzerkennung, p,
ipadresse, VARCHAR(25), ipadresse, p

table, strkatalog, ,StrassenkatalogNeu
id, INT, id, s,
von, VARCHAR(5), von Hausnummer, p,
bis, VARCHAR(5), bis Hausnummer, p,
gu, VARCHAR(1), gerade (G)  oder ungerade (U) oder NULL, p, 
name, VARCHAR(60), Strassenname, p,
plz, VARCHAR(5), Postleitzahl, p,
ort, VARCHAR(60), Ort, p,
ortsteil, VARCHAR(60), Ortsteil, p,
samtgemeinde, VARCHAR(60), Samtgemeinde, p,
bezirk, VARCHAR(60), Bezirk, p,
plraum, VARCHAR(60), Planungsraum, p,

table, akte, , Akte, Akte
id, INT, id, s
vn, VARCHAR(35), Vorname, p,
na, VARCHAR(35), Name, p,
gb, VARCHAR(10), Geburtsdatum, p,
gs, INT, Geschlecht, k, gs
ber, VARCHAR(30), Ausbildung, p,
aufbew, INT, Aufbewahrungskategorie, k, aufbew
str, VARCHAR(35), Strasse, p,
hsnr, VARCHAR(5), Hausnummer, p,
plz, VARCHAR(9), Postleitzahl, p,
plraum, VARCHAR(60), Planungsraum, p, 
lage, INT, inBerlin, p,
ort, VARCHAR(60), Ort, p,
tl1, VARCHAR(25), Telefon, p,
tl2, VARCHAR(25), Diensttelefon, p,
fs, INT, Familienstatus (lebt bei), k, fsfs,
no, VARCHAR(255), Notiz, p,
stzbg, INT, Aufnahmedienststelle, k, stzei
stzak, INT, Aktuelle Dienststelle (obsolet), k, stzei
zeit, INT, Änderungszeit, p,

table, fall, , Fall, Fall
id, INT, id, s,
akte_id, INT, Aktenid, f, akte, faelle
fn, VARCHAR(30), Fallnummer, p,
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
von, VARCHAR(35), angemeldet von, p,
ad, INT, Anmeldetag, p,
am, INT, Anmeldemonat, p,
ay, INT, Anmeldejahr, p,
mtl, VARCHAR(25), Telefon, p,
me, VARCHAR(35), auf Empfehlung von, p,
zm, INT, Zugangsart, k, fszm
mg, VARCHAR(255), Anmeldegrund, p,
no, VARCHAR(255), Notiz, p,

table, bezugsperson, , Bezugsperson, Bezugsperson
id, INT, id, s,
akte_id, INT, Aktenid, f, akte, bezugspersonen
vn, VARCHAR(35), Vorname, p,
na, VARCHAR(35), Name, p,
gb, VARCHAR(10), Geburtsdatum, p,
gs, INT, Geschlecht, k, gs
ber, VARCHAR(30), Beruf, p,
str, VARCHAR(35), Strasse, p,
hsnr, VARCHAR(5), Hausnummer, p,
lage, INT, inBerlin, p,
plz, VARCHAR(9), Postleitzahl, p,
ort, VARCHAR(35), Ort, p,
tl1, VARCHAR(25), Telefon, p,
tl2, VARCHAR(25), Diensttelefon, p,
fs, INT, Familienstatus (lebt bei), k, fsfs
verw, INT, Verwandschaftsgrad, k, klerv
no, VARCHAR(255), Notiz, p,
nobed, INT, Notizbedeutung, k, notizbed
vrt, INT, im Verteiler, k, vert

table, einrichtung, , Kontakt mit Einrichtung, Einrichtungskontakt
id, INT, id, s,
akte_id, INT, Aktenid, f, akte, einrichtungen
na, VARCHAR(80), Name, p,
tl1, VARCHAR(25), Telefon1, p,
tl2, VARCHAR(25), Telefon2, p,
insta, INT, Einrichtungsart, k, klinsta
no, VARCHAR(255), Notiz, p,
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

table, beratungskontakt, , Beratungskontakt, Beratungskontakt
id, INT, id, s,
gruppe_id, INT, Gruppeid, f, gruppe, termine
le_id, INT, Leistungsid, f, leistung, beratungskontakte
art, INT, Kontaktart, k, fska
art_bs, INT, Kontaktart, k, kabs
teilnehmer, VARCHAR(255), Teilnehmer am Kontakt, m, teilnbs
teilnehmer_bs, VARCHAR(255), Teilnehmer am Kontakt, m, teilnbs
anzahl, INT, Anzahl der Teilnehmer, p
kd, INT, Kontakt Tag, p,
km, INT, Kontakt Monat, p,
ky, INT, Kontakt Jahr, p,
kh, INT, Kontakt Stunde, p,
kmin, INT, Kontakt Minute, p,
jgh, INT, Kontakt im Sinne der Jugendstatistik, k, ja_nein
dauer, INT, Dauer in Minuten, k, fskd
dauer_f2f, INT, Face to face Minuten, p,
dauer_vornach, INT, Vorbereitung/Nachbereitung Minuten, p,
faktor, VARCHAR(255), offenes Merkmal zur Verrechnung, p
offenespr, INT, Beratung in der offenen Sprechstunde, k, ja_nein
no, VARCHAR(255), Notiz, p,
stz, INT, Dienststelle, k, stzei

table, mitarbeiterberatungskontakt, ,Mitarbeiterberatungskontakt, Mitarbeiterberatungskontakt
id, INT, id, s
mit_id, INT, Mitarbeiterid, f, mitarbeiter, mitarbeiterberatungskontakte
bkont_id, INT, Beratungskontaktid, f, beratungskontakt, mitarbeiterberatungskontakte
zeit, INT, Änderungszeit, p,

table, fallberatungskontakt, , Fallberatungskontakt, Fallberatungskontakt
id, INT, id, s
fall_id, INT, Fallid, f, fall, fallberatungskontakte
bezugsp_id, INT, Bezugspersonid, f, bezugsperson, fallberatungskontakte
bkont_id, INT, Beratungskontaktid, f, beratungskontakt, fallberatungskontakte
zeit, INT, Änderungszeit, p,

table, fua_bs, , Fallunabhängige Aktivitäten Braunschweig, Fua_BS
id, INT, id, s,
mit_id, INT, Mitarbeiterid, f, mitarbeiter, beratungskontakte_bs
art, INT, Aktivitätsart, k, fuabs
kd, INT, Aktivität Tag, p,
km, INT, Aktivität Monat, p,
ky, INT, Aktivität Jahr, p,
dauer, INT, Dauer der Aktivität in 10-Minuten-Einheiten (ohne Vor- und Nachbereitung), b, fuadbs
no, VARCHAR(255), Notiz, p,
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
betr, VARCHAR(255), Betrifft, p,
fname, VARCHAR(255), Dateiname, p,
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
betr, VARCHAR(254), Betrifft, p,
fname, VARCHAR(254), Dateiname, p,
art, INT, Text ist, k, dokart
vd, INT, Tag, p,
vm, INT, Monat, p,
vy, INT, Jahr, p,
mtyp, INT, Mime Typ, k, mimetyp
dok, BLOB, Dokument, p,
zeit, INT, Änderungszeit, p,

table, gruppe, , Gruppe, Gruppe
id, INT, id, s,
gn, VARCHAR(20), Gruppennummer, p,
name, VARCHAR(255), Name, p,
thema, VARCHAR(255), Thema, p,
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
fall_fn, VARCHAR(60), Fallnummer, p,
jahr, INT, Jahr, p,
stz, INT, Dienststelle, k, stzei, default ist aktuelle Dst. des Falles, wird benötigt wegen standalone Funktion der Fachstatistik
plz, VARCHAR(9), Postleitzahl, p,
ort, VARCHAR(60), Ort, p,
ortsteil, VARCHAR(60), Ortsteil, p,
samtgemeinde, VARCHAR(60), Samtgemeinde, p,
bezirk, VARCHAR(60), Bezirk, p,
plraum, VARCHAR(60), Planungsraum, p,
gs, INT, Geschlecht, k, gs
ag, INT, Altersgruppe Kind, k, fsag
fs, INT, Familienstatus (lebt bei), k, fsfs
zm, INT, Zugangsart, k, fszm
qualij, INT, Qualifikation des/r Jugendlicher/n, k, fsqualij
hkm, INT, Herkunft der Mutter, k, fshe
hkv, INT, Herkunft des Vaters, k, fshe
bkm, INT, Beschäftigungsverhältnis der Mutter, k, fsbe
bkv, INT, Beschäftigungsverhältnis des Vaters, k, fsbe
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
no, VARCHAR(255), Notiz, p,
no2, VARCHAR(255), anders geartete Problemlagen Kind, p,
no3, VARCHAR(255), anders geartete Problemlagen Eltern, p,
anmprobleme, VARCHAR(255), Problem(e) bei der Anmeldung, m, fsba
kindprobleme, VARCHAR(255), Problemspektrum Kind/Jugendliche(r), m, fspbk
elternprobleme, VARCHAR(255), Problemspektrum Eltern, m, fspbe
eleistungen, VARCHAR(255), Erbrachte Leistungen, m, fsle
joka1, INT, Frei definierbar unter Angaben zum Klienten, k, fsjoka1
joka2, INT, Frei definierbar unter Angaben zum Klienten, k, fsjoka2
joka3, INT, Frei definierbar unter Angaben zum Klienten, k, fsjoka3
joka4, INT, Frei definierbar unter Angaben zum Klienten, k, fsjoka4
jokf5, INT, Frei definierbar eigenständig, k, fsjokf5
jokf6, INT, Frei definierbar eigenständig, k, fsjokf6
jokf7, INT, Frei definierbar eigenständig, k, fsjokf7
jokf8, INT, Frei definierbar eigenständig, k, fsjokf8
zeit, INT, Änderungszeit, p,

table, jghstat, , Jugendhilfestatistik, Jugendhilfestatistik
id, INT, id, s,
fall_id, INT, Fallid, f, fall, jgh_statistiken
mit_id, INT, Mitarbeiterid, f, mitarbeiter, jgh_statistiken
fall_fn, VARCHAR(20), Fallnummer, p,
gfall, INT, Geschwisterfall, k, gfall
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

table, jghstat07, , Jugendhilfestatistik ab 2007, Jugendhilfestatistik2007
id, INT, id, s,
fall_id, INT, Fallid, f, fall, jgh07_statistiken
fall_fn, VARCHAR(20), Fallnummer, p,
mit_id, INT, Mitarbeiterid, f, mitarbeiter, jgh07_statistiken
stz, INT, Dienststelle, k, stzei, default ist aktuelle Dst. des Falles
gfall, INT, Geschwisterfall, k, gfall
land, INT, Land, k, land
kr, INT, Kreis, k, kr, bundesweite Statistik - stellen- nicht klientenbezogen
einrnr, INT, Einrichtungsnummer, k, einrnr
lnr, INT, laufende Nummer, p,
bgm, INT, Beginn der Hilfe Monat, p,
bgy, INT, Beginn der Hilfe Jahr, p,
zustw, VARCHAR(1), Übernahme wegen Zuständigkeitswechsels, p,
hilf_art, INT, Art der Hilfe, k, hilf_art
hilf_ort, INT, Ort der Hilfe, k, hilf_ort
traeger, INT, Träger der Einrichtung oder des Dienstes, k, traeger
gs, INT, Geschlecht, k, gs
gem, INT, Geburtsmonat, p,
gey, INT, Geburtsjahr, p,
aort_vor, INT, Aufenthaltsort vor der Hilfe, k, auf_ort
sit_fam, INT, Situation in der Herkunftsfamilie, k, shf
ausl_her, INT, Ausländische Herkunft mindestens eines Elternteils, k, ja_ne_un
vor_dt, INT, Vorrangig deutsch gesprochen, k, ja_ne_un
wirt_sit, INT, Lebt von ALGII oder Grundsicherung oder Sozialhilfe, k, ja_ne_un
aip, INT, Anregende Institution oder Person, k, aip
ees, INT, Entzug der elterlichen Sorge nach §1666 BGB, k, ja_nein
va52, INT, Verfahrensaussetzung nach §52 FGG, k, ja_nein
rgu, INT, Unterbringung nach §1631b BGB, k, ja_nein
hda, INT, Hilfe dauert am Jahresende an, k, ja_nein
nbkakt, INT, Zahl der Beratungskontakte bei andauernder Hilfe, b, fskat
gr1, INT, Hauptgrund für die Hilfegewährung, k, gruende
gr2, INT, 2. Grund für die Hilfegewährung, k, gruende
gr3, INT, 3. Grund für die Hilfegewährung, k, gruende
em, INT, Ende der Hilfe Monat, p,
ey, INT, Ende der Hilfe Jahr, p,
nbkges, INT, Zahl der Beratungskontakte insgesamt, b, fskat
lbk6m, INT, Letzter Kontakt vor mehr als 6 Monaten, k, ja_nein
grende, INT, Gründe für Beendigung, k, grende
aort_nac, INT, Anschließender Aufenthalt, k, auf_ort
unh, INT, Unmittelbar nachfolgende Hilfe, k, unh
zeit, INT, Änderungszeit, p,


table, code, code.kat_id/code.kat_code/name.kat_id/name.kat_code, Code, Code
id, INT, id, s,
kat_id, INT, Kategorienid, f, kategorie, codes
kat_code, VARCHAR(8), Kategoriencode, p,
code, VARCHAR(8), Code, p, , kann auch als Abkürzung im Interface verwendet werden
name, VARCHAR(160), Name, p,
sort, INT, Sortierreihenfolge, p,
mini, INT, Bereichsminimum, p,
maxi, INT, Bereichsmaximum, p,
off, INT, Ungültig, p,
dm, INT, Ungültig ab Monat, p,
dy, INT, Ungültig ab Jahr, p,
dok, VARCHAR(255), Erläuterung, p,
flag, INT, Flags, p
zeit, INT, Änderungszeit, p,

table, kategorie, code/name, Kategorie, Kategorie
id, INT, id, s,
code, VARCHAR(8), Code, p,
name, VARCHAR(60), Name, p,
kat_id, INT, Kategorienart, f, kategorie, kategorien
dok, VARCHAR(255), Erläuterung, p,
flag, INT, Flags, p
zeit, INT, Änderungszeit, p,

table, feld, tab_id.feld, Feld, Feld
id, INT, id, s,
tab_id, INT, Tabelle, f, tabelle, felder
feld, VARCHAR(30), Feldname, p,
name, VARCHAR(60), Langname des Feldes, p,
inverse, VARCHAR(60), Name für inverse Beziehung, p,
typ, VARCHAR(20), Datenbanktyp, p,
laenge, INT, Feldlänge, p,
notnull, INT, Nicht NULL, p,
verwtyp, INT, Verwendungstyp, k, verwtyp,
ftab_id, INT, Fremdtabelle, f, tabelle, inverse,
kat_id, INT, Kategorienid, f, kategorie
kat_code, VARCHAR(8), Kategoriencode, p,
flag, INT, Flags, p,
dok, VARCHAR(255), Erläuterung, p,

table, tabelle, tabelle/name/klasse, Tabelle, Tabelle
id, INT, id, s,
tabelle, VARCHAR(30), Tabellenname, p,
name, VARCHAR(60), Langname der Tabelle, p,
klasse, VARCHAR(60), Klassenname, p,
flag, INT, Flags, p,
dok, VARCHAR(255), Erläuterung, p,
maxist, INT, Maximale verwendete ID, p,

table, register, regkey, Register, Register
id, INT, id, s,
regkey, VARCHAR(255), Schluessel, p,
value, MEDIUMBLOB, Wert, p,

table, abfrage, name, Abfrage, Abfrage
id, INT, id, s,
mit_id, INT, Mitarbeiterid, f, mitarbeiter,
name, VARCHAR(255), Name, p,
dok, TEXT, Beschreibung, p,
value, TEXT, Wert, p,
typ, VARCHAR(255), Typ der Abfrage, p,
zeit, INT, Änderungszeit, p,

table, altdaten, , Altdaten zur Übernahme, Altdaten
id, INT, id, s,
vorname, VARCHAR(35), Vorname, p,
name, VARCHAR(35), Name, p,
geburtsdatum, VARCHAR(10), Geburtsdatum, p,
geschlecht, VARCHAR(10), Geschlecht (m oder w), p,
jahr, INT, Jahr des letzten Kontakts, p,
fallnummer, VARCHAR(20), Fallnummer, p,
mitarbeiter, VARCHAR(60), Mitarbeiter, p,
strasse, VARCHAR(35), Strasse, p,
hausnummer, VARCHAR(5), Hausnummer, p,
plz, VARCHAR(9), Postleitzahl, p,
ort, VARCHAR(60), Ort, p,
telefon1, VARCHAR(25), Telefon, p,
telefon2, VARCHAR(25), Diensttelefon, p,
memo, TEXT, Memo, p,

"""

#fname, fdbtype, lname, vtyp =  {s,f,k,b,p}, { , tablename, kat_code, kat_code, }
#tname, fn1/fn3.fn3/fn5.fn6, lname, classname












"""
table, beratungskontakt_bs, , Beratungskontakt_BS, Beratungskontakt_BS
id, INT, id, s,
fall_id, INT, Fallid, f, fall, beratungskontakte_bs
fall1_id, INT, Fallid, f, fall, beratungskontakte_bs1
fall2_id, INT, Fallid, f, fall, beratungskontakte_bs2
mit_id, INT, Mitarbeiterid, f, mitarbeiter, beratungskontakte_bs
mit1_id, INT, Mitarbeiterid, f, mitarbeiter, beratungskontakte_bs1
mit2_id, INT, Mitarbeiterid, f, mitarbeiter, beratungskontakte_bs2
teilnehmer, VARCHAR(60), Teilnehmer am Kontakt, m, teilnbs
anzahl, INT, Anzahl der Teilnehmer, p
art, INT, Kontaktart, k, kabs
kd, INT, Kontakt Tag, p,
km, INT, Kontakt Monat, p,
ky, INT, Kontakt Jahr, p,
dauer, INT, Dauer der Kontakts in 10-Minuten-Einheiten (ohne Vor- und Nachbereitung), b, kdbs
offenespr, INT, Beratung in der offenen Sprechstunde, k, ja_nein
no, VARCHAR(255), Notiz, p,
stz, INT, Dienststelle, k, stzei
"""
