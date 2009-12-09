Die Struktur der Dateien hier ist immer noch ziemlich
unübersichtlich. 

Grob gesagt geht es um folgendes:

1. In ``schemadata.py`` wird das Datenbankschema für EBKuS in
   einem EBKuS-spezifischen Format definiert.

2. Aus (1) wird in MySQL eine Datenbank generiert
   (``schemagen.py``).

3. Aus (1) werden ferner ein Menge von Python-Klassen generiert,
   die den komfortablen Zugriff auf diese Datenbank ermöglichen
   (``genEB.py``, das Resultat ist ``lib/ebkus/app/ebapigen.py``).

4. Die Datenbank wird mit einer Menge von Kategorien und
   Merkmalen initialisiert, die in ``sql/merkmale_{berlin,
   standard, minimal}.py`` definiert sind (``migrate.py``).

5. In die Datenbank wird ein Straßenkatalog eingelesen 
   (``migrate_strkat.py``).

Die Initialisierung einer Datenbank erfolgt nun beim
automatischen Installieren. Siehe 
``ComponentEbkusInstance.generate_initial_database()`` in
``lib/ebkus/Install.py``. Dabei werden

  schemadata.py
  schemagen.py
  migrate.py
  migrate_strkat.py

verwendet.

Es gibt zur Zeit kein funktionierendes Skript zu Punkt 3.,
Generierung der Python-Datenbank-Zugriffsklassen. Das wäre erst
wieder dann nötig, wenn das Datenbankschema verändert würde.
Die generierte Datei für das jetzige Schema,
``lib/ebkus/app/ebapigen.py``, liegt statisch im CVS und wird
**nicht** im Zuge der Datenbankinitialisierung generiert.

