# coding: latin-1
# Achtung: zu publizierende Funktionen haben nicht immer
# einen __doc__ string. Ich habe cgi_module_publisher.py (Zeile 803
# entsprechend modifiziert.

from ebkus import Version
from ebkus.db import sql
from ebkus.db import dbapp
from ebkus.config import config
import logging

class EBKuS:
    """Eine Instanz dieser Klasse bildet den Ausgangspunkt für Bobos
    Suche nach dem zu publizierendem Objekt.
    http://localhost/efb/ebs/klkarte?akid=22
    Gefunden wird entweder
    - eine Methode dieser Klasse
    - ein Funktionsobjekt über __getitem__
    """
    def __init__(self):
        self.functions = getFunctionsToBePublished()
        self.classes = getClassesToBePublished()
        logging.info("EBKuS Version %s", Version)
        logging.info("EBKuS-Konfigurationsdatei: %s", config.ebkus_conf)
        if config.instance_conf:
            logging.info("Instanz-Konfigurationsdatei: %s", config.instance_conf)
        logging.debug("Aktuelle Konfiguration:\n%s>>>>\n%s\n<<<<%s", '-'*50,
                      config.dump(), '-'*50)
        try:
            sql.opendb()
        except:
            # geloggt wird in ebkus.dbadapter.connect
            # Der Start des Servers sollte aber hier
            # nicht scheitern, die Datenbank könnt ja
            # später wieder hochkommen.
            pass
        
        
    def __getitem__(self, name):
        """Das hier aufgrund des Names gefundene Funktions-Objekt
        gelangt zu dem Publisher, des es aufruft und das Ergebnis an
        den Klienten zurückgibt."""
        try:
            klass = getattr(self.classes, name)
            object = klass()
            object.ebkus = self
            res = object.process
            return res
        except:
            pass
        return getattr(self.functions, name)
        
    def dispatch(self, name, REQUEST, RESPONSE):
        function = self[name]
        return function(REQUEST, RESPONSE)
        
        # Beispiele
        
        ##   def xakteneu(self, REQUEST, RESPONSE):
        ##     "publish"
        ##     import Cakteneu
        ##     obj = Cakteneu.akteneu()
        ##     return obj.process(REQUEST, RESPONSE)
        
        ##   def xmenu(self, REQUEST, RESPONSE):
        ##     "publish"
        ##     import menu
        ##     return menu.menu(REQUEST, RESPONSE)
        
        ##   def test(self, REQUEST, RESPONSE):
        ##     "publish"
        ##     return "the test result" + str(REQUEST.form)
        
    def index_html(self, REQUEST, RESPONSE):
        return "Die Default Seite"
        
def makeObject(dict):
    class p: pass
    object = p()
    object.__dict__.update(dict)
    return object
    
def getClassesToBePublished():
    """publish"""
    from ebkus.html.menu import menu
    from ebkus.html.klientenkarte import klkarte
    from ebkus.html.gruppenkarte import gruppenkarte
    from ebkus.html.akte import akteneu, waufnneu, updakte, updfall, zda, zdar, rmakten, rmakten2
    from ebkus.html.anmeldung import anmneu, updanm,viewanm
    from ebkus.html.bezugsperson import persneu, updpers,viewpers
    from ebkus.html.einrichtungskontakt import einrneu, updeinr
    from ebkus.html.leistung import leistneu, updleist
    from ebkus.html.zustaendigkeit import zustneu, updzust
    # updfs wird auch als updfsform importiert weil es einen Nameclash zwischen
    # der Funktion ebupd.updfs und der Klasse updfs gibt. klkarte.py ist verzockt.
    from ebkus.html.fachstatistik import fsneu, updfs, updfsausw, updfs as updfsform
    from ebkus.html.jghstatistik import jghneu, updjgh, updjghausw, updjgh as updjghform
    from ebkus.html.aktenvorblatt import vorblatt
    from ebkus.html.dokumentenkarte import dokkarte
    from ebkus.html.dokument import vermneu, updverm, updvermausw, upload, updgrverm, rmdok
    from ebkus.html.viewdokument import dokview, dokview2, print_pdf, printgr_pdf, suchetxt
    from ebkus.html.gruppe import menugruppe, gruppeneu, updgruppe, gruppeteilnausw, \
         gruppeteiln, updteiln, rmteiln
    from ebkus.html.abfragen import formabfr2, \
         abfr1, abfr2, formabfr3, abfr3, formabfr4, abfr4, formabfr5, abfr5, \
         jghabfr, jghergebnis, fsabfr, fsergebnis, formabfr6, \
         formabfr6a, formabfr6b, abfr6b, abfr6a, fsabfr_plraum, fsergebnis_plraum, \
         formabfr8, formabfr8a, formabfr9, formabfr9a, formabfr10, formabfr10a, \
         formabfr11, formabfr11a, formabfr12a, formabfr12, formabfr13, \
         formabfr13a, formabfr14, formabfr14a
    from ebkus.html.datenaustausch import formabfrjghexport, jghexportfeedback, jghexportlist, \
         formabfrdbexport, stellenabgleich
    from ebkus.html.mitarbeiter import mitausw, mitneu, updmit
    from ebkus.html.code import codelist, codetab, codeneu, updcode
    from ebkus.html.administration import admin, feedback, admin_protocol
    # msg neue klassen
    from ebkus.html.login import login, logout
    from ebkus.html.password import pwchange, pw_make_change
    from ebkus.html.menu_protocol import menu_protocol
    from ebkus.html.wordexp import wordexport
    from ebkus.html.protokoll_login import login_formular
    from ebkus.html.protokoll_login import check_protokoll_login
    from ebkus.html.ebkushilfe import ebkus_help_document, ebkus_help_tree, ebkus_help
    from ebkus.html.strkat import strkat
    from ebkus.html.statistik_ergebnis import auszergebnis
    return makeObject(locals())
    
    
def getFunctionsToBePublished():
    """Alle Funktionen, die hier im lokalen Namesraum sichtbar sind,
    werden von Bobo publiziert.
    Die Funktion sollte etwas zurückliefern, mit dem Bobo etwas anfangen
    kann:
    - einen String (HTML oder Text)
    - ein Objekt mit einer asHTML() Methode
    - ansonstent wird das Ergebnis der repr() Funktion genommen
    
    """
    #  Alle bisherigen Funktionen sind jetzt Klassen von
    #  getClassesToBePublished().
    
    #  Beispiel:
    #  from menu import menu
    
    return makeObject(locals())
    

# wird vom pcgi_publisher ab und zu zwischen zwei Requests
# aufgerufen, so dass keine threads benoetigt werden.
def clean_up():
    # damit der cache auch mal geleert wird :-)
    logging.info("Clean-up. Cache size: %s", len(dbapp._cache.data))
    dbapp.cache_clear_if_gt(50000)

    
    
    
    
    
    
    
    
    
    
    
    
    
