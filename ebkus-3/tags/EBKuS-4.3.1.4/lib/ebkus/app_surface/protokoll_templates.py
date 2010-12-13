# coding: latin-1
protokoll_login_t= """
<script language="JavaScript">
<!--
function set_focus()
{
   document.logindaten.username1.focus();
}
// -->
</script>
</head>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000">
<table width="735" align="center">
  <tr>
    <td height="288" align="center" valign="top">
      <form name="logindaten" method="post" action="check_protokoll_login">
      <table border="0" cellpadding="1" width="95%%">
        <tr>
          <td width="45%%" align="center" class="legendtext" valign="top" height="200">
            <fieldset><legend class="legendtext">Anmeldung zur EBKuS Vorgangsprotokollierung</legend>
            <table width="90%%" border="0" cellpadding="1" height="200">
              <tr>
                <td align="right" valign="middle" height="32" class="labeltext" width="102">
                  Benutzername1: </td>
                <td align="left" valign="middle" height="32" width="148" class="12norm">
                  <input type="text" maxlength=25 name="username1" class="textbox" value="%(ben)s">
                </td>
                <td align="right" valign="middle" height="32" width="109" class="labeltext">Passwort1:
                </td>
                <td align="left" valign="middle" height="32" width="130" class="12norm">
                  <input type="password" maxlength=20 name="userpass1" class="textbox" value="%(pass)s">
                </td>
              </tr>
              <tr>
                <td align="right" valign="middle" height="37" width="102" class="labeltext">
                  Benutzername2: </td>
                <td align="left" valign="middle" height="37" width="148" class="12norm">
                  <input type="text" maxlength=25 name="username2" class="textbox">
                </td>
                <td align="right" valign="middle" height="37" width="109" class="labeltext">Passwort2:
                </td>
                <td align="left" valign="middle" height="37" width="130" class="12norm">
                  <input type="password" maxlength=20 name="userpass2" class="textbox">
                </td>
              </tr>
              <tr align="center">
                <td valign="middle" height="44" colspan="4" class="labeltext">
                  <input type="submit" name="anmeldebutton" value="Anmelden" class="button">
                </td>
              </tr>
            </table>
            </fieldset></td>
        </tr>
      </table>
          </form>
</table>
</body>
</html>"""


archivfile_anzeigen_t = """
<tr align="left">
<td>%s</td>
</tr>
"""


auswahlprotocol_t = """
</head>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000">
<table width="735" border="0" align="center">
  <tr>
    <td valign="top">
      <table align="center" width="95%%" height="469">
        <tr align="center">
          <td colspan="2" height="93">
            <table width="95%%" border="0">
              <tr>
                <td width="50%%" align="center" height="75" class="legendtext">
                  <form action="menu_protocol">
                    <fieldset><legend class="legendtext">Anzeigeeinstellungen</legend>
                    <table width="93%%" border="0">
                      <tr>
                        <td align="right" valign="middle" width="10%%" class="normaltext">von:</td>
                        <td align="left" valign="middle" width="15%%" class="normaltext">
                          <input name="von_id" size=6 maxlenght=6 type=int style="width:70" class="textboxsmall">
                        </td>
                        <td align="right" width="11%%" valign="middle" class="normaltext">bis:</td>
                        <td align="left" width="15%%" valign="middle" class="normaltext">
                          <input name="bis_id" size=6 maxlenght=6 style="width:70" type=int class="textboxsmall">
                        </td>
                        <td align="center" width="49%%" valign="middle" class="normaltext">
                          <input type="submit" value="Zeigen" style="width:70" name="submit2" class="button">
                        </td>
                      </tr>
                    </table>
                  </form>
                </td>
                <td width="50%%" align="center" class="legendtext" height="75"><fieldset><legend >Protokollierungsoptionen</legend>
                  <table width="95%%" border="0">
                    <tr align="center">
                      <td colspan="2" valign="middle">
                        <form action="menu_protocol">
                          <input type=hidden name="protocolanaus" value="protocolanaus">
                          <input type="submit" value="%sschalten" class="button" name="submit3">
                        </form>
                      </td>
                      <td valign="middle">
                        <form action="logout" method="post">
                          <input type="submit" value="Ausloggen" class="button" name="submit">
                        </form>
                      </td>
                    </tr>
                  </table>
                  </fieldset> </td>
              </tr>
            </table>
          </td>
        <tr align="center">
          <td colspan="2" height="350">
            <table width="95%%" border="0">
              <tr>
                <td align="center" class="legendtext" valign="middle"><fieldset><legend class="legendtext">Aktuelle
                  Anzeige: %s bis %s (%s) </legend>
                  <form action="menu_protocol" method="post">
                    <table width="95%%" border="0">
                      <tr>
                        <td align="center">
                          <select size=15 name="protokolleintrag"  multiple class="listbox" style="width:500">"""


protocolauswahl_t = """
                            <option value="%(nr)s" align="right"> %(nr)07d | %(zeit)s
                            | %(artdeszugriffs)0.25s | %(benutzerkennung)s | %(ipadresse)s
                            """

protocolsubmit_t = """
                          </select>
                        </td>
                      </tr>
                      <tr>
                        <td align="center">
                          <input type="submit" value="Anzeigen" class="button" name="submit4">
                        </td>
                      </tr>
                    </table>
                  </form>
                  </fieldset> </td>
              </tr>
              <tr>
                <td align="center" class="legendtext"> """

archivfile_head_t = """
                        <FORM ACTION="menu_protocol" METHOD="post">
                          <fieldset><legend class="legendtext">Archivierte Protokolle</legend>
                          <table width="95%">
                            <td align="left" bgcolor="#CCCCCC" class="labeltext">&nbsp;
                            </td>
                            <td align="left" bgcolor="#CCCCCC" class="labeltext">
                              Name: </td>
                            <td align="left" bgcolor="#CCCCCC" class="labeltext">
                              Byte: </td>
                            <td align="left" bgcolor="#CCCCCC" class="labeltext">
                              Erstellt am: </td>
                            <td align="left" bgcolor="#CCCCCC" class="labeltext">
                              Letzte Speicherung: </td>
                            """

archivfile_mid_t = """
                            <tr>
                              <td class="normaltext">
                                <input type="radio" name="%s" value="%s">
                              </td>
                              <td bgcolor="#FFFFFF" class="normaltext" border=1 align="left">%s</td>
                              <td bgcolor="#FFFFFF" class="normaltext" border=1 align="left">%s</td>
                              <td bgcolor="#FFFFFF" class="normaltext" border=1 align="left">%s</td>
                              <td bgcolor="#FFFFFF" class="normaltext" border=1 align="left">%s</td>
                            </tr>
                            """

archivfile_end_t = """
                            <tr>
                              <td>&nbsp;</td>
                              <td colspan="2" align="center">
                                <input type="submit" class="button" value="Anzeigen">
                              </td>
                              <td colspan="2" align="center">
                                <input type="reset" class="button" value="Zur&uuml;cksetzen">
                              </td>
                            </tr>
                             <tr>
                           <td colspan="5">&nbsp;</td>
                           </tr>
                          </table>
                          </fieldset>
                        </form>
                </td>
              </tr>
            </table>
          </td>
        </tr>
      </table>
    </td>
  </tr>
</table>
</body>
</html>
"""

singleprotocolview_head_t = """
</head>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000">
<table width="735" align="center">
  <tr>
    <td class="legendtext" align="center"> <fieldset><legend class="legendtext">Detailansicht</legend>
      <FORM ACTION="menu_protocol" METHOD="post">
        <table width="95%">
          <tr align="left">
            <td class="labeltext"> Nr.:</td>
            <td class="labeltext"> Zeit: </td>
            <td class="labeltext"> Art des Zugriffs:</td>
            <td class="labeltext"> Benutzerkennung:</td>
            <td class="labeltext"> IP-Adresse:</td>
            """

singleprotocolview_mid_t = """
          <tr align="center">
            <td border=1 bgcolor="#FFFFFF" align="left" class="normaltext">%(nr)s</td>
            <td border=1 bgcolor="#FFFFFF" align="left" class="normaltext">%(zeit)s</td>
            <td border=1 bgcolor="#FFFFFF" align="left" class="normaltext">%(artdeszugriffs)s</td>
            <td border=1 bgcolor="#FFFFFF" align="left" class="normaltext">%(benutzerkennung)s</td>
            <td border=1 bgcolor="#FFFFFF" align="left" class="normaltext">%(ipadresse)s</td>
          </tr>
          """

singleprotocolview_end_t = """
        <tr align="center">
            <td border=1 class="normaltext" colspan="5">
              <input type="submit" value="Zurück" name="submit" class="button">
            </td>
          </tr>
        </table>
</form>
</fieldset>
</td>
</tr>
</table>
</body>
</html>
"""

archivdel_t = """
<FORM ACTION="menu_protocol" METHOD="post">
<br>
<div align="center">
Protokolltabelle wurde archiviert
und gelöscht.
</div>
<br>
<input type="submit" value="Zurück">
</form>
"""

protocolanaus_t = """
</head><body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000">
<FORM ACTION="menu_protocol" METHOD="post">
<br>
<div align="center">
Protokollierung wurde %sgeschaltet.
</div>
<br>
<center>
<input type="submit" value="Zurück">
</center>
</form>
"""

fullgrenze_t = """
</head><body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000">
<FORM ACTION="menu_protocol" METHOD="post">
<br>
<div align="center">
Füllgrenze der Protokolltabelle wurde auf %s gesetzt.
</div>
<br>
<center>
<input type="submit" value="Zurück">
</center>
</form>
"""

dateitop_t = """
</head><body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000">
<FORM ACTION="menu_protocol" METHOD="post">
"""
datei_t = """
%(nr)07d,%(zeit)s,%(artdeszugriffs)s,%(benutzerkennung)s,%(ipadresse)s"""
dateiend_t = """
<center>
<input type="submit" value="Zurück">
</center>
</form>
"""
menufuss_t = """
</BODY>
</HTML> """
