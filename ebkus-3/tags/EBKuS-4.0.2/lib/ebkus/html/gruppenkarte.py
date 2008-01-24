# coding: latin-1

"""Module für die Gruppenkarte."""
from ebkus.app import Request
from ebkus.app import ebupd
from ebkus.app.ebapi import Gruppe
import ebkus.html.htmlgen as h
from ebkus.html.akte_share import akte_share

class grkarte(Request.Request, akte_share):
    permissions = Request.GRUPPENKARTE_PERM
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
    
    def processForm(self, REQUEST, RESPONSE):
        file = self.form.get('file')
        
        # Fall 1 Gruppenkarte direkt darstellen
        
        if not file or file == 'grkarte':
            gruppeid = self.form.get('gruppeid')
            mitid = self.mitarbeiter['id']
            if gruppeid:
                gruppeid = int(gruppeid)
            else:
                self.last_error_message = "Keine Men&uuml;auswahl erhalten"
                return self.EBKuSError(REQUEST, RESPONSE)
            return self.gruppenkarte_display(gruppeid, mitid)
            
        # Fall 2 erst einfuegen oder updaten, dann Klientenkarte darstellen
        if self.einfuege_oder_update_operationen.get(file):
            gruppeid = self.einfuegen_oder_update(file)
            # damit Klientenkarte nicht als Ergebnis eines POST
            # dargestellt wird
            RESPONSE.redirect('grkarte?gruppeid=%s' % gruppeid)
            return ''
            # Fall 3 Dokumenten- Update- oder Einfuegeformular anzeigen
            # Folgende URLs haben denselben Effekt:
            # 1)  http://localhost/efb/ebs/gruppenkarte?file=gruppeneu
            # 2)  http://localhost/efb/ebs/gruppeneu
            # Variante 1) nützlich wg. Aufruf aus menu.
            # Könnte auch mir redirect gelöst werden.
        if file == 'grdok':
            gruppeid = self.form.get('gruppeid')
            if not gruppeid:
                self.last_error_message = "Keine Men&uuml;auswahl erhalten"
                return self.EBKuSError(REQUEST, RESPONSE)
            RESPONSE.redirect('grdok?gruppeid=%s' % gruppeid)
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
        bezugspersongruppe_list = gruppe['bezugspersonen']
        bezugspersongruppe_list.sort('bezugsp_id__na','bezugsp_id__vn')
        fallgruppe_list = gruppe['faelle']
        fallgruppe_list.sort('fall_id__akte_id__na','fall_id__akte_id__vn')

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
            h.Button(value="Gruppendokumente",
                     tip="Gruppendokumente ansehen",
                     class_='buttonbig',
                     onClick="go_to_url('grdok?gruppeid=%(id)s')" % gruppe,
                   ),
            h.SelectGoto(name='Auswahl1',
                         options =
"""<option value="nothing">[ Neu ]</option>
<option value="gruppeneu">Neue Gruppe</option>
<option value="gruppeteilnausw?gruppeid=%(id)s">Teilnehmer hinzufügen</option>
<option value="vermneu?gruppeid=%(id)s">Dokument erstellen</option>
<option value="upload?gruppeid=%(id)s">Dokument importieren</option>
""" % gruppe),
##             h.SelectGoto(name='Auswahl2',
##                          options =
## """<option value="nothing">[ Anzeige ]</option>"""),
        ]]
        )
        teilnehmer = h.FieldsetDataTable(
            legend='Teilnehmer',
            headers=('Name', 'Art', 'Von', 'Bis'),
            daten=
            [[h.Icon(href='updteiln?fallgrid=%(id)d' % fg,
                     icon="/ebkus/ebkus_icons/teilnehmer_edit_button.gif",
                     tip='Teilnahme bearbeiten'),
              h.Icon(href='rmteiln?fallgrid=%(id)d' % fg,
                     icon="/ebkus/ebkus_icons/teilnehmer_del_button.gif",
                     tip='Teilnehmer entfernen'),
##               h.Icon(href='#',
##                      onClick="view_details('viewpers?akid=%(fall__akte__id)d')" % fg,
##                      icon= "/ebkus/ebkus_icons/view_details.gif",
##                      tip= 'Details für Klienten ansehen'),
              h.Icon(href='viewpers?akid=%(fall__akte__id)d' % fg,
                     target='_blank',
                     icon= "/ebkus/ebkus_icons/view_details.gif",
                     tip= 'Details für Klienten ansehen'),
              h.Link(string="%(fall__akte__vn)s  %(fall__akte__na)s" % fg,
                     url='klkarte?akid=%(fall__akte__id)s' %fg,
                     target='_blank', # TODO soll das in ein anderes Fenster?
                     tip='Klientenkarte zeigen',
                     ),
              h.String(string="Klient"),
              h.Datum(date=fg.getDate('bg')),
              h.Datum(date=fg.getDate('e')),
              ] for fg in fallgruppe_list]
            +
            [[h.Icon(href='updteiln?bzpgrid=%(id)d' % bg,
                     icon="/ebkus/ebkus_icons/teilnehmer_edit_button.gif",
                     tip='Teilnahme bearbeiten'),
            h.Icon(href='rmteiln?bzpgrid=%(id)d' % bg,
                     icon="/ebkus/ebkus_icons/teilnehmer_del_button.gif",
                     tip='Teilnehmer entfernen'),
##               h.Icon(href='#',
##                      onClick="view_details('viewpers?bpid=%(bezugsp_id)d')" % bg,
##                      icon="/ebkus/ebkus_icons/view_details.gif",
##                      tip='Details für Bezugsperson ansehen'),
              h.Icon(href='viewpers?bpid=%(bezugsp_id)d' % bg,
                     target='_blank',
                     icon="/ebkus/ebkus_icons/view_details.gif",
                     tip='Details für Bezugsperson ansehen'),
              h.Link(string="%(bezugsp__vn)s  %(bezugsp__na)s" % bg,
                     url='klkarte?akid=%(bezugsp__akte__id)s' % bg,
                     target='_blank', # TODO soll das in ein anderes Fenster?
                     tip='Klientenkarte zeigen',
                     ),
              h.String(string="%(bezugsp__verw__name)s" % bg),
              h.Datum(date=bg.getDate('bg')),
              h.Datum(date=bg.getDate('e')),
            ] for bg in bezugspersongruppe_list],
            button=h.Button(value= "Hinzufügen",
                            tip= "Teilnehmer hinzufügen",
                            onClick= "go_to_url('gruppeteilnausw?gruppeid=%(id)d')" % gruppe,
                            ),
            )
        res = h.FormPage(
            title='Gruppenkarte',
            name="",action="",method="",hidden=(),
            help=True,
            breadcrumbs = (('Hauptmenü', 'menu'),
                           ('Gruppenmenü', 'menugruppe'),
                           ),
            rows=(menu,
                  self.get_gruppendaten(gruppe, readonly=True),
                  teilnehmer,
                  ),
            )
        return res.display()
