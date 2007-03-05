# coding: latin-1

"""Module für die Administration und Feedback"""


import string
import os
import time
import Cookie
import re
import rotor

from ebkus.app import Request
from ebkus.app import ebupd
from ebkus.app.ebapi import Akte, Fachstatistik, Jugendhilfestatistik, Code, Mitarbeiter, Kategorie
from ebkus.app.ebapi import ProtokollList, TabellenID, Code
from ebkus.app_surface.standard_templates import *
from ebkus.config import config
from ebkus.app_surface.protokoll_templates import datei_t
from ebkus.app.protocol import set_protocol_limit, archive_sql_protocol

class admin(Request.Request):
    """Für Admineinträge in der DB."""
    
    permissions = Request.ADMIN_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        file = self.form.get('file')
        
        if not file or file == 'admin':
            self.last_error_message = "Keine Dateneingabe erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)

        # Bei removeakten eine Meldung über die Zahl der gelöschten Akten/Gruppen
        # ausgeben.
        if file == 'removeakten':
            akten_geloescht, gruppen_geloescht = ebupd.removeakten(self.form)
            meldung = {'titel':'&Auml;nderung durchgef&uuml;hrt!',
                       'legende':'Hinweis','url':'menu',
                       'zeile1':'Es wurden %s Akte(n) und %s Gruppe(n) gel&ouml;scht.'
                       % (akten_geloescht, gruppen_geloescht),
                       'zeile2':'Sie werden zum Hauptmen&uuml; weitergeleitet.'}
            return meldung_weiterleitung_t % meldung
            
        if self.einfuege_oder_update_operationen.get(file):
            einfuegen = self.einfuegen_oder_update(file)
            return self.admin_display()
            
        return self.ebkus.dispatch(file, REQUEST, RESPONSE)
        
    einfuege_oder_update_operationen = {
      'miteinf' : ('mitid', Mitarbeiter),
      'updmit' : ('mitid', Mitarbeiter),
      'codeeinf' : ('codeid', Code),
      'updcode' : ('codeid', Code),
      'removeakten' : ('akid', Akte),
      }
    
    def einfuegen_oder_update(self, file):
        function = getattr(ebupd, file)
        function(self.form)
        return ''
        
    def admin_display(self):
        """Feedback"""
        
        # Liste der Templates als String
        res = []
        meldung = {'titel':'&Auml;nderung durchgef&uuml;hrt!',
                   'legende':'Hinweis','url':'menu',
                   'zeile1':'Die &Auml;nderungen wurden durchgef&uuml;hrt!',
                   'zeile2':'Sie werden zum Hauptmen&uuml; weitergeleitet.'}
        res.append(meldung_weiterleitung_t % meldung)
        return string.join(res, '')
        
        
        
class feedback(Request.Request):
    """Für Einfügen der Statistik ohne Fallnummer."""
    
    permissions = Request.STAT_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        file = self.form.get('file')
        
        if not file or file == 'feedback':
            self.last_error_message = "Keine Dateneingabe erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
            
        if self.einfuege_oder_update_operationen.get(file):
            einfuegen = self.einfuegen_oder_update(file)
            return self.feedback_display()
            
        return self.ebkus.dispatch(file, REQUEST, RESPONSE)
        
    einfuege_oder_update_operationen = {
      'fseinf' : ('fsid', Fachstatistik),
      'fseinf' : ('fsid', Fachstatistik),
      'jgheinf' : ('jghid', Jugendhilfestatistik),
      'jgheinf' : ('jghid', Jugendhilfestatistik),
      }
    
    def einfuegen_oder_update(self, file):
        function = getattr(ebupd, file)
        function(self.form)
        return ''
        
    def feedback_display(self):
        """Feedback"""
        res = []
        meldung = {'titel':'&Auml;nderung durchgef&uuml;hrt!',
                   'legende':'Hinweis','url':'menu',
                   'zeile1':'Die &Auml;nderungen wurden durchgef&uuml;hrt!',
                   'zeile2':'Sie werden zum Hauptmen&uuml; weitergeleitet.'}
        res.append(meldung_weiterleitung_t % meldung)
        return string.join(res, '')
        
        
class admin_protocol(Request.Request):

    permissions = Request.ADMIN_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        res = []
        auswahl = self.form.get('auswahl')
        grenze = self.form.get('grenze')
        
        if auswahl == 'archiv':
            archive_sql_protocol(self.user)
            meldung = {'titel':'&Auml;nderung durchgef&uuml;hrt!',
                      'legende':'Hinweis','url':'menu',
                      'zeile1':'Die Protokolltabelle wurde erfolgreich archiviert!',
                      'zeile2':'Sie werden zum Hauptmen&uuml; weitergeleitet.'}
            res.append(meldung_weiterleitung_t % meldung)
                
        if auswahl == 'pgrenze':
            set_protocol_limit(grenze)
            meldung = {'titel':'&Auml;nderung durchgef&uuml;hrt!',
                      'legende':'Hinweis','url':'menu',
                      'zeile1':'Die Protokollgrenze wurde auf %s gesetzt!' % grenze,
                      'zeile2':''}
            res.append(meldung_weiterleitung_t % meldung)
                
        if auswahl != 'pgrenze' and auswahl != 'archiv':
            meldung = {'titel':'Keine &Auml;nderung durchgef&uuml;hrt!',
                     'legende':'Hinweis',
                     'zeile1':'Es wurde keine Men&uuml;auswahl get&auml;tigt!',
                     'zeile2':''}
            res.append(meldung_t % meldung)
        return string.join(res, '')
        
##     def protokol_archivierung(self):
##         try:
##          # falls im adminformular archivieren/löschen gedrückt wurde kommt man in
##          # für Datumskonvertierung
##             tmp_yek = "2001.12.31"
##             # diesen abschnitt. hier wird zu erst in eine datei archiviert, dann gelöscht
##             # zeit generieren und fileobjekt erstellen.
##             local_time_insec = time.time()
##             local_time_tupel = time.localtime(local_time_insec)
##             zeitstempel = time.strftime("%d%m%y%H%M%S", local_time_tupel)
##             zeitstempel2 =time.strftime("%d.%m.%y um %H:%M:%S", local_time_tupel)
##             datei = ""
##             pfad = os.path.join(config.PROTOCOL_DIR, zeitstempel + ".txt")
##             #if os.exists(PROTOCOL_DIR) != true:
##             #mkdir(PROTOCOL_DIR)
##             fdatei = open(pfad, "wb")
##             # jede zeile aus der protokolltabelle wird in die datei geschrieben
##             protokolleintraege = ProtokollList(where = '')
##             protokolleintraege.sort('nr')
##             rot = rotor.newrotor(tmp_yek)
##             for p in protokolleintraege:
##                 fdatei.write(rot.encryptmore(datei_t % p))
##                 fdatei.write(rot.encryptmore('<br>'))
##             fdatei.write(rot.encryptmore("<br>****************************<br>Die Protokolltabellen wurden am %s von %s geloescht und in die Datei %s archiviert.<br>****************************<br>" % (zeitstempel2, self.user, pfad)))
##             fdatei.close()
##             # Maxist in tabid für protokolltabelle wird gesetzt
##             prottabid = TabellenID(table_name = 'protokoll')
##             prottabid2 = TabellenID()
##             prottabid2['maxist'] = 0
##             prottabid.update(prottabid2)
##             # protokolltabelle wird gelöscht
##             protokolleintraege2 = ProtokollList(where = '')
##             protokolleintraege2.deleteall()
##         except:
##          #return 1
##             raise
##         return 0
        
##     def protokol_grenze(self, grenze):
##         try:
##         # falls im formular füllgrenze setzten gedrückt wurde kommt man in
##         # diesen abschnitt. hier wird die füllgrenze neu gesetzt
##             prottabid = TabellenID(table_name = 'protokoll')
##             prottabid2 = TabellenID()
##             prottabid2['maxid'] = grenze
##             prottabid.update(prottabid2)
##         except:
##          #return 1
##             raise
##         return 0
        
        
        
        
        
