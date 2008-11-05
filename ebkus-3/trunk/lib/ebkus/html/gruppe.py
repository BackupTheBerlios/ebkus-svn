# coding: latin-1

"""Module für Gruppen."""

from ebkus.app import Request
from ebkus.app.ebapi import Gruppe, MitarbeiterGruppeList, \
     FallGruppe, BezugspersonGruppe, \
     ZustaendigkeitList, getNewGruppennummer, Date, today

import ebkus.html.htmlgen as h
from ebkus.html.akte_share import akte_share

class menugruppe(Request.Request, akte_share):
    """Hauptmenü der Gruppenkartei (Tabellen: Gruppe, MitarbeiterGruppe)."""
    permissions = Request.MENUGRUPPE_PERM
    def for_gruppen(self):
        """Optionen für Gruppenauswahl erstellen"""
        option_t = '<option value="%(gruppe_id)s">%(mit_id__na)s | %(gruppe_id__name)s | %(gruppe_id__gn)s</option>\n'
        options = ''
        where = "gruppe.stz=%s" % self.stelle['id']
        if self.mitarbeiter['benr__code'] == 'bearb':
            where += ' and mit_id = %s' % self.mitarbeiter['id']
        elif self.mitarbeiter['benr__code'] == 'verw':
            pass
        else:
            raise EE('Keine Berechtigung')
        mitarbeitergruppenl = MitarbeiterGruppeList(
                where=where,
                join=[('gruppe', 'mitarbeitergruppe.gruppe_id=gruppe.id')])
        mitarbeitergruppenl.sort('mit_id__na', 'gruppe_id__name')
        for m in mitarbeitergruppenl:
            options += option_t % m
        return options
        
    def processForm(self, REQUEST, RESPONSE):
        gruppe = h.FieldsetFormInputTable(
            action='grkarte',
            name='gruppeform',
            method='post',
            legend='Gruppenauswahl', 
            daten=[
                   [h.SelectItem(name='gruppeid',
                                 size="12",
                                 class_="listbox280",
                                 tip="Alle Gruppen, für die Sie Zugriffsrechte haben",
                                 options=self.for_gruppen(),
                                 n_col=4,
                                 nolabel=True,
                                 ),
                    ],
                   [h.RadioItem(label='Gruppenkarte',
                                name='file',
                                value='grkarte',
                                checked=True,
                                tip='Gruppenkarte für ausgewählte Gruppe ansehen',
                                ),
                    h.RadioItem(label='Gruppendokumente',
                                name='file',
                                value='grdok',
                                tip='Gruppendokumente für ausgewählte Gruppe ansehen',
                                ),
                    ],
                   [h.DummyItem(n_col=4)],
                   [h.Button(value='Ok',
                             type='submit',
                             n_col=2,
                             ),
                    h.Button(value='Neue Gruppe',
                             type='button',
                             onClick="go_to_url('gruppeneu')",
                             tip='Neue Gruppe anlegen',
                             n_col=2,
                             ),
                    ],
                   ],
            )
        hauptmenu = h.FieldsetInputTable(
            daten=[[h.Button(value='Hauptmenü',
                             onClick="go_to_url('menu')",
                             tip="Hauptmenü",
                             ),
            ]]
            )
        res = h.Page(
            title='Gruppenmenü',
            help="das-gruppenmen",
            breadcrumbs = (('Hauptmenü', 'menu'),
                           ),
            rows=(h.Pair(left=(hauptmenu,
                               self.get_suche(),
                               ),
                         right=(gruppe,
                                ),
                         ),
                  ),
            )
        return res.display()

class _gruppe(Request.Request,akte_share):
    def _display_gruppendaten(self,
                      file,
                      title,
                      gruppe,
                      ):
        res = h.FormPage(
            title=title,
            name='gruppenform',action="grkarte",method="post",
            breadcrumbs = (('Hauptmenü', 'menu'),
                           ('Gruppenmenü', 'menu'),
                          (not file=='gruppeeinf') and
                           ('Gruppenkarte', 'grkarte?gruppeid=%s' % gruppe['id'])
                           or None,
                           ),
            hidden=(("gruppeid", gruppe['id']),
                    ("file", file),
                    ("stz", gruppe['stz']),
                    ),
            rows=(self.get_gruppendaten(gruppe, readonly=False),
                  h.SpeichernZuruecksetzenAbbrechen(),
                  ),
            )
        return res.display()

class gruppeneu(_gruppe):
    """Neue Gruppe eintragen (Tabellen: Gruppe, MitarbeiterGruppe)."""
    permissions = Request.GRUPPENEU_PERM
    def processForm(self, REQUEST, RESPONSE):
        gruppe = Gruppe()
        gruppe.init(
            id=Gruppe().getNewId(),
            tzahl=None,
            stzahl=None,
            teiln=None,
            grtyp=None,
            stz=self.stelle['id'],
            mitarbeiter=[{'mit_id':self.mitarbeiter['id']}],
            )
        gruppe.setDate('bg', today())
        gruppe.setDate('e', Date(0,0,0))
        return self._display_gruppendaten(file='gruppeeinf',
                                          title='Neue Gruppe erstellen',
                                          gruppe=gruppe)

class updgruppe(_gruppe):
    """Gruppe ändern (Tabellen: Gruppe, MitarbeiterGruppe)."""
    permissions = Request.GRUPPENEU_PERM
    def processForm(self, REQUEST, RESPONSE):
        gruppeid = self.form.get('gruppeid')
        if gruppeid:
            gruppe = Gruppe(gruppeid)
        else:
            self.last_error_message = "Keine ID fuer die Gruppe erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
        return self._display_gruppendaten(file='updgr',
                                          title='Gruppendaten bearbeiten',
                                          gruppe=gruppe)
        
class gruppeteilnausw(Request.Request, akte_share):
    """Teilnehmerauswahl (Tabellen: FallGruppe, BezugspersonGruppe)."""
    permissions = Request.GRUPPETEILN_PERM
    def processForm(self, REQUEST, RESPONSE):
        gruppeid = self.form.get('gruppeid')
        if gruppeid:
            gruppe = Gruppe(gruppeid)
        else:
            self.last_error_message = "Keine ID fuer die Gruppe erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
        klientenauswahl = h.FieldsetInputTable(
            legend='Klientenauswahl', 
            daten=[[h.SelectItem(name='fallid',
                                 size="10",
                                 multiple=True,
                                 class_="listbox220",
                                 tip="Alle offene Fälle, für die Sie Zugriffsrechte haben",
                                 options=self.for_klienten(kurz=True,order='akte_na'),
                                 nolabel=True,
                                 ),
                    ]])
        bezugspersonenauswahl = h.FieldsetInputTable(
            legend='Bezugspersonenauswahl', 
            daten=[[h.SelectItem(name='bezugspid',
                                 size="10",
                                 multiple=True,
                                 class_="listbox220",
                                 tip="Alle Bezugspersonen von offenen Fällen, für die Sie Zugriffsrechte haben",
                                 options=self.for_bezugspersonen(order='bp_na'),
                                 nolabel=True,
                                 ),
                    ]])
        datumsetzen = h.FieldsetInputTable(
            legend = 'Teilnahmezeitraum',
            daten = [[h.DatumItem(label='Beginndatum',
                                  name='bg',
                                  date=today(),
                                  ),
                      h.DatumItem(label='Endedatum',
                                  name='e',
                                  ),
                      ]]
            )
        res = h.FormPage(
            title='Teilnehmerauswahl',
            name='gruppenform',action="grkarte",method="post",
            breadcrumbs = (('Hauptmenü', 'menu'),
                           ('Gruppenmenü', 'menu'),
                           ('Gruppenkarte', 'grkarte?gruppeid=%s' % gruppe['id']),
                           ),
            hidden=(("gruppeid", gruppe['id']),
                    ("file", 'gruppeteilneinf'),
                    ("mitid", self.mitarbeiter['id']),
                    ),
            rows=(h.Pair(left=klientenauswahl,
                         right=bezugspersonenauswahl),
                  datumsetzen,
                  h.SpeichernZuruecksetzenAbbrechen(),
                  ),
            )
        return res.display()
        
class updteiln(Request.Request):
    """Teilnehmerdaten ändern (Tabellen: FallGruppe, BezugspersonGruppe)."""
    permissions = Request.GRUPPETEILN_PERM
    def processForm(self, REQUEST, RESPONSE):
        fallgr_id = self.form.get('fallgrid')
        bzpgr_id = self.form.get('bzpgrid')
        if not (fallgr_id or bzpgr_id):
            self.last_error_message = "Keine ID fuer Teilnehmer erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
        if bzpgr_id:
            bzpgr = obj = BezugspersonGruppe(bzpgr_id)
            name = "%(vn)s %(na)s" % bzpgr['bezugsp']
            hidden_val = ('bzpgrid', bzpgr_id)
            gruppe = bzpgr['gruppe']
        elif fallgr_id:
            fallgr = obj = FallGruppe(fallgr_id)
            name = "%(vn)s %(na)s" % fallgr['fall__akte']
            hidden_val = ('fallgrid', fallgr_id)
            gruppe = fallgr['gruppe']
        datumsetzen = h.FieldsetInputTable(
            legend = 'Teilnahmezeitraum für %s' % name,
            daten = [[h.DatumItem(label='Beginndatum',
                                  name='bg',
                                  date = obj.getDate('bg'),
                                  ),
                      h.DatumItem(label='Endedatum',
                                  name='e',
                                  date = obj.getDate('e'),
                                  ),
                      ]]
            )
        res = h.FormPage(
            title='Datum für Beginn und Ende der Gruppenteilnahme ändern',
            name="teilnform",action="grkarte",method="post",
            breadcrumbs = (('Hauptmenü', 'menu'),
                           ('Gruppenmenü', 'menu'),
                           ('Gruppenkarte', 'grkarte?gruppeid=%s' % gruppe['id'])
                           ),
            hidden=(("file", 'updgrteiln'),
                    ('gruppeid', gruppe['id']),
                    hidden_val,
                    ),
            rows=(datumsetzen,
                  h.SpeichernZuruecksetzenAbbrechen(),
                  )
            )
        return res.display()

class rmteiln(Request.Request):
    """Teilnehmer löschen (Tabellen: FallGruppe, BezugspersonGruppe)."""
    permissions = Request.RMTEILN_PERM
    def processForm(self, REQUEST, RESPONSE):
        fallgr_id = self.form.get('fallgrid')
        bzpgr_id = self.form.get('bzpgrid')
        if not (fallgr_id or bzpgr_id):
            self.last_error_message = "Keine ID fuer Teilnehmer erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
        name = ''
        if bzpgr_id:
            bzpgr = BezugspersonGruppe(bzpgr_id)
            name = "%(vn)s %(na)s" % bzpgr['bezugsp']
            hidden_val = ('bzpgrid', bzpgr_id)
            gruppe = bzpgr['gruppe']
        elif fallgr_id:
            fallgr = FallGruppe(fallgr_id)
            name = "%(vn)s %(na)s" % fallgr['fall__akte']
            hidden_val = ('fallgrid', fallgr_id)
            gruppe = fallgr['gruppe']
        return h.SubmitOrBack(
            legend='Teilnehmer entfernen',
            action='grkarte',
            method='post',
            hidden=(('file', 'removeteiln'),
                    ('gruppeid', gruppe['id']),
                    hidden_val,
                    ),
            zeilen=('Soll der Teilnehmer %s aus der Gruppe %s(%s) entfernt werden?' %
                    (name, gruppe['name'], gruppe['gn'],),
            )
            ).display()
