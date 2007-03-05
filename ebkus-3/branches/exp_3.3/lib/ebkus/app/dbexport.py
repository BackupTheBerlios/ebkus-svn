#!/usr/local/bin/python
# coding: latin-1

"""Datenabgleich zwischen verschiedenen Sites

      LEIDER NOCH NICHT GANZ FERTIG, DIE DOKUMENTATION!

      Zweck: Aussenstellen ohne Netzanschluss an die Hauptdatenbank
      können auf diese Weise ihre Daten in die Hauptdatenbank (Masterdb)
      importieren. Die Hauptdatenbank muss dazu die Mitarbeiter und den
      Code regelmässig in die Nebendatenbanken exportieren (mit der ID).

Caveats:

*** Löschungen von Datensätzen werden nicht berücksichtigt! ***

*** Tabellen ohne primären Schlüssel werden nicht behandelt! ***
*** Tabellen zu Dokument und Gruppe werden nicht exportiert ****

*** Korrigierte dbexport.py von Huber 10.03.2002

"""

import sys, time, marshal, os
from ebkus.db.sql import opendb, closedb
from ebkus.app import ebapi
from ebkus.config import config

def dbexport(mit_id):
    opendb()
    site = ebapi.getDBSite()
    site_id = ebapi.cc('dbsite', site)
    export_time = int(time.time())
    export_time_string = time.strftime('%d%m%y-%H%M%S', time.localtime(export_time))
    exportprot = ebapi.Exportprotokoll()
    exportprot.new()
    export_id = exportprot['id']
    this_export_dir = os.path.join(config.INSTANCE_HOME, 'daten', 'export',
                                   'export-%s-%s-%s' %
                                   (site, export_id, export_time_string))
    os.mkdir(this_export_dir,0700)
    
    print "Daten exportieren nach: '%s' ..." % this_export_dir
    
    def dump(klass, dir = this_export_dir, where = '', order = 'id'):
        name = klass.resultClass.table
        # Tabelle aus der Datenbank holen (Tupelliste, *keine* dicts Feldname:Wert)
        table = klass().getTable(where = where, order = order)
        # In eine Datei schreiben
        f = open('%s/%s' % (dir, name), 'wb')
        marshal.dump(table, f)
        f.close()
        
    if site == config.MASTER_SITE:
        dump(ebapi.MitarbeiterList)
        dump(ebapi.CodeList)
    else:
        dump(ebapi.AkteList)
        dump(ebapi.FallList)
        dump(ebapi.BezugspersonList)
        dump(ebapi.EinrichtungskontaktList)
        dump(ebapi.LeistungList)
        dump(ebapi.AnmeldungList)
        dump(ebapi.ZustaendigkeitList)
        dump(ebapi.FachstatistikList)
        dump(ebapi.FachstatistikleistungList)
        dump(ebapi.FachstatistikkindproblemList)
        dump(ebapi.FachstatistikelternproblemList)
        dump(ebapi.JugendhilfestatistikList)
        
    dump(ebapi.ImportprotokollList, where = 'dbsite = %s' % site_id)
    exportprot['dbsite'] = site_id
    exportprot['zeit'] = export_time
    exportprot['mit_id'] = mit_id
    exportprot.insert()
    dump(ebapi.ExportprotokollList, where = 'dbsite = %s' % site_id)
    f = open(os.path.join(this_export_dir, 'export.inf'), 'w')
    f.write("%s\n%s\n%s\n" % (site, str(export_id), str(export_time)))
    f.close()
    print 'Ok'
    
def dbimport(mit_id):
    import_dir = os.path.join(config.INSTANCE_HOME, 'daten', 'import')
    exports = os.listdir(import_dir)
    export_infs = []
    for e in exports:
        dir = os.path.join(import_dir, e)
        try:    f = open(os.path.join(dir, 'export.inf'), 'r')
        except: continue # keine export.inf Datei, also ignorieren
        lines = f.readlines()
        export_infs.append({'mit_id': mit_id, 'dir': dir, 'export_site': lines[0][:-1],
                            'export_id': int(lines[1]), 'export_time': int(lines[2])})
        
    export_infs.sort(lambda x,y: cmp(x['export_time'], y['export_time']))
    for e in export_infs:
        apply(_dbimport, (), e)
        
        
def _dbimport(mit_id, dir, export_site, export_id, export_time):
    print '_dbimport', dir, export_site, export_id
    opendb()
    site = ebapi.getDBSite()
    site_id = ebapi.cc('dbsite', site)
    exp_site = ebapi.cc('dbsite', export_site)
    if site_id == exp_site:
        print "Kein Import von '%s', da selbe Stelle" % dir
        return
    importprot = ebapi.ImportprotokollList(where = "exp_id = %s" % export_id)
    if len(importprot) > 0:
        print "Bereits importiert aus: '%s'" % dir
        return
    print "Daten Importieren aus: '%s' ... " % dir
    
    def load(klass, dir = dir):
        name = klass.resultClass.table
        f = open(os.path.join(dir, name), 'rb')
        table = marshal.load(f)
        klass().updateOrInsertTable(table)
        
    import_time = int(time.time())
    if export_site == config.MASTER_SITE:
        load(ebapi.MitarbeiterList)
        load(ebapi.CodeList)
    else:
        load(ebapi.AkteList)
        load(ebapi.FallList)
        load(ebapi.BezugspersonList)
        load(ebapi.EinrichtungskontaktList)
        load(ebapi.LeistungList)
        load(ebapi.AnmeldungList)
        load(ebapi.ZustaendigkeitList)
        load(ebapi.FachstatistikList)
        load(ebapi.FachstatistikleistungList)
        load(ebapi.FachstatistikkindproblemList)
        load(ebapi.FachstatistikelternproblemList)
        load(ebapi.JugendhilfestatistikList)
        load(ebapi.ImportprotokollList)
    load(ebapi.ExportprotokollList)
    importprot = ebapi.Importprotokoll()
    importprot['exp_id'] = export_id
    importprot['dbsite'] = site_id
    importprot['zeit'] = import_time
    importprot['mit_id'] = mit_id
    importprot.new()
    importprot.insert()
    print 'Ok'
    
def history():
    print "Noch nicht vorhanden"
    print "Siehe aber: im EBkuS Menu 'Stellenabgleich' wählen"
    
if __name__ == '__main__':
    def usage():
        print 'Usage: '
        print '  dbabgleich -l             # Import/Export history anzeigen'
        print '  dbabgleich -i <Benutzer>  # nur importieren'
        print '  dbabgleich -e <Benutzer>  # nur exportieren'
    arg1 = arg2 = None
    try:
        arg1 = sys.argv[1]
        arg2 = sys.argv[2]
    except: pass
    if arg1 == '-l':
        history()
        sys.exit(0)
    if arg2:
        opendb()
        ml = ebapi.MitarbeiterList(where = "ben = '%s'"  % arg2)
        if len(ml) != 1:
            print "Falsche Benutzerkennung: '%s'" % arg2
            sys.exit(1)
        id = ml[0]['id']
        if arg1 == '-i':
            dbimport(id)
            sys.exit(0)
        if arg1 == '-e':
            dbexport(id)
            sys.exit(0)
    usage()
