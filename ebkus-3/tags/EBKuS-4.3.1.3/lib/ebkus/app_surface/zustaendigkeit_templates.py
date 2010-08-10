# coding: latin-1
###################
# Zustaendigkeit neu
###################

thzustneu_t = """
</head>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000">
<table width="735" align="center">
  <tr>
    <td height="465" align="center" valign="top">
      <form name="klkarte" method="post" action="klkarte">
        <input type="hidden" value="%(akte_id)d" name="akid">
        <input type="hidden" value="%(id)d" name="fallid">
        <table border="0" cellpadding="1" width="95%%">
          <tr>
            <td width="95%%" align="center" class="legendtext" valign="top"> <fieldset><legend class="legendtext">Klientendaten</legend>
              <table width="95%%" border="0" cellpadding="1">
                <tr>
                  <td align="left" bgcolor="#CCCCCC" class="labeltext">Name:</td>
                  <td align="left" bgcolor="#CCCCCC" class="labeltext">Geburtsdatum:</td>
                  <td align="left" bgcolor="#CCCCCC" class="labeltext">Fallnummer:</td>
                <tr>
                  <td align="center" bgcolor="#FFFFFF" class="normaltext">%(akte_id__vn)s
                    %(akte_id__na)s</td>
                  <td align="center" bgcolor="#FFFFFF" class="normaltext">%(akte_id__gb)s</td>
                  <td align="center" bgcolor="#FFFFFF" class="normaltext">%(fn)s</td>
                </tr>
                <tr>
                  <td colspan="3">&nbsp;</td>
                </tr>
              </table>
              </fieldset> </td>
          </tr>
          <tr>
            <td width="45%%" align="center" class="legendtext" valign="top"> <fieldset><legend class="legendtext">Zust&auml;ndigkeiten</legend>
              <table width="95%%" border="0" cellpadding="1">
                <tr>
                  <td width="50%%" align="center" class="labeltext">Bearbeiter:</td>
                  <td width="50%%" align="center" class="labeltext">Beginn:</td>
                </tr>
                <tr>
                  <td align="center">
                    <select name="mitid" class="listbox" style="width:200">"""

zustneudatum_t = """

                    </select>
                  </td>
                  <td align="center">
                    <table>
                      <tr>
                      <td>
                    <input type="text" class="textboxsmall" size=2 maxlength=2 value="%(day)d" name="bgd">
                      </td>
                      <td>.</td>
                      <td>
                    <input type="text" class="textboxsmall" size=2 maxlength=2 value="%(month)d" name="bgm">
                      </td>
                      <td>.</td>
                      <td>
                    <input type="text" class="textboxmid" size=4 maxlength=4 value="%(year)d" name="bgy">
                      </td>
                    </tr>
                  </table>
                  </td>
                </tr>
                <tr><td colspan="2">&nbsp;</td></tr>
              </table>
              </fieldset> </td>
          </tr>
          """

zustende_t = """
          <tr>
            <td align="center" class="legendtext" valign="middle"> <fieldset><legend>Bisherige
              Zust&auml;ndigkeit wird ausgetragen</legend>
              <table width="95%%" border="0" cellpadding="1">
                <tr>
                  <td width="77%%" align="left" valign="middle" class="labeltext" colspan="2">
                    Bearbeiter: </td>
                  <td align="left" valign="middle" width="33%%" class="labeltext">
                    Beginn: </td>
                </tr>
                <tr>
                  <td width="33%%" align="center" valign="middle" class="normaltext"" bgcolor="#FFFFFF">
                    &#160;%(mit_id__vn)s </td>
                  <td width="33%%" align="center" valign="middle" class="normaltext"" bgcolor="#FFFFFF">
                    &#160;%(mit_id__na)s </td>
                  <td align="center" valign="middle" width="33%%" class="normaltext" bgcolor="#FFFFFF">
                    &#160;%(bgd)d.%(bgm)d.%(bgy)d </td>
                </tr>
                <tr>
                  <td colspan="3">&nbsp;</td>
                </tr>
              </table>
              </fieldset></td>
            <input type="hidden" value="%(mit_id__id)d" name="aktuellmitid">
            <input type="hidden" value="%(id)d" name="aktuellzustid">
          </tr>
          """

thzustaendigkeiten_t = """
          <tr>
            <td align="center" class="legendtext" valign="middle"> <fieldset><legend>Zust&auml;ndigkeiten</legend>
              <table width="95%%" border="0" cellpadding="1">
                <tr>
                  <td width="33%%" align="left" valign="middle" class="labeltext">
                    Bearbeiter: </td>
                  <td align="left" valign="middle" width="33%%" class="labeltext">
                    Beginn: </td>
                  <td align="left" valign="middle" width="34%%" class="labeltext">
                    Ende: </td>
                </tr>
                """

zustaendigkeiten_t = """
                <tr>
                  <td width="33%%" align="center" valign="middle" class="normaltext"" bgcolor="#FFFFFF">
                    &#160;%(mit_id__na)s </td>
                  <td align="center" valign="middle" width="33%%" class="normaltext" bgcolor="#FFFFFF">
                    &#160;%(bgd)d.%(bgm)d.%(bgy)d </td>
                  <td align="center" valign="middle" width="34%%" class="normaltext" bgcolor="#FFFFFF">
                    &#160;%(ed)d.%(em)d.%(ey)d </td>
                </tr>
                """

zustaendigkeiten_ende_t = """
               <tr><td colspan="2">&nbsp;</td></tr>
              </table>
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
              </fieldset> </td>
          </tr>
        </table>
      </form>
</table>
</body>
</html>
"""

##Zuständigkeit update

thzustupd_ta = """
</head>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000">
<table width="735" align="center">
  <tr>
    <td height="465" align="center" valign="top">
      <form name="klkarte" method="post" action="klkarte">
"""
thzustupd_t_zustid = """
        <input type="hidden" value="%s" name="zustid">
"""

thzustupd_tb = """
        <input type="hidden" value="%(akte_id)d" name="akid">
        <input type="hidden" value="%(id)d" name="fallid">
        <table border="0" cellpadding="1" width="95%%">
          <tr>
            <td width="95%%" align="center" class="legendtext" valign="top"> <fieldset><legend class="legendtext">Klientendaten</legend>
              <table width="95%%" border="0" cellpadding="1">
                <tr>
                  <td align="left" bgcolor="#CCCCCC" class="labeltext">Name:</td>
                  <td align="left" bgcolor="#CCCCCC" class="labeltext">Geburtsdatum:</td>
                  <td align="left" bgcolor="#CCCCCC" class="labeltext">Fallnummer:</td>
                <tr>
                  <td align="center" bgcolor="#FFFFFF" class="normaltext">%(akte_id__vn)s
                    %(akte_id__na)s</td>
                  <td align="center" bgcolor="#FFFFFF" class="normaltext">%(akte_id__gb)s</td>
                  <td align="center" bgcolor="#FFFFFF" class="normaltext">%(fn)s</td>
                </tr>
                <tr>
                  <td colspan="3">&nbsp;</td>
                </tr>
              </table>
              </fieldset> </td>
          </tr>
          <tr>
            <td width="45%%" align="center" class="legendtext" valign="top"> <fieldset><legend class="legendtext">Zust&auml;ndigkeiten</legend>
              <table width="95%%" border="0" cellpadding="1">
                <tr>
                  <td width="40%%" align="center" class="labeltext">Bearbeiter:</td>
                  <td width="30%%" align="center" class="labeltext">Beginn:</td>
                  <td width="30%%" align="center" class="labeltext">Ende:</td>
                </tr>
                <tr>
                  <td align="left">
                    <select name="mitid" class="listbox" style="width:250">"""

updzustdatum_t = """

                    </select>
                  </td>
                  <td align="center">
                    <table>
                      <tr>
                      <td>
                    <input type="text" class="textboxsmall" size=2 maxlength=2 value="%(bgd)d" name="bgd">
                      </td>
                      <td>.</td>
                      <td>
                    <input type="text" class="textboxsmall" size=2 maxlength=2 value="%(bgm)d" name="bgm">
                      </td><td>.</td>
                      <td>
                    <input type="text" class="textboxmid" size=4 maxlength=4 value="%(bgy)d" name="bgy">
                      </td>
                      </tr>
                    </table>
                  </td>
                  <td align="center">
                    <table>
                      <tr>
                      <td>
                    <input type="text" class="textboxsmall" size=2 maxlength=2 value="%(ed)d" name="ed">
                      </td>
                      <td>.</td>
                      <td>
                    <input type="text" class="textboxsmall" size=2 maxlength=2 value="%(em)d" name="em">
                      </td>
                      <td>.</td>
                      <td>
                    <input type="text" class="textboxmid" size=4 maxlength=4 value="%(ey)d" name="ey">
                      </td>
                      </tr>
                    </table>
                  </td>
                </tr>
                <tr><td colspan="3">&nbsp;</td></tr>
              </table>
              </fieldset> </td>
          </tr>
          """

zustendeupd_t = """
          <tr>
            <td align="center" class="legendtext" valign="middle"> <fieldset><legend>Bisherige
              Zust&auml;ndigkeit wird ausgetragen</legend>
              <table width="95%%" border="0" cellpadding="1">
                <tr>
                  <td width="77%%" align="left" valign="middle" class="labeltext" colspan="2">
                    Bearbeiter: </td>
                  <td align="left" valign="middle" width="33%%" class="labeltext">
                    Beginn: </td>
                </tr>
                <tr>
                  <td width="33%%" align="center" valign="middle" class="normaltext"" bgcolor="#FFFFFF">
                    &#160;%(mit_id__vn)s </td>
                  <td width="33%%" align="center" valign="middle" class="normaltext"" bgcolor="#FFFFFF">
                    &#160;%(mit_id__na)s </td>
                  <td align="center" valign="middle" width="33%%" class="normaltext" bgcolor="#FFFFFF">
                    &#160;%(bgd)d.%(bgm)d.%(bgy)d </td>
                </tr>
                <tr>
                  <td colspan="3">&nbsp;</td>
                </tr>
              </table>
              </fieldset></td>
            <input type="hidden" value="%(mit_id__id)d" name="aktuellmitid">
            <input type="hidden" value="%(id)d" name="aktuellzustid">
          </tr>
          """

