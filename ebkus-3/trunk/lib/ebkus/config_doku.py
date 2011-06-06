# coding: latin-1

"""Dokumentation der fachlischen Konfigurationsvariablen

Dict mit Variablenname als Schl�ssel.

Wert ist ein tuple mit vier Feldern:

- fachlich: boolean, falls True ist die Variable vom Anwendungsadministrator editierbar.
- valid_pattern: regex oder None zur Validierung.
- beschreibung: Kurzbeschreibung (m�glichst eine Zeile)
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
    >>> bool(re.match(re_wohnt_nicht_ausserhalb(), " plz:12345; 65432;ortsteil:Gro�beeren"))
    True
    >>> bool(re.match(re_wohnt_nicht_ausserhalb(), " plz:1234; 65432;ortsteil:Gro�beeren"))
    False
    >>> bool(re.match(re_wohnt_nicht_ausserhalb(), "plz:12345; 65432;\\nortsteil:Gro�beeren;\\nwe123 ; samtgemeinde:a;b;c"))
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
         'abgeschlossener Fall wiederaufgenommen werden kann ("z.d.A. r�ckg�ngig").',
         "Danach muss ein neuer Fall angelegt werden.",
         ),
    
    'loeschfrist':
        (True,
         r"^\d{1,3}$",
         "L�schfrist in Monaten.",
         "Akten, die �lter sind, k�nnen vom Administrator gel�scht werden.",
         ),                                               
    
    'session_time':
        (True,
         r"^[123456789]\d{0,2}$",
         "L�nge einer Session in Minuten. ",
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
         """Langname f�r die Instanz.""",
         """Erscheint bei der
Anmeldung und in der Statuszeile.""",
         ),
    
    'beratungskontakte':
        (True,
         None,
         """Falls <code>true</code> k�nnen in der
Klientenakte einzelne Beratungskontakte eingetragen werden.""",
         """Die Summen werden in die Bundesstatistik und in die 
Fachstatistik als Vorgabe �bernommen.""",
         ),
    
    'beratungskontakte_bs':
        (True,
         None,
         """Falls <code>true</code> treten Anpassungen speziell
f�r Braunschweig in Kraft.""",
         """Die Variable <code>beratungskontakte</code>
muss ebenfalls auf <code>true</code> stehen."""
         ),
    
    'fallunabhaengige_aktivitaeten_bs':
        (True,
         None,
         """Falls <code>true</code> k�nnen
fallunabh�ngige Aktivit�ten eingetragen und ausgewertet
werden. Speziell f�r Braunschweig.""",
         ),
    
    'strassenkatalog':
        (True,
         None,
         """Falls diese Variable nicht leer ist, wird bei der Adresseingabe der Stra�enkatalog
verwendet.""",
         """Der eigentliche Wert der Variable spielt nur bei der Erstinstallation
der Instanz eine Rolle.<br />Eine Instanz ohne Stra�enkatalog kann auch sp�ter noch f�r die Verwendung 
mit Stra�enkatalog eingerichtet werden, indem der Stra�enkatalog �ber 	
"Administratorhauptmen� -- Stra�enkatalog importieren" importiert wird und der Variable 'strassenkatalog' ein
beliebiger Wert zugewiesen wird, beispielsweise der Ortsname.""",
         ),
    
    'strassenkatalog_vollstaendig':
        (True,
         None,
         """Falls <code>true</code> wird
angenommen, dass der Stra�enkatalog Eintr�ge f�r jede einzelne
Hausnummer enth�lt.""",
         """Ansonsten wird angenommen, dass lediglich Eintr�ge f�r ganze Stra�en
bzw. f�r bestimmte Intervalle von Hausnummern vorhanden sind.""",
         ),
    
    'strassensuche':
        (True,
         r"^(\s*(ort|bezirk|ortsteil|samtgemeinde)\s*)*$",
         """Bestimmt die Anzeige von Zusatzinformationen aus dem
Stra�enkatalog bei der Darstellung und Eingabe von Adressen.""",
         """Zul�ssige Werte sind: <code>ort bezirk ortsteil samtgemeinde</code>.<br /><br />
Beispiele:
<ul>
<li>In Berlin gibt es nur einen Ort im Stra�enkatalog, n�mlich 'Berlin'. Das Feld <code>ort</code> ist daher 
nicht n�tig. Ortsteil und Samtgemeinde haben im Stra�enkatalog keine Werte, Bezirk allerdings schon. Der sinnvolle
Wert f�r Berlin ist also
<pre>
    bezirk
</pre>
</li>
<li>In Gifhorn gibt es mehrere Orte im Stra�enkatalog. Sowohl Ortsteile und Samtgemeinden spielen eine Rolle und sind
im Stra�enkatalog erfasst, Bezirke jedoch nicht. Der sinnvolle
Wert hier ist also
<pre>
    ort ortsteil samtgemeinde
</pre>
</li>
<li>Wenn es nur einen Ort gibt und weder Bezirke, Ortsteile oder Samtgemeinden im Stra�enkatalog erfasst sind,
sollte die Variable leer bleiben.
</ul>
<br /><br />Irrelevant, wenn kein Stra�enkatalog verwendet wird.""",
         ),
    
    'anmeldungsdaten_obligatorisch':
        (True,
         None,
         """Falls <code>true</code>
werden die Anmeldungsdaten obligatorisch im Aufnahmeformular erhoben anstatt optional 
in einer getrennten Maske.""",
         """Die entsprechenden Pflichfelder sind dabei
auszuf�llen. Eine sp�tere Bearbeitung der Anmeldungsdaten erfolgt
wie bisher in einer eigenst�ndigen Maske (analog der sp�teren
Bearbeitung einer Leistung).""",
         ),
    
    'sql_abfrage':
        (True,
         None,
         """Falls <code>true</code>
steht die Maske zum Absetzen von SQL-Abfragen vom
Administrationsmen� aus zur Verf�gung.""",
         '',
         ),
    
    'warnung_bei_fachstatistik_akte_diskrepanz':
        (True,
         None,
         """Falls <code>true</code>
wird beim Speichern der Fachstatistik auf eine Diskrepanz 
zwischen Akte und Fachstatistik hingewiesen, falls vorhanden.""",
         """Wenn man bei dem
dann zur Verf�gung stehendem Item "Diskrepanz zur Akte zulassen" ein H�kchen
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
so gar nicht entstehen. Allerdings muss bei �nderungen in der
Akte die Fachstatistik neu abgespeichert werden, damit die
�nderungen �bernommen und f�r die Statistik wirksam werden.<br />
Betroffen sind nur die Items 'Familienstatus',
'Empfohlen von' und 'Erbrachte Leistungen in der Fachstatistik', deren
Werte im Normalfall aus der Akte vorbelegt werden.""",
         ),

    'wohnt_nicht_ausserhalb':
        (True,
         re_wohnt_nicht_ausserhalb(),
         """Definiert die Teilmenge der Adressen, die im Sinne der Bundesstatistik in die Zust�ndigkeit
der Beratungsstelle fallen.""",
         """Aufgrund der hier angegebenen Kriterien wird entschieden, ob der Klient
in der Bundesstatistik als ausserhalb des Kreises der Beratungsstelle wohnend angegeben wird.
Als m�gliche Kriterien kommen in Frage: <code>plz,ort,ortsteil,samtgemeinde,bezirk,plraum</code>.
Die Kriterien <code>ortsteil,samtgemeinde,bezirk</code> sind nur sinnvoll, wenn ein Stra�enkatalog
verwendet wird und dieser auch entsprechende Angaben enth�lt.
<br /><br />
Die Kriterien werden wie folgt in der angegebenen Reihenfolge abgearbeitet:
<ul>
<li>Wenn die Klientenadresse keinen Wert f�r das Kriterium aufweist, wird zum n�chsten
Kriterium �bergegangen.
</li>
<li>Falls die Klientenadresse einen Wert hat und im Kriterium genannt wird, wohnt er nicht au�erhalb. 
Ist der Wert im Kriterium nicht genannt, wohnt er au�erhalb. In beiden F�llen werden die weiteren Kriterien 
nicht mehr betrachtet.
</li>
<li>Falls aufgrund fehlender Werte (oder fehlender Kriterien) kein Kriterium angewendet werden konnte, 
wird standardm��ig angenommen, dass der Klient nicht au�erhalb wohnt. 
</li>
</ul>
Beispiele:
<ul>
<li>
<pre>
bezirk: Friedrichshain-Kreuzberg; ort: Berlin
</pre>
In Berlin enthalten alle mit dem Stra�enkatalog abgeglichene Adressen einen Wert f�r den Bezirk. Da
jede Beratungsstelle genau f�r einen Bezirk zust�ndig ist, kann auf dieser Basis entschieden werden.
Falls eine Adresse nicht mit dem Stra�enkatalog abgeglichen wurde, kann der Ort als Kriterium herangezogen 
werden, da in diesem Fall f�r Bezirk keine Angaben vorliegen.
</li>
<li>
Falls kein Stra�enkatalog verwendet wird, kann nur der Ort, die Postleitzahl oder evt. der Planungsraum
(falls solche definiert sind und routinem��ig mit den Klientenadressen zusammen erfasst werden) als Kriterium
verwendet werden, z.B. (fiktiv!):
<pre>
plz: 12345;23456;34567
</pre>
Adressen mit diesen Postleitzahlen werden als nicht au�erhalb wohnend betrachtet, alle
anderen als au�erhalb. Falls die Klientenadresse keine 5-stellige PLZ enth�lt, gilt der Wert als fehlend. 
Ungenauigkeiten werden in Kauf genommen, da die Region der Zust�ndigkeit nicht immer exakt mit
den Regionen der Postleitzahlen �bereinstimmt.
</li>
<li>
<pre>
samtgemeinde: Name1;Name2;Name3; plz: 12345;23456
</pre>
Analog zum Berliner Beispiel w�rde hier auch zun�chst das Kriterium Samtgemeinde versucht, das
aber nur nach einem Abgleich mit dem Stra�enkatalog bekannt ist. F�r die nicht abgeglichenen Adressen
wird dann die Postleitzahl herangezogen. In seltenen F�llen kann das zu Fehlern f�hren, da
die Bereiche der Postleitzahlen manchmal nicht mit den Bereichen der Zust�ndigkeit exakt �bereinstimmen.
</li>
</ul>

Falls das Ergebnis "wohnt au�erhalb" ist, wird automatisch ein entsprechender Eintrag in die
Bundesstatistik vorgenommen, der beim Ausf�llen oben im Kasten "Falldaten" angezeigt wird.
Wenn m�glich wird der <strong>amtliche Gemeindeschl�ssel</strong> eingetragen. Wenn dieser 
nicht gefunden wird, wird Postleitzahl und Wohnort angegeben.
<br /><br />

<strong>Syntax</strong> wie in den Beispielen. Rund um die Trenner <code>;</code> und <code>:</code> d�rfen Leerzeichen stehen.
Es k�nnen auch mehrere Zeilen verwendet werden. 
<br /><br />
Unter (Berater-) "Hauptmen� -- Statistik -- Teilmenge -- Neu -- Neue Bedingung" finden Sie 
f�r jedes Kriterium die Menge der m�glichen Werte.
<br /><br />

Zur <strong>Testen</strong> gibt es unter "Aministratorhauptmen� -- Bundesstatistik -- Exportieren" einen neuen 
Punkt "Adressen au�erhalb pr�fen". Sie k�nnen dort in einer Tabelle sehen, welche Adressen als
au�erhalb klassifiziert werden.
""",
         ),

    'gemeindeschluessel_von_plz':
        (False,
         r"^\s*$|^\s*\d{1,5}\s*(;\s*\d{1,5}\s*)*$",
         """Definiert die Teilmenge der amtlichen Gemeindeschl�ssel f�r die Bundesstatistik.""",
         """In der Bundesstatistik soll der amtliche Gemeindeschl�ssel f�r den Wohnort des Klienten 
eingetragen werden, wenn der Wohnort des Klienten au�erhalb des Kreises der Beratungsstelle liegt. 
Um die Menge der Daten zu begrenzen, kann hier �ber die Anfangsziffern der Postleitzahl eine Teilmenge 
definiert werden. Wenn mehrere Ziffernfolgen angegeben werden, m�ssen diese mit <code>;</code> getrennt 
werden.<br /><br />
Im Normalfall brauchen Sie den voreingestellten Wert nicht zu �ndern.
<br /><br />
Beispiele:
<ul>
<li>Alle Gemeindeschl�ssel verwenden, au�er die Postleitzahl der Gemeinde beginnt mit '9':
<pre>
0;1;2;3;4;5;6;7;8
</pre>
</li>
<li>Gro�e Teile Niedersachsens:
<pre>
29;30;31;37;38
</pre>
</li>
<li>N�rdliches Niedersachsen und Schleswig Holstein:
<pre>
2
</pre>
</li>
<li>Berlin und Umgebung:
<pre>
10;12;13;14;15;16
</pre>
</li>
<li>Bleibt die Variable leer, werden alle Gemeindeschl�ssel verwendet.
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
         """Die Regionen, f�r die in der Tabelle die Neumeldungen ausgez�hlt werden sollen, m�ssen unter 
"Hauptmen� -- Statistikabfrage -- Teilmenge -- Neu" als Teilmengendefinitionen eingef�hrt werden. Der Namen der
gew�nschten Definitionen werden durch <code>;</code> getrennt aufgef�hrt.
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
         """Inhalt wird als Meldung vom Administrator un�bersehbar auf jeder EBKuS-Seite �ber der Statuszeile ausgegeben.""",
         """Damit kann der Administrator
Meldungen an alle aktiven EBKuS-Nutzer ausgeben, z.B. um einen
Ausfall von EBKuS wegen Wartungsarbeiten anzuk�ndigen.
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
