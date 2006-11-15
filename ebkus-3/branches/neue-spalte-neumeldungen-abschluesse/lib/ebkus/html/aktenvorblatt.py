# coding: latin-1

"""Module für das Aktenvorblatt."""

import string

from ebkus.app import Request
from ebkus.app.ebapi import Fall, FallGruppeList, BezugspersonGruppeList, today, cc
from ebkus.app_surface.aktenvorblatt_templates import *
from ebkus.app_surface.standard_templates import *


class vorblatt(Request.Request):
    """Aktenvorblatt in HTML ausgeben"""
    
    permissions = Request.KLKARTE_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        mitarbeiterliste = self.getMitarbeiterliste()
        user = self.user
        if self.form.has_key('fallid'):
            fallid = self.form.get('fallid')
        else:
            self.last_error_message = "Keine ID fuer den Fall erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
        fall = Fall(int(fallid))
        akte = fall['akte']
        bezugspersonen = akte['bezugspersonen']
        einrichtungen = akte['einrichtungen']
        faelle = akte['faelle']
        faelle.sort('bgy', 'bgm', 'bgd')
        bezugspersonen.sort('verw__sort')
        einrichtungen.sort('status', 'na')
        
        # Aktueller bzw. letzter Fall, Wiederaufnehmbarkeit
        
        letzter_fall = akte['letzter_fall']
        aktueller_fall = akte['aktueller_fall']
        wiederaufnehmbar =  akte['wiederaufnehmbar']
        res = []
        res.append(head_normal_ohne_help_t % "Aktenvorblatt")
        res.append(vkopf_t % today())
        res.append(vakten1_t % akte)
        if akte['no'] !='':
            akte['nobedakte'] = 'Notiz'
        else:
            akte['nobedakte'] = ''
        if akte['ber'] != '' or akte['fs'] != cc('fsfs', '999') or akte['no'] !='':
            res.append(vakten2_t % akte)
        del akte['nobedakte']
        
        for b in bezugspersonen:
            res.append(vbezugspersonen1_t % b)
            if b['ber'] != '' or b['fs'] != cc('fsfs', '999') or b['no'] != '':
                res.append(vbezugspersonen2_t % b)
        i = 0
        res.append(vbezugspersonenzeile_t)
        
        res.append(veinrichtungs_kopf1_t)
        res.append(veinrichtungs_kopf2_t)
        for e in einrichtungen:
            res.append(veinrichtung_t % e)
        i = 0
        res.append(veinrichtungszeile_t)
        
        res.append(vanmeldung_kopf_t)
        for f in faelle:
            for a in f['anmeldung']:
                if a['no'] !='':
                    a['nobedanm'] = 'Notiz'
                else:
                    a['nobedanm'] = ''
                res.append(vanmeldung_t % a)
                del a['nobedanm']
                
        res.append(vleistungs_kopf_t)
        for f in faelle:
            for l in f['leistungen']:
                res.append(vleistungs_t % l)
                if l['ey'] == 0:
                    res.append(vleistungsendeleer_t)
                else:
                    res.append(vleistungsendedatum_t % l)
        i = 0
        res.append(vleistungszeile_t)
        
        res.append(vbearbeiter_kopf_t)
        for f in faelle:
            for z in f['zustaendigkeiten']:
                res.append(vbearbeiter_t % z)
                if z['ey'] == 0:
                    res.append(vbearbeiterendeoffen_t)
                else:
                    res.append(vbearbeiterendedatum_t % z)
        i = 0
        res.append(vbearbeiterzeile_t)
        
        res.append(vfall_kopf_t)
        for f in faelle:
            res.append(vfall_t % f)
            if f['aktuell'] == 1:
                res.append(vfalloffen_t)
            else:
                res.append(vfallendedatum_t % f)
        i = 0
        res.append(vfallzeile_t)
        res.append(vtabende_t)
        
        res.append(vnotiz_t)
        if akte['no']:
            res.append(vnotizakte_t % akte)
        for b in bezugspersonen:
            if b['no']:
                res.append(vnotizbperson_t % b)
        for e in einrichtungen:
            if e['no']:
                res.append(vnotizeinr_t % e)
        for f in faelle:
            for a in f['anmeldung']:
                if a['no']:
                    res.append(vnotizanm_t % a)
                    
        for f in faelle:
            fallgruppen = FallGruppeList(where = 'fall_id = %s' % f['id'])
            for g in fallgruppen:
                res.append(klkartegruppef_t % f)
                res.append(klkartegruppe_t % g)
                
        for b in bezugspersonen:
            bezugspersongruppen = BezugspersonGruppeList(where = 'bezugsp_id = %s' % b["id"])
            for e in bezugspersongruppen:
                res.append(klkartegruppeb_t % b)
                res.append(klkartegruppe_t % e)
        res.append(vnotizende_t)
        return string.join(res, '')
