# coding: latin-1

"""Modul Beratungskontakte."""

from ebkus.app import Request
from ebkus.app.ebapi import Code, Fall, MitarbeiterList, Beratungskontakt, BeratungskontaktList, \
     today, cc, cn, bcode, check_int_not_empty, check_list, EE
from ebkus.app.ebapih import get_codes
from ebkus.config import config

import ebkus.html.htmlgen as h
from ebkus.html.akte_share import akte_share

class _bkont(Request.Request, akte_share):
    # bkontneu und updbkont mit derselben Routine,
    # nur anders parametrisiert

    def _process(self, REQUEST, RESPONSE,
                 title,
                 legendtext,
                 fall, # einer der F�lle, der am Kontakt teilnahme
                       # von dessen Klientenkarte aus man kam
                 bkont,
                 file,
                 ):
        if config.BERATUNGSKONTAKTE_BS:
            beratungs_kontakt_bearbeiten = h.FieldsetInputTable(
                legend = '%s %s %s' % (legendtext, fall['akte__vn'], fall['akte__na']),
                daten = [[h.SelectItem(label='Mitarbeiter',
                                       name='mitid',
                                       options=self.for_mitarbeiter(
                sel=[m['id'] for m in bkont['mitarbeiter']]),
                                       multiple=True,
                                       size=8,
                                       ),
                          h.SelectItem(label='Klienten',
                                       name='bkfallid',
                                       class_='listbox280',
                                       options=self.for_klienten(
                sel=[f['id'] for f in bkont['faelle']]),
                                       multiple=True,
                                       size=8,
                                       ),
                          ],
                          [h.DatumItem(label='Datum/Uhrzeit',
                                       name='k',
                                       date =  bkont.getDate('k'),
                                       time = bkont.getTime('k'),
                                       ),
                           h.SelectItem(label='Teilnehmer',
                                        name='teilnehmer_bs',
                                        multiple=True,
                                        size=4,
                                        rowspan=3,
                                        options=self.for_kat('teilnbs', sel=bkont['teilnehmer_bs'])
                                        ),
                           ],
                          [h.TextItem(label='Dauer in Minuten)',
                                      name='dauer',
                                      value=bkont['dauer'],
                                      tip='Bitte in 10-Schritten angeben, z.B. 10, 20, 40, etc.',
                                      class_='textboxsmall',
                                      maxlength=3,
                                      ),
                           ],
                          [h.SelectItem(label='Art des Kontaktes',
                                        name='art_bs',
                                        options=self.for_kat('kabs', sel=bkont['art_bs'])
                                        ),
                           ],
                          [h.CheckItem(label='In offener Sprechstunde',
                                       name='offenespr',
                                       value=cn('ja_nein', 'ja'),
                                       checked=bkont['offenespr']==cn('ja_nein', 'ja'),
                                       ),
                           h.TextItem(label='Anzahl',
                                      name='anzahl',
                                      value=bkont['anzahl'],
                                      class_='textboxsmall',
                                      maxlength=2,
                                      ),
                           ],
                          [h.TextItem(label='Notiz',
                                      name='no',
                                      value=bkont['no'],
                                      class_='textboxverylarge',
                                      maxlength=1024,
                                      n_col=4,
                                      ),
                           ],
                          ],
                )
        else:
            beratungs_kontakt_bearbeiten = h.FieldsetInputTable(
                legend = '%s %s %s' % (legendtext, fall['akte__vn'], fall['akte__na']),
                daten = [[h.SelectItem(label='Mitarbeiter',
                                       name='mitid',
                                       options=self.for_mitarbeiter(
                sel=[m['id'] for m in bkont['mitarbeiter']]),
                                       multiple=True,
                                       size=8,
                                       ),
                          h.SelectItem(label='Klienten',
                                       name='bkfallid',
                                       class_='listbox280',
                                       options=self.for_klienten(
                sel=[f['id'] for f in bkont['faelle']]),
                                       multiple=True,
                                       size=8,
                                       n_col=4,
                                       ),
                          ],
                         [h.DatumItem(label='Datum',
                                      name='k',
                                      date =  bkont.getDate('k')),
                          h.SelectItem(label='Art des Kontaktes',
                                     name='art',
                                     options=self.for_kat('fska', sel=bkont['art'])),
                          h.SelectItem(label='Dauer',
                                       name='dauer_kat',
                                       options=self.for_kat('fskd',
                                                            sel=bcode('fskd', bkont['dauer'], 0)['id'])),
                          ],
                          [h.TextItem(label='Notiz',
                                      name='no',
                                      value=bkont['no'],
                                      class_='textboxverylarge',
                                      maxlength=1024,
                                      n_col=4,
                                      ),
                           ],
                          ],
                )
        beratungskontakte = fall['beratungskontakte']
        konseq_jgh = h.FieldsetDataTable(
            legend='Konsequenzen f�r die Bundesstatistik',
            )
        res = h.FormPage(
            title=title,
            name="beratungskontakt",action="klkarte",method="post",
            breadcrumbs = (('Hauptmen�', 'menu'),
                           ('Klientenkarte', 'klkarte?akid=%(akte_id)s' % fall),
                           ),
            hidden=(("akid", fall['akte_id']),
                    ("stz", bkont['stz']),
                    ("bkontid", bkont['id']),
                    ("fallid", fall['id']),
                    ("file", file),
                    ),
            rows=(beratungs_kontakt_bearbeiten,
                  #konseq_jgh,
                  h.SpeichernZuruecksetzenAbbrechen(),
                  self.get_beratungskontakte(beratungskontakte),
                  )
            )
        return res.display()
    
class bkontneu(_bkont):
    """Neue Beratungskontakt eintragen. (Tabelle: Beratungskontakt.)"""
    permissions = Request.UPDATE_PERM
    def processForm(self, REQUEST, RESPONSE):
        if self.form.has_key('fallid'):
            fallid = self.form.get('fallid')
        else:
            self.last_error_message = "Keine ID f�r den Fall erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
        fall = Fall(fallid)
        benr = self.mitarbeiter['benr__code']
        if benr in ('verw',):
            # Verwaltungskraft kann Eintr�ge f�r andere Mitarbeiter machen
            mitarbeiter = []
        else:
            mitarbeiter = [self.mitarbeiter]
        bkont = Beratungskontakt()
        bkont.init(
            id=Beratungskontakt().getNewId(),
            faelle=[fall],
            mitarbeiter=mitarbeiter,
            teilnehmer_bs=None,
            anzahl='',
            art_bs=None,
            art=None,
            dauer='',
            offenespr=cn('ja_nein', 'nein'),
            no='',
            stz=self.stelle['id'],
           )
        bkont.setDate('k', today())
        return self._process(REQUEST, RESPONSE,
                             title="Neuen Beratungskontakt eintragen",
                             legendtext="Neuen Beratungskontakt eintragen f�r",
                             fall=fall,
                             bkont=bkont,
                             file='bkonteinf',
                             )
        
class updbkont(_bkont):
    """Beratungskontakt �ndern. (Tabelle: Beratungskontakt.)"""
    permissions = Request.UPDATE_PERM
    def processForm(self, REQUEST, RESPONSE):
        id = self.form.get('bkontid')
        if not id:
            self.last_error_message = "Keine ID f�r den Beratungskontakt erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
        fall_id = self.form.get('fallid')
        if not fall_id:
            self.last_error_message = "Keine Fall-ID f�r den Beratungskontakt erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
        bkont = Beratungskontakt(id)
        fall = Fall(fall_id)
        #TODO rausnehmen
        assert fall in bkont['faelle']
        return self._process(REQUEST, RESPONSE,
                             title="Beratungskontakt bearbeiten",
                             legendtext="Beratungskontakt bearbeiten von",
                             fall=fall,
                             bkont=bkont,
                             file='updbkont',
                             )

class rmbkont(Request.Request):
    """Beratungskontakt l�schen."""
    permissions = Request.UPDATE_PERM
    def processForm(self, REQUEST, RESPONSE):
        id = self.form.get('bkontid')
        if not id:
            self.last_error_message = "Keine ID f�r den Beratungskontakt erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
        fall_id = self.form.get('fallid')
        if not fall_id:
            self.last_error_message = "Keine Fall-ID f�r den Beratungskontakt erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
        bkont = Beratungskontakt(id)
        fall = Fall(fall_id)
        #TODO rausnehmen
        assert fall in bkont['faelle']
        return h.SubmitOrBack(
            legend='Beratungskontakt l�schen',
            action='klkarte',
            method='post',
            hidden=(('file', 'removebkont'),
                    ('bkontid', bkont['id']),
                    ('fallid', fall_id),
                    ),
            zeilen=('Soll der Beratungskontakt vom %s endg�ltig gel�scht werden?' % bkont.getDate('k'),
                    'Beteiligte Klienten: %s' % ', '.join([f['name'] for f in bkont['faelle']]),
                    'Beteiligte Mitarbeiter: %s' % ', '.join([m['na'] for m in bkont['mitarbeiter']]),
                    ),
            ).display()

class bkontbsabfr(Request.Request, akte_share):
    permissions = Request.ABFR_PERM
    def _init_res(self):
        netto = {}
        brutto = {}
        for ka in get_codes('kabs'):
            netto[ka['code']] = 0
            brutto[ka['code']] = 0
        netto['offenespr'] = 0
        brutto['offenespr'] = 0
        return netto, brutto
    def _add_res(self, summe, summand):
        for k,v in summand.items():
            summe[k] += v
##     def count_row(self, netto, brutto, bkont):
##         "Einen Kontakt ausz�hlen"
##         art = bkont['art_bs__code']
##         dauer = bkont['dauer']
##         if art == '5':
##             # ausgefallen
##             netto[art] += 20
##             brutto[art] += 20
##         elif art in ('3', '7', '9'):
##             # Fahrzeiten
##             netto[art] += dauer
##             brutto[art] += dauer
##         else:
##             # alles andere +40% Vor- und Nachbereitung
##             netto[art] += dauer
##             brutto[art] += dauer + (dauer*.4)
##         if bkont['offenespr'] == cn('ja_nein', 'ja'):
##             # Offene Sprechstunde
##             netto['offenespr'] += dauer
##             brutto['offenespr'] += dauer + (dauer*.4)
    def count_row(self, netto, brutto, bkont):
        "Einen Kontakt ausz�hlen"
        art = bkont['art_bs__code']
        dauer = bkont['dauer']
        netto[art] += dauer
        brutto[art] += bkont['brutto']
        if bkont['offenespr'] == cn('ja_nein', 'ja'):
            # Offene Sprechstunde
            netto['offenespr'] += dauer
            brutto['offenespr'] += bkont['brutto']
    def count(self, stz_list, von_jahr, bis_jahr, quartal=None):
        """Kontaktzeiten ausz�hlen.
        Ergebnis ist abh�ngig von Berechtigungen:
        - verw: alle Mitarbeiter der spezifierten Stellen
                Summe �ber alle Mitarbeiter der spezifizierten Stellen
        - bearb: der Mitarbeiter selber
                 Summe �ber alle Mitarbeiter der spezifizierten Stellen

        Berechnung der Summen f�r einen Mitarbeiter:
        - es gelten grunds�tzlich die Zeiten, die ein Mitarbeiter aufwendet,
          unabh�ngig davon, wieviele Klienten betroffen sind. Es wird also jede
          Zeile der Beratungskontakt-Tabelle, in der der Mitarbeiter aufgef�hrt ist,
          ber�cksichtigt.
        - Berechnung der Summe f�r die Beratungsstelle:
          es wird ebenso wie bei Mitarbeitern die Summe des Aufwandes der Beratungsstelle
          berechnet. Dh die Summe f�r die Stelle ist gleich der Summe aus allen
          Mitarbeitern.
          Der Aufwand pro Klient spielt hingegen keine Rolle.

        - F�r beide Berechnungen gilt: Jede Zeile der Beratungskontakt-Tabelle geht so
          oft in die Summierung ein, wie die Anzahl der am Kontakt beteiligten Mitarbeiter.

        Daraus ergibt sich, dass die Aufw�nde unabh�ngig davon sind, wieviel Gruppenarbeit
        gemacht wird. 

        Die pro Klient aufgewendete Zeit geht hingegen nur in die Bundesstatistik ein.
        Die Summe der Kontakte in der Bundesstatistik
        ist um so h�her, je mehr Gruppenarbeit gemacht wird, bei gleichem Zeiteinsatz von
        Mitarbeitern.
        """
        stellen = ','.join(["%s" % s for s in stz_list])
        where = ("ky is not NULL and "
        "ky >= %(von_jahr)s and ky  <= %(bis_jahr)s and "
        "stz in ( %(stellen)s )") % locals()
        if quartal:
            assert von_jahr == bis_jahr
            monate = range(1,13)[3*quartal-3:3*quartal]
            where += " and km in (%s)" % ','.join([str(i) for i in monate])
        bkont_list = BeratungskontaktList(where=where)
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
        # f�r jeden Mitarbeiter einen Z�hler mit netto, brutto
        res = {}
        for m in mitarbeiter:
            #id --> (netto, brutto)
            res[m['id']] = self._init_res()
        for b in bkont_list:
            #for f in b('mit_id', 'mit1_id', 'mit2_id'):
            for m in b['mitarbeiter']:
                # jeder Eintrag wird sooft gez�hlt, wie Mitarbeiter darin vorkommen
                try:
                    netto, brutto = res[m['id']]
                    self.count_row(netto, brutto, b)
                except:
                    pass # falls Mitarbeiter in bkont, aber nicht in MitarbeiterList
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
                raise EE('Quartalsauswertungen nur in einem Jahr m�glich')
        else:
            quartal == None
        mitarbeiter, res = self.count(stellen_ids, von_jahr, bis_jahr, quartal)
        kontakt_arten = [c['code'] for c in get_codes('kabs')]
        def row(name, tupl):
            netto, brutto = tupl
            row = [h.String(string=name)]
            for ka in kontakt_arten:
                row.append(h.String(string="%s / %s" %
                                    (netto[ka], brutto[ka]),
                                    tip='Netto/Brutto')
                           )
            return row
        mitarbeiter_daten = [row(m['name'], res[m['id']])
                             for m in mitarbeiter]
        stellen_row = row(', '.join([Code(s)['name'] for s in stellen_ids]),
                          res['summe'])
        headers = [''] + [c['name'] for c in get_codes('kabs')]
        fuer = ''
        if von_jahr < bis_jahr:
            fuer += " f�r %(von_jahr)s bis %(bis_jahr)s" % locals()
        else:
            fuer += " f�r %(bis_jahr)s" % locals()
        if quartal:
            fuer += " Quartal %(quartal)s" % locals()
        tabelle_mitarbeiter = h.FieldsetDataTable(
            legend='Beratungskontaktzeiten Mitarbeiter' + fuer,
            headers=headers,
            daten=mitarbeiter_daten,
            )
        tabelle_stellen = h.FieldsetDataTable(
            legend='Beratungskontaktzeiten summiert f�r Stellen' + fuer,
            headers=headers,
            daten=[stellen_row],
            )
        res = h.FormPage(
            title='Auswertung Beratungskontaktzeiten',
            name="bkontform",action="bkontbsabfr",method="post",
            breadcrumbs = (('Hauptmen�', 'menu'),
                           ),
            hidden = (),
            rows=(self.get_auswertungs_menu(),
                  self.grundgesamtheit(von_jahr=von_jahr,
                                       bis_jahr=bis_jahr,
                                       quartal=quartal,
                                       stellen_ids=stellen_ids,
                                       legend='Jahr und Stelle w�hlen',
                                       submit_value='Anzeigen'),
                  tabelle_mitarbeiter,
                  tabelle_stellen,
                  ),
            )
        return res.display()

##     def processForm(self, REQUEST, RESPONSE):
##         res = h.FormPage(
##             title='Abfrage Beratungskontaktzeiten',
##             name="bkontform",action="bkontbsabfr",method="post",
##             breadcrumbs = (('Hauptmen�', 'menu'),
##                            ),
##             hidden = (),
##             rows=(self.get_auswertungs_menu(),
##                   self.grundgesamtheit(legend='Jahr und Stelle w�hlen'),
##                   h.SpeichernZuruecksetzenAbbrechen(value='Anzeigen'),
##                   ),
##             )
##         return res.display()

def get_jgh_kontakte(fall):
    """Ermittelt Anzahl der Kontakte sowohl f�r den ganzen Fall
    als auch f�r das vergangene Jahr.

    In Braunschweig anders als sonst.

    1;pers�nlicher Kontakt �28;kabs
    2;telefonischer Kontakt (mit Beratungscharakter);kabs
    3;Schreiben;kabs
    4;Fachkontakt;kabs
    5;ausgefallener Kontakt;kabs
    6;Gruppenkontakt;kabs
    7;E-Mail;kabs
    8;interner Fachkontakt, Fallbesprechung;kabs
    9;fallbezogene Fahrzeit;kabs
    F�r die Bundesstatistik z�hlt 1,2,4,6,7
    """
    jahr = today().year - 1 # Normalerweise vom letzten Jahr
    # TODO wieder auf > 10 stellen
    # TODO wie genau z�hlen? Noch mal absprechen
    if today().month > 6:  # Ab Juli von diesem Jahr
        jahr += 1
    bkont_list = fall['beratungskontakte']
    kontakte_im_jahr = kontakte_insgesamt = 0
    if config.BERATUNGSKONTAKTE:
        for row in bkont_list:
            k = row['jghkontakte'] # definiert in ebapi.py und �ber art_bs__dok
            if row['ky'] == jahr:
                kontakte_im_jahr += k
            kontakte_insgesamt += k
    else:
        kontakte_im_jahr = 0
        kontakte_insgesamt = 0
    return kontakte_im_jahr, kontakte_insgesamt
