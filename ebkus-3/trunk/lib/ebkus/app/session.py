# coding: latin-1

# Sessions sind nicht persistent. Nach 
# einem Server-Neustart sind sie weg.

import time, sha, logging

from ebkus.config import config
from ebkus.app.ebapi import Session, SessionList

def get_session(REQUEST, RESPONSE):
    """Gibt eine gültige Session zurück oder None""" 
    try:
        session_id = REQUEST.get('session_id')
    except:
        session_id = None
    session = _session._session_dict.get(session_id)
    if session:
        if session.is_valid():
            session.touch()
            return session
        else:
            session.expire(RESPONSE)
    RESPONSE.expireCookie('session_id')
    return None

def create_session(user, RESPONSE):
    """Legt eine neue Session für user an""" 
    session = _session(user, RESPONSE)
    return session

def has_session(user):
    """Gibt eine gültige Sessions von user zurück oder None"""
    _check_sessions()
    return _session._user_dict.get(user)


# ab hier alles private

def _check_sessions():
    """Ungültige Sessions rauswerfen"""
    for s_id, s in _session._session_dict.items():
        if not s.is_valid():
            del s._session_dict[s_id]
            del s._user_dict[s.user]
            
# die _session Klasse ist ebenfalls private
class _session(object):
    # hier werden alle sessions aufbewahrt
    _session_dict = {}
    _user_dict = {}

    def __init__(self, user, RESPONSE):
        self.user = user
        self.time = time.time()
        self.session_id = self._create_session_id()
        # hier kann das Programm über Requests hinweg Daten ablegen
        self.data = {}
        self._session_dict[self.session_id] = self
        self._user_dict[user] = self
        # cookie haelt nur einen guten Tag (mehr als 86400 Sek.)
        RESPONSE.setCookie("session_id", self.session_id, max_age=100000)
        
    def _create_session_id(self):
        s = sha.new("%s %s" % (self.user, self.time))
        return s.hexdigest()

    def is_valid(self):
        valid = time.time() < int(config.SESSION_TIME*60) + self.time
        logging.debug("Sessionzeit: %s (%s)", time.ctime(self.time), valid)
        return valid

    def expire(self, RESPONSE):
        """Eine Session sofort beenden"""
        del self._session_dict[self.session_id]
        del self._user_dict[self.user]
        RESPONSE.expireCookie("session_id")
        _check_sessions()
        
    def delete(self):
        del self._session_dict[self.session_id]
        del self._user_dict[self.user]
        _check_sessions()
        
    def touch(self):
        """Eine Session aktualisieren"""
        self.time = time.time()
