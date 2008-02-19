# coding: latin-1

"""Module für die Administration und Feedback"""


import os

from ebkus.app import Request
from ebkus.app import ebupd
from ebkus.app.ebapi import Akte, Fachstatistik, Jugendhilfestatistik, Code, Mitarbeiter, Kategorie
from ebkus.app.ebapi import Code, cc
from ebkus.app_surface.standard_templates import *
from ebkus.config import config

import ebkus.html.htmlgen as h
from ebkus.html.akte_share import akte_share

class CustomizeFachstatistik(object):

    standard_felder = ( # nur die abschaltbaren Felder mit Kategorien
        'gs', 'ag', 'fs', 'zm', 'qualij', 'hkm', 'hkv', 'bkm', 'bkv', 
        'qualikm', 'qualikv', 'agkm', 'agkv', 'ba1', 'ba2', 'pbe', 'pbk',
        'anmprobleme', 'kindprobleme', 'elternprobleme', 'eleistungen',
        )
    felder_mit_notiz = {'pbe': 'no3',
                        'pbk': 'no2'}
    termin_felder = ('kat', 'kkm', 'kkv', 'kki', 'kpa', 'kfa',
                     'ksoz', 'kleh', 'kerz', 'kkonf', 'kson',)
    joker_klient = ('joka1', 'joka2', 'joka3', 'joka4',) 
    joker_frei = ('jokf5', 'jokf6', 'jokf7', 'jokf8',) 
    joker_felder = joker_klient + joker_frei
    abschaltbare_items = (standard_felder +
                          tuple(felder_mit_notiz.keys()) +
                          tuple(felder_mit_notiz.values()) +
                          ('kat', 'no') +
                          joker_felder)
    def __init__(self):
        from ebkus.app.ebapi import Tabelle, FeldList
        tab = Tabelle(tabelle='fachstat')
        felder = FeldList(where="tab_id=%s" % tab['id'])
        self.fd = {}
        for f in felder:
            self.fd[f['feld']] = f  # feldname --> feldobjekt

    def get(self, feldname):
        return self.fd.get(feldname)

    def deaktiviert(self, feld):
        if feld in self.termin_felder:
            feld = 'kat' # alle Terminfelder deaktivieren wenn kat deaktiviert ist
        if feld in self.fd:
            # deaktiviert wenn erstes bit auf eins steht
            return (self.fd[feld]['flag'])&1
        return False

    def multifeld(self, feld):
        return self.get(feld)['verwtyp'] == cc('verwtyp', 'm')
    def jokerfeld(self, feld):
        # Name fängt mit jok an
        return feld.startswith('jok')
    def jokerfeld_bei_angaben(self, feld): # item in Angaben zum Klienten eingebunden
        # Name fängt mit joka an
        return feld.startswith('joka')
    def jokerfeld_eigenstaendig(self, feld): # item in eigenem Fieldset
        # Name fängt mit jokf an
        return feld.startswith('jokf')
    def set_status(self, feldname, status):
        f_obj = self.fd.get(feldname)
        flag = f_obj['flag']
        if status:
            f_obj.update({'flag': flag&~1})
        else:
            f_obj.update({'flag': flag|1})


fs_customize = CustomizeFachstatistik()

class fskonfig(Request.Request, akte_share):
    """Konfiguration der Fachstatistik."""
    
    permissions = Request.ADMIN_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        fsc = fs_customize
        daten = []
        for feld in fsc.standard_felder:
            row = [h.CheckItem(name="%s_a" % feld,
                               value="1",
                               tip='Item aktivieren',
                               checked=not fsc.deaktiviert(feld)),
                   h.String(tip='Name des Items',
                            string=fsc.get(feld)['name']),
                   h.String(tip='Name der Antwortkategorie',
                            string=fsc.get(feld)['kat__name']),
                   h.Icon(href="updkat?katid=%s" % fsc.get(feld)['kat_id'],
                           icon= "/ebkus/ebkus_icons/edit_button.gif",
                           tip="Antwortkategorie bearbeiten"),
                   feld in fsc.felder_mit_notiz and
                   h.CheckItem(name="%s_a" % fsc.felder_mit_notiz[feld],
                               value="1",
                               tip='Notizfeld aktivieren',
                               checked=not fsc.deaktiviert(fsc.felder_mit_notiz[feld]))
                   or h.DummyItem(),
                ]
            daten.append(row)
        feld = 'kat' # Termine als ganze aktivieren oder deaktivieren
        daten.append([h.CheckItem(name="%s_a" % feld,
                                  value="1",
                                  tip='Item aktivieren',
                                  checked=not fsc.deaktiviert(feld)),
                      h.String(tip='Name des Items',
                               string='Termine'),
                      h.DummyItem(),
                      h.DummyItem(),
                      ]
                     )
        feld = 'no' # Notizfeld
        daten.append([h.CheckItem(name="%s_a" % feld,
                                  value="1",
                                  tip='Item aktivieren',
                                  checked=not fsc.deaktiviert(feld)),
                      h.String(tip='Name des Items',
                               string=fsc.get(feld)['name']),
                      h.DummyItem(),
                      h.DummyItem(),
                      ]
                     )
        standard_items = h.FieldsetDataTable(
            legend="Standard-Items",
            headers=('', 'Aktiviert', 'Name', 'Kategorie', '', '', 'Notiz',),
            daten=daten,
            )

        daten = []
        for feld in fsc.joker_klient:
            row = [h.CheckItem(name="%s_a" % feld,
                               value="1",
                               tip='Item aktivieren',
                               checked=not fsc.deaktiviert(feld)),
                   h.TextItem(tip='Name des Items',
                              name="%s_l" % feld,
                              value=fsc.get(feld)['name'],
                              class_='textboxlarge'),
                   h.SelectItem(tip='Antwortkategorie auswählen',
                                options=self.for_fs_kategorie(sel=fsc.get(feld)['kat_id']),
                                name="%s_k" % feld,
                                class_='listbox220'),
                   h.Icon(href="updkat?katid=%s" % fsc.get(feld)['kat_id'],
                           icon= "/ebkus/ebkus_icons/edit_button.gif",
                           tip="Antwortkategorie bearbeiten"),
##                    h.Icon(href="codetab?tabelle=Fachstatistik",
##                            icon= "/ebkus/ebkus_icons/neu_button.gif",
##                            tip="Neue Antwortkategorie definieren"),
                ]
            daten.append(row)
        joker_items_klient = h.FieldsetDataTable(
            legend="Frei definierbare Items im Kasten 'Angaben zum Klienten  und dessen Angehörige'",
            headers=('', 'Aktiviert', '', 'Name', '', 'Kategorie'),
            daten=daten,
            )
        daten = []
        for feld in fsc.joker_frei:
            kat_id = fsc.get(feld)['kat_id']
            row = [h.CheckItem(name="%s_a" % feld,
                               value="1",
                               tip='Item aktivieren',
                               checked=not fsc.deaktiviert(feld)),
                   h.TextItem(tip='Name des Items',
                              name="%s_l" % feld,
                              value=fsc.get(feld)['name'],
                              class_='textboxlarge'),
                   h.SelectItem(tip='Antwortkategorie auswählen',
                                options=self.for_fs_kategorie(sel=kat_id),
                                name="%s_k" % feld,
                                class_='listbox220'),
                   h.Icon(href="updkat?katid=%s" % kat_id,
                           icon= "/ebkus/ebkus_icons/edit_button.gif",
                           tip="Antwortkategorie bearbeiten"),
##                    h.Icon(href="codetab?tabelle=Fachstatistik",
##                            icon= "/ebkus/ebkus_icons/neu_button.gif",
##                            tip="Neue Antwortkategorie definieren"),
                   h.CheckItem(name="%s_m" % feld,
                               value="1",
                               tip='Mehrfachauswahl zulassen',
                               checked=fsc.multifeld(feld)),
                ]
            daten.append(row)
        joker_items_frei = h.FieldsetDataTable(
            legend="Frei definierbare Items im jeweils eigenen Kasten",
            headers=('', 'Aktiviert', '', 'Name', '', 'Kategorie', '', '', 'Mehrfach'),
            daten=daten,
            )
        res = h.FormPage(
            title="Fachstatistik konfigurieren",
            help=False,
            name="fskonfigform",action="admin",method="post",
            breadcrumbs = (('Aministratorhauptmenü', 'menu'),
                           ),
            rows=(standard_items,
                  joker_items_klient,
                  joker_items_frei,
                  h.SpeichernZuruecksetzenAbbrechen(abbrechen='menu'),
                  ),
            hidden=(('file', 'updfskonfig'),
                    ('view', 'menu'),
                    ),
            )
        return res.display()

##         standard items:
##           Aktiviert Label (readonly), Kategoriename (readonly), 
##         joker Angaben zum Klienten:
##           Aktiviert Label, Kategorieauswahl, button Neue Kategorie, button Kategorie bearbeiten
##         joker mit eigenem Fieldset:
##           Aktiviert Label, Kategorieauswahl, Mehrfachauswahl (checkbox), button Neue Kategorie, button Kategorie bearbeiten

##         Fieldsets:
##             Standarditems
##                 Aktiviert Label, Typ, Kategoriename (alles readonly), button Kategorie bearbeiten
##             Frei definierbare Items bei Angaben zum Klienten:
##                 Aktiviert Label, Kategorieauswahl, button Neue Kategorie, button Kategorie bearbeiten
##             Frei definierbare Items in eigenem Kasten:
##                 Aktiviert Label, Kategorieauswahl, button Neue Kategorie, button Kategorie bearbeiten



##         Namen für die Formulare:
##             feldname + _ + {aktiv, label, katcode, 
                        
