# coding: latin-1
anmeldung_neu_t1 = """
</HEAD>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000" onLoad="javascript:document.persneuform.vn.focus();">
<table width="735" align="center">
 <tr>
    <td height="465" align="center" valign="top">
      <form name="persneuform" method="post" action="klkarte">
        <table border="0" cellpadding="1" width="95%">
          <tr>
            <td width="45%" align="center" class="legendtext" valign="top" height="200">
              <fieldset><legend class="legendtext">Personendaten</legend>
              <table width="90%" border="0" cellpadding="1" height="200">
                <tr>
                  <td width="37%" align="right"> <span class="labeltext">Vorname:</span></td>
                  <td width="63%" align="left">
                    <input type="text" size="10" maxlength=35 name="vn" class="textbox">
                  </td>
                </tr>
                <tr>
                  <td align="right" valign="middle"> <span class="labeltext">Nachname:</span></td>
                  <td align="left" valign="middle">
                    <input type="text" size="10" maxlength=35 name="na" class="textbox">
                  </td>
                </tr>
                <tr>
                  <td align="right" valign="middle" class="labeltext">Geburtstag:</td>
                  <td align="left" valign="middle" class="labeltext">
                    <input type="text" size="10" maxlength=10 name="gb" class="textbox" onBlur="PruefeDatum(gb,1960,2060)">
                  </td>
                </tr>
                <tr>
                  <td align="right" valign="middle" class="labeltext">Telefon
                    1:</td>
                  <td align="left" valign="middle" class="labeltext">
                    <input type="text" size="10" maxlength=25 name="tl1" class="textbox">
                  </td>
                </tr>
                <tr>
                  <td align="right" valign="middle" class="labeltext">Telefon
                    2:</td>
                  <td align="left" valign="middle" class="labeltext">
                    <input type="text" size="10" maxlength=25 name="tl2" class="textbox">
                  </td>
                </tr>
                <tr>
                  <td align="right" valign="middle" class="labeltext">Ausbildung:</td>
                  <td align="left" valign="middle" class="labeltext">
                    <input type="text" size="10" maxlength=30 name="ber" class="textbox">
                  </td>
                </tr>
              </table>
              </fieldset> </td>
            <td valign="top" align="center" class="legendtext" width="55%" height="200">
              <fieldset><legend class="legendtext">Anschrift</legend>
              <table border="0" cellpadding="1" width="311" height="200">
                <tr>
                  <td align="right" class="labeltext"> <span class="labeltext">Strasse
                    in Berlin:</span></td>
                  <td>
                    <select name="select3" class="listbox130" style="width:210">
"""
anmeldung_neu_t2 = """
                    </select>
                  </td>
                </tr>
                <tr>
                  <td align="right" valign="middle" class="labeltext">
                    <span class="labeltext">Strasse a. v. Berlin:</span></td>
                  <td align="left" valign="middle">
                    <input type="text" name="textfield7" maxlength=35 class="textbox">
                  </td>
                </tr>
                <tr>
                  <td align="right" valign="middle" class="labeltext">Hausnummer:</td>
                  <td align="left" valign="middle">
                    <input type="text" size="2" maxlength=5 name="hsnr" class="textboxmid">
                  </td>
                </tr>
                <tr>
                  <td align="right" valign="middle" class="labeltext">Postleitzahl:</td>
                  <td align="left" valign="middle">
                    <input type="text" size="2" maxlength=9 name="plz" class="textboxmid">
                  </td>
                </tr>
                <tr>
                  <td align="right" valign="middle" class="labeltext">Ort:</td>
                  <td align="left" valign="middle">
                    <input type="text" size="10" maxlength=35 name="ort" class="textbox">
                  </td>
                </tr>
                <tr>
                  <td align="right" valign="middle" class="labeltext">
                    <p>Wohnt bei:</p>
                  </td>
                  <td align="left" valign="middle">
                    <select name="fs" class="listbox130">"""

anmeldung_neu_t3 = """
                    </select>
                  </td>
                </tr>
              </table>
              </fieldset> </td>
          </tr>
          <tr>
            <td align="center" class="legendtext" valign="middle" colspan="2">
              <fieldset><legend>Notiz</legend>
              <table width="95%%" border="0" cellpadding="1">
                <tr>
                  <td width="85%%" align="center" height="35" valign="middle" class="normaltext">
                    <input type="text" size="50" maxlength=255 name="no">
                    <input type="checkbox" value="%(nobed)s"  name="nobed" >Wichtig
                    <input type="hidden" value="%(vrt)s" name="vrt">
                  </td>
                </tr>
              </table>
              </fieldset> </td>
          </tr>"""

anmeldung_neu_t4a = """
          <tr>
            <td align="center" class="legendtext" valign="middle" colspan="2">
              <fieldset><legend>Verwandschaftsart</legend>
              <table width="95%" border="0" cellpadding="1">
                <tr>
                  <td width="85%" align="center" height="35" valign="middle">
                   <select name="verw" class="listbox130">"""

anmeldung_neu_t4b = """
                   </select>
                  </td>
                </tr>
              </table>
              </fieldset> </td>
          </tr>"""

anmeldung_neu_t5 = """
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
        """

anmeldung_neu_t6 = """
      <input type="hidden" value="%(akte_id)d" name="akid">
      <input type="hidden" value="%(id)d" name="fallid">
      </form>
    </td>
  </tr>
</table>
</body>
</html>
"""

anmneuvon_t = """
</HEAD>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000" onLoad="javascript:document.persneuform.von.focus();">
<table width="735" align="center" height="264">
  <tr>
    <td height="285" align="center" valign="top">
      <form name="persneuform" method="post" action="klkarte">
        <table border="0" cellpadding="1" width="95%%" height="246">
          <tr>
            <td width="45%%" align="center" class="legendtext" valign="top" height="201">
              <fieldset><legend class="legendtext">Anmeldekontakt</legend>
              <table width="90%%" border="0" cellpadding="1" height="168">
                <tr>
                  <td align="right" class="labeltext">Gemeldet von:</td>
                  <td>
                    <input type="text" class="textbox" maxlength=35 value="%(von)s" name="von">
                  </td>
                  <td align="right" class="labeltext">Telefon:</td>
                  <td class="labeltext">
                    <input type="text" class="textbox" maxlength=20 value="%(mtl)s" name="mtl">
                  </td>
                </tr>
                <tr>
                  <td class="labeltext" align="right">Zugangsart:</td>
                  <td>
                    <select name="zm">"""

anmneuempfehlung_t = """
                   </select>
                  </td>
                  <td class="labeltext" align="right">Empfehlung von:</td>
                  <td>
                    <input type="text" class="textbox" maxlength=35 value="" name="me">
                  </td>
                </tr>
                <tr>
                  <td align="right" class="labeltext" height="23">Gemeldet am:
                  <td colspan="3" height="23" align="left">
                    <input type="text" maxlength=2 size="1" class="textboxsmall" value="%(ad)d"
               name="ad">
                    .
<input type="text" class="textboxsmall" size="1" maxlength=2 value="%(am)d"
               name="am">
                    .
<input type="text" class="textboxmid" size="2" maxlength=4 value="%(ay)d"
               name="ay">
                  </td>
                </tr>
                <tr>
                  <td align="right" class="labeltext">Anmeldegrund:&#160;
                  <td colspan="3">
                    <input type="text" class="textboxlarge" style="width:410" maxlength=255 value="" name="mg">
                  </td>
                </tr>
                <tr>
                  <td align="right" class="labeltext">Notiz:&#160; </td>
                  <td colspan="3">
                    <input type="text" class="textboxlarge" style="width:410" maxlength=255 value="" name="no">
                  </td>
                </tr>
              </table>
              </fieldset>
          <tr>
            <td width="45%%" align="center" class="legendtext" valign="top" height="31">
              <fieldset>
              <table width="95%%" border="0" cellpadding="1">
                <tr height="40">
                  <td width="33%%" align="center" valign="middle">
                    <input type="submit" name="Input" value="Speichern" class="button">
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
        </table>"""

anmneuende_t = """
        <input type="hidden" value="%(akte_id)d" name="akid">
        <input type="hidden" value="%(id)d" name="fallid">
      </form>
</table>
</body>
</html> """



updanmempfehlung_t = """
                   </select>
                  </td>
                  <td class="labeltext" align="right">Empfehlung von:</td>
                  <td>
                    <input type="text" class="textbox" maxlength=35 value="%(me)s" name="me">
                  </td>
                </tr>
                <tr>
                  <td align="right" class="labeltext" height="23">Gemeldet am:
                  <td colspan="3" height="23" align="left">
                    <input type="text" maxlength=2 size="1" class="textboxsmall" value="%(ad)d"
               name="ad">
                    .
<input type="text" class="textboxsmall" size="1" maxlength=2 value="%(am)d"
               name="am">
                    .
<input type="text" class="textboxmid" size="2" maxlength=4 value="%(ay)d"
               name="ay">
                  </td>
                </tr>
                <tr>
                  <td align="right" class="labeltext">Anmeldegrund:&#160;
                  <td colspan="3">
                    <input type="text" class="textboxlarge" style="width:410" maxlength=255 value="%(mg)s" name="mg">
                  </td>
                </tr>
                <tr>
                  <td align="right" class="labeltext">Notiz:&#160; </td>
                  <td colspan="3">
                    <input type="text" class="textboxlarge" style="width:410" maxlength=255 value="%(no)s" name="no">
                  </td>
                </tr>
              </table>
              </fieldset>
          <tr>
            <td width="45%%" align="center" class="legendtext" valign="top" height="31">
              <fieldset>
              <table width="95%%" border="0" cellpadding="1">
                <tr height="40">
                  <td width="33%%" align="center" valign="middle">
                    <input type="submit" name="Input" value="Speichern" class="button">
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
        <input type="hidden" value="%(id)d" name="anmid">
        </table>"""

anmupdende_t = """
        <input type="hidden" value="%(akte_id)d" name="akid">
        <input type="hidden" value="%(id)d" name="fallid">
      </form>
</table>
</body>
</html> """