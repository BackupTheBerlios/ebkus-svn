# coding: latin-1

jghstatneu_t = """
</head>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000">
<table width="735" align="center">
  <tr>
    <td height="465" align="center" valign="top">
      <form name="jghform" method="post" action="klkarte">
        <input type="hidden" value="%(id)s" name="fallid">
        <table border="0" cellpadding="1" width="95%%">
          <tr>
            <td align="center" class="legendtext" valign="top" height="104" colspan="2">
              <fieldset><legend class="legendtext"><b>Falldaten</b></legend>
              <table width="100%%" border="0" cellpadding="1" height="103">
                """

jghstatneufn_t = """
                <tr height="20">
                  <input type="hidden" value="%(fall_fn)s" name="fall_fn" >
                  <td width="16%%" align="right" class="labeltext" >Fallnummer:</td>
                  <td width="34%%" align="left"  colspan="2" class="legendtext">%(fall_fn)s</td>
                  """

jghstatneugemeinde_t = """
                  <input type="hidden" value="%d" name="gm">
                  """
jghstatneugemeindeteil_t = """
                  <input type="hidden" value="%d" name="gmt">
                  """
jghstatneumit_t = """
                  <input type="hidden" value="%(mit_id)d" name="mitid">
                  <td width="16%%" align="right" class="labeltext">Mitarbeiter:</td>
                  <td width="34%%" align="left" class="legendtext">%(mit_name)s</td>
                </tr>
                """
jghstatneubeginn_t = """
                <tr height="20">
                  <input type="hidden" value="%(bgm)s" name="bgm">
                  <input type="hidden" value="%(bgy)s" name="bgy">
                  <input type="hidden" value="%(bgd)s" name="bgd">
                  <td width="16%%" align="right" class="labeltext">Beginn:</td>
                  <td width="16%%" align="left"  colspan="2" class="legendtext">%(bgd)s.%(bgm)s.%(bgy)s</td>
                  <td width="16%%" align="right" class="labeltext">Land:</td>
                  <td width="34%%" align="left">
                    <select name="rbz" class="listbox" style="width:150">"""

jghstatneuende_t = """
                    </select>
                  </td>
                </tr>
                <tr height="40">
                  <input type="hidden" value="%(day)d" name="ed">
                  <td width="16%%" align="right" class="labeltext">Ende:</td>
                  <td align="left" nowrap>
                    <input type="text" name="em" value="%(month)d" class="textboxsmall" maxlength="2" size="2">
                  </td>
                  <td width="34%%" align="left" nowrap>
                    <input type="text" name="ey" value="%(year)d" class="textboxmid" maxlength="4" size="4">
                  </td>
                  """

jghstatneukreis_t = """
                  <td width="16%" align="right" class="labeltext" height="26">Kreis:</td>
                  <td width="34%" align="left" height="26">
                    <select name="kr" class="listbox" style="width:150">"""

jghstatneuwbz_t = """
                    </select>
                  </td>
                </tr>
                <tr height="33">
                  <td colspan="3" width="50%%" height="33" >&nbsp;
                  <input type="hidden" value="%d" name="wohnbez"></td>"""

jghstatneugfall_t = """
                  <td width="16%" align="right" class="labeltext" height="33">Geschwisterfall:</td>
                  <td width="34%" align="left" height="33">
                    <select name="gfall" class="listbox" style="width:150">"""

jghstatneuwbz_berlin_t = """
                    </select>
                  </td>
                </tr>
                <tr height="40">
                  <td width="16%" align="right" class="labeltext" height="33" >Wohnbezirk:</td>
                  <td width="34%" align="left" colspan="2" height="33">
                    <select name="wohnbez" class="listbox" style="width:150">"""

jghstatneugfall_berlin_t = """
                    </select>
                  </td>
                  <td width="16%" align="right" class="labeltext" height="33">Geschwisterfall:</td>
                  <td width="34%" align="left" height="33">
                    <select name="gfall" class="listbox" style="width:150">"""

jghstatneutraeger_t = """
                    </select>
                  </td>
                </tr>
              </table>
              </fieldset> </td>
          </tr>
          <tr>
            <td align="center" class="legendtext" valign="top" height="91" colspan="2">
              <fieldset><legend class="legendtext">Beratungsdaten</legend>
              <table width="100%" border="0" cellpadding="1" height="56">
                <tr align="right">
                  <td height="47" colspan="3" class="labeltext"> Tr&auml;ger:</td>
                  <td align="left" height="47" width="60%">
                    <select name="traeg" class="listbox130" style="width:250">"""

jghstatneukontakt_t = """
                    </select>
                  </td>
                </tr>
                <tr align="right">
                  <td height="47" colspan="3" class="labeltext"> 1.Kontakt durch:</td>
                  <td align="left" height="47" width="60%">
                    <select name="zm" class="listbox130" style="width:270">"""

jghstatneuendegrund_t = """
                    </select>
                  </td>
                </tr>
                <tr align="right">
                  <td height="38" colspan="3" class="labeltext">Beendigungsgrund:</td>
                  <td align="left" height="38" width="60%">
                    <select name="bgr" class="listbox130" style="width:270">"""

jghstatneuanlass_t = """
                    </select>
                  </td>
                </tr>
                <tr align="right">
                  <td height="47" colspan="3" class="labeltext">Beratungsanl&auml;sse:</td>
                  <td align="left" height="47" width="60%">
                    <select name="ba" multiple class="listbox130" style="width:270" size="6">"""

jgstatneuschwerpunkt_t = """
                    </select>
                  </td>
                </tr>
                <tr align="right">
                  <td height="42" colspan="3" class="labeltext">Beratungsschwerpunkt:</td>
                  <td align="left" height="42" width="60%" class="labeltext">
                    <select name="schw" class="listbox130" style="width:270" size="1">"""

jghstatneulebtbei_t = """
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

jghstatneugeschlecht_t = """
                    </select>
                  </td>
                  <td align="right" height="35" width="31%" class="labeltext">Geschlecht:</td>
                  <td align="left" height="35" width="14%">
                    <select name="gs" style="width:40">"""

jghstatneualter_t = """
                    </select>
                  </td>
                </tr>
                <tr>
                  <td align="right" height="35" width="21%" class="labeltext">Alter:</td>
                  <td align="left" height="35" width="34%">
                    <select name="ag" style="width:100">"""

jghstatneu_t2a = """
                    </select>
                  </td>
                  <td align="right" height="35" width="31%" class="labeltext">Geschwisteranzahl
                    bekannt:</td>
                  <td align="left" height="35" width="14%">
                      <input type="text" name="gsa" size=2 maxlength=2>"""

jghstatneu_t2b = """
                  </td>
                </tr>
                <tr>
                  <td align="right" height="35" width="21%" class="labeltext">Staatsangeh&ouml;rigkeit:</td>
                  <td align="left" height="35" width="34%">
                    <select class="listbox" name="hke" style="width:100">
                      <option value="" selected >"""

jghstatneu_t3 = """
                    </select>
                  </td>
                  <td align="right" height="35" width="31%%" class="labeltext">Geschwisteranzahl
                    unbekannt:</td>
                  <td align="left" height="35" width="14%%">
                    <input type="checkbox" value="%(id)d" name="gsu">
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
jghstatneu_t4 = """ </td>
                </tr>
                <tr>
                  <td align="right" class="labeltext" width="52%">in der Gruppe:</td>
                  <td align="left" class="labeltext" width="48%">"""

jghstatneu_t5 = """ </td>
                </tr>
              </table>
              </fieldset> </td>
            <td align="center" class="legendtext" valign="top" width="50%" height="77">
              <fieldset><legend class="legendtext">Therapieansatz Eltern</legend>
              <table width="100%" border="0" cellpadding="1">
                <tr>
                  <td align="right" width="52%" class="labeltext">allein:</td>
                  <td align="left" class="labeltext" width="48%">"""

jghstatneu_t6 = """ </td>
                </tr>
                <tr>
                  <td align="right" width="52%" class="labeltext">in der Gruppe:</td>
                  <td align="left" class="labeltext" width="48%">"""

jghstatneu_t7 = """ </td>
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
jghstatneu_t8 = """ </td>
                  <td align="center" class="labeltext" width="50%">"""
jghstatneu_t9 = """ </td>
                </tr>
              </table>
              </fieldset> </td>
          </tr>
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



jghstatedit_t = """
</head>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000">
<table width="735" align="center">
  <tr>
    <td height="465" align="center" valign="top">
      <form name="jghform" method="post" action="klkarte">
        <input type="hidden" value="%(id)s" name="fallid">
        <table border="0" cellpadding="1" width="95%%">
          <tr>
            <td align="center" class="legendtext" valign="top" height="104" colspan="2">
              <fieldset><legend class="legendtext">Falldaten</legend>
              <table width="100%%" border="0" cellpadding="1" height="103">
                """

jghstateditfn_t = """
                <tr height="20">
                  <input type="hidden" value="%(fall_fn)s" name="fall_fn" >
                  <td width="16%%" align="right" class="labeltext" >Fallnummer:</td>
                  <td width="34%%" align="left" colspan="2" class="legendtext">%(fall_fn)s</td>
                  """
jghstateditgemeinde_t = """
                  <input type="hidden" value="%d" name="gm">
                  """
jghstateditgemeindeteil_t = """
                  <input type="hidden" value="%d" name="gmt">
                  """
jghstateditmit_t = """
                  <input type="hidden" value="%(mit_id)d" name="mitid">
                  <td width="16%%" align="right" class="labeltext">Mitarbeiter:</td>
                  <td width="34%%" align="left" class="legendtext">%(mit_name)s</td>
                </tr>
                """
jghstateditbeginn_t = """
                <tr height="20">
                  <input type="hidden" value="%(bgm)s" name="bgm">
                  <input type="hidden" value="%(bgy)s" name="bgy">
                  <td width="16%%" align="right" class="labeltext">Beginn:</td>
                  <td width="16%%" align="left"  colspan="2" class="legendtext">%(bgm)s.%(bgy)s</td>
                  <td width="16%%" align="right" class="labeltext">Land:</td>
                  <td width="34%%" align="left">
                    <select name="rbz" class="listbox" style="width:150">"""

jghstateditende_t = """
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
                  """
jghstateditkreis_t = """
                  <td width="16%" align="right" class="labeltext" height="26">Kreis:</td>
                  <td width="34%" align="left" height="26">
                    <select name="kr" class="listbox" style="width:150">"""

jghstateditwbz_t = """
                    </select>
                  </td>
                </tr>
                <tr height="66" width="100%">
                  <td colspan="3" width="50%" height="66" >&nbsp;</td>"""

jghstateditgfall_t = """
                  <td width="16%" align="right" class="labeltext" height="33">Geschwisterfall:</td>
                  <td width="34%" align="left" height="33">
                    <select name="gfall" class="listbox" style="width:150">"""

jghstateditwbz_berlin_t = """
                    </select>
                  </td>
                </tr>
                <tr height="40">
                  <td width="16%" align="right" class="labeltext" height="33" >Wohnbezirk:</td>
                  <td width="34%" align="left" colspan="2" height="33">
                    <select name="wohnbez" class="listbox" style="width:150">"""

jghstateditgfall_berlin_t = """
                    </select>
                  </td>
                  <td width="16%" align="right" class="labeltext" height="33">Geschwisterfall:</td>
                  <td width="34%" align="left" height="33">
                    <select name="gfall" class="listbox" style="width:150">"""

jghstatedittraeger_t = """

                    </select>
                  </td>
                </tr>
              </table>
              </fieldset> </td>
          </tr>
          <tr>
            <td align="center" class="legendtext" valign="top" height="91" colspan="2">
              <fieldset><legend class="legendtext">Beratungsdaten</legend>
              <table width="100%" border="0" cellpadding="1" height="56">
                <tr align="right">
                  <td height="47" colspan="3" class="labeltext"> Tr&auml;ger:</td>
                  <td align="left" height="47" width="60%" class="labeltext">
                    <select name="traeg" class="listbox130" style="width:250">"""

jghstateditkontakt_t = """

                    </select>
                  </td>
                </tr>
                <tr align="right">
                  <td height="47" colspan="3" class="labeltext"> 1.Kontakt durch:</td>
                  <td align="left" height="47" width="60%" class="labeltext">
                    <select name="zm" class="listbox130" style="width:270">"""

jghstateditendegrund_t = """

                    </select>
                  </td>
                </tr>
                <tr align="right">
                  <td height="38" colspan="3" class="labeltext">Beendigungsgrund:</td>
                  <td align="left" height="38" width="60%" class="labeltext">
                    <select name="bgr" class="listbox130" style="width:270">"""

jghstateditanlass_t = """

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

jghstateditlebtbei_t = """

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

jghstateditgeschlecht_t = """

                    </select>
                  </td>
                  <td align="right" height="35" width="31%" class="labeltext">Geschlecht:</td>
                  <td align="left" height="35" width="14%">
                    <select name="gs" style="width:40">"""

jghstateditalter_t = """

                    </select>
                  </td>
                </tr>
                <tr>
                  <td align="right" height="35" width="21%" class="labeltext">Alter:</td>
                  <td align="left" height="35" width="34%">
                    <select name="ag" style="width:100">"""

jghstatedit_t2a = """

                    </select>
                  </td>
                  <td align="right" height="35" width="31%%" class="labeltext">Geschwisteranzahl
                    bekannt:</td>
                  <td align="left" height="35" width="14%%">
                   <input type="text" name="gsa" size=2 maxlength=2 value="%s">"""

jghstatedit_t2b = """
                  </td>
                </tr>
                <tr>
                  <td align="right" height="35" width="21%%" class="labeltext">Staatsangeh&ouml;rigkeit:</td>
                  <td align="left" height="35" width="34%%">
                    <select class="listbox" name="hke" style="width:100">
                      <option value=""> """

jghstatedit_t3 = """
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

jghstatedit_t4 = """ </td>
                </tr>
                <tr>
                  <td align="right" class="labeltext" width="52%">in der Gruppe:</td>
                  <td align="left" class="labeltext" width="48%">"""
jghstatedit_t5 = """ </td>
                </tr>
              </table>
              </fieldset> </td>
            <td align="center" class="legendtext" valign="top" width="50%" height="77">
              <fieldset><legend class="legendtext">Therapieansatz Eltern</legend>
              <table width="100%" border="0" cellpadding="1">
                <tr>
                  <td align="right" width="45%" class="labeltext">allein:</td>
                  <td width="55%">"""
jghstatedit_t6 = """ </td>
                </tr>
                <tr>
                  <td align="right" width="45%" class="labeltext">in der Gruppe:</td>
                  <td width="55%">"""

jghstatedit_t7 = """ </td>
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

jghstatedit_t8 = """ </td>
                  <td align="center" class="labeltext" width="50%">"""
jghstatedit_t9 = """ </td>
                </tr>
              </table>
              </fieldset> </td>
          </tr>
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

jghansaetzefamilie_t = """in der Familie <input type="checkbox" value="%(id)d" name="%(kat_code)s" > """

jghansaetzeumfeld_t = """im sozialen Umfeld <input type="checkbox" value="%(id)d" name="%(kat_code)s" >"""

jghansaetzefamiliecheck_t = """in der Familie <input type="checkbox" checked value="%(id)d" name="%(kat_code)s" > """

jghansaetzeumfeldcheck_t = """im sozialen Umfeld <input type="checkbox" checked value="%(id)d" name="%(kat_code)s" >"""

thupdstausw_t = """
</head>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000">
<table width="735" align="center">
  <tr>
    <td height="200" align="center" valign="top">
      <form name="jghform" method="post" action="updjgh">
        <table border="0" cellpadding="1" width="95%%">
          <tr>
            <td align="center" class="legendtext" valign="top"> <fieldset><legend class="legendtext">%(legendtext)s</legend>
              <table width="90%%" border="0" cellpadding="1">
                <tr height="40">
                  <td width="20%%" align="center" class="labeltext" >
                  <select size=10 class="listbox" name="jghid">"""

updfsausw1_t = """
     <option value="%(id)s" >%(fall_fn)s | %(jahr)s | %(mit_id__na)s """

updjghausw1_t = """
     <option value="%(id)s" >%(fall_fn)s | %(ey)s | %(mit_id__na)s """

updstausw2_t = """
                  </select>
                  </td>
                </tr>
              </table>
              <table width="95%%" border="0" cellpadding="1">
                <tr height="40">
                  <td width="33%%" align="center" valign="middle">
                    <input type="submit" name="" value="Bearbeiten" class="button">
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
    </td>
  </tr>
</table>
</body>
</html>"""
