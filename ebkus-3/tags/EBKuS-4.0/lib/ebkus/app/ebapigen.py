# coding: latin-1
"""
AUTOMATISCH GENERIERTE DATEI! NICHT EDITIEREN!

Automatisch generierte Anwendungsschnittstelle für die EB Klientenverwaltung.

Generiert von genEb.py

"""

from ebkus.db.dbapp import DBObjekt, Container, DBAppError
from ebkus.db.sql import SQLError, SQL, SimpleSQL, \
                opendb, closedb, getDBHandle

#####################################
# Mitarbeiter  (Tabelle 'mitarbeiter')
#####################################


class Mitarbeiter(DBObjekt):
    table = 'mitarbeiter'
    fields =  ['id', 'vn', 'na', 'ben', 'anr', 'tl1', 'fax', 'mail', \
                       'stat', 'benr', 'stz', 'zeit', 'pass']
    fieldtypes = {}
    foreignfieldtypes = {}
    inversefieldtypes = {}
    multikatfieldtypes = {}
    attributemethods = {}
    conditionalfields = {}
    pathdefinitions = {}
    attributehandler = None
    primarykey = 'id'
    otherkeys = []
    querySQL  = SimpleSQL(table = table, fields = fields)
    updateSQL = querySQL

class MitarbeiterList(Container):
    resultClass = Mitarbeiter
    querySQL = resultClass.querySQL

#####################################
# Protokoll  (Tabelle 'protokoll')
#####################################


class Protokoll(DBObjekt):
    table = 'protokoll'
    fields =  ['nr', 'zeit', 'artdeszugriffs', 'benutzerkennung', \
                       'ipadresse']
    fieldtypes = {}
    foreignfieldtypes = {}
    inversefieldtypes = {}
    multikatfieldtypes = {}
    attributemethods = {}
    conditionalfields = {}
    pathdefinitions = {}
    attributehandler = None
    primarykey = 'nr'
    otherkeys = []
    querySQL  = SimpleSQL(table = table, fields = fields)
    updateSQL = querySQL

class ProtokollList(Container):
    resultClass = Protokoll
    querySQL = resultClass.querySQL

#####################################
# StrassenkatalogNeu  (Tabelle 'strkatalog')
#####################################


class StrassenkatalogNeu(DBObjekt):
    table = 'strkatalog'
    fields =  ['id', 'von', 'bis', 'gu', 'name', 'plz', 'ort', \
                       'ortsteil', 'samtgemeinde', 'bezirk', 'plraum']
    fieldtypes = {}
    foreignfieldtypes = {}
    inversefieldtypes = {}
    multikatfieldtypes = {}
    attributemethods = {}
    conditionalfields = {}
    pathdefinitions = {}
    attributehandler = None
    primarykey = 'id'
    otherkeys = []
    querySQL  = SimpleSQL(table = table, fields = fields)
    updateSQL = querySQL

class StrassenkatalogNeuList(Container):
    resultClass = StrassenkatalogNeu
    querySQL = resultClass.querySQL

#####################################
# Akte  (Tabelle 'akte')
#####################################


class Akte(DBObjekt):
    table = 'akte'
    fields =  ['id', 'vn', 'na', 'gb', 'gs', 'ber', 'aufbew', 'str', \
                       'hsnr', 'plz', 'plraum', 'lage', 'ort', 'tl1', 'tl2', \
                       'fs', 'no', 'stzbg', 'stzak', 'zeit']
    fieldtypes = {}
    foreignfieldtypes = {}
    inversefieldtypes = {}
    multikatfieldtypes = {}
    attributemethods = {}
    conditionalfields = {}
    pathdefinitions = {}
    attributehandler = None
    primarykey = 'id'
    otherkeys = []
    querySQL  = SimpleSQL(table = table, fields = fields)
    updateSQL = querySQL

class AkteList(Container):
    resultClass = Akte
    querySQL = resultClass.querySQL

#####################################
# Fall  (Tabelle 'fall')
#####################################


class Fall(DBObjekt):
    table = 'fall'
    fields =  ['id', 'akte_id', 'fn', 'bgd', 'bgm', 'bgy', 'zdad', \
                       'zdam', 'zday', 'status']
    fieldtypes = {}
    foreignfieldtypes = {}
    inversefieldtypes = {}
    multikatfieldtypes = {}
    attributemethods = {}
    conditionalfields = {}
    pathdefinitions = {}
    attributehandler = None
    primarykey = 'id'
    otherkeys = []
    querySQL  = SimpleSQL(table = table, fields = fields)
    updateSQL = querySQL

class FallList(Container):
    resultClass = Fall
    querySQL = resultClass.querySQL

#####################################
# Anmeldung  (Tabelle 'anmeldung')
#####################################


class Anmeldung(DBObjekt):
    table = 'anmeldung'
    fields =  ['id', 'fall_id', 'von', 'mtl', 'me', 'zm', 'mg', 'no']
    fieldtypes = {}
    foreignfieldtypes = {}
    inversefieldtypes = {}
    multikatfieldtypes = {}
    attributemethods = {}
    conditionalfields = {}
    pathdefinitions = {}
    attributehandler = None
    primarykey = 'id'
    otherkeys = []
    querySQL  = SimpleSQL(table = table, fields = fields)
    updateSQL = querySQL

class AnmeldungList(Container):
    resultClass = Anmeldung
    querySQL = resultClass.querySQL

#####################################
# Bezugsperson  (Tabelle 'bezugsperson')
#####################################


class Bezugsperson(DBObjekt):
    table = 'bezugsperson'
    fields =  ['id', 'akte_id', 'vn', 'na', 'gb', 'gs', 'ber', 'str', \
                       'hsnr', 'lage', 'plz', 'ort', 'tl1', 'tl2', 'fs', \
                       'verw', 'no', 'nobed', 'vrt']
    fieldtypes = {}
    foreignfieldtypes = {}
    inversefieldtypes = {}
    multikatfieldtypes = {}
    attributemethods = {}
    conditionalfields = {}
    pathdefinitions = {}
    attributehandler = None
    primarykey = 'id'
    otherkeys = []
    querySQL  = SimpleSQL(table = table, fields = fields)
    updateSQL = querySQL

class BezugspersonList(Container):
    resultClass = Bezugsperson
    querySQL = resultClass.querySQL

#####################################
# Einrichtungskontakt  (Tabelle 'einrichtung')
#####################################


class Einrichtungskontakt(DBObjekt):
    table = 'einrichtung'
    fields =  ['id', 'akte_id', 'na', 'tl1', 'tl2', 'insta', 'no', \
                       'nobed', 'status']
    fieldtypes = {}
    foreignfieldtypes = {}
    inversefieldtypes = {}
    multikatfieldtypes = {}
    attributemethods = {}
    conditionalfields = {}
    pathdefinitions = {}
    attributehandler = None
    primarykey = 'id'
    otherkeys = []
    querySQL  = SimpleSQL(table = table, fields = fields)
    updateSQL = querySQL

class EinrichtungskontaktList(Container):
    resultClass = Einrichtungskontakt
    querySQL = resultClass.querySQL

#####################################
# Leistung  (Tabelle 'leistung')
#####################################


class Leistung(DBObjekt):
    table = 'leistung'
    fields =  ['id', 'fall_id', 'mit_id', 'le', 'bgd', 'bgm', 'bgy', \
                       'ed', 'em', 'ey', 'stz']
    fieldtypes = {}
    foreignfieldtypes = {}
    inversefieldtypes = {}
    multikatfieldtypes = {}
    attributemethods = {}
    conditionalfields = {}
    pathdefinitions = {}
    attributehandler = None
    primarykey = 'id'
    otherkeys = []
    querySQL  = SimpleSQL(table = table, fields = fields)
    updateSQL = querySQL

class LeistungList(Container):
    resultClass = Leistung
    querySQL = resultClass.querySQL

#####################################
# Beratungskontakt  (Tabelle 'beratungskontakt')
#####################################


class Beratungskontakt(DBObjekt):
    table = 'beratungskontakt'
    fields =  ['id', 'gruppe_id', 'le_id', 'art', 'art_bs', \
                       'teilnehmer', 'teilnehmer_bs', 'anzahl', 'kd', 'km', \
                       'ky', 'kh', 'kmin', 'jgh', 'dauer', 'dauer_f2f', \
                       'dauer_vornach', 'faktor', 'offenespr', 'no', 'stz']
    fieldtypes = {}
    foreignfieldtypes = {}
    inversefieldtypes = {}
    multikatfieldtypes = {}
    attributemethods = {}
    conditionalfields = {}
    pathdefinitions = {}
    attributehandler = None
    primarykey = 'id'
    otherkeys = []
    querySQL  = SimpleSQL(table = table, fields = fields)
    updateSQL = querySQL

class BeratungskontaktList(Container):
    resultClass = Beratungskontakt
    querySQL = resultClass.querySQL

#####################################
# Mitarbeiterberatungskontakt  (Tabelle 'mitarbeiterberatungskontakt')
#####################################


class Mitarbeiterberatungskontakt(DBObjekt):
    table = 'mitarbeiterberatungskontakt'
    fields =  ['id', 'mit_id', 'bkont_id', 'zeit']
    fieldtypes = {}
    foreignfieldtypes = {}
    inversefieldtypes = {}
    multikatfieldtypes = {}
    attributemethods = {}
    conditionalfields = {}
    pathdefinitions = {}
    attributehandler = None
    primarykey = 'id'
    otherkeys = []
    querySQL  = SimpleSQL(table = table, fields = fields)
    updateSQL = querySQL

class MitarbeiterberatungskontaktList(Container):
    resultClass = Mitarbeiterberatungskontakt
    querySQL = resultClass.querySQL

#####################################
# Fallberatungskontakt  (Tabelle 'fallberatungskontakt')
#####################################


class Fallberatungskontakt(DBObjekt):
    table = 'fallberatungskontakt'
    fields =  ['id', 'fall_id', 'bezugsp_id', 'bkont_id', 'zeit']
    fieldtypes = {}
    foreignfieldtypes = {}
    inversefieldtypes = {}
    multikatfieldtypes = {}
    attributemethods = {}
    conditionalfields = {}
    pathdefinitions = {}
    attributehandler = None
    primarykey = 'id'
    otherkeys = []
    querySQL  = SimpleSQL(table = table, fields = fields)
    updateSQL = querySQL

class FallberatungskontaktList(Container):
    resultClass = Fallberatungskontakt
    querySQL = resultClass.querySQL

#####################################
# Fua_BS  (Tabelle 'fua_bs')
#####################################


class Fua_BS(DBObjekt):
    table = 'fua_bs'
    fields =  ['id', 'mit_id', 'art', 'kd', 'km', 'ky', 'dauer', 'no', \
                       'stz']
    fieldtypes = {}
    foreignfieldtypes = {}
    inversefieldtypes = {}
    multikatfieldtypes = {}
    attributemethods = {}
    conditionalfields = {}
    pathdefinitions = {}
    attributehandler = None
    primarykey = 'id'
    otherkeys = []
    querySQL  = SimpleSQL(table = table, fields = fields)
    updateSQL = querySQL

class Fua_BSList(Container):
    resultClass = Fua_BS
    querySQL = resultClass.querySQL

#####################################
# Zustaendigkeit  (Tabelle 'zustaendigkeit')
#####################################


class Zustaendigkeit(DBObjekt):
    table = 'zustaendigkeit'
    fields =  ['id', 'fall_id', 'mit_id', 'bgd', 'bgm', 'bgy', 'ed', \
                       'em', 'ey']
    fieldtypes = {}
    foreignfieldtypes = {}
    inversefieldtypes = {}
    multikatfieldtypes = {}
    attributemethods = {}
    conditionalfields = {}
    pathdefinitions = {}
    attributehandler = None
    primarykey = 'id'
    otherkeys = []
    querySQL  = SimpleSQL(table = table, fields = fields)
    updateSQL = querySQL

class ZustaendigkeitList(Container):
    resultClass = Zustaendigkeit
    querySQL = resultClass.querySQL

#####################################
# Dokument  (Tabelle 'dokument')
#####################################


class Dokument(DBObjekt):
    table = 'dokument'
    fields =  ['id', 'fall_id', 'mit_id', 'betr', 'fname', 'art', \
                       'vd', 'vm', 'vy', 'mtyp', 'dok', 'zeit']
    fieldtypes = {}
    foreignfieldtypes = {}
    inversefieldtypes = {}
    multikatfieldtypes = {}
    attributemethods = {}
    conditionalfields = {}
    pathdefinitions = {}
    attributehandler = None
    primarykey = 'id'
    otherkeys = []
    querySQL  = SimpleSQL(table = table, fields = fields)
    updateSQL = querySQL

class DokumentList(Container):
    resultClass = Dokument
    querySQL = resultClass.querySQL

#####################################
# Gruppendokument  (Tabelle 'gruppendokument')
#####################################


class Gruppendokument(DBObjekt):
    table = 'gruppendokument'
    fields =  ['id', 'gruppe_id', 'mit_id', 'betr', 'fname', 'art', \
                       'vd', 'vm', 'vy', 'mtyp', 'dok', 'zeit']
    fieldtypes = {}
    foreignfieldtypes = {}
    inversefieldtypes = {}
    multikatfieldtypes = {}
    attributemethods = {}
    conditionalfields = {}
    pathdefinitions = {}
    attributehandler = None
    primarykey = 'id'
    otherkeys = []
    querySQL  = SimpleSQL(table = table, fields = fields)
    updateSQL = querySQL

class GruppendokumentList(Container):
    resultClass = Gruppendokument
    querySQL = resultClass.querySQL

#####################################
# Gruppe  (Tabelle 'gruppe')
#####################################


class Gruppe(DBObjekt):
    table = 'gruppe'
    fields =  ['id', 'gn', 'name', 'thema', 'tzahl', 'stzahl', 'bgd', \
                       'bgm', 'bgy', 'ed', 'em', 'ey', 'teiln', 'grtyp', 'stz', \
                       'zeit']
    fieldtypes = {}
    foreignfieldtypes = {}
    inversefieldtypes = {}
    multikatfieldtypes = {}
    attributemethods = {}
    conditionalfields = {}
    pathdefinitions = {}
    attributehandler = None
    primarykey = 'id'
    otherkeys = []
    querySQL  = SimpleSQL(table = table, fields = fields)
    updateSQL = querySQL

class GruppeList(Container):
    resultClass = Gruppe
    querySQL = resultClass.querySQL

#####################################
# FallGruppe  (Tabelle 'fallgruppe')
#####################################


class FallGruppe(DBObjekt):
    table = 'fallgruppe'
    fields =  ['id', 'fall_id', 'gruppe_id', 'bgd', 'bgm', 'bgy', \
                       'ed', 'em', 'ey', 'zeit']
    fieldtypes = {}
    foreignfieldtypes = {}
    inversefieldtypes = {}
    multikatfieldtypes = {}
    attributemethods = {}
    conditionalfields = {}
    pathdefinitions = {}
    attributehandler = None
    primarykey = 'id'
    otherkeys = [('',), ('fall_id', 'gruppe_id'), ('gruppe_id', 'fall_id')]
    querySQL  = SimpleSQL(table = table, fields = fields)
    updateSQL = querySQL

class FallGruppeList(Container):
    resultClass = FallGruppe
    querySQL = resultClass.querySQL

#####################################
# BezugspersonGruppe  (Tabelle 'bezugspersongruppe')
#####################################


class BezugspersonGruppe(DBObjekt):
    table = 'bezugspersongruppe'
    fields =  ['id', 'bezugsp_id', 'gruppe_id', 'bgd', 'bgm', 'bgy', \
                       'ed', 'em', 'ey', 'zeit']
    fieldtypes = {}
    foreignfieldtypes = {}
    inversefieldtypes = {}
    multikatfieldtypes = {}
    attributemethods = {}
    conditionalfields = {}
    pathdefinitions = {}
    attributehandler = None
    primarykey = 'id'
    otherkeys = [('',), ('bezugsp_id', 'gruppe_id'), ('gruppe_id', 'bezugsp_id')]
    querySQL  = SimpleSQL(table = table, fields = fields)
    updateSQL = querySQL

class BezugspersonGruppeList(Container):
    resultClass = BezugspersonGruppe
    querySQL = resultClass.querySQL

#####################################
# MitarbeiterGruppe  (Tabelle 'mitarbeitergruppe')
#####################################


class MitarbeiterGruppe(DBObjekt):
    table = 'mitarbeitergruppe'
    fields =  ['id', 'mit_id', 'gruppe_id', 'bgd', 'bgm', 'bgy', 'ed', \
                       'em', 'ey', 'zeit']
    fieldtypes = {}
    foreignfieldtypes = {}
    inversefieldtypes = {}
    multikatfieldtypes = {}
    attributemethods = {}
    conditionalfields = {}
    pathdefinitions = {}
    attributehandler = None
    primarykey = 'id'
    otherkeys = [('mit_id', 'gruppe_id'), ('gruppe_id', 'mit_id')]
    querySQL  = SimpleSQL(table = table, fields = fields)
    updateSQL = querySQL

class MitarbeiterGruppeList(Container):
    resultClass = MitarbeiterGruppe
    querySQL = resultClass.querySQL

#####################################
# Fachstatistik  (Tabelle 'fachstat')
#####################################


class Fachstatistik(DBObjekt):
    table = 'fachstat'
    fields =  ['id', 'mit_id', 'fall_id', 'fall_fn', 'jahr', 'stz', \
                       'plz', 'ort', 'ortsteil', 'samtgemeinde', 'bezirk', \
                       'plraum', 'gs', 'ag', 'fs', 'zm', 'qualij', 'hkm', \
                       'hkv', 'bkm', 'bkv', 'qualikm', 'qualikv', 'agkm', \
                       'agkv', 'ba1', 'ba2', 'pbe', 'pbk', 'kat', 'kkm', 'kkv', \
                       'kki', 'kpa', 'kfa', 'ksoz', 'kleh', 'kerz', 'kkonf', \
                       'kson', 'no', 'no2', 'no3', 'anmprobleme', \
                       'kindprobleme', 'elternprobleme', 'eleistungen', \
                       'joka1', 'joka2', 'joka3', 'joka4', 'jokf5', 'jokf6', \
                       'jokf7', 'jokf8', 'zeit']
    fieldtypes = {}
    foreignfieldtypes = {}
    inversefieldtypes = {}
    multikatfieldtypes = {}
    attributemethods = {}
    conditionalfields = {}
    pathdefinitions = {}
    attributehandler = None
    primarykey = 'id'
    otherkeys = []
    querySQL  = SimpleSQL(table = table, fields = fields)
    updateSQL = querySQL

class FachstatistikList(Container):
    resultClass = Fachstatistik
    querySQL = resultClass.querySQL

#####################################
# Jugendhilfestatistik  (Tabelle 'jghstat')
#####################################


class Jugendhilfestatistik(DBObjekt):
    table = 'jghstat'
    fields =  ['id', 'fall_id', 'mit_id', 'fall_fn', 'gfall', 'stz', \
                       'rbz', 'kr', 'gm', 'gmt', 'lnr', 'traeg', 'bgm', 'bgy', \
                       'em', 'ey', 'bgr', 'gs', 'ag', 'fs', 'hke', 'gsa', \
                       'gsu', 'zm', 'ba0', 'ba1', 'ba2', 'ba3', 'ba4', 'ba5', \
                       'ba6', 'ba7', 'ba8', 'ba9', 'schw', 'fbe0', 'fbe1', \
                       'fbe2', 'fbe3', 'zeit']
    fieldtypes = {}
    foreignfieldtypes = {}
    inversefieldtypes = {}
    multikatfieldtypes = {}
    attributemethods = {}
    conditionalfields = {}
    pathdefinitions = {}
    attributehandler = None
    primarykey = 'id'
    otherkeys = []
    querySQL  = SimpleSQL(table = table, fields = fields)
    updateSQL = querySQL

class JugendhilfestatistikList(Container):
    resultClass = Jugendhilfestatistik
    querySQL = resultClass.querySQL

#####################################
# Jugendhilfestatistik2007  (Tabelle 'jghstat07')
#####################################


class Jugendhilfestatistik2007(DBObjekt):
    table = 'jghstat07'
    fields =  ['id', 'fall_id', 'fall_fn', 'mit_id', 'stz', 'gfall', \
                       'land', 'kr', 'einrnr', 'lnr', 'bgm', 'bgy', 'zustw', \
                       'hilf_art', 'hilf_ort', 'traeger', 'gs', 'gem', 'gey', \
                       'aort_vor', 'sit_fam', 'ausl_her', 'vor_dt', 'wirt_sit', \
                       'aip', 'ees', 'va52', 'rgu', 'hda', 'nbkakt', 'gr1', \
                       'gr2', 'gr3', 'em', 'ey', 'nbkges', 'lbk6m', 'grende', \
                       'aort_nac', 'unh', 'zeit']
    fieldtypes = {}
    foreignfieldtypes = {}
    inversefieldtypes = {}
    multikatfieldtypes = {}
    attributemethods = {}
    conditionalfields = {}
    pathdefinitions = {}
    attributehandler = None
    primarykey = 'id'
    otherkeys = []
    querySQL  = SimpleSQL(table = table, fields = fields)
    updateSQL = querySQL

class Jugendhilfestatistik2007List(Container):
    resultClass = Jugendhilfestatistik2007
    querySQL = resultClass.querySQL

#####################################
# Code  (Tabelle 'code')
#####################################


class Code(DBObjekt):
    table = 'code'
    fields =  ['id', 'kat_id', 'kat_code', 'code', 'name', 'sort', \
                       'mini', 'maxi', 'off', 'dm', 'dy', 'dok', 'flag', \
                       'zeit']
    fieldtypes = {}
    foreignfieldtypes = {}
    inversefieldtypes = {}
    multikatfieldtypes = {}
    attributemethods = {}
    conditionalfields = {}
    pathdefinitions = {}
    attributehandler = None
    primarykey = 'id'
    otherkeys = [('code', 'kat_id'), ('code', 'kat_code'), ('name', 'kat_id'), ('name', 'kat_code')]
    querySQL  = SimpleSQL(table = table, fields = fields)
    updateSQL = querySQL

class CodeList(Container):
    resultClass = Code
    querySQL = resultClass.querySQL

#####################################
# Kategorie  (Tabelle 'kategorie')
#####################################


class Kategorie(DBObjekt):
    table = 'kategorie'
    fields =  ['id', 'code', 'name', 'kat_id', 'dok', 'flag', 'zeit']
    fieldtypes = {}
    foreignfieldtypes = {}
    inversefieldtypes = {}
    multikatfieldtypes = {}
    attributemethods = {}
    conditionalfields = {}
    pathdefinitions = {}
    attributehandler = None
    primarykey = 'id'
    otherkeys = [('code',), ('name',)]
    querySQL  = SimpleSQL(table = table, fields = fields)
    updateSQL = querySQL

class KategorieList(Container):
    resultClass = Kategorie
    querySQL = resultClass.querySQL

#####################################
# Feld  (Tabelle 'feld')
#####################################


class Feld(DBObjekt):
    table = 'feld'
    fields =  ['id', 'tab_id', 'feld', 'name', 'inverse', 'typ', \
                       'laenge', 'notnull', 'verwtyp', 'ftab_id', 'kat_id', \
                       'kat_code', 'flag', 'dok']
    fieldtypes = {}
    foreignfieldtypes = {}
    inversefieldtypes = {}
    multikatfieldtypes = {}
    attributemethods = {}
    conditionalfields = {}
    pathdefinitions = {}
    attributehandler = None
    primarykey = 'id'
    otherkeys = [('tab_id', 'feld')]
    querySQL  = SimpleSQL(table = table, fields = fields)
    updateSQL = querySQL

class FeldList(Container):
    resultClass = Feld
    querySQL = resultClass.querySQL

#####################################
# Tabelle  (Tabelle 'tabelle')
#####################################


class Tabelle(DBObjekt):
    table = 'tabelle'
    fields =  ['id', 'tabelle', 'name', 'klasse', 'flag', 'dok', \
                       'maxist']
    fieldtypes = {}
    foreignfieldtypes = {}
    inversefieldtypes = {}
    multikatfieldtypes = {}
    attributemethods = {}
    conditionalfields = {}
    pathdefinitions = {}
    attributehandler = None
    primarykey = 'id'
    otherkeys = [('tabelle',), ('name',), ('klasse',)]
    querySQL  = SimpleSQL(table = table, fields = fields)
    updateSQL = querySQL

class TabelleList(Container):
    resultClass = Tabelle
    querySQL = resultClass.querySQL

#####################################
# Register  (Tabelle 'register')
#####################################


class Register(DBObjekt):
    table = 'register'
    fields =  ['id', 'regkey', 'value']
    fieldtypes = {}
    foreignfieldtypes = {}
    inversefieldtypes = {}
    multikatfieldtypes = {}
    attributemethods = {}
    conditionalfields = {}
    pathdefinitions = {}
    attributehandler = None
    primarykey = 'id'
    otherkeys = [('regkey',)]
    querySQL  = SimpleSQL(table = table, fields = fields)
    updateSQL = querySQL

class RegisterList(Container):
    resultClass = Register
    querySQL = resultClass.querySQL

#####################################
# Abfrage  (Tabelle 'abfrage')
#####################################


class Abfrage(DBObjekt):
    table = 'abfrage'
    fields =  ['id', 'mit_id', 'name', 'dok', 'value', 'typ', 'zeit']
    fieldtypes = {}
    foreignfieldtypes = {}
    inversefieldtypes = {}
    multikatfieldtypes = {}
    attributemethods = {}
    conditionalfields = {}
    pathdefinitions = {}
    attributehandler = None
    primarykey = 'id'
    otherkeys = [('name',)]
    querySQL  = SimpleSQL(table = table, fields = fields)
    updateSQL = querySQL

class AbfrageList(Container):
    resultClass = Abfrage
    querySQL = resultClass.querySQL

#####################################
# Altdaten  (Tabelle 'altdaten')
#####################################


class Altdaten(DBObjekt):
    table = 'altdaten'
    fields =  ['id', 'vorname', 'name', 'geburtsdatum', 'geschlecht', \
                       'jahr', 'fallnummer', 'mitarbeiter', 'strasse', \
                       'hausnummer', 'plz', 'ort', 'telefon1', 'telefon2', \
                       'memo']
    fieldtypes = {}
    foreignfieldtypes = {}
    inversefieldtypes = {}
    multikatfieldtypes = {}
    attributemethods = {}
    conditionalfields = {}
    pathdefinitions = {}
    attributehandler = None
    primarykey = 'id'
    otherkeys = []
    querySQL  = SimpleSQL(table = table, fields = fields)
    updateSQL = querySQL

class AltdatenList(Container):
    resultClass = Altdaten
    querySQL = resultClass.querySQL

    
# Die folgenden Einträge ermöglichen die automatische Navigation über
# Fremdschlüssel. Wird insbesondere von DBObjekt.__getitem__ verwendet.
#   fall['akte_id__vn'] kann damit automatisch evaluiert werden.
    
Mitarbeiter.foreignfieldtypes['stat'] = (Code, None)
Mitarbeiter.foreignfieldtypes['benr'] = (Code, None)
Mitarbeiter.foreignfieldtypes['stz'] = (Code, None)
Akte.foreignfieldtypes['gs'] = (Code, None)
Akte.foreignfieldtypes['aufbew'] = (Code, None)
Akte.foreignfieldtypes['fs'] = (Code, None)
Akte.foreignfieldtypes['stzbg'] = (Code, None)
Akte.foreignfieldtypes['stzak'] = (Code, None)
Fall.foreignfieldtypes['akte_id'] = (Akte, 'faelle')
Fall.foreignfieldtypes['status'] = (Code, None)
Anmeldung.foreignfieldtypes['fall_id'] = (Fall, 'anmeldung')
Anmeldung.foreignfieldtypes['zm'] = (Code, None)
Bezugsperson.foreignfieldtypes['akte_id'] = (Akte, 'bezugspersonen')
Bezugsperson.foreignfieldtypes['gs'] = (Code, None)
Bezugsperson.foreignfieldtypes['fs'] = (Code, None)
Bezugsperson.foreignfieldtypes['verw'] = (Code, None)
Bezugsperson.foreignfieldtypes['nobed'] = (Code, None)
Bezugsperson.foreignfieldtypes['vrt'] = (Code, None)
Einrichtungskontakt.foreignfieldtypes['akte_id'] = (Akte, 'einrichtungen')
Einrichtungskontakt.foreignfieldtypes['insta'] = (Code, None)
Einrichtungskontakt.foreignfieldtypes['nobed'] = (Code, None)
Einrichtungskontakt.foreignfieldtypes['status'] = (Code, None)
Leistung.foreignfieldtypes['fall_id'] = (Fall, 'leistungen')
Leistung.foreignfieldtypes['mit_id'] = (Mitarbeiter, 'leistungen')
Leistung.foreignfieldtypes['le'] = (Code, None)
Leistung.foreignfieldtypes['stz'] = (Code, None)
Beratungskontakt.foreignfieldtypes['gruppe_id'] = (Gruppe, 'termine')
Beratungskontakt.foreignfieldtypes['le_id'] = (Leistung, 'beratungskontakte')
Beratungskontakt.foreignfieldtypes['art'] = (Code, None)
Beratungskontakt.foreignfieldtypes['art_bs'] = (Code, None)
Beratungskontakt.foreignfieldtypes['jgh'] = (Code, None)
Beratungskontakt.foreignfieldtypes['dauer'] = (Code, None)
Beratungskontakt.foreignfieldtypes['offenespr'] = (Code, None)
Beratungskontakt.foreignfieldtypes['stz'] = (Code, None)
Mitarbeiterberatungskontakt.foreignfieldtypes['mit_id'] = (Mitarbeiter, 'mitarbeiterberatungskontakte')
Mitarbeiterberatungskontakt.foreignfieldtypes['bkont_id'] = (Beratungskontakt, 'mitarbeiterberatungskontakte')
Fallberatungskontakt.foreignfieldtypes['fall_id'] = (Fall, 'fallberatungskontakte')
Fallberatungskontakt.foreignfieldtypes['bezugsp_id'] = (Bezugsperson, 'fallberatungskontakte')
Fallberatungskontakt.foreignfieldtypes['bkont_id'] = (Beratungskontakt, 'fallberatungskontakte')
Fua_BS.foreignfieldtypes['mit_id'] = (Mitarbeiter, 'beratungskontakte_bs')
Fua_BS.foreignfieldtypes['art'] = (Code, None)
Fua_BS.foreignfieldtypes['stz'] = (Code, None)
Zustaendigkeit.foreignfieldtypes['fall_id'] = (Fall, 'zustaendigkeiten')
Zustaendigkeit.foreignfieldtypes['mit_id'] = (Mitarbeiter, 'zustaendigkeiten')
Dokument.foreignfieldtypes['fall_id'] = (Fall, 'dokumente')
Dokument.foreignfieldtypes['mit_id'] = (Mitarbeiter, 'dokumente')
Dokument.foreignfieldtypes['art'] = (Code, None)
Dokument.foreignfieldtypes['mtyp'] = (Code, None)
Gruppendokument.foreignfieldtypes['gruppe_id'] = (Gruppe, 'gruppendokumente')
Gruppendokument.foreignfieldtypes['mit_id'] = (Mitarbeiter, 'gruppendokumente')
Gruppendokument.foreignfieldtypes['art'] = (Code, None)
Gruppendokument.foreignfieldtypes['mtyp'] = (Code, None)
Gruppe.foreignfieldtypes['teiln'] = (Code, None)
Gruppe.foreignfieldtypes['grtyp'] = (Code, None)
Gruppe.foreignfieldtypes['stz'] = (Code, None)
FallGruppe.foreignfieldtypes['fall_id'] = (Fall, 'gruppen')
FallGruppe.foreignfieldtypes['gruppe_id'] = (Gruppe, 'faelle')
BezugspersonGruppe.foreignfieldtypes['bezugsp_id'] = (Bezugsperson, 'gruppen')
BezugspersonGruppe.foreignfieldtypes['gruppe_id'] = (Gruppe, 'bezugspersonen')
MitarbeiterGruppe.foreignfieldtypes['mit_id'] = (Mitarbeiter, 'gruppen')
MitarbeiterGruppe.foreignfieldtypes['gruppe_id'] = (Gruppe, 'mitarbeiter')
Fachstatistik.foreignfieldtypes['mit_id'] = (Mitarbeiter, 'fachstatistiken')
Fachstatistik.foreignfieldtypes['fall_id'] = (Fall, 'fachstatistiken')
Fachstatistik.foreignfieldtypes['stz'] = (Code, None)
Fachstatistik.foreignfieldtypes['gs'] = (Code, None)
Fachstatistik.foreignfieldtypes['ag'] = (Code, None)
Fachstatistik.foreignfieldtypes['fs'] = (Code, None)
Fachstatistik.foreignfieldtypes['zm'] = (Code, None)
Fachstatistik.foreignfieldtypes['qualij'] = (Code, None)
Fachstatistik.foreignfieldtypes['hkm'] = (Code, None)
Fachstatistik.foreignfieldtypes['hkv'] = (Code, None)
Fachstatistik.foreignfieldtypes['bkm'] = (Code, None)
Fachstatistik.foreignfieldtypes['bkv'] = (Code, None)
Fachstatistik.foreignfieldtypes['qualikm'] = (Code, None)
Fachstatistik.foreignfieldtypes['qualikv'] = (Code, None)
Fachstatistik.foreignfieldtypes['agkm'] = (Code, None)
Fachstatistik.foreignfieldtypes['agkv'] = (Code, None)
Fachstatistik.foreignfieldtypes['ba1'] = (Code, None)
Fachstatistik.foreignfieldtypes['ba2'] = (Code, None)
Fachstatistik.foreignfieldtypes['pbe'] = (Code, None)
Fachstatistik.foreignfieldtypes['pbk'] = (Code, None)
Fachstatistik.foreignfieldtypes['joka1'] = (Code, None)
Fachstatistik.foreignfieldtypes['joka2'] = (Code, None)
Fachstatistik.foreignfieldtypes['joka3'] = (Code, None)
Fachstatistik.foreignfieldtypes['joka4'] = (Code, None)
Fachstatistik.foreignfieldtypes['jokf5'] = (Code, None)
Fachstatistik.foreignfieldtypes['jokf6'] = (Code, None)
Fachstatistik.foreignfieldtypes['jokf7'] = (Code, None)
Fachstatistik.foreignfieldtypes['jokf8'] = (Code, None)
Jugendhilfestatistik.foreignfieldtypes['fall_id'] = (Fall, 'jgh_statistiken')
Jugendhilfestatistik.foreignfieldtypes['mit_id'] = (Mitarbeiter, 'jgh_statistiken')
Jugendhilfestatistik.foreignfieldtypes['gfall'] = (Code, None)
Jugendhilfestatistik.foreignfieldtypes['stz'] = (Code, None)
Jugendhilfestatistik.foreignfieldtypes['rbz'] = (Code, None)
Jugendhilfestatistik.foreignfieldtypes['kr'] = (Code, None)
Jugendhilfestatistik.foreignfieldtypes['gm'] = (Code, None)
Jugendhilfestatistik.foreignfieldtypes['gmt'] = (Code, None)
Jugendhilfestatistik.foreignfieldtypes['traeg'] = (Code, None)
Jugendhilfestatistik.foreignfieldtypes['bgr'] = (Code, None)
Jugendhilfestatistik.foreignfieldtypes['gs'] = (Code, None)
Jugendhilfestatistik.foreignfieldtypes['ag'] = (Code, None)
Jugendhilfestatistik.foreignfieldtypes['fs'] = (Code, None)
Jugendhilfestatistik.foreignfieldtypes['hke'] = (Code, None)
Jugendhilfestatistik.foreignfieldtypes['gsu'] = (Code, None)
Jugendhilfestatistik.foreignfieldtypes['zm'] = (Code, None)
Jugendhilfestatistik.foreignfieldtypes['ba0'] = (Code, None)
Jugendhilfestatistik.foreignfieldtypes['ba1'] = (Code, None)
Jugendhilfestatistik.foreignfieldtypes['ba2'] = (Code, None)
Jugendhilfestatistik.foreignfieldtypes['ba3'] = (Code, None)
Jugendhilfestatistik.foreignfieldtypes['ba4'] = (Code, None)
Jugendhilfestatistik.foreignfieldtypes['ba5'] = (Code, None)
Jugendhilfestatistik.foreignfieldtypes['ba6'] = (Code, None)
Jugendhilfestatistik.foreignfieldtypes['ba7'] = (Code, None)
Jugendhilfestatistik.foreignfieldtypes['ba8'] = (Code, None)
Jugendhilfestatistik.foreignfieldtypes['ba9'] = (Code, None)
Jugendhilfestatistik.foreignfieldtypes['schw'] = (Code, None)
Jugendhilfestatistik.foreignfieldtypes['fbe0'] = (Code, None)
Jugendhilfestatistik.foreignfieldtypes['fbe1'] = (Code, None)
Jugendhilfestatistik.foreignfieldtypes['fbe2'] = (Code, None)
Jugendhilfestatistik.foreignfieldtypes['fbe3'] = (Code, None)
Jugendhilfestatistik2007.foreignfieldtypes['fall_id'] = (Fall, 'jgh07_statistiken')
Jugendhilfestatistik2007.foreignfieldtypes['mit_id'] = (Mitarbeiter, 'jgh07_statistiken')
Jugendhilfestatistik2007.foreignfieldtypes['stz'] = (Code, None)
Jugendhilfestatistik2007.foreignfieldtypes['gfall'] = (Code, None)
Jugendhilfestatistik2007.foreignfieldtypes['land'] = (Code, None)
Jugendhilfestatistik2007.foreignfieldtypes['kr'] = (Code, None)
Jugendhilfestatistik2007.foreignfieldtypes['einrnr'] = (Code, None)
Jugendhilfestatistik2007.foreignfieldtypes['hilf_art'] = (Code, None)
Jugendhilfestatistik2007.foreignfieldtypes['hilf_ort'] = (Code, None)
Jugendhilfestatistik2007.foreignfieldtypes['traeger'] = (Code, None)
Jugendhilfestatistik2007.foreignfieldtypes['gs'] = (Code, None)
Jugendhilfestatistik2007.foreignfieldtypes['aort_vor'] = (Code, None)
Jugendhilfestatistik2007.foreignfieldtypes['sit_fam'] = (Code, None)
Jugendhilfestatistik2007.foreignfieldtypes['ausl_her'] = (Code, None)
Jugendhilfestatistik2007.foreignfieldtypes['vor_dt'] = (Code, None)
Jugendhilfestatistik2007.foreignfieldtypes['wirt_sit'] = (Code, None)
Jugendhilfestatistik2007.foreignfieldtypes['aip'] = (Code, None)
Jugendhilfestatistik2007.foreignfieldtypes['ees'] = (Code, None)
Jugendhilfestatistik2007.foreignfieldtypes['va52'] = (Code, None)
Jugendhilfestatistik2007.foreignfieldtypes['rgu'] = (Code, None)
Jugendhilfestatistik2007.foreignfieldtypes['hda'] = (Code, None)
Jugendhilfestatistik2007.foreignfieldtypes['gr1'] = (Code, None)
Jugendhilfestatistik2007.foreignfieldtypes['gr2'] = (Code, None)
Jugendhilfestatistik2007.foreignfieldtypes['gr3'] = (Code, None)
Jugendhilfestatistik2007.foreignfieldtypes['lbk6m'] = (Code, None)
Jugendhilfestatistik2007.foreignfieldtypes['grende'] = (Code, None)
Jugendhilfestatistik2007.foreignfieldtypes['aort_nac'] = (Code, None)
Jugendhilfestatistik2007.foreignfieldtypes['unh'] = (Code, None)
Code.foreignfieldtypes['kat_id'] = (Kategorie, 'codes')
Kategorie.foreignfieldtypes['kat_id'] = (Kategorie, 'kategorien')
Feld.foreignfieldtypes['tab_id'] = (Tabelle, 'felder')
Feld.foreignfieldtypes['verwtyp'] = (Code, None)
Feld.foreignfieldtypes['ftab_id'] = (Tabelle, 'inverse')
Feld.foreignfieldtypes['kat_id'] = (Kategorie, '')
Abfrage.foreignfieldtypes['mit_id'] = (Mitarbeiter, '')

    
# Die folgenden Einträge ermöglichen die automatische Navigation über
# inverse Fremdschlüssel. Wird insbesondere von DBObjekt.__getitem__ 
# verwendet.
#   fall['leistungen'] kann damit automatisch evaluiert werden.
    
Akte.inversefieldtypes['faelle'] = (FallList, 'akte_id')
Fall.inversefieldtypes['anmeldung'] = (AnmeldungList, 'fall_id')
Akte.inversefieldtypes['bezugspersonen'] = (BezugspersonList, 'akte_id')
Akte.inversefieldtypes['einrichtungen'] = (EinrichtungskontaktList, 'akte_id')
Fall.inversefieldtypes['leistungen'] = (LeistungList, 'fall_id')
Mitarbeiter.inversefieldtypes['leistungen'] = (LeistungList, 'mit_id')
Gruppe.inversefieldtypes['termine'] = (BeratungskontaktList, 'gruppe_id')
Leistung.inversefieldtypes['beratungskontakte'] = (BeratungskontaktList, 'le_id')
Mitarbeiter.inversefieldtypes['mitarbeiterberatungskontakte'] = (MitarbeiterberatungskontaktList, 'mit_id')
Beratungskontakt.inversefieldtypes['mitarbeiterberatungskontakte'] = (MitarbeiterberatungskontaktList, 'bkont_id')
Fall.inversefieldtypes['fallberatungskontakte'] = (FallberatungskontaktList, 'fall_id')
Bezugsperson.inversefieldtypes['fallberatungskontakte'] = (FallberatungskontaktList, 'bezugsp_id')
Beratungskontakt.inversefieldtypes['fallberatungskontakte'] = (FallberatungskontaktList, 'bkont_id')
Mitarbeiter.inversefieldtypes['beratungskontakte_bs'] = (Fua_BSList, 'mit_id')
Fall.inversefieldtypes['zustaendigkeiten'] = (ZustaendigkeitList, 'fall_id')
Mitarbeiter.inversefieldtypes['zustaendigkeiten'] = (ZustaendigkeitList, 'mit_id')
Fall.inversefieldtypes['dokumente'] = (DokumentList, 'fall_id')
Mitarbeiter.inversefieldtypes['dokumente'] = (DokumentList, 'mit_id')
Gruppe.inversefieldtypes['gruppendokumente'] = (GruppendokumentList, 'gruppe_id')
Mitarbeiter.inversefieldtypes['gruppendokumente'] = (GruppendokumentList, 'mit_id')
Fall.inversefieldtypes['gruppen'] = (FallGruppeList, 'fall_id')
Gruppe.inversefieldtypes['faelle'] = (FallGruppeList, 'gruppe_id')
Bezugsperson.inversefieldtypes['gruppen'] = (BezugspersonGruppeList, 'bezugsp_id')
Gruppe.inversefieldtypes['bezugspersonen'] = (BezugspersonGruppeList, 'gruppe_id')
Mitarbeiter.inversefieldtypes['gruppen'] = (MitarbeiterGruppeList, 'mit_id')
Gruppe.inversefieldtypes['mitarbeiter'] = (MitarbeiterGruppeList, 'gruppe_id')
Mitarbeiter.inversefieldtypes['fachstatistiken'] = (FachstatistikList, 'mit_id')
Fall.inversefieldtypes['fachstatistiken'] = (FachstatistikList, 'fall_id')
Fall.inversefieldtypes['jgh_statistiken'] = (JugendhilfestatistikList, 'fall_id')
Mitarbeiter.inversefieldtypes['jgh_statistiken'] = (JugendhilfestatistikList, 'mit_id')
Fall.inversefieldtypes['jgh07_statistiken'] = (Jugendhilfestatistik2007List, 'fall_id')
Mitarbeiter.inversefieldtypes['jgh07_statistiken'] = (Jugendhilfestatistik2007List, 'mit_id')
Kategorie.inversefieldtypes['codes'] = (CodeList, 'kat_id')
Kategorie.inversefieldtypes['kategorien'] = (KategorieList, 'kat_id')
Tabelle.inversefieldtypes['felder'] = (FeldList, 'tab_id')
Tabelle.inversefieldtypes['inverse'] = (FeldList, 'ftab_id')
Kategorie.inversefieldtypes[''] = (FeldList, 'kat_id')
Mitarbeiter.inversefieldtypes[''] = (AbfrageList, 'mit_id')

    
# Die folgenden Einträge ermöglichen Mehrfachauswahlfelder.
# In das Feld werden die IDs von Code-Instanzen als Strings
# geschrieben. Beim Aufruf über __getitem__ werden die durch
# Code-Instanzen ersetzt.
    
Beratungskontakt.multikatfieldtypes['teilnehmer'] = CodeList
Beratungskontakt.multikatfieldtypes['teilnehmer_bs'] = CodeList
Fachstatistik.multikatfieldtypes['anmprobleme'] = CodeList
Fachstatistik.multikatfieldtypes['kindprobleme'] = CodeList
Fachstatistik.multikatfieldtypes['elternprobleme'] = CodeList
Fachstatistik.multikatfieldtypes['eleistungen'] = CodeList
