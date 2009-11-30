# coding: latin-1
"""Modul für die Statistik-Abfragen."""

import sys
from ebkus.config import config
from ebkus.db.sql import SQL
from ebkus.app import Request
from ebkus.app.ebapi import EE, nfc, Fachstatistik, FachstatistikList, \
     JugendhilfestatistikList, Jugendhilfestatistik2007List, \
     Jugendhilfestatistik, Jugendhilfestatistik2007, \
     ZustaendigkeitList, AkteList, BezugspersonList, FallList, GruppeList, \
     Tabelle, Code, Feld, Mitarbeiter, MitarbeiterList, MitarbeiterGruppeList, \
     sorted, today, cc, check_int_not_empty, check_list, \
     check_str_not_empty, EBUpdateDataError, getQuartal, get_rm_datum, Date, Abfrage, AbfrageList
from ebkus.app.ebapih import get_codes, mksel, get_all_codes
from ebkus.html.statistik_ergebnis import auszergebnis
from ebkus.app.statistik import CodeAuszaehlung, WertAuszaehlung
from ebkus.html.abfragedef import Query
from ebkus.html.beratungskontakt import hatte_kontakt_im_abschlussjahr
from ebkus.app_surface.standard_templates import *
from ebkus.app_surface.abfragen_templates import *
from ebkus.app import ebupd
import ebkus.html.htmlgen as h
from ebkus.html.akte_share import akte_share


class Ueberschrift(object):
    "Für Auszählungen, wird in den Strom der Tabellen eingefügt"
    def __init__(self, ueberschrift):
        self.ueberschrift = ueberschrift
        self.identname = self.ueberschrift.lower().replace('/','_').replace(' ', '_')
        self.title = '------------------- %s ---' % ueberschrift
    def ueberschrift_einfuegen(self, res):
        res.append(h.Tr(cells=[h.String(string='<a name="%s"></a>%s' %
                                        (self.identname, self.ueberschrift),
                                        class_='titeltext')]).display()
                   )

class _statistik(Request.Request, akte_share):
    pass

class statabfr(_statistik):
    "Formular für die Fach- und Bundesstatistikabfrage"
    permissions = Request.ABFR_PERM
    def _process(self):
        teilmenge = h.FieldsetDataTable(
            legend='Teilmenge',
            daten=[[h.SelectItem(label='Definierte Teilmengen',
                                 name='teilm',
                                 tip="Teilmenge auswählen, um Häufigkeitstabellen "
                                 "nur für diese zu erstellen ",
                                 options=self.for_teilmengen(),
                                 n_col=3,
                                 ),
                    ],
                   [h.Button(value="Bearbeiten",
                             name='abfrop',
                             tip="Ausgewählte Definition ansehen und bearbeiten",
                             type='submit',
                             ),
                    h.Button(value="Neu",
                             name='abfrop',
                             tip="Neue Teilmengendefinition erstellen",
                             type='submit',
                             ),
                    h.Button(value="Löschen",
                             name='abfrop',
                             tip="Ausgewählte Definition löschen",
                             type='submit',
                             ),
                    ],
                   ],
            )
        auszaehlung = h.FieldsetInputTable(
            legend='Auszählung',
            daten=[[h.CheckItem(label='Fachstatistik',
                                tip="Häufigkeitstabellen für die Fragen der Fachstatistik",
                                name='item_auswahl',
                                value='fs_gesamt',
                                ),
                    h.CheckItem(label='Bundesstatistik',
                                name='item_auswahl',
                                tip="Häufigkeitstabellen für die Fragen der Bundesstatistik",
                                value='jgh_gesamt',
                                ),
                    h.CheckItem(label='Regionalstatistik',
                                name='item_auswahl',
                                tip="Häufigkeitstabellen für %s" %
                                ', '.join(['Planungsraum', 'Ort', 'PLZ'] +
                                          [s.capitalize() for s in config.STRASSENSUCHE.split()]),
                                value='regional',
                                ),
                    h.CheckItem(label='Teilmengen',
                                name='item_auswahl',
                                tip="Eine Häufigkeitstabelle mit der Anzahl der Klienten "
                                "in jeder der benutzerdefinierten Teilmengen",
                                value='teilmengen',
                                ),
                    ],
                   ]
            )

        buttons = h.FieldsetInputTable(daten=[[
            h.Button(value="Auszählen",
                     name='op',
                     tip="Auswertung durchführen",
                     type='submit',
                     ),
            ]])
        res = h.FormPage(
            title='Statistikabfrage',
            name="statform",action="statabfr",method="post",
            breadcrumbs = (('Hauptmenü', 'menu'),
                           ),
            hidden = (),
            rows=(self.get_auswertungs_menu(),
                  self.grundgesamtheit(show_quartal=False,
                                       show_welche=True,
                                       welche='abgeschlossen',
                                       show_ohne_bk_raus=config.BERATUNGSKONTAKTE,
                                       ),
                  teilmenge,
                  auszaehlung,
                  #h.SpeichernZuruecksetzenAbbrechen(),
                  buttons,
                  ),
            )
        return res.display()
                 
    def processForm(self, REQUEST, RESPONSE):
        #print 'FORM', self.form
        file = self.form.get('file')
        op = self.form.get('op')
        abfrop = self.form.get('abfrop')
        teilm = self.form.get('teilm')
        if abfrop in ('Bearbeiten', 'Neu', 'Löschen'):
            if abfrop == 'Neu':
                RESPONSE.redirect('abfragedef?op=new')
                return ''
            if teilm:
                url = 'abfragedef?op=%s&abfrid=%s'
                if abfrop == 'Bearbeiten':
                    url = url % ('edit', teilm)
                elif abfrop == 'Löschen':
                    url = url % ('del', teilm)
                RESPONSE.redirect(url)
                return ''
        if file == 'abfragedef':
            if op == 'Speichern':
                ebupd.upd_or_einf_abfr(self.form)
            elif op == 'Abbrechen':
                pass
            else:
                # nicht Speichern oder Abbrechen gedrückt, es geht weiter mir abfragedef
                return self.ebkus.dispatch(file, REQUEST, RESPONSE)
        if op == 'Auszählen':
            return self.ebkus.dispatch('statergebnis', REQUEST, RESPONSE)
        if file == 'rmabfr':
            ebupd.rmabfr(self.form)
        return self._process()

class _statistik_ergebnis(Request.Request, akte_share):
    """Oberklasse für alle Fachstatistikabfragen, die bisher
    fstat_ausgabe benutzt haben.
    """
    permissions = Request.ABFR_PERM
    def get_fachstatistik_auszaehlungen(self, liste, session_key):
        """Liefert eine Liste von Auszählungsobjekten für fstat_ausgabe"""
        from ebkus.app.statistik import \
             CodeAuszaehlung as CA, \
             WertAuszaehlung as WA, \
             RohWertAuszaehlung as RWA, \
             ObjektAuszaehlung as OA, \
             MehrfachCodeAuszaehlung as MA
        felder = Tabelle(klasse='Fachstatistik')['felder']
        auszaehlungen = [Ueberschrift('Fachstatistik')]
        auszaehlungen += [CA(liste, f, session_key=session_key)
                         for f in felder
                         if f.get('kat_code') and
                         not f['flag']&1
                         ]
        app = auszaehlungen.append # Abkürzung
        app(OA(liste, 'mit_id', self.getMitarbeiterliste(), 'na',
               title="Mitarbeiter", session_key=session_key))
        return auszaehlungen
                             
    def get_jgh07_auszaehlungen(self, liste, session_key):
        """Liefert eine Liste von Auszählungsobjekten"""
        from ebkus.app.statistik import \
             CodeAuszaehlung as CA, \
             MehrfachCodeAuszaehlung as MA, \
             MehrfachCodeAuszaehlung2 as MA2, \
             ObjektAuszaehlung as OA, \
             BereichsKategorieAuszaehlung as BKA, \
             EinzelWertAuszaehlung as EWA
        auszaehlungen = [Ueberschrift('Bundesstatistik')]
        auszaehlungen += [
            CA(liste, 'stz', title='Dienststelle', session_key=session_key),
            EWA(liste, 'zustw', ('1',),
                title='Übernahme wegen Zuständigkeitswechsel', session_key=session_key),
            CA(liste, 'hilf_art', title='Art der Hilfe', session_key=session_key),
            CA(liste, 'hilf_ort', title='Ort der Durchführung', session_key=session_key),
##             CA(liste, 'traeger', title='Traeger', session_key=session_key),
            CA(liste, 'gs', title='Geschlecht', session_key=session_key),
            BKA(liste, 'alter', 'jghag', title='Altersgruppen', session_key=session_key),
            CA(liste, 'aort_vor', title='Aufenthaltsort vor der Hilfe',
               session_key=session_key),
            CA(liste, 'sit_fam', title='Situation in der Herkunftsfamilie',
               session_key=session_key),
            CA(liste, 'ausl_her',
               title='Ausländische Herkunft mindestens eines Elternteils',
               session_key=session_key),
            CA(liste, 'vor_dt',
               title='In der Familie wird vorrangig deutsch gesprochen',
               session_key=session_key),
            CA(liste, 'wirt_sit',
               title='Lebt von ALGII, Grundsicherung oder Sozialhilfe',
               session_key=session_key),
            CA(liste, 'aip',
               title='Anregende Institution oder Person',
               session_key=session_key),
            CA(liste, 'ees',
               title='Teilweiser oder vollständiger Entzug der elterlichen Sorge',
               session_key=session_key),
            CA(liste, 'va52',
               title='Verfahrensaussetzung nach §52 FGG',
               session_key=session_key),
            CA(liste, 'rgu',
               title='Unterbringung mit Freiheitsentzug',
               session_key=session_key),
            MA2(liste, ['gr1', 'gr2', 'gr3'],
               title='Gründe für die Hilfegewährung',
               session_key=session_key),
            BKA(liste, 'nbkges', 'fskat',
                title='Zahl der Beratungskontakte',
                session_key=session_key),
            CA(liste, 'lbk6m',
               title='Letzter Beratungskontakt liegt mehr als sechs Monate zurück',
               session_key=session_key),
            CA(liste, 'grende',
               title='Grund für die Beendigung',
               session_key=session_key),
            CA(liste, 'aort_nac',
               title='Anschließender Aufenthalt',
               session_key=session_key),
            CA(liste, 'unh',
               title='Unmittelbar nachfolgende Hilfe',
               session_key=session_key),
            ]
##         mitarbeiter = MitarbeiterList(where="benr = %s" % cc('benr', 'bearb'))
##         auszaehlungen.append(OA(liste, 'mit_id', mitarbeiter,
##                                 'na', title="Mitarbeiter", file=file))
        return auszaehlungen

    def get_jgh_auszaehlungen(self, liste, session_key):
        """Liefert eine Liste von Auszählungsobjekten"""
        from ebkus.app.statistik import \
             CodeAuszaehlung as CA, \
             MehrfachCodeAuszaehlung as MA, \
             ObjektAuszaehlung as OA
        auszaehlungen = [Ueberschrift('Alte Bundesstatistik')]
        auszaehlungen += [
            CA(liste, 'stz', title='Dienststelle', session_key=session_key),  
            CA(liste, 'bgr', title="Beendigungsgrund", session_key=session_key),
            CA(liste, 'gs',  title="Geschlecht", session_key=session_key),
            CA(liste, 'ag',  title="Altersgruppe", session_key=session_key),
            CA(liste, 'fs',  title="Junger Mensch lebt", session_key=session_key),
            CA(liste, 'hke', title="Staatsangehörigkeit", session_key=session_key),
            CA(liste, 'gsa', title="Geschwisterzahl", session_key=session_key),
            CA(liste, 'gsu', title="Geschwisterzahl unbekannt", session_key=session_key),
            CA(liste, 'zm',  title="1. Kontaktaufnahme durch", session_key=session_key),
            MA(liste, ['ba0', 'ba1', 'ba2', 'ba3', 'ba4',
                       'ba5', 'ba6', 'ba7', 'ba8', 'ba9'],
               title='Beratungsanlass', session_key=session_key),
            CA(liste, 'schw', title="Beratungsschwerpunkt", session_key=session_key),
            CA(liste, 'fbe0', title="Beratung setzt ein bei dem jungen Menschen",
               session_key=session_key),
            CA(liste, 'fbe1', title="Beratung setzt ein bei den Eltern",
               session_key=session_key),
            CA(liste, 'fbe2', title="Beratung setzt ein in der Familie",
               session_key=session_key),
            CA(liste, 'fbe3', title="Beratung setzt ein im sozialen Umfeld",
                               session_key=session_key)
            ]
##         mitarbeiter = MitarbeiterList(where="benr = %s" % cc('benr', 'bearb'))
##         auszaehlungen.append(OA(liste, 'mit_id', mitarbeiter,
##                                 'na', title="Mitarbeiter", session_key=session_key))
        return auszaehlungen


    def get_regional_auszaehlungen(self, liste, session_key):
        from ebkus.app.statistik import \
             WertAuszaehlung as WA, \
             RohWertAuszaehlung as RWA
        auszaehlungen = [Ueberschrift('Regionalstatistik')]
        app = auszaehlungen.append # Abkürzung
        #app(WA(liste, 'bz', title="Planungsraum", session_key=session_key))
        #app(RWA(liste, 'bz', title="Planungsraum", session_key=session_key))
        app(RWA(liste, 'plraum', title="Planungsraum", session_key=session_key))
        app(RWA(liste, 'ort', title="Ort", session_key=session_key))
        app(RWA(liste, 'plz', title="PLZ", session_key=session_key))
        for f in ('bezirk', 'ortsteil', 'samtgemeinde'):
            if f in config.STRASSENSUCHE:
                app(RWA(liste, f, title=f.capitalize(), session_key=session_key))
        return auszaehlungen

    def _get_kompatible_abfragen(self, liste, abfrage_list):
        # Hack um Teilmengendefs für die Teilmengenauszählung auszuschliessen,
        # wenn die entsprechende Liste gar nicht da ist:
        classes = []
        try:
            for e in liste[0]: # Liste von tupeln
                classes.append(e.__class__)
        except:
            classes.append(liste[0].__class__)
        for c in classes:
            assert c in (Fachstatistik, Jugendhilfestatistik2007, Jugendhilfestatistik)
        abfragen = []
        for a in abfrage_list:
            q = Query(a)
            if (q.fs or q.ort) and Fachstatistik not in classes:
                continue
            if q.jgh and Jugendhilfestatistik2007 not in classes:
                continue
            abfragen.append(a)
        return abfragen
    
    def get_teilmengen_auszaehlungen(self, liste, session_key, abfr_ids=None):
        from ebkus.app.statistik import FunktionsAuszaehlung as FA
        if abfr_ids:
            abfrage_list = [Abfrage(id) for id in abfr_ids]
        else:
            abfrage_list = AbfrageList(where='')
        abfrage_list = self._get_kompatible_abfragen(liste, abfrage_list)
        name_functions = [(a['name'], Query(a).test) for a in abfrage_list]
        return [Ueberschrift('Benutzerdefinierte Teilmengen'),
                FA(liste, name_functions, title="Benutzerdefinierte Teilmengen",
                   session_key=session_key)]

    def stat_ausgabe(self, res, liste, item_auswahl, anzeige_gg, query):
        """Ausgabe der Fachstatistik für die verschiedenen Abfragen.
        Parameter res ist eine Liste, an die HTML-Strings angehängt
        werden. Die Strings sind <tr>-Elemente.
        Die Auszählungsergebnisse, die textuelle Beschreibung der Abfrage (anzeige_gg) und
        das query-Objekt werden in der Session gespeichert, so dass
        sie für weitere Abfragen zur Verfügung stehen.
        """
        if not liste:
            raise EE("Keine Datensätze")
        auszaehlungen = []
        session_key = self.__class__.__name__
        liste0 = liste1 = None
        if isinstance(liste[0], tuple):
            liste0 = [el[0] for el in liste]
            liste1 = [el[1] for el in liste]
        listen = [l for l in (liste, liste0, liste1) if l]
        if 'teilmengen' in item_auswahl:
            auszaehlungen += self.get_teilmengen_auszaehlungen(listen[0], session_key)
        if 'regional' in item_auswahl:
            auszaehlungen += self.get_regional_auszaehlungen(
                liste0 and liste0 or liste, session_key)
        for list in listen:
            klass_name = list[0].__class__.__name__
            if 'fs_gesamt' in item_auswahl:
                if klass_name == 'Fachstatistik':
                    auszaehlungen += self.get_fachstatistik_auszaehlungen(list, session_key)
            if 'jgh_gesamt' in item_auswahl:
                if klass_name == 'Jugendhilfestatistik':
                    auszaehlungen += self.get_jgh_auszaehlungen(list, session_key)
                if klass_name == 'Jugendhilfestatistik2007':
                    auszaehlungen += self.get_jgh07_auszaehlungen(list, session_key)
##         if not plraum_tabelle:
##             # In der Regel das letzte Element löschen
##             del auszaehlungen[-1]
        self.session.data[session_key] = {} # alle früheren in der Session löschen
        self.session.data[session_key]['seq'] = [] # Liste mit auszählungen, so dass Ergebnisse in der 
                                              # richtigen Reihenfolge ausgegeben werden können
        # im session-Objekt ablegen
        seq = self.session.data[session_key]['seq']
        for a in auszaehlungen:
            if not isinstance(a, Ueberschrift):
                self.session.data[session_key][a.id] = a
            seq.append(a)
        # fuer die druckfreundliche Ausgabe
        self.session.data[session_key]['query'] = query
        self.session.data[session_key]['anzeige_gg'] = anzeige_gg
        self.session.data[session_key]['anzahl'] = len(liste)
        # siehe statistik_ergebnis.auszergebnis.add_tabelle
        taball_url = "newXX auszergebnis?typ=taball&session_key=%s" % (session_key,)
        csvall_url = "newXX auszergebnis?typ=csvall&session_key=%s" % (session_key,)
        menu = h.FieldsetInputTable(
            legend='Auswahlmenü',
            daten=[[h.SelectGoto(name='Auswahl',
                                 options='<option value="#top">- Gehe zu ...</option>\n' + '\n'.join([
                                '<option value="#%s">%s' % (a.identname, a.title)
                                for a in auszaehlungen])),
                    h.Button(value="Drucken",
                             tip="Druckfreundliche Ausgabe aller Tabellen",
                             onClick="go_to_url('%s')" % taball_url,
                             ),
                    h.Button(value="CSV-Datei",
                             tip="Alle Daten im CSV-Format für die Tabellenkalkulation exportieren",
                             onClick="go_to_url('%s')" % csvall_url,
                             ),
                    ]])
        res.append(menu.display())
        # Ergebnistabellen mit links auf Einzeltabelle und Chart hinzufügen
        for a in auszaehlungen:
            if isinstance(a, Ueberschrift):
                a.ueberschrift_einfuegen(res)
            else:
                erg = auszergebnis()
                erg.auszaehlung = a
                erg.add_tabelle(res)
        
    def get_grundgesamtheit(self, stz_list, von_jahr, bis_jahr, welche, klass, ohne_bk_raus):
        "Liefert alle FS bzw. JGH-Objekte (abhängig von klass) der"
        "angegebenen Stellen und Jahre."
        "Je nach dem Wert von 'welche' werden nur abgeschlossene, nur laufende oder alle Fälle genommen."
        "Statistiken mir fehlender fall_id werden immer zu den abgeschlossenen Fällen gezählt"
        "Wenn ohne_bk_raus True liefert, werden solche abgeschlossenen Fälle herausgenommen, "
        "die im Abschlussjahr keine Kontakte im Sinne der Bundesstatistik aufweisen."

        if klass == JugendhilfestatistikList:
            assert welche == 'abgeschlossenen'
        if klass in (JugendhilfestatistikList,):
            jahr = 'ey'
        # neue Bundesstatistik hat ein jahr-Feld, das für abgeschlossene Fälle
        # identisch sein muss mit ey (Endejahr der Hilfe)
        elif klass in (FachstatistikList, Jugendhilfestatistik2007List):
            jahr = 'jahr'
        else:
            raise EE('Interner Fehler in get_grundgesamtheit')
        stellen = ','.join(stz_list)
        where_fall = 'fall.zday %s 0 and ' % (welche=='laufend' and '=' or
                                              welche=='abgeschlossen' and '>' or
                                              welche=='alle' and '>='
                                              )
        where_kein_fall = "fall_id IS NULL and "
        where = """%(jahr)s  >= %(von_jahr)s and %(jahr)s  <= %(bis_jahr)s and 
        stz in ( %(stellen)s )""" % locals()
        ggl = klass(where=where_fall + where,
                    join=[('fall', '%s.fall_id=fall.id' % klass.resultClass.table)]
                    )
        if welche in ('alle', 'abgeschlossen') and ohne_bk_raus:
            ggl = [el for el in ggl if hatte_kontakt_im_abschlussjahr(el['fall'], el[jahr])]
        if welche in ('alle', 'abgeschlossen'):
            ggl += klass(where=where_kein_fall + where)
        return ggl
                     
    def get_grundgesamtheit_anzeige(self, stz_list, von_jahr, bis_jahr, welche,
                                    fs, jgh, jgh07, anzahl_gg, ohne_bk_raus):
        "Liefert ein Paar, z.B. "
        "Stelle A und Jahre 1999 - 2003, Alle Fälle mit Bundesstatistik (45 Klienten)"
        
        if welche in ('laufend', 'abgeschlossen'):
            suffix = 'e'
        else:
            suffix = ''
        welche_str = "%s%s Fälle" % (welche, suffix)
        if von_jahr == bis_jahr:
            jahr_str = 'Jahr %s' % bis_jahr
        else:
            jahr_str = 'Jahre %s - %s' % (von_jahr, bis_jahr)
        stellen = ', '.join([Code(s)['name'] for s in stz_list])
        if len(stz_list) == 1:
            stellen_str = 'Stelle %s' % stellen
        else:
            stellen_str = 'Stellen %s' % stellen
        bs = jgh and "(alter) Bundesstatistik" or jgh07 and "Bundesstatistik" or ''
        fs = fs and "Fachstatistik" or ''
        ohne_bk = ''
        if ohne_bk_raus:
            ohne_bk = " (keine abgeschlossene Fälle ohne Kontakt im Abschlussjahr)"
        res = ['%s und %s, %s%s' % (jahr_str, stellen_str, welche_str, ohne_bk)]
        # if ohne_bk_raus:
        #     res.append("Keine Fälle ohne Kontakt im Abschlussjahr")
        res.append("Alle Fälle mit %s (%s Klient%s)" %
                   (fs and bs and "%s und %s" % (fs, bs) or fs or bs,
                    anzahl_gg,
                    anzahl_gg > 1 and 'en' or '')
                   )
        return res

    def join_fs_jgh_list(self, fs_list, jgh_list):
        "Beide Listen müssen nicht geordnet sein."
        "Es wird eine Liste aus Paaren (fs, jgh) gebildet, mit je gleicher fall_id."
        "Enthalten ist nur die Schnittmenge zwischen beiden Listen."
        fs_dict = dict([(f['fall_fn'],f) for f in fs_list])
        jgh_dict = dict([(j['fall_fn'],j) for j in jgh_list])
        keys = sorted(jgh_dict.keys())
        res = [(fs_dict[k], jgh_dict[k]) for k in keys if fs_dict.has_key(k)]
        return res

class statergebnis(_statistik_ergebnis):
    "Ergebnisse der Fach- und Bundesstatistikauszählung"
    permissions = Request.ABFR_PERM

    def processForm(self, REQUEST, RESPONSE):
        #print 'FORM', self.form
        welche = self.form.get('w')
        ohne_bk_raus = self.form.get('ohne_bk_raus')
        von_jahr = self.form.get('von_jahr')
        bis_jahr = self.form.get('bis_jahr')
        if bis_jahr:
            bis_jahr = check_int_not_empty(self.form, 'bis_jahr', "Jahr fehlt")
        else:
            bis_jahr = today().year
        von_jahr = check_int_not_empty(self.form, 'von_jahr', "Jahr fehlt", bis_jahr)
        if von_jahr > bis_jahr:
            von_jahr = bis_jahr
        stz = check_list(self.form, 'stz', 'Keine Stelle')
        item_auswahl = check_list(self.form, 'item_auswahl', 'Bitte gewünschte Auszählung ankreuzen.')
        teilm = self.form.get('teilm')
        if teilm:
            abfr = Abfrage(teilm)
            query = Query(abfr)
        else:
            query = Query()
        fs, jgh, jgh07 = self.check_params(von_jahr, bis_jahr, stz, item_auswahl, query, welche)
        if fs:
            fs_ggl = self.get_grundgesamtheit(stz, von_jahr, bis_jahr, welche,
                                              FachstatistikList, ohne_bk_raus)
        if jgh:
            jgh_ggl = self.get_grundgesamtheit(stz, von_jahr, bis_jahr, welche,
                                               JugendhilfestatistikList, ohne_bk_raus)
        if jgh07:
            jgh_ggl = self.get_grundgesamtheit(stz, von_jahr, bis_jahr, welche,
                                               Jugendhilfestatistik2007List, ohne_bk_raus)
        if fs and (jgh or jgh07):
            # beide nötig: erzeugt wird eine Liste von Paaren (fs, jgh) für jeden Fall
            # für den beide Statistiken vorliegen
            ggl = self.join_fs_jgh_list(fs_ggl, jgh_ggl)
            #ggl = ggl*500  # Performance bei längeren Listen? ---> ok, 3sec bei 3000 Fälle
            #ggl = ggl*5000 # Performance bei längeren Listen? ---> ok, 26sec bei 30000 Fälle
        elif fs:
            ggl = fs_ggl
        else:
            ggl = jgh_ggl
        anzeige_gg = self.get_grundgesamtheit_anzeige(stz, von_jahr, bis_jahr, welche,
                                                      fs, jgh, jgh07, len(ggl), ohne_bk_raus)
        
        if not ggl:
            raise EE("Keine Datensätze für die gewünschte Grundgesamtheit:"
                     "\n\n%s\n und %s" % (anzeige_gg[0], anzeige_gg[1]))
        if query.always_true():
            ggl_teilm = ggl
        else:
            def qfilter(el):
                return query.test(el)
            #ggl_teilm = ggl.filter(qfilter)
            ggl_teilm = [el for el in ggl if(qfilter(el))]
            if not ggl_teilm:
                raise EE("Keine Datensätze für Teilmenge '%s'" % abfr['name'])
        return self._display_ergebnis(
            ggl_teilm,
            anzeige_gg=anzeige_gg,
            query=query,
            item_auswahl=item_auswahl,
            )

    def check_params(self, von_jahr, bis_jahr, stz, item_auswahl, query, welche):
        assert item_auswahl and von_jahr and bis_jahr and query and stz
        fs = jgh = jgh07 = False
        for k in ('fs_gesamt', 'regional', 'teilmengen'):
            if k in item_auswahl:
                fs = True
                break
        if von_jahr >= 2007 and 'teilmengen' in item_auswahl:
            # Damit kann man Teilmengen alleine auszählen,
            # ohne BS oder FS anzukreuzen
            jgh07 = True
        if query.fs or query.ort:
            fs = True
        if query.jgh:
            jgh07 = True
        if 'jgh_gesamt' in item_auswahl and von_jahr < 2007:
            jgh = True
        if 'jgh_gesamt' in item_auswahl and bis_jahr >= 2007:
            jgh07 = True
        if query.jgh and von_jahr < 2007:
            raise EE("Statistik vor 2007 nicht möglich mit Teilmenge '%s'" % query.name)
        if von_jahr < 2007 and bis_jahr >= 2007 and 'jgh_gesamt' in item_auswahl:
            raise EE("Bundesstatistik entweder nur bis 2006 oder ab 2007 möglich")
        if welche in ('laufend', 'alle') and von_jahr != bis_jahr:
            raise EE("Auswertung über mehrere Jahre hinweg nur für abgeschlossene Fälle möglich.")
        if welche in ('laufend', 'alle') and jgh:
            raise EE("Auswertung von laufenden Fällen für alte Bundesstatistik nicht möglich.")
        assert not (jgh and jgh07)
        assert fs or jgh or jgh07
        return fs, jgh, jgh07

    def _display_ergebnis(self,
                          liste,
                          anzeige_gg,
                          query,
                          item_auswahl,
                          ):
        menu = h.FieldsetInputTable(
            daten=[[h.Button(value="Hauptmenü",
                             tip="Zum Hauptmenü",
                             onClick="go_to_url('menu')",
                             ),
                    h.Button(value="Statistikabfrage",
                             tip="Zur Statistikabfrage",
                             onClick="go_to_url('statabfr')",
                             ),
                    ]])
        res = []
        self.stat_ausgabe(res, liste, item_auswahl, anzeige_gg, query)
        tabellen = ''.join(res)
        res = h.FormPage(
            title='Statistikauszählung',
            name="statform",action="statergebnis",method="post",
            breadcrumbs = (('Hauptmenü', 'menu'),
                           ('Statistikabfrage', 'statabfr'),
                           ),
            hidden = (),
            rows=(menu,
                  get_abfrage(anzeige_gg, query, len(liste)),
                  tabellen,
                  ),
            )
        return res.display()


# als Funktion herausgezogen, damit das auch von in statistik_ergebnis 
# für druckerfreundliche Ausgabe genutzt werden kann
def get_abfrage(anzeige_gg, query, anzahl, cls=None):
    if not cls:
        cls = h.FieldsetDataTable
    abfrage = cls(
        legend = 'Abfrage',
        daten=[[h.String(string="Grundgesamtheit:",
                         align='right',
                         class_='tabledatabold',
                         ),
                h.String(string=anzeige_gg[0],
                         class_='tabledata',
                         ),
                ],
               [h.String(string="",
                         align='right',
                         class_='tabledatabold',
                         ),
                h.String(string=anzeige_gg[1],
                         class_='tabledata',
                         ),
                ]] 
        + ((len(anzeige_gg) > 2) and 
                [[h.String(string="",
                           align='right',
                           class_='tabledatabold',
                           ),
                  h.String(string=anzeige_gg[2],
                           class_='tabledata',
                           ),
          ]] or [])
        + (not query.always_true() and
                [[h.String(string="Teilmenge:",
                          align='right',
                          class_='tabledatabold',
                          ),
                 h.String(string="%s (%s Klient%s)" % (query.name, anzahl,
                                                       anzahl > 1 and 'en' or ''),
                          class_='tabledata',
                         ),
                 ],
                [h.String(string="Teilmengendefinition:",
                          align='right',
                          class_='tabledatabold',
                          ),
                 h.String(string=query.get_anzeige(),
                          class_='tabledata',
                          ),
                 ]] or [])
        )
    return abfrage
