# coding: latin-1
"""Das Module, in dem Bobo Objekte zum 'publishen' findet.
Publiziert wird der Wert von bobo_application, eine Instanz der
Klasse EBKuS."""

import sys
import warnings
# weg mit der 'rotor is deprecated' Warnung
warnings.filterwarnings('ignore', '', DeprecationWarning, 'ebkus\.html\.administration', 11)
warnings.filterwarnings('ignore', '', DeprecationWarning, 'ebkus\.app\.protocol', 11)
# weg mit der 'regsub, regex is deprecated' Warnung
warnings.filterwarnings('ignore', '', DeprecationWarning, 'ebkus\.bobo\.cgi_module_publisher', 455)
warnings.filterwarnings('ignore', '', DeprecationWarning, 'ebkus\.bobo\.CGIResponse', 59)
warnings.filterwarnings('ignore', '', DeprecationWarning, 'regsub', 15)

from ebkus.db import sql
sql.debug = 0
from ebkus.db import dbapp
# dbapp.cache_off()
dbapp.cache_on()

from ebkus.app import EBKuS
bobo_application = EBKuS.EBKuS()
__bobo_hide_tracebacks__ = None

