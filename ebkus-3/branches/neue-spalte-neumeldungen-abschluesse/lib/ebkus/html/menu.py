# coding: latin-1
import string
from ebkus.app import Request
from ebkus.app.ebapi import today, ZustaendigkeitList, TabellenID
from ebkus.app_surface.menu_templates import *
from ebkus.app_surface.standard_templates import *
from ebkus.config import config

class menu(Request.Request):
    permissions = Request.MENU_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        mitarbeiterliste = self.getMitarbeiterliste()
        user = self.user
        stelle = self.stelle
        mitarbeiter = self.mitarbeiter
        # damit das logo auf dem Hauptmenü auf die Eingangsseite der Instanz
        # verlinken kann
        mitarbeiter['index_url'] = "/ebkus/%s/index.html" % config.INSTANCE_NAME
        res = []
        if mitarbeiter['benr__code'] == 'bearb':
            res.append(head_normal_t % ('Hauptmen&uuml;'))
            zustaendigkeiten = ZustaendigkeitList(where = 'ed = 0 and mit_id = %s'
                                                  % mitarbeiter['id'] )
            zustaendigkeiten.sort('mit_id__na', 'fall_id__akte_id__na',
                                  'fall_id__akte_id__vn')
            res.append(main_menu_t % mitarbeiter)
            for z in zustaendigkeiten:
                if z['fall_id__akte_id__stzak'] == stelle['id']:
                    res.append(klientauswahl_t % z)
            res.append(menusubmit_t )
            
        elif mitarbeiter['benr__code'] == 'verw':
            res.append(head_normal_t % ('Hauptmen&uuml;'))
            zustaendigkeiten = ZustaendigkeitList(where = 'ed = 0', order = 'id')
            zustaendigkeiten.sort('mit_id__na', 'fall_id__akte_id__na',
                                  'fall_id__akte_id__vn')
            res.append(main_menu_t % mitarbeiter)
            for z in zustaendigkeiten:
                if z['fall_id__akte_id__stzak'] == stelle['id']:
                    res.append(klientauswahl_t % z)
            res.append(menusubmit_t )
            
            # Admin soll keine Klientennamen erhalten, er braucht nur das Admin-Menu.
        elif mitarbeiter['benr__code'] == 'admin':
            res.append(head_normal_ohne_help_t % ('Hauptmen&uuml;'))
            prottabid = TabellenID(table_name = 'protokoll')
            grenze = prottabid['maxid']
            res.append(administration_t % grenze)
            
        elif mitarbeiter['benr__code'] == 'protokol':
            res2 = []
            meldung = {'titel':'Gesicherter Bereich!',
                      'legende':'Achtung!',
                      'zeile1':'Sie betreten einen Hochsicherheitsbereich',
                      'zeile2':'Sie werden zur Protokoll - Anmeldung weitergeleitet.','url':'login_formular'}
            res2.append(meldung_weiterleitung_t % meldung)
            return string.join(res2, '')
        return string.join(res, '')
        
        
        
        
        
        
        
        
