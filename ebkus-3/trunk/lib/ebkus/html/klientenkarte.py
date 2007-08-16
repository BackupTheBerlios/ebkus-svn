# coding: latin-1

"""Module für die Klientenkarte."""
# TODO an die Standards anpassen
from ebkus.config import config
from ebkus.app import Request
from ebkus.app import ebupd
from ebkus.app import ebapi
from ebkus.html.htmlgen import Base, Form, FormPage, Fieldset, FieldsetDataTable, Tr, Pair, \
     FieldsetInputTable, Button, Datum, String, Icon, IconDead, SelectGoto, Klientendaten, \
     TextItem, DummyItem

import ebkus.html.htmlgen as h

from ebkus.app.ebapih import get_all_codes
from ebkus.app_surface.klientenkarte_templates import *
from ebkus.app_surface.standard_templates import *

from ebkus.html.akte_share import akte_share

class klkarte(Request.Request, akte_share):
    """Klientenkarte."""
    
    permissions = Request.KLKARTE_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        file = self.form.get('file')
        # Fall 1 Klientenkarte direkt darstellen
        if not file or file == 'klkarte':
            fallid = self.form.get('fallid')
            akid = self.form.get('akid')
            mitid = self.mitarbeiter['id']
            if akid:
                akid = int(akid)
            elif fallid:
                fallid = int(fallid)
                fall = ebapi.Fall(fallid)
                akid = fall['akte_id']
            else:
                return h.Meldung(
                    legend='Keine Men&uuml;auswahl erhalten!',
                    zeilen=('Es wurde nichts aus dem Men&uuml; ausgew&auml;hlt.',)
                    ).display()
            return self.klkarte_display(akid)
            
            # Fall 2 erst einfuegen oder updaten, dann Klientenkarte darstellen
        if self.einfuege_oder_update_operationen.get(file):
            akid = self.einfuegen_oder_update(file)
            # damit Klientenkarte nicht als Ergebnis eines POST
            # dargestellt wird
            RESPONSE.redirect('klkarte?akid=%s' % akid)
            return ''
            
            # Fall 3 Dokumenten- Update- oder Einfuegeformular anzeigen
            # Folgende URLs haben denselben Effekt:
            # 1)  http://localhost/efb/ebs/klkarte?file=akteneu
            # 2)  http://localhost/efb/ebs/akteneu
            # Variante 1) nützlich wg. Aufruf aus menu.
            # Könnte auch mit redirect gelöst werden.
            
        if file == 'dokkarte':
            fallid = self.form.get('fallid')
            if fallid:
                    fallid = int(fallid)
            else:
                return h.Meldung(
                    legend='Keine Men&uuml;auswahl erhalten!',
                    zeilen=('Es wurde nichts aus dem Men&uuml; ausgew&auml;hlt.',),
                    ).display()
            RESPONSE.redirect('dokkarte?fallid=%s' % fallid)
            return ''
        if file == 'updjghform' or file == 'updfsform':
            fallid = self.form.get('fallid')
            if not fallid:
                return h.Meldung(
                    legend='Keine Men&uuml;auswahl erhalten!',
                    zeilen=('Es wurde nichts aus dem Men&uuml; ausgew&auml;hlt.',),
                    ).display()
        return self.ebkus.dispatch(file, REQUEST, RESPONSE)
        
    einfuege_oder_update_operationen = {
      'akteeinf': ('akid', ebapi.Akte),
      'perseinf': ('akid', ebapi.Akte),
      'einreinf': ('akid', ebapi.Akte),
      'anmeinf': ('fallid', ebapi.Fall),
      'leisteinf': ('fallid', ebapi.Fall),
      'bkonteinf': ('fallid', ebapi.Fall),
      'zusteinf': ('fallid', ebapi.Fall),
      'zdaeinf': ('fallid', ebapi.Fall),
      #'updfall': ('gfall', ebapi.Fall),
      'updakte': ('akid', ebapi.Akte),
      'updpers': ('bpid', ebapi.Bezugsperson),
      'updeinr': ('einrid', ebapi.Einrichtungskontakt),
      'updanm': ('anmid', ebapi.Anmeldung),
      'updleist': ('leistid', ebapi.Leistung),
      'updbkont': ('bkontid', ebapi.Beratungskontakt),
      'updzust': ('zustid', ebapi.Zustaendigkeit),
      'updfall': ('fallid', ebapi.Fall),
      'waufneinf': ('fallid', ebapi.Fall),
      'zdareinf': ('fallid', ebapi.Fall),
      'fseinf': ('fsid', ebapi.Fachstatistik),
      'updfs': ('fsid', ebapi.Fachstatistik),
      #'jgheinf': ('jghid', ebapi.Jugendhilfestatistik), # wg. jgh07
      'jgheinf': ('fallid', ebapi.Fall),
      'jgh07einf': ('fallid', ebapi.Fall),
      #'updjgh': ('jghid', ebapi.Jugendhilfestatistik),  # wg. jgh07
      'updjgh': ('fallid', ebapi.Fall),
      'updjgh07': ('fallid', ebapi.Fall),
      'fseinf': ('fsid', ebapi.Fachstatistik)
      }
    
    def einfuegen_oder_update(self, file):
        # API Funktion aufrufen
        function = getattr(ebupd, file)
        function(self.form)
        # Akte id ermitteln um klkarte anzeigen zu können
        id_name, klass = self.einfuege_oder_update_operationen.get(file)
        akid = klass(int(self.form[id_name]))['akte__id']
        return akid
        


    def klkarte_display(self, akid):
        "Darstellung der Klientenkarte."
        
        akte = ebapi.Akte(akid)
        bezugspersonen_list = akte['bezugspersonen']
        einrichtungskontakte_list = akte['einrichtungen']
        faelle = akte['faelle']
        
        faelle.sort('bgy', 'bgm', 'bgd')
        bezugspersonen_list.sort('verw__sort')
        einrichtungskontakte_list.sort('status', 'na')
        leistungen_list = []
        zustaendigkeiten_list = []
        beratungskontakte_list = []
        anmeldekontakte_list = []
        fachstatistik_list = []
        jugendhilfestatistik_list = []
        fallgruppen_list = []
        bezugspersongruppen_list = []
        for f in faelle:
            leistungen_list += f['leistungen']
            zustaendigkeiten_list += f['zustaendigkeiten']
            beratungskontakte_list += f['beratungskontakte']
            anmeldekontakte_list += f['anmeldung']
            fachstatistik_list += f['fachstatistiken']
            jugendhilfestatistik_list += f['jgh_statistiken']
            jugendhilfestatistik_list += f['jgh07_statistiken']
            fallgruppen_list +=  f['gruppen']
        for b in bezugspersonen_list:
            bezugspersongruppen_list += b['gruppen']
        letzter_fall = akte['letzter_fall']
        aktueller_fall = akte['aktueller_fall']
        wiederaufnehmbar =  akte['wiederaufnehmbar']
        
        menu = h.Fieldset(content=Tr(cells=(
            h.Button(value="Hauptmenü",
                   tip="Zum Hauptmenü",
                   onClick="go_to_url('menu')",
                   ),
            h.Button(value="Gruppenmenü",
                   tip="Zum Gruppenmenü",
                   onClick="go_to_url('menugruppe')",
                   ),
            (aktueller_fall and
             h.SelectGoto(name='Auswahl1', options =
"""<option value="nothing">[ Neu ]</option>
<option value="akteneu?file=aktene">- Neuaufnahme</option>
<option value="persneu?akid=%(akte_id)s&fallid=%(id)s">- Familie</option>
<option value="einrneu?akid=%(akte_id)s&fallid=%(id)s">- Einrichtung</option>
<option value="anmneu?akid=%(akte_id)s&fallid=%(id)s">- Anmeldung</option>
<option value="leistneu?akid=%(akte_id)s&fallid=%(id)s">- Leistung</option>
<option value="bkontneu?akid=%(akte_id)s&fallid=%(id)s">- Beratungskontakt</option>
<option value="zustneu?akid=%(akte_id)s&fallid=%(id)s">- Bearbeiter</option>
<option value="vermneu?akid=%(akte_id)s&fallid=%(id)s">- Vermerk</option>
<option value="upload?akid=%(akte_id)s&fallid=%(id)s">- Dateiimport</option>
<option value="fsneu?akid=%(akte_id)s&fallid=%(id)s">- Fachstatistik</option>
<option value="jgh07neu?akid=%(akte_id)s&fallid=%(id)s">- Bundesstatistik</option>
<option value="zda?akid=%(akte_id)s&fallid=%(id)s">- zu den Akten</option>
""" % aktueller_fall)
                  or wiederaufnehmbar and
                  h.SelectGoto(name='Auswahl1', options =
"""<option value="nothing">[ Neu ]</option>
<option value="akteneu?file=aktene">- Neuaufnahme</option>
<option value="waufnneu?akid=%(akte_id)d&fallid=%(id)d">- Wiederaufnahme</option>
""" % letzter_fall)
                  or
                  h.SelectGoto(name='Auswahl1', options =
"""<option value="nothing">[ Neu ]</option>
<option value="akteneu?file=aktene">- Neuaufnahme</option>
<option value="zdar?akid=%(akte_id)d&fallid=%(id)d">- zdA R&uuml;ckg&auml;ngig</option>
""" % letzter_fall)),

            (aktueller_fall and
             h.SelectGoto(name='Auswahl2', options =
"""<option value="nothing">[ Anzeige ]</option>
<option value="newXX vorblatt?akid=%(akte_id)d&fallid=%(id)d">- Vorblatt</option>
<option value="dokkarte?akid=%(akte_id)d&fallid=%(id)d">- Akte</option>
<option value="formabfr3">- Suche</option>
<option value="wordexport?akid=%(akte_id)d">- Word-Export</option>
""" % aktueller_fall)
             or
             h.SelectGoto(name='Auswahl2', options =
"""<option value="nothing">[ Anzeige ]</option>
<option value="vorblatt?akid=%(akte_id)d&fallid=%(id)d">- Vorblatt</option>
<option value="dokkarte?akid=%(akte_id)d&fallid=%(id)d">- Akte</option>
<option value="formabfr3">- Suche</option>
""" % letzter_fall )),
            )))

        klientendaten = self.get_klientendaten_readonly(
            akte, 
            button=h.Button(value="Bearbeiten",
                            tip="Klientenstammdaten bearbeiten",
                            onClick= "go_to_url('updakte?akid=%(id)s')" % akte)
            )
        bezugspersonen = self.get_bezugspersonen(bezugspersonen_list, aktueller_fall,
                                                 edit_button=True, view_button=True)
        leistungen = h.FieldsetDataTable(
            legend= 'Leistungen',
            headers= ('Mitarbeiter', 'Leistung', 'Am', 'Bis'),
            daten= [[(aktueller_fall == leist['fall'] and
                      h.Icon(href= 'updleist?fallid=%(fall_id)d&leistid=%(id)d' % leist,
                           icon= "/ebkus/ebkus_icons/edit_button.gif",
                           tip= 'Leistung bearbeiten')
                      or
                      h.IconDead(icon= "/ebkus/ebkus_icons/edit_button_inaktiv_locked.gif",
                               tip= 'Funktion gesperrt')),
                     h.String(string= leist['mit_id__na']),
                     h.String(string= leist['le__name']),
                     h.Datum(date=leist.getDate('bg')),
                     h.Datum(date=leist.getDate('e')),
                     ]
                    for leist in leistungen_list],
            button= (aktueller_fall and
                     h.Button(value= "Hinzufügen",
                            tip= "Leistung hinzufügen",
                         onClick= "go_to_url('leistneu?akid=%(id)d&fallid=%(aktueller_fall__id)d')" % akte,
                            ) or None),
            )
        beratungskontakte = h.FieldsetDataTable(
            legend= 'Beratungskontakte',
            headers= ('Mitarbeiter', 'Art', 'Datum', 'Dauer', 'Notiz'),
            daten= [[(aktueller_fall == bkont['fall'] and
                      h.Icon(href= 'updbkont?fallid=%(fall_id)d&bkontid=%(id)d' % bkont,
                           icon= "/ebkus/ebkus_icons/edit_button.gif",
                           tip= 'Beratungskontakt bearbeiten')
                      or
                      h.IconDead(icon= "/ebkus/ebkus_icons/edit_button_inaktiv_locked.gif",
                               tip= 'Funktion gesperrt')),
                       h.String(string= bkont['mit_id__na']),
                       h.String(string= bkont['art__name']),
                       h.Datum(day=   bkont['kd'],
                             month= bkont['km'],
                             year=  bkont['ky']),
                       h.String(string= bkont['dauer__name']),
                       h.String(string= bkont['no'])]
                    for bkont in beratungskontakte_list],
            button= (aktueller_fall and
                     h.Button(value= "Hinzufügen",
                            tip= "Beratungskontakt hinzufügen",
                        onClick= "go_to_url('bkontneu?akid=%(id)d&fallid=%(aktueller_fall__id)d')" % akte,
                            ) or None),
            )
        stand = h.FieldsetDataTable(
            legend= 'Stand',
            headers= ('Fallnummer', 'Beginn', 'z.d.A.'),
            daten= [[(fall == aktueller_fall and
                      h.Icon(href= 'updfall?akid=%(akte_id)d&fallid=%(id)d' % fall,
                           icon= "/ebkus/ebkus_icons/edit_button.gif",
                           tip= 'Fallstatus bearbeiten')
                      or
                      h.IconDead(icon= "/ebkus/ebkus_icons/edit_button_inaktiv_locked.gif",
                               tip= 'Funktion gesperrt')),
                     h.String(string=fall['fn']),
                     h.Datum(day=fall['bgd'],
                           month= fall['bgm'],
                           year=  fall['bgy']),
                     h.Datum(day=fall['zdad'],
                           month= fall['zdam'],
                           year=  fall['zday'])]
                    for fall in faelle],
            button= (aktueller_fall and
                     h.Button(value= "Zu den Akten",
                            tip= "Fall abschließen",
                            onClick= "go_to_url('zda?akid=%(akte_id)s&fallid=%(id)d')" % aktueller_fall,)
                     or wiederaufnehmbar and 
                     h.Button(value= "Wiederaufnahme",
                            tip= "Fall wiederaufnehmen",
                          onClick= "go_to_url('waufnneu?akid=%(akte_id)s&fallid=%(id)d')" % letzter_fall,)
                     or
                     h.Button(value= "ZdA rückgängig",
                            tip= "Fall aktivieren",
                            onClick= "go_to_url('zdar?akid=%(akte_id)s&fallid=%(id)d')" % letzter_fall,)),
            )
        bearbeiter = h.FieldsetDataTable(
            legend= 'Bearbeiter',
            headers= ('Bearbeiter', 'Beginn', 'Ende'),
            daten= [[(zust['fall'] == aktueller_fall and
                      h.Icon(href= 'updzust?fallid=%(fall_id)d&zustid=%(id)d' % zust,
                           icon= "/ebkus/ebkus_icons/edit_button.gif",
                           tip= "Zuständigkeit bearbeiten")
                      or
                      h.IconDead(icon= "/ebkus/ebkus_icons/edit_button_inaktiv_locked.gif",
                               tip= 'Funktion gesperrt')),
                     h.String(string= zust['mit_id__na']),
                     h.Datum(day=   zust['bgd'],
                           month= zust['bgm'],
                           year=  zust['bgy']),
                     h.Datum(day=zust['ed'],
                           month= zust['em'],
                           year=  zust['ey'])]
                    for zust in zustaendigkeiten_list],
            button=(aktueller_fall and
                    h.Button(value= "Hinzufügen",
                           tip= "Neue Zuständigkeit eintragen",
                           onClick= "go_to_url('zustneu?akid=%(akte_id)s&fallid=%(id)d')" % aktueller_fall,)
                    or None),
            )
        anmeldekontakte = h.FieldsetDataTable(
            legend= 'Anmeldungskontakte',
            headers= ('Gemeldet von', 'Gemeldet am', 'Anmeldegrund'),
            daten= [[(aktueller_fall == a['fall'] and
                     h.Icon(href= 'updanm?anmid=%(id)d' % a,
                          icon= "/ebkus/ebkus_icons/edit_button.gif",
                          tip= 'Anmeldungskontakt bearbeiten')
                      or
                      h.IconDead(icon= "/ebkus/ebkus_icons/edit_button_inaktiv_locked.gif",
                               tip= 'Funktion gesperrt')),
                     (aktueller_fall and
                      h.Icon(href= '#',
                           onClick= "view_details('viewanm?anmid=%(id)d')" % a,
                           icon= "/ebkus/ebkus_icons/view_details.gif",
                           tip= 'Anmeldungskontakt ansehen')
                           or
                      h.IconDead(icon= "/ebkus/ebkus_icons/view_details_inaktiv.gif",
                               tip= 'Funktion gesperrt')),
                       h.String(string= a['von']),
                       h.Datum(day=   a['ad'],
                             month= a['am'],
                             year=  a['ay']),
                       h.String(string= a['mg'])]
                       for a in anmeldekontakte_list],
            button= (aktueller_fall and not aktueller_fall['anmeldung'] and
                     h.Button(value= "Hinzufügen",
                            tip= "Anmeldungskontakt hinzufügen",
                            onClick=
                            "go_to_url('anmneu?fallid=%(id)d')" % aktueller_fall,
                            ) or None),
            )

        einrichtungskontakte = h.FieldsetDataTable(
            legend= 'Einrichtungskontakte',
            headers= ('Art', 'Name', 'Telefon 1', 'Telefon 2', 'Aktuell'),
            daten= [[(aktueller_fall and
                      h.Icon(href= 'updeinr?einrid=%(id)d' % e,
                           icon= "/ebkus/ebkus_icons/edit_button.gif",
                           tip= 'Einrichtungskontakt bearbeiten')
                      or
                      h.IconDead(icon= "/ebkus/ebkus_icons/edit_button_inaktiv_locked.gif",
                               tip= 'Funktion gesperrt')),
                     h.String(string= e['insta__name']),
                     h.String(string= e['na']),
                     h.String(string= e['tl1']),
                     h.String(string= e['tl2']),
                     h.String(string= e['status__code'])]
                    for e in einrichtungskontakte_list],
            button= (aktueller_fall and
                     h.Button(value= "Hinzufügen",
                            tip= "Einrichtungskontakt hinzufügen",
                            onClick=
                            "go_to_url('einrneu?fallid=%(id)d')" % aktueller_fall,
                            ) or None),
            )

        notiz_daten = []
        if akte['no']:
            notiz_daten.append([h.String(string= 'AK'),
                          h.String(string= "%(vn)s %(na)s" % akte),
                          h.String(string= akte['no']),
                          h.String(string= ''),
                          ])
        for b in bezugspersonen_list:
            if b['no']:
                notiz_daten.append([h.String(string= 'BP'),
                              h.String(string= "%(vn)s %(na)s" % b),
                              h.String(string= b['no']),
                              h.String(string= b['nobed__name'],
                                     class_=ebapi.cc('notizbed', 't')==b['nobed'] and 'tabledatabold'
                                     or 'tabledata'),
                              ])
        for e in einrichtungskontakte_list:
            if e['no']:
                notiz_daten.append([h.String(string= 'ER'),
                              h.String(string= "%(insta__name)s %(na)s" % e),
                              h.String(string= e['no']),
                              h.String(string= e['nobed__name'],
                                     class_=ebapi.cc('notizbed', 't')==e['nobed'] and 'tabledatabold'
                                     or 'tabledata'),
                              ])
        for a in anmeldekontakte_list:
            if a['no']:
                notiz_daten.append([h.String(string= 'AM'),
                              h.String(string= "%(von)s" % a),
                              h.String(string= a['no']),
                              h.String(string= ''),
                              ])
            
        notizen = h.FieldsetDataTable(
            legend= 'Notizen',
            daten= notiz_daten,
            button=None,
            )

        fachstatistik = h.FieldsetDataTable(
            legend= 'Fachstatistiken',
            headers= ('Fallnummer', 'Jahr',),
            daten= [[h.Icon(href= 'updfs?fsid=%(id)d' % fs,
                          icon= "/ebkus/ebkus_icons/edit_stat_button.gif",
                          tip= 'Fachstatistik bearbeiten'),
                     h.String(string= fs['fall_fn']),
                     h.String(string= fs['jahr'])]
                    for fs in fachstatistik_list],
            button= (aktueller_fall and
                     h.Button(value= "Hinzufügen",
                            tip= "Fachstatistik hinzufügen",
                            onClick=
                            "go_to_url('fsneu?fallid=%(id)d')" % aktueller_fall,
                            ) or None),
            )
        jugendhilfestatistik_list = []
        for f in faelle:
            for js in f['jgh_statistiken']:
                if js['ey']: # warum diese Prüfung?
                    js['action'] = 'updjgh'
                    jugendhilfestatistik_list.append(js)
            for js in f['jgh07_statistiken']:
                if js['bgy']: # warum diese Prüfung?
                    js['action'] = 'updjgh07'
                    jugendhilfestatistik_list.append(js)
        jugendhilfestatistik = h.FieldsetDataTable(
            legend= 'Jugendhilfestatistiken',
            headers= ('Fallnummer', 'Ende'),
            daten= [[h.Icon(href= '%(action)s?jghid=%(id)d' % js,
                          icon= "/ebkus/ebkus_icons/edit_stat_button.gif",
                          tip= 'Jugendhilfestatistik bearbeiten'),
                     h.String(string= js['fall_fn']),
                     h.Datum(month= js['em'],
                           year=  js['ey'])]
                    for js in jugendhilfestatistik_list],
            button= (aktueller_fall and
                     h.Button(value= "Hinzufügen",
                            tip= "Jugendhilfestatistik hinzufügen",
                            onClick=
                            "go_to_url('jgh07neu?fallid=%(id)d')" % aktueller_fall,
                            ) or None),
            )



##         # Alternative Schreibweise
##         daten = []
##         for fg in fallgruppen_list:
##             zeile = []
##             if aktueller_fall:
##                 icon = h.Icon(href='gruppenkarte?gruppeid=%(gruppe_id)s' % fg,
##                             icon="/ebkus/ebkus_icons/edit_grp_button.gif",
##                             tip='Gruppenkarte bearbeiten')
##             else:
##                 icon = h.IconDead(icon="/ebkus/ebkus_icons/edit_grp_button_inaktiv.gif",
##                                 tip='Funktion gesperrt'),
##             zeile.append(icon)
##             zeile.append(h.String(string=fg['gruppe_id__gn']))
##             zeile.append(h.String(string="%(fall__akte__vn)s %(fall__akte__na)s" % fg))
##         fallgruppen = h.FieldsetDataTable(
##             legend='Gruppenkarten des Falls',
##             headers=('Gruppennr.', 'Name',),
##             daten=daten)


        fallgruppen = h.FieldsetDataTable(
            legend='Gruppenkarten des Falls',
            headers=('Gruppennr.', 'Name',),
            daten=[[(aktueller_fall
                     and
                     h.Icon(href='gruppenkarte?gruppeid=%(gruppe_id)s' % fg,
                          icon="/ebkus/ebkus_icons/edit_grp_button.gif",
                          tip='Gruppenkarte bearbeiten')
                     or 
                     h.IconDead(icon="/ebkus/ebkus_icons/edit_grp_button_inaktiv.gif",
                              tip='Funktion gesperrt')),
                    h.String(string=fg['gruppe_id__gn']),
                    h.String(string="%(fall__akte__vn)s %(fall__akte__na)s" % fg)]
                   for fg in fallgruppen_list],
            )
        bezugspersongruppen = h.FieldsetDataTable(
            legend= 'Gruppenkarten der Bezugspersonen',
            headers= ('Gruppennr.', 'Name',),
            daten= [[(aktueller_fall and
                      h.Icon(href= 'gruppenkarte?gruppeid=%(gruppe_id)s' % bg,
                           icon= "/ebkus/ebkus_icons/edit_grp_button.gif",
                           tip= 'Gruppenkarte bearbeiten')
                      or 
                      h.IconDead(icon= "/ebkus/ebkus_icons/edit_grp_button_inaktiv.gif",
                               tip= 'Funktion gesperrt')),
                     h.String(string= bg['gruppe_id__gn']),
                     h.String(string= "%(bezugsp__vn)s %(bezugsp__na)s" % bg)]
                    for bg in bezugspersongruppen_list],
            )
        res = h.FormPage(
            title='Klientenkarte',
            name="",action="",method="",hidden=(),
            help=True,
            rows=(menu,
                  klientendaten,
                  bezugspersonen,
                  beratungskontakte,
                  leistungen,
                  h.Pair(left=stand,
                         right=bearbeiter),
                  anmeldekontakte,
                  einrichtungskontakte,
                  h.Pair(left=fachstatistik,
                         right=jugendhilfestatistik),
                  notizen,
                  h.Pair(left=fallgruppen,
                         right=bezugspersongruppen),
            ))
        return res.display()

