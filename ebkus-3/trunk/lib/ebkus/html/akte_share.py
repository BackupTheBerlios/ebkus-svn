# coding: latin-1

"""Gemeinsame Elemente für die Akte."""

from ebkus.config import config
from ebkus.app.ebapi import today, cc, Akte, Bezugsperson
import ebkus.html.htmlgen as h

class akte_share(object):
    """Html-Elemente, die an verschiedenen Stellen gebraucht werden
    und hier nur einmal definiert werden.
    """
    
    def get_klientendaten(self, data):
        if isinstance(data, Akte):
            bezug = 'des Klienten'
        elif isinstance(data, Bezugsperson):
            bezug = 'der Bezugsperson'
        klientendaten = h.FieldsetInputTable(
            legend = 'Klientendaten',
            daten = [[h.TextItem(label='Vorname',
                               name='vn',
                               value=data['vn'],
                               tip='Vorname %s' % bezug,
                               )],
                     [h.TextItem(label='Nachname',
                               name='na',
                               value=data['na'],
                               tip='Nachname %s' % bezug,
                               )],
                     [h.TextItem(label='Geburtstag',
                               name='gb',
                               value=data['gb'],
                               tip="Bitte den Geburtstag in der Form (TT.MM.JJJJ) eingeben",
                               onBlur="PruefeDatum(gb,1910,2060)",
                               )],
                     [h.TextItem(label='Telefon1',
                               name='tl1',
                               value=data['tl1'],
                               )],
                     [h.TextItem(label='Telefon2',
                               name='tl2',
                               value=data['tl2'],
                               )],
                     [h.TextItem(label='Ausbildung',
                               name='ber',
                               value=data['ber'],
                               tip='Die Ausbildung %s' % bezug,
                               )],
                      ],
                     )
        return klientendaten

    def get_anschrift(self, data):
        if config.BERLINER_VERSION:
            icon = h.Icon(href="javascript:view_strkat()",
                        tip="Straßensuche starten",
                        icon="/ebkus/ebkus_icons/strkatview_button.jpg",
            )
            n_col = 3 # eine Spalte mehr wg. icon
        else:
            icon = None
            n_col = 2
        str = h.TextItem(label='Straße',
                         name='str',
                         value=data['str'],
                         tip='Straße',
                         icon=icon,
                       )
        strkat = h.TextItem(label='Straße',
                       name='strkat',
                       value=data['str_inner'],
                       tip='Straße',
                       icon=icon,
                       )
        str_ausser = h.TextItem(label='Außerhalb',
                       name='str',
                       value=data['str_ausser'],
                       tip='Straße außerhalb von Berlin',
                       )
        hsnr = h.TextItem(label='Hausnummer',
                        name='hsnr',
                        value=data['hsnr'],
                        tip='Hausnummer',
                        n_col=n_col,
                        )
        plz = h.TextItem(label='Postleitzahl',
                       name='plz',
                       value=data['plz'],
                       tip="Postleitzahl",
                       n_col=n_col,
                       )
        ort = h.TextItem(label='Ort',
                       name='ort',
                       value=data['ort'],
                       tip="Wohnort",
                       n_col=n_col,
                       )
        if data.get('planungsr'):
            planungsr = h.TextItem(label='Planungsraum',
                                 name='planungsr',
                                 value=data['planungsr'],
                                 tip="Der Planungsraum des Klienten",
                                 n_col=n_col,
                                 )
        else:
            planungsr = h.DummyItem()
        fs = h.SelectItem(label='Wohnt bei',
                        name='fs',
                        options=self.options.for_kat('fsfs', sel=data['fs']),
                        tip='Bei wem der Klient lebt',
                        n_col=n_col,
                        )
        if config.BERLINER_VERSION:
            items = (strkat, str_ausser, hsnr, plz, ort, fs)
        else:
            items = (str, hsnr, plz, ort, planungsr, fs)
        anschrift = h.FieldsetInputTable(
            legend = 'Anschrift',
            daten = [[i] for i in items])
        return anschrift
    
    def get_klientendaten_kurz(self, fall):
        akte = fall['akte']
        klientendaten = h.FieldsetDataTable(
            legend='Klientendaten',
            headers= ('Name', 'Geburtsdatum', 'Fallnummer'),
            daten=[[h.String(string="%(vn)s %(na)s" % akte),
                    h.String(string="%(gb)s" % akte),
                    h.String(string="%(fn)s" % fall),
                    ]]
            )
        return klientendaten
        

    def get_zustaendigkeiten(self, zustaendigkeiten_list):
        zustaendigkeiten = h.FieldsetDataTable(
            legend='Zuständigkeiten',
            headers= ('Bearbeiter', 'Beginn', 'Ende'),
            daten=[[h.String(string= zust['mit_id__na']),
                    h.Datum(day=zust['bgd'],
                            month=zust['bgm'],
                            year=zust['bgy']),
                    h.Datum(day=zust['ed'],
                            month=zust['em'],
                            year=zust['ey'])]
                   for zust in zustaendigkeiten_list],
            )
        return zustaendigkeiten

    def get_bisherige_zustaendigkeit(self, aktuell_zustaendig):
        bisherige_zustaendigkeit = h.FieldsetDataTable(
            legend='Bisherige Zuständigkeit wird ausgetragen',
            headers= ('Bearbeiter', 'Beginn'),
            daten=[[h.String(string= "%(mit__vn)s %(mit__na)s" % aktuell_zustaendig),
                    h.Datum(date=aktuell_zustaendig.getDate('bg')),
                    ]],
            )
        return bisherige_zustaendigkeit


    def get_bezugspersonen(self, bezugspersonen_list, aktueller_fall,
                           edit_button, view_button):
        bezugspersonen = h.FieldsetDataTable(
            legend= 'Bezugspersonen',
            headers= ('Art', 'Vorname', 'Nachname', 'Telefon 1', 'Telefon 2'),
            daten= [[(aktueller_fall and
                      h.Icon(href= 'updpers?akid=%(akte_id)d&bpid=%(id)d' % b,
                           icon= "/ebkus/ebkus_icons/edit_button.gif",
                           tip= 'Bezugsperson bearbeiten')
                      or
                      h.IconDead(icon= "/ebkus/ebkus_icons/edit_button_inaktiv_locked.gif",
                               tip= 'Funktion gesperrt')),

                       (aktueller_fall and
                        h.Icon(href= '#',
                             onClick= "view_details('viewpers?akid=%(akte_id)d&bpid=%(id)d')" % b,
                             icon= "/ebkus/ebkus_icons/view_details.gif",
                             tip= 'Bezugsperson ansehen')
                        or
                        h.IconDead(icon= "/ebkus/ebkus_icons/view_details_inaktiv.gif",
                                 tip= 'Funktion gesperrt')),

                       h.String(string= b['verw__name']),
                       h.String(string= b['vn']),
                       h.String(string= b['na']),
                       h.String(string= b['tl1']),
                       h.String(string= b['tl2'])]
                      for b in bezugspersonen_list],
            button= (aktueller_fall and
                     h.Button(value="Hinzufügen",
                            tip="Bezugsperson hinzufügen",
                            onClick=
                       "go_to_url('persneu?akid=%(akte_id)d&fallid=%(id)d&klerv=1')" %
                              aktueller_fall,
                            ) or None),
            )
        self.delete_icons(bezugspersonen.daten, edit_button, view_button)
        return bezugspersonen
        
    def delete_icons(self, daten, edit_button, view_button):
        """löscht bereits generierte icons aus den Tabellenitems.
        Erscheint mir einfacher, als die Generierung weiter zu verschachteln.
        """
        if edit_button:
            if not view_button:
                for zeile in daten:
                    del zeile[1]
        else:
            for zeile in daten:
                del zeile[0]
            if not view_button:
                for zeile in daten:
                    del zeile[0]
