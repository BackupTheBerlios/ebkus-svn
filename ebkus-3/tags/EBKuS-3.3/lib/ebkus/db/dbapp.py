# coding: latin-1
"""Modul zur Unterstützung von simplen Datenbankanwendungen mit Python.

Dieses Modul ist unabhängig von einer bestimmten Datenbank, da die
gesamte Kommunikation mit der Datenbank über das hier verwendete Modul
'sql' abgewickelt wird.

Folgende Klassen und Funktionen sind zum Export aus diesem Modul
gedacht:

DBObjekt, Container
===================

Es werden zwei abstrakte Klassen zur Verfügung gestellt, DBObjekt und
Container, für die in einer Anwendung konkrete Klassen definiert
werden müssen. Die konkreten Anwendungsklassen müssen im einfachsten
Fall lediglich einige Parameter spezifizieren; es müssen keine eigenen
Methoden definiert werden, falls nur die Standardfunktionalität genutzt
werden soll, die bereits in die abstrakten Klassen eingebaut ist.

Unterklassen von DBObjekt entsprechen Entitäten der Anwendung, wobei
einer Entität im einfachen Fall eine Tabelle in der Datenbank
zugeordnet ist. Instanzen von DBObjekt (bzw. von deren konkreten
Unterklassen) verhalten sich als Python-Dictionary, bestehend aus
Paaren (Feldname, Wert).

Unterklassen von Container stellen Mengen von Instanzen einer Entität
dar. Instanzen von Container verhalten sich als Python-Liste mit
Instanzen von DBObjekt als Listenelemente.

Unter Verwendung der Standardfunktionalität können natürlich auch
spezialisierte Anwendungsklassen aufgebaut werden, z.B. Objekte, die
auf Daten aus mehreren Tabellen beruhen.

Zur Kommunikation mit der Datenbank werden standardmäßig Instanzen der
im Modul 'sql' definierten Klasse SimpleSQL verwendet. Instanzen
dieser Klassen ermögliche SELECT, INSERT, UPDATE und DELETE
Operationen auf einer Datenbanktabelle (siehe Modul 'sql'). Für jede
in einer Anwendung konkrete Unterklasse von DBObjekt und Container muß
je ein SQL-Objekt für Queries und für Insert/Update/Delete definiert
werden.

"""

import string, re
import sql
from ebkus.db import dbcache

class DBAppError(Exception):
    pass
    
_cache = dbcache.DBCache()

# nicht-primitive Felder im Cache ablegen
_cache_fields = 1
#_cache_fields = 0

def cache_off():
    _cache.off()
    
def cache_on():
    _cache.on()
    
def cache_is_on():
    return _cache.is_on()
    
def undo_cached_fields():
    _cache.undo_cached_fields()
    

def cache_clear_if_gt(no_items):
    _cache.clear_if_gt(no_items)
    
    #cache_off()
    
getitemcount = 0

from UserDict import UserDict
class DBObjekt(UserDict):
    """Abstrakte Klasse, mit Funktionalität für die Abbildung von
    Datenbankentitäten auf Python-Objekte.
    
    Für jede Entität der Datenbank (also in der Regel für jede Tabelle) muß
    die Anwendung eine konkrete Unterklasse definieren.
    
    Im einfachsten Fall kann dies z.B. für eine Entität Mitarbeiter so
    aussehen:
    
    class Mitarbeiter(DBObjekt):
    table = 'mitarbeiter'           # die Datenbanktabelle, deren Zeilen eine
                                    # Instanz der Entität repräsentiern
    fields =  ['id', 'vn', 'na', 'stat', 'benr', 'stz']  # Felder
    foreignfieldtypes = {}          # Initialisierung, s.u.
    inversefieldtypes = {}          # Initialisierung, s.u.
    primarykey = 'id'               # Primärschlüssel für die Tabelle
                                    # None, falls keiner vorhanden
    otherkeys = [('vn', 'na')]      # weitere Schlüsselkombinationen, die
                                    # die eindeutige Identifikation eines
                                    # Objekts (= einer Zeile) ermöglichen
    
    querySQL  = SimpleSQL('Mitarbeiter',     # SQL-Objekt für Queries
                          table = table,
                          fields = fields)
    updateSQL = querySQL                     # SQL-Objekt für Insert/Update/Delete
                                             # Ein SimpleSQL-Objekt geht für beides.
    
    
    ## Die folgenden Einträge müssen nach den eigentliche
    ## Klassendefinition stehen, da die Klassen, die sie referieren,
    ## bereits definiert sein müssen.
    
    # Dieser Eintrag besagt, daß die Werte des Feldes 'stat' Schlüssel sind
    # für Instanzen der Klasse Code.
    Mitarbeiter.foreignfieldtypes['stat'] = Code
    
    # Dieser Eintrag besagt, daß 'leistungen' als inverse Relation für das Feld
    # mit_id in der Klasse Leistung definiert ist.
    Mitarbeiter.inversefieldtypes['leistungen'] = (LeistungList, 'mit_id')
    
    Nach dieser Klassendefinition steht folgende Standardfunkionalität (in
    der Klasse DBObjekt implementiert) zur Verfügung:
    
    m = Mitarbeiter()                 Leeres Objekt.
    m.new()                           Erzeugt neues Objekt, verwendet Methode
                                    getNewId() zur Erzeugung des Keys.
    m.new(55)                         Erzeugt neues Objekt mit id = 55.
                                    Wirft Exception, falls Key(s) schon Werte haben.
    
    m = Mitarbeiter(id = 5)           Holt das Objekt mit dem übergebenen Key
    m = Mitarbeiter(5)                bzw. den übergebenen Parametern aus der DB.
    m = Mitarbeiter(vn = 'Tom', na = 'Gast')
                                    Wirft Exception, falls keine eindeutige Instanz
                                    (also genau eine) existiert.
    
    m['na'] = 'Tom'                   Setzen von Feldern.
    m['id'] = 5                       Wirft Exception, falls der Primärschlüssel
                                    verändert werden soll.
    na = m['na']                      Lesen von Feldern.
    
    cn = m['stat__name']              Durch Verkettung mit '__' können Attributwerte
                                    von Objekten gelesen werden, die über Fremd-
                                    schlüssel verknüpft sind. Im Beispiel muß es dazu
                                    einen Eintrag foreignfieldtypes['stat'] = Code
                                    geben, auch über längere Ketten:
    kcn = m['stat__kat_id__name']
    llist = m['leistungen']           Falls für die betreffende Klasse 'leistungen' als
                                    inverse definiert ist durch einen Eintrag
                                    inversefieldtypes['leistungen'] = (LeistungList, 'mit_id')
                                    kann über dieses Attribut die Liste der dem Mitarbeit
                                    zugordnete Leistungen ermittelt werden.
    
    llist = m.getinv('leistungen', where = 'le = 104')
                                    Dasselbe wie oben, aber mit der zusätzlichen
                                    Möglichkeit, durch Bedingungen die Liste einzu-
                                    schränken. Anstatt ein explizites where-Argument
                                    können auch Feld-Wert angegeben werden, also:
    llist = m.getinv('leistungen', 'le', 104)
    
    akte_obj = fall['akte']           Falls das Attribut verlängert um den String '_id'
    akte_id  = fall['akte_id']        den Feldnamen eines Fremdschlüssels ergibt, wird
                                    das Objekt zurückgegeben, statt des Schlüssels.
    
    m.beliebiger_name = 'Wert'        Normale Attribute können auch gesetzt werden,
                                    sind jedoch von Datanbankfeldern unabhängig.
    
    
    # Für die folgenden Operationen wird geprüft, ob sie jeweils eindeutig sind.
    # Falls es einen Primärschlüssel für die Objektklasse gibt, muß dieser einen
    # Wert haben.
    
    m.insert()                        Exception,
                                    - falls ein Objekt mit dem Schlüssel schon existiert,
                                    - falls notNull Feld fehlt (über die Datenbank)
                                    - falls Schlüsselwerte fehlen
    m.update()                        Exception, falls Objekt nicht existiert.
                                    Es werden nur die Felder updatet, für die Werte
                                    im Objekt definiert sind.
    m.delete()                        Exception, falls nicht existent,
                                    Standard delete sorgt nicht für referentielle
                                    Integrität!
                                    Dies könnte aber noch implementiert werden
                                    unter Ausnutzung der inversefieldtypes.
    
    """
    
    def __init__(self, s_NXXlnokey_word = None, **params):
      # s_NXXlnokey_word wird wohl niemand als Parameter für den Aufruf nehmen,
      # d.h. es ist nur belegt, wenn __init__ ohne keywords aufgerufen wurde.
      # Wir nehmen dann an, daß es sich um den Wert für den primarykey handelt.
      # self.changed = 0
        if  not s_NXXlnokey_word is None:
            if _cache.get(self, s_NXXlnokey_word):
            ##      if self._test_data():
            ##        print self._test_data()
            ##        print self.data
            ##        raise AttributeError, 'in __getitem__'
                return
            primarykeyval = s_NXXlnokey_word
            if params:
                raise DBAppError("No additional parameters allowed if primarykey value is given.")
            params[self.primarykey] = primarykeyval
        elif not params:
          # keine Parameter, leeres, unregistriertes Objekt
            self.data = {}
            return
        self.data = params
        if _cache.get(self):
            return
        wherelist = []
        for k,v in params.items():
            wherelist.append("%s = %s" % (k, sql.msql_quote(v)))
        where = string.join(wherelist, ' and ')
        res = self.querySQL.executeQuery(where)
        if len(res) != 1:
            raise DBAppError(
              "No unique object for given parameters: %s (class %s)"
              % (params, self.__class__.__name__))
        self.data = sql.tuple2dict(res[0], self.querySQL.fieldnames)
        self.data['__p__'] = 1
        _cache.cache(self)
        ##     if self._test_data():
        ##       print self._test_data()
        ##       print self.data
        ##       raise AttributeError, 'in __getitem__'
        
        
    def _getKeyValue1(self, ktuple, dict):
        """Versucht, für jedes Element im tuple ktuple einen vWert in dict
        nachzuschlagen. Falls dieses gelingt, die vollständige Liste der Werte
        zurückgeben, sonst None.
        """
        vlist = []
        for k in ktuple:
            val =  dict.get(k)
            if val is None:
                return None
            vlist.append(val)
        return vlist
        
    def _getKeyValues(self, dict):
        for ktuple in self.otherkeys:
            values = self._getKeyValue1(ktuple, dict)
            if values:
                return ktuple, values
        return None
        
    def get_other_key_values(self):
        value_tuple_list = []
        for otherkey in self.otherkeys:
            found = 1
            value_list = []
            for field in otherkey:
                value = self.data.get(field)
                if value: value_list.append(value)
                else:
                    found = 0
                    break
            if found:
                value_tuple_list.append(tuple(value_list))
            else:
                value_tuple_list.append(None)
        return value_tuple_list
        
    def __setitem__(self, key, item):
        persistent = self.data.get('__p__')
        if persistent and key in self.fields:
            raise DBAppError("Attempt to change database field of dbobject")
        self.data[key] = item
        
        
    def _cache_field(self, key, value):
        if _cache_fields:
            self.data[key] = value
            
    def undo_cached_fields(self):
        fields = self.fields
        data = self.data
        inv = self.inversefieldtypes
        for k in data.keys():
            if k in fields:
                continue
            if k[-4:] == '_ids' and inv.has_key(k[:-4]):
                continue
            #print 'undo: %s' % k
            del data[k]
            
            
            
            # Experimental
    def __getitem__(self, key):
        """
        1. key ist in self.data
        2. key ist in self.inversefieldtypes
        3. key ist <key1>__<rest> und key1 ist in self.data und in foreignfieldtypes
        4. <key>_id ist in self.data und foreignfieldtypes
        5. key ist in self.keymethods, die Funktion wird mit <func>(self, key)
           aufgerufen
        6. key wird an die Methode self.keyhandler übergeben, die mit
           self.keyhandler(key) aufgerufen wird
        
        """
        ##     if self._test_data():
        ##       print self._test_data()
        ##       print self.data
        ##       raise AttributeError, 'in __getitem__'
        ##     #  print '__getitem__ %s: %s->%s' % (self.clk(), key, self.data.get(key))
        ##    assert self._test_data
        if self.data.has_key(key):
            return self.data[key]
        if self.inversefieldtypes.has_key(key):
            return self._getinverses(key)
        if self.attributemethods.has_key(key):
            return self.attributemethods[key](self, key)
        if self.pathdefinitions.has_key(key):
            return self[self.pathdefinitions[key]]
        if self.conditionalfields.has_key(key):
            return self.get_conditional(key)
        if key == 'self':
            return self
        try:
            return self._lookup_path(key)
        except DBAppError, e:
            print e.args
            raise AttributeError("Could not resolve field '%s' for instance of '%s'" %
                                 (key, self.__class__.__name__))
            
            
    def get_conditional(self, key):
      #print self.__class__.__name__, key
        alts = self.conditionalfields[key]
        cond =  alts[0]
        if type(cond) == type(''):
            cond = (cond,)
        for i in range(len(cond)):
            if self[cond[i]]:
              #print alts[i+1] , 'SELF:\n' # self.data
                res = alts[i+1] % self
                # self.data[key] = res # data cache
                self._cache_field(key, res)
                return res
        res = alts[i+2] % self
        # self.data[key] = res # data cache
        self._cache_field(key, res)
        return res
        
        
    def _lookup_path(self, key):
        """Should throw an exception only if 'key' is not a correct path.
        If path elements are not found because of NULL values, None is
        returned.
        """
        path = string.split(key, '__')
        # not a real path
        if len(path) == 1:
            foreignkey = key + '_id'
            if self.foreignfieldtypes.has_key(foreignkey):
                klass = self.foreignfieldtypes[foreignkey][0]
                foreignkeyvalue = self.data.get(foreignkey)
                if foreignkeyvalue:
                    res = klass(self[foreignkey])
                else:
                    res = None
                    # self[key] = res # data cache
                self._cache_field(key, res)
                return res
            else:
                raise DBAppError, "lookup error: '%s' is not a valid path" % key
                # len > 1
        val = self
        prevobj = None
        for elem in path:
          # val must be either a DBObjekt or a foreignkey
          # if val is itsself the result of the previous part of the path
          # there must be a prevobj where it was looked up in.
            if isinstance(val, DBObjekt):
                obj = val
            else:  # check whether val is a foreign key looked up in previous iteration
                assert prevobj
                klass = prevobj.__class__
                if klass.foreignfieldtypes.has_key(prevelem):
                    klass = klass.foreignfieldtypes[prevelem][0]
                    obj = klass(val)
                else:
                    raise DBAppError, "path lookup error: '%s' is not a foreign key in %s" % \
                        (prevelem, prevobj.__class__.__name__)
            try:
                val = obj[elem]
            except:
                raise DBAppError, "path lookup error: '%s' is not a valid path for %s" % \
                      (elem, prevobj.__class__.__name__)
                # At this point we are guaranteed to have a val (or an exception)
            if val is None:
                return None
            prevelem = elem
            prevobj = obj
            #print 'Key:',key, 'Elem:',elem, 'Val:', val, 'Obj:',obj
            #self[key] = val # data cache
        self._cache_field(key, val)
        return val
        
        ##   def _lookup_path(self, key):
        ##     """Should throw an exception only if 'key' is not a correct path.
        ##     If path elements are not found because of NULL values, None is
        ##     returned.
        ##     """
        ##     path = string.split(key, '__')
        ##     # not a real path
        ##     if len(path) == 1:
        ##       foreignkey = key + '_id'
        ##       if self.foreignfieldtypes.has_key(foreignkey):
        ##         klass = self.foreignfieldtypes[foreignkey]
        ##         foreignkeyvalue = self.data.get(foreignkey)
        ##         if foreignkeyvalue:
        ##           res = klass(self[foreignkey])
        ##         else:
        ##           res = None
        ##         # self[key] = res # data cache
        ##      self._cache_field(key, res)
        ##         return res
        ##       else:
        ##         raise DBAppError, "lookup error: '%s' is not a valid path" % key
        ##     # len > 1
        ##     obj = self
        ##     for elem in path:
        ##       try:
        ##         val = obj[elem]
        ##       except:
        ##         raise DBAppError, "path lookup error: '%s' is not a valid path for %s" % \
        ##               (elem, obj.__class__.__name__)
        ##       # At this point we are guaranteed to have a val (or an exception)
        ##       if val is None:
        ##         return None
        ##       if isinstance(val, DBObjekt):
        ##         obj = val
        ##       else:  # check whether val is a foreign key
        ##         klass = obj.__class__
        ##         if klass.foreignfieldtypes.has_key(elem):
        ##           klass = klass.foreignfieldtypes[elem]
        ##           obj = klass(val)
        ##      else: obj = None
        ##       print 'Key:',key, 'Elem:',elem, 'Val:', val, 'Obj:',obj
        ##     #self[key] = val # data cache
        ##     self._cache_field(key, val)
        ##     return val
        
        
    def _getinverses(self, key):
        klass, field = self.inversefieldtypes[key]
        ids = self.data.get(key + '_ids')
        #print "Gecachte Inversen für %s(%s).%s: %s" \
         # % (self.__class__.__name__, self[self.primarykey], key, ids)
        if not ids is None:
            return klass(ids)
        list = klass(field, self.data[self.primarykey])
        #print "Inversen registrieren für %s(%s).%s: %s" \
         # % (self.__class__.__name__, self[self.primarykey], key, list.getIds())
        self.data[key + '_ids'] = list.getIds()
        return list
        
        
    def getinv(self, inverse, where = None, v1 = None, k2 = None, v2 = None, order = None):
        if self.inversefieldtypes.has_key(inverse):
            if where == v1 == k2 == v2 == order == None:
                return self._getinverses(inverse)
            klass, field = self.inversefieldtypes[inverse]
            wherestr = "%s = %s" % (field, self.data[self.primarykey])
            if not where is None and v1 is None:
                if where:
                    wherestr = "%s and %s" % (where, wherestr)
            if where and not v1 is None:
                wherestr = "%s and %s = %s" % (wherestr, where, sql.msql_quote(v1))
                if k2 and not v2 is None:
                    wherestr = "%s and %s = %s" % (wherestr, k2, sql.msql_quote(v2))
            return klass(where = wherestr, order = order)
        else:
            raise DBAppError("Not defined as inverse relation: '%s'" % inverse)
            
    def new(self, keyval = None):
        if not self.primarykey:
            raise DBAppError("Method 'new' only for objects with a primarykey")
        if not keyval:
            keyval =  self.getNewId()
        self[self.primarykey] = keyval
        
    def getNewId(self):
        """Standardmethode, um neue Werte für Schlüsselfelder zu erzeugen.
        
        Liefert ein dictionary mit einem Wert für jeden Schlüssel.
        Sollte von Unterklassen überschrieben werden.
        Funktioniert aber, wenn
        - es ein einziges Schlüsselfeld gibt, und
        - dieses von Typ Integer ist.
        """
        if not self.primarykey:
            raise DBAppError("Cannot getNewId without primarykey")
        max = self._max(self.primarykey)
        if type(max) in (type(1L), type(1)):
            return max + 1
        raise DBAppError("Could not assign key value for new dbobject")
        
        # Für die referentielle Integrität im Cache müssen die Inversen
        # updatet werden
    def insert(self, keyval = None):
        if keyval: self.new(keyval)
        wherestr, res = self._testKey()
        if len(res) > 0:
            raise DBAppError("Insert for already existing dbobject", wherestr, res)
        res = self.updateSQL.executeInsert(self.data)
        _cache.cache(self, update_inverses = 1)
        self.data['__p__'] = 1
        return res
        
        
    dict_update = UserDict.update
    
    def update(self, dict = None):
        data = self.data
        for k in dict.keys():
            if dict[k] == data[k]: del dict[k]
        if not dict: return
        primarykey = self.primarykey
        if (primarykey and dict.has_key(primarykey) and
            dict[primarykey] != self.data[primarykey]):
            raise DBAppError("Attempt to change value of primary key")
            
        wherestr, res = self._testKey()
        if len(res) == 0:
            raise DBAppError("Update for non-existent dbobject", wherestr)
        if len(res) > 1:
            raise DBAppError("Update for non-unique object", wherestr, res)
        res = self.updateSQL.executeUpdate(dict, wherestr)
        if primarykey:
            primarykeyvalue = self.data[primarykey]
            for k in dict.keys():
                if self.foreignfieldtypes.has_key(k):
                    (klass, inversefield) = self.foreignfieldtypes[k]
                    if inversefield:
                        new_fk = dict[k]
                        old_fk = self.data.get(k)
                        if old_fk and _cache.is_cached(klass, old_fk):
                            inverselist = klass(old_fk).data.get(inversefield + '_ids')
                            if not inverselist is None:
                                inverselist.remove(primarykeyvalue)
                        if new_fk and _cache.is_cached(klass, new_fk):
                            inverselist = klass(new_fk).data.get(inversefield + '_ids')
                            if not inverselist is None:
                                inverselist.append(primarykeyvalue)
        if self.otherkeys:
            _cache.uncache(self)
            self.dict_update(dict)
            _cache.cache(self)
        else:
            self.dict_update(dict)
        return res
        
        
        # Für die referentielle Integrität im Cache müssen die Inversen
        # updatet werden
    def delete(self):
        wherestr, res = self._testKey()
        if len(res) == 0:
            raise DBAppError("Delete for non-existent dbobject", wherestr)
        if len(res) > 1:
            raise DBAppError("Delete for non-unique dbobject", wherestr, res)
        res = self.updateSQL.executeDelete(wherestr)
        _cache.uncache(self, update_inverses = 1)
        #jh: wirft Exception, key __p__, bei removeteiln -- (n-n) Beiehung
        try:
            del self.data['__p__']
        except: pass
        return res
        
    def _testKey(self):
        if self.primarykey:
            val = self.get(self.primarykey)
            if val is None:
                raise DBAppError("Required key '%s' missing for insert, update or delete"
                                 % (self.primarykey,))
            where ="%s = %s" % (self.primarykey, sql.msql_quote(val))
        else:
            kv = self._getKeyValues(self.data)
            if kv:
                otherkeys, values = kv
            else:
                raise DBAppError("Required keys '%s' missing for insert, update or delete"
                                 % (self.otherkeys,))
            wherelist = []
            for k,v in map(None, otherkeys, values):
                wherelist.append("%s = %s" % (k, sql.msql_quote(v)))
            where = string.join(wherelist, ' and ')
        return where, self.querySQL.executeQuery(where)
        
    def _max(self, field, where = ''):
        res = self.querySQL.executeQuery(where = where, order = field)
        if res:
            last = res[-1]
            return last[self.querySQL.fieldnames.index(field)]
        return None
        
        
        
    def show(self):
        print "instance of class `%s':" % self.__class__.__name__
        for k in self.keys():
            print "%10s:  %s" % (k, self[k])
            
            
    def _test_consistency(self):
        """All ids are unique. All referenced foreign keys exist."""
        tmp = cache_is_on()
        cache_off()
        print 'Testing %s' % self.__class__,__name__
        ok = 1
        res = self.querySQL.executeQuery(where='')
        iddict = {}
        for tuple in res:
            dict = sql.tuple2dict(tuple, self.querySQL.fieldnames)
            m = self.__class__()
            m.data = dict
            id = self.primarykey
            if id:
                if iddict.has_key(m.data[id]):
                    print "  Key %s occurs multiple times in %s" \
                                     % (m.data[id], self.__class__.__name__)
                    ok = 0
                iddict[m.data[id]] = 1
            ok = m._test_foreign_keys()
            #print len(res), len(iddict)
            #print res, iddict
        if ok:
            print 'Class %s is consistent (%s different keys)' \
                  % (self.__class__.__name__, len(res))
        else:
            print '***** %s is inconsistent (%s different keys)' \
                  % (self.__class__.__name__, len(res))
            
        if tmp: cache_on()
        return ok
        
    def _test_foreign_keys(self):
        assert not cache_is_on()
        ok = 1
        idfield = self.primarykey
        id = None
        if idfield:
            id = self.data[idfield]
        message = " id: %s, %s: %s  (%s)"
        for fk, (klass, inversefield) in self.foreignfieldtypes.items():
            fkval = self.data[fk]
            if fkval is None:
                print message % (id, fk, fkval, "Missing foreign key")
            elif fkval < 1:
                print message % (id, fk, fkval, "Wrong foreign key")
            else:
                try:
                    klass(fkval)
                except Exception, e:
                    print message % (id, fk, fkval, e)
                    ok = 0
        return ok
        
    def _test_data(self):
        data = self.data
        for f in self.fields:
            if not data.has_key(f):
                return "%s: %s" % (self.clk(), f)
        return 0
        
    def clk(self):
        if self.primarykey:
            return "%s(%s)" % (self.__class__.__name__, self.data[self.primarykey])
        return "%s(nokey)" % (self.__class__.__name__)
        
from  UserList import UserList
class Container(UserList):
    """Abstrakte Klasse für Container-Objekte.
    
    Die Klasse kann nur von konkreten Unterklassen verwendet werden. Für
    jede Unterklasse von DBObjekt kann eine solche Klasse definiert werden.
    
    Im einfachsten Fall kann dies z.B. für MitarbeiterList so
    aussehen:
    
    class MitarbeiterList(Container):
    resultClass = Mitarbeiter     # Die Klasse, von der die Listenelemente Instanz
                                  # sein sollen. (Diese Klasse braucht eine
                                  # _initializeFromData Methode)
    querySQL = SQL.SimpleSQL.MitarbeiterList
    # oder:  querySQL = resultClass.querySQL
                                  # SQL statement mit dem die Liste erzeugt wird
                                  # (muß vorher definiert sein)
    
    
    Nach dieser Klassendefinition steht folgende Standardfunktionalität zur Verfügung:
    
    ml = MitarbeiterList()          # Leerer Container.
    ml = MitarbeiterList(AndereMitarbeiterList)
                                  # Container wird mit einer anderen Liste desselben
                                  # Typs initialisiert.
    ml = MitarbeiterList(where = '')
                                  # Container mit allen Objekten der
                                  # betr. Klasse aus der Datenbank.
    
    ml = MitarbeiterList(where = "age < 30 or name clike '%asf%'", order = 'age desc, zdam')
                                     # where und order müssen als keyword Argumente
                                     # angegeben werden!!
                                     # Die Menge der Objekte, die den Bedingungen
                                     # genügen. Es werden für die Feldnamen die Namen
                                     # verwendet, die bei der Definition des SQL-Objekts
                                     # vereinbart wurden. Bei SimpleSQL sind das die
                                     # Datenbankfeldnamen, bei StandardQuery können das
                                     # auch andere sein, die automatisch durch die korrekten
                                     # Datenbankfeldnamen ersetzt werden.
    
    ml = MitarbeiterList('age', 30, 'na', 'Gast', order = 'stat')
                                     # Alternativ können auch Feld-Wert Paare angegeben
                                     # werden.
    

    zl = ZustaendigkeitList(where = "fall.fn='1-2003A'", 
                            join = [('fall', 'zustaendigkeit.fall_id=fall.id')])
                                  # join erwartet eine Liste von 2-Tupeln, bestehend aus
                                  # Tabellennamen und join-Bedingung.

    Die folgenden Operationen führen die entsprechende Einzeloperation auf allen
    Elementen des Containers aus:
    
    ml.insertall()
    ml.updateall()
    ml.deleteall()
    
    sml = MitarbeiterList(ml)  # Liste kopierem
    
    sml.sort('name', ('vname, 'desc')', 'age')  # Sortieren nach Feldwerten
    
    
    m = ml.findu('na', 'Bischoff')    # Eindeutiges Element finden mit dem
                                    # gegebenen Feld-Wert Paar.
                                    # Exception, falls kein eindeutiges Ergebnis
                                    # (d.h. keiner bzw. mehrere)
    
    fml = ml.find('vn', 'Peter')      # Alle Elemente finden mit dem
                                    # gegebenen Feld-Wert Paar.
                                    # Ergebnis kann leer sein.
    
    
    fml = ml.filter(myFilterFunction) # Alle Elemente finden, für die myFilterFunction
                                    # true liefert.
    
    # Filterfunktionen können so
    
    def myFilterFunction(obj):
    return obj['age'] > 20 or obj['name'] == 'Tom'
    
    #   bzw. so
    
    fml = ml.filter(lambda obj: obj['age'] > 20 or obj['name'] == 'Tom')
    
    # definert werden.
    
    Darüber hinaus alle Operationen auf Listen erlaubt.
    """
    
    def __init__(self, data = [], where = None, k2 = None, v2 = None, order = '', join = []):
        self.data = []
        if data and  where is None:
            if type(data) == type([]):
              # Initialisierung mit Liste von ids
                if type(data[0]) in (type(1L), type(1)):
                    for id in data:
                        self.data.append(self.resultClass(id))
                        # Initialisierung mit Liste von Objekten
                elif isinstance(data[0], self.resultClass):
                    self.data = data
                else:
                    raise DBAppError('Wrong data for initialization of Container: %s', data)
            elif isinstance(data, self.__class__):
              # Initialisierung mit Container
                self.data = data.data
            else:
                raise DBAppError('Wrong data for initialization of Container: %s', data)
            return
            
        if data and not where is None:   # wird als feld = wert interpretiert
            where = "%s = %s" % (data, sql.msql_quote(where))
            if k2 and not v2 is None:
                where = "%s and %s = %s" % (where, k2, sql.msql_quote(v2))
        if not where is None:
            where, order, join = self._expand(where, order, join)
            res = self.querySQL.executeQuery(where, order, join)
            for tuple in res:
                dict = sql.tuple2dict(tuple, self.querySQL.fieldnames)
                m = self.resultClass()
                m.data = dict
                # m.data may be replaced by an already cached state of the object
                # the values from the database should be identical to the cached
                # values, but the cached object may have additional values
                if _cache.get(m):
                  # vielleicht besser:
                  # assert m.data == dict (nicht ganz, da es auch noch gecachte paths geben kann)
                    m.data.update(dict)
                else:
                    m.data['__p__'] = 1
                    _cache.cache(m)
                self.data.append(m)
                
    def _expand(self, where, order, join):
        if string.find(where, '__') < 0:
            return (where, order, join)
            # offensichtlich gequotete strings rausnehmen
        assert not join, "Joins in Verbindung mit Feld-Pfad-Ausdrücken noch nicht getestet"
        wsl = re.split(r"('[^']*')", where)
        res = []
        join = dict(join)
        klass = self.resultClass
        fieldnames = klass.fields
        table = klass.table
        for i in range(len(wsl)):
            if wsl[i]:
              # nur in nicht-strings ersetzen
                if wsl[i][0] == "'":
                    res.append(wsl[i])
                else:
                    p = re.split("([\W]+)", wsl[i])
                    for j in range(len(p)):
                        pj = p[j]
                        if pj in fieldnames:
                            p[j] = "%s.%s" % (table, pj)
                        else:
                            path = string.split(pj, '__')
                            if len(path) == 1: continue
                            curr_class = klass
                            for elem in path[:-1]:
                                if curr_class.foreignfieldtypes.has_key(elem):
                                    prev_class = curr_class
                                    curr_class, inv = prev_class.foreignfieldtypes[elem]
                                    join[curr_class.table] = "%s.%s = %s.%s" % \
                                                 (prev_class.table, elem,
                                                  curr_class.table, curr_class.primarykey)
                                elif curr_class.inversefieldtypes.has_key(elem):
                                    prev_class = curr_class
                                    curr_class_list, field = prev_class.inversefieldtypes[elem]
                                    curr_class = curr_class_list.resultClass
                                    join[curr_class.table] = "%s.%s = %s.%s" % \
                                                 (prev_class.table, prev_class.primarykey,
                                                  curr_class.table, field)
                                else:
                                    raise DBAppError("Error in field path: '%s'" % path)
                            p[j] = "%s.%s" % (curr_class.table, path[-1])
                    res = res + p
                    
        if order:
            p = re.split("([\W]+)", order)
            for j in range(len(p)):
                pj = p[j]
                if 'desc' != string.lower(pj) and pj in fieldnames:
                    p[j] = "%s.%s" % (table, pj)
            order = string.join(p, '')
        return string.join(res, ''), order, join.items()
        
        
    def getTable(self, where = '', order = ''):
        where, order, join = self._expand(where, order, [])
        return self.querySQL.executeQuery(where, order, join)
        
    def _updateOrInsertTableSmall(self, table):
        """Table is a list of tuples or lists each of which represents a database
        record (row of a table). For each row in table, either insert it into the
        database (into the table self.resultClass.table) if a record with the same
        key does not already exist, or update the existing record if necessary.
        Assumes that table is sorted by key. """
        
        keyname = self.resultClass.primarykey
        key_index = self.resultClass.fields.index(keyname)
        updatesql = self.resultClass.updateSQL
        if keyname is None:
            raise DBAppError('updateOrInsertTable not implemented for composite primary keys')
        wherelist = []
        for row in table:
            wherelist.append("%s = %s" % (keyname, sql.msql_quote(row[key_index])))
        wherestr = string.join(wherelist, ' or ')
        res = self.getTable(where = wherestr, order = keyname)
        res_dict = {}
        for i in range(len(res)):
            res_dict[res[i][key_index]] = res[i]
        for row in table:
            key = row[key_index]
            dbrow = res_dict.get(key)
            if dbrow:
                if dbrow != row:
                    updatesql.executeUpdate(row,
                                            where = "%s = %s" % (keyname, sql.msql_quote(key)))
            else:
                updatesql.executeInsert(row)
                
                
                
    def updateOrInsertTable(self, table):
        """Table is a list of tuples or lists each of which represents a database
        record (row of a table). For each row in table, either insert it into the
        database (into the table self.resultClass.table) if a record with the same
        key does not already exist, or update the existing record if necessary. """
        
        while table:
            if len(table) > 40:
                batch = table[:40]
                table = table[40:]
            else:
                batch = table
                table = None
            self._updateOrInsertTableSmall(batch)
            
            
    def byQuery(self, query, **params):
        """Es müssen alle Feldnamen einer Tabelle in der richtigen Reihenfolge
        der Tabellenfelder in der Select-Anweisung aufgeführt sein (!), wenn
        die Klasse SQL in sql.py direkt für Select-Statements benutzt wird
        sein. """
        
        res = query.execute(params)
        self.data = []
        fields = self.resultClass.fields
        for tuple in res:
            dict = sql.tuple2dict(tuple, fields)
            m = self.resultClass()
            m.data = dict
            if _cache.get(m):
                m.data.update(dict)
            else:
                m.data['__p__'] = 1
                _cache.cache(m)
            self.data.append(m)
        return self
        
    def insertall(self):
        for o in self:
            o.insert()
            
    def updateall(self):
        for o in self:
            o.update()
            
    def deleteall(self):
        keyname = self.resultClass.primarykey
        if keyname is None:
            for o in self:
                o.delete()
            return
        wherelist = []
        batchcount = 0
        if self.data:
            _cache.clear()
        for o in self:
            if not isinstance(o, self.resultClass):
                raise DBAppError('Wrong object in Container for deletion')
            wherelist.append("%s = %s" % (keyname, sql.msql_quote(o[keyname])))
            batchcount = batchcount + 1
            if batchcount > 40:
              # Wir müssen die deletes ab und zu abschicken, da msql nicht
              # so lange where strings mag
                wherestr = string.join(wherelist, ' or ')
                self.resultClass.updateSQL.executeDelete(wherestr)
                wherelist = []
                batchcount = 0
        if wherelist:
            wherestr = string.join(wherelist, ' or ')
            self.resultClass.updateSQL.executeDelete(wherestr)
            #self.resultClass.updateSQL.executeDelete('1=1')
            
            
    def filter(self, function):
        elems = filter(function, self)
        return self.__class__(elems)
        
        
    def find(self, key, value):
        """finds list of elements matching list by key, value pair."""
        return self.filter(lambda x, k=key, v=value: x[k]==v)
        
    def findu(self, key, value, throw = 1):
        """finds unique element in list by key, value pair."""
        res = filter(lambda x, k=key, v=value: x[k]==v, self)
        if len(res) == 1:
            return res[0]
        elif throw:
            if len(res) == 0:
                raise DBAppError("findu: element with '%s = %s' not found" % (key, value))
            else:
                raise DBAppError("findu: more than one element with '%s = %s' found" % (key, value))
        else:
            return None
            
            
    def sort(self, *fields):
        ftuplelist = []
        for f in fields:
            if type(f) != type((1,)):
                f = (f,None)
            ftuplelist.append(f)
        def mycmp(a, b, fields = ftuplelist):
            for f in fields:
                fn = f[0]
                res = cmp(a[fn], b[fn])
                if res != 0:
                    if f[1]: return -res
                    return res
            return 0
        UserList.sort(self, mycmp)
        
    def __cmp__(self, list):
        if type(list) == type(self.data):
            return cmp(self.data, list)
        elif isinstance(list, self.__class__):
            return cmp(self.data, list.data)
        else:
            return cmp(self.data, list)
            
            
    def getIds(self):
        res = []
        primarykey = self.resultClass.primarykey
        if primarykey:
            for o in self.data:
                res.append(o[primarykey])
            return res
            
            
