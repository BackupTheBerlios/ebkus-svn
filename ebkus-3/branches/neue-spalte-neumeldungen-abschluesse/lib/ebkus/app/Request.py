# coding: latin-1

"""Allgemeine Klasse für den Request."""
import sys, os, logging

from ebkus.app import ebapi
from ebkus.config import config
from ebkus.app.session import get_session, create_session
from ebkus.app_surface.standard_templates import *
from ebkus.db.sql import opendb, SQLError
from ebkus.db.dbadapter import DatabaseError
from ebkus.db.dbapp import DBAppError
from ebkus.app.ebapi import EBUpdateError, EBUpdateDataError

# Benutzerrechte für inhaltliche Teile (Dateien) des Programms.
# Neue Einträge in der Kategorie 'Benutzerrechte' müssen hier
# aufenommen werden, damit sie wirksam sind.
# (STAT ist die Abkürzung für Statistik, ABFR für Abfragen)
# VERM für Vermerk, RM für REMOVE.

ALL = 'admin','verw','bearb','protokol'
ADMIN_PERM = 'admin',
UPDATE_PERM = 'verw','bearb',
CODE_PERM = 'admin','verw','bearb',
ABFR_PERM = 'verw','bearb',
STATABFR_PERM = 'verw','bearb',
STAT_PERM = 'verw','bearb',
KLKARTE_PERM = 'verw','bearb',
MENU_PERM = 'admin','verw','bearb','protokol'
VERM_PERM = 'bearb',            # vermerk_permission
NOTIZ_PERM = 'bearb',
DOK_PERM = 'bearb',
DOKVIEW_PERM = 'bearb',
RMDOK_PERM = 'bearb',
RMAKTEN_PERM = 'admin',
GRUPPENKARTE_PERM = 'bearb',
MENUGRUPPE_PERM = 'bearb',
GRUPPETEILN_PERM = 'bearb',
GRUPPENEU_PERM = 'bearb',
RMTEILN_PERM = 'bearb',
PROTOCOL_MENU = 'protokol',        #brehmea(msg)
CHECK_PROTOKOLL_LOGIN = 'protokol'


# globale Variable, wird nur für SQL-Protokollieren gebraucht (protocol.py)
_current_request = None
def getRequest():
    global _current_request
    return _current_request


class NichtIdentifiziert(Exception):
    pass
class KeineZugriffsberechtigung(Exception):
    pass

class Request(object):
    def process(self, REQUEST, RESPONSE):
        global _current_request
        try:
            # Dieser Server ist single-threaded. Es gibt also zu jedem
            # Zeitpunkt nur einen einzigen Reqest, der hier global über
            # getRequest() zur Verfügung steht.
            # Der Grund für diesen Hack besteht darin, dass beim SQL-Protokollieren
            # (DBAdapter.query()) user und ip benötigt wird.
            # Eine bessere Lösung setzte eine umfangreiche Umstrukturierung voraus,
            # die man vornehmen müsste, wenn man multi-threaded arbeiten wollte.
            _current_request = self
            self.REQUEST = REQUEST
            self.RESPONSE = RESPONSE
            self.ip = REQUEST.environ.get('REMOTE_ADDR')
            # wenn etwas protokolliert wird bevor der Benutzer bekannt ist
            self.user = 'unbekannt' 
            try:
                self.form = self.REQUEST.form
                opendb()
                self.checkAuth()
                return self.processForm(REQUEST, RESPONSE)
            except NichtIdentifiziert:
                return self.nichtIdentifiziert(REQUEST, RESPONSE)
            except KeineZugriffsberechtigung:
                return self.keineZugriffsberechtigung(REQUEST, RESPONSE)
            except (DatabaseError, DBAppError, SQLError), e:
                # ist nie von Anwender zu verantworten, also ein interner Fehler
                t = sys.exc_info()[0]
                logging.exception("Datenbankfehler: %s: %s", t, e)
                self.last_error_message = "Datenbankfehler: %s: %s" % (t, e)
                RESPONSE.setStatus('InternalError')
                return self.EBKuSError(REQUEST, RESPONSE)
            except EBUpdateDataError, e:
                # in der Regel ausgelöst durch die Eingaben des Anwenders
                logging.debug("Eingabefehler: %s", e)
                self.last_error_message = str(e)
                return self.EBKuSError(REQUEST, RESPONSE)
            except EBUpdateError, e:
                # schwerer Fehler, der geloggt werden soll
                t = sys.exc_info()[0]
                logging.exception("%s: %s", t, e)
                self.last_error_message = "%s: %s" % (t, e)
                RESPONSE.setStatus('InternalError')
                return self.EBKuSError(REQUEST, RESPONSE)
            except Exception, e:
                # ist nie (wenn doch, ist es ein Bug) vom Anwender zu verantworten,
                # also ein interner Fehler
                t = sys.exc_info()[0]
                logging.exception("Interner Fehler: %s: %s", t, e)
                self.last_error_message = "%s: %s" % (t, e)
                RESPONSE.setStatus('InternalError')
                return self.EBKuSError(REQUEST, RESPONSE)
        finally:
            _current_request = None

    def checkAuth(self):
        """Holt Benutzername aus der Session, prüft Benutzerberechtigung.
        Setzt self.user, self.mitarbeiter, self.stelle"""
        # auto_user = 'atms' # so ist das Entwickeln einfacher
        auto_user = ''   # so sollte es im Betrieb sein
        if auto_user:
            self.session = get_session(self.REQUEST, self.RESPONSE)
            if self.session:
                self.user = self.session.user
            else:
                self.session = create_session(auto_user, self.RESPONSE)
                self.user = self.session.user
                
            self.mitarbeiter = ebapi.Mitarbeiter(ben=self.user,
                                                 stat=ebapi.cc('status', 'i'))
            self.stelle = ebapi.Code(self.mitarbeiter['stz'])
            if self.mitarbeiter['benr__code'] not in self.permissions:
                raise KeineZugriffsberechtigung()
            return

        self.session = get_session(self.REQUEST, self.RESPONSE)
        if self.session:
            self.user = self.session.user
        else:
            raise NichtIdentifiziert()
        self.mitarbeiter = ebapi.Mitarbeiter(ben=self.user,
                                             stat=ebapi.cc('status', 'i'))
        self.stelle = ebapi.Code(self.mitarbeiter['stz'])
        if self.mitarbeiter['benr__code'] not in self.permissions:
            raise KeineZugriffsberechtigung()

    def nichtIdentifiziert(self, REQUEST, RESPONSE):
        meldung = {'titel': 'Zugriff verweigert!',
                   'legende': 'Zugriff Verweigert!',
                   'url':'login',
                   'zeile1': 'Sie konnten nicht eindeutig als angemeldeter Benutzer identifiziert werden.',
                   'zeile2': 'Hinweis:<br> EBKuS meldet Sie nach ' + str(config.SESSION_TIME) + ' Min. ' +
                   'automatisch vom System ab!'}
        return (meldung_weiterleitung_t % meldung)

    def keineZugriffsberechtigung(self, REQUEST, RESPONSE):
        meldung = {'titel': 'Zugriff verweigert!',
                   'legende': 'Zugriff Verweigert!',
                   'url':'menu',
                   'zeile1': 'Sie haben keine Zugriffsberechtigung.',
                   'zeile2': 'Hinweis:<br> Sie werden in das Hauptmen&uuml weitergeleitet!'}
        return (meldung_weiterleitung_t % meldung)


    def EBKuSError(self, REQUEST, RESPONSE):
        RESPONSE.setHeader('content-type', 'text/html')
        meldung = {'titel': 'Es ist ein Fehler aufgetreten!',
                  'legende': 'Fehlerbeschreibung',
                  'zeile1': '%s' % str(self.last_error_message),
                  'zeile2': ''}
        return (meldung_t % meldung)
            
            
    def getMitarbeiterliste(self):
        stz_id = self.stelle['id']
        ml = ebapi.MitarbeiterList(
          where = 'stat = %s and benr = %s and stz = %s'
          % (ebapi.cc('status', 'i'), ebapi.cc('benr', 'bearb'), stz_id),
          order = 'na')
        return ml
        
        
        
        
        
        
        
        
