# coding: latin-1

"""Module für Akte und Fall."""

import os
import csv
from ebkus.app import Request
from ebkus.config import config
from ebkus.app.ebapi import Akte, Fall, FallList, \
     FeldList, AltdatenList, Altdaten, Zustaendigkeit, Date, today, cc, EE

from ebkus.html.strkat import split_hausnummer, fuellen
from ebkus.app_surface.standard_templates import *
from ebkus.app_surface.akte_templates import *

import ebkus.html.htmlgen as h
from ebkus.html.akte_share import akte_share



class altimport(Request.Request, akte_share):
    permissions = Request.ADMIN_PERM

    def get_altdaten_felder(self):
        return [f['feld'] for f in FeldList(
            where="tabelle.tabelle='altdaten'",
            join=[('tabelle', 'tabelle.id=feld.tab_id')])]
        
    def read_data(self, f):
        #print 'FILE: ', f, type(f)
        data = []
        feldnamen = self.get_altdaten_felder()[1:]
        size = len(feldnamen)
        reader = csv.reader(f.readlines(),
                            delimiter=';',
                            doublequote=True,
                            quotechar='"',
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
                                     "mit Feldnamen überein", 1, erste_zeile)
        for i, row in enumerate(reader):
            #print 'ZEILE: ', row
            if size != len(row):
                self.csv_lese_fehler("Anzahl der Felder in Zeile %(znr)s stimmt nicht",
                                     i+2, row)
            dic = dict(zip(erste_zeile, row))
            dic = self.validate_normalize_altdaten(dic, i+2, row)
            dic['id'] = i+2
            altd = Altdaten()
            altd.init(**dic)
            data.append(altd)
        return data

    def validate_normalize_altdaten(self, dic, znr, daten):
        strasse = dic.get('strasse', '')
        if strasse:
            for end in ('trasse', 'traße'):
                if strasse.endswith(end):
                    i = strasse.index(end)
                    strasse = strasse[:i] + 'tr.'
            dic['strasse'] = strasse
        gb = dic.get('geburtsdatum')
        if gb:
            try:
                d,m,j = [int(x) for x in gb.split('.')]
                date = Date(j,m,d)
                if not date.check():
                    raise Exception()
                dic['geburtsdatum'] = str(date)
            except:
                self.csv_lese_fehler('Fehler im Geburtsdatum: %s' % gb, znr, daten)
        gs = dic.get('geschlecht')
        if gs:
            if gs not in ('m', 'w', 'M', 'W'):
                self.csv_lese_fehler('Fehler im Geschlecht: %s' % gs, znr, daten)
            dic['geschlecht'] = gs.lower()
        jahr = dic.get('jahr')
        if jahr:
            try:
                assert 1980 < int(jahr) < today().year
            except:
                self.csv_lese_fehler('Fehler im Jahr: %s' % jahr, znr, daten)
        plz = dic.get('plz')
        if plz:
            try:
                assert 10000 < int(plz) < 99999
            except:
                self.csv_lese_fehler('Fehler in der Postleitzahl: %s' % plz, znr, daten)
        hausnummer = dic.get('hausnummer')
        if hausnummer:
            try:
                nummer, buchstabe, gu = split_hausnummer(hausnummer)
                dic['hausnummer'] = "%s%s" % (nummer, buchstabe.upper())
            except:
                self.csv_lese_fehler('Fehler in Hausnummer: %s' % hausnummer, znr, daten)
        return dic
    
    def csv_lese_fehler(self, msg, znr='', zeile=''):
        werte = ''.join([("%s: %s<br />" % (fuellen(k, 13),v))
                  for k,v in zip(self.get_altdaten_felder()[1:],
                                  zeile)])
        #raise
        raise EE('Fehler beim Lesen der CSV-Datei: <br /><br />' + (msg%locals())
                 + '<br /><br />' +
                 'Zeilennummer: %(znr)s<br />Zeilendaten:<br />%(werte)s' % locals())

    def processForm(self, REQUEST, RESPONSE):
        example = self.form.get('example')
        datei = self.form.get('datei')
        if datei:
            data = self.read_data(datei)
            self.session.data['altdaten'] = data
            return  h.SubmitOrBack(
                legend='Altdaten übernehmen',
                action='altimport',
                method='post',
                hidden=(('altdaten_validiert', '1'),
                        ),
                zeilen=("Kein Fehler gefunden. Altdaten in die Datenbank übernehmen?",
                        )
                ).display()
        altdaten_validiert = self.form.get('altdaten_validiert')
        if altdaten_validiert:
            data = self.session.data['altdaten']
            AltdatenList(where='').deleteall()
            altd_list = AltdatenList(data)
            altd_list.insertall()
            res = h.Meldung(
                legend="Altdaten erfolgreich importiert",
                zeilen=("Altdaten erfolgreich importiert.",
                      "%s Datensätze eingelesen" % len(altd_list),
                        'Weiter zum  Hauptmen&uuml ...',
                        ),
                onClick="go_to_url('menu')",
                )
            return res.display()
        if self.session.data.get('altdaten'):
            del self.session.data['altdaten']
        fname = 'demo_altdaten.csv'
        demo_altdaten = os.path.join(config.EBKUS_HOME, 'sql', fname)
        if example == '1':
            f = open(demo_altdaten)
            content = f.read()
            f.close()
            self.RESPONSE.setHeader('content-type', 'text/plain; charset=iso-8859-1')
            #self.RESPONSE.setHeader('content-disposition', 'attachment; filename=%s' % fname)
            self.RESPONSE.setBody(content)
            return
        elif example == '2':
            f = open(demo_altdaten)
            content = f.read()
            f.close()
            self.RESPONSE.setHeader('content-type', "text/csv; charset=iso-8859-1")
            self.RESPONSE.setHeader('content-disposition',
                                    'attachment; filename=%s' % fname)
            self.RESPONSE.setBody(content)
            return
        erste_zeile = ';'.join(['"%s"' % f for f in self.get_altdaten_felder()][1:])
        hinweise_csv = h.FieldsetDataTable(
            legend='Hinweise zur CSV-Datei',
            daten=[[h.String(string="Die CSV-Datei muss genauso aufgebaut sein wie die " +
                      '<a href="altimport?example=1">Beispieldatei</a>.<br /> ' +
                      "Dieses Format kann direkt mit Open Office oder MS Excel " +
                      "geöffnet und geschrieben werden " +
                      '(<a href="altimport?example=2">Beispiel</a>).',
                      n_col=2,
                      )
                    ],
                   [h.String(string='Erste Zeile:'
                             ),
                    h.String(string=
                             "In der ersten Zeile müssen in jeder Spalte "
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
                    h.String(string='"'
                             ),
                    ],
                   [h.String(string='Texttrennzeichen im Text:'
                             ),
                    h.String(string='"" (Verdoppelung)'
                             ),
                    ],
                   [h.String(string='Zeilenumbrüche in einem Feld:'
                             ),
                    h.String(string='zulässig'
                             ),
                    ],
                   [h.String(string='Kodierung:'
                             ),
                    h.String(string='iso-8859-1, iso-8859-15, latin-1, WinLatin1 '
                             '(Das ist das, '
                             'was im großen und ganzen '
                             'standardmäßig von Open Office und MS Excel erzeugt wird, zumindest '
                             'was die Umlaute und das EssZett betrifft. Es ist nicht Unicode oder utf8) '
                             ),
                    ],
                   ],
            )
        hinweise_felder = h.FieldsetDataTable(
            legend='Hinweise zu den Feldern',
            daten=[[h.String(string="Felder können leer sein, die entsprechenden "
                      'Daten stehen dann nicht für eine Übernahme zur Verfügung.',
                      n_col=2,
                      )
                    ],
                   [h.String(string='geburtsdatum:'
                             ),
                    h.String(string=
                             "Tag . Monat . Jahr <br /> "
                             "Das Jahr muss vierstellig sein, Tag und Monat ein- oder zweistellig, <br /> "
                             "z.B. 1.1.2002, 10.01.1999"
                             ),
                    ],
                   [h.String(string='geschlecht:'
                             ),
                    h.String(string='m oder w, alles andere ist ungültig'
                             ),
                    ],
                   [h.String(string='jahr:'
                             ),
                    h.String(string='eine vierstellige Zahl'
                             ),
                    ],
                   [h.String(string='strasse:'
                             ),
                    h.String(string='Endung mit <em>strasse, Strasse, straße, Straße</em> '
                             'werden zu <em>str.</em> bzw. <em>Str.</em> normalisiert.'
                             ),
                    ],
                   [h.String(string='hausnummer:'
                             ),
                    h.String(string='ein- bis dreistellige Zahl und evt. ein Buchstabe als '
                             'Zusatz, der zum großgeschriebenen Buchstaben normalisiert wird.'
                             ),
                    ],
                   [h.String(string='plz:'
                             ),
                    h.String(string='fünfstellige Zahl'
                             ),
                    ],
                   ],
            )
        altdimport = h.FieldsetFormInputTable(
            legend='Altdaten importieren (evt. bereits vorhandene werden ersetzt)',
            name='altimport',action="altimport",method="post",
            daten=[[h.UploadItem(label='Lokaler Dateiname',
                                 name='datei',
                                 tip='CSV-Datei mit Altdaten hochladen',
                                 class_="textboxverylarge",
                                 ),
                    ]],
                button=h.Button(value="Hochladen",
                                name='op',
                                tip="Gewählte Datei mit Altdaten hochladen",
                                type='submit',
                                n_col=2,
                                ),
            )
        res = h.Page(
            title='Altdaten importieren',
            breadcrumbs = (('Administratorhauptmenü', 'menu'),
                           ),
            hidden=(),
            rows=(self.get_hauptmenu(),
                  altdimport,
                  hinweise_csv,
                  hinweise_felder,
                  ),
            )
        return res.display()

class altlist(Request.Request, akte_share):
    permissions = Request.ABFR_PERM
    def processForm(self, REQUEST, RESPONSE):
        vorname = self.form.get('vorname', '')
        name = self.form.get('name', '')
        fallnummer = self.form.get('fallnummer', '')
        rest = self.form.get('rest', '')
        where = []
        altdaten = []
        if vorname:
            where.append("vorname like '%%%(vorname)s%%'" % locals())
        if name:
            where.append("name like '%%%(name)s%%'" % locals())
        if fallnummer:
            where.append("fallnummer like '%%%(fallnummer)s%%'" % locals())
        if rest:
            where.append("(strasse like '%%%(rest)s%%' or "
                         "ort like '%%%(rest)s%%' or "
                         "plz like '%%%(rest)s%%' or "
                         "memo like '%%%(rest)s%%' or "
                         "mitarbeiter like '%%%(rest)s%%')" % locals())
        if where:
            altdaten = AltdatenList(where=' and '.join(where), order='name, vorname, fallnummer')

        where = []
        aktuelle_daten = []
        if vorname:
            where.append("akte.vn like '%%%(vorname)s%%'" % locals())
        if name:
            where.append("akte.na like '%%%(name)s%%'" % locals())
        if where:
            aktuelle_daten = FallList(where=' and '.join(where),
                                      join=[('akte', 'fall.akte_id=akte.id')],
                                      order='akte.na, akte.vn')
        auswahl_kriterien = h.FieldsetFormInputTable(
            name="altlist",
            #action="abfragedef",
            action="altlist",
            method="post",
            hidden = (),
            legend='Suchkriterien eingeben',
            daten=[[h.TextItem(label='Vorname enthält',
                               name='vorname',
                               value=vorname,
                               tip='Groß/Kleinschreibung egal, kann mittendrin erscheinen',
                               ),
                    h.TextItem(label='Nachname enthält',
                               name='name',
                               value=name,
                               tip='Groß/Kleinschreibung egal, kann mittendrin erscheinen',
                               ),
                    ],
                   [h.TextItem(label='Alte Fallnummer enthält',
                               name='fallnummer',
                               value=fallnummer,
                               tip='Groß/Kleinschreibung egal, kann mittendrin erscheinen',
                               ),
                    h.TextItem(label='Memo-, Mitarbeiter- oder Adressfeld enthält',
                               name='rest',
                               value=rest,
                               tip='Zeichenkette erscheint in einem der Felder',
                               ),
                    ],
                   [h.Dummy(n_col=4)],
                   [h.Button(value="Anzeigen",
                             name='op',
                             tip="Altdaten entsprechend den Suchkriterien anzeigen",
                             type='submit',
                             n_col=4,
                             ),
                    ],
                   ],
            )
        daten = []
        for altd in altdaten:
            daten.append([h.String(string=altd['vorname']),
                          h.String(string=altd['name']),
                          h.String(string=altd['geburtsdatum']),
                          h.String(string=altd['geschlecht']),
                          h.String(string=altd['jahr']),
                          h.String(string=altd['fallnummer']),
                          h.String(string=altd['mitarbeiter']),
                          h.String(string="%(strasse)s %(hausnummer)s, %(plz)s %(ort)s" % altd),
                          h.String(string="%(telefon1)s, %(telefon2)s" % altd),
                          h.CheckItem(label='',
                                      name='uebern',
                                      value=altd['id'],
                                      checked=False,
                                      tip='Hier markieren, um die Daten in die Neuaufnahme zu übernehmen',
                                      ),
                          ])
            daten.append([h.String(string=altd['memo'],
                                   n_col=9),
                          h.DummyItem(),
                          ])
            daten.append([h.Dummy(n_col=11),
                          ])
        altdaten_table = h.FieldsetFormDataTable(
            name="altdaten",
            #action="abfragedef",
            action="akteneu",
            method="post",
            hidden = (),
            legend='Altdaten passend zu den Suchkriterien',
            headers=('Vorname', 'Name', 'Geb.', 'm/w', 'Jahr', 'Fallnr.', 'Mitarbeiter',
                     'Adresse', 'Telefon', '', 'Übern.'),
            daten=daten,
            no_button_if_empty=False,
            buttons=[daten and h.Button(value="Übernehmen",
                              name='op',
                              tip="Markierten Datensatz für die Neuaufnahme übernehmen",
                              type='submit',
                              ) or None,
                     h.Button(value="Abbrechen",
                              name='op',
                              tip="Zurück zur Neuaufnahme ohne Datenübernahme",
                              type='button',
                              onClick="go_to_url('akteneu')",
                              ),
                     ],
            empty_msg="Keine passenden Altdaten gefunden.",
            )
        aktuelle_daten_table = h.FieldsetDataTable(
            legend='Klienten passend zu den Suchkriterien Vorname/Nachname',
            headers=('Fallnr', 'Vorname', 'Name', 'Geb.', 'Beginn', 'z.d.A.', 'Zuständig',),
            daten=[[h.Link(string=fall['fn'],
                           url='klkarte?akid=%(akte_id)s' % fall),
                    h.String(string=fall['akte__vn']),
                    h.String(string=fall['akte__na']),
                    h.String(string=fall['akte__gb']),
                    h.Datum(date=fall.getDate('bg')),
                    h.Datum(date=fall.getDate('zda')),
                    h.String(string=fall['zuletzt_zustaendig__mit__na']),
            ] for fall in aktuelle_daten],
            empty_msg="Keine Klienten gefunden.",
            )
        res = h.Page(
            title='Altdaten',
            breadcrumbs = (('Hauptmenü', 'menu'),
                           ('Neue Akte anlegen', 'akteneu'),
                           ),
            rows=(self.get_hauptmenu(),
                  auswahl_kriterien,
                  altdaten_table,
                  aktuelle_daten_table,
                  ),
            )
        return res.display()

