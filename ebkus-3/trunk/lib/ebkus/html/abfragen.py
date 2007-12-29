# coding: latin-1
"""Module für die Abfragen."""

# TODO: nicht gebrauchte Abfragen entfernen: formabfr3, abfr3, formabfr8 - 14 (ohne 'a')

import sys
from ebkus.config import config
CLIKE = 'like' # gibts andere DBs wo das nicht geht?
from ebkus.app import Request
from ebkus.app.ebapi import nfc, Fachstatistik, FachstatistikList, \
     JugendhilfestatistikList, Jugendhilfestatistik2007List, \
     ZustaendigkeitList, AkteList, BezugspersonList, FallList, GruppeList, \
     Tabelle, Code, Feld, Mitarbeiter, MitarbeiterList, MitarbeiterGruppeList, \
     today, cc, check_int_not_empty, \
     check_str_not_empty, EBUpdateDataError, EE, getQuartal, get_rm_datum, Date
from ebkus.app.ebapih import get_codes, mksel, get_all_codes
from ebkus.html.statistik_ergebnis import auszergebnis
from ebkus.app.statistik import CodeAuszaehlung, WertAuszaehlung
from ebkus.app_surface.standard_templates import *
from ebkus.app_surface.abfragen_templates import *
        
import ebkus.html.htmlgen as h
from ebkus.html.akte_share import akte_share



## # ab Fallnummer        
## class formabfr2(Request.Request):
##     """Suchformular (Tabellen: Fall, Akte, Zuständigkeit)."""
    
##     permissions = Request.ABFR_PERM
    
##     def processForm(self, REQUEST, RESPONSE):
##         mitarbeiterliste = self.getMitarbeiterliste()
##         user = self.user
##         stellen = get_all_codes('stzei')
        
##         res = []
##         res.append(head_normal_t %("Suche alle Beratungen ab Fallnummer"))
##         res.append(suchefallnummer_t)
##         mksel(res, codeliste_t, stellen, 'id', self.stelle['id'])
##         res.append(suchefallnummer2_t)
##         return ''.join(res)
        
        


class abfr1(Request.Request, akte_share):
    """Ergebnis der Abfrage aller Klienten, Beratungen
    (Tabellen: Fall, Akte, Zuständigkeit)."""
    permissions = Request.ABFR_PERM
    def beratungen(self, welche, mitarbeiter=None,
                   stelle=None,
                   ab_jahr=None,
                   ab_fallnummer=None,
                   sort=()):
        assert welche in ('laufend', 'abgeschlossen', 'alle')
        assert ab_jahr and ab_fallnummer or not ab_fallnummer
        where = 'fall.zday %s 0' % (welche=='laufend' and '=' or
                                    welche=='abgeschlossen' and '>' or
                                    welche=='alle' and '>='
                                    )
        # nur die letzte Zuständigkeit deren Endedatum gleich dem ZDA-Datum ist
        where += """ and fall.zday = zustaendigkeit.ey and 
        fall.zdam = zustaendigkeit.em and 
        fall.zdad = zustaendigkeit.ed"""
        
        if mitarbeiter:
            where += ' and mitarbeiter.id=%s' % mitarbeiter['id']
        if stelle:
            where += ' and akte.stzbg=%s' % stelle['id']
        if ab_jahr:
            where += ' and fall.bgy >= %s' % ab_jahr
        fall_list = FallList(
            where=where,
            join=[('zustaendigkeit', 'zustaendigkeit.fall_id=fall.id'),
                  ('akte', 'fall.akte_id=akte.id'),
                  ('mitarbeiter', 'zustaendigkeit.mit_id=mitarbeiter.id')])
        if ab_jahr and ab_fallnummer:
            def ab_fn(fall):
                j = fall['bgy']
                c = fall['fn_count'] # Fallnummerzähler, definiert in ebapi.py
                return  j > ab_jahr or (j == ab_jahr and c >= ab_fallnummer)
            fall_list = fall_list.filter(ab_fn)
        fall_list.sort(*sort)
        return fall_list

    def processForm(self, REQUEST, RESPONSE):
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
        sel = ' selected="selected"'
        welche_options = '\n'.join([tmpl % (v,
                                            v==welche and sel or '',
                                            v.capitalize())
                                    for v in ('laufend', 'abgeschlossen', 'alle')])
        title = (welche=='laufend' and 'Laufende' or
                 welche=='abgeschlossen' and 'Abgeschlossene' or
                 welche=='alle' and 'Alle' or '') + ' Beratungen'
        legend_app = ''
        jahr = check_int_not_empty(self.form, 'jahr', "Fehler im Jahr", '')
        fn_count = check_int_not_empty(self.form, 'fnc', "Fehler in laufender Nummer", '')
        if fn_count and not jahr:
            raise EE("Laufende Fallnummer nur zusammen mit Jahr")
        if fn_count:
            legend_app += ' ab Fallnummer %s-%s%s' % (fn_count, jahr, self.stelle['code'])
        elif jahr:
            legend_app += ' ab Jahr %s' % (jahr,)
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
        sort_options = '\n'.join([tmpl % (c, c==seq_new and sel or '', n)
                                  for c, n in sort_options_data])
        sort = tuple([default_sort[i] for i in seq])
        mitarbeiter = None
        if self.mitarbeiter['benr__code'] == 'verw':
            if mit_id:
                mitarbeiter = Mitarbeiter(mit_id)
                mitarbeiter_options = (tmpl % ('', '', 'Alle')
                + self.for_mitarbeiter(sel=int(mit_id)))
            else:
                mitarbeiter_options = (tmpl % ('', 'selected="selected"', 'Alle')
                + self.for_mitarbeiter(sel=None))
        elif self.mitarbeiter['benr__code'] == 'bearb':
            mitarbeiter = self.mitarbeiter
        beratungen = self.beratungen(welche=welche,
                                     stelle=self.stelle,
                                     mitarbeiter=mitarbeiter,
                                     ab_jahr=jahr,
                                     ab_fallnummer=fn_count,
                                     sort=sort)

        anzeige = h.FieldsetInputTable(
            legend='Anzuzeigende Beratungen',
            daten=[[h.SelectItem(label='Welche',
                                 name='w',
                                 options=welche_options,
    tip='Nur laufende, nur abgeschlossene, oder alle Fälle zeigen',
                                 ),
                    h.SelectItem(label='Fallbeginn ab Jahr',
                                 name='jahr',
                                 class_='listbox45',
                                 tip='Nur Fälle ab dem gewählten Jahr zeigen',
                                 options=self.for_jahre(sel=jahr,
                                                        erster_eintrag='Alle'),
                                 ),
                    h.TextItem(label='ab laufender Nummer',
                               name='fnc',
                               class_='textboxmid',
                               value=fn_count,
                               tip='Nur Fälle ab der laufenden Nummer des gewählten Jahres zeigen',
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
                     h.SelectItem(label='Sortieren nach',
                                  name='seqn',
                                  tip='Wonach die Fälle sortiert sein sollen',
                                  options=sort_options,
                                  ),
                    ],
                   [h.Dummy(n_col=8)],
                   [h.Button(value="Anzeigen",
                             name='op',
                             tip="Beratungen anzeigen",
                             type='submit',
                             n_col=8,
                             ),
                    ],
                   ],
            )

        #faelle = ('fn', 'vn', 'na', 'gb', 'fallbeginn', 'fallende', 'mitarbeiter', 'fs', 'jgh')
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
            hidden=(("seq", ''.join([('%s' % i) for i in seq])),
                    ),
            rows=(self.get_auswertungs_menu(),
                  anzeige,
                  report,
                  ),
            )
        return res.display()
        
##     def processForm(self, REQUEST, RESPONSE):
##         mitarbeiterliste = self.getMitarbeiterliste()
##         user = self.user
##         mitarbeiter = self.mitarbeiter
##         stelle = self.stelle
        
##         try:
##             o = check_str_not_empty(self.form, 'o', "Kein Operator")
##             ed = check_int_not_empty(self.form, 'ed', "Kein Datum", 0)
##         except EBUpdateDataError, e:
##             meldung = {'titel':'Fehler',
##                        'legende':'Fehlerbeschreibung',
##                        'zeile1': str(e),
##                        'zeile2':'Versuchen Sie es bitte erneut.'}
##             return (meldung_t %meldung)
            
##         if o == 'laufend':
##             ber = 'Laufende'
##             op = '='
##         elif o == 'alle':
##             ber = 'Alle'
##             op = '>='
##         elif o == 'zda':
##             ber = 'Abgeschlossene'
##             op = '>'
            
            
##         res = []
##         res.append(head_normal_t %("%s Beratungen" %ber))
##         res.append(thabfr1_t)
##         if mitarbeiter['benr__code'] == 'bearb':
##             zustaendigkeiten = ZustaendigkeitList(where = 'ed %s %s and mit_id = %s'
##                                                   % (op, ed, mitarbeiter['id'] ))
##             zustaendigkeiten.sort('mit_id__na', 'fall_id__akte_id__na',
##                                   'fall_id__akte_id__vn')
##             for z in zustaendigkeiten:
##                 if z['fall_id__akte_id__stzak'] == stelle['id']:
##                     res.append(abfr1_t % z)
                    
##         elif mitarbeiter['benr__code'] == 'verw':
##             zustaendigkeiten = ZustaendigkeitList(where = 'ed %s %s' %(op, ed)
##                                                   , order = 'id')
##             # Auch nach Mitarbeiter sortieren
##             zustaendigkeiten.sort('mit_id__na', 'fall_id__akte_id__na',
##                                   'fall_id__akte_id__vn')
##             #zustaendigkeiten.sort('fall_id__id')
##             # nur Fälle der Stelle des Mitarbeiters
##             # Reihenfolge: Jahr, Fallnummer
##             for z in zustaendigkeiten:
##                 if z['fall_id__akte_id__stzak'] == stelle['id']:
##                     res.append(abfr1_t % z)
                    
##         elif mitarbeiter['benr__code'] == 'admin':
##             zustaendigkeiten = ZustaendigkeitList(where = 'ed %s %s' %(op, ed)
##                                                   , order = 'id')
##             zustaendigkeiten.sort('fall_id__id')
##             for z in zustaendigkeiten:
##                 if z['fall_id__akte_id__stzak'] == stelle['id']:
##                     res.append(abfr1_t % z)
##         res.append(abfr1b_t)
##         return ''.join(res)
        
        
        
## class abfr2(Request.Request):
##     """Ergebnis der Suche in der Klienten- oder Gruppenkartei."""
    
##     permissions = Request.ABFR_PERM
    
##     def processForm(self, REQUEST, RESPONSE):
##         mitarbeiterliste = self.getMitarbeiterliste()
##         user = self.user
##         mitarbeiter = self.mitarbeiter
##         stelle = self.stelle
        
##         try:
##             fn = check_str_not_empty(self.form, 'expr', "Keine Fallnummer")
##             stzid = check_int_not_empty(self.form, 'stz', "Kein Stellenzeichen")
##         except EBUpdateDataError, e:
##             meldung = {'titel':'Fehler',
##                        'legende':'Fehlerbeschreibung',
##                        'zeile1': str(e),
##                        'zeile2':'Versuchen Sie es bitte erneut.'}
##             return (meldung_t %meldung)
            
##         op = '>='
##         ed = 0
##         if op == '=':
##             ber = 'Laufende'
##         elif op == '>=':
##             ber = 'Alle'
##         elif op == '>':
##             ber = 'Abgeschlossene'
            
##         stelle = Code(id=stzid)
##         faelle = FallList(where = "fn = '%s' " % fn )
##         if len(faelle) == 1:
##             fall = faelle[0]
##         else:
##             res = []
##             meldung = {'titel':'Suche nicht erfolgreich.',
##                      'legende':'Suche nicht erfolgreich',
##                      'zeile1':'Es konnte kein Fall eindeutig identifiziert werden!',
##                      'zeile2':'Versuchen Sie es bitte erneut.'}
##             res.append(meldung_t % meldung)
##             return ''.join(res)
            
##             # Headerblock, Menue u. Überschrift fuer das HTML-Template
            
##         res = []
##         res.append(head_normal_t %("Alle Beratungen ab Fallnummer"))
##         res.append(thabfr1_t)
        
##         if mitarbeiter['benr__code'] == 'bearb':
##             zustaendigkeiten = ZustaendigkeitList(where = 'ed %s %s and mit_id = %s and fall_id >= %s'
##                        % (op, ed, mitarbeiter['id'], fall['id'] ))
##             zustaendigkeiten.sort('mit_id__na', 'fall_id__akte_id__na',
##                                   'fall_id__akte_id__vn')
##             for z in zustaendigkeiten:
##                 if z['fall_id__akte_id__stzbg'] == stelle['id']:
##                     res.append(abfr1_t % z)
                    
##         elif mitarbeiter['benr__code'] == 'verw':
##             zustaendigkeiten = ZustaendigkeitList(where = 'ed %s %s and fall_id >= %s'
##                                               % (op, ed, fall['id']) , order = 'id')
##             zustaendigkeiten.sort('fall_id__id')
##             for z in zustaendigkeiten:
##                 if z['fall_id__akte_id__stzbg'] == stelle['id']:
##                     res.append(abfr1_t % z)
                    
##         elif mitarbeiter['benr__code'] == 'admin':
##             zustaendigkeiten = ZustaendigkeitList(where = 'ed %s %s and fall_id >= %s'
##                                                  % (op, ed, fall['id']), order = 'id')
##             zustaendigkeiten.sort('fall_id__id')
##             for z in zustaendigkeiten:
##                 if z['fall_id__akte_id__stzbg'] == stelle['id']:
##                     res.append(abfr1_t % z)
                    
##         res.append(abfr1b_t)
##         return ''.join(res)
        
        
## class formabfr3(Request.Request):
##     """Suchformular Gruppenkarte(Tabellen: Fall, Akte, Gruppe, Zuständigkeit)."""
    
##     permissions = Request.ABFR_PERM
    
##     def processForm(self, REQUEST, RESPONSE):
##         mitarbeiterliste = self.getMitarbeiterliste()
##         user = self.user
##         stellen = get_all_codes('stzei')
##         stelle = self.stelle
        
##         res = []
##         res.append(head_normal_t %("Suche in der Kartei nach Vorname oder Nachname oder Fallnummer oder Gruppe"))
##         res.append(suchwort_t)
##         res.append(menuefs_t)
##         res.append(suchwort2a_t)
##         # nicht mehr nach der Stelle fragen
##         #mksel(res, codeliste_t, stellen, 'id', stelle['id'])
##         res.append(suchwort2b_t)
##         return ''.join(res)
        
        
## class abfr3(Request.Request):
##     """Ergebnis der Suche in der Klienten- oder Gruppenkartei."""
    
##     permissions = Request.ABFR_PERM
    
##     def processForm(self, REQUEST, RESPONSE):
##         mitarbeiterliste = self.getMitarbeiterliste()
##         user = self.user
##         mitarbeiter = self.mitarbeiter
##         stelle = self.stelle
        
##         try:
##             expr = check_str_not_empty(self.form, 'expr', "Kein Suchausdruck")
##             table = check_str_not_empty(self.form, 'table', "Keine Suchklasse")
##         except EBUpdateDataError, e:
##             meldung = {'titel':'Fehler',
##                        'legende':'Fehlerbeschreibung',
##                        'zeile1': str(e),
##                        'zeile2':'Versuchen Sie es bitte erneut.'}
##             return (meldung_t %meldung)
##         stzid = stelle['id']
        
##         expr1 = "%" + expr + "%"
##         if table == "akte":
##             akten = AkteList(where = "stzbg = %s and (vn %s '%s' or na %s '%s')"
##                              % (stzid, CLIKE, expr1, CLIKE, expr1),
##                              order = 'na,vn')
            
##         elif table == "fall":
##             faelle = FallList(where = "fn %s '%s'" % (CLIKE, expr1),
##                               order = 'fn' )
            
##         elif table == "bezugsperson":
##             bezugspersonen = BezugspersonList(where = "vn %s '%s' or na %s '%s'"
##                                               % (CLIKE, expr1, CLIKE,
##                                                  expr1),
##                                               order = 'na,vn')
            
##         elif table == 'gruppe':
##             gruppen = GruppeList(where = "stz = '%s' and name %s '%s' or thema %s '%s'"
##                               % (stzid, CLIKE, expr1, CLIKE, expr1))
            
##         res = []
##         res.append(head_normal_t %("Resultat der Karteiabfrage nach %s" % expr))
##         res.append(thabfr3_start_t)
##         if table == "akte" and mitarbeiter['benr__code'] == 'bearb':
##             res.append(thabfr3_header_t)
##             for a in akten:
##                 letzter_fall = a['letzter_fall']
##                 zustaendigkeit = letzter_fall['zuletzt_zustaendig']
##                 if zustaendigkeit['mit_id'] == mitarbeiter['id']:
##                     res.append(abfr2_item_t % zustaendigkeit)
##             res.append(abfr_tab_ende_t)
            
##         elif table == "akte" and (mitarbeiter['benr__code'] == 'verw' or mitarbeiter['benr__code'] == 'admin'):
##             res.append(thabfr3_header_t)
##             for a in akten:
##                 letzter_fall = a['letzter_fall']
##                 zustaendigkeit = letzter_fall['zuletzt_zustaendig']
##                 if zustaendigkeit['fall_id__akte_id__stzbg'] == stzid:
##                     res.append(abfr2_item_t % zustaendigkeit)
##             res.append(abfr_tab_ende_t)
            
##         elif table == "bezugsperson" and mitarbeiter['benr__code'] == 'bearb':
##             res.append(thabfr3_header_t)
##             for b in bezugspersonen:
##                 if b['akte_id__stzbg'] == stzid:
##                     letzter_fall = b['akte_id__letzter_fall']
##                     zustaendigkeit = letzter_fall['zuletzt_zustaendig']
##                     if zustaendigkeit['mit_id'] == mitarbeiter['id']:
##                         res.append(abfr3a_t % zustaendigkeit)
##                         res.append(abfr3b_t % b)
##                         res.append(abfr3c_t % zustaendigkeit)
##             res.append(abfr_tab_ende_t)
            
##         elif table == "bezugsperson" and (mitarbeiter['benr__code'] == 'verw' or mitarbeiter['benr__code'] == 'admin'):
##             res.append(thabfr3_header_t)
##             for b in bezugspersonen:
##                 if b['akte_id__stzbg'] == stzid:
##                     letzter_fall = b['akte_id__letzter_fall']
##                     zustaendigkeit = letzter_fall['zuletzt_zustaendig']
##                     if zustaendigkeit['fall_id__akte_id__stzbg'] == stzid:
##                         res.append(abfr3a_t % zustaendigkeit)
##                         res.append(abfr3b_t % b)
##                         res.append(abfr3c_t % zustaendigkeit)
##             res.append(abfr_tab_ende_t)
            
##         elif table == "fall" and mitarbeiter['benr__code'] == 'bearb':
##             res.append(thabfr3_header_t)
##             for f in faelle:
##                 if f['akte_id__stzbg'] == stzid:
##                     zustaendigkeit = f['zuletzt_zustaendig']
##                     if zustaendigkeit['mit_id'] == mitarbeiter['id']:
##                         res.append(abfr2_item_t % zustaendigkeit)
##             res.append(abfr_tab_ende_t)
            
##         elif table == "fall" and (mitarbeiter['benr__code'] == 'verw' or mitarbeiter['benr__code'] == 'admin'):
##             res.append(thabfr3_header_t)
##             for f in faelle:
##                 if f['akte_id__stzbg'] == stzid:
##                     zustaendigkeit = f['zuletzt_zustaendig']
##                     if zustaendigkeit['fall_id__akte_id__stzbg'] == stzid:
##                         res.append(abfr2_item_t % zustaendigkeit)
##             res.append(abfr_tab_ende_t)
            
##         elif table == "gruppe" and mitarbeiter['benr__code'] == 'bearb':
##             res.append(thabfrgr_t)
##             for g in gruppen:
##                 mitgruppen = mitarbeiter['gruppen']
##                 for m in mitgruppen:
##                     if m['gruppe_id'] == g['id']:
##                         res.append(abfrgr_t % g)
##             res.append(abfr_tab_ende_t)
            
##         elif table == "gruppe" and (mitarbeiter['benr__code'] == 'verw' or mitarbeiter['benr__code'] == 'admin'):
##             res.append(thabfrgr_t)
##             for g in gruppen:
##                 if g['stz'] == stzid:
##                     res.append(abfrgr_t % g)
##             res.append(abfr_tab_ende_t)
            
##         res.append(abfr3_ende_t)
##         return ''.join(res)


class abfr3(Request.Request, akte_share):
    """Ergebnis der Suche in der Klienten- oder Gruppenkartei."""
    permissions = Request.ABFR_PERM

    def beratungen_fall(self, mitarbeiter=None, klname=None, fn=None):
        join=[('zustaendigkeit', 'zustaendigkeit.fall_id=fall.id'),
              ('akte', 'fall.akte_id=akte.id'),
              ('mitarbeiter', 'zustaendigkeit.mit_id=mitarbeiter.id')]
        # nur die eigene Stelle
        where = "akte.stzbg=%s" % self.stelle['id']
        # nur die letzte Zuständigkeit deren Endedatum gleich dem ZDA-Datum ist
        where += """ and fall.zday = zustaendigkeit.ey and 
        fall.zdam = zustaendigkeit.em and 
        fall.zdad = zustaendigkeit.ed"""
        if klname:
            where += " and (akte.vn like '%%%s%%' or akte.na like '%%%s%%')" % (klname, klname)
            sort = ('akte__na', 'akte__vn', 'bgy', 'bgm', 'bgd')
        if fn:
            where += " and fall.fn like '%%%s%%'" % fn
            sort = ('bgy', 'fn_count')
        if mitarbeiter:
            where += " and mitarbeiter.id = %s" % mitarbeiter['id']
        fall_list = FallList(
            where=where,
            join=join,
            )
        fall_list.sort(*sort)
        return fall_list
        
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
            where += " and (bezugsperson.vn like '%%%s%%' or bezugsperson.na like '%%%s%%')" % \
                     (bzpname, bzpname)
        if mitarbeiter:
            where += " and mitarbeiter.id = %s" % mitarbeiter['id']
        bezugsperson_list = BezugspersonList(
            where=where,
            join=join,
            )
        sort = ('na', 'vn',
        'bezugsperson__akte__letzter_fall__bgy',
        'bezugsperson__akte__letzter_fall__bgm',
        'bezugsperson__akte__letzter_fall__bgd',
        )
        bezugsperson_list.sort(*sort)
        return bezugsperson_list
        
    def beratungen_gruppe(self, mitarbeiter=None, grname=None):
        join=[('mitarbeitergruppe', 'gruppe.id=mitarbeitergruppe.gruppe_id'),
              ('mitarbeiter', 'mitarbeitergruppe.mit_id=mitarbeiter.id')]
        # nur die eigene Stelle
        where = "gruppe.stz=%s" % self.stelle['id']
        if mitarbeiter:
            where += " and mitarbeiter.id = %s" % mitarbeiter['id']
        if grname:
            where += " and (gruppe.name like '%%%s%%' or gruppe.thema like '%%%s%%')" % \
                     (grname, grname)
        gruppe_list = GruppeList(
            where=where,
            join=join,
            )
        sort = ('name', 'bgy', 'bgm', 'bgd')
        gruppe_list.sort(*sort)
        return gruppe_list
        


    def get_table_daten(self, elems, fields):
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
                    zeile.append(h.String(string=e[f]))
            daten.append(zeile)
        return daten
                    
                
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
            headers=('Gruppennr.', 'Name', 'Thema', 'Art', 'Beginn', 'Ende', 'Mitarbeiter')
            gruppen = self.beratungen_gruppe(mitarbeiter, grname=expr)
            daten = self.get_table_daten(gruppen,
                                         (('gn', 'grkarte?gruppeid=%(id)s'),
                                          'name', 'thema', 'grtyp__name',
                                          'bg', 'e', 'mitarbeiternamen'
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
                                         
##             akten = AkteList(where = "stzbg = %s and (vn %s '%s' or na %s '%s')"
##                              % (stzid, CLIKE, expr1, CLIKE, expr1),
##                              order = 'na,vn')
            
##         elif table == "fall":
##             faelle = FallList(where = "fn %s '%s'" % (CLIKE, expr1),
##                               order = 'fn' )
            
##         elif table == "bezugsperson":
##             bezugspersonen = BezugspersonList(where = "vn %s '%s' or na %s '%s'"
##                                               % (CLIKE, expr1, CLIKE,
##                                                  expr1),
##                                               order = 'na,vn')
            
##         elif table == 'gruppe':
##             gruppen = GruppeList(where = "stz = '%s' and name %s '%s' or thema %s '%s'"
##                               % (stzid, CLIKE, expr1, CLIKE, expr1))
            
##         res = []
##         res.append(head_normal_t %("Resultat der Karteiabfrage nach %s" % expr))
##         res.append(thabfr3_start_t)
##         if table == "akte" and mitarbeiter['benr__code'] == 'bearb':
##             res.append(thabfr3_header_t)
##             for a in akten:
##                 letzter_fall = a['letzter_fall']
##                 zustaendigkeit = letzter_fall['zuletzt_zustaendig']
##                 if zustaendigkeit['mit_id'] == mitarbeiter['id']:
##                     res.append(abfr2_item_t % zustaendigkeit)
##             res.append(abfr_tab_ende_t)
            
##         elif table == "akte" and (mitarbeiter['benr__code'] == 'verw' or mitarbeiter['benr__code'] == 'admin'):
##             res.append(thabfr3_header_t)
##             for a in akten:
##                 letzter_fall = a['letzter_fall']
##                 zustaendigkeit = letzter_fall['zuletzt_zustaendig']
##                 if zustaendigkeit['fall_id__akte_id__stzbg'] == stzid:
##                     res.append(abfr2_item_t % zustaendigkeit)
##             res.append(abfr_tab_ende_t)
            
##         elif table == "bezugsperson" and mitarbeiter['benr__code'] == 'bearb':
##             res.append(thabfr3_header_t)
##             for b in bezugspersonen:
##                 if b['akte_id__stzbg'] == stzid:
##                     letzter_fall = b['akte_id__letzter_fall']
##                     zustaendigkeit = letzter_fall['zuletzt_zustaendig']
##                     if zustaendigkeit['mit_id'] == mitarbeiter['id']:
##                         res.append(abfr3a_t % zustaendigkeit)
##                         res.append(abfr3b_t % b)
##                         res.append(abfr3c_t % zustaendigkeit)
##             res.append(abfr_tab_ende_t)
            
##         elif table == "bezugsperson" and (mitarbeiter['benr__code'] == 'verw' or mitarbeiter['benr__code'] == 'admin'):
##             res.append(thabfr3_header_t)
##             for b in bezugspersonen:
##                 if b['akte_id__stzbg'] == stzid:
##                     letzter_fall = b['akte_id__letzter_fall']
##                     zustaendigkeit = letzter_fall['zuletzt_zustaendig']
##                     if zustaendigkeit['fall_id__akte_id__stzbg'] == stzid:
##                         res.append(abfr3a_t % zustaendigkeit)
##                         res.append(abfr3b_t % b)
##                         res.append(abfr3c_t % zustaendigkeit)
##             res.append(abfr_tab_ende_t)
            
##         elif table == "fall" and mitarbeiter['benr__code'] == 'bearb':
##             res.append(thabfr3_header_t)
##             for f in faelle:
##                 if f['akte_id__stzbg'] == stzid:
##                     zustaendigkeit = f['zuletzt_zustaendig']
##                     if zustaendigkeit['mit_id'] == mitarbeiter['id']:
##                         res.append(abfr2_item_t % zustaendigkeit)
##             res.append(abfr_tab_ende_t)
            
##         elif table == "fall" and (mitarbeiter['benr__code'] == 'verw' or mitarbeiter['benr__code'] == 'admin'):
##             res.append(thabfr3_header_t)
##             for f in faelle:
##                 if f['akte_id__stzbg'] == stzid:
##                     zustaendigkeit = f['zuletzt_zustaendig']
##                     if zustaendigkeit['fall_id__akte_id__stzbg'] == stzid:
##                         res.append(abfr2_item_t % zustaendigkeit)
##             res.append(abfr_tab_ende_t)
            
##         elif table == "gruppe" and mitarbeiter['benr__code'] == 'bearb':
##             res.append(thabfrgr_t)
##             for g in gruppen:
##                 mitgruppen = mitarbeiter['gruppen']
##                 for m in mitgruppen:
##                     if m['gruppe_id'] == g['id']:
##                         res.append(abfrgr_t % g)
##             res.append(abfr_tab_ende_t)
            
##         elif table == "gruppe" and (mitarbeiter['benr__code'] == 'verw' or mitarbeiter['benr__code'] == 'admin'):
##             res.append(thabfrgr_t)
##             for g in gruppen:
##                 if g['stz'] == stzid:
##                     res.append(abfrgr_t % g)
##             res.append(abfr_tab_ende_t)
            
##         res.append(abfr3_ende_t)
##         return ''.join(res)
        
        
## class formabfr4(Request.Request):
##     """Suchformular für die Anzahl der Neumeldungen und zdA's pro Jahr."""
    
##     permissions = Request.ABFR_PERM
    
##     def processForm(self, REQUEST, RESPONSE):
##         mitarbeiterliste = self.getMitarbeiterliste()
##         user = self.user
##         stelle = self.stelle
##         res = []
##         res.append(head_normal_t %("Neumelde- und Abschlusszahlen"))
##         res.append(thformabfr_kopf_t %("abfr4"))
##         res.append(formabfr_jahr_t % ('Neumelde- und Abschlusszahl',today().year) )
##         res.append(formabfr_ende_t)
##         return ''.join(res)
        
class abfr4(Request.Request, akte_share):
    """Anzahl der Neumeldungen u. Abschlüsse pro Jahr und Quartal."""
    permissions = Request.ABFR_PERM
    def get_neumelde_abschluss_daten(self, jahr):
        "fast unverändert übernommen, müsste gestrafft werden."
        stelle = self.stelle
        JGHList = (jahr >= 2007 and Jugendhilfestatistik2007List or JugendhilfestatistikList)
        neumeldungen = FallList(where = 'bgy = %s' % jahr
                                + ' and akte_id__stzbg = %d' % stelle['id'],
                                order = 'bgm' )
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
        zdal = [z['em'] for z in zdaliste]
        hauptf = [z['em'] for z in hauptfallliste]
        geschw = [z['em'] for z in geschwliste]
        quartal1_neu = quartal1_zda = quartal1_hauptf = quartal1_geschw = 0
        quartal2_neu = quartal2_zda = quartal2_hauptf = quartal2_geschw = 0
        quartal3_neu = quartal3_zda = quartal3_hauptf = quartal3_geschw = 0
        quartal4_neu = quartal4_zda = quartal4_hauptf = quartal4_geschw = 0
        i = 1
        monats_ergebnisse = []
        while i < 13:
            # i steht für den Monat in jahr
            neumeldezahl = neul.count(i)
            zdazahl = zdal.count(i)
            hauptfzahl = hauptf.count(i)
            geschwzahl = geschw.count(i)
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
                quartal1_zda += zdazahl
                quartal1_hauptf +=  hauptfzahl
                quartal1_geschw +=  geschwzahl
                # msg systems 02.07.2002 fehler der schon in ebkus 2.0 vorhanden war
                # zufaellig gefunden und korrigiert.
                # if i > 3 < 7:
            elif i <= 6:
                quartal2_neu += neumeldezahl
                quartal2_zda += zdazahl
                quartal2_hauptf += hauptfzahl
                quartal2_geschw += geschwzahl
            elif i <= 9:
                quartal3_neu += neumeldezahl
                quartal3_zda += zdazahl
                quartal3_hauptf += hauptfzahl
                quartal3_geschw += geschwzahl
            elif i <= 12:
                quartal4_neu += neumeldezahl
                quartal4_zda += zdazahl
                quartal4_hauptf += hauptfzahl
                quartal4_geschw += geschwzahl
            monats_ergebnisse.append((i, laufendzahl, neumeldezahl,
                                      hauptfzahl, geschwzahl, zdazahl)) 
            i = i + 1
        quartals_ergebnisse = []
        quartals_ergebnisse.append((1, quartal1_neu, quartal1_hauptf,
                                    quartal1_geschw, quartal1_zda,))
        
        quartals_ergebnisse.append((2, quartal2_neu, quartal2_hauptf,
                                    quartal2_geschw, quartal2_zda,))
        quartals_ergebnisse.append((3, quartal3_neu, quartal3_hauptf,
                                    quartal3_geschw, quartal3_zda,))
        quartals_ergebnisse.append((4, quartal4_neu, quartal4_hauptf,
                                    quartal4_geschw, quartal4_zda,))
        gesamt_ergebnisse = (len(neul), len(hauptf), len(geschw), len(zdal))
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

        #faelle = ('fn', 'vn', 'na', 'gb', 'fallbeginn', 'fallende', 'mitarbeiter', 'fs', 'jgh')
        monats_ergebnisse, quartals_ergebnisse, gesamt_ergebnisse = \
                           self.get_neumelde_abschluss_daten(jahr)
        report = h.FieldsetDataTable(
            legend='Neumeldungen und Abschlüsse %s' % jahr,
            headers=('Monat', 'Laufende am Monatsende', 'Neu', 'Hauptfall',
                     'Geschwisterfall', 'z.d.A'),
            daten=[[h.String(string=m[0]),
                    h.String(string=m[1]),
                    h.String(string=m[2]),
                    h.String(string=m[3]),
                    h.String(string=m[4]),
                    h.String(string=m[5]),
            ] for m in monats_ergebnisse] +
            [[h.String(string='Quartal %s' % m[0],
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
             ]],
            )
        res = h.FormPage(
            title='Neumelde- und Abschlusszahlen',
            name='neumelde',action="abfr4",method="post",
            breadcrumbs = (('Hauptmenü', 'menu'),
                           ),
            hidden=(),
            rows=(self.get_auswertungs_menu(),
                  anzeige,
                  report,
                  ),
            )
        return res.display()

        
        
        

class abfr5(Request.Request, akte_share):
    """Klientenzahl pro Mitarbeiter u. Jahr."""
    permissions = Request.ABFR_PERM
    def get_mitarbeiter_ergebnisse(self, jahr):
        a = b = c = 0
        mitarbeiter_ergebnisse = []
        for m in self.getMitarbeiterliste():
            neuel = ZustaendigkeitList(where = 'bgy = %s' % jahr
                                       + ' and mit_id = %d ' %m['id'])
            laufendl = ZustaendigkeitList(where = 'ey = 0 and bgy <= %s' % jahr
                                         + ' and bgy > 1980 and mit_id = %d ' %m['id'])
            abgeschl = ZustaendigkeitList(where = 'ey = %s' % jahr
                                           + ' and mit_id = %d ' %m['id'])
            mitarbeiter_ergebnisse.append((m['na'], len(neuel),
                                           len(laufendl), len(abgeschl)))
            a = a + len(neuel)
            b = b + len(laufendl)
            c = c + len(abgeschl)
        gesamt = a,b,c
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
            headers=('Mitarbeiter', 'Neu %s' % jahr, 'Laufend', 'Beendet',),
            daten=[[h.String(string=m[0]),
                    h.String(string=m[1]),
                    h.String(string=m[2]),
                    h.String(string=m[3]),
            ] for m in mitarbeiter_ergebnisse] +
            [[h.String(string='Gesamt',
                      class_='tabledatabold'),
             h.String(string=gesamt[0],
                      class_='tabledatabold'),
             h.String(string=gesamt[1],
                      class_='tabledatabold'),
             h.String(string=gesamt[2],
                      class_='tabledatabold'),
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

        
    def xprocessForm(self, REQUEST, RESPONSE):
        mitarbeiterliste = self.getMitarbeiterliste()
        user = self.user
        stelle = self.stelle
        try:
            jahr = check_int_not_empty(self.form, "jahr", "Keine Jahreszahl eingeben")
        except EBUpdateDataError, e:
            meldung = {'titel':'Fehler',
                       'legende':'Fehlerbeschreibung',
                       'zeile1': str(e),
                       'zeile2':'Versuchen Sie es bitte erneut.'}
            return (meldung_t %meldung)
        loeschfrist = get_rm_datum()
        lauf_jahr = '%(year)d' % today()
        if jahr > loeschfrist['loeschjahr'] or jahr <= int(lauf_jahr):
            pass
        else:
            self.last_error_message = "Die Jahreszahl ist kleiner als das eingestellte Löschdatum (Jahr) oder grösser als das laufende Jahr"
            return self.EBKuSError(REQUEST, RESPONSE)
            
        res = []
        res.append(head_normal_t %("Klientenzahl pro Mitarbeiter"))
        res.append(thabfr5_t % jahr)
        
        

##*************************************************************************
## Ueberblicksliste zu den Gruppen, fuer einen bestimmten Zeitraum
##
##
## Heller 02.10.2001
##*************************************************************************
        
class formabfr8(Request.Request):

    permissions = Request.ABFR_PERM
    def processForm(self, REQUEST, RESPONSE):
        stelle = self.stelle
        lauf_jahr = '%(year)d' % today()
        monat_von = self.form.get('monatvon')
        jahr_von = self.form.get('jahrvon')
        monat_bis = self.form.get('monatbis')
        jahr_bis = self.form.get('jahrbis')
        seite = { 'seite':'./formabfr8a'}
        
        ##***************************************************************
        ## Fehlerausgabe bei falschem Datum oder unvollstaendigen Daten
        ## Heller 02.10.2001
        ##***************************************************************
        res = []
        if jahr_von == '' or jahr_bis =='':
            meldung = {'titel':'Daten unvollst&auml;ndig!',
                       'legende':'Hinweis!',
                       'zeile1':'Die angegebenen Daten waren unvollst&auml;ndig!',
                       'zeile2':'Versuchen Sie es bitte erneut.'}
            res.append(meldung_t % meldung)
            return ''.join(res)
            
        if jahr_von > jahr_bis :
            meldung = {'titel':'Jahreszahl ist nicht korrekt!',
                       'legende':'Hinweis!',
                       'zeile1':'Das Von-Datum liegt nach Bis-Datum!',
                       'zeile2':'Versuchen Sie es bitte erneut.'}
            res.append(meldung_t % meldung)
            return ''.join(res)
            
        if jahr_von < '1970' or jahr_von >'2030':
            meldung = {'titel':'Jahreszahl ist nicht korrekt!',
                       'legende':'Hinweis!',
                       'zeile1':'Das Von-Datum liegt vor 1970 oder nach 2030!',
                       'zeile2':'Versuchen Sie es bitte erneut.'}
            res.append(meldung_t % meldung)
            return ''.join(res)
            
        if jahr_bis > lauf_jahr:
            meldung = {'titel':'Jahreszahl ist nicht korrekt!',
                       'legende':'Hinweis!',
                       'zeile1':'Das Bis-Datum liegt hinter dem heutigem!',
                       'zeile2':'Versuchen Sie es bitte erneut.'}
            res.append(meldung_t % meldung)
            return ''.join(res)
            
        if monat_von > monat_bis and jahr_von == jahr_bis:
            meldung = {'titel':'Monatsangabe ist nicht korrekt!',
                     'legende':'Hinweis!',
                     'zeile1':'Von-Monat ist gr&ouml;sser als Bis-Monat!',
                     'zeile2':'Versuchen Sie es bitte erneut.'}
            res.append(meldung_t % meldung)
            return ''.join(res)
            
        alle = GruppeList( where = ' ((bgy = %s' % jahr_von + ' and bgm >= %s' % monat_von
                                    + ') or ( bgy > %s))' % jahr_von
                                    + ' and ((bgy = %s' % jahr_bis
                                    + ' and bgm <= %s)' % monat_bis
                                    + ' or ( bgy < %s)) ' % jahr_bis
                                      , order = 'bgy,bgm,bgd desc' )
        
        if len(alle):
            pass
        else:
            meldung = {'titel':'Fehler',
                       'legende':'Fehlerbeschreibung',
                       'zeile1': 'Keine Datens&auml;tze gefunden',
                       'zeile2':'Versuchen Sie es bitte erneut.'}
            res.append(meldung_t %meldung)
            return ''.join(res)
            
        res.append(head_normal_t %("Gruppen&uuml;berblick"))
        res.append(thabfr8_t)
        
        for i in alle:
            mitarbeiterl = MitarbeiterGruppeList(where = 'gruppe_id = %d' % i['id'])
            mitarbeiter = ' '
            for m in mitarbeiterl:
                mitarbeiter = mitarbeiter + '%s ' % m['mit_id__na']
            res.append(abfr8ges_t % (i['gn'],i['name'],nfc(i['grtyp']),nfc(i['teiln']),
                                     i['tzahl'],i['bgd'],i['bgm'],i['bgy'],i['ed'],i['em'],
                                     i['ey'], mitarbeiter))
        res.append(abfr8ges_ende_t)
        return ''.join(res)
        
        
        ##*************************************************************************
        ## Zeitraumauswahl fuer eine Gruppenuebersicht
        ##
        ##
        ## Heller 26.09.2001
        ##*************************************************************************
        
class formabfr8a(Request.Request):


    permissions = Request.ABFR_PERM
    
    def processForm(self, REQUEST, RESPONSE):
    
    
        stelle = self.stelle
        res = []
        res.append(head_normal_t %("Auswahl des Zeitraumes für die Gruppenuebersicht"))
        res.append(abfr8ages_t)
        return ''.join(res)
        

        
        
