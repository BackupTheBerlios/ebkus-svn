# coding: latin-1
import re
import csv
import os
from ebkus.db.sql import escape
from ebkus.app import Request
from ebkus.app.ebapi import EE, cc, check_list, SQL, SQLError
from ebkus.config import config

import ebkus.html.htmlgen as h
from ebkus.html.akte_share import akte_share 

class sql_abfrage(Request.Request, akte_share):
    permissions = Request.ADMIN_PERM
    def csv_gen(self, erste_zeile, res):
        import cStringIO
        out = cStringIO.StringIO()
        writer = csv.writer(out,
                            delimiter=';',
                            doublequote=True,
                            quotechar='"',
                            lineterminator='\r\n',
                            )
        if erste_zeile:
            writer.writerow(erste_zeile)
        #print 'RES', res
        writer.writerows(res)
        return out.getvalue()
    def get_felder(self, eingabe):
        reader = csv.reader([eingabe.strip()],
                            delimiter=' ',
                            doublequote=True,
                            quotechar='"',
                            lineterminator='\r\n',
                            )
        try:
            return reader.next()
        except StopIteration:
            return []
    def processForm(self, REQUEST, RESPONSE):
        download = self.form.get('download')
        sql = self.form.get('query', '')
        erste_zeile = self.form.get('felder', '')
        op = self.form.get('op', '')
        #erste_zeile = self.get_felder(erste_zeile)
        erste_zeile = erste_zeile.split()
        if download == '1' and sql and op == 'Ergebnistabelle':
            sql = sql.strip()
            sqlupper = sql.upper()
            if not (sqlupper.startswith('SELECT') or
                    sqlupper.startswith('SHOW')):
                raise EE("SQL-Abfrage muss mit 'SELECT' oder 'SHOW' beginnen")
            for s in ('INSERT', 'DELETE', 'UPDATE'):
                if s in sqlupper:
                    raise EE("Nicht erlaubt in einer SQL-Abfrage: '%s'" % s)
            try:
                res = SQL(sql).execute()
            except SQLError, e:
                raise EE("SQL Fehler:<br />%s" % e[1])
            if res and erste_zeile and len(res[0]) != len(erste_zeile):
                raise EE("Anzahl der Feldnamen passt nicht zur SQL-Abfrage.")
            if not res:
                return h.Meldung(
                    legend="Ergebnismenge ist leer",
                    zeilen=('Die Abfrage ergab keine Ergebnisse',
                            'Zurück ...',
                            ),
                    ).display()
            content = self.csv_gen(erste_zeile, res)
            self.RESPONSE.setHeader('content-type', "text/csv; charset=iso-8859-1")
            self.RESPONSE.setHeader('content-disposition',
                                    'attachment; filename=%s' % 'sql_abfrage.csv')
            self.RESPONSE.setBody(content)
            return
        elif op == 'Beispiel 1':
            # Beispiel 1
            sql = """SELECT f.fn, CONCAT(f.bgd, '.', f.bgm, '.', f.bgy), a.plz, a.ort
FROM fall f, akte a
WHERE f.akte_id = a.id
-- Beispiel 1 """
            erste_zeile = ['Fallnummer', 'Anmeldedatum', 'Postleitzahl', 'Ort']
        elif op == 'Beispiel 2':
            # Beispiel 2
            sql = """
SELECT b.id,                               -- Beratungskontakt ID
       CONCAT(b.kd, '.', b.km, '.', b.ky), -- Datum des Kontakts (aus drei Feldern)
       c_art_bs.code, c_art_bs.name,       -- Code und Name: Art des Kontakts
       c_offenespr.code, c_offenespr.name, -- Code und Name: offenespr
       f.fn,                               -- Fallnummer
       a.plz, a.ort, a.plraum              -- Regionaldaten aus Akte
FROM 
-- n:m Beziehung zwischen Beratungskontakt und Fall wird durch Fallberatungskontakt 
-- abgebildet.
-- Im Ergebnis steht eine Zeile fuer jede Kombination Fall/Beratungskontakt.
fallberatungskontakt fb, beratungskontakt b, fall f, akte a,
-- Die Joins fuer die Merkmalskataloge:
     code c_art_bs,
     code c_offenespr
WHERE fb.bkont_id = b.id AND fb.fall_id = f.id AND f.akte_id = a.id AND
      c_art_bs.id = b.art_bs AND
      c_offenespr.id = b.offenespr
ORDER BY b.id
-- Beispiel 2 """
            erste_zeile = ['Beratungskontakt-Id', 'Datum', 'Art-Code', 'Art',
                           'Offene_Sprechstunde-Code', 'Offene_Sprechstunde',
                           'Fallnummer', 'PLZ', 'Ort', 'Planungsraum']
        sqlabfrage = h.FieldsetFormInputTable(
            name='sqlabfrage',action='sql_abfrage',method='post',
            hidden=(('download', '1'),
                    ),
            legend='SQL Abfrage',
            daten=[[h.String(string='Hinweis:',
                             class_='labeltext',
                                   ),
                    h.String(string='<small>Feldnamen sind optional. Falls angegeben, '
                             'erscheinen sie in der ersten Zeile der Ergebnistabelle '
                             '(Spaltenüberschriften). Für jedes Feld im SELECT-Ausdruch '
                             'muss genau ein Feldname angegeben werden. '
                             'Feldnamen durch Leerzeichen trennen. Der Feldname selbst '
                             'darf keine Leerzeichen enthalten.<br />'
                             'Das Datenbankschema ist in der Datei <code>'
                             '&lt;ebkus-installationsverzeichnis&gt;/ebkus/lib/ebkus/gen/schemadata.py '
                             '</code> dokumentiert.<br />'
                             'Zulässige SELECT-Syntax: '
                             '<a href="http://dev.mysql.com/doc/refman/4.1/en/select.html">'
                             'MySQL Handbuch 3.23, 4.0, 4.1</a></small>' ,
                                   ),
                    ],
                   [h.TextareaItem(label='Feldnamen',
                                   name='felder',
                                   value=' '.join(erste_zeile),
                                   rows="1",
                                   cols="200",
                                   class_ = 'textareastr600',
                                   tip="Feldnamen mit Leerzeichen getrennt",
                                   ),
                    ],
                   [h.TextareaItem(label='SQL',
                                   name='query',
                                   value=sql,
                                   rows="18",
                                   cols="200",
                                   class_ = 'textareastr600',
                                   tip="SQL Abfrage",
                                   ),
                    ],
                   ],
##             button=h.Button(value="Ergebnistabelle",
##                             name='op',
##                             tip="Ergebnis der SQL-Abfrage als CSV-Datei herunterladen",
##                             type='submit',
##                             n_col=2,
##                             ),
            buttons=[h.Button(value="Ergebnistabelle",
                            name='op',
                            tip="Ergebnis der SQL-Abfrage als CSV-Datei herunterladen",
                            type='submit',
                            ),
                     h.Button(value="Beispiel 1",
                              name='op',
                              tip="Beispielabfrage einfügen",
                              type='submit',
                              ),
                     h.Button(value="Beispiel 2",
                              name='op',
                              tip="Beispielabfrage einfügen",
                              type='submit',
                              ),
                     ]
            )
        res = h.Page(
            title='SQL Abfrage',
            breadcrumbs = (('Administratorhauptmenü', 'menu'),
                           ),
            rows=(self.get_hauptmenu(),
                  sqlabfrage,
                  ),
            )
        return res.display()
    
