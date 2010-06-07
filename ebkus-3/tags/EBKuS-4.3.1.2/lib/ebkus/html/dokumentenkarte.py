# coding: latin-1

"""Module für die Dokumentenkarte."""

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
    def einfuegen_oder_update(self, file, path):
        function = getattr(ebupd, file)
        function(self.form)
        # Dies ist eine Art die Akte herauszufinden, auf die
        # sich das Einfuegen oder das Update bezog.
        # Es wäre vielleicht besser, die akid immer als
        # hidden Variable mitzuführen.
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
                # Falldokumente nur wenn sie zu einem aktuellem Fall gehören
                return dok['fall_id'] == aktueller_fall['id']
            return False
        return h.FieldsetDataTable(
            legend=legend,
            headers=('Datum', 'Betreff', 'Typ', 'Aufgenommen von'),
            noheaders=3, # keine header für edit, del, view icon
            daten= [[editierbar(dok, aktueller_fall) and
                     h.Icon(href=upd % dok,
                            icon= "/ebkus/ebkus_icons/edit_text_button.gif",
                            tip= 'Dokument bearbeiten') or
                     h.Dummy(),
                     editierbar(dok, aktueller_fall) and
                     h.Icon(href=rm % dok,
                            icon= "/ebkus/ebkus_icons/del_text_button.gif",
                            tip= 'Dokument löschen') or
                     h.Dummy(),
                     h.Icon(href=view % dok,
                            target="_blank",
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
            h.Button(value="Hauptmenü",
                   tip="Zum Hauptmenü",
                   onClick="go_to_url('menu')",
                   ),
            h.Button(value="Gruppenmenü",
                   tip="Zum Gruppenmenü",
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
<option value="gruppeteilnausw?gruppeid=%(id)s">Teilnehmer hinzufügen</option>
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


        res = h.FormPage(
            title='Gruppendokumente',
            help='gruppendoumente', # TODO hier muss neues Kapitel 'Gruppendokumente' rein
            breadcrumbs = (('Hauptmenü', 'menu'),
                           ('Gruppenmenü', 'menugruppe'),
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
            h.Button(value="Hauptmenü",
                   tip="Zum Hauptmenü",
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

        res = h.FormPage(
            title='Klientendokumente',
            help='klientendokumente', # TODO hier muss neues Kapitel 'Klientendokumente' rein
            breadcrumbs = (('Hauptmenü', 'menu'),
                           ),
            rows=(menu,
                  self.get_klientendaten_kurz(aktueller_fall or letzter_fall),
                  dokumente,
                  notizen,
                  buttons_neu,
                  )
            )
        return res.display()

        
        
