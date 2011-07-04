# coding: latin-1

"""Dokumentation der fachlischen Konfigurationsvariablen

Dict mit Variablenname als Schlüssel.

Wert ist ein tuple mit vier Feldern:

- fachlich: boolean, falls True ist die Variable vom Anwendungsadministrator editierbar.
- valid_pattern: regex oder None zur Validierung.
- beschreibung: Kurzbeschreibung (möglichst eine Zeile)
- doku: Weitere Dokumentation
"""

import re

def re_wohnt_nicht_ausserhalb():
    """
    Ist etwas komplizierter, daher ausgelagert,
    >>>
    >>> bool(re.match(re_wohnt_nicht_ausserhalb(), "ort:Berlin"))
    True
    >>> bool(re.match(re_wohnt_nicht_ausserhalb(), "ort:Berlin;bezirk:Treptow"))
    True
    >>> bool(re.match(re_wohnt_nicht_ausserhalb(), "ort :Berlin;Brandenburg"))
    True
    >>> bool(re.match(re_wohnt_nicht_ausserhalb(), "plz:Berlin"))
    False
    >>> bool(re.match(re_wohnt_nicht_ausserhalb(), "plraum:Berlin"))
    True
    >>> bool(re.match(re_wohnt_nicht_ausserhalb(), " plz:12345; 65432;ortsteil:Großbeeren"))
    True
    >>> bool(re.match(re_wohnt_nicht_ausserhalb(), " plz:1234; 65432;ortsteil:Großbeeren"))
    False
    >>> bool(re.match(re_wohnt_nicht_ausserhalb(), "plz:12345; 65432;\\nortsteil:Großbeeren;\\nwe123 ; samtgemeinde:a;b;c"))
    True
    """
    res = re.compile(r"""
         ^\s*$|                             # kann leer sein
           ^(
              (\s*(bezirk|ort|ortsteil|samtgemeinde|plraum)\s*:\s*[^;:]+\s*(;\s*[^;:]+\s*)*)
              |
              (\s*plz\s*:\s*\d{5,5}\s*(;\s*\d{5,5}\s*)*)
            )
           (;
              (\s*(bezirk|ort|ortsteil|samtgemeinde|plraum)\s*:\s*[^;:]+\s*(;\s*[^;:]+\s*)*)
              |
              (\s*plz\s*:\s*\d{5,5}\s*(;\s*\d{5,5}\s*)*)
           )*
          $""", re.VERBOSE)
    return res

param_doks = {
    'wiederaufnahmefrist':
        (True, 
         r"^\d{1,2}$",
         "Anzahl der Monate, innerhalb derer ein "
         'abgeschlossener Fall wiederaufgenommen werden kann ("z.d.A. rückgängig").',
         "Danach muss ein neuer Fall angelegt werden.",
         ),
    
    'loeschfrist':
        (True,
         r"^\d{1,3}$",
         "Löschfrist in Monaten.",
         "Akten, die älter sind, können vom Administrator gelöscht werden.",
         ),                                               
    
    'session_time':
        (True,
         r"^[123456789]\d{0,2}$",
         "Länge einer Session in Minuten. ",
         "Nach dieser Zeit wird ein Benutzer"
         " automatisch abgemeldet, wenn er keine Eingaben mehr macht."
         ),
    
    'admin_name':
        (True,
         None,
         "Name des Anwendungsadministrators.",
         "Wird in Fehlermeldungen genannt.",
         ),
    
    'admin_tel':
        (True,
         None,
         "Telefonnummer des Anwendungsadministrators.",
         "Wird in Fehlermeldungen genannt.",
         ),
    
    'admin_email':
        (True,
         None,
         "Email-Adresse des Anwendungsadministrators.",
         "Wird in Fehlermeldungen genannt.",
         ),
    
    'instance_title':
        (True,
         None,
         """Langname für die Instanz.""",
         """Erscheint bei der
Anmeldung und in der Statuszeile.""",
         ),
    
    'beratungskontakte':
        (True,
         None,
         """Falls <code>true</code> können in der
Klientenakte einzelne Beratungskontakte eingetragen werden.""",
         """Die Summen werden in die Bundesstatistik und in die 
Fachstatistik als Vorgabe übernommen.""",
         ),
    
    'beratungskontakte_bs':
        (True,
         None,
         """Falls <code>true</code> treten Anpassungen speziell
für Braunschweig in Kraft.""",
         """Die Variable <code>beratungskontakte</code>
muss ebenfalls auf <code>true</code> stehen."""
         ),
    
    'fallunabhaengige_aktivitaeten_bs':
        (True,
         None,
         """Falls <code>true</code> können
fallunabhängige Aktivitäten eingetragen und ausgewertet
werden. Speziell für Braunschweig.""",
         ),
    
    'strassenkatalog':
        (True,
         None,
         """Falls diese Variable nicht leer ist, wird bei der Adresseingabe der Straßenkatalog
verwendet.""",
         """Der eigentliche Wert der Variable spielt nur bei der Erstinstallation
der Instanz eine Rolle.<br />Eine Instanz ohne Straßenkatalog kann auch später noch für die Verwendung 
mit Straßenkatalog eingerichtet werden, indem der Straßenkatalog über 	
"Administratorhauptmenü -- Straßenkatalog importieren" importiert wird und der Variable 'strassenkatalog' ein
beliebiger Wert zugewiesen wird, beispielsweise der Ortsname.""",
         ),
    
    'strassenkatalog_vollstaendig':
        (True,
         None,
         """Falls <code>true</code> wird
angenommen, dass der Straßenkatalog Einträge für jede einzelne
Hausnummer enthält.""",
         """Ansonsten wird angenommen, dass lediglich Einträge für ganze Straßen
bzw. für bestimmte Intervalle von Hausnummern vorhanden sind.""",
         ),
    
    'strassensuche':
        (True,
         r"^(\s*(ort|bezirk|ortsteil|samtgemeinde)\s*)*$",
         """Bestimmt die Anzeige von Zusatzinformationen aus dem
Straßenkatalog bei der Darstellung und Eingabe von Adressen.""",
         """Zulässige Werte sind: <code>ort bezirk ortsteil samtgemeinde</code>.<br /><br />
Beispiele:
<ul>
<li>In Berlin gibt es nur einen Ort im Straßenkatalog, nämlich 'Berlin'. Das Feld <code>ort</code> ist daher 
nicht nötig. Ortsteil und Samtgemeinde haben im Straßenkatalog keine Werte, Bezirk allerdings schon. Der sinnvolle
Wert für Berlin ist also
<pre>
    bezirk
</pre>
</li>
<li>In Gifhorn gibt es mehrere Orte im Straßenkatalog. Sowohl Ortsteile und Samtgemeinden spielen eine Rolle und sind
im Straßenkatalog erfasst, Bezirke jedoch nicht. Der sinnvolle
Wert hier ist also
<pre>
    ort ortsteil samtgemeinde
</pre>
</li>
<li>Wenn es nur einen Ort gibt und weder Bezirke, Ortsteile oder Samtgemeinden im Straßenkatalog erfasst sind,
sollte die Variable leer bleiben.
</ul>
<br /><br />Irrelevant, wenn kein Straßenkatalog verwendet wird.""",
         ),
    
    'anmeldungsdaten_obligatorisch':
        (True,
         None,
         """Falls <code>true</code>
werden die Anmeldungsdaten obligatorisch im Aufnahmeformular erhoben anstatt optional 
in einer getrennten Maske.""",
         """Die entsprechenden Pflichfelder sind dabei
auszufüllen. Eine spätere Bearbeitung der Anmeldungsdaten erfolgt
wie bisher in einer eigenständigen Maske (analog der späteren
Bearbeitung einer Leistung).""",
         ),
    
    'sql_abfrage':
        (True,
         None,
         """Falls <code>true</code>
steht die Maske zum Absetzen von SQL-Abfragen vom
Administrationsmenü aus zur Verfügung.""",
         '',
         ),
    
    'warnung_bei_fachstatistik_akte_diskrepanz':
        (True,
         None,
         """Falls <code>true</code>
wird beim Speichern der Fachstatistik auf eine Diskrepanz 
zwischen Akte und Fachstatistik hingewiesen, falls vorhanden.""",
         """Wenn man bei dem
dann zur Verfügung stehendem Item "Diskrepanz zur Akte zulassen" ein Häkchen
setzt, kann man trotzdem speichern.<br />
Betroffen sind nur die Items 'Familienstatus',
'Empfohlen von' und 'Erbrachte Leistungen in der Fachstatistik', deren
Werte im Normalfall aus der Akte vorbelegt werden.""",
         ),
    
    'fachstatistik_akte_diskrepanz_nicht_zulassen':
        (True,
         None,
         """Falls <code>true</code>
werden Diskrepanzen zwischen Fachstatistik und Akte nicht zugelassen.""",
         """Die entsprechenden Items in der Fachstatistik zeigen die Werte
aus der Akte und sind nicht modifizierbar. Eine Diskrepanz kann
so gar nicht entstehen. Allerdings muss bei Änderungen in der
Akte die Fachstatistik neu abgespeichert werden, damit die
Änderungen übernommen und für die Statistik wirksam werden.<br />
Betroffen sind nur die Items 'Familienstatus',
'Empfohlen von' und 'Erbrachte Leistungen in der Fachstatistik', deren
Werte im Normalfall aus der Akte vorbelegt werden.""",
         ),

    'wohnt_nicht_ausserhalb':
        (True,
         re_wohnt_nicht_ausserhalb(),
         """Definiert die Teilmenge der Adressen, die im Sinne der Bundesstatistik in die Zuständigkeit
der Beratungsstelle fallen.""",
         """Aufgrund der hier angegebenen Kriterien wird entschieden, ob der Klient
in der Bundesstatistik als ausserhalb des Kreises der Beratungsstelle wohnend angegeben wird.
Als mögliche Kriterien kommen in Frage: <code>plz,ort,ortsteil,samtgemeinde,bezirk,plraum</code>.
Die Kriterien <code>ortsteil,samtgemeinde,bezirk</code> sind nur sinnvoll, wenn ein Straßenkatalog
verwendet wird und dieser auch entsprechende Angaben enthält.
<br /><br />
Die Kriterien werden wie folgt in der angegebenen Reihenfolge abgearbeitet:
<ul>
<li>Wenn die Klientenadresse keinen Wert für das Kriterium aufweist, wird zum nächsten
Kriterium übergegangen.
</li>
<li>Falls die Klientenadresse einen Wert hat und im Kriterium genannt wird, wohnt er nicht außerhalb. 
Ist der Wert im Kriterium nicht genannt, wohnt er außerhalb. In beiden Fällen werden die weiteren Kriterien 
nicht mehr betrachtet.
</li>
<li>Falls aufgrund fehlender Werte (oder fehlender Kriterien) kein Kriterium angewendet werden konnte, 
wird standardmäßig angenommen, dass der Klient nicht außerhalb wohnt. 
</li>
</ul>
Beispiele:
<ul>
<li>
<pre>
bezirk: Friedrichshain-Kreuzberg; ort: Berlin
</pre>
In Berlin enthalten alle mit dem Straßenkatalog abgeglichene Adressen einen Wert für den Bezirk. Da
jede Beratungsstelle genau für einen Bezirk zuständig ist, kann auf dieser Basis entschieden werden.
Falls eine Adresse nicht mit dem Straßenkatalog abgeglichen wurde, kann der Ort als Kriterium herangezogen 
werden, da in diesem Fall für Bezirk keine Angaben vorliegen.
</li>
<li>
Falls kein Straßenkatalog verwendet wird, kann nur der Ort, die Postleitzahl oder evt. der Planungsraum
(falls solche definiert sind und routinemäßig mit den Klientenadressen zusammen erfasst werden) als Kriterium
verwendet werden, z.B. (fiktiv!):
<pre>
plz: 12345;23456;34567
</pre>
Adressen mit diesen Postleitzahlen werden als nicht außerhalb wohnend betrachtet, alle
anderen als außerhalb. Falls die Klientenadresse keine 5-stellige PLZ enthält, gilt der Wert als fehlend. 
Ungenauigkeiten werden in Kauf genommen, da die Region der Zuständigkeit nicht immer exakt mit
den Regionen der Postleitzahlen übereinstimmt.
</li>
<li>
<pre>
samtgemeinde: Name1;Name2;Name3; plz: 12345;23456
</pre>
Analog zum Berliner Beispiel würde hier auch zunächst das Kriterium Samtgemeinde versucht, das
aber nur nach einem Abgleich mit dem Straßenkatalog bekannt ist. Für die nicht abgeglichenen Adressen
wird dann die Postleitzahl herangezogen. In seltenen Fällen kann das zu Fehlern führen, da
die Bereiche der Postleitzahlen manchmal nicht mit den Bereichen der Zuständigkeit exakt übereinstimmen.
</li>
</ul>

Falls das Ergebnis "wohnt außerhalb" ist, wird automatisch ein entsprechender Eintrag in die
Bundesstatistik vorgenommen, der beim Ausfüllen oben im Kasten "Falldaten" angezeigt wird.
Wenn möglich wird der <strong>amtliche Gemeindeschlüssel</strong> eingetragen. Wenn dieser 
nicht gefunden wird, wird Postleitzahl und Wohnort angegeben.
<br /><br />

<strong>Syntax</strong> wie in den Beispielen. Rund um die Trenner <code>;</code> und <code>:</code> dürfen Leerzeichen stehen.
Es können auch mehrere Zeilen verwendet werden. 
<br /><br />
Unter (Berater-) "Hauptmenü -- Statistik -- Teilmenge -- Neu -- Neue Bedingung" finden Sie 
für jedes Kriterium die Menge der möglichen Werte.
<br /><br />

Zur <strong>Testen</strong> gibt es unter "Aministratorhauptmenü -- Bundesstatistik -- Exportieren" einen neuen 
Punkt "Adressen außerhalb prüfen". Sie können dort in einer Tabelle sehen, welche Adressen als
außerhalb klassifiziert werden.
""",
         ),

    'gemeindeschluessel_von_plz':
        (False,
         r"^\s*$|^\s*\d{1,5}\s*(;\s*\d{1,5}\s*)*$",
         """Definiert die Teilmenge der amtlichen Gemeindeschlüssel für die Bundesstatistik.""",
         """In der Bundesstatistik soll der amtliche Gemeindeschlüssel für den Wohnort des Klienten 
eingetragen werden, wenn der Wohnort des Klienten außerhalb des Kreises der Beratungsstelle liegt. 
Um die Menge der Daten zu begrenzen, kann hier über die Anfangsziffern der Postleitzahl eine Teilmenge 
definiert werden. Wenn mehrere Ziffernfolgen angegeben werden, müssen diese mit <code>;</code> getrennt 
werden.<br /><br />
Im Normalfall brauchen Sie den voreingestellten Wert nicht zu ändern.
<br /><br />
Beispiele:
<ul>
<li>Alle Gemeindeschlüssel verwenden, außer die Postleitzahl der Gemeinde beginnt mit '9':
<pre>
0;1;2;3;4;5;6;7;8
</pre>
</li>
<li>Große Teile Niedersachsens:
<pre>
29;30;31;37;38
</pre>
</li>
<li>Nördliches Niedersachsen und Schleswig Holstein:
<pre>
2
</pre>
</li>
<li>Berlin und Umgebung:
<pre>
10;12;13;14;15;16
</pre>
</li>
<li>Bleibt die Variable leer, werden alle Gemeindeschlüssel verwendet.
</li>
</ul>

Wenn es bei der Erkennung von Gemeindeschluesseln zu vielen Fehlern kommt, beispielsweise wegen
unterschiedlicher Schreibweisen von Orten, kann man selber eine Datei 
<code>EBKUS_HOME/sql/gemeindeschluessel.csv</code> erstellen, bestehend aus einer Tabelle mit den Spalten 
<code>plz, ort ags</code>. Als Vorlage kann die Datei
<code>EBKUS_HOME/sql/gemeindeschluessel_cache.csv</code> dienen, die automatisch erzeugt wird, 
wenn die Konfigurationsvariable <code>gemeindeschluessel_von_plz</code> einen Wert hat.
""",
         ),

    'neumeldungen_nach_region':
        (True,
         r"^\s*$|^\s*[^;]+\s*(;\s*[^;]+\s*)*$",
         """Definiert eine Tabelle "Neumeldungen nach Region" unter "Neumelde- und Abschlusszahlen".""",
         """Die Regionen, für die in der Tabelle die Neumeldungen ausgezählt werden sollen, müssen unter 
"Hauptmenü -- Statistikabfrage -- Teilmenge -- Neu" als Teilmengendefinitionen eingeführt werden. Der Namen der
gewünschten Definitionen werden durch <code>;</code> getrennt aufgeführt.
<br /><br />
Beispiel:
<ul>
<li>
<pre>
    Gifhorn und Samtgemeinde Meinersen; Braunschweig 38120 und 38112
</pre>
</li>
</ul>
"Gifhorn und Samtgemeinde Meinersen" ist eine Teilmengendefinition mit der Definition:
<code>( ort = 'Gifhorn' ODER samtgemeinde = 'Meinersen' )</code>.
"Braunschweig 38120 und 38112" ist eine Teilmengendefinition mit der Definition:
<code>( ort = 'Braunschweig' UND plz = '38112' oder '38120' )</code>.
<br /><br />
""",
         ),
    
    'meldung_vom_admin':
        (True,
         "",
         """Inhalt wird als Meldung vom Administrator unübersehbar auf jeder EBKuS-Seite über der Statuszeile ausgegeben.""",
         """Damit kann der Administrator
Meldungen an alle aktiven EBKuS-Nutzer ausgeben, z.B. um einen
Ausfall von EBKuS wegen Wartungsarbeiten anzukündigen.
""",
         ),
    
    'keine_bundesstatistik':
        (False,
         "",
         """Fall kann ohne Bundestatistik abgeschlossen werden.""",
         """Alles andere sollte trotzdem noch funktionieren.
""",
         ),
    }

if __name__ == "__main__":
    import doctest
    doctest.testmod()
