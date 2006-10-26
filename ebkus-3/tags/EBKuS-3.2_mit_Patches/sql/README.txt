Dateien zur Initialisierung der Datenbank
=========================================


Vollst�ndiger Berliner Stra�enkatalog bzw. Auschnitt f�r Demo::

  strassen_katalog_berlin.txt.gz
  strassen_katalog_berlin_ausschnitt.txt.gz


Merkmalsdefinitionen zur Initialisierung der Datenbank
mit Berliner Merkmalen bzw. ohne Berliner Merkmalen::

  merkmale_berlin.py
  merkmale_standard.py

Hier sollten nur die Merkmale stehen, die f�r das Funktionieren
von EBKuS unbedingt erforderlich sind. Im Moment aber noch 
identisch mit merkmale_standard.py::

  merkmale_minimal.py


SQL-Dumps f�r die Initialisierung der Datenbank. Dienen nur dazu,
die Installation zu beschleunigen. Sie k�nnen jederzeit regeneriert
werden mit Hilfe der obigen Merkmalsdateien und dem 
Demodaten-Generator in ``lib/ebkus/gen/demodaten.py``::

  demo_berlin.sql.gz
  demo_standard.sql.gz
  standard.sql.gz
