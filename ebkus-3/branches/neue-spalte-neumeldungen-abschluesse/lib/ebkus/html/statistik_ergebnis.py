# coding: latin-1

import logging
from ebkus.app import Request
from ebkus.app_surface.standard_templates import *
from ebkus.app_surface.abfragen_templates import *

import gdchart
import cStringIO

class auszergebnis(Request.Request):
    """Eine Auszählung.

    - liefert html-Tabelle für die Einbettung in die Statistikergebnisse
      (add_tabelle) und links, die URLs enthalten für Statistikergebnisse,
      die den Zugriff auf Einzeltabellen und Charts ermöglichen

    - liefert Einzeltabelle (html)
    - liefert Chart (html)
    - liefert Image für Chart (gif)
    (Das ist der Ersatz für frühere Dateien im chart-Verzeichnis)

    - bezieht seine Daten aus einer Instanz der Klasse
      ebkus.app.statistik._Auszaehlung
    - diese Instanz wird erzeugt bei der Abfrage selbst und wird dann
      in der session unter einer eindeutigen id abgelegt.
    - wenn dann ein Chart oder eine Einzeltabelle verlangt wird,
      wird mit Hilfe der übergebenen id das Auszaehlungsobjekt aus
      der session geholt und damit das Chart bzw. die Tabelle erzeugt.
    """
    
    permissions = Request.ABFR_PERM

    def processForm(self, REQUEST, RESPONSE):
        self.id = self.form.get('id')
        self.typ = self.form.get('typ')
        self.file = self.form.get('file')
        try:
            self.auszaehlung = self.session.data[self.file][self.id]
        except KeyError:
            meldung = {
                'titel':'Abfrageergebnis veraltet',
                'legende':'Abfrageergebnis veraltet',
                'zeile1':'Die Abfrageergebnisse stammen aus einer fr&uuml;heren Session.',
                'zeile2':'Bitte wiederholen Sie die Anfrage.'
                }
            return meldung_t % meldung


        if self.typ == 'tab':
            # Einzeltabelle zum Drucken
            return self.show_tabelle()
        elif self.typ == 'chart':
            # HTML-Rahmen für Chart
            return self.show_chart()
        elif self.typ == 'image':
            # das eigentliche Chart
            return self.generate_chart()
        

    def generate_chart(self):
        """Generiert ein Chart und gibt es als GIF an den Browser zurück."""
        counts = self.auszaehlung.get_result()
        chart = Chart(
            title=self.auszaehlung.title,
            xtitle=self.auszaehlung.xtitle,
            ytitle=self.auszaehlung.ytitle,
            names=[i[0] for i in counts],
            frequencies=[i[1] for i in counts],
            )
        self.RESPONSE.setHeader('content-type', 'image/gif')
        self.RESPONSE.setBody(chart.draw())

    def show_chart(self):
        """Zeigt eine eine HTML-Seite für eine Ergebnistabelle,
        die als einzigen Inhalt einen Link auf das Chart-Image hat."""
        image_url = "auszergebnis?typ=image&file=%s&id=%s" % (self.file, self.id)
        inhalt2 = {'titel': self.auszaehlung.title,
                   'imagedir': "\"" + image_url + "\""}
        res = efbchart_html_tag_datei % inhalt2
        return res
        
    def show_tabelle(self):
        """Zeigt eine einzelne Ergebnistabelle"""
        res = []
        res.append(head_normal_ohne_help_t % self.auszaehlung.auswertungs_ueberschrift)
        res.append(fsergebnis1_tab_t)
        res.append(thkategoriejgh_tab_t % self.auszaehlung.title)
        for i, data in enumerate(self.auszaehlung.get_result()):
            template = i%2 and item_tab_g_t or item_tab_w_t
            res.append(template % (data[0],  data[1], data[2]) )
        res.append(item_ende_tab_t)
        res.append(fsergebnis_ende_tab_t)
        return ''.join(res)


    def add_tabelle(self, res):
        """Fügt eine Ergebnistabelle mit Links auf die Einzeltabelle
        und das Chart in die Ausgabe (res) ein.

        Diese Methode wird nur für den Aufbau der Gesamtergebnisseite
        mit allen Tabellen benötigt (jghergebnis, fstat_ausgabe, ...)
        """
        self.id = self.auszaehlung.id
        self.file = self.auszaehlung.file
        res.append(sprungmarke_t % self.auszaehlung.identname)
        res.append(thkategoriejgh_t % self.auszaehlung.title)
        for i in self.auszaehlung.get_result():
            res.append(item_t % (i[0],  i[1], i[2]) )
        res.append(item_ende_t)
        image_url = "auszergebnis?typ=chart&file=%s&id=%s" % (self.file, self.id)
        tab_url = "auszergebnis?typ=tab&file=%s&id=%s" % (self.file, self.id)
        # tbd template überarbeiten (vereinfachen)
        inhalt = {'titel1': self.auszaehlung.title,
                  'imagedir1': "\"" + tab_url + "\"",
                  'titel2': self.auszaehlung.title,
                  'imagedir2': "\"" + image_url + "\""}
        res.append(efbchart_html_tag % inhalt)


class Chart(object):
    """Verantworlich für die Generierung eines Charts."""
    def __init__(self,
                 title=None,
                 xtitle=None,
                 ytitle=None,
                 names=[],
                 frequencies=[]):
        logging.debug("Chart: t: %s x: %s y: %s names: %s freqs: %s" %
                 (title,
                 xtitle,
                 ytitle,
                 names,
                 frequencies))
        # Get a copy of the default options
        self.options = gdchart.option().copy()
        self.size = (400, 500)
        self.option(set_color=(0x54A3DB, 0x307BAF))
        self.option(bg_color=0xFFFFFF, plot_color=0x0000cd, line_color=0x000000)
        self.option(title=title, xtitle=xtitle, ytitle=ytitle)
        self.names = names
        self.frequencies = frequencies
        
    def option(self, **args):
        # Save option values in the object's dictionary.
        self.options.update(args)
        
    def draw(self):
        """Erstellt Chart als GIF. Gibt das GIF als string zurück."""
        # Put options into effect.
        gdchart.option(*(), **self.options)
        file = cStringIO.StringIO()
        args = (gdchart.GDC_3DBAR, self.size,
                file,
                self.names,
                self.frequencies)
        gdchart.chart(*args)
        return file.getvalue()



