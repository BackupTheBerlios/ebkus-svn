# coding: latin-1

"""Module für die Klientenkarte."""
# TODO an die Standards anpassen
import re, time
from ebkus.config import config
from ebkus.app import Request
from ebkus.app import ebupd
from ebkus.app import ebapi
import ebkus.html.htmlgen as h

from ebkus.html.akte_share import akte_share

class klkarte(Request.Request, akte_share):
    """Klientenkarte."""
    permissions = Request.KLKARTE_PERM
    def processForm(self, REQUEST, RESPONSE):
        #print 'KLIENTENKATE FORM', sorted([i for i in dict(self.form).items()])
        file = self.form.get('file')
        # Fall 1 Klientenkarte direkt darstellen
        if not file or file == 'klkarte':
            fallid = self.form.get('fallid')
            akid = self.form.get('akid')
            if not akid:
                if fallid:
                    akid = ebapi.Fall(fallid)['akte_id']
                else:
                    raise ebapi.EE('Es wurde nichts aus dem Menü ausgewählt.')
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
            
        if file == 'kldok':
            fallid = self.form.get('fallid')
            if fallid:
                    fallid = int(fallid)
            else:
                raise ebapi.EE('Es wurde nichts aus dem Menü ausgewählt.')
            RESPONSE.redirect('kldok?fallid=%s' % fallid)
            return ''
        # für die Behandlung der Statistiken vom Hauptmenü aus:
        if file in ('updjghform', 'updfsform', 'vorblatt'):
            fallid = self.form.get('fallid')
            if not fallid:
                raise ebapi.EE('Es wurde nichts aus dem Menü ausgewählt.')
            fall = ebapi.Fall(fallid)
            if file == 'updjghform':
                jgh = fall['jgh'] # in ebapi definiert
                if not jgh:
                    file = 'jgh07neu'
            elif file == 'updfsform':
                if not fall['fachstatistiken']:
                    file = 'fsneu'
            # vorblatt geht an dispatch
            # wie schafft man es an dieser Stelle, dass ein
            # neuer Fenster für das Vorblatt aufgemacht wird?
        return self.ebkus.dispatch(file, REQUEST, RESPONSE)
        
    einfuege_oder_update_operationen = {
      'akteeinf': ('akid', ebapi.Akte),
      'perseinf': ('akid', ebapi.Akte),
      'einreinf': ('akid', ebapi.Akte),
      'anmeinf': ('fallid', ebapi.Fall),
      'leisteinf': ('fallid', ebapi.Fall),
      'bkonteinf': ('fallid', ebapi.Fall),
      'removebkont': ('fallid', ebapi.Fall),
      'zusteinf': ('fallid', ebapi.Fall),
      'zdaeinf': ('fallid', ebapi.Fall),
      #'updfall': ('gfall', ebapi.Fall),
      'updakte': ('akid', ebapi.Akte),
      'updpers': ('bpid', ebapi.Bezugsperson),
      'removepers': ('bpid', ebapi.Bezugsperson),
      'updeinr': ('einrid', ebapi.Einrichtungskontakt),
      'removeeinr': ('einrid', ebapi.Einrichtungskontakt),
      'updanm': ('anmid', ebapi.Anmeldung),
      'updleist': ('leistid', ebapi.Leistung),
      'removeleist': ('leistid', ebapi.Leistung),
      'updbkont': ('fallid', ebapi.Fall),
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
        # Akte id ermitteln um klkarte anzeigen zu können
        id_name, klass = self.einfuege_oder_update_operationen.get(file)
        akid = None
        if file.startswith('remove'):
            # vorher, weils Objekt später weg ist
            akid = klass(int(self.form[id_name]))['akte__id']
        # API Funktion aufrufen
        function = getattr(ebupd, file)
        function(self.form)
        if not akid:
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
        
        menu = h.FieldsetInputTable(daten=[[
            h.Button(value="Hauptmenü",
                     tip="Zum Hauptmenü",
                     onClick="go_to_url('menu')",
                     ),
            h.Button(value="Klientendokumente",
                     class_='buttonbig',
                     tip="Klientendokumente ansehen",
                     onClick="go_to_url('kldok?akid=%(id)s')" % akte,
                     ),
            self.get_button_klienten_neu(aktueller_fall, wiederaufnehmbar, letzter_fall),
            self.get_button_klienten_anzeige(aktueller_fall, letzter_fall),
            ]])

        klientendaten = self.get_klientendaten_readonly(
            akte, 
            button=aktueller_fall and
            h.Button(value="Bearbeiten",
                     tip="Klientenstammdaten bearbeiten",
                     onClick= "go_to_url('updakte?akid=%(id)s')" % akte)
            or None,
            )
        bezugspersonen = self.get_bezugspersonen(bezugspersonen_list, aktueller_fall,
                                                 edit_button=True, view_button=True,
                                                 hinzufuegen_button=True)
        leistungen = h.FieldsetDataTable(
            legend= 'Leistungen',
            headers= ('Mitarbeiter', 'Leistung', 'Am', 'Bis'),
            noheaders=2,
            daten= [[aktueller_fall == leist['fall'] and
                      h.Icon(href= 'updleist?fallid=%(fall_id)d&leistid=%(id)d' % leist,
                           icon= "/ebkus/ebkus_icons/edit_button.gif",
                           tip= 'Leistung bearbeiten')
                     or h.Dummy(),
                     aktueller_fall == leist['fall'] and
                     h.Icon(href= 'rmleist?&leistid=%(id)d' % leist,
                            icon= "/ebkus/ebkus_icons/del_button.gif",
                            tip= 'Leistung löschen')
                     or h.Dummy(),
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

        if config.BERATUNGSKONTAKTE:
            # auch für Braunschweig
            beratungskontakte = self.get_beratungskontakte(beratungskontakte_list,
                                                           aktueller_fall=aktueller_fall,
                                                           edit_button=True,
                                                           hinzufuegen_button=True)
##            
##         elif config.BERATUNGSKONTAKTE:
##             beratungskontakte = h.FieldsetDataTable(
##                 legend= 'Beratungskontakte',
##                 headers= ('Mitarbeiter', 'Art', 'Datum', 'Dauer', 'Notiz'),
##                 daten= [[(aktueller_fall == bkont['fall'] and
##                           h.Icon(href= 'updbkont?fallid=%(fall_id)d&bkontid=%(id)d' % bkont,
##                                icon= "/ebkus/ebkus_icons/edit_button.gif",
##                                tip= 'Beratungskontakt bearbeiten')
##                           or
##                           h.IconDead(icon= "/ebkus/ebkus_icons/edit_button_inaktiv_locked.gif",
##                                    tip= 'Funktion gesperrt')),
##                            h.String(string= bkont['mit_id__na']),
##                            h.String(string= bkont['art__name']),
##                            h.Datum(day=   bkont['kd'],
##                                  month= bkont['km'],
##                                  year=  bkont['ky']),
##                            h.String(string= bkont['dauer__name']),
##                            h.String(string= bkont['no'])]
##                         for bkont in beratungskontakte_list],
##                 button= (aktueller_fall and
##                          h.Button(value= "Hinzufügen",
##                                 tip= "Beratungskontakt hinzufügen",
##                             onClick= "go_to_url('bkontneu?akid=%(id)d&fallid=%(aktueller_fall__id)d')" % akte,
##                                 ) or None),
##                 )
        else:
            beratungskontakte = None
        stand = h.FieldsetDataTable(
            legend= 'Stand',
            headers= ('Fallnummer', 'Anmeldedatum', 'z.d.A.'),
            noheaders=1,
            daten= [[fall == aktueller_fall and
                      h.Icon(href= 'updfall?akid=%(akte_id)d&fallid=%(id)d' % fall,
                           icon= "/ebkus/ebkus_icons/edit_button.gif",
                           tip= 'Fallstatus bearbeiten')
                      or h.Dummy(),
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
            noheaders=1,
            daten= [[zust['fall'] == aktueller_fall and
                      h.Icon(href= 'updzust?fallid=%(fall_id)d&zustid=%(id)d' % zust,
                           icon= "/ebkus/ebkus_icons/edit_button.gif",
                           tip= "Zuständigkeit bearbeiten")
                      or h.Dummy(),
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
            legend= 'Anmeldekontakte',
            headers= ('Gemeldet von', 'Telefon', 'Empf.', 'durch', 
                      'Gemeldet am', 'Anmeldegrund', 'Notiz'),
            noheaders=1,
            daten= [[aktueller_fall == a['fall'] and
                     h.Icon(href= 'updanm?anmid=%(id)d' % a,
                            icon= "/ebkus/ebkus_icons/edit_button.gif",
                            tip= 'Anmeldekontakt bearbeiten')
                     or h.Dummy(),
                     h.String(string= a['von']),
                     h.String(string= a['mtl']),
                     h.String(string= a['zm__name']),
                     h.String(string= a['me']),
                       h.Datum(date=a['fall'].getDate('bg')),
                     h.String(string= a['mg']),
                     h.String(string= a['no']),
                     ]
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
            headers= ('Art', 'Name', 'Telefon 1', 'Telefon 2', 'Aktuell', 'Notiz'),
            noheaders=2,
            daten= [[aktueller_fall and
                     h.Icon(href= 'updeinr?einrid=%(id)d' % e,
                            icon= "/ebkus/ebkus_icons/edit_button.gif",
                            tip= 'Einrichtungskontakt bearbeiten')
                     or h.Dummy(),
                     aktueller_fall and
                      h.Icon(href= 'rmeinr?einrid=%(id)d' % e,
                             icon= "/ebkus/ebkus_icons/del_button.gif",
                             tip= 'Einrichtungskontakt löschen')
                     or h.Dummy(),
                     h.String(string= e['insta__name']),
                     h.String(string= e['na']),
                     h.String(string= e['tl1']),
                     h.String(string= e['tl2']),
                     h.String(string= e['status__code']),
                     h.String(string= e['no'],
                              class_=ebapi.cc('notizbed', 't')==e['nobed'] and 'tabledatared'
                                     or 'tabledata'
                              ),
                     ]
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
                                     class_=ebapi.cc('notizbed', 't')==b['nobed'] and 'tabledatared'
                                     or 'tabledata'),
                              ])
        for e in einrichtungskontakte_list:
            if e['no']:
                notiz_daten.append([h.String(string= 'ER'),
                              h.String(string= "%(insta__name)s %(na)s" % e),
                              h.String(string= e['no']),
                              h.String(string= e['nobed__name'],
                                     class_=ebapi.cc('notizbed', 't')==e['nobed'] and 'tabledatared'
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
                     h.Icon(href= 'viewfs?fsid=%(id)d' % fs,
                            target='_blank',
                            icon= "/ebkus/ebkus_icons/view_details.gif",
                            tip= 'Fachstatistik ansehen/drucken'),
                     h.String(string= fs['fall_fn']),
                     h.String(string= fs['jahr'])]
                    for fs in fachstatistik_list],
            button= (aktueller_fall and not aktueller_fall['fachstatistiken'] and
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
                     not (aktueller_fall['jgh_statistiken'] or
                          aktueller_fall['jgh07_statistiken']) and
                     h.Button(value= "Hinzufügen",
                            tip= "Jugendhilfestatistik hinzufügen",
                            onClick=
                            "go_to_url('jgh07neu?fallid=%(id)d')" % aktueller_fall,
                            ) or None),
            )

        bezugspersongruppen = fallgruppen = ''
        if fallgruppen_list:
            fallgruppen = h.FieldsetDataTable(
                legend='Gruppenkarten des Falls',
                headers=('Gruppennummer', 'Name',),
                noheaders=1,
                daten=[[aktueller_fall
                         and
                         h.Icon(href='grkarte?gruppeid=%(gruppe_id)s' % fg,
                              icon="/ebkus/ebkus_icons/edit_grp_button.gif",
                              tip='Gruppenkarte ansehen')
                         or h.Dummy(),
                        h.String(string=fg['gruppe_id__gn']),
                        h.String(string="%(fall__akte__vn)s %(fall__akte__na)s" % fg)]
                       for fg in fallgruppen_list],
                )
        if bezugspersongruppen_list:
            bezugspersongruppen = h.FieldsetDataTable(
                legend= 'Gruppenkarten der Bezugspersonen',
                headers= ('Gruppennummer.', 'Name',),
                noheaders=1,
                daten= [[aktueller_fall and
                          h.Icon(href= 'grkarte?gruppeid=%(gruppe_id)s' % bg,
                               icon= "/ebkus/ebkus_icons/edit_grp_button.gif",
                               tip= 'Gruppenkarte ansehen')
                          or h.Dummy(),
                         h.String(string= bg['gruppe_id__gn']),
                         h.String(string= "%(bezugsp__vn)s %(bezugsp__na)s" % bg)]
                        for bg in bezugspersongruppen_list],
                )
        res = h.FormPage(
            title='Klientenkarte',
            name="",action="",method="",hidden=(),
            help=True,
            breadcrumbs = (('Hauptmenü', 'menu'),
                           ),
            rows=(menu,
                  klientendaten,
                  #None,
                  self.get_extern_fieldset(akte),
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

    def get_extern_fieldset(self, akte):
        if not config.EXTERN_FIELDSET_LABEL:
            return None
        letzter_fall = akte['letzter_fall']
        aktueller_fall = akte['aktueller_fall']
        if aktueller_fall:
            fall = aktueller_fall
        else:
            fall =letzter_fall
        extern_data = []
        for i in range(1, 5):
            url = getattr(config, "EXTERN_BUTTON%s_URL" % i)
            if '$$fall_id$$' in url:
                url = url.replace('$$fall_id$$', str(fall['id']))
            label = getattr(config, "EXTERN_BUTTON%s_LABEL" % i)
            if url and label:
                extern_data.append((label, url))
        fieldset = h.FieldsetInputTable(
            legend=config.EXTERN_FIELDSET_LABEL,
            daten=[[
            h.Button(value=label,
                     onClick="go_to_url('newXX %s')" % (url,),
                     )
            for label, url in extern_data
            ]])
        if extern_data:
            return fieldset
        return None
