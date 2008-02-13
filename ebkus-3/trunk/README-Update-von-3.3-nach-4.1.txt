Update von EBKuS 3.3 nach 4.1
=============================


Update einer vorhandenen Version 3.3 nach 4.1:


1. Alle EBKuS-Instanzen herunterfahren.

2. Aktuelles Backup aller Instanzen erstellen.

3. Ein Kopie des Installationsverzeichnisses erstellen.

Mit Schritten 1 - 3 ist gewährleistet, dass im Notfall die
vorhandene Installation wieder hergestellt werden kann.

4. Anpassung der Konfigurationsdatei
   (``<Homeverzeichnis>/ebkus.conf``). Hier sind eventuell neue
   Konfigurationsvariable zu setzen, siehe NEU_IN_VERSION_4.1.txt.

5. Den Inhalt dieses Archivs in das Homeverzeichnis kopieren.

6. Eine EBKuS-Instanz wieder hochfahren. Beim Start der Instanz
   wird das Update durchgeführt. Im Logfile der Instanz wird der
   Erfolg bzw. Misserfolg des Updates gemeldet.

7. Im Erfolgsfall die übrigen Instanzen hochfahren. In den
   entsprechenden Logfiles wird ebenfalls der Erfolg des Updates
   gemeldet.

8. Bevor die neue Bundesstatistik genutzt werden kann, müssen vom
   Administrator der Anwendung die vom statistischen Landesamt
   vergebenen Codes für das Land und den Kreis sowie die
   Einrichtungsnummer eingetragen werden. Siehe Handbuch (für
   Version 3.3!) Abschnitt 4.2.1.


Anmerkungen zu den Schritten:

(2) Skript ``datenbank_sichern --zip <Verzeichnis>`` aus dem
Verzeichnis jeder Instanz

(3) Die alte Installation kann wiederhergestellt werden, indem
die Kopie des Installationsverzeichnisses wieder an die alte
Stelle kopiert oder entsprechend umbenannt wird und die Backups für jede
Instanz wieder eingelesen werden. (Skript
``datenbank_initialisieren.py --zip <Backup-Datei.zip>``).

(5) Zur Kontrolle: nach dem Kopieren muss es in
``<homeverzeichnis>/lib/ebkus`` eine aktualisierte Datei
``update.py`` (Datum!) geben. 

Die in diesem Archiv enthaltenen Dateien ersetzen die
entsprechenden Dateien im Homeverzeichnis. Es kommen auch neue
Dateien hinzu. Die relativen Pfade beziehen sich auf das
Homeverzeichnis. Das Homeverzeichnis ist das Verzeichnis
``ebkus`` im Installationsverzeichnis (siehe Handbuch Abschnitt
5.3.4 Homeverzeichnis).

(6) Anstatt den EBKuS-Dienst für die Instanz hochzufahren, kann
auch der Befehl ``python start.py --console`` aus dem
Instanzverzeichnis verwendet werden. Dann sieht man die
Log-Meldungen direkt auf der Konsole.


Kompatibilität der Datenbankdumps
---------------------------------

Da das Datenbankschema in EBKuS 4.1 sich gegenüber 3.3 verändert
hat, sind die Datenbanksicherungen nicht ohne weiteres
kompatibel. Wenn ein alter Dump in eine neue Version eingelesen
wird (``datenbank_sichern.py, datenbank_initialisieren.py``), wird
danach beim Hochfahren wieder der Update-Vorgang
angestossen. Dann sollte alles in Ordnung sein. Umgekehrt ist es
allerdings weder sinnvoll noch möglich, einen neuen Dump in eine
alte Installation einzulesen.


Bei Problemen, Fragen, Anregungen wenden Sie sich bitte an
Albrecht Schmiedel, atms@alibi.in-berlin.de oder +49 30 6859236.