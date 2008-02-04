# coding: latin-1
import re
import csv
import os
from ebkus.db.sql import escape
from ebkus.app import Request
from ebkus.app.ebapi import StrassenkatalogNeuList, \
     StrassenkatalogNeu, FeldList, EE, cc, check_list, SQL
from ebkus.app_surface.strkat_templates import *
from ebkus.config import config

import ebkus.html.htmlgen as h
from ebkus.html.akte_share import akte_share 

class strkat(Request.Request):
    permissions = Request.MENU_PERM
    def processForm(self, REQUEST, RESPONSE):
        try:
            strassen_list = get_strassen_list(self.form)
        except Exception, e:
            return h.Meldung(
                legend='Fehler bei der Adresse',
                zeilen=(str(e),),
                onClick="javascript:window.close()" # strkat wird mit open geöffnet
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
                # pi mal Daumen, so dass die Überschriften
                # in etwa über den Spalten stehen
                header += sp*int(18-last_len) + f.capitalize()
                last_len = len(f)
        ergebnisse = h.FieldsetInputTable(
            legend='Passende Einträge im Straßenkatalog',
            daten=[[h.String(align="left",
                             string=header,
                             n_col=2,
                             class_='strtext11'), # kann auch 10 sein, wenn 3 Zusatzinfos rein sollen
                    ],
                   [h.SelectItem(label_width="0%",
                                 size=18,
                                 class_='listboxstrlarge', # kann auch verylarge sein
                                 name='strid',
                                 tip='Addresse auswählen',
                                 options=self.get_address_options_neu(
            strassen_list, self.form.get('hsnr'),
            such_muster, nichts_gefunden,
            zuviel_gefunden),
                                 ),
                    ],
                   ],
            )
        buttons = h.FieldsetInputTable(
            daten=[[h.Button(value="Übernehmen",
                             tip="Ausgewählten Eintrag übernehmen",
                             type='button',
                             onClick="submit_strkat()",
                             name='uebernehmen',
                             ),
                    h.Button(value="Abbrechen",
                             tip="Straßensuche abbrechen",
                             onClick="window.close()",
                             ),
                    ]])

        res = h.FormPage(
            #width=800, # evt vergrößeren bei mehr Zusatzfelder
            title='Straßensuche',
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
            "spätere Lücken werden opportunistisch aufgefüllt."
            # bei diesen Positionen sollten die Felder anfangen
            if config.STRASSENKATALOG_VOLLSTAENDIG:
                tabstops = (0,20,26,32,50,68,86) # eine Hausnummer statt von-bis 
            else:
                tabstops = (0,18,23,27,30,36,54,72,90) 
            res = []
            ist = 0 # wo wir das nächste Element starten können
            for i,f in enumerate(felder):
                soll = tabstops[i] # wo es starten soll
                if ist < soll:
                    res.append(sp*(soll - ist))
                    ist = soll
                val = element[f]
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
                    "Anfangsbuchstaben der Straße und/oder eines andere Feldes.",
                    )
        elif nichts_gefunden:
            text = ("Keine Straße gefunden.",
                    "Schwächen Sie Ihre Suchkriterien ab ",
                    "(oder verwenden Sie den Straßenkatalog nicht).",
                    )
        elif zuviel_gefunden:
            text = ("Zuviele Straßen gefunden." ,
                    "Bitte engen Sie Ihre Suchkriterien ein.",
                    )
        if text:
            for t in text:
                options.append('<option value="">%s</option>' % t)
        else:
            # Die Werte werden in das value-Attribut gepackt und von
            # javascript ausgewertet und in das aufrufende Formular
            # zurückgeschrieben.
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
                hsnr = hausnr # der übergebene Wert von der form
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
    """Rückgabe: Exception: bei Fehlern in den Suchstrings
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
    if hsnr.startswith('-'): # ausdrücklich keine Hausnummer
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
    """liefert möglichst genau ein Element aus dem Strassenkatalog, passend zu data,
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
            raise EE("Ungültige Hausnummer: '%s' <br /><br />"
                     "Richtig wäre z.B. '1', '10', '100', '1a', '10a', '100a'. <br />"
                     "Geben Sie '---' anstelle einer Nummer ein, falls <br />"
                     "ausdrücklich keine Hausnummer "
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
    """Abfrageformular zum Löschen von Akten."""
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
            legend='Straßenkatalog exportieren',
            daten=[[h.SelectItem(label='Postleitzahlen',
                                 name='plz',
                                 multiple=True,
                                 size=20,
                                 options=self.for_plz(),
                                 tip="Einträge für gewählte PLZ, oder alle Einträge",
                                 ),
                    ]],
            button=h.Button(value="Herunterladen",
                            name='op',
                            tip="Straßenkatalog für gewählte PLZ bzw. insgesamt herunterladen",
                            type='submit',
                            n_col=2,
                            ),
            )
        res = h.Page(
            title='Straßenkatalog exportieren',
            breadcrumbs = (('Administratorhauptmenü', 'menu'),
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
                                     "mit Feldnamen überein", 1, erste_zeile)
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
        "gibt Liste der Zusatzfelder zurück, die teilweise vorhanden sind"
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
            for end in ('trasse', 'traße'):
                if strasse.endswith(end):
                    i = strasse.index(end)
                    strasse = strasse[:i] + 'tr.'
            dic['name'] = strasse
        else:
            self.csv_lese_fehler('Straßenname fehlt', znr, daten)
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
                self.csv_lese_fehler("Es muss entweder für 'von' und für 'bis' einen Wert geben, "
                                     'oder beide müssen leer sein', znr, daten)
            try:
                vn, vb, vg = split_hausnummer(von)
                bn, bb, bg = split_hausnummer(bis)
            except:
                self.csv_lese_fehler('Fehler in Hausnummer', znr, daten)
            if (vn == bn and not vb.upper() <=  bb.upper()) or vn > bn:
                self.csv_lese_fehler("Hausnummer 'von' muss größer sein als 'bis'", znr, daten)
            dic['von'] = "%s%s" % (vn, vb.upper())
            dic['bis'] = "%s%s" % (bn, bb.upper())
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
                feedback1 = """Der vorhandene Straßenkatalog wird
durch die Datensätze der importierten Datei
vollständig ersetzt."""
            else:
                self.session.data['replace'] = False
                feedback1 = """Für diese Postleitzahlen werden die Einträge 
im Straßenkatalog ersetzt."""
            return  h.SubmitOrBack(
                legend='Straßenkatalog übernehmen',
                action='strkatimport',
                method='post',
                hidden=(('strkat_validiert', '1'),
                        ),
                zeilen=("Kein Fehler gefunden. ",
                        "%s Datensätze" % len(strkat_list),
                        "Es gibt Datensätze für die folgenden Postleitzahlen:",) +
                tuple([str(plz) for plz in plzs]) +
                (feedback1, "",
                 "Datensätze übernehmen?",)
                ).display()
        strkat_validiert = self.form.get('strkat_validiert')
        if strkat_validiert:
            strkat_list = self.session.data['strkat']
            plzs = self.session.data['plzs']
            if self.session.data['replace']:
                where = ''
                feedback2 = """Der vorhandene Straßenkatalog wurde
durch die Datensätze der importierten Datei
erfolgreich ersetzt."""
            else:
                where = "plz in (%s)" % ','.join([("'%s'" % p) for p in plzs])
                feedback2 = """Für die genannten Postleitzahlen wurden die Einträge
im Straßenkatalog erfolgreich ersetzt."""
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
                legend="Straßenkatalog erfolgreich importiert",
                zeilen=(feedback2,
                        "%s Datensätze übernommen" % len(strkat_list),
                        'Weiter zum  Hauptmen&uuml ...',
                        ),
                weiter='menu',
                )
            return res.display()
        if self.session.data.get('strkat'):
            del self.session.data['strkat']
            del self.session.data['plzs']
        fname = 'demo_strkatalog.csv'
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
                             '(Kein Unicode; das ist das, '
                             'was im großen und ganzen '
                             'standardmäßig von Open Office und MS Excel erzeugt wird, zumindest '
                             'was die Umlaute und das EssZett betrifft) '
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
        strkatimport = h.FieldsetFormInputTable(
            legend='Straßenkatalog importieren',
            name='strkatimport',action="strkatimport",method="post",
            daten=[[h.RadioItem(label='Nur Einträge für die gegebenen Postleitzahlen ersetzen',
                                name='replace',
                                tip='Es werden nur die Einträge für die in der Importdatei vorkommenden Postleitzahlen ersetzt',
                                value='false',
                                checked=True,
                                ),
                    ],
                   [h.RadioItem(label='Vorhandenen Straßenkatalog vollständig ersetzen',
                                name='replace',
                                tip='Der aktuell vorhanden Straßenkatalog wird vollständig durch den Import ersetzt',
                                value='true',
                                checked=False,
                                ),
                    ],
                   [h.DummyItem()],
                   [h.UploadItem(label='Lokaler Dateiname',
                                 name='datei',
                                 tip='CSV-Datei mit Straßenkatalog',
                                 class_="textboxverylarge",
                                 ),
                    ]],
                button=h.Button(value="Hochladen",
                                name='op',
                                tip="Gewählte Datei mit Straßenkatalog hochladen",
                                type='submit',
                                n_col=2,
                                ),
            )
        res = h.Page(
            title='Straßenkatalog importieren',
            breadcrumbs = (('Administratorhauptmenü', 'menu'),
                           ),
            hidden=(),
            rows=(self.get_hauptmenu(),
                  strkatimport,
                  #hinweise_csv,
                  #hinweise_felder,
                  ),
            )
        return res.display()
