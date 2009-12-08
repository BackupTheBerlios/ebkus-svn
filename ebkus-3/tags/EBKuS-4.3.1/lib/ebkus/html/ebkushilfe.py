# coding: latin-1
## Standardimporte
import string

## EBKuS - Importe
from ebkus.app import Request
from ebkus.app_surface.ebkushilfe_templates import *
from ebkus.app_surface.ebkushilfe_texte import *
from ebkus.app_surface.standard_templates import *

##***************************************************************************
## Projekt:     Kobit/EBKuS-neu
## Datei:       ebkus/html/ebkushilfe.py
##
## Beschreibung: Klasse zum Aufruf des Hilfeframesets
##
## Basisklasse: Request
##
## Typen:       -
##
## Klassenname: ebkus_help
## Klassenart:  Klasse für die EBKuS - Onlinehilfe
##
##---------------------------------------------------------------------------
##
## REVISIONEN:
##
## DATUM        AUTOR           BESCHREIBUNG
## 21.12.2001   MastaleckT(msg)    Ersterstellung
##***************************************************************************

class ebkus_help(Request.Request):
    permissions = Request.ALL
    def processForm(self, REQUEST, RESPONSE):
        res = []
        if self.form.has_key('help_id'):
            help_id = self.form.get('help_id')
            res.append(help_frameset_t %help_id)
        else:
            res.append(help_frameset_t %('no_content'))
        return string.join(res, '')
        
        ##***************************************************************************
        ## Projekt:     Kobit/EBKuS-neu
        ## Datei:       ebkus/html/ebkushilfe.py
        ##
        ## Beschreibung: Klasse zur Darstellung und Auswahl des betreffenden
        ##               Hilfe - Dokumentes
        ##
        ## Basisklasse: Request
        ##
        ## Typen:       -
        ##
        ## Klassenname: ebkus_help_document
        ## Klassenart:  Klasse für die EBKuS - Onlinehilfe
        ##
        ##---------------------------------------------------------------------------
        ##
        ## REVISIONEN:
        ##
        ## DATUM        AUTOR           BESCHREIBUNG
        ## 21.12.2001   MastaleckT(msg)    Ersterstellung
        ##***************************************************************************
        
class ebkus_help_document(Request.Request):
    permissions = Request.ALL
    def processForm(self, REQUEST, RESPONSE):
        res = []
        if self.form.has_key('help_id'):
            help_id = self.form.get('help_id')
        else:
            res.append(help_document_start_t)
            res.append(help_document_text_t %("Kein passendes Hilfethema gefunden"))
            res.append(help_document_end_t)
            return string.join(res, '')
        res.append(help_document_start_t)
        if help_id=='start_seite':
            res.append(help_document_text_t %(ht_start_seite_t))
        elif help_id=='Bedienungsanleitung':
            res.append(help_document_theme_t %("Das Hauptmen&uuml;"))
            res.append(help_document_text_t %('Dieser Abschnitt beinhaltet die Online-Hilfe zum Thema: Hauptmen&uuml;'))
        elif help_id=='Klientenakte':
            res.append(help_document_theme_t %("Die Klientenakte"))
            res.append(help_document_text_t %('Dieser Abschnitt beinhaltet die Online-Hilfe zum Thema: Klientenakte'))
        elif help_id=='Bezugspersonen':
            res.append(help_document_theme_t %("Die Bezugspersonen"))
            res.append(help_document_text_t %('Dieser Abschnitt beinhaltet die Online-Hilfe zum Thema: Bezugspersonen'))
        elif help_id=='Leistungen':
            res.append(help_document_theme_t %("Die Leistungen"))
            res.append(help_document_text_t %('Dieser Abschnitt beinhaltet die Online-Hilfe zum Thema: Leistungen'))
        elif help_id=='Zustaendigkeit':
            res.append(help_document_theme_t %("Die Zust&auml;ndigkeit"))
            res.append(help_document_text_t %('Dieser Abschnitt beinhaltet die Online-Hilfe zum Thema: Zust&auml;ndigkeit'))
        elif help_id=='Statistik':
            res.append(help_document_theme_t %("Die Statistiken"))
            res.append(help_document_text_t %('Dieser Abschnitt beinhaltet die Online-Hilfe zum Thema: Statistiken'))
        elif help_id=='Kontakte':
            res.append(help_document_theme_t %("Die Kontakte"))
            res.append(help_document_text_t %('Dieser Abschnitt beinhaltet die Online-Hilfe zum Thema: Kontakte'))
        elif help_id=='Gruppen':
            res.append(help_document_theme_t %("Die Gruppen"))
            res.append(help_document_text_t %('Dieser Abschnitt beinhaltet die Online-Hilfe zum Thema: Gruppen'))
        elif help_id=='Abfragen':
            res.append(help_document_theme_t %("Die Abfragen"))
            res.append(help_document_text_t %('Dieser Abschnitt beinhaltet die Online-Hilfe zum Thema: Abfragen'))
        elif help_id[:8]=='Hauptmen':
            res.append(help_document_theme_t %("Das Hauptmen&uuml;"))
            res.append(help_document_grafix_t %("hauptmenu.gif"))
            res.append(help_document_text_t %(ht_hauptmenu_t))
        elif help_id=='Klientenkarte':
            res.append(help_document_theme_t %("Die Klientenkarte"))
            res.append(help_document_grafix_t %("klientenkarte.gif"))
            res.append(help_document_text_t %(ht_klientenkarte_t))
        elif help_id=='Neue_Akte_anlegen':
            res.append(help_document_theme_t %("Neue Akte anlegen"))
            res.append(help_document_grafix_t %("neue_akte_anlegen.gif"))
            res.append(help_document_text_t %(ht_neue_akte_anlegen_t))
        elif help_id=='Akte_aktualisieren':
            res.append(help_document_theme_t %("Akte aktualisieren"))
            res.append(help_document_grafix_t %("akte_aktualisieren.gif"))
            res.append(help_document_text_t %(ht_akte_aktualisieren_t))
        elif help_id=='Neue_Person_eintragen':
            res.append(help_document_theme_t %("Neue Bezugsperson eintragen"))
            res.append(help_document_grafix_t %("bezugsperson_eintragen.gif"))
            res.append(help_document_text_t %(ht_bezugsperson_eintragen_t))
        elif help_id=='Bezugsperson_bearbeiten':
            res.append(help_document_theme_t %("Bezugsperson aktualisieren"))
            res.append(help_document_grafix_t %("bezugsperson_aktualisieren.gif"))
            res.append(help_document_text_t %(ht_bezugsperson_aktualisieren_t))
        elif help_id=='Neue_Leistung_eintragen':
            res.append(help_document_theme_t %("Neue Leistung eintragen"))
            res.append(help_document_grafix_t %("leistung.gif"))
            res.append(help_document_text_t %(ht_neue_leistung_eintragen_t))
        elif help_id=='Leistung_bearbeiten':
            res.append(help_document_theme_t %("Leistung bearbeiten"))
            res.append(help_document_grafix_t %("leistung.gif"))
            res.append(help_document_text_t %(ht_leistung_bearbeiten_t))
            #elif help_id=='Neue_Zuständigkeit_eintragen':
        elif help_id[:9]=='Neue_Zust':
            res.append(help_document_theme_t %("Zust&auml;ndigkeit eintragen"))
            res.append(help_document_grafix_t %("zustaendigkeit.gif"))
            res.append(help_document_text_t %(ht_zustaendigkeit_eintragen_t))
            #elif help_id=='Eintrag_zur_Zuständigkeit_bearbeiten':
        elif help_id[:16]=='Eintrag_zur_Zust':
            res.append(help_document_theme_t %("Zust&auml;ndigkeit bearbeiten"))
            res.append(help_document_grafix_t %("zustaendigkeit.gif"))
            res.append(help_document_text_t %(ht_zustaendigkeit_bearbeiten_t))
        elif help_id=='Gruppenkartei':
            res.append(help_document_theme_t %("Gruppenmen&uuml;"))
            res.append(help_document_grafix_t %("gruppenkartei.gif"))
            res.append(help_document_text_t %(ht_gruppenkartei_t))
        elif help_id=='Neue_Gruppe_erstellen':
            res.append(help_document_theme_t %("Neue Gruppe erstellen"))
            res.append(help_document_grafix_t %("neue_gruppe_erstellen.gif"))
            res.append(help_document_text_t %(ht_neue_gruppen_erstellen_t))
        elif help_id=='Gruppe_bearbeiten':
            res.append(help_document_theme_t %("Gruppe bearbeiten"))
            res.append(help_document_grafix_t %("gruppe_bearbeiten.gif"))
            res.append(help_document_text_t %(ht_gruppe_bearbeiten_t))
        elif help_id=='Teilnehmerauswahl_aus_der_Klientenkartei':
            res.append(help_document_theme_t %("Gruppenteilnehmer hinzuf&uuml;gen"))
            res.append(help_document_grafix_t %("grp_teilnehm_neu.gif"))
            res.append(help_document_text_t %(ht_grp_teilnehm_neu_t))
            #elif help_id=='Datum_des_Gruppenteilnehmers_ändern':
        elif help_id[:28]=='Datum_des_Gruppenteilnehmers':
            res.append(help_document_theme_t %("Gruppenteilnehmer bearbeiten"))
            res.append(help_document_grafix_t %("grp_teilnehm_bearb.gif"))
            res.append(help_document_text_t %(ht_grp_teilnehm_bearb_t))
            #elif help_id=='Teilnehmer_der_Gruppe_löschen':
        elif help_id[:21]=='Teilnehmer_der_Gruppe':
            res.append(help_document_theme_t %("Gruppenteilnehmer l&ouml;schen"))
            res.append(help_document_grafix_t %("grp_teilnehm_del.gif"))
            res.append(help_document_text_t %(ht_grp_teilnehm_del_t))
        elif help_id=='Dokumentenindex_der_Gruppe' or help_id=='Dokumentenindex_der_Akte':
            res.append(help_document_theme_t %("Dokumentenindex"))
            res.append(help_document_grafix_t %("dokumentenindex.gif"))
            res.append(help_document_text_t %(ht_dokumentenindex_t))
        elif help_id=='Wordauswahl':
            res.append(help_document_theme_t %("Die Word-Exportfunktion"))
            res.append(help_document_grafix_t %("wordexport.gif"))
            res.append(help_document_text_t %(ht_word_export_t))
        elif help_id=='Datei_in_die_Akte_aufnehmen' or help_id=='Datei_zur_Gruppe_importieren':
            res.append(help_document_theme_t %("Importieren von Dateien"))
            res.append(help_document_grafix_t %("dateiimport.gif"))
            res.append(help_document_text_t %(ht_dateiimport_t))
            #elif help_id=='Neuen_Texteintrag_zur_Gruppe_hinzufügen' or help_id=='Neuen_Texteintrag_zur_Akte_hinzufügen':
        elif help_id[:35]=='Neuen_Texteintrag_zur_Gruppe_hinzuf' or help_id[:33]=='Neuen_Texteintrag_zur_Akte_hinzuf':
            res.append(help_document_theme_t %("Neuer Texteintrag"))
            res.append(help_document_grafix_t %("texteintrag_neu.gif"))
            res.append(help_document_text_t %(ht_texteintrag_neu_t))
            #elif help_id=='Texteintrag_der_Akte_zum_Ändern_auswählen' or                                                            #      help_id=='Texteintrag_der_Gruppe_zum_Ändern_ausw&auml;hlen':
        elif help_id[:24]=='Texteintrag_der_Akte_zum' or help_id[:26]=='Texteintrag_der_Gruppe_zum':
            res.append(help_document_theme_t %("Texteintrag ausw&auml;hlen"))
            res.append(help_document_grafix_t %("texteintrag_ausw.gif"))
            res.append(help_document_text_t %(ht_texteintrag_ausw_t))
            #elif help_id=='Texteintrag_der_Gruppe_ändern' or help_id=='Texteintrag_der_Akte_ändern':
        elif help_id[:22]=='Texteintrag_der_Gruppe' or help_id[:20]=='Texteintrag_der_Akte':
            res.append(help_document_theme_t %("Texteintrag bearbeiten"))
            res.append(help_document_grafix_t %("texteintrag_bearb.gif"))
            res.append(help_document_text_t %(ht_texteintrag_bearb_t))
            #elif help_id=='Dokumente_und_Texteinträge_der_Akte_löschen' or                                                          #      help_id=='Dokumente_und_Texteinträge_der_Gruppe_löschen':
        elif help_id[:23]=='Dokumente_und_Texteintr':
            res.append(help_document_theme_t %("Dokumente l&ouml;schen"))
            res.append(help_document_grafix_t %("texteintrag_ausw.gif"))
            res.append(help_document_text_t %(ht_texteintrag_loesch_t))
        elif help_id=='Aenderung_des_Benutzerpasswortes':
            res.append(help_document_theme_t %("Passwort&auml;nderung"))
            res.append(help_document_grafix_t %("pass_change.gif"))
            res.append(help_document_text_t %(ht_pass_change_t))
        elif help_id=='Neue_Fachstatistik_erstellen':
            res.append(help_document_theme_t %('Neue Fachstatistik'))
            res.append(help_document_grafix_t %("fachstatistik.gif"))
            res.append(help_document_text_t %(ht_neue_fachstat_eintragen_t))
            #elif help_id=='Fachstatistik_ändern':
        elif help_id[:14]=='Fachstatistik_':
            res.append(help_document_theme_t %('Fachstatistik bearbeiten'))
            res.append(help_document_grafix_t %("fachstatistik.gif"))
            res.append(help_document_text_t %(ht_fachstat_bearbeiten_t))
        elif help_id=='Neue_Bundesstatistik_erstellen':
            res.append(help_document_theme_t %('Neue Bundesstatistik'))
            res.append(help_document_grafix_t %("bundesstatistik.gif"))
            res.append(help_document_text_t %(ht_neue_bundesstat_eintragen_t))
            #elif help_id=='Bundesstatistik_ändern':
        elif help_id[:16]=='Bundesstatistik_':
            res.append(help_document_theme_t %('Bundesstatistik bearbeiten'))
            res.append(help_document_grafix_t %("bundesstatistik.gif"))
            res.append(help_document_text_t %(ht_fachstat_bearbeiten_t))
        elif help_id=='Neue_Anmeldeinformation_eintragen':
            res.append(help_document_theme_t %('Neuen Anmeldungskontakt'))
            res.append(help_document_grafix_t %("anmeldekontakt.gif"))
            res.append(help_document_text_t %(ht_neuen_anmeldekontakt_eintragen_t))
            #elif help_id=='Anmeldeinformation_ändern':
        elif help_id[:19]=='Anmeldeinformation_':
            res.append(help_document_theme_t %('Anmeldekontakt bearbeiten'))
            res.append(help_document_grafix_t %("anmeldekontakt.gif"))
            res.append(help_document_text_t %(ht_anmeldekontakt_bearbeiten_t))
        elif help_id=='Neuen_Einrichtungskontakt_eintragen':
            res.append(help_document_theme_t %('Neuen Einrichtungskontakt hinzuf&uuml;gen'))
            res.append(help_document_grafix_t %("einrichtungskontakt.gif"))
            res.append(help_document_text_t %(ht_neuen_einrichtungskontakt_eintragen_t))
            #elif help_id=='Einrichtungskontakt_ändern':
        elif help_id[:20]=='Einrichtungskontakt_':
            res.append(help_document_theme_t %('Einrichtungskontakt bearbeiten'))
            res.append(help_document_grafix_t %("einrichtungskontakt.gif"))
            res.append(help_document_text_t %(ht_einrichtungskontakt_bearbeiten_t))
            
            ##*************************************************************************
            ##  Statistische Abfragen
            ##*************************************************************************
        elif help_id=='Statistische_Abfragen':
            res.append(help_document_theme_t %("Statistische Abfragen"))
            res.append(help_document_text_t %(ht_statistische_abfragen_t))
        elif help_id=='Alle_Beratungen':
            res.append(help_document_theme_t %("Abfrage:<br><b>Alle Beratungen</b>"))
            res.append(help_document_grafix_t %("recordlist.gif"))
            res.append(help_document_text_t %(ht_alle_beratungen_t))
        elif help_id=='Laufende_Beratungen':
            res.append(help_document_theme_t %("Abfrage:<br><b>Laufende Beratungen</b>"))
            res.append(help_document_grafix_t %("recordlist.gif"))
            res.append(help_document_text_t %(ht_laufende_beratungen_t))
        elif help_id=='Abgeschlossene_Beratungen':
            res.append(help_document_theme_t %("Abfrage:<br><b>Abgeschlossene Beratungen</b>"))
            res.append(help_document_grafix_t %("recordlist.gif"))
            res.append(help_document_text_t %(ht_abgeschlossene_beratungen_t))
        elif help_id=='Suche_alle_Beratungen_ab_Fallnummer' or help_id=='Alle_Beratungen_ab_Fallnummer':
            res.append(help_document_theme_t %("Abfrage:<br><b>Beratungen ab Fallnummer</b>"))
            res.append(help_document_grafix_t %("sucheabfallnr.gif"))
            res.append(help_document_text_t %(ht_beratungen_abfallnummer_t))
            res.append(help_document_theme_t %("Abfrageergebnis:"))
            res.append(help_document_grafix_t %("sucheabfallnr2.gif"))
            res.append(help_document_text_t %(ht_beratungen_abfallnummer2_t))
        elif help_id=='Bundesstatistikabfrage' or help_id=='Bundesstatistikauswertung':
            res.append(help_document_theme_t %("Abfrage:<br><b>Bundesstatistik</b>"))
            res.append(help_document_grafix_t %("bundesstatistikabfrage.gif"))
            res.append(help_document_text_t %(ht_bundesstatistikabfrage_t))
            res.append(help_document_theme_t %("Abfrageergebnis:"))
            res.append(help_document_grafix_t %("bundesstatistikergebnis.gif"))
            res.append(help_document_text_t %(ht_bundesstatistikergebnis_t))
        elif help_id=='Fachstatistikabfrage' or help_id=='Fachstatistikergebnisse':
            res.append(help_document_theme_t %("Abfrage:<br><b>Fachstatistik</b>"))
            res.append(help_document_grafix_t %("bundesstatistikabfrage.gif"))
            res.append(help_document_text_t %(ht_fachstatistikabfrage_t))
            res.append(help_document_theme_t %("Abfrageergebnis:"))
            res.append(help_document_grafix_t %("bundesstatistikergebnis.gif"))
            res.append(help_document_text_t %(ht_fachstatistikergebnis_t))
        elif help_id=='Statistikabfrage:_Kategoriewahl' or \
        help_id=='Statistikabfrage:_Auswahl_von_Items_aus_1_Kategorie':
            res.append(help_document_theme_t %("Abfrage:<br><b>Kategorieabfrage</b>"))
            res.append(help_document_grafix_t %("kat_auswahl.gif"))
            res.append(help_document_text_t %(ht_abfrage_katauswahl_single_t))
            res.append(help_document_theme_t %("Auswahl der Kategorie-Items"))
            res.append(help_document_grafix_t %("kat_auswahl2.gif"))
            res.append(help_document_text_t %(ht_abfrage_katauswahl_single_2_t))
            res.append(help_document_theme_t %("Abfrageergebnis:"))
            res.append(help_document_grafix_t %("kat_ergebnis.gif"))
            res.append(help_document_text_t %(ht_abfrage_katauswahl_single_3_t))
        elif help_id=='Statistikabfrage:_Kategorienwahl' or \
        help_id=='Statistikabfage:_Itemwahl_aus_mehreren_Kategorien':
            res.append(help_document_theme_t %("Abfrage:<br><b>Kategorienabfrage</b>"))
            res.append(help_document_grafix_t %("kat_auswahl.gif"))
            res.append(help_document_text_t %(ht_abfrage_katauswahl_multi_t))
            res.append(help_document_theme_t %("Auswahl der Kategorie-Items"))
            res.append(help_document_grafix_t %("kat_auswahl2b.gif"))
            res.append(help_document_text_t %(ht_abfrage_katauswahl_multi_2_t))
            res.append(help_document_theme_t %("Abfrageergebnis:"))
            res.append(help_document_grafix_t %("kat_ergebnis.gif"))
            res.append(help_document_text_t %(ht_abfrage_katauswahl_multi_3_t))
            #elif help_id=='Auswahl_Konsultationsanzahl_und_Zeitraum_für_alle_Personen' or \
            #  help_id=='Anzahl_abgeschl._Fälle_-_gleiche_Konsultationsanzahl':
        elif help_id=='Auswahl_Konsultationsanzahl_und_Zeitraum_für_alle_Personen' or \
          help_id=='Anzahl_abgeschl._Faelle_-_gleiche_Konsultationsanzahl':
            res.append(help_document_theme_t %("Abfrage:<br><b>Konsultationszahl</b>"))
            res.append(help_document_grafix_t %("jahresauswahl.gif"))
            res.append(help_document_text_t %(ht_konsultationszahl_t))
            res.append(help_document_theme_t %("Abfrageergebnis:"))
            res.append(help_document_grafix_t %("konsultationszahl_erg.gif"))
            res.append(help_document_text_t %(ht_konsultationszahl_ergebnis_t))
        elif help_id=='Anzahl_abgeschl._Faelle_-_gleiche_Konsultationssumme':
            res.append(help_document_theme_t %("Abfrage:<br><b>Konsultationsumme</b>"))
            res.append(help_document_grafix_t %("jahresauswahl.gif"))
            res.append(help_document_text_t %(ht_konsultationssumme_t))
            res.append(help_document_theme_t %("Abfrageergebnis:"))
            res.append(help_document_grafix_t %("ergebniskonsultationssumme.gif"))
            res.append(help_document_text_t %(ht_konsultationssumme2_t))
        elif help_id=='Auswahl_des_gewuenschten_Zeitraumes_und_die_Laenge_der_Beratungszeit_in_Monaten' or \
          help_id=='Anzahl_der_abgeschl._Faelle_mit_gleichlanger_Beratungsdauer':
            res.append(help_document_theme_t %("Abfrage:<br><b>Beratungsdauer</b>"))
            res.append(help_document_grafix_t %("jahresauswahl.gif"))
            res.append(help_document_text_t %(ht_beratungsdauer_t))
            res.append(help_document_theme_t %("Abfrageergebnis:"))
            res.append(help_document_grafix_t %("beratungsdauer2.gif"))
            res.append(help_document_text_t %(ht_beratungsdauer2_t))
        elif help_id=='Auswahl_des_gewuenschten_Zeitraumes_und_Auswahl_einer_Leistung' or \
          help_id=='Anzahl_der_abgeschl._Faelle_mit_gleicher_Beratungsdauer_zu_einer_bestimmten_Leistung':
            res.append(help_document_theme_t %("Abfrage:<br><b>Beratungsdauer zu einer best. Leistung</b>"))
            res.append(help_document_grafix_t %("beratungsdauer_leist.gif"))
            res.append(help_document_text_t %(ht_beratungsdauer_leistung_t))
            res.append(help_document_theme_t %("Abfrageergebnis:"))
            res.append(help_document_grafix_t %("beratungsdauer_leist2.gif"))
            res.append(help_document_text_t %(ht_beratungsdauer_leistung2_t))
            ##     elif help_id=='Anzahl_der_abgeschl._Faelle_-_Unterscheidung_nach_Haupt-_bzw._Geschwisterfall':
            ##       res.append(help_document_theme_t %("Abfrage:<br><b>Abgeschl. F&auml;lle Haupt- bzw. Geschwisterfall</b>"))
            ##       res.append(help_document_grafix_t %("abgeschlhauptgeschw.gif"))
            ##       res.append(help_document_text_t %(ht_haupt_geschwisterfaelle_t))
        elif help_id=='Anzahl_abgeschl._Faelle_-_Mutter_oder_Vater_Merkmal_x_gleich' or \
          help_id=='Anzahl_der_abgeschl._Faelle_-_Mutter_oder_Vater_haben_das_Merkmal_x':
            res.append(help_document_theme_t %("Abfrage:<br><b>Abgeschl. F&auml;lle - Mutter o. Vater Merkmal x gleich</b>"))
            res.append(help_document_grafix_t %("jahresauswahl.gif"))
            res.append(help_document_text_t %(ht_elternteil_merkmalx_t))
            res.append(help_document_theme_t %("Abfrageergebnis:"))
            res.append(help_document_grafix_t %("ergebniselternteilxgleich.gif"))
            res.append(help_document_text_t %(ht_elternteil_merkmalx2_t))
        elif help_id=='Anzahl_abgeschl._Faelle_-_Mutter_und_Vater_haben_das_gleiche_Merkmal_x':
            res.append(help_document_theme_t %("Abfrage:<br><b>Abgeschl. F&auml;lle - Mutter u. Vater Merkmal x gleich</b>"))
            res.append(help_document_grafix_t %("jahresauswahl.gif"))
            res.append(help_document_text_t %(ht_eltern_merkmalx_t))
            res.append(help_document_theme_t %("Abfrageergebnis:"))
            res.append(help_document_grafix_t %("ergebniselternxgleich.gif"))
            res.append(help_document_text_t %(ht_eltern_merkmalx2_t))
        elif help_id=='Auswahl_des_Zeitraumes_für_die_Gruppenuebersicht' or help_id=='Gruppenüberblick':
            res.append(help_document_theme_t %("Abfrage:<br><b>Gruppen&uuml;bersicht</b>"))
            res.append(help_document_grafix_t %("gruppenueberblick.gif"))
            res.append(help_document_text_t %(ht_gruppenuebersicht_t))
            res.append(help_document_theme_t %("Abfrageergebnis:"))
            res.append(help_document_grafix_t %("gruppenueberblick2.gif"))
            res.append(help_document_text_t %(ht_gruppenuebersicht2_t))
        elif help_id=='Neumelde-_und_Abschlusszahlen':
            res.append(help_document_theme_t %("Abfrage:<br><b>Neumelde- und Abschlusszahlen f&uuml;r das Jahr x</b>"))
            res.append(help_document_grafix_t %("neumeldeabschl1.gif"))
            res.append(help_document_text_t %(ht_neumelde_und_abschluesse_t))
            res.append(help_document_theme_t %("Abfrageergebnis:"))
            res.append(help_document_grafix_t %("neumeldeabschl2.gif"))
            res.append(help_document_text_t %(ht_neumelde_und_abschluesse2_t))
        elif help_id=='Klientenzahl_pro_Mitarbeiter':
            res.append(help_document_theme_t %("Abfrage:<br><b>Klienten pro Mitarbeiter f&uuml;r das Jahr x</b>"))
            res.append(help_document_grafix_t %("klientenpromitarbeiter1.gif"))
            res.append(help_document_text_t %(ht_klienten_pro_mitarbeiter_t))
            res.append(help_document_theme_t %("Abfrageergebnis:"))
            res.append(help_document_grafix_t %("klientenpromitarbeiter2.gif"))
            res.append(help_document_text_t %(ht_klienten_pro_mitarbeiter2_t))
            
            ##*************************************************************************
            ##  Stichworterklärungen
            ##*************************************************************************
        elif help_id=='monatsgenau':
            res.append(help_document_theme_t %("Stichworterkl&auml;rung: monatsgenau"))
            res.append(help_document_text_t %(st_monatsgenau_t))
            res.append(help_document_back_t)
        elif help_id=='Strassenkatlog':
            res.append(help_document_theme_t %("Stichworterkl&auml;rung: Strassenkatalog"))
            res.append(help_document_text_t %(st_strassenkatalog_t))
            res.append(help_document_back_t)
        elif help_id=='Fallnummer':
            res.append(help_document_theme_t %("Stichworterkl&auml;rung: Fallnummer"))
            res.append(help_document_text_t %(st_fallnummer_t))
            res.append(help_document_back_t)
        elif help_id=='Funktionen_zda':
            res.append(help_document_theme_t %("Stichworterkl&auml;rung: Fallnummer"))
            res.append(help_document_text_t %(st_zu_den_akten_button_t))
            res.append(help_document_back_t)
        else:
            res.append(help_document_theme_t %("Kein passendes Hilfethema gefunden"))
            res.append(help_document_text_t %(no_content_t))
        res.append(help_document_end_t)
        return string.join(res, '')
        
        ##***************************************************************************
        ## Projekt:     Kobit/EBKuS-neu
        ## Datei:       ebkus/html/ebkushilfe.py
        ##
        ## Beschreibung: Klasse zur Darstellung des Dokumentenbaumes der Onlinehilfe
        ##
        ## Basisklasse: Request
        ##
        ## Typen:       -
        ##
        ## Klassenname: ebkus_help_tree
        ## Klassenart:  Klasse für die EBKuS - Onlinehilfe
        ##
        ##---------------------------------------------------------------------------
        ##
        ## REVISIONEN:
        ##
        ## DATUM        AUTOR           BESCHREIBUNG
        ## 21.12.2001   MastaleckT(msg)    Ersterstellung
        ##***************************************************************************
        
class ebkus_help_tree(Request.Request):
    permissions = Request.ALL
    def processForm(self, REQUEST, RESPONSE):
        res = []
        res.append(help_tree_start_t)
        res.append(help_tree_item_parent_t %({'p_nr':3,'p_link':'Bedienungsanleitung',\
                                              'p_text':'Hauptmen&uuml;'}))
        res.append(help_tree_child_start_t%("3"))
        res.append(help_tree_item_child_t %({'c_nr':3,'c_link':'Hauptmenü',\
                                              'c_text':'Das Hauptmen&uuml;'}))
        res.append(help_tree_item_child_t %({'c_nr':3,'c_link':'Aenderung_des_Benutzerpasswortes',\
                                              'c_text':'Passwort&auml;nderung'}))
        res.append(help_tree_child_end_t)
        ##*************************************************************************
        ##  Akte
        ##*************************************************************************
        res.append(help_tree_item_parent_t %({'p_nr':4,'p_link':'Klientenakte',\
                                              'p_text':'Klientenakte'}))
        res.append(help_tree_child_start_t%("4"))
        res.append(help_tree_item_child_t %({'c_nr':4,'c_link':'Neue_Akte_anlegen',\
                                              'c_text':'Akte neu anlegen'}))
        res.append(help_tree_item_child_t %({'c_nr':4,'c_link':'Akte_aktualisieren',\
                                              'c_text':'Akte bearbeiten'}))
        res.append(help_tree_item_child_t %({'c_nr':4,'c_link':'Klientenkarte',\
                                              'c_text':'Klientenkarte'}))
        res.append(help_tree_item_child_t %({'c_nr':4,'c_link':'Datei_in_die_Akte_aufnehmen',\
                                              'c_text':'Datei aufnehmen'}))
        res.append(help_tree_item_child_t %({'c_nr':4,'c_link':'Dokumente_und_Texteinträge_der_Akte_löschen',\
                                              'c_text':'Dokumente l&ouml;schen'}))
        res.append(help_tree_child_end_t)
        ##*************************************************************************
        ##  Bezugspersonen
        ##*************************************************************************
        res.append(help_tree_item_parent_t %({'p_nr':5,'p_link':'Bezugspersonen',\
                                              'p_text':'Bezugspersonen'}))
        res.append(help_tree_child_start_t%("5"))
        res.append(help_tree_item_child_t %({'c_nr':5,'c_link':'Neue_Person_eintragen',\
                                              'c_text':'Bezugsperson hinzuf&uuml;gen'}))
        res.append(help_tree_item_child_t %({'c_nr':5,'c_link':'Bezugsperson_bearbeiten',\
                                              'c_text':'Bezugsperson bearbeiten'}))
        res.append(help_tree_child_end_t)
        ##*************************************************************************
        ##  Leistungen
        ##*************************************************************************
        res.append(help_tree_item_parent_t %({'p_nr':6,'p_link':'Leistungen',\
                                              'p_text':'Leistungen'}))
        res.append(help_tree_child_start_t%("6"))
        
        res.append(help_tree_item_child_t %({'c_nr':6,'c_link':'Neue_Leistung_eintragen',\
                                              'c_text':'Leistung hinzuf&uuml;gen'}))
        res.append(help_tree_item_child_t %({'c_nr':6,'c_link':'Leistung_bearbeiten',\
                                              'c_text':'Leistung bearbeiten'}))
        res.append(help_tree_child_end_t)
        ##*************************************************************************
        ##  Zuständigkeit
        ##*************************************************************************
        res.append(help_tree_item_parent_t %({'p_nr':7,'p_link':'Zustaendigkeit',\
                                              'p_text':'Zust&auml;ndigkeit'}))
        res.append(help_tree_child_start_t%("7"))
        
        res.append(help_tree_item_child_t %({'c_nr':7,'c_link':'Neue_Zuständigkeit_eintragen',\
                                              'c_text':'Zuständigkeit eintragen'}))
        res.append(help_tree_item_child_t %({'c_nr':7,'c_link':'Eintrag_zur_Zuständigkeit_bearbeiten',\
                                              'c_text':'Zuständigkeit bearbeiten'}))
        res.append(help_tree_child_end_t)
        ##*************************************************************************
        ##  Kontakte
        ##*************************************************************************
        res.append(help_tree_item_parent_t %({'p_nr':8,'p_link':'Kontakte',\
                                              'p_text':'Kontakte'}))
        res.append(help_tree_child_start_t%("8"))
        
        res.append(help_tree_item_child_t %({'c_nr':8,'c_link':'Neue_Anmeldeinformation_eintragen',\
                                              'c_text':'Neuer Anmeldungskontakt'}))
        res.append(help_tree_item_child_t %({'c_nr':8,'c_link':'Anmeldeinformation_ändern',\
                                              'c_text':'Anmeldekontakt bearbeiten'}))
        res.append(help_tree_item_child_t %({'c_nr':8,'c_link':'Neuen_Einrichtungskontakt_eintragen',\
                                              'c_text':'Neuen Einrichtungskontakt'}))
        res.append(help_tree_item_child_t %({'c_nr':8,'c_link':'Einrichtungskontakt_ändern',\
                                              'c_text':'Einrichtungskontakt bearb.'}))
        res.append(help_tree_child_end_t)
        ##*************************************************************************
        ##  Gruppen
        ##*************************************************************************
        res.append(help_tree_item_parent_t %({'p_nr':9,'p_link':'Gruppen',\
                                              'p_text':'Gruppen'}))
        res.append(help_tree_child_start_t%("9"))
        
        res.append(help_tree_item_child_t %({'c_nr':9,'c_link':'Gruppenkartei',\
                                              'c_text':'Gruppenmen&uuml;'}))
        res.append(help_tree_item_child_t %({'c_nr':9,'c_link':'Neue_Gruppe_erstellen',\
                                              'c_text':'Neue Gruppe erstellen'}))
        res.append(help_tree_item_child_t %({'c_nr':9,'c_link':'Gruppe_bearbeiten',\
                                              'c_text':'Gruppe bearbeiten'}))
        res.append(help_tree_item_child_t %({'c_nr':9,'c_link':'Teilnehmerauswahl_aus_der_Klientenkartei',\
                                              'c_text':'Teilnehmer neu'}))
        res.append(help_tree_item_child_t %({'c_nr':9,'c_link':'Datum_des_Gruppenteilnehmers_ändern',\
                                              'c_text':'Teilnehmer bearbeiten'}))
        res.append(help_tree_item_child_t %({'c_nr':9,'c_link':'Teilnehmer_der_Gruppe_löschen'  ,\
                                              'c_text':'Teilnehmer l&ouml;schen'}))
        res.append(help_tree_item_child_t %({'c_nr':9,'c_link':'Dokumentenindex_der_Gruppe',\
                                              'c_text':'Dokumentenindex'}))
        res.append(help_tree_item_child_t %({'c_nr':9,'c_link':'Datei_in_die_Akte_aufnehmen',\
                                              'c_text':'Datei aufnehmen'}))
        res.append(help_tree_item_child_t %({'c_nr':9,'c_link':'Neuen_Texteintrag_zur_Gruppe_hinzufügen',\
                                              'c_text':'Texteintrag neu'}))
        res.append(help_tree_item_child_t %({'c_nr':9,'c_link':'Texteintrag_der_Gruppe_ändern',\
                                              'c_text':'Texteintrag bearbeiten'}))
        res.append(help_tree_item_child_t %({'c_nr':9,'c_link':'Texteintrag_der_Akte_zum_Ändern_auswählen',\
                                              'c_text':'Texteintragauswahl'}))
        res.append(help_tree_item_child_t %({'c_nr':9,'c_link':'Dokumente_und_Texteinträge_der_Akte_löschen',\
                                              'c_text':'Dokumente l&ouml;schen'}))
        res.append(help_tree_item_child_t %({'c_nr':9,'c_link':'Wordauswahl',\
                                              'c_text':'Word Export'}))
        res.append(help_tree_child_end_t)
        ##*************************************************************************
        ##  Statistik
        ##*************************************************************************
        res.append(help_tree_item_parent_t %({'p_nr':10,'p_link':'Statistik',\
                                              'p_text':'Statistik'}))
        res.append(help_tree_child_start_t%("10"))
        
        res.append(help_tree_item_child_t %({'c_nr':10,'c_link':'Neue_Fachstatistik_erstellen',\
                                              'c_text':'Neue Fachstatistik'}))
        res.append(help_tree_item_child_t %({'c_nr':10,'c_link':'Fachstatistik_ändern',\
                                              'c_text':'Fachstatistik bearbeiten'}))
        res.append(help_tree_item_child_t %({'c_nr':10,'c_link':'Neue_Bundesstatistik_erstellen',\
                                              'c_text':'Neue Bundesstatistik'}))
        res.append(help_tree_item_child_t %({'c_nr':10,'c_link':'Bundesstatistik_ändern',\
                                              'c_text':'Bundesstatistik bearbeiten'}))
        res.append(help_tree_child_end_t)
        ##*************************************************************************
        ##  Statistische Abfragen
        ##*************************************************************************
        res.append(help_tree_item_parent_t %({'p_nr':11,'p_link':'Statistische_Abfragen',\
                                              'p_text':'Statistische Abfragen'}))
        res.append(help_tree_child_start_t%("11"))
        res.append(help_tree_item_child_t %({'c_nr':11,'c_link':'Alle_Beratungen',\
                                              'c_text':'Alle Beratungen'}))
        res.append(help_tree_item_child_t %({'c_nr':11,'c_link':'Laufende_Beratungen',\
                                              'c_text':'Laufende Beratungen'}))
        res.append(help_tree_item_child_t %({'c_nr':11,'c_link':'Abgeschlossene_Beratungen',\
                                              'c_text':'Abgeschl. Beratungen'}))
        res.append(help_tree_item_child_t %({'c_nr':11,'c_link':'Suche_alle_Beratungen_ab_Fallnummer',\
                                              'c_text':'Beratungen ab Fallnummer'}))
        res.append(help_tree_item_child_t %({'c_nr':11,'c_link':'Bundesstatistikabfrage',\
                                              'c_text':'Bundesstatistikabfrage'}))
        res.append(help_tree_item_child_t %({'c_nr':11,'c_link':'Fachstatistikabfrage',\
                                              'c_text':'Fachstatistikabfrage'}))
        res.append(help_tree_item_child_t %({'c_nr':11,'c_link':'Statistikabfrage:_Kategoriewahl',\
                                              'c_text':'Itemauswahl'}))
        res.append(help_tree_item_child_t %({'c_nr':11,'c_link':'Statistikabfrage:_Kategorienwahl',\
                                              'c_text':'Kategorienauswahl'}))
        res.append(help_tree_item_child_t %({'c_nr':11,'c_link':'Auswahl_Konsultationsanzahl_und_Zeitraum_für_alle_Personen',\
                                              'c_text':'Konsultationszahl'}))
        res.append(help_tree_item_child_t %({'c_nr':11,'c_link':'Anzahl_abgeschl._Faelle_-_gleiche_Konsultationssumme',\
                                              'c_text':'Konsultationssumme'}))
        res.append(help_tree_item_child_t %({'c_nr':11,\
        'c_link':'Auswahl_des_gewuenschten_Zeitraumes_und_die_Laenge_der_Beratungszeit_in_Monaten',\
                                              'c_text':'Beratungsdauer'}))
        res.append(help_tree_item_child_t %({'c_nr':11,\
        'c_link':'Auswahl_des_gewuenschten_Zeitraumes_und_Auswahl_einer_Leistung',\
                                              'c_text':'Beratungsd. & Leistung'}))
        ##     res.append(help_tree_item_child_t %({'c_nr':11,\
        ##     'c_link':'Anzahl_der_abgeschl._Faelle_-_Unterscheidung_nach_Haupt-_bzw._Geschwisterfall',\
        ##                                           'c_text':'Abgeschl. H. oder G.F&auml;lle'}))
        res.append(help_tree_item_child_t %({'c_nr':11,\
        'c_link':'Anzahl_abgeschl._Faelle_-_Mutter_und_Vater_haben_das_gleiche_Merkmal_x',\
                                              'c_text':'Eltern Merkmal x'}))
        res.append(help_tree_item_child_t %({'c_nr':11,\
        'c_link':'Anzahl_abgeschl._Faelle_-_Mutter_oder_Vater_Merkmal_x_gleich',\
                                              'c_text':'Elternteil Merkmal x'}))
        res.append(help_tree_item_child_t %({'c_nr':11,\
        'c_link':'Auswahl_des_Zeitraumes_für_die_Gruppenuebersicht',\
                                              'c_text':'Gruppen&uuml;bersicht'}))
        res.append(help_tree_item_child_t %({'c_nr':11,\
        'c_link':'Neumelde-_und_Abschlusszahlen',\
                                              'c_text':'Neumeld. und Abschl&uuml;sse'}))
        res.append(help_tree_item_child_t %({'c_nr':11,\
        'c_link':'Klientenzahl_pro_Mitarbeiter',\
                                              'c_text':'Klienten pro Mitarbeiter'}))
        res.append(help_tree_child_end_t)
        res.append(help_tree_end_t)
        return string.join(res, '')
