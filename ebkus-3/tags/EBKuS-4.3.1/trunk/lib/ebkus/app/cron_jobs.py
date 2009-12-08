#!/usr/local/bin/python
# coding: latin-1


#########################################################################
#   Alle cron_jobs fuer EBKuS. Kann einmal nachts ausgefuehrt werden.
#   Die Routinen sind in ebupd.py (alle Aenderungen der DB) oder in
#   ebapi.py bzw. ebapih.py .
##########################################################################

import time, os

from ebkus.app import ebupd
from ebkus.app import ebapi 
from ebkus.config import config


def rmakten():
    """Loescht die Akten nach Ablauf der Aufbewahrungszeit, vgl. config.py"""
    
    from ebupd import removeakten
    
    opendb()
    form = { 'frist' : '%s' % config.LOESCHFRIST}
    removeakten(form)
    closedb()
    
    
if __name__ == '__main__':

  ############################################################
  # Achtung! Bei falschem Systemdatum droht Verlust der Akten!
  ############################################################

##   if '%(day)s' % today() == '23':     # Tag des Jobs. Nach Bedarf ändern.
##     rmakten()                         


  ################################################################
  # wandelt die importierten PDF-Dokumente in grausliges Ascii um!
  # wird für die Suche (mit grep) gebraucht.
  #################################################################

    ebapi.convert_pstoascii()
    
