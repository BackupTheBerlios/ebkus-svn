# coding: latin-1
##Mitarbeiterauswahl

mitauswstart_t = """
</HEAD>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000">
<table width="735" align="center">
  <tr>
    <td align="center" valign="top">
      <table border="0" cellpadding="1" width="95%">
        <tr>
          <td align="center" class="legendtext"> """


menuemit_t = """ <fieldset><legend class="legendtext">Steuerung</legend>
            <table border="0" cellpadding="1" width="50%%" height="30">
              <tr valign="top">
                <td align="center" height="30">
                  <input type="button" name="Schaltfl&auml;che" onClick="go_to_url('menu')" value="Hauptmen&uuml;" class="button">
                </td>
              </tr>
            </table>
            </fieldset>
            </td>
          <td align="center" class="legendtext"> <fieldset><legend class="legendtext">Mitarbeiter</legend>
            <table border="0" cellpadding="1" height="30">
              <tr>
                <td align="center" class="smalltext" height="30">
                  <A HREF="mitneu"><img border="0" src="/ebkus/ebkus_icons/teilnehmer_neu_button.gif"></A>
                  <A HREF="mitausw"><img border="0" src="/ebkus/ebkus_icons/teilnehmer_edit_button.gif"></A>
                  <A HREF="codetab?tabelle=Mitarbeiter">
                  <img border="0" src="/ebkus/ebkus_icons/mitarbeiter_merkmale_button.gif"></A>
                </td>
              </tr>
            </table>
            </fieldset> </td>"""

mitausw_anz = """
        </tr>
        <tr>
          <td colspan="2" class="legendtext" align="center"><fieldset><legend class="legendtext">Mitarbeiterliste</legend>
           <table width="95%">
              <tr>
                <td class="labeltext" align="left" "bgcolor=#CCCCCC">Vorname:</td>
                <td class="labeltext" align="left" "bgcolor=#CCCCCC">Name:</td>
                <td class="labeltext" align="left" "bgcolor=#CCCCCC">Benutzer:</td>
                <td class="labeltext" align="left" "bgcolor=#CCCCCC">Status:</td>
                <td class="labeltext" align="left" "bgcolor=#CCCCCC">Rechte:</td>
                <td class="labeltext" align="left" "bgcolor=#CCCCCC">Stelle:</td>
              </tr>"""


mitlistehrefs_t = """
              <tr>
                <td class="normaltext" bgcolor="#FFFFFF" align="center"><A HREF="updmit?mitid=%(id)s">
                  %(vn)s</A></td>
                <td class="normaltext" bgcolor="#FFFFFF" align="center">%(na)s</td>
                <td class="normaltext" bgcolor="#FFFFFF" align="center">%(ben)s</td>
                <td class="normaltext" bgcolor="#FFFFFF" align="center">%(stat__name)s</td>
                <td class="normaltext" bgcolor="#FFFFFF" align="center">%(benr__code)s</td>
                <td class="normaltext" bgcolor="#FFFFFF" align="center">%(stz__name)s</td>
              </tr>
              """

mitausw_anz_ende_t = """
              <tr>
                <td colspan="6">&nbsp;</td>
              </tr>
            </table>
            </fieldset> </td>
        </tr>
      </table>
    </td>
  </tr>
</table>
</body>
</html>
"""

mitarbeiter_neu_t1 = """
</head>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000">
<table width="735" align="center">
  <tr>
    <td height="327" align="center" valign="top">
      <form name="mitneuform" method="post" action="admin">
        <table border="0" cellpadding="1" width="95%">
          <tr>
            <td align="center" class="legendtext" valign="top"> <fieldset><legend class="legendtext">Mitarbeiterdaten</legend>
              <table width="95%" border="0" cellpadding="1">
                <tr>
                  <td width="25%" class="labeltext" align="right">Vorname:</td>
                  <td width="24%" align="left">
                    <input type="text" size="10" maxlength=35 name="vn" class="textbox">
                  </td>
                  <td align="right" class="labeltext" width="14%">Status</td>
                  <td width="37%" align="left">
                    <select name="stat" class="listbox130">"""

mitarbeiter_neu_t2 = """
                    </select>
                  </td>
                </tr>
                <tr>
                  <td align="right" valign="middle" width="25%" class="labeltext">Nachname:</td>
                  <td align="left" valign="middle" width="24%">
                    <input type="text" size="10" name="na" maxlength=35 class="textbox">
                  </td>
                  <td align="right" valign="middle" class="labeltext" width="14%">Rechte:</td>
                  <td align="left" valign="middle" width="37%">
                    <select name="benr" class="listbox130">"""

mitarbeiter_neu_t3 = """
                    </select>
                  </td>
                </tr>
                <tr>
                  <td align="right" valign="middle" class="labeltext" width="25%">Benutzername:</td>
                  <td align="left" valign="middle" class="labeltext" width="24%">
                    <input type="text" size="10" maxlength=25 name="ben" class="textbox">
                  </td>
                  <td align="right" valign="middle" class="labeltext" width="14%">Stelle:</td>
                  <td align="left" valign="middle" class="labeltext" width="37%">
                    <select name="stz" class="listbox130">"""

mitarbeiter_neu_t4 = """
                    </select>
                  </td>
                </tr>
              </table>
              </fieldset> </td>
          </tr>
          <tr>
            <td align="center" class="legendtext" valign="middle"> <fieldset><legend>Mitarbeiterliste</legend>
              <table width="95%" border="0" cellpadding="1">
                <tr>
                  <td class="labeltext" align="left" "bgcolor=#CCCCCC">Vorname:</td>
                  <td class="labeltext" align="left" "bgcolor=#CCCCCC">Name:</td>
                  <td class="labeltext" align="left" "bgcolor=#CCCCCC">Benutzer:</td>
                  <td class="labeltext" align="left" "bgcolor=#CCCCCC">Status:</td>
                  <td class="labeltext" align="left" "bgcolor=#CCCCCC">Rechte:</td>
                  <td class="labeltext" align="left" "bgcolor=#CCCCCC">Stelle:</td>
                </tr>
                """

mitliste_t = """
                <tr>
                  <td class="normaltext" bgcolor="#FFFFFF" align="center"> %(vn)s </td>
                  <td class="normaltext" bgcolor="#FFFFFF" align="center"> %(na)s </td>
                  <td class="normaltext" bgcolor="#FFFFFF" align="center"> %(ben)s </td>
                  <td class="normaltext" bgcolor="#FFFFFF" align="center"> %(stat__name)s </td>
                  <td class="normaltext" bgcolor="#FFFFFF" align="center"> %(benr__code)s </td>
                  <td class="normaltext" bgcolor="#FFFFFF" align="center"> %(stz__name)s </td>
                </tr>
                """

mitarbeiter_neu_t5 = """
              <tr>
              <td>&nbsp;</td>
              </tr>
              </table>
              </fieldset> </td>
          </tr>
          <tr>
            <td align="center" class="legendtext" valign="middle"> <fieldset>
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
              </fieldset> </td>
          </tr>
        </table>
      </form>
    </td>
  </tr>
</table>
</body>
</html>
"""

mitarbeiter_upd_t1 = """
</head>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000">
<table width="735" align="center">
  <tr>
    <td colspan="2" align="center" valign="top">
      <form name="mitneuform" method="post" action="admin">
        <table border="0" cellpadding="1" width="95%%">
          <tr>
            <td align="center" class="legendtext" valign="top"> <fieldset><legend class="legendtext">Mitarbeiterdaten</legend>
              <table width="95%%" border="0" cellpadding="1">
                <tr>
                  <td width="25%%" class="labeltext" align="right">Vorname:</td>
                  <td width="24%%" align="left">
                    <input type="text" size="10" maxlength=35 value="%(vn)s" name="vn" class="textbox">
                  </td>
                  <td align="right" class="labeltext" width="14%%">Status</td>
                  <td width="37%%" align="left">
                    <select name="stat" class="listbox130">"""

mitarbeiter_upd_t2 = """
                    </select>
                  </td>
                </tr>
                <tr>
                  <td align="right" valign="middle" width="25%%" class="labeltext">Nachname:</td>
                  <td align="left" valign="middle" width="24%%">
                    <input type="text" size="10" maxlength=35 name="na" value="%(na)s" class="textbox">
                  </td>
                  <td align="right" valign="middle" class="labeltext" width="14%%">Rechte:</td>
                  <td align="left" valign="middle" width="37%%">
                    <select name="benr" class="listbox130">"""

mitarbeiter_upd_t3 = """
                    </select>
                  </td>
                </tr>
                <tr>
                  <td align="right" valign="middle" class="labeltext" width="25%%">Benutzername:</td>
                  <td align="left" valign="middle" class="labeltext" width="24%%">
                    <input type="text" size="10" maxlength=25 name="ben" value="%(ben)s" class="textbox">
                  </td>
                  <td align="right" valign="middle" class="labeltext" width="14%%">Stelle:</td>
                  <td align="left" valign="middle" class="labeltext" width="37%%">
                    <select name="stz" class="listbox130">"""

mitarbeiter_upd_t4 = """
                    </select>
                  </td>
                </tr>
                <tr>
                <td colspan=3>
                <input type="checkbox" name="changepassword" value="1">Passwort zur&uuml;cksetzen
                </td>
                </tr>
              </table>
              </fieldset> </td>
          </tr>
          <tr>
            <td align="center" class="legendtext" valign="middle"> <fieldset><legend>Mitarbeiterliste</legend>
              <table width="95%" border="0" cellpadding="1">
                <tr>
                  <td class="labeltext" align="left" "bgcolor=#CCCCCC">Vorname:</td>
                  <td class="labeltext" align="left" "bgcolor=#CCCCCC">Name:</td>
                  <td class="labeltext" align="left" "bgcolor=#CCCCCC">Benutzer:</td>
                  <td class="labeltext" align="left" "bgcolor=#CCCCCC">Status:</td>
                  <td class="labeltext" align="left" "bgcolor=#CCCCCC">Rechte:</td>
                  <td class="labeltext" align="left" "bgcolor=#CCCCCC">Stelle:</td>
                </tr>
                """

mitarbeiter_upd_t5 = """
              <tr>
              <td colspan="6">&nbsp;</td>
              </tr>
              </table>
              </fieldset> </td>
          </tr>
          <tr>
            <td align="center" class="legendtext" valign="middle"> <fieldset>
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
              </fieldset> </td>
          </tr>
        </table>
      </form>
    </td>
  </tr>
</table>
</body>
</html>
"""