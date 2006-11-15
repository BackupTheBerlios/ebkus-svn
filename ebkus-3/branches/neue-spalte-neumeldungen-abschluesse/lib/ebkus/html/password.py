# coding: latin-1

"""Module für die Mitarbeiter-Daten."""

import sha

from ebkus.app import Request
from ebkus.app.ebapi import *
from ebkus.app.ebapih import get_codes, get_all_codes, mksel
from ebkus.app_surface.pass_change_template import *
from ebkus.app_surface.standard_templates import *


class pwchange(Request.Request):
    """Auswahlformular zum Ändern der Mitarbeiterdaten. """
    
    permissions = Request.ALL
    
    def processForm(self, REQUEST, RESPONSE):
        akt_mitarbeiter = Mitarbeiter(ben=self.user)
        header = {'titel':
                  '&Auml;nderung des Benutzerpasswortes'
                  }
        
        res = []
        res.append(head_normal_t % ('&Auml;nderung des Benutzerpasswortes'))
        res.append(pass_change_t % akt_mitarbeiter)
        return ''.join(res)
        
class pw_make_change(Request.Request):
    permissions = Request.ALL
    def processForm(self, REQUEST, RESPONSE):
        res = []
        mitold = Mitarbeiter(ben=self.user)
        mit = Mitarbeiter()
        typed_old_pass = self.form.get('old_pass')
        new_pass = self.form.get('new_pass')
        repeat_pass = self.form.get('repeat_pass')
        db_old_pass = mitold['pass']
        #brehmea (msg) 13.09.2001
        s1 = sha.new(typed_old_pass)
        #if typed_old_pass == db_old_pass:
        if s1.hexdigest() == db_old_pass:
         #mastalet (msg) 14.09.2001 Verhindert das Speichern leerer und zu langer Passwörter
            if len(new_pass) >= 4 and len(new_pass) <= 20:
                if new_pass == repeat_pass:
                  #brehmea (msg) 13.09.2001
                    s2 = sha.new(new_pass)
                    mit['pass'] = s2.hexdigest()
                    mitold.update(mit)
                    meldung = {'titel':'&Auml;nderung durchgef&uuml;hrt!',
                           'legende':'&Auml;nderung durchgef&uuml;hrt!','url':'menu',
                            'zeile1':'Ihr Benutzerprofil wurde erfolgreich aktualisiert.',
                            'zeile2':'Ihr neues Passwort ist ab sofort g&uuml;ltig!'}
                    res.append(meldung_weiterleitung_t % meldung)
                else:
                    meldung = {'titel':'&Auml;nderung konnte nicht durchgef&uuml;hrt werden!',
                           'legende':'&Auml;nderung konnte nicht durchgef&uuml;hrt werden!',
                            'zeile1':'Die Verifizierung Ihres Passwortes war nicht erfolgreich.',
                            'zeile2':'Bitte versuchen Sie es erneut.'}
                    res.append(meldung_t % meldung)
            else:
                meldung = {'titel':'&Auml;nderung konnte nicht durchgef&uuml;hrt werden!',
                         'legende':'&Auml;nderung konnte nicht durchgef&uuml;hrt werden!',
                          'zeile1':'Die L&auml;nge des neuen Passwortes muss zwischen 4 und 20 Zeichen betragen.',
                          'zeile2':'Bitte versuchen Sie es erneut.'}
                res.append(meldung_t % meldung)
        else:
            meldung = {'titel':'&Auml;nderung konnte nicht durchgef&uuml;hrt werden!',
                      'legende':'&Auml;nderung konnte nicht durchgef&uuml;hrt werden!',
                       'zeile1':'Ihr altes Passwort wurde nicht korrekt eingegeben.',
                       'zeile2':'Passwort&auml;nderung wird abgebrochen.'}
            res.append(meldung_t % meldung)
        return ''.join(res)
        
        
        
        
        
        
        
        
        
        
        
