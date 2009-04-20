# coding: latin-1

"""Modul Fallunabhängige Aktivitäten für Braunschweig/Gifhorn."""

from ebkus.app import Request
from ebkus.app import ebupd
from ebkus.app.ebapi import Code, Fall, MitarbeiterList, Fua_BS, Fua_BSList, \
     today, cc, cn, check_int_not_empty, check_list, EE
from ebkus.app.ebapih import get_codes
from ebkus.config import config

import ebkus.html.htmlgen as h
from ebkus.html.akte_share import akte_share

class _fua(Request.Request, akte_share):
    # fuaneu und updfua mit derselben Routine,
    # nur anders parametrisiert

    def _process(self, REQUEST, RESPONSE,
                 title,
                 legendtext,
                 fua,
                 file,
                 ):
        # evt. einbauen, falls Rolle=verw
        kein_mitarbeiter = fua['mit_id']==None and True or False
        multi_mit = (file=='fuabseinf')
        fua_bearbeiten = h.FieldsetInputTable(
            legend = legendtext,
            daten = [[h.SelectItem(label='Mitarbeiter',
                                   name='mitid',
                                   options=self.for_mitarbeiter(sel=fua['mit_id'],
                                                                empty_option=kein_mitarbeiter),
                                   multiple=multi_mit,
                                   size=multi_mit and 6 or None,
                                   ),
                      h.DatumItem(label='Datum',
                                  name='k',
                                  date =  fua.getDate('k')
                                  ),
                      ],
                      [h.TextItem(label='Dauer in Minuten',
                                  name='dauer',
                                  value=fua['dauer'],
                                  class_='textboxsmall',
                                  tip='Bitte in 10-Schritten angeben, z.B. 10, 20, 40, etc.',
                                  maxlength=3,
                                  ),
                       h.SelectItem(label='Art der Aktivität',
                                    name='art',
                                    class_='listbox',
                                    options=self.for_kat('fuabs', sel=fua['art'])
                                    ),
                       ],
                     [h.TextItem(label='Notiz',
                                 name='no',
                                 value=fua['no'],
                                 class_='textboxverylarge',
                                  maxlength=1024,
                                 n_col=4,
                                 ),
                      ],
                     ],
            )
##         bisherige_kontakte = h.FieldsetDataTable(
##             legend = 'Liste der bisherigen Kontakte',
##             empty_msg = "Bisher keine Kontakte eingetragen.",
##             headers = ('Datum', 'Mitarbeiter', 'Klienten', 'Art',
##                        'Teilnehmer', 'Dauer (x10min)', 'Notiz'),
##             daten =  [[h.Datum(date =  b.getDate('k')),
##                        h.String(string=', '.join([b['mit%s__na'] % i
##                                                   for i in ('', '1', '2')
##                                                   if b['mit%s_id'] % i]),
##                                 ),
##                        h.String(string=', '.join([b['fall%s__name'] % i
##                                                   for i in ('', '1', '2')
##                                                   if b['fall%s_id'] % i]),
##                                 ),
##                        h.String(string=b['art__name']),
##                        h.String(string=', '.join([Code(i)['name']
##                                                   for i in b['teilnehmer'].split()]),
##                                 ),
##                        h.String(string=b['dauer']),
##                        h.String(string=b['no']),
##                        ]
##                       for b in self.get_beratungskontakte()],
##             )
        year = today().year
        month = today().month
        res = h.FormPage(
            title=title,
            name="fua_bs",action="fua",method="post",
            breadcrumbs = (('Hauptmenü', 'menu'),
                           ('Fallunabhängige Aktivitäten', 'fua'),
                           ),
            hidden=(("stz", fua['stz']),
                    ("fuaid", fua['id']),
                    ("file", file),
                    ),
            rows=(fua_bearbeiten,
                  #konseq_jgh,
                  h.SpeichernZuruecksetzenAbbrechen(),
                  self.get_fua_bs(year, month, 
                                  'Bisherige Aktivitäten für %s/%s' % (month, year)),
                  )
            )
        return res.display()
    
    def get_fua_bs(self, jahr, monat, legend,
                   edit_button=False,
                   hinzufuegen_button=False):

        
        benr = self.mitarbeiter['benr__code']
        where = "ky=%s" % jahr
        if benr == 'bearb':
            where += " and mit_id=%s" % self.mitarbeiter['id']
        elif benr == 'verw':
            where += " and stz=%s" % self.stelle['id']
        if monat:
            where += " and km=%s" % monat
        aktivitaeten_list = Fua_BSList(where=where , order="ky desc, km desc, kd desc")
        aktivitaeten_list.sort('mit__na', 'ky', 'km', 'kd')
        bisherige_aktivitaeten = h.FieldsetDataTable(
            legend=legend,
            empty_msg="Bisher keine Aktivitäten eingetragen.",
            headers=('Datum', 'Mitarbeiter', 'Art', 'Dauer in Minuten', 'Notiz'),
            daten=[[(edit_button and h.Icon(href= 'updfua?fuaid=%(id)d' % fua,
                                            icon= "/ebkus/ebkus_icons/edit_button.gif",
                                            tip= 'Aktivität bearbeiten') or None),
                    (edit_button and h.Icon(href='rmfua?fuaid=%(id)d' % fua,
                                            icon="/ebkus/ebkus_icons/del_button.gif",
                                            tip='Fallunabhängige Aktivität endgültig löschen') or None),
                    h.Datum(date =  fua.getDate('k')),
                    h.String(string=fua['mit__na']),
                    h.String(string=fua['art__name']),
                    h.String(string="%(dauer)s / %(brutto)s" % fua,
                             tip='Netto/Brutto'),
                    h.String(string=fua['no']),
                    ]
                   for fua in aktivitaeten_list],
            button=(hinzufuegen_button and
                    h.Button(value="Hinzufügen",
                             tip="Aktivität hinzufügen",
                             onClick="go_to_url('fuaneu')",
                             ) or None),
            )
        return bisherige_aktivitaeten
        

class fua(_fua):
    "Liste der fallunabhängigen Aktivitäten für ein Mitarbeiter."
    permissions=Request.UPDATE_PERM
    def processForm(self, REQUEST, RESPONSE):
        file = self.form.get('file')
        if file in ('fuabseinf', 'updfuabs', 'removefuabs'):
            # API Funktion einf bzw. upd aufrufen
            getattr(ebupd, file)(self.form)
        jahr = self.form.get('jahr')
        monat = self.form.get('monat', '')
        if not jahr:
            jahr = today().year
            monat = today().month
        auswahl = h.FieldsetInputTable(
            legend="Bisherige Aktivitäten zeigen",
            daten=[[h.TextItem(label='Jahr',
                               name='jahr',
                               tip='Jahr der zu zeigenden Aktivitäten',
                               value=jahr,
                               class_='textboxmid',
                               ),
                    h.TextItem(label='Monat',
                               name='monat',
                               tip='Monat der zu zeigenden Aktivitäten (leer lassen für Aktivitäten des ganzen Jahres)',
                               value=monat,
                               class_='textboxsmall',
                               ),
                    h.Button(value="Zeigen",
                             tip="Aktivitäten zeigen",
                             type="submit",
                             ),
                    ]],
            )
        title="Fallunabhängige Aktivitäten für %s%s" % (monat and "%s/" % monat or '', jahr)
        res = h.FormPage(
            title=title,
            name="fua",action="fua",method="get",
            breadcrumbs = (('Hauptmenü', 'menu'),
                           ),
##             hidden=(("akid", fall['akte_id']),
##                     ("stz", fua['stz']),
##                     ("fuaid", fua['id']),
##                     ("fallid", fall['id']),
##                     ("file", file),
##                     ),
            rows=(self.get_hauptmenu(),
                  auswahl,
                  self.get_fua_bs(jahr, monat, title,
                                  edit_button=True,
                                  hinzufuegen_button=True),
                  )
            )
        return res.display()



class fuaneu(_fua):
    """Neue Aktivität eintragen."""
    permissions = Request.UPDATE_PERM
    def processForm(self, REQUEST, RESPONSE):
        benr = self.mitarbeiter['benr__code']
        if benr in ('verw',):
            # Verwaltungskraft kann Einträge für andere Mitarbeiter machen
            mit_id = None
        else:
            mit_id = self.mitarbeiter['id'],
        fua = Fua_BS()
        fua.init(
            id=Fua_BS().getNewId(),
            mit_id=mit_id,
            art=None,
            dauer='',
            no='',
            stz=self.stelle['id'],
           )
        fua.setDate('k', today())
        return self._process(REQUEST, RESPONSE,
                             title="Neue fallunabhängige Aktivität eintragen",
                             legendtext="Neue fallunabhängige Aktivität",
                             fua=fua,
                             file='fuabseinf',
                             )
        
class updfua(_fua):
    """Aktivität ändern."""
    permissions = Request.UPDATE_PERM
    def processForm(self, REQUEST, RESPONSE):
        if self.form.has_key('fuaid'):
            id = self.form.get('fuaid')
        else:
            self.last_error_message = "Keine ID für die Aktivität erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
        fua = Fua_BS(id)
        return self._process(REQUEST, RESPONSE,
                             title="Aktivität bearbeiten",
                             legendtext="Aktivität bearbeiten",
                             fua=fua,
                             file='updfuabs',
                             )

class rmfua(Request.Request):
    """Beratungskontakt löschen."""
    permissions = Request.UPDATE_PERM
    def processForm(self, REQUEST, RESPONSE):
        if self.form.has_key('fuaid'):
            id = self.form.get('fuaid')
        else:
            self.last_error_message = "Keine ID für die Aktivität erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
        fua = Fua_BS(id)
        return h.SubmitOrBack(
            legend='Fallunabhängige Aktivität',
            action='fua',
            method='post',
            hidden=(('file', 'removefuabs'),
                    ('fuaid', fua['id']),
                    ),
            zeilen=('Soll die fallunabhängige Aktivität vom %s endgültig gelöscht werden?' % fua.getDate('k'),
                    ),
            ).display()

class fuabsabfrform(Request.Request, akte_share):
    permissions = Request.ABFR_PERM
    def processForm(self, REQUEST, RESPONSE):
        res = h.FormPage(
            title='Abfrage fallunabhängige Aktivitäten',
            name="fuaform",action="fuabsabfr",method="post",
            breadcrumbs = (('Hauptmenü', 'menu'),
                           ),
            hidden = (),
            rows=(self.get_auswertungs_menu(),
                  self.grundgesamtheit(legend='Jahr und Stelle wählen'),
                  h.SpeichernZuruecksetzenAbbrechen(value='Anzeigen'),
                  ),
            )
        return res.display()
    
class fuabsabfr(Request.Request, akte_share):
    permissions = Request.ABFR_PERM
    def _init_res(self):
        netto = {}
        brutto = {}
        for ka in get_codes('fuabs'):
            netto[ka['code']] = 0
            brutto[ka['code']] = 0
        return netto, brutto
    def _add_res(self, summe, summand):
        for k,v in summand.items():
            summe[k] += v
##     def count_row(self, netto, brutto, fua):
##         "Eine Aktivitaet auszählen"
##         art = fua['art__code']
##         dauer = fua['dauer']
##         if art == '1':
##             # Erstgespräch ohne Fallnummer 
##             netto[art] += 20
##             brutto[art] += 20
##         elif art == '3':
##             # Gruppenarbeit
##             netto[art] += dauer
##             brutto[art] += dauer*3
##         elif art == '5':
##             # Vernetzung
##             netto[art] += dauer
##             brutto[art] += dauer*1.5
##         elif art == '6':
##             # Familien- und Jugenbildung
##             netto[art] += dauer
##             brutto[art] += dauer*2
##         else:
##             # alles andere reine Durchführungszeit
##             netto[art] += dauer
##             brutto[art] += dauer
    def count_row(self, netto, brutto, fua):
        "Eine Aktivitaet auszählen"
        art = fua['art__code']
        dauer = fua['dauer']
        netto[art] += dauer
        brutto[art] += fua['brutto']

    def count(self, stz_list, von_jahr, bis_jahr, quartal=None, monat=None):
        """Aktivitätszeiten auszählen.
        Ergebnis ist abhängig von Berechtigungen:
        - verw: alle Mitarbeiter der spezifierten Stellen
                Summe über alle Mitarbeiter der spezifizierten Stellen
        - bearb: der Mitarbeiter selber
                 Summe über alle Mitarbeiter der spezifizierten Stellen
        """
        stellen = ','.join(["%s" % s for s in stz_list])
        where = ("ky is not NULL and "
        "ky >= %(von_jahr)s and ky  <= %(bis_jahr)s and "
        "stz in ( %(stellen)s )") % locals()
        if quartal:
            assert von_jahr == bis_jahr
            monate = range(1,13)[3*quartal-3:3*quartal]
            where += " and km in (%s)" % ','.join([str(i) for i in monate])
        if monat:
            assert not quartal
            assert von_jahr == bis_jahr
            #monate = range(1,13)[3*quartal-3:3*quartal]
            monate = [monat]
            where += " and km in (%s)" % ','.join([str(i) for i in monate])
        fua_list = Fua_BSList(where=where)
        benr_id = self.mitarbeiter['benr']
        benr = self.mitarbeiter['benr__code']
        mitarbeiter = []
        if benr == 'bearb':
            mitarbeiter = [self.mitarbeiter]
        elif benr == 'verw':
            bearb_benr_id = cc('benr', 'bearb')
            status = cc('status', 'i')
            mitarbeiter = MitarbeiterList(
                where='stz in (%(stellen)s) and stat = %(status)s and benr = %(bearb_benr_id)s' % locals(),
                order='na')
        # für jeden Mitarbeiter einen Zähler mit netto, brutto
        res = {}
        for m in mitarbeiter:
            #id --> (netto, brutto)
            res[m['id']] = self._init_res()
        for b in fua_list:
                try:
                    netto, brutto = res[b['mit_id']]
                    self.count_row(netto, brutto, b)
                except:
                    #import traceback
                    #traceback.print_exc()
                    pass # falls Mitarbeiter in fua, aber nicht in MitarbeiterList
                         # sollte nicht vorkommen, wenn doch, ignorieren
        summe_netto, summe_brutto = self._init_res()
        for netto, brutto in res.values():
            self._add_res(summe_netto, netto)
            self._add_res(summe_brutto, brutto)
        res['summe'] = summe_netto, summe_brutto
        return mitarbeiter, res
            
    def processForm(self, REQUEST, RESPONSE):
        #print 'FORM', self.form
        von_jahr = self.form.get('von_jahr')
        bis_jahr = self.form.get('bis_jahr')
        if bis_jahr:
            bis_jahr = check_int_not_empty(self.form, 'bis_jahr', "Jahr fehlt")
        else:
            bis_jahr = today().year
        von_jahr = check_int_not_empty(self.form, 'von_jahr', "Jahr fehlt", bis_jahr)
        if von_jahr > bis_jahr:
            von_jahr = bis_jahr
        stellen_ids = [int(id) for id in check_list(self.form, 'stz', 'Keine Stelle',
                                                    [self.stelle['id']])]
        quartal = self.form.get('quartal')
        if quartal:
            quartal = check_int_not_empty(self.form, 'quartal', 'Fehler im Quartal')
            if von_jahr != bis_jahr:
                raise EE('Quartalsauswertungen nur in einem Jahr möglich')
        else:
            quartal == None
        monat = self.form.get('monat')
        if monat:
            monat = check_int_not_empty(self.form, 'monat', 'Fehler im Monat')
            if von_jahr != bis_jahr:
                raise EE('Monatsauswertungen nur in einem Jahr möglich')
        else:
            monat == None
        if monat and quartal:
            raise EE('Monats- und Quartalsauswertung nicht gleichzeitig möglich')
        mitarbeiter, res = self.count(stellen_ids, von_jahr, bis_jahr,
                                      quartal, monat)
        aktivitaets_arten = [c['code'] for c in get_codes('fuabs')]
        def row(name, tupl):
            netto, brutto = tupl
            row = [h.String(string=name)]
            summe_netto = 0
            summe_brutto = 0
            for ka in aktivitaets_arten:
                summe_netto += netto[ka]
                summe_brutto += brutto[ka]
                row.append(h.String(string="%s / %s" %
                                    (netto[ka], brutto[ka]),
                                    tip='Netto/Brutto')
                           )
            row.append(h.String(string="%s / %s" %
                                    (summe_netto, summe_brutto),
                                    tip='Netto/Brutto')
                           )
            return row
        mitarbeiter_daten = [row(m['name'], res[m['id']])
                             for m in mitarbeiter]
        stellen_row = row(', '.join([Code(s)['name'] for s in stellen_ids]),
                          res['summe'])
        headers = [''] + [c['name'] for c in get_codes('fuabs')] + ['Summe']
        fuer = ''
        if von_jahr < bis_jahr:
            fuer += " für %(von_jahr)s bis %(bis_jahr)s" % locals()
        else:
            fuer += " für %(bis_jahr)s" % locals()
        if quartal:
            fuer += " Quartal %(quartal)s" % locals()
        if monat:
            fuer += " Monat %(monat)s" % locals()
        tabelle_mitarbeiter = h.FieldsetDataTable(
            legend='Zeiten für fallunabhängige Aktivitäten Mitarbeiter' + fuer,
            headers=headers,
            daten=mitarbeiter_daten,
            )
        tabelle_stellen = h.FieldsetDataTable(
            legend='Zeiten für fallunabhängige Aktivitäten summiert für Stellen' + fuer,
            headers=headers,
            daten=[stellen_row],
            )
        res = h.FormPage(
            name="fuaform",action="fuabsabfr",method="post",
            title='Auswertung fallunabhängige Aktivitäten',
            breadcrumbs = (('Hauptmenü', 'menu'),
                           ),
            hidden = (),
            rows=(self.get_auswertungs_menu(),
                  self.grundgesamtheit(von_jahr=von_jahr,
                                       bis_jahr=bis_jahr,
                                       quartal=quartal,
                                       monat=monat,
                                       show_monat=True,
                                       stellen_ids=stellen_ids,
                                       legend='Jahr und Stelle wählen',
                                       submit_value='Anzeigen'),
                  tabelle_mitarbeiter,
                  tabelle_stellen,
                  ),
            )
        return res.display()

