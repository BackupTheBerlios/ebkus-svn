# coding: latin-1
##*************************************************************************
##  Gruppenkartei (Gruppenmenü)
##
##*************************************************************************

gruppenmenu_t = """
</head>
<BODY bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000">
<FORM ACTION="gruppenkarte" METHOD="post">
  <table width="735" align="center">
    <tr>
      <td>
        <table width="95%%" border="0" align="center" height="306">
          <tr>
            <td colspan="2" align="center" height="20">
              <table width="100%%" height="20">
                <tr>
                  <td align="center" colspan="2"> <img border="0" src="/ebkus/ebkus_icons/ebkus_logo.gif">
                  </td>
                </tr>
              </table>
            </td>
          </tr>
          <tr>
            <td width="45%%" align="center" valign="top" height="238">
              <table width="326" border="0" height="212">
                <tr>
                  <td align="center" valign="top" width="155" legend class="legendtext" height="61"><fieldset><legend class="legendtext"><b>Neu</b></legend>
                    <table width="140" height="31">
                      <tr>
                        <td align="left" class="labeltext" height="31">
                          <input type="radio" value="gruppeneu" name="file" title="Neue Gruppe anlegen.">
                          Gruppe </td>
                      </tr>
                    </table>
                    </fieldset> </td>
                  <td align="center" valign="top" width="153" legend class="legendtext" rowspan="2"><fieldset><legend class="legendtext"><b>Ansicht</b></legend>
                    <table width="140" border="0" height="110">
                      <tr>
                        <td class="labeltext" height="37">
                          <input type="radio" value="gruppeteiln" name="file"  title="Teilnehmer ansehen.">
                          Teilnehmer </td>
                      </tr>
                      <tr>
                        <td class="labeltext" height="35">
                          <input type="radio" value="gruppenkarte" name="file" title="Gruppenkarte ansehen.">
                          Gruppenkarte </td>
                      </tr>
                      <tr>
                        <td class="labeltext" height="41">
                          <input type="radio" value="hauptmenue" name="file" title="Zum Hauptmen&uuml;.">
                          Hauptmen&uuml;</td>
                      </tr>
                    </table>
                    </fieldset></td>
                </tr>
                <tr>
                  <td align="center" valign="top" width="155" legend class="legendtext"><fieldset><legend class="legendtext"><b>Suche</b></legend>
                    <table width="140" border="0">
                      <tr>
                        <td class="labeltext" align="left">
                          <input type="radio" value="formabfr3" name="file" title="Suchen einer Klientenkarte">
                          Klientenkarte</td>
                      </tr>
                      <tr>
                        <td class="labeltext" align="left" height="28">
                          <input type="radio" value="formabfr3" name="file" title="Suchen einer Gruppenkarte">
                          Gruppenkarte</td>
                      </tr>
                    </table>
                    </fieldset> </td>
                </tr>
                <tr>
                  <td align="center" valign="top" height="42" colspan="2" legend class="legendtext">
                    <fieldset>
                    <table width="97%">
                      <tr>
                        <td align="center" height="42" width="50%">
                          <input type="submit" value="&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Ok&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;" class="button" name="submit2">
                        </td>
                        <td align="center" height="42" width="50%">
                          <input type="reset"  value="Zur&uuml;cksetzen" class="button" name="reset2">
                        </td>
                      </tr>
                    </table>
                    </fieldset> </td>
                </tr>
              </table>
            </td>
            <td width="55%%" height="238" align="center" valign="top">
              <table width="100%%" border="0" height="235">
                <tr>
                  <td valign="top" align="center" legend class="legendtext" height="232"><fieldset><legend class="legendtext"><b>Gruppe</b></legend>
                    <table cellpadding=0 width="333" border="0" height="188" align="center">
                      <tr>
                        <td align="center" valign="top" height="181">
                          <select style="width:330" size="10" width=330 name="gruppeid" class="listbox">"""

gruppenmenu_auswahl_t = """
                            <option value="%(gruppe_id)s" >%(mit_id__na)s | %(gruppe_id__name)s"""
gruppemenu_ende_t = """
                          </select>
                        </td>
                      </tr>
                    </table>
                    </fieldset></td>
                </tr>
              </table>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</form>
</BODY>
</html>
"""
##** Ende Templates Gruppenkartei (Gruppenmenü) ***************************

##*************************************************************************
##  Erstellen einer neuen Gruppe
##
##*************************************************************************
gruppe_neu_t = """
</head>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000" onLoad="document.gruppeneuform.name.focus();">
<table width="735" align="center" height="362">
  <tr>
    <td align="center" valign="top" height="441">
      <form name="gruppeneuform" method="post" action="gruppenkarte">
"""

gruppe_neu_t2 = """
        <table border="0" cellpadding="1" width="95%%">
          <tr>
            <td align="center" class="legendtext" valign="top" width="50%%"> <fieldset><legend>Neue
              Gruppe %(gn)s</legend>
              <table width="89%%" border="0" cellpadding="1" height="255">
                <tr>
                  <td align="left" height="20" valign="middle" class="normaltext" width="95%%">Gruppenname:</td>
                </tr>
                <tr>
                  <td align="left" valign="middle" class="normaltext" width="95%%">
                    <input type="text" size="20" maxlength="255" name="name" value="" width=290 style="width:290">
                  </td>
                </tr>
                <tr>
                  <td align="left" height="20" valign="middle" class="normaltext" width="95%%">Gruppenthema:</td>
                </tr>
                <tr>
                  <td align="left" valign="middle" class="normaltext" width="95%%" height="170">
                    <textarea wrap=off rows="7" class="textbox" width=290 style="width:290" name="thema"></textarea>
                  </td>
                </tr>
              </table>
              </fieldset> </td>
            <td align="center" class="legendtext" valign="top"> <fieldset><legend class="legendtext">Gruppendetails</legend>
              <table border="0" width="260" height="255">
                <tr>"""

gruppe_neu_datum_t ="""
                  <td align="right" height="35" class="labeltext">Beginndatum:</td>
                  <td align="left" height="35">
                    <table>
                      <tr>
                      <td>
                    <input type="text" size=2 maxlength=2 value="" name="bgd" class="textboxsmall">
                      </td>
                      <td>.</td>
                      <td>
                    <input type="text" size="2" maxlength=2 value="%(month)d" name="bgm" class="textboxsmall">
                      </td>
                      <td>.</td>
                      <td>
                    <input type="text" size="4" maxlength=4 value="%(year)d" name="bgy" class="textboxmid">
                      </td>
                    </tr>
                  </table>
                  </td>
                </tr>"""

gruppe_neu_teilnehmer_t = """
                <tr>
                  <td align="right" height="25" class="labeltext">Teilnehmer:</td>
                  <td align="left" height="25">
                    <select name="teiln" style="width:150">"""

gruppe_neu_mitarbeiter_t = """
                    </select>
                  </td>
                </tr>
                <tr>
                  <td height="54" align="right" class="labeltext">Mitarbeiter:</td>
                  <td height="54" align="left">
                    <select multiple size="3" name="mitid" style="width:150" width=150>"""


gruppe_neu_gruppenart_t = """
                    </select>
                  </td>
                </tr>
                <tr>
                  <td align="right" class="labeltext" height="35">Endedatum:</td>
                  <td align="left" height="35">
                    <table>
                      <tr>
                      <td>
                    <input type="text" size=2 maxlength=2 name="ed" class="textboxsmall">
                      </td>
                    <td>.</td>
                    <td>
                    <input type="text" size=2 maxlength=2 name="em" class="textboxsmall">
                      </td>
                    <td>.</td>
                    <td>
                    <input type="text" size=4 maxlength=4 name="ey" class="textboxmid">
                    </td>
                    </tr>
                    </table>
                  </td>
                </tr>
                <tr>
                  <td align="right" class="labeltext" height="26">Gruppenart:</td>
                  <td align="left" height="26">
                    <select name="grtyp" style="width:150">"""

gruppe_neu_ende_t = """
                    </select>
                  </td>
                </tr>
                <tr>
                  <td align="right" class="labeltext" height="27">Teilnehmerzahl:</td>
                  <td align="left" height="27"><b>
                    <input type="text" name="tzahl" size="3" maxlength="3">
                    </b></td>
                </tr>
                <tr>
                  <td align="right" class="labeltext">Stundenzahl:</td>
                  <td align="left"><b>
                    <input type="text" name="stzahl" size="3" maxlength="3">
                    </b></td>
                </tr>
              </table>
              </fieldset> </td>
          </tr>
          <tr>
            <td align="center" class="legendtext" valign="middle" colspan="2">
              <fieldset>
              <table width="95%%" border="0" cellpadding="1">
                <tr height="40">
                  <td width="33%%" align="center" valign="middle">
                    <input type="submit" name="" value="Speichern" class="button">
                  </td>
                  <td align="center" valign="middle" width="33%%">
                    <input type="reset" value="Zur&uuml;cksetzen" class="button">
                  </td>
                  <td align="center" valign="middle" width="34%%">
                    <input type="button" value="Abbrechen" class="button" onClick="javascript:history.back()">
                  </td>
                </tr>
              </table>
              </fieldset></td>
          </tr>
        </table>
      </form>
    </td>
  </tr>
</table>
</body>
</html>
"""

##** Erstellen einer neuen Gruppe *****************************************

##*************************************************************************
##  Bearbeiten der Eigenschaften einer Gruppe
##
##*************************************************************************
gruppe_upd_t = """
</head>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000" onLoad="document.gruppeneuform.name.focus();">
<table width="735" align="center" height="362">
  <tr>
    <td align="center" valign="top" height="441">
      <form name="gruppeneuform" method="post" action="gruppenkarte">
        <table border="0" cellpadding="1" width="95%%">
          <tr>
            <td align="center" class="legendtext" valign="top" width="50%%"> <fieldset><legend>Bearbeiten der Gruppe %(gn)s</legend>
              <table width="89%%" border="0" cellpadding="1" height="255">
                <tr>
                  <td align="left" height="20" valign="middle" class="normaltext" width="95%%">Gruppenname:</td>
                </tr>
                <tr>
                  <td align="left" valign="middle" class="normaltext" width="95%%">
                    <input type="text" size="20" width=290 maxlength="255" name="name" value="%(name)s" style="width:290">
                  </td>
                </tr>
                <tr>
                  <td align="left" height="20" valign="middle" class="normaltext" width="95%%">Gruppenthema:</td>
                </tr>
                <tr>
                  <td align="left" valign="middle" class="normaltext" width="95%%" height="170">
                    <textarea wrap=off class="textbox" style="width:290" width=290 rows="7" name="thema">%(thema)s</textarea>
                  </td>
                </tr>
              </table>
              </fieldset> </td>
            <td align="center" class="legendtext" valign="top"> <fieldset><legend class="legendtext">Gruppendetails</legend>
              <table border="0" width="260" height="255">
                <tr>"""

gruppe_upd_datum_t ="""
                  <td align="right" height="35" class="labeltext">Beginndatum:</td>
                  <td align="left" height="35">
                    <table>
                      <tr>
                      <td>
                    <input type="text" size=2 maxlength=2 value="%(bgd)d" class="textboxsmall" name="bgd">
                      </td>
                      <td>.</td>
                      <td>
                    <input type="text" size=2 maxlength=2 value="%(bgm)d" class="textboxsmall" name="bgm">
                      </td>
                      <td>.</td>
                      <td>
                    <input type="text" size=4 maxlength=4 value="%(bgy)d" class="textboxmid" name="bgy">
                      </td>
                      </tr>
                    </table>
                  </td>
                </tr>"""

gruppe_upd_teilnehmer_t = """
                <tr>
                  <td align="right" height="25" class="labeltext">Teilnehmer:</td>
                  <td align="left" height="25">
                    <select name="teiln" style="width:150">"""

gruppe_upd_mitarbeiter_t = """
                    </select>
                  </td>
                </tr>
                <tr>
                  <td height="54" align="right" class="labeltext">Mitarbeiter:</td>
                  <td height="54" align="left">
                    <select multiple size="3" style="width:150" width=150 name="mitid">"""

gruppe_sel_mit_t = """
<option value="%(id)d" selected>%(na)s"""

gruppe_notsel_mit_t = """
<option value="%(id)d">%(na)s"""


gruppe_upd_gruppenart_t = """
                    </select>
                  </td>
                </tr>
                <tr>
                  <td align="right" class="labeltext" height="35">Endedatum:</td>
                  <td align="left" height="35">
                    <table>
                      <tr>
                      <td>
                    <input type="text" size="2" maxlength=2 value="%(ed)d" class="textboxsmall" name="ed">
                      </td>
                      <td>.</td>
                      <td>
                    <input type="text" size="2" maxlength=2 value="%(em)d" class="textboxsmall" name="em">
                      </td>
                      <td>.</td>
                      <td>
                    <input type="text" size="4" maxlength=4 value="%(ey)d" class="textboxmid" name="ey">
                      </td>
                      </tr>
                    </table>
                  </td>
                </tr>
                <tr>
                  <td align="right" class="labeltext" height="26">Gruppenart:</td>
                  <td align="left" height="26">
                    <select name="grtyp" style="width:150">"""

gruppe_upd_ende_t = """
                    </select>
                  </td>
                </tr>
                <tr>
                  <td align="right" class="labeltext" height="27">Teilnehmerzahl:</td>
                  <td align="left" height="27"><b>
                    <input type="text" name="tzahl" value="%(tzahl)d" size="3" maxlength="3">
                    </b></td>
                </tr>
                <tr>
                  <td align="right" class="labeltext">Stundenzahl:</td>
                  <td align="left"><b>
                    <input type="text" name="stzahl" value="%(stzahl)d" size="3" maxlength="3">
                    </b></td>
                </tr>
              </table>
              </fieldset> </td>
          </tr>
          <tr>
            <td align="center" class="legendtext" valign="middle" colspan="2">
              <fieldset>
              <table width="95%%" border="0" cellpadding="1">
                <tr height="40">
                  <td width="33%%" align="center" valign="middle">
                    <input type="submit" name="" value="Speichern" class="button">
                  </td>
                  <td align="center" valign="middle" width="33%%">
                    <input type="reset" value="Zur&uuml;cksetzen" class="button">
                  </td>
                  <td align="center" valign="middle" width="34%%">
                    <input type="button" value="Abbrechen" class="button" onClick="javascript:history.back()">
                  </td>
                </tr>
              </table>
              </fieldset></td>
          </tr>
        </table>
      </form>
    </td>
  </tr>
</table>
</body>
</html>
"""
##** Bearbeiten der Eigenschaften einer Gruppe ****************************


##*************************************************************************
##  Hinzufügen eines Teilnehmers zu einer Gruppe
##
##*************************************************************************

teilnauswahl_form_t = """
</head>
<BODY bgcolor=#CCCCCC link="#CCCCCC" vlink="#CCCCCC" alink="#000000">
<FORM ACTION="gruppenkarte" METHOD="post">
<input type="hidden" value="%(id)d" name="gruppeid">"""

teilnauswahl_t = """
  <table width="776" align="center">
    <tr>
      <td width="747" align="center" valign="top" height="358">
        <table width="92%%" border="0" align="center">
          <tr>
            <td align="center" class="legendtext" valign="top"> <fieldset><legend class="legendtext"><b>Fall (Kind / Jugendlicher)</b></legend>
              <table width="95%%" border="0" height="195">
                <tr>
                  <td height="188" align="center">
                    <select multiple class="listbox" style="width:250" size="10" name="fallid">"""

teilnauswahl1_t = """
                      <option value="%(fall_id)s">%(fall_id__akte_id__na)s %(fall_id__akte_id__vn)s|
                      %(fall_id__fn)s"""
teilnauswahl2_t = """
                    </select>
                  </td>
                </tr>
              </table>
              </fieldset> </td>
            <td align="center" valign="top" class="legendtext"> <fieldset><legend class="legendtext"><b>Familienangeh&ouml;rige</b></legend>
              <table width="95%%" border="0" height="195">
                <tr>
                  <td height="183" align="center">
                    <select class="listbox" style="width:250" name="bezugspid" multiple size="10">"""

teilnauswahl3_t = """
                      <option value="%(id)s">%(na)s %(vn)s | %(fn)s """

teilnauswahl4_t = """
                    </select>
                  </td>
                </tr>
              </table>
              </fieldset> </td>
          </tr>
          <tr>
            <td align="center" class="legendtext" valign="top"> <fieldset><legend class="legendtext"><b>Beginndatum:</b></legend>
              <table width="95%%" border="0">
                <tr>
                  <td height="30" align="center">
                  <table>
                    <tr>
                    <td>
                      <input type="text" size=2 maxlength=2 value=""  name="bgd" class="textboxsmall">
                    </td>
                    <td>.</td>
                    <td>
                    <input type="text" size=2 maxlength=2 value="%(month)d" name="bgm" class="textboxsmall">
                    </td>
                    <td>.</td>
                    <td>
                    <input type="text" size=4 maxlength=4 value="%(year)d" name="bgy" class="textboxmid">
                    </td>
                   </tr>
                  </table>
                  </td>
                </tr>
              </table>
                          </fieldset>
            </td>
            <td align="center" class="legendtext" valign="top"> <fieldset><legend class="legendtext"><b>Endedatum:</b></legend>
              <table width="95%%" border="0">
                <tr>
                  <td height="30" align="center">
                  <table>
                    <tr>
                    <td>
                    <input type="text" size=2 maxlength=2 name="ed" class="textboxsmall">
                    </td>
                    <td>.</td>
                    <td>
                    <input type="text" size=2 maxlength=2 name="em" class="textboxsmall">
                    </td>
                    <td>.</td>
                    <td>
                    <input type="text" size=4 maxlength=4 name="ey" class="textboxmid">
                    </td>
                   </tr>
                  </table>
                  </td>
                </tr>
              </table>
              </fieldset>
            </td>
          </tr>
                  <tr>
            <td align="center" class="legendtext" valign="middle" colspan="2">
              <fieldset>
              <table width="95%%" border="0" cellpadding="1">
                <tr height="40">
                  <td width="33%%" align="center" valign="middle">
                    <input type="submit" name="" value="Speichern" class="button">
                  </td>
                  <td align="center" valign="middle" width="33%%">
                    <input type="reset" value="Zur&uuml;cksetzen" class="button">
                  </td>
                  <td align="center" valign="middle" width="34%%">
                    <input type="button" value="Abbrechen" class="button" onClick="javascript:history.back()">
                  </td>
                </tr>
              </table>
              </fieldset></td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</form>
</body>
</html>"""

##** Hinzufügen eines Teilnehmers zu einer Gruppe *************************

##*************************************************************************
##  Templates für die Teilnehmerliste
##
##*************************************************************************

teilnehmerliste_t = """
</head>
<BODY bgcolor=#CCCCCC link="#CCCCCC" vlink="#CCCCCC" alink="#000000">
<table width="735" align="center">
<tr>
<td colspan="3" bgcolor="#FFFFFF" align="center" class="legendtext">Teilnehmerliste der Gruppe: %s</td>
</tr>
<tr>
<td colspan="3" bgcolor="#CCCCCC" align="center" class="legendtext">&nbsp;</td>
</tr>
<tr>
<td bgcolor="#FFFFFF" align="left" class="legendtext">Vorname, Nachname:</td>
<td bgcolor="#FFFFFF" align="left" class="legendtext">Strasse, Plz, Ort:</td>
<td bgcolor="#FFFFFF" align="left" class="legendtext">Von - Bis:</td>
</tr>"""

teilnehmerliste_fall1_t = """
  <tr>
    <td bgcolor="#FFFFFF" align="left" valign="top" height="20" width="40%%" class="normaltext">%(vn)s %(na)s </td>
    <td bgcolor="#FFFFFF" class="normaltext" width="40%%" height="20">%(str)s %(hsnr)s, %(plz)s, %(ort)s</td>
  """
teilnehmerliste_fall2_t = """
    <td bgcolor="#FFFFFF" align="left" valign="top" width="20%%" class="normaltext" height="20">%(bgd)s.%(bgm)s.%(bgy)s-%(ed)s.%(em)s.%(ey)s</td>
  </tr>"""

teilnehmerliste_bzpers1_t = """
  <tr>
    <td bgcolor="#FFFFFF" align="left" valign="top" width="40%%" height="20" class="normaltext" height="20">%(vn)s %(na)s </td>
    <td bgcolor="#FFFFFF" class="normaltext" width="40%%">%(str)s %(hsnr)s, %(plz)s, %(ort)s</td>
  """
teilnehmerliste_bzpers2_t = """
    <td bgcolor="#FFFFFF" align="left" valign="top" height="20" width="20%%" class="normaltext">%(bgd)s.%(bgm)s.%(bgy)s-%(ed)s.%(em)s.%(ey)s</td>
  </tr>"""

teilnehmerliste_ende_t ="""
<tr><td>&nbsp;</td></tr>
<tr>
<td align="center" class="legendtext" valign="middle" colspan="3">
  <fieldset>
    <table width="95%%" border="0" cellpadding="1">
    <form>
      <tr height="40">
        <td align="center" valign="middle" width="34%%">
          <input type="button" value="Zur&uuml;ck" class="button" onClick="javascript:history.back()">
        </td>
      </tr>
    </form>
    </table>
  </fieldset>
</td>
</tr>
</table>
</body>
</html>"""

##** Ende Templates für die Teilnehmerliste *******************************

##*************************************************************************
##  Templates für Teilnehmerupdates (Datumsänderung)
##
##*************************************************************************
teilnupd_t = """
<table width="735" align="center">
  <tr>
    <td align="center" class="legendtext" height="84"><fieldset><legend class="legendtext">Kind - Jugendlicher</legend>
      <table width="95%%" border="0" height="60">
        <tr>
          <td align="center">
            <table width="95%%">
              <tr>
                <td class="labeltext" class="labeltext" bgcolor="#CCCCCC" width="70" align="right">Vorname:</td>
                <td bgcolor="#FFFFFF" class="normaltext" align="left" width="226">%(fall_id__akte_id__vn)s</td>
                <td bgcolor="#CCCCCC" class="labeltext" width="76" align="right">Nachname:</td>
                <td bgcolor="#FFFFFF" class="normaltext" align="left" width="299">%(fall_id__akte_id__na)s</td>
              </tr>"""

teilnupdb_t = """
<table width="735" align="center">
  <tr>
    <td align="center" class="legendtext" height="190"><fieldset><legend class="legendtext">Bezugsperson</legend>
          <table width="95%%" border="0" height="84">
        <tr>
          <td align="center" height="72">
            <table width="95%">
              <tr>
                <td bgcolor="#CCCCCC" class="labeltext" align="right" width="81">Vorname:</td>
                <td bgcolor="#FFFFFF" class="normaltext" align="left" width="183">%(bezugsp_id__vn)s</td>
                <td bgcolor="#CCCCCC" class="labeltext" align="right" width="75">Nachname:</td>
                <td bgcolor="#FFFFFF" class="normaltext" align="left" width="186">%(bezugsp_id__na)s</td>
              </tr>"""

teilnupd1_t = """
              <tr>
                <td width="81" align="right" class="labeltext">Beginndatum:</td>
                <td width="183">
                <table>
                   <tr>
                   <td>
                   <input type="text" size="2" class="textboxsmall" maxlength=2 value="%(bgd)d"  name="bgd">
                  </td><td>.</td>
                   <td>
                  <input type="text" size="2" class="textboxsmall" maxlength=2 value="%(bgm)d" name="bgm">
                  </td><td>.</td>
                   <td>
                   <input type="text" size="4" class="textboxmid" maxlength=4 value="%(bgy)d" name="bgy">
                   </td>
                   </tr>
                  </table>
                 </td>
                <td width="75" align="right" class="labeltext">Endedatum: </td>
                <td width="186">
                 <table>
                   <tr>
                   <td>
                  <input type="text" size="2" class="textboxsmall" maxlength=2 value="%(ed)d" name="ed">
                   </td><td>.</td>
                   <td>
                  <input type="text" size="2" class="textboxsmall" maxlength=2 value="%(em)d" name="em">
                   </td><td>.</td>
                   <td>
                  <input type="text" size="4" class="textboxmid" maxlength=4 value="%(ey)d" name="ey">
                    </td>
                   </tr>
                  </table>
                </td>
            </table>
          </td>
        </tr>
        </table>
      </fieldset>
    </td>
  </tr>
  <tr>
  <td align="center" class="legendtext" valign="middle" colspan="2">
      <fieldset>
      <table width="95%%" border="0" cellpadding="1">
             <tr height="40">
                 <td width="33%%" align="center" valign="middle">
                 <input type="submit" name="" value="Speichern" class="button">
                 </td>
                 <td align="center" valign="middle" width="33%%">
                 <input type="reset" value="Zur&uuml;cksetzen" class="button">
                 </td>
                 <td align="center" valign="middle" width="34%%">
                 <input type="button" value="Abbrechen" class="button" onClick="javascript:history.back()">
                 </td>
             </tr>
      </table>
      </fieldset>
  </td>
  </tr>
</table>
</form>
</body>
</html>"""
##** Templates für Teilnehmerupdates (Datumsänderung) *********************


##*************************************************************************
##  Templates für das Löschen von Teilnehmern aus einer Gruppe
##
##*************************************************************************

teilnauswahl_loesch_t = """
  <table width="776" align="center">
    <tr>
      <td width="747" align="center" valign="top" height="358">
        <table width="92%%" border="0" align="center">
          <tr>
            <td align="center" class="legendtext" valign="top"> <fieldset><legend class="legendtext"><b>Fall (Kind / Jugendlicher)</b></legend>
              <table width="95%%" border="0" height="195">
                <tr>
                  <td height="188" align="center">
                    <select multiple class="listbox" style="width:250" size="10" name="fallid">"""

teilnauswahl1_loesch_t = """
                      <option value="%(id)s">%(fall_id__akte_id__na)s %(fall_id__akte_id__vn)s| %(fall_id__fn)s"""

teilnauswahl2_loesch_t = """
                    </select>
                  </td>
                </tr>
              </table>
              </fieldset> </td>
            <td align="center" class="legendtext" valign="top"> <fieldset><legend class="legendtext"><b>Familienangeh&ouml;rige</b></legend>
              <table width="95%%" border="0" height="195">
                <tr>
                  <td height="183" align="center">
                    <select class="listbox" style="width:250" name="bezugspid" multiple size="10">"""

teilnauswahl3_loesch_t = """
                      <option value="%(id)s">%(bezugsp_id__na)s %(bezugsp_id__vn)s"""

teilnauswahl4_loesch_t = """
                    </select>
                  </td>
                </tr>
              </table>
              </fieldset> </td>
          </tr>
                  <tr>
            <td align="center" class="legendtext" valign="middle" colspan="2">
              <fieldset>
              <table width="95%%" border="0" cellpadding="1">
                <tr height="40">
                  <td width="33%%" align="center" valign="middle">
                    <input type="submit" name="" value="L&ouml;schen" class="button">
                  </td>
                  <td align="center" valign="middle" width="33%%">
                    <input type="reset" value="Zur&uuml;cksetzen" class="button">
                  </td>
                  <td align="center" valign="middle" width="34%%">
                    <input type="button" value="Abbrechen" class="button" onClick="javascript:history.back()">
                  </td>
                </tr>
              </table>
              </fieldset></td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</form>
</body>
</html>"""
##** Templates für das Löschen von Teilnehmern aus einer Gruppe ***********