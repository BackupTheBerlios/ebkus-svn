# coding: latin-1

"""Module f�r die Dokumentenkarte."""

import string

from ebkus.app import Request
from ebkus.app import ebupd
from ebkus.app.ebapi import Akte, Fall, DokumentList, Gruppe, \
     GruppendokumentList, Gruppendokument, cc,is_binary
from ebkus.app_surface.standard_templates import *
from ebkus.app_surface.dokkarte_templates import *

import ebkus.html.htmlgen as h
from ebkus.html.akte_share import akte_share

class _dok(Request.Request, akte_share):
##     def _processForm(self, karte, kartenid_name, kartenid_path, REQUEST, RESPONSE):
##         file = self.form.get('file')
##         if not file or file == karte:
##             id = self.form.get(kartenid_name)
##             if not id:
##                 self.last_error_message = "Keine Men&uuml;auswahl erhalten"
##                 return self.EBKuSError(REQUEST, RESPONSE)
##             return self._display_dokkarte()
##         if self.einfuege_oder_update_operationen.get(file, kartenid_path):
##             id = self.einfuegen_oder_update(file)
##             # damit Dokumentenkarte nicht als Ergebnis eines POST
##             # dargestellt wird
##             RESPONSE.redirect('%s?%s=%s' % (karte, kartenid_name, id))
##             return ''
##         return self.ebkus.dispatch(file, REQUEST, RESPONSE)
    def einfuegen_oder_update(self, file, path):
        function = getattr(ebupd, file)
        function(self.form)
        # Dies ist eine Art die Akte herauszufinden, auf die
        # sich das Einfuegen oder das Update bezog.
        # Es w�re vielleicht besser, die akid immer als
        # hidden Variable mitzuf�hren.
        id_name, klass = self.einfuege_oder_update_operationen.get(file)
        id = klass(int(self.form[id_name]))[path]
        return id
    
    def get_dokumenten_tabelle(self, legend,
                               dokumente_list,
                               cgi_name, # gruppeid oder fallid
                               db_name,  # gruppe_id oder fall_id
                               container, # gruppe oder fall
                               aktueller_fall, # nur wenn container der aktuelle Fall ist, sonst None
                               art,       # anotiz oder bnotiz
                               ):
        upd = "updverm?%(cgi_name)s=%%(%(db_name)s)s&dokid=%%(id)d" % locals()
        rm = "rmdok?%(cgi_name)s=%%(%(db_name)s)s&dokid=%%(id)d" % locals()
        view = "dokview?%(cgi_name)s=%%(%(db_name)s)s&dokid=%%(id)d" % locals()
        drucken_txt = "go_to_url('newXX dokview2?%(cgi_name)s=%%(id)d&art=%(art)s')" % locals()
        drucken_txt = drucken_txt % container
        drucken_pdf = "go_to_url('newXX print_pdf?%(cgi_name)s=%%(id)d&art=%(art)s')" % locals()
        drucken_pdf = drucken_pdf % container
        def editierbar(dok, aktueller_fall):
            if isinstance(dok, Gruppendokument):
                # Gruppendokumente immer editierbar
                return True
            if aktueller_fall:
                # Falldokumente nur wenn sie zu einem aktuellem Fall geh�ren
                return dok['fall_id'] == aktueller_fall['id']
            return False
        return h.FieldsetDataTable(
            legend=legend,
            headers=('Datum', 'Betreff', 'Typ', 'Aufgenommen von'),
            noheaders=3, # keine header f�r edit, del, view icon
            daten= [[editierbar(dok, aktueller_fall) and
                     h.Icon(href=upd % dok,
                            icon= "/ebkus/ebkus_icons/edit_text_button.gif",
                            tip= 'Dokument bearbeiten') or
                     h.Dummy(),
                     editierbar(dok, aktueller_fall) and
                     h.Icon(href=rm % dok,
                            icon= "/ebkus/ebkus_icons/del_text_button.gif",
                            tip= 'Dokument l�schen') or
                     h.Dummy(),
                     h.Icon(href=view % dok,
                            target="_new",
                            icon= "/ebkus/ebkus_icons/view_details.gif",
                            tip= 'Dokument ansehen'),
                     h.Datum(date=dok.getDate('v')),
                     h.String(string="%(art__name)s: %(betr)s" % dok),
                     h.String(string="%(mtyp__code)s" % dok),
                     h.String(string="%(mit_id__na)s" % dok)]
                    for dok in dokumente_list],
            buttons=dokumente_list and
            [h.Button(value="Drucken (TXT)",
                      tip="Zum Drucken im Text-Format zusammenstellen (nur Textdokumente)",
                      onClick=drucken_txt,
                      ),
             h.Button(value="Drucken (PDF)",
                      tip="Zum Drucken im PDF-Format zusammenstellen (nur Textdokumente)",
                      onClick=drucken_pdf,
                      ),
             ] or None,
            )
##     def _display_dokkarte(self):
##         gruppeid = self.form.get('gruppeid')
##         gruppe = Gruppe(gruppeid)
##         dokumente_list = GruppendokumentList(
##             where = 'gruppe_id = %s and art != %s'
##             % (gruppe['id'], cc('dokart', 'bnotiz')),
##             order = 'vy,vm,vd')
##         beraternotizen = GruppendokumentList(
##             where = 'gruppe_id = %s and art = %s and mit_id = %s' %
##             (gruppe['id'], cc('dokart', 'bnotiz'), self.mitarbeiter['id']),
##             order = 'vy,vm,vd')
        
##         dokumente_list = self.get_dokumente_list()
##         menu = h.FieldsetInputTable(
##             daten=[[
##             h.Button(value="Hauptmen�",
##                    tip="Zum Hauptmen�",
##                    onClick="go_to_url('menu')",
##                    ),
##             h.Button(value="Gruppenmen�",
##                    tip="Zum Gruppenmen�",
##                    onClick="go_to_url('menugruppe')",
##                    ),
##             h.Button(value="Gruppenkarte",
##                      tip="Gruppenkarte ansehen",
##                      class_='buttonbig',
##                      onClick="go_to_url('grkarte?gruppeid=%(id)s')" % gruppe,
##                    ),
##             h.SelectGoto(name='Auswahl1',
##                          options =
## """<option value="nothing">[ Neu ]</option>
## """
##                          ),
##             ]],
##             )
##         dokumente = h.FieldsetDataTable(
##             legend= 'Dokumente',
##             headers= ('Datum', 'Betreff', 'Aufgenommen von'),
##             noheaders=2, # keine header f�r edit bzw. view icon
##             daten= [[is_binary(dok['mtyp']) and h.Dummy() or
##                      h.Icon(href=
##                             "gruppenkarte?gruppeid=%(gruppe_id)d&dokid=%(id)d&file=updgrverm" % dok,
##                             icon= "/ebkus/ebkus_icons/edit_button.gif",
##                             tip= 'Dokument bearbeiten'),
##                      h.Icon(href="dokview?gruppeid=%(gruppe_id)d&dokid=%(id)d" % dok,
##                             target="_new",
##                             icon= "/ebkus/ebkus_icons/view_details.gif",
##                             tip= 'Dokument ansehen'),
##                      h.Datum(date=dok.getDate('v')),
##                      h.String(string="%(art__name)s: %(betr)s" % dok),
##                      h.String(string="%(mit_id__na)s" % dok)]
##                     for dok in dokumente_list],
##             buttons=[h.Button(value="Hinzuf�gen",
##                               tip="Dokument hinzuf�gen (hochladen)",
##                               onClick=
##                               "go_to_url('upload?gruppeid=%(id)s')" % gruppe,
##                             ),
##                      h.Button(value="Drucken (TXT)",
##                               tip="Dokumente im Text-Format zum Drucken zusammenstellen",
##                               onClick=
##                               "go_to_url('newXX dokview2?gruppeid=%(id)d&art=anotiz')" % gruppe,
##                             ),
##                      h.Button(value="Drucken (PDF)",
##                               tip="Dokumente im PDF-Format zum Drucken zusammenstellen",
##                               onClick=
##                               "go_to_url('newXX printgr_pdf?gruppeid=%(id)d&art=anotiz')" % gruppe,
##                             ),
##                      ],
##             )

##         res = h.FormPage(
##             title='Gruppendokumente',
##             help='gruppendoumente', # TODO hier muss neues Kapitel 'Gruppendokumente' rein
##             breadcrumbs = (('Hauptmen�', 'menu'),
##                            ('Gruppenmen�', 'menugruppe'),
##                            ),
##             rows=(menu,
##                   dokumente,
##                   )
##             )
##         return res.display()

class grdok(_dok):
    """Dokumentenkarte."""
    permissions = Request.DOKVIEW_PERM
    einfuege_oder_update_operationen = {
      'uploadgreinf' : ('gruppeid', Gruppe),
      'dokgreinf' : ('gruppeid', Gruppe),
      'updgrvermeinf' : ('gruppeid', Gruppe),
      'removegrdoks' : ('gruppeid', Gruppe)
      }
    def _display_dokkarte(self):
        gruppeid = self.form.get('gruppeid')
        gruppe = Gruppe(gruppeid)
        dokumente_list = GruppendokumentList(
            where = 'gruppe_id = %s and art != %s'
            % (gruppe['id'], cc('dokart', 'bnotiz')),
            order = 'vy,vm,vd')
        beraternotiz_list = GruppendokumentList(
            where = 'gruppe_id = %s and art = %s and mit_id = %s' %
            (gruppe['id'], cc('dokart', 'bnotiz'), self.mitarbeiter['id']),
            order = 'vy,vm,vd')
        
        menu = h.FieldsetInputTable(
            daten=[[
            h.Button(value="Hauptmen�",
                   tip="Zum Hauptmen�",
                   onClick="go_to_url('menu')",
                   ),
            h.Button(value="Gruppenmen�",
                   tip="Zum Gruppenmen�",
                   onClick="go_to_url('menugruppe')",
                   ),
            h.Button(value="Gruppenkarte",
                     tip="Gruppenkarte ansehen",
                     class_='buttonbig',
                     onClick="go_to_url('grkarte?gruppeid=%(id)s')" % gruppe,
                   ),
            h.SelectGoto(name='Auswahl1',
                         options =
"""<option value="nothing">[ Neu ]</option>
<option value="gruppeneu">Neue Gruppe</option>
<option value="gruppeteilnausw?gruppeid=%(id)s">Teilnehmer hinzuf�gen</option>
<option value="vermneu?gruppeid=%(id)s">Dokument erstellen</option>
<option value="upload?gruppeid=%(id)s">Dokument importieren</option>
""" % gruppe
                         ),
            ]],
            )
        buttons_neu = h.FieldsetInputTable(
            daten=[[
            h.Button(value="Dokument erstellen",
                     tip="Neues Textdokument erstellen",
                     class_='buttonbig',
                     onClick="go_to_url('vermneu?gruppeid=%(id)s')" % gruppe,
                   ),
            h.Button(value="Dokument importieren",
                     tip="Vorhandenes Dokument importieren",
                     onClick="go_to_url('upload?gruppeid=%(id)s')" % gruppe,
                     class_='buttonbig',
                   ),
            ]],
            )
        dokumente = self.get_dokumenten_tabelle(
            legend='Dokumente',
            dokumente_list=dokumente_list,
            cgi_name='gruppeid',
            db_name='gruppe_id',
            container=gruppe,
            aktueller_fall=None,
            art='anotiz')
        notizen = self.get_dokumenten_tabelle(
            legend='Beraternotizen',
            dokumente_list=beraternotiz_list,
            cgi_name='gruppeid',
            db_name='gruppe_id',
            container=gruppe,
            aktueller_fall=None,
            art='bnotiz')

##         dokumente = h.FieldsetDataTable(
##             legend= 'Dokumente',
##             headers= ('Datum', 'Betreff', 'Aufgenommen von'),
##             noheaders=2, # keine header f�r edit bzw. view icon
##             daten= [[is_binary(dok['mtyp']) and h.Dummy() or
##                      h.Icon(href=
##                             "gruppenkarte?gruppeid=%(gruppe_id)d&dokid=%(id)d&file=updgrverm" % dok,
##                             icon= "/ebkus/ebkus_icons/edit_button.gif",
##                             tip= 'Dokument bearbeiten'),
##                      h.Icon(href="dokview?gruppeid=%(gruppe_id)d&dokid=%(id)d" % dok,
##                             target="_new",
##                             icon= "/ebkus/ebkus_icons/view_details.gif",
##                             tip= 'Dokument ansehen'),
##                      h.Datum(date=dok.getDate('v')),
##                      h.String(string="%(art__name)s: %(betr)s" % dok),
##                      h.String(string="%(mit_id__na)s" % dok)]
##                     for dok in dokumente_list],
##             buttons=[h.Button(value="Hinzuf�gen",
##                               tip="Dokument hinzuf�gen (hochladen)",
##                               onClick=
##                               "go_to_url('upload?gruppeid=%(id)s')" % gruppe,
##                             ),
##                      h.Button(value="Drucken (TXT)",
##                               tip="Dokumente im Text-Format zum Drucken zusammenstellen",
##                               onClick=
##                               "go_to_url('newXX dokview2?gruppeid=%(id)d&art=anotiz')" % gruppe,
##                             ),
##                      h.Button(value="Drucken (PDF)",
##                               tip="Dokumente im PDF-Format zum Drucken zusammenstellen",
##                               onClick=
##                               "go_to_url('newXX printgr_pdf?gruppeid=%(id)d&art=anotiz')" % gruppe,
##                             ),
##                      ],
##             )

        res = h.FormPage(
            title='Gruppendokumente',
            help='gruppendoumente', # TODO hier muss neues Kapitel 'Gruppendokumente' rein
            breadcrumbs = (('Hauptmen�', 'menu'),
                           ('Gruppenmen�', 'menugruppe'),
                           ),
            rows=(menu,
                  self.get_gruppendaten_kurz(gruppe),
                  dokumente,
                  notizen,
                  buttons_neu,
                  )
            )
        return res.display()
        
    def processForm(self, REQUEST, RESPONSE):
        file = self.form.get('file')
        if not file or file == 'grdok':
            gruppeid = self.form.get('gruppeid')
            if not gruppeid:
                self.last_error_message = "Keine Men&uuml;auswahl erhalten"
                return self.EBKuSError(REQUEST, RESPONSE)
            return self._display_dokkarte()
        if self.einfuege_oder_update_operationen.get(file):
            gruppeid = self.einfuegen_oder_update(file, 'gruppe__id')
            RESPONSE.redirect('grdok?gruppeid=%s' % gruppeid)
            return ''
        return self.ebkus.dispatch(file, REQUEST, RESPONSE)
        
class kldok(_dok):
    """Dokumentenkarte."""
    permissions = Request.DOKVIEW_PERM
    einfuege_oder_update_operationen = {
      'uploadeinf' : ('fallid', Fall),
      'dokeinf' : ('fallid', Fall),
      'removedoks' : ('fallid', Fall),
      'updvermeinf' : ('fallid', Fall),
      }
    def processForm(self, REQUEST, RESPONSE):
        file = self.form.get('file')
        if not file or file == 'kldok':
            fallid = self.form.get('fallid')
            akid = self.form.get('akid')
            if not (fallid or akid):
                self.last_error_message = "Keine Men&uuml;auswahl erhalten"
                return self.EBKuSError(REQUEST, RESPONSE)
            return self._display_dokkarte()
        if self.einfuege_oder_update_operationen.get(file):
            akid = self.einfuegen_oder_update(file, 'akte__id')
            RESPONSE.redirect('kldok?akid=%s' % akid)
            return ''
        return self.ebkus.dispatch(file, REQUEST, RESPONSE)
        
    def _display_dokkarte(self):
        fallid = self.form.get('fallid')
        akid = self.form.get('akid')
        if akid:
            akte = Akte(akid)
        else:
            akte = Fall(fallid)['akte']
        faelle = akte['faelle']
        faelle.sort('bgy', 'bgm', 'bgd')
        letzter_fall = akte['letzter_fall']
        aktueller_fall = akte['aktueller_fall']
        wiederaufnehmbar =  akte['wiederaufnehmbar']
        
        dokumente_list = []
        beraternotiz_list = []
        for f in faelle:
            # alle Dokumente des Falles, die nicht Beraternotiz sind
            dokumente_list += DokumentList(
                where = 'fall_id = %s and art != %s'
                % (f['id'], cc('dokart', 'bnotiz')),
                order = 'vy,vm,vd')
            # alle Dokumente des Falles, die Beraternotizen sind und vom
            # Benutzer selber angelegt wurden
            # Beraternotizen anderer Mitarbeiter sind also nicht sichtbar
            # TODO ist das richtig??
            beraternotiz_list += DokumentList(
                where = 'fall_id = %s and art = %s and mit_id = %s' %
                (f['id'], cc('dokart', 'bnotiz'), self.mitarbeiter['id']),
                order = 'vy,vm,vd')

        menu = h.FieldsetInputTable(
            daten=[[
            h.Button(value="Hauptmen�",
                   tip="Zum Hauptmen�",
                   onClick="go_to_url('menu')",
                   ),
            h.Button(value="Klientenkarte",
                   tip="Klientenkarte zeigen",
                   onClick="go_to_url('klkarte?akid=%(id)s')" % akte,
                   ),
            self.get_button_klienten_neu(aktueller_fall, wiederaufnehmbar, letzter_fall),
            self.get_button_klienten_anzeige(aktueller_fall, letzter_fall),
            ]],
            )
        if aktueller_fall:
            buttons_neu = h.FieldsetInputTable(
                daten=[[
                h.Button(value="Dokument erstellen",
                         tip="Neues Textdokument erstellen",
                         onClick="go_to_url('vermneu?fallid=%(id)s')" % aktueller_fall,
                         class_='buttonbig',
                       ),
                h.Button(value="Dokument importieren",
                         tip="Vorhandenes Dokument importieren",
                         onClick="go_to_url('upload?fallid=%(id)s')" % aktueller_fall,
                         class_='buttonbig',
                       ),
                ]],
                )
        else:
            buttons_neu = None
        dokumente = self.get_dokumenten_tabelle(
            legend='Dokumente',
            dokumente_list=dokumente_list,
            cgi_name='fallid',
            db_name='fall_id',
            container=aktueller_fall or letzter_fall,
            aktueller_fall=aktueller_fall,
            art='anotiz')
        notizen = self.get_dokumenten_tabelle(
            legend='Beraternotizen',
            dokumente_list=beraternotiz_list,
            cgi_name='fallid',
            db_name='fall_id',
            container=aktueller_fall or letzter_fall,
            aktueller_fall=aktueller_fall,
            art='bnotiz')
##         dokumente = h.FieldsetDataTable(
##             legend= 'Dokumente',
##             headers= ('Datum', 'Betreff', 'Aufgenommen von'),
##             noheaders=2, # keine header f�r edit bzw. view icon
##             daten= [[is_binary(dok['mtyp']) and h.Dummy() or
##                      h.Icon(href=
##                             "updverm?gruppeid=%(gruppe_id)d&dokid=%(id)d" % dok,
##                             icon= "/ebkus/ebkus_icons/edit_text_button.gif",
##                             tip= 'Dokument bearbeiten'),
##                      h.Icon(href="rmdok?gruppeid=%(gruppe_id)d&dokid=%(id)d" % dok,
##                             icon= "/ebkus/ebkus_icons/del_text_button.gif",
##                             tip= 'Dokument l�schen'),
##                      h.Icon(href="dokview?gruppeid=%(gruppe_id)d&dokid=%(id)d" % dok,
##                             target="_new",
##                             icon= "/ebkus/ebkus_icons/view_details.gif",
##                             tip= 'Dokument ansehen'),
##                      h.Datum(date=dok.getDate('v')),
##                      h.String(string="%(art__name)s: %(betr)s" % dok),
##                      h.String(string="%(mtyp__code)s" % dok),
##                      h.String(string="%(mit_id__na)s" % dok)]
##                     for dok in dokumente_list],
##             buttons=[h.Button(value="Hinzuf�gen",
##                               tip="Dokument hinzuf�gen (hochladen)",
##                               onClick=
##                               "go_to_url('upload?gruppeid=%(id)s')" % gruppe,
##                             ),
##                      h.Button(value="Drucken (TXT)",
##                               tip="Dokumente im Text-Format zum Drucken zusammenstellen",
##                               onClick=
##                               "go_to_url('newXX dokview2?gruppeid=%(id)d&art=anotiz')" % gruppe,
##                             ),
##                      h.Button(value="Drucken (PDF)",
##                               tip="Dokumente im PDF-Format zum Drucken zusammenstellen",
##                               onClick=
##                               "go_to_url('newXX printgr_pdf?gruppeid=%(id)d&art=anotiz')" % gruppe,
##                             ),
##                      ],
##             )

        res = h.FormPage(
            title='Klientendokumente',
            help='klientendokumente', # TODO hier muss neues Kapitel 'Klientendokumente' rein
            breadcrumbs = (('Hauptmen�', 'menu'),
                           ),
            rows=(menu,
                  self.get_klientendaten_kurz(aktueller_fall or letzter_fall),
                  dokumente,
                  notizen,
                  buttons_neu,
                  )
            )
        return res.display()

##     def kldok_display(self, akid, fallid = None, mitid=None):
##         "Darstellung der Dokumentenkarte."
        
##         if not akid and fallid:
##             fall = Fall(fallid)
##             akte = Akte(fall['akte_id'])
##         else:
##             akte = Akte(int(akid))
            
##         faelle = akte['faelle']
##         faelle.sort('bgy', 'bgm', 'bgd')
        
##         # Aktueller bzw. letzter Fall, Wiederaufnehmbarkeit
        
##         letzter_fall = akte['letzter_fall']
##         aktueller_fall = akte['aktueller_fall']
        
##         res = []
##         res.append(head_normal_t %("Dokumentenindex der Akte"))
##         res.append(kldok_start_t1)
##         if aktueller_fall:
##             res.append(menuedok_t % aktueller_fall)
##         else:
##             res.append(menuedokzda_t % letzter_fall)
##         res.append(dokausgabe1_t % ('Aktendokumente der Akte %(vn)s %(na)s' %akte))
##         for f in faelle:
##             dokl = DokumentList(where = 'fall_id = %s'
##                                    % (f['id']), order = 'vy,vm,vd')
##             aktendokl = []
##             for d in dokl:
##                 if d['art'] != cc('dokart', 'bnotiz'):
##                     aktendokl.append(d)
##             for a in aktendokl:
##                 if aktueller_fall:
##                     if is_binary(a['mtyp']):
##                         res.append(dokausgabe2_ohne_edit_t % a)
##                     else:
##                         res.append(dokausgabe2_mit_edit_t % a)
##                 else:
##                     res.append(dokausgabe2b_t % a)
##         res.append(dokausgabe3_t)
##         res.append(dokausgabe1_t % ('Beraternotizen der Akte %(vn)s %(na)s' %akte))
##         for f in faelle:
##             beraternotizen = DokumentList(where = 'fall_id = %s and art = %s and mit_id = %s'% (f['id'], cc('dokart', 'bnotiz'), self.mitarbeiter['id']),
##                                    order = 'vy,vm,vd')
##             for b in beraternotizen:
##                 if aktueller_fall:
##                     if is_binary(b['mtyp']):
##                         res.append(dokausgabe2_ohne_edit_t % b)
##                     else:
##                         res.append(dokausgabe2_mit_edit_t % b)
##                 else:
##                     res.append(dokausgabe2b_t % b)
##         res.append(dokausgabe3_t)
##         if beraternotizen or aktendokl:
##             res.append(dokausgabe1_t % ('Printausgabe'))
##             if aktendokl and aktueller_fall:
##                 res.append(dokausgabe5_t % aktueller_fall)
##             elif aktendokl and letzter_fall:
##                 res.append(dokausgabe5_t % letzter_fall)
##             if beraternotizen and aktueller_fall:
##                 res.append(dokausgabe4_t % aktueller_fall)
##             elif beraternotizen and letzter_fall:
##                 res.append(dokausgabe4_t % letzter_fall)
##             res.append(dokausgabe6_t)
##             ##*************************************************************************
##             ##  Entfernt wegen UNIX Kommando agrep. Funktioniert nicht unter Win
##             ##
##             ##  MastaleckT 08.03.2002
##             ##*************************************************************************
##             #res.append(dokausgabe7a_t % ('Suche in den Texten', ''))
##             #if aktueller_fall:
##             #  res.append(formhiddennamevalues_t % ({'name' : 'fallid' ,
##             #                                      'value' : aktueller_fall['id']}))
##             #elif letzter_fall:
##             #  res.append(formhiddennamevalues_t % ({'name' : 'fallid' ,
##             #                                      'value' : letzter_fall['id']}))
##             #res.append(dokausgabe7b_t)
##         res.append(dokkarte_ende_t)
##         return string.join(res, '')
        
        
