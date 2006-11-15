# coding: latin-1

"""Module für den Im- und Export aus der Datenbank."""

import time, os


from ebkus.app import Request
from ebkus.config import config
from ebkus.app.ebapi import Code, JugendhilfestatistikList, ExportprotokollList, ImportprotokollList, today, cc, getDBSite, EE
from ebkus.app_surface.standard_templates import *
from ebkus.app_surface.datenaustausch_templates import *
from ebkus.app.jghexport import jghexport

EXPORT_DIR = os.path.join('daten', 'export')
EXPORT_DIR_URL = 'daten/export'

class formabfrjghexport(Request.Request):
    """Auswahlformular für den Export der Jugendhilfestatistik."""
    
    permissions = Request.ADMIN_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        mitarbeiterliste = self.getMitarbeiterliste()
        user = self.user
        site = Code(cc('dbsite', '%s' % getDBSite()))
        
        res = []
        bestaetigung = {'titel':("Bundesjugendhilfestatistik: Exportdatei erstellen der %s" % site['name']),
                        'legende':'Best&auml;tigung des Exportvorgangs',
                        'zeile':'Bitte das Exportjahr eingeben und mit Ok best&auml;tigen!',
                        'jahr' : '%s' % (today().year),
                        'dest_url':'menu'}
        res.append(bestaetigung_t %(bestaetigung))
        return ''.join(res)
        
        
class jghexportfeedback(Request.Request):
    """Aufruf zum Export der Jugendhilfestatistik und Feedback."""
    
    permissions = Request.ADMIN_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        import os
        
        mitarbeiterliste = self.getMitarbeiterliste()
        user = self.user
        
        if self.form.has_key('jahr'):
            jahr = self.form.get('jahr')
        else:
            self.last_error_message = "Kein Jahr erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
            
        daten_saetze, log_daten_saetze = jghexport(jahr)
        if not daten_saetze:
            self.last_error_message = 'Keine Bundesstatistik f&uuml;r %s vorhanden' % jahr
            return self.EBKuSError(REQUEST, RESPONSE)
        try:
            filename = 'jgh_%s.txt' % jahr
            path = os.path.join(config.DOCUMENT_ROOT, EXPORT_DIR, filename)
            f = open(path, 'w')
            f.write(daten_saetze)
            f.close()
            log_filename = 'jgh_log_%s.txt' % jahr
            log_path = os.path.join(config.DOCUMENT_ROOT, EXPORT_DIR, log_filename)
            f_log = open(log_path, 'w')
            f_log.write(log_daten_saetze)
            f_log.close()
        except Exception, e:
            raise EE("Fehler beim Exportieren: %s" % str(e) ) 
            
        site = Code(cc('dbsite', '%s' % getDBSite()))
        
        res = []
        res.append(head_normal_ohne_help_t %("Exportdatei der %s" % site['name'] + " f&uuml;r das Jahr %s " % jahr))

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
        if self.form.has_key('file'):
            file = self.form.get('file')
            try:
                filename = os.path.join(config.DOCUMENT_ROOT, EXPORT_DIR, file)
                f = open(filename)
                content = f.read()
                f.close()
                self.RESPONSE.setHeader('content-type', 'text/plain')
                self.RESPONSE.setBody(content)
                return
            except Exception, e:
                raise EE("Fehler beim Download: %s" % str(e) ) 
        
        mitarbeiterliste = self.getMitarbeiterliste()
        user = self.user
        site = Code(cc('dbsite', '%s' % getDBSite()))
        dateiliste = os.listdir(os.path.join(config.DOCUMENT_ROOT, EXPORT_DIR) )
        dateiliste.sort()
        
        res = []
        res.append(head_normal_ohne_help_t %("Bundesjugendhilfestatistik: Liste der Exportdateien der %s" % site['name']))
        res.append(thjghexportliste_t)
        for f in dateiliste:
            if f[0:4] == 'jgh_':
                res.append(jghexportliste_t % ('jghexportlist?file=%s' % f, f))
        res.append(jghexportliste_ende_t)
        return ''.join(res)
        
class formabfrdbexport(Request.Request):
    """Auswahlformular für den Ex- bzw. Import von Daten."""
    
    permissions = Request.ADMIN_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        mitarbeiterliste = self.getMitarbeiterliste()
        user = self.user
        site = Code(cc('dbsite', '%s' % getDBSite() ) )
        
        res = []
        res.append(head_normal_ohne_help_t %('Stellenabgleich: Ex- und Import von Daten in die Datenbank der ' + site['name']))
        res.append(formexport_t)
        return ''.join(res)
        
        
class stellenabgleich(Request.Request):
    """Aufruf der Datei für den Ex- bzw. Import von Daten."""
    
    permissions = Request.ADMIN_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        import os
        mitarbeiterliste = self.getMitarbeiterliste()
        user = self.user
        site = Code(cc('dbsite', '%s' % getDBSite()))
        if self.form.has_key('dbexport'):
            arg = self.form.get('dbexport')
        else:
            self.last_error_message = "Kein Jahr erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
            
        if arg == 'i' or arg == 'e':
            try:
                # TBD: dbexport importieren!
                os.system('python %s/ebkus/app/dbexport.py -%s %s ' % (config.INSTANCE_HOME,
                                                   arg, self.mitarbeiter['ben']))
            except Exception, e:
                raise EE("Fehler beim Exportieren: %s") % str(e)
        exportliste = ExportprotokollList(where = 'id > 0',
                                          order = 'dbsite,zeit desc')
        importliste = ImportprotokollList(where = 'id > 0',
                                          order = 'dbsite,zeit desc')
        
        res = []
        res.append(head_normal_ohne_help_t %("Stellenabgleich: Protokoll zum Ex- und Import von Daten in die Datenbank der %s" % site['name']))
        res.append(thexport_start_t)
        if exportliste:
            res.append(thexport_t % 'Export - Protokolldaten')
            for e in exportliste:
                datum = time.strftime('%d.%m.%y / %H:%M:%S', time.localtime(e['zeit']))
                e['datum'] = datum
                res.append(export_t % e)
                del e['datum']
        if importliste:
            res.append(thexport_t % 'Import - Protokolldaten')
            for i in importliste:
                datum = time.strftime('%d.%m.%y / %H:%M:%S', time.localtime(i['zeit']))
                i['datum'] = datum
                res.append(export_t % i)
                del i['datum']
        res.append(thexport_ende_t)
        return ''.join(res)
        
        
