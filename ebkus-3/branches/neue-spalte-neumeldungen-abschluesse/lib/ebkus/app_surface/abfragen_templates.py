# coding: latin-1
###########################
# Fachstatistik Abfrage
###########################

fsabfrjahr_t = """
</head>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000">
<table width="735" align="center">"""

fsabfrjahr2_t = """
<form action="%(file)s" method="post">
                <tr>
                  <td align="center" colspan="2" class="legendtext"> <fieldset><legend>Stellenauswahl</legend>
                    <table border="0" cellpadding="1" width="71%%" height="30">
                      <tr>
                        <td align="right" class="legendtext" width="18%%"><B>Jahr:
                          </B></td>
                        <td align="left" class="legendtext" width="82%%">
                          <select name="op" class="listbox130">
                            <option value="="> gleich
                            <option value="<"> kleiner als
                            <option value=">"> gr&ouml;sser als
                            <option value="<="> kleiner als u. gleich
                            <option value=">="> gr&ouml;sser als u. gleich
                          </select>
                          <input type="text" size="2" maxlength="4" value="%(year)s" name="year" class="textboxmid">
                        </td>
                        """
fsabfrstelle_t = """ </tr>
                      <tr>
                        <td align="right" class="legendtext" width="18%" height="118"><B>Stelle(n):</B></td>
                        <td align="left" rowspan=2 class="legendtext" width="82%" height="118">
                          <select name="stz" multiple size=6 style="width:300pt">"""

fsabfrplraum_t = """  </select>
                     </td>
                    </tr>
                   </table>
                   </fieldset>
                   </td>
                  </tr>
                   <tr>
                    <td align="center" colspan="2" class="legendtext"> <fieldset><legend>Planungsraumauswahl</legend>
                    <table border="0" cellpadding="1" width="71%%" height="30">
                      <tr>
                        <td align="right" class="legendtext" width="18%%"><B>Planungraum:</B></td>
                        <td align="left" rowspan=2 class="legendtext" width="82%" height="118">
                        
                         <select name="bz" multiple size=6 style="width:300pt">"""

fsabfrtabende_t = """
                          </select>
                        </td>
                      </tr>
                    </table>
                    </fieldset>
                  </td>
                </tr>
                <tr>
                  <td align="center" class="legendtext" valign="middle" colspan="3">
                    <fieldset>
                    <table width="95%%" border="0" cellpadding="1">
                      <tr height="40">
                        <td width="33%%" align="center" valign="middle">
                          <input type="submit" name="" value="&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Ok&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" class="button">
                        </td>
                        <td align="center" valign="middle" width="33%%">
                          <input type="reset" value="Zur&uuml;cksetzen" class="button">
                        </td>
                        <td align="center" valign="middle" width="34%%">
                          <input type="button" value="Abbrechen" class="button" onClick="javascript:history.back()">
                        </td>
                      </tr>
                    </table>
                    </fieldset> </td>
                </tr>
              </form>
            </table>
</body>
</html>
"""

##*************************************************************************
##
##  Fachstatistikergebnis
##
##*************************************************************************

fsergebnis1_t = """
</head>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000">
<table width="735" align="center">
"""

gesamtzahl_t = """
  <tr>
    <td colspan="2" align="center" class="legendtext">
      <fieldset><legend class="legendtext">Abfrage</legend>
        <table width="95%%">
          <tr>
            <td align="center" bgcolor="#FFFFFF" class="legendtext">Klientenzahl: %d von %d</td>
          </tr>
          <tr>
            <td align="center" class="normaltext" bgcolor="#FFFFFF">%s</td>
          </tr>
          <tr>
            <td>&nbsp;</td>
          </tr>
        </table>
      </fieldset>
    </td>
  </tr>
"""
thkategorie_t = """
  <tr>
    <td colspan="2" align="center" class="legendtext">
      <fieldset><legend class="legendtext">%(name)s</legend>
        <table border=0 cellspacing=1 width="95%%" align="center">
          <tr>
            <td class="legendtext" bgcolor=#FFFFFF>&nbsp;</td>
            <td class="legendtext" bgcolor=#FFFFFF width="30" align="center">&#160; S</td>
            <td class="legendtext" bgcolor=#FFFFFF width="60" align="center">&#160; %%</td>
          </tr>"""

item_t = """
          <tr>
            <td align="left" class="normaltext" bgcolor=#FFFFFF>  %s </td>
            <td align="right" class="normaltext" bgcolor=#FFFFFF width="30"> %s </td>
            <td align="right" class="normaltext" bgcolor=#FFFFFF width="60"> %.2f</td>
          </tr>"""

item_ende_t = """
          <tr>
          <td bgcolor="#CCCCCC" colspan="3">&nbsp;</td>
          </tr>
        </table>
      </fieldset>
    </td>
  </tr>
   """

thkategoriejgh_t = """
  <tr>
    <td colspan="2" align="center" class="legendtext">
      <fieldset><legend class="legendtext">%s</legend>
        <table border=0 cellspacing=1 width="95%%" align="center">
          <tr>
            <td class="legendtext" bgcolor=#FFFFFF>&nbsp;</td>
            <td class="legendtext" bgcolor=#FFFFFF width="30" align="center">&#160; S</td>
            <td class="legendtext" bgcolor=#FFFFFF width="60" align="center">&#160; %%</td>
          </tr>"""

fsergebnis_ende_t = """
  </table>
</body>
</html>
"""
##*************************************************************************
##
##  Fachstatistikergebnis Einzeltabellenansicht
##
##*************************************************************************

fsergebnis1_tab_t = """
</head>
<body bgcolor="#FFFFFF" link="#FFFFFF" vlink="#FFFFFF" alink="#FFFFFF">
<table width="735" align="center">
"""

thkategorie_tab_t = """
  <tr>
    <td colspan="2" align="center">
        <table border=0 cellspacing=1 width="95%%" align="center">
          <tr>
            <td class="legendtext" bgcolor=#FFFFFF>%(name)s</td>
            <td class="legendtext" bgcolor=#FFFFFF width="30" align="center">&#160; S</td>
            <td class="legendtext" bgcolor=#FFFFFF width="60" align="center">&#160; %%</td>
          </tr>"""

item_tab_w_t = """
          <tr>
            <td align="left" class="normaltext" bgcolor=#FFFFFF>%s</td>
            <td align="right" class="normaltext" bgcolor=#FFFFFF width="30"> %s </td>
            <td align="right" class="normaltext" bgcolor=#FFFFFF width="60"> %.2f</td>
          </tr>"""

item_tab_g_t = """
          <tr>
            <td align="left" class="normaltext" bgcolor=#EEEEEE>%s</td>
            <td align="right" class="normaltext" bgcolor=#EEEEEE width="30"> %s </td>
            <td align="right" class="normaltext" bgcolor=#EEEEEE width="60"> %.2f</td>
          </tr>"""


item_ende_tab_t = """
        </table>
    </td>
  </tr>
   """

thkategoriejgh_tab_t = """
  <tr>
    <td colspan="2" align="center">
        <table border=0 cellspacing=1 width="95%%" align="center">
          <tr>
            <td class="legendtext" bgcolor=#FFFFFF>%s</td>
            <td class="legendtext" bgcolor=#FFFFFF width="30" align="center">&#160; S</td>
            <td class="legendtext" bgcolor=#FFFFFF width="60" align="center">&#160; %%</td>
          </tr>"""

fsergebnis_ende_tab_t = """
  </table>
</body>
</html>
"""


#####################################################
# HTML-Gerüst für die einzelnen Chart-Seiten
# abrehme (msg) 18.09.2001
#####################################################
efbchart_html_tag="""
  <tr>
    <td align="left" class="legendtext">
    <a href="#top" alt="Nach oben">
      <img border="0" src="/ebkus/ebkus_icons/button_go_top.gif">
    </a>
    </td>
    <td align="right" class="legendtext">
    <table>
      <tr valign="top">
        <td align="center" width="40"><A href=%(imagedir1)s target="_new" alt="%(titel1)s"><img  border="0" src="/ebkus/ebkus_icons/printer_button.gif"></A></td>
        <td align="right" width="40"><A href=%(imagedir2)s target="_new" alt="%(titel2)s"><img border="0" src="/ebkus/ebkus_icons/diagramm_button.gif"></A></td>
      </tr>
    </table>
    </td>
  </tr>
"""
efbchart_html_tag_datei="""
<html>
<head>
  <title>%(titel)s</title>
</head>
<body bgcolor=#FFFFFF link="#CCCCCC" vlink="#CCCCCC" alink="#000000">
<center>
<table cellspacing=30>
  <tr>
    <td> <img border="0" src=%(imagedir)s>
  <tr>
</table>
</center>
</body>
</html>
"""

##*************************************************************************
## formabfr2
##*************************************************************************

suchefallnummer_t = """
</head>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000" onLoad="javascript:document.abfr2.expr.focus();">
<table width="735" align="center">
  <form action="abfr2" name="abfr2" method="post">
  <tr>
    <td align="center" class="legendtext"><fieldset><legend class="legendtext"><b>Suche ab Fallnummer</b></legend>
      <table border=0 cellspacing=1 cellpadding="8" width="95%">
        <tr align="center">
          <td height="36" width="50%" align="right">
            <select name="stz">"""

suchefallnummer2_t = """
            </select>
          </td>
          <td height="36" width="50%" align="left">
            <select name="table">
              <option value="fall" selected> Beratungsfallnummer
            </select>
          </td>
        </tr>
        <tr align="center" class="labeltext">
          <td height="36" align="right" width="50%">Suchausdruck: </td>
          <td height="36" align="left">
            <input type="text" class="textbox" size=30 maxlength=30 name="expr">
          </td>
        </tr>
      </table>
      </fieldset> </td>
  </tr>
  <tr>
    <td align="center" class="legendtext" valign="middle" colspan="3"> <fieldset>
      <table width="95%%" border="0" cellpadding="1">
        <tr height="40">
          <td width="33%%" align="center" valign="middle">
            <input type="submit" name="" value="&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Ok&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" class="button">
          </td>
          <td align="center" valign="middle" width="33%%">
            <input type="reset" value="Zur&uuml;cksetzen" class="button">
          </td>
          <td align="center" valign="middle" width="34%%">
            <input type="button" value="Abbrechen" class="button" onClick="javascript:history.back()">
          </td>
        </tr>
      </table>
      </fieldset> </td>
  </tr>
  </form>
</table>
</body>
</html>"""

##*************************************************************************
## abfr1 (Fallanzeige -> Bsp.: Alle Fälle anzeigen)
##*************************************************************************

thabfr1_t = """
</head>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000">
<table width="735" align="center">
<form>
   <tr>
    <td align="center" class="legendtext"><fieldset><legend class="legendtext"><b>F&auml;lle</b></legend>
      <table border=0 cellspacing=1 width="95%">
        <tr height="19">
          <td bgcolor="#FFFFFF" class="labeltext">Fallnr.:</td>
          <td bgcolor="#FFFFFF" class="labeltext">Vorname: </td>
          <td bgcolor="#FFFFFF" class="labeltext">Name:</td>
          <td bgcolor="#FFFFFF" class="labeltext">Gb:</td>
          <td bgcolor="#FFFFFF" class="labeltext">Bearbeiter:</td>
          <td bgcolor="#FFFFFF" class="labeltext">von:</td>
          <td bgcolor="#FFFFFF" class="labeltext">bis:</td>
          <td bgcolor="#FFFFFF" class="labeltext">Beginn:</td>
          <td bgcolor="#FFFFFF" class="labeltext">z.d.A:</td>
        </tr>
        """

abfr1_t = """
        <tr align="center" height="19">
          <td bgcolor="#FFFFFF" class="normaltext"> <A HREF="klkarte?akid=%(fall_id__akte_id)d&fallid=%(fall_id)d">
            %(fall_id__fn)s</A></td>
          <td bgcolor="#FFFFFF" class="normaltext">%(fall_id__akte_id__vn)s </td>
          <td bgcolor="#FFFFFF" class="normaltext">%(fall_id__akte_id__na)s </td>
          <td bgcolor="#FFFFFF" class="normaltext">%(fall_id__akte_id__gb)s </td>
          <td bgcolor="#FFFFFF" class="normaltext"> %(mit_id__na)s </td>
          <td bgcolor="#FFFFFF" class="normaltext">%(bgd)d.%(bgm)d.%(bgy)d</td>
          <td bgcolor="#FFFFFF" class="normaltext">%(ed)d.%(em)d.%(ey)d</td>
          <td bgcolor="#FFFFFF" class="normaltext">%(fall_id__bgd)d.%(fall_id__bgm)d.%(fall_id__bgy)d
          </td>
          <td bgcolor="#FFFFFF" class="normaltext"> %(fall_id__zdad)d.%(fall_id__zdam)d.%(fall_id__zday)d</td>
        </tr>"""

abfr1b_t = """
       <tr><td>&nbsp;</td></tr>
       </table>
        <tr>
   <td align="center" class="legendtext">
      <fieldset>
      <table width="95%">
      <tr height="40">
      <td align="center"><input type="button" name="" value="Zur&uuml;ck" class="button" onClick="javascript:history.back()"></td>
      </tr>
      </table>
      </fieldset>
    </td>
  </tr>
  </form>
</table>
"""

##*************************************************************************
## formabfr3
##*************************************************************************

suchwort_t = """
</head>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000" onLoad="javascript:document.abfr3.expr.focus();">
<table width="735" align="center">"""

suchwort2a_t = """
  <form action="abfr3" method="post" name="abfr3">
  <tr>
    <td align="center" colspan="2" class="legendtext"><fieldset><legend class="legendtext"><b>Suche</b></legend>
      <table border=0 cellspacing=1 cellpadding="8" width="95%">
        <tr align="center">
          <td height="36" width="50%" align="right">
            <select name="stz">"""


suchwort2b_t = """
 </select>
          </td>
          <td height="36" width="50%" align="left">
            <select name="table">
                <option value="akte" selected> Vor- oder Nachname, Klient
                            <option value="bezugsperson"> Vor- oder Nachname, Bezugsperson
                            <option value="fall"> Beratungsfallnummer
                            <option value="gruppe"> Gruppe
            </select>
          </td>
        </tr>
        <tr align="center" class="labeltext">
          <td height="36" align="right" width="50%">Suchausdruck: </td>
          <td height="36" align="left">
            <input type="text" class="textbox" size=30 maxlength=30 name="expr">
          </td>
        </tr>
      </table>
      </fieldset> </td>
  </tr>
  <tr>
    <td align="center" class="legendtext" valign="middle" colspan="2"> <fieldset>
      <table width="95%%" border="0" cellpadding="1">
        <tr height="40">
          <td width="33%%" align="center" valign="middle">
            <input type="submit" name="" value="Suche" class="button">
          </td>
          <td align="center" valign="middle" width="33%%">
            <input type="reset" value="Zur&uuml;cksetzen" class="button">
          </td>
          <td align="center" valign="middle" width="34%%">
            <input type="button" value="Abbrechen" class="button" onClick="javascript:history.back()">
          </td>
        </tr>
      </table>
      </fieldset> </td>
  </tr>
  </form>
</table>
</body>
</html>"""

##*************************************************************************
## abfr3
##*************************************************************************

thabfr3_start_t = """
</head>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000">
<table width="735" align="center">"""

thabfr3_header_t = """
   <tr>
    <td align="center" class="legendtext"><fieldset><legend class="legendtext"><b>F&auml;lle</b></legend>
      <table border=0 cellspacing=1 width="95%">
        <tr height="19">
          <td bgcolor="#FFFFFF" class="labeltext">Fallnr.:</td>
          <td bgcolor="#FFFFFF" class="labeltext">Vorname: </td>
          <td bgcolor="#FFFFFF" class="labeltext">Name:</td>
          <td bgcolor="#FFFFFF" class="labeltext">Gb:</td>
          <td bgcolor="#FFFFFF" class="labeltext">Bearbeiter:</td>
          <td bgcolor="#FFFFFF" class="labeltext">von:</td>
          <td bgcolor="#FFFFFF" class="labeltext">bis:</td>
          <td bgcolor="#FFFFFF" class="labeltext">Beginn:</td>
          <td bgcolor="#FFFFFF" class="labeltext">z.d.A:</td>
        </tr>
        """

thgrabfr3_header_t = """
   <tr>
    <td align="center" class="legendtext"><fieldset><legend class="legendtext"><b>F&auml;lle</b></legend>
      <table border=0 cellspacing=1 width="95%">
        <tr height="19">
          <td bgcolor="#FFFFFF" class="labeltext">Fallnr.:</td>
          <td bgcolor="#FFFFFF" class="labeltext">Vorname: </td>
          <td bgcolor="#FFFFFF" class="labeltext">Name:</td>
          <td bgcolor="#FFFFFF" class="labeltext">Gb:</td>
          <td bgcolor="#FFFFFF" class="labeltext">Bearbeiter:</td>
          <td bgcolor="#FFFFFF" class="labeltext">von:</td>
          <td bgcolor="#FFFFFF" class="labeltext">bis:</td>
          <td bgcolor="#FFFFFF" class="labeltext">Beginn:</td>
          <td bgcolor="#FFFFFF" class="labeltext">z.d.A:</td>
        </tr>
        """


abfr2_item_t = """
        <tr align="center" height="19">
          <td bgcolor="#FFFFFF" class="normaltext"> <A HREF="klkarte?akid=%(fall_id__akte_id)d&fallid=%(fall_id)d">
            %(fall_id__fn)s</A></td>
          <td bgcolor="#FFFFFF" class="normaltext">%(fall_id__akte_id__vn)s </td>
          <td bgcolor="#FFFFFF" class="normaltext">%(fall_id__akte_id__na)s </td>
          <td bgcolor="#FFFFFF" class="normaltext">%(fall_id__akte_id__gb)s </td>
          <td bgcolor="#FFFFFF" class="normaltext"> %(mit_id__na)s </td>
          <td bgcolor="#FFFFFF" class="normaltext">%(bgd)d.%(bgm)d.%(bgy)d</td>
          <td bgcolor="#FFFFFF" class="normaltext">%(ed)d.%(em)d.%(ey)d</td>
          <td bgcolor="#FFFFFF" class="normaltext">%(fall_id__bgd)d.%(fall_id__bgm)d.%(fall_id__bgy)d
          </td>
          <td bgcolor="#FFFFFF" class="normaltext"> %(fall_id__zdad)d.%(fall_id__zdam)d.%(fall_id__zday)d</td>
        </tr>"""

abfr_tab_ende_t = """
      <tr><td colspan ="9">&nbsp;</td></tr>
      </table>
      </fieldset>
      </td>
      </tr>"""

abfr3_ende_t = """
   <tr>
   <td align="center" class="legendtext">
      <fieldset>
      <table width="95%">
      <form>
      <tr height="40">
      <td align="center"><input type="button" name="" value="Zur&uuml;ck" class="button" onClick="javascript:history.back()"></td>
      </tr>
      </form>
      </table>
      </fieldset>
    </td>
  </tr>
</table>
</body>
</html>"""


abfr3a_t = """
     <tr align="center" height="19">
          <td bgcolor="#FFFFFF" class="normaltext">
          <A HREF="klkarte?akid=%(fall_id__akte_id)d&fallid=%(fall_id)d"> %(fall_id__fn)s</A></td>
    """
abfr3b_t = """
    <td bgcolor="#FFFFFF" class="normaltext">%(vn)s</td>
    <td bgcolor="#FFFFFF" class="normaltext">%(na)s </td>
    """
abfr3c_t = """
    <td bgcolor="#FFFFFF" class="normaltext">%(fall_id__akte_id__gb)s </td>
    <td bgcolor="#FFFFFF" class="normaltext">%(mit_id__na)s </td>
    <td bgcolor="#FFFFFF" class="normaltext">%(bgd)d.%(bgm)d.%(bgy)d</td>
    <td bgcolor="#FFFFFF" class="normaltext">%(ed)d.%(em)d.%(ey)d</td>
    <td bgcolor="#FFFFFF" class="normaltext">%(fall_id__bgd)d.%(fall_id__bgm)d.%(fall_id__bgy)d </td>
    <td bgcolor="#FFFFFF" class="normaltext">%(fall_id__zdad)d.%(fall_id__zdam)d.%(fall_id__zday)d</td>
    </tr> """

thabfrgr_t = """
<tr>
    <td align="center" class="legendtext"><fieldset><legend class="legendtext"><b>Gruppen</b></legend>
      <table border=0 cellspacing=1 width="95%">
        <tr height="19">
          <td bgcolor="#FFFFFF" class="normaltext">Gruppe</td>
          <td bgcolor="#FFFFFF" class="normaltext">Thema</td>
          <td bgcolor="#FFFFFF" class="normaltext">Beginn</td>
          <td bgcolor="#FFFFFF" class="normaltext">Ende</td>
        </tr>"""

abfrgr_t = """
<tr>
<td bgcolor="#FFFFFF" class="normaltext"><A HREF="gruppenkarte?gruppeid=%(id)d">%(name)s</A> </td>
<td bgcolor="#FFFFFF" class="normaltext">%(thema)s </td>
<td bgcolor="#FFFFFF" class="normaltext">%(bgd)d.%(bgm)d.%(bgy)d </td><td bgcolor="#FFFFFF"> %(ed)d.%(em)d.%(ey)s </td>
</tr>"""

##*************************************************************************
##  formabrage4
##*************************************************************************



##*************************************************************************
## abfr4
##*************************************************************************

thabfr4_t = """
</head>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000">
<table width="735" align="center">
 <tr>
    <td align="center" class="legendtext"><fieldset><legend class="legendtext"><b>Neumelde- u. Abschlusszahlen</b></legend>
    <table border=0 cellspacing=1 width="95%">
    <tr>
    <td align="right" width="33%" class="labeltext" bgcolor="#FFFFFF">Monat</td>
    <td align="center" widht="33%" class="labeltext" bgcolor="#FFFFFF">Neu</td>
    <td align="center" widht="34%" class="labeltext" bgcolor="#FFFFFF">Hauptfall</td>
    <td align="center" widht="34%" class="labeltext" bgcolor="#FFFFFF">Geschwisterfall</td>
    <td align="center" widht="34%" class="labeltext" bgcolor="#FFFFFF">z.d.A.</td>
    </tr> """

abfr4_t = """
    <tr>
    <td align="right" class="normaltext" bgcolor="#FFFFFF">%d  </td>
    <td align="center" class="normaltext" bgcolor="#FFFFFF">%d  </td>
    <td align="center" class="normaltext" bgcolor="#FFFFFF">%d  </td>
    <td align="center" class="normaltext" bgcolor="#FFFFFF">%d  </td>
    <td align="center" class="normaltext" bgcolor="#FFFFFF">%d  </td>
    </tr> """

abfr4ges_t = """
    <tr>
    <td align="right" class="legendtext" bgcolor="#FFFFFF">Quartal 1</td>
    <td align="center" class="legendtext" bgcolor="#FFFFFF">%d</td>
    <td align="center" class="legendtext" bgcolor="#FFFFFF">%d</td>
    <td align="center" class="legendtext" bgcolor="#FFFFFF">%d</td>
    <td align="center" class="legendtext" bgcolor="#FFFFFF">%d</td>
    </tr>
    <tr>
    <td align="right" class="legendtext" bgcolor="#FFFFFF">Quartal 2</td>
    <td align="center" class="legendtext" bgcolor="#FFFFFF">%d</td>
    <td align="center" class="legendtext" bgcolor="#FFFFFF">%d</td>
    <td align="center" class="legendtext" bgcolor="#FFFFFF">%d</td>
    <td align="center" class="legendtext" bgcolor="#FFFFFF">%d</td>
    </tr>
    <tr>
    <td align="right" class="legendtext" bgcolor="#FFFFFF">Quartal 3</td>
    <td align="center" class="legendtext" bgcolor="#FFFFFF">%d</td>
    <td align="center" class="legendtext" bgcolor="#FFFFFF">%d</td>
    <td align="center" class="legendtext" bgcolor="#FFFFFF">%d</td>
    <td align="center" class="legendtext" bgcolor="#FFFFFF">%d</td>
    </tr>
    <tr>
    <td align="right" class="legendtext" bgcolor="#FFFFFF">Quartal 4</td>
    <td align="center" class="legendtext" bgcolor="#FFFFFF">%d</td>
    <td align="center" class="legendtext" bgcolor="#FFFFFF">%d</td>
    <td align="center" class="legendtext" bgcolor="#FFFFFF">%d</td>
    <td align="center" class="legendtext" bgcolor="#FFFFFF">%d</td>
    </tr>
    <tr>
    <td align="right" class="legendtext" bgcolor="#FFFFFF">Gesamt</td>
    <td align="center" class="legendtext" bgcolor="#FFFFFF">%d</td>
    <td align="center" class="legendtext" bgcolor="#FFFFFF">%d</td>
    <td align="center" class="legendtext" bgcolor="#FFFFFF">%d</td>
    <td align="center" class="legendtext" bgcolor="#FFFFFF">%d</td>
    </tr>
    <tr><td colspan="3" bgcolor="#CCCCCC">&nbsp;</td></tr>
</table>
</fieldset>
</td>
</tr>
<tr>
   <td align="center" class="legendtext">
      <fieldset>
      <table width="95%%">
      <form>
      <tr height="40">
      <td align="center"><input type="button" name="" value="Zur&uuml;ck" class="button" onClick="javascript:history.back()"></td>
      </tr>
      </form>
      </table>
      </fieldset>
    </td>
  </tr>
</table>
</body>
</html>"""

##*************************************************************************
## abfr5
##*************************************************************************

thabfr5_t = """
</head>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000">
<table width="735" align="center">
 <tr>
    <td align="center" class="legendtext"><fieldset><legend class="legendtext"><b>Neumelde- u. Abschlusszahlen</b></legend>
    <table border=0 cellspacing=1 width="95%%">
    <tr>
    <td align="right" width="25%%" class="labeltext" bgcolor="#FFFFFF">Mitarbeiter</td>
    <td align="center" widht="25%%" class="labeltext" bgcolor="#FFFFFF">Neu %s</td>
    <td align="center" widht="25%%" class="labeltext" bgcolor="#FFFFFF">Laufend</td>
    <td align="center" widht="25%%" class="labeltext" bgcolor="#FFFFFF">Beendet</td>
    </tr> """

abfr5_t = """
    <tr>
    <td align="right" class="normaltext" bgcolor="#FFFFFF">%s  </td>
    <td align="center" class="normaltext" bgcolor="#FFFFFF">%d  </td>
    <td align="center" class="normaltext" bgcolor="#FFFFFF">%d  </td>
    <td align="center" class="normaltext" bgcolor="#FFFFFF">%d  </td>
    </tr> """

abfr5ges_t = """
    <tr>
      <td align="right" class="normaltext" bgcolor="#FFFFFF">Gesamt</td>
      <td align="center" class="normaltext" bgcolor="#FFFFFF">%d  </td>
      <td align="center" class="normaltext" bgcolor="#FFFFFF">%d  </td>
      <td align="center" class="normaltext" bgcolor="#FFFFFF">%d  </td>
    </tr>
<tr><td colspan="3" bgcolor="#CCCCCC">&nbsp;</td></tr>
</table>
</fieldset>
</td>
</tr>
<tr>
   <td align="center" class="legendtext">
      <fieldset>
      <table width="95%%">
      <form>
      <tr height="40">
      <td align="center"><input type="button" name="" value="Zur&uuml;ck" class="button" onClick="javascript:history.back()"></td>
      </tr>
      </form>
      </table>
      </fieldset>
    </td>
  </tr>
</table>
</body>
</html>"""



##*************************************************************************
## formabfr6
##*************************************************************************

abfr6_kopf_t = """
</head>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000">
<table width="735" align="center">"""

abfr6_t = """
 <form action="%s" method="post">
 <tr>
    <td align="center" class="legendtext" colspan="2"><fieldset><legend class="legendtext"><b>Kategorien</b></legend>
     <table width="95%%" cellpadding="7">
      <tr>
      <td align="center">"""

abfr6_ende_t = """
      </select>
      </td>
      </tr>
      </table>
      </fieldset>
      <tr>
      <td align="center" colspan="2" class="legendtext">
      <fieldset>
      <table width="95%%">
      <form>
      <tr height="40">
      <td align="center"><input type="submit" name="" value="&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Ok&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" class="button"></td>
      <td align="center"><input type="reset" name="" value="Zur&uuml;cksetzen" class="button"></td>
      <td align="center"><input type="button" name="" value="Abbrechen" class="button" onClick="javascript:history.back()"></td>
      </tr>
      </form>
      </table>
      </fieldset>
      </td>
      </tr>
    </table>
  </body>
</html>
"""
##*************************************************************************
## formabfr6a
##*************************************************************************
formabfr6a1_t = """
</head>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000">
<table width="735" align="center">
  <form action="abfr6a" method="post">
    <tr>
      <td class="legendtext" align="center"><fieldset><legend class="legendtext"><b>Festlegen der
        Suchkriterien</b></legend>
        <table width="95%%" cellpadding="4">
          <tr>
            <td align="right" class="labeltext">Jahr:</td>
            <td align="left" class="labeltext">
              <select name="year_op">
                <option value = "=" > =
                <option value = "<" > <
                <option value = ">" > >
                <option value = "<=" > <=
                <option value = ">=" > >=
              </select>
              <input type="text" class="textboxmid" size="2" maxlength="4" value="%(year)s" name="year">
            </td>
          </tr>
          <tr>
            <td class="labeltext" align="right">Stelle:</td>
            <td align="left">
              <select class="listbox" name="stz">
                <option value=-1 > alle Beratungsstellen"""

formabfr6a2_t = """
              </select>
            </td>
          </tr>
          <tr>
            <td class="labeltext" align="right">Verkn&uuml;pfung der Bedingungen</td>
            <td class="normaltext" align="left"> und
              <input type="radio" value="and" name="konj" checked>
              / oder
              <input type="radio" value="or" name="konj" >
            </td>
          </tr>
        </table>
        </fieldset> </td>
    </tr>
    <tr>
      <td align="center" class="legendtext"><fieldset><legend class="legendtext"><b>Bedingungen</b></legend>
        <table width="95%%" cellpadding="4">
          <tr>
            <td align="left" class="labeltext" width="50%%">Kategorie:</td>
            <td align="left" class="labeltext" width="50%%">Item:</td>
          </tr>
          """

formitemausw1_t = """
          <tr>
            <td class="labeltext" align="right">
              <input type="hidden" value="%(id)s" name="feldid" >
              <input type="hidden" value="%(feld)s" name="%(id)s_feld" >
              <input type="hidden" value="=" name="%(id)s_op">
              %(name)s: </td>
            <td align="left">
              <select class="listbox" style="width:300pt" name="%(id)s_codeid" >"""

formitemausw2_t = """
              </select>
            </td>
          </tr>
          """

formabfr6a_ende_t = """
      </table>
      </td>
      </tr>
      <tr>
       <td align="center" class="legendtext">
      <fieldset>
      <table width="95%%">
      <form>
      <tr height="40">
      <td align="center"><input type="submit" name="" value="&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Ok&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" class="button"></td>
      <td align="center"><input type="reset" name="" value="Zur&uuml;cksetzen" class="button"></td>
      <td align="center"><input type="button" name="" value="Abbrechen" class="button" onClick="javascript:history.back()"></td>
      </tr>
      </form>
      </table>
      </fieldset>
      </td>
      </tr>
  </form>
</table>
</body>
</html>
"""

##*************************************************************************
## formabfr6b
##*************************************************************************

formabfr6b1_t = """
</head>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000">
<table width="735" align="center">
  <form action="abfr6b" method="post">
    <tr>
      <td align="center" class="legendtext"><fieldset><legend class="legendtext"><b>Festlegen der
        Suchkriterien</b></legend>
        <table width="95%%" cellpadding="4">
          <tr>
            <td align="right" class="labeltext">Jahr:</td>
            <td align="left" class="labeltext">
              <select name="year_op">
                <option value = "=" > =
                <option value = "<" > <
                <option value = ">" > >
                <option value = "<=" > <=
                <option value = ">=" > >=
              </select>
              <input type="text" class="textboxmid" size="4" maxlength="4" value="%(year)s" name="year">
            </td>
          </tr>
          <tr>
            <td class="labeltext" align="right">Stelle:</td>
            <td align="left">
              <select class="listbox" name="stz">
                <option value=-1 > alle Beratungsstellen"""

itemauswb_t = """
          <tr>
              <input type="hidden" value="or" name="%(id)s_konj" >
              <input type="hidden" value="=" name="%(id)s_op">
          </tr>
            """

itemauswb1_t = """
          <tr>
            <td align="right" class="labeltext">%(name)s:</td>
                        <td align="left">
<input type="checkbox" value="%(id)s" name="codeid">
            </td>
          </tr>
          """

itemauswb2_t = """
          <input type="hidden" value="%(id)s" name="feldid" >
          <input type="hidden" value="%(feld)s" name="%(id)s_feld" >
          """

formabfr6b_ende_t = """
        </table>
      </td>
    </tr>
    <tr>
      <td align="center" class="legendtext"><fieldset>
        <table width="95%%">
          <tr height="40">
            <td align="center">
              <input type="submit" name="" value="&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Ok&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" class="button">
            </td>
            <td align="center">
              <input type="reset" name="" value="Zur&uuml;cksetzen" class="button">
            </td>
            <td align="center">
              <input type="button" name="" value="Abbrechen" class="button" onClick="javascript:history.back()">
            </td>
          </tr>
        </table>
        </fieldset> </td>
    </tr>
  </form>
</table>
</body>
</html>
"""

##*************************************************************************
##  abfr6ab
##*************************************************************************


abfr6ab_ende_t = """
                <tr>
                  <td align="center" class="legendtext" valign="middle" colspan="3">
                    <fieldset>
                    <table width="95%%" border="0" cellpadding="1">
                      <tr height="40">
                        <td width="33%%" align="center" valign="middle">
                          <input type="submit" name="" value="&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Ok&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" class="button">
                        </td>
                        <td align="center" valign="middle" width="33%%">
                          <input type="reset" value="Zur&uuml;cksetzen" class="button">
                        </td>
                        <td align="center" valign="middle" width="34%%">
                          <input type="button" value="Abbrechen" class="button" onClick="javascript:history.back()">
                        </td>
                      </tr>
                    </table>
                    </fieldset> </td>
                  </form>
                </tr>
            </table>
</body>
</html>
"""
##*************************************************************************
##  abfr8
##*************************************************************************

thabfr8_t = """
</head>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000">
<table width="735" align="center">
  <form method="post">
    <tr>
      <td align="center" class="legendtext"><fieldset><legend class="legendtext"><b>Gruppen&uuml;berblick</b></legend>
        <table width="95%" cellpadding="4">
          <tr align="left">
            <td align="center" class="labeltext"> Nummer: </td>
            <td align="center" class="labeltext"> Name: </td>
            <td align="center" class="labeltext"> Gruppenart: </td>
            <td align="center" class="labeltext"> Teilnehmerkreis: </td>
            <td align="center" class="labeltext"> -zahl: </td>
            <td align="center" class="labeltext"> Beginn: </td>
            <td align="center" class="labeltext"> Ende: </td>
            <td align="center" class="labeltext"> Mitarbeiter: </td>
          </tr>"""
abfr8ges_t = """
          <tr>
            <td align="left" class="normaltext" bgcolor="#FFFFFF"> %s</td>
            <td align="left" class="normaltext" bgcolor="#FFFFFF"> %s </td>
            <td align="left" class="normaltext" bgcolor="#FFFFFF"> %s </td>
            <td align="left" class="normaltext" bgcolor="#FFFFFF"> %s </td>
            <td align="center" class="normaltext" bgcolor="#FFFFFF"> %d</td>
            <td align="left" class="normaltext" bgcolor="#FFFFFF"> %d.%d.%d</td>
            <td align="left" class="normaltext" bgcolor="#FFFFFF"> %d.%d.%d</td>
            <td align="left" class="normaltext" bgcolor="#FFFFFF"> %s</td>
          </tr>
"""
abfr8ges_ende_t = """
          <tr><td>&nbsp;</td></tr>
          </table>
          </td>
          </tr>
          <tr>
            <td align="center" class="legendtext">
              <fieldset>
               <table width="95%">
                 <tr height="40">
                   <td align="center"><input type="button" name="" value="Zur&uuml;ck" class="button" onClick="javascript:history.back()"></td>
                 </tr>
               </table>
              </fieldset>
            </td>
          </tr>
        </table>
      </td>
     </tr>
   </form>
</table>
</body>
</html>
"""



abfr8ages_t ="""
</head>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000">
<table width="735" align="center">
  <form action="formabfr8" method="post">
    <tr>
      <td class="legendtext" align="center"><fieldset><legend class="legendtext"><b>Zeitraum f&uuml;r
        die Abfrage</b></legend>
        <table width="95%%" cellpadding="0">
          <tr>
            <td class="labeltext" align="center" width="25%">Ab Monat:</td>
            <td class="labeltext" align="center" width="25%">Ab Jahr:</td>
            <td class="labeltext" align="center">Bis Monat:</td>
            <td class="labeltext" align="center">Bis Jahr:</td>
          </tr>
          <tr>
            <td align="center">
              <select name="monatvon" class="listbox130" style="width:80">
                <option value = "1" > 1
                <option value = "2" > 2
                <option value = "3" > 3
                <option value = "4" > 4
                <option value = "5" > 5
                <option value = "6" > 6
                <option value = "7" > 7
                <option value = "8" > 8
                <option value = "9" > 9
                <option value = "10" > 10
                <option value = "11" > 11
                <option value = "12" > 12
              </select>
            </td>
            <td align="center" width="25%">
              <input type="text" size="2" maxlength=4 name="jahrvon" class="textboxmid">
            </td>
            <td align="center">
              <select name="monatbis" class="listbox130" style="width:80">
                <option value = "1" > 1
                <option value = "2" > 2
                <option value = "3" > 3
                <option value = "4" > 4
                <option value = "5" > 5
                <option value = "6" > 6
                <option value = "7" > 7
                <option value = "8" > 8
                <option value = "9" > 9
                <option value = "10" > 10
                <option value = "11" > 11
                <option value = "12" > 12
              </select>
            </td>
            <td align="center">
              <input type="text" size="2" maxlength=4 name="jahrbis" class="textboxmid">
            </td>
          </tr>
          <tr><td colspan="4">&nbsp;</td></tr>
        </table>
        </fieldset>
        </td>
      </tr>
    <tr>
      <td class="legendtext" align="center">
           <fieldset>
        <table width="95%%" border="0" cellpadding="1">
          <tr height="40">
            <td width="33%%" align="center" valign="middle">
              <input type="submit" name="Input" value="&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Ok&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" class="button">
            </td>
            <td align="center" valign="middle" width="33%%">
              <input type="reset" value="Zur&uuml;cksetzen" class="button" name="reset">
            </td>
            <td align="center" valign="middle" width="34%%">
              <input type="button" value="Abbrechen" class="button" onClick="javascript:history.back()" name="button">
            </td>
          </tr>
        </table>
        </fieldset>
  </form>
</table>
</body>
</html>
"""

##*************************************************************************
##  abfr9
##*************************************************************************
thabfr9_t = """
</head>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000">
<table width="735" align="center">
  <form method="post">
    <tr>
      <td class="legendtext" align="center"><fieldset><legend class="legendtext"><b>&Uuml;bersicht abgeschlossene Beratungsf&auml;lle - gleiche Konsultationssumme</b></legend>
        <table width="95%" cellpadding="0">
          <tr align="left">
            <td class="labeltext"> Summe:</td>
            <td class="labeltext"> Anzahl:</td>
            <td class="labeltext"> Prozentsatz:</td>
          </tr>
          """
abfr9mid_t = """
          <tr align="center" bgcolor="#FFFFFF">
            <td class="normaltext" width="40%%" align="center">%d</td>
            <td class="normaltext" width="30%%" align="center">%d</td>
            <td class="normaltext" width="30%%" align="center"> %.2f </td>
          </tr>
"""

abfr9end_t = """
          <tr><td colspan="2">&nbsp;</td></tr>
        </table>
        </fieldset>
      </td>
    </tr>
    <tr>
      <td class="legendtext" align="center">
        <fieldset>
          <table width="95%%">
            <tr height="40">
            <td align="center" valign="middle" width="34%%" colspan="2">
              <input type="button" value="Zur&uuml;ck" class="button" onClick="javascript:history.back()" name="button">
            </td>
          </tr>
        </table>
        </fieldset>
        </td>
        </tr>
      </form>
</table>
</body>
</html>
"""

abfr9ages_t ="""
</head>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000" onLoad="document.formabfr9.jahrvon.focus();">
<table width="735" align="center">
  <form action="formabfr9" method="post" name="formabfr9">
    <tr>
      <td class="legendtext" align="center"><fieldset><legend class="legendtext"><b>Zeitraum f&uuml;r
        die Abfrage</b></legend>
       <table width="95%%" cellpadding="0">
          <tr align="center">
            <td class="labeltext" width="25%%" height="44">Von Jahr: </td>
            <td class="labeltext" width="25%%" height="44">Bis Jahr: </td>
          </tr>
          <tr align="center">
            <td class="labeltext" width="25%%">
              <input type="text" size="2" maxlength=4 name="jahrvon" class="textboxmid">
            </td>
            <td class="labeltext" width="25%%">
              <input type="text" size="2" maxlength=4 name="jahrbis" class="textboxmid">
            </td>
          </tr>
          <tr>
            <td colspan="2">&nbsp;</td>
          </tr>
        </table> </fieldset> </td>
    </tr>
    <tr>
      <td class="legendtext" align="center"> <fieldset>
        <table width="95%%" border="0" cellpadding="1">
          <tr height="40">
            <td width="33%%" align="center" valign="middle">
              <input type="submit" name="Input" value="&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Ok&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" class="button">
            </td>
            <td align="center" valign="middle" width="33%%">
              <input type="reset" value="Zur&uuml;cksetzen" class="button" name="reset">
            </td>
            <td align="center" valign="middle" width="34%%">
              <input type="button" value="Abbrechen" class="button" onClick="javascript:history.back()" name="button">
            </td>
          </tr>
        </table>
        </fieldset>
  </form>
</table>
</body>
</html>
"""


##*************************************************************************
##  abfr10
##*************************************************************************



thabfr10_t = """
</head>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000">
<table width="735" align="center">
  <form method="post">
"""


abfr10start_t = """
    <tr>
      <td class="legendtext" align="center"><fieldset><legend class="legendtext"><b>%s</b></legend>
        <table width="95%%" cellpadding="0">
          <tr align="left">
            <td class="labeltext"> Konsultationszahl:</td>
            <td class="labeltext"> Anzahl:</td>
            <td class="labeltext"> Prozentsatz:</td>
          </tr>
          """


abfr10mid_t = """
          <tr align="center" bgcolor="#FFFFFF">
            <td class="normaltext" width="40%%" align="center">%d</td>
            <td class="normaltext" width="30%%" align="center">%d</td>
            <td class="normaltext" width="30%%" align="center"> %.2f </td>
          </tr>
"""

abfr10end_t = """
        <tr><td colspan="2">&nbsp;</td></tr>
        </table>
        </fieldset>
      </td>
    </tr>"""


all_end_abfr10_t = """
  <tr>
    <td class="legendtext" align="center">
      <fieldset>
        <table width="95%%" border="0" cellpadding="1">
          <tr height="40">
            <td align="center" valign="middle" width="34%%">
              <input type="button" value="Zur&uuml;ck" class="button" onClick="javascript:history.back()" name="button">
            </td>
          </tr>
        </table>
        </fieldset>
      </td>
    </tr>
  </form>
</table>
</body>
</html>"""


abfr10ages_t ="""
</head>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000" onLoad="document.formabfr10.jahrvon.focus();">
<table width="735" align="center">
  <form action="formabfr10" method="post" name="formabfr10">
    <tr>
      <td class="legendtext" align="center"><fieldset><legend class="legendtext"><b>Zeitraum f&uuml;r
        die Abfrage</b></legend>
       <table width="95%%" cellpadding="0">
          <tr align="center">
            <td class="labeltext" width="25%%" height="44">Von Jahr: </td>
            <td class="labeltext" width="25%%" height="44">Bis Jahr: </td>
          </tr>
          <tr align="center">
            <td class="labeltext" width="25%%">
              <input type="text" size="2" maxlength=4 name="jahrvon" class="textboxmid">
            </td>
            <td class="labeltext" width="25%%">
              <input type="text" size="2" maxlength=4 name="jahrbis" class="textboxmid">
            </td>
          </tr>
          <tr>
            <td colspan="2">&nbsp;</td>
          </tr>
        </table> </fieldset> </td>
    </tr>
    <tr>
      <td class="legendtext" align="center"> <fieldset>
        <table width="95%%" border="0" cellpadding="1">
          <tr height="40">
            <td width="33%%" align="center" valign="middle">
              <input type="submit" name="Input" value="&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Ok&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" class="button">
            </td>
            <td align="center" valign="middle" width="33%%">
              <input type="reset" value="Zur&uuml;cksetzen" class="button" name="reset">
            </td>
            <td align="center" valign="middle" width="34%%">
              <input type="button" value="Abbrechen" class="button" onClick="javascript:history.back()" name="button">
            </td>
          </tr>
        </table>
        </fieldset>
  </form>
</table>
</body>
</html>
"""
##


## abfr11

thabfr11_t = """
</head>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000">
<table width="735" align="center">
  <form method="post">
    <tr>
      <td class="legendtext" align="center"><fieldset><legend class="legendtext">&Uuml;bersicht abgeschlossene Beratungsf&auml;lle - gleiche Dauer</b></legend>
        <table width="95%" cellpadding="0">
          <tr align="left">
            <td class="labeltext"> Beratungsdauer in Monaten: </td>
            <td class="labeltext"> Anzahl der F&auml;lle:</td>
            <td class="labeltext"> Prozentsatz:</td>
          </tr>
          """

abfr11mid_t = """
          <tr align="center" bgcolor="#FFFFFF">
            <td class="normaltext" width="40%%" align="center"> %s </td>
            <td class="normaltext" width="30%%" align="center"> %d </td>
            <td class="normaltext" width="30%%" align="center"> %.2f </td>
          </tr>
"""

abfr11end_t = """
           <tr><td>&nbsp;</td></tr>
          </table>
          </td>
        </tr>
      <tr>
      <td class="legendtext" align="center"> <fieldset>
        <table width="95%%" border="0" cellpadding="1">
          <tr height="40">
            <td align="center" valign="middle" width="34%%">
              <input type="button" value="Zur&uuml;ck" class="button" onClick="javascript:history.back()" name="button">
            </td>
          </tr>
        </table>
        </fieldset>
      </td>
    </tr>
  </form>
</table>
</body>
</html>"""

abfr11ages_t ="""
</head>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000" onLoad="document.formabfr11.jahrvon.focus();">
<table width="735" align="center">
  <form action="formabfr11" method="post" name="formabfr11">
    <tr>
      <td class="legendtext" align="center"><fieldset><legend class="legendtext"><b>Zeitraum f&uuml;r
        die Abfrage</b></legend>
        <table width="95%%" cellpadding="0">
          <tr align="center">
            <td class="labeltext" width="25%%" height="44">Von Jahr: </td>
            <td class="labeltext" width="25%%" height="44">Bis Jahr: </td>
          </tr>
          <tr align="center">
            <td class="labeltext" width="25%%">
              <input type="text" size="2" maxlength=4 name="jahrvon" class="textboxmid">
            </td>
            <td class="labeltext" width="25%%">
              <input type="text" size="2" maxlength=4 name="jahrbis" class="textboxmid">
            </td>
          </tr>
          <tr>
            <td colspan="2">&nbsp;</td>
          </tr>
        </table>
        </fieldset>
      </td>
    </tr>
    <tr>
      <td class="legendtext" align="center">
           <fieldset>
        <table width="95%%" border="0" cellpadding="1">
          <tr height="40">
            <td width="33%%" align="center" valign="middle">
              <input type="submit" name="Input" value="&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Ok&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" class="button">
            </td>
            <td align="center" valign="middle" width="33%%">
              <input type="reset" value="Zur&uuml;cksetzen" class="button" name="reset">
            </td>
            <td align="center" valign="middle" width="34%%">
              <input type="button" value="Abbrechen" class="button" onClick="javascript:history.back()" name="button">
            </td>
          </tr>
        </table>
        </fieldset>
  </form>
</table>
</body>
</html>
"""

##abfr12

abfr12ages_t ="""
</head>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000" onLoad="document.formabfr12.jahrvon.focus();">
<table width="735" align="center">
  <form action="formabfr12" method="post" name="formabfr12">
    <tr>
      <td class="legendtext" align="center"><fieldset><legend class="legendtext"><b>Bedingungen f&uuml;r
        die Abfrage</b></legend>
        <table width="95%%" cellpadding="0">
          <tr align="center">
            <td class="labeltext" width="25%%" height="44">Von Jahr: </td>
            <td class="labeltext" width="25%%" height="44">Bis Jahr: </td>
            <td align="center" class="labeltext">Leistung: </td>
          </tr>
          <tr align="center">
            <td class="labeltext" width="25%%">
              <input type="text" size="2" maxlength=4 name="jahrvon" class="textboxmid">
            </td>
            <td class="labeltext" width="25%%">
              <input type="text" size="2" maxlength=4 name="jahrbis" class="textboxmid">
            </td>
            <td align="center" class="labeltext">
              <select name="leistung" class="listbox">"""

abfr12ages2_t = """
                <select>
              </select>
            </td>
          </tr>
          <tr>
            <td colspan="4">&nbsp;</td>
          </tr>
        </table>
        </fieldset> </td>
    </tr>
    <tr>
      <td class="legendtext" align="center"> <fieldset>
        <table width="95%%" border="0" cellpadding="1">
          <tr height="40">
            <td width="33%%" align="center" valign="middle">
              <input type="submit" name="Input" value="&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Ok&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" class="button">
            </td>
            <td align="center" valign="middle" width="33%%">
              <input type="reset" value="Zur&uuml;cksetzen" class="button" name="reset">
            </td>
            <td align="center" valign="middle" width="34%%">
              <input type="button" value="Abbrechen" class="button" onClick="javascript:history.back()" name="button">
            </td>
          </tr>
        </table>
        </fieldset>
      </td>
    </tr>
  </form>
</table>
</body>
</html>
"""

thabfr12_t = """
</head>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000">
<table width="735" align="center">
  <form method="post">
    <tr>
      <td class="legendtext" align="center"><fieldset><legend class="legendtext">Abgeschlossene Beratungsf&auml;lle - gleiche Dauer und der Leistung %s</b></legend>
        <table width="95%%" cellpadding="0">
          <tr align="left">
            <td class="labeltext"> Beratungsdauer in Monaten: </td>
            <td class="labeltext"> Anzahl der F&auml;lle:</td>
            <td class="labeltext"> Prozentsatz:</td>
          </tr>
          """

abfr12mid_t = """
          <tr align="left" bgcolor="#FFFFFF">
            <td class="normaltext" width="40%%" align="center">%s</td>
            <td class="normaltext" width="30%%" align="center">%d</td>
            <td class="normaltext" width="30%%" align="center"> %.2f</td>
          </tr>
"""

abfr12end_t = """
          <tr><td colspan="3">&nbsp;</td></tr>
          <tr>
        </table>
        </td>
        </tr>
        <tr>
      <td class="legendtext" align="center"> <fieldset>
        <table width="95%%" border="0" cellpadding="1">
          <tr height="40">
            <td align="center" valign="middle" width="34%%">
              <input type="button" value="Zur&uuml;ck" class="button" onClick="javascript:history.back()" name="button">
            </td>
          </tr>
        </table>
        </fieldset>
      </td>
    </tr>
      </form>
</table>
</body>
</html>"""



##abfr13

thabfr13_t = """
</head>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000">
<table width="735" align="center">
  <form method="post">
    <tr>
      <td class="legendtext" align="center"><fieldset><legend class="legendtext"><b>&Uuml;bersicht abgeschlossene Beratungsf&auml;lle - gleiches Merkmal x f&uuml;r %s bis %s</b></legend>
        <table width="95%%" cellpadding="0">
          <tr align="left">
            <td class="labeltext"> Stelle:</td>
            <td class="labeltext">  Herkunft:</td>
            <td class="labeltext">  Beruf:</td>
            <td class="labeltext">  Qualifikation:</td>
            <td class="labeltext">  Altersgruppe:</td>
          </tr>
          """

abfr13ges_t = """
          <tr align="center" bgcolor="#FFFFFF">
            <td class="normaltext">%s </td>
            <td class="normaltext">%d</td>
            <td class="normaltext">%d</td>
            <td class="normaltext">%d</td>
            <td class="normaltext">%d</td>
          </tr>
          <tr><td colspan="5">&nbsp;</td></tr>
       </table>
      </td>
    </tr>
"""

abfr13start_t = """
    <tr>
      <td class="legendtext" align="center"><fieldset><legend class="legendtext"><b>%s</b></legend>
        <table width="95%%" cellpadding="0">
          <tr align="left">
            <td class="labeltext"> Merkmal:</td>
            <td class="labeltext"> Anzahl:</td>
          </tr>
          """

abfr13mid_t = """
          <tr align="left" bgcolor="#FFFFFF">
            <td class="normaltext" width="50%%" align="center">%s</td>
            <td class="normaltext" width="50%%" align="center">%s</td>
          </tr>
"""

abfr13end_t = """
        <tr><td colspan="2">&nbsp;</td></tr>
        </table>
        </fieldset>
      </td>
    </tr>"""

all_end_abfr13_t = """
  <tr>
    <td class="legendtext" align="center">
      <fieldset>
        <table width="95%%" border="0" cellpadding="1">
          <tr height="40">
            <td align="center" valign="middle" width="34%%">
              <input type="button" value="Zur&uuml;ck" class="button" onClick="javascript:history.back()" name="button">
            </td>
          </tr>
        </table>
        </fieldset>
      </td>
    </tr>
  </form>
</table>
</body>
</html>"""

abfr13enda_t = """
      </form>
</table>
</body>
</html>
"""


abfr13ages_t ="""
</head>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000" onLoad="document.formabfr13.jahrvon.focus();">
<table width="735" align="center">
  <form action="formabfr13" method="post" name="formabfr13">
    <tr>
      <td class="legendtext" align="center"><fieldset><legend class="legendtext"><b>Zeitraum f&uuml;r
        die Abfrage</b></legend>
        <table width="95%%" cellpadding="0">
          <tr align="center">
            <td class="labeltext" width="25%%" height="44">Von Jahr: </td>
            <td class="labeltext" width="25%%" height="44">Bis Jahr: </td>
          </tr>
          <tr align="center">
            <td class="labeltext" width="25%%">
              <input type="text" size="2" maxlength=4 name="jahrvon" class="textboxmid">
            </td>
            <td class="labeltext" width="25%%">
              <input type="text" size="2" maxlength=4 name="jahrbis" class="textboxmid">
            </td>
          </tr>
          <tr>
            <td colspan="2">&nbsp;</td>
          </tr>
        </table>
        </fieldset> </td>
    </tr>
    <tr>
      <td class="legendtext" align="center"> <fieldset>
        <table width="95%%" border="0" cellpadding="1">
          <tr height="40">
            <td width="33%%" align="center" valign="middle">
              <input type="submit" name="Input" value="&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Ok&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" class="button">
            </td>
            <td align="center" valign="middle" width="33%%">
              <input type="reset" value="Zur&uuml;cksetzen" class="button" name="reset">
            </td>
            <td align="center" valign="middle" width="34%%">
              <input type="button" value="Abbrechen" class="button" onClick="javascript:history.back()" name="button">
            </td>
          </tr>
        </table>
        </fieldset>
  </form>
</table>
</body>
</html>
"""





##abfr14

thabfr14_t = """
</head>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000">
<table width="735" align="center">
  <form method="post">
    <tr>
      <td class="legendtext" align="center"><fieldset><legend class="legendtext"><b>&Uuml;bersicht abgeschlossene Beratungsf&auml;lle - 1 Elternteil hat Merkmal x f&uuml;r %s bis %s</b></legend>
        <table width="95%%" cellpadding="0">
          <tr align="left">
            <td class="labeltext"> Stelle:</td>
            <td class="labeltext">  Herkunft:</td>
            <td class="labeltext">  Beruf:</td>
            <td class="labeltext">  Qualifikation:</td>
            <td class="labeltext">  Altersgruppe:</td>
          </tr>
          """

abfr14ges_t = """
          <tr align="center" bgcolor="#FFFFFF">
            <td class="normaltext">%s </td>
            <td class="normaltext">%d</td>
            <td class="normaltext">%d</td>
            <td class="normaltext">%d</td>
            <td class="normaltext">%d</td>
          </tr>
          <tr><td colspan="5">&nbsp;</td></tr>
       </table>
      </td>
    </tr>
"""


abfr14start_t = """
    <tr>
      <td class="legendtext" align="center"><fieldset><legend class="legendtext"><b>%s</b></legend>
        <table width="95%%" cellpadding="0">
          <tr align="left">
            <td class="labeltext"> Merkmal:</td>
            <td class="labeltext"> Anzahl:</td>
          </tr>
          """

abfr14mid_t = """
          <tr align="left" bgcolor="#FFFFFF">
            <td class="normaltext" width="50%%" align="center">%s</td>
            <td class="normaltext" width="50%%" align="center">%s</td>
          </tr>
"""

abfr14end_t = """
        <tr><td colspan="2">&nbsp;</td></tr>
        </table>
        </fieldset>
      </td>
    </tr>"""

abfr14enda_t = """
      </form>
</table>
</body>
</html>
"""


abfr14ages_t ="""
</head>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000" onLoad="document.formabfr14.jahrvon.focus();">
<table width="735" align="center">
  <form action="formabfr14" method="post" name="formabfr14">
    <tr>
      <td class="legendtext" align="center"><fieldset><legend class="legendtext"><b>Zeitraum f&uuml;r
        die Abfrage</b></legend>
        <table width="95%%" cellpadding="0">
          <tr align="center">
            <td class="labeltext" width="25%%" height="44">Von Jahr: </td>
            <td class="labeltext" width="25%%" height="44">Bis Jahr: </td>
          </tr>
          <tr align="center">
            <td class="labeltext" width="25%%">
              <input type="text" size="2" maxlength=4 name="jahrvon" class="textboxmid">
            </td>
            <td class="labeltext" width="25%%">
              <input type="text" size="2" maxlength=4 name="jahrbis" class="textboxmid">
            </td>
          </tr>
          <tr>
            <td colspan="2">&nbsp;</td>
          </tr>
        </table>
        </fieldset> </td>
    </tr>
    <tr>
      <td class="legendtext" align="center"> <fieldset>
        <table width="95%%" border="0" cellpadding="1">
          <tr height="40">
            <td width="33%%" align="center" valign="middle">
              <input type="submit" name="Input" value="&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Ok&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" class="button">
            </td>
            <td align="center" valign="middle" width="33%%">
              <input type="reset" value="Zur&uuml;cksetzen" class="button" name="reset">
            </td>
            <td align="center" valign="middle" width="34%%">
              <input type="button" value="Abbrechen" class="button" onClick="javascript:history.back()" name="button">
            </td>
          </tr>
        </table>
        </fieldset> </td>
    </tr>
  </form>
</table>
</body>
</html>
"""


all_end_abfr14_t = """
  <tr>
    <td class="legendtext" align="center">
      <fieldset>
        <table width="95%%" border="0" cellpadding="1">
          <tr height="40">
            <td align="center" valign="middle" width="34%%">
              <input type="button" value="Zur&uuml;ck" class="button" onClick="javascript:history.back()" name="button">
            </td>
          </tr>
        </table>
        </fieldset>
      </td>
    </tr>
  </form>
</table>
</body>
</html>"""
