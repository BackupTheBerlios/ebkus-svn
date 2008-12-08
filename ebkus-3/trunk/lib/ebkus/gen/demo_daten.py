# coding: latin-1

import sys, os, time, sha
from ebkus.app.ebapi import cc, cn, getNewFallnummer, Date, today, str2date, getDate, setDate, \
     Kategorie, Code, Mitarbeiter, MitarbeiterList, Akte, Fall, FallList, Leistung, \
     Beratungskontakt, FeldList, \
     Zustaendigkeit, Bezugsperson, Einrichtungskontakt, CodeList, \
     StrassenkatalogNeuList, Fachstatistik, Jugendhilfestatistik, Jugendhilfestatistik2007, \
     Altdaten
from ebkus.app.ebapih import  get_codes
from ebkus.app.ebupd import akteeinf, fseinf, jgheinf, jgh07einf, miteinf, codeeinf, \
     leisteinf, zdaeinf, waufneinf, perseinf, einreinf
from ebkus.html.strkat import split_hausnummer
from random import choice, randrange, sample, random, seed

import logging
def log(s):
    logging.info(s)
    print s

seed(100) # zum Testen besser immer neu, da fallen mehr Fehler auf

N_AKTEN = 100
N_BEARBEITER = 4
N_STELLEN = 2
VON_JAHR = Date(2006)
BIS_JAHR = None
#TODAY = (2007,7,1)   # gefaked today, sollte im laufenden Demosystem auch gefaked werden
TODAY = None          # aktuelles Datum


def create_schulungs_daten(iconfig,                    # config Objekt für die entsprechende Instanz
                           logf=None):
##                       n_akten=N_AKTEN,            # Anzahl von Akten in der demo
##                       n_bearbeiter=N_BEARBEITER,  # Anzahl der Mitarbeiter in der Bearbeiterrolle
##                                                   # ohne explizite Angabe wachsend mit n_akten
##                       n_stellen=N_STELLEN,        # Anzahl der Stellen, default wachsend mit n_akten
##                       von_jahr=VON_JAHR,          # Jahr in dem die ersten Akten angelegt werden
##                                                   # default ist heute vor zwei Jahren
##                       bis_jahr=BIS_JAHR,          # Jahr in dem die letzten Akten angelegt werden,
##                                                   # default ist dieses Jahr
##                       fake_today=TODAY):          # gefaktes heute: (2009,6,6), default das reale heute 

##     n_akten = 400
##     n_bearbeiter = 16
##     n_stellen = 4
##     von_jahr = Date(2006)
##     bis_jahr = None
##     fake_today = None

##     n_akten = 600
##     n_bearbeiter = 20
##     n_stellen = 4
##     von_jahr = Date(2006)
##     bis_jahr = None
##     fake_today = None

    n_akten = 100
    n_bearbeiter = 4
    n_stellen = 2
    von_jahr = Date(2006)
    bis_jahr = None
    fake_today = None

    global config
    config = iconfig
    from ebkus.app import protocol
    #protocol.on()
    if logf:
        global log
        log = logf
    #handle_stellen_einrichtung_muster(n_stellen)
    handle_stellen_einrichtung(n_stellen)
    log("Heutiges Datum: %s" % today())
    ort = config.STRASSENKATALOG
    if ort:
        log("Demodaten für %s-Version" % ort)
    else:
        log("Demodaten für Standard Version")
    log("Instanz: %s" % config.INSTANCE_NAME)
    DemoDaten.n_akten = n_akten
    if not n_stellen:
        n_stellen = int(n_akten**.2)
    assert n_stellen < 27, "Zuviele Demostellen"
    if not n_bearbeiter:
        n_bearbeiter = int(n_akten**.3)
    if not bis_jahr:
        bis_jahr = today()
    if not von_jahr:
        von_jahr = bis_jahr.add_month(-24)
    DemoDaten.bis_jahr = bis_jahr
    DemoDaten.von_jahr = von_jahr
    stellen = DemoDaten.stellen = CodeList(where="kat_code='stzei'")
    if ort:
        DemoDaten.strkat = StrassenkatalogNeuList(where='')
        DemoDaten.ort = ort.capitalize()
    else:
        DemoDaten.ort = Code(kat_code='kr', sort=1)['name']
    # die beiden protokoll-Berechtigten
##     DemoDaten().fake_mitarbeiter(benr=cc('benr', 'protokol'), ben='pr1')
##     DemoDaten().fake_mitarbeiter(benr=cc('benr', 'protokol'), ben='pr2')

    ## gf1 wob1 wf1 bs1
    ## gf_verw wob_verw
    ## gf_admin wob_admin

    for i in range(n_stellen):
        stelle = stellen[i]
        code = stelle['code'].lower()
        for j in range(n_bearbeiter/n_stellen):
            ben = "%s%s" % (code, j+1)
            vn = "%s_vn" % ben
            na = "%s_na" % ben
            DemoDaten().fake_mitarbeiter(
                stelle=stelle,
                benr=cc('benr', 'bearb'),
                ben=ben,
                vn=vn,
                na=na,
                )
        # verw    
        ben = "%s_verw" % code
        DemoDaten().fake_mitarbeiter(
            stelle=stelle,
            benr=cc('benr', 'verw'),
            ben=ben,
            vn=ben+'_vn',
            na=ben+'_na',
            )
        # admin    
        ben = "%s_admin" % code
        DemoDaten().fake_mitarbeiter(
            stelle=stelle,
            benr=cc('benr', 'admin'),
            ben=ben,
            vn=ben+'_vn',
            na=ben+'_na',
            )

    # ich
    DemoDaten().fake_mitarbeiter(benr=cc('benr', 'bearb'),
                                 ben='test',
                                 vn='Test', na='Tester',
                                 stz=stellen[0]['id']) # immer Stelle A
    DemoDaten().fake_mitarbeiter(benr=cc('benr', 'verw'),
                                 ben='verw',
                                 vn='Verw', na='Verwaltungskraft',
                                 stz=stellen[0]['id']) # immer Stelle A
    DemoDaten.mitarbeiter = MitarbeiterList(where = 'stat = %s and benr = %s' %
                                            (cc('status', 'i'), cc('benr', 'bearb')))
    for i in range(1, n_akten+1):
        DemoDaten().fake_akte()
    # ohne feld 'id'
    fields = [f['feld'] for f in FeldList(
        where="tabelle.tabelle='altdaten'",
        join=[('tabelle', 'tabelle.id=feld.tab_id')])][1:]
    csv_path = os.path.join(config.EBKUS_HOME, 'sql', 'demo_altdaten.csv')
    csv_file = open(csv_path, 'wb')
    csv_file.write(';'.join(['"%s"' % f for f in fields]) + '\r\n')
    for i in range(1, 500):
        DemoDaten().fake_altdaten(csv_file, fields)
    log('Altdaten CSV generiert: %s' % csv_path)

def set_default_fachstatistik():
    from ebkus.html.fskonfig import fs_customize
    abzuschalten = (
        'ba1', 'ba2', 'pbe', 'pbk',
        'joka1', 'joka2', 'joka3', 'joka4', 
        'jokf5', 'jokf6', 'jokf7', 'jokf8',
        'no2', 'no3',
        )
    for f in abzuschalten:
        fs_customize.set_status(f, False)

def create_demo_daten(iconfig,                    # config Objekt für die entsprechende Instanz
                      logf=None,
                      n_akten=N_AKTEN,            # Anzahl von Akten in der demo
                      n_bearbeiter=N_BEARBEITER,  # Anzahl der Mitarbeiter in der Bearbeiterrolle
                                                  # ohne explizite Angabe wachsend mit n_akten
                      n_stellen=N_STELLEN,        # Anzahl der Stellen, default wachsend mit n_akten
                      von_jahr=VON_JAHR,          # Jahr in dem die ersten Akten angelegt werden
                                                  # default ist heute vor zwei Jahren
                      bis_jahr=BIS_JAHR,          # Jahr in dem die letzten Akten angelegt werden,
                                                  # default ist dieses Jahr
                      fake_today=TODAY):          # gefaktes heute: (2009,6,6), default das reale heute 
    set_default_fachstatistik()
    create_schulungs_daten(iconfig, logf)
    
## def create_demo_daten(iconfig,                    # config Objekt für die entsprechende Instanz
##                       logf=None,
##                       n_akten=N_AKTEN,            # Anzahl von Akten in der demo
##                       n_bearbeiter=N_BEARBEITER,  # Anzahl der Mitarbeiter in der Bearbeiterrolle
##                                                   # ohne explizite Angabe wachsend mit n_akten
##                       n_stellen=N_STELLEN,        # Anzahl der Stellen, default wachsend mit n_akten
##                       von_jahr=VON_JAHR,          # Jahr in dem die ersten Akten angelegt werden
##                                                   # default ist heute vor zwei Jahren
##                       bis_jahr=BIS_JAHR,          # Jahr in dem die letzten Akten angelegt werden,
##                                                   # default ist dieses Jahr
##                       fake_today=TODAY):          # gefaktes heute: (2009,6,6), default das reale heute 
##     global config
##     config = iconfig
##     from ebkus.app import protocol
##     #protocol.on()
##     if logf:
##         global log
##         log = logf
##     if config.BERLINER_VERSION:
##         # In der Berliner Version muss der Kreis, für den die Stelle
##         # zuständig ist, in der Sortierreihenfolge an erster Stelle
##         # stehen. Sonst funktionieren die Planungsräume nicht.
##         Code(kat_code='kr', code='01', name='Mitte').update({'sort': 4})
##         Code(kat_code='kr', code='04',
##              name='Charlottenburg-Wilmersdorf').update({'sort': 1})
        
##     # umbenennen des vordefinierten Stellenzeichens
##     Code(kat_code='stzei', code='A').update({'name': 'Stelle A', 'code': 'A'})
## ##     if fake_today:
## ##         today_date = Date(*fake_today)
## ##         global today
## ##         def today():
## ##             return today_date
## ##         import ebkus
## ##         ebkus.app.ebapi.today = today
##     if TODAY:
##         log("Gefaked: heutiges Datum: %s" % today())
##     log("Heutiges Datum: %s" % today())
##     ort = config.STRASSENKATALOG
##     if ort:
##         log("Demodaten für %s-Version" % ort)
##     else:
##         log("Demodaten für Standard Version")
##     log("Instanz: %s" % config.INSTANCE_NAME)
##     DemoDaten.n_akten = n_akten
##     if not n_stellen:
##         n_stellen = int(n_akten**.2)
##     assert n_stellen < 27, "Zuviele Demostellen"
##     if not n_bearbeiter:
##         n_bearbeiter = int(n_akten**.3)
##     if not bis_jahr:
##         bis_jahr = today()
##     if not von_jahr:
##         von_jahr = bis_jahr.add_month(-24)
##     DemoDaten.bis_jahr = bis_jahr
##     DemoDaten.von_jahr = von_jahr
##     for i in range(1, n_stellen):
##         DemoDaten().fake_stelle(i)
##     stellen = DemoDaten.stellen = CodeList(where="kat_code='stzei'")
##     if ort:
##         DemoDaten.strkat = StrassenkatalogNeuList(where='')
##         DemoDaten.ort = ort.capitalize()
##     else:
##         DemoDaten.ort = Code(kat_code='kr', sort=1)['name']
##     # die beiden protokoll-Berechtigten
##     DemoDaten().fake_mitarbeiter(benr=cc('benr', 'protokol'), ben='pr1')
##     DemoDaten().fake_mitarbeiter(benr=cc('benr', 'protokol'), ben='pr2')
##     # Verwaltungskraft
##     DemoDaten().fake_mitarbeiter(benr=cc('benr', 'verw'), ben='verw')
##     # Bearbeiter
##     for i in range(n_bearbeiter):
##         DemoDaten().fake_mitarbeiter(benr=cc('benr', 'bearb'), ben='bearb%s' % (i+1))
##     # ich
##     DemoDaten().fake_mitarbeiter(benr=cc('benr', 'bearb'),
##                                  ben='test',
##                                  vn='Test', na='Tester',
##                                  stz=stellen[0]['id']) # immer Stelle A
##     DemoDaten.mitarbeiter = MitarbeiterList(where = 'stat = %s and benr = %s' %
##                                             (cc('status', 'i'), cc('benr', 'bearb')))
##     for i in range(1, n_akten+1):
##         DemoDaten().fake_akte()


class DemoDaten(object):
    strassen = ('Teichweg', 'Müllerstr.', 'Am Rott', 'Karl-Marx-Str.',
                'Hinterm Markt', 'Rosenweg')
    orte = ('Unterhausen', 'Groß-Lehnau', 'Klein-Magrau')
    vornamen = ('Tom', 'Ögür', 'Frieda', 'Magda', 'Hugo', 'Peter', )
    namen = ('Haß', 'Öhlbrecht', 'Wäderich', 'Schmidt', 'Müller', 'Düsentrieb')
    def fake_stelle(self, i, **kw):
        """i=1 --> Stelle B
           i=2 --> Stelle C
           ...
        """
        code_id = Code().getNewId()
        form = {}
        form['codeid'] = code_id
        form['katcode'] = Kategorie(code='stzei')['code']
        form['katid'] = Kategorie(code='stzei')['id']
        form['code'] = kw.get('code', chr(ord('A') + i))
        form['name'] = kw.get('name', 'Stelle %s' % form['code'])
        form['sort'] = i + 1
        codeeinf(form)
        log(form['name'])

    def fake_mitarbeiter(self, **kw):
        form = {}
        form['benr'] = benr_id = kw.get('benr', cc('benr', 'bearb'))
        benr = Code(benr_id)
        mit_id = Mitarbeiter().getNewId()
        form['mitid'] = mit_id
        form['vn'] = kw.get('vn', ("%s%sVn" % (benr['code'], mit_id)).capitalize())
        form['na'] = kw.get('na', ("%s%sNa" % (benr['code'], mit_id)).capitalize())
        form['ben'] = kw.get('ben', "%s%s" % (benr['code'], mit_id))
        form['anr'] = kw.get('anr', choice(('Frau', 'Herr')))
        form['tl1'] = "54367 %s" % mit_id
        form['fax'] = "54368 %s" % mit_id
        form['stat'] = cc('status', 'i')
        stelle = kw.get('stelle', choice(self.stellen))
        form['stz'] = stelle['id']
        form.update(kw)
        form['mail'] = '%s@efb.in-%s.de' % (form['ben'], self.ort.lower())
        form['pass'] = sha.new(form['ben']).hexdigest() # ben == passwort
        miteinf(form)
        log("Mitarbeiter ben=%s benr=%s stelle=%s" %
             (form['ben'], benr['code'], stelle['code']))


    def choose_mitarbeiter(self, stelle_id):
        return choice([m for m in self.mitarbeiter if m['stz'] == stelle_id])

    def choose_code(self, kat_code):
        """Niemals 'keine Angabe' liefern"""
        codes = get_codes(kat_code)
        while True:
            code = choice(codes)
            if code['code'] != '999':
                return code
    def choose_code_id(self, kat_code):
        return self.choose_code(kat_code)['id']
    def choose_code_id_several(self, kat_code, min, max, unique=False):
        codes = get_codes(kat_code)
        how_many = randrange(min, max+1)
        selection = sample(codes, how_many)
        if not unique:
            selection_2 = sample(codes, how_many)
            n = how_many / 2
            # auf diese Weise können welche doppelt auftauchen
            selection = selection[:n] + selection_2[n:]
        return [c['id'] for c in selection]
    
    def choose_date(self, min=None, max=None):
        if not max:
            max = today()
        if not min:
            min = Date(today().year - 2)
        #log("CHOOSE_DATE min/max: %s/%s" % (min,max))
        assert max >= min
        assert min != Date(0,0,0)
        assert max != Date(0,0,0)
        while True:
            year = randrange(min.year, max.year + 1)
            month = randrange(1, 13)
            day = randrange(1, 29)
            date = Date(year, month, day)
            if date >= min and date <= max:
                return date

    def fake_adresse(self, obj):
        if config.STRASSENKATALOG:
            obj['strkat_on'] = 1
            st = choice(self.strkat)
            obj['strid'] = str(st['id'])
            obj['str'] = st['name']
            obj['ort'] = st['ort']
            von, bis = st['von'], st['bis']
            if von and bis:
                vnummer =  split_hausnummer(von)[0]
                bnummer =  split_hausnummer(bis)[0]
                if vnummer == bnummer:
                    obj['hsnr'] = von
                else:
                    assert vnummer < bnummer
                    nr = randrange(vnummer, bnummer+1, 2)
                    if nr == vnummer:
                        nr = von
                    elif nr == bnummer:
                        nr = bis
                    obj['hsnr'] = str(nr)
            else:
                assert von == bis == None
                obj['hsnr'] = str(randrange(1, 200))
            obj['plz'] = st['plz']
            #print 'STRASSENKATALOG:', config.STRASSENKATALOG
        else:
            obj['str'] = choice(self.strassen)
            obj['hsnr'] = str(randrange(1, 200))
            obj['plz'] = "%05d" % randrange(16000, 99999)
            obj['plraum'] = "%08d" % randrange(60, 61+int(self.n_akten**.35))
            obj['ort'] = choice(self.orte)
        #print 'FAKE_ADRESSE', obj['hsnr'], type(obj['hsnr'])
        log('FAKE ADRESSE: ort: %(ort)s str: %(str)s hsnr: %(hsnr)s plz: %(plz)s' % obj)


    def p_ja_nein(self, zahl, z1=1, p1=.1, z2=36, p2=.9):
        """Liefert mit einer bestimmten Wahrscheilichkeit True oder False.
        Die Wahrscheinlichkeit hängt ab von zahl und den Parametern.
        Für z1 <= zahl <= z2 steigt die Wahrscheilichkeit linear von p1 auf p2,
        für kleinere bzw. größere Werte ist sie p1 bzw. p2:
                            
                p2         ___       
                          / 
                         /
                p1  ____/ 
                       z1 z2     

        """
        if zahl <= z1:
            p = p1
        elif zahl >= z2:
            p = p2
        else:
            p = (p2-float(p1))*(zahl-float(z1))/(z2-float(z1)) + p1
        if random() <= p: # wenn p klein ist, ist die Zufallszahl meist größer
            return True
        return False

    def fake_zda(self, datum=None):
        """schliesst einen Fall mit einer bestimmten
        Wahrscheinlichkeit ab, je älter desto
        wahscheinlicher.
        Fügt vor dem Schliessen noch ein paar Leistungen ein.
        Erledigt vor dem Schliessen auch die Statistiken,
        sonst wird die Schliessung nicht akzeptiert.
        """
        fall = Akte(self.akte_id)['letzter_fall']
        fn = fall['fn']
        beginn = fall.getDate('bg')
        alter = beginn.diff(today()) 
        if alter < 2:
            return
        form = {}
        form['fallid'] = fall['id']
        form['aktuellzustid'] = fall['zustaendig__id']
        # Dauer des Falles
        if datum:
            zda = datum
        else:
            zda = self.choose_date(beginn.add_month(1), min(beginn.add_month(24), today()))
##             if random() < .2:
##                 zda = self.choose_date(beginn.add_month(12), min(beginn.add_month(24), today()))
##             else:
##                 # die meisten Fälle bis ein Jahr
##                 zda = self.choose_date(beginn.add_month(1), min(beginn.add_month(12), today()))
##             zda = self.choose_date(beginn.add_month(1), min(beginn.add_month(alter), today()))
        # eine Statistik pro abgeschlossenem Fall
        self.fake_fachstatistik(fall, zda)
        self.fake_jghstatistik(fall, zda, abgeschlossen=True)
        setDate(form, 'zda', zda)
        # 0 bis 5 Leistungen hinzufügen
        for i in range(randrange(6)):
            self.fake_leistung(fall, zda)
        zdaeinf(form)
        log("Zda %s am %s" % (fn, zda))


    def fake_waufn(self, datum=None):
        akte = Akte(self.akte_id)
        stelle_id = akte['stzbg']
        letzter_fall = akte['letzter_fall']
        zdadatum = letzter_fall.getDate('zda')
        if zdadatum == Date(0,0,0):
##             log(zdadatum)
            return
        if zdadatum.add_month(int(config.WIEDERAUFNAHMEFRIST)) > today():
##             log(zdadatum)
##             log(zdadatum.add_month(1))
##             log(zdadatum == Date(0,0,0))
##             log(zdadatum.add_month(1) > today())
##             log("WAUF Return")
            return
        form = {}
        form['akid'] = self.akte_id
        form['fallid'] = Fall().getNewId()
        if not datum:
            datum = self.choose_date(min=zdadatum.add_month(1))
        setDate(form, 'zubg', datum)
        mitarbeiter = self.choose_mitarbeiter(stelle_id)
        form['zumitid'] = mitarbeiter['id']
        form['lemitid'] = mitarbeiter['id']
        form['le'] = self.choose_code_id('fsle')
        setDate(form, 'lebg', getDate(form, 'zubg')) # erste Leistung zu Fallbeginn
        form['lestz'] = stelle_id
        # form benötigt die Adressdaten, sonst wird in ebupd.waufneinf die Adresse gelöscht
        form['gs'] = akte['gs']
        setDate(form, 'gb', str2date(akte['gb']))
        for k in ('ort', 'str', 'plz', 'hsnr'):
            v = akte.get(k)
            if v:
                form[k] = v
        if config.STRASSENKATALOG:
            form['strkat_on'] = 1
        waufneinf(form)
        log("Wiederaufnahme als %s am %s" % (Akte(self.akte_id)['letzter_fall']['fn'],
                                             getDate(form, 'zubg')))

    def fake_leistung(self, fall, beginn_vor):
        form = {}
        form['leistid'] = Leistung().getNewId()
        form['fallid'] = fall['id']
        setDate(form, 'bg',
                self.choose_date(fall.getDate('bg'), beginn_vor))
        form['mitid'] = fall['zustaendig__mit_id']
        if not form.get('mitid'):
            log("KEIN zustaendiger Mitarbeiter für Leistung gefunden!")
        form['stz'] = fall['zustaendig__mit__stz']
        form['le'] = self.choose_code_id('fsle')
        leisteinf(form)
        log("Leistung %s für %s" % (Code(form['le'])['name'], fall['fn']))
        
    def fake_akte(self):
        """erzeugt Daten für eine Akte"""
        akte_id = self.akte_id = Akte().getNewId()
        stelle_id = self.choose_code_id('stzei')
        form = {}
        form['akid'] = akte_id
        form['vn'] = "Klient%sVn" % akte_id
        form['na'] = "Klient%sNa" % akte_id
##         form['gb'] = "%s.%s.%s" % (randrange(1, 29), randrange(1, 13),
##                                    randrange(self.von_jahr.add_month(-240), self.bis_jahr.add_month(-24)))
        setDate(form, 'gb', self.choose_date(self.von_jahr.add_month(-240),
                                             self.bis_jahr.add_month(-24)))
        form['gs'] = self.choose_code_id('gs')
        form['aufbew'] = self.choose_code_id('aufbew')
        form['ber'] = "Ausbildung von Nr.: %s" % akte_id
        self.fake_adresse(form)                                                      
        form['tl1'] = str(randrange(20000, 99999999))
        form['tl2'] = ''
        form['fs'] = self.choose_code_id('fsfs')
        form['no'] = 'Das sind alles Beispieldaten für Form %s' % self.akte_id
        form['stzbg'] = stelle_id
        # Fall
        setDate(form, 'zubg', self.choose_date(min=self.von_jahr))
##         form['zumitid'] = choice(self.mitarbeiter)['id']
##         form['lemitid'] = choice(self.mitarbeiter)['id']
        form['zumitid'] = self.choose_mitarbeiter(stelle_id)['id']
        form['lemitid'] = self.choose_mitarbeiter(stelle_id)['id']
        form['le'] = self.choose_code_id('fsle')
        setDate(form, 'lebg', getDate(form, 'zubg')) # erste Leistung zu Fallbeginn
        form['lestz'] = stelle_id
        akteeinf(form)
        fall = Akte(self.akte_id)['letzter_fall']
        log("Akte %s" % akte_id)
        log("Fall %s" % fall['fn'])
        for i in range(randrange(1,4)): # 1 - 3
            self.fake_bezugsperson()
        for i in range(randrange(3)):   # 0 - 2
            self.fake_einrichtung()
        self.repeat_zda_waufn()

    def repeat_zda_waufn(self):
        """Hier soll alles rein, was die Wahrscheinlichkeit eines ZDA
        und WAUFN betrifft."""
        for i in range(5):
            af = Akte(self.akte_id)['aktueller_fall']
            if af:
                bg = af.getDate('bg')
                zda = self.choose_date(bg.add_month(1), bg.add_month(30))
                if zda < today():
                    self.fake_zda(zda)
            lf = Akte(self.akte_id)['letzter_fall']
            zda = lf.getDate('zda')
            if not zda.is_zero() and random() < .4:
                waufn = self.choose_date(zda.add_month(1), zda.add_month(30))
                if waufn < today():
                    self.fake_waufn(waufn)
        
    def fake_bezugsperson(self):
        form = {}
        bp_id = Bezugsperson().getNewId()
        form['bpid'] = bp_id
        form['akid'] = self.akte_id
        form['vn'] = "Bezugsperson%sVn" % bp_id
        form['na'] = "Bezugsperson%sNa" % bp_id
        setDate(form, 'gb', self.choose_date(Date(1910),
                                             self.bis_jahr.add_month(-240)))
        form['gs'] = self.choose_code_id('gs')
        form['ber'] = "Bezugsperson Beruf: %s" % bp_id
        form['no'] = "Notiz für Bezugsperson: %s" % bp_id
        form['tl1'] = str(randrange(20000, 99999999))
        form['tl2'] = ''
        self.fake_adresse(form)
        form['verw'] = self.choose_code_id('klerv')
        form['fs'] = self.choose_code_id('fsfs')
        form['nobed'] = self.choose_code_id('notizbed')
        form['vrt'] = self.choose_code_id('vert')
        perseinf(form)
        log("Bezugsperson %s" % bp_id)

    def fake_einrichtung(self):
        form = {}
        einr_id = Einrichtungskontakt().getNewId()
        form['einrid'] = einr_id
        form['akid'] = self.akte_id
        form['na'] = "Einrichtungsname%s" % einr_id
        form['no'] = "Notiz für Bezugsperson: %s" % einr_id
        form['tl1'] = str(randrange(20000, 99999999))
        form['tl2'] = ''
        form['insta'] = self.choose_code_id('klinsta')
        form['nobed'] = self.choose_code_id('notizbed')
        form['status'] = self.choose_code_id('einrstat')
        einreinf(form)
        log("Einrichtung %s" % einr_id)


    def fake_fachstatistik(self, fall, ende_datum):
        akte = Akte(self.akte_id)
        form = {}
        fs_id = Fachstatistik().getNewId()
        form['fsid'] = fs_id
        form['fallid'] = fall['id']
        form['fall_fn'] = fall['fn']
        form['mitid'] = fall['zustaendig__mit_id']
        form['jahr'] = ende_datum.year
        form['stz'] = akte['stzbg']
        form['plr'] = akte['plraum']
        form['gs'] = akte['gs']
        form['ag'] = self.choose_code_id('fsag')
        form['fs'] = self.choose_code_id('fsfs')
        form['zm'] = self.choose_code_id('fszm')
        form['qualij'] = self.choose_code_id('fsqualij')
        form['hkm'] = self.choose_code_id('fshe')
        form['hkv'] = self.choose_code_id('fshe')
        form['bkm'] = self.choose_code_id('fsbe')
        form['bkv'] = self.choose_code_id('fsbe')
        form['qualikm'] = self.choose_code_id('fsquali')
        form['qualikv'] = self.choose_code_id('fsquali')
        form['agkm'] = self.choose_code_id('fsagel')
        form['agkv'] = self.choose_code_id('fsagel')
        form['ba1'] = self.choose_code_id('fsba')
        form['ba2'] = self.choose_code_id('fsba')
        form['pbe'] = self.choose_code_id('fspbe')
        form['pbk'] = self.choose_code_id('fspbk')
        form['anmprobleme'] = self.choose_code_id_several('fsba', 1, 4, unique=True)
        form['elternprobleme'] = self.choose_code_id_several('fspbe', 1, 4, unique=True)
        form['kindprobleme'] = self.choose_code_id_several('fspbk', 1, 4, unique=True)
        form['eleistungen'] =  self.choose_code_id_several('fsle', 1, 10)
##         form['pbeltern'] = self.choose_code_id_several('fspbe', 1, 4, unique=True)
##         form['pbkind'] = self.choose_code_id_several('fspbk', 1, 4, unique=True)
##         form['le'] =  self.choose_code_id_several('fsle', 1, 10)
        sum = 0
        for f in ('kkm', 'kkv', 'kki', 'kpa', 'kfa',
                  'ksoz', 'kleh', 'kerz', 'kkonf','kson'):
            anzahl = randrange(0, 10)
            form[f] = anzahl
            sum += anzahl
        form['kat'] = sum
        joker_felder = ('joka1', 'joka2', 'joka3', 'joka4',
                        'jokf5', 'jokf6', 'jokf7', 'jokf8',)
        for f in joker_felder:
            form[f] = self.choose_code_id('fs' + f)
        fseinf(form)
        log("Fachstatistik für %s (akte_id=%s)" % (fall['fn'], self.akte_id))
            
    def fake_jghstatistik(self, fall, ende_datum, abgeschlossen=None):
        log("fake_jghstatistik %s (akte_id=%s)" % (fall['fn'], self.akte_id))
        if ende_datum.year >= 2007:
            self.fake_jgh07statistik(fall, ende_datum, abgeschlossen)
            return
        akte = Akte(self.akte_id)
        form = {}
        jgh_id = Jugendhilfestatistik().getNewId()
        form['jghid'] = jgh_id
        form['fallid'] = fall['id']
        form['fall_fn'] = fall['fn']
        form['mitid'] = fall['zustaendig__mit_id']
        form['stz'] = akte['stzbg']
        form['gfall'] = self.choose_code_id('gfall')
        setDate(form, 'bg', fall.getDate('bg'))
        setDate(form, 'e', ende_datum)
        #setDate(form, 'e', today()) # 
        form['rbz'] = self.choose_code_id('rbz')
        form['kr'] = Code(kat_code='kr', sort=1)['id'] # zuständige Stelle!
        form['gm'] = self.choose_code_id('gm')
        form['gmt'] = self.choose_code_id('gmt')
        form['traeg'] = self.choose_code_id('traeg')
        form['bgr'] = self.choose_code_id('bgr')
        form['gs'] = akte['gs']
        form['ag'] = self.choose_code_id('ag')
        form['fs'] = self.choose_code_id('fs')
        form['hke'] = self.choose_code_id('hke')
        form['gsu'] = self.choose_code_id('gsu')
        form['gsa'] = ''
        if form['gsu'] == cc('gsu', '0'):
            # Geschwisterzahl bekannt
            form['gsa'] = randrange(0, 8)
        form['zm'] = self.choose_code_id('zm')
        form['schw'] = self.choose_code_id('schw')
        fbe = ('fbe0', 'fbe1', 'fbe2', 'fbe3')
        angekreuzt = [choice(fbe) for i in range(randrange(1, 3))]
        for f in fbe:
            form[f] = ''
            if f in angekreuzt:
                form[f] = self.choose_code_id(f)

        ba = ('ba0', 'ba1', 'ba2', 'ba3', 'ba4', 'ba5', 'ba6', 'ba7', 'ba8', 'ba9')
        angekreuzt = [choice(ba) for i in range(randrange(1, 3))] # eins auf jeden Fall
        form['ba'] = [cc(f, '1') for f in angekreuzt]
        jgheinf(form)
        log("Jugendhilfestatistik für %s (akte_id=%s)" % (fall['fn'], self.akte_id))

    def fake_jgh07statistik(self, fall, ende_datum, abgeschlossen):
        log("fake_jgh07statistik %s (akte_id=%s)" % (fall['fn'], self.akte_id))
        assert ende_datum.year >= 2007
        akte = Akte(self.akte_id)
        form = {}
        jgh_id = Jugendhilfestatistik2007().getNewId()
        form['jghid'] = jgh_id
        form['fallid'] = fall['id']
        form['fall_fn'] = fall['fn']
        form['jahr'] = ende_datum.year
        form['mitid'] = fall['zustaendig__mit_id']
        form['stz'] = akte['stzbg']
        form['gfall'] = self.choose_code_id('gfall')
        form['land'] = Code(kat_code='land', sort=1)['id']
        form['kr'] = Code(kat_code='kr', sort=1)['id'] # zuständige Stelle!
        form['einrnr'] = Code(kat_code='einrnr', sort=1)['id'] # zuständige Stelle!
        setDate(form, 'bg', fall.getDate('bg'))
        if random() < .3:
            form['zustw'] = '1'
        form['hilf_art'] = self.choose_code_id('hilf_art')
        form['hilf_ort'] = self.choose_code_id('hilf_ort')
        form['traeger'] = self.choose_code_id('traeger')
        form['gs'] = self.choose_code_id('gs')
        setDate(form, 'ge', self.choose_date(Date(1990), today().add_month(-20)))
        form['aort_vor'] = self.choose_code_id('auf_ort')
        form['sit_fam'] = self.choose_code_id('shf')
        form['ausl_her'] = self.choose_code_id('ja_ne_un')
        form['vor_dt'] = self.choose_code_id('ja_ne_un')
        form['wirt_sit'] = self.choose_code_id('ja_ne_un')
        form['aip'] = self.choose_code_id('aip')
        form['ees'] = self.choose_code_id('ja_nein')
        form['va52'] = self.choose_code_id('ja_nein')
        form['rgu'] = self.choose_code_id('ja_nein')
        #form['hda'] = cc('ja_nein', '1')
        if abgeschlossen == True:
            form['hda'] = cc('ja_nein', '2')
        elif abgeschlossen == False:
            form['hda'] = cc('ja_nein', '1')
        else:
            form['hda'] = self.choose_code_id('ja_nein')
        gruende = self.choose_code_id_several('gruende', 1, 3, unique=True)
        form['gr1'] = gruende[0]
        if len(gruende) > 1:
            form['gr2'] = gruende[1]
            if len(gruende) > 2:
                form['gr3'] = gruende[2]
        if form['hda'] == cc('ja_nein', '1'):
            form['nbkakt'] = randrange(1, 30)
        else:
            form['lbk6m'] = self.choose_code_id('ja_nein')
            form['grende'] = self.choose_code_id('grende')
            form['aort_nac'] = self.choose_code_id('auf_ort')
            form['unh'] = self.choose_code_id('unh')
            form['nbkges'] = randrange(1, 50)
            setDate(form, 'e', ende_datum)
        #print 'Fake jgh07: ', form
        jgh07einf(form)
        log("Jugendhilfestatistik 2007 für %s (akte_id=%s)" % (fall['fn'], self.akte_id))

    def fake_altdaten(self, csv_file, fields):
        id=Altdaten().getNewId()
        jahr=str(self.choose_date(Date(1999), Date(2006)).year)
        altd = Altdaten()
        altd.init(
            id=id,
            vorname=choice(self.vornamen),
            name=choice(self.namen),
            geburtsdatum=str(self.choose_date(Date(1989,3,1), today().add_month(-24))),
            geschlecht=choice(('m', 'w')),
            jahr=jahr,
            fallnummer=("%s%03d" % (jahr, choice(range(1,1000)))),
            mitarbeiter="Mitarb%s" % id,
            strasse=choice(self.strassen),
            hausnummer=str(randrange(1, 200)),
            plz=str(randrange(10000, 99999)),
            ort=choice(self.orte),
            telefon1=str(randrange(10001, 99999999)),
            telefon2=str(randrange(10001, 99999999)),
            memo=("Memo für Altdaten id=%s. "
            "äöüÄÖÜß Hier kann man noch eine Menge über den alten Fall reinschreiben. "
            "Auch längere Texte. " % id)[:randrange(25,150)]
            )
        csv = ';'.join([('"%%(%s)s"' % a) % altd for a in fields])
        csv_file.write(csv + '\r\n')
        altd.insert()
        log("Altdaten %s" % id)
        return altd

def handle_stellen_einrichtung(n_stellen):
    stellen_codes = ('BS', 'GF', 'WF', 'WOB')
    kreise = ('Braunschweig', 'Gifhorn', 'Wolfenbüttel', 'Wolfsburg')
    einrnr_codes = (
        ('100100', 'BSEinrichtungsnummmer'),
        ('200200', 'GFEinrichtungsnummer'),
        ('300300', 'WFEinrichtungsnummer'),
        ('400400', 'WOBEinrichtungsnummer'),
        )
    CodeList(where="kat_code='einrnr'").deleteall()
    kat_code = 'einrnr'
    for i, (c, n) in enumerate(einrnr_codes):
        code = Code()
        code.init(
            kat_id=Kategorie(code=kat_code)['id'],
            kat_code=kat_code,
            code=c,
            name=n,
            sort=i+1,
            off=0,
            dok='Stelle %s; # Bei dieser Stelle steht dieses Merkmal oben' % stellen_codes[i]
            )
        code.new()
        code.insert()
            
    for i, (st, kr) in enumerate(zip(stellen_codes, kreise)):
        kr_code = Code(name=kr)
        kr_code.update({'dok': "Stelle %s; # kommt bei St. %s nach oben" % (st, st) })
    land_code = Code(name='Niedersachsen')
    land_code.update({'dok': "%s # kommt bei diesen Stellen nach oben" %
                      ' '.join([("Stelle %s;" % s) for s in stellen_codes]) })
    # umbenennen des vordefinierten Stellenzeichens
    Code(kat_code='stzei', code='A').update({'name': 'Stelle BS', 'code': 'BS'})
    for i in range(1, n_stellen):
        DemoDaten().fake_stelle(i, code=stellen_codes[i])

def handle_stellen_einrichtung_muster(n_stellen):
    stellen_codes = ('A', 'B', 'C', 'D')
    kreise = ('Braunschweig', 'Gifhorn', 'Wolfenbüttel', 'Wolfsburg')
    einrnr_codes = (
        ('100100', 'A_Einrichtungsnummmer'),
        ('200200', 'B_Einrichtungsnummer'),
        ('300300', 'C_Einrichtungsnummer'),
        ('400400', 'D_Einrichtungsnummer'),
        )
    CodeList(where="kat_code='einrnr'").deleteall()
    kat_code = 'einrnr'
    for i, (c, n) in enumerate(einrnr_codes):
        code = Code()
        code.init(
            kat_id=Kategorie(code=kat_code)['id'],
            kat_code=kat_code,
            code=c,
            name=n,
            sort=i+1,
            off=0,
            dok='Stelle %s; # Bei dieser Stelle steht dieses Merkmal oben' % stellen_codes[i]
            )
        code.new()
        code.insert()
            
    for i, (st, kr) in enumerate(zip(stellen_codes, kreise)):
        kr_code = Code(name=kr)
        kr_code.update({'dok': "Stelle %s; # kommt bei St. %s nach oben" % (st, st) })
    land_code = Code(name='Niedersachsen')
    land_code.update({'dok': "%s # kommt bei diesen Stellen nach oben" %
                      ' '.join([("Stelle %s;" % s) for s in stellen_codes]) })
    # umbenennen des vordefinierten Stellenzeichens
    Code(kat_code='stzei', code='A').update({'name': 'Stelle A',})
    for i in range(1, n_stellen):
        DemoDaten().fake_stelle(i, code=stellen_codes[i])
