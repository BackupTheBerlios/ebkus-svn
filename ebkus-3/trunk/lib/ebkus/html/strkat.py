# coding: latin-1
import re
from ebkus.app import Request
from ebkus.app.ebapi import StrassenkatalogList, StrassenkatalogNeuList, EE, cc
from ebkus.app_surface.strkat_templates import *
from ebkus.config import config

import ebkus.html.htmlgen as h

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
        such_muster = True
        if strassen_list == None:
            such_muster = False
        elif len(strassen_list) < 1:
            nichts_gefunden = True
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
            tmpl = '<option value="%s">' % value
            tmpl += '%(option_name2)s</option>'
            optionale_suchfelder = config.STRASSENSUCHE.split()
            if config.STRASSENKATALOG_VOLLSTAENDIG:
                hausnummern = ['hausnr_ohne_nullen',]
            else:
                hausnummern = ['von2', 'bis2', 'gu2',]
            felder = ['name',] +  hausnummern + ['plz'] + optionale_suchfelder
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
                options.append(tmpl % element)
        return '\n'.join(options)
        
def get_strassen_list(form):
    """Rückgabe: Exception: bei Fehlern in den Suchstrings
                 None: Keine Suchstrings
                 Sonst: die Liste der Ergebnisse, die leer sein kann"""
    #print 'GET_STRASSEN_LIST FORM', form
    str_id = form.get('strid')
    str_felder = ('ort', 'plz', 'bezirk', 'samtgemeinde', 'ortsteil')
    where = []
    if str_id:
        where.append("id = %s" % str_id)
    for f in str_felder:
        val = form.get(f, '')
        if val:
            where.append("%s like '%s%%'" % (f, val))
    str = check_strasse(form.get('str', ''))
    if str:
        where.append("name like '%s%%'" % str)
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
    """liefert Element aus dem Strassenkatalog, passend zu data,
    oder {}
    """
    strasse = {}
    if (data.get('lage') == cc('lage', '0') and
        data['ort'] and  data['plz']):
        # innerhalb der Geltung des Strassenkatalogs
        strassen_list = get_strassen_list(data)
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

