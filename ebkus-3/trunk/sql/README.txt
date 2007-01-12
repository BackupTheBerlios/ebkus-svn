Dateien zur Initialisierung der Datenbank
=========================================


Vollständiger Berliner Straßenkatalog bzw. Auschnitt für Demo::

  strassen_katalog_berlin.txt.gz
  strassen_katalog_berlin_ausschnitt.txt.gz

Neuer Berliner Straßenkatalog ab EBKuS 3.3, nicht mehr als
Textdatei, sonder als SQL:

  strassenkat_berlin.sql.gz
  strassenkat_berlin_ausschnitt.sql.gz

Merkmalsdefinitionen zur Initialisierung der Datenbank
mit Berliner Merkmalen bzw. ohne Berliner Merkmalen::

  merkmale_berlin.py
  merkmale_standard.py

Hier sollten nur die Merkmale stehen, die für das Funktionieren
von EBKuS unbedingt erforderlich sind. Im Moment aber noch 
identisch mit merkmale_standard.py::

  merkmale_minimal.py


SQL-Dumps für die Initialisierung der Datenbank. Dienen nur dazu,
die Installation zu beschleunigen. Sie können jederzeit regeneriert
werden mit Hilfe der obigen Merkmalsdateien und dem 
Demodaten-Generator in ``lib/ebkus/gen/demodaten.py``::

  demo_berlin.sql.gz
  demo_standard.sql.gz
  standard.sql.gz
