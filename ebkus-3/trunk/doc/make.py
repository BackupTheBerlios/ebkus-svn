#!/usr/bin/env python
# coding: latin-1

"""Bringt die EBKuS Dokumentation auf den neuesten Stand.

Setzt voraus, dass das Paket ``docutils`` installiert ist,
(rst2html, rst2latex).
Quelle: http://docutils.sourceforge.net/

Dieses Paket definiert eine Syntax f�r Textdateien, die dann
automatische nach HTML und Latex/PDF �bersetzt werden k�nnen.

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


In erster N�herung:

Wenn es eine Quelle gibt, die neuer als eine Target ist, wird alles
neu gemacht.

Kann man sp�ter vielleicht verfeinern.
"""

import os, sys
from os.path import join, split, dirname, exists, isdir, isfile, normpath, normcase, abspath
from urllib import urlretrieve
assert sys.version_info >= (2,3), "Es wird Python 2.3 oder h�her ben�tigt"

#sources = ['manual.txt', 'docutils.conf', 'manual.css', 'manual.sty', 'make.py']
kapitel = ['einleitung.txt', 'anwendungsbeschreibung.txt', 'bedienungsanleitung.txt',
           'administration.txt', 'installation.txt']
latex_sources = ['manual.txt', 'docutils.conf', 'manual.sty', 'make.py'] + kapitel
html_sources = ['manual.txt', 'docutils.conf', 'manual.css', 'make.py'] + kapitel

# Navigationstipp und Kapitelnumerierung nur bei HTML
html_spezifisch = {'NAVIG': """
[Navigationstipp: Inhaltsverzeichnis und Kapitel�berschriften
sind wechselseitig verlinkt. Ein Klick auf eine Kapitel�berschrift f�hrt
zur�ck zum Inhaltsverzeichnis!] 
""",

                   'SECNUM': ".. sectnum::"
                   }
latex_spezifisch = {'NAVIG': '', 'SECNUM': ''
                   }

def pre_process(filein, fileout, dict):
    """In filename Ersetzungen gem�� dict vornehmen"""
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
    """Figure Optionen �ndern"""
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
make.py [-h, --help, -r, --readme] [html|latex|pdf|clean]

   EBKuS-Dokumentation im HTML-Format oder als PDF erstellen.
   oder mit Option -r, --readme: nur HTML-Versionen der READMEs
   im Distributionsverzeichnis erstellen, nicht das Handbuch)
   
   Ohne Argumente wird bei Bedarf die gesamte Dokumentation neu
   erstellt. (Bedarf besteht, wenn in einer der Quelldateien sich
   etwas ge�ndert hat.)

   Wenn html, latex oder pdf angegeben wird, wird nur der betreffende
   Teil bei Bedarf generiert.

   Setzt voraus, dass das Paket ``docutils`` installiert ist,
   (rst2html, rst2latex).
   Quelle: http://docutils.sourceforge.net/

   Setzt ferner voraus, dass das Kommando pdflatex installiert ist.
   In Suse 10.0 erreicht man das, indem man die Pakete
   tetex und te_latex installiert.
   
   Falls ``docutils`` nicht installiert ist, wird das Handbuch im HTML- und im
   PDF-Format von http://ebkus.berlios.de/ebkus-3.3/ heruntergeladen.
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
        run_cmd('rst2latex manual_for_latex.txt manual.tex')
        print "postprocessing 'manual.tex'"
        post_process_latex('manual.tex')
    

def make_readme():
    "HTML-Versionen der Dokumentation im Distributionsverzeichnis erstellen."
    docs = ('NEU_IN_DIESER_VERSION', 'VERSIONS_GESCHICHTE',)
    for d in docs:
#         os.system("rst2html.py --input-encoding=latin1 --stylesheet-path=manual.css " +
#                   "--config=docutils.conf --initial-header-level=3 ../%s.txt ../%s.html" % (d, d))
        os.system("rst2html --input-encoding=latin1 --stylesheet-path=manual.css " +
                  "--config=docutils.conf --initial-header-level=3 ../%s.txt ../%s.html" % (d, d))

if __name__ == '__main__':
    os.chdir(dirname(abspath(sys.argv[0])))
    pdf = html = latex = clean = False
    args = sys.argv
    if len(args) > 1:
        if 'pdf' in args:
            pdf = True
        if 'html' in args:
            html = True
        if 'latex' in args:
            latex = True
        if 'clean' in args:
            clean = True
        if '-r' in args or '--readme' in args:
            make_readme()
            sys.exit(0)
        if '-h' in args or '--help' in args:
            usage()
            sys.exit(0)
        if not(pdf or html or latex or clean):
            usage()
            sys.exit(1)
    else:
        pdf = html = latex = True
        if pdf_uptodate():
            # im default-Fall k�mmern wir uns um Latex nicht, wenn pdf ok ist.
            latex = False

    if clean:
        pats = ('*~', '*.pyc',
                'manual_for_html.txt',
                'manual_for_latex.txt',
                '*toc', '*log', '*out', '*tex', '*aux')
        from glob import glob
        for p in pats:
            m = glob(p)
            for f in m:
                os.remove(f)
        sys.exit(0)
    
    if os.system('rst2html --version') != 0:
        # keine docutils, downloaden
        print "docutils zum Generieren des Handbuchs sind nicht installiert"
        url_dir = 'http://ebkus.berlios.de/ebkus-3.3/'
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
                run_cmd('rst2html manual_for_html.txt EBKuS_Handbuch.html')
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

