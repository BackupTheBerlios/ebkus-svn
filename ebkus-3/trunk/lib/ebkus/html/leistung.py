# coding: latin-1

"""Module für die Leistung."""

from ebkus.app import Request
from ebkus.app.ebapi import Fall, Leistung, today
from ebkus.app.ebapih import get_codes, make_option_list
from ebkus.config import config

class _leist(Request.Request):
    # leistneu und updleist mit derselben Routine,
    # nur anders parametrisiert
    def _process(self, REQUEST, RESPONSE,
                 title,
                 legendtext,
                 fall,
                 leistung,
                 file,
                 mitarbeiter_selected,
                 leistung_selected,
                 ):
        leistungen = fall['leistungen']
        leistungen.sort('bgy', 'bgm', 'bgd')
        leistungsarten = get_codes('fsle')
        # hier kommt alles rein, was das template braucht
        context_dict = {
            'weiterleitung': False,
            'title': title,
            'legendtext': legendtext,
            'fall': fall,
            'file': file,
            'mitarbeiter_options': make_option_list(self.getMitarbeiterliste(),
                                                    'id', 'na',
                                                    selected=mitarbeiter_selected),
            'leistungsart_options': make_option_list(leistungsarten,
                                                    'id', 'name',
                                                    selected=leistung_selected),
            'leistung': leistung,
            'leistungen': leistungen,
            }
        return self.render('leistung', context_dict)
    
class leistneu(_leist):
    """Neue Leistung eintragen. (Tabelle: Leistung.)"""
    
    permissions = Request.UPDATE_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        if self.form.has_key('fallid'):
            fallid = self.form.get('fallid')
        else:
            self.last_error_message = "Keine ID für den Fall erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
        fall = Fall(int(fallid))
        leistung = {
            'id': Leistung().getNewId(),
            'bgy': today().year,
            'bgm': today().month,
            'bgd': today().day,
            'ey': '',
            'em': '',
            'ed': '',
            'stz': self.stelle['id'],
            }
        return self._process(REQUEST, RESPONSE,
                             "Neue Leistung eintragen",
                             "Neue Leistung eintragen für",
                             fall,
                             leistung,
                             'leisteinf',
                             self.mitarbeiter['id'],
                             None,
                             )
        
class updleist(_leist):
    """Leistung ändern. (Tabelle: Leistung.)"""
    
    permissions = Request.UPDATE_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        if self.form.has_key('leistid'):
            id = self.form.get('leistid')
        else:
            self.last_error_message = "Keine ID für die Leistung erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
        leistung = Leistung(int(id))
        fall = Fall(leistung['fall_id'])
        return self._process(REQUEST, RESPONSE,
                             "Leistung bearbeiten",
                             "Leistung bearbeiten von",
                             fall,
                             leistung,
                             'updleist',
                             leistung['mit_id'],
                             leistung['le']
                             )

