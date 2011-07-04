# coding: latin-1

"""Modul für Allgemeine Konfiguration."""

from ebkus.app import Request
from ebkus.config import config
from ebkus.app.ebapi import EE
from ebkus.app.ebapih import make_option_list

import ebkus.html.htmlgen as h
from ebkus.html.akte_share import akte_share

class _konfig(Request.Request, akte_share):
    def get_konfig_vars(self, 
                        edit_button=False, # falls False, kein edit button
                        ):
        konfig_list = [(kv.name, kv) for kv in config.iter() if kv.fachlich]
        konfig_list.sort()
        konfig_table = h.FieldsetDataTable(
            legend='Allgemeine Konfigurationsvariablen',
            headers=('Name', 'Aktueller Wert', 'Kurzbeschreibung',),
            daten=[[edit_button and h.Icon(href= 'updkonfig?konfig_name=%(name)s' % kv,
                                            icon= "/ebkus/ebkus_icons/edit_button.gif",
                                            tip= 'Konfigurationsvariable bearbeiten')
                                      or None,
                    h.String(string=kv['name']),
                    h.String(string=kv.print_value('value')), # damit true anstatt True geschrieben wird
                    h.String(string=kv['beschreibung']),
                    ]
                    for _,kv in konfig_list],
            )
        return konfig_table

    def _process(self, 
                 title,
                 file,
                 konfig_name,
                 ):
        kv = [kv for kv in config.iter() if kv.name == konfig_name]
        if kv:
            kv = kv[0]
        else:
            raise EE("Unbekannte Konfigurationsvariable: %s" % konfig_name)
        edit = h.FieldsetInputTable(
            legend=title,
            daten=[[h.String(string='Name:',
                             class_='labeltext',
                             align='right',
                             ),
                    h.String(string=kv.name,
                             class_='largetextbold',
                             ),
                    ],
                   [h.String(string='Beschreibung:',
                             class_='labeltext',
                             align='right',
                             ),
                    h.String(string=kv.beschreibung + "<br /><br />" + kv.doku
                             ),
                    ],
                   [kv.is_boolean() and 
                    h.SelectItem(label='Wert',
                                 name='konfig_value',
                                 options=make_option_list(
                            elements=[{'name':'true', 'value':'true'},
                                      {'name':'false', 'value':'false'},],
                            value_field='value',
                            name_field='name',
                            selected=kv.value and 'true' or 'false',
                            ),
                                 ) or
                    h.TextareaItem(label='Wert',
                               name='konfig_value',
                               value=kv.value,
                               class_='textareaverylarge',
                               )
                    ],
                   ],
            )
        res = h.FormPage(
            title=title,
            name='konfedit',action="konfigausw",method="post",
            breadcrumbs = (('Hauptmenü', 'menu'),
                           ('Allgemeine Konfiguration', 'konfausw'),
                           ),
            hidden=(("konfig_name", konfig_name),
                    ("file", file),
                    ),
            rows=(edit,
                  h.SpeichernZuruecksetzenAbbrechen(),
                  #self.get_mitarbeiter(),
                  ),
            )
        return res.display()

class konfigausw(_konfig):
    """Auswahlformular zum Ändern der Mitarbeiterdaten. """
    permissions = Request.ADMIN_PERM
    def processForm(self, REQUEST, RESPONSE):
        file = self.form.get('file')
        if file:
            from ebkus.app import ebupd
            function = getattr(ebupd, file)
            function(self.form)
        res = h.Page(
            title='Konfiguration',
            breadcrumbs = (('Aministratorhauptmenü', 'menu'),
                           ),
            rows=(self.get_hauptmenu(),
                  self.get_konfig_vars(edit_button=True,
                                       #hinzufuegen_button=True,
                                       ),
                  ),
            )
        return res.display()

        
class updkonfig(_konfig):
    """Updateformular für die Stammdaten der Mitarbeiter. """
    permissions = Request.ADMIN_PERM
    def processForm(self, REQUEST, RESPONSE):
        konfig_name = self.form.get('konfig_name')
        if not konfig_name:
            raise EE('Keine Konfigurationsvariable')
        return self._process('Konfigurationsvariable bearbeiten',
                             'updkonfig',
                             konfig_name)

        
        
