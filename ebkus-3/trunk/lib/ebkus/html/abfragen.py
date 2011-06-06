# coding: latin-1
"""Module für die Abfragen."""

import sys
from ebkus.config import config
from ebkus.db.sql import escape
from ebkus.app import Request
from ebkus.app.ebapi import JugendhilfestatistikList, Jugendhilfestatistik2007List, \
     ZustaendigkeitList, AkteList, BezugspersonList, FallList, GruppeList, \
     Tabelle, Code, Feld, Mitarbeiter, MitarbeiterList, MitarbeiterGruppeList, \
     AbfrageList, \
     today, cc, check_int_not_empty, \
     check_str_not_empty, EBUpdateDataError, EE, getQuartal, get_rm_datum, Date
from ebkus.html.abfragedef import Query
from ebkus.app.statistik import BereichsKategorieAuszaehlung        
import ebkus.html.htmlgen as h
from ebkus.html.akte_share import akte_share


class fall_abfrage(Request.Request, akte_share):
    

    def fall_auswahl_form(self):
        default_sort = ('bgy', 'fn_count', 'akte__na',
                        'zuletzt_zustaendig__mit__na',
                        'has_fachstatistik', 'has_jghstatistik')
        default_sort_code = '012345' # Indizes in default_sort
        tmpl = '<option value="%s"%s>%s</option>'
        # erster Wert ist Index in default_sort
        sort_options_data = (
            (0, 'Jahr des Fallbeginns'),
            (1, 'Fallnummer'),
            (2, 'Name des Klienten'),
            (3, 'Name des Mitarbeiters'),
            (4, 'Fachstatistik vorhanden'),
            (5, 'Bundesstatistik vorhanden'),
            )
        welche = check_str_not_empty(self.form, 'w', "Keine Fallart", 'laufend')
        jahr = check_int_not_empty(self.form, 'jahr', "Fehler in ab Jahr", '')
        fn_count = check_int_not_empty(self.form, 'fnc', "Fehler in laufender Nummer", '')
        bis_jahr = check_int_not_empty(self.form, 'bis_jahr', "Fehler in bis Jahr", '')
        bis_fn_count = check_int_not_empty(self.form, 'bis_fnc', 
                                           "Fehler in bis laufender Nummer", '')
        ab_jahr_zda = check_int_not_empty(self.form, 'ab_jahr_zda', 
                                          "Fehler in ab Jahr Abschluss", '')
        bis_jahr_zda = check_int_not_empty(self.form, 'bis_jahr_zda', 
                                          "Fehler in ab Jahr Abschluss", '')

        if fn_count and not jahr:
            raise EE("Ab laufende Fallnummer nur zusammen mit ab Jahr")
        if bis_fn_count and not bis_jahr:
            raise EE("Bis laufende Fallnummer nur zusammen mit bis Jahr")
        if ab_jahr_zda or bis_jahr_zda:
            # in diesem Fall nur abgeschlossene Fälle
            welche = 'abgeschlossen'
        mit_id = check_str_not_empty(self.form, 'mitid', "Kein Mitarbeiter", '')
        seq = check_str_not_empty(self.form, 'seq', "Keine Sortierung", default_sort_code)
        seq = [int(x) for x in seq]
        seq_new = check_str_not_empty(self.form, 'seqn', "Keine Sortierung", '1')
        if seq_new:
            seq_new = int(seq_new)
            assert seq_new in seq, 'Fehler beim Sortieren'
            if seq_new == 1:
                seq.remove(1)
                seq.remove(0)
                seq = [0,1] + seq
            else:
                seq.remove(seq_new)
                seq = [seq_new] + seq
        sort = tuple([default_sort[i] for i in seq])

        mitarbeiter = None
        if self.mitarbeiter['benr__code'] == 'verw':
            if mit_id:
                mitarbeiter = Mitarbeiter(mit_id)
        elif self.mitarbeiter['benr__code'] == 'bearb':
            mitarbeiter = self.mitarbeiter
        legend='Anzuzeigende Beratungen',
        return dict(welche=welche,
                    ab_jahr=jahr,
                    ab_fallnummer=fn_count,
                    bis_jahr=bis_jahr,
                    bis_fallnummer=bis_fn_count,
                    ab_jahr_zda=ab_jahr_zda,
                    bis_jahr_zda=bis_jahr_zda,
                    mitarbeiter=mitarbeiter,
                    sort_options_data=sort_options_data,
                    sort_sel=seq_new, # index der auswahl
                    sort_seq=seq,     # liste von indices
                    sort=sort,        # tuple der sortier-felder
                    )
        

    def get_fall_auswahl(self, legend, welche, ab_jahr, ab_fn_count,
                         bis_jahr, bis_fn_count,
                         ab_jahr_zda, bis_jahr_zda, 
                         mitarbeiter, sort_options_data, sort_sel,
                         submitop='op',
                         ):
        tmpl = '<option value="%s"%s>%s</option>'
        selected = ' selected="selected"'
        welche_options = '\n'.join([tmpl % (v,
                                            v==welche and selected or '',
                                            v.capitalize())
                                    for v in ('laufend', 'abgeschlossen', 'alle')])
        sel = mitarbeiter and mitarbeiter['id'] or None
        alle_sel = (not mitarbeiter) and selected or ''
        mitarbeiter_options = (tmpl % ('', alle_sel, 'Alle')
                               + self.for_mitarbeiter(sel=sel))
        sort_options = '\n'.join([tmpl % (c, c==sort_sel and selected or '', n)
                                  for c, n in sort_options_data])
        anzeige = h.FieldsetInputTable(
            legend=legend,
            daten=[[h.SelectItem(label='Welche',
                                 name='w',
                                 options=welche_options,
    tip='Nur laufende, nur abgeschlossene, oder alle Fälle zeigen',
                                 ),
                    h.SelectItem(label='Fallbeginn ab Jahr',
                                 name='jahr',
                                 class_='listbox45',
                                 tip='Nur Fälle ab dem gewählten Jahr zeigen',
                                 options=self.for_jahre(sel=ab_jahr,
                                                        erster_eintrag='Alle'),
                                 ),
                    h.TextItem(label='ab laufender Nummer',
                               name='fnc',
                               class_='textboxmid',
                               value=ab_fn_count,
                               tip='z.B. 9, 23, etc.',
                               ),
                    ],
                    [self.mitarbeiter['benr__code'] == 'verw' and
                     h.SelectItem(label='Mitarbeiter',
                                  name='mitid',
                                  tip='Nur Fälle des gewählten Mitarbeiters zeigen',
                                  options=mitarbeiter_options,
                                  ) or
                    h.TextItem(label='Mitarbeiter',
                               name='xxx',
                               value=mitarbeiter['na'],
                               readonly=True,
                               ),
                    h.SelectItem(label='Fallbeginn bis Jahr',
                                 name='bis_jahr',
                                 class_='listbox45',
                                 tip='Nur Fälle bis zu dem gewählten Jahr zeigen',
                                 options=self.for_jahre(sel=bis_jahr,
                                                        erster_eintrag='Alle'),
                                 ),
                    h.TextItem(label='bis laufender Nummer',
                               name='bis_fnc',
                               class_='textboxmid',
                               value=bis_fn_count,
                               tip='z.B. 9, 23, etc.',
                               ),
                    ],
                    [h.SelectItem(label='Sortieren nach',
                                  name='seqn',
                                  tip='Wonach die Fälle sortiert sein sollen',
                                  options=sort_options,
                                  ),
                    h.SelectItem(label='Fallabschluss ab Jahr',
                                 name='ab_jahr_zda',
                                 class_='listbox45',
                                 tip='Nur Fälle zeigen, die ab dem gewählten Jahr abgeschlossen wurden',
                                 options=self.for_jahre(sel=ab_jahr_zda,
                                                        erster_eintrag='Alle'),
                                 ),
                    h.SelectItem(label='Fallabschluss bis Jahr',
                                 name='bis_jahr_zda',
                                 class_='listbox45',
                                 tip='Nur Fälle zeigen, die bis zu dem gewählten Jahr abgeschlossen wurden',
                                 options=self.for_jahre(sel=bis_jahr_zda,
                                                        erster_eintrag='Alle'),
                                 ),
                    ],
                   [h.Dummy(n_col=8)],
                   [h.Button(value="Anzeigen",
                             name=submitop,
                             tip="Beratungen anzeigen",
                             type='submit',
                             n_col=8,
                             ),
                    ],
                   ],
            )
        return anzeige

#class _abfr(Request.Request, akte_share):
class _abfr(fall_abfrage):
    "Superklasse für Abfragen"
    def get_table_daten(self, elems, fields):
        "Element von fields kann ein Tupel sein: string, url"
        "Dann wird ein verlinkter Text angezeigt."
        daten = []
        for e in elems:
            zeile = []
            for f in fields:
                if isinstance(f, tuple):
                    acc, tmpl = f
                    zeile.append(h.Link(string=e[acc], url=tmpl % e))
                elif e.get(f+'y') != None:
                    # TODO very dirty hack!!!!
                    zeile.append(h.Datum(date=e[f]))
                else:
                    v = e[f]
                    if v == None:
                        v = ''
                    zeile.append(h.String(string=v))
            daten.append(zeile)
        return daten

    def beratungen_gruppe(self,
                          welche=None,
                          mitarbeiter=None,
                          stelle=None,
                          ab_jahr=None,
                          grname=None):
        join=[('mitarbeitergruppe', 'gruppe.id=mitarbeitergruppe.gruppe_id'),
              ('mitarbeiter', 'mitarbeitergruppe.mit_id=mitarbeiter.id')]
        # nur die eigene Stelle
        where = []
        if stelle:
            where.append("gruppe.stz=%s" % stelle['id'])
        if ab_jahr:
            where.append("gruppe.bgy>=%s" % ab_jahr)
        if mitarbeiter:
            where.append("mitarbeiter.id=%s" % mitarbeiter['id'])
        if grname:
            expr = escape('%' + grname + '%')
            where.append("(gruppe.name like %s or gruppe.thema like %s)" % \
                     (expr, expr))
        if welche=='laufend':
            where.append('gruppe.ey=0')
        elif welche=='abgeschlossen':
            where.append('gruppe.ey>0')
        gruppe_list = GruppeList(
            where=' and '.join(where),
            join=join,
            )
        sort = ('bgy', 'bgm', 'bgd', 'name')
        gruppe_list.sort(*sort)
        return gruppe_list
    

class abfr1(_abfr):
    """Ergebnis der Abfrage aller Klienten, Beratungen
    (Tabellen: Fall, Akte, Zuständigkeit)."""
    permissions = Request.ABFR_PERM

## Jetzt in akte_share
##     def beratungen(...):
##         pass
    

    def processForm(self, REQUEST, RESPONSE):
        params = self.fall_auswahl_form()

        welche = params['welche']
        ab_jahr =  params['ab_jahr']
        ab_fallnummer =  params['ab_fallnummer']
        mitarbeiter = params['mitarbeiter']
        sort_options_data = params['sort_options_data']
        sort_sel = params['sort_sel']
        sort_seq = params['sort_seq']
        sort = params['sort']
        bis_jahr = params['bis_jahr']
        bis_fallnummer = params['bis_fallnummer']
        ab_jahr_zda =  params['ab_jahr_zda']
        bis_jahr_zda =  params['bis_jahr_zda']


        title = (welche=='laufend' and 'Laufende' or
                 welche=='abgeschlossen' and 'Abgeschlossene' or
                 welche=='alle' and 'Alle' or '') + ' Beratungen'
        if ab_fallnummer:
            legend_app = ' ab Fallnummer %s-%s%s' % (ab_fallnummer, ab_jahr, self.stelle['code'])
        elif ab_jahr:
            legend_app = ' ab Jahr %s' % (ab_jahr,)
        else:
            legend_app = ''

        #print 'PARAMS: ', params    

        anzeige = self.get_fall_auswahl('Anzuzeigende Beratungen', welche, 
                                        ab_jahr, ab_fallnummer, 
                                        bis_jahr, bis_fallnummer, 
                                        ab_jahr_zda, bis_jahr_zda,
                                        mitarbeiter, 
                                        sort_options_data, sort_sel)
        beratungen = self.beratungen(welche=welche,
                                     stelle=self.stelle,
                                     mitarbeiter=mitarbeiter,
                                     ab_jahr=ab_jahr,
                                     ab_fallnummer=ab_fallnummer,
                                     bis_jahr=bis_jahr,
                                     bis_fallnummer=bis_fallnummer,
                                     ab_jahr_zda=ab_jahr_zda,
                                     bis_jahr_zda=bis_jahr_zda,
                                     sort=sort)

        #faelle = ('fn', 'vn', 'na', 'gb', 'fallbeginn', 'fallende', 'mitarbeiter', 'fs', 'jgh')
        if config.KEINE_BUNDESSTATISTIK:
            report = h.FieldsetDataTable(
                legend=title + legend_app,
                headers=('Fallnr.', 'Vorname', 'Name', 'Geb.', 'Beginn', 'z.d.A', 'Zuständig', 'FS',),
                daten=[[h.Link(string=fall['fn'],
                               url='klkarte?akid=%(akte_id)s' % fall),
                        h.String(string=fall['akte__vn']),
                        h.String(string=fall['akte__na']),
                        h.String(string=fall['akte__gb']),
                        h.Datum(date=fall.getDate('bg')),
                        h.Datum(date=fall.getDate('zda')),
                        h.String(string=fall['zuletzt_zustaendig__mit__na']),
                        h.String(string=fall['has_fachstatistik']),
                ] for fall in beratungen],
                )
        else:
            report = h.FieldsetDataTable(
                legend=title + legend_app,
                headers=('Fallnr.', 'Vorname', 'Name', 'Geb.', 'Beginn', 'z.d.A', 'Zuständig', 'FS', 'BS'),
                daten=[[h.Link(string=fall['fn'],
                               url='klkarte?akid=%(akte_id)s' % fall),
                        h.String(string=fall['akte__vn']),
                        h.String(string=fall['akte__na']),
                        h.String(string=fall['akte__gb']),
                        h.Datum(date=fall.getDate('bg')),
                        h.Datum(date=fall.getDate('zda')),
                        h.String(string=fall['zuletzt_zustaendig__mit__na']),
                        h.String(string=fall['has_fachstatistik']),
                        h.String(string=fall['has_jghstatistik']),
                ] for fall in beratungen],
                )

        res = h.FormPage(
            title=title,
            name='beratungen',action="abfr1",method="post",
            breadcrumbs = (('Hauptmenü', 'menu'),
                           ),
            hidden=(("seq", ''.join([('%s' % i) for i in sort_seq])),
                    ),
            rows=(self.get_auswertungs_menu(),
                  anzeige,
                  report,
                  ),
            )
        return res.display()
        

class abfr3(_abfr):
    """Ergebnis der Suche in der Klienten- oder Gruppenkartei."""
    permissions = Request.ABFR_PERM

    def beratungen_bezugsperson(self, mitarbeiter=None, bzpname=None):
        join=[('zustaendigkeit', 'zustaendigkeit.fall_id=fall.id'),
              ('akte', 'bezugsperson.akte_id=akte.id'),
              ('fall', 'fall.akte_id=akte.id'),
              ('mitarbeiter', 'zustaendigkeit.mit_id=mitarbeiter.id')]
        # nur die eigene Stelle
        where = "akte.stzbg=%s" % self.stelle['id']
        # nur die letzte Zuständigkeit deren Endedatum gleich dem ZDA-Datum ist
        where += """ and fall.zday = zustaendigkeit.ey and 
        fall.zdam = zustaendigkeit.em and 
        fall.zdad = zustaendigkeit.ed"""
        if bzpname:
            expr = escape('%' + bzpname + '%')
            where += " and (bezugsperson.vn like %s or bezugsperson.na like %s)" % \
                     (expr, expr)
        if mitarbeiter:
            where += " and mitarbeiter.id = %s" % mitarbeiter['id']
        bezugsperson_list = BezugspersonList(
            where=where,
            join=join,
            )
        sort = ('na', 'vn',
        'akte__letzter_fall__bgy',
        'akte__letzter_fall__bgm',
        'akte__letzter_fall__bgd',
        )
        bezugsperson_list.sort(*sort)
        return bezugsperson_list
        
    def processForm(self, REQUEST, RESPONSE):
        expr = check_str_not_empty(self.form, 'expr', "Kein Suchausdruck")
        table = check_str_not_empty(self.form, 'table', "Keine Suchklasse")
        if not expr:
            raise EE('Kein Suchausdruck')
        if not table:
            raise EE('Keine Suchklasse')
        if self.mitarbeiter['benr__code'] == 'bearb':
            # eingeschränkt auf angemeldeten Mitarbeiter
            mitarbeiter = self.mitarbeiter
        elif self.mitarbeiter['benr__code'] == 'verw':
            mitarbeiter = None
        if table == "akte":
            headers=('Fallnr.', 'Vorname', 'Name', 'Geb.', 'Beginn', 'z.d.A', 'Zuständig')
            faelle = self.beratungen_fall(mitarbeiter, klname=expr)
            daten = self.get_table_daten(faelle,
                                         (('fn', 'klkarte?akid=%(akte_id)s'),
                                          'akte__vn', 'akte__na', 'akte__gb',
                                          'bg', 'zda', 'zuletzt_zustaendig__mit__na',
                                          ),
                                         )
            legend="Suchergebnisse für: Klientenname enthält '%s'" % expr
        elif table == "fall":
            headers=('Fallnr.', 'Vorname', 'Name', 'Geb.', 'Beginn', 'z.d.A', 'Zuständig')
            faelle = self.beratungen_fall(mitarbeiter, fn=expr)
            daten = self.get_table_daten(faelle,
                                         (('fn', 'klkarte?akid=%(akte_id)s'),
                                          'akte__vn', 'akte__na', 'akte__gb',
                                          'bg', 'zda', 'zuletzt_zustaendig__mit__na',
                                          ),
                                         )
            legend="Suchergebnisse für: Fallnummer enthält '%s'" % expr
        elif table == "bezugsperson":
            headers=('Fallnr.', 'Vorname der Bezugsperson', 'Nachname der Bezugsperson', 'Bezug', 'Beginn', 'z.d.A', 'Zuständig')
            bezugspersonen = self.beratungen_bezugsperson(mitarbeiter, bzpname=expr)
            daten = self.get_table_daten(bezugspersonen,
                                         (('akte__letzter_fall__fn', 'klkarte?akid=%(akte_id)s'),
                                          'vn', 'na', 'verw__name',
                                          'akte__letzter_fall__bg', 'akte__letzter_fall__zda',
                                          'akte__letzter_fall__zuletzt_zustaendig__mit__na',
                                          ),
                                         )
            legend="Suchergebnisse für: Bezugspersonname enthält '%s'" % expr
        elif table == "gruppe":
            headers=('Gruppennr.', 'Mitarbeiter', 'Name',
                     'Thema', 'Art', 'Teilnehmer', '-zahl', 'Beginn', 'Ende')

            gruppe_list = self.beratungen_gruppe(mitarbeiter=mitarbeiter, grname=expr)
            daten = self.get_table_daten(gruppe_list,
                                         (('gn', 'grkarte?gruppeid=%(id)s'),
                                          'mitarbeiternamen', 'name', 'thema',
                                          'grtyp__name', 'teiln__name', 'tzahl',
                                          'bg', 'e',
                                          ),
                                         )
            legend = "Suchergebnisse für: Gruppenname oder -thema enthält '%s'" % expr
        tabelle = h.FieldsetDataTable(
            legend=legend,
            headers=headers,
            daten=daten,
            )
        res = h.Page(
            title='Suchergebnisse',
            breadcrumbs = (('Hauptmenü', 'menu'),
                           ),
            rows=(self.get_zurueck(),
                  tabelle,
                  ),
            )
        return res.display()
                                         
        
class abfr4(_abfr):
    """Anzahl der Neumeldungen u. Abschlüsse pro Jahr und Quartal."""
    permissions = Request.ABFR_PERM
    def get_neumelde_abschluss_daten(self, jahr):
        "fast unverändert übernommen, müsste gestrafft werden."
        stelle = self.stelle
        JGHList = (jahr >= 2007 and Jugendhilfestatistik2007List or JugendhilfestatistikList)
        neumeldungen = FallList(where = 'bgy = %s' % jahr
                                + ' and akte_id__stzbg = %d' % stelle['id'],
                                order = 'bgm' )
        asdliste = [f for f in neumeldungen
                    if f['anmeldung'] and f['anmeldung'][0]['zm__code'] == '3']
        zdaliste = JGHList(where = 'ey = %s' % jahr
                                + ' and stz = %d' % stelle['id'],
                                order = 'em' )
        
        hauptfallliste = JGHList(where = 'ey = %s' % jahr
                                + ' and gfall = %d'   % cc('gfall', '1')
                                + ' and stz = %d' % stelle['id'],
                                order = 'em' )
        
        geschwliste = JGHList(where = 'ey = %s' % jahr
                                + ' and gfall = %d' %  cc('gfall', '2')
                                + ' and stz = %d' % stelle['id'],
                                order = 'em' )
        laufendliste = FallList(where = 'bgy <= %s' % jahr
                                + ' and akte_id__stzbg = %d' % stelle['id']
                                + ' and (zday = 0 or zday >= %s)' % jahr,
                                order = 'bgy, bgm' )
        neul = [n['bgm'] for n in neumeldungen]
        asdl = [f['bgm'] for f in asdliste]
        zdal = [z['em'] for z in zdaliste]
        hauptf = [z['em'] for z in hauptfallliste]
        geschw = [z['em'] for z in geschwliste]
        quartal1_neu = quartal1_asd = quartal1_zda = quartal1_hauptf = quartal1_geschw = 0
        quartal2_neu = quartal2_asd = quartal2_zda = quartal2_hauptf = quartal2_geschw = 0
        quartal3_neu = quartal3_asd = quartal3_zda = quartal3_hauptf = quartal3_geschw = 0
        quartal4_neu = quartal4_asd = quartal4_zda = quartal4_hauptf = quartal4_geschw = 0
        i = 1
        monats_ergebnisse = []
        while i < 13:
            # i steht für den Monat in jahr
            neumeldezahl = neul.count(i)
            asdzahl = asdl.count(i)
            zdazahl = zdal.count(i)
            hauptfzahl = hauptf.count(i)
            geschwzahl = geschw.count(i)
            laufendzahl = 0
            davonkeinzdazahl = 0
            # immer der erste des Folgemonats
            if i == 12:
                laufend_stichtag = Date(jahr+1, 1, 1)
            else:
                laufend_stichtag = Date(jahr, i+1, 1)
            for f in laufendliste:
                if (f.getDate('bg') < laufend_stichtag and
                    f.getDate('zda') >= laufend_stichtag):
                    laufendzahl +=1
                    jgh = f['jgh']
                    if jgh and jgh['ey'] == jahr and jgh['em'] == i:
                        # laufender Fall am Ende des Monats, aber 
                        # Ende der Beratung für diesen Monat bereits eingetragen
                        davonkeinzdazahl += 1
            if i <= 3:
                quartal1_neu += neumeldezahl
                quartal1_asd += asdzahl
                quartal1_zda += zdazahl
                quartal1_hauptf +=  hauptfzahl
                quartal1_geschw +=  geschwzahl
                # msg systems 02.07.2002 fehler der schon in ebkus 2.0 vorhanden war
                # zufaellig gefunden und korrigiert.
                # if i > 3 < 7:
            elif i <= 6:
                quartal2_neu += neumeldezahl
                quartal2_asd += asdzahl
                quartal2_zda += zdazahl
                quartal2_hauptf += hauptfzahl
                quartal2_geschw += geschwzahl
            elif i <= 9:
                quartal3_neu += neumeldezahl
                quartal3_asd += asdzahl
                quartal3_zda += zdazahl
                quartal3_hauptf += hauptfzahl
                quartal3_geschw += geschwzahl
            elif i <= 12:
                quartal4_neu += neumeldezahl
                quartal4_asd += asdzahl
                quartal4_zda += zdazahl
                quartal4_hauptf += hauptfzahl
                quartal4_geschw += geschwzahl
            monats_ergebnisse.append((i, laufendzahl, neumeldezahl, asdzahl,
                                      hauptfzahl, geschwzahl, zdazahl, davonkeinzdazahl)) 
            i = i + 1
        quartals_ergebnisse = []
        quartals_ergebnisse.append((1, quartal1_neu, quartal1_asd, quartal1_hauptf,
                                    quartal1_geschw, quartal1_zda,))
        
        quartals_ergebnisse.append((2, quartal2_neu, quartal2_asd, quartal2_hauptf,
                                    quartal2_geschw, quartal2_zda,))
        quartals_ergebnisse.append((3, quartal3_neu, quartal3_asd, quartal3_hauptf,
                                    quartal3_geschw, quartal3_zda,))
        quartals_ergebnisse.append((4, quartal4_neu, quartal4_asd, quartal4_hauptf,
                                    quartal4_geschw, quartal4_zda,))
        gesamt_ergebnisse = (len(neul), len(asdl), len(hauptf), len(geschw), len(zdal))
        return monats_ergebnisse, quartals_ergebnisse, gesamt_ergebnisse
    
    def get_neumelde_abschluss_daten_ohne_bundesstatistik(self, jahr):
        "So viel wie möglich aber ohne Rückgriff auf die Bundesstatistik."
        stelle = self.stelle
        neumeldungen = FallList(where = 'bgy = %s' % jahr
                                + ' and akte_id__stzbg = %d' % stelle['id'],
                                order = 'bgm' )
        asdliste = [f for f in neumeldungen
                    if f['anmeldung'] and f['anmeldung'][0]['zm__code'] == '3']
        zdaliste_fall = FallList(where = 'zday = %s' % jahr
                                + ' and akte_id__stzbg = %d' % stelle['id'],
                                order = 'zdam' )
        laufendliste = FallList(where = 'bgy <= %s' % jahr
                                + ' and akte_id__stzbg = %d' % stelle['id']
                                + ' and (zday = 0 or zday >= %s)' % jahr,
                                order = 'bgy, bgm' )
        neul = [n['bgm'] for n in neumeldungen]
        asdl = [f['bgm'] for f in asdliste]
        zdal = [z['zdam'] for z in zdaliste_fall]
        quartal1_neu = quartal1_asd = quartal1_zda = quartal1_hauptf = quartal1_geschw = 0
        quartal2_neu = quartal2_asd = quartal2_zda = quartal2_hauptf = quartal2_geschw = 0
        quartal3_neu = quartal3_asd = quartal3_zda = quartal3_hauptf = quartal3_geschw = 0
        quartal4_neu = quartal4_asd = quartal4_zda = quartal4_hauptf = quartal4_geschw = 0
        i = 1
        monats_ergebnisse = []
        while i < 13:
            # i steht für den Monat in jahr
            neumeldezahl = neul.count(i)
            asdzahl = asdl.count(i)
            zdazahl = zdal.count(i)
            laufendzahl = 0
            # immer der erste des Folgemonats
            if i == 12:
                laufend_stichtag = Date(jahr+1, 1, 1)
            else:
                laufend_stichtag = Date(jahr, i+1, 1)
            for f in laufendliste:
                if (f.getDate('bg') < laufend_stichtag and
                    f.getDate('zda') >= laufend_stichtag):
                    laufendzahl +=1
            if i <= 3:
                quartal1_neu += neumeldezahl
                quartal1_asd += asdzahl
                quartal1_zda += zdazahl
            elif i <= 6:
                quartal2_neu += neumeldezahl
                quartal2_asd += asdzahl
                quartal2_zda += zdazahl
            elif i <= 9:
                quartal3_neu += neumeldezahl
                quartal3_asd += asdzahl
                quartal3_zda += zdazahl
            elif i <= 12:
                quartal4_neu += neumeldezahl
                quartal4_asd += asdzahl
                quartal4_zda += zdazahl
            monats_ergebnisse.append((i, laufendzahl, neumeldezahl, asdzahl,
                                      zdazahl, 
                                      )) 
            i = i + 1
        quartals_ergebnisse = []
        quartals_ergebnisse.append((1, quartal1_neu, quartal1_asd, 
                                    quartal1_zda,))
        
        quartals_ergebnisse.append((2, quartal2_neu, quartal2_asd, 
                                    quartal2_zda,))
        quartals_ergebnisse.append((3, quartal3_neu, quartal3_asd, 
                                    quartal3_zda,))
        quartals_ergebnisse.append((4, quartal4_neu, quartal4_asd, 
                                    quartal4_zda,))
        gesamt_ergebnisse = (len(neul), len(asdl), 
                             len(zdal))
        return monats_ergebnisse, quartals_ergebnisse, gesamt_ergebnisse

    def processForm(self, REQUEST, RESPONSE):
        jahr = check_int_not_empty(self.form, 'jahr', "Fehler im Jahr", '')
        if not jahr:
            jahr = today().year
        anzeige = h.FieldsetInputTable(
            legend='Jahr wählen',
            daten=[[h.SelectItem(label='Jahr',
                                 name='jahr',
                                 class_='listbox45',
                                 tip='Neumeldungen und Abschlüsse für das gewählte Jahr',
                                 options=self.for_jahre(sel=jahr),
                                 ),
                    h.Button(value="Anzeigen",
                             name='op',
                             tip="Neumeldungen und Abschlüsse anzeigen",
                             type='submit',
                             n_col=2,
                             ),
                    ],
                   ],
            )
        if config.KEINE_BUNDESSTATISTIK:
            report = self.get_report_ohne_bundesstatistik(jahr)
        else:
            report = self.get_report(jahr)
        res = h.FormPage(
            title='Neumelde- und Abschlusszahlen',
            name='neumelde',action="abfr4",method="post",
            breadcrumbs = (('Hauptmenü', 'menu'),
                           ),
            hidden=(),
            rows=(self.get_auswertungs_menu(),
                  anzeige,
                  report,
                  self.get_neumelde_nach_region_tabelle(jahr)
                  ),
            )
        return res.display()
        #faelle = ('fn', 'vn', 'na', 'gb', 'fallbeginn', 'fallende', 'mitarbeiter', 'fs', 'jgh')

    def get_report(self, jahr):
        monats_ergebnisse, quartals_ergebnisse, gesamt_ergebnisse = \
                           self.get_neumelde_abschluss_daten(jahr)
        report = h.FieldsetDataTable(
            legend='Neumeldungen und Abschlüsse %s' % jahr,
            headers=('Monat', 'Laufende am Monatsende', 'Neu', 'davon ASD', 'Hauptfall',
                     'Geschwisterfall', 'abgeschl. Bundesstatistik', 'davon noch ohne z.d.A'),
            daten=[[h.String(string=m[0]),
                    h.String(string=m[1]),
                    h.String(string=m[2]),
                    h.String(string=m[3]),
                    h.String(string=m[4]),
                    h.String(string=m[5]),
                    h.String(string=m[6]),
                    h.String(string=m[7]),
            ] for m in monats_ergebnisse] +
            [[h.String(string='Quartal&nbsp;%s' % m[0],
                      class_='tabledatabold'),
             h.String(string=''),
             h.String(string=m[1],
                      class_='tabledatabold'),
             h.String(string=m[2],
                      class_='tabledatabold'),
             h.String(string=m[3],
                      class_='tabledatabold'),
             h.String(string=m[4],
                      class_='tabledatabold'),
             h.String(string=m[5],
                      class_='tabledatabold'),
             h.String(string=''),
             ] for m in quartals_ergebnisse] +
            [[h.String(string='Gesamt',
                      class_='tabledatabold'),
             h.String(string=''),
             h.String(string=gesamt_ergebnisse[0],
                      class_='tabledatabold'),
             h.String(string=gesamt_ergebnisse[1],
                      class_='tabledatabold'),
             h.String(string=gesamt_ergebnisse[2],
                      class_='tabledatabold'),
             h.String(string=gesamt_ergebnisse[3],
                      class_='tabledatabold'),
             h.String(string=gesamt_ergebnisse[4],
                      class_='tabledatabold'),
             h.String(string=''),
             ]],
            )
        return report

    def get_report_ohne_bundesstatistik(self, jahr):
        monats_ergebnisse, quartals_ergebnisse, gesamt_ergebnisse = \
                           self.get_neumelde_abschluss_daten_ohne_bundesstatistik(jahr)
        report = h.FieldsetDataTable(
            legend='Neumeldungen und Abschlüsse %s' % jahr,
            headers=('Monat', 'Laufende am Monatsende', 'Neu', 'davon ASD', 
                     'Abgeschlossen', #'abgeschl. Bundesstatistik', 
                     ),
            daten=[[h.String(string=m[0]),
                    h.String(string=m[1]),
                    h.String(string=m[2]),
                    h.String(string=m[3]),
                    h.String(string=m[4]),
            ] for m in monats_ergebnisse] +
            [[h.String(string='Quartal&nbsp;%s' % m[0],
                      class_='tabledatabold'),
             h.String(string=''),
             h.String(string=m[1],
                      class_='tabledatabold'),
             h.String(string=m[2],
                      class_='tabledatabold'),
             h.String(string=m[3],
                      class_='tabledatabold'),
             h.String(string=''),
             ] for m in quartals_ergebnisse] +
            [[h.String(string='Gesamt',
                      class_='tabledatabold'),
             h.String(string=''),
             h.String(string=gesamt_ergebnisse[0],
                      class_='tabledatabold'),
             h.String(string=gesamt_ergebnisse[1],
                      class_='tabledatabold'),
             h.String(string=gesamt_ergebnisse[2],
                      class_='tabledatabold'),
             h.String(string=''),
             ]],
            )
        return report

    def get_neumelde_nach_region_daten(self, jahr):
        """Konfigurationsvariable:
        neumeldungen_nach_region: name1;name2;name3
        """
        abfrage_namen = [name.strip() for name in config.NEUMELDUNGEN_NACH_REGION.split(';') if name.strip()]

        # queries = None
        # if abfrage_namen:
        #     abfragen = AbfrageList(where='name in (%s)' % ','.join([("'%s'" % n) for n in abfrage_namen]))
        #     queries = [(a['name'], Query(a)) for a in abfragen]
        # if not queries:
        #     return None,None,None,None

        queries = []
        for n in abfrage_namen:
            abfragen = AbfrageList(where="name = '%s'" % n)
            if abfragen:
                queries.append((n, Query(abfragen[0])))
        if not queries:
            return None,None,None,None


        stelle = self.stelle
        #JGHList = (jahr >= 2007 and Jugendhilfestatistik2007List or JugendhilfestatistikList)
        neumeldungen = FallList(where = 'bgy = %s' % jahr
                                + ' and akte_id__stzbg = %d' % stelle['id'],
                                order = 'bgm' )
        neul = [n['bgm'] for n in neumeldungen]
        # analog für Regionen
        # für jede Region eine Liste, jeder Eintrag entspricht einem Monat, in der die Neumeldung
        # aus dieser Region erfolgte.
        # Liste (name, monatsliste)
        regiolisten = []
        for name, query in queries:
            rl = [f['bgm'] for f in neumeldungen if query.test(f['akte'])]
            regiolisten.append(rl)
        n = len(regiolisten) + 1 # Neumeldungen, für jede Region eine weitere Spalte
        quartale = [([i]+[0]*n) for i in range(1,5)] # zusätzlich Quartalsnummer als erstes Element
        monate =   [([i]+[0]*n) for i in range(1,13)] # zusätzlich Monatsnummer als erstes Element
        for monat in monate:
            # i steht für den Monat in jahr
            i = monat[0]
            #print 'MONAT', i, 'QUARTAL', getQuartal(i)
            #print quartale
            quartal = quartale[getQuartal(i)-1] # getQuartal: {1..12} --> {1..4}
            monat[1] = neul.count(i)
            quartal[1] += monat[1]
            for j,rl in enumerate(regiolisten):
                monat[j+2] = rl.count(i)
                quartal[j+2] += monat[j+2]
        gesamt = (len(neul),) + tuple([len(rl) for rl in regiolisten])
        return tuple(abfrage_namen), monate, quartale, gesamt
    
    def get_neumelde_nach_region_tabelle(self, jahr):
        """Neumeldungen aufgeteilt nach Region.
        Gibts nur, wenn die Konfigurationsvariable 'neumeldungen_nach_region' 
        eingerichtet ist.
        neumeldungen_nach_region: name1;name2;name3
        name1, ... sind Namen von Teilmengendefinitionen, die in der Tabelle abfrage
        gespeichert sind.
        """
        regionen, monats_ergebnisse, quartals_ergebnisse, gesamt_ergebnisse = \
            self.get_neumelde_nach_region_daten(jahr)
        if not regionen:
            return None
        report_nach_region = h.FieldsetDataTable(
            legend='Neumeldungen nach Region %s' % jahr,
            headers=('Monat', 'Neu gesamt',) + tuple([("davon aus %s" % r) for r in regionen]),
            daten=
            [[h.String(string=m[i]) for i in range(len(m))]
              for m in monats_ergebnisse] +

            [[h.String(string='Quartal&nbsp;%s' % q[0],
                       class_='tabledatabold'),] +
             [h.String(string=q[i],
                       class_='tabledatabold')
              for i in range(1, len(q))]
             for q in quartals_ergebnisse] +
        
            [[h.String(string='Gesamt',
                       class_='tabledatabold'),] +
             [h.String(string=g,
                       class_='tabledatabold')
              for g in gesamt_ergebnisse]
             ],
        )
        return report_nach_region
        
        

class abfr5(_abfr):
    """Klientenzahl pro Mitarbeiter u. Jahr."""
    permissions = Request.ABFR_PERM
    def get_mitarbeiter_ergebnisse(self, jahr):
        a = b = c = d = e = 0
        mitarbeiter_ergebnisse = []
        for m in self.getMitarbeiterliste():
            neuel = ZustaendigkeitList(where = 'bgy = %s' % jahr
                                       + ' and mit_id = %d ' %m['id'])
            davon_fallbeginn = [z for z in neuel
                                if z['fall'].getDate('bg') == z.getDate('bg')]
            laufendl = ZustaendigkeitList(where = 'ey = 0 and bgy <= %s' % jahr
                                         + ' and bgy > 1980 and mit_id = %d ' %m['id'])
            abgeschl = ZustaendigkeitList(where = 'ey = %s' % jahr
                                           + ' and mit_id = %d ' %m['id'])
            davon_zda = [z for z in abgeschl
                         if z['fall'].getDate('zda') == z.getDate('e')]
            mitarbeiter_ergebnisse.append((m['na'], len(neuel),len(davon_fallbeginn),
                                           len(laufendl), len(abgeschl), len(davon_zda)))
            a = a + len(neuel)
            b = b + len(davon_fallbeginn)
            c = c + len(laufendl)
            d = d + len(abgeschl)
            e = e + len(davon_zda)
        gesamt = a,b,c,d,e
        return mitarbeiter_ergebnisse, gesamt
    def processForm(self, REQUEST, RESPONSE):
        jahr = check_int_not_empty(self.form, 'jahr', "Fehler im Jahr", '')
        if not jahr:
            jahr = today().year
        anzeige = h.FieldsetInputTable(
            legend='Jahr wählen',
            daten=[[h.SelectItem(label='Jahr',
                                 name='jahr',
                                 class_='listbox45',
                                 tip='Klientenzahl pro Mitarbeiter für das gewählte Jahr',
                                 options=self.for_jahre(sel=jahr),
                                 ),
                    h.Button(value="Anzeigen",
                             name='op',
                             tip="Klientenanzahl pro Mitarbeiter anzeigen",
                             type='submit',
                             n_col=2,
                             ),
                    ],
                   ],
            )
        mitarbeiter_ergebnisse, gesamt = self.get_mitarbeiter_ergebnisse(jahr)
        report = h.FieldsetDataTable(
            legend='Neumeldungen und Abschlüsse pro Mitarbeiter %s' % jahr,
            headers=('Mitarbeiter', 'Neu', 'davon Fallbeginn', 'Laufend', 'Beendet','davon z.d.A.'),
            daten=[[h.String(string=m[0]),
                    h.String(string=m[1],
                             tip='Zuständigkeit neu übernommen'),
                    h.String(string=m[2],
                             tip='Zuständigkeit für neuen Fall übernommen'),
                    h.String(string=m[3],
                             tip='Laufende Fälle am Ende des Jahres'),
                    h.String(string=m[4],
                             tip='Zuständigkeit beendet'),
                    h.String(string=m[5],
                             tip='Zuständigkeitsende durch Fallabschluss'),
            ] for m in mitarbeiter_ergebnisse] +
            [[h.String(string='Gesamt',
                      class_='tabledatabold'),
             h.String(string=gesamt[0],
                      class_='tabledatabold',
                      tip='Zuständigkeit neu übernommen'),
             h.String(string=gesamt[1],
                      class_='tabledatabold',
                      tip='Zuständigkeit für neuen Fall übernommen'),
             h.String(string=gesamt[2],
                      class_='tabledatabold',
                      tip='Laufende Fälle am Ende des Jahres'),
             h.String(string=gesamt[3],
                      class_='tabledatabold',
                      tip='Zuständigkeit beendet'),
             h.String(string=gesamt[4],
                      class_='tabledatabold',
                      tip='Zuständigkeitsende durch Fallabschluss'),
             ]],
            )
        res = h.FormPage(
            title='Neumeldungen und Abschlüsse pro Mitarbeiter',
            name='neumelde',action="abfr5",method="post",
            breadcrumbs = (('Hauptmenü', 'menu'),
                           ),
            hidden=(),
            rows=(self.get_auswertungs_menu(),
                  anzeige,
                  report,
                  ),
            )
        return res.display()


class abfr8(_abfr):
    "Gruppenübersicht"
    permissions = Request.ABFR_PERM
    def processForm(self, REQUEST, RESPONSE):
        jahr = check_int_not_empty(self.form, 'jahr', "Fehler im Jahr", '')
        anzeige = h.FieldsetInputTable(
            legend='Jahr wählen',
            daten=[[h.SelectItem(label='Ab Jahr',
                                 name='jahr',
                                 class_='listbox45',
                                 tip='Gruppenbeginn ab dem gewählten Jahr',
                                 options=self.for_jahre(sel=jahr,
                                                        erster_eintrag='Alle'),
                                 ),
                    h.Button(value="Anzeigen",
                             name='op',
                             tip="Gruppen anzeigen",
                             type='submit',
                             n_col=2,
                             ),
                    ],
                   ],
            )
        mitarbeiter = welche = stelle = None
        gruppe_list = self.beratungen_gruppe(ab_jahr=jahr,
                                             mitarbeiter=mitarbeiter,
                                             welche=welche,
                                             stelle=stelle)
        headers=('Gruppennr.', 'Mitarbeiter', 'Name',
                 'Thema', 'Art', 'Teilnehmer', '-zahl', 'Beginn', 'Ende')
        daten = self.get_table_daten(gruppe_list,
                                     (('gn', 'grkarte?gruppeid=%(id)s'),
                                      'mitarbeiternamen', 'name', 'thema',
                                      'grtyp__name', 'teiln__name', 'tzahl',
                                      'bg', 'e',
                                      ),
                                     )
        report = h.FieldsetDataTable(
            legend='Gruppenüberblick',
            headers=headers,
            daten=daten,
            )
        res = h.FormPage(
            title='Gruppenüberblick',
            name='gruppenue',action="abfr8",method="post",
            breadcrumbs = (('Hauptmenü', 'menu'),
                           ),
            hidden=(),
            rows=(self.get_auswertungs_menu(),
                  anzeige,
                  report,
                  ),
            )
        return res.display()
        
class wartezeiten(_abfr):
    """Tabelle mit Wartezeiten zwischen Anmeldung und Erstleistung."""
    permissions = Request.ABFR_PERM
    def processForm(self, REQUEST, RESPONSE):
        jahr = check_int_not_empty(self.form, 'jahr', "Fehler im Jahr", '')
        if not jahr:
            jahr = today().year
        anzeige = h.FieldsetInputTable(
            legend='Jahr wählen',
            daten=[[h.SelectItem(label='Jahr',
                                 name='jahr',
                                 class_='listbox45',
                                 tip='Wartezeiten für das gewählte Jahr',
                                 options=self.for_jahre(sel=jahr),
                                 ),
                    h.Button(value="Anzeigen",
                             name='op',
                             tip="Tabelle mit Wartezeiten anzeigen",
                             type='submit',
                             n_col=2,
                             ),
                    ],
                   ],
            )
        # Fälle ermitteln, wo der Leistungsbeginn in dem gewählten
        # Jahr liegt
        faelle = self.beratungen(welche='alle',
                                 stelle=self.stelle,
                                 ab_jahr=jahr-1, # Vorjahr mit einbeziehen
                                 bis_jahr=jahr,
                                 sort=('bg',))
        faelle = faelle.filter(lambda x: x['leistungsbeginn'].year==jahr)

        auszaehlung = BereichsKategorieAuszaehlung(faelle,
                                                   'wartezeit', 
                                                   'wartez',
                                                   title='Verteilung der Wartezeiten',
                                                   )
        ausz_res = auszaehlung.get_result()
        summe_haeufigkeiten = sum([m[1] for m in ausz_res])
        summe_prozent = sum([m[2] for m in ausz_res])
        haeufigkeiten = h.FieldsetDataTable(
            legend='Wartezeiten für Fälle mit erster Leistung im Jahr %s' % jahr,
            headers=('', 'Häufigkeit', 'Prozent',),
            daten=[[h.String(string=m[0]),
                    h.String(string=m[1],
                             class_="tabledataright",),
                    h.String(string="%.2f" % m[2],
                             class_="tabledataright",),
            ] for m in ausz_res] + 
            [[h.String(string='Summe',
                       class_='tabledatabold',
                       ),
              h.String(string=summe_haeufigkeiten,
                       class_='tabledataboldright',
                       align="right",
                       ),
              h.String(string="%.2f" % summe_prozent,
                       align="right",
                       class_='tabledataboldright',
                       ),
              ]
             ]
            )

        faelle.sort('wartezeit')
#         for f in faelle:
#             print f['fn'], f['bg'], f['leistungsbeginn'], f['wartezeit']
        if len(faelle) > 0:
            median = faelle[(len(faelle)/2)]['wartezeit']
            mittelwert = sum([f['wartezeit'] for f in
                              faelle])/float(len(faelle))
        else:
            median = 'NA'
            mittelwert = 'NA'
        
        mittel = h.FieldsetDataTable(
            legend='Mittelwert und Median der Wartezeiten in '
            'Kalendertagen für Fälle mit erster Leistung im Jahr %s' % jahr,
            daten=[[h.String(string='Mittelwert (n=%s)' % len(faelle),
                             class_='tabledatabold',
                             ),
                    h.String(string="%s" % (isinstance(mittelwert,
                                                       (int,long,float))
                                            and ("%.2f" % mittelwert)
                                            or mittelwert,),
                             align="right",
                             class_='tabledataboldright',
                             ),
                    ],
                   [h.String(string='Median (n=%s)' % len(faelle),
                             class_='tabledatabold',
                             ),
                     h.String(string="%s" % median,
                              align="right",
                              class_='tabledataboldright',
                              ),
                    ],
                   ]
            )
        res = h.FormPage(
            title='Wartezeiten',
            name='wartezeiten',action="wartezeiten",method="post",
            breadcrumbs = (('Hauptmenü', 'menu'),
                           ),
            hidden=(),
            rows=(self.get_auswertungs_menu(),
                  anzeige,
                  haeufigkeiten,
                  mittel,
                  ),
            )
        return res.display()
