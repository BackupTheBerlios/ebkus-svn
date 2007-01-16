Update von EBKuS 3.2 nach 3.3
=============================


Update einer vorhandenen Version 3.2 nach 3.2:


1. Alle EBKuS-Instanzen herunterfahren.

2. Aktuelles Backup aller Instanzen erstellen.

3. Ein Kopie des Homeverzeichnisses erstellen.

Mit Schritten 1 - 3 ist gewährleistet, dass im Notfall die
vorhandene Installation wieder hergestellt werden kann.

4. Den Inhalt dieses Archivs in das Homeverzeichnis kopieren.

5. Eine EBKuS-Instanz wieder hochfahren. Beim Start der Instanz
   wird das Update durchgeführt. Im Logfile der Instanz wird der
   Erfolg bzw. Misserfolg des Updates gemeldet.

6. Im Erfolgsfall die übrigen Instanzen hochfahren. In den
   entsprechenden Logfiles wird gemeldet, dass kein Update nötig
   ist.

7. Bevor die neue Bundesstatistik genutzt werden kann, müssen vom
   Administrator der Anwendung die vom statistischen Landesamt
   vergebenen Codes für das Land und den Kreis sowie die
   Einrichtungsnummer eingetragen werden. Siehe Handbuch (für
   Version 3.3!) Abschnitt 4.2.1.


Anmerkungen zu den Schritten:

(2) z.B. datenbank_sichern --zip <Verzeichnis> aus dem
Verzeichnis jeder Instanz

(3) Die alte Installation kann wiederhergestellt werden, indem
die Kopie des Homeverzeichnisses wieder an die alte Stelle
kopiert oder umbenannt wird und das Backup wieder eingelesen wird
(datenbank_initialisieren.py).

(4) Zur Kontrolle: nach dem Kopieren muss es in
<homeverzeichnis>/lib/ebkus eine Datei update.py geben.

Die in diesem Archiv enthaltenen Dateien ersetzen die
entsprechenden Dateien in der Distribution. Es kommen auch neue
Dateien hinzu. Die relativen Pfade beziehen sich auf das
Homeverzeichnis. Das Homeverzeichnis ist das Verzeichnis
``ebkus`` im Installationsverzeichnis (siehe Handbuch Abschnitt
5.3.4 Homeverzeichnis).

Ein Update kann auch von einem vollständigem Quellverzeichnis
(EBKuS-3.3) bzw. Distributionsverzeichnis (ebkus-3.3) aus
vorgenommen werden. Einfach alle Dateien von dort in das
Homeverzeichnis kopieren und wie oben verfahren. Das Patch-Archiv
enthält lediglich die gegenüber 3.2 veränderten Dateien.

(5) Anstatt den EBKuS-Dienst für die Instanz hochzufahren, kann
auch der Befehl 'python start.py --console' aus dem
Instanzverzeichnis verwendet werden. Dann sieht man die
Log-Meldungen direkt auf der Konsole.


Kompatibilität der Datenbankdumps
=================================

Da das Datenbankschema in EBKuS 3.3 sich gegenüber 3.2 verändert
hat, sind die Datenbanksicherungen nicht ohne weiteres
kompatibel. Wenn ein alter Dump in eine neue Version eingelesen
wird (datenbank_sichern.py, datenbank_initialisieren.py), wird
danach beim Hochfahren wieder der Update-Vorgang
angestossen. Dann sollte alles in Ordnung sein. Umgekehrt ist es
allerdings weder sinnvoll noch möglich, einen neuen Dump in eine
alte Installation einzulesen.


Bei Problemen, Fragen, Anregungen wenden Sie sich bitte an
Albrecht Schmiedel, atms@alibi.in-berlin.de oder +49 30 6859236.