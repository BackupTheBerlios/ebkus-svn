# coding: latin-1
##*************************************************************************
##
## Projekt:      EBKuS
## Datei:        date.py
##
## Beschreibung: Funktion zum Berechnen des Alters nach dem Geburtsdatum
##
##*************************************************************************
##
## Revisionen:
##
## Datum      Autor                Beschreibung
##
## 28.09.2001 mastaleckT           Ersterstellung
##
##*************************************************************************
import time

def calc_age(geb,fall_bgd,fall_bgm,fall_bgy):
    try:
    ##*************************************************************************
    ##
    ## Auseinandernehmen des Geburtsdatums in DD MM YYYY
    ##
    ## mastaleckT(msg)28.09.01
    ##
    ##*************************************************************************
        geburtstag_t = int(geb[:2])
        geburtstag_m = int(geb[3:5])
        geburtstag_Y = int(geb[6:])
        ##*************************************************************************
        ##
        ## Auseinandernehmen des aktuellen Datums in DD MM YYYY
        ##
        ## mastaleckT(msg)28.09.01
        ##
        ##*************************************************************************
        
        today_t = int(fall_bgd)
        today_m = int(fall_bgm)
        today_Y = int(fall_bgy)
        maxold = today_Y - geburtstag_Y
        ##*************************************************************************
        ##
        ## Wegen Jahresgenauigkeit bei der Statistischen Angabe tritt ein Fehler
        ## auf, wenn Geburtsjahr gleich dem akt. Jahr ist. (Differenz ist 0)
        ## Fehler wird hier abgefangen. Zusätzlich die obligatorische Abfrage
        ## auf negative Differenz.
        ##
        ## mastaleckT(msg)28.09.01
        ##
        ##*************************************************************************
        if(maxold <= 0):
            return 0
        else:
            if(geburtstag_m < today_m):
                return maxold
            elif(geburtstag_m == today_m):
                if(geburtstag_t <= today_t):
                    return maxold
                else:
                    return maxold - 1
            else:
                return maxold - 1
    except:
        return -1
        
        
