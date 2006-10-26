# coding: latin-1
##***************************************************************************
## Projekt:     Kobit/EBKuS-neu
## Datei:       ebkus/html/strkat.py
##
## Beschreibung:Maske für die Strassensuche
##
## Basisklasse: Request
##
## Typen:       -
##
## Klassenname: strkat
## Klassenart:  Klasse für die Strassensuche (Maske)
##
##---------------------------------------------------------------------------
##
## REVISIONEN:
##
## DATUM        AUTOR           BESCHREIBUNG
## 26.03.2002   brehmea(msg)    Ersterstellung
##
##***************************************************************************

## Standardimporte
import string

## EBKuSimporte

from ebkus.app import Request

from ebkus.app.ebapi import StrassenkatalogList, EE

from ebkus.app_surface.strkat_templates import *

class strkat(Request.Request):
##***************************************************************************
## Instanzvariablen
##***************************************************************************
    permissions = Request.MENU_PERM
    
    ##***************************************************************************
    ## Methoden - CTOR / DTOR
    ##***************************************************************************
    
    ##***************************************************************************
    ## Methoden - eigene Funktionalität
    ##***************************************************************************
    
    ##***************************************************************************
    ## Methode:     processForm
    ## Parameter:   (REQUEST, RESPONSE)
    ## Return:      string, der ein HTML-Gerüst darstellt.
    ##
    ## Beschreibung:
    ##
    ## Vorbed.:     -
    ## Nebenwirk.:  -
    ##***************************************************************************
    def processForm(self, REQUEST, RESPONSE):
    
        try:
            suche_strasse = str(self.form.get('suche_strasse'))
        except:
            suche_strasse = ""
        try:
            suche_hausnr  = str(self.form.get('suche_hausnr'))
        except:
            suche_hausnr  = ""
        try:
            suche_plz     = str(self.form.get('suche_plz'))
        except:
            suche_plz     = ""
            
        if (len(suche_strasse) < 2) or suche_strasse[0] == "%":
            eemsg = "Das verwendete Suchmuster ist nicht g&uuml;ltig."
            eemsg = eemsg + "<br>Bitte geben Sie mindestens 2 Zeichen des"
            eemsg = eemsg + "<br>Stra&szlig;ennamens an und vermeiden Sie<br>Sonderzeichen."
            raise EE(eemsg)
        setted = 0
        if (suche_strasse != "" and suche_strasse != "None"):
            wherestr = 'str_name Like \'%s%%\'' % suche_strasse
            setted = 1
        else:
            wherestr = ''
            setted += 0
            
        if (suche_hausnr != "" and suche_hausnr != "None"):
            if setted == 1:
                wherestr = wherestr + ' and '
            wherestr = wherestr + 'hausnr Like \'%s%%\'' % suche_hausnr
            setted += 1
        else:
            setted += 0
            
        if (suche_plz != "" and suche_plz != "None"):
            if setted > 0:
                wherestr = wherestr + ' and '
            wherestr = wherestr + 'plz Like \'%s%%\'' % suche_plz
            setted += 1
        else:
            setted += 0
            
        if setted > 0:
            strassenkat = StrassenkatalogList(where = '%s' %wherestr)
            strassenkat.sort('str_name')
            if len(strassenkat) < 1:
                raise EE('Keine Strasse gefunden.')
                
        res = []
        res.append(strkat_start_t)
        if suche_strasse == "None":
            suche_strasse = ""
        if suche_hausnr == "None":
            suche_hausnr = ""
        if suche_plz == "None":
            suche_plz = ""
        res.append(strkat_main1_t % (suche_strasse, suche_hausnr, suche_plz))
        if setted > 0:
            for element in strassenkat:
              # auffuellen mit "&nbsp;"
                tmpstr = element['str_name']
                lentmpstr = len(tmpstr)
                while lentmpstr < 20:
                    tmpstr += "&nbsp;"
                    lentmpstr += 1
                element['str_name2'] = tmpstr
                if len(element['str_name']) > 20:
                    element['str_name2'] = "%0.20s" % element['str_name']
                    
                tmpstr = element['hausnr']
                lentmpstr = len(tmpstr)
                while lentmpstr < 4:
                    tmpstr += "&nbsp;"
                    lentmpstr += 1
                element['hausnr2'] = tmpstr
                
                tmpstr = str(element['plz'])
                lentmpstr = len(tmpstr)
                while lentmpstr < 5:
                    tmpstr += "&nbsp;"
                    lentmpstr += 1
                element['plz2'] = tmpstr
                
                tmpstr = element['Plraum']
                lentmpstr = len(tmpstr)
                while lentmpstr < 4:
                    tmpstr = "&nbsp;" + tmpstr
                    lentmpstr += 1
                element['Plraum2'] = tmpstr
                
                res.append(strkat_element_t % element)
        res.append(strkat_main2_t)
        res.append(strkat_end_t)
        
        return string.join(res, '')
        
        
        
        
        
        
        
        
