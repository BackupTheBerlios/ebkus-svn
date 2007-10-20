# coding: latin-1

"""Modul Beratungskontakte."""

from ebkus.app import Request
from ebkus.app.ebapi import Code, Fall, Beratungskontakt_BS, Beratungskontakt_BSList, \
     today, cc, cn, check_int_not_empty, check_list
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
                 fall,
                 bkont,
                 file,
                 ):
        beratungs_kontakt_bearbeiten = h.FieldsetInputTable(
            legend = '%s %s %s' % (legendtext, fall['akte__vn'], fall['akte__na']),
            daten = [[h.SelectItem(label='Mitarbeiter',
                                 name='mitid',
                                 options=self.for_mitarbeiter(sel=bkont['mit_id']),
                                   ),
                      h.TextItem(label='Klienten',
                                 value="%(akte__vn)s %(akte__na)s (%(fn)s)" % bkont['fall'],
                                 readonly=True,
                                   ),
                      ],
                     [h.SelectItem(label='',
                                 name='mit1id',
                                 options=self.for_mitarbeiter(
            sel=bkont['mit1_id'],
            empty_option=bkont['mit1_id']==None and True or False)
                                   ),
                      h.SelectItem(label='',
                                 name='fall1id',
                                 options=self.for_klienten(
            sel=bkont['fall1_id'],
            empty_option=bkont['fall1_id']==None and True or False,
            kurz=True),
                                   ),
                      ],
                     [h.SelectItem(label='',
                                 name='mit2id',
                                 options=self.for_mitarbeiter(
            sel=bkont['mit2_id'],
            empty_option=bkont['mit1_id']==None and True or False)
                                   ),
                      h.SelectItem(label='',
                                 name='fall2id',
                                 options=self.for_klienten(
            sel=bkont['fall2_id'],
            empty_option=bkont['fall1_id']==None and True or False,
            kurz=True),
                                   ),
                      ],
                      [h.DatumItem(label='Datum',
                                   name='k',
                                   date =  bkont.getDate('k')
                                   ),
                       h.SelectItem(label='Teilnehmer',
                                    name='teilnehmer',
                                    multiple=True,
                                    size=4,
                                    rowspan=3,
                                    options=self.for_kat('teilnbs', sel=bkont['teilnehmer'])
                                    ),
                       ],
                      [h.TextItem(label='Dauer (10Min. Einheiten)',
                                  name='dauer',
                                  value=bkont['dauer'],
                                  class_='textboxsmall',
                                  maxlength=2,
                                  ),
                       ],
                      [h.SelectItem(label='Art des Kontaktes',
                                    name='art',
                                    options=self.for_kat('kabs', sel=bkont['art'])
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
        beratungskontakte = fall['beratungskontakte_bs']
        beratungskontakte += fall['beratungskontakte_bs1']
        beratungskontakte += fall['beratungskontakte_bs2']
        beratungskontakte.sort('ky', 'km', 'kd')
        konseq_jgh = h.FieldsetDataTable(
            legend='Konsequenzen für die Bundesstatistik',
            )
        res = h.FormPage(
            title=title,
            name="beratungskontakt",action="klkarte",method="post",
            breadcrumbs = (('Hauptmenü', 'menu'),
                           ('Klientenkarte', 'klkarte?akid=%(fall__akte_id)s' % bkont),
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
                  self.get_beratungskontakte_bs(beratungskontakte),
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
            self.last_error_message = "Keine ID für den Fall erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
        fall = Fall(fallid)
        bkont = Beratungskontakt_BS()
        bkont.init(
            id=Beratungskontakt_BS().getNewId(),
            fall_id=fall['id'],
            fall1_id=None,
            fall2_id=None,
            mit_id=self.mitarbeiter['id'],
            mit1_id=None,
            mit2_id=None,
            teilnehmer=None,
            anzahl='',
            art=None,
            dauer='',
            offenespr=cn('ja_nein', 'nein'),
            no='',
            stz=self.stelle['id'],
           )
        bkont.setDate('k', today())
        return self._process(REQUEST, RESPONSE,
                             title="Neuen Beratungskontakt eintragen",
                             legendtext="Neuen Beratungskontakt eintragen für",
                             fall=fall,
                             bkont=bkont,
                             file='bkontbseinf',
                             )
        
class updbkont(_bkont):
    """Beratungskontakt ändern. (Tabelle: Beratungskontakt.)"""
    permissions = Request.UPDATE_PERM
    def processForm(self, REQUEST, RESPONSE):
        if self.form.has_key('bkontid'):
            id = self.form.get('bkontid')
        else:
            self.last_error_message = "Keine ID für den Beratungskontakt erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
        bkont = Beratungskontakt_BS(id)
        fall = Fall(bkont['fall_id'])
        return self._process(REQUEST, RESPONSE,
                             title="Beratungskontakt bearbeiten",
                             legendtext="Beratungskontakt bearbeiten von",
                             fall=fall,
                             bkont=bkont,
                             file='updbkontbs',
                             )

class bkontbsabfrform(Request.Request, akte_share):
    permissions = Request.ABFR_PERM
    def processForm(self, REQUEST, RESPONSE):
        res = h.FormPage(
            title='Abfrage Beratungskontaktzeiten',
            name="bkontform",action="bkontbsabfr",method="post",
            breadcrumbs = (('Hauptmenü', 'menu'),
                           ),
            hidden = (),
            rows=(self.get_auswertungs_menu(),
                  self.grundgesamtheit(),
                  h.SpeichernZuruecksetzenAbbrechen(),
                  ),
            )
        return res.display()
    
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
    def count_row(self, netto, brutto, bkont):
        "Einen Kontakt auszählen"
        art = bkont['art__code']
        dauer = bkont['dauer']
        if art == '5':
            # ausgefallen
            netto[art] += 2
            brutto[art] += 2
        elif art == '9':
            # Fahrzeiten
            netto[art] += dauer
            brutto[art] += dauer
        else:
            # alles andere +40% Vor- und Nachbereitung
            netto[art] += dauer
            brutto[art] += dauer + (dauer*.4)
        if bkont['offenespr'] == cn('ja_nein', 'ja'):
            # Offene Sprechstunde
            netto['offenespr'] += dauer
            brutto['offenespr'] += dauer + (dauer*.4)
    def count(self, stz_list, von_jahr, bis_jahr):
        """Kontaktzeiten auszählen.
        Ergebnis ist abhängig von Berechtigungen:
        - verw: alle Mitarbeiter der spezifierten Stellen
                Summe über alle Mitarbeiter der spezifizierten Stellen
        - bearb: der Mitarbeiter selber
                 Summe über alle Mitarbeiter der spezifizierten Stellen

        Berechnung der Summen für einen Mitarbeiter:
        - es gelten grundsätzlich die Zeiten, die ein Mitarbeiter aufwendet,
          unabhängig davon, wieviele Klienten betroffen sind. Es wird also jede
          Zeile der Beratungskontakt-Tabelle, in der der Mitarbeiter aufgeführt ist,
          berücksichtigt.
        - Berechnung der Summe für die Beratungsstelle:
          es wird ebenso wie bei Mitarbeitern die Summe des Aufwandes der Beratungsstelle
          berechnet. Dh die Summe für die Stelle ist gleich der Summe aus allen
          Mitarbeitern.
          Der Aufwand pro Klient spielt hingegen keine Rolle.

        - Für beide Berechnungen gilt: Jede Zeile der Beratungskontakt-Tabelle geht so
          oft in die Summierung ein, wie die Anzahl der am Kontakt beteiligten Mitarbeiter.

        Daraus ergibt sich, dass die Aufwände unabhängig davon sind, wieviel Gruppenarbeit
        gemacht wird. 

        Die pro Klient aufgewendete Zeit geht hingegen nur in die Bundesstatistik ein.
        Die Summe der Kontakte in der Bundesstatistik
        ist um so höher, je mehr Gruppenarbeit gemacht wird, bei gleichem Zeiteinsatz von
        Mitarbeitern.
        """
        stellen = ','.join(["%s" % s for s in stz_list])
        where = ("ky is not NULL and "
        "ky >= %(von_jahr)s and ky  <= %(bis_jahr)s and "
        "stz in ( %(stellen)s )") % locals()
        bkont_list = Beratungskontakt_BSList(where=where)
        benr_id = self.mitarbeiter['benr']
        benr = self.mitarbeiter['benr__code']
        mitarbeiter = []
        if benr == 'bearb':
            mitarbeiter = [self.mitarbeiter]
        elif benr == 'verw':
            mitarbeiter = MitarbeiterList(
                where='stz in (%(stellen)s) and benr = %(benr_id)s' % locals(),
                order='na')
        # für jeden Mitarbeiter einen Zähler mit netto, brutto
        res = {}
        for m in mitarbeiter:
            #id --> (netto, brutto)
            res[m['id']] = self._init_res()
        for b in bkont_list:
            for f in ('mit_id', 'mit1_id', 'mit2_id'):
                # jeder Eintrag wird sooft gezählt, wie Mitarbeiter darin vorkommen
                try:
                    netto, brutto = res[b[f]]
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
        print 'FORM', self.form
        von_jahr = self.form.get('von_jahr')
        bis_jahr = check_int_not_empty(self.form, 'bis_jahr', "Jahr fehlt")
        if not von_jahr or von_jahr > bis_jahr:
            von_jahr = bis_jahr
        stz = check_list(self.form, 'stz', 'Keine Stelle')
        mitarbeiter, res = self.count(stz, von_jahr, bis_jahr)
        kontakt_arten = [c['code'] for c in get_codes('kabs')]
        def row(name, tupl):
            netto, brutto = tupl
            row = [h.String(string=name)]
            for ka in kontakt_arten:
                row.append(h.String(string="%s/%s" %
                                    (netto[ka], brutto[ka]))
                           )
            return row
        mitarbeiter_daten = [row(m['name'], res[m['id']])
                             for m in mitarbeiter]
        stellen_row = row(', '.join([Code(s)['name'] for s in stz]),
                          res['summe'])
        headers = [''] + [c['name'] for c in get_codes('kabs')]
        
        tabelle_mitarbeiter = h.FieldsetDataTable(
            legend='Beratungskontaktzeiten Mitarbeiter',
            headers=headers,
            daten=mitarbeiter_daten,
            )
        tabelle_stellen = h.FieldsetDataTable(
            legend='Beratungskontaktzeiten summiert für Stellen',
            headers=headers,
            daten=[stellen_row],
            )
        res = h.Page(
            title='Tabelle Beratungskontaktzeiten',
            breadcrumbs = (('Hauptmenü', 'menu'),
                           ('Abfrage Beratungskontaktzeiten', 'bkontbsabfrform'),
                           ),
            hidden = (),
            rows=(tabelle_mitarbeiter,
                  tabelle_stellen,
                  h.SpeichernZuruecksetzenAbbrechen()
                  ),
            )
        return res.display()



def get_anzahl_jgh_kontakte_row(row):
    return n # immer 0,1 oder 2

def get_jgh_kontakte_bs(fall):
    "Ermittelt Anzahl der Kontakte sowohl für den ganzen Fall "
    "als auch für das vergangene Jahr"
    """
    1;persönlicher Kontakt §28;kabs
    2;telefonischer Kontakt (mit Beratungscharakter);kabs
    3;Schreiben;kabs
    4;Fachkontakt;kabs
    5;ausgefallener Kontakt;kabs
    6;Gruppenkontakt;kabs
    7;E-Mail;kabs
    8;interner Fachkontakt, Fallbesprechung;kabs
    9;fallbezogene Fahrzeit;kabs
    Für die Bundesstatistik zählt 1,2,4,6,7
    """
    jahr = today().year - 1 # Normalerweise vom letzten Jahr
    # TODO wieder auf > 10 stellen
    if today().month > 6:  # Ab Juli von diesem Jahr
        jahr += 1
    fall_id = fall['id']
    where = "fall_id=%(fall_id)s or fall1_id=%(fall_id)s or fall2_id=%(fall_id)s" % locals()
    bkont_list = Beratungskontakt_BSList(where=where)
    kontakte_im_jahr = kontakte_insgesamt = 0
    for row in bkont_list:
        k = 0
        code = row['art__code']
        dauer = row['dauer']*1.4*10 # Zeit in Minuten inklusive 40% Vor- und Nachbereitung
        if code in ('1', '2', '4', '6', '7'):
            if dauer >= 30:
                if dauer <= 60:
                    k = 1
                else:
                    k = 2
        if row['ky'] == jahr:
            kontakte_im_jahr += k
        kontakte_insgesamt += k
    return kontakte_im_jahr, kontakte_insgesamt
