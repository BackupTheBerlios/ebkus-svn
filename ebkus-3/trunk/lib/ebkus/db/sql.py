# coding: latin-1
"""Funktionen und Klassen zur Kommunikation mit der Datenbank.

Funktionen
==========

opendb()       die Datenbank �ffnen
closedb()      dito, schlie�en
getDBHandle()  Objekt f�r ge�ffnete Datenbank holen, auf dem queries, etc.
               azsgef�hrt werden k�nnen


Klassen
=======

SQL                  Basisklasse f�r parametrisierbare SQL statements
SimpleSQL(SQL)       Erm�glicht Select, Update, Insert, Delete auf einer Tabelle

Funktionen
==========

tuple2dict          Macht aus einem Tuple und einer gleichlangen Namenliste eine
                    dictionary


"""

## import log
import string
import time
import logging
from ebkus.db.dbadapter import connect
from ebkus.config import config


# Falls 1, werden alle SQL Statements vor der Ausf�hrung ausgegeben, sowie
# deren Ergebnisse nach der Ausf�hrung
###########################
# msg systems ag 02.07.2002
###########################
debug = 0
def debug_on():
    global debug
    debug = 1
def debug_off():
    global debug
    debug = 0
    
    # globale Variablen, die von opendb(), closedb() und getDBHandle()
    # verwendet wird.
dbHandle = None
# Nach einer Stunde wird die connection zwangsweise geschlossen
# und eine neue geholt. Damit wird vermieden, dass alte
# connections erhalten bleiben, die vom MySQL-Server schon ein
# timeout erfahren haben ("MySQL server has gone away")
_dbHandle_creation_time = None
#_dbHandle_timeout = 15 # zum testen
_dbHandle_timeout = 3600


class SQLError(Exception):
    pass
    
def opendb(host=config.DATABASE_HOST, user=config.DATABASE_USER,
           passwd=config.DATABASE_PASSWORD, db=config.DATABASE_NAME):
    global dbHandle
    global _dbHandle_creation_time
    if dbHandle:
        if (time.time() - _dbHandle_timeout) > _dbHandle_creation_time:
            dbHandle.close()
            dbHandle = None
            logging.debug("Database connection timeout")
        else:
            return
    dbHandle = connect(host=host, user=user,
                       passwd=passwd, db=db)
    _dbHandle_creation_time = time.time()
    logging.debug("Neue database connection erzeugt")

def closedb():
    # TBD: was sollte hier passieren?
    pass
    #  global dbHandle
    #  if not dbHandle is None:
    #    dbHandle.close()
    #  dbHandle = None
    
    
def getDBHandle():
    global dbHandle
    if dbHandle is None:
        raise SQLError('Database not opened')
    return dbHandle
    
    
    
WHERE_ORDER_TEMPLATE = "%(WHERE_KW)s %(WHERE)s %(ORDER_KW)s %(ORDER)s"


class SQL:
    """Basisklassen zur Verwaltung von SQL Statements.
    
    Instanzen dieser Klassen sind parametrisierbare, ausf�hrbare SQL statements.
    Beispiel:
    
    Erzeugung einer Instanz von SQL:
    sql = SQL("SELECT %(fields)s FROM %(table)",
             table = 'mitarbeiter',              # default f�r Parameter table
             fields = "vn, na")                  # default f�r Parameter fields
    
    Anwendung der Instanz:
    res = sql.execute()                                  # verwendet beide defaults
    res = sql.execute(fields = "vn, na, stz")            # verwendet default nur f�r table
    res = sql.execute(table = 'akte', fields = "vn, na") # verwendet keine defaults
    
    string = sql.getSQL(table = 'akte')  # Liefert den substituierten SQL-statement,
                                        # der von execute ausgef�hrt werden w�rde.
    
    
    Es kann sich auch um INSERT, UPDATE und DELETE statements handeln.
    
    """
    
    def __init__(self, sqltemplate, defaults = {}, **params):
        self.sqltemplate = sqltemplate
        defaults.update(params)
        self.defaults = defaults
        
    def evalSQLTemplate(self, params):
        actual_params = self.defaults.copy()
        actual_params.update(params)
        try:
            result = self.sqltemplate % actual_params
        except:
            raise
##             raise SQLError('Error in parameter substitution',
##                            params, actual_params)
        return result
        
    def execute(self, params={}):
        """Substitute variables in self.sqltemplate using params (or
        self.defaults), and execute the resulting SQL statement."""
        
        sql = self.evalSQLTemplate(params)
        #if debug: log.log1( sql)
        if debug: print sql
        try:
            result = getDBHandle().query(sql)
        except Exception, text:
            raise SQLError('database error', str(text), sql)
            #if debug: log.log1(result)
        if debug: print result
        return result
        
    def getSQL(self, **params):
        return self.evalSQLTemplate(params)
        
    def __call__(self, **params):
        return self.execute(params)

def execute(sql):
    s = SQL(sql)
    return s.execute()
        
class SimpleSQL(SQL):

    """Einfache SQL Objekte, die sowohl f�r einfache Queries als auch f�r
    Insert, Update und Delete verwendet werden k�nnen.
    
    Auch joins sind m�glich.
    
    
    Beispiele f�r SimpleSQL
    
    s=SimpleSQL(table = 'zustaendigkeit',             # Tabellenname wie in der Datenbank
           fields =   ['id', 'fall_id', 'mit_id',\  # Feldnamen wie in der Datenbank
                      'bgd', 'bgm', 'bgy', 'ed', \
                         'em', 'ey'],
           WHERE = 'ey = 0',                        # default f�r WHERE nur f�r SELECT
           ORDER = 'ey DESC')                       # default f�r ORDER bei SELECT
    
    
    Anwendungsbeispiele:
    
    res = s.executeQuery(where ="fall_id = 40 or id < 20", order = 'bgm DESC')
    res = s.executeUpdate({'bgm':0,'ed':1}, where ="fall_id = 40 or id < 20")
    res = s.executeDelete(where ="fall_id = 40 or id < 20")
    res = s.executeInsert({'id':55, 'fall_id':22, 'bgm':0, 'ed':1})
    
    Dieselben Paramter wie bei execute*( ... ):
    
    sqlstring = s.getQuerySQL( ... )
    sqlstring = s.getUpdateSQL( ... )
    sqlstring = s.getInsertSQL( ... )
    sqlstring = s.getDeleteSQL( ... )

    Beispiel mit einem join:

    s = SimpleSQL(table = 'zustaendigkeit',
                  fields = ['id', 'fall_id', 'mit_id', 'bgd', 'bgm', 'bgy', 'ed', 'em', 'ey'])
    s.executeQuery(where = "fall.fn='1-2003A'", order = 'fall_id',
                   join = [('fall', 'zustaendigkeit.fall_id=fall.id')])

    join erwartet eine Liste von 2-Tuple, bestehend aus Tabellennamen und join-Bedingung.
        
    """
    
    def __init__(self, table, fields, WHERE = '', ORDER = ''):
        self.fieldnames = fields
        self.table = table
        SELECTstr = string.join(map(lambda x,t=table: "%s.%s"%(t,x), fields), ', ')
        TABLES = "%(TABLES)s"
        self.sqlquerytemplate = "SELECT distinct %s FROM %s %s" % \
                                (SELECTstr, TABLES, WHERE_ORDER_TEMPLATE)
        self.whereconst = WHERE
        self.orderconst = ORDER
        apply(SQL.__init__, (self, '%(SQL_DML)s'))
        
    def getQueryParams(self, where = '', order = '', join = []):
        tables = [self.table]
        for t,c in join:
            tables.append(t)
            if where:
                where = "%s and %s" % (c, where)
            else: where = c
        if self.whereconst and where:
            andw = ' and '
            where = "( %s )" % where
        else:
            andw = ''
        where = self.whereconst + andw + where
        if not order:
            order = self.orderconst
        params = {}
        params['TABLES'] = string.join(tables, ', ')
        if where:
            params['WHERE_KW'] = 'WHERE'
            params['WHERE'] = where
        else:
            params['WHERE_KW'] = ''
            params['WHERE'] = ''
        if order:
            params['ORDER_KW'] = 'ORDER BY'
            params['ORDER'] = order
        else:
            params['ORDER_KW'] = ''
            params['ORDER'] = ''
        return params
        
    def getQuerySQL(self, where = '', order = '', join=[]):
        return self.evalSQLTemplate({ 'SQL_DML' :
                              self.sqlquerytemplate % \
                                      self.getQueryParams(where, order, join)})
        
    def executeQuery(self, where = '', order = '', join=[]):
        return self.execute({ 'SQL_DML' :
                              self.sqlquerytemplate % \
                              self.getQueryParams(where, order, join)})
        
    def executeUniqueQuery(self, where = ''):
        result = self.executeQuery(where)
        if not len(result) == 1:
            raise SQLError('Result not unique', self.getQuerySQL(where))
        return result[0]
        
    def getUpdateSQL(self, values, where):
        fns = self.fieldnames
        setlist = []
        if not (type(values) == type(()) or type(values) == type([])):
            for i in range(len(fns)):
                if values.has_key(fns[i]):
                    val = values[fns[i]]
                    if val is None:
                        setlist.append("%s = NULL" % (fns[i],))
                    else:
                        setlist.append("%s = %s" % (fns[i], msql_quote(val)))
        else:
            for i in range(len(fns)):
                val = values[i]
                if val is None:
                    setlist.append("%s = NULL" % (fns[i],))
                else:
                    setlist.append("%s = %s" % (fns[i], msql_quote(val)))
        setstr = string.join(setlist, ', ')
        sql = "UPDATE %s SET %s WHERE %s" % (self.table, setstr, where)
        return sql
        
        ## INSERT INTO table_name [ ( column [ , column ]** ) ]
        ##               VALUES (value [, value]** )
        
    def getInsertSQL(self, values):
        fns = self.fieldnames
        
        collist = []
        vallist = []
        if not (type(values) == type(()) or type(values) == type([])):
            for i in range(len(fns)):
                val = values.get(fns[i])
                if not val is None:
                    collist.append(fns[i])
                    vallist.append(msql_quote(val))
        else:
            for i in range(len(fns)):
                val = values[i]
                if not val is None:
                    collist.append(fns[i])
                    vallist.append(msql_quote(val))
                    
        colstr = string.join(collist, ', ')
        valstr = string.join(vallist, ', ')
        sql = "INSERT INTO %s ( %s ) VALUES ( %s )" % (self.table, colstr, valstr)
        return sql
        
        
        
        ##          DELETE FROM table_name
        ##               WHERE column OPERATOR value
        ##               [ AND | OR column OPERATOR value ]**
        
    def getDeleteSQL(self, where):
        sql = "DELETE FROM %s WHERE %s" % (self.table, where)
        return sql
        
    def executeUpdate(self, values, where):
        return self.execute({ 'SQL_DML' : self.getUpdateSQL(values, where) } )
        
        
    def executeInsert(self, values):
        return self.execute({ 'SQL_DML' : self.getInsertSQL(values) } )
        
        
    def executeDelete(self, where):
        return self.execute({ 'SQL_DML' : self.getDeleteSQL(where) } )
        
        
        ###############################################
        # Hilfsfunktionen:
        #   tuple2dict, msql_quote
        ################################################
        
        
        ## Man k�nnte auch auf die Konvertierung verzichten, und die Werte von Namen
        ## �ber den assoziierten Index im Tuple ermitteln!!
        
def tuple2dict(tuple, names, dict = None):
    """Converts a tuples in a dictionarie using the provided
    names as keys."""
    
    if len(names) != len(tuple):
        raise SQLError('Wrong number of names for mapping names to tuple')
    if not dict:
        dict = {}
    for i in range(len(names)):
        dict[names[i]] = tuple[i]
    return dict
    
    
def msql_quote(arg):
    if type(arg) == type(''):
        return "'%s'" % arg.replace("'", "\\'")
    else:
        return "%s" % arg
        #return repr(arg)
        
        
        
        
