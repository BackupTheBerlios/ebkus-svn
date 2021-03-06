# coding: latin-1

"""Allgemeine Klasse f�r den Request."""
import sys, os, logging

from ebkus.app import ebapi
from ebkus.config import config
from ebkus.app.session import get_session, create_session
from ebkus.app_surface.standard_templates import *
from ebkus.db.sql import opendb, SQLError
from ebkus.db.dbadapter import DatabaseError
from ebkus.db.dbapp import DBAppError
from ebkus.app.ebapi import EBUpdateError, EBUpdateDataError
import ebkus.html.htmlgen as h


# Benutzerrechte f�r inhaltliche Teile (Dateien) des Programms.
# Neue Eintr�ge in der Kategorie 'Benutzerrechte' m�ssen hier
# aufenommen werden, damit sie wirksam sind.
# (STAT ist die Abk�rzung f�r Statistik, ABFR f�r Abfragen)
# VERM f�r Vermerk, RM f�r REMOVE.

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
GRUPPENKARTE_PERM = 'bearb','verw'
MENUGRUPPE_PERM = 'bearb','verw'
GRUPPETEILN_PERM = 'bearb','verw'
GRUPPENEU_PERM = 'bearb','verw'
RMTEILN_PERM = 'bearb','verw'
PROTOCOL_MENU = 'protokol',        #brehmea(msg)
CHECK_PROTOKOLL_LOGIN = 'protokol'


# globale Variable, wird nur f�r SQL-Protokollieren gebraucht (protocol.py)
_current_request = None
def getRequest():
    global _current_request
    return _current_request

def get_traceback():
    import traceback
    s = "<pre>%s</pre>" % ''.join(traceback.format_exception(*sys.exc_info()))
    return s

class NichtIdentifiziert(Exception):
    pass
class KeineZugriffsberechtigung(Exception):
    pass

class Request(object):
    def process(self, REQUEST, RESPONSE):
        global _current_request
        try:
            # Dieser Server ist single-threaded. Es gibt also zu jedem
            # Zeitpunkt nur einen einzigen Reqest, der hier global �ber
            # getRequest() zur Verf�gung steht.
            # Der Grund f�r diesen Hack besteht darin, dass beim SQL-Protokollieren
            # (DBAdapter.query()) user und ip ben�tigt wird.
            # Eine bessere L�sung setzte eine umfangreiche Umstrukturierung voraus,
            # die man vornehmen m�sste, wenn man multi-threaded arbeiten wollte.
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
                #print 'FORM: ', self.form
                return self.processForm(REQUEST, RESPONSE)
            except NichtIdentifiziert:
                return self.nichtIdentifiziert(REQUEST, RESPONSE)
            except KeineZugriffsberechtigung:
                return self.keineZugriffsberechtigung(REQUEST, RESPONSE)
            except (DatabaseError, DBAppError, SQLError), e:
                # ist nie von Anwender zu verantworten, also ein interner Fehler
                t = sys.exc_info()[0]
                logging.exception("Datenbankfehler: %s: %s", t, e)
                self.last_error_message = "Datenbankfehler: \n%s" % get_traceback()
                RESPONSE.setStatus('InternalError')
                return self.EBKuSInternalError(REQUEST, RESPONSE)
            except EBUpdateDataError, e:
                # in der Regel ausgel�st durch die Eingaben des Anwenders
                logging.debug("Eingabefehler: %s", e)
                self.last_error_message = str(e)
                return self.EBKuSError(REQUEST, RESPONSE)
            except EBUpdateError, e:
                # schwerer Fehler, der geloggt werden soll
                t = sys.exc_info()[0]
                logging.exception("%s: %s", t, e)
                self.last_error_message = get_traceback()
                RESPONSE.setStatus('InternalError')
                return self.EBKuSInternalError(REQUEST, RESPONSE)
            except Exception, e:
                # ist nie (wenn doch, ist es ein Bug) vom Anwender zu verantworten,
                # also ein interner Fehler
                t = sys.exc_info()[0]
                logging.exception("Interner Fehler: %s: %s", t, e)
                self.last_error_message = get_traceback()
                RESPONSE.setStatus('InternalError')
                return self.EBKuSInternalError(REQUEST, RESPONSE)
        finally:
            _current_request = None

    def checkAuth(self):
        """Holt Benutzername aus der Session, pr�ft Benutzerberechtigung.
        Setzt self.user, self.mitarbeiter, self.stelle"""
        auto_user = ''   # so sollte es im Betrieb sein
        #auto_user = 'test' # so ist das Entwickeln einfacher
        #auto_user = 'Admin' # so ist das Entwickeln einfacher
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
        return h.Meldung(
            legend='Zugriff verweigert',
            weiter='login',
            zeilen=('Sie konnten nicht eindeutig als angemeldeter Benutzer identifiziert werden.',
                  'Hinweis:',
                  'EBKuS meldet Sie nach ' + str(config.SESSION_TIME) +
                  ' Minuten ohne Aktivit�t automatisch vom System ab.',
                  'Weiter zum Login ...',
                  ),
            ).display()

    def keineZugriffsberechtigung(self, REQUEST, RESPONSE):
        return h.Meldung(
            legend='Zugriff verweigert',
            weiter='menu',
            zeilen=('Sie haben keine Zugriffsberechtigung.',
                  'Weiter zum  Hauptmen&uuml ...',
                  ),
            ).display()


    def EBKuSError(self, REQUEST, RESPONSE):
        RESPONSE.setHeader('content-type', 'text/html')
        le = str(self.last_error_message)
        close = False
        # schneller Hack: wenn die Fehlermeldung mit 'XXX' beginnt, wird das Fenster
        # geschlossen, anstatt history.back() gemacht.
        # F�r die F�lle, wo ein neues Fenster aufgemacht wurde.
        if le.startswith('XXX'):
            close = True
            le = le[3:]
        return h.Meldung(
            title='Fehlermeldung',
            legend='Fehlerbeschreibung',
            close=close,
            zeilen=(le,
                  'Zur�ck ...',
                  ),
            ).display()
            
            
    def EBKuSInternalError(self, REQUEST, RESPONSE):
        RESPONSE.setHeader('content-type', 'text/html')
        return h.Meldung(
            title='Interner Fehler',
            legend='Fehlerbeschreibung',
            align='left',
            zeilen=(
                "<strong>Es handelt sich h�chstwahrscheinlich um einen "
                "internen (Programmier-) Fehler in EBKuS. Bitte die folgende Meldung "
                "markieren, kopieren und in eine Email an den Entwickler "
                "(albrecht.schmiedel@ebkus.org) einf�gen. ",
                "<strong>Danke!</strong>",
                str(self.last_error_message),
                '&nbsp;',
                '&nbsp;',
                'Zur�ck ...',
                  ),
            ).display()
            
    def getMitarbeiterliste(self):
        stz_id = self.stelle['id']
        ml = ebapi.MitarbeiterList(
          where = 'stat = %s and benr = %s and stz = %s'
          % (ebapi.cc('status', 'i'), ebapi.cc('benr', 'bearb'), stz_id),
          order = 'na')
        return ml

                              
        
        
        
        
        
        
