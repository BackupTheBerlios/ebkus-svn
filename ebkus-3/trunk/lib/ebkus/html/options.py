# coding: latin-1

#���

from ebkus.app.ebapih import get_codes, make_option_list
from ebkus.app.ebapi import KategorieList, ZustaendigkeitList, today, AbfrageList
from ebkus.db.sql import SQL
from ebkus.config import config

class options(object):
    """Klasse zur Generierung von Option-Listen
    """
    option_tmpl = '<option value="%s"%s>%s</option>'


    def for_auswertungen(self, sel=None):
        bs = ''
        if config.BERATUNGSKONTAKTE_BS:
            bs =  """
                     <option value="nothing">[ Speziell f�r Braunschweig ]
                     <option value="bkontbsabfrform">- Beratungskontaktzeiten
                     <option value="nothing">
                     """
        options = ("""
                      <option value="nothing">[ Beratungen ]
                      <option value="abfr1?o=alle&ed=0">- alle Beratungen
                      <option value="abfr1?o=laufend&ed=0">- laufende Beratungen
                      <option value="abfr1?o=zda&ed=0">- abgeschlossene Beratungen
                      <option value="formabfr2">- ab Fallnummer?
                      <option value="nothing">
"""                      + bs +
"""
                      <option value="nothing">[ Klientenzahl ]
                      <option value="formabfr4">- Neumeldungen u. Abschl&uuml;sse
                      <option value="formabfr5">- Klienten pro Mitarbeiter
                      <option value="nothing">
                      <option value="nothing">[ Gruppen ]
                      <option value="formabfr8a">- Gruppen&uuml;berblick
                      <option value="nothing">
                      <option value="nothing">[ Fach- und Bundesstatistik ]
                      <option value="statabfr">- Statistik
                      <option value="nothing">
                      <option value="nothing">***Nicht mehr ben�tigt:
                      <option value="nothing">
                      <option value="nothing">[ Bundesstatistik ]
                      <option value="jghabfr">- Bundesstatistik
                      <option value="nothing">
                      <option value="nothing">[ Fachstatistik ]
                      <option value="fsabfr">- Fachstatistik
                      <option value="formabfr6?file=abfritem">- Itemauswahl
                      <option value="formabfr6?file=abfrkat">- Kategorienauswahl
                      <option value="fsabfr_plraum">- Planungs- und Sozialraum
                      <option value="formabfr10a">- Konsultationszahl
                      <option value="formabfr9a">- Konsultationssumme
                      <option value="formabfr11a">- Beratungsdauer
                      <option value="formabfr12a">- Beratungsdauer - Leistung
<!-----               <option value="formabfr13a">- Eltern - Merkmal x gleich
                      <option value="formabfr14a">- Elternteil - Merkmal x gleich //--->
                      """)
        return options



    def for_mitarbeiter(self, sel=None, empty_option=False):
        return make_option_list(self.getMitarbeiterliste(),
                                'id', 'na',
                                selected=sel, empty_option=empty_option)

    def for_teilmengen(self, sel=None):
        "Definierte Teilmengen, erm�glichen Abfragen �ber definierte Gruppen "
        "in der Fach- und Bundesstatistik."
        abfrage_list = AbfrageList(where='')
        return (self.option_tmpl % ('', '', 'Alle')) + make_option_list(abfrage_list,
                                                               'id', 'name',
                                                               selected=sel)

    def for_jahre(self, sel=None, first=None, last=None, erster_eintrag=None):
        "Optionen f�r Jahre, entweder explizit oder anhand aller Fallbeginne"
        if not last:
            last = today()['year']
        if not first:
            jahre = SQL("select distinct bgy from fall order by bgy").execute()
            if jahre:
                first = jahre[0][0]
            else:
                first = last
        jahre = [j for j in range(first, last+1)]
        options = []
        select_attr = ' selected="selected" '
        if erster_eintrag:
            options.append(self.option_tmpl % ('', '', erster_eintrag))
        options += [self.option_tmpl % (j, j==sel and select_attr or '', j)
                    for j in jahre]
        return '\n'.join(options)

    def for_kat(self, kat, sel=None):
        if sel in ('', ' ',):
            empty_option = True
        else:
            empty_option = False
        # das ist ein hack. Eigentlich m�sste ein multi-kat Feld eine List von Integern liefern.
        # Ist aber ein String von Zahlen, zB "233 44 444"
        if isinstance(sel, basestring):
            sel = [int(x) for x in sel.split()]
        return  make_option_list(get_codes(kat),
                                 'id', 'name',
                                 selected=sel,
                                 empty_option=empty_option)

    
    def for_fs_kategorie(self, sel=None):
        from ebkus.html.fskonfig import fs_customize
        kat_ids = ', '.join([str(f['kat_id']) for f in fs_customize.fd.values()
                                 if f['kat_id']])
        fs_kategorien = KategorieList(where="id in (%s)" % kat_ids)
        fs_kategorien.sort('name')
        return make_option_list(fs_kategorien,
                                'id', 'name',
                                selected=sel)

    def for_code_sort(self, kat, sel=None):
        elems = [c['sort'] for c in kat['codes']]
        elems.sort()
        if sel and sel > max(elems):
            elems.append(sel)
        elems = [{'sort': s} for s in elems]
        return make_option_list(elems, 'sort', 'sort', selected=sel)



    def get_aktuelle_zustaendigkeiten(self):
        """Generiert alle Zust�ndigkeiten f�r den angemeldeten Mitarbeiter"""
        wherestr = 'ed = 0'
        benr = self.mitarbeiter['benr__code']
        if benr in ('bearb', 'verw', 'admin'):
            if benr == 'bearb':
                wherestr += ' and mit_id = %s' % self.mitarbeiter['id']
            zustaendigkeiten = ZustaendigkeitList(where=wherestr)
            zustaendigkeiten.sort('mit_id__na', 'fall_id__akte_id__na',
                                  'fall_id__akte_id__vn')
            for z in zustaendigkeiten:
                if z['fall_id__akte_id__stzak'] == self.stelle['id']:
                    yield z

    def get_aktuelle_bezugspersonen(self):
        for z in self.get_aktuelle_zustaendigkeiten():
            for b in z['fall__akte__bezugspersonen']:
                b['fn'] = z['fall__fn'] # drangepappt f�r das Template unten was Fallnummer braucht
                yield b

    # TBD Verzockt besser mit make_option_list
    def for_klienten(self, sel=None, kurz=False, empty_option=False):
        """Optionen f�r Klientenauswahl"""
        selected = ' selected="selected" '
        if not sel:
            sel = ''
        sel = [int(s) for s in sel.split()]
        tmpl = """<option value="%(fall_id)s"%(xxsel)s>%(mit__na)s | %(fall__akte__vn)s %(fall__akte__na)s, %(fall__akte__gb)s | %(fall__fn)s </option>"""
        tmpl_kurz = """<option value="%(fall_id)s"%(xxsel)s>%(fall__akte__vn)s %(fall__akte__na)s | %(fall__fn)s</option>"""
        if kurz:
            tmpl = tmpl_kurz
        if empty_option:
            options = "<option value="" >&nbsp;</option>"
        else:
            options = ''
        for z in self.get_aktuelle_zustaendigkeiten():
            if z['fall_id'] in sel:
                z['xxsel'] = selected
            else:
                z['xxsel'] = ''
            options += tmpl % z
            if z.has_key('xxsel'):
                del z['xxsel']
        return options

    def for_bezugspersonen(self):
        """Optionen f�r Bezugspersonenauswahl"""
        tmpl = """<option value="%(id)s">%(na)s %(vn)s | %(fn)s</option>"""
        options = ''
        for b in self.get_aktuelle_bezugspersonen():
                options += tmpl % b
        return options
