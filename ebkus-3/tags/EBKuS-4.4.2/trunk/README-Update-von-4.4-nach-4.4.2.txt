Update von EBKuS 4.4 nach 4.4.2
===============================


Update einer vorhandenen Version 4.4 nach 4.4.1:

0. Stellen Sie sicher, dass eine Version 4.4 oder h�her installiert
   ist. Die Version erscheint in der Mitte der Statuszeile, die auf
   fast allen Masken der Anwendung ausgegeben wird.

1. Alle EBKuS-Instanzen herunterfahren.

2. Aktuelles Backup aller Instanzen erstellen.

3. Ein Kopie des Installationsverzeichnisses erstellen.

Mit Schritten 1 - 3 ist gew�hrleistet, dass im Notfall die
vorhandene Installation wieder hergestellt werden kann.

4. Den Inhalt dieses Archivs in das Homeverzeichnis kopieren.

5. Eine EBKuS-Instanz wieder hochfahren. Im Logfile der Instanz wird
   bei Erfolg "Datenbankversion und Softwareversion sind
   kompatibel." und "Keine Update erforderlich" gemeldet.

6. Im Erfolgsfall die �brigen Instanzen hochfahren. In den
   entsprechenden Logfiles erscheinen dieselben Meldungen.


Anmerkungen zu den Schritten:

(2) Skript ``datenbank_sichern --zip <Verzeichnis>`` aus dem
Verzeichnis jeder Instanz

(3) Die alte Installation kann wiederhergestellt werden, indem
die Kopie des Installationsverzeichnisses wieder an die alte
Stelle kopiert oder entsprechend umbenannt wird und die Backups f�r jede
Instanz wieder eingelesen werden. (Skript
``datenbank_initialisieren.py --zip <Backup-Datei.zip>``).

(5) Zur Kontrolle: nach dem Kopieren muss es in
``<homeverzeichnis>/lib/ebkus`` eine aktualisierte Datei
``update.py`` (Datum!) geben. 

Die in diesem Archiv enthaltenen Dateien ersetzen die
entsprechenden Dateien im Homeverzeichnis. Es k�nnen auch neue
Dateien hinzukommen. Die relativen Pfade beziehen sich auf das
Homeverzeichnis. Das Homeverzeichnis ist das Verzeichnis
``ebkus`` im Installationsverzeichnis (siehe Handbuch Abschnitt
5.3.4 Homeverzeichnis).

(6) Anstatt den EBKuS-Dienst f�r die Instanz hochzufahren, kann
auch der Befehl ``python start.py --console`` aus dem
Instanzverzeichnis verwendet werden. Dann sieht man die
Log-Meldungen direkt auf der Konsole.


Kompatibilit�t der Datenbankdumps
---------------------------------

Da das Datenbankschema in EBKuS 4.4.2 sich gegen�ber 4.4 nicht
ver�ndert hat, sind die Datenbanksicherungen kompatibel. 

Bei Problemen, Fragen, Anregungen wenden Sie sich bitte an
Albrecht Schmiedel, albrecht.schmiedel@ebkus.org oder +49 30 6859236.
