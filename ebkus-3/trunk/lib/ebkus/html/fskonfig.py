# coding: latin-1

"""Module für die Administration und Feedback"""


import os

from ebkus.app import Request
from ebkus.app import ebupd
from ebkus.app.ebapi import Akte, Fachstatistik, Jugendhilfestatistik, Code, Mitarbeiter, Kategorie
from ebkus.app.ebapi import ProtokollList, TabellenID, Code
from ebkus.app_surface.standard_templates import *
from ebkus.config import config

from ebkus.app.fachstatistikdef import fsdef

class fskonfig(Request.Request):
    """Konfiguration der Fachstatistik."""
    
    permissions = Request.ADMIN_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        pass
