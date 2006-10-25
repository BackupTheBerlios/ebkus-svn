# coding: latin-1

import sys, os, time, sha
from ebkus.app.ebapi import cc, getNewFallnummer, Date, today, getDate, setDate, \
     Kategorie, Code, Mitarbeiter, MitarbeiterList, Akte, Fall, FallList, Leistung, \
     Zustaendigkeit, Bezugsperson, Einrichtungskontakt, CodeList, \
     StrassenkatalogList, Fachstatistik, Jugendhilfestatistik
from ebkus.app.ebapih import  get_codes
from ebkus.app.ebupd import akteeinf, fseinf, jgheinf, miteinf, codeeinf, \
     leisteinf, zdaeinf, waufneinf, perseinf, einreinf
from ebkus.config import config
from random import choice, randrange, sample, random

def log(s):
    print s
    
def create_demo_daten(logf=None,
                      n_akten=35,         # Anzahl von Akten in der demo
                      n_bearbeiter=None,  # Anzahl der Mitarbeiter in der Bearbeiterrolle
                                          # ohne explizite Angabe wachsend mit n_akten
                      n_stellen=None,     # Anzahl der Stellen, default wachsend mit n_akten
                      von_jahr=None,      # Jahr in dem die ersten Akten angelegt werden
                                          # default ist heute vor zwei Jahren
                      bis_jahr=None):     # Jahr in dem die letzten Akten angelegt werden,
                                          # default ist dieses Jahr
    from ebkus.app import protocol
    #protocol.on()
    if logf:
        global log
        log = logf
    if config.BERLINER_VERSION:
        # In der Berliner Version muss der Kreis, für den die Stelle
        # zuständig ist, in der Sortierreihenfolge an erster Stelle
        # stehen. Sonst funktionieren die Planungsräume nicht.
        Code(kat_code='kr', code='01', name='Mitte').update({'sort': 4})
        Code(kat_code='kr', code='04',
             name='Charlottenburg-Wilmersdorf').update({'sort': 1})
        
    # umbenennen des vordefinierten Stellenzeichens
    Code(kat_code='stzei', code='A').update({'name': 'Stelle A', 'code': 'A'})
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
    for i in range(1, n_stellen):
        DemoDaten().fake_stelle(i)
    stellen = DemoDaten.stellen = CodeList(where="kat_code='stzei'")
    if config.BERLINER_VERSION:
        DemoDaten.strkat = StrassenkatalogList(where='')
        DemoDaten.ort = 'Berlin'
    else:
        DemoDaten.ort = Code(kat_code='kr', sort=1)['name']
    # die beiden protokoll-Berechtigten
    DemoDaten().fake_mitarbeiter(benr=cc('benr', 'protokol'), ben='pr1')
    DemoDaten().fake_mitarbeiter(benr=cc('benr', 'protokol'), ben='pr2')
    # Verwaltungskraft
    DemoDaten().fake_mitarbeiter(benr=cc('benr', 'verw'), ben='verw')
    # Bearbeiter
    for i in range(n_bearbeiter):
        DemoDaten().fake_mitarbeiter(benr=cc('benr', 'bearb'), ben='bearb%s' % (i+1))
    # ich
    DemoDaten().fake_mitarbeiter(benr=cc('benr', 'bearb'),
                                 ben='test',
                                 vn='Test', na='Tester',
                                 stz=stellen[0]['id']) # immer Stelle A
    DemoDaten.mitarbeiter = MitarbeiterList(where = 'stat = %s and benr = %s' %
                                            (cc('status', 'i'), cc('benr', 'bearb')))
    for i in range(1, n_akten+1):
        DemoDaten().fake_akte()

class DemoDaten(object):
    strassen = ('Teichweg', 'Müllerstr.', 'Am Rott', 'Karl-Marx-Str.',
                'Hinterm Markt', 'Rosenweg')
    orte = ('Unterhausen', 'Groß-Lehnau', 'Klein-Magrau')

    def fake_stelle(self, i):
        """i=1 --> Stelle B
           i=2 --> Stelle C
           ...
        """
        code_id = Code().getNewId()
        st_code = chr(ord('A') + i)
        form = {}
        form['codeid'] = code_id
        form['katcode'] = Kategorie(code='stzei')['code']
        form['katid'] = Kategorie(code='stzei')['id']
        form['code'] = st_code
        form['name'] = 'Stelle %s' % st_code
        form['sort'] = i + 1
        codeeinf(form)
        log(form['name'])

    def fake_mitarbeiter(self, **kw):
        benr_id = kw.get('benr', cc('benr', 'bearb'))
        benr = Code(benr_id)
        mit_id = Mitarbeiter().getNewId()
        form = {}
        form['mitid'] = mit_id
        form['vn'] = ("%s%sVn" % (benr['code'], mit_id)).capitalize()
        form['na'] = ("%s%sNa" % (benr['code'], mit_id)).capitalize()
        form['ben'] = "%s%s" % (benr['code'], mit_id)
        form['anr'] = choice(('Frau', 'Herr'))
        form['tl1'] = "54367 %s" % mit_id
        form['fax'] = "54368 %s" % mit_id
        form['stat'] = cc('status', 'i')
        form['benr'] = benr_id
        stelle = choice(self.stellen)
        form['stz'] = stelle['id']
        form.update(kw)
        form['mail'] = '%s@efb.in-%s.de' % (form['ben'], self.ort.lower())
        form['pass'] = sha.new(form['ben']).hexdigest() # ben == passwort
        miteinf(form)
        log("Mitarbeiter ben=%s benr=%s stelle=%s" %
             (form['ben'], benr['code'], stelle['code']))

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
    
    def choose_date(self, min=None, max=today()):
        if not min:
            min = Date(today().year - 2)
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
        if config.BERLINER_VERSION:
            st = choice(self.strkat)
            obj['strkat'] = st['str_name']
            obj['hsnr'] = st['hausnr']
            obj['plz'] = str(st['plz'])
            ## diese kommen aus dem Strassenkatalog
            ## obj['planungsr'] =  st['Plraum']
            ## obj['wohnbez'] = cc('wohnbez', "%02d" % st['bezirk'])
            ## obj['lage'] = cc('lage', '0') # innerhalb der Geltung des Straßenkatalogs
            obj['ort'] = 'Berlin'
            return
        obj['str'] = choice(self.strassen)
        obj['hsnr'] = str(randrange(1, 300))
        obj['plz'] = "%05d" % randrange(16000, 99999)
        obj['planungsr'] = "%04d" % randrange(60, 61+int(self.n_akten**.35))
        ## wird automatisch von setAdresse zugewiesen
        ## obj['wohnbez'] = cc('wohnbez', "13") # sollte egal sein
        ## obj['lage'] = cc('lage', '1') # außerhalb der Geltung des Straßenkatalogs
        obj['ort'] = choice(self.orte)


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

    def fake_zda(self):
        """schliesst einen Fall mit einer bestimmten
        Wahrscheinlichkeit ab, je älter desto
        wahscheinlicher.
        Fügt vor dem Schliessen noch ein paar Leistungen ein."""
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
        zda = self.choose_date(beginn.add_month(1), min(beginn.add_month(alter), today()))
        setDate(form, 'zda', zda)
        # 0 bis 5 Leistungen hinzufügen
        for i in range(randrange(6)):
            self.fake_leistung(fall, zda)
        zdaeinf(form)
        log("Zda %s am %s" % (fn, zda))


    def fake_waufn(self):
        letzter_fall = Akte(self.akte_id)['letzter_fall']
        zdadatum = letzter_fall.getDate('zda')
        if zdadatum == Date(0,0,0):
##             log(zdadatum)
            return
        if zdadatum.add_month(1) > today():
##             log(zdadatum)
##             log(zdadatum.add_month(1))
##             log(zdadatum == Date(0,0,0))
##             log(zdadatum.add_month(1) > today())
##             log("WAUF Return")
            return
        form = {}
        form['akid'] = self.akte_id
        form['fallid'] = Fall().getNewId()
        setDate(form, 'zubg', self.choose_date(min=zdadatum.add_month(1)))
        mitarbeiter = choice(self.mitarbeiter)
        form['zumitid'] = mitarbeiter['id']
        form['stzbg'] = mitarbeiter['stz'] # TODO ist das richtig? akte.stzbg wird dadrauf gesetzt
        form['lemitid'] = mitarbeiter['id']
        form['le'] = self.choose_code_id('fsle')
        setDate(form, 'lebg', getDate(form, 'zubg')) # erste Leistung zu Fallbeginn
        form['lestz'] = mitarbeiter['stz']
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
        form = {}
        form['akid'] = akte_id
        form['vn'] = "Klient%sVn" % akte_id
        form['na'] = "Klient%sNa" % akte_id
##         form['gb'] = "%s.%s.%s" % (randrange(1, 29), randrange(1, 13),
##                                    randrange(self.von_jahr.add_month(-240), self.bis_jahr.add_month(-24)))
        form['gb'] = "%s" % self.choose_date(self.von_jahr.add_month(-240), self.bis_jahr.add_month(-24))
        form['ber'] = "Ausbildung von Nr.: %s" % akte_id
        self.fake_adresse(form)                                                      
        form['tl1'] = str(randrange(20000, 99999999))
        form['tl2'] = ''
        form['fs'] = self.choose_code_id('fsfs')
        form['no'] = 'Das sind alles Beispieldaten für Form %s' % self.akte_id
        form['stzbg'] = self.choose_code_id('stzei')
        form['stzak'] = form['stzbg'] # beim Anlegen die gleiche Stelle
        # Fall
        setDate(form, 'zubg', self.choose_date(min=self.von_jahr))
        form['zumitid'] = choice(self.mitarbeiter)['id']
        form['lemitid'] = choice(self.mitarbeiter)['id']
        form['le'] = self.choose_code_id('fsle')
        setDate(form, 'lebg', getDate(form, 'zubg')) # erste Leistung zu Fallbeginn
        form['lestz'] = Mitarbeiter(form['lemitid'])['stz']
        akteeinf(form)
        fall = Akte(self.akte_id)['letzter_fall']
        log("Akte %s" % akte_id)
        log("Fall %s" % fall['fn'])
        for i in range(randrange(1,4)): # 1 - 3
            self.fake_bezugsperson()
        for i in range(randrange(3)):   # 0 - 2
            self.fake_einrichtung()
        #print "WOHNBEZIRK: ", self.akte['wohnbez']
        self.fake_fachstatistik(fall)
        self.fake_jghstatistik(fall)
        # den Fall mit einer gewissen Wahrscheinlichkeit schließen;
        # je älter, desto wahrscheinlicher
        alter = fall.getDate('bg').diff(today()) 
        if self.p_ja_nein(alter, z1=1, p1=.1, z2=36, p2=.9):
            self.fake_zda()
            # 30% wiederaufnehmen
            if random() < .3:
                self.fake_waufn()
        
    def fake_bezugsperson(self):
        form = {}
        bp_id = Bezugsperson().getNewId()
        form['bpid'] = bp_id
        form['akid'] = self.akte_id
        form['vn'] = "Bezugsperson%sVn" % bp_id
        form['na'] = "Bezugsperson%sNa" % bp_id
        form['gb'] = "%s" % self.choose_date(Date(1910), self.bis_jahr.add_month(-240))
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


    def fake_fachstatistik(self, fall):
        akte = Akte(self.akte_id)
        form = {}
        fs_id = Fachstatistik().getNewId()
        form['fsid'] = fs_id
        form['fallid'] = fall['id']
        form['fall_fn'] = fall['fn']
        form['mitid'] = fall['zustaendig__mit_id']
        form['jahr'] = fall['bgy'] # TODO: OK?
        form['stz'] = akte['stzak']
        form['plr'] = akte['planungsr']
        form['gs'] = self.choose_code_id('gs')
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
        form['pbeltern'] = self.choose_code_id_several('fspbe', 1, 4, unique=True)
        form['pbkind'] = self.choose_code_id_several('fspbk', 1, 4, unique=True)
        form['le'] =  self.choose_code_id_several('fsle', 1, 10)
        sum = 0
        for f in ('kkm', 'kkv', 'kki', 'kpa', 'kfa',
                  'ksoz', 'kleh', 'kerz', 'kkonf','kson'):
            anzahl = randrange(0, 10)
            form[f] = anzahl
            sum += anzahl
        form['kat'] = sum
        fseinf(form)
        log("Fachstatistik für %s (akte_id=%s)" % (fall['fn'], self.akte_id))
            
    def fake_jghstatistik(self, fall):
        akte = Akte(self.akte_id)
        form = {}
        jgh_id = Jugendhilfestatistik().getNewId()
        form['jghid'] = jgh_id
        form['fallid'] = fall['id']
        form['fall_fn'] = fall['fn']
        form['mitid'] = fall['zustaendig__mit_id']
        form['jahr'] = fall['bgy'] # TODO: OK?
        form['stz'] = akte['stzak']
        form['gfall'] = self.choose_code_id('gfall')
        setDate(form, 'bg', fall.getDate('bg'))
        #setDate(form, 'e', fall.getDate('zda')) # TODO: OK?
        setDate(form, 'e', today()) # TODO: OK?
        form['rbz'] = self.choose_code_id('rbz')
        form['kr'] = Code(kat_code='kr', sort=1)['id'] # zuständige Stelle!
        form['gm'] = self.choose_code_id('gm')
        form['gmt'] = self.choose_code_id('gmt')
        form['wohnbez'] = akte['wohnbez']
        #form['bezirksnr'] = Code(kat_code='kr', sort=1)['id'] # zuständige Stelle!
        form['traeg'] = self.choose_code_id('traeg')

        form['bgr'] = self.choose_code_id('bgr')
        form['gs'] = self.choose_code_id('gs')
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
