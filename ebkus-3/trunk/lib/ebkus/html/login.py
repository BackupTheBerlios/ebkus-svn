# coding: latin-1
import sha, logging

from ebkus.app.session import create_session, get_session, has_session
from ebkus.app_surface.standard_templates import *
from ebkus.app_surface.session_templates import *
from ebkus.app import Request
from ebkus.app.ebapi import MitarbeiterList, cc
from ebkus.app.protocol import write_sql_protocol
from ebkus.config import config


class login(Request.Request):
    
    def checkAuth(self):
        """Überschreiben der checkAuth-Methode von Request.
        Damit wird kein seltsamer 'login'-User mehr gebraucht."""
        self.session = get_session(self.REQUEST, self.RESPONSE)
        if self.session:
            self.session.expire(self.RESPONSE)


    def processForm(self, REQUEST, RESPONSE):
        res = []
        username = self.form.get('username')
        password = self.form.get('pass')

        if username is None:
            res.append(head_normal_ohne_help_t % ("EBKuS Benutzeranmeldung"))
            res.append(login_interface_t %
                       {'index_url': "/ebkus/%s/index.html" % config.INSTANCE_NAME,
                        'title': config.INSTANCE_TITLE,
                        })
            return ''.join(res)

        ml = MitarbeiterList(where="ben = '%s' and stat = %s" %
                             (username, cc('status', 'i')))
        if not ml:
            write_sql_protocol(
                artdeszugriffs='LOGIN : Ungültiger Benutzername (%s)' % username,
                username=username, ip=self.ip)
            raise EE('Ungültiger Benutzername')
        mitarbeiter = ml[0]
        if not mitarbeiter['pass'] == sha.new(password).hexdigest():
            write_sql_protocol(artdeszugriffs='LOGIN : Falsches Passwort (%s)' % username,
                               username=username, ip=self.ip)
            raise EE('Ungültiges Passwort')
        other_session = has_session(username)
        if other_session:
            # Es gibt noch eine Session desselben Benutzers, die
            # nicht mit einem logout oder durch Timeout beendet wurde.
            other_session.delete()
        weiterleitung = 'menu'

        if mitarbeiter['pass'] == sha.new(username).hexdigest():
            # Passwort ist identisch mit dem Benutzernamen
            weiterleitung = 'pwchange'
        self.session = create_session(username, self.RESPONSE)
        write_sql_protocol(artdeszugriffs='LOGIN : Gültiges Login (%s)' % username,
                           username=username, ip=self.ip)
        RESPONSE.redirect(weiterleitung)
        return ''
                

class logout(Request.Request):

    permissions = Request.ALL

    def processForm(self, REQUEST, RESPONSE):
        write_sql_protocol(
            artdeszugriffs='LOGOUT : Benutzer (%s) hat sich abgemeldet' % self.user,
            username=self.user, ip=self.ip)
        if self.session:
            self.session.expire(RESPONSE)
        RESPONSE.redirect('login')
        return ''
