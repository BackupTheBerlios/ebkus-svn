EBKuS 3.2
=========

Klientenverwaltung, Aktendokumentation, Gruppenverwaltung 
und Statistik für Erziehungs- und Familienberatungsstellen

Copyright (1997-2004) Jürg Huber, Albrecht Schmiedel 
Lizenz: GNU General Public License (GPL)

E-Mail: juerg@pantau.in-berlin.de, atms@alibi.in-berlin.de
Mailing-Liste: ebkus-support@lists.berlios.de
WWW: http://ebkus.berlios.de/index.html

Hinweis für Windows-Benutzer
----------------------------

Bitte wordpad.exe oder einen anderen Texteditor zum Lesen/Ändern
der Textdateien (insbesondere der Konfigurationsdatei)
verwenden. ``notepad.exe`` versteht die Zeilenstruktur nicht.

EBKuS läuft nur auf Windows NT/2000/XP, nicht Windows 95/98/ME.
Auf Windows NT ist das Service-Pack 6 erforderlich.

Dokumentation
-------------

Handbuch:

lokal: 

- doc/EBKuS_Handbuch.html
- doc/EBKuS_Handbuch.pdf

WWW:   

- http://ebkus.berlios.de/ebkus-3.2/EBKuS_Handbuch.html
- http://ebkus.berlios.de/ebkus-3.2/EBKuS_Handbuch.pdf

Installation
------------

Zur Installation siehe die Datei doc/installation.txt bzw. das
Kapitel Installation im Handbuch.

EBKuS-Software
--------------

- Quellen direkt aus dem CVS (bash unter Linux)::

    export CVS_RSH=ssh
    cvs -z3 -d:pserver:anonymous@cvs.EBKuS.berlios.de:/cvsroot/ebkus co ebkus-2

- nur Quellen (ca. 5MB)::

    ftp://ftp.bke.de/pub/ebkus/ebkus-3.2/ebkus-3.2-src.zip
    http://ebkus.berlios.de/ebkus/ebkus-3.2-src.zip
    http://ebkus.berlios.de/ebkus/ebkus-3.2-src.tar.gz

  Aus den Quellen kann mit dem mitgelieferten Skript create_cd.py
  eine vollständige Distribution erstellt werden.  Siehe auch den
  Abschnitt "create_cd.py" im Handbuch bzw. in der Datei
  doc/installation.txt.

- vollständige Distribution inklusive der gesamten zusätzlich
  benötigten Software (ca. 70MB)::

    ftp://ftp.bke.de/pub/ebkus/ebkus-3.2/ebkus-3.2-dist.zip


