# coding: latin-1

"""Module für die Mitarbeiter-Daten."""

import string

from ebkus.app import Request
from ebkus.config import config
from ebkus.app.ebapi import Mitarbeiter, MitarbeiterList, Code, today
from ebkus.app.ebapih import get_codes, get_all_codes, mksel,mksel_benr
from ebkus.app_surface.mitarbeiter_templates import *
from ebkus.app_surface.standard_templates import *

class mitausw(Request.Request):
    """Auswahlformular zum Ändern der Mitarbeiterdaten. """
    
    permissions = Request.ADMIN_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        bearbeiterliste = self.getMitarbeiterliste()
        user = self.user
        stelle = self.stelle
        mitarbeiterliste = MitarbeiterList(where = '', order = 'na')
        stellenzeichen = get_all_codes('stzei')
        benutzerarten = get_all_codes('benr')
        dienststatusl = get_all_codes('status')
        
        # Liste der Templates als String
        
        res = []
        res.append(head_normal_ohne_help_t %("Mitarbeitereintrag zum &Auml;ndern ausw&auml;hlen"))
        res.append(mitauswstart_t)
        res.append(menuemit_t)
        res.append(mitausw_anz)
        for m in mitarbeiterliste:
            res.append(mitlistehrefs_t % m)
        res.append(mitausw_anz_ende_t)
        return string.join(res, '')
        
        
class mitneu(Request.Request):
    """Mitarbeiterstammdatenformular."""
    
    permissions = Request.ADMIN_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        bearbeiterliste = self.getMitarbeiterliste()
        user = self.user
        stelle = self.stelle
        mitarbeiterliste = MitarbeiterList(where = '', order = 'na')
        stellenzeichen = get_all_codes('stzei')
        masterdb = Code(kat_code = 'dbsite', code = '%s' % config.MASTER_SITE)
        benutzerarten = get_all_codes('benr')
        dienststatusl = get_all_codes('status')
        
        
        # Form-Hidden-Values
        
        hidden ={'file': 'miteinf'}
        mitid = Mitarbeiter().getNewId()
        hiddenid ={'name': 'mitid', 'value': mitid}
        
        # Liste der Templates als String
        
        res = []
        res.append(head_normal_ohne_help_t %("Neuen Mitarbeiter eintragen"))
        res.append(mitarbeiter_neu_t1)
        mksel(res, codelistecode_t, dienststatusl, 'code', 'i')
        res.append(mitarbeiter_neu_t2)
        mksel_benr(res, codelistecode_t, benutzerarten, 'code', 'bearb')
        res.append(mitarbeiter_neu_t3)
        mksel(res, codelistecode_t, stellenzeichen, 'code', stelle['code'])
        res.append(mitarbeiter_neu_t4)
        for m in mitarbeiterliste:
            res.append(mitliste_t % m)
        res.append(formhiddenvalues_t % hidden)
        res.append(formhiddennamevalues_t % hiddenid)
        res.append(mitarbeiter_neu_t5)
        return string.join(res, '')
        
        
class updmit(Request.Request):
    """Updateformular für die Stammdaten der Mitarbeiter. """
    permissions = Request.ADMIN_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        bearbeiterliste = self.getMitarbeiterliste()
        user = self.user
        stelle = self.stelle
        stellenzeichen = get_codes('stzei')
        benutzerarten = get_codes('benr')
        dienststatusl = get_codes('status')
        mitarbeiterliste = MitarbeiterList(where = '', order = 'na')
        if self.form.has_key('mitid'):
            mitid = self.form.get('mitid')
            mit = Mitarbeiter(int(mitid))
        else:
            self.last_error_message = "Keine ID fuer den Mitarbeiter erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
            
        hidden ={'file': 'updmit'}
        hiddenid ={'name': 'mitid', 'value': mitid}
        
        # Liste der Templates als String
        
        res = []
        res.append(head_normal_ohne_help_t %("Mitarbeitereintrag für '%(vn)s %(na)s' &auml;ndern" % mit))
        res.append(mitarbeiter_upd_t1 %mit)
        mksel(res, codelistecode_t, dienststatusl, 'id', mit['stat'])
        res.append(mitarbeiter_upd_t2 %mit)
        mksel_benr(res, codelistecode_t, benutzerarten, 'id', mit['benr'])
        res.append(mitarbeiter_upd_t3 %mit)
        mksel(res, codelistecode_t, stellenzeichen, 'id', mit['stz'])
        res.append(mitarbeiter_upd_t4)
        for m in mitarbeiterliste:
            res.append(mitlistehrefs_t % m)
        res.append(formhiddenvalues_t % hidden)
        res.append(formhiddennamevalues_t % hiddenid)
        res.append(mitarbeiter_upd_t5)
        return string.join(res, '')
        
        
        
