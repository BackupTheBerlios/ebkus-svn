# coding: latin-1

"""Module für den Im- und Export aus der Datenbank."""

import time, os


from ebkus.app import Request
from ebkus.config import config
from ebkus.app.ebapi import Code, JugendhilfestatistikList, today, cc, EE, Fall
from ebkus.app_surface.standard_templates import *
from ebkus.app_surface.datenaustausch_templates import *
from ebkus.app.jghexport import jghexport, get_export_datei_name
from ebkus.db.sql import SQL

EXPORT_DIR = os.path.join('daten', 'export')
EXPORT_DIR_URL = 'daten/export'

class formabfrjghexport(Request.Request):
    """Auswahlformular für den Export der Jugendhilfestatistik."""
    
    permissions = Request.ADMIN_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        bestaetigung = {'titel': "Bundesjugendhilfestatistik: Exportdatei erstellen",
                        'legende':'Bundesjugendhilfestatistik: Exportdatei erstellen',
                        'zeile':'Bitte das Exportjahr eingeben und mit Ok best&auml;tigen!',
                        'jahr' : '%s' % (today().year),
                        'dest_url':'menu'}
        return bestaetigung_t % bestaetigung
        
        
class jghexportfeedback(Request.Request):
    """Aufruf zum Export der Jugendhilfestatistik und Feedback."""
    permissions = Request.ADMIN_PERM
    def _keine_statistik_liste(self, jahr):
        """Liste aller Fälle, die in jahr oder davor begonnen haben,
        für die keine Jugendhilfestatistik existiert.

        Wir brauchen nur offene Fälle zu betrachten, da alle geschlossenen
        Fälle eine Statistik haben müssen.
        """
        # zustaendigkeit, mitarbeiter nur zum sortieren
        sql = """
SELECT fall.id
FROM fall JOIN zustaendigkeit JOIN mitarbeiter
LEFT JOIN jghstat07 ON fall.id=jghstat07.fall_id
LEFT JOIN jghstat on fall.id=jghstat.fall_id
WHERE jghstat07.fall_id IS NULL AND
      jghstat.fall_id IS NULL AND
      fall.bgy<=%d AND
      fall.zday=0 AND
      zustaendigkeit.fall_id=fall.id AND
      mitarbeiter.id=zustaendigkeit.mit_id
ORDER BY mitarbeiter.na, fall.bgy, fall.bgm""" % jahr
        q = SQL(sql)
        faelle_ids_ohne = q.execute()
        res = []
        res.append(head_normal_ohne_help_t % "Fälle ohne Bundesjugendhilfestatistik")
        res.append(thkeinestatistik_t)
        for fall_id_t in faelle_ids_ohne:
            fall = Fall(fall_id_t[0])
            res.append(keinestatistikliste_t % fall)
        res.append(jghexportliste_ende_t)
        return ''.join(res)
        
    def processForm(self, REQUEST, RESPONSE):
        jahr = self.form.get('jahr')
        if jahr and jahr.isdigit():
            jahr = int(jahr)
        else:
            self.last_error_message = "Kein gültiges Jahr"
            return self.EBKuSError(REQUEST, RESPONSE)
        
        if  self.form.get('welche') == 'keine':
            return self._keine_statistik_liste(jahr)
        andauernd = self.form.get('welche') == 'andauernd'
        if andauernd and jahr < 2007:
            self.last_error_message = \
               'Bundesstatistik für andauernde Fälle erst ab 2007 möglich'
            return self.EBKuSError(REQUEST, RESPONSE)
        daten_saetze, log_daten_saetze = jghexport(jahr, andauernd)
        if not daten_saetze:
            self.last_error_message = 'Keine Bundesstatistik f&uuml;r %s vorhanden' % jahr
            return self.EBKuSError(REQUEST, RESPONSE)
        try:
            filename = get_export_datei_name(jahr, log=False, andauernd=andauernd) 
            log_filename = get_export_datei_name(jahr, log=True, andauernd=andauernd) 
            path = os.path.join(config.DOCUMENT_ROOT, EXPORT_DIR, filename)
            f = open(path, 'wb')
            f.write(daten_saetze)
            f.close()
            log_path = os.path.join(config.DOCUMENT_ROOT, EXPORT_DIR, log_filename)
            f_log = open(log_path, 'w')
            f_log.write(log_daten_saetze)
            f_log.close()
        except Exception, e:
            raise EE("Fehler beim Exportieren: %s" % str(e) ) 
            
        res = []
        res.append(head_normal_ohne_help_t %("Exportdatei f&uuml;r das Jahr %s" % jahr))

        ausgabe = {
            'jahr' : jahr,
            'jgh_filename' : filename,
            'jgh_url' : 'jghexportlist?file=%s' % filename,
            'jgh_log_filename' : log_filename,
            'jgh_log_url' : 'jghexportlist?file=%s' % log_filename,
            }
        res.append(jghexportfeedback_t % ausgabe)
        return ''.join(res)
        

class jghexportlist(Request.Request):
    """Listet die exportierten Jugendhilfestatistiken.

    Falls ein Parameter file vorhanden ist, wird die entsprechende
    Jugendhilfestatistikdatei direkt zurückgegeben, so dass der Anwender
    sie bei sich abspeichern kann.
    """
    permissions = Request.ADMIN_PERM
    

    def processForm(self, REQUEST, RESPONSE):
        import os
        #print REQUEST
        if self.form.has_key('file'):
            file = self.form.get('file')
            try:
                filename = os.path.join(config.DOCUMENT_ROOT, EXPORT_DIR, file)
                f = open(filename)
                content = f.read()
                f.close()
                self.RESPONSE.setHeader('content-type', 'text/plain')
                self.RESPONSE.setHeader('content-disposition', 'attachment; filename=%s' % file)
                self.RESPONSE.setBody(content)
                #print RESPONSE
                return
            except Exception, e:
                raise EE("Fehler beim Download: %s" % str(e) ) 
        
        dateiliste = os.listdir(os.path.join(config.DOCUMENT_ROOT, EXPORT_DIR) )
        abgeschlossen, andauernd = _ordne_dateinamen(dateiliste)
        
        res = []
        res.append(head_normal_ohne_help_t % "Bundesjugendhilfestatistik: Liste der Exportdateien")
        res.append(thjghexportliste_t)
        for d, l in abgeschlossen:
            res.append(jghexportliste_t % ('jghexportlist?file=%s' % d, d,
                                           'jghexportlist?file=%s' % l, l))
        res.append(jghexportliste_trenner_t)
        for d, l in andauernd:
            res.append(jghexportliste_t % ('jghexportlist?file=%s' % d, d,
                                           'jghexportlist?file=%s' % l, l))
        res.append(jghexportliste_ende_t)
        return ''.join(res)

def _ordne_dateinamen(liste):
    an = [n for n in liste if n.find('andauernd') >= 0 and n.startswith('jgh_')]
    daten = [n for n in an if n.find('log') == -1]
    log = [n for n in an if n.find('log') >= 0]
    daten.sort()
    log.sort()
    andauernd = zip(daten, log)

    ab = [n for n in liste if n.find('andauernd') == -1 and n.startswith('jgh_')]
    daten = [n for n in ab if n.find('log') == -1]
    log = [n for n in ab if n.find('log') >= 0]
    daten.sort()
    log.sort()
    abgeschlossen = zip(daten, log)
    return abgeschlossen, andauernd
        
