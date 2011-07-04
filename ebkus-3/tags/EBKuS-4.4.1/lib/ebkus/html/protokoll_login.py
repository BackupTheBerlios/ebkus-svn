# coding: latin-1

"""Login für zwei protokollberechtigte Mitarbeiter."""

import sha

from ebkus.app import Request
from ebkus.app.ebapi import cc, Mitarbeiter
from ebkus.app_surface.protokoll_templates import *
from ebkus.app_surface.standard_templates import *

class login_formular(Request.Request):
    """Formular zur Anmeldung eines zweiten protokollberechtigten
    Benutzers."""
    permissions = Request.PROTOCOL_MENU

    def processForm(self, REQUEST, RESPONSE):
        header = {'titel':
                  'Anmeldung zur Protokolleinsicht'
                  }
        res = []
        res.append(head_normal_ohne_help_t % ('Anmeldung zur Vorgangsprotokollierung'))
        # die Daten für den ersten Protokollberechtigten sind die des angemeldeten
        # Benutzers
        res.append(protokoll_login_t % {'ben': self.user, 'pass': '******'})
        return ''.join(res)
        
class check_protokoll_login(Request.Request):
    """Überprüft, ob die beiden Benutzer protokollberechtigt sind.
    Im Erfolgsfall werden die Benutzernamen im Session-Objekt
    gespeichert."""
    permissions = Request.PROTOCOL_MENU
    
    def processForm(self, REQUEST, RESPONSE):
        username1 = str(self.form.get('username1'))
        userpass1 = str(self.form.get('userpass1'))
        username2 = str(self.form.get('username2'))
        userpass2 = str(self.form.get('userpass2'))
        if not username1 == self.user:
            return self.wiederholen(
                zeile1 = "Benutzername1 muss der angemeldete Benutzer sein")
        mitarbeiter1 = Mitarbeiter(ben=username1,
                                   stat=cc('status', 'i'))
        try:
            mitarbeiter2 = Mitarbeiter(ben=username2,
                                       stat=cc('status', 'i'))
        except:
            return self.wiederholen(
                zeile1 = "Benutzername2 ist ungültig")
        if username1 == username2:
            return self.wiederholen(
                zeile1 = ("Es müssen sich zwei verschiedene " +
                          "protokollberechtigte Benutzer anmelden"))
        if not mitarbeiter1['benr'] == cc('benr', 'protokol'):
            return self.wiederholen(
                zeile1="Benutzer %(ben)s ist nicht protokollberechtigt" % mitarbeiter1)
        if not mitarbeiter2['benr'] == cc('benr', 'protokol'):
            return self.wiederholen(
                zeile1 = "Benutzer %(ben)s ist nicht protokollberechtigt" % mitarbeiter2)
        # Passwort von mitarbeiter1 wird nicht überprüft, da dieser bereits
        # angemeldet ist.
        if not mitarbeiter2['pass'] == sha.new(userpass2).hexdigest():
            return self.wiederholen(
                zeile1 = "Passwort von %(ben)s ist falsch" % mitarbeiter2)
        # erfolgreich, in der Session vermerken
        self.session.data['protokollbenutzer1'] = username1
        self.session.data['protokollbenutzer2'] = username2
        res = []
        meldung = {
            'titel':'Identifikation erfolgreich!',
            'legende':'Identifikation erfolgreich!',
            'url': 'menu_protocol',
            'zeile1':'Sie konnten erfolgreich identifiziert werden.',
            'zeile2':'Bitte best&auml;tigen Sie.'
            }
        res.append(meldung_weiterleitung_t % meldung)
        return ''.join(res)

    def wiederholen(self, zeile1=None):
        """Meldung ausgeben, wobei evt. die zeile1 durch den
        übergebenen Parameter ersetzt wird."""
        res = []
        meldung = {'titel':'Identifikation fehlgeschlagen!',
                   'legende':'Identifikation fehlgeschlagen!','url':'login_formular',
                   'zeile1':'Ihre Daten waren unvollst&auml;ndig oder nicht g&uuml;tig',
                   'zeile2':'Bitte best&auml;tigen Sie.'}
        if zeile1:
            meldung['zeile1'] = zeile1
        res.append(meldung_weiterleitung_t % meldung)
        return ''.join(res)

