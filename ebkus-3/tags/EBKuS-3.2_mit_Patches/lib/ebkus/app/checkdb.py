#!/usr/local/bin/python
# coding: latin-1

from ebkus.app import ebapi
from ebkus.db import dbapp, sql

sql.opendb()
sql.debug=0
dbapp.cache_off()

ebapi.Akte()._test_consistency()
ebapi.Leistung()._test_consistency()
ebapi.Einrichtungskontakt()._test_consistency()
ebapi.Anmeldung()._test_consistency()
ebapi.Bezugsperson()._test_consistency()
ebapi.Zustaendigkeit()._test_consistency()
ebapi.Fall()._test_consistency()
ebapi.Mitarbeiter()._test_consistency()
ebapi.Dokument()._test_consistency()
ebapi.Gruppe()._test_consistency()
ebapi.Gruppendokument()._test_consistency()
ebapi.FallGruppe()._test_consistency()
ebapi.BezugspersonGruppe()._test_consistency()
ebapi.MitarbeiterGruppe()._test_consistency()

ebapi.Code()._test_consistency()
ebapi.Kategorie()._test_consistency()
ebapi.Jugendhilfestatistik()._test_consistency()
ebapi.Fachstatistik()._test_consistency()
ebapi.Fachstatistikleistung()._test_consistency()
ebapi.Fachstatistikkindproblem()._test_consistency()
ebapi.Fachstatistikelternproblem()._test_consistency()

## höchstens eine Anmeldung/Fall
## höchstens ein aktueller Fall
## genau eine offene Zuständigkeit für einen offenen Fall

sql.closedb()


