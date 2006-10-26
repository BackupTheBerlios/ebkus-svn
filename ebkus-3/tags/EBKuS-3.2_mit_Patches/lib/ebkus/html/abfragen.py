# coding: latin-1
"""Module für die Abfragen."""

# TODO: nicht gebrauchte Abfragen entfernen: formabfr3, abfr3, formabfr8 - 14 (ohne 'a')

from ebkus.config import config
from ebkus.db.sql import SQL
CLIKE = 'like' # gibts andere DBs wo das nicht geht?
from ebkus.app import Request
from ebkus.app.ebapi import nfc, Fachstatistik, FachstatistikList, JugendhilfestatistikList, \
     ZustaendigkeitList, AkteList, BezugspersonList, FallList, GruppeList, \
     Tabelle, Code, Feld, Mitarbeiter, MitarbeiterGruppeList, \
     today, cc, check_int_not_empty, \
     check_str_not_empty, EBUpdateDataError, getQuartal, get_rm_datum, Date
from ebkus.app.ebapih import get_codes, mksel, get_all_codes
from ebkus.html.statistik_ergebnis import auszergebnis
from ebkus.app.statistik import CodeAuszaehlung, WertAuszaehlung
from ebkus.app_surface.standard_templates import *
from ebkus.app_surface.abfragen_templates import *
        

class fachstatistik_ergebnis(Request.Request):
    """Oberklasse für alle Fachstatistikabfragen, die bisher
    fstat_ausgabe benutzt haben.
    """
    permissions = Request.ABFR_PERM
    
    def _expand(self, liste, pfad):
        """Wird z.B. benutzt um die Menge aller Leistungen über
        alle Fachstatistiken hinweg zu berechnen."""
        alle = []
        for f in liste:
            for l in f[pfad]:
                alle.append(l)
        return alle

    def get_auszaehlungen(self, liste, file):
        """Liefert eine Liste von Auszählungsobjekten für fstat_ausgabe"""
        from ebkus.app.statistik import \
             CodeAuszaehlung as CA, \
             WertAuszaehlung as WA, \
             ObjektAuszaehlung as OA, \
             MehrfachCodeAuszaehlung as MA
        felder = Tabelle(klasse='Fachstatistik')['felder']
        auszaehlungen = [CA(liste, f, file=file)
                         for f in felder if f.get('kat_code')]
        app = auszaehlungen.append # Abkürzung
        app(CA(self._expand(liste, 'leistungen'), 'le',
               title="Erbrachte Leistungen", file=file))
        app(CA(self._expand(liste, 'fachstatelternprobleme'), 'pbe',
               title="Problemspektrum der Eltern", file=file))
        app(CA(self._expand(liste, 'fachstatkindprobleme'), 'pbk',
               title="Problemspektrum Kind/Jugendliche", file=file))
        app(OA(liste, 'mit_id', self.getMitarbeiterliste(), 'na',
               title="Mitarbeiter", file=file))
        app(WA(liste, 'bz', title="Planungsraum", file=file))
        return auszaehlungen
                             
    def fstat_ausgabe(self, res, liste, plraum_tabelle=None):
        """Ausgabe der Fachstatistik für die verschiedenen Abfragen
        """
        file = self.__class__.__name__
        auszaehlungen = self.get_auszaehlungen(liste, file)
        if not plraum_tabelle:
            # In der Regel das letzte Element löschen
            del auszaehlungen[-1]
        self.session.data[file] = {} # alle früheren in der Session löschen
        # im session-Objekt ablegen
        for a in auszaehlungen:
            self.session.data[file][a.id] = a
        # Menu
        res.append(jghstat_menue_head_t)
        res.append(jghstat_menue_t % ("top","- Gehe zu ..."))
        for a in auszaehlungen:
            res.append(jghstat_menue_t % (a.identname, a.title))
        res.append(jghstat_menue_end_t)
        # Ergebnistabellen mit links auf Einzeltabelle und Chart hinzufügen
        for a in auszaehlungen:
            erg = auszergebnis()
            erg.auszaehlung = a
            erg.add_tabelle(res)
        

    def get_sql_feld(self, feld_id, value_ids, konj):
        feld_obj = Feld(feld_id) # Feldobjekt
        feld_name = feld_obj['name']
        feld = feld_obj['feld']
        feld_verwtyp = feld_obj['verwtyp__code']
        if feld_verwtyp in ('b', 'k'):
            values = [Code(i) for i in value_ids]
            name = 'name'
        elif feld_obj['feld'] == 'mit_id':
            values = [Mitarbeiter(i) for i in value_ids]
            name = 'na'
            feld_name = 'Mitarbeiter'
        konj_name = (konj == 'and' and 'und' or 'oder')
        mehrfach_items = {
            'le': 'fachstatlei',
            'pbe': 'fachstatelternproblem',
            'pbk': 'fachstatkindproblem'
            }
        join = []
        # Dieser Fall muss getrennt behandelt werden, da
        # es soviele joins geben muss wie mit 'and' zu kombinierende Feldwerte
        special = (feld in mehrfach_items and konj == 'and' and
                   len(value_ids) > 1 and not feld_verwtyp == 'b')
        if special:
            tab_aliases = [('%s_%s' % (feld, i)) for i in range(len(value_ids))]
            tab = mehrfach_items[feld]
            join = [("%s as %s" % (tab, alias), "fachstat.id = %s.fstat_id" % alias)
                    for alias in tab_aliases]
        elif feld in mehrfach_items:
            tab = mehrfach_items[feld]
            join = [(tab, "fachstat.id = %s.fstat_id" % tab)]
        else:
            tab = 'fachstat'
        if feld_verwtyp == 'b':
            item_query = (" %s " % konj).join(["(%s.%s >= %s and %s.%s <= %s)" %
                                               (tab, feld, v['mini'], tab, feld, v['maxi'])
                                               for v in values])
        elif special:
            item_query = (" %s " % konj).join(["%s.%s = %s" % (alias, feld, i)
                                               for alias, i in zip(tab_aliases, value_ids)])
        else:
            item_query = (" %s " % konj).join(["%s.%s = %s" % (tab, feld, i) for i in value_ids])
        # Kontaktzahl Sonstige = '5-10'    lesbarer als
        # Kontaktzahl Sonstige >= 5 and Kontaktzahl Sonstige <= 10
        item_query_anzeige = (" %s " % konj_name).join(["%s = '%s'" % (feld_name, v[name])
                                                        for v in values])
        return item_query, item_query_anzeige, join


    def get_sql_all(self, feld_dict, feld_konj, year, year_op, stz_id):
        if stz_id == -1:
            stelle = {'name': 'Alle Beratungsstellen'}
        else:
            stelle = Code(id=stz_id)
        item_queries = []
        item_queries_anzeigen = []
        joins = []
        for feld_id, (code_konj, value_ids) in feld_dict.items():
            iq, iqa, j = self.get_sql_feld(feld_id, value_ids, code_konj)
            item_queries.append(iq)
            item_queries_anzeigen.append(iqa)
            joins += j
        if len(item_queries) > 1:
            # extra Klammern
            item_queries = [("(%s)" % i) for i in item_queries]
            item_queries_anzeigen = [("(%s)" % i) for i in item_queries_anzeigen]
        item_query = (" %s " % feld_konj).join(item_queries)
        konj_name = (feld_konj == 'and' and 'und' or 'oder')
        item_query_anzeige = (" %s " % konj_name).join(item_queries_anzeigen)
        year_query = "fachstat.jahr %s %s" % (year_op, year)
        year_query_anzeige = "Jahr %s %s" % (year_op, year)
        where = "(%s) and (%s)" % (item_query, year_query)
        query_anzeige = "(%s) und (%s)" % (item_query_anzeige, year_query_anzeige)
        if stz_id != -1:
            where += " and fachstat.stz = %s" % stz_id
            query_anzeige += " und Stelle = '%(name)s' " % stelle

        sql_string = Fachstatistik.querySQL.getQuerySQL(where=where, order='', join=joins)
        return where, '', joins, query_anzeige

        
class formabfr2(Request.Request):
    """Suchformular (Tabellen: Fall, Akte, Zuständigkeit)."""
    
    permissions = Request.ABFR_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        mitarbeiterliste = self.getMitarbeiterliste()
        user = self.user
        stellen = get_all_codes('stzei')
        
        res = []
        res.append(head_normal_t %("Suche alle Beratungen ab Fallnummer"))
        res.append(suchefallnummer_t)
        mksel(res, codeliste_t, stellen, 'id', self.stelle['id'])
        res.append(suchefallnummer2_t)
        return ''.join(res)
        
        
class abfr1(Request.Request):
    """Ergebnis der Abfrage aller Klienten, Beratungen
    (Tabellen: Fall, Akte, Zuständigkeit)."""
    
    permissions = Request.ABFR_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        mitarbeiterliste = self.getMitarbeiterliste()
        user = self.user
        mitarbeiter = self.mitarbeiter
        stelle = self.stelle
        
        try:
            o = check_str_not_empty(self.form, 'o', "Kein Operator")
            ed = check_int_not_empty(self.form, 'ed', "Kein Datum", 0)
        except EBUpdateDataError, e:
            meldung = {'titel':'Fehler',
                       'legende':'Fehlerbeschreibung',
                       'zeile1': str(e),
                       'zeile2':'Versuchen Sie es bitte erneut.'}
            return (meldung_t %meldung)
            
        if o == 'laufend':
            ber = 'Laufende'
            op = '='
        elif o == 'alle':
            ber = 'Alle'
            op = '>='
        elif o == 'zda':
            ber = 'Abgeschlossene'
            op = '>'
            
            
        res = []
        res.append(head_normal_t %("%s Beratungen" %ber))
        res.append(thabfr1_t)
        if mitarbeiter['benr__code'] == 'bearb':
            zustaendigkeiten = ZustaendigkeitList(where = 'ed %s %s and mit_id = %s'
                                                  % (op, ed, mitarbeiter['id'] ))
            zustaendigkeiten.sort('mit_id__na', 'fall_id__akte_id__na',
                                  'fall_id__akte_id__vn')
            for z in zustaendigkeiten:
                if z['fall_id__akte_id__stzak'] == stelle['id']:
                    res.append(abfr1_t % z)
                    
        elif mitarbeiter['benr__code'] == 'verw':
            zustaendigkeiten = ZustaendigkeitList(where = 'ed %s %s' %(op, ed)
                                                  , order = 'id')
            zustaendigkeiten.sort('fall_id__id')
            # nur Fälle der Stelle des Mitarbeiters
            # Reihenfolge: Jahr, Fallnummer
            for z in zustaendigkeiten:
                if z['fall_id__akte_id__stzak'] == stelle['id']:
                    res.append(abfr1_t % z)
                    
        elif mitarbeiter['benr__code'] == 'admin':
            zustaendigkeiten = ZustaendigkeitList(where = 'ed %s %s' %(op, ed)
                                                  , order = 'id')
            zustaendigkeiten.sort('fall_id__id')
            for z in zustaendigkeiten:
                if z['fall_id__akte_id__stzak'] == stelle['id']:
                    res.append(abfr1_t % z)
        res.append(abfr1b_t)
        return ''.join(res)
        
        
        
class abfr2(Request.Request):
    """Ergebnis der Suche in der Klienten- oder Gruppenkartei."""
    
    permissions = Request.ABFR_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        mitarbeiterliste = self.getMitarbeiterliste()
        user = self.user
        mitarbeiter = self.mitarbeiter
        stelle = self.stelle
        
        try:
            fn = check_str_not_empty(self.form, 'expr', "Keine Fallnummer")
            stzid = check_int_not_empty(self.form, 'stz', "Kein Stellenzeichen")
        except EBUpdateDataError, e:
            meldung = {'titel':'Fehler',
                       'legende':'Fehlerbeschreibung',
                       'zeile1': str(e),
                       'zeile2':'Versuchen Sie es bitte erneut.'}
            return (meldung_t %meldung)
            
        op = '>='
        ed = 0
        if op == '=':
            ber = 'Laufende'
        elif op == '>=':
            ber = 'Alle'
        elif op == '>':
            ber = 'Abgeschlossene'
            
        stelle = Code(id=stzid)
        faelle = FallList(where = "fn = '%s' " % fn )
        if len(faelle) == 1:
            fall = faelle[0]
        else:
            res = []
            meldung = {'titel':'Suche nicht erfolgreich.',
                     'legende':'Suche nicht erfolgreich',
                     'zeile1':'Es konnte kein Fall eindeutig identifiziert werden!',
                     'zeile2':'Versuchen Sie es bitte erneut.'}
            res.append(meldung_t % meldung)
            return ''.join(res)
            
            # Headerblock, Menue u. Überschrift fuer das HTML-Template
            
        res = []
        res.append(head_normal_t %("Alle Beratungen ab Fallnummer"))
        res.append(thabfr1_t)
        
        if mitarbeiter['benr__code'] == 'bearb':
            zustaendigkeiten = ZustaendigkeitList(where = 'ed %s %s and mit_id = %s and fall_id >= %s'
                       % (op, ed, mitarbeiter['id'], fall['id'] ))
            zustaendigkeiten.sort('mit_id__na', 'fall_id__akte_id__na',
                                  'fall_id__akte_id__vn')
            for z in zustaendigkeiten:
                if z['fall_id__akte_id__stzak'] == stelle['id']:
                    res.append(abfr1_t % z)
                    
        elif mitarbeiter['benr__code'] == 'verw':
            zustaendigkeiten = ZustaendigkeitList(where = 'ed %s %s and fall_id >= %s'
                                              % (op, ed, fall['id']) , order = 'id')
            zustaendigkeiten.sort('fall_id__id')
            for z in zustaendigkeiten:
                if z['fall_id__akte_id__stzak'] == stelle['id']:
                    res.append(abfr1_t % z)
                    
        elif mitarbeiter['benr__code'] == 'admin':
            zustaendigkeiten = ZustaendigkeitList(where = 'ed %s %s and fall_id >= %s'
                                                 % (op, ed, fall['id']), order = 'id')
            zustaendigkeiten.sort('fall_id__id')
            for z in zustaendigkeiten:
                if z['fall_id__akte_id__stzak'] == stelle['id']:
                    res.append(abfr1_t % z)
                    
        res.append(abfr1b_t)
        return ''.join(res)
        
        
class formabfr3(Request.Request):
    """Suchformular Gruppenkarte(Tabellen: Fall, Akte, Gruppe, Zuständigkeit)."""
    
    permissions = Request.ABFR_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        mitarbeiterliste = self.getMitarbeiterliste()
        user = self.user
        stellen = get_all_codes('stzei')
        stelle = self.stelle
        
        res = []
        res.append(head_normal_t %("Suche in der Kartei nach Vorname oder Nachname oder Fallnummer oder Gruppe"))
        res.append(suchwort_t)
        res.append(menuefs_t)
        res.append(suchwort2a_t)
        mksel(res, codeliste_t, stellen, 'id', stelle['id'])
        res.append(suchwort2b_t)
        return ''.join(res)
        
        
class abfr3(Request.Request):
    """Ergebnis der Suche in der Klienten- oder Gruppenkartei."""
    
    permissions = Request.ABFR_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        mitarbeiterliste = self.getMitarbeiterliste()
        user = self.user
        mitarbeiter = self.mitarbeiter
        stelle = self.stelle
        
        try:
            expr = check_str_not_empty(self.form, 'expr', "Kein Suchausdruck")
            stzid = check_int_not_empty(self.form, 'stz', "Kein Stellenzeichen")
            table = check_str_not_empty(self.form, 'table', "Keine Suchklasse")
        except EBUpdateDataError, e:
            meldung = {'titel':'Fehler',
                       'legende':'Fehlerbeschreibung',
                       'zeile1': str(e),
                       'zeile2':'Versuchen Sie es bitte erneut.'}
            return (meldung_t %meldung)
        stzid = stelle['id']
        
        expr1 = "%" + expr + "%"
        if table == "akte":
            akten = AkteList(where = "stzak = %s and (vn %s '%s' or na %s '%s')"
                             % (stzid, CLIKE, expr1, CLIKE, expr1),
                             order = 'na,vn')
            
        elif table == "fall":
            faelle = FallList(where = "fn %s '%s'" % (CLIKE, expr1),
                              order = 'fn' )
            
        elif table == "bezugsperson":
            bezugspersonen = BezugspersonList(where = "vn %s '%s' or na %s '%s'"
                                              % (CLIKE, expr1, CLIKE,
                                                 expr1),
                                              order = 'na,vn')
            
        elif table == 'gruppe':
            gruppen = GruppeList(where = "stz = '%s' and name %s '%s' or thema %s '%s'"
                              % (stzid, CLIKE, expr1, CLIKE, expr1))
            
        res = []
        res.append(head_normal_t %("Resultat der Karteiabfrage nach %s" % expr))
        res.append(thabfr3_start_t)
        if table == "akte" and mitarbeiter['benr__code'] == 'bearb':
            res.append(thabfr3_header_t)
            for a in akten:
                letzter_fall = a['letzter_fall']
                zustaendigkeit = letzter_fall['zuletzt_zustaendig']
                if zustaendigkeit['mit_id'] == mitarbeiter['id']:
                    res.append(abfr2_item_t % zustaendigkeit)
            res.append(abfr_tab_ende_t)
            
        elif table == "akte" and (mitarbeiter['benr__code'] == 'verw' or mitarbeiter['benr__code'] == 'admin'):
            res.append(thabfr3_header_t)
            for a in akten:
                letzter_fall = a['letzter_fall']
                zustaendigkeit = letzter_fall['zuletzt_zustaendig']
                if zustaendigkeit['fall_id__akte_id__stzak'] == stzid:
                    res.append(abfr2_item_t % zustaendigkeit)
            res.append(abfr_tab_ende_t)
            
        elif table == "bezugsperson" and mitarbeiter['benr__code'] == 'bearb':
            res.append(thabfr3_header_t)
            for b in bezugspersonen:
                if b['akte_id__stzak'] == stzid:
                    letzter_fall = b['akte_id__letzter_fall']
                    zustaendigkeit = letzter_fall['zuletzt_zustaendig']
                    if zustaendigkeit['mit_id'] == mitarbeiter['id']:
                        res.append(abfr3a_t % zustaendigkeit)
                        res.append(abfr3b_t % b)
                        res.append(abfr3c_t % zustaendigkeit)
            res.append(abfr_tab_ende_t)
            
        elif table == "bezugsperson" and (mitarbeiter['benr__code'] == 'verw' or mitarbeiter['benr__code'] == 'admin'):
            res.append(thabfr3_header_t)
            for b in bezugspersonen:
                if b['akte_id__stzak'] == stzid:
                    letzter_fall = b['akte_id__letzter_fall']
                    zustaendigkeit = letzter_fall['zuletzt_zustaendig']
                    if zustaendigkeit['fall_id__akte_id__stzak'] == stzid:
                        res.append(abfr3a_t % zustaendigkeit)
                        res.append(abfr3b_t % b)
                        res.append(abfr3c_t % zustaendigkeit)
            res.append(abfr_tab_ende_t)
            
        elif table == "fall" and mitarbeiter['benr__code'] == 'bearb':
            res.append(thabfr3_header_t)
            for f in faelle:
                if f['akte_id__stzak'] == stzid:
                    zustaendigkeit = f['zuletzt_zustaendig']
                    if zustaendigkeit['mit_id'] == mitarbeiter['id']:
                        res.append(abfr2_item_t % zustaendigkeit)
            res.append(abfr_tab_ende_t)
            
        elif table == "fall" and (mitarbeiter['benr__code'] == 'verw' or mitarbeiter['benr__code'] == 'admin'):
            res.append(thabfr3_header_t)
            for f in faelle:
                if f['akte_id__stzak'] == stzid:
                    zustaendigkeit = f['zuletzt_zustaendig']
                    if zustaendigkeit['fall_id__akte_id__stzak'] == stzid:
                        res.append(abfr2_item_t % zustaendigkeit)
            res.append(abfr_tab_ende_t)
            
        elif table == "gruppe" and mitarbeiter['benr__code'] == 'bearb':
            res.append(thabfrgr_t)
            for g in gruppen:
                mitgruppen = mitarbeiter['gruppen']
                for m in mitgruppen:
                    if m['gruppe_id'] == g['id']:
                        res.append(abfrgr_t % g)
            res.append(abfr_tab_ende_t)
            
        elif table == "gruppe" and (mitarbeiter['benr__code'] == 'verw' or mitarbeiter['benr__code'] == 'admin'):
            res.append(thabfrgr_t)
            for g in gruppen:
                if g['stz'] == stzid:
                    res.append(abfrgr_t % g)
            res.append(abfr_tab_ende_t)
            
        res.append(abfr3_ende_t)
        return ''.join(res)
        
        
class formabfr4(Request.Request):
    """Suchformular für die Anzahl der Neumeldungen und zdA's pro Jahr."""
    
    permissions = Request.ABFR_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        mitarbeiterliste = self.getMitarbeiterliste()
        user = self.user
        stelle = self.stelle
        res = []
        res.append(head_normal_t %("Neumelde- und Abschlusszahlen"))
        res.append(thformabfr_kopf_t %("abfr4"))
        res.append(formabfr_jahr_t % ('Neumelde- und Abschlusszahl',today().year) )
        res.append(formabfr_ende_t)
        return ''.join(res)
        
        
class abfr4(Request.Request):
    """Anzahl der Neumeldungen u. Abschlüsse pro Jahr und Quartal."""
    
    permissions = Request.ABFR_PERM
    
    def processForm(self, REQUEST, RESPONSE):
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
        if jahr > loeschfrist['loeschjahr'] and jahr <= int(lauf_jahr) :
            pass
        else:
            self.last_error_message = "Die Jahreszahl ist kleiner als das eingestellte Löschdatum (Jahr) oder grösser als das laufende Jahr"
            return self.EBKuSError(REQUEST, RESPONSE)
            
        neumeldungen = FallList(where = 'bgy = %s' % jahr
                                + ' and akte_id__stzak = %d' % stelle['id'],
                                order = 'bgm' )
        zdaliste = JugendhilfestatistikList(where = 'ey = %s' % jahr
                                + ' and stz = %d' % stelle['id'],
                                order = 'em' )
        
        hauptfallliste = JugendhilfestatistikList(where = 'ey = %s' % jahr
                                + ' and gfall = %d'   % cc('gfall', '1')
                                + ' and stz = %d' % stelle['id'],
                                order = 'em' )
        
        geschwliste = JugendhilfestatistikList(where = 'ey = %s' % jahr
                                + ' and gfall = %d' %  cc('gfall', '2')
                                + ' and stz = %d' % stelle['id'],
                                order = 'em' )
        
        neul = map(lambda x, item = 'bgm': x[item], neumeldungen)
        zdal = map(lambda x, item = 'em': x[item], zdaliste)
        hauptf = map(lambda x, item = 'em': x[item], hauptfallliste)
        geschw = map(lambda x, item = 'em': x[item], geschwliste)
        
        res = []
        res.append(head_normal_t % ("Neumelde- und Abschlusszahlen"))
        res.append(thabfr4_t)
        
        quartal1_neu = quartal1_zda = quartal1_hauptf = quartal1_geschw = 0
        quartal2_neu = quartal2_zda = quartal2_hauptf = quartal2_geschw = 0
        quartal3_neu = quartal3_zda = quartal3_hauptf = quartal3_geschw = 0
        quartal4_neu = quartal4_zda = quartal4_hauptf = quartal4_geschw = 0
        i = 1
        while i < 13:
            neumeldezahl = neul.count(i)
            zdazahl = zdal.count(i)
            hauptfzahl = hauptf.count(i)
            geschwzahl = geschw.count(i)
            if i < 4:
                quartal1_neu = quartal1_neu + neumeldezahl
                quartal1_zda = quartal1_zda + zdazahl
                quartal1_hauptf = quartal1_hauptf + hauptfzahl
                quartal1_geschw = quartal1_geschw + geschwzahl
                # msg systems 02.07.2002 fehler der schon in ebkus 2.0 vorhanden war
                # zufaellig gefunden und korrigiert.
                # if i > 3 < 7:
            if i > 3 and i < 7:
                quartal2_neu = quartal2_neu + neumeldezahl
                quartal2_zda = quartal2_zda + zdazahl
                quartal2_hauptf = quartal2_hauptf + hauptfzahl
                quartal2_geschw = quartal2_geschw + geschwzahl
            if i > 6 and i < 10:
                quartal3_neu = quartal3_neu + neumeldezahl
                quartal3_zda = quartal3_zda + zdazahl
                quartal3_hauptf = quartal3_hauptf + hauptfzahl
                quartal3_geschw = quartal3_geschw + geschwzahl
            if i > 9 and i < 13:
                quartal4_neu = quartal4_neu + neumeldezahl
                quartal4_zda = quartal4_zda + zdazahl
                quartal4_hauptf = quartal4_hauptf + hauptfzahl
                quartal4_geschw = quartal4_geschw + geschwzahl
            res.append(abfr4_t % (i, neumeldezahl, hauptfzahl, geschwzahl, zdazahl) )
            i = i + 1
            
        res.append(abfr4ges_t % (quartal1_neu, quartal1_hauptf,
                                 quartal1_geschw, quartal1_zda,
                                 quartal2_neu, quartal2_hauptf,
                                 quartal2_geschw, quartal2_zda,
                                 quartal3_neu, quartal3_hauptf,
                                 quartal3_geschw, quartal3_zda,
                                 quartal4_neu, quartal4_hauptf,
                                 quartal4_geschw, quartal4_zda,
                                 len(neul), len(hauptf), len(geschw), len(zdal) ))
        return ''.join(res)
        
        
class formabfr5(Request.Request):
    """Suchformular: Klientenzahl pro Mitarbeiter u. Jahr."""
    
    permissions = Request.ABFR_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        mitarbeiterliste = self.getMitarbeiterliste()
        user = self.user
        
        res = []
        res.append(head_normal_t % ("Klientenzahl pro Mitarbeiter"))
        res.append(thformabfr_kopf_t %("abfr5"))
        res.append(formabfr_jahr_t % ('Klientenzahl pro Mitarbeiter', today().year) )
        res.append(formabfr_ende_t)
        return ''.join(res)
        
        

class abfr5(Request.Request):
    """Klientenzahl pro Mitarbeiter u. Jahr."""
    
    permissions = Request.ABFR_PERM
    
    def processForm(self, REQUEST, RESPONSE):
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
        
        a = b = c = 0
        for m in mitarbeiterliste:
            neuel = ZustaendigkeitList(where = 'bgy = %s' % jahr
                                       + ' and mit_id = %d ' %m['id'])
            laufendl = ZustaendigkeitList(where = 'ey = 0 and bgy <= %s' % jahr
                                         + ' and bgy > 1980 and mit_id = %d ' %m['id'])
            abgeschl = ZustaendigkeitList(where = 'ey = %s' % jahr
                                           + ' and mit_id = %d ' %m['id'])
            res.append(abfr5_t % (m['na'], len(neuel),
                                  len(laufendl), len(abgeschl)) )
            a = a + len(neuel)
            b = b + len(laufendl)
            c = c + len(abgeschl)
            
        res.append(abfr5ges_t % (a, b, c))
        return ''.join(res)
        
class jghabfr(Request.Request):
    """Formular für die Bundesjugendhilfestatistikabfrage."""
    
    permissions = Request.ABFR_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        stellen = get_all_codes('stzei')
        res = []
        res.append(head_normal_t % 'Bundesstatistikabfrage')
        res.append(fsabfrjahr_t)
        res.append(menuefs_t)
        res.append(fsabfrjahr2_t % ({'file' : 'jghergebnis',
                                     'year' : '%(year)s' % today()}))
        res.append(fsabfrstelle_t)
        mksel(res, codeliste_t, stellen, 'id', self.stelle['id'])
        res.append(fsabfrtabende_t)
        return ''.join(res)
        
        
class jghergebnis(Request.Request):
    """Ergebnis der Bundesjugendhilfestatistikabfrage.
    (Tabelle: Jugendhilfestatistik)."""
    
    permissions = Request.ABFR_PERM

    # Diese Liste steuert die Einträge in der Ergebnisseite
    def get_auszaehlungen(self, liste, file):
        """Liefert eine Liste von Auszählungsobjekten"""
        from ebkus.app.statistik import \
             CodeAuszaehlung as CA, \
             MehrfachCodeAuszaehlung as MA, \
             ObjektAuszaehlung as OA
        auszaehlungen = [
            CA(liste, 'stz', title='Dienststelle', file=file),  
            CA(liste, 'bgr', title="Beendigungsgrund", file=file),
            CA(liste, 'gs',  title="Geschlecht", file=file),
            CA(liste, 'ag',  title="Altersgruppe", file=file),
            CA(liste, 'fs',  title="Junger Mensch lebt", file=file),
            CA(liste, 'hke', title="Staatsangehörigkeit", file=file),
            CA(liste, 'gsa', title="Geschwisterzahl", file=file),
            CA(liste, 'gsu', title="Geschwisterzahl unbekannt", file=file),
            CA(liste, 'zm',  title="1. Kontaktaufnahme durch", file=file),
            MA(liste, ['ba0', 'ba1', 'ba2', 'ba3', 'ba4',
                       'ba5', 'ba6', 'ba7', 'ba8', 'ba9'],
               title='Beratungsanlass', file=file),
            CA(liste, 'schw', title="Beratungsschwerpunkt", file=file),
            CA(liste, 'fbe0', title="Beratung setzt ein bei dem jungen Menschen",
               file=file),
            CA(liste, 'fbe1', title="Beratung setzt ein bei den Eltern",
               file=file),
            CA(liste, 'fbe2', title="Beratung setzt ein in der Familie",
               file=file),
            CA(liste, 'fbe3', title="Beratung setzt ein im sozialen Umfeld",
                               file=file)
            ]
        if config.BERLINER_VERSION:
            auszaehlungen.append(
                CA(liste, 'bezirksnr', title="Wohnbezirk", file=file))
        auszaehlungen.append(OA(liste, 'mit_id', self.getMitarbeiterliste(),
                                'na', title="Mitarbeiter", file=file))
        return auszaehlungen


    def processForm(self, REQUEST, RESPONSE):
        self.year = check_int_not_empty(self.form, 'year', "Fehler beim Jahr",)
        self.op = check_str_not_empty(self.form, 'op', "Fehler beim Operator",)
        stz = self.form.get('stz')
        if type(stz) is type(''):
            stz = [stz]
        self.stz = stz
        self.stz_url_params = '&'.join(["stz=%s" % i for i in stz])

        query_stelle = ' or '.join(['stz = %s' % i for i in self.stz])
        self.jghl = JugendhilfestatistikList(where = 'ey  %s %s and ( %s )'
                                             % (self.op, self.year, query_stelle) )
        self.jghl_gesamt = JugendhilfestatistikList(where = 'ey  %s %s'
                                                    % (self.op, self.year))
        if not self.jghl:
            meldung = {'titel':'Fehler',
                       'legende':'Fehlerbeschreibung',
                       'zeile1': 'Keine Datens&auml;tze gefunden',
                       'zeile2':'Versuchen Sie es bitte erneut.'}
            return (meldung_t %meldung)

        stellen_str = ' '.join([ Code(i)['name']  for i in self.stz ])
        query_anzeige = 'Jahr %s %s und Stelle(n): %s' % (self.op, self.year,
                                                          stellen_str)
        self.res = res = []
        res.append(head_normal_t % ("Bundesstatistikauswertung"))
        res.append(fsergebnis1_t)
        res.append(menuefs_t)
        res.append(gesamtzahl_t % (len(self.jghl), len(self.jghl_gesamt), query_anzeige))
        res.append(sprungmarke_t % "top")
        res.append(jghstat_menue_head_t)

        # Auszaehlungsobjekte anlegen und in Session ablegen
        file = self.__class__.__name__
        auszaehlungen = self.get_auszaehlungen(self.jghl, file)
        self.session.data[file] = {} # alle früheren löschen
        for a in auszaehlungen:
            self.session.data[file][a.id] = a
        # Menu mit Sprungzielen zu jeder Einzeltabelle
        res.append(jghstat_menue_t % ("top","- Gehe zu ..."))
        for a in auszaehlungen:
            res.append(jghstat_menue_t % (a.identname, a.title))
        res.append(jghstat_menue_end_t)
        
        # Ergebnistabellen mit links auf Einzeltabelle und Chart hinzufügen
        for a in auszaehlungen:
            erg = auszergebnis()
            erg.auszaehlung = a
            erg.add_tabelle(res)
        res.append(fsergebnis_ende_t)
        
        return ''.join(res)

        
        
class fsabfr(Request.Request):
    """Formular für die Fachstatistikabfrage."""
    
    permissions = Request.ABFR_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        mitarbeiterliste = self.getMitarbeiterliste()
        user = self.user
        stellen = get_all_codes('stzei')
        
        # Headerblock, Menue u. Uberschrift fuer das HTML-Template
        
        res = []
        res.append(head_normal_t %('Fachstatistikabfrage'))
        res.append(fsabfrjahr_t)
        res.append(menuefs_t)
        res.append(fsabfrjahr2_t % ({'file' : 'fsergebnis','year': '%(year)s' % today()}))
        res.append(fsabfrstelle_t)
        mksel(res, codeliste_t, stellen, 'id', self.stelle['id'])
        res.append(fsabfrtabende_t)
        return ''.join(res)
        
class fsergebnis(fachstatistik_ergebnis):
    """Ergebnis der Fachstatistikabfrage (Tabellen: Fachstatistik,
    FachstatistikLeistung, FachstatistikElternproblem,
    FachstatistikKindproblem)."""
    
    def processForm(self, REQUEST, RESPONSE):
        year = check_int_not_empty(self.form, 'year', "Fehler beim Jahr",)
        op = check_str_not_empty(self.form, 'op', "Fehler beim Operator",)
        if self.form.has_key('stz'):
            stz = self.form.get('stz')
        else:
            raise EBUpdateDataError('Sie haben keine Stelle ausgew&auml;hlt')
        if type(stz) is type(''):
            stz = [stz]
        query_stelle = ''
        stellen_anzeige = ''
        for s in stz:
            stelle = Code(s)
            query_stelle = query_stelle + ' or stz =' + ' %s ' % s
            stellen_anzeige = stellen_anzeige + ' %(name)s. ' % stelle
            
        fsl = FachstatistikList (where =  "jahr %s %s and ( %s )"
                                 % (op, year, query_stelle[4:]) )
        query_anzeige = "Jahr %s %s und Stelle(n): %s" % (op, year, stellen_anzeige)
        if not fsl:
            meldung = {'titel':'Keine Datens&auml;tze gefunden',
                       'legende':'Hinweis!',
                       'zeile1':'Es wurden keine Datens&auml;tze gefunden!',
                       'zeile2':'Versuchen Sie es bitte erneut.'}
            return meldung_t % meldung
        gesamt = len(fsl)
        res = []
        res.append(head_normal_t % ("Fachstatistikergebnisse"))
        res.append(fsergebnis1_t)
        res.append(menuefs_t)
        res.append(gesamtzahl_t % (gesamt, gesamt, query_anzeige))
        ausgabe = self.fstat_ausgabe(res, fsl)
        res.append(fsergebnis_ende_t)
        return ''.join(res)
        

class formabfr6(Request.Request):
    """Auswahl von Kategorie(n) für die Fachstatistikabfrage."""
    
    permissions = Request.ABFR_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        mitarbeiterliste = self.getMitarbeiterliste()
        user = self.user
        
        if self.form.has_key('file'):
            file = self.form['file']
        else:
            self.last_error_message = "Keine Wahl für die Kategorie(n) erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
            
        fsfelder = Tabelle(klasse='Fachstatistik')['felder']
        fsfelder.sort('name')
        leifelder = Tabelle(klasse='Fachstatistikleistung')['felder']
        leifelder.sort('name')
        pbefelder = Tabelle(klasse='Fachstatistikelternproblem')['felder']
        pbefelder.sort('name')
        pbkfelder = Tabelle(klasse='Fachstatistikkindproblem')['felder']
        pbkfelder.sort('name')
            
            # Headerblock, Menue u. Uberschrift fuer das HTML-Template
            
        if file == 'abfrkat':
            header = 'Statistikabfrage: Kategorienwahl'
        else:
            header = 'Statistikabfrage: Kategoriewahl'
            
        res = []
        res.append(head_normal_t %(header))
        res.append(abfr6_kopf_t)
        res.append(menuefs_t)
        if file == 'abfrkat':
            res.append(abfr6_t % "formabfr6a")
            res.append(selectmbg_t % {'name' : 'feldid', 'size' : '12'})
        else:
            res.append(abfr6_t % "formabfr6b")
            res.append(selectbg_t % {'name' : 'feldid', 'size' : '12'})
            
        for f in fsfelder:
            if f.get('kat_code'):
                res.append(codelisteos_t % f)
            if f['feld'] == 'mit_id':
                res.append(codelisteos_t % {'id' : f['id'], 'name' : "Mitarbeiter" })
                
        if file == 'abfritem':
            for l in leifelder:
                if l.get('kat_code'):
                    res.append(codelisteos_t % l)
            for e in pbefelder:
                if e.get('kat_code'):
                    res.append(codelisteos_t % e)
            for k in pbkfelder:
                if k.get('kat_code'):
                    res.append(codelisteos_t % k)
        res.append(abfr6_ende_t)
        return ''.join(res)
        
        
class formabfr6a(Request.Request):
    """Auswahl von Items mehrerer Kategorien für die Fachstatistikabfrage."""
    
    permissions = Request.ABFR_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        mitarbeiterliste = self.getMitarbeiterliste()
        user = self.user
        stellen = get_all_codes('stzei')
        stelle = self.stelle
        
        if self.form.has_key('feldid'):
            feldid = self.form.get('feldid')
            if type(feldid) is type(''):
                feldid = [feldid]
                if len(feldid) == 0 :
                    meldung = {'titel':'Fehler',
                           'legende':'Fehlerbeschreibung',
                           'zeile1': 'Keine Kategorie gew&auml;hlt',
                           'zeile2':'Versuchen Sie es bitte erneut.'}
                    return (meldung_t %meldung)
        else:
            self.last_error_message = "Keine Kategorie erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
            
        res = []
        res.append(head_normal_t %("Statistikabfage: Itemwahl aus mehreren Kategorien"))
        res.append(formabfr6a1_t % today())
        mksel(res, codeliste_t, stellen, 'id', stelle['id'])
        res.append(formabfr6a2_t)
        for f in feldid:
            feld = Feld(int(f))
            res.append(formitemausw1_t % feld)
            if feld['feld'] == 'mit_id':
                mksel(res, mitarbeiterliste_t, mitarbeiterliste, 'ben', user)
                res.append(formitemausw2_t)
            else:
                codeliste = get_codes(feld['kat_code'])
                mksel(res, codeliste_t, codeliste)
                res.append(formitemausw2_t)
        res.append(formabfr6a_ende_t)
        return ''.join(res)
        
        
class formabfr6b(Request.Request):
    """Auswahl von Items einer Kategorie der Fachstatistik."""
    
    permissions = Request.ABFR_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        mitarbeiterliste = self.getMitarbeiterliste()
        user = self.user
        stelle = self.stelle
        stellen = get_all_codes('stzei')
        
        if self.form.has_key('feldid'):
            feldid = self.form.get('feldid')
            feld = Feld(int(feldid))
        else:
            self.last_error_message = "Keine Kategorie erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
            
        if feld.has_key('kat_code'):
            if feld['kat_code']:
                codeliste = get_all_codes(feld['kat_code'])
                
        res = []
        res.append(head_normal_t %("Statistikabfrage: Auswahl von Items aus 1 Kategorie"))
        res.append(formabfr6b1_t % today())
        mksel(res, codeliste_t, stellen, 'id', stelle['id'])
        res.append(formabfr6a2_t)
        if feld['feld'] == 'mit_id':
            for m in mitarbeiterliste:
                res.append(itemauswb_t % {'id' : m['id'], 'name' : feld['name']})
                res.append(itemauswb1_t % {'id' : m['id'], 'name' : m['na']})
        else:
            for c in codeliste:
                res.append(itemauswb_t % {'id' : c['id'], 'name' : feld['name']})
                res.append(itemauswb1_t % c)
        res.append(itemauswb2_t % feld)
        res.append(formabfr6b_ende_t)
        return ''.join(res)
        
class abfr6a(fachstatistik_ergebnis):
    """Ergebnis der Fachstatistikabfrage (formabfr6a)."""
    
    def processForm(self, REQUEST, RESPONSE):
        year = check_int_not_empty(self.form, 'year', "Fehler beim Jahr",)
        year_op = check_str_not_empty(self.form, 'year_op',
                                      "Fehler beim Vergleichsoperator",)
        stz = check_int_not_empty(self.form, 'stz',
                                  "Fehler beim Stellenzeichen", -1)
        if self.form.has_key('feldid'):
            feldid = self.form.get('feldid')
            if isinstance(feldid, str):
                feldid = [feldid]
        else:
            raise EBUpdateDataError("Keine Kategorie erhalten")
        konj = self.form.get('konj')
        feld_dict = {}
        for f in feldid:
            codeid = self.form.get('%s_codeid' % f)
            assert codeid
            if not isinstance(codeid, list):
                codeid = [codeid]
            feld_dict[f] = ('or', codeid)
        where, order, join, query_anzeige = self.get_sql_all(feld_dict, konj, year, year_op, stz)
        fsl = FachstatistikList(where=where, order=order, join=join)
        fsl_alle = FachstatistikList(where = "jahr %s %s " % (year_op, year))
        if not fsl:
            self.last_error_message = "Keine Datensätze gefunden."
            return self.EBKuSError(REQUEST, RESPONSE)
        res = []
        res.append(head_normal_t %("Fachstatistikabfrageergebnis "
                  + "vom %(day)d.%(month)d.%(year)d" % today()))
        res.append(fsabfrjahr_t)
        res.append(menuefs_t)
        res.append(gesamtzahl_t % (len(fsl), len(fsl_alle), query_anzeige))
        ausgabe = self.fstat_ausgabe(res, fsl)
        res.append(abfr6ab_ende_t)
        return ''.join(res)
        
        
class abfr6b(fachstatistik_ergebnis):
    """Ergebnis der Fachstatistikabfrage (formabfr6b).

    Auswahl von Items einer Kategorie der Fachstatistik.
    (Auswahl von Ausprägungen eines Merkmals der Fachstatistik.)
    """
    
        
    def processForm(self, REQUEST, RESPONSE):
        year = check_int_not_empty(self.form, 'year', "Fehler beim Jahr",)
        year_op = check_str_not_empty(self.form, 'year_op',
                                      "Fehler beim Vergleichsoperator",)
        feldid = check_int_not_empty(self.form, 'feldid', "Keine ID für das Feld")
        stz = check_int_not_empty(self.form, 'stz',
                                  "Fehler beim Stellenzeichen", -1)
        if self.form.has_key('codeid'):
            codeid = self.form.get('codeid')
            if type(codeid) is type(''):
                codeid = [codeid]
        else:
            raise EBUpdateDataError("Keine Items erhalten.")
        konj = self.form['konj']
        where, order, join, query_anzeige = self.get_sql_all({feldid: (konj, codeid)},
                                                             'or', year, year_op, stz)
        fsl = FachstatistikList(where=where, order=order, join=join)
        res = []
        if not fsl:
            meldung = {'titel':'Fehler',
                       'legende':'Fehlerbeschreibung',
                       'zeile1': 'Keine Datens&auml;tze gefunden',
                       'zeile2':'Versuchen Sie es bitte erneut.'}
            return meldung_t %meldung
        fsl_alle = FachstatistikList(where = "jahr %s %s " % (year_op, year))
        res.append(head_normal_t % ("Fachstatistikabfrageergebnis " +
                                    "vom %(day)d.%(month)d.%(year)d" % today()))
        res.append(fsabfrjahr_t)
        res.append(menuefs_t)
        res.append(gesamtzahl_t % (len(fsl), len(fsl_alle), query_anzeige))
        ausgabe = self.fstat_ausgabe(res, fsl)
        res.append(abfr6ab_ende_t)
        return ''.join(res)
        

class fsabfr_plraum(Request.Request):
    """Formular für die Fachstatistikabfrage. Erfasst die Planungs-/Sozialraeume
       des zustaendigen Kreises/Bezirkes"""

    permissions = Request.ABFR_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        mitarbeiterliste = self.getMitarbeiterliste()
        user = self.user
        stellen = get_all_codes('stzei')

        if config.BERLINER_VERSION:
            # Der zustaendige Kreis/Bezirk ist jeweils als erste Position
            # fuer die Anzeige in den Formularen markiert.
            kreisliste = get_all_codes('kr')
            kreisliste.sort('sort')
            # Erhalte die Planungsraeume 1 Bezirkes aus dem Strassenkatalog
            s = SQL("SELECT distinct Plraum from strassenkat where bezirk = '%(code)s' order by Plraum" % kreisliste[0])
            plraumliste = s.execute({})
        else:
            # alle Planungsräume, die in Akte vorkommen außer 0 und 9999, die
            # keine gültigen Planungsräume sind
            t = SQL("SELECT distinct planungsr FROM akte \
                     WHERE planungsr != '0' and planungsr != '9999' ORDER BY planungsr")
            plraumliste = t.execute({})

            
        # Headerblock, Menue u. Ueberschrift fuer das HTML-Template
        res = []
        res.append(head_normal_t %('Fachstatistikabfrage'))
        res.append(fsabfrjahr_t)
        res.append(menuefs_t)
        res.append(fsabfrjahr2_t % ({'file' : 'fsergebnis_plraum','year': '%(year)s' % today()}))
        res.append(fsabfrstelle_t)
        mksel(res, codeliste_t, stellen, 'id', self.stelle['id'])
        res.append(fsabfrplraum_t)
        for p in plraumliste:
            res.append('<option value="%s" > %s ' %(p[0],p[0]))
        res.append(fsabfrtabende_t)
        return ''.join(res)
        

class fsergebnis_plraum(fachstatistik_ergebnis):
    """Ergebnis der Fachstatistikabfrage (Tabellen: Fachstatistik,
    FachstatistikLeistung, FachstatistikElternproblem,
    FachstatistikKindproblem).
    Erfasst die Planungs-/Sozialraeume """
    
    def processForm(self, REQUEST, RESPONSE):
        if config.BERLINER_VERSION:
            # Wohnbezirk, dem die Planungsraeume zugeordnet sind.
            # Der zustaendige Kreis/Bezirk ist jeweils als erste Position
            # fuer die Anzeige in den Formularen markiert.
            # Es sollen in diese Auswertung nur die Klienten genommen werden,
            # die in dem zuständigen Kreis (in Berlin Bezirk) wohnen.
            wohnbezirk = Code(kat_code='wohnbez',
                           code=Code(kat_code='kr', sort=1)['code']
                           )
        else:
            pass
            # jgh.bezirksnr sollte in der nicht Berliner Version nicht
            # verwendet werden.
            # wohnbezirk = Code(cc('wohnbez', '13'))

        year = check_int_not_empty(self.form, 'year', "Fehler beim Jahr",)
        op = check_str_not_empty(self.form, 'op', "Fehler beim Operator",)
        if self.form.has_key('stz'):
            stz = self.form.get('stz')
        else:
            raise EBUpdateDataError('Sie haben keine Stelle ausgew&auml;hlt')

        if type(stz) is type(''):
            stz = [stz]
        stellen_anzeige = ', '.join([Code(s)['name'] for s in stz])
        query_stelle = ' or '.join([('fachstat.stz = %s' % s) for s in stz])

        # Planungsraeume des Bezirks
        if self.form.has_key('bz'):
            bz = self.form.get('bz')
            if type(bz) is type(''):
                bz = [bz]
            query_plraum = ' or '.join([('fachstat.bz = %s ' % b) for b in bz])
            plraum_anzeige = "und Planungsräume: " + ', '.join([str(b) for b in bz])
            if config.BERLINER_VERSION:
                query_wohnbezirk = " jghstat.bezirksnr = '%(id)s' " % wohnbezirk
                wohnbezirk_anzeige = "im Bezirk: '%(name)s.' " % wohnbezirk
            else:
                query_wohnbezirk = ''
                wohnbezirk_anzeige = ''
            plraum_tabelle = True
        else:
            plraum_tabelle = False
            plraum_anzeige = ''  
            wohnbezirk_anzeige = ''
            
        query_anzeige = "Jahr %s %s und Stelle(n): %s %s %s" % (op,
                        year, stellen_anzeige, plraum_anzeige, wohnbezirk_anzeige)

        meldung = {'titel':'Keine Datens&auml;tze gefunden',
                   'legende':'Hinweis!',
                    'zeile1':'Es wurden keine Datens&auml;tze gefunden!',
                    'zeile2':'Versuchen Sie es bitte erneut.'}

        # Abfrage der Fachstatistik pro Zeitraum und Stelle(n)
        query_gesamt = "( fachstat.jahr %s %s ) and ( %s ) "  % (op,
                        year, query_stelle)

        fsl_gesamt =  FachstatistikList(where=query_gesamt, join=[])
        if not fsl_gesamt:
            return meldung_t % meldung
    
        # Abfrage der Fachstatistik pro Zeitraum und Stelle(n)
        # und Planungsraeume
        if plraum_tabelle:
            query = "( fachstat.jahr %s %s ) and ( %s ) and ( %s )" % (op,
                     year, query_stelle, query_plraum)
            if config.BERLINER_VERSION:
                join=[('jghstat', 'fachstat.fall_fn = jghstat.fall_fn')]
                query += " and ( %s )" % query_wohnbezirk
            else:
                # keine Abfrage von jghstat.bezirksnr
                join = []
            fsl_plraum =  FachstatistikList(where=query, join=join)
            if fsl_plraum:
                fsl = fsl_plraum
                gesamt1 = len(fsl_plraum)
                gesamt2 = len(fsl_gesamt)
            else:
                return meldung_t % meldung
        else:
            fsl = fsl_gesamt
            gesamt1 = len(fsl_gesamt)
            gesamt2 = gesamt1
            
        # Headerblock, Menue u. Uberschrift fuer das HTML-Template
        res = []
        res.append(head_normal_t % ("Fachstatistikergebnisse"))
        res.append(fsergebnis1_t)
        res.append(menuefs_t)
        res.append(gesamtzahl_t % (gesamt1, gesamt2, query_anzeige))
        ausgabe = self.fstat_ausgabe(res, fsl, plraum_tabelle)
        res.append(fsergebnis_ende_t)
        return ''.join(res)



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
        
        ##*************************************************************************
        ## Anzahl der abgeschlossenen Faelle, fuer einen bestimmten Zeitraum, mit
        ## gleicher Konsultationssumme
        ##
        ## Heller 25.09.2001
        ##*************************************************************************
class formabfr9(Request.Request):

    permissions = Request.ABFR_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        stelle = self.stelle
        lauf_jahr = '%(year)d' % today()
        jahr_von = self.form.get('jahrvon')
        jahr_bis = self.form.get('jahrbis')
        seite = { 'seite':'./formabfr9a'}
        
        ##***************************************************************
        ## Fehlerausgabe bei falschem Datum oder unvollstaendigen Daten
        ## HeS 28.09.2001
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
                     'zeile1':'Das Bis-Datum liegt nach dem heutigem!',
                     'zeile2':'Versuchen Sie es bitte erneut.'}
            res.append(meldung_t % meldung)
            return ''.join(res)
            
        fsl = FachstatistikList(where = 'jahr >= %s and jahr <= %s '
                                % (jahr_von, jahr_bis) )
        if len(fsl) > 0:
            pass
        else:
            meldung = {'titel':'Keine Datens&auml;tze gefunden!',
                     'legende':'Hinweis!',
                     'zeile1':'Es wurden keine Datens&auml;tze gefunden!',
                     'zeile2':'Versuchen Sie es bitte erneut.'}
            res.append(meldung_t % meldung)
            return ''.join(res)
            
        res.append(head_normal_t
                   %("Anzahl abgeschl. F&auml;lle - gleiche Konsultationssumme"))
        res.append(thabfr9_t)
        for k in WertAuszaehlung(fsl, 'kat').get_result():
            res.append(abfr9mid_t % (k[0], k[1], k[2]))
        res.append(abfr9end_t)
        return ''.join(res)
        
        ##*************************************************************************
        ## Zeitraumauswahl  der Konsultationssummen
        ## fuer abgeschlossene Faelle
        ##
        ## Heller 26.09.2001
        ##*************************************************************************
class formabfr9a(Request.Request):

    permissions = Request.ABFR_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        stelle = self.stelle
        res = []
        res.append(head_normal_t %("Anzahl abgeschl. F&auml;lle - gleiche Konsultationssumme"))
        res.append(abfr9ages_t)
        return ''.join(res)
        
        ##*************************************************************************
        ## Anzahl der Faelle, fuer einen bestimmten Zeitraum, mit gleicher
        ## Konsultationsanzahl bei den verschiedenen Personen
        ##
        ## Heller 26.09.2001
        ## Juerg geaendert 3.06.2002
        ##*************************************************************************
        
class formabfr10(Request.Request):

    permissions = Request.ABFR_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        stelle = self.stelle
        lauf_jahr = '%(year)d' % today()
        jahr_von = self.form.get('jahrvon')
        jahr_bis = self.form.get('jahrbis')
        seite = { 'seite':'./formabfr10a'}
        
        
        ##***************************************************************
        ## Fehlerausgabe bei falschem Datum oder unvollstaendigen Daten
        ## HeS 28.09.2001
        ##***************************************************************
        res = []
        if jahr_von == '' or jahr_bis =='' :
            meldung = {'titel':'Daten unvollst&auml;ndig!',
                     'legende':'Hinweis!','dauer':'4','url':'formabfr10a',
                     'zeile1':'Die angegebenen Daten waren unvollst&auml;ndig!',
                     'zeile2':'Versuchen Sie es bitte erneut.','url2':'formabfr10a'}
            return meldung_t % meldung
            
        if jahr_von > jahr_bis :
            meldung = {'titel':'Jahreszahl ist nicht korrekt!',
                     'legende':'Hinweis!','dauer':'4','url':'formabfr10a',
                     'zeile1':'Das Von-Datum liegt nach Bis-Datum!',
                     'zeile2':'Versuchen Sie es bitte erneut.','url2':'formabfr10a'}
            return meldung_t % meldung
            
        if jahr_von < '1970' or jahr_von >'2030':
            meldung = {'titel':'Jahreszahl ist nicht korrekt!',
                     'legende':'Hinweis!','dauer':'4','url':'formabfr10a',
                     'zeile1':'Das Von-Datum liegt vor 1970 oder nach 2030!',
                     'zeile2':'Versuchen Sie es bitte erneut.','url2':'formabfr10a'}
            return meldung_t % meldung
            
        if jahr_bis > lauf_jahr:
            meldung = {'titel':'Jahreszahl ist nicht korrekt!',
                     'legende':'Hinweis!','dauer':'4','url':'formabfr10a',
                     'zeile1':'Das Bis-Datum liegt nach dem heutigem!',
                     'zeile2':'Versuchen Sie es bitte erneut.','url2':'formabfr10a'}
            return meldung_t % meldung
            
        fsl = FachstatistikList(where = 'jahr >= %s and jahr <= %s '
                                % (jahr_von, jahr_bis) )
        if len(fsl) > 0:
            pass
        else:
            meldung = {'titel':'Keine Datens&auml;tze gefunden!',
                     'legende':'Hinweis!',
                     'zeile1':'Es wurden keine Datens&auml;tze gefunden!',
                     'zeile2':'Versuchen Sie es bitte erneut.'}
            return meldung_t % meldung
            
        res.append(head_normal_t %("Anzahl abgeschl. F&auml;lle - gleiche Konsultationsanzahl" ))
        res.append(thabfr10_t)
        res2 = []
        
        feldliste = [("Kontaktanzahl Mutter","kkm"),("Kontaktanzahl Vater","kkv"),
                     ("Kontaktanzahl Kind","kki"),("Kontaktanzahl Paar","kpa"),
                     ("Kontaktanzahl Familie","kfa"),
                     ("Kontaktanzahl Sozialarbeiter","ksoz"),
                     ("Kontaktanzahl Lehrer","kleh"),("Kontaktanzahl Erzieher","kerz"),
                     ("Kontaktanzahl Hilfebesprechung","kkonf"),
                     ("Kontaktanzahl Sonstige","kson")]
        
        for f in feldliste:
            res2.append(abfr10start_t % f[0])
            for k in WertAuszaehlung(fsl, f[1]).get_result():
                res2.append(abfr10mid_t % (k[0], k[1], k[2]))
            res2.append(abfr10end_t)
        res.append(''.join(res2))
        res.append(all_end_abfr10_t)
        
        return ''.join(res)
        
        
        
        
        ##*************************************************************************
        ## Zeitraumauswahl und Auswahl der Konsultationsanzahl fuer abgeschlossenen
        ## Faelle mit gleicher Konsultationsanzahl bei den verschiedenen Personen
        ##
        ## Heller 26.09.2001
        ##*************************************************************************
class formabfr10a(Request.Request):

    permissions = Request.ABFR_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        res = []
        res.append(head_normal_t %("Anzahl abgeschl. F&auml;lle - gleiche Konsultationsanzahl"))
        res.append(abfr10ages_t)
        return ''.join(res)
        
        
        ##*************************************************************************
        ## Anzahl der abgeschlossenen Faelle, fuer einen bestimmten Zeitraum,
        ## mit gleichlanger Beratungsdauer
        ##
        ## Heller 26.09.2001
        ## jh 14.06.02
        ##*************************************************************************
class formabfr11(Request.Request):

    permissions = Request.ABFR_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        stelle = self.stelle
        lauf_jahr = '%(year)d' % today()
        jahr_von = self.form.get('jahrvon')
        jahr_bis = self.form.get('jahrbis')
        seite = { 'seite':'./formabfr11a'}
        
        ##***************************************************************
        ## Fehlerausgabe bei falschem Datum oder unvollstaendigen Daten
        ## HeS 28.09.2001
        ##***************************************************************
        res = []
        if jahr_von == '' or jahr_bis =='':
            meldung = {'titel':'Daten unvollst&auml;ndig!',
                       'legende':'Hinweis!',
                       'zeile1':'Die angegebenen Daten waren unvollst&auml;ndig!',
                       'zeile2':'Versuchen Sie es bitte erneut.'}
            return meldung_t % meldung
            
        if jahr_von > jahr_bis :
            meldung = {'titel':'Jahreszahl ist nicht korrekt!',
                       'legende':'Hinweis!',
                       'zeile1':'Das Von-Datum liegt nach Bis-Datum!',
                       'zeile2':'Versuchen Sie es bitte erneut.'}
            return meldung_t % meldung
            
        if jahr_von < '1970' or jahr_von >'2030':
            meldung = {'titel':'Jahreszahl ist nicht korrekt!',
                       'legende':'Hinweis!',
                       'zeile1':'Das Von-Datum liegt vor 1970 oder nach 2030!',
                       'zeile2':'Versuchen Sie es bitte erneut.'}
            return meldung_t % meldung
            
        if jahr_bis > lauf_jahr:
            meldung = {'titel':'Jahreszahl ist nicht korrekt!',
                     'legende':'Hinweis!',
                     'zeile1':'Das Bis-Datum liegt nach dem heutigem!',
                     'zeile2':'Versuchen Sie es bitte erneut.'}
            return meldung_t % meldung
            
        gleichDauer = JugendhilfestatistikList(where = 'ey >= %s' % jahr_von
                              + ' and ey <= %s ' % jahr_bis )
        
        if len(gleichDauer) > 0:
            pass
        else:
            meldung = {'titel':'Keine Datens&auml;tze gefunden!',
                     'legende':'Hinweis!',
                     'zeile1':'Es wurden keine Datens&auml;tze gefunden!',
                     'zeile2':'Versuchen Sie es bitte erneut.'}
            return meldung_t % meldung
            
        liste_beratdauern = []
        for zeile in gleichDauer:
            beginn = Date(zeile['bgy'], zeile['bgm'])
            dauer = beginn.diff(Date(zeile['ey'], zeile['em']))
            liste_beratdauern.append(dauer)
            
        res.append(head_normal_t %("Anzahl der abgeschl. F&auml;lle mit gleichlanger Beratungsdauer"))
        res.append(thabfr11_t)
        
        liste_beratdauern.sort()
        i = 0
        if liste_beratdauern > 0:
            while i < len(liste_beratdauern):
                anzahl = liste_beratdauern.count(liste_beratdauern[i])
                if liste_beratdauern[i] == 0: liste_beratdauern[i] = '< 1'
                res.append(abfr11mid_t % (liste_beratdauern[i], anzahl,
                                          float(anzahl)*100/float(len(liste_beratdauern))))
                i = i + anzahl
                
        res.append(abfr11end_t)
        return ''.join(res)
        
        
        ##*************************************************************************
        ## Zeitraumauswahl fuer abgeschlossene Faelle
        ## mit gleichlanger Beratungsdauer
        ##
        ## Heller 26.09.2001
        ##*************************************************************************
class formabfr11a(Request.Request):

    permissions = Request.ABFR_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        res = []
        res.append(head_normal_t %("Auswahl des gew&uuml;nschten Zeitraumes und die Länge der Beratungszeit in Monaten"))
        res.append(abfr11ages_t)
        return ''.join(res)
        
        ##*************************************************************************
        ## Zeitraumauswahl und Auswahl einer Leistung fuer abgeschlossene Faelle
        ## mit gleichlanger Beratungsdauer
        ##
        ## Heller 26.09.2001
        ## jh 14.06.02
        ##*************************************************************************
class formabfr12a(Request.Request):

    permissions = Request.ABFR_PERM
    def processForm(self, REQUEST, RESPONSE):
        massnahmen = get_codes('fsle')
        
        res = []
        res.append(head_normal_t %("Auswahl des gew&uuml;nschten Zeitraumes und Auswahl einer Leistung"))
        res.append(abfr12ages_t)
        mksel(res, codeliste_t, massnahmen)
        res.append(abfr12ages2_t)
        return ''.join(res)
        
        
        ##*************************************************************************
        ## Anzahl der abgeschlossenen Faelle mit gleichlanger Beratungsdauer
        ## zu einer Leistung fuer einen bestimmten Zeitraum
        ##
        ## Heller 28.09.2001
        ## jh 14.06.02
        ##*************************************************************************
class formabfr12(Request.Request):

    permissions = Request.ABFR_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        stelle = self.stelle
        lauf_jahr = '%(year)d' % today()
        jahr_von = self.form.get('jahrvon')
        jahr_bis = self.form.get('jahrbis')
        leistung = self.form.get('leistung')
        seite = { 'seite':'./formabfr12a'}
        
        ##***************************************************************
        ## Fehlerausgabe bei falschem Datum oder unvollstaendigen Daten
        ## HeS 31.09.2001
        ##***************************************************************
        if jahr_von == '' or jahr_bis =='':
            meldung = {'titel':'Daten unvollst&auml;ndig!',
                       'legende':'Hinweis!',
                       'zeile1':'Die angegebenen Daten waren unvollst&auml;ndig!',
                       'zeile2':'Versuchen Sie es bitte erneut.'}
            return meldung_t % meldung
            
        if jahr_von > jahr_bis :
            meldung = {'titel':'Jahreszahl ist nicht korrekt!',
                       'legende':'Hinweis!',
                       'zeile1':'Das Von-Datum liegt nach Bis-Datum!',
                       'zeile2':'Versuchen Sie es bitte erneut.'}
            return meldung_t % meldung
            
        if jahr_von < '1970' or jahr_von >'2030':
            meldung = {'titel':'Jahreszahl ist nicht korrekt!',
                       'legende':'Hinweis!',
                       'zeile1':'Das Von-Datum liegt vor 1970 oder nach 2030!',
                       'zeile2':'Versuchen Sie es bitte erneut.'}
            return meldung_t % meldung
            
        if jahr_bis > lauf_jahr:
            meldung = {'titel':'Jahreszahl ist nicht korrekt!',
                       'legende':'Hinweis!',
                       'zeile1':'Das Bis-Datum liegt nach dem heutigem!',
                       'zeile2':'Versuchen Sie es bitte erneut.'}
            return meldung_t % meldung
            
        query = 'fachstatlei.le = %s and jghstat.ey >= %s and jghstat.ey <= %s' % \
                (leistung, jahr_von, jahr_bis)
        join = [('fachstat', 'fachstat.fall_fn = jghstat.fall_fn'),
                ('fachstatlei', 'fachstat.id = fachstatlei.fstat_id')]
        jghl = JugendhilfestatistikList(where=query, join=join)
        if not jghl:
            meldung = {'titel':'Keine Datens&auml;tze gefunden!',
                     'legende':'Hinweis!',
                     'zeile1':'Es wurden keine Datens&auml;tze gefunden!',
                     'zeile2':'Versuchen Sie es bitte erneut.'}
            return meldung_t % meldung
        liste_beratdauern = []
        for j in jghl:
            beginn = Date(j['bgy'], j['bgm'])
            dauer = beginn.diff(Date(j['ey'], j['em']))
            liste_beratdauern.append(dauer)
            
        res = []
        res.append(
            head_normal_t %
            ("Anzahl der abgeschl. F&auml;lle mit gleicher " +
             "Beratungsdauer zu einer bestimmten Leistung"))
        res.append(thabfr12_t % nfc(leistung))
        
        liste_beratdauern.sort()
        i = 0
        while i < len(liste_beratdauern):
            anzahl = liste_beratdauern.count(liste_beratdauern[i])
            if liste_beratdauern[i] == 0: liste_beratdauern[i] = '< 1'
            res.append(abfr12mid_t %  (liste_beratdauern[i], anzahl,
                                        float(anzahl)*100/float(len(liste_beratdauern))))
            i = i + anzahl
            
        res.append(abfr12end_t)
        return ''.join(res)
        
        
        ##*************************************************************************
        ## Anzahl der abgeschlossenen Faelle fuer einen bestimmten Zeitraum,
        ## bei denen 'Mutter und Vater' das gleiche Merkmal x haben
        ##
        ## Heller 31.09.2001
        ## jh 14.06.02
        ##*************************************************************************
class formabfr13(Request.Request):

    permissions = Request.ABFR_PERM
    def processForm(self, REQUEST, RESPONSE):
        stelle = self.stelle
        lauf_jahr = '%(year)d' % today()
        jahr_von = self.form.get('jahrvon')
        jahr_bis = self.form.get('jahrbis')
        seite = {'seite': './formabfr13a'}
        
        ##***************************************************************
        ## Fehlerausgabe bei falschem Datum oder unvollstaendigen Daten
        ## HeS 31.09.2001
        ##***************************************************************
        res = []
        if jahr_von == '' or jahr_bis =='':
            meldung = {'titel':'Daten unvollst&auml;ndig!',
                       'legende':'Hinweis!',
                       'zeile1':'Die angegebenen Daten waren unvollst&auml;ndig!',
                       'zeile2':'Versuchen Sie es bitte erneut.'}
            return meldung_t % meldung
            
        if jahr_von > jahr_bis :
            meldung = {'titel':'Jahreszahl ist nicht korrekt!',
                       'legende':'Hinweis!',
                       'zeile1':'Das Von-Datum liegt nach Bis-Datum!',
                       'zeile2':'Versuchen Sie es bitte erneut.'}
            return meldung_t % meldung
            
        if jahr_von < '1980' or jahr_von >'2030':
            meldung = {'titel':'Jahreszahl ist nicht korrekt!',
                     'legende':'Hinweis!',
                     'zeile1':'Das Von-Datum liegt vor 1970 oder nach 2030!',
                     'zeile2':'Versuchen Sie es bitte erneut.'}
            return meldung_t % meldung
            
        if jahr_bis > lauf_jahr:
            meldung = {'titel':'Jahreszahl ist nicht korrekt!',
                       'legende':'Hinweis!',
                       'zeile1':'Das Bis-Datum liegt nach dem heutigem!',
                       'zeile2':'Versuchen Sie es bitte erneut.'}
            return meldung_t % meldung
            
        res.append(head_normal_t %("Anzahl abgeschl. F&auml;lle - Mutter und Vater haben das gleiche Merkmal x"))
        res.append(thabfr13_t %(jahr_von,jahr_bis))
        
        #                 (Titel, kat_code, dbfeld, dbfeld)
        merkmalsliste = [("Gleiche Herkunft",'fshe','hkm','hkv'),
                         ("Gleicher Beruf",'fsbe','bkm','bkv'),
                         ("Gleiche Qualifikation",'fsquali','qualikm','qualikv'),
                         ("Gleiche Altersgruppe",'fsagel','agkm','agkv')]
        
        gl = []  # sammelt Anzahl der Datensaetze fuer 1 Abfrage
        res2 = []
        for m in merkmalsliste:
            fsl =  FachstatistikList(where = '%s = %s and jahr >= %s and jahr <= %s'
                                       % (m[2],m[3],jahr_von,jahr_bis), order = m[2] )
            if(len(fsl) > 0):
                res2.append(abfr13start_t % m[0])
                for a in CodeAuszaehlung(fsl, m[2]).get_result():
                    res2.append(abfr13mid_t % (a[0], a[1]))
                res2.append(abfr13end_t)
            gl.append(len(fsl))
            
        res.append(abfr13ges_t % (stelle['name'],gl[0],gl[1],gl[2],gl[3]))
        res.append(''.join(res2))
        res.append(all_end_abfr13_t)
        return ''.join(res)
        
        ##*************************************************************************
        ## Zeitraumauswahl fuer abgeschlossenen Faelle, bei denen 'Mutter und Vater'
        ## das gleiche Merkmal x haben
        ##
        ## Heller 31.09.2001
        ##*************************************************************************
class formabfr13a(Request.Request):

    permissions = Request.ABFR_PERM
    def processForm(self, REQUEST, RESPONSE):
    
        res = []
        res.append(head_normal_t %("Anzahl abgeschl. F&auml;lle - Mutter und Vater haben das gleiche Merkmal x"))
        res.append(abfr13ages_t)
        return ''.join(res)
        
        
        ##*************************************************************************
        ## Anzahl der abgeschlossenen Faelle fuer einen bestimmten Zeitraum,
        ## bei denen 'Mutter oder Vater' das gleiche Merkmal x haben
        ##
        ## Heller 31.09.2001
        ## jh 14.06.02
        ##*************************************************************************
class formabfr14(Request.Request):

    permissions = Request.ABFR_PERM
    def processForm(self, REQUEST, RESPONSE):
        stelle = self.stelle
        lauf_jahr = '%(year)d' % today()
        jahr_von = self.form.get('jahrvon')
        jahr_bis = self.form.get('jahrbis')
        seite = {'seite': './formabfr14a'}
        
        
        ##***************************************************************
        ## Fehlerausgabe bei falschem Datum oder unvollstaendigen Daten
        ## HeS 28.09.2001
        ##***************************************************************
        res = []
        if jahr_von == '' or jahr_bis =='':
            meldung = {'titel':'Daten unvollst&auml;ndig!',
                       'legende':'Hinweis!',
                       'zeile1':'Die angegebenen Daten waren unvollst&auml;ndig!',
                       'zeile2':'Versuchen Sie es bitte erneut.'}
            return meldung_t % meldung
            
        if jahr_von > jahr_bis :
            meldung = {'titel':'Jahreszahl ist nicht korrekt!',
                       'legende':'Hinweis!',
                       'zeile1':'Das Von-Datum liegt nach Bis-Datum!',
                       'zeile2':'Versuchen Sie es bitte erneut.'}
            return meldung_t % meldung
            
        if jahr_von < '1980' or jahr_von >'2030':
            meldung = {'titel':'Jahreszahl ist nicht korrekt!',
                       'legende':'Hinweis!',
                       'zeile1':'Das Von-Datum liegt vor 1970 oder nach 2030!',
                       'zeile2':'Versuchen Sie es bitte erneut.',}
            return meldung_t % meldung
            
        if jahr_bis > lauf_jahr:
            meldung = {'titel':'Jahreszahl ist nicht korrekt!',
                       'legende':'Hinweis!',
                       'zeile1':'Das Bis-Datum liegt nach dem heutigem!',
                       'zeile2':'Versuchen Sie es bitte erneut.',}
            return meldung_t % meldung
            
        res.append(head_normal_t %("Anzahl der abgeschl. F&auml;lle - Mutter oder Vater haben das Merkmal x"))
        res.append(thabfr14_t %(jahr_von,jahr_bis))
        
        #                 (Titel, kat_code, dbfeld, dbfeld)
        merkmalsliste = [("Gleiche Herkunft",'fshe','hkm','hkv'),
                         ("Gleicher Beruf",'fsbe','bkm','bkv'),
                         ("Gleiche Qualifikation",'fsquali','qualikm','qualikv'),
                         ("Gleiche Altersgruppe",'fsagel','agkm','agkv')]
        
        gl = []  # enthaelt Laenge der Liste fuer 1 Abfrage
        res2 = []
        for m in merkmalsliste:
            fsl =  FachstatistikList(where = '%s != %s and jahr >= %s and jahr <= %s'
                                       % (m[2],m[3],jahr_von,jahr_bis), order = m[2])
            if(len(fsl) > 0):
                res2.append(abfr14start_t % m[0])
                for a in CodeAuszaehlung(fsl, m[2]).get_result():
                    res2.append(abfr14mid_t % (a[0], a[1]))
                res2.append(abfr14end_t)
            gl.append(len(fsl))
            
        res.append(abfr14ges_t % (stelle['name'],gl[0],gl[1],gl[2],gl[3]))
        res.append(''.join(res2))
        res.append(all_end_abfr14_t)
        return ''.join(res)
        
        ##*************************************************************************
        ## Zeitraumauswahl fuer abgeschlossenen Faelle, bei denen 'Mutter oder Vater'
        ## das gleiche Merkmal x haben
        ##
        ## Heller 31.09.2001
        ##*************************************************************************
class formabfr14a(Request.Request):

    permissions = Request.ABFR_PERM

    def processForm(self, REQUEST, RESPONSE):
        res = []
        res.append(head_normal_t %("Anzahl abgeschl. F&auml;lle - Mutter oder Vater Merkmal x gleich"))
        res.append(abfr14ages_t)
        return ''.join(res)

        
        
