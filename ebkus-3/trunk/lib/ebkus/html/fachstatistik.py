# coding: latin-1

import string
from ebkus.config import config
from ebkus.app import ebapi
from ebkus.app import Request
from ebkus.app.ebapi import Akte, Fall, Fachstatistik, FachstatistikList, \
     LeistungList,cc,today,calc_age, bcode, EE
from ebkus.html.strkat import get_strasse

import ebkus.html.htmlgen as h
from ebkus.html.akte_share import akte_share
from ebkus.html.fskonfig import fs_customize

class _fachstatistik(Request.Request, akte_share):
    # fs und options wird von customize_item gebraucht
    def _customize(self, fs, rows):
        """Überträgt die in fskonfig definierten Anpassungen der Fachstatistik
        auf den Aufbau des Formulars. Die eigentliche Arbeit findet in
        _customize_item statt.

        Das aus fskonfig importierte fs_customize-Objekt enthält die für die
        Anpassung nötigen Informationen.
        """
        self._fs = fs
        res = []
        for r in rows:
            rc = self._customize_fieldset(r)
            if rc:
                res.append(rc)
        return tuple(res)
    def _customize_fieldset(self, f):
        res = []
        self._legend = None # _customize item kann hier was reinschreiben
        for zeile in f.daten:
            z = self._customize_zeile(zeile)
            if z:
                res.append(z)
        if res:
            f.daten = res
            if self._legend:
                f.legend = self._legend
            return f
        return None # es kann sein, dass ein fieldset wegfällt, wenn es keine gültigen Zeilen hat
    def _customize_zeile(self, zeile):
        res = []
        valid_item = False # mindestens 1 gültiges item pro Zeile, sonst verschwindet Zeile
        for item in zeile:
            i = self._customize_item(item)
            #print 'CUSTOMIZE ITEM: ', item.name, i
            if i and not isinstance(i, h.DummyItem):
                valid_item = True
                res.append(i)
            else:
                res.append(h.DummyItem())
        if valid_item:
            return res
        return None
    def _customize_item(self, item):
        if fs_customize.deaktiviert(item.name):
            return None
        if fs_customize.jokerfeld(item.name):
            feld = fs_customize.fd[item.name]
            kat_code = feld['kat_code']
            if kat_code:
                multiple = feld['verwtyp'] == cc('verwtyp', 'm')
                if fs_customize.jokerfeld_eigenstaendig(item.name):
                    self._legend = feld['name']
                    item.label = ''
                else:
                    item.label = feld['name']
                if multiple:
                    item.multiple = True
                    item.size = 8
                if self._fs: # fachstat Objekt vorhanden, wir sind in updfs
                    item.options = self.for_kat(kat_code, self._fs[item.name])
                elif multiple: # initialisieren
                    item.options = self.for_kat(kat_code, None)
                else:
                    item.options = self.for_kat(kat_code, ' ')
##         try:
##             item.label = '>>' + item.label
##         except:
##             pass
        return item

    def _process(self,
                 title,
                 file,
                 fs,
                 ):
        falldaten = h.FieldsetInputTable(
            legend='Falldaten',
            daten = [[h.TextItem(label='Fallnummer',
                                 name='xxx',
                                 value=fs['fall_fn'],
                                 readonly=True,
                               ),
                      h.TextItem(label='Mitarbeiter',
                                 name='xxx',
                                 value=fs['mit__ben'],
                                 readonly=True,
                               ),
                      h.TextItem(label='Jahr',
                                 name='jahr',
                                 value=fs['jahr'],
                                 class_='textboxmid',
                                 maxlength=4,
                               ),
                      ]],
            )
        regional_info = "Ort: %s" % fs['ort']
        for f in config.STRASSENSUCHE.split():
            if f != 'ort':
                regional_info += " %s: %s" % (f.capitalize(), fs[f])
        angabenklient = h.FieldsetInputTable(
            legend="Angaben zum Klienten und dessen Angehörige",
            daten = [[h.TextItem(label='Planungsraum',
                                 name='xxx',
                                 value=fs['plraum'],
                                 readonly=True,
                                 ),
                      h.TextItem(label='PLZ',
                                 name='xxx',
                                 value=fs['plz'],
                                 readonly=True,
                                 tip=regional_info,
                                 ),
                      ],
                     [h.TextItem(label='Geschlecht',
                                 name='xxx',
                                 value=fs['gs__name'],
                                 class_='textbox13',
                                 readonly=True,
                                 ),
                      h.SelectItem(label='Alter Kind/Jugendliche(r)',
                                   name='ag',
                                   options=self.for_kat('fsag', fs['ag']),
                                   aktiviert=True,
                                    ),
                      ],
                     [h.SelectItem(label='Lebensmittelpunkt Kind/Jugendliche(r)',
                                   name='fs',
                                   options=self.for_kat('fsfs', fs['fs']),
                                   ),
                      h.SelectItem(label='Empfohlen von',
                                   name='zm',
                                   options=self.for_kat('fszm', fs['zm']),
                                   ),
                      ],
                     [h.SelectItem(label='Beschäftigung Jugendliche(r)',
                                   name='qualij',
                                   options=self.for_kat('fsqualij', fs['qualij']),
                                   ),
                      h.DummyItem(),
                      ],
                     [h.SelectItem(label='Qualifikation Mutter',
                                   name='qualikm',
                                   options=self.for_kat('fsquali', fs['qualikm']),
                                   ),
                      h.SelectItem(label='Qualifikation Vater',
                                   name='qualikv',
                                   options=self.for_kat('fsquali', fs['qualikv']),
                                   ),
                      ],
                     [h.SelectItem(label='Beschäftigungsverhältnis Mutter',
                                   name='bkm',
                                   options=self.for_kat('fsbe', fs['bkm']),
                                   ),
                      h.SelectItem(label='Beschäftigungsverhältnis Vater',
                                   name='bkv',
                                   options=self.for_kat('fsbe', fs['bkv']),
                                   ),
                      ],
                     [h.SelectItem(label='Herkunftsland Mutter',
                                   name='hkm',
                                   options=self.for_kat('fshe', fs['hkm']),
                                   ),
                      h.SelectItem(label='Herkunftsland Vater',
                                   name='hkv',
                                   options=self.for_kat('fshe', fs['hkv']),
                                   ),
                      ],
                     [h.SelectItem(label='Alter Mutter',
                                   name='agkm',
                                   options=self.for_kat('fsagel', fs['agkm']),
                                   ),
                      h.SelectItem(label='Alter Vater',
                                   name='agkv',
                                   options=self.for_kat('fsagel', fs['agkv']),
                                   ),
                      ],
                     [h.SelectItem(label='Joker 1',
                                   name='joka1',
                                   options=self.for_kat('fsjoka1', fs['joka1']),
                                   ),
                      h.SelectItem(label='Joker 2',
                                   name='joka2',
                                   options=self.for_kat('fsjoka2', fs['joka2']),
                                   ),
                      ],
                     [h.SelectItem(label='Joker 3',
                                   name='joka3',
                                   options=self.for_kat('fsjoka3', fs['joka3']),
                                   ),
                      h.SelectItem(label='Joker 4',
                                   name='joka4',
                                   options=self.for_kat('fsjoka4', fs['joka4']),
                                   ),
                      ],
                     ]
            )
        label_width = "20%" # richtet die Select-Elemente Fieldset-übergreifend aus
        ba1 = h.FieldsetInputTable(
            legend='Problem 1 bei der Anmeldung',
            daten=[[h.SelectItem(label='',
                                 name='ba1',
                                 class_='listbox310',
                                 label_width=label_width,
                                 options=self.for_kat('fsba', fs['ba1']),
                                 )
                    ]],
            )
        ba2 = h.FieldsetInputTable(
            legend='Problem 2 bei der Anmeldung',
            daten=[[h.SelectItem(label='',
                                 name='ba2',
                                 class_='listbox310',
                                 label_width=label_width,
                                 options=self.for_kat('fsba', fs['ba2']),
                                 )
                    ]],
            )
        pbk = h.FieldsetInputTable(
            legend='Hauptproblematik Kind/Jugendliche(r)',
            daten=[[h.SelectItem(label='',
                                 name='pbk',
                                 class_='listbox310',
                                 label_width=label_width,
                                 options=self.for_kat('fspbk', fs['pbk']),
                                 )
                    ],
                   [h.TextItem(label='Sonstige',
                               name='no2',
                               value=fs['no2'],
                               class_="textbox310",
                               ),
                    ]
                   ],
            )
##         jokf1 = h.FieldsetInputTable(
##             legend='Hauptproblematik Kind / Jugendliche',
##             daten=[[h.SelectItem(label='',
##                                  name='jokf1',
##                                  class_='listbox310',
##                                  label_width=label_width,
##                                  options=self.for_kat('fspbk', fs['pbk']),
##                                  )
##                     ]],
##             )
        pbe = h.FieldsetInputTable(
            legend='Hauptproblematik der Eltern',
            daten=[[h.SelectItem(label='',
                                 name='pbe',
                                 class_='listbox310',
                                 label_width=label_width,
                                 options=self.for_kat('fspbe', fs['pbe']),
                                 )
                    ],
                   [h.TextItem(label='Sonstige',
                               name='no3',
                               value=fs['no3'],
                               class_="textbox310",
                                  ),
                    ]
                   ],
            )
        anmprobleme = h.FieldsetInputTable(
            legend='Problem(e) bei der Anmeldung',
            daten=[[h.SelectItem(label='',
                                 name='anmprobleme',
                                 options=self.for_kat('fsba', fs['anmprobleme']),
                                 multiple=True,
                                 class_='listbox310',
                                 label_width=label_width,
                                 size=8,
                                 ),
                    ]],
            )
        kindprobleme = h.FieldsetInputTable(
            legend='Problemspektrum Kind/Jugendliche(r)',
            daten=[[h.SelectItem(label='',
                                 name='kindprobleme',
                                 options=self.for_kat('fspbk', fs['kindprobleme']),
                                 multiple=True,
                                 class_='listbox310',
                                 label_width=label_width,
                                 size=8,
                                 ),
                    ],
                   ],
            )
        elternprobleme = h.FieldsetInputTable(
            legend='Problemspektrum Eltern',
            daten=[[h.SelectItem(label='',
                                 name='elternprobleme',
                                 options=self.for_kat('fspbe', fs['elternprobleme']),
                                 multiple=True,
                                 class_='listbox310',
                                 label_width=label_width,
                                 size=8,
                                 ),
                    ],
                   ],
            )

        jokf5 = h.FieldsetInputTable(
            legend='Joker 5',
            daten=[[h.SelectItem(label='',
                                 name='jokf5',
                                 class_='listbox310',
                                 label_width=label_width,
                                 options=self.for_kat('fsjokf5', fs['jokf5']),
                                 )
                    ]],
            )
        jokf6 = h.FieldsetInputTable(
            legend='Joker 6',
            daten=[[h.SelectItem(label='',
                                 name='jokf6',
                                 class_='listbox310',
                                 label_width=label_width,
                                 options=self.for_kat('fsjokf6', fs['jokf6']),
                                 )
                    ]],
            )
        jokf7 = h.FieldsetInputTable(
            legend='Joker 7',
            daten=[[h.SelectItem(label='',
                                 name='jokf7',
                                 class_='listbox310',
                                 label_width=label_width,
                                 options=self.for_kat('fsjokf7', fs['jokf7']),
                                 )
                    ]],
            )
        jokf8 = h.FieldsetInputTable(
            legend='Joker 8',
            daten=[[h.SelectItem(label='',
                                 name='jokf8',
                                 class_='listbox310',
                                 label_width=label_width,
                                 options=self.for_kat('fsjokf8', fs['jokf8']),
                                 )
                    ]],
            )
        eleistungen = h.FieldsetInputTable(
            legend='Erbrachte Leistungen',
            daten=[[h.SelectItem(label='',
                                 name='eleistungen',
                                 class_='listbox310',
                                 label_width=label_width,
                                 multiple=True,
                                 options=self.for_kat('fsle', fs['eleistungen']),
                                 size=8,
                                 ),
                    ]],
            )
        #### anfang get_termine_daten
        def get_termine_daten():
            label = ('KiMu', 'KiVa', 'Kind', 'Paar', 'Familie',
                     'Soz.', 'Lehrer', 'Erz.', 'Hilfebespr.', 'Sonst.', 'Summe')
            namen = ('kkm', 'kkv', 'kki', 'kpa', 'kfa',
                     'ksoz', 'kleh', 'kerz', 'kkonf', 'kson', 'kat')

            items = [h.TextItem(label=lab,
                                name=name,
                                value=fs[name],
                                class_='textboxmid',
                                onBlur="set_term_sum_fachstat('%s')" % name,
                                )
                     for lab, name in zip(label, namen)]
            kat = items[-1]
            kat.bold_label=True
            kat.bold_value=True
            if config.BERATUNGSKONTAKTE and not config.BERATUNGSKONTAKTE_BS:
                # wenn die Terminsumme aus den Beratungskontakten gleich der
                # Terminsumme in der Datenbank ist, nehmen wir an, dass die Daten
                # übernommen wurden und markieren das Kästchen.
                # Wenn nicht, sieht der Benutzer, dass die Daten nicht übernommen sind
                # und kann das Kästchen markieren, um sie erneut zu übernehmen.
                from ebkus.html.beratungskontakt import get_fs_kontakte
                pseudo_fs = {}
                fall_id = fs['fall_id']
                if fall_id:
                    fall = Fall(fall_id)
                    get_fs_kontakte(fall, pseudo_fs)
                    checked = pseudo_fs['kat'] == fs['kat']
                else:
                    checked = False
                checkitem = h.CheckItem(label="Aus Beratungskontakten übernehmen",
                                        name="uebernehmen",
                                        value='1',
                                        checked=checked,
                                        tip="Markieren, um Terminsummen aus Beratungskontakten zu übernehmen",
                                        )
            else:
                checkitem = h.DummyItem()
            return [items[0:5]+[checkitem], items[5:10]+[kat]]
        ### ende get_termine_daten
        termine = h.FieldsetInputTable(
            legend='Terminsumme',
            daten=get_termine_daten(),
            )
        notiz = h.FieldsetInputTable(
            legend='Notiz',
            daten=[[h.TextItem(label='Notiz',
                               name='no',
                               value=fs['no'],
                               class_='textboxverylarge',
                               ),
            ]],
            )
        if file == 'updfs':
            fstat = fs
        else:
            fstat = None
        rows = self._customize(fstat, (
            falldaten,
            angabenklient,
            ba1, ba2,
            pbk, pbe,
            anmprobleme,
            kindprobleme,
            elternprobleme,
            jokf5, jokf6, jokf7, jokf8, 
            eleistungen,
            termine,
            notiz,
            ))
        res = h.FormPage(
            title=title,
            help=False,
            name="fachstatform",action="klkarte",method="post",
            breadcrumbs = (('Hauptmenü', 'menu'),
                           ('Klientenkarte', 'klkarte?akid=%(fall__akte_id)s' % fs),
                           ),
            rows=rows + (h.SpeichernZuruecksetzenAbbrechen(),),
            hidden=(('file', file),
                    ('stz', fs['stz']),
                    ('fallid', fs['fall_id']),
                    ('fall_fn', fs['fall_fn']),
                    ('mitid', fs['mit_id']),
                    ('fsid', fs['id']),
                    ('gs', fs['gs']),
                    ),
            )
        return res.display()



class fsneu(_fachstatistik):
    """Neue Fachstatistik eintragen. (Tabelle: Fachstatistik)"""
    permissions = Request.STAT_PERM
    def processForm(self, REQUEST, RESPONSE):
        fallid = self.form.get('fallid')
        if not fallid:
            raise EE('Erstellen einer Fachstatistik nur f&uuml;r einen Fall moeglich.')
        fall = Fall(fallid)
        akte = fall['akte']
        geschlecht = akte['gs']
        if not geschlecht:
            raise EE("Bitte zuerst das Geschlecht in die Klientenkarte eintragen!")
        # Ich kanns mir nicht anders vorstellen:
        if akte['aktueller_fall']:
            assert fall['id'] == akte['aktueller_fall']['id'] == akte['letzter_fall']['id']
        # das geht nicht immer weil Gleichheit nicht richtig definiert ist
        #assert fall == akte['letzter_fall'] == akte['aktueller_fall']
        leistungen = fall['leistungen']
        jahresl = ebapi.FachstatistikList(where = "fall_fn = '%s'" % fall['fn'])
        if jahresl:
            raise EE('Fachstatistik f&uuml;r den Fall schon vorhanden')
        fs = Fachstatistik()
        # Alter relativ zum Fallbeginn
        alter = calc_age(akte['gb'], fall.getDate('bg'))
        def altersgruppe():
            ag = cc('fsag','999')
            try:
                ag = bcode('fsag', alter)['id']
            except:
                pass # kein bereich gefunden
            return ag
        def altersgruppeeltern(verwcode):
            ag = cc('fsagel','999')
            try:
                for b in akte['bezugspersonen']:
                    if b['verw__code'] == verwcode:
                        if b['gb']:
                            alter = calc_age(b['gb'], fall.getDate('bg'))
                            ag = bcode('fsagel', alter)['id']
            except:
                pass # kein valides Geburtsdatum gefunden
            return ag
                        
        if config.STRASSENKATALOG:
            strasse = get_strasse(akte)
        else:
            strasse = {}
        fs.init(
            id=Fachstatistik().getNewId(),
            mit_id=fall['zustaendig__mit_id'],
            fall_id=fall['id'],
            fall_fn=fall['fn'],
            jahr=str(today().year),
            stz=akte['stzbg'],
            plraum=akte['plraum'],
            ort=akte['ort'],
            plz=akte['plz'],
            ortsteil=strasse.get('ortsteil', ''),
            bezirk=strasse.get('bezirk', ''),
            samtgemeinde=strasse.get('samtgemeinde', ''),
            gs=akte['gs'],
            ag=altersgruppe(),
            agkm=altersgruppeeltern('1'), # code klerv für Mutter
            agkv=altersgruppeeltern('2'), # code klerv für Vater
            fs=akte['fs'],
            anmprobleme=None,
            kindprobleme=None,
            elternprobleme=None,
            )
        fs['eleistungen'] = ' '.join([str(leist['le']) for leist in leistungen])
        single_kat_felder = ('zm', 'qualij', 'hkm', 'hkv', 'bkm', 'bkv',
                             'qualikm', 'qualikv',
                             'ba1', 'ba2', 'pbe', 'pbk', )
        for f in single_kat_felder:
            fs[f] = ' ' # leere, selektierte Option, es muss aktiv ausgewählt werden

        # falls unter 14 Beschäftigung vorbelegen
        try:
            if alter < 14:
                fs['qualij'] = cc('fsqualij', '7')
        except:
            pass
        anm = fall['anmeldung']
        if anm:
            fs['zm'] = anm[0]['zm']
        joker_felder = ('joka1', 'joka2', 'joka3', 'joka4',
                        'jokf5', 'jokf6', 'jokf7', 'jokf8',)
        for f in joker_felder:
            if fs_customize.multifeld(f):
                fs[f] = None
            else:
                fs[f] = ' ' # leere, selektierte Option, es muss aktiv ausgewählt werden
        termin_felder = ('kkm', 'kkv', 'kki', 'kpa', 'kfa',
                         'ksoz', 'kleh', 'kerz', 'kkonf', 'kson', 'kat',)
        if config.BERATUNGSKONTAKTE and not config.BERATUNGSKONTAKTE_BS:
            from ebkus.html.beratungskontakt import get_fs_kontakte
            get_fs_kontakte(fall, fs)
        else:
            for f in termin_felder:
                fs[f] = 0
        #print '***********FSNEU', fs
        return self._process(title='Neue Fachstatistik erstellen',
                             file='fseinf',
                             fs=fs,
                             )

# kann auch als updfsform angesprochen werden (siehe EBKuS.py)
# wird in menu_templates.py verwendet
class updfs(_fachstatistik):
    permissions = Request.STAT_PERM
    def processForm(self, REQUEST, RESPONSE):
        fsid = self.form.get('fsid')
        fallid = self.form.get('fallid')
        if fsid:
            fs = Fachstatistik(fsid)
        elif fallid:
            fall = Fall(fallid)
            fs_list = fall['fachstatistiken']
            if not fs_list:
                raise EE('Noch keine Fachstatistik f&uuml;r den Fall vorhanden.')
            else:
                fs = fs_list[-1] # müsste eigentlich immer nur eine sein ...
        else:
            self.last_error_message = "Keine ID für die Fachstatistik erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
        return self._process(title='Fachstatistik &auml;ndern',
                             file='updfs',
                             fs=fs,
                             )



        
        
        
        
        
        
        
        
        
        
        
