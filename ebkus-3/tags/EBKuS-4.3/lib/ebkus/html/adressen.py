# coding: latin-1
"""Module für den Adressenexport."""

import re
import csv
import os
import sha
from ebkus.db.sql import escape
from ebkus.app import Request
from ebkus.app.ebapi import FeldList, EE, check_list, SQL, \
     today, cc, check_int_not_empty, \
     check_str_not_empty, EBUpdateDataError, getQuartal, get_rm_datum, Date, \
     Fall, FallList, FallGruppe, BezugspersonGruppe, \
     FallGruppeList, BezugspersonGruppeList, \
     Gruppe, Akte, Bezugsperson

from ebkus.app_surface.strkat_templates import *
from ebkus.config import config

import ebkus.html.htmlgen as h
from ebkus.html.akte_share import akte_share 


class Adresse(dict):
    def __getattr__(self, key): 
        try: 
            return self[key]
        except KeyError, k: 
            return None
    def __setattr__(self, key, value): 
        self[key] = value
    def __delattr__(self, key):
        try: 
            del self[key]
        except KeyError, k: 
            raise AttributeError, k
    def felder(self):
        return self._felder
    def items(self):
        return [(f, self[f]) for f in self.felder()]
    def __init__(self, **kw):
        felder = self.felder()
        for k,v in kw.items():
            if k not in self.felder():
                raise KeyError, k
            self[k] = v
        self.set_key()
    def set_key(self):
        self.key = sha.new(self.rolle+self.fallnummer+(self.gruppennummer or '')+
                           self.vorname+self.nachname).hexdigest()
class GruppeAddresse(Adresse):
    _felder = (
        'key',
        'teilnehmer',
        'rolle',
        'fallnummer',
        'gruppennummer',
        'gruppenname',
        'gruppenbeginn',
        'gruppenende',
        'mitarbeiter',
        'anrede',
        'vorname',
        'nachname',
        'strasse',
        'hausnummer',
        'plz',
        'ort',
        'planungsraum',
        )

class FallAddresse(Adresse):
    _felder = (
        'key',
        'rolle',
        'mitarbeiter',
        'fallnummer',
        'fallbeginn',
        'fallabschluss',
        'anrede',
        'vorname',
        'nachname',
        'strasse',
        'hausnummer',
        'plz',
        'ort',
        'planungsraum',
        )


from ebkus.html.abfragen import fall_abfrage
class adressen(fall_abfrage):
    permissions = Request.ABFR_PERM
    def processForm(self, REQUEST, RESPONSE):
        #print 'ADRESSEN FORM:', self.form
        welche = check_str_not_empty(self.form, 'wel', "Keine Exportart", 'keine')
        if welche == 'gruppe':
            return self._process_gruppe(REQUEST, RESPONSE)
        elif welche == 'fall':
            return self._process_fall(REQUEST, RESPONSE)
        else:
            return 'Keine Auswahl'

    def _get_adresse_gruppe(self, teilnehmer, rolle, 
                            fall, gruppe, adresse):

        assert isinstance(teilnehmer, basestring)
        assert isinstance(rolle, basestring)
        assert isinstance(fall, Fall)
        assert isinstance(gruppe, Gruppe)
        assert isinstance(adresse, (Akte, Bezugsperson))
        gruppenende = gruppe.getDate('e')
        if gruppenende.is_zero():
            gruppenende = ''
        return GruppeAddresse(
            teilnehmer=teilnehmer,
            rolle=rolle,
            fallnummer=fall['fn'], # muss index 3 haben !!!
            gruppennummer=gruppe['gn'],
            gruppenname=gruppe['name'],
            gruppenbeginn=gruppe.getDate('bg'),
            gruppenende=gruppenende,
            mitarbeiter=gruppe['mitarbeiternamen'],
            anrede=adresse['gs__code']=='1' and 'Herr' or 'Frau',
            vorname=adresse['vn'],
            nachname=adresse['na'],
            strasse=adresse['str'],
            hausnummer=adresse['hsnr'],
            plz=adresse['plz'],
            ort=adresse['ort'],
            planungsraum=adresse.get('plraum') or '',
            )


    def _get_gruppen_adressen_pro_fall(self, fall, gruppe):
        """Liefert Liste von Adressen des Klienten und jeder Bezugsperson
        für einen gegebenen Fall. Die Gruppendaten werden ebenfalls
        eingefügt. teilnehmer ist immer 'nein', muss später eingefügt werden.
        """
        # TODO letzte Zuständigkeit noch mit rein, evt. Mitarbeiter der Gruppe
        res = []
        # Klient
        assert isinstance(fall, Fall)
        akte = fall['akte']
        assert isinstance(akte, Akte)
        # Adresse des teilnehmenden Klienten
        res1 = self._get_adresse_gruppe(
                teilnehmer='nein', 
                rolle='Klient', 
                fall=fall,
                gruppe=gruppe, 
                adresse=akte,
                )
        #print 'RES1', res1
        res.append(res1)
        # Adressen der Bezugspersonen
        for bezugsperson in akte['bezugspersonen']:
            res.append(self._get_adresse_gruppe(
                    teilnehmer='nein', 
                    rolle=bezugsperson['verw__name'], 
                    fall=fall,
                    gruppe=gruppe, 
                    adresse=bezugsperson,
                    ))
        return res

    def _get_adresse_fall(self, rolle, fall, adresse):
        assert isinstance(rolle, basestring)
        assert isinstance(fall, Fall)
        assert isinstance(adresse, (Akte, Bezugsperson))
        fallabschluss = fall.getDate('zda')
        if fallabschluss.is_zero():
            fallabschluss = ''
        return FallAddresse(
            rolle=rolle,
            mitarbeiter=fall['zuletzt_zustaendig__mit__na'],
            fallnummer=fall['fn'],
            fallbeginn=fall.getDate('bg'),
            fallabschluss=fallabschluss,
            anrede=adresse['gs__code']=='1' and 'Herr' or 'Frau',
            vorname=adresse['vn'],
            nachname=adresse['na'],
            strasse=adresse['str'],
            hausnummer=adresse['hsnr'],
            plz=adresse['plz'],
            ort=adresse['ort'],
            planungsraum=adresse.get('plraum') or '',
            )
    def _get_adressen_pro_fall(self, fall):
        # TODO letzte Zuständigkeit noch mit rein
        assert isinstance(fall, Fall)
        akte = fall['akte']
        rolle = 'Klient'
        res = [self._get_adresse_fall(rolle, fall, akte)]
        for bp in akte['bezugspersonen']:
            rolle = bp['verw__name']
            res.append(self._get_adresse_fall(rolle, fall, bp))
        return res

    def _get_gruppe_address_data(self, gruppen_ids):
        """Eine dict pro Adresse. Mehrere dicts pro Teilnehmer.
        Zuerst die dict des Teilnehmers selber, dann der Klient, 
        falls nicht selber Teilnehmer, dann die übrigen 
        Bezugspersonen.
        """
        res = []
        for gruppe_id in gruppen_ids:
            # innerhalb einer Gruppe die Adressen eines Falles
            # nur einmal anzeigen
            res += self._get_gruppe_address_data_for_one(gruppe_id)
        return res
    def _get_gruppe_address_data_for_one(self, gruppe_id):
        """Eine dict pro Adresse. Mehrere dicts pro Teilnehmer.
        Zuerst die dict des Teilnehmers selber, dann der Klient, 
        falls nicht selber Teilnehmer, dann die übrigen 
        Bezugspersonen.
        """
        res = []
        gruppe = Gruppe(gruppe_id)
        # innerhalb einer Gruppe die Adressen eines Falles
        # nur einmal anzeigen
        fn2fall = {}
        teilnehmer = {}
        kl_teilnehmer = FallGruppeList(
            where='gruppe_id=%s' % gruppe_id)
        bp_teilnehmer = BezugspersonGruppeList(
            where='gruppe_id=%s' % gruppe_id)
        # alle beteiligte Fälle ermitteln
        for kl in kl_teilnehmer:
            fall = kl['fall']
            fn = fall['fn']
            fn2fall[fn] = fall
            key = GruppeAddresse(rolle='Klient',
                                 fallnummer=fn,
                                 vorname=fall['akte__vn'],
                                 nachname=fall['akte__na'],
                                 ).key
            teilnehmer[key] = True
        for bpg in bp_teilnehmer:
            bp = bpg['bezugsp']            
            akte = bp['akte']
            fall =  akte['letzter_fall']
            fn = fall['fn']
            fn2fall[fn] = fall
            key = GruppeAddresse(rolle=bp['verw__name'],
                                 fallnummer=fn,
                                 vorname=bp['vn'],
                                 nachname=bp['na'],
                                 ).key
            teilnehmer[key] = True
        faelle = FallList(fn2fall.values())
        faelle.sort('bgy', 'bgm', 'bgd')
        for fall in faelle:
            ag = self._get_gruppen_adressen_pro_fall(fall, gruppe)
            for a in ag:
                if a.key in teilnehmer:
                    a.teilnehmer = 'ja'
            res += ag
        return res

    def _get_fall_address_data(self, faelle):
        """Eine dict pro Adresse. Mehrere dicts pro Teilnehmer.
        Zuerst die dict des Teilnehmers selber, dann der Klient, 
        falls nicht selber Teilnehmer, dann die übrigen 
        Bezugspersonen.
        """
        res = []
        for f in faelle:
            a = self._get_adressen_pro_fall(f)
            #print 'ADRESSE', a
            res += a
        return res

    def _get_address_list(self, adressen):
        if not adressen:
            return None
        a0 = adressen[0]
        felder = a0.felder()[1:]
        #n_col = 2 + len(a0[1:])
        n_col = 2 + len(felder)
        #felder = [t[0] for t in a0[1:]]
        daten_before_headers = [
            [h.String(string="Felder:",
                      n_col=3,
                      ),
             h.String(string=' '.join(felder),
                      n_col=n_col-3,
                      tip="Felder in der Reihenfolge, in der sie in der Tabelle stehen",
                      ),
             ],
            [h.Dummy(n_col=n_col),],
            [h.Dummy(n_col=n_col),],
            ]
        header = ['<span title="%s">'%t[0] + t[0][:3] + '</span>' 
                  #for t in adressen[0][1:]]
                  for t in felder]
        data = []
        fallnummer = None
        # Adressen, die zu einem Fall gehören werden farblich gruppiert.
        # In der Regel wird nur eine Adress aus der Gruppe benötigt.
        fallfarben = ['tabledatajaune', 'tabledatableu']
        ff_index = 1
        for a in adressen:
            old_fallnummer = fallnummer
            #fallnummer = a[3][1]
            fallnummer = a.fallnummer
            ff_index = (ff_index + (old_fallnummer != fallnummer)) % 2
            class_ = fallfarben[ff_index]
            #print 'ADRESSE', a
            zeile = [h.CheckItem(name='adr',
                                 #value=a[0][1],
                                 value=a.key,
                                 tip='Diese Zeile behalten bzw. entfernen',
                                 )
                     ]
            zeile += [h.String(string=a[f],
                              tip=f,
                              class_=class_) for f in felder]
            #print 'ZEILE', zeile
            data.append(zeile)
        adress_list = h.FieldsetDataTable(
            legend='Adressen auswählen und als CSV-Datei herunterladen',
            daten_before_headers=daten_before_headers,
            #headers=header,
            noheaders=2,
            daten=data,
            buttons_left=True,
            buttons=[h.Button(value="Markierte behalten",
                             name='submitop',
                             tip="Nur angekreuzte Adressen behalten",
                             type='submit',
                              class_='buttonbig',
                             ),
                    h.Button(value="Markierte entfernen",
                             name='submitop',
                             tip="Angekreuzte Adressen entfernen",
                             type='submit',
                              class_='buttonbig',
                             ),
                    h.Button(value="Herunterladen",
                             name='submitop',
                             tip="Alle angezeigten Adressen als CSV-Datei herunterladen",
                             type='submit',
                             ),
                    ],
            )
        return adress_list

    def send_csv(self, adressen, RESPONSE):
        content = self.csv_gen(adressen)
        self.RESPONSE.setHeader('content-type', "text/csv; charset=iso-8859-1")
        self.RESPONSE.setHeader('content-disposition',
                                'attachment; filename=%s' % 'adressen.csv')
        self.RESPONSE.setBody(content)
        return
    def csv_gen(self, adressen):
        import cStringIO
        out = cStringIO.StringIO()
        writer = csv.writer(out,
                            delimiter=';',
                            doublequote=True,
                            quotechar='"',
                            lineterminator='\r\n',
                            )
        
        # erstes Feld 'key' weglassen
        felder = adressen[0].felder()[1:]
        writer.writerow(felder)
        rows = []
        for a in adressen:
            vals = [a[f] for f in felder]
            rows.append(vals)
        writer.writerows(rows)
        return out.getvalue()
        
    def _process_gruppe(self, REQUEST, RESPONSE):
        submitop = self.form.get('submitop')
        adr = check_list(self.form, 'adr', 'Keine Auswahl', [])
        #gruppen_ids = [1]
        gruppen_ids = check_list(self.form, 'grid', 
                                 'Keine Gruppe ausgewählt', [])
        if gruppen_ids:
            # Duplikate entfernen, absteigend sortieren
            gruppen_ids = [int(g) for g in gruppen_ids]
            id_dict = dict([(id, True) for id in gruppen_ids])
            gruppen_ids = id_dict.keys()
            gruppen_ids.sort()
            gruppen_ids.reverse()
        
        #print 'GRUPPEN_IDS:', gruppen_ids
        adressen = []
        if submitop == 'Anzeigen':
            if gruppen_ids:
                adressen = self._get_gruppe_address_data(gruppen_ids)
                if not adressen:
                    raise EE('Keine Adressen für gewählte Gruppe(n) vorhanden.')
                self.session.data['gruppenadressen'] = adressen
            else:
                raise EE('Keine Gruppe ausgewählt!')
        elif submitop:
            adressen = self.session.data.get('gruppenadressen')
            if not adressen:
                raise EE('Keine Adressen, bitte neu anzeigen lassen!')
            if submitop == 'Markierte behalten':
                #adressen = [a for a in adressen if a[0][1] in adr]
                adressen = [a for a in adressen if a.key in adr]
                self.session.data['gruppenadressen'] = adressen
            elif submitop == 'Markierte entfernen':
                #adressen = [a for a in adressen if a[0][1] not in adr]
                adressen = [a for a in adressen if a.key not in adr]
                self.session.data['gruppenadressen'] = adressen
            elif submitop == 'Herunterladen':
                return self.send_csv(adressen, RESPONSE)
            else:
                raise EE('Fehler: Unbekannter Submit-Button')
        anzeige = h.FieldsetInputTable(
            legend='Gruppenauswahl für anzuzeigende Adressen',
            daten=[
                   [h.SelectItem(name='grid',
                                 size="6",
                                 class_="listbox280",
                                 tip="Alle Gruppen, für die Sie Zugriffsrechte haben",
                                 options=self.for_gruppen(sel=gruppen_ids),
                                 sel=gruppen_ids,
                                 multiple=True,
                                 #n_col=4,
                                 nolabel=True,
                                 ),
                    ],
                ],
            button=h.Button(value="Anzeigen",
                     name='submitop',
                     tip="Alle Adressen der gewählten Gruppen anzeigen",
                     type='submit',
                     ),
            )

        #hidden = tuple([('grid', id) for id in gruppen_ids])
        hidden = (('wel', 'gruppe'),)
        #print 'HIDDEN', hidden
        res = h.FormPage(
            title='Adressenexport',
            name="adr",action="adressen",method="post",
            breadcrumbs = (('Hauptmenü', 'menu'),
                           ),
            hidden=hidden,
            rows=(self.get_auswertungs_menu(gruppenmenu=True),
                  anzeige,
                  self._get_address_list(adressen),
                  ),
            )
        return res.display()


    def _process_fall(self, REQUEST, RESPONSE):
        submitop = self.form.get('submitop')
        adr = check_list(self.form, 'adr', 'Keine Auswahl', [])
        params = self.fall_auswahl_form()

        welche_faelle = params['welche']
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



        adressen = []
        if submitop == 'Anzeigen':
            beratungen = self.beratungen(welche=welche_faelle,
                                         stelle=self.stelle,
                                         mitarbeiter=mitarbeiter,
                                         ab_jahr=ab_jahr,
                                         ab_fallnummer=ab_fallnummer,
                                         bis_jahr=bis_jahr,
                                         bis_fallnummer=bis_fallnummer,
                                         ab_jahr_zda=ab_jahr_zda,
                                         bis_jahr_zda=bis_jahr_zda,
                                         sort=sort)

            #print 'BERATUNGEN', beratungen
            if beratungen:
                adressen = self._get_fall_address_data(beratungen)
                #print 'ADRESSEN', adressen
                if not adressen:
                    raise EE('Keine Adressen für gewählte Fälle vorhanden.')
                self.session.data['falladressen'] = adressen
            else:
                raise EE('Keine Fälle in der Auswahl!')
        elif submitop:
            adressen = self.session.data.get('falladressen')
            if not adressen:
                raise EE('Keine Adressen, bitte neu anzeigen lassen!')
            if submitop == 'Markierte behalten':
                adressen = [a for a in adressen if a.key in adr]
                #adressen = [a for a in adressen if a[0][1] in adr]
                self.session.data['falladressen'] = adressen
            elif submitop == 'Markierte entfernen':
                adressen = [a for a in adressen if a.key not in adr]
                #adressen = [a for a in adressen if a[0][1] not in adr]
                self.session.data['falladressen'] = adressen
            elif submitop == 'Herunterladen':
                return self.send_csv(adressen, RESPONSE)
            else:
                raise EE('Fehler: Unbekannter Submit-Button')

        anzeige = self.get_fall_auswahl('Fallauswahl für anzuzeigende Adressen', welche_faelle, 
                                        ab_jahr, ab_fallnummer, 
                                        bis_jahr, bis_fallnummer, 
                                        ab_jahr_zda, bis_jahr_zda,
                                        mitarbeiter, 
                                        sort_options_data, sort_sel,
                                        submitop='submitop',
                                        )


        hidden = (('wel', 'fall'),)
        res = h.FormPage(
            title='Adressenexport',
            name="adr",action="adressen",method="post",
            breadcrumbs = (('Hauptmenü', 'menu'),
                           ),
            hidden=hidden,
            rows=(self.get_auswertungs_menu(),
                  anzeige,
                  self._get_address_list(adressen),
                  ),
            )
        return res.display()

