Neue Bundesstatistik 2007
=========================

Der Hauptgrund für das Update von EBKuS 3.2 auf 3.3 ist die neue
Bundesstatistik ab dem Jahr 2007.


Einrichtung nach der Installation und vor der Inbetriebnahmen
-------------------------------------------------------------

Bevor die neue Bundesstatistik genutzt werden kann, müssen vom
Administrator der Anwendung die vom statistischen Landesamt
vergebenen Codes für das Land und den Kreis sowie die
Einrichtungsnummer eingetragen werden. Siehe Handbuch (für
Version 3.3!, siehe ebkus/doc/EBKuS_Handbuch.html) Abschnitt 4.2.1.


Alte und neue Statistik nebeneinander
-------------------------------------

Ist es möglich, nach dem Update noch mit der alten
Bundesstatistik zu arbeiten?

Ja, das ist möglich, je nach dem, welches Endedatum in das
Statistikformular eingetragen wird. 

- Fälle, für die bereits eine Statistik im alten Jahr ausgefüllt
  wurde, behalten diese. Falls ein solcher Fall jedoch
  fortgeführt werden soll, kann die alte Statistik durch eine
  neue ersetzt werden, indem ein Endedatum aus dem Jahr 2007 in
  die alte Statistik eingetragen und abgespeichtert wird. Darauf
  erscheint das neue Statistikformular, das nunmehr ausgefüllt
  werden muss.

- Fälle, für die noch keine Statistik angelegt wurde, bekommen
  zunächst immer ein Formular der neuen Statistik. Wenn der Fall
  jedoch im Jahr 2006 oder früher begonnen wurde und im Nachhinein
  noch im Jahr 2006 abgeschlossen werden soll, wird als Endedatum
  ein Datum aus dem Jahr 2006 eingetragen und
  abgespeichtert. Darauf erscheint das alte Statistikformular,
  das nunmehr ausgefüllt werden muss.

Bei der Auswertung der Bundesstatistik hängt es von den
angegebenen Jahren ab, ob die alte oder die neue Statistik
zugrunde gelegt wird. Es können keine Auswertungen vorgenommen
werden, die sowohl Jahre bis 2006 als auch Jahre ab 2007
umfassen. 

Der Export der Datensätze hängt ebenfalls vom angegebenen
Jahrgang ab. Ab 2007 ist es immer das neue Format. 


Andauernde Fälle
================

Neben der Statistik über abschlossene Fälle gibt es nun auch eine
solche für am Jahresende andauernden Fälle. Auch für diese können
Exportdateien für die Abgabe beim Landesamt erzeugt werden. Es
gehen alle Fälle ein, für die Statistiken existieren, deren
Beginn im Vorjahr (oder früher) des Exportjahres liegt und wo im
Formular 'am Jahresende andauernd' angekreuzt wurde. 

Die für einen andauernden Fall erzeugte laufende Nummer wird
beibehalten, wenn der Fall später abgeschlossen wird.
