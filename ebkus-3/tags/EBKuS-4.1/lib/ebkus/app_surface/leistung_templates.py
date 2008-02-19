# coding: latin-1
###################
# Leistung einfuegen
###################


thleistneu_t = """
</head>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000">
<table width="735" align="center">
  <tr>
    <td align="center" valign="top">
      <form name="leistungneu" method="post" action="klkarte">
        <input type="hidden" value="%(akte_id)d" name="akid">
        <input type="hidden" value="%(id)d" name="fallid">
        <table border="0" cellpadding="1" width="95%%">
          <tr>"""

thleistneu2_t = """
            <td width="45%%" align="center" class="legendtext" valign="top"> <fieldset><legend class="legendtext">Neue
              Leistung f&uuml;r %(vn)s %(na)s</legend>
              <table width="90%%" border="0" cellpadding="1">
                <tr>
                  <td width="50%%" class="labeltext" align="left">Mitarbeiter:</td>
                  <td width="50%%" class="labeltext" align="left">Leistung:</td>
                </tr>
                <tr>
                  <td align="center">
                    <select name="mitid" class="listbox" style="width:200">"""

leistneu_t = """
                    </select>
                  </td>
                  <td align="center">
                    <select name="le" class="listbox" style="width:300">"""

leistneubg_t = """
                    </select>
                  </td>
                </tr>
                <tr><td colspan="2">&nbsp;</td><tr>
              </table>
              </fieldset> </td>
          </tr>
          <tr>
            <td width="45%%" align="center" class="legendtext" valign="top"> <fieldset><legend class="legendtext">Leistungszeitraum</legend>
              <table width="90%%" border="0" cellpadding="1">
                <tr>
                  <td width="50%%" class="labeltext" align="center">Am:</td>
                  <td width="50%%" class="labeltext" align="center">Bis:</td>
                </tr>
                <tr>
                  <td align="center">
                    <input type="text" class="texboxsmall" size=2 maxlength=2 value="%(day)d" name="bgd">
                    <b>.</b>
                    <input type="text" class="texboxsmall" size=2 maxlength=2 value="%(month)d" name="bgm">
                    <b>.</b>
                    <input type="text" class="texboxmid" size=4 maxlength=4 value="%(year)d" name="bgy">
                  </td>
                  <td align="center">
                    <input type="text" class="texboxsmall" size=2 maxlength=2 name="ed">
                    <b>.</b>
                    <input type="text" class="texboxsmall" size=2 maxlength=2 name="em">
                    <b>.</b>
                    <input type="text" class="texboxmid" size=4 maxlength=4 name="ey">
                  </td>
                </tr>
                <tr><td colspan="2">&nbsp;</td></tr>
              </table>
            </td>
          </tr>
  """
thleistungsliste_t = """
          <tr>
            <td width="45%%" align="center" class="legendtext" valign="top"> <fieldset>
            <legend class="legendtext">Liste der bisherigen Leistungen</legend>
              <table width="90%%" border="0" cellpadding="1">
                <tr>
                  <td width="20%%" class="labeltext" align="left">Mitarbeiter:</td>
                  <td width="40" class="labeltext" align="left">Leistungen:</td>
                  <td width="20%%" class="labeltext" align="left">Am:</td>
                  <td width="20%%" class="labeltext" align="left">Bis:</td>
                </tr>
        """
leistungsliste_t = """
                <tr>
                  <td align="center" bgcolor="#FFFFFF" class="normaltext">%(mit_id__na)s
                  </td>
                  <td align="center" bgcolor="#FFFFFF" class="normaltext">%(le__name)s
                  </td>
                  <td align="center" bgcolor="#FFFFFF" class="normaltext">%(bgd)d<B>.</B>%(bgm)d<B>.</B>%(bgy)d</td>
                  <td align="center" bgcolor="#FFFFFF" class="normaltext">%(ed)d<B>.</B>%(em)d<B>.</B>%(ey)d</td>
                </tr>
        """

leistungsliste_ende_t = """
               <tr><td colspan="4">&nbsp;</td><tr>
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
     </td>
  </tr>
</table>
</body>
</html>
"""



keineleistungneu_t = """
<div align="center"> Bisher keine Leistung eingetragen. """

thleistupd_t = """
            <td width="45%%" align="center" class="legendtext" valign="top"> <fieldset><legend class="legendtext">Leistung bearbeiten von %(vn)s %(na)s</legend>
              <table width="90%%" border="0" cellpadding="1">
                <tr>
                  <td width="50%%" class="labeltext" align="left">Mitarbeiter:</td>
                  <td width="50%%" class="labeltext" align="left">Leistung:</td>
                </tr>
                <tr>
                  <td align="center">
                    <select name="mitid" class="listbox" style="width:200">"""

leistupdbg_t = """
                    </select>
                  </td>
                </tr>
                <tr><td colspan="2">&nbsp;</td><tr>
              </table>
              </fieldset> </td>
          </tr>
          <tr>
            <td width="45%%" align="center" class="legendtext" valign="top"> <fieldset><legend class="legendtext">Leistungszeitraum</legend>
              <table width="90%%" border="0" cellpadding="1">
                <tr>
                  <td width="50%%" class="labeltext" align="center">Am:</td>
                  <td width="50%%" class="labeltext" align="center">Bis:</td>
                </tr>
                <tr>
                  <td align="center">
                    <input type="text" value="%(bgd)d" class="texboxsmall" size=2 maxlength=2 name="bgd">
                    <b>.</b>
                    <input type="text" value="%(bgm)d" class="texboxsmall" size=2 maxlength=2 name="bgm">
                    <b>.</b>
                    <input type="text" value="%(bgy)d" class="texboxmid" size=4 maxlength=4  name="bgy">
                  </td>
                  <td align="center">
                    <input type="text" value="%(ed)d" class="texboxsmall" size=2 maxlength=2 name="ed">
                    <b>.</b>
                    <input type="text" value="%(em)d" class="texboxsmall" size=2 maxlength=2 name="em">
                    <b>.</b>
                    <input type="text" value="%(ey)d" class="texboxmid" size=4 maxlength=4 name="ey">
                  </td>
                </tr>
                <input type="hidden" value="%(id)d" name="leistid">
                <tr><td colspan="2">&nbsp;</td></tr>
              </table>
            </td>
          </tr>
  """

keineleistungneu_t = """
<div align="center"> Bisher keine Leistung eingetragen. """