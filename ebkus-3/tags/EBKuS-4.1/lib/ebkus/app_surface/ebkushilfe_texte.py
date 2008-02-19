# coding: latin-1
from ebkus.config import config

##*************************************************************************
## Templates mit den einzelnen Hilfetexten zu den einzelnen Dokuementen
##*************************************************************************

ht_start_seite_t = """
<table width="95%">
  <tr>
    <td colspan="2" class="legendtext" align="center">
      <img border="0" src="/ebkus/ebkus_icons/ebkus_logo_w.gif">
    </td>
  </tr>
  <tr>
    <td colspan="2" class="legendtext" align="center">&nbsp;</td>
  </tr>
  <tr>
    <td colspan="2" class="normaltext">
    <p align="justify">
    Sie befinden sich auf der Startseite des EBKuS-Hilfesystems.
    Es soll dazu dienen, Sie bei Ihrer t&auml;glichen Arbeit mit
    der EBKuS-Anwendung zu unterst&uuml;tzen.<br><br>
    Bei nicht beantworteten Fragen oder technischen Problemen,
    wenden Sie sich bitte an Ihren Systemadministrator.
    </p>
    </td>
  <tr><td>&nbsp;</td></tr>
  <tr>
    <td align="right" class="normaltext">
      <b>Name:</b>
    </td>
    <td align="left" class="normaltext">"""+ config.ADMIN_NAME + """
    </td>
  </tr>
  <tr>
    <td align="right" class="normaltext">
      <b>Telefon:</b>
    </td>
    <td align="left" class="normaltext">"""+ config.ADMIN_TEL + """
    </td>
  </tr>
  <tr>
    <td align="right" class="normaltext">
      <b>E-Mail:</b>
    </td>
    <td align="left" class="normaltext">"""+ config.ADMIN_EMAIL + """
    </td>
  </tr>
</table>
"""

no_content_t = """
Es wurde kein passender Hilfetext zum angeforderten Thema gefunden.
"""

##*************************************************************************
## Templates Bedienungsanleitung
##*************************************************************************

ht_hauptmenu_t = """

Das rechte Auswahlfenster zeigt dem Benutzer alle Klienten (Bearbeiter,
 Klientenvor- und -nachname, Geburtsdatum, Fallnummer) aus seinen
laufenden Beratungen. Die Auswahl eines Klientennamens mit der Maus
 und die Eingabebest&auml;tigung fordern die zugeh&ouml;rige Klientenkarte mit
allen Eintr&auml;gen f&uuml;r diesen Klienten an.
Soll gleichzeitig ein bestimmtes Formular f&uuml;r eine Eingabe zum ausgew&auml;hlten
 Klienten geladen werden, ist dieses im Men&uuml; links zu markieren (z.B.
 'Fachstatistik', 'Bundesjugendhilfestatistik'), bevor mit der Maus
 die Eingabe best&auml;tigt wird. Die Anwendung erwartet, dass immer genau ein
 Klient und ein Formular ausgew&auml;hlt ist. Eine Ausnahme bildet die Klientenkarte,
 bei der die Auswahl des Klienten f&uuml;r die Anzeige der Klientenkarte
 ausreichend ist, sowie die Suchfunktion.
Die Men&uuml;auswahl neben der Klientenauswahl enth&auml;lt die Formularseiten bzw.
Aktionen in folgenden Untermen&uuml;s:<br><br>
<b>Neu:</b><br>
Neuaufnahme<br>
Neue Gruppe<br>
Neue Fachstatistik<br>
Neue Jugendhilfestatistik<br><br>
<b>Suche:</b><br>
Klientenkarte<br>
Gruppenkarte<br><br>
<b>&Auml;ndern:</b><br>
Fachstatistik &auml;ndern<br>
Jugendhilfestatistik &auml;ndern<br><br>
<b>Ansicht:</b><br>
Klientenkarte<br>
Aktenvorblatt<br>
Akte (Dokumente)<br>
Gruppenmen&uuml;<br><br>

Das Feld <a href="ebkus_help_document?help_id=Statistische_Abfragen">
Statistische Abfragen</a> enth&auml;lt eine aufklappbare Auswahlliste.
 Zum Ausw&auml;hlen einer Abfrage muss diese in der ausgeklappten Liste mit
 der Maus markiert werden.
"""

ht_neue_akte_anlegen_t = """
Das Formular 'Neue Akte anlegen' dient zum Anlegen neuer Akten.<br><br>

Das Formular ist in folgende Bereiche unterteilt:
<br><br>
<b>Klientendaten:</b><br>
  In diesem Formularbereich werden die Personendaten des Klienten eingetragen.
<br><br>
<b>Hinweis:</b><br>
  Nach Eingabe des Geburtsdatums wird dieses auf G&uuml;ltigkeit &uuml;berpr&uuml;ft. Es
  ist in der Form TT.MM.JJJJ mindestens
  <a href="ebkus_help_document?help_id=monatsgenau">monatsgenau</a> einzugeben.
  Wird ein ung&uuml;ltiges Datum eingegeben, so wird der Eintrag automatisch aus
  dem Textfeld entfernt und eine Meldung an den Benutzer ausgegeben.
<br><br>
<b>Anschrift:</b><br>
  In diesem Formularbereich wird der Wohnsitz des Klienten eingetragen sowie
  der Wohnumstand aus dem Listenfeld 'Wohnt bei' ausgew&auml;hlt.
  F&uuml;r eine n&auml;here Erl&auml;uterung zur Eingabe der Adresse eines Klienten klicken
  Sie bitte auf <a href="ebkus_help_document?help_id=Strassenkatlog">Stra&szlig;enkatalog</a>.
<br><br>
<b>Notiz:</b><br>
  Es ist m&ouml;glich, eine Notiz zum Klienten in die Akte aufzunehmen. Diese
  wird auf der <a href="ebkus_help_document?help_id=Klientenkarte">Klientenkarte</a> angezeigt.
<br><br>
<b>Falldaten:</b><br>
  In diesem Formularbereich wird der Beginn des Falles angegeben.
  Die drei Textfelder stellen die Eingabem&ouml;glichkeit f&uuml;r Tag.Monat.Jahr dar.
  Die beiden Felder Monat und Jahr sind bereits mit dem aktuellen Monat und
  Jahr vorbelegt.<br><br>
  Wird das leere Feld Tag nicht ausgef&uuml;llt, so wird der aktuelle Tag
  automatisch beim Speichern der neuen Akte eingesetzt.
  Jede Akte ben&ouml;tigt eine eindeutige
  <a href="ebkus_help_document?help_id=Fallnummer">Fallnummer</a>. Mit dem Anlegen einer
  neuen Akte wird diese automatisch generiert.
<br><br>
<b>Leistung:</b><br>
  Beim Anlegen einer Akte wird die erste erbrachte Leistung am Klienten
  miterfasst. Daf&uuml;r ist das Datum des Beginns der Leistung notwendig.
  Die drei Textfelder stellen die Eingabem&ouml;glichkeit f&uuml;r Tag.Monat.Jahr dar.
  Die beiden Felder Monat und Jahr sind bereits mit dem aktuellen Monat und
  Jahr vorbelegt.<br><br>
  Die erbrachte Leistung muss aus dem Leistungs-Auswahlfeld gew&auml;hlt werden.
<br><br><br>
<b>Siehe auch:</b>
<br><a href="ebkus_help_document?help_id=Strassenkatlog">Stra&szlig;enkatalog</a>
<br><a href="ebkus_help_document?help_id=Fallnummer">Fallnummer</a>
"""

ht_akte_aktualisieren_t = """
Dieses Formular bietet Ihnen die M&ouml;glichkeit, die Stammdaten einer
Person zu bearbeiten und zu speichern. Die bisher gespeicherten Werte
werden im Formular angezeigt.
"""

ht_bezugsperson_eintragen_t = """
<b>Personen:</b><br>
  In diesem Formularbereich werden die Daten der Person eingetragen.
<br><br>
<b>Hinweis:</b><br>
  Nach Eingabe des Geburtsdatums wird dieses auf G&uuml;ltigkeit &uuml;berpr&uuml;ft. Es
  ist in der Form TT.MM.JJJJ mindestens
  <a href="ebkus_help_document?help_id=monatsgenau">monatsgenau</a> einzugeben.
  Wird ein ung&uuml;ltiges Datum eingegeben, so wird der Eintrag automatisch aus
  dem Textfeld entfernt und eine Meldung an den Benutzer ausgegeben.
<br><br>
<b>Anschrift:</b><br>
  In diesem Formularbereich wird der Wohnsitz der Person eingetragen sowie
  der Wohnumstand aus dem Listenfeld 'Wohnt bei' ausgew&auml;hlt.
  F&uuml;r eine n&auml;here Erl&auml;uterung zur Eingabe der Adresse eines Klienten klicken
  Sie bitte auf <a href="ebkus_help_document?help_id=Strassenkatlog">Stra&szlig;enkatalog</a>.
<br><br>
<b>Notiz:</b><br>
  Es ist m&ouml;glich eine Notiz zur Person mit in die Akte aufzunehmen. Diese
  wird auf der <a href="ebkus_help_document?help_id=Klientenkarte">Klientenkarte</a> angezeigt.
  Das Markieren der Checkbox 'Wichtig' bewirkt einen Vermerk 'Notiz wichtig!' hinter
  der Notizanzeige auf der Klientenkarte.
<br><br>
<b>Verwandtschaftsart:</b><br>
  Hier w&auml;hlen Sie das Verwandtschaftsverh&auml;ltnis aus, das zwischen der Person und dem
  Klienten besteht."""

ht_bezugsperson_aktualisieren_t = """
Dieses Formular bietet Ihnen die M&ouml;glichkeit, die Stammdaten einer
Bezugsperson zu bearbeiten und zu speichern. Die bisher gespeicherten Werte
werden im Formular angezeigt.
"""


ht_klientenkarte_t = """
<b>Allgemeines:</b><br>
Die Klientenkarte enth&auml;lt die Stammdaten des Klienten und der Bezugspersonen
aus der Beratung, die Anmeldeinformation, die Einrichtungskontakte, die
Beratungsleistungen, -Datumsangaben und Mitarbeiter, den zust&auml;ndigen
Bearbeiter, den Beratungsstand (laufend, zu den Akten (z. d. A.)) sowie das Vorliegen
der Statistikeintr&auml;ge, die Notizen und evtl. Zugeh&ouml;rigkeit zu einer Gruppe.
<br><br>
<b>&Auml;nderung:</b><br>
Nach jeder &Auml;nderung bzw. jedem Neueintrag wird die angezeigte
Klientenkarte mit den in der Datenbank eingegebenen Daten aktualisiert.
<br><br>
Die Buttons in der Klientenkarte (zum Bearbeiten bzw. Hinzuf&uuml;gen von
Eintr&auml;gen) stehen nur f&uuml;r laufende Beratungsf&auml;lle zur Verf&uuml;gung.
<br><br>
Nach dem z. d. A.-Eintrag (Beratungsabschluss) erscheint die Klientenkarte
im 'Lesemodus', mit inaktiven Buttons zum Bearbeiten oder Hinzuf&uuml;gen.
Die Wiederaufnahme oder das R&uuml;ckg&auml;ngigmachen des z. d. A.-Eintrages revidiert
die Anzeige f&uuml;r den aktuellen 'Beratungsfall' wieder auf eine mit
aktiven Buttons, w&auml;hrend die abgeschlossenen 'Beratungsf&auml;lle' dauerhaft
mit inaktiven Buttons dargestellt werden.
<br><br>
Die Klientenkarte fasst alle eingetragenen Informationen zum Klienten
zusammen und unterteilt diese in folgende Bereiche:
<br><br>
<b>Klientendaten:</b><br>
  In diesem Formularbereich werden die Klientendaten aufgef&uuml;hrt. Um zum
  <a href="ebkus_help_document?help_id=Akte_aktualisieren">
  Bearbeiten des Klienten</a> zu wechseln, muss auf die Schaltfl&auml;che
  'Bearbeiten' gedr&uuml;ckt werden.
<br><br>
<b>Bezugspersonen:</b><br>
  In diesem Formularbereich werden die Bezugspersonen eines Klienten
  aufgef&uuml;hrt.
  Neben jedem Listeneintrag befinden sich immer folgende zwei Schaltfl&auml;chen
  der dazugeh&ouml;rigen Funktionen:<br><br>
  <img border="0" src="/ebkus/ebkus_icons/edit_button.gif">
  <a href="ebkus_help_document?help_id=Bezugsperson_bearbeiten"> Bezugsperson bearbeiten</a><br><br>
  <img border="0" src="/ebkus/ebkus_icons/view_details.gif"> <b>Anzeigen der Stammdaten der Bezugsperson</b><br><br>
  Die Schaltfl&auml;che Hinzuf&uuml;gen &ouml;ffnet eine Maske, in der eine
  <a href="ebkus_help_document?help_id=Neue_Person_eintragen">neue Bezugsperson</a> angelegt werden kann.
<br><br>
<b>Leistungen:</b><br>
  In diesem Formularbereich werden die Leistungen, die ein Klient erhalten
  hat, aufgef&uuml;hrt.
  Neben jedem Listeneintrag befindet sich immer folgende Schaltfl&auml;chen mit
  der dazu genannten Funktion:<br><br>
  <img border="0" src="/ebkus/ebkus_icons/edit_button.gif">
  <a href="ebkus_help_document?help_id=Leistung_bearbeiten">Leistung bearbeiten</a><br><br>
  Die Schaltfl&auml;che 'Hinzuf&uuml;gen' &ouml;ffnet eine Maske, in der eine
  <a href="ebkus_help_document?help_id=Neue_Leistung_eintragen">neue Leistung</a>
  angelegt werden kann.
<br><br>
<b>Stand:</b><br>
  Gibt einen &Uuml;berblick &uuml;ber den Fallstatus und die Historie des Falls
<br><br>
<b>Hinweis:</b><br>
   Die Schaltfl&auml;che in diesem Formularbereich kann drei verschiedene
   Aufschriften und <a href="ebkus_help_document?help_id=Funktionen_zda">Funktionen</a> besitzen.
<br><br>
<b>Bearbeiter:</b><br>
  In diesem Formularbereich werden die Bearbeiter eines Falles und
  der Zeitraum seiner Zust&auml;ndigkeit aufgef&uuml;hrt.
  Die Zeitr&auml;ume k&ouml;nnen mit der Schaltfl&auml;che <img border="0" src="/ebkus/ebkus_icons/edit_button.gif">
  <a href="ebkus_help_document?help_id=Eintrag_zur_Zust&auml;ndigkeit_bearbeiten"> nachtr&auml;glich
  bearbeitet</a> werden. Mit der Schaltfl&auml;che hinzuf&uuml;gen &ouml;ffnet man ein
  Formular, mit dem man den bisher zust&auml;ndigen Mitarbeiter und dessen
  Zust&auml;ndigkeit austragen und einen
  <a href="ebkus_help_document?help_id=Neue_Zust&auml;ndigkeit_eintragen">neuen Bearbeiter</a>
  erfassen kann.
<br><br>
<b>Anmeldungskontakt:</b><br>
  In diesem Formularbereich werden die Anmeldekontakte eines
  Falles aufgef&uuml;hrt.<br>
  Neben jedem Listeneintrag befinden sich immer zwei Schaltfl&auml;chen mit
  den dazugeh&ouml;rigen Funktionen:<br><br>
  <img border="0" src="/ebkus/ebkus_icons/edit_button.gif">
  <a href="ebkus_help_document?help_id=Anmeldeinformation_&auml;ndern">Anmeldekontakt bearbeiten</a><br><br>
  <img border="0" src="/ebkus/ebkus_icons/view_details.gif"> <b>Anzeigen der Stammdaten des Anmeldekontakts</b><br><br>
  Die Schaltfl&auml;che 'Hinzuf&uuml;gen' &ouml;ffnet eine Maske, in der ein
  <a href="ebkus_help_document?help_id=Neue_Anmeldeinformation_eintragen">neuer Anmeldekontakt</a> angelegt werden kann.
<br><br>
<b>Einrichtungkonstakte:</b><br>
  In diesem Formularbereich werden die Einrichtungskontakte des Falles
  aufgef&uuml;hrt.<br>
  Neben jedem Listeneintrag befindet sich immer folgende Schaltfl&auml;che mit
  der dazu genannten Funktion:<br><br>
  <img border="0" src="/ebkus/ebkus_icons/edit_button.gif">
  <a href="ebkus_help_document?help_id=Einrichtungskontakt_&auml;ndern">Einrichtungskontakt bearbeiten</a><br><br>
  Die Schaltfl&auml;che 'Hinzuf&uuml;gen' &ouml;ffnet eine Maske, in der ein
  <a href="ebkus_help_document?help_id=Neuen_Einrichtungskontakt_eintragen">neuer Einrichtungskontakt</a>
  angelegt werden kann.
<br><br>
<b>Fachstatistiken:</b><br>
  In diesem Formularbereich werden die Fachstatistiken des Falles
  aufgef&uuml;hrt.<br>
  Neben jedem Listeneintrag befindet sich immer folgende Schaltfl&auml;che mit
  der dazu genannten Funktion:<br><br>
  <img border="0" src="/ebkus/ebkus_icons/edit_stat_button.gif">
  <a href="ebkus_help_document?help_id=Fachstatistik_&auml;ndern">Fachstatistik bearbeiten</a><br><br>
  Die Schaltfl&auml;che 'Hinzuf&uuml;gen' &ouml;ffnet eine Maske, in der eine
  <a href="ebkus_help_document?help_id=Neue_Fachstatistik_erstellen">neue Fachstatistik</a>
  angelegt werden kann.
<br><br>
<b>Jugendhilfestatistiken:</b><br>
  In diesem Formularbereich werden die Jugendhilfestatistiken des Falles
  aufgef&uuml;hrt.<br>
  Neben jedem Listeneintrag befindet sich immer folgende Schaltfl&auml;che mit
  der dazu genannten Funktion:<br><br>
  <img border="0" src="/ebkus/ebkus_icons/edit_stat_button.gif">
  <a href="ebkus_help_document?help_id=Bundesstatistik_&auml;ndern">Jugendhilfestatistik bearbeiten</a><br><br>
  Die Schaltfl&auml;che 'Hinzuf&uuml;gen' &ouml;ffnet eine Maske, in der eine
  <a href="ebkus_help_document?help_id=Neue_Bundesstatistik_erstellen">neue Jugendhilfestatistik</a>
  angelegt werden kann.
<br><br>
<b>Notizen:</b><br>(nur bei Vorhandensein einer Notiz sichtbar)<br>
  In diesem Formularbereich werden alle Notizen des Falles
  aufgef&uuml;hrt. Dazu geh&ouml;ren die Notizen zu den Bezugspersonen, Gruppennotizen usw..
<br><br>
<b>Gruppenkarten des Falls:</b><br>
 (Nur bei Mitgliedschaft in einer Gruppe sichtbar)<br><br>
  In diesem Formularbereich werden die Gruppen aufgef&uuml;hrt, in denen der Klient Mitglied
  ist oder war.<br>
  Neben jedem Listeneintrag befindet sich immer folgende Schaltfl&auml;che mit
  der dazu genannten Funktion:<br><br>
  <img border="0" src="/ebkus/ebkus_icons/edit_grp_button.gif"> <b>Gruppe bearbeiten</b>
<br>
<br>
<b>Gruppenkarten der Bezugspersonen:</b><br>
 (Nur bei Mitgliedschaft in einer Gruppe sichtbar)<br><br>
  In diesem Formularbereich werden die Gruppen aufgef&uuml;hrt, in denen eine Bezugsperson
  des Falles Mitglied ist oder war.
  Neben jedem Listeneintrag befindet sich immer folgende Schaltfl&auml;che mit
  der dazu genannten Funktion:<br><br>
  <img border="0" src="/ebkus/ebkus_icons/edit_grp_button.gif"> <b>Gruppe bearbeiten</b>
"""

ht_neue_fachstat_eintragen_t = """
<p align="justify">
Dieses Formular dient dazu, eine neue Fachstatistik f&uuml;r einen Klienten zu erstellen.<br><br>
Es werden, soweit m&ouml;glich, die Felder der Fachstatistik mit Daten aus der Klientenakte vorbelegt.<br><br>
<b>Hinweis:</b><br>
Es muss und darf f&uuml;r jede Fallnummer genau eine Fachstatistik existieren. Ist f&uuml;r einen Fall keine Statistik vorhanden, so ist es nicht m&ouml;glich, ihn zu den Akten zu legen.
</p>
"""

ht_fachstat_bearbeiten_t = """
<p align="justify">
Dieses Formular dient dazu, die zu einem Klienten angelegte Fachstatistik zu bearbeiten.
</p>
"""

ht_neue_bundesstat_eintragen_t = """
<p align="justify">
Dieses Formular dient dazu, eine neue Bundesstatistik f&uuml;r einen Klienten zu erstellen.<br><br>
Es werden, soweit m&ouml;glich, die Felder der Bundesstatistik mit Daten aus der Klientenakte vorbelegt.<br><br>
<b>Hinweis:</b><br>
Es muss und darf f&uuml;r jede Fallnummer genau eine Bundesstatistik existieren. Ist f&uuml;r einen Fall keine Statistik vorhanden, so ist es nicht m&ouml;glich, ihn zu den Akten zu legen.
</p>
"""

ht_bundesstat_bearbeiten_t = """
<p align="justify">
Dieses Formular dient dazu, die zu einem Klienten angelegte Bundesstatistik zu bearbeiten.
</p>
"""

ht_neuen_anmeldekontakt_eintragen_t = """
<p align="justify">
Dieses Formular dient dazu, einen Anmeldekontakt zu einem Klienten hinzuzuf&uuml;gen.<br><br>
<b>Hinweis:</b><br>
Es existiert immer genau ein Anmeldekontakt zu einer Fallnummer. Dieses Formular ist nach einem abgeschlossenen Hinzuf&uuml;gen nicht mehr aufrufbar. Wird der Fall neu aufgenommen, ist es wieder m&ouml;glich, einen neuen Kontakt hinzuzuf&uuml;gen, da er durch die Wiederaufnahme eine neue Fallnummer erh&auml;lt.
</p>
"""

ht_anmeldekontakt_bearbeiten_t = """
<p align="justify">
Dieses Formular dient dazu, den zu einem Klienten geh&ouml;rigen Anmeldekontakt zu bearbeiten.<br><br>
<b>Hinweis:</b><br><br>
Das Bearbeiten eines Anmeldekontaktes von einem bereits abgeschlossenem Fall ist nicht m&ouml;glich. Bitte verwenden Sie zur Ansicht die Funktion Detailansicht des Anmeldekontaktes.
</p>
"""

ht_neuen_einrichtungskontakt_eintragen_t = """
<p align="justify">
Dieses Formular dient dazu, einen neuen Einrichtungskontakt zu einem Klienten hinzuzuf&uuml;gen.
</p>
"""

ht_einrichtungskontakt_bearbeiten_t = """
<p align="justify">
Dieses Formular dient dazu, die zu einem Klienten geh&ouml;rigen Einrichtungskontakte zu bearbeiten.<br><br>
</p>
"""




ht_neue_leistung_eintragen_t = """
<p align="justify">
Dieses Formular dient dazu, die f&uuml;r einen Klienten erbrachten Leistungen zu erfassen.<br><br>
<b>Vorgehensweise:</b><br><br>
1. W&auml;hlen Sie die zu speichernde Leistung aus der Auswahlliste mit der Bezeichnung 'Leistung'.<br><br>
2. Legen Sie den Leistungszeitraum in den daf&uuml;r vorgesehenen Textfeldern fest.<br><br>
3. Bet&auml;tigen Sie die Schaltfl&auml;che 'Speichern'.
"""

ht_leistung_bearbeiten_t = """
<p align="justify">
Dieses Formular dient dazu, die f&uuml;r einen Klienten erfassten Leistungen zu bearbeiten.<br><br>
Sie k&ouml;nnen sowohl die Leistung ab&auml;ndern, als auch den Zeitraum der Leistung bearbeiten und speichern.
</p>"""


ht_zustaendigkeit_eintragen_t = """
<p align="justify">
In diesem Formular k&ouml;nnen Sie die Zust&auml;ndigkeit eines Mitarbeiters f&uuml;r einen Klienten austragen und einem anderen Mitarbeiter &uuml;bertragen.<br><br>
<b>Vorgehensweise:</b><br>
1. W&auml;hlen Sie einen Mitarbeiter aus der Auswahlliste 'Bearbeiter' aus, der die Zust&auml;ndigkeit &uuml;bernehmen soll.<br><br>
2. Geben Sie das Datum des Wechsels der Zust&auml;ndigkeit in Feld 'Beginndatum' an.<br><br>
3. Bet&auml;tigen Sie die Schaltfl&auml;che 'Speichern' um den Vorgang abzuschliessen.<br>
<br>
Mit der Schaltfl&auml;che 'Abbrechen' gelangen Sie wieder zum vorhergehenden Formular. Eventuell get&auml;tigte &Auml;nderungen werden verworfen und nicht in der Akte gespeichert.
</p>"""

ht_zustaendigkeit_bearbeiten_t = """
<p align="justify">
In diesem Formular k&ouml;nnen Sie die Zust&auml;ndigkeit eines Mitarbeiters f&uuml;r einen Klienten korrigieren.<br><br>
<b>Hinweis:</b><br>
Diese Funktion ist nur f&uuml;r unumg&auml;ngliche Korrekturen gedacht. Verwenden Sie soweit m&ouml;glich nur
das Wechseln von Zust&auml;ndigkeiten.
</p>
"""

ht_gruppenkartei_t = """
<p align="justify">
        Das rechte Auswahlfenster zeigt dem Benutzer die Gruppen
      (Benutzername, Gruppenname) aus seinen laufenden Beratungen. Die Auswahl
      eines Gruppennamens mit der Maus und die Eingabebest&auml;tigung fordern
      die zugeh&ouml;rige Gruppenkarte mit allen Eintr&auml;gen f&uuml;r diese
      Gruppe an.<br>
      Soll gleichzeitig ein bestimmtes Formular f&uuml;r eine Eingabe zur ausgew&auml;hlten
      Gruppe geladen werden, ist dieses im Men&uuml; links anzukreuzen (z.B. 'Teilnehmer',
      'Gruppenkarte'), bevor mit der Maus die Eingabe best&auml;tigt
      wird. Die Anwendung erwartet, dass immer eine Gruppe und ein Formular angegeben
      sind. Eine Ausnahme bildet die Gruppenkarte, bei der die Auswahl der Gruppe f&uuml;r die
      Anzeige der Gruppenkarte ausreichend ist.
      <p><b>Das Gruppenmen&uuml; enth&auml;lt folgende Hauptpunkte:</b><br>
      </p>
      <p><b>Neu:</b><br>
        Gruppe<br>
        <br>
        <b>Ansicht:</b><br>
        Teilnehmer; Gruppenkarte; Hauptmen&uuml;<br>
      </p>
      <b>Suche:</b><br>
      Klientenkarte; Gruppenkarte<br>"""

ht_neue_gruppen_erstellen_t = """
<p align="justify">
Das Formular 'Neue Gruppe erstellen' dient zum Anlegen einer neuen Gruppe.<br>
<br>
Das Formular ist in folgende Bereiche unterteilt:<br><br>

<b>Neue Gruppe:</b><br>
  In diesem Formularbereich werden der Gruppenname und das Gruppenthema eingetragen.<br><br>

<b>Gruppendetails:</b><br>
  In diesem Formularbereich werden die Daten zur Gruppe eingetragen.
  Dies sind das Beginndatum, Art der Teilnehmer, der bearbeitende Mitarbeiter, das
  Endedatum, Gruppenart, Teilnehmeranzahl und die Stundenanzahl.
</p>"""

ht_gruppe_bearbeiten_t = """
<p align="justify">
Das Formular 'Gruppe bearbeiten' dient zum Bearbeiten der Daten einer Gruppe.<br>
<br>
Die Daten, die beim Anlegen der Akte eingegeben und gespeichert wurden, k&ouml;nnen in diesem Formular
korrigiert oder angepasst werden.
</p>
 """
ht_grp_teilnehm_neu_t = """
<p align="justify">
Dieses Formular dient dazu, Klienten und/oder deren Bezugsperson einer vorhandenen Gruppe zuzuordnen.<br>
<br>
In den beiden gro&szlig;en Auswahlfeldern werden die Klienten auf der linken und die Familienangeh&ouml;rigen auf der rechten Seite aufgelistet. Aus beiden Feldern k&ouml;nnen beliebig viele Personen ausgew&auml;hlt werden.<br><br>
Mit den Feldern 'Beginndatum' und 'Endedatum' kann der Zeitraum der Gruppenzugeh&ouml;rigkeit bestimmt werden.<br><br>
<b>Hinweis:</b><br>
Mit gleichzeitigem Dr&uuml;cken der Taste 'Strg' und der linken Maustaste k&ouml;nnen Sie die Eintr&auml;ge einzeln markieren.<br><br>
Durch Dr&uuml;cken der Taste 'Speichern', werden die Personen der aktuellen Gruppe zugeordnet.
</p>
"""
ht_grp_teilnehm_bearb_t = """
<p align="justify"
In diesem Formular ist das Anpassen des Zeitraums der Gruppenzugeh&oumlrigkeit m&ouml;glich.<br><br>
Die &Auml;nderungen werden durch Dr&uuml;cken  der Taste Speichern aktualisiert.
</p>
"""
ht_grp_teilnehm_del_t = """
<p align="justify">
In diesem Formular k&ouml;nnen Sie Personen aus der Gruppe entfernen.<br><br>
Zum L&ouml;schen markieren Sie die entsprechende/n Person/en und dr&uuml;cken Sie die Schaltfl&auml;che L&ouml;schen.<br><br>
<b>Hinweis:</b><br>
Mit gleichzeitigem Dr&uuml;cken der Taste 'Strg' und der linken Maustaste k&ouml;nnen Sie die Eintr&auml;ge einzeln markieren.<br>
<b>Es wird nur die Gruppenzugeh&ouml;rigkeit ausgetragen. Die Klienten und Personen werden nicht gel&ouml;scht.</b>
</p>
"""
ht_dokumentenindex_t = """
<p align="justify">
Die Dokumentenkarte zeigt den Dokumentenindex einer Akte oder einer Gruppe sowie den Index der Beraternotizen an.<br><br>
Sie enth&auml;lt in der Kopfzeile das Hauptmen&uuml; f&uuml;r die dokumentenbezogenen Funktionen (Import, Neuer Text, &Auml;ndern, L&ouml;schen) wie f&uuml;r die Print- und Viewausgaben der Dokumente.<br><br>
<b>&Auml;nderung:</b><br>
Nach jeder &Auml;nderung bzw. jedem Neueintrag oder Import einer Datei in die Akte oder Gruppe wird die angezeigte Dokumentenkarte mit den in der Datenbank eingegebenen Daten aktualisiert.<br><br>
Die Buttons in der Dokumentenkarte stehen f&uuml;r laufende Beratungsf&auml;lle dem zust&auml;ndigen Berater zur Verf&uuml;gung.<br><br> Nach dem z. d. A-Eintrag (Beratungsabschluss) erscheint die Dokumentenkarte im 'Lesemodus', mit inaktiven Button. Die Wiederaufnahme oder das R&uuml;ckg&auml;ngigmachen des z. d. A-Eintrages schalten die Anzeige f&uuml;r die Dokumentenliste wieder auf eine Anzeige mit aktiven Schaltfl&auml;chen.<br>
Im Formularbereich Printausgabe haben Sie die Möglichkeit die Aktendokumente einer Akte in einer zusammengefassten Ausgabe einzusehen und auch auszudrucken. Zur Auswahl des Anzeigeformates w&auml;hlen Sie bitte eine der beiden Schaltfl&auml;chen.<br><br>
<b>Hinweis:</b><br>
F&uuml;r die Anzeige im Format eines Adobe Acrobat-Dokumentes muss der Adobe Acrobat Reader installiert sein.<br>
Ist Adobe Acrobat auf Ihrem PC nicht installiert, so installieren Sie diesen bitte von der EBKuS-Distributions CD. Sie erhalten die neueste Version auch aus dem Internet unter : http://www.adobe.com
<br>
</p>
"""
ht_dateiimport_t = """
<p align="justify">
Dieses Formular dient zum Hochladen von Dateien auf den Server.<br><br>
Die Dateien werden einer Akte oder Gruppe zugeordnet.<br><br>
<b>M&ouml;gliche Dateitypen:</b><br><br>
<table width="95%" align="center" class="normaltext">
<tr>
<td align="left">*.doc - Microsoft Word</td>
</tr>
<tr>
<td align="left">*.dot - Microsoft Word</td>
</tr>
<tr>
<td align="left">*.wrd - Microsoft Word</td>
</tr>
<tr>
<td align="left">*.rtf  - Richtext Format</td>
</tr>
<tr>
<td align="left">*.xls  - Microsoft Excel</td>
</tr>
<tr>
<td align="left">*.sdw  - Star Office</td>
</tr>
<tr>
<td align="left">*.sdc  - Star Division</td>
</tr>
<tr>
<td align="left">*.zip  - Zip-Dateien</td>
</tr>
<tr>
<td align="left">*.gtar - gtar-Dateien</td>
</tr>
<tr>
<td align="left">*.tgz - tgz-Dateien</td>
</tr>
<tr>
<td align="left">*.gz - gz-Dateien</td>
</tr>
<tr>
<td align="left">*.tar - tar-Dateien</td>
</tr>
<tr>
<td align="left">*.rtx - rtx-Dateien</td>
</tr>
<tr>
<td align="left">*.gif - gif-Dateien</td>
</tr>
<tr>
<td align="left">*.jpg - jpeg-Dateien</td>
</tr>
<tr>
<td align="left">*.jpeg - jpeg-Dateien</td>
</tr>
<tr>
<td align="left">*.jpe - jpeg-Dateien</td>
</tr>
<tr>
<td align="left">*.tiff - tiff-Dateien</td>
</tr>
<tr>
<td align="left">*.tif - tiff-Dateien</td>
</tr>
<tr>
<td align="left">*.png - png-Dateien</td>
</tr>
<tr>
<td align="left">*.bmp - bmp-Dateien</td>
</tr>
</table><br><br>
<b>Vorgehensweise:</b><br><br>
1. Dr&uuml;cken Sie die Schaltfl&auml;che 'Durchsuchen' und w&auml;hlen Sie im folgenden Dateiauswahlfenster die Datei, die Sie hochladen m&ouml;chten.<br><br>
2. Geben Sie im Feld 'Betreff' einen Betrefftext ein, der zu der Datei gespeichert wird.<br><br>
3. Im Feld 'Dateityp' w&auml;hlen Sie bitte den Typ Ihres Dokumentes aus. Dieses dient sp&auml;ter zum besseren Identifizieren der einzelnen Dokumente. <br><br>
4. Dr&uuml;cken Sie die Schaltfl&auml;che 'Hochladen'
</p>
"""
ht_texteintrag_neu_t = """
<p align="justify">
Mit diesem Formular k&ouml;nnen Sie direkt in EBKuS verfasste Texte zur Akte oder Gruppe hinzuf&uuml;gen.<br><br>
<b>Vorgehensweise:</b><br><br>
1. Geben Sie einen Betrefftext im Feld 'Betreff' ein. Dieser wird mit dem Text gespeichert.<br><br>
2. Geben Sie Ihren Text in das gro&szlig;e Feld mit der Bezeichnung 'Textinhalt' ein.<br><br>
3. W&auml;hlen Sie den Typ Ihres Textes im Feld 'Festlegung des Texttyps'.<br><br>
4. Bet&auml;tigen Sie die Schaltfl&auml;che 'Speichern'.<br>
</p>
"""
ht_texteintrag_bearb_t = """
<p align="justify">
Mit diesem Formular k&ouml;nnen Sie die in einer Akte oder Gruppe enthaltenen Texte bearbeiten, ab&auml;ndern und speichern.
</p>"""

ht_texteintrag_ausw_t = """
<p align="justify">
Dieses Formular dient dazu, einen von den in einer Akte oder Gruppe enthaltenen Texte auszuw&auml;hlen, um diesen in einem <a href="ebkus_help_document?help_id=Texteintrag_der_Gruppe_&auml;ndern">Bearbeitungsformular</a> zu bearbeiten.
</p> """

ht_texteintrag_loesch_t = """
<p align="justify">
Dieses Formular dient dazu, eine beliebige Anzahl der in einer Akte oder Gruppe enthaltenen Texte auszuw&auml;hlen, um diese aus der Akte oder Gruppe zu entfernen.<br><br>
<b>Hinweis:</b><br>
Achtung! Das L&ouml;schen von Texten ist nicht wieder r&uuml;ckg&auml;ngig zu machen!
</p>
"""

ht_word_export_t = """
Diese Exportfunktionalit&auml;t setzt das Betriebssystem Windows ab Version 9.x / Nt mit installiertem
Internet Explorer ab Version 5.0 und Microsoft Word ab Version 97 voraus.
Eine Wordvorlage muss erstellt werden. In dieser Wordvorlage m&uuml;ssen Textboxen mit folgender Struktur (Inhalt) erstellt werden. Siehe dazu Wordexport Beispielvorlage /ebkus/klkarteexp2.doc Außerdem m&uuml;ssen die Internet Explorer Sicherheitseinstellungen f&uuml;r das lokale Netzwerk auf niedrig gestellt werden, damit ein Wordobjekt erstellt werden kann, welches die Ersetzung der Platzhalter in der Vorlage mit g&uuml;ltigen Werten vornimmt.<br> Bei 1 zu n Beziehungen muss eine laufende Nummer mit eingebunden werden. z.B. %bzp(lfdnr)s_vn -> %bzp1s_vn = Vorname <br>
<br>
<b>Klientenstammdaten (1 zu 1 Beziehung):</b><br>
%kl_vn = Vorname des Klienten<br>
%kl_na = Nachname des Klienten<br>
%kl_gb = Geburtstag des Klienten<br>
%kl_str = Stra&szlig;e des Klienten<br>
%kl_plz = Postleitzahl des Klienten<br>
%kl_ort = Wohnort des Klienten<br>
%kl_tl1 = 1. Telefonnummer des Klienten<br>
%kl_tl2 = 2. Telefonnummer des Klienten<br>
%kl_ber = Ausbildung des Klienten<br>
%kl_bei = Klient wohnt bei ...<br>
<br>
<br>
<b>Bezugsperson-Nr. (lfdnr) (1 zu n Beziehung):</b><br>
%bzp(lfdnr)s_vn = Vorname der Bezugsperson (lfdnr) des Klienten<br>
%bzp(lfdnr)s_na = Nachname der Bezugsperson (lfdnr) des Klienten<br>
%bzp(lfdnr)s_gb = Geburtstag der Bezugsperson (lfdnr) des Klienten<br>
%bzp(lfdnr)s_str = Stra&szlig;e der Bezugsperson (lfdnr) des Klienten<br>
%bzp(lfdnr)s_plz = Postleitzahl der Bezugsperson (lfdnr) des Klienten<br>
%bzp(lfdnr)s_ort = Wohnort der Bezugsperson (lfdnr) des Klienten<br>
%bzp(lfdnr)s_tl1 = 1. Telefonnummer der Bezugsperson (lfdnr) des Klienten<br>
%bzp(lfdnr)s_tl2 = 2. Telefonnummer der Bezugsperson (lfdnr) des Klienten<br>
%bzp(lfdnr)s_ber = Ausbildung der Bezugsperson (lfdnr) des Klienten<br>
%bzp(lfdnr)s_bei = Bezugsperson (lfdnr) des Klienten wohnt bei ...<br>
<br>
<br>
<b>Leistungen-Nr. (lfdnr) (1 zu n Beziehung):</b><br>
%lst(lfdnr)s_bea = Bearbeiter der (lfdnr). Leistung<br>
%lst(lfdnr)s_lst = Art der (lfdnr). Leistung<br>
%lst(lfdnr)s_beg = Beginn der (lfdnr). Leistung<br>
%lst(lfdnr)s_end = Ende der (lfdnr). Leistung<br>
<br>
<br>
<b>Stand-Nr. (lfdnr) (1 zu n Beziehung):</b><br>
%std(lfdnr)s_fnr = Fallnummer des Stands (lfdnr)<br>
%std(lfdnr)s_beg = Beginndatum<br>
%std(lfdnr)s_end = Endedatum<br>
<br>
<br>
<b>Bearbeiter-Nr. (lfdnr) (1 zu n Beziehung):</b><br>
%brb(lfdnr)s_bea = Bearbeiterkennung von Nr. (lfdnr)<br>
%brb(lfdnr)s_beg = Bearbeitungsbeginn von Nr. (lfdnr)<br>
%brb(lfdnr)s_end = Bearbeitungsende von Nr. (lfdnr)<br>
<br>
<br>
<b>Anmeldungskontakte-Nr. (lfdnr) (1 zu n Beziehung):</b><br>
%amd(lfdnr)s_von = Angemeldet von<br>
%amd(lfdnr)s_am = Datum der Anmeldung<br>
%amd(lfdnr)s_tel = Telefon des Bearbeiters<br>
%amd(lfdnr)s_zgs = Zugangsart<br>
%amd(lfdnr)s_epf = Empfehlung von<br>
%amd(lfdnr)s_grd = Grund der Anmeldung<br>
%amd(lfdnr)s_ntz = Notiz<br>
<br>
<br>
<b>Einrichtungskontakte-Nr. (lfdnr) (1 zu n Beziehung):</b><br>
%einr(lfdnr)s_art = Art des Einrichtungskontakt<br>
%einr(lfdnr)s_na = Name<br>
%einr(lfdnr)s_tl1 = 1. Telefonnummer<br>
%einr(lfdnr)s_tl2 = 2. Telefonnummer<br>
%einr(lfdnr)s_ntz = Notiz<br>
%einr(lfdnr)s_wtg = Wichtig?<br>
<br>
<br>
<b>Fachstatistiken-Nr. (lfdnr) (1 zu n Beziehung):</b><br>
%fst(lfdnr)s_jhr = Jahr der (lfdnr). Fachstatistik<br>
<br>
<br>
<b>Jugenhilfestatistiken-Nr. (lfdnr) (1 zu n Beziehung):</b><br>
%jgh(lfdnr)s_jhr = Jahr der (lfdnr). Bundesstatistik/Jugendhilfestatistik<br>
<br>
<br>
<b>Gruppenkarten des Falls Nr. (lfdnr) (1 zu n Beziehung):</b><br>
%gkf(lfdnr)s_nr = Nummer der (lfdnr). Gruppe<br>
%gkf(lfdnr)s_na = Name der (lfdnr). Gruppe<br>
<br>
<br>
<b>Gruppenkarten der Bezugspersonen Nr. (lfdnr) (1 zu n Beziehung):</b><br>
%gkb(lfdnr)s_nr = Nummer der (lfdnr). Gruppe<br>
%gkb(lfdnr)s_na = Name der (lfdnr). Gruppe<br>
<br>
<br>
<b>Notizen der Klientenkarte Nr. (lfdnr) (1 zu n Beziehung):</b><br>
<br>
<b>Notiz Klient:</b><br>
%ntz0 = Notiz bei Anlegen des Klienten<br>
<br>
<b>Notiz Bezugsperson, Einrichtungskontakte und Anmeldungskontakte:</b><br>
%ntz(lfdnr)s = Notiz (lfdnr). Nach Erstellungsreihenfolge<br>
<br>
Bei Fehler bitte wir wie folgt vorzugehen:<br>
Pr&uuml;fen ob Sicherheit f&uuml;r Lokales Intranet auf niedrig steht.<br>
Pr&uuml;fen ob Javascript installiert ist. <br>
<br>
Bei Fehler "Cannot create Automatation Object":<br>
<p align="justify"> Dieser Fehler tritt bei wenigen Systemen auf, die folgende
  Software installiert haben.<br>
  <br>
  <b>MS Office, Norton Antivirus, Visual Basic.</b><br>
  <br>
  Gehen Sie wie folgt vor:<br>
  <b>1. M&ouml;glichkeit:</b><br>
  a. Start -> Ausf&uuml;hren<br>
  b. Folgendes eingeben: regsvr32 /U "C:\Programme\Norton AntiVirus\OfficeAV.dll"<br>
  bb. Pfad gegeben falls anpassen<br>
  c. Dialogfeld m&uuml;sste &Auml;nderung best&auml;tigen.<br>
  <br>
  <b>2. M&ouml;glichkeit:</b><br>
  a. Deinstallieren Sie Office<br>
  b. Deinstallieren Sie Norton Antivirus<br>
  c. Visual Basic Runtime Dateien updaten (/ebkus/stuff/vbruntime/vbrun60sp4.exe)<br>
  d. Office neu installieren (Ab hier m&uuml;sste es gehen)<br>
  e. Norton Antivirus installieren (Ab hier wieder nicht)<br>
  f. 1. M&ouml;glichkeit ausf&uuml;hren.<br>
  g. Ende.<br>
  <br>
  Entnommen aus:<br>
  http://www.notes.net/<br>
  46dom.nsf/<br>
  ShowMyTopicsAllFlatweb/<br>
  4b92eb9b89ba4d0985256b1700538bb3?OpenDocument<br>
"""

ht_pass_change_t = """
<p align="justify">
Mit diesem Formular k&ouml;nnen Sie Ihr Benutzerpasswort &auml;ndern.<br><br>
<b>Vorgehensweise:</b><br><br>
1. Geben Sie Ihr vorheriges Passwort in das erste Feld ein.<br><br>

<b>Hinweis:</b>
Wenn Sie Ihr Passwort zum ersten Mal &auml;ndern, dann ist Ihr Passwort identisch mit Ihrem Benutzernamen.<br><br>

2. Geben Sie Ihr neues Passwort in das entsprechend bezeichnete Feld ein.<br><br>
3. Wiederholen Sie die Eingabe im darunter liegenden Feld, um Ihr neues Passwort zu verifizieren.<br><br>
4. Bet&auml;tigen Sie die Schaltfl&auml;che <b>Speichern</b>.<br>

Die Schaltfl&auml;che Abbrechen schliesst das Formular, ohne dass Ihr Passwort ge&auml;ndert wird.
</p>
 """


##*************************************************************************
## Templates Statistische Abfragen
##*************************************************************************


ht_statistische_abfragen_t = """
W&auml;hlen Sie bitte f&uuml;r n&auml;here Erl&auml;uterungen einen der unten stehenden
Eintr&auml;ge<br><br>
Liste aller m&ouml;glicher statistischer Abfragen:

<b>Beratungen:<b><br><br>
<a href="ebkus_help_document?help_id=Alle_Beratungen">- alle</a><br>
<a href="ebkus_help_document?help_id=Laufende_Beratungen">- laufende</a><br>
<a href="ebkus_help_document?help_id=Abgeschlossene_Beratungen">- abgeschlossene</a><br>
<a href="ebkus_help_document?help_id=Suche_alle_Beratungen_ab_Fallnummer">- ab Fallnummer?</a><br>
<br><br>
<b>Statistiken:<b><br><br>
<a href="ebkus_help_document?help_id=Bundesstatistikabfrage">- Bundesstatistik<br></a>
<a href="ebkus_help_document?help_id=Fachstatistikabfrage">- Fachstatistik<br></a>
<a href="ebkus_help_document?help_id=Statistikabfrage:_Kategoriewahl">- Itemauswahl<br></a>
<a href="ebkus_help_document?help_id=Statistikabfrage:_Kategorienwahl">- Kategorieauswahl<br></a>
<a href="ebkus_help_document?help_id=Auswahl_Konsultationsanzahl_und_Zeitraum_f&uuml;r_alle_Personen">- Konsultationszahl<br></a>
<a href="ebkus_help_document?help_id=Anzahl_abgeschl._F&auml;lle_-_gleiche_Konsultationssumme">- Konsultationssumme<br></a>
<a href="ebkus_help_document?help_id=Auswahl_des_gew&uuml;nschten_Zeitraumes_und_die_L&auml;nge_der_Beratungszeit_in_Monaten">- Beratungsdauer<br></a>
<a href="ebkus_help_document?help_id=Auswahl_des_gew&uuml;nschten_Zeitraumes_und_Auswahl_einer_Leistung">- Beratungsdauer-Leistung<br></a>
<!--- <a href="ebkus_help_document?help_id=Anzahl_der_abgeschl._F&auml;lle_-_Unterscheidung_nach_Haupt-_bzw._Geschwisterfall">- abgeschl.Haupt-/Geschwisterf&auml;lle<br></a>
 //-->
<a href="ebkus_help_document?help_id=Anzahl_abgeschl._F&auml;lle_-_Mutter_und_Vater_haben_das_gleiche_Merkmal_x">- Eltern-Merkmal x gleich<br></a>
<a href="ebkus_help_document?help_id=Anzahl_abgeschl._F&auml;lle_-_Mutter_oder_Vater_Merkmal_x_gleich">- Elternteil-Merkmal x gleich<br></a>
<a href="ebkus_help_document?help_id=Auswahl_des_Zeitraumes_f&uuml;r_die_Gruppenuebersicht">- Gruppen&uuml;berblick<br></a>
<a href="ebkus_help_document?help_id=Neumelde-_und_Abschlusszahlen">- Neumeldungen u. Abschl&uuml;sse<br></a>
<a href="ebkus_help_document?help_id=Klientenzahl_pro_Mitarbeiter">- Klienten pro Mitarbeiter<br></a>
"""

ht_alle_beratungen_t = """
Diese Abfrage l&ouml;st das Anzeigen aller vorhandenen Beratungen f&uuml;r den
 aktuellen Mitarbeiter aus. Eine wie oben dargestellte Liste wird ausgegeben.

 """

ht_laufende_beratungen_t = """
Diese Abfrage l&ouml;st das Anzeigen aller laufenden Beratungen f&uuml;r den
 aktuellen Mitarbeiter aus. Eine wie oben dargestellte Liste wird ausgegeben.

 """

ht_abgeschlossene_beratungen_t = """
Diese Abfrage l&ouml;st das Anzeigen aller abgeschlossenen Beratungen f&uuml;r den
 aktuellen Mitarbeiter aus. Eine wie oben dargestellte Liste wird ausgegeben.

 """
ht_beratungen_abfallnummer_t = """
Durch die Auswahl dieser Abfrage wird ein Formular wie oben dargestellt angezeigt.
In diesem Formular k&ouml;nnen die Suchkriterien hinsichtlich der Fallnummer f&uuml;r das
Anzeigen der Beratungen eingegeben werden.<br><br>

 """
ht_beratungen_abfallnummer2_t = """
In diesem Formular wird Ihnen das Ergebnis Ihrer Abfrage ausgegeben.<br><br>
"""

ht_bundesstatistikabfrage_t = """
Durch die Auswahl dieser Abfrage wird ein Formular wie oben dargestellt angezeigt.
In diesem Formular k&ouml;nnen die Suchkriterien f&uuml;r das
Anzeigen der Bundesstatistik eingegeben werden.<br><br>
"""

ht_bundesstatistikergebnis_t = """
Auf der obigen grafischen Darstellung sehen Sie das Ergebnis einer Bundesstatistikabfrage.<br><br>
"""


ht_fachstatistikabfrage_t = """
Durch die Auswahl dieser Abfrage wird ein Formular wie oben dargestellt angezeigt.
In diesem Formular k&ouml;nnen die Suchkriterien f&uuml;r das
Anzeigen der Fachstatistik eingegeben werden.<br><br>
"""

ht_fachstatistikergebnis_t = """Auf der obigen grafischen Darstellung sehen Sie das Ergebnis einer Fachstatistikabfrage.<br><br>
 """

ht_abfrage_katauswahl_single_t = """
<b>Abfrage: Kategoriewahl</b><br>
Durch die Auswahl dieser Abfrage wird ein Formular wie oben dargestellt angezeigt.
In diesem Formular kann genau eine Kategorie f&uuml;r das
Anzeigen der Statistik ausgew&auml;hlt werden.
<br><br>
"""
ht_abfrage_katauswahl_single_2_t = """
<b>Abfrage: Itemauswahl der Kategorie</b><br>
In diesem Formular w&auml;hlen Sie die Items der Kategorie, die in der Abfrage
ber&uuml;cksichtigt werden sollen.
<br><br>
"""

ht_abfrage_katauswahl_single_3_t = """
In diesem Formular werden Ihnen die Ergebnisse der Abfrage angezeigt.
<br><br>
"""


ht_abfrage_katauswahl_multi_t = """
<b>Abfrage: Kategorienauswahl</b><br>
Durch die Auswahl dieser Abfrage wird ein Formular wie oben dargestellt angezeigt.
In diesem Formular k&ouml;nnen mehrere Kategorie gleichzeitig f&uuml;r das
Anzeigen der Statistik ausgew&auml;hlt werden.<br><br>
"""

ht_abfrage_katauswahl_multi_2_t = """
Durch die Auswahl dieser Abfrage wird ein Formular wie oben dargestellt angezeigt.
In diesem Formular k&ouml;nnen Sie die Items f&uuml;r Ihre gew&auml;hlten Kategorien
w&auml;hlen, die in der Abfrage ber&uuml;cksichtigt werden sollen.<br><br>
"""

ht_abfrage_katauswahl_multi_3_t = """
In diesem Formular werden Ihnen die Ergebnisse der Abfrage angezeigt.
<br><br>
"""

ht_konsultationszahl_t = """
In diesem Formular wird eine &Uuml;bersicht &uuml;ber die Anzahl der abgeschlossenen Beratungsf&auml;lle mit einer vorher bestimmten Konsultationszahl bei den verschiedenen Personen oder Institutionen ausgegeben.<br><br>
"""

ht_konsultationszahl_ergebnis_t = """Auf der grafischen Darstellung sehen Sie das Ergebnis einer Konsultationszahlabfrage.<br><br>
 """

ht_konsultationssumme_t = """
In diesem Formular wird eine &Uuml;bersicht &uuml;ber die Anzahl der abgeschlossenen Beratungsf&auml;lle mit den verschiedenen Konsultationssummen ausgegeben.<br><br>
"""
ht_konsultationssumme2_t = """
In diesem Formular wird Ihnen das Ergebnis Ihrer Abfrage ausgegeben.<br><br>
"""

ht_beratungsdauer_t = """
In diesem Formular wird eine &Uuml;bersicht &uuml;ber die abgeschlossenen Beratungsf&auml;lle eines oder mehrerer Jahre mit einer bestimmten Laufdauer (in Monaten) ausgegeben.<br><br>
 """
ht_beratungsdauer2_t = """
In diesem Formular wird Ihnen das Ergebnis Ihrer Abfrage ausgegeben.<br><br>
"""

ht_beratungsdauer_leistung_t = """
In diesem Formular wird eine &Uuml;bersicht &uuml;ber die abgeschlossenen Beratungsf&auml;lle eines oder mehrerer Jahre,  mit einer bestimmten Laufdauer (in Monaten) zu einer bestimmten Leistung, ausgegeben.<br><br>
 """

ht_beratungsdauer_leistung2_t = """
In diesem Formular wird Ihnen das Ergebnis Ihrer Abfrage ausgegeben.<br><br>
"""

ht_haupt_geschwisterfaelle_t = """
In diesem Formular wird eine &Uuml;bersicht &uuml;ber die abgeschlossenen Beratungsf&auml;lle unterschieden nach Haupt- und Geschwisterfall augegeben. Hierbei wird eine quartalsweise Aufschl&uuml;sselung vorgenommen.<br><br>
 """
ht_haupt_geschwisterfaelle2_t = """
In diesem Formular wird Ihnen das Ergebnis Ihrer Abfrage ausgegeben.<br><br>
"""

ht_elternteil_merkmalx_t = """
In diesem Formular wird eine &Uuml;bersicht &uuml;ber die abgeschlossenen Beratungsf&auml;lle, bei der nur ein Elternteil das Merkmal x hat, ausgegeben. Hierbei werden die betroffenen Kategorien aufgeschl&uuml;sselt.<br><br>
 """
ht_elternteil_merkmalx2_t = """
In diesem Formular wird Ihnen das Ergebnis Ihrer Abfrage ausgegeben.<br><br>
"""

ht_eltern_merkmalx_t = """
In diesem Formular wird eine &Uuml;bersicht &uuml;ber die abgeschlossenen Beratungsf&auml;lle, bei denen beide Elternteile das gleiche Merkmal x haben, ausgegeben. Hierbei werden die betroffenen Kategorien aufgeschl&uuml;sselt.<br><br>
 """

ht_eltern_merkmalx2_t = """
In diesem Formular wird Ihnen das Ergebnis Ihrer Abfrage ausgegeben.<br><br>
"""

ht_gruppenuebersicht_t = """
In diesem Formular k&ouml;nnen Sie die Einstellungen f&uuml;r die Gruppen&uuml;berblick-Abfrage eingeben.<br><br>
"""

ht_gruppenuebersicht2_t = """
In diesem Formular wird Ihnen das Ergebnis Ihrer Abfrage ausgegeben.<br><br>
"""

ht_neumelde_und_abschluesse_t = """
In diesem Formular k&ouml;nnen Sie das Jahr f&uuml;r die Abfrage der neugemeldeten und abschlossenen
 F&auml;lle eingeben.<br><br>
"""

ht_neumelde_und_abschluesse2_t = """
In diesem Formular wird Ihnen das Ergebnis Ihrer Abfrage ausgegeben.<br><br>
"""

ht_klienten_pro_mitarbeiter_t = """
In diesem Formular k&ouml;nnen Sie das Jahr f&uuml;r die Abfrage der Klienten pro Mitarbeiter
 eingeben.<br><br>
"""

ht_klienten_pro_mitarbeiter2_t = """
In diesem Formular wird Ihnen das Ergebnis Ihrer Abfrage ausgegeben.<br><br>
"""


##*************************************************************************
## Stichwort: Monatsgenaues Datum
##*************************************************************************
st_monatsgenau_t = """
Liegt ein unbekannter Tag der Geburt vor, so ist der erste Tag des
Monats als Geburtstag zu w&auml;hlen.
<br><br>
Beispiel:<br>
<br>
Klient: Frank Schulze, geb. April 1978<br>
Einzugebendes Datum: 01.04.1978"""

##*************************************************************************
## Stichwort: Die Fallnummer
##*************************************************************************
st_fallnummer_t = """
Die Zahl vor dem Bindestrich gibt die Anzahl der Beratungsf&auml;lle seit
Jahresbeginn, die Buchstaben nach der Jahreszahl das (maximal achtstellige)
Stellenzeichen(K&uuml;rzel) an.<br>Die Beratungsfallnummer dient zur Abstimmung
mit der Papierakte bzw. anderen Formularen"""

##*************************************************************************
## Stichwort: Strassenkatalog
##*************************************************************************
st_strassenkatalog_t = """
Der Stra&szlig;enkatalog von Berlin ist in EBKuS integriert.<br>
Um den Stra&szlig;enkatalog zu verwenden ist folgende Schaltfl&auml;che <img border="0" src="/ebkus/ebkus_helppics/strassenauswahl_button.gif"> zu bet&auml;tigen.<br>
<br><br>
<b>1. Textfeld 'Stra&szlig;e in Berlin'</b><br>
   Dieses Textfeld enth&auml;lt nach Auswahl aus dem Stra&szlig;enkatalog den Stra&szlig;ennamen.<br>
<br>
<br><br>
<b>2. Textfeld 'Ausserhalb'</b><br>
   Dieses Textfeld dient f&uuml;r die freie Eingabe eines Stra&szlig;ennamens.<br>
<br><br>
<b>Erkl&auml;rung:</b><br>
<br><br>
<b>Fall1 (Person wohnt in Berlin):</b><br><br>
Wohnt die Person, deren Adresse erfasste werden soll in Berlin,
so kann der Name der Stra&szlig;e aus dem Stra&szlig;enkatalog gew&auml;hlt werden.
<br>
Hierzu ist die oben angegebene Schaltfl&auml;che zu bet&auml;tigen, welche einen seperaten Auswahldialog &ouml;ffnet.<br><br>
<img border="0" src="/ebkus/ebkus_helppics/strassenauswahl_klein.gif"><br>
<br>
Es findet vorerst keine Datenbankabfrage bezüglich des Straßenkataloges statt, alle Eingabefelder und das Listenfeld sind leer. Der Anwender macht eine Eingabe im Feld "Straßenname", wobei er mindestens die ersten beiden Buchstaben eines Straßennamens angeben muss. Unzureichende Eingaben führen zu einer Fehlermeldung. Zusätzlich zum Straßennamen (zwei Anfangsbuchstaben bis vollständiger Name) kann der Anwender eine Hausnummer und/oder Postleitzahl in die entsprechenden Felder eintragen. Je genauer er seine Suchkriterien spezifiziert, um so kleiner ist die Liste der möglichen Suchergebnisse und um so schneller ist die Datenbankabfrage beendet. Bestenfalls sind die Eingaben so eindeutig, dass genau ein Eintrag (Straßenname mit Hausnummer, Postleitzahl und Planungsraum) gefunden wird.
Im Anschluss an die eigentliche Straßensuche, die durch Klicken der Schaltfläche "Straße suchen" gestartet wird, selektiert der Anwender mit der Maus eine Zeile in der Ergebnisliste und klickt anschließend auf die Schaltfläche "Übernehmen". Die Werte (Straßenname, Hausnummer, Postleitzahl) der selektierten Zeile werden in die entsprechenden Felder der Karte "Neuaufnahme" (oder eine der anderen Karten, wo der Strassenkatalog verwendet wird) übernommen und der Auswahldialog wird automatisch geschlossen. Möchte der Anwender doch keine Straße auswählen, kann er mit der Schaltfläche "Abbrechen" die Eingaben verwerfen und den Auswahldialog schließen.
<br><br>
<b>Fall2 (Person wohnt nicht in Berlin):</b><br><br>
Es ist m&ouml;glich, dass eine Person, deren Adresse erfasst werden soll
ausserhalb Berlins wohnt.<br>
Dessen Anschrift kann folglich nicht im Stra&szlig;enkatalog von Berlin
enthalten sein.<br>
In solch einem Fall, muss der Eintrag per Hand durchgef&uuml;hrt werden.<br>
Es m&uuml;ssen Hausnummer, Postleitzahl und Ort in die dafür vorgesehenden
Felder eingegeben werden.<br>
Den Stra&szlig;ennamen der Klientenanschrift tr&auml;gt man in das 2. Feld
mit der Beschriftung 'Ausserhalb' ein.<br>
Beim Speichern wird nun der Eintrag diesem Textfeld mit der Akte
gespeichert.<br>
"""

##*************************************************************************
## Stichwort: Zu den Akten Button
##*************************************************************************

st_zu_den_akten_button_t = """
Die verschiedenen Funktionen des z.d.Akten Buttons<br>
<br>
<b>zu den Akten:</b><br>
  Tr&auml;gt die Schaltfl&auml;che diese Aufschrift, so handelt es sich um einen
  laufenden Fall, der zu den Akten gelegt werden kann. Er wird dann nicht
  mehr im <a href="ebkus_help_document?help_id=Hauptmen&uuml;">Hauptmen&uuml;</a> als laufender Fall angezeigt.
<br><br>
<b>zu den Akten r&uuml;ckg&auml;ngig:</b><br>
  Tr&auml;gt die Schaltfl&auml;che diese Aufschrift, so handelt es sich um einen vor
  nicht mehr als einen Monat zu den Akten gelegten Fall. Dieser
  Zustand kann wieder r&uuml;ckg&auml;ngig gemacht werden.
  (Beachten Sie: Das Zur&uuml;cksetzen funktioniert nur innerhalb eines Monats!)
<br><br>
<b>Wiederaufnahme:</b><br>
  Tr&auml;gt die Schaltfl&auml;che diese Aufschrift, so handelt es sich um einen vor
  mehr als einen Monat zu den Akten gelegten Fall. Dieser wird als
  'neuer Klient' betrachtet. EBKuS gibt aber so die M&ouml;glichkeit, bereits
  erfasste Stammdaten an den 'neuen Klienten' zu &uuml;bergeben.
"""
