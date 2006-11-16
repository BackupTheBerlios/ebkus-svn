# coding: latin-1


jghhead_t = """
</head>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000">
<table width="735" align="center">
  <tr>
    <td height="465" align="center" valign="top">
      <form name="jghform" method="post" action="jgh_check">
        <input type="hidden" value="%(fall_id)s" name="fallid">
        <table border="0" cellpadding="1" width="95%%">"""

jghfalldaten_t = """
          <tr>
            <td align="center" class="legendtext" valign="top" height="104" colspan="2">
              <fieldset><legend class="legendtext">Falldaten</legend>
              <table width="100%%" border="0" cellpadding="1" height="103">
                <tr height="20">
                  <input type="hidden" value="%(fall_fn)s" name="fall_fn" >
                  <input type="hidden" value="%(stz)s" name="stz" >
                  <input type="hidden" value="%(jghid)s" name="jghid" >
                  <input type="hidden" value="%(file)s" name="file" >
                  <td width="16%%" align="right" class="labeltext" >Fallnummer:</td>
                  <td width="34%%" align="left" colspan="2" class="legendtext">%(fall_fn)s</td>
                  <input type="hidden" value="%(gm)s" name="gm">
                  <input type="hidden" value="%(gmt)s" name="gmt">
                  <input type="hidden" value="%(mit_id)d" name="mitid">
                  <td width="16%%" align="right" class="labeltext">Mitarbeiter:</td>
                  <td width="34%%" align="left" class="legendtext">%(mit_id__ben)s</td>
                </tr>
                <tr height="20">
                  <input type="hidden" value="1" name="bgd">
                  <input type="hidden" value="%(bgm)s" name="bgm">
                  <input type="hidden" value="%(bgy)s" name="bgy">
                  <td width="16%%" align="right" class="labeltext">Beginn:</td>
                  <td width="16%%" align="left"  colspan="2" class="legendtext">%(bgm)s.%(bgy)s</td>
                  <td width="16%%" align="right" class="labeltext">Land:</td>
                  <td width="34%%" align="left">
                    <select name="rbz" class="listbox" style="width:150">
                    %(rbz_sel)s
                    </select>
                  </td>
                </tr>
                <tr height="40">
                  <input type="hidden" value="" name="ed">
                  <td width="16%%" align="right" class="labeltext">Ende:</td>
                  <td align="left" nowrap>
                  <input type="text" name="em" size="1" value="%(em)s" class="textboxsmall" maxlength="2">
                  </td>
                  <td align="left" nowrap>
                    <input type="text" name="ey" size="2" value="%(ey)s"class="textboxmid" maxlength="4">
                  </td>
                  <td width="16%%" align="right" class="labeltext" height="26">Kreis:</td>
                  <td width="34%%" align="left" height="26">
                    <select name="kr" class="listbox" style="width:150">
                    %(kr_sel)s                    
                    </select>
                  </td>
                </tr>
                  <td colspan="3" width="50%%" height="66" >&nbsp;</td>
                  <td width="16%%" align="right" class="labeltext" height="33">Geschwisterfall:</td>
                  <td width="34%%" align="left" height="33">
                    <select name="gfall" class="listbox" style="width:150">
                    %(gfall_sel)s                    
                    </select>
                  </td>
                </tr>
              </table>
              </fieldset>
            </td>
          </tr>"""

jghpersonendaten_t = """
          <tr>
            <td align="center" class="legendtext" valign="top" height="143" colspan="2">
              <fieldset><legend class="legendtext">Personendaten</legend>
              <table width="100%%" border="0" cellpadding="1">
                <tr>
                  <td align="right" height="35" width="21%%" class="labeltext">Familiensituation:</td>
                  <td align="left" height="35" width="34%%">
                    <select name="sit_fam" style="width:200">
                    %(shf_sel)s
                    </select>
                  </td>
                  <td align="right" height="35" width="31%%" class="labeltext">Geschlecht:</td>
                  <td align="left" height="35" width="14%%">
                    <select name="gs" style="width:40">
                    </select>
                  </td>
                </tr>
              </table>
              </fieldset>
            </td>
          </tr>"""


jghberatungsdaten_t = """
          <tr>
            <td align="center" class="legendtext" valign="top" height="91" colspan="2">
              <fieldset><legend class="legendtext">Beratungsdaten</legend>
              <table width="100%" border="0" cellpadding="1" height="56">
                <tr align="right">
                  <td height="47" colspan="3" class="labeltext"> Tr&auml;ger:</td>
                  <td align="left" height="47" width="60%" class="labeltext">
                    <select name="traeg" class="listbox130" style="width:250">"""

jghkontakt_t = """

                    </select>
                  </td>
                </tr>
                <tr align="right">
                  <td height="47" colspan="3" class="labeltext"> 1.Kontakt durch:</td>
                  <td align="left" height="47" width="60%" class="labeltext">
                    <select name="zm" class="listbox130" style="width:270">"""

jghendegrund_t = """

                    </select>
                  </td>
                </tr>
                <tr align="right">
                  <td height="38" colspan="3" class="labeltext">Beendigungsgrund:</td>
                  <td align="left" height="38" width="60%" class="labeltext">
                    <select name="bgr" class="listbox130" style="width:270">"""

jghanlass_t = """

                    </select>
                  </td>
                </tr>
                <tr align="right">
                  <td height="47" colspan="3" class="labeltext">Beratungsanl&auml;sse:</td>
                  <td align="left" height="47" width="60%" class="labeltext">
                    <select name="ba" multiple class="listbox130" style="width:270" size="6">"""

jgstateditschwerpunkt_t = """

                    </select>
                  </td>
                </tr>
                <tr align="right">
                  <td height="42" colspan="3" class="labeltext">Beratungsschwerpunkt:</td>
                  <td align="left" height="42" width="60%" class="labeltext">
                    <select name="schw" class="listbox130" style="width:270" size="1">"""

jghlebtbei_t = """

                    </select>
                  </td>
                </tr>
              </table>
              </fieldset> </td>
          </tr>
          <tr>
            <td align="center" class="legendtext" valign="top" height="143" colspan="2">
              <fieldset><legend class="legendtext">Personendaten</legend>
              <table width="100%" border="0" cellpadding="1">
                <tr>
                  <td align="right" height="35" width="21%" class="labeltext">lebt:</td>
                  <td align="left" height="35" width="34%">
                    <select name="fs" style="width:200">"""

jghgeschlecht_t = """

                    </select>
                  </td>
                  <td align="right" height="35" width="31%" class="labeltext">Geschlecht:</td>
                  <td align="left" height="35" width="14%">
                    <select name="gs" style="width:40">"""

jghalter_t = """

                    </select>
                  </td>
                </tr>
                <tr>
                  <td align="right" height="35" width="21%" class="labeltext">Alter:</td>
                  <td align="left" height="35" width="34%">
                    <select name="ag" style="width:100">"""

jgh_t2a = """

                    </select>
                  </td>
                  <td align="right" height="35" width="31%%" class="labeltext">Geschwisteranzahl
                    bekannt:</td>
                  <td align="left" height="35" width="14%%">
                   <input type="text" name="gsa" size=2 maxlength=2 value="%s">"""

jgh_t2b = """
                  </td>
                </tr>
                <tr>
                  <td align="right" height="35" width="21%%" class="labeltext">Staatsangeh&ouml;rigkeit:</td>
                  <td align="left" height="35" width="34%%">
                    <select class="listbox" name="hke" style="width:100">
                      <option value=""> """

jgh_t3 = """
                    </select>
                  </td>
                  <td align="right" height="35" width="31%%" class="labeltext">Geschwisteranzahl
                    unbekannt:</td>
                  <td align="left" height="35" width="14%%">
                    <input type="checkbox" %(check)s value="%(gsu)d" name="gsu">
                  </td>
                </tr>
              </table>
              </fieldset> </td>
          </tr>
          <tr>
            <td align="center" class="legendtext" valign="top" width="50%%" height="77">
              <fieldset><legend class="legendtext">Therapieansatz Kind/Jugendliche</legend>
              <table width="100%%" border="0" cellpadding="1">
                <tr>
                  <td align="right" class="labeltext" width="52%%">allein:</td>
                  <td align="left" class="labeltext" width="48%%">"""

jgh_t4 = """ </td>
                </tr>
                <tr>
                  <td align="right" class="labeltext" width="52%">in der Gruppe:</td>
                  <td align="left" class="labeltext" width="48%">"""
jgh_t5 = """ </td>
                </tr>
              </table>
              </fieldset> </td>
            <td align="center" class="legendtext" valign="top" width="50%" height="77">
              <fieldset><legend class="legendtext">Therapieansatz Eltern</legend>
              <table width="100%" border="0" cellpadding="1">
                <tr>
                  <td align="right" width="45%" class="labeltext">allein:</td>
                  <td width="55%">"""
jgh_t6 = """ </td>
                </tr>
                <tr>
                  <td align="right" width="45%" class="labeltext">in der Gruppe:</td>
                  <td width="55%">"""

jgh_t7 = """ </td>
                </tr>
              </table>
              </fieldset> </td>
          </tr>
          <tr>
            <td align="center" class="legendtext" valign="top" colspan="2" height="49">
              <fieldset><legend class="legendtext">Therapieansatz Sonstiges</legend>
              <table width="100%" border="0" cellpadding="1">
                <tr>
                  <td align="center" class="labeltext" width="50%">"""

jgh_t8 = """ </td>
                  <td align="center" class="labeltext" width="50%">"""
jgh_t9 = """ </td>
                </tr>
              </table>
              </fieldset> </td>
          </tr>"""


jghbuttons_t = """
          <tr>
            <td align="center" class="legendtext" valign="middle" colspan="3">
              <fieldset>
              <table width="100%%" border="0" cellpadding="1">
                <tr height="40">
                  <td width="33%%" align="center" valign="middle">
                    <input type="submit" name="" value="Speichern" class="button">
                  </td>
                  <td align="center" valign="middle" width="33%%">
                    <input type="reset" value="Zur&uuml;cksetzen" class="button">
                  </td>
                  <td align="center" valign="middle" width="34%%">
                    <input type="button" value="Abbrechen" class="button"
                     onClick="javascript:history.back()">
                  </td>
                </tr>
              </table>
              </fieldset> </td>
          </tr>"""

jghfoot_t = """
        </table>
      </form>
    </td>
  </tr>
</table>
</body>
</html>
"""

jghansaetzefamilie_t = """in der Familie <input type="checkbox" value="%(id)d" name="%(kat_code)s" > """

jghansaetzeumfeld_t = """im sozialen Umfeld <input type="checkbox" value="%(id)d" name="%(kat_code)s" >"""

jghansaetzefamiliecheck_t = """in der Familie <input type="checkbox" checked value="%(id)d" name="%(kat_code)s" > """

jghansaetzeumfeldcheck_t = """im sozialen Umfeld <input type="checkbox" checked value="%(id)d" name="%(kat_code)s" >"""

