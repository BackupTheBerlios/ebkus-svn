# coding: latin-1

"""Module für die Dokumentenkarte."""

import string

from ebkus.app import Request
from ebkus.app import ebupd
from ebkus.app.ebapi import Akte, Fall, DokumentList, cc,is_binary
from ebkus.app_surface.standard_templates import *
from ebkus.app_surface.dokkarte_templates import *

class dokkarte(Request.Request):
    """Dokumentenkarte."""
    
    permissions = Request.DOKVIEW_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        file = self.form.get('file')
        # Fall 1 Dokumentenkarte direkt darstellen
        if not file or file == 'dokkarte':
            fallid = self.form.get('fallid')
            mitid = self.mitarbeiter['id']
            akid = self.form.get('akid')
            if akid: akid = int(akid)
            elif fallid:
                fallid = int(fallid)
                fall = Fall(fallid)
                akid = fall['akte_id']
                akid = int(akid)
            else:
                self.last_error_message = "Keine Men&uuml;auswahl erhalten"
                return self.EBKuSError(REQUEST, RESPONSE)
            return self.dokkarte_display(akid, fallid, mitid)
            
            # Fall 2 erst einfuegen oder updaten, dann Dokumentenkarte darstellen
        if self.einfuege_oder_update_operationen.get(file):
            akid = self.einfuegen_oder_update(file)
            # damit Dokumentenkarte nicht als Ergebnis eines POST
            # dargestellt wird
            RESPONSE.redirect('dokkarte?akid=%s' % akid)
            return ''
            
            # Fall 3 Update- oder Einfuegeformular anzeigen
            # Folgende URLs haben denselben Effekt:
            # 1)  http://localhost/efb/ebs/dokkarte?file=akteneu
            # 2)  http://localhost/efb/ebs/vermneu
            # Variante 1) nützlich wg. Aufruf aus menu
            # Könnte auch mir redirect gelöst werden.
        return self.ebkus.dispatch(file, REQUEST, RESPONSE)
        
    einfuege_oder_update_operationen = {
      'uploadeinf' : ('fallid', Fall),
      'dokeinf' : ('fallid', Fall),
      'removedoks' : ('fallid', Fall),
      'updvermeinf' : ('fallid', Fall),
      }
    
    def einfuegen_oder_update(self, file):
        function = getattr(ebupd, file)
        function(self.form)
        # Dies ist eine Art die Akte herauszufinden, auf die
        # sich das Einfuegen oder das Update bezog.
        # Es wäre vielleicht besser, die akid immer als
        # hidden Variable mitzuführen.
        id_name, klass = self.einfuege_oder_update_operationen.get(file)
        akid = klass(int(self.form[id_name]))['akte__id']
        return akid
        
    def dokkarte_display(self, akid, fallid = None, mitid=None):
        "Darstellung der Dokumentenkarte."
        
        if not akid and fallid:
            fall = Fall(fallid)
            akte = Akte(fall['akte_id'])
        else:
            akte = Akte(int(akid))
            
        faelle = akte['faelle']
        faelle.sort('bgy', 'bgm', 'bgd')
        
        # Aktueller bzw. letzter Fall, Wiederaufnehmbarkeit
        
        letzter_fall = akte['letzter_fall']
        aktueller_fall = akte['aktueller_fall']
        
        res = []
        res.append(head_normal_t %("Dokumentenindex der Akte"))
        res.append(dokkarte_start_t1)
        if aktueller_fall:
            res.append(menuedok_t % aktueller_fall)
        else:
            res.append(menuedokzda_t % letzter_fall)
        res.append(dokausgabe1_t % ('Aktendokumente der Akte %(vn)s %(na)s' %akte))
        for f in faelle:
            dokl = DokumentList(where = 'fall_id = %s'
                                   % (f['id']), order = 'vy,vm,vd')
            aktendokl = []
            for d in dokl:
                if d['art'] != cc('dokart', 'bnotiz'):
                    aktendokl.append(d)
            for a in aktendokl:
                if aktueller_fall:
                    if is_binary(a['mtyp']):
                        res.append(dokausgabe2_ohne_edit_t % a)
                    else:
                        res.append(dokausgabe2_mit_edit_t % a)
                else:
                    res.append(dokausgabe2b_t % a)
        res.append(dokausgabe3_t)
        res.append(dokausgabe1_t % ('Beraternotizen der Akte %(vn)s %(na)s' %akte))
        for f in faelle:
            beraternotizen = DokumentList(where = 'fall_id = %s and art = %s and mit_id = %s'% (f['id'], cc('dokart', 'bnotiz'), self.mitarbeiter['id']),
                                   order = 'vy,vm,vd')
            for b in beraternotizen:
                if aktueller_fall:
                    if is_binary(b['mtyp']):
                        res.append(dokausgabe2_ohne_edit_t % b)
                    else:
                        res.append(dokausgabe2_mit_edit_t % b)
                else:
                    res.append(dokausgabe2b_t % b)
        res.append(dokausgabe3_t)
        if beraternotizen or aktendokl:
            res.append(dokausgabe1_t % ('Printausgabe'))
            if aktendokl and aktueller_fall:
                res.append(dokausgabe5_t % aktueller_fall)
            elif aktendokl and letzter_fall:
                res.append(dokausgabe5_t % letzter_fall)
            if beraternotizen and aktueller_fall:
                res.append(dokausgabe4_t % aktueller_fall)
            elif beraternotizen and letzter_fall:
                res.append(dokausgabe4_t % letzter_fall)
            res.append(dokausgabe6_t)
            ##*************************************************************************
            ##  Entfernt wegen UNIX Kommando agrep. Funktioniert nicht unter Win
            ##
            ##  MastaleckT 08.03.2002
            ##*************************************************************************
            #res.append(dokausgabe7a_t % ('Suche in den Texten', ''))
            #if aktueller_fall:
            #  res.append(formhiddennamevalues_t % ({'name' : 'fallid' ,
            #                                      'value' : aktueller_fall['id']}))
            #elif letzter_fall:
            #  res.append(formhiddennamevalues_t % ({'name' : 'fallid' ,
            #                                      'value' : letzter_fall['id']}))
            #res.append(dokausgabe7b_t)
        res.append(dokkarte_ende_t)
        return string.join(res, '')
        
        
