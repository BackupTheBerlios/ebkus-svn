# coding: latin-1
"""Generic database adapter for MySQL. Implements only the minimum
of functionality needed in sql.py"""

import logging
from ebkus.config import config


assert config.DATABASE_TYPE == 'MySQLdb', "Zur Zeit funktioniert EBKuS nur mit MySQLdb"

import MySQLdb
from _mysql_exceptions import MySQLError as DatabaseError

ebkustype_conv = { MySQLdb.FIELD_TYPE.TINY: int,
            MySQLdb.FIELD_TYPE.SHORT: int,
            MySQLdb.FIELD_TYPE.LONG: int,
            MySQLdb.FIELD_TYPE.FLOAT: float,
            MySQLdb.FIELD_TYPE.DOUBLE: float,
            MySQLdb.FIELD_TYPE.LONGLONG: long,
            MySQLdb.FIELD_TYPE.INT24: int,
            MySQLdb.FIELD_TYPE.YEAR: int }

MySQLdb.type_conv = ebkustype_conv

def connect(host='', user='', passwd='', db=''):
    dbname = db
    try:
        db = MySQLdb.connect(host=host, user=user, passwd=passwd, db=dbname)
        logging.info("Datenbankverbindung hergestellt: host=%s db=%s user=%s pw=*****" %
                     (host, dbname, user))
        return DBAdapter(db)
    except Exception, e:
        logging.exception("Datenbankfehler: Verbindung konnte nicht hergestellt werden")
        raise

class DBAdapter:
    def __init__(self, dbhandle):
        self.dbhandle = dbhandle

    def selectdb(self, db = ''):
        self.dbhandle.connect(db = config.DATABASE_NAME)

    def query(self, query):
        #print query
        query = query.strip()
        try:
            from ebkus.app import protocol
            protocol.write_sql_protocol(sql=query)
        except:
            # hat für die Funktionalität keine Bedeutung
            logging.exception("Probleme beim SQL-Protokollieren")
        cursor = self.dbhandle.cursor()
        is_select = query[:6].lower() == 'select'
        try:
            logging.debug("Datenbankzugriff: \n%s", query)
            e_res = cursor.execute(query)
            logging.debug("Resultat (execute): %s", e_res)
            if is_select:
                f_res = cursor.fetchall()
                logging.debug("Resultat (fetchall):\n%s", f_res)
                # schöner, aber overhead für jeden Request auch ohne debugging
                logging.debug("Resultat (fetchall):\n%s", '\n'.join([str(e) for e in f_res]))
                return f_res
            else:
                return e_res
        except Exception, e:
            logging.debug("Fehler beim Datenbankzugriff:", exc_info=True)
            raise

    def listtables(self):
        cursor = self.dbhandle.cursor()
        cursor.execute('SHOW tables')
        tables = map(lambda x: x[0], cursor.fetchall())
        return tables

    def listfields(self, table):
        cursor = self.dbhandle.cursor()
        cursor.execute('SHOW fields from %s' % table)
        return cursor.fetchall()

    def close(self):
        self.dbhandle.close()
        self.dbhandle = None

