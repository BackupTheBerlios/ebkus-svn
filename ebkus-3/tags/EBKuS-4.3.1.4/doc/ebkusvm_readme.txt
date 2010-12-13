EBKuS Virtuelle Maschine für VMware
-----------------------------------

.. |download_url| replace:: ftp://ftp.efb-berlin.de/pub/ebkus/ebkusvm/us-10.04-i386-ebkus-vm.zip

:Autor: Albrecht Schmiedel
:Email: albrecht.schmiedel@ebkus.org
:EBKuS-VM: |download_url|
:EBKuS-Homepage: http://www.ebkus.org
:Datum: 2010-08-10

[Überschriften und Inhaltsverzeichnis sind *gegenseitig* verlinkt]

.. contents::

.. sectnum::

Was ist EBKuS-VM?
.................

EBKuS-VM ist ein virtuelle Maschine (VM), auf dem sowohl ein
Betriebssystem als auch die Anwendung EBKuS installiert
sind. Nach dem Start der VM (Gastsystem) auf einem realen Rechner
(Hostsystem) in einer geeigneten Virtualisierungsumgebung stehen
die auf dem Gast installierten Anwendungen zur Verfügung. Die
virtuelle Maschine verhält sich wie ein zusätzlicher Rechner im
lokalen Netzwerk.

Die EBKuS-VM benötigt die VMware Virtualisierungsumgebung. Im
einfachsten Fall steht diese in Form des VMware Player zur
Verfügung, der kostenlos für Windows und GNU/Linux erhältlich
ist:

- http://www.vmware.com/products/player/ (inzwischen auch von
  anderen Websites herunterladbar)

Die VMware Virtualisierungsumgebung wird aber auch in
Rechenzentren verwendet. So laufen sämtliche Berliner
EBKuS-Installationen auf einer ähnlichen wie hier beschriebenen
virtuellen Maschine, die vom IT-Service des Bezirksamts
Friedrichshain-Kreuzberg gehostet wird.

Das Betriebssystem der EBKuS-VM ist Ubuntu 10.04 LTS (Lucid Lynx)
Server (eine GNU/Linux Distribution). Diese Version wurde im
April 2010 freigegeben und wird bis April 2015 unterstützt (LTS
steht für Long Term Support).

Eine grafische Oberfläche gibt es nicht. Der Resourcenverbrauch
ist entsprechend gering. 

Im ZIP-Archiv befindet sich das Verzeichnis
``us-10.04-i386-ebkus-vm`` mit allen notwendigen Dateien, u.a.:

- ``ebkusvm1.vmx``: Eine Textdatei mit Parametern für VMware
  Player, die mit einem Editor bearbeitet werden kann. Das ist
  die Konfiguration des virtuellen PCs. Der diesem PC zugeteilte
  Arbeitsspeicher ist in folgender Zeile definiert::

    memsize = "256"

  Dieser voreingestellte Wert dürfte in der Regel für den
  Betrieb von ein paar EBKuS-Instanzen genügen.

- ``scsi_lsilogic_6gb.vmdk``: Das virtuelle Laufwerk. Sämtliche Daten des
  virtuellen PC befinden sich in dieser Datei. Das Laufwerk hat
  eine Kapazität von 6GB, die aber physikalisch auf dem Hostsystem erst
  bei entsprechendem Bedarf anfallen. Im Auslieferungszustand
  nimmt die EBKuS-VM 1,6GB Plattenplatz ein.


Schnellstart
............

Voraussetzung: 

- Ein PC oder Notebook im lokalen Netzwerk (GNU/Linux oder
  Windows) mit minimal 1GB Ram und 3GB freien Platz auf der
  Festplatte. 

- Ein DHCP-Server, der einem neuen Rechner im lokalen Netz eine
  neue IP-Nummer zuweisen kann. In einem üblichen WLAN oder mit
  einem Standard-DSL-Router ist das normalerweise der Fall.

Schritte:

1. VMware Player installieren.

2. EBKuS-VM herunterladen und auspacken.

3. Die im Ordner ``us-10.04-i386-ebkus-vm`` enthaltene Datei
   ``ebkusvm1.vmx`` doppelklicken bzw. mit VMware Player
   öffnen.

4. IP-Nummer der gestarteten EBKuS-VM ermitteln:

  - In das schwarze Fenster des Player hineinklicken und Return
    eingeben, bis die Aufforderung zum Login erkennbar ist. 

  - Anmelden als Benutzer ``ebkus`` und dem Passwort ``ebkus``.

  - ``ifconfig`` eingeben und mit Return abschicken. Die
    IP-Nummer erscheint oben rechts neben ``eth0`` nach ``inet addr``.

  - Durch gemeinsames Drücken der Steuerung- und Alt-Taste die
    VM-Konsole verlassen.

5. In das Adressfeld des Firefox (oder auch des IE) folgende
   Adresse eintippen (``<IP-Nummer>`` durch die ermittelte Nummer
   ersetzen!)::

     https://<IP-Nummer>/ebkus/demo/cgi/do/login

6. Anmelden mit Benutzer ``test`` mit Passwort ``test``
   bzw. ``Admin`` mit Passwort ``Admin``.

7. Enjoy!


Server Administration
.....................


Arbeiten auf der Kommandozeile
,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,

Grundsätzlich kann auf der EBKuS-VM nur mit der Kommandozeile
gearbeitet werden, da keine grafische Oberfläche installiert
ist. 

Entweder man meldet sich direkt auf der virtuellen Konsole an
(die einzige Möglichkeit, solange das Netzwerk nicht
funktioniert), oder man verwendet ``ssh``, was in der Regel
komfortabler ist.

GNU/Linux::

  ssh -l ebkus <IP-Nummer>

Windows: Das Programm ``putty`` kann man sich kostenlos
herunterladen und installieren. Es handelt sich um einen
vollwertigen ssh-Client.

In beiden Fällen erhält man nach der Anmeldung eine Konsole, in
die man Befehle eingeben kann. Eine minimale Vertrautheit mit
Befehlen wie ``ls``, ``cd``, ``rm``, etc. ist hier von Vorteil
:-)

Den Benutzer ``root`` für Operationen, die Administratorrechte
erfordern, benötigt man nicht, da man jedem Befehl ``sudo``
voranstellen kann. Editieren einer Datei mit Administratorrechten::

  sudo nano /etc/sshd_config


Benutzer und Passwort
,,,,,,,,,,,,,,,,,,,,,

Für die Arbeit mit EBKuS ist ein Benutzer ``ebkus``
eingerichtet. Das Passwort ist ebenfalls ``ebkus``, das man mit
dem Befehl ``passwd`` ändern kann. 

Tip: Wenn man wiederum ein "einfaches" Passwort haben möchte,
sollte man als Administrator das Passwort wechseln::

  sudo passwd ebkus

Der Benutzer ``ebkus`` hat Administratorrechte, d.h. er kann
Befehle durch voranstellen von ``sudo`` als Administrator
ausführen, wobei er beim ersten Mal (in einer gewissen
Zeitspanne) nach seinem *eigenen*
Passwort gefragt wird.

Netzwerkkonfiguration
,,,,,,,,,,,,,,,,,,,,,

Für die regelmäßige Benutzung von EBKuS ist es unerlässlich, dass
die EBKuS-VM immer dieselbe IP-Nummer hat. Ansonsten müsste man
beim Zugriff über den Browser immer eine andere Adresse eintragen.

DHCP
;;;;

Die VM ist so vorkonfiguriert, dass sie ihre IP-Adresse über einen
vorhandenen DHCP-Server bezieht. Dies kann eine Weile
dauern. Evt. erscheint der Login-Prompt der VM, bevor eine
IP-Adresse zugewiesen ist.

Damit der DHCP-Server der VM immer dieselbe IP-Adresse zuweist,
muss ein entsprechender Eintrag in die DHCP-Konfiguration
vorgenommen werden. Dabei wird die Mac-Adresse der (virtuellen) Netzwerkkarte
der EBKuS-VM verwendet.  Ein solcher Eintrag ist bei vielen
Routern möglich, auch bei solchen, die im privaten Bereich
eingesetzt werden.  Die Mac-Adresse des virtuellen Servers findet
sich in der Datei ``ebkusvm1.vmx`` in der Zeile::

  ethernet0.generatedAddress = "00:0c:29:c4:d7:19"


Statische IP-Nummer
;;;;;;;;;;;;;;;;;;;

Die andere Möglichkeit besteht darin, direkt in der EBKuS-VM eine
statische IP-Adresse zu konfigurieren. Dazu muss die Datei
``/etc/network/interfaces`` in der VM editiert werden (als
Administrator, d.h. der Editor ist immer mit vorangestelltem
``sudo`` aufzurufen!).

Dynamische Konfiguration::

  # The primary network interface
  auto eth0
  iface eth0 inet dhcp
  #iface eth0 inet static
  #   address 192.168.1.226
  #   netmask 255.255.255.0
  #   gateway 192.168.1.1
  #   broadcast 192.168.1.255

Statische Konfiguration mit z.B. mit ``192.168.1.226``::

  # The primary network interface
  auto eth0
  #iface eth0 inet dhcp
  iface eth0 inet static
     address 192.168.1.226
     netmask 255.255.255.0
     gateway 192.168.1.1
     broadcast 192.168.1.255

Damit die Veränderungen in Kraft treten, muss das Netzwerk neu
gestartet werden::

  sudo /etc/init.d/networking restart

Die wirksame (dynamisch zugewiesene bzw. statische) IP-Adresse
erfährt man mit dem Befehl ``ifconfig``.

Nach der korrekten Installation und dem Start der VM muss auf dem
Hostsystem (oder auf einem anderen Rechner im lokalen Netz)
``ping <IP-Nummer>`` funktionieren, wobei <IP-Nummer> die
IP-Adresse der VM ist.

SSH
;;;

Auf der EBKuS-VM ist ein ssh-Server betriebsbereit. Der Zugriff
erfolgt über den Standard-Port 22, es aber auch ein Zugriff über den
Nicht-Standard-Port 7077 möglich. Wenn ein Zugriff von außen über
das Internet ermöglicht werden soll (siehe nächsten Abschnitt),
empfiehlt es sich, den Zugang über Benutzer/Passwort zu verbieten
und ausschließlich den Zugang über Schlüsselpaare
zuzulassen, womit Angriffe über das Erraten von Passwörter
unmöglich werden. Konfiguriert wird das in der Datei
``/etc/ssh/sshd_config``. Standardmäßig ist der Zugang über
Benutzer/Passwort erlaubt.

SSH-Tunnel
;;;;;;;;;;

Wenn die EBKuS-VM in einem lokalen Netzwerk hinter einer Firewall
steht, kann sie dennoch sicher von außen (d.h vom Internet)
angesprochen werden, sowohl zum Administrieren als auch zum
Zugriff auf die EBKuS-Anwendung. Folgende Schritte sind nötig:

- Ein "Loch" in der Firewall für den ssh-Port 22 und die
  Weiterleitung an die EBKuS-VM als Endpunkt für Zugriffe auf den
  Port 22. Anstelle des Standard-Ports 22 kann auch ein
  Nicht-Standard-Port gewählt werden, z.B. 7077, der in der
  EBKuS-VM vorkonfiguriert ist (``/etc/ssh/sshd_config``).

.. _

- Ein privater und ein öffentlicher Schlüssel, generiert mit
  ``ssh-keygen`` bzw. ``puttygen`` auf Windows. Der öffentliche
  Schlüssel wird auf der EBKuS-VM installiert, der private kommt
  auf die Rechner der berechtigten Benutzer. Der private
  Schlüssel kann zusätzlich mir einer Passphrase abgesichert
  werden, so dass jemand, der unberechtigt an den Schlüssel
  gelangt, damit nichts anfangen kann, solange er die Passphrase
  nicht kennt.

.. _

- Falls die Anbindung des lokalen Netzwerks an das Internet nicht
  über eine statische IP-Nummer erfolgt (was bei den
  preisgünstigen Providern für den Heimgebrauch immer der Fall
  ist), muss der Zugriff von außen über einen dynamischen
  DNS-Dienst erfolgen. (Das kann man in vielen Routern direkt
  konfigurieren, z.B. kann ich auf meinen Rechner zu Hause über
  die domain ``alibi.dnsalias.org`` zugreifen, die mir von dem
  DNS-Dienst dyndns_ zugeteilt wurde.)

.. _dyndns: http://www.dyndns.org/

- Ein Login auf die EBKuS-VM von irgendwo (kann in der Firewall
  auch bestimmte IP-Adress-Bereiche eingeschränkt werden) aus dem
  Internet sähe dann z.B. so aus (vorausgesetzt der private
  Schlüssel ist lokal vorhanden und der Nicht-Standard-Port 7077
  ist in der Firewall freigeschaltet)::

    ssh -l ebkus -p 7077 alibi.dnsalias.org


- Ein Zugriff auf die EBKuS-Anwendung von einem entfernten
  Rechner aus über das Internet kann dann über die (lokale) Adresse::

    https://localhost:7890/ebkus/demo/cgi/do/login

  erfolgen, wenn vorher auf dem entfernten Rechner ein ssh-Tunnel wie folgt aufgebaut
  wurde::

    ssh -l ebkus -p 7077 -L 7890:192.168.1.226:443 ebkus@alibi.dnsalias.org


- Von einem entfernten Windows-Rechner sind mit putty_ beide Zugriffsarten ebenfalls möglich.

.. _putty: http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html

Shares
,,,,,,

Das EBKuS Verzeichnis ``/home/ebkus`` der VM lässt sich als
Netzlaufwerk auf dem Hostsystem (oder einem anderen Rechner im
lokalen Netzwerk) wie eine Windows-Freigabe einbinden:

- Windows: im Explorer: Netzlaufwerk verbinden: ``\\<IP-Nummer>\ebkus``

- Ubuntu Linux: im Datei-Browser: Datei --> mit Server verbinden 

- Linux Kommandozeile: (geht nur, wenn Samba-Client installiert ist), z.B.::
  
   mount -t smbfs -o 'username=ebkus,password=ebkus' //<IP-Nummer>/ebkus /mnt/ebkus

Benutzer und Passwort ist ``ebkus``.
Das Passwort ändert sich nicht, wenn man das Linux-Benutzer
Passwort mit ``passwd`` ändert. Man kann es wie folgt ändern::

  sudo smbpasswd ebkus
  ... [man wird aufgefordert, das neue Passwort einzugeben]
  sudo /etc/init.d/samba restart


Dateien editieren
,,,,,,,,,,,,,,,,,

Falls ``/home/ebkus`` als Share auf dem Host
eingebunden ist, kann natürlich jeder Editor (außer Notepad, der
mit Unix-Zeilenumbruch nicht klar kommt) auf dem Hostsystem
verwendet werden, z.B. `notepad++`_ (kann kostenlos heruntergeladen
werden). 

.. _`notepad++`: http://notepad-plus-plus.org/de/node/56

Auf der EBKuS-VM selbst gibt es nur die text-basierte Editoren
``emacs``, ``vi`` und ``nano``. Nano ist vollständig
selbstdokumentierend und daher am einfachsten, wenn man die
anderen nicht kennt.

Log-Dateien
,,,,,,,,,,,

Da verschiedene Dateien (insbesondere Log-Dateien) mit der Zeit
sehr viel Platz einnehmen können, ist es für einen lange Zeit
laufenden Server wichtig, dass automatisch und regelmäßig solche
Dateien komprimiert und nach einer gewissen Zeit auch gelöscht
werden. ``logrotate`` ist hierfür das einschlägige Programm auf
einem GNU/Linux-System. Die EBKuS-VM ist so konfiguriert, dass sie
ohne manuelle Wartung auf diesem Gebiet dauerhaft laufen kann.

Voraussetzung ist jedoch, dass die Maschine zu den Zeiten läuft,
wo diese Wartungsprozesse aufgerufen werden. Diese Zeiten sind in
der Datei ``/etc/crontab`` definiert::

  # m h dom mon dow user  command
  17 *    * * *   root    cd / && run-parts --report /etc/cron.hourly
  25 17   * * *   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily )
  47 17   * * 7   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.weekly )
  52 17   1 * *   root    test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.monthly )
  #

Die ``17`` in der zweiten Spalte unter ``h`` definiert die
Stunde, in der die Wartungsskripte aufgerufen werden. Zu dieser
Zeit müsste EBKuS-VM also laufen. Hier kann man eine genehme
Stunde eintragen.

Im Notfall kann man auch gelegentlich per Hand das entsprechende
Skript anstossen:: 

  sudo logrotate  /etc/logrotate.conf 

Die Log-Dateien der EBKuS-Instanzen (siehe unten)
(``/home/ebkus/ebkus_installation/ebkus/<Instanzname>/<Instanzname>.log``)
sind in das logrotate-Verfahren eingebunden
(Konfigurationseinträge im Verzeichnis  ``/etc/logrotate.d/``).
Log-Dateien für EBKuS-Instanzen werden 52 Wochen aufbewahrt, ehe sie
gelöscht werden.


Updates
,,,,,,,

Ein gelegentliches::

  sudo apt-get update

gefolgt von::

  sudo apt-get upgrade

hält eine EBKuS-VM mit Internetzugang auf dem neuesten Stand, insbesondere was
Sicherheitslücken betrifft. (Das kann auch automatisiert werden.
Ich bin mir nicht ganz klar darüber, ob die EBKuS-VM das
automatisch macht.)



EBKuS-Administration
....................

Obwohl das `EBKuS-Handbuch`_ hinsichtlich der Anwendung sich
nicht auf dem neuesten Stand befindet, ist das Kapitel
Installation_ nach wie vor aktuell. Alles, was dort für die
GNU/Linux-Installation gesagt wird, gilt auch für die EBKuS-VM.
Hier wird nur auf die Besonderheiten der EBKuS-VM eingegangen.

.. _`EBKuS-Handbuch`: http://ebkus.org/doc/EBKuS_Handbuch.html

.. _Installation: http://ebkus.org/doc/EBKuS_Handbuch.html#installation

Das EBKuS-Handbuch findet man lokal als Datei unter::

  /home/ebkus/ebkus_installation/ebkus/doc/EBKuS_Handbuch.html

bzw. über den Browser unter::

  https://<IP-Nummer>/ebkus/doc/EBKuS_Handbuch.html

oder auch im Internet unter http://ebkus.org/doc/EBKuS_Handbuch.html


Verzeichnisse
,,,,,,,,,,,,,

Die gesamte EBKuS-Installation findet sich beim Benutzer
``ebkus`` unter ``/home/ebkus``.

Verzeichnisse (siehe `Handbuch Kapitel 5.3`_):

.. _`Handbuch Kapitel 5.3`: http://ebkus.org/doc/EBKuS_Handbuch.html#verzeichnisstruktur-und-dateien

- Installationsverzeichnis: ``/home/ebkus/ebkus_installation/``
- Homeverzeichnis: ``/home/ebkus/ebkus_installation/ebkus/``
- Backupverzeichnis: ``/home/ebkus/backups``


Installierte EBKuS-Instanzen
,,,,,,,,,,,,,,,,,,,,,,,,,,,,

Auf der VM sind vier EBKuS-Instanzen konfiguriert: 

- ``demo`` (mit Demodaten)
- ``demo_berlin`` (mit Demodaten und dem Berliner
  Straßenkatalog) 
- ``demo_braunschweig`` (mit Demodaten und Braunschweiger Straßenkatalog)
- ``test1`` (ohne Demodaten)

Die Instanzen werden automatisch beim Hochfahren gestartet und
sind auf dem Host-Rechner und im lokalen Netz unter folgender URL
ansprechbar::

  https://<IP-Nummer>/ebkus/<Instanzname>/

``<IP-Nummer>`` ist die IP-Adresse der EBKuS-VM. 

Anmelden bei den drei Demo-Instanzen:

- als Administrator: Benutzer: ``Admin``, Passwort: ``Admin``
- als Bearbeiter: Benutzer: ``test``, Passwort: ``test``

Anmelden bei der leeren Instanz ``test1`` ist nur als
Administrator möglich:

- Benutzer: ``Admin``, Passwort: ``Admin``

Als Administrator können dann weitere Benutzer eingerichtet
werden. 


Instanzen starten/anhalten/Status abfragen
,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,

Zusätzlich zu den im `Handbuch`_ beschriebenen Verfahren gibt es
ein Skript ``ebkusctl``, mit dem sich die einzelnen
EBKuS-Instanzen steuern lassen::

  ebkusctl <Instanzname oder all> <start|restart|stop|status>

z.B.::
  
  ebkusctl help
  ebkusctl all stop
  ebkusctl demo_berlin status

.. _`Handbuch`: http://ebkus.org/doc/EBKuS_Handbuch.html#start-des-ebkus-servers

Alle Instanzen sind standardmäßig als Dienste eingerichtet, die
beim Hochfahren des Systems automatisch gestartet und beim
Herunterfahren automatisch angehalten werden. Zur Fehlersuche
empfiehlt sich das im Handbuch beschriebene Verfahren, z.B. für
die Instanz ``demo_berlin``::

  cd /home/ebkus/ebkus_installation/ebkus/demo_berlin
  ./status.py
  ./stop.py
  ./start.py --console

Eine auf diese Weise gestartete Instanz schreibt ihre Ausgabe auf
die Konsole anstatt in die Log-Datei.

Einrichten einer neuen EBKuS-Instanz
,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,

Siehe im Handbuch besonders die Kapitel Konfiguration_ und `configure.py`_.

.. _Konfiguration: http://ebkus.org/doc/EBKuS_Handbuch.html#konfiguration

.. _`configure.py`: http://ebkus.org/doc/EBKuS_Handbuch.html#configure-py


1. Mit einem Texteditor die neue Instanz in die
   Konfigurationsdatei eintragen::

     cd /home/ebkus/ebkus_installation/ebkus/
     nano ebkus.conf

   Zu beachten:

   - Wenn der Instanzname mit ``demo_`` anfängt, werden
     automatisch Beispieldaten generiert. Eine solche Instanz ist
     für die Produktion ungeeignet.

   - Unbedingt eine noch nicht verwendete Port-Nummer für
     die neue Instanz vergeben!

   - Hinweise auf neue, im Handbuch noch nicht dokumentierte
     Konfigurationsvariablen finden sich in der
     Versionsgeschichte_ bzw. in der Datei::

       /home/ebkus/ebkus_installation/ebkus/VERSIONS_GESCHICHTE.html

.. _Versionsgeschichte: http://ebkus.org/VERSIONS_GESCHICHTE.html
       

2. Das ``configure.py``-Skript ausführen::

     cd /home/ebkus/ebkus_installation/ebkus/
     ./configure.py <Instanzname>

3. Apache neu starten::

     sudo apache2ctl restart

4. Instanz starten::

     ebkusctl <Instanzname> start


Löschen einer EBKuS-Instanz
,,,,,,,,,,,,,,,,,,,,,,,,,,,

Siehe im Handbuch das Kapitel `uninstall.py`_.

.. _`uninstall.py`: http://ebkus.org/doc/EBKuS_Handbuch.html#uninstall-py

1. Instanz anhalten::

     ebkusctl <Instanzname> stop

2. ``uninstall.py``-Skript ausführen::

     cd /home/ebkus/ebkus_installation/ebkus/
     ./uninstall.py .. <Instanzname>

3. Mit einem Texteditor die gelöschte Instanz aus der
   Konfigurationsdatei entfernen::

     cd /home/ebkus/ebkus_installation/ebkus/
     nano ebkus.conf

4. Apache neu starten::

     sudo apache2ctl restart


Datenbank Passworte
,,,,,,,,,,,,,,,,,,,


Die Datenbank-Passworte für die EBKuS-Instanzen stehen in der
Konfigurationsdatei ``ebkus.conf``. Der Datenbank-Benutzer
``root`` hat kein Passwort. Ein Sicherheitsrisiko stellt das
nicht dar, da die Datenbank so konfiguriert ist, dass sie nur
lokal von der EBKuS-VM aus angesprochen werden kann.

Direkter shell-Zugriff auf die Datenbank::

  mysql -uroot


Backups
,,,,,,,

Zusätzlich zu dem im Handbuchkapitel Datensicherung_
beschriebenen Verfahren gibt es das Skript ``ebkusdump``, das
z.B. so aufgerufen werden kann::

  ebkusdump all /home/ebkus/backups

.. _Datensicherung: http://ebkus.org/doc/EBKuS_Handbuch.html#datensicherung

Damit wird für jede Instanz eine Datensicherung in das angegebene
Backup-Verzeichnis geschrieben. Weitere Aufrufmöglichkeiten::

  ebkusdump help
  ebkusdump demo_berlin /home/ebkus

Wie im Handbuchkapitel Datensicherung_ beschrieben, kann man
einen Cron-Job einrichten, der täglich automatisch ein Backup für
alle Instanzen in das Backup-Verzeichnis durchführt. Im
``crontab`` für den Benutzer EBKuS stehen bereits die Zeilen::

  # Jeden Tag 11:31h ausfuehren
  #31 11 * * * $HOME/bin/ebkusdump all $HOME/backups &> /dev/null

Wenn man von der letzten Zeile das Kommentarzeichen entfernt,
wird täglich 11:31 eine Sicherung aller Instanzen durchgeführt.

Crontab ansehen/verändern::

  crontab -l
  crontab -e

Wenn ein solches automatische Backup eingerichtet wird, ist
natürlich dafür zu sorgen, dass die Backups auf ein physisch
getrenntes Medium kopiert werden, was allerdings auch
automatisiert werden könnte. 

Weiterhin müssen im
Backup-Verzeichnis alte Backups regelmäßig gelöscht werden, damit
der Festplattenbedarf nicht ständig wächst. Das Verzeichnis
``/home/ebkus/backups`` ist nicht in ``logrotate``-Verfahren
eingebunden! 

