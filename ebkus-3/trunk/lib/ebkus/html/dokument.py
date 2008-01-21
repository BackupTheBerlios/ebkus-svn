# coding: latin-1

"""Module für die Dokumente."""

import os

from ebkus.app import Request
from ebkus.app.ebapi import Fall, Akte, Dokument, Gruppendokument, DokumentList, \
     GruppendokumentList, Gruppe, today, cc, get_akte_path, get_gruppe_path, is_binary
from ebkus.app.ebapih import get_codes, mksel
from ebkus.app_surface.dokument_templates import *
from ebkus.app_surface.standard_templates import *

import ebkus.html.htmlgen as h
from ebkus.html.akte_share import akte_share


class _dokument(Request.Request, akte_share):
    def _edit_dokument(self,
                       title,
                       file,
                       dok,
                       ):
        #print '_EDIT_DOKUMENT', file, dok
        fall_id = dok.get('fall_id')
        if fall_id:
            fall = Fall(fall_id)
            hidden_val = ('fallid', fall_id)
        else:
            fall = None
            gruppe = Gruppe(dok['gruppe_id'])
            hidden_val = ('gruppeid', gruppe['id'])
        new = file in ('dokeinf', 'dokgreinf', 'uploadeinf', 'uploadgreinf')
        upload = file in ('uploadeinf', 'uploadgreinf')
        meta = h.FieldsetInputTable(
            legend='Betreff, Art, Datum',
            daten=[[h.SelectItem(label='Art des Dokuments',
                                 name='art',
                                 options=self.for_kat('dokart', sel=dok['art']),
                                 ),
                    h.DatumItem(label='Datum',
                                name='v',
                                date=dok.getDate('v'),
                                ),
                    ],
                   [h.TextItem(label='Betreff',
                               name='betr',
                               value='%(betr)s' % dok,
                               class_='textboxverylarge',
                               n_col=4,
                               ),
                    ],
                   ],
            )
        if upload:
            inp = h.FieldsetInputTable(
                legend='Datei importieren',
                daten=[[h.UploadItem(label='Lokaler Dateiname',
                                     name='datei',
                                     tip='Lokale Datei hochladen',
                                     class_='textboxlarge',
                                     ),
                        ]],
                )
        elif not is_binary(dok):
            inp = h.FieldsetInputTable(
                legend='Inhalt',
                daten=[[h.TextareaItem(label_width='122pt',
                                       name='text',
                                       value=dok['text'],
                                       rows='10',
                                       cols='70',
                                       class_='textareaverylarge',
                                       tip='Text schreiben oder einfügen',
                                     ),
                ]],
                )
        else:
            inp = None
        if fall:
            breadcrumbs = (('Hauptmenü', 'menu'),
                           ('Klientendokumente', 'kldok?fallid=%(id)s' % fall),
                           )
        else:
            breadcrumbs = (('Hauptmenü', 'menu'),
                           ('Gruppenmenü', 'menugruppe'),
                           ('Gruppendokumente', 'grdok?gruppeid=%(id)s' % gruppe),
                           )
##         help={'uploadeinf': 'dateiimport',
##               'uploadgreinf': 'dateiimport',
##               # etc
##               }[file],
        res = h.FormPage(
            title=title,
            # TODO hier müssen neue Kapitel  rein, oder nachsehen
            breadcrumbs=breadcrumbs,
            #help=help,
            name='dokform',
            action=fall and 'kldok' or 'grdok',
            method='post',
            hidden=(('file', file),
                    ('dokid', dok['id']),
                    ('mitid', dok['mit_id']),
                    hidden_val,
                    ),
            rows=(fall and self.get_klientendaten_kurz(fall) or
                  self.get_gruppendaten_kurz(gruppe),
                  meta,
                  inp,
                  h.SpeichernZuruecksetzenAbbrechen(),
                  ),
            )
        return res.display()

class vermneu(_dokument):
    """Neuen Text  eintragen (Tabelle: Dokument, Gruppendokument)."""
    permissions = Request.VERM_PERM
    def processForm(self, REQUEST, RESPONSE):
        # Das Formular ist 1 Fall oder 1 Gruppe zugeordnet.
        gruppeid = self.form.get('gruppeid')
        fallid = self.form.get('fallid')
        if gruppeid:
            gruppe = Gruppe(gruppeid)
            dok = Gruppendokument()
            dok.init(
                id=Gruppendokument().getNewId(),
                gruppe_id=gruppe['id'],
                )
            file = 'dokgreinf'
        elif fallid:
            fall = Fall(fallid)
            dok = Dokument()
            dok.init(
                id=Dokument().getNewId(),
                fall_id=fall['id'],
                )
            file = 'dokeinf'
            dokid = Dokument().getNewId()
        else:
            self.last_error_message = "Keine ID fuer Gruppe oder Fall erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)

        dok.setDate('v', today())
        dok.init(
            mit_id=self.mitarbeiter['id'],
            art=cc('dokart', 'bnotiz'),
            mtyp=cc('mimetyp', 'txt'),
            )
        dok['text'] = '' # kein db-Feld!
        return self._edit_dokument(title='Neues Textdokument erstellen',
                                   file=file,
                                   dok=dok,
                                   )
    
##         dokarten = get_codes('dokart')
##         dokarten.sort('name')
        
##         # Liste der Templates als String
        
##         res = []
##         res.append(head_normal_t % header)
##         res.append(tabkopf)
##         res.append(formhiddenvalues_t % hidden)
##         res.append(formhiddennamevalues_t % hiddendokid)
##         res.append(vermneu_t % today() )
##         res.append(vermneu2_t % self.mitarbeiter)
##         mksel(res, codeliste_t, dokarten, 'name', 'Beraternotiz')
##         res.append(vermneu3_t)
##         return string.join(res, '')
        
        
class updverm(_dokument):
    """Text ändern (Tabelle: Dokument, Gruppendokument)."""
    permissions = Request.VERM_PERM
    def processForm(self, REQUEST, RESPONSE):
        # Das Formular ist 1 Fall oder 1 Gruppe zugeordnet.
        gruppeid = self.form.get('gruppeid')
        fallid = self.form.get('fallid')
        dokid = self.form.get('dokid')
        if not dokid:
            self.last_error_message = "Keine ID fuer Dokument erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
        if gruppeid:
            dok = Gruppendokument(dokid)
            file='updgrvermeinf'
            gruppe_path = get_gruppe_path(int(gruppeid))
            fname = os.path.join(gruppe_path, dok['fname'])
        elif fallid:
            file='updvermeinf'
            dok = Dokument(dokid)
            fall = Fall(fallid)
            fname = os.path.join(get_akte_path(fall['akte__id']),
                                 dok['fname'])
        else:
            self.last_error_message = "Keine ID fuer Gruppe oder Fall erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
        if not is_binary(dok):
            dok['text'] = open(fname, 'r').read()
        return self._edit_dokument(title='Dokument bearbeiten',
                                   file=file,
                                   dok=dok,
                                   )
##         # Fuer FORM-HIDDEN-VALUES
        
##         hidden ={'file': 'updvermeinf'}
##         hiddendokid ={'name': 'dokid', 'value': dokid}
        
##         # Liste der Templates als String
        
##         res = []
##         res.append(head_normal_t %("Texteintrag der Akte &auml;ndern"))
##         res.append(formkopfdokneu_t % fall)
##         res.append(formhiddenvalues_t % hidden)
##         res.append(formhiddennamevalues_t % hiddendokid)
##         res.append(vermupd_t % dok )
##         res.append(vermneu2_t % self.mitarbeiter)
##         del dok['text']
##         mksel(res, codeliste_t, dokarten, 'id', dok['art'])
##         res.append(vermneu3_t)
##         return string.join(res, '')

# dieselber Prozedur für Gruppendolumente
updgrverm = updverm

## class updvermausw(_dokument):
##     """Auswahlbox zum Öffnen eines Textes
##     (Tabellen: Dokument, Gruppendokument)."""
    
##     permissions = Request.VERM_PERM
    
##     def processForm(self, REQUEST, RESPONSE):
##         mitarbeiterliste = self.getMitarbeiterliste()
##         user = self.user
        
##         # Das Dokument ist 1 Fall oder 1 Gruppe zugeordnet.
        
##         if self.form.has_key('fallid'):
##             fallid = self.form.get('fallid')
##             fall = Fall(int(fallid))
##             akte = Akte(fall['akte_id'])
##             dokliste = DokumentList(where = 'fall_id = %s and mit_id = %s and mtyp = %s'
##                                         % (fall['id'], self.mitarbeiter['id'],
##                                            cc('mimetyp', 'txt')), order = 'vy,vm,vd')
            
##             header = "Texteintrag der Akte zum &Auml;ndern ausw&auml;hlen"
##             hidden ={'file': 'updverm'}
##             formkopf = formkopfdokneu_t % fall
            
##         elif self.form.has_key('gruppeid'):
##             gruppeid = self.form.get('gruppeid')
##             gruppe = Gruppe(int(gruppeid))
##             dokliste = GruppendokumentList(where = 'gruppe_id = %s and mit_id = %s and mtyp = %s'
##                                         % (gruppe['id'], self.mitarbeiter['id'],
##                                            cc('mimetyp', 'txt')), order = 'vy,vm,vd')
            
##             header = "Texteintrag der Gruppe zum &Auml;ndern ausw&auml;hlen"
##             hidden ={'file': 'updgrverm'}
##             formkopf = formkopfdokgrneu_t % gruppe
            
##         else:
##             self.last_error_message = "Keine ID fuer Fall oder Gruppe erhalten"
##             return self.EBKuSError(REQUEST, RESPONSE)
            
##             # Liste der Templates als String
            
##         res = []
##         res.append(head_normal_t % header)
##         res.append(formkopf)
##         res.append(formhiddenvalues_t % hidden)
##         res.append(vermausw_t)
##         for d in dokliste:
##             res.append(vermausw2_t % d)
##         res.append(vermausw3_t)
##         return string.join(res, '')
        
        
class upload(_dokument):
    """Dokument uploaden (Tabellen: Dokument, Gruppendokument)."""
    permissions = Request.VERM_PERM
    def processForm(self, REQUEST, RESPONSE):
        gruppeid = self.form.get('gruppeid')
        fallid = self.form.get('fallid')
        if gruppeid:
            gruppe = Gruppe(gruppeid)
            dok = Gruppendokument()
            dok.init(
                id=Gruppendokument().getNewId(),
                gruppe_id=gruppe['id'],
                )
            file = 'uploadgreinf'
        elif fallid:
            fall = Fall(fallid)
            dok = Dokument()
            dok.init(
                id=Dokument().getNewId(),
                fall_id=fall['id'],
                )
            file = 'uploadeinf'
            dokid = Dokument().getNewId()
        else:
            self.last_error_message = "Keine ID fuer Gruppe oder Fall erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
        dok.setDate('v', today())
        dok.init(
            mit_id=self.mitarbeiter['id'],
            art=cc('dokart', 'Bericht'),
            )
        return self._edit_dokument(title='Dokument importieren',
                                   file=file,
                                   dok=dok,
                                   )

##         mitarbeiterliste = self.getMitarbeiterliste()
##         user = self.user
        
##         if self.form.has_key('gruppeid'):
##             gruppeid = self.form.get('gruppeid')
##             gruppe = Gruppe(int(gruppeid))
##             action = "grdok"
##             hidden = {'file': 'uploadgreinf'}
##             dokid = Gruppendokument().getNewId()
##             hiddendokid ={'name': 'dokid', 'value': dokid}
##             header = "Datei zur Gruppe importieren"
##             tabkopf = formulargrh_t % gruppe
##         elif self.form.has_key('fallid'):
##             fallid = self.form.get('fallid')
##             fall = Fall(int(fallid))
##             akte = Akte(fall['akte_id'])
##             action = "kldok"
##             hidden = {'file': 'uploadeinf'}
##             dokid = Dokument().getNewId()
##             hiddendokid ={'name': 'dokid', 'value': dokid}
##             header = "Datei in die Akte aufnehmen"
##             tabkopf = formularh_t % fall
##         else:
##             self.last_error_message = "Keine ID fuer Fall oder Gruppe erhalten"
##             return self.EBKuSError(REQUEST, RESPONSE)
            
##         dokartl = get_codes('dokart')
##         dokartl.sort('name')
        
##         # Liste der Templates als String
        
##         res = []
##         res.append(head_normal_t % header)
##         res.append(uploadformh_t % action)
##         res.append(formhiddenvalues_t % hidden)
##         res.append(formhiddennamevalues_t % hiddendokid)
##         res.append(tabkopf)
##         res.append(uploadform_t % today())
##         res.append(uploadform2_t % self.mitarbeiter)
##         mksel(res, codeliste_t, dokartl, 'name', 'Bericht')
##         res.append(uploadform3_t)
##         page = string.join(res, '')
##         #print "UPLOADPAGE: "
##         #print page
##         return page
        
        
## class updgrverm(_dokument):
##     """Update Gruppendokument (Tabelle: Gruppendokument)."""
    
##     permissions = Request.VERM_PERM
    
##     def processForm(self, REQUEST, RESPONSE):
##         mitarbeiterliste = self.getMitarbeiterliste()
##         user = self.user
##         if self.form.has_key('dokid'):
##             dokid = self.form.get('dokid')
##         else:
##             self.last_error_message = "Keine ID fuer Dokument erhalten"
##             return self.EBKuSError(REQUEST, RESPONSE)
##         dok = Gruppendokument(int(dokid))
##         gruppe = Gruppe(dok['gruppe_id'])
##         dokarten = get_codes('dokart')
##         dokarten.sort('name')
        
##         try:
##             gruppe_path = get_gruppe_path(gruppe['id'])
##             f = open('%s/%s'
##                      % (gruppe_path,dok['fname']), 'r')
##             text = f.read()
##             f.close()
##         except Exception, e:
##             meldung = {'titel':'Fehler',
##                        'legende':'Fehlerbeschreibung',
##                        'zeile1': str(e),
##                        'zeile2':'Versuchen Sie es bitte erneut.'}
##             return (meldung_t %meldung)
            
##         dok['text'] = text
        
##         header = "Texteintrag der Gruppe &auml;ndern"
        
##         # Fuer FORM-HIDDEN-VALUES
        
##         hidden ={'file': 'updgrvermeinf'}
##         hiddendokid ={'name': 'dokid', 'value': dokid}
        
##         # Liste der Templates als String
        
##         res = []
##         res.append(head_normal_t % header)
##         res.append(formkopfdokgrneu_t % gruppe)
##         res.append(formhiddenvalues_t % hidden)
##         res.append(formhiddennamevalues_t % hiddendokid)
##         res.append(vermupd_t % dok )
##         res.append(vermneu2_t %self.mitarbeiter)
##         del dok['text']
##         mksel(res, codeliste_t, dokarten, 'id', dok['art'])
##         res.append(vermneu3_t)
##         return string.join(res, '')
        
        
class rmdok(_dokument):
    """Lösche Dokument (Tabellen: Dokument, Gruppendokument)."""
    permissions = Request.RMDOK_PERM
    def processForm(self, REQUEST, RESPONSE):
        dokid = self.form.get('dokid')
        fallid = self.form.get('fallid')
        gruppeid = self.form.get('gruppeid')
        if not dokid:
            self.last_error_message = "Keine ID für Dokument erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
        if fallid:
            dok = Dokument(dokid)
            file = 'removedoks'
            action = 'kldok'
            hidden_val = ('fallid', fallid)
        elif gruppeid:
            dok = Gruppendokument(dokid)
            file = 'removegrdoks'
            action = 'grdok'
            hidden_val = ('gruppeid', gruppeid)
        else:
            self.last_error_message = "Keine ID fuer Fall oder Gruppe erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
        return h.SubmitOrBack(
            legend='Dokument löschen',
            action=action,
            method='post',
            hidden=(('file', file),
                    ('dokids', dokid),
                    hidden_val,
                    ),
            zeilen=('Soll ','',
                    "%(art__name)s: %(betr)s (Typ: %(mtyp__code)s, Datum: %(vd)s.%(vm)s.%(vy)s, Mitarbeiter: %(mit_id__na)s)" % dok, '',
                    ' gelöscht werden?',
            )
            ).display()
##         dokliste.sort('art__name','vy','vm','vd')
        
##         # Liste der Templates als String
        
##         res = []
##         res.append(head_normal_t % header)
##         res.append(formkopf)
##         res.append(formhiddenvalues_t % hidden)
##         res.append(rmverm_t )
##         for d in dokliste:
##             res.append(rmverm2_t % d)
##         res.append(rmverm3_t)
##         return string.join(res, '')
        
        
        
