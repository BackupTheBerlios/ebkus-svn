# coding: latin-1


from  cStringIO import StringIO

def join(seq):
    return ''.join([str(i) for i in seq if i])

class _HTML(object):
    """Abstrakte Oberklasse zur HTML Generierung
    
    Initialisierung immer mit einer Menge von key/values.
    Die in den konkreten Klassen als obligat genannten keys müssen
    immer angegeben werden, die optionalen können angegeben werden.

    __init__ merkt sich nur die übergebenden Parameter.

    Die eigentliche Initialisierung wird von der display-Methode angestoßen
    durch Aufruf der _init-Methode. Diese ruft immer zuerst die _init-Methode
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


    def __init__(self, **kw):
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
        __init__ sollte nicht überschrieben werden.
        """
        if self.tip:
            self.tip = self.tip_t % self
    def __getattr__(self, k):
        return ''
    def __getitem__(self, k):
        return getattr(self, k)
    def __str__(self):
        return self.display()
    def display(self):
        self._init()
        return self.tmpl % self
##     def display_tr(self, cells):
##         return "<tr>%s</tr>\n" % ''.join([str(c) for c in cells])
##     def display_tds(self, contents):
##         pass

class Base(_HTML):
    """oblig: title, content
    optional: onload, delay, url, weiterleitung
    erwartet in content: string von Block-Element
    liefert string mit kompletter HTML Seite
    """
    onload = ''
    delay = ''
    url = ''
    help = ''
    weiterleitung_t = """<meta http-equiv="refresh" content="%(delay)s; URL=%(url)s">\n"""
    help_t = """<script src="/ebkus/ebkus_javascripte/ebkus_help.js" type="text/javascript"></script>\n"""
    def _init(self):
        super(Base, self)._init()
        if self.weiterleitung:
            self.weiterleitung = self.weiterleitung_t % self
        if self.help:
            self.help = self.help_t
    tmpl = """<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
"http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<title> %(title)s </title>
<meta name="robots" content="noindex">
<meta http-equiv="content-type" content="text/html; charset=iso-8859-1">
%(weiterleitung)s<script src="/ebkus/ebkus_javascripte/ebkus_sonstige.js" type="text/javascript"></script>
%(help)s<link rel="stylesheet" type="text/css" href="/ebkus/ebkus_styles/css_styles.css">
</head>
<body %(onload)s>
<table width="800" align="center">
  <tr>
      <td align="center" valign="top">
%(content)s
     </td>
  </tr>
</table>
</body>
</html>
"""
#"

class Meldung(_HTML):
    """obligat: legend, zeilen
    optional: titel
    """
    empty_row = '<tr><td>&nbsp;&nbsp;&nbsp;&nbsp;</td></tr>'
    def _init(self):
        super(Meldung, self)._init()
        if not self.titel:
            self.titel = self.legend
    def display(self):
        self._init()
        rows = [self.empty_row]*3
        rows += ['<tr><td>%s</td></tr>' % z for z in self.zeilen]
        rows += [self.empty_row]*3
        button = Button(value="&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Ok&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;",
                        onClick="javascript:history.back()",
                        tip="Zurück",
                        )
        rows.append('<tr>%s</tr>' % str(button)) 
        form = FormPage(
            title=self.titel,
            rows=(Fieldset(legend=self.legend,
                           rows=rows,),
                  )
            )
        return form.display()
           
class FormPage(_HTML):
    """obligat:title, rows ODER content
    optional: name,method,action,hidden
    erwartet in rows: Seq von <tr>
    liefert: string mit komplette HTML-Seite
    """
    name = method = action = ''
    hidden = ()
    def display(self):
        self._init()
        form = Form(
            name=self.name,
            action=self.action,
            method=self.method,
            hidden=self.hidden,
            rows=self.rows,
            )
        page = Base(
            title=self.title,
            content=form.display(),
            )
        return page.display()


class Tr(_HTML):
    """obligat: cells
    erwartet in cells: Seq von <td>
    liefert: string mit ein <tr>
    """
    tmpl = "<tr>%(content)s</tr>\n"
    def display(self):
        self._init()
        if not self.content:
            self.content = join(self.cells)
        return self.tmpl % self
    
class Form(_HTML):
    """oblig: rows ODER content
    optional: name,method,action,hidden
    erwartet in rows: Seq von <tr>
    liefert: string mit ein <form>
    """
    name = method = action = ''
    hidden = ()
    tmpl = """<form name="%(name)s" method="%(method)s" action="%(action)s">
%(hidden_input)s
<table border="0" cellpadding="1" width="95%%">
%(content)s
</table>\n</form>
"""
    def _init(self):
        super(Form, self)._init()
        self.hidden_input = join([
            """<input type="hidden" name="%s" value="%s">\n""" % (name, value)
            for name, value in self.hidden
            ])
        if not self.content:
            self.content = join(self.rows)
        
class Fieldset(_HTML):
    """obligat: legend, rows ODER content
    erwartet in rows: Seq  <tr>
    liefert: string mit ein <tr>

    """
    legend = ''
    def _init(self):
        super(Fieldset, self)._init()
        if not self.content:
            self.content = join(self.rows)
    tmpl ="""           <tr>
            <td align="center"> 
              <fieldset>
              <legend class="legendtext">%(legend)s</legend>
              <table width="90%%" border="0" cellpadding="2">
%(content)s
              </table>
              </fieldset> 
            </td>
          </tr>
"""
              
class Pair(_HTML):
    """left, right
    erwartet in left bzw right: String von <tr>
    liefert: <tr>
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
  

class DataTable(_HTML):
    """oblig: daten oder button oder empty_msg
    optional: headers
    erwartet in headers: Seq von string
    erwartet in daten: Seq von Seq von <td>
    liefert string mit ein oder mehrere <tr>
    """
    daten = ()
    headers = ()
    button = None
    empty_msg = None
    def display(self):
        self._init()
        cols = 0 # enthält am Ende die Zahl Spalten
        buf = StringIO()
        pr = buf.write
        if self.daten and self.headers:
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
        for zeile in self.daten:
            pr("<tr>")
            for spalte in zeile:
                pr(str(spalte))
            pr("</tr>\n")
        if self.button:
            #self.button.set_n_col(cols)
            self.button.n_col = cols
            pr("<tr>")
            pr(str(self.button))
            pr("</tr>\n")
        elif not self.daten and self.empty_msg:
            self.colspan = cols
            pr("<tr>")
            pr("""<td colspan="%(colspan)s">%(empty_msg)s</td>""" % self)
            pr("</tr>\n")
        return buf.getvalue()

class InputTable(_HTML):
    """oblig: daten
    optional: button
    erwartet in daten: Seq von Seq von <td>
    Liefert string mit ein oder mehrere <tr>
    """
    def display(self):
        self._init()
        buf = StringIO()
        pr = buf.write
        cols = 0 # enthält am Ende die Zahl Spalten
        
        if self.daten:
            for spalte in self.daten[0]:
                cols += spalte.n_col
        for zeile in self.daten:
            pr("<tr>")
            for spalte in zeile:
                pr(str(spalte))
            pr("</tr>\n")
        if self.button:
            #self.button.set_n_col(cols)
            self.button.n_col = cols
            pr("<tr>")
            pr(str(self.button))
            pr("</tr>\n")
        return buf.getvalue()
                            
class FieldsetDataTable(DataTable):
    legend = ''
    def display(self):
        self._init()
        return Fieldset(legend=self.legend,
                        content=DataTable.display(self)).display()

class FieldsetInputTable(InputTable):
    legend = ''
    def display(self):
        self._init()
        return Fieldset(legend=self.legend,
                        content=InputTable.display(self)).display()

class Item(_HTML):
    """optional: class_, n_col
    
    Jede Instanz dieser Klasse generiert 1 oder mehrere td-Elemente.
    n_td die Zahl der td-Elemente
    n_col die Zahl der überspannten Zellen
    colspan der colspan Wert für die Zelle, die mehrere Spalten überspannen kann
    Es gilt: n_col = n_td + colspan - 1
    """
    n_td = 1 # Anzahl der td-Elemente, colspan kann größer sein
    n_col = 1 # Anzahl der überspannten Zellen

    def _init(self):
        super(Item, self)._init()
        if self.n_col != self.n_td:
            self.colspan = self.n_col - self.n_td + 1
            self.expand_attr('colspan')
        self.expand_attr('onBlur')
##     def set_n_col(self, val):
##         self.n_col = val
##         if val != self.n_td:
##             self.colspan = self.n_col - self.n_td + 1
##             self.expand_attr('colspan')

class Icon(Item):
    href = ''
    onClick = ''
    tmpl = """<td width="1%%"%(colspan_attr)s>
      <a
         href="%(href)s"
         onClick="%(onClick)s"
      >
        <img border="0" 
             src="%(icon)s"%(tip)s>
      </a>
</td>
"""
class IconDead(Item):
    tmpl = """<td width="1%%"%(colspan_attr)s>
        <img border="0" 
             src="%(icon)s"%(tip)s>
    </td>
"""

class String(Item):
    """
    obligat: string
    """
    class_ = 'tabledata'
    tmpl = """<td class="%(class_)s"%(colspan_attr)s>%(string)s</td>"""
    
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
    tmpl = """<td class="tabledata"%(colspan_attr)s>%(content)s</td>"""
    def _init(self):
        super(Datum, self)._init()
        if self.date:
            self.year = self.date.year
            self.month = self.date.month
            self.day = self.date.day
        if not self.year:
            content = "offen"
        else:
            content = ''
            if self.day:
                content = "%(day)s<B>.</B>" % self
            content += "%(month)s<B>.</B>%(year)s" % self
        self.content = content

class Button(Item):
    """obligat: value, onClick
    """
    tmpl = """<td class="buttoncell" align="center" %(colspan_attr)s>
      <input type="button" 
       class="button"
       value="%(value)s"
       onClick="%(onClick)s"%(tip)s>
     </td>
"""

class SelectGoto(Item):
    """name, options"""
    tmpl = """<td%(tip)s%(colspan_attr)s>
     <select size="1" 
             name="%(name)s" 
             onChange="go_to_url(this.form.%(name)s.options[this.form.%(name)s.options.selectedIndex].value)"           
             class="listbox130">
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
              readonly
    InputItems haben in der Regel zwei <td> Elemente (label und Eingabeelement)
    """
    n_td = 2
    n_col = 2
    boolean_attrs = ('multiple', 'readonly', 'checked')
    def _init(self):
        super(InputItem, self)._init()
        self.id = self.name # Verknüpfung label - input-element
        for a in self.boolean_attrs:
            self.expand_attr(a, boolean=True)
        if self.label:
            self.label += ':'
        if self.label_width:
            self.label_width_attr = ' width="%s" ' % self.label_width
class DummyItem(Item):
    tmpl = """<td%(tip)s%(label_width_attr)s></td><td%(tip)s%(colspan_attr)s></td>"""
    
class TextItem(InputItem):
    """label,name,value
    optional: readonly, icon
    """
    class_ = 'textbox120'
    maxlength = 50
    def _init(self):
        super(TextItem, self)._init()
        if self.icon:
            self.iconcell = str(self.icon)
            n_col = 3
    tmpl = """<td align="right" class="labeltext"%(label_width_attr)s>
    <label for="%(id)s">%(label)s</label></td>
    <td align="left"%(colspan_attr)s%(tip)s>
    <input type="text" name="%(name)s" value="%(value)s" id="%(id)s"
    class="%(class_)s" maxlength="%(maxlength)s"%(onBlur_attr)s%(readonly_attr)s>
    </td>%(iconcell)s
"""

class CheckItem(InputItem):
    """label,name,value
    optional: readonly, checked
    """
    class_ = 'textbox'
    tmpl = """
    <td align="right" class="labeltext"%(label_width_attr)s>
    <label for="%(id)s">%(label)s</label></td>
    <td align="left"%(tip)s%(colspan_attr)s>
    <input type="checkbox" name="%(name)s" value="%(value)s" id="%(id)s"
     %(checked_attr)s%(readonly_attr)s>
    </td>
"""


class SelectItem(InputItem):
    """label,name,options
    optional: class_, multiple, label_width
    """
    class_ = 'listbox120'
    def _init(self):
        super(SelectItem, self)._init()
        if self.size and int(self.size) > 1:
            self.expand_attr('size')
            
    tmpl = """<td align="right" class="labeltext"%(label_width_attr)s>
    <label for="%(id)s">%(label)s</label></td>
    <td align="left"%(tip)s%(colspan_attr)s>
      <select name="%(name)s"%(size_attr)sclass="%(class_)s"%(multiple_attr)s%(readonly_attr)s>
    %(options)s
      </select></td>
"""

class DatumItem(InputItem):
    """label,name,(year,month,day oder date)"""
    def _init(self):
        super(DatumItem, self)._init()
        if self.date:
            self.year = self.date.year or ''
            self.month = self.date.month or ''
            self.day = self.date.day or ''
        self.dname = self.name + 'd'
        self.mname = self.name + 'm'
        self.yname = self.name + 'y'
    tmpl = """    <td align="right" class="labeltext"%(label_width_attr)s>
    <label for="%(id)s">%(label)s</label></td>
    <td align="left"%(tip)s%(colspan_attr)s>
      <input id="%(name)s" type="text" value="%(day)s" class="textboxsmall"
             size=2 maxlength=2 name="%(dname)s"%(readonly_attr)s>
      <b>.</b>
      <input type="text" value="%(month)s" class="textboxsmall" size=2 maxlength=2
             name="%(mname)s"%(readonly_attr)s>
      <b>.</b>
      <input type="text" value="%(year)s" class="textboxmid" size=4 maxlength=4
             name="%(yname)s"%(readonly_attr)s>
    </td>
"""

class Klientendaten(_HTML):
    """legend, akte, button
    liefert: string von <tr>
    """
    def display(self):
        self._init()
        content = self.tmpl % self.akte
        if self.button:
            self.button.n_col = 6 
            content += Tr(cells=(self.button,)).display()
        return Fieldset(legend=self.legend, content=content).display()
    tmpl = """<tr>
          <td align="right" class="labeltext">Vorname:</td>
          <td>
            <input type="text"  value="%(vn)s" size="14" class="textbox" readonly>
          </td>
          <td class="labeltext" align="right">Strasse:</td>
          <td>
            <input type="text" value="%(str)s %(hsnr)s" size="14" class="textbox" readonly>
          </td>
          <td class="labeltext" align="right">Wohnt bei:</td>
          <td>
            <input type="text" value="%(fs__name)s" size="14" class="textbox" readonly>
          </td>
        </tr>
        <tr>
          <td align="right" class="labeltext">Nachname:</td>
          <td>
            <input type="text" value="%(na)s" size="14" class="textbox" readonly>
          </td>
          <td class="labeltext" align="right">Postleitzahl:</td>
          <td>
            <input type="text" value="%(plz)s" size="14" class="textbox" readonly>
          </td>
          <td class="labeltext" align="right">Telefon 1:</td>
          <td>
            <input type="text" value="%(tl1)s" size="14" class="textbox" readonly>
          </td>
        </tr>
        <tr>
          <td align="right" class="labeltext">Geburtstag:</td>
          <td>
            <input type="text" value="%(gb)s " size="14" class="textbox" readonly>
          </td>
          <td class="labeltext" align="right">Ort:</td>
          <td>
            <input type="text" value="%(ort)s" size="14" class="textbox" readonly>
          </td>
          <td class="labeltext" align="right">Telefon 2:</td>
          <td>
            <input type="text" value="%(tl2)s" size="14" class="textbox" readonly>
          </td>
        </tr>
        <tr valign="top">
          <td align="right" class="labeltext" height="2">Ausbildung:</td>
          <td height="2">
            <input type="text" value="%(ber)s" size="14" class="textbox" readonly>
          </td>
          <td height="2" colspan="4"></td>
        </tr>
"""
    

class SpeichernZuruecksetzenAbbrechen(_HTML):
    def display(self):
        self._init()
        return Fieldset(content=self.tmpl % self).display()
    
    tmpl = """
                <tr height="40">
                  <td width="33%%" align="center" valign="middle">
                    <input type="submit" name="" value="Speichern" class="button">
                  </td>
                  <td align="center" valign="middle" width="33%%">
                    <input type="reset" value="Zur&uuml;cksetzen" class="button">
                  </td>
                  <td align="center" valign="middle" width="34%%">
                    <input type="button" value="Abbrechen" class="button" onClick="javascript:history.back()">
                  </td>
                </tr>
"""
                  
