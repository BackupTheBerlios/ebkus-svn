# coding: latin-1

"""Module für die Gruppenkarte."""

import string

from ebkus.app import Request
from ebkus.app import ebupd
from ebkus.app.ebapi import Gruppe, Akte, Fall, Bezugsperson, GruppendokumentList, cc,is_binary
from ebkus.app_surface.gruppenkarte_templates import *
from ebkus.app_surface.standard_templates import *

class gruppenkarte(Request.Request):

    permissions = Request.GRUPPENKARTE_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        file = self.form.get('file')
        
        # Fall 1 Gruppenkarte direkt darstellen
        
        if not file or file == 'gruppenkarte':
            gruppeid = self.form.get('gruppeid')
            mitid = self.mitarbeiter['id']
            if gruppeid: gruppeid = int(gruppeid)
            else:
                self.last_error_message = "Keine Men&uuml;auswahl erhalten"
                return self.EBKuSError(REQUEST, RESPONSE)
            return self.gruppenkarte_display(gruppeid, mitid)
            
            # Fall 2 erst einfuegen oder updaten, dann Klientenkarte darstellen
        if self.einfuege_oder_update_operationen.get(file):
            gruppeid = self.einfuegen_oder_update(file)
            # damit Klientenkarte nicht als Ergebnis eines POST
            # dargestellt wird
            RESPONSE.redirect('gruppenkarte?gruppeid=%s' % gruppeid)
            return ''
            
            # Fall 3 Dokumenten- Update- oder Einfuegeformular anzeigen
            # Folgende URLs haben denselben Effekt:
            # 1)  http://localhost/efb/ebs/gruppenkarte?file=gruppeneu
            # 2)  http://localhost/efb/ebs/gruppeneu
            # Variante 1) nützlich wg. Aufruf aus menu.
            # Könnte auch mir redirect gelöst werden.
            
        if file == 'dokkarte':
            gruppeid = self.form.get('gruppeid')
            if gruppeid: gruppeeid = int(gruppeid)
            else:
                self.last_error_message = "Keine Men&uuml;auswahl erhalten"
                return self.EBKuSError(REQUEST, RESPONSE)
            RESPONSE.redirect('dokkarte?gruppeid=%s' % gruppeid)
            return ''
            
        if file == 'hauptmenue':
            RESPONSE.redirect('menu')
            return ''
            
            # Achtung, das folgende wird nicht gehen, da die
            # Auswahl der Prozedur von den Parametern abhängig
            # gemacht wurde:
            #        elif file == 'updjghausw' and (fallid or akid):
            #          import updjgh
            #          return updjgh.updjgh(form, RESPONSE)
            #        elif file == 'updjghausw' and not fallid:
            #          import updjghausw
            #          return updjghausw.updjghausw(form, RESPONSE)
        return self.ebkus.dispatch(file, REQUEST, RESPONSE)
        
        
        
    einfuege_oder_update_operationen = {
      'gruppeeinf' : ('gruppeid', Gruppe),
      'gruppeteilneinf' : ('gruppeid', Gruppe),
      'uploadgreinf' : ('gruppeid', Gruppe),
      'dokgreinf' : ('gruppeid', Gruppe),
      'updgr' : ('gruppeid', Gruppe),
      'updgrvermeinf' : ('gruppeid', Gruppe),
      'updgrteiln' : ('gruppeid', Gruppe),
      'removeteiln' : ('gruppeid', Gruppe),
      'removegrdoks' : ('gruppeid', Gruppe)
      }
    
    def einfuegen_oder_update(self, file):
        function = getattr(ebupd, file)
        function(self.form)
        # Dies ist eine Art die Gruppe herauszufinden, auf die
        # sich das Einfuegen oder das Update bezog.
        # Es wäre vielleicht besser, die akid immer als
        # hidden Variable mitzuführen.
        id_name, klass = self.einfuege_oder_update_operationen.get(file)
        gruppeid = klass(int(self.form[id_name]))['gruppe__id']
        return gruppeid
        
    def gruppenkarte_display(self, gruppeid, mitid=None):
        "Darstellung der Gruppenkarte."
        
        gruppe = Gruppe(gruppeid)
        
        bezugspersonen = gruppe['bezugspersonen']
        bezugspersonen.sort('bezugsp_id__na','bezugsp_id__vn')
        faelle = gruppe['faelle']
        faelle.sort('fall_id__akte_id__na','fall_id__akte_id__vn')
        
        dokl = GruppendokumentList(where = 'gruppe_id = %s'
                               % (gruppe['id']), order = 'vy,vm,vd')
        
        beraternotizen = GruppendokumentList(where = 'gruppe_id = %s and art = %s and mit_id = %s' %
                (gruppe['id'], cc('dokart', 'bnotiz'), self.mitarbeiter['id']),
                               order = 'vy,vm,vd')
        
        res = []
        res.append(head_normal_t %("Dokumentenindex der Gruppe"))
        res.append(gruppenkarte_t1)
        res.append(gruppe_menu_t % gruppe)
        aktendokl = []
        for d in dokl:
            if d['art'] != cc('dokart', 'bnotiz'):
                aktendokl.append(d)
        res.append(dokausgabe1_t % ('Gruppenakte der Gruppe %(name)s' %gruppe))
        if aktendokl:
            for a in aktendokl:
                if is_binary(a['mtyp']):
                    res.append(dokausgabe2b_ohne_edit_t % a)
                else:
                    res.append(dokausgabe2b_mit_edit_t % a)
        res.append(dokausgabe3_t)
        res.append(dokausgabe1_t % ('Beraternotizen'))
        if beraternotizen:
            for b in beraternotizen:
                if is_binary(b['mtyp']):
                    res.append(dokausgabe2b_ohne_edit_t % b)
                else:
                    res.append(dokausgabe2b_mit_edit_t % b)
        res.append(dokausgabe3_t)
        res.append(dokausgabe1_t % ('Teilnehmerliste'))
        if bezugspersonen or faelle:
            for f in faelle:
                fall = Fall(f['fall_id'])
                akte = Akte(fall['akte_id'])
                res.append(teiln1_t % akte)
                res.append(teiln2_t % f)
                
            for b in bezugspersonen:
                bezugsp = Bezugsperson(b['bezugsp_id'])
                res.append(teiln1b_t % bezugsp)
                res.append(teiln2b_t % b)
                
        res.append(teiln3_t)
        res.append(dokausgabe1_t % ('Printausgabe'))
        if beraternotizen or aktendokl:
            if aktendokl:
                res.append(dokausgabe5b_t % gruppe )
            if beraternotizen:
                res.append(dokausgabe4b_t % gruppe )
        res.append(dokausgabe6_t)
        ##*************************************************************************
        ##  Entfernt wegen UNIX Kommando agrep. Funktioniert nicht unter Win
        ##
        ##  MastaleckT 08.03.2002
        ##*************************************************************************
        #if dokl:
        #  res.append(formhiddennamevalues_t % ({'name' : 'gruppeid' ,
        #                                        'value' : gruppeid}))
        #  res.append(dokausgabe7_t % ('Suche in den Texten', ''))
        res.append(gruppenkarte_ende_t)
        return string.join(res, '')
