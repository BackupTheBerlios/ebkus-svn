# coding: latin-1

"""Module für das Anzeigen der Dokumente (im PDF-Format)."""

import string

from ebkus.app import Request

from ebkus.app.ebapi import Fall, Akte, Dokument, Gruppendokument, Code, GruppendokumentList, DokumentList, Gruppe, today, cc, get_akte_path, get_gruppe_path
from ebkus.app.ebapih import get_codes, mksel, mk_columns, mk_text
from ebkus.app_surface.viewdokument_templates import *
from ebkus.app_surface.standard_templates import *
# Package Reportlab
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, cm
from reportlab.lib.pagesizes import A4


class dokview(Request.Request):
    """1 Dokument senden (Tabellen Dokument, Gruppendokument"""
    
    permissions = Request.DOKVIEW_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        mitarbeiterliste = self.getMitarbeiterliste()
        user = self.user
        
        if self.form.has_key('gruppeid'):
            dokid = self.form.get('dokid')
            gruppeid = self.form.get('gruppeid')
            gruppe = Gruppe(gruppeid)
            dok = Gruppendokument(dokid)
            mimetyp = Code(dok['mtyp'])
            try:
                gruppe_path = get_gruppe_path(gruppe['id'])
                f = open('%s/%s'
                         % (gruppe_path, dok['fname']), 'rb')
                datei = f.read()
                f.close()
            except Exception, e:
                meldung = {'titel':'Fehler',
                         'legende':'Fehlerbeschreibung',
                         'zeile1': str(e),
                         'zeile2':'Versuchen Sie es bitte erneut.'}
                return (meldung_t %meldung)
        else:
            fallid = self.form.get('fallid')
            fall = Fall(int(fallid))
            akte = Akte(fall['akte_id'])
            dokid = self.form.get('dokid')
            dok = Dokument(int(dokid))
            mimetyp = Code(dok['mtyp'])
            
            try:
                akte_path = get_akte_path(akte['id'])
                f = open('%s/%s'
                         % (akte_path, dok['fname']), 'rb')
                datei = f.read()
                f.close()
            except Exception, e:
                meldung = {'titel':'Fehler',
                         'legende':'Fehlerbeschreibung',
                         'zeile1': str(e),
                         'zeile2':'Versuchen Sie es bitte erneut.'}
                return (meldung_t %meldung)
                
        if dok['mtyp'] == cc('mimetyp','txt'):
            kopfzeile = '%(vd)d.%(vm)d.%(vy)d: %(art__name)s' % dok
            fuss = '%(mit_id__vn)s %(mit_id__na)s' % dok
            betreff = mk_columns(dok['betr'],70)
            zeilen = string.split(betreff,'\n')
            betr = ''
            for z in zeilen:
                betr = betr + '%s\n' % z
            datei_out = '\n%s.\nBetr.: %s\n%s\n\n%s\n'\
                        % (kopfzeile, betr, datei, fuss)
        else:
            datei_out = datei
            
        if RESPONSE:
            RESPONSE.setHeader('content-type', '%(name)s' % mimetyp)
            RESPONSE.setHeader('filename', dok['fname'])
            RESPONSE.setBody(datei_out)
        else:
            return "Fehler beim Anzeigen des Dokumentes"
            
            
class dokview2(Request.Request):
    """Mehrere Ascii-Texte der Akte zusammenfassen und senden (Tabellen: Dokument, Gruppendokument)"""
    
    permissions = Request.DOKVIEW_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        mitarbeiterliste = self.getMitarbeiterliste()
        user = self.user
        
        if self.form.has_key('gruppeid'):
            gruppeid = self.form.get('gruppeid')
            gruppe = Gruppe(gruppeid)
            dokid = self.form.get('dokid')
            dok = Gruppendokument(dokid)
            titel = 'Auszug vom %(day)d.%(month)d.%(year)d.' % today() + \
                      ' - %s -' % gruppe['gn'] + '\n\n\n'
        else:
            fallid = self.form.get('fallid')
            fall = Fall(int(fallid))
            akte = Akte(fall['akte_id'])
            faelle = akte['faelle']
            faelle.sort('bgy','bgm','bgd')
            titel = 'Auszug vom %(day)d.%(month)d.%(year)d.' % today() + ' - %s -' % fall['fn'] + '\n\n\n'
            
        art = self.form.get('art')
        
        out = ''
        
        # Aktendokumente
        
        if self.form.has_key('fallid'):
            for f in faelle:
                if art == 'bnotiz':
                    dokl = DokumentList(where = 'fall_id = %s and art = %s and mtyp = %s and mit_id = %s' % (f['id'], cc('dokart', 'bnotiz'), cc('mimetyp', 'txt'), self.mitarbeiter['id']), order = 'vy,vm,vd')
                    
                elif art=='anotiz':
                    adokl = DokumentList(where = 'fall_id = %s and mtyp = %s'
                                           % (f['id'], cc('mimetyp', 'txt')), order = 'vy,vm,vd')
                    dokl = []
                    for d in adokl:
                        if d['art'] != cc('dokart', 'bnotiz'):
                            dokl.append(d)
                            
                out = out + mk_text(dokl, get_akte_path(akte['id']))
                
                # Gruppendokumente
                
        elif gruppeid and art == 'bnotiz':
            dokl = GruppendokumentList(where = 'gruppe_id = %s and art = %s and mtyp = %s and mit_id = %s'% (gruppe['id'], cc('dokart', 'bnotiz'), cc('mimetyp', 'txt'), self.mitarbeiter['id']), order = 'vy,vm,vd')
            out = mk_text(dokl, get_gruppe_path(gruppe['id']))
            
        elif gruppeid and art=='anotiz':
            adokl = GruppendokumentList(where = 'gruppe_id = %s and mtyp = %s'
                                   % (gruppe['id'], cc('mimetyp', 'txt')), order = 'vy,vm,vd')
            dokl = []
            for d in adokl:
                if d['art'] != cc('dokart', 'bnotiz'):
                    dokl.append(d)
            out = mk_text(dokl, get_gruppe_path(gruppe['id']))
            
            # Plain-Text-Ausgabe fuer den Browser. Alternativ: print_pdf.py
            
        if out is None or out == '':
            out = 'Kein Ascii-Text vorhanden'
        else:
            out = titel + out
            
            # Datei uebertragen
            
        if RESPONSE:
            RESPONSE.setHeader('content-type', '%s' % 'text/plain')
            RESPONSE.setHeader('filename', 'zusammenfassung.txt')
            RESPONSE.setBody(out)
        else:
            return "Fehler beim Anzeigen des Dokumentes"
            
            #
            # return "Fehler ..." durch Fehlerbehandlung ersetzen.
            #
            
            
            # Layout fuer pdf
top_margin = A4[1] - inch
bottom_margin = inch
left_margin = inch
right_margin = A4[0] - inch
frame_width = right_margin - left_margin


class print_pdf(Request.Request):
    """PDF-Text aus Ascii-Texten erstellen und senden (Tabelle: Dokument.)"""
    
    permissions = Request.DOKVIEW_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        mitarbeiterliste = self.getMitarbeiterliste()
        user = self.user
        
        art = self.form.get('art')
        if self.form.has_key('fallid'):
            fallid = self.form.get('fallid')
            fall = Fall(int(fallid))
            akte = Akte(fall['akte_id'])
            faelle = akte['faelle']
            faelle.sort('bgy','bgm','bgd')
            
            try:
                akte_path = get_akte_path(akte['id'])
            except Exception, e:
                meldung = {'titel':'Fehler',
                         'legende':'Fehlerbeschreibung',
                         'zeile1': str(e),
                         'zeile2':'Versuchen Sie es bitte erneut.'}
                return (meldung_t %meldung)
                
        else:
            meldung = {'titel':'Fehler',
                      'legende':'Fehlerbeschreibung',
                      'zeile1': 'Kein Fall',
                      'zeile2':'Versuchen Sie es bitte erneut.'}
            return (meldung_t %meldung)
            
        if art == 'bnotiz':
            head_l = 'Beraternotizen'
        elif art == 'anotiz':
            head_l = 'Aktenauszug'
        head_m = fall['fn']
        head_r = '%(day)d.%(month)d.%(year)d' % today()
        
        # Seitenlayout
        
        def drawPageFrame(canv, head_links, head_mitte, head_rechts):
            canv.line(left_margin, top_margin, right_margin, top_margin)
            canv.setFont('Helvetica-Oblique',11)
            canv.drawString(left_margin, top_margin + 2, "%s" % head_links + "                                  - %s - " % head_mitte)
            canv.drawString(right_margin - 0.85*inch, top_margin + 2, '%s'
                            % head_rechts)
            canv.line(left_margin, top_margin, right_margin, top_margin)
            canv.line(left_margin, bottom_margin, right_margin, bottom_margin)
            canv.drawCentredString(0.5*A4[0], 0.5 * inch,
                         "- %d -" % canv.getPageNumber())
            
        canv = canvas.Canvas('%s/%s_%s.pdf' % (akte_path, art, akte['id']))
        canv.setPageCompression(0)
        drawPageFrame(canv, head_l, head_m, head_r)
        canv.setAuthor('%(vn) %(na)s' % self.mitarbeiter)
        canv.setTitle('%s - %s -' % (art, fall['fn']))
        
        # Inhaltsverzeichnis
        
        canv.setFont("Helvetica-Bold", 14)
        canv.drawString(left_margin, top_margin - 0.5 * inch, "Inhaltsverzeichnis")
        
        canv.setFont("Helvetica", 11)
        tx = canv.beginText(left_margin, top_margin - 0.9 * inch)
        
        for f in faelle:
            if art == 'bnotiz':
                dokl = DokumentList(where = 'fall_id = %s and art = %s \
                and mit_id = %s' % (f['id'], cc('dokart', 'bnotiz'),
                self.mitarbeiter['id']), order = 'vy,vm,vd')
                
                for d in dokl:
                    zeilen = string.split(mk_columns(d['betr'],55),'\n')
                    tx.textLine("%(vd)s.%(vm)s.%(vy)s:" % d + " %s" % zeilen[0])
                    if len(zeilen) > 1:
                        for z in zeilen[1:]:
                            tx.textLine("                    %s" % z)
                            
            elif art == 'anotiz':
                aktendokl = DokumentList(where = 'fall_id = %s  '
                                       % (f['id']), order = 'vy,vm,vd')
                dokl = []
                print aktendokl
                for d in aktendokl:
                    if d['art'] != cc('dokart', 'bnotiz'):
                        zeilen = string.split(mk_columns(d['betr'],60),'\n')
                        tx.textLine("%(vd)s.%(vm)s.%(vy)s: %(art__name)s" % d )
                        for z in zeilen:
                            tx.textLine("       %s" % z)
        canv.drawText(tx)
        canv.showPage()
        
        # Die einzelnen Textdateien plus Items aus der DB
        
        drawPageFrame(canv, head_l, head_m, head_r)
        canv.setFont("Helvetica", 11)
        tx = canv.beginText(left_margin, top_margin - 0.5*inch)
        
        for f in faelle:
            if art == 'bnotiz':
                dokl = DokumentList(where = 'fall_id = %s and art = %s and mtyp = %s \
                and mit_id = %s'% (f['id'], cc('dokart', 'bnotiz'),
                cc('mimetyp', 'txt'), self.mitarbeiter['id']), order = 'vy,vm,vd')
                
            elif art == 'anotiz':
                aktendokl = DokumentList(where = 'fall_id = %s and mtyp = %s'
                                       % (f['id'], cc('mimetyp', 'txt')),
                                         order = 'vy,vm,vd')
                dokl = []
                for d in aktendokl:
                    if d['art'] != cc('dokart', 'bnotiz'):
                        dokl.append(d)
                        
            for b in dokl:
                try:
                    data = open('%s/%s' % (akte_path, b['fname']), 'r').readlines()
                except Exception, e:
                    meldung = {'titel':'Fehler',
                           'legende':'Fehlerbeschreibung',
                           'zeile1': str(e),
                           'zeile2':'Versuchen Sie es bitte erneut.'}
                    return (meldung_t %meldung)
                zeilen = string.split(mk_columns(d['betr'],70),'\n')
                tx.textLine("%(vd)s.%(vm)s.%(vy)s: %(art__name)s." %b )
                tx.textLine('Betr.: %s' % zeilen[0])
                for z in zeilen[1:]:
                    tx.textLine("      %s" % z)
                tx.textLine('')
                
                lines = data + ['%(mit_id__vn)s %(mit_id__na)s' % b ]
                for line in lines:
                    tx.textLine(line)
                    y = tx.getY()   #get y coordinate
                    if y < bottom_margin + 0.6*inch:
                        canv.drawText(tx)
                        canv.showPage()
                        drawPageFrame(canv,head_l, head_m, head_r)
                        canv.setFont('Helvetica', 11)
                        tx = canv.beginText(left_margin, top_margin - 0.5*inch)
                        
                        #page
                        pg = canv.getPageNumber()
                        if pg % 10 == 0:
                            print 'formatted page %d' % canv.getPageNumber()
                tx.textLine('')
        if tx:
            canv.drawText(tx)
            canv.showPage()
            
        canv.save()
        
        f = open('%s/%s_%s.pdf' % (akte_path, art, akte['id']), 'r')
        datei = f.read()
        f.close()
        try:
            os.remove('%s/%s_%s.pdf' % (akte_path, art, akte['i']))
        except: pass
        
        # Datei uebertragen
        
        if RESPONSE:
            RESPONSE.setHeader('content-type', '%s' % 'application/pdf')
            RESPONSE.setHeader('filename', '%s_%d.pdf' % (art, akte['id']))
            RESPONSE.setBody(datei)
        else:
            meldung = {'titel':'Fehler',
                       'legende':'Fehlerbeschreibung',
                       'zeile1': 'Fehler beim Anzeigen des Dokumentes',
                       'zeile2':'Versuchen Sie es bitte erneut.'}
            return (meldung_t %meldung)
            
class printgr_pdf(Request.Request):
    """PDF-Text aus Ascii-Texten erstellen und senden
    (Tabelle: GruppenDokument)."""
    
    permissions = Request.DOKVIEW_PERM
    
    def processForm(self, REQUEST, RESPONSE):
        mitarbeiterliste = self.getMitarbeiterliste()
        user = self.user
        
        art = self.form.get('art')
        if self.form.has_key('gruppeid'):
            gruppeid = self.form.get('gruppeid')
            gruppe = Gruppe(int(gruppeid))
            dokid = self.form.get('dokid')
            dok = Gruppendokument(dokid)
            
            try:
                gruppe_path = get_gruppe_path(gruppe['id'])
            except Exception, e:
                meldung = {'titel':'Fehler',
                         'legende':'Fehlerbeschreibung',
                         'zeile1': str(e),
                         'zeile2':'Versuchen Sie es bitte erneut.'}
                return (meldung_t %meldung)
        if art == 'bnotiz':
            head_l = 'Beraternotizen'
        elif art == 'anotiz':
            head_l = 'Gruppenakte'
        head_m = gruppe['gn']
        head_r = '%(day)d.%(month)d.%(year)d' % today()
        
        # Seitenlayout
        
        def drawPageFrame(canv, head_links, head_mitte, head_rechts):
            canv.line(left_margin, top_margin, right_margin, top_margin)
            canv.setFont('Helvetica-Oblique',11)
            canv.drawString(left_margin, top_margin + 2, "%s" % head_links + "                                  - %s - " % head_mitte)
            canv.drawString(right_margin - 0.85*inch, top_margin + 2, '%s'
                            % head_rechts)
            canv.line(left_margin, top_margin, right_margin, top_margin)
            canv.line(left_margin, bottom_margin, right_margin, bottom_margin)
            canv.drawCentredString(0.5*A4[0], 0.5 * inch,
                         "- %d -" % canv.getPageNumber())
            
        canv = canvas.Canvas('%s/%s_%s.pdf' % (gruppe_path, art, gruppe['id']))
        canv.setPageCompression(0)
        drawPageFrame(canv, head_l, head_m, head_r)
        canv.setAuthor('%(vn) %(na)s' % self.mitarbeiter)
        canv.setTitle('%s - %s -' % (art, gruppe['gn']))
        
        # Inhaltsverzeichnis
        
        canv.setFont("Helvetica-Bold", 14)
        canv.drawString(left_margin, top_margin - 0.5 * inch, "Inhaltsverzeichnis")
        
        canv.setFont("Helvetica", 11)
        tx = canv.beginText(left_margin, top_margin - 0.9 * inch)
        
        if art == 'bnotiz':
            dokl = GruppendokumentList(where = 'gruppe_id = %s and art = %s \
            and mit_id = %s' % (gruppe['id'], cc('dokart', 'bnotiz'),
            self.mitarbeiter['id']), order = 'vy,vm,vd')
            
            for d in dokl:
                zeilen = string.split(mk_columns(d['betr'],55),'\n')
                tx.textLine("%(vd)s.%(vm)s.%(vy)s:" % d + " %s" % zeilen[0])
                if len(zeilen) > 1:
                    for z in zeilen[1:]:
                        tx.textLine("                    %s" % z)
                        
        elif art == 'anotiz':
            aktendokl = GruppendokumentList(where = 'gruppe_id = %s  '
                                   % (gruppe['id']), order = 'vy,vm,vd')
            dokl = []
            print aktendokl
            for d in aktendokl:
                if d['art'] != cc('dokart', 'bnotiz'):
                    zeilen = string.split(mk_columns(d['betr'],60),'\n')
                    tx.textLine("%(vd)s.%(vm)s.%(vy)s: %(art__name)s" % d )
                    for z in zeilen:
                        tx.textLine("       %s" % z)
        canv.drawText(tx)
        canv.showPage()
        
        
        # Die einzelnen Textdateien plus Items aus der DB
        
        
        drawPageFrame(canv, head_l, head_m, head_r)
        canv.setFont("Helvetica", 11)
        tx = canv.beginText(left_margin, top_margin - 0.5*inch)
        
        if art == 'bnotiz':
            dokl = GruppendokumentList(where = 'gruppe_id = %s and art = %s and mtyp = %s \
            and mit_id = %s'% (gruppe['id'], cc('dokart', 'bnotiz'),
            cc('mimetyp', 'txt'), self.mitarbeiter['id']), order = 'vy,vm,vd')
            
        elif art == 'anotiz':
            aktendokl = GruppendokumentList(where = 'gruppe_id = %s and mtyp = %s'
                                   % (gruppe['id'], cc('mimetyp', 'txt')),
                                     order = 'vy,vm,vd')
            dokl = []
            for d in aktendokl:
                if d['art'] != cc('dokart', 'bnotiz'):
                    dokl.append(d)
                    
        for b in dokl:
            try:
                data = open('%s/%s' % (gruppe_path, b['fname']), 'r').readlines()
            except Exception, e:
                meldung = {'titel':'Fehler',
                         'legende':'Fehlerbeschreibung',
                         'zeile1': str(e),
                         'zeile2':'Versuchen Sie es bitte erneut.'}
                return (meldung_t %meldung)
                
            zeilen = string.split(mk_columns(d['betr'],70),'\n')
            tx.textLine("%(vd)s.%(vm)s.%(vy)s: %(art__name)s." % b )
            tx.textLine('Betr.: %s' % zeilen[0])
            for z in zeilen[1:]:
                tx.textLine("      %s" % z)
            tx.textLine('')
            
            lines = data + ['%(mit_id__vn)s %(mit_id__na)s' % b ]
            for line in lines:
                tx.textLine(line)
                y = tx.getY()   #get y coordinate
                if y < bottom_margin + 0.6*inch:
                    canv.drawText(tx)
                    canv.showPage()
                    drawPageFrame(canv,head_l, head_m, head_r)
                    canv.setFont('Helvetica', 11)
                    tx = canv.beginText(left_margin, top_margin - 0.5*inch)
                    
                    #page
                    pg = canv.getPageNumber()
                    if pg % 10 == 0:
                        print 'formatted page %d' % canv.getPageNumber()
            tx.textLine('')
        if tx:
            canv.drawText(tx)
            canv.showPage()
            
        canv.save()
        
        f = open('%s/%s_%s.pdf' % (gruppe_path, art, gruppe['id']), 'r')
        datei = f.read()
        f.close()
        try:
            os.remove('%s/%s_%s.pdf' % (gruppe_path, art, gruppe['i']))
        except: pass
        
        # Datei uebertragen
        
        if RESPONSE:
            RESPONSE.setHeader('content-type', '%s' % 'application/pdf')
            RESPONSE.setHeader('filename', '%s_%d.pdf' % (art, gruppe['id']))
            RESPONSE.setBody(datei)
        else:
            meldung = {'titel':'Fehler',
                       'legende':'Fehlerbeschreibung',
                       'zeile1': 'Fehler beim Anzeigen des Dokumentes',
                       'zeile2':'Versuchen Sie es bitte erneut.'}
            return (meldung_t %meldung)
            
class suchetxt(Request.Request):
    """Suche Text (Expression) im Ascii-Text
    (Tabelle: Dokument, Gruppendokument)."""
    
    permissions = Request.DOKVIEW_PERM
    def processForm(self, REQUEST, RESPONSE):
        import os
        popen = os.popen
        
        akte = None
        print "***************************"
        print self.form.has_key('fallid')
        
        mitarbeiterliste = self.getMitarbeiterliste()
        user = self.user
        if self.form.has_key('expr'):
            expr = self.form.get('expr')
        else:
            self.last_error_message = "Kein Suchaudruck erhalten"
            return self.EBKuSError(REQUEST, RESPONSE)
            
        string.strip(expr)
        if len(expr) > 2:
            pass
        else:
            meldung = {'titel':'Fehler',
                       'legende':'Fehlerbeschreibung',
                       'zeile1': 'Der Suchausdruck sollte mind. 3 Buchstaben haben',
                       'zeile2':'Versuchen Sie es bitte erneut.'}
            return (meldung_t %meldung)
            
        if self.form.has_key('gruppeid'):
            gruppeid = self.form.get('gruppeid')
            gruppe = Gruppe(int(gruppeid))
            
            try:
                gruppe_path = get_gruppe_path(gruppe['id'])
                cwd = os.getcwd()
                os.chdir('%s' % gruppe_path)
                fd = popen('agrep -n -i %s *.txt ' % expr)
                ergebnis = fd.readlines()
                fd.close()
                os.chdir(cwd)
            except Exception, e:
                meldung = {'titel':'Fehler',
                         'legende':'Fehlerbeschreibung',
                         'zeile1': str(e),
                         'zeile2':'Versuchen Sie es bitte erneut.'}
                return (meldung_t %meldung)
                
            menue = menuegruppe_t % gruppe
            header = ("Suchergebnis in den Texten der Gruppe &quot;%(name)s&quot; " % gruppe)
            formhiddenv = formhiddennamevalues_t % ({'name' : 'gruppeid' ,
                                                     'value' : gruppeid})
            
        elif self.form.has_key('fallid'):
            fallid = self.form.get('fallid')
            fall = Fall(fallid)
            akte = Akte(fall['akte_id'])
            letzter_fall = akte['letzter_fall']
            aktueller_fall = akte['aktueller_fall']
            
            try:
                akte_path = get_akte_path(akte['id'])
                cwd = os.getcwd()
                os.chdir('%s' % akte_path)
                print "************* VOR POPEN *******************"
                fd = popen('agrep -n -i %s *.txt /dev/null' % expr)
                print "************* NACH POPEN ******************"
                print fd.readlines()
                ergebnis = fd.readlines()
                fd.close()
                os.chdir(cwd)
            except Exception, e:
                meldung = {'titel':'Fehler',
                         'legende':'Fehlerbeschreibung',
                         'zeile1': str(e),
                         'zeile2':'Versuchen Sie es bitte erneut.'}
                return (meldung_t %meldung)
                
            if aktueller_fall:
                formhiddenv = formhiddennamevalues_t % ({'name' : 'fallid' ,
                                                    'value' : aktueller_fall['id']})
            else:
                formhiddenv = formhiddennamevalues_t % ({'name' : 'fallid' ,
                                                    'value' : letzter_fall['id']})
                
        res = []
        #res.append(head_normal_t %("Suchergebnis in der Akte &quot;%(vn)s %(na)s&quot; " % akte))
        res.append(formkopfv_t % 'suchetxt')
        res.append(formhiddenv)
        res.append(dokausgabe7_t % ('Suche in den Texten', expr))
        res.append(dokausgabe1_t % 'Suchergebnis')
        
        if not ergebnis:
            res.append('Kein Ergebnis.')
        else:
            n = 0
            datei = []
            for line in ergebnis:
                i = string.index(line,'.txt')
                datei.append(line[:i])
                if self.form.has_key('gruppeid'):
                    if n == 0:
                        dok = Gruppendokument(line[:i])
                        res.append(dokausgabe2b_t % dok)
                    if datei[n] != datei[n-1]:
                        dok = Gruppendokument(line[:i])
                        res.append(dokausgabe2b_t % dok)
                    res.append(dokausgabe8_t % line[i+5:])
                    n = n + 1
                    
                elif self.form.has_key('fallid'):
                    if n == 0:
                        dok = Dokument(line[:i])
                        res.append(dokausgabe2_t % dok)
                    if datei[n] != datei[n-1]:
                        dok = Dokument(line[:i])
                        res.append(dokausgabe2_t % dok)
                    res.append(dokausgabe8_t % line[i+5:])
                    n = n + 1
        res.append(dokausgabe3_t)
        return string.join(res, '')
        
        
        
