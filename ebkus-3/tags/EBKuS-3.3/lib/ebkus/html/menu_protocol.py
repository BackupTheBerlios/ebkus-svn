# coding: latin-1

import os, stat, time, rotor

from ebkus.config import config
from ebkus.app.session import get_session
from ebkus.app import Request
from ebkus.app.ebapi import cc, ProtokollList, Code, Mitarbeiter
from ebkus.app_surface.standard_templates import *
from ebkus.app_surface.protokoll_templates import *
from ebkus.db.sql import execute
from ebkus.app import protocol

class menu_protocol(Request.Request):
    permissions = Request.PROTOCOL_MENU

    def checkAuth(self):
        """Überschreibt Request.checkAuth.
        Prüft anhand der Session, ob zwei protokollberechtigte
        Benutzer angemeldet sind."""

        self.session = get_session(self.REQUEST, self.RESPONSE)
        if self.session:
            self.user = self.session.user
        else:
            raise Request.NichtIdentifiziert()
        mitarbeiter1 = self.mitarbeiter = Mitarbeiter(ben=self.user,
                                                      stat=cc('status', 'i'))
        # nun das protokoll-spezifische
        try:
            user1 = self.session.data['protokollbenutzer1']
            user2 = self.session.data['protokollbenutzer2']
            assert user1 == self.user
            mitarbeiter2 = Mitarbeiter(ben=user2,
                                       stat=cc('status', 'i'))
            assert mitarbeiter1['benr__code'] in self.permissions
            assert mitarbeiter2['benr__code'] in self.permissions
        except:
            return zugriffVerweigert()

##     # tbd keine Authentifizierung, nur zum testen, 
##     def checkAuth(self):
##         self.user = 'pruefer1'
##         self.mitarbeiter = Mitarbeiter(ben=self.user,
##                                        stat=cc('status', 'i'))

    def zugriffVerweigert(self):
        meldung = {'titel': 'Zugriff verweigert!',
                   'legende': 'Zugriff Verweigert!',
                   'url':'login',
                   'zeile1': 'Sie haben keine Zugriffsberechtigung.',
                   'zeile2': 'Bitte melden Sie sich neu an.'}
        return (meldung_weiterleitung_t % meldung)


    def processForm(self, REQUEST, RESPONSE):
        # Formulardaten holen
        archivfiles = os.listdir(config.PROTOCOL_DIR)
        protokolleintrag = self.form.get('protokolleintrag')
        von_id = self.form.get('von_id')
        bis_id = self.form.get('bis_id')
        archivdatei = self.form.get('archiv_datei')
        protocolanaus = self.form.get('protocolanaus')

        # toggle Protokoll an/aus
        if protocolanaus == 'protocolanaus':
            if protocol.is_on():
                protocol.off()
                anaustext = 'aus'
            else:
                protocol.on()
                anaustext = 'an'
            meldung = {
                'titel':'Prokollierung',
                'legende':'Protokollierung',
                'url':'menu_protocol',
                'zeile1':'Folgende &Auml;nderungen wurden durchgef&uuml;hrt:',
                'zeile2':'Die Protokollierung wurde %sgeschaltet' % anaustext
                }
            return meldung_weiterleitung_t % meldung

        res = []
        res.append(head_normal_ohne_help_t % ('Protokollansicht/-bearbeitung'))

        # Einzelanzeige
        if protokolleintrag:
            res.append(singleprotocolview_head_t)
            protokolleintraege = self.get_protokoll_eintraege(id_list=protokolleintrag)
            for p in protokolleintraege:
                res.append(singleprotocolview_mid_t % p)
            res.append(singleprotocolview_end_t)
            return ''.join(res)

        # Archivdatei anzeigen
        if archivdatei:
             # für Datumskonvertierung
            tmp_yek = "2001.12.31"
            archivfile = os.path.join(config.PROTOCOL_DIR, archivdatei)
            rot = rotor.newrotor(tmp_yek)
            fdatei1 = open(archivfile, "rb")
            line = fdatei1.readline()
            res.append(dateitop_t)
            while line:
                res.append( rot.decryptmore(line))
                line = fdatei1.readline()
            res.append(dateiend_t)
            fdatei1.close()
            return ''.join(res)
        
        # Ansonsten Menu anzeigen
        if protocol.is_on():
            anaustext = 'Aus'
        else:
            anaustext = 'An'
        protokolleintraege = self.get_protokoll_eintraege(von_id, bis_id)
        von_id = von_id or protokolleintraege and protokolleintraege[0]['nr'] or '0'
        bis_id = bis_id or protokolleintraege and protokolleintraege[-1]['nr'] or '0'
        res.append(auswahlprotocol_t % (anaustext, von_id, bis_id, self.get_max_id()))
        for p in protokolleintraege:
            res.append(protocolauswahl_t % p)
        res.append(protocolsubmit_t )
        res.append(archivfile_head_t)

        files_to_sort = [(os.stat(os.path.join(config.PROTOCOL_DIR, f))[stat.ST_CTIME],
                          f) for f in archivfiles]
        files_to_sort.sort()
        files_to_sort.reverse()
        for ctime, afile in files_to_sort:
            dateides = os.stat(os.path.join(config.PROTOCOL_DIR, afile))
            dateigroesse = dateides[6]
            local_time_tupel = time.localtime(ctime)
            dateitime =time.strftime("%d.%m.%y um %H:%M:%S", local_time_tupel)
            local_time_tupel = time.localtime(dateides[8]) # ST_MTIME
            dateitime2 =time.strftime("%d.%m.%y um %H:%M:%S", local_time_tupel)
            res.append(archivfile_mid_t % ("archiv_datei", afile, afile,
                                           dateigroesse, dateitime, dateitime2))

        res.append(archivfile_end_t)
        return ''.join(res)

    def get_protokoll_eintraege(self, von_id=None, bis_id=None, id_list=None):
        """Falls id_list nicht leer ist, genau diese.
        Falls von_id und bis_id fehlen, (max_id - 100) bis max_id.
        Ansonsten von_id bis bis_id, jeweils um 1 bzw. maxid
        ergänzt, falls eine Angabe fehlt
        """
        try:
            protocol.temp_off()
            if id_list:
                if type(id_list) == type([]):
                    ids = ','.join(id_list)
                else:
                    ids = id_list
                return ProtokollList(where='nr in (%s)' % ids, order='nr')
            maxid = self.get_max_id()
            if not von_id and not bis_id:
                von_id = maxid - 100
                bis_id = maxid
            elif not von_id:
                von_id = 1
            elif not bis_id:
                bis_id = maxid
            return ProtokollList(where = 'nr >= %s and nr <= %s' %
                                 (von_id, bis_id), order='nr')
        finally:
            protocol.temp_on()

    def get_max_id(self):
        try:
            # cache
            return self.maxid
        except:
            res = execute("SELECT max(nr) FROM protokoll")
            self.maxid = res[0][0] or 0
            return self.maxid
    
