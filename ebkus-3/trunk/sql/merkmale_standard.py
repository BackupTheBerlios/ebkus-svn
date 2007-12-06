# coding: latin-1

####################################################################
#
#  Standard Merkmale -- ohne ortsspezifische Merkmale 
#
####################################################################


####################################################################
#
# Enthält die Daten, welche nach der Generierung in die Datenbank
# eingelesen werden.
#
# Code und Kategorien für die Datenbank;
# Code- und Kategorienlisten zur Klientenverwaltung und Fachstatistik;
# Mitarbeiterliste
#
#######################################################################

#
# Code-Liste
#
# Code;Merkmalsname;Code der Kategorie;Bereichsminimum;Bereichsmaximum
#

code_list_str = \
"""s;Schlüssel;verwtyp
f;Fremdschlüssel;verwtyp
k;Kategorie;verwtyp
b;Bereichskategorie;verwtyp
p;Primitiv;verwtyp
m;Mehrfachkategorie;verwtyp
1;m;gs
2;w;gs
1;0-2;fsag
2;3-5;fsag
3;6-9;fsag
4;10-13;fsag
5;14-17;fsag
6;18-20;fsag
7;21-26;fsag
8;vor d. Schw.;fsag
9;pränatal;fsag
999;keine Angabe;fsag
1;bis 20;fsagel
2;21-26;fsagel
3;27-44;fsagel
4;45-54;fsagel
5;55-64;fsagel
6;65-74;fsagel
7;75-;fsagel
999;keine Angabe;fsagel
1;verheiratet, leibl. Eltern;fsfs
2;unverheiratet, leibl. Eltern;fsfs
3;wechselnd bei Km u. Kv;fsfs
4;Elternteil u. Stiefelternteil;fsfs
5;alleinerziehende Mutter;fsfs
6;alleinerziehender Vater;fsfs
7;Verwandte;fsfs
8;Pflegefamilie;fsfs
9;Adoptivfamilie;fsfs
10;Heim;fsfs
11;Wohngemeinschaft;fsfs
12;eigene Wohnung;fsfs
13;obdachlos;fsfs
14;sonstige;fsfs
999;keine Angabe;fsfs
1;ohne Empfehlung;fszm
2;Klient/Bekannte;fszm
3;ASD;fszm
4;KJGD/KJPD;fszm
5;Kita/Hort;fszm
6;Schule;fszm
7;Schulpsychologie;fszm
8;Kinder-/Jugendbetreuung;fszm
9;Medizinische Einrichtung;fszm
10;Gericht;fszm
11;Öffentlichkeitsarbeit;fszm
12;Sonstige;fszm
999;keine Angabe;fszm
1;Entwicklungs-, Verhaltensauff. in d. Familie;fsba
2;Entwicklungs-, Verhaltensauff. in d. Kita;fsba
3;Entwicklungs-, Verhaltensauff. in d. Schule;fsba
4;Entwicklungs-, Verhaltensauff. im sonst. Umfeld;fsba
5;Entwickungs- , Verhaltensauff., sonstige;fsba
6;Leistungsproblem in der Schule/Ausbildung;fsba
7;Lebensproblem der Jugendlichen;fsba
8;Ablösungsproblem des Jugendlichen;fsba
9;Krise der Jugendlichen;fsba
10;sexueller Missbrauch;fsba
11;Überforderung der Eltern;fsba
12;Erziehungsunsicherheiten;fsba
13;Familienkonflikt;fsba
14;Paarkonflikt;fsba
15;Trennungs- / Scheidungsproblem der Eltern;fsba
16;Sorge- oder Umgangsrecht;fsba
17;Begleiteter Umgang;fsba
18;akute Krise des Ratsuchenden;fsba
19;Begleitung vor u. nach Fremdunterbringung;fsba
20;Stellungnahme KJHG-Psychotherapie;fsba
21;Stellungnahme für anderen Dienst;fsba
22;Gerichtsgutachten;fsba
23;sonstiges;fsba
999;keine Angabe;fsba
1;nicht berufstätig;fsbe
2;Vollzeit angestellt;fsbe
3;Teilzeit angestellt;fsbe
4;Schichtarbeit;fsbe
5;selbständig;fsbe
6;arbeitslos (ALGI/II);fsbe
7;Sozialhilfe;fsbe
8;berentet;fsbe
9;in Ausbildung oder Umschulung;fsbe
10;sonstige;fsbe
999;keine Angabe;fsbe
1;Deutschland;fshe
2;Europa;fshe
3;Ost-Europa;fshe
4;Türkei;fshe
5;arabische Länder;fshe
6;Schwarz-Afrika;fshe
7;Asien;fshe
8;Nordamerika;fshe
9;Lateinamerika;fshe
10;Australien;fshe
11;andere Länder;fshe
999;keine Angabe;fshe
1;Krankheit, Behinderung;fspbe
2;Alkohol-, Drogenkonsum;fspbe
3;chronifizierte psychische Erkrankung;fspbe
4;Opfer familiärer Gewalt, sex. Missbrauchs;fspbe
5;starke Traumatisierung (Krieg, Folter);fspbe
6;Überforderung;fspbe
7;Isolation und Kontaktschwierigkeiten;fspbe
11;Trennung, Scheidung, Sorge-/Umgangsrecht;fspbe
12;Beziehungskonflikte;fspbe
8;Verschuldung;fspbe
9;unzureichende Wohnverhältnisse;fspbe
10;sonstige;fspbe
999;keine Angabe;fspbe
1;allg. Erziehungs-, Entwicklungsproblem;fspbk
2;neurotische oder psychosomatische Reaktion;fspbk
3;Vernachlässigung, Verwahrlosung;fspbk
4;Opfer von Gewalt, Misshandlung;fspbk
5;Sexueller Missbrauch (Opfer);fspbk
6;Alkohol-, Drogenkonsum;fspbk
7;strafbares Verhalten;fspbk
8;Schulleistungsproblem;fspbk
9;Schulverweigerung;fspbk
10;soziale Kontaktschwierigkeit, Isolation;fspbk
11;aggressives Verhalten;fspbk
12;Gewaltbereitschaft des Jugendlichen;fspbk
13;berufliche Perspektive;fspbk
14;Behinderung;fspbk
15;Suizidgefährdung;fspbk
16;Esstörung;fspbk
17;traumat. Verlust, Tod einer Bezugsperson;fspbk
18;sonstige;fspbk
999;keine Angabe;fspbk
1;Erziehungsberatung;fsle
2;Trennungs-, Scheidungsberatung, Mediation, Umgangsberatung;fsle
3;Begleiteter Umgang;fsle
4;Familienberatung, -therapie;fsle
5;Paarberatung, -therapie;fsle
6;Einzelbetreuung / -therapie Kind;fsle
7;Einzelbetreuung / -therapie Jugendlicher;fsle
8;Einzelbetreuung / -therapie Erwachsener;fsle
9;Gruppentherapie Kinder;fsle
10;Gruppentherapie Jugendliche;fsle
11;Gruppentherapie Erwachsene;fsle
12;Arbeit im sozialen Umfeld;fsle
13;spezieller Diagnostikauftrag;fsle
14;Hilfeplanung, Hilfekonferenz;fsle
15;fachliche Bescheinigung für Klienten;fsle
16;Begleitung KJHG-Therapie;fsle
17;Fachdienstliche Stellungnahme;fsle
18;Gerichtsgutachten;fsle
19;sonstige;fsle
999;keine Angabe;fsle
0;weniger als 30 Minuten;fskd;0;29
1;30 bis 60 Minuten;fskd;30;59
2;60 bis 120 Minuten;fskd;60;119
3;mehr als 120 Minuten;fskd;120;99999
0;weniger als 30 Minuten;kdbs;0;2
1;30 bis 60 Minuten;kdbs;3;5
2;60 bis 120 Minuten;kdbs;6;11
3;mehr als 120 Minuten;kdbs;12;99999
1;Mutter;teilnbs
2;Vater;teilnbs
3;Stiefmutter;teilnbs
4;Stiefvater;teilnbs
5;Kind/Jugendlicher;teilnbs
6;Geschwister;teilnbs
7;Andere Verwandte;teilnbs
8;Andere Institutionen;teilnbs
9;sonstige;teilnbs
0;weniger als 30 Minuten;fuadbs;0;2
1;30 bis 60 Minuten;fuadbs;3;5
2;60 bis 120 Minuten;fuadbs;6;11
3;mehr als 120 Minuten;fuadbs;12;99999
1;Mutter;fska
2;Vater;fska
3;Kind/Jugendlicher;fska
4;Paar;fska
5;Familie;fska
6;Sozialarbeiter;fska
7;Lehrer;fska
8;Erzieher;fska
9;Hilfebesprechung;fska
10;Sonstige;fska
1;persönlicher Kontakt §28;kabs
2;telefonischer Kontakt (mit Beratungscharakter);kabs
3;Schreiben;kabs
4;Fachkontakt;kabs
5;ausgefallener Kontakt;kabs
6;Gruppenkontakt;kabs
7;E-Mail;kabs
8;interner Fachkontakt, Fallbesprechung;kabs
9;fallbezogene Fahrzeit;kabs
1;ausgefallene Erstgespräche ohne Fall-Nr.;fuabs
2;offen angebotene Zeiten (Präsenz, Sekretariatsvertretung, Beratungstelefonate mit Nicht-Klienten....);fuabs
3;Gruppenarbeit (K6);fuabs
4;gebührenpflichtige Leistungen;fuabs
5;Vernetzung;fuabs
6;Familien- und Jugendbildung;fuabs
7;Fahrzeiten;fuabs
0;keine Angabe;fskat;0;0
1;1-5;fskat;1;5
2;6-10;fskat;6;10
3;11-15;fskat;11;15
4;16-20;fskat;16;20
5;21-30;fskat;21;30
6;31-40;fskat;31;40
7;41-50;fskat;41;50
8;mehr als 50;fskat;51;
1;Mutter;klerv
2;Vater;klerv
3;Geschwister;klerv
4;Halbgeschw.;klerv
5;Stiefmutter;klerv
6;Stiefvater;klerv
7;Grossmutter;klerv
8;Grossvater;klerv
9;verwandt;klerv
10;Pflegemutter;klerv
11;Pflegevater;klerv
12;Adoptivmutter;klerv
13;sonstige;klerv
999;k. Angabe;klerv
1;ASD;klinsta
2;KJGD/KJPD;klinsta
3;Kita/Hort;klinsta
4;Schule;klinsta
5;Heim;klinsta
6;Wohngemeinschaft;klinsta
7;Freizeiteinr.;klinsta
8;Arzt;klinsta
9;Klinik;klinsta
10;Gericht;klinsta
11;Schulpsychologie;klinsta
12;Sonstige;klinsta
999;keine Angabe;klinsta
1;Schule;fsqualij
2;Studium;fsqualij
3;Lehre;fsqualij
4;Arbeitslos;fsqualij
5;berufstätig;fsqualij
5;Berufsförderung;fsqualij
6;sonstige;fsqualij
999;keine Angabe;fsqualij
1;Schule;fsquali
2;ungelernt;fsquali
3;Berufsausbildung;fsquali
4;Facharbeiter;fsquali
5;Hochschulabschluss;fsquali
6;Umschulung;fsquali
7;sonstige;fsquali
999;keine Angabe;fsquali
i;im Dienst;status
a;nicht im Dienst;status
A;EFB-Dienststelle;stzei
admin;Administrator;benr
bearb;Fallbearbeiter;benr
verw;Verwaltung;benr
protokol;protokol;benr
l;laufender Fall;stand
zdA; zu den Akten;stand
t;Notiz wichtig;notizbed
f;Notiz;notizbed
t;ist im Verteiler;vert
f;nicht im Verteiler;vert
ja;aktuelle Einrichtung;einrstat
nein;frühere Einrichtung;einrstat
0;Musterregierungsbezirk;rbz
01;Musterkreis;kr
000;N.N.;gm
000;N.N.;gmt
1;Träger der öffentl. JGH;traeg
2;Träger der freien JGH;traeg
1;Beratung wurde einvernehmlich beendet;bgr
2;letzter Kontakt liegt mehr als 6 M. zurück;bgr
3;Weiterverweisung;bgr
1;unter 3;ag
2;3 - unter 6;ag
3;6 - unter 9;ag
4;9 - unter 12;ag
5;12 - unter 15;ag
6;15 - unter 18;ag
7;18 - unter 21;ag
8;21 - unter 24;ag
9;24 - unter 27;ag
01;bei Eltern;fs
02;bei 1 Elternteil mit Stiefelternteil;fs
03;bei alleinerziehendem Elternteil;fs
04;bei Grosseltern, Verwandten;fs
05;in einer Pflegestelle;fs
06;in einem Heim;fs
07;in einer Wohngemeinschaft;fs
08;in eigener Wohnung;fs
09;ohne feste Unterkunft;fs
10;an unbekanntem Ort;fs
1;deutsch;hke
2;nicht-deutsch;hke
3;unbekannt;hke
0;kein Geschwister;gsa;0;0
1;1 Geschwister;gsa;1;1
2;2 Geschwister;gsa;2;2
3;3 Geschwister;gsa;3;3
4;mehr als 3 Geschwister;gsa;4;20
0;bekannt;gsu
1;unbekannt;gsu
1;jungen Menschen selbst;zm
2;Eltern gemeinsam;zm
3;Mutter;zm
4;Vater;zm
5;soziale Dienste;zm
6;Sonstige;zm
1;Entwicklungsauffälligkeiten;ba0
0;leer;ba0
1;Beziehungsprobleme;ba1
0;leer;ba1
1;Schule-/Ausbildungsprobleme;ba2
0;leer;ba2
1;Straftat d. Jugendl./jungen Volljährigen;ba3
0;leer;ba3
1;Suchtprobleme des jungen Menschen;ba4
0;leer;ba4
1;Anzeichen für Kindesmisshandlung;ba5
0;leer;ba5
1;Anzeichen für sexuellen Missbrauch;ba6
0;leer;ba6
1;Trennung/Scheidung der Eltern;ba7
0;leer;ba7
1;Wohnungsprobleme;ba8
0;leer;ba8
1;sonstige Probleme in u. mit der Familie;ba9
0;leer;ba9
1;Erziehungs-/Familienberatung;schw
2;Jugendberatung;schw
3;Suchtberatung;schw
1;allein;fbe0
2;in der Gruppe;fbe0
0;leer;fbe0
1;allein;fbe1
2;in der Gruppe;fbe1
0;leer;fbe1
1;in der Familie;fbe2
0;leer;fbe2
1;im sozialen Umfeld;fbe3
0;leer;fbe3
txt;text/plain;mimetyp
asc;text/plain;mimetyp
html;text/html;mimetyp
htm;text/html;mimetyp
pdf;application/pdf;mimetyp
ps;application/postscript;mimetyp
doc;application/msword;mimetyp
dot;application/msword;mimetyp
wrd;application/msword;mimetyp
rtf;application/rtf;mimetyp
xls;application/x-msexcel;mimetyp
sdw;application/soffice;mimetyp
sxw;application/soffice;mimetyp
sdc;application/vnd.stardivision.calc;mimetyp
odt;application/vnd.oasis.opendocument.text;mimetyp
ods;application/vnd.oasis.opendocument.spreadsheet;mimetyp
odp;application/vnd.oasis.opendocument.presentation;mimetyp
odg;application/vnd.oasis.opendocument.graphics;mimetyp
odc;application/vnd.oasis.opendocument.chart;mimetyp
odf;application/vnd.oasis.opendocument.formula;mimetyp
odi;application/vnd.oasis.opendocument.image;mimetyp
odm;application/vnd.oasis.opendocument.text-master;mimetyp
zip;application/zip;mimetyp
gtar;application/x-gtar;mimetyp
tgz;application/x-gtar;mimetyp
gz;application/x-gzip;mimetyp
tar;application/x-tar;mimetyp
rtx;text/richtext;mimetyp
gif;image/gif;mimetyp
jpg;image/jpeg;mimetyp
jpeg;image/jpeg;mimetyp
jpe;image/jpeg;mimetyp
tiff;image/tiff;mimetyp
tif;image/tiff;mimetyp
png;image/png;mimetyp
bmp;image/bmp;mimetyp
bnotiz;Beraternotiz;dokart
Vm;Vermerk;dokart
anotiz;Aktennotiz;dokart
Brief;Brief;dokart
Prot;Protokoll;dokart
Dok;Dokument;dokart
Antrag;Antrag;dokart
Bericht;Bericht;dokart
Stellung;Stellungnahme;dokart
Befund;Befunddokument;dokart
Gutacht;Gutachten;dokart
Beschein;Bescheinigung;dokart
Sonstig;Sonstiges;dokart
Kinder;Kinder;teiln
Jugendl;Jugendliche;teiln
Eltern;Eltern;teiln
Väter;Väter;teiln
Mütter;Mütter;teiln
Altgem;Altersgemischt;teiln
Familien;Familien;teiln
Erzieher;ErzieherInnen;teiln
Lehrer;Lehrer;teiln
Paare;Paare;teiln
sonstige;sonstige;teiln
Eabend;Elternabend;grtyp
Kurs;Kurs;grtyp
Therapie;Therapiegruppe;grtyp
Seminar;Seminar;grtyp
Selbster;Selbsterfahrung;grtyp
Superv;Supervision;grtyp
sonstige;sonstige;grtyp
1;Nein;gfall
2;Ja;gfall
13;außerhalb;wohnbez
999;keine Angabe;wohnbez
A;DBSite A;dbsite;1;1000000000
0;innerhalb des Geltungsbereichs des Straßenkatalogs;lage
1;außerhalb des Geltungsbereichs des Straßenkatalogs;lage
999;keine Angabe;lage
protocol;off;config
"""

# Ergänzungen für die neue Bundesstatistik 2007
code_list_str += \
"""12;Muster-Land;land
11;11 Muster-Einrichtungsnummer;einrnr
1;Eltern leben zusammen;shf
2;Elternteil lebt alleine ohne (Ehe-)Partner (mit/ohne weitere/n Kinder/n);shf
3;Elternteil lebt mit neuer Partnerin/neuem Partner (mit/ohne weitere/n Kinder/n)(z.B. Stiefelternkonstellation);shf
4;beide Eltern sind verstorben;shf
5;unbekannt;shf
1;ja;ja_nein
2;nein;ja_nein
0;unbekannt;ja_ne_un
1;ja;ja_ne_un
2;nein;ja_ne_un
01;Erziehungsberatung vorrangig mit der Familie (Eltern und Kind);hilf_art
02;Erziehungsberatung vorrangig mit den Eltern (zusammen oder einzeln);hilf_art
03;Erziehungsberatung vorrangig mit dem jungen Menschen;hilf_art
01;In der Wohnung der Herkunftsfamilie/Adoptivfamilie;hilf_ort
02;In (der Wohnung) einer Verwandtenfamilie;hilf_ort
03;In einer nicht-verwandten Familie (privater Haushalt);hilf_ort
04;In einer Einrichtung der Kindertagesbetreuung;hilf_ort
05;In der Schule;hilf_ort
06;In den Räumen eines ambulaten Dienstes/einer Beratungsstelle;hilf_ort
07;In einer Einrichtung über Tag;hilf_ort
08;In einer Mehrgruppen-Einrichtung über Tag und Nacht;hilf_ort
09;In einer Eingruppen-Einrichtung (auch Außenwohngruppe) über Tag und Nacht;hilf_ort
10;In der Wohnung des Jugendlichen/jungen Volljährigen;hilf_ort
11;Außerhalb von Deutschland;hilf_ort
12;Sonstiger Ort (z.B. JVA, Klinik, Frauenhaus);hilf_ort
01;Im Haushalt der Eltern/eines Elternteils/des Sorgeberechtigten;auf_ort
02;In einer Verwandtenfamilie;auf_ort
03;In einer nicht.verwandten Familie (z.B. Pflegestelle);auf_ort
04;In der eigenen Wohnung;auf_ort
05;In einer Pflegefamilie;auf_ort
06;In einem Heim oder einer betreuten Wohnform;auf_ort
07;In der Psychiatrie;auf_ort
08;In einer sozialpädagogisch betreuten Einrichtung (z.B. Internat, Mutter-/Vater-Kind Einrichtung);auf_ort
09;Sonstiger Aufenthalt (z.B. JVA, Frauenhaus);auf_ort
10;Ohne festen Aufenthalt;auf_ort
11;An unbekanntem Ort;auf_ort
10;Träger der öffentlichen Jugendhilfe;traeger
21;Arbeiterwohlfahrt oder deren Mitgliedsorganisation;traeger
22;Deutscher Paritätischer Wohlfahrtsverband oder dessen Mitgliedsorganisation;traeger
23;Deutsches Rotes Kreuz oder dessen Mitgliedsorganisation;traeger
24;Diakonisches Werk oder sonstiger der EKD angeschlossener Träger;traeger
25;Deutscher Caritasverband oder sonstiger katholischer Traeger;traeger
26;Zentralwohlfahrtsinstitut der Juden in Deutschland oder jüdische Kultusgemeinde;traeger
27;Sonstige Religionsgemeinschaft des öffentlichen Rechts;traeger
28;Sonstiger anerkannter Träger der Jugendhilfe;traeger
29;Sonstige juristische Person, andere Vereinigung;traeger
30;Wirtschaftsunternehmen (privat-gewerblich);traeger
40;Pflegefamilie, die Vollzeitpflege gemäß §33 SGB VIII durchführt;traeger
1;Junger Mensch selbst;aip
2;Eltern bzw. Personensorgeberechtigte/r;aip
3;Schule/Kindertageseinrichtung;aip
4;Soziale/r Dienst/e und andere Institution/en (z.B. Jugendamt);aip
5;Gericht/Staatsanwaltschaft/Polizei;aip
6;Arzt/Klinik/Gesundheitsamt;aip
7;Ehemalige Klienten/Bekannte;aip
8;Sonstige;aip
10;Unversorgtheit des jungen Menschen;gruende
11;Unzureichende Förderung/Betreuung/Versorgung des jungen Menschen in der Familie;gruende
12;Gefährdung des Kindeswohls;gruende
13;Eingeschränkte Erziehungskompetenz der Eltern/Personensorgeberechtigten;gruende
14;Belastungen des jungen Menschen durch Problemlagen der Eltern;gruende
15;Belastungen des jungen Menschen durch familiäre Konflikte;gruende
16;Auffälligkeiten im sozialen Verhalten (dissoziales Verhalten) des jungen Menschen;gruende
17;Entwicklungsauffälligkeiten/seelische Probleme des jungen Menschen;gruende
18;Schulische/beruflische Probleme des jungen Menschen;gruende
19;Übernahme von einem anderen Jugendamt wegen Zuständigkeitswechsels;gruende
10;Beendigung gemäß Hilfeplan/Beratungszielen;grende
20;Beendigung abweichend von Hilfeplan/Beratungszielen durch den Sorgeberechtigten/den jungen Volljährigen (auch durch unzureichende Mitwirkung);grende
21;Beendigung abweichend von Hilfeplan/Beratungszielen durch die bisher betreuende Einrichtung, die Pflegefamilie, den Dienst;grende
22;Beendigung abweichend von Hilfeplan/Beratungszielen durch den Minderjährigen;grende
30;Adoptionspflege/Adoption;grende
40;Abgabe an ein anderes Jugendamt wegen Zuständigkeitswechsels;grende
50;Sonstige Gründe;grende
1;Zuständigkeitswechsel:Fortführung in derselben Pflegefamilie bzw. Einrichtung;unh
2;Weiterverweisung an Eheberatung, Schuldnerberatung, Kinder- und Jugendlichenpsychotherapeuten, andere Einrichtungen;unh
3;Beratung in allgemeinen Fragen der Erziehung durch den Allgemeinen Sozialdienst (ASD) (§16 Abs.2 Nr.2 SGB VIII);unh
4;Hilfe zur Erziehung gemäß §§27-35, 41 SGB VIII;unh
5;Eingliederungshilfe gemäß §35a SGB VIII;unh
6;Keine nachfolgende Hilfe gemäß §§27-35, 41 SGB VIII bekannt;unh
1;0-2;jghag;0;2
2;3-5;jghag;3;5
3;6-9;jghag;6;9
4;10-13;jghag;10;13
5;14-17;jghag;14;17
6;18-20;jghag;18;20
7;21-26;jghag;21;26
8;ab 27;jghag;27;99
"""

# Ergänzungen für frei definierbare Fragen in der Fachstatistik
code_list_str += """
1;Merkmal 1;fsjoka1
1;Merkmal 1;fsjoka2
1;Merkmal 1;fsjoka3
1;Merkmal 1;fsjoka4
1;Merkmal 1;fsjokf5
1;Merkmal 1;fsjokf6
1;Merkmal 1;fsjokf7
1;Merkmal 1;fsjokf8
"""

#
# Welche Kategorien sind Bereichskategorien?
#
bereichs_kategorien_str = "fskat gsa dbsite jghag kdbs fuadbs"


#
# Kategorien-Liste
#
# Kategorien-Code;Name der Kategorie
#

kategorie_list_str = \
"""verwtyp;Feldverwendungstyp; Kategorie für das Feld der Metatabelle
fsag;Altersgruppe Kind/Jugendliche
fsagel;Altersgruppe Eltern
fsfs;Lebensmittelpunkt des Kindes
fszm;Zugangsweg
fsba;Vorstellungsanlass bei der Anmeldung
fsbe;Beschäftigungsverhältnis der Eltern
fshe;Herkunftsland der Eltern
fspbe;Problemspektrum Eltern
fspbk;Problemspektrum Kind, Jugendliche
fsle;Erbrachte Leistungen
fskd;Dauer des Kontakts
kdbs;Dauer des Kontakts in 10Min. Einheiten (BS)
fuadbs;Dauer der fallunabhängigen Aktivität in 10Min. Einheiten (BS)
fska;Art des Beratungskontakts
kabs;Art des Beratungskontakts (BS)
teilnbs;Teilnehmer am Kontakt (BS)
fuabs;Art der fallunabhängigen Aktivität (BS)
fskat;Anzahl der Termine
fsqualij;sozialer Status Jugendlicher, 14-27
fsquali;Qualifikation der Eltern
klerv;Verwandtschaftsgrad
klinsta;Einrichtungskontakt
status;Mitarbeiterstatus
stzei;Dienststelle
benr;Benutzungsrecht
stand;Bearbeitungsstand
notizbed;Notizbedeutung
vert;im Verteiler
einrstat;Aktueller Kontakt
rbz;Regierungsbezirk
kr;Kreis
gm;Gemeinde
gmt;Gemeindeteil
traeg;Jugendhilfe-Träger
bgr;Beendigungsgrund
gs;Geschlecht
ag;Alter
fs;Junger Mensch lebt bei
hke;Staatsangehörigkeit
zm;1. Kontakt durch
gsa;Geschwisteranzahl
gsu;Kenntnis der Geschwisterzahl
ba0;Beratungsanlass 0
ba1;Beratungsanlass 1
ba2;Beratungsanlass 2
ba3;Beratungsanlass 3
ba4;Beratungsanlass 4
ba5;Beratungsanlass 5
ba6;Beratungsanlass 6
ba7;Beratungsanlass 7
ba8;Beratungsanlass 8
ba9;Beratungsanlass 9
schw;Beratungsschwerpunkt
fbe0;beim jungen Menschen
fbe1;bei den Eltern
fbe2;in der Familie
fbe3;im sozialen Umfeld
mimetyp;Mime Typ
dokart;Der Eintrag ist
teiln;Teilnehmer/innnen
grtyp;Gruppentyp
gfall;Geschwisterfall
wohnbez;Wohnbezirksnr des Klienten
dbsite;Datenbank-Site
lage;Lage innerhalb oder außerhalb des Geltungsbereichs des Straßenkatalogs
config;Konfigurationseinstellungen
"""

# Ergänzungen für die neue Bundesstatistik 2007
kategorie_list_str += """
shf;Situation in der Herkunftsfamilie
ja_nein;Ja oder Nein
ja_ne_un;Ja/Nein oder unbekannt
hilf_art;Art der Hilfe
hilf_ort;Ort der Hilfe
auf_ort;Aufenthaltsort vor bzw. nach der Hilfe
traeger;Traeger der Einrichtung oder des Dienstes
aip;Die Hilfe/Beratung anregende Institution oder Person
gruende;Gründe für die Hilfegewährung
grende;Gründe für die Beendigung der Hilfe/Beratung
unh;Unmittelbar nachfolgende Hilfe
land;Land (Feld 2-3)
einrnr;Einrichtungs-Nr (Feld 10-15)
jghag;Altersgruppe
"""

# Ergänzungen für frei definierbare Fragen in der Fachstatistik
kategorie_list_str += """
fsjoka1;Frei definierbare Kategorie für Joker 1
fsjoka2;Frei definierbare Kategorie für Joker 2
fsjoka3;Frei definierbare Kategorie für Joker 3
fsjoka4;Frei definierbare Kategorie für Joker 4
fsjokf5;Frei definierbare Kategorie für Joker 5
fsjokf6;Frei definierbare Kategorie für Joker 6
fsjokf7;Frei definierbare Kategorie für Joker 7
fsjokf8;Frei definierbare Kategorie für Joker 8
"""

#
# Mitarbeiterliste für Ersteintrag
#
# Vorname;Nachname;ben;status;benr;stzei;pw-hash
# Beispiel:
# Admin;Administrator;Admin;i;admin;A
# Gast;Gast;Gast;i;bearb;A
# Susi;Meier;Susi;i;verw;A
# Elfi;Hansen;Elfi;i;bearb;B
#
# Admin muss hier stehen, sonst kann man sich nicht anmelden 
#

mitarbeiter_list_str = \
"""Admin;Administrator;Admin;i;admin;A;4e7afebcfbae000b22c7c85e5560f89a2a0280b4
"""














