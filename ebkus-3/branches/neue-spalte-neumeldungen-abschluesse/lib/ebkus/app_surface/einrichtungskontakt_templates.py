# coding: latin-1
########################
# Einrichtungskontaktneu
########################

formkopfneu_t = """
<FORM ACTION="klkarte" METHOD="post">
<table border=1 cellspacing=1 cellpadding=6 bgcolor=#CCCCCC>
    <th align="center"> %(akte_id__vn)s %(akte_id__na)s, %(akte_id__gb)s </th>
    <th align="right"><em> %(fn)s </em></th>
    </tr>
</table>
<input type="hidden" value="%(akte_id)d" name="akid">
<input type="hidden" value="%(id)d" name="fallid">
"""

theinrneu_t = """
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
            <td align="center" class="legendtext">
              <fieldset><legend class="legendtext">Kontaktdaten</legend>
              <table border=0 width="95%%" cellspacing=0 cellpadding=0>
                <th align="left" class="labeltext">Art:</th>
                <th align="left" class="labeltext">Name:</th>
                <th align="left" class="labeltext">Telefon 1:</th>
                <th align="left" class="labeltext">Telefon 2:</th>
                <tr height="40">
                  <td align="left">
                    <select name="insta"> """

einrneuna_t = """
                    </select></td>
                  <td align="left"><input type="text" class="textbox" size=10 maxlength=80 name="na" onMouseOver="window.status='Name des Einrichtungskontakts';return true;" onMouseOut="window.status='';return true;" title="Name des Einrichtungskontakts"></td>
                  <td align="left"><input type="text" class="textbox" size=10 maxlength=25 name="tl1"></td>
                  <td align="left"><input type="text" class="textbox" size=10 maxlength=25 name="tl2"></td>
                </tr>
                <tr height="40">
                  <td align="center"  valign="middle" class="legendtext" colspan=4>Notiz&#160;
                    <input type="text" size=60 maxlength=255 name="no">
                    <input type="checkbox" value="%(nobed)s" name="nobed">Wichtig</td>
                </tr>
                <tr><td colspan="4">&nbsp;</td></tr>
              </table>
              </fieldset>
            </td>
          </tr>
          <input type="hidden" value="%(status)s" name="status">
           <tr>
            <td align="center" class="legendtext" valign="middle"> <fieldset><legend>Kontaktliste</legend>
              <table width="95%%" border="0" cellpadding="1">
"""

theinrneueinrichtungen_t = """
                <tr>
                  <td width="33%" align="left" valign="middle" class="labeltext">
                    Art: </td>
                  <td align="left" valign="middle" width="33%" class="labeltext">
                    Name: </td>
                  <td align="left" valign="middle" width="34%" class="labeltext">
                    Telefon1: </td>
                  <td align="left" valign="middle" width="34%" class="labeltext">
                    Telefon2: </td>
                  <td align="left" valign="middle" width="34%" class="labeltext">
                    Aktualit&auml;t:</td>
                </tr>"""

einrneueinrichtungen_t = """
                <tr>
                  <td align="center" width="20%%" valign="middle" class="normaltext" bgcolor="#FFFFFF">&#160; %(insta__name)s</td>
                  <td align="center" width="20%%" valign="middle" class="normaltext" bgcolor="#FFFFFF">&#160; %(na)s </td>
                  <td align="center" width="20%%" valign="middle" class="normaltext" bgcolor="#FFFFFF">&#160; %(tl1)s </td>
                  <td align="center" width="20%%" valign="middle" class="normaltext" bgcolor="#FFFFFF">&#160; %(tl2)s </td>
                  <td align="center" width="20%%" valign="middle" class="normaltext" bgcolor="#FFFFFF">&#160; %(status__code)s </td>
                </tr>
                <tr>
                  <td align="center" colspan=5 bgcolor="#FFFFFF"> %(nobed__name)s: %(no)s </td>
                </tr>
                 """


keineeinrneu_t = """
                <tr>
                  <td colspan="5" align="center" class"normaltext" bgcolor="#FFFFFF">Bisher keine Einrichtung eingetragen.</td>
                </tr>
                """
#############################
# Einrichtungskontakt updaten
############################


updeinrna_t = """

                </select></td>
                  <td align="left" valign="middle" >
                   <input type="text" class="textbox" size=10 maxlength=80 value="%(na)s" name="na"></td>
                  <td align="left" valign="middle">
                    <input type="text" class="textbox" size=10 maxlength=25 value="%(tl1)s" name="tl1"></td>
                  <td align="left" valign="middle" >
                    <input type="text" class="textbox" size=10 maxlength=25 value="%(tl2)s" name="tl2"></td>
                </tr>
                <tr height="40">
                 <td align="center" valign="middle" class="legendtext" colspan="4"><B>Notiz</B>
                 <input type="text" size=60 maxlength=255 value="%(no)s" name="no">"""



updeinraktuell_t = """
                  Wichtig
                </tr>
                <tr><td colspan="4">&nbsp;</td></tr>
              </table>
              </fieldset>
            </td>
          </tr>
          <input type="hidden" value="%(status)d" name="status">
          <input type="hidden" value="%(id)d" name="einrid">
          <tr>
            <td align="center" class="legendtext" valign="middle"> <fieldset><legend>Kontaktliste</legend>
              <table width="95%%" border="0" cellpadding="1">

         <!--<B> Wichtig </B></td>
        </tr>
        <tr><td colspan="5">&nbsp;</td></tr>
       </table>
       </td>
       </tr>-->
"""

einr_neu_ende_t = """
            <tr><td colspan="5">&nbsp;</td></tr>
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
              </fieldset> </td>
          </tr>
        </table>
      </form>
</table>
</body>
</html>"""