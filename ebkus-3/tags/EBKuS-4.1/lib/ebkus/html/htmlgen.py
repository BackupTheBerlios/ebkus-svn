# coding: latin-1


from  cStringIO import StringIO
from ebkus.config import config
from ebkus import Version

def join(seq):
    #print 'JOIN', seq
    return ''.join([str(i) for i in seq if i])

# abstrakt
class _HTML(object):
    """Abstrakte Oberklasse zur HTML Generierung
    
    Initialisierung immer mit einer Menge von key/values.
    Die in den konkreten Klassen als obligat genannten keys müssen
    immer angegeben werden, die optionalen können angegeben werden.

    __init__ merkt sich nur die übergebenden Parameter.

    Die eigentliche Initialisierung wird von der display-Methode angestoßen
    durch Aufruf der _init-Methode. Diese ruft in der Regel zuerst die _init-Methode
    der Oberklasse auf, und kann dann als letzte das Objekt für das display
    vorbereiten.

    Attribute können immer auch als dict keys abgerufen werden, damit die
    templates funktionieren (__getitem__). Nicht initialisierte Attribute
    liefern immer '' zurück, *keine* Exception.

    Jedes Objekt kann sich als String darstellen (__str__). __str__ ruft dazu
    die display-Methode auf.

    Jede Unterklasse kann ihre eigene display-Methode definieren, wenn das
    default-display nicht ausreicht.
    """
    tip_t = """ title="%(tip)s" onMouseOver="window.status='%(tip)s';return true;" onMouseOut="window.status='';return true;" """

    # können sein: basestring, _HTML-Instanz, Sequenz. Wird automatisch evaluiert
    attribute_to_evaluate = ('content', 'left', 'right', 'rows', 'cells')
    def __init__(self, **kw):
        """Nicht überschreiben."""
        for k,v in kw.items():
            setattr(self, k, v)
    def expand_attr(self, attr, boolean=False):
        """Für ein nicht leeres Attribut 'name' mit dem Wert 'val'
        wird ein zusätzliches Attribut 'name_attr' mit dem Wert
        'name="val"' angelegt.
        Falls boolean True ist, ist val identisch mit dem Namen
        des Attributs (selected, multiple, readonly, ...)
        """
        v = getattr(self, attr)
        if v:
            if boolean:
                setattr(self, attr+'_attr', ' %s="%s" ' % (attr, attr))
            else:
                setattr(self, attr+'_attr', ' %s="%s" ' % (attr, v))
    def _init(self):
        """Jede Unterklasse kann diese Methode zur Initialisierung implementieren, sollte
        aber als erstes super(<klass>, self)._init() aufrufen.
        """
        if self.tip and not(self.tip1 or self.tip2):
            self.tip1 = self.tip2 = self.tip
        for t in ('tip', 'tip1', 'tip2'):
            val = getattr(self, t)
            if val:
                setattr(self, t, self.tip_t % {'tip': val})
        for attr in self.attribute_to_evaluate:
            val = getattr(self, attr)
            if val:
                #print 'HTMLGEN', val
                if isinstance(val, _HTML):
                    setattr(self, attr, val.display())
                elif not isinstance(val, basestring):
                    setattr(self, attr, join(val))
    def __getattr__(self, k):
        return ''
    def __getitem__(self, k):
        return getattr(self, k)
    def __str__(self):
        return self.display()
    def display(self):
        self._init()
        return self.tmpl % self
    def set_form(self):
        """optional: name,method,action,hidden,onSubmit
        setzt self.form_begin und self.form_end
        """
        if not self.hidden:
            self.hidden = ()
        self.expand_attr('onSubmit')
        self.hidden_input = join([
            """<input type="hidden" name="%s" value="%s">\n""" % (name, value)
            for name, value in self.hidden
            ])
        form_begin_t = """<form name="%(name)s" method="%(method)s" action="%(action)s" enctype="multipart/form-data"%(onSubmit_attr)s>
        %(hidden_input)s""" % self
        self.form_begin = form_begin_t % self
        self.form_end = "</form>\n"

# Block
class Base(_HTML):
    """oblig: title, content
    optional: onload, delay, url, weiterleitung, width
    erwartet in content: Block-Element
    liefert string mit kompletter HTML Seite
    """
    width = 760
    weiterleitung_t = """<meta http-equiv="refresh" content="%(delay)s; URL=%(url)s">\n"""
    #help_t = """<script src="/ebkus/ebkus_javascripte/ebkus_help.js" type="text/javascript"></script>\n"""
    #help_t = """<div id="help")s><a href="/ebkus/doc/EBKuS_Handbuch.html#%(help)s" target="_blank">Hilfe</a></div>\n"""
    help_t = """<a href="/ebkus/doc/EBKuS_Handbuch.html#%(help)s" target="_blank">Hilfe</a>"""
    #breadcrumbs_t = """<tr><td class="breadcrumb" align="left">%s</td></tr>"""
    #breadcrumbs_t = """<tr><td>
    #                    <table><tr><td class="breadcrumb" align="left">%s</td>
    #                               <td class="breadcrumb" align="right">%s</td>
    #                    </tr></table></td></tr>"""
    xstatuszeile_t = """
<div id="help">%(help)s</div>
<div id="breadcrumb">%(breadcrumb)s</div>
<div id="instanz">%(instanz)s</div>
<div id="login">%(login)s</div>
<div id="logout"><a href="logout">Abmelden</a></div>
"""
    xstatuszeile_t = """
<table class="breadcrumb" width="100%%"><tr>
<td align="left">%(help)s</tdd>
<td>%(breadcrumb)s</tdd>
<td>%(instanz)s</tdd>
<td>%(login)s</tdd>
<td align="right"><a href="logout">Abmelden</a></td>
"""
    statuszeile_t = """
<table class="breadcrumb" width="100%%"><tr valign="top">
<td width="5%%" align="left">%(help)s</td>
<td width="35%%">%(breadcrumb)s</td>
<td width="25%%">%(instanz)s</td>
<td width="30%%">%(login)s</td>
<td width="8%%" align="right"><a href="logout">Abmelden</a></td>
</tr></table>
"""
    


    def _init(self):
        super(Base, self)._init()
        self.expand_attr('onload')
        if self.weiterleitung:
            self.weiterleitung = self.weiterleitung_t % self
##         if self.help:
##             self.help = self.help_t % self
##         else:
##             self.help = ''
        self.help = self.help_t % self
        if self.breadcrumbs:
            # name, url, falls keine url, nur der Name ohne link
            crumbs = [(entry[1] and '<a href="%s">%s</a>' %
                       (entry[1], entry[0])) or entry[0]
                      for entry in self.breadcrumbs if entry]
            crumbs += [self.title]
            crumbs = ' > '.join(crumbs)
##             crumbs = ' > '.join([(entry[1] and '<a href="%s">%s</a>' %
##                                   (entry[1], entry[0])) or entry[0]
##                                  for entry in self.breadcrumbs if entry])
##             crumbs += ' > %s' % self.title
            # TODO user daten übernehmen
            from ebkus.app.Request import getRequest
            mitarbeiter = getRequest().mitarbeiter
            self.login = "%(vn)s %(na)s (%(ben)s@%(stz__code)s, %(benr__name)s)" % mitarbeiter
            #self.breadcrumb = self.breadcrumbs_t % (crumbs, login)
            self.breadcrumb = crumbs
            self.instanz = "EBKuS %s: %s" % (Version, config.INSTANCE_TITLE)
            self.statuszeile = self.statuszeile_t % self
    tmpl = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
"http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<title> %(title)s </title>
<meta name="robots" content="noindex">
<meta http-equiv="content-type" content="text/html; charset=iso-8859-1">
%(weiterleitung)s<script src="/ebkus/ebkus_javascripte/ebkus_sonstige.js" type="text/javascript"></script>
<link rel="stylesheet" type="text/css" href="/ebkus/ebkus_styles/css_styles.css">
</head>
<body%(onload_attr)s><a name="top"></a>
%(statuszeile)s
<table class="pageframe">
  <tr>
      <td align="center" valign="top">
%(form_begin)s%(content)s%(form_end)s
     </td>
  </tr>
</table>
</body>
</html>
"""
#"

# <tr>-Elemente
class Page(Base):
    """obligat:rows
    erwartet in rows: <tr>
    liefert: string mit komplette HTML-Seite
    """
    def set_content(self):
        tmpl_table = """<table width="100%%" border="0" cellpadding="1">
%s
</table>
"""
        self.content = tmpl_table % join(self.rows)
    def _init(self):
        super(Page, self)._init()
        self.set_content()




# <tr>-Elemente
class FormPage(Page):
    """liefert string mit kompletter HTML-Seite
    """
    def _init(self):
        super(FormPage, self)._init()
        self.set_form()
        

# <td>-Elemente
class Tr(_HTML):
    """obligat: cells
    erwartet in cells: Seq von <td>
    liefert: string mit ein <tr>
    """
    tmpl = "<tr>%(cells)s</tr>\n"
    
# <tr>-Elemente
class Pair(_HTML):
    """left, right
    erwartet in left bzw right: <tr>,
    also z.B. mehrere Fieldsets
    liefert: <tr> mit einer Zelle
    """
    def display(self):
        self._init()
        if self.left or self.right:
            return self.tmpl % self
        else:
            return ''
    tmpl = """<tr><td width="100%%">
  <table width="100%%">
  <tr><td width="50%%"><table width="100%%">
  %(left)s
  </table></td><td width="50%%"><table width="100%%">
  %(right)s
  </table></td></tr>
  </table>
</td></tr>
"""

class Table(_HTML):
    """obligat: rows
    optional: colspan - wird in die einzelne Zelle eingesetzt
    erwartet in rows: <tr>
    liefert: string mit ein <tr>, das eine Zelle enthält
    """
    def _init(self):
        super(Table, self)._init()
        self.expand_attr('colspan')
    tmpl ="""           <tr>
            <td align="center"%(colspan_attr)s>%(fieldset_begin)s%(form_begin)s 
              <table width="100%%" border="0" cellpadding="2">
%(rows)s
              </table>%(form_end)s%(fieldset_end)s
            </td>
          </tr>
"""

    def set_fieldset(self):
        """optional: legend, anchor - Name für ein Sprungziel zur legend
        """
        legend_t = """<legend class="legendtext">%(legend)s</legend>"""
        fieldset_begin_t = """\n<fieldset%(tip)s>%(legend_elem)s"""
        fieldset_end = "</fieldset>\n"
        if self.anchor:
            self.legend = '<a name="%(anchor)s" id="%(anchor)s">%(legend)s</a>' % self
        if self.legend:
            self.legend_elem = legend_t % self
        self.fieldset_begin = fieldset_begin_t % self
        self.fieldset_end = fieldset_end



class Fieldset(Table):
    def _init(self):
        super(Fieldset, self)._init()
        self.set_fieldset()
        
class FieldsetForm(Table):
    """liefert ein Fieldset dessen Inhalt von einer form eingerahmt ist.
    """
    def _init(self):
        super(FieldsetForm, self)._init()
        self.set_fieldset()
        self.set_form()

class DataTable(object):
    """oblig: daten oder button oder buttons oder empty_msg
    optional: daten_before_headers - Zeilen, die vor headers eingefügt werden
              headers - Spaltenüberschriften, strings
              no_button_if_empty
    erwartet in headers: Seq von string
    erwartet in daten: Seq von Seq von <td>
    liefert string mit ein oder mehrere <tr>

    Items in Daten müssen alle aus einer td bestehen, sonst stehen die
    header nicht an der richtigen Stelle!!
    """
    daten_before_headers = ()
    headers = ()
    noheaders = 0 # Anzahl der Spalten am Anfang ohne header
                  # alternativ zum Auszählen der Icons, s.u.
    daten = ()
    button = None
    empty_msg = None
    def set_rows(self):
        max_cols = 0 # enthält am Ende die Zahl der Zeile mit den meisten Spalten
                 # Damit kann colspan für button gesetzt werden.
        # TODO cols wird nicht in allen Fällen richtig gesetzt
        # (keine header, keine daten)
        has_button = (self.button or self.buttons)
        if not self.daten:
            # Kein button wenn leer und no_button_if_empty gesetzt
            has_button = not self.no_button_if_empty
        buf = StringIO()
        pr = buf.write
        if self.daten_before_headers:
            for zeile in self.daten_before_headers:
                if zeile:
                    cols = 0 
                    pr("<tr>")
                    for spalte in zeile:
                        if spalte:
                            cols += spalte.n_col
                            pr(str(spalte))
                    pr("</tr>\n")
                    max_cols = max(max_cols, cols)
        if self.daten and self.headers:
            cols = 0
            if self.noheaders:
                for i in range(self.noheaders):
                    pr("<th></th>")
                    cols += 1
            else:
                for i in self.daten[0]:
                    # leere Header einfügen entsprechend der Anzahl der Icons
                    if isinstance(i, (Icon, IconDead)):
                        pr("<th></th>")
                        cols += i.n_col
                    else:
                        break
            for h in self.headers:
                cols += 1
                if h != '':
                    h += ':'
                pr("<th>%s</th>" % h)
            pr("</tr>\n")
            max_cols = max(max_cols, cols)
        if self.daten:
            for zeile in self.daten:
                if zeile:
                    cols = 0
                    pr("<tr>")
                    for spalte in zeile:
                        if spalte:
                            pr(str(spalte))
                    pr("</tr>\n")
                    max_cols = max(max_cols, cols)
        if has_button:
            if self.button:
                #self.button.set_n_col(cols)
                self.button.n_col = max(self.button.n_col, max_cols)
                pr("<tr>")
                pr(str(self.button))
                pr("</tr>\n")
            elif self.buttons:
                # Wenn mehrere Button reinsollen, besser eine eigene Tabelle
                class _TableDataTable(Table, DataTable):
                    def _init(self):
                        super(_TableDataTable, self)._init()
                        self.set_rows()
                button_zeile = _TableDataTable(
                    daten=[self.buttons],
                    colspan=max(1, max_cols),
                    )
                pr(str(button_zeile))
        if not self.daten and self.empty_msg and not has_button:
            self.colspan = max(1, max_cols)
            pr("<tr>")
            pr("""<td colspan="%(colspan)s">%(empty_msg)s</td>""" % self)
            pr("</tr>\n")
        self.rows = buf.getvalue()


class InputTable(object):
    """oblig: daten
    optional: button
    erwartet in daten: Seq von Seq von <td>
    Liefert string mit ein oder mehrere <tr>
    """
    def set_rows(self):
        buf = StringIO()
        pr = buf.write
        max_cols = 0 # enthält am Ende die Zahl Spalten
        for zeile in self.daten:
            if zeile:
                cols = 0
                pr("<tr>")
                for spalte in zeile:
                    if spalte:
                        cols += spalte.n_col
                        pr(str(spalte))
                pr("</tr>\n")
                max_cols = max(max_cols, cols)
        if self.button:
            self.button.n_col = max(self.button.n_col, max_cols)
            pr("<tr>")
            pr(str(self.button))
            pr("</tr>\n")
        self.rows = buf.getvalue()
                            

class FieldsetDataTable(Fieldset, DataTable):
    """liefert ein Fieldset dessen Inhalt von einer Datatable aufgefüllt wird.
    """
    def _init(self):
        super(FieldsetDataTable, self)._init()
        self.set_rows()
        
class FieldsetInputTable(Fieldset, InputTable):
    """liefert ein Fieldset dessen Inhalt von einer InputTable aufgefüllt wird.
    """
    def _init(self):
        super(FieldsetInputTable, self)._init()
        self.set_rows()
        
class FieldsetFormInputTable(FieldsetForm, InputTable):
    """liefert ein Fieldset dessen Inhalt von einer InputTable aufgefüllt wird
    und von einer Form umgeben ist.
    """
    def _init(self):
        super(FieldsetFormInputTable, self)._init()
        self.set_rows()

class FieldsetFormDataTable(FieldsetForm, DataTable):
    """liefert ein Fieldset dessen Inhalt von einer DataTable aufgefüllt wird
    und von einer Form umgeben ist.
    """
    def _init(self):
        super(FieldsetFormDataTable, self)._init()
        self.set_rows()

class Meldung(FormPage):
    """obligat: legend, zeilen
    optional: title
    """
    onClick = "javascript:history.back()"
    empty_row = '<tr><td>&nbsp;&nbsp;&nbsp;&nbsp;</td></tr>'
    def _init(self):
        if self.weiter:
            self.onClick = "go_to_url('%s')" % self.weiter
        self.set_rows()
        super(Meldung, self)._init()
        if not self.title:
            self.title = self.legend
    def set_rows(self):
        rows = [self.empty_row]*3
        rows += ['<tr><td align="center">%s</td></tr>' % z for z in self.zeilen]
        rows += [self.empty_row]*3
        button = Button(value="Ok",
                        onClick=self.onClick,
                        tip="Zurück",
                        )
        rows.append('<tr>%s</tr>' % str(button)) 
        self.rows = (Fieldset(legend=self.legend,
                              rows=rows,),
                     )

class SubmitOrBack(FormPage):
    """obligat: legend, zeilen
    optional: title
    optional: alle Parameter von Form
    """
    onclick_abbrechen = "javascript:history.back()"
    onclick_submit = ''
    
    empty_row = '<tr><td colspan="2">&nbsp;&nbsp;&nbsp;&nbsp;</td></tr>'
    def _init(self):
        self.set_rows()
        super(SubmitOrBack, self)._init()
        if not self.title:
            self.title = self.legend
    def set_rows(self):
        rows = [self.empty_row]*3
        rows += ['<tr><td colspan="2">%s</td></tr>' % z for z in self.zeilen]
        rows += [self.empty_row]*3
        button_back = Button(value="Abbrechen",
                             onClick=self.onclick_abbrechen,
                             tip="Aktion nicht durchführen",
                             )
        button_submit = Button(value="Ok",
                               onClick=self.onclick_submit,
                               type='submit',
                               tip="Aktion durchführen",
                               )
        rows.append('<tr>%s%s</tr>' % (str(button_submit), str(button_back)))
        self.rows = (Fieldset(legend=self.legend,
                              rows=rows,),
                     )

class Item(_HTML):
    """optional: class_, n_col, n_label
    
    Jede Instanz dieser Klasse generiert 1 oder mehrere td-Elemente.
    n_td die Zahl der td-Elemente
    n_col die Zahl der überspannten Zellen
    n_label damit kann bei Input-Items auch der label-Teil mehrere Zellen überspannen
    colspan der colspan Wert für die Zelle, die mehrere Spalten überspannen kann
    Es gilt: n_col = n_td + colspan - 1
    """
    n_td = 1 # Anzahl der td-Elemente, colspan kann größer sein
    n_col = 1 # Anzahl der überspannten Zellen

    def _init(self):
        super(Item, self)._init()
        if self.n_col != self.n_td:
            if self.n_label:
                self.label_colspan_attr = ' colspan="%s" ' % self.n_label
                diff = self.n_col - self.n_td - self.n_label + 1
            else:
                diff = self.n_col - self.n_td
            if diff > 0:
                self.colspan = diff + 1
                self.expand_attr('colspan')
        self.expand_attr('onBlur')
        self.expand_attr('align')
        self.expand_attr('onClick')
        self.expand_attr('onChange')
        self.expand_attr('width')
        self.expand_attr('target')
        self.expand_attr('rowspan')

class Dummy(Item):
    tmpl = """<td%(tip)s%(label_width_attr)s%(colspan_attr)s%(rowspan_attr)s></td>"""

class Icon(Item):
    href = ''
    onClick = ''
    tmpl = """<td width="1%%"%(colspan_attr)s%(align_attr)s%(rowspan_attr)s>
      <a href="%(href)s"%(onClick_attr)s%(target_attr)s>
        <img border="0" src="%(icon)s"%(tip)s>
      </a>
</td>
"""
class IconDead(Item):
    tmpl = """<td width="1%%"%(colspan_attr)s%(align_attr)s%(rowspan_attr)s>
        <img border="0" 
             src="%(icon)s"%(tip)s>
    </td>
"""

class String(Item):
    """
    obligat: string
    """
    class_ = 'tabledata'
    tmpl = """<td class="%(class_)s"%(colspan_attr)s%(tip)s%(align_attr)s%(rowspan_attr)s>%(string)s</td>"""
    
class Link(Item):
    """
    obligat: string, url
    """
    class_ = 'tabledata'
    tmpl = """<td class="%(class_)s"%(colspan_attr)s%(tip)s%(align_attr)s%(rowspan_attr)s><a href="%(url)s"%(target_attr)s>%(string)s</a></td>"""
    

class Datum(Item):
    """
    obligat: date ODER year, month, day, 
    erwartet in date: ebapi.Date Instanz
    ohne Daten oder year=0 wird 'offen' in die Zelle geschrieben.
    Tag kann weggelassen werden, dann werden nur Monat und Jahr geschrieben.
    year, month, day
    """
    year = ''
    day = ''
    tmpl = """<td class="tabledata"%(colspan_attr)s%(rowspan_attr)s>%(datum)s</td>"""
    def _init(self):
        super(Datum, self)._init()
        if self.date:
            self.year = self.date.year
            self.month = self.date.month
            self.day = self.date.day
        if self.time and not self.time.empty:
            self.hours = self.time.hours
            self.minutes = self.time.minutes
        if not self.year:
            datum = "offen"
        else:
            datum = ''
            if self.day:
                datum = "%(day)02d<B>.</B>" % self
            datum += "%(month)02d<B>.</B>%(year)s" % self
            if self.hours:
                datum += "&nbsp;%(hours)s<B>:</B>%(minutes)s" % self
        self.datum = datum

class Button(Item):
    """obligat: value
    optional: onClick, type, class_, name
    """
    class_ = 'button'
    type = 'button'
    align = 'center'
    tmpl = """<td class="buttoncell"%(colspan_attr)s%(align_attr)s%(width_attr)s%(rowspan_attr)s>
      <input type="%(type)s" 
       class="%(class_)s" name="%(name)s"
       value="%(value)s"%(onClick_attr)s%(tip)s>
     </td>
"""

class SelectGoto(Item):
    """name, options"""
    class_='listbox130'
    tmpl = """<td%(tip)s%(colspan_attr)s%(align_attr)s%(rowspan_attr)s>
     <select size="1" 
             name="%(name)s" 
             onChange="go_to_url(this.form.%(name)s.options[this.form.%(name)s.options.selectedIndex].value)"           
             class="%(class_)s">
     %(options)s
     </select>
     </td>
"""

class InputItem(Item):
    """Items, die der Eingabe von Daten dienen.
    optional: label, ohne label wird kein ':' geschrieben
              label_width, damit können Eingabeelemente positioniert werden
                    auch wenn keine labels da sind, oder sie in verschieden
                    Fieldsets stehen
              label_class, die Klasse der ersten Zelle
              class_, die Klasse der zweiten Zelle 
              readonly, disabled
    InputItems haben in der Regel zwei <td> Elemente (label und Eingabeelement)
    """
    n_td = 2
    n_col = 2
    boolean_attrs = ('multiple', 'readonly', 'disabled', 'checked')
    label_class='labeltext'
    class_='textbox'
    def _init(self):
        super(InputItem, self)._init()
        self.id = self.name # Verknüpfung label - input-element
        for a in self.boolean_attrs:
            self.expand_attr(a, boolean=True)
        if self.label:
            self.label += ':'
        if self.label_width:
            self.label_width_attr = ' width="%s" ' % self.label_width
        if self.value == None:
            self.value = ''

class DummyItem(InputItem):
    """optional: name, value
    damit wird ein hidden input gesetzt.
    """
    def _init(self):
        super(InputItem, self)._init()
        if self.name:
            self.hidden_attr = '<input type="hidden" name="%(name)s" value="%(value)s">' 
    tmpl = """<td class="%(label_class)s" %(tip)s%(label_width_attr)s%(rowspan_attr)s%(label_colspan_attr)s></td><td class="%(class_)s"%(tip)s%(colspan_attr)s%(rowspan_attr)s>%(hidden_attr)s</td>"""
    
class TextItem(InputItem):
    """label,name,value
    optional: readonly, icon
    """
    class_ = 'textbox120'
    maxlength = 1024
    def __init__(self, **kw):
        super(TextItem, self).__init__(**kw)
        # muss *vor* _init gemacht werden:
        if self.icon:
            n_col = 3
    tmpl = """<td align="right" class="%(label_class)s"%(label_width_attr)s%(rowspan_attr)s%(label_colspan_attr)s>
    <label for="%(id)s">%(label)s</label></td>
    <td align="left"%(colspan_attr)s%(tip)s%(rowspan_attr)s>
    <input type="text" name="%(name)s" value="%(value)s" id="%(id)s"
    class="%(class_)s" maxlength="%(maxlength)s"%(onBlur_attr)s%(readonly_attr)s>
    </td>%(icon)s
"""

class TextareaItem(InputItem):
    """label,name,value,rows,cols
    optional: readonly
    """
    class_ = 'textbox120'
    class_ = 'textareanormal'
    tmpl = """<td align="right" class="%(label_class)s"%(label_width_attr)s%(rowspan_attr)s%(label_colspan_attr)s>
    <label for="%(id)s">%(label)s</label></td>
    <td align="left"%(colspan_attr)s%(tip)s%(rowspan_attr)s>
    <textarea name="%(name)s" id="%(id)s" rows="%(rows)s" cols="%(cols)s"
    class="%(class_)s" %(onBlur_attr)s%(readonly_attr)s>%(value)s</textarea>
    </td>
"""



class UploadItem(InputItem):
    """obligatorisch: label,name
    """
    tmpl = """<td align="right" class="%(label_class)s"%(label_width_attr)s%(rowspan_attr)s%(label_colspan_attr)s>
    <label for="%(id)s">%(label)s</label></td>
    <td %(colspan_attr)s%(tip)s%(rowspan_attr)s>
    <input type="file" name="%(name)s" id="%(id)s" class="%(class_)s"%(onBlur_attr)s>
    </td>
"""

class CheckItem(InputItem):
    """label,name,value
    optional: readonly, checked, onClick
    """
    class_ = 'textbox'
    tmpl = """
    <td align="right" class="%(label_class)s"%(label_width_attr)s%(tip1)s%(label_colspan_attr)s>
    <label for="%(id)s">%(label)s</label></td>
    <td class="%(class_)s" align="left"%(tip2)s%(colspan_attr)s>
    <input type="checkbox" name="%(name)s" value="%(value)s" id="%(id)s"
     %(checked_attr)s%(readonly_attr)s%(onClick_attr)s%(onChange_attr)s>
    </td>
"""

class RadioItem(InputItem):
    """label,name,value
    optional: readonly, checked
    """
    class_ = 'textbox'
    def _init(self):
        super(RadioItem, self)._init()
        if self.label[-1] == ':':
            self.label = self.label[:-1]
    tmpl = """
    <td align="right"%(tip)s%(colspan_attr)s>
    <input type="radio" name="%(name)s" value="%(value)s" id="%(id)s"
     %(checked_attr)s%(readonly_attr)s></td>
    <td align="left" class="%(label_class)s"%(label_width_attr)s%(tip)s%(label_colspan_attr)s>
    <label for="%(id)s">%(label)s</label></td>
"""

class SelectItem(InputItem):
    """label,name,options
    optional: class_, multiple, label_width, size, nolabel, onChange
    """
    class_ = 'listbox120'
    def _init(self):
        if self.nolabel:
            self.n_td = 1
        if self.readonly:
            self.disabled = True
        super(SelectItem, self)._init()
        if self.size and int(self.size) > 1:
            self.expand_attr('size')
    def display(self):
        self._init()
        if self.nolabel:
            return self.tmpl_i % self
        else:
            return (self.tmpl_l + self.tmpl_i) % self
    tmpl_l = """<td align="right" class="%(label_class)s"%(label_width_attr)s%(rowspan_attr)s%(label_colspan_attr)s>
    <label for="%(id)s">%(label)s</label></td>
"""
    tmpl_i = """<td%(colspan_attr)s align="left" %(tip)s%(rowspan_attr)s>
      <select name="%(name)s"%(size_attr)s%(onChange_attr)s class="%(class_)s"%(multiple_attr)s%(disabled_attr)s>
    %(options)s
      </select></td>
"""

class DatumItem(InputItem):
    """label,name,(year,month,day oder date)
    optional: noday - Kein input-Feld für den Tag
              time, hour, minute
    """
    def _init(self):
        super(DatumItem, self)._init()
        if self.date:
            if self.date.year == 0:
                self.year = self.month = self.day = ''
            else:
                self.year = self.date.years
                self.month = self.date.months
                self.day = self.date.days
        if self.time:
            self.hour = self.time.hours
            self.minute = self.time.minutes
        self.dname = self.name + 'd'
        self.mname = self.name + 'm'
        self.yname = self.name + 'y'
        self.hname = self.name + 'h'
        self.minname = self.name + 'min'
    def display(self):
        self._init()
        if self.noday:
            self.day_input = ''
        else:
            self.day_input = self.day_t % self
        if self.time:
            self.time_input = self.uhrzeit_t % self
        return self.tmpl % self
    day_t = """<input id="%(name)s" type="text" value="%(day)s" class="textbox13"
             size=2 maxlength=2 name="%(dname)s"%(readonly_attr)s><b>.</b>"""
    uhrzeit_t = """&nbsp;
       <input id="%(name)s" type="text" value="%(hour)s" class="textbox13"
             size=2 maxlength=2 name="%(hname)s"%(readonly_attr)s><b>:</b><input
             id="%(name)s" type="text" value="%(minute)s" class="textbox13"
             size=2 maxlength=2 name="%(minname)s"%(readonly_attr)s>
      """
    tmpl = """    <td align="right" class="%(label_class)s"%(label_width_attr)s%(label_colspan_attr)s>
    <label for="%(id)s">%(label)s</label></td>
    <td align="left"%(tip)s%(colspan_attr)s><nobr>%(day_input)s<input
    type="text" value="%(month)s" class="textbox13" size=2 maxlength=2
             name="%(mname)s"%(readonly_attr)s><b>.</b><input
             type="text" value="%(year)s" class="textbox30" size=4 maxlength=4
             name="%(yname)s"%(readonly_attr)s>%(time_input)s
    </nobr></td>
"""

class SpeichernZuruecksetzenAbbrechen(_HTML):
    """
    optional: abbrechen - anstatt history.back() eine URL
              name - für submit
              value- für submit
    """
    value = 'Speichern'
    onclick_abbrechen = "javascript:history.back()"
    onclick_submit = ''
    value_abbrechen = 'Abbrechen'
    def display(self):
        self._init()
        if self.abbrechen:
            self.onclick_abbrechen = "go_to_url('%(abbrechen)s')" % self
        return Fieldset(rows=self.tmpl % self).display()
    
    tmpl = """
                <tr height="40">
                  <td width="33%%" align="center" valign="middle">
                    <input type="submit" name="%(name)s" value="%(value)s" class="button"
                     onClick="%(onclick_submit)s">
                  </td>
                  <td align="center" valign="middle" width="33%%">
                    <input type="reset" value="Zur&uuml;cksetzen" class="button">
                  </td>
                  <td align="center" valign="middle" width="34%%">
                    <input type="button" value="%(value_abbrechen)s" class="button" onClick="%(onclick_abbrechen)s">
                  </td>
                </tr>
"""
                  
