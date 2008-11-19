# coding: latin-1
"""Module f�r den Adressenexport."""

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


# parms: 
# w: fall gruppe keine
# gruppeid: <gruppen_id> (adressen der Gruppe zur Auswahl anbieten)
# adr: (gew�hlte Adressen als csv downloaden)

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
        self.key = sha.new(self.rolle+self.fallnummer+
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
        print 'ADRESSEN FORM:', self.form
        welche = check_str_not_empty(self.form, 'wel', "Keine Exportart", 'keine')
        if welche == 'gruppe':
            return self._process_gruppe(REQUEST, RESPONSE)
        elif welche == 'fall':
            return self._process_fall(REQUEST, RESPONSE)
        else:
            return 'Keine Auswahl'



#     def x_get_adressen_pro_gruppenteilnehmer(self, obj):
#         # TODO letzte Zust�ndigkeit noch mit rein
#         if isinstance(obj, FallGruppe):
#             gruppe = obj['gruppe']
#             fall =  obj['fall']
#             key = "FallGruppe_%(id)s" % obj
#             res = [[
#                 ('key', key),
#                 ('teilnehmer', 'ja'),
#                 ('rolle', 'Klient'),
#                 ('fallnummer', fall['fn']),
#                 ('gruppennummer', gruppe['gn']),
#                 ('gruppenname', gruppe['name']),
#                 ('gruppenbeginn', gruppe.getDate('bg')),
#                 ('gruppenende', gruppe.getDate('e')),
#                 ('anrede', obj['fall__akte__gs__code']=='1' and 'Herr' or 'Frau'),
#                 ('vorname', obj['fall__akte__vn']),
#                 ('nachname', obj['fall__akte__na']),
#                 ('strasse', obj['fall__akte__str']),
#                 ('hausnummer', obj['fall__akte__hsnr']),
#                 ('plz', obj['fall__akte__plz']),
#                 ('ort', obj['fall__akte__ort']),
#                 ('planungsraum', obj['fall__akte__plraum']),
#                 ]]
#             bezugspersonen = obj['fall__akte__bezugspersonen']
#             for obj in bezugspersonen:
#                 key = "Bezugsperson_%(id)s" % obj
#                 res.append([
#                 ('key', key),
#                 ('teilnehmer', 'nein'),
#                 ('rolle', obj['verw__name']),
#                 ('fallnummer', fall['fn']),
#                 ('gruppennummer', gruppe['gn']),
#                 ('gruppenname', gruppe['name']),
#                 ('gruppenbeginn', gruppe.getDate('bg')),
#                 ('gruppenende', gruppe.getDate('e')),
#                 ('anrede', obj['gs__code']=='1' and 'Herr' or 'Frau'),
#                 ('vorname', obj['vn']),
#                 ('nachname', obj['na']),
#                 ('strasse', obj['str']),
#                 ('hausnummer', obj['hsnr']),
#                 ('plz', obj['plz']),
#                 ('ort', obj['ort']),
#                 ('planungsraum', ''), # TODO
#                 ])
#         elif isinstance(obj, BezugspersonGruppe):
#             pass
#         return res


    def _merge_gruppe_adresse(self, prev, adressen):
        """
        prev und adressen sind jeweils die zu einem Fall
        geh�renden Adressen, wobei jeweils eine Adresse als 
        Teilnehmer an der Gruppe gekennzeichnet ist, z.B.
        zwei verschiedene Bezugspersonen vom selben Fall,
        oder der Klient selbst und eine Bezugsperson.
        
        Es soll eine Liste von Adressen geliefert werden, in 
        der mehrere Adressen als teilnehmen gekennzeichnet sind.
        """
        assert len(prev) == len(adressen)
        adressen_teilnehmer = [a for a in adressen if a.teilnehmer == 'ja']
        for p in prev:
            for a in adressen_teilnehmer:
                if p.key == a.key:
                    p.teilnehmer = 'ja'

#     def _get_adresse_gruppe(self, key, teilnehmer, rolle, 
#                             fall, gruppe, adresse):


#         assert isinstance(key, basestring)
#         assert isinstance(teilnehmer, basestring)
#         assert isinstance(rolle, basestring)
#         assert isinstance(fall, Fall)
#         assert isinstance(gruppe, Gruppe)
#         assert isinstance(adresse, (Akte, Bezugsperson))
#         return [
#             ('key', key),
#             ('teilnehmer', teilnehmer),
#             ('rolle', rolle),
#             ('fallnummer', fall['fn']), # muss index 3 haben !!!
#             ('gruppennummer', gruppe['gn']),
#             ('gruppenname', gruppe['name']),
#             ('gruppenbeginn', gruppe.getDate('bg')),
#             ('gruppenende', gruppe.getDate('e')),
#             ('anrede', adresse['gs__code']=='1' and 'Herr' or 'Frau'),
#             ('vorname', adresse['vn']),
#             ('nachname', adresse['na']),
#             ('strasse', adresse['str']),
#             ('hausnummer', adresse['hsnr']),
#             ('plz', adresse['plz']),
#             ('ort', adresse['ort']),
#             ('planungsraum', adresse.get('plraum') or ''),
#             ]
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

    def _get_adressen_pro_gruppenteilnehmer(self, obj):
        # TODO letzte Zust�ndigkeit noch mit rein, evt. Mitarbeiter der Gruppe
        res = []
        if isinstance(obj, FallGruppe):
            # Klient ist Teilnehmer
            fallgruppe = obj
            assert isinstance(fallgruppe, FallGruppe)
            gruppe = fallgruppe['gruppe']
            assert isinstance(gruppe, Gruppe)
            fall =  fallgruppe['fall']
            assert isinstance(fall, Fall)
            akte = fall['akte']
            assert isinstance(akte, Akte)
            # Adresse des teilnehmenden Klienten
            res1 = self._get_adresse_gruppe(
                    teilnehmer='ja', 
                    rolle='Klient', 
                    fall=fall,
                    gruppe=gruppe, 
                    adresse=akte,
                    )
            #print 'RES1', res1
            res.append(res1)
            # Adresse der Bezugspersonen
            for bezugsperson in akte['bezugspersonen']:
                res.append(self._get_adresse_gruppe(
                        teilnehmer='nein', 
                        rolle=bezugsperson['verw__name'], 
                        fall=fall,
                        gruppe=gruppe, 
                        adresse=bezugsperson,
                        ))
        elif isinstance(obj, BezugspersonGruppe):
            # Bezugsperson ist Teilnehmer
            bezugspersongruppe = obj
            gruppe = bezugspersongruppe['gruppe']
            teilnehmer_bezugsperson = bezugspersongruppe['bezugsp']
            akte = teilnehmer_bezugsperson['akte']
            fall =  akte['letzter_fall']
            bezugspersonen = [b for b in akte['bezugspersonen']
                              if not b == teilnehmer_bezugsperson]
            # Adresse der teilnehmenden Bezugsperson
            res.append(self._get_adresse_gruppe(
                    teilnehmer='ja', 
                    rolle=teilnehmer_bezugsperson['verw__name'], 
                    fall=fall,
                    gruppe=gruppe, 
                    adresse=teilnehmer_bezugsperson,
                    ))
            # Adresse des nicht-teilnehmenden Klienten
            res.append(self._get_adresse_gruppe(
                    teilnehmer='nein', 
                    rolle='Klient',
                    fall=fall,
                    gruppe=gruppe, 
                    adresse=akte,
                    ))
            # Adressen der �brigen Bezugspersonen
            for bezugsperson in bezugspersonen:
                res.append(self._get_adresse_gruppe(
                        teilnehmer='nein', 
                        rolle=bezugsperson['verw__name'], 
                        fall=fall,
                        gruppe=gruppe, 
                        adresse=bezugsperson,
                        ))
        #print 'RES _GET_ADRESSEN_PRO_GRUPPENTEILNEHMER', res
        return res

    def _get_gruppen_adressen_pro_fall(self, fall, gruppe):
        """Liefert Liste von Adressen des Klienten und jeder Bezugsperson
        f�r einen gegebenen Fall. Die Gruppendaten werden ebenfalls
        eingef�gt. teilnehmer ist immer 'nein', muss sp�ter eingef�gt werden.
        """
        # TODO letzte Zust�ndigkeit noch mit rein, evt. Mitarbeiter der Gruppe
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

#     def _get_adressen_pro_fall(self, obj):
#         # TODO letzte Zust�ndigkeit noch mit rein
#         assert isinstance(obj, Fall)
#         fall = obj
#         key = "Fall_%(id)s" % obj
#         res = [[
#             ('key', key),
#             ('rolle', 'Klient'),
#             ('mitarbeiter', fall['zuletzt_zustaendig__mit__na']),
#             ('fallnummer', fall['fn']),
#             ('fallbeginn', fall.getDate('bg')),
#             ('fallabschluss', fall.getDate('zda')),
#             ('anrede', fall['akte__gs__code']=='1' and 'Herr' or 'Frau'),
#             ('vorname', fall['akte__vn']),
#             ('nachname', fall['akte__na']),
#             ('strasse', fall['akte__str']),
#             ('hausnummer', fall['akte__hsnr']),
#             ('plz', fall['akte__plz']),
#             ('ort', fall['akte__ort']),
#             ('planungsraum', fall['akte__plraum']),
#             ]]
#         bezugspersonen = fall['akte__bezugspersonen']
#         for obj in bezugspersonen:
#             key = "Bezugsperson_%(id)s" % obj
#             res.append([
#             ('key', key),
#             ('rolle', obj['verw__name']),
#             ('mitarbeiter', fall['zuletzt_zustaendig__mit__na']),
#             ('fallnummer', fall['fn']),
#             ('fallbeginn', fall.getDate('bg')),
#             ('fallabschluss', fall.getDate('zda')),
#             ('anrede', obj['gs__code']=='1' and 'Herr' or 'Frau'),
#             ('vorname', obj['vn']),
#             ('nachname', obj['na']),
#             ('strasse', obj['str']),
#             ('hausnummer', obj['hsnr']),
#             ('plz', obj['plz']),
#             ('ort', obj['ort']),
#             ('planungsraum', ''),
#             ])
#         return res
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
        # TODO letzte Zust�ndigkeit noch mit rein
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
        falls nicht selber Teilnehmer, dann die �brigen 
        Bezugspersonen.
        """
        res = []
        for gruppe_id in gruppen_ids:
            # innerhalb einer Gruppe die Adressen eines Falles
            # nur einmal anzeigen
            res += self._get_gruppe_address_data_for_one(gruppe_id)
        return res
#     def _get_gruppe_address_data_for_one(self, gruppe_id):
#         """Eine dict pro Adresse. Mehrere dicts pro Teilnehmer.
#         Zuerst die dict des Teilnehmers selber, dann der Klient, 
#         falls nicht selber Teilnehmer, dann die �brigen 
#         Bezugspersonen.
#         """
#         res = []
#         # innerhalb einer Gruppe die Adressen eines Falles
#         # nur einmal anzeigen
#         fn2fall = {}
#         fn2adressen = {}
#         kl_teilnehmer = FallGruppeList(
#             where='gruppe_id=%s' % gruppe_id)
#         bp_teilnehmer = BezugspersonGruppeList(
#             where='gruppe_id=%s' % gruppe_id)
#         for kl in kl_teilnehmer:
#             ag = self._get_adressen_pro_gruppenteilnehmer(kl)
#             print 'ADRESSE', ag
#             fn = ag[0].fallnummer
#             prev = fn2adressen.get(fn)
#             if prev:
#                 # addressen vom selben Fall
#                 self._merge_gruppe_adresse(prev, ag)
#             else:
#                 fn2adressen[fn] = ag
#                 res += ag
#         for bp in bp_teilnehmer:
#             ag = self._get_adressen_pro_gruppenteilnehmer(bp)
#             print 'ADRESSE', ag
#             fn = ag[0].fallnummer
#             prev = fn2adressen.get(fn)
#             if prev:
#                 # addressen vom selben Fall
#                 self._merge_gruppe_adresse(prev, ag)
#             else:
#                 fn2adressen[fn] = ag
#                 res += ag
#             res += ag
#         return res

    def _get_gruppe_address_data_for_one(self, gruppe_id):
        """Eine dict pro Adresse. Mehrere dicts pro Teilnehmer.
        Zuerst die dict des Teilnehmers selber, dann der Klient, 
        falls nicht selber Teilnehmer, dann die �brigen 
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
        # alle beteiligte F�lle ermitteln
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
        falls nicht selber Teilnehmer, dann die �brigen 
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
        # Adressen, die zu einem Fall geh�ren werden farblich gruppiert.
        # In der Regel wird nur eine Adress aus der Gruppe ben�tigt.
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
#             zeile += [h.String(string=t[1],
#                               tip=t[0],
#                               class_=class_) for t in a[1:]]
            zeile += [h.String(string=a[f],
                              tip=f,
                              class_=class_) for f in felder]
            #print 'ZEILE', zeile
            data.append(zeile)
        adress_list = h.FieldsetDataTable(
            legend='Adressen ausw�hlen und als CSV-Datei herunterladen',
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
                                 'Keine Gruppe ausgew�hlt', [])
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
                    raise EE('Keine Adressen f�r gew�hlte Gruppe(n) vorhanden.')
                self.session.data['gruppenadressen'] = adressen
            else:
                raise EE('Keine Gruppe ausgew�hlt!')
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
            legend='Gruppenauswahl f�r anzuzeigende Adressen',
            daten=[
                   [h.SelectItem(name='grid',
                                 size="6",
                                 class_="listbox280",
                                 tip="Alle Gruppen, f�r die Sie Zugriffsrechte haben",
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
                     tip="Alle Adressen der gew�hlten Gruppen anzeigen",
                     type='submit',
                     ),
            )

        #hidden = tuple([('grid', id) for id in gruppen_ids])
        hidden = (('wel', 'gruppe'),)
        #print 'HIDDEN', hidden
        res = h.FormPage(
            title='Adressenexport',
            name="adr",action="adressen",method="post",
            breadcrumbs = (('Hauptmen�', 'menu'),
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
                    raise EE('Keine Adressen f�r gew�hlte F�lle vorhanden.')
                self.session.data['falladressen'] = adressen
            else:
                raise EE('Keine F�lle in der Auswahl!')
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

        anzeige = self.get_fall_auswahl('Fallauswahl f�r anzuzeigende Adressen', welche_faelle, 
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
            breadcrumbs = (('Hauptmen�', 'menu'),
                           ),
            hidden=hidden,
            rows=(self.get_auswertungs_menu(),
                  anzeige,
                  self._get_address_list(adressen),
                  ),
            )
        return res.display()


    def hinweise(self, felder):
        hinweise_csv = h.FieldsetDataTable(
            legend='Hinweise',
            daten=[[h.String(string="Die CSV-Datei muss genauso aufgebaut sein wie die " +
                      '<a href="altimport?example=1">Beispieldatei</a>.<br /> ' +
                      "Dieses Format kann direkt mit Open Office oder MS Excel " +
                      "ge�ffnet und geschrieben werden " +
                      '(<a href="altimport?example=2">Beispiel</a>).',
                      n_col=2,
                      )
                    ],
                   [h.String(string='Erste Zeile:'
                             ),
                    h.String(string=
                             "In der ersten Zeile m�ssen in jeder Spalte "
                             " die entsprechenden Feldnamen stehen: "
                             "%s<em>&lt;Umbruch wg. Lesbarkeit&gt;</em> %s" %
                             (erste_zeile[:60],
                             erste_zeile[60:])
                             ),
                    ],
                   [h.String(string='Feldtrennzeichen:'
                             ),
                    h.String(string=';'
                             ),
                    ],
                   [h.String(string='Texttrennzeichen:'
                             ),
                    h.String(string='" (Anf�hrungszeichen). Kann bei einfachen Feldern entfallen, die selbst keine Anf�hrungszeichen oder Zeilenumbr�che enthalten.'
                             ),
                    ],
                   [h.String(string='Texttrennzeichen im Text:'
                             ),
                    h.String(string='"" (Verdoppelung)'
                             ),
                    ],
                   [h.String(string='Zeilenumbr�che in einem Feld:'
                             ),
                    h.String(string='zul�ssig'
                             ),
                    ],
                   [h.String(string='Kodierung:'
                             ),
                    h.String(string='iso-8859-1, iso-8859-15, latin-1, WinLatin1 '
                             '(Das ist das, '
                             'was im gro�en und ganzen '
                             'standardm��ig von Open Office und MS Excel erzeugt wird, zumindest '
                             'was die Umlaute und das EssZett betrifft. Es ist nicht Unicode oder utf8) '
                             ),
                    ],
                   ],
            )


class strkat(Request.Request):
    permissions = Request.MENU_PERM
    def processForm(self, REQUEST, RESPONSE):
        try:
            strassen_list = get_strassen_list(self.form)
        except Exception, e:
            return h.Meldung(
                legend='Fehler bei der Adresse',
                zeilen=(str(e),),
                onClick="javascript:window.close()" # strkat wird mit open ge�ffnet
                ).display()
        nichts_gefunden = False
        zuviel_gefunden = False
        ein_treffer = False
        such_muster = True
        if strassen_list == None:
            such_muster = False
        elif len(strassen_list) < 1:
            nichts_gefunden = True
        elif len(strassen_list) == 1:
            ein_treffer = True
        elif len(strassen_list) > 1000:
            zuviel_gefunden = True
        sp = '&nbsp;'
        # obligatorische Felder
        if config.STRASSENKATALOG_VOLLSTAENDIG:
            header = "Stra&szlig;enname&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" \
                     "Hausnr.&nbsp;&nbsp;PLZ&nbsp;&nbsp;Ort"
        else:
            header = "Stra&szlig;enname&nbsp;&nbsp;Hsnr.&nbsp;Von&nbsp;&nbsp;" \
                     "Bis&nbsp;&nbsp;&nbsp;&nbsp;PLZ&nbsp;&nbsp;&nbsp;Ort"
        # optionale Felder
        # ort, ortsteil, samtgemeinde, bezirk je nach config
        felder = config.STRASSENSUCHE.split()
        last_len = 3
        #felder = ('ortsteil', 'samtgemeinde', 'bezirk') # nur zum testen
        for f in felder:
            if f and f != 'ort':
                # pi mal Daumen, so dass die �berschriften
                # in etwa �ber den Spalten stehen
                header += sp*int(18-last_len) + f.capitalize()
                last_len = len(f)
        ergebnisse = h.FieldsetInputTable(
            legend='Passende Eintr�ge im Stra�enkatalog',
            daten=[[h.String(align="left",
                             string=header,
                             n_col=2,
                             class_='strtext11'), # kann auch 10 sein, wenn 3 Zusatzinfos rein sollen
                    ],
                   [h.SelectItem(label_width="0%",
                                 size=18,
                                 class_='listboxstrlarge', # kann auch verylarge sein
                                 name='strid',
                                 tip='Addresse ausw�hlen',
                                 options=self.get_address_options_neu(
            strassen_list, self.form.get('hsnr'),
            such_muster, nichts_gefunden,
            zuviel_gefunden),
                                 ),
                    ],
                   ],
            )
        buttons = h.FieldsetInputTable(
            daten=[[h.Button(value="�bernehmen",
                             tip="Ausgew�hlten Eintrag �bernehmen",
                             type='button',
                             onClick="submit_strkat()",
                             name='uebernehmen',
                             ),
                    h.Button(value="Abbrechen",
                             tip="Stra�ensuche abbrechen",
                             onClick="window.close()",
                             ),
                    ]])

        res = h.FormPage(
            #width=800, # evt vergr��eren bei mehr Zusatzfelder
            title='Stra�ensuche',
            name="strkat",action="klkarte",method="post",
            onSubmit="submit_strkat()",
            onload=ein_treffer and "submit_strkat()" or '',
            rows=(
                  ergebnisse,
                  buttons,
                  ),
            )
        return res.display()

    def get_address_options_neu(self, strassen_list, hausnr, such_muster,
                                nichts_gefunden,zuviel_gefunden):
        sp = '&nbsp;'
        def _format_option(element, felder):
            "formatiert den Inhalt einer Option tabellarisch bei der Strassensuche"
            "Bei langen Namen wird alles nach rechts verschoben, aber"
            "sp�tere L�cken werden opportunistisch aufgef�llt."
            # bei diesen Positionen sollten die Felder anfangen
            if config.STRASSENKATALOG_VOLLSTAENDIG:
                tabstops = (0,20,26,32,50,68,86) # eine Hausnummer statt von-bis 
            else:
                tabstops = (0,18,23,27,30,36,54,72,90) 
            res = []
            ist = 0 # wo wir das n�chste Element starten k�nnen
            for i,f in enumerate(felder):
                soll = tabstops[i] # wo es starten soll
                if ist < soll:
                    res.append(sp*(soll - ist))
                    ist = soll
                val = element[f]
                if val == None:
                    val = ''
                l = len(val)
                if f in ('von2', 'bis2'):
                    n_sp = val.count(sp)
                    l = l - n_sp*len(sp) + n_sp
                res.append(val+sp)
                ist += l + 1
            return ''.join(res)
        options = []
        text = ''
        if not such_muster:
            text = ("Keine Suchkriterien.",
                    "Geben Sie Teile der Adresse ein, z.B.",
                    "Anfangsbuchstaben der Stra�e und/oder eines andere Feldes.",
                    )
        elif nichts_gefunden:
            text = ("Keine Stra�e gefunden.",
                    "Schw�chen Sie Ihre Suchkriterien ab ",
                    "(oder verwenden Sie den Stra�enkatalog nicht).",
                    )
        elif zuviel_gefunden:
            text = ("Zuviele Stra�en gefunden." ,
                    "Bitte engen Sie Ihre Suchkriterien ein.",
                    )
        if text:
            for t in text:
                options.append('<option value="">%s</option>' % t)
        else:
            # Die Werte werden in das value-Attribut gepackt und von
            # javascript ausgewertet und in das aufrufende Formular
            # zur�ckgeschrieben.
            value_fields = ['name','hausnr_ohne_nullen','plz','ort',
                            'ortsteil','samtgemeinde','bezirk','id']
            value = '#'.join(['%%(%s)s' % f for f in value_fields])
            tmpl = '<option value="%s"%%(sel)s>' % value
            tmpl += '%(option_name2)s</option>'
            optionale_suchfelder = config.STRASSENSUCHE.split()
            if config.STRASSENKATALOG_VOLLSTAENDIG:
                hausnummern = ['hausnr_ohne_nullen',]
            else:
                hausnummern = ['von2', 'bis2', 'gu2',]
            felder = ['name',] +  hausnummern + ['plz'] + optionale_suchfelder
            single = len(strassen_list) == 1
            for element in strassen_list:
                hsnr = hausnr # der �bergebene Wert von der form
                von = element['von']
                if von and von == element['bis']: # Hausnummer durch Katalog definiert
                    hsnr = von
                element['hausnr_ohne_nullen'] = fuehrende_nullen_ersetzen(hsnr)
                element['von2'] = fuehrende_nullen_ersetzen(element['von'], sp)
                element['bis2'] = fuehrende_nullen_ersetzen(element['bis'], sp)
                element['gu2'] = element['gu'] or ''
                element['option_name2'] =  _format_option(element, felder)
                element['sel'] = single and ' selected="selected"' or ''
                options.append(tmpl % element)
        return '\n'.join(options)
        
def get_strassen_list(form, exact=False):
    """R�ckgabe: Exception: bei Fehlern in den Suchstrings
                 None: Keine Suchstrings
                 Sonst: die Liste der Ergebnisse, die leer sein kann"""
    #print 'GET_STRASSEN_LIST FORM', form
    if exact:
        joker = ''
    else:
        joker = '%'
    str_id = form.get('strid')
    str_felder = ('ort', 'plz', 'bezirk', 'samtgemeinde', 'ortsteil')
    where = []
    if str_id:
        where.append("id = %s" % str_id)
    for f in str_felder:
        val = form.get(f, '')
        if val:
            where.append("%s like %s" % (f, escape(val + joker)))
    str = check_strasse(form.get('str', ''))
    if str:
        where.append("name like %s" % (escape(str + joker)))
    hsnr  = check_hausnr(form.get('hsnr', ''))
    if hsnr.startswith('-'): # ausdr�cklich keine Hausnummer
        where.append("von IS NULL and bis IS NULL")
    elif hsnr:
        gu = split_hausnummer(hsnr)[2]
        where.append("(von <= '%s' or von IS NULL)" % hsnr)
        where.append("(bis >= '%s' or bis IS NULL)" % hsnr)
        where.append("(gu = '%s' or gu IS NULL)" % gu)
    strassen_list = []
    if where:
        wherestr = ' and '.join(where)
        #print 'GET_STRASSEN_LIST WHERE', where
        strassen_list = StrassenkatalogNeuList(where=wherestr, order='ort, plz, name')
        return strassen_list
    else:
        return None

def get_strasse(data):
    """liefert m�glichst genau ein Element aus dem Strassenkatalog, passend zu data,
    oder {}
    """
    strasse = {}
    if (data.get('lage') == cc('lage', '0') and
        data['ort'] and  data['plz']):
        # innerhalb der Geltung des Strassenkatalogs
        strassen_list = get_strassen_list(data, exact=True)
        if len(strassen_list) == 1: # sollte immer der Fall sein
            return strassen_list[0]
    return {}
    
def check_sonderzeichen(str):
    if '%' in str:
        raise EE("Bitte nur das Zeichen * als Platzhalter in der Suche verwenden.")
    return str.replace('*', '%')
def check_strasse(str):
    return check_sonderzeichen(str)

def check_hausnr(str):
    str = fuehrende_nullen_ersetzen(str)
    if str:
        #print 'CHECK_HAUSNR', str
        if not re.match(r"\-+$|[0-9]{1,3}[a-zA-Z]?$", str):
            raise EE("Ung�ltige Hausnummer: '%s' <br /><br />"
                     "Richtig w�re z.B. '1', '10', '100', '1a', '10a', '100a'. <br />"
                     "Geben Sie '---' anstelle einer Nummer ein, falls <br />"
                     "ausdr�cklich keine Hausnummer "
                     "angegeben werden soll.<br /><br />"
                     "Platzhalter bei Hausnummern nicht erlaubt." % str
                     )
        if not re.match(r"\-+$", str):
            str = hausnr_fuellen(str)
    return str
def check_plz(str):
    return check_sonderzeichen(str)

def fuehrende_nullen_ersetzen(s, womit=''):
    """Vorangehende '0' werden durch womit ersetzt."""
    if not s:
        return ''
    val_ohne_fuehrende_null = []
    anfang = True
    for x in list(s):
        if anfang and x == '0':
            val_ohne_fuehrende_null.append(womit)
        else:
            anfang = False
            val_ohne_fuehrende_null.append(x)
    return ''.join(val_ohne_fuehrende_null)

def hausnr_fuellen(s):
    """hausnr mit fuehrenden nullen fuellen"""
    if re.match(r".*[a-zA-Z]$", s):
        f = 4
    else:
        f = 3
    return s.zfill(f)

def fuellen(val, laenge, fuehrende_nullen_ersetzen_mit=''):
    if val == None:
        lval = 0
        val = ''
    else:
        lval = len(val)
        if fuehrende_nullen_ersetzen_mit:
            val = fuehrende_nullen_ersetzen(
                val,
                womit=fuehrende_nullen_ersetzen_mit)
    return val + "&nbsp;"*(laenge-lval)


def split_hausnummer(hsnr):
    """liefert (zahl, buchstabe, G oder U)"""
    #print 'SPLIT_HAUSNUMMER', hsnr
    if hsnr[-1].isalpha():
        nummer = int(hsnr[:-1])
        buchstabe = hsnr[-1]
    else:
        nummer = int(hsnr)
        buchstabe = ''
    gu = (nummer % 2 and 'U' or 'G')
    return nummer, buchstabe, gu

def get_strkat_felder():
    return [f['feld'] for f in FeldList(
        where="tabelle.tabelle='strkatalog'",
        join=[('tabelle', 'tabelle.id=feld.tab_id')])]

class strkatcheck(Request.Request):
    """Abfrageformular zum L�schen von Akten."""
    permissions = Request.ADMIN_PERM
    def processForm(self, REQUEST, RESPONSE):
        return "Noch nicht implementiert"


class strkatexport(Request.Request, akte_share):
    permissions = Request.ADMIN_PERM
    def csv_gen(self, where=''):
        import cStringIO
        out = cStringIO.StringIO()
        writer = csv.writer(out,
                            delimiter=';',
                            doublequote=True,
                            quotechar='"',
                            lineterminator='\r\n',
                            )
        
        felder = get_strkat_felder()[1:]
        strkat_list = StrassenkatalogNeuList(where=where)
        strkat_list.sort('name')
        writer.writerow(felder)
        rows = []
        for s in strkat_list:
            vals = []
            for f in felder:
                v = s[f]
                if f in ('von', 'bis') and v:
                    n,b,_ = split_hausnummer(v)
                    v = "%s%s" % (n, b)
                vals.append(v)
            rows.append(vals)
        writer.writerows(rows)
        return out.getvalue()
    def processForm(self, REQUEST, RESPONSE):
        download = self.form.get('download')
        plz = check_list(self.form, 'plz', 'Keine PLZ', [])
        if download == '1':
            if plz:
                where = "plz in (%s)" % ','.join([("'%s'" % p) for p in plz])
            else:
                where = ''
            content = self.csv_gen(where)
            self.RESPONSE.setHeader('content-type', "text/csv; charset=iso-8859-1")
            self.RESPONSE.setHeader('content-disposition',
                                    'attachment; filename=%s' % 'strassenkatalog.csv')
            self.RESPONSE.setBody(content)
            return
        strexport = h.FieldsetFormInputTable(
            name='strkatexport',action='strkatexport',method='post',
            hidden=(('download', '1'),
                    ),
            legend='Stra�enkatalog exportieren',
            daten=[[h.SelectItem(label='Postleitzahlen',
                                 name='plz',
                                 multiple=True,
                                 size=20,
                                 options=self.for_plz(),
                                 tip="Eintr�ge f�r gew�hlte PLZ, oder alle Eintr�ge",
                                 ),
                    ]],
            button=h.Button(value="Herunterladen",
                            name='op',
                            tip="Stra�enkatalog f�r gew�hlte PLZ bzw. insgesamt herunterladen",
                            type='submit',
                            n_col=2,
                            ),
            )
        res = h.Page(
            title='Stra�enkatalog exportieren',
            breadcrumbs = (('Administratorhauptmen�', 'menu'),
                           ),
            rows=(self.get_hauptmenu(),
                  strexport,
                  ),
            )
        return res.display()
    
class strkatimport(Request.Request, akte_share):
    permissions = Request.ADMIN_PERM
        
    def read_data(self, f):
        "liefert Liste von initialisierten, nicht-persistenten "
        "StrassenkatalogNeu Objekten"
        #print 'FILE: ', f, type(f)
        data = []
        feldnamen = get_strkat_felder()[1:]
        size = len(feldnamen)
        reader = csv.reader(f.readlines(),
                            delimiter=';',
                            doublequote=True,
                            quotechar='"',
                            lineterminator='\r\n',
                            )
        try:
            erste_zeile = reader.next()
        except StopIteration:
            self.csv_lese_fehler("Keine Daten gefunden")
            
        #print 'ERSTE_ZEILE: ', erste_zeile
        if size != len(erste_zeile):
            self.csv_lese_fehler("Anzahl der Feldnamen in der ersten Zeile stimmt nicht", 1,
                                 erste_zeile)
        for ist, soll in zip(erste_zeile, feldnamen):
            if ist != soll:
                self.csv_lese_fehler("Erste Zeile mit den Feldnamen stimmt nicht "
                                     "mit Feldnamen �berein", 1, erste_zeile)
        for i, row in enumerate(reader):
            #print 'ZEILE: ', row
            if size != len(row):
                self.csv_lese_fehler("Anzahl der Felder in Zeile %(znr)s stimmt nicht",
                                     i+2, row)
            dic = dict(zip(erste_zeile, row))
            dic = self.validate_normalize_strkat(dic, i+2, row)
            strk = StrassenkatalogNeu()
            strk.init(**dic)
            data.append(strk)
        return data


    def validate_eindeutig(self, strkat_list):
        plzs = []
        strkat_list.sort('plz')
        kombiset = {}
        old_plz = None
        for s in strkat_list:
            plz = s['plz']
            if plz != old_plz:
                kombiset = {}
                old_plz = plz
                plzs.append(plz)
            kombi = (s['plz'], s['ort'], s['name'], s['von'], s['bis'], s['gu']) 
            if kombi in kombiset:
                self.csv_lese_fehler("Kombination (plz, ort, name, von, bis, gu) nicht eindeutig: "
                                     "<br /><br />%s" % (kombi,))
            kombiset[kombi] = True
        return plzs

    def validate_zusatz_info(self, strkat_list):
        "gibt Liste der Zusatzfelder zur�ck, die teilweise vorhanden sind"
        " (also weder immer noch nie)"
        teilweise = []
        for f in ('bezirk', 'ortsteil', 'samtgemeinde', 'plraum'):
            strkat_list.sort(f)
            if not strkat_list[0][f] and strkat_list[-1][f]:
                teilweise.append(f)
        return teilweise
                

    def validate_normalize_strkat(self, dic, znr, daten):
        strasse = dic.get('name')
        if strasse:
            for end in ('trasse', 'tra�e'):
                if strasse.endswith(end):
                    i = strasse.index(end)
                    strasse = strasse[:i] + 'tr.'
            dic['name'] = strasse
        else:
            self.csv_lese_fehler('Stra�enname fehlt', znr, daten)
        ort = dic.get('ort')
        if not ort:
            self.csv_lese_fehler('Ort fehlt', znr, daten)
        plz = dic.get('plz')
        if plz:
            try:
                assert int(plz)
                assert len(plz) == 5
            except:
                self.csv_lese_fehler("Fehler im Feld 'plz': %s" % plz, znr, daten)
        else:
            self.csv_lese_fehler('Postleitzahl fehlt', znr, daten)
        von = dic.get('von')
        bis = dic.get('bis')
        if von or bis:
            if not (von and bis):
                self.csv_lese_fehler("Es muss entweder f�r 'von' und f�r 'bis' einen Wert geben, "
                                     'oder beide m�ssen leer sein', znr, daten)
            try:
                vn, vb, vg = split_hausnummer(von)
                bn, bb, bg = split_hausnummer(bis)
                assert 0 < vn < 1000 
                assert 0 < bn < 1000 
            except:
                self.csv_lese_fehler('Fehler in Hausnummer', znr, daten)
            if (vn == bn and not vb.upper() <=  bb.upper()) or vn > bn:
                self.csv_lese_fehler("Hausnummer 'von' muss gr��er sein als 'bis'", znr, daten)
            dic['von'] = "%03d%s" % (vn, vb.upper())
            dic['bis'] = "%03d%s" % (bn, bb.upper())
        else:
            dic['von'] = None
            dic['bis'] = None
        gu = dic.get('gu')
        if gu:
            try:
                assert gu in ('G', 'U', 'g', 'u')
            except:
                self.csv_lese_fehler("Fehler in Feld 'gu': %s (muss g, G, u, U oder leer sein)"
                                     % gu, znr, daten)
            try:
                assert dic.get('von')
            except:
                self.csv_lese_fehler("'gu' darf nur dann einen Wert haben, "
                                     "wenn auch 'von' und 'bis' einen Wert haben.",
                                     znr, daten)
            dic['gu'] = gu.upper()
        else:
            dic['gu'] = None
        return dic
    
    def csv_lese_fehler(self, msg, znr='', zeile=''):
        if znr:
            werte = ''.join([("%s: %s<br />" % (k,v))
                      for k,v in zip(get_strkat_felder()[1:],
                                      zeile)])
        #raise
        message = 'Fehler beim Lesen der CSV-Datei: <br /><br />' + (msg%locals())
        if znr:
            message += (' <br /><br />Zeilennummer: %(znr)s<br /><br />'
            'Zeilendaten:<br />%(werte)s') % locals()
        raise EE(message)

    def processForm(self, REQUEST, RESPONSE):
        print self.form
        example = self.form.get('example')
        datei = self.form.get('datei')
        replace = self.form.get('replace')
        if datei:
            data = self.read_data(datei)
            strkat_list = StrassenkatalogNeuList(data)
            plzs = self.validate_eindeutig(strkat_list)
            self.session.data['strkat'] = strkat_list
            self.session.data['plzs'] = plzs
            if replace == 'true':
                self.session.data['replace'] = True
                feedback1 = """Der vorhandene Stra�enkatalog wird
durch die Datens�tze der importierten Datei
vollst�ndig ersetzt."""
            else:
                self.session.data['replace'] = False
                feedback1 = """F�r diese Postleitzahlen werden die Eintr�ge 
im Stra�enkatalog ersetzt."""
            return  h.SubmitOrBack(
                legend='Stra�enkatalog �bernehmen',
                action='strkatimport',
                method='post',
                hidden=(('strkat_validiert', '1'),
                        ),
                zeilen=("Kein Fehler gefunden. ",
                        "%s Datens�tze" % len(strkat_list),
                        "Es gibt Datens�tze f�r die folgenden Postleitzahlen:",) +
                tuple([str(plz) for plz in plzs]) +
                (feedback1, "",
                 "Datens�tze �bernehmen?",)
                ).display()
        strkat_validiert = self.form.get('strkat_validiert')
        if strkat_validiert:
            strkat_list = self.session.data['strkat']
            plzs = self.session.data['plzs']
            if self.session.data['replace']:
                where = ''
                feedback2 = """Der vorhandene Stra�enkatalog wurde
durch die Datens�tze der importierten Datei
erfolgreich ersetzt."""
            else:
                where = "plz in (%s)" % ','.join([("'%s'" % p) for p in plzs])
                feedback2 = """F�r die genannten Postleitzahlen wurden die Eintr�ge
im Stra�enkatalog erfolgreich ersetzt."""
            StrassenkatalogNeuList(where=where).deleteall()
##             maxid = SQL("select max(id) from strkatalog").execute()[0][0]
##             if not maxid:
##                 maxid = 0
##             for i,s in enumerate(strkat_list):
##                 s.insert(maxid + i +1)
            for s in strkat_list:
                s.new()
                s.insert()
            res = h.Meldung(
                legend="Stra�enkatalog erfolgreich importiert",
                zeilen=(feedback2,
                        "%s Datens�tze �bernommen" % len(strkat_list),
                        'Weiter zum  Hauptmen&uuml ...',
                        ),
                weiter='menu',
                )
            return res.display()
        if self.session.data.get('strkat'):
            del self.session.data['strkat']
            del self.session.data['plzs']
        fname = 'beispiel_strkatalog.csv'
        demo_strkatalog = os.path.join(config.EBKUS_HOME, 'sql', fname)
        if example == '1':
            f = open(demo_strkatalog)
            content = f.read()
            f.close()
            self.RESPONSE.setHeader('content-type', 'text/plain; charset=iso-8859-1')
            #self.RESPONSE.setHeader('content-disposition', 'attachment; filename=%s' % fname)
            self.RESPONSE.setBody(content)
            return
        elif example == '2':
            f = open(demo_strkatalog)
            content = f.read()
            f.close()
            self.RESPONSE.setHeader('content-type', "text/csv; charset=iso-8859-1")
            self.RESPONSE.setHeader('content-disposition',
                                    'attachment; filename=%s' % fname)
            self.RESPONSE.setBody(content)
            return
        erste_zeile = ';'.join(['%s' % f for f in get_strkat_felder()][1:])
        hinweise_csv = h.FieldsetDataTable(
            legend='Hinweise zur CSV-Datei',
            daten=[[h.String(string="Die CSV-Datei muss genauso aufgebaut sein wie die " +
                      '<a href="strkatimport?example=1">Beispieldatei</a>.<br /> ' +
                      "Dieses Format kann direkt mit Open Office oder MS Excel " +
                      "ge�ffnet und geschrieben werden " +
                      '(<a href="strkatimport?example=2">Beispiel</a>).',
                      n_col=2,
                      )
                    ],
                   [h.String(string='Erste Zeile:'
                             ),
                    h.String(string=
                             "In der ersten Zeile m�ssen in jeder Spalte "
                             " die entsprechenden Feldnamen stehen: %s" % erste_zeile,
                             ),
                    ],
                   [h.String(string='Feldtrennzeichen:'
                             ),
                    h.String(string=';'
                             ),
                    ],
                   [h.String(string='Texttrennzeichen:'
                             ),
                    h.String(string='" (Anf�hrungszeichen). Kann bei einfachen Feldern entfallen, die selbst keine Anf�hrungszeichen oder Zeilenumbr�che enthalten.'
                             ),
                    ],
                   [h.String(string='Kodierung:'
                             ),
                    h.String(string='iso-8859-1, iso-8859-15, latin-1, WinLatin1 '
                             '(Kein Unicode; das ist das, '
                             'was im gro�en und ganzen '
                             'standardm��ig von Open Office und MS Excel erzeugt wird, zumindest '
                             'was die Umlaute und das EssZett betrifft) '
                             ),
                    ],
                   ],
            )
        hinweise_felder = h.FieldsetDataTable(
            legend='Bedingungen f�r die Korrektheit eines Stra�enkatalogs',
            daten=[[h.String(string='Pflichtfelder:'
                             ),
                    h.String(string="Die Felder plz, ort, name d�rfen nicht leer sein."
                             ),
                    ],
                   [h.String(string='Hausnummern:'
                             ),
                    h.String(string='Ein <em>vollst�ndiger Stra�enkatalog</em> enth�lt einen Eintrag '
                             'f�r jede Hausnummer. Die Felder von und bis sind dann immer identisch '
                             'und niemals leer. Das Feld gu ist immer leer. <br />'
                             'Ein <em>unvollst�ndiger Stra�enkatalog</em> muss keine Eintr�ge '
                             'f�r Hausnummern haben. In diesem Fall gibt es f�r eine Stra�e '
                             'nur einen Eintrag, und die Stra�e ist damit einer einzigen Postleitzahl '
                             'zugeordnet. Alternativ kann durch die Felder von/bis ein Intervall '
                             'von Hausnummern definiert werden, wodurch mehrere Eintr�ge pro Stra�e '
                             'm�glich sind, denen auch unterschiedliche Postleitzahlen zugeordnet '
                             'sein k�nnen. In diesem Fall muss immer sowohl von als auch bis '
                             'einen Wert haben. Wenn ein Intervall vorliegt, kann das Feld gu den '
                             "Wert 'g', 'G', 'u', 'U'  annehmen, "
                             'wodurch der zugeh�rige Intervall als nur aus den geraden bzw. '
                             'ungeraden Zahlen bestehend definiert wird. <br />'
                             'Wenn ein vollst�ndiger Stra�enkatalog verwendet wird, sollte  '
                             'in der Konfiguration der Parameter <em>strassenkatalog_vollstaendig</em> '
                             'auf true gesetzt werden. <br />'
                             'Hausnummern bestehen immer aus einer maximal dreistellige Zahl, '
                             'evt. gefolgt von einem Buchstaben. '
                             ),
                    ],
                   [h.String(string='Eindeutigkeit:'
                             ),
                    h.String(string='Eine Kombination der Felder von, bis, gu, name, plz, ort '
                             'darf im gesamten Stra�enkatalog nur einmal vorkommen, da eine Adresse '
                             'durch plz, ort, strasse und hausnummer eindeutig definiert ist. '
                             'Die Zusatzfelder ortsteil, bezirk, samtgemeinde d�rfen grunds�tzlich '
                             'nicht zur Differenzierung von Adressen herangezogen werden. '
                             'Z.B. d�rfen die folgenden Eintr�ge nicht zusammen in einem Stra�enkatalog '
                             'erscheinen: <br />'
                             ';;;An der Schule;38116;Braunschweig;Alt-Lehndorf;;;;<br />'
                             ';;;An der Schule;38116;Braunschweig;Neu-Lehndorf;;;;<br />'
                             'Zul�ssig ist jedoch: <br />'
                             ';;;An der Schule;38116;Braunschweig;Alt-Lehndorf;;;;<br />'
                             ';;;An der Schule;38117;Braunschweig;Neu-Lehndorf;;;;<br />'
                             '1;1;;Arndtstr.;38118;Braunschweig;Wilhelmitor-S�d;;;;<br />'
                             '17;21;;Arndtstr.;38120;Braunschweig;Hermannsh�he;;;;<br />'
                             '36;38;;Arndtstr.;38118;Braunschweig;Wilhelmitor-S�d;;;;<br />'
                             ),
                    ],
                   [h.String(string='Zusatzfelder:'
                             ),
                    h.String(string='Die Felder ortsteil, bezirk, samtgemeinde und plraum '
                             'geben zus�tzliche Informationen f�r eine gegebene Adresse. '
                             'Sie k�nnen leer bleiben, aber wenn sie verwendet werden, '
                             'sollte sinnvollerweise f�r jeden Eintrag ein '
                             'Wert vorhanden sein. Sie k�nnen dann bei der Stra�ensuche '
                             'als Suchkriterien verwendet werden, und es k�nnen statistische '
                             'Auswertungen dar�ber durchgef�hrt werden.<br />'
                             'Die jeweils verwendeten Zusatzfelder m�ssen in der Konfiguration '
                             'ebkus.conf im Parameter <em>strassensuche</em> aufgef�hrt werden. '
                             ),
                    ],
                   [h.String(string='Schreibweise:'
                             ),
                    h.String(string='Endung mit <em>strasse, Strasse, stra�e, Stra�e</em> '
                             'werden zu <em>str.</em> bzw. <em>Str.</em> normalisiert.'
                             ),
                    ],
                   ],
            )
        strkatimport = h.FieldsetFormInputTable(
            legend='Stra�enkatalog importieren',
            name='strkatimport',action="strkatimport",method="post",
            daten=[[h.RadioItem(label='Nur Eintr�ge f�r die gegebenen Postleitzahlen ersetzen',
                                name='replace',
                                tip='Es werden nur die Eintr�ge f�r die in der Importdatei vorkommenden Postleitzahlen ersetzt',
                                value='false',
                                checked=True,
                                ),
                    ],
                   [h.RadioItem(label='Vorhandenen Stra�enkatalog vollst�ndig ersetzen',
                                name='replace',
                                tip='Der aktuell vorhanden Stra�enkatalog wird vollst�ndig durch den Import ersetzt',
                                value='true',
                                checked=False,
                                ),
                    ],
                   [h.DummyItem()],
                   [h.UploadItem(label='Lokaler Dateiname',
                                 name='datei',
                                 tip='CSV-Datei mit Stra�enkatalog',
                                 class_="textboxverylarge",
                                 ),
                    ]],
                button=h.Button(value="Hochladen",
                                name='op',
                                tip="Gew�hlte Datei mit Stra�enkatalog hochladen",
                                type='submit',
                                n_col=2,
                                ),
            )
        res = h.Page(
            title='Stra�enkatalog importieren',
            breadcrumbs = (('Administratorhauptmen�', 'menu'),
                           ),
            hidden=(),
            rows=(self.get_hauptmenu(),
                  strkatimport,
                  hinweise_csv,
                  hinweise_felder,
                  ),
            )
        return res.display()
