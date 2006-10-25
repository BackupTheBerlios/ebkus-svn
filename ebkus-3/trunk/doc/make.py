#!/usr/bin/env python
# coding: latin-1

"""Bringt die EBKuS Dokumentation auf den neuesten Stand.

Setzt voraus, dass das Paket ``docutils`` installiert ist,
(rst2html.py, rst2latex.py).
Quelle: http://docutils.sourceforge.net/

Dieses Paket definiert eine Syntax für Textdateien, die dann
automatische nach HTML und Latex/PDF übersetzt werden können.

Quellen:
  make.py (dieses Skript)
  docutils.conf                  -- 
  manual.css
  manual.sty
  manual.txt
  einleitung.txt
  anwendungsbeschreibung.txt
  bedienungsanleitung.txt
  administration.txt
  installation.txt

Targets:
  EBKuS_Handbuch.html
  manual.tex --> EBKuS_Handbuch.pdf


In erster Näherung:

Wenn es eine Quelle gibt, die neuer als eine Target ist, wird alles
neu gemacht.

Kann man später vielleicht verfeinern.
"""

import os, sys
from os.path import join, split, dirname, exists, isdir, isfile, normpath, normcase, abspath
from urllib import urlretrieve
assert sys.version_info >= (2,3), "Es wird Python 2.3 oder höher benötigt"

#sources = ['manual.txt', 'docutils.conf', 'manual.css', 'manual.sty', 'make.py']
kapitel = ['einleitung.txt', 'anwendungsbeschreibung.txt', 'bedienungsanleitung.txt',
           'administration.txt', 'installation.txt']
latex_sources = ['manual.txt', 'docutils.conf', 'manual.sty', 'make.py'] + kapitel
html_sources = ['manual.txt', 'docutils.conf', 'manual.css', 'make.py'] + kapitel

# Navigationstipp und Kapitelnumerierung nur bei HTML
html_spezifisch = {'NAVIG': """
[Navigationstipp: Inhaltsverzeichnis und Kapitelüberschriften
sind wechselseitig verlinkt. Ein Klick auf eine Kapitelüberschrift führt
zurück zum Inhaltsverzeichnis!] 
""",

                   'SECNUM': ".. sectnum::"
                   }
latex_spezifisch = {'NAVIG': '', 'SECNUM': ''
                   }

def pre_process(filein, fileout, dict):
    """In filename Ersetzungen gemäß dict vornehmen"""
    f = open(filein, "rU")  # U ist Universal Newline
    t = f.read()
    f.close()
    t = t % dict
    open(fileout, 'w').write(t)
    
def mtime(path):
    try:
        return os.path.getmtime(path)
    except:
        # gibs nich, gaanz alt
        return 0
        
def is_newer(file1, file2):
    """Ist file1 nach file2 modifiziert worden? (mtime)"""
    return mtime(file1) > mtime(file2)

def newest(*paths):
    return max([mtime(p) for p in paths])

def post_process_latex(filename):
    """Figure Optionen ändern"""
    f = open(filename, "rU")  # U ist Universal Newline
    t = f.read()
    f.close()
    t = t.replace(r"\begin{figure}[htbp]\begin{center}",
                  r"\begin{figure}[H]\begin{center}")
    open(filename, 'w').write(t)

def run_cmd(cmd):
    print cmd
    res = os.system(cmd)
    if res != 0:
        msg = '  Fehlgeschlagen: %s' % cmd
        #print msg
        raise Exception(msg)

def usage():
    msg ="""\
make.py [-h, --help] [html|latex|pdf]

   EBKuS-Dokumentation im HTML-Format oder als PDF erstellen.

   Ohne Argumente wird bei Bedarf die gesamte Dokumentation neu
   erstellt. (Bedarf besteht, wenn in einer der Quelldateien sich
   etwas geändert hat.)

   Wenn html, latex oder pdf angegeben wird, wird nur der betreffende
   Teil bei Bedarf generiert.

   Setzt voraus, dass das Paket ``docutils`` installiert ist,
   (rst2html.py, rst2latex.py).
   Quelle: http://docutils.sourceforge.net/

   Falls ``docutils`` nicht installiert ist, wird das Handbuch im HTML- und im
   PDF-Format von http://ebkus.berlios.de/ebkus-3.2/ heruntergeladen.
"""
    print msg

def latex_uptodate():
    if (isfile('manual.tex') and
        newest(*latex_sources) <= mtime('manual.tex')):
        return True
    return False

def pdf_uptodate():
    if (isfile('EBKuS_Handbuch.pdf') and
        newest(*latex_sources) <= mtime('EBKuS_Handbuch.pdf')):
        return True
    return False
    
def html_uptodate():
    if (isfile('EBKuS_Handbuch.html') and
        newest(*html_sources) <= mtime('EBKuS_Handbuch.html')):
        return True
    return False

def make_latex():
    if not latex_uptodate():
        pre_process('manual.txt', 'manual_for_latex.txt', latex_spezifisch)
        run_cmd('rst2latex.py manual_for_latex.txt manual.tex')
        print "postprocessing 'manual.tex'"
        post_process_latex('manual.tex')
    

if __name__ == '__main__':
    os.chdir(dirname(abspath(sys.argv[0])))
    pdf = html = latex = False
    args = sys.argv
    if len(args) > 1:
        if 'pdf' in args:
            pdf = True
        if 'html' in args:
            html = True
        if 'latex' in args:
            latex = True
        if '-h' in args or '--help' in args:
            usage()
            sys.exit(0)
        if not(pdf or html or latex):
            usage()
            sys.exit(1)
    else:
        pdf = html = latex = True
        if pdf_uptodate():
            # im default-Fall kümmern wir uns um Latex nicht, wenn pdf ok ist.
            latex = False

    if os.system('rst2html.py --version') != 0:
        # keine docutils, downloaden
        print "docutils zum Generieren des Handbuchs sind nicht installiert"
        url_dir = 'http://ebkus.berlios.de/ebkus-3.2/'
        target = 'EBKuS_Handbuch.html'
        if html:
            if isfile(target):
                print "  %s bereits vorhanden" % target
            else:
                url = "%s/%s" % (url_dir, target)
                print '  herunterladen: %s  ... ' % url
                urlretrieve(url, target)
                print '    erfolgreich heruntergeladen'
        target = 'EBKuS_Handbuch.pdf'
        if pdf:
            if isfile(target):
                print "  %s bereits vorhanden" % target
            else:
                url = "%s/%s" % (url_dir, target)
                print '  herunterladen: %s  ... ' % url
                urlretrieve(url, target)
                print '    erfolgreich heruntergeladen'
        sys.exit(0)

    try:
        if html:
            if html_uptodate():
                print "html uptodate"
            else:
                pre_process('manual.txt', 'manual_for_html.txt', html_spezifisch)
                run_cmd('rst2html.py manual_for_html.txt EBKuS_Handbuch.html')
        if latex:
            if latex_uptodate():
                print 'latex uptodate'
            else:
                make_latex()
        if pdf:
            if pdf_uptodate():
                print 'pdf uptodate'
            else:
                make_latex()
                run_cmd('pdflatex manual.tex')
                # zweimal wg. Inhaltsverzeichnis
                run_cmd('pdflatex manual.tex')
                os.rename('manual.pdf', 'EBKuS_Handbuch.pdf')
    except Exception, e:
        print e
        sys.exit(1)
    sys.exit(0)

