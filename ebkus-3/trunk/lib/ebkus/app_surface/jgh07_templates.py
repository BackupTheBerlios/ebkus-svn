# coding: latin-1


jghhead_t = """
</head>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000">
<table width="800" align="center">
  <tr>
    <td height="465" align="center" valign="top">
      <form name="jghform" method="post" action="jgh_check">
        <input type="hidden" value="%(fall_id)s" name="fallid">
        <input type="hidden" value="%(fall_fn)s" name="fall_fn" >
        <input type="hidden" value="%(stz)s" name="stz" >
        <input type="hidden" value="%(jghid)s" name="jghid" >
        <input type="hidden" value="%(file)s" name="file" >
        <input type="hidden" value="%(mit_id)d" name="mitid">
        <table border="0" cellpadding="1" width="95%%">"""

jghfalldaten_t = """
          <tr>
            <td align="center" class="legendtext" valign="top" height="104" colspan="2">
              <fieldset><legend class="legendtext">Falldaten</legend>
              <table width="100%%" border="0" cellpadding="1">
                <tr>
                  <td width="16%%" align="right" class="labeltext" >Fallnummer:</td>
                  <td width="34%%" align="left" class="legendtext">%(fall_fn)s</td>
                  <td  align="right" class="labeltext">Land:</td>
                  <td  align="left">
                    <select name="land" class="listbox" style="width:180">
                   %(land_sel)s
                    </select>
                  </td>
                </tr>
                <tr>
                  <td  align="right" class="labeltext">Beginn:</td>
                  <td  align="left"  class="legendtext">%(bgm)s.%(bgy)s</td>
                  <td  align="right" class="labeltext">Kreis:</td>
                  <td  align="left">
                    <select name="kr" class="listbox" style="width:180">
                    %(kr_sel)s                    
                    </select>
                  </td>
                </tr>
                <tr>
                  <td  align="right" class="labeltext">Mitarbeiter:</td>
                  <td  align="left" class="legendtext">%(mit_id__ben)s</td>
                  <td  align="right" class="labeltext">Einrichtungs-Nr.:</td>
                  <td  align="left">
                    <select name="einrnr" class="listbox" style="width:180">
                    %(einrnr_sel)s                    
                    </select>
                  </td>
                </tr>
                <tr>
                  <td  align="right" class="labeltext">Geschwisterfall:</td>
                  <td  align="left">
                    <select name="gfall" class="listbox" style="width:70">
                    %(gfall_sel)s                    
                    </select>
                  </td>
                  <td  align="right" class="labeltext">Laufende-Nr.:</td>
                  <td  align="left" class="legendtext">%(laufendenr)s</td>
                </tr>
                %(wohnbez_kl)s
              </table>
              </fieldset>
            </td>
          </tr>"""

jghwohnbez_klient_t = """
                <tr>
                  <td  colspan=4>
                  <input type="hidden" name="wohnbez" value="%d">
                  </td>
                </tr>"""
jghwohnbez_klient_berlin_t = """
                <tr>
                  <td  align="right" class="labeltext">Wohnbezirk des Klienten:</td>
                  <td  align="left">
                    <select name="wohnbez" class="listbox" style="width:180">
                    %s                    
                    </select>
                  </td>
                  <td></td>
                  <td></td>
                </tr>"""

jghbuttons_t = """
          <tr>
            <td align="center" class="legendtext" valign="middle" colspan="3">
              <fieldset><legend class="legendtext"></legend>
              <table width="100%%" border="0" cellpadding="1">
                <tr>
                  <td width="33%%" align="center">
                    <input type="submit" name="" value="Speichern" class="button">
                  </td>
                  <td align="center" width="33%%">
                    <input type="reset" value="Zur&uuml;cksetzen" class="button">
                  </td>
                  <td align="center" width="34%%">
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

fb_abschnitt_t = """
          <tr>
            <td align="center" class="legendtext" valign="top" colspan="2">
              <fieldset><legend class="legendtext">%(abschnitt)s %(title)s</legend>
              <table width="100%%" border="0" cellpadding="1">
%(items)s
              </table>
              </fieldset>
            </td>
          </tr>"""

fb_select_one_item_t = """
                <tr>
                  <td align="left" width="35%%" class="labeltext">
                  %(frage)s:
                  </td>
                  <td align="left" valign="bottom">
                    <select %(onChange)s name="%(name)s" class="listbox" style="width:%(width)s">
                    %(options)s
                    </select>
                  </td>
                </tr>"""
fb_option_t = """
      <option value="%(id)d" title="%(name)s" %(sel)s > %(name)s """

fb_int_item_t = """
                <tr>
                  <td align="left" width="35%%" class="labeltext">
                  %(frage)s:
                  </td>
                  <td align="left" valign="bottom">
                    <input type="text" name="%(name)s" value="%(value)s"
                    size="%(size)s" maxlength="%(size)s" %(ro)s>
                  </td>
                </tr>"""

fb_checkbox_item_t = """
                <tr>
                  <td align="left" width="35%%" class="labeltext">
                  %(frage)s:
                  </td>
                  <td align="left" valign="bottom">
                    <input type="checkbox" name="%(name)s" value="%(value)s" %(checked)s>
                  </td>
                </tr>"""

fb_k_header_t = """
                <tr>
                  <td align="left" width="67%">
                  Gründe (bitte 1 - 3 Gründe ankreuzen)
                  </td>
                  <td align="center" width="11%">Hauptgrund</td>
                  <td align="center" width="11%">2. Grund</td>
                  <td align="center" width="11%">3. Grund</td>
                </tr>"""
fb_k_item_t = """
                <tr>
                  <td align="left" class="labeltext">
                  %(frage)s:
                  </td>
                  <td align="center" valign="bottom">
                    <input type="checkbox" name="gr1" value="%(id)s" %(ch1)s>
                  </td>
                  <td align="center" valign="bottom">
                    <input type="checkbox" name="gr2" value="%(id)s" %(ch2)s>
                  </td>
                  <td align="center" valign="bottom">
                    <input type="checkbox" name="gr3" value="%(id)s" %(ch3)s>
                  </td>
                </tr>"""

fb_k_last_item_t = """
                <tr>
                  <td align="left" class="labeltext">
                  %(frage)s:
                  </td>
                  <td align="center" valign="bottom">
                    <input type="checkbox" name="gr1" value="%(id)s" %(ch3)s>
                  </td>
                  <td align="center" valign="bottom">
                            </td>
                  <td align="center" valign="bottom">
                            </td>
                </tr>"""

fb_zwischenueberschrift_t = """
                <tr>
                  <td align="left"
 style="font-family:Arial,Helvetica,sans-serif;font-size:11pt;font-weight:bold" colspan="2">
                  %s
                  </td>
                </tr>"""

fb_item_trenner_t = """
                <tr><td colspan="2" height="5"></td></tr>"""
fb_abschnitt_trenner_t = """
          <tr><td height="12"></td></tr>"""
