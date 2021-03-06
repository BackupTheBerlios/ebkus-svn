# coding: latin-1

"""Module f�r die Anmeldung."""

from ebkus.app import Request
from ebkus.app.ebapi import Akte, Fall, Anmeldung, cc


import ebkus.html.htmlgen as h
from ebkus.html.akte_share import akte_share


class _anm(Request.Request, akte_share):
    def _process(self,
                 title,
                 anm,
                 hidden,
                 ):
        anmeldekontakt = self.get_anmeldekontakt(anm)
        res = h.FormPage(
            title=title,
            name='anmform',action="klkarte",method="post",
            breadcrumbs = (('Hauptmen�', 'menu'),
                           ('Klientenkarte', 'klkarte?akid=%(fall__akte_id)s' % anm),
                           ),
            hidden=hidden,
            rows=(anmeldekontakt,
                  h.SpeichernZuruecksetzenAbbrechen(),
                  ),
            )
        return res.display()

class anmneu(_anm):
    """Neue Anmeldung eintragen. (Tabelle: Anmeldung)"""
    permissions = Request.UPDATE_PERM
    def processForm(self, REQUEST, RESPONSE):
        if self.form.has_key('fallid'):
            fallid = self.form.get('fallid')
        else:
            self.last_error_message = "Keine ID f�r den Fall erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
        fall = Fall(fallid)
        akte = Akte(fall['akte_id'])
        anm = Anmeldung()
        anm.init(
            id=Anmeldung().getNewId(),
            fall_id=fall['id'],
            zm=cc('fszm', '999'),
            )
        # Nachname und Telefon des Klienten
        # im Formular anbieten.
        anm['von'] = akte['na']
        anm['mtl'] = akte['tl1']
                    
        return self._process(
            title="Neue Anmeldeinformation eintragen",
            anm=anm,
            hidden=(('anmid', anm['id']),
                    ('file', 'anmeinf'),
                    ('fallid', anm['fall_id']),
                    )
            )
        
class updanm(_anm):
    """Anmeldung �ndern. (Tabelle: Anmeldung)"""
    permissions = Request.UPDATE_PERM
    def processForm(self, REQUEST, RESPONSE):
        if self.form.has_key('anmid'):
            id = self.form.get('anmid')
        else:
            self.last_error_message = "Keine ID f�r die Anmeldung erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
        anm = Anmeldung(id)
        return self._process(
            title="Anmeldeinformation &auml;ndern",
            anm=anm,
            hidden=(('anmid', anm['id']),
                    ('file', 'updanm'),
                    ),
            )

        

