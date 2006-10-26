# coding: latin-1

"""Module für Gruppen."""

import string

from ebkus.app import Request
from ebkus.app. ebapi import Gruppe, MitarbeiterGruppe, MitarbeiterGruppeList, Akte, Fall, FallGruppe, Bezugsperson, BezugspersonGruppe, ZustaendigkeitList, getNewGruppennummer, today, cc,ist_gruppen_mitarbeiter
from ebkus.app.ebapih import get_codes, mksel
from ebkus.app_surface.gruppe_templates import *
from ebkus.app_surface.standard_templates import *

class menugruppe(Request.Request):
    """Hauptmenü der Gruppenkartei (Tabellen: Gruppe, MitarbeiterGruppe)."""
    
    permissions = Request.MENUGRUPPE_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        mitarbeiterliste = self.getMitarbeiterliste()
        user = self.user
        
        res = []
        res.append(head_normal_t % 'Gruppenkartei')
        res.append(gruppenmenu_t)
        if self.mitarbeiter['benr__code'] == 'bearb':
            mitarbeitergruppenl = MitarbeiterGruppeList(where = 'mit_id = %s'
                                                  % self.mitarbeiter['id'] )
            mitarbeitergruppenl.sort('mit_id__na', 'gruppe_id__name')
            for m in mitarbeitergruppenl:
                if m['gruppe_id__stz'] == self.stelle['id']:
                    res.append(gruppenmenu_auswahl_t % m)
                    
        elif self.mitarbeiter['benr__code'] == 'verw' or self.mitarbeiter['benr__code'] == 'admin':
            mitarbeitergruppenl = MitarbeiterGruppeList()
            mitarbeitergruppenl.sort('mit_id__na', 'gruppe_id__name')
            for m in mitarbeitergruppenl:
                if m['gruppe_id__stz'] == self.stelle['id']:
                    res.append(gruppenmenu_auswahl_t % m)
        res.append(gruppemenu_ende_t)
        return string.join(res, '')
        
        
class gruppeneu(Request.Request):
    """Neue Gruppe eintragen (Tabellen: Gruppe, MitarbeiterGruppe)."""
    
    permissions = Request.GRUPPENEU_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        mitarbeiterliste = self.getMitarbeiterliste()
        user = self.user
        gruppentypen = get_codes('grtyp')
        teilnehmer = get_codes('teiln')
        gruppentypen.sort('name')
        teilnehmer.sort('name')
        hidden ={'file': 'gruppeeinf'}
        gruppeid = Gruppe().getNewId()
        hiddenid ={'name': 'gruppeid', 'value': gruppeid}
        hiddenid2 ={'name': 'stz', 'value': self.stelle['id']}
        
        # Gruppenummer
        
        gruppennummer = getNewGruppennummer(self.stelle['code'])
        hiddengn ={'name': 'gn', 'value': gruppennummer }
        
        # Liste der Templates als String
        
        res = []
        res.append(head_normal_t % 'Neue Gruppe erstellen')
        res.append(gruppe_neu_t)
        res.append(formhiddenvalues_t % hidden)
        res.append(formhiddennamevalues_t % hiddenid)
        res.append(formhiddennamevalues_t % hiddengn)
        res.append(formhiddennamevalues_t % hiddenid2)
        res.append(gruppe_neu_t2 % {'gn' : gruppennummer})
        res.append(gruppe_neu_datum_t % today())
        res.append(gruppe_neu_teilnehmer_t)
        mksel(res, codeliste_t, teilnehmer)
        res.append(gruppe_neu_mitarbeiter_t)
        mksel(res, mitarbeiterliste_t, mitarbeiterliste, 'ben', user)
        res.append(gruppe_neu_gruppenart_t)
        mksel(res, codeliste_t, gruppentypen)
        res.append(gruppe_neu_ende_t)
        return string.join(res, '')
        
        
class updgruppe(Request.Request):
    """Gruppe ändern (Tabellen: Gruppe, MitarbeiterGruppe)."""
    
    permissions = Request.GRUPPENEU_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        mitarbeiterliste = self.getMitarbeiterliste()
        user = self.user
        
        if self.form.has_key('gruppeid'):
            gruppeid = self.form.get('gruppeid')
            gruppe = Gruppe(int(gruppeid))
        else:
            self.last_error_message = "Keine ID fuer die Gruppe erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
            
        mitarbeitergruppe =  gruppe['mitarbeiter']
        gruppentypen = get_codes('grtyp')
        teilnehmer = get_codes('teiln')
        gruppentypen.sort('name')
        teilnehmer.sort('name')
        hidden ={'file': 'updgr'}
        hiddenid ={'name': 'gruppeid', 'value': gruppeid}
        hiddenid2 ={'name': 'stz', 'value': self.stelle['id']}
        
        # Liste der Templates als String
        
        res = []
        res.append(head_normal_t % 'Gruppe bearbeiten')
        res.append(gruppe_upd_t % gruppe )
        res.append(formhiddenvalues_t % hidden)
        res.append(formhiddennamevalues_t % hiddenid)
        res.append(formhiddennamevalues_t % hiddenid2)
        res.append(gruppe_upd_datum_t % gruppe)
        res.append(gruppe_upd_teilnehmer_t % gruppe)
        mksel(res, codeliste_t, teilnehmer, 'id', gruppe['teiln'])
        res.append(gruppe_upd_mitarbeiter_t)
        for m in mitarbeiterliste:
            if ist_gruppen_mitarbeiter(gruppe['id'],m['id']):
                res.append(gruppe_sel_mit_t % m)
            else:
                res.append(gruppe_notsel_mit_t % m)
        res.append(gruppe_neu_gruppenart_t)
        mksel(res, codeliste_t, gruppentypen, 'id', gruppe['grtyp'])
        res.append(gruppe_upd_ende_t % gruppe)
        return string.join(res, '')
        
        
class gruppeteilnausw(Request.Request):
    """Teilnehmerauswahl (Tabellen: FallGruppe, BezugspersonGruppe)."""
    
    permissions = Request.GRUPPETEILN_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        mitarbeiterliste = self.getMitarbeiterliste()
        user = self.user
        if self.form.has_key('gruppeid'):
            gruppeid = self.form.get('gruppeid')
            gruppe = Gruppe(gruppeid)
        else:
            self.last_error_message = "Keine ID fuer die Gruppe erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
            
            # Fuer FORM-HIDDEN-VALUES
            
        hidden ={'file': 'gruppeteilneinf'}
        hiddenid ={'name': 'mitid', 'value': self.mitarbeiter['id']}
        
        # Liste der Templates als String
        
        res = []
        res.append(head_normal_t %("Teilnehmerauswahl aus der Klientenkartei"))
        res.append(teilnauswahl_form_t % gruppe)
        res.append(formhiddenvalues_t % hidden)
        res.append(formhiddennamevalues_t % hiddenid)
        
        if self.mitarbeiter['benr__code'] == 'bearb':
            zustaendigkeiten = ZustaendigkeitList(where = 'ed = 0 and mit_id = %s'
                                                  % self.mitarbeiter['id'] )
            zustaendigkeiten.sort('mit_id__na', 'fall_id__akte_id__na',
                                  'fall_id__akte_id__vn')
            res.append(teilnauswahl_t)
            
            for z in zustaendigkeiten:
                if z['fall_id__akte_id__stzak'] == self.stelle['id']:
                    res.append(teilnauswahl1_t % z)
            res.append(teilnauswahl2_t)
            
            for z in zustaendigkeiten:
                if z['fall_id__akte_id__stzak'] == self.stelle['id']:
                    akte = Akte(z['fall_id__akte_id'])
                    fn = z['fall_id__fn']
                    bezugspliste = akte['bezugspersonen']
                    for b in bezugspliste:
                        b['fn'] = fn
                        res.append(teilnauswahl3_t % b)
                        del b['fn']
            res.append(teilnauswahl4_t % today())
            
        elif self.mitarbeiter['benr__code'] == 'verw' or 'admin':
            zustaendigkeiten = ZustaendigkeitList(where = 'ed = 0' )
            zustaendigkeiten.sort('mit_id__na', 'fall_id__akte_id__na',
                                  'fall_id__akte_id__vn')
            res.append(teilnauswahl_t)
            
            for z in zustaendigkeiten:
                if z['fall_id__akte_id__stzak'] == self.stelle['id']:
                    res.append(teilnauswahl1_t % z)
            res.append(teilnauswahl2_t)
            
            for z in zustaendigkeiten:
                if z['fall_id__akte_id__stzak'] == self.stelle['id']:
                    akte = Akte(z['fall_id__akte_id'])
                    fn = z['fall_id__fn']
                    bezugspliste = akte['bezugspersonen']
                    for b in bezugspliste:
                        b['fn'] = fn
                        res.append(teilnauswahl3_t % b)
                        del b['fn']
            res.append(teilnauswahl4_t % today())
        return string.join(res, '')
        
        
class gruppeteiln(Request.Request):
    """Gruppenteilnehmer eintragen (Tabellen: FallGruppe, BezugspersonGruppe)."""
    
    permissions = Request.GRUPPETEILN_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        mitarbeiterliste = self.getMitarbeiterliste()
        user = self.user
        
        if self.form.has_key('gruppeid'):
            gruppeid = self.form.get('gruppeid')
            gruppe = Gruppe(gruppeid)
        else:
            self.last_error_message = "Keine ID fuer Gruppe erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
            
        bezugspersonen = gruppe['bezugspersonen']
        bezugspersonen.sort('bgy','bgm','bgd')
        faelle = gruppe['faelle']
        faelle.sort('fall_id__akte_id__na','bgy','bgm','bgd')
        
        res = []
        res.append(head_normal_ohne_help_t %("Teilnehmerliste der Gruppe: " + "%(name)s, %(bgd)s.%(bgm)s.%(bgy)s-%(ed)s.%(em)s.%(ey)s" % gruppe))
        res.append(teilnehmerliste_t %("%(name)s, %(bgd)s.%(bgm)s.%(bgy)s-%(ed)s.%(em)s.%(ey)s" % gruppe))
        
        for f in faelle:
            fall = Fall(f['fall_id'])
            akte = Akte(fall['akte_id'])
            res.append(teilnehmerliste_fall1_t % akte)
            res.append(teilnehmerliste_fall2_t % f)
            
        for b in bezugspersonen:
            bezugsp = Bezugsperson(b['bezugsp_id'])
            res.append(teilnehmerliste_bzpers1_t % bezugsp)
            res.append(teilnehmerliste_bzpers2_t % b)
            
        res.append(teilnehmerliste_ende_t)
        return string.join(res, '')
        
        
class updteiln(Request.Request):
    """Teilnehmerdaten ändern (Tabellen: FallGruppe, BezugspersonGruppe)."""
    
    permissions = Request.GRUPPETEILN_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        mitarbeiterliste = self.getMitarbeiterliste()
        user = self.user
        
        if self.form.has_key('gruppeid'):
            gruppeid = self.form.get('gruppeid')
            gruppe = Gruppe(gruppeid)
        else:
            self.last_error_message = "Keine ID fuer die Gruppe erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
            
        if self.form.has_key('bezugspid'):
            bezugspgrid = self.form.get('id')
            teiln = BezugspersonGruppe(int(bezugspgrid))
            bezugsp = Bezugsperson(teiln['bezugsp_id'])
        elif self.form.has_key('fallid'):
            fallgrid = self.form.get('id')
            teiln = FallGruppe(int(fallgrid))
            fall = Fall(teiln['fall_id'])
        else:
            self.last_error_message = "Keine ID fuer Fall oder Bezugsperson erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
            
        hidden ={'file': 'updgrteiln'}
        
        # Liste der Templates als String
        
        res = []
        res.append(head_normal_t % 'Datum des Gruppenteilnehmers &auml;ndern')
        res.append(teilnauswahl_form_t % gruppe)
        res.append(formhiddenvalues_t % hidden)
        if self.form.has_key('fallid'):
            res.append(teilnupd_t % teiln)
            res.append(formhiddennamevalues_t % ({ 'name': 'fallgrid',
                                                   'value' : teiln['id'] }))
        elif self.form.has_key('bezugspid'):
            res.append(formhiddennamevalues_t % ({ 'name': 'bezugspgrid',
                                                   'value' : teiln['id'] }))
            res.append(teilnupdb_t % teiln)
        res.append(teilnupd1_t % teiln)
        return string.join(res, '')
        
        
class rmteiln(Request.Request):
    """Teilnehmer löschen (Tabellen: FallGruppe, BezugspersonGruppe)."""
    
    permissions = Request.RMTEILN_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        mitarbeiterliste = self.getMitarbeiterliste()
        user = self.user
        
        if self.form.has_key('gruppeid'):
            gruppeid = self.form.get('gruppeid')
            gruppe = Gruppe(gruppeid)
        else:
            self.last_error_message = "Keine ID fuer Dokument erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
            
        bezugspersonen = gruppe['bezugspersonen']
        faelle = gruppe['faelle']
        
        hidden ={'file': 'removeteiln'}
        
        # Liste der Templates als String
        
        res = []
        res.append(head_normal_t % ("Teilnehmer der Gruppe l&ouml;schen"))
        res.append(teilnauswahl_form_t % gruppe)
        res.append(formhiddenvalues_t % hidden)
        res.append(teilnauswahl_loesch_t)
        for f in faelle:
            res.append(teilnauswahl1_loesch_t % f)
        res.append(teilnauswahl2_loesch_t)
        for b in bezugspersonen:
            res.append(teilnauswahl3_loesch_t % b)
        res.append(teilnauswahl4_loesch_t)
        return string.join(res, '')
        
