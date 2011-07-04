Update von EBKuS 4.3 nach 4.4
=============================


Update einer vorhandenen Version 4.3 (möglich ist auch eine
vorhandene Version 4.2) nach 4.4:

0. Stellen Sie sicher, dass die Version 4.3 (oder 4.2)  installiert
   ist. Die Version erscheint in der Mitte der Statuszeile, die auf
   fast allen Masken der Anwendung ausgegeben wird bzw. in der Datei
   ``<Homeverzeichnis>/lib/ebkus/__init__.py`` der Installation.

1. Alle EBKuS-Instanzen herunterfahren.

2. Aktuelles Backup aller Instanzen erstellen.

3. Ein Kopie des Installationsverzeichnisses erstellen.

Mit Schritten 1 - 3 ist gewährleistet, dass im Notfall die
vorhandene Installation wieder hergestellt werden kann.

4. Für die Durchführung des Updates muss die Konfigurationsdatei
   (``<Homeverzeichnis>/ebkus.conf``) nicht angepasst werden. Ab
   Version 4.4 kann der Anwendungsbetreuer selber fachbezogene
   Konfigurationsvariablen im laufenden Betrieb ändern.

5. Den Inhalt dieses Archivs in das Homeverzeichnis kopieren.

6. Eine EBKuS-Instanz wieder hochfahren. Beim Start der Instanz
   wird das Update durchgeführt. Im Logfile der Instanz wird der
   Erfolg bzw. Misserfolg des Updates gemeldet.

7. Im Erfolgsfall die übrigen Instanzen hochfahren. In den
   entsprechenden Logfiles wird ebenfalls der Erfolg des Updates
   gemeldet.

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
auch der Befehl ``start.py --console`` aus dem Instanzverzeichnis
verwendet werden (im DOS-Fenster). Dann sieht man die
Log-Meldungen direkt auf der Konsole. Im Erfolgsfall kann man mit
dem Befehl ``stop.py`` (aus einem anderen DOS-Fenster) die
Instanz wieder herunterfahren und den entsprechenden EBKuS-Dienst 
wieder starten.


Kompatibilität der Datenbankdumps
---------------------------------

Da das Datenbankschema in EBKuS 4.4 sich gegenüber 4.3 verändert
hat, sind die Datenbanksicherungen nicht ohne weiteres
kompatibel. Wenn ein alter Dump in eine neue Version eingelesen
wird (``datenbank_sichern.py, datenbank_initialisieren.py``),
wird danach beim Hochfahren wieder der Update-Vorgang
angestossen. Dies geht allerdings nur für Dumps, die mit Version
4.2 bzw. 4.3 erzeugt wurden, nicht jedoch für ältere. Umgekehrt
ist es allerdings weder sinnvoll noch möglich, einen neuen Dump
in eine alte Installation einzulesen.


Bei Problemen, Fragen, Anregungen wenden Sie sich bitte an
Albrecht Schmiedel, albrecht.schmiedel@ebkus.org oder +49 30 6859236.
