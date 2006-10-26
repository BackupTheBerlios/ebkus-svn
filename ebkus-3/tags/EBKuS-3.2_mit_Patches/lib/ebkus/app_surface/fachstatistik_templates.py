# coding: latin-1
##*************************************************************************
##
## Formular: Erstellen einer neuen Fachstatistik
##
##*************************************************************************

fsneu_t1 = """
</head>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000">
<table width="735" align="center">
  <tr>
    <td height="465" align="center" valign="top">
      <form name="fachstatform" method="post" action="klkarte">
        <table border="0" cellpadding="1" width="95%%">
          <tr>
            <td align="center" class="legendtext" valign="top"> <fieldset><legend class="legendtext">Falldaten</legend>
              <table width="90%%" border="0" cellpadding="1">
                <tr height="40">
                  <td width="20%%" align="right" class="labeltext" >Fallnummer:</td>"""
fsneu_fn_t = """
                  <input type="hidden" value="%(akte_id__stzak)s" name="stz">
                  <input type="hidden" value="%(id)s" name="fallid">
                  <input type="hidden" value="%(fn)s" name="fall_fn">
                  <td width="10%%" align="left" class="legendtext">%(fn)s</td>
                  <td width="20%%" align="right" class="labeltext" >Mitarbeiter:</td>"""

fsneu_mit_t = """
                  <input type="hidden" value="%(mit_id)d" name="mitid">
                  <td width="20%%" align="left" class="legendtext">%(mit_name)s</td>
                  <td width="10%%" align="right" class="labeltext" >Jahr:</td>
                  <td width="20%%">"""


fsneu_jahr_t = """
                    <input type="text" size="4" maxlength=4 name="jahr" value="%(year)d" class="textboxmid">
                  </td>
                </tr>
              </table>
              </fieldset> </td>
          </tr>
          <tr>
"""

fsneu_region_t = """
          <tr>
            <td align="center" class="legendtext" valign="top"> <fieldset><legend class="legendtext">Angaben
              zum Klienten und dessen Angeh&ouml;rige</legend>
              <table width="90%%" height="200" border="0" cellpadding="1">
                <tr>
                  <td width="20%%" align="right" class="labeltext">Planungsraum:
                  </td>
                  <input type="hidden" value="%(planungsr)s" name="plr">
                  <td width="20%%" align="left" class="legendtext">%(planungsr)s</td>
                  """

fsneu_geschlecht_t = """
                  <td width="16%" align="right" class="labeltext">&nbsp; </td>
                  <td width="32%" align="left">&nbsp; </td>
                </tr>
                <tr>
                  <td width="20%" align="right" class="labeltext" >Geschlecht:</td>
                  <td width="32%" align="left">
                    <select name="gs" class="listbox130" style="width:180">
                      <option value=" " selected >"""

fsneu_altersgr_t = """
                    </select>
                  </td>
                  <td width="16%" align="right" class="labeltext">Alter Kind:</td>
                  <td width="32%" align="left">
                    <select name="ag" style="width:180">"""

fsneu_famstatus_t = """

                    </select>
                  </td>
                </tr>
                <tr>
                  <td width="20%" align="right" class="labeltext" >Lebensmittelpunkt
                    des Kindes:</td>
                  <td width="32%" align="left">
                    <select name="fs" class="listbox130" style="width:180">
                    """

fsneu_zugangsmodus_t = """

                    </select>
                  </td>
                  <td width="16%" align="right" class="labeltext">Empfohlen von:</td>
                  <td width="32%" align="left">
                    <select name="zm" style="width:180">
                      <option value=" " selected >"""

fsneu_qualikind_t= """
                    </select>
                  </td>
                </tr>
                <tr>
                  <td width="20%" align="right" class="labeltext" >Qualifikation Jugendlicher:</td>
                  <td width="32%" align="left">
                    <select name="qualij" class="listbox130" style="width:180">
                    <option value=" " selected >"""


fsneu_qualimutter_t = """
                    </select>
                  </td>
                  <td width="16%" align="right" class="labeltext">&nbsp;</td>
                  <td width="16%" align="right" class="labeltext">&nbsp;</td>
                </tr>
                <tr><td colspan="4"s>&nbsp;</td></tr>
                <tr>
                  <td width="20%" align="right" class="labeltext" >Qualifikation
                    Mutter</td>
                  <td width="32%" align="left">
                    <select name="qualikm" class="listbox130" style="width:180">
                      <option value=" " selected >"""

fsneu_qualivater_t = """
                    </select>
                  </td>
                  <td width="16%" align="right" class="labeltext">Qualifikation
                    Vater </td>
                  <td width="32%" align="left">
                    <select name="qualikv" class="listbox130" style="width:180">
                      <option value=" " selected >"""

fsneu_berufmutter_t = """
                    </select>
                  </td>
                </tr>
                <tr>
                  <td width="20%" align="right" class="labeltext" >Beruf Mutter:</td>
                  <td width="32%" align="left">
                    <select name="bkm" class="listbox130" style="width:180">
                      <option value=" " selected >"""

fsneu_berufvater_t = """
                    </select>
                  </td>
                  <td width="16%" align="right" class="labeltext">Beruf Vater:</td>
                  <td width="32%" align="left">
                    <select name="bkv" style="width:180">
                      <option value=" " selected >"""

fsneu_hkmutter_t = """
                    </select>
                  </td>
                </tr>
                <tr>
                  <td width="20%" align="right" class="labeltext" >Herkunftsland
                    Mutter:</td>
                  <td width="32%" align="left">
                    <select name="hkm" class="listbox130" style="width:180">
                      <option value=" " selected >"""

fsneu_hkvater_t = """
                    </select>
                  </td>
                  <td width="16%" align="right" class="labeltext">Herkunftsland
                    Vater:</td>
                  <td width="32%" align="left">
                    <select name="hkv" style="width:180">
                      <option value=" " selected >"""

fsneu_altermutter_t = """
                    </select>
                  </td>
                </tr>
                <tr>
                  <td width="20%" align="right" class="labeltext" height="39" >Alter
                    Mutter:</td>
                  <td width="32%" align="left" height="39">
                    <select name="agkm" class="listbox130" style="width:180">
                      <option value=" " selected >"""

fsneu_altervater_t = """
                    </select>
                  </td>
                  <td width="16%" align="right" class="labeltext" height="39">Alter
                    Vater:</td>
                  <td width="32%" align="left" height="39">
                    <select name="agkv" style="width:180">
                      <option value=" " selected >"""

fsneu_beratungsanlass1_t = """
                    </select>
                  </td>
                </tr>
              </table>
              </fieldset> </td>
          </tr>
          <tr>
            <td align="center" class="legendtext" valign="top"> <fieldset><legend class="legendtext">Problem 1
              bei der Anmeldung</legend>
              <table width="90%" border="0" cellpadding="1">
                <tr>
                  <td align="center" height="40">
                    <select name="ba1" class="listbox130" style="width:310">
                    <option value=" " selected >"""

fsneu_beratungsanlass2_t = """
                    </select>
                  </td>
                <tr>
              </table>
              </fieldset> </td>
          </tr>
          <tr>
            <td align="center" class="legendtext" valign="top"> <fieldset><legend class="legendtext">Problem 2
              bei der Anmeldung</legend>
              <table width="90%" border="0" cellpadding="1">
                <tr>
                  <td align="center" height="40">
                    <select name="ba2" class="listbox130" style="width:310">
                    <option value=" " selected >"""

fsneu_problemkind_t = """
                    </select>
                  </td>
                <tr>
              </table>
              </fieldset> </td>
          </tr>
          <tr>
            <td align="center" class="legendtext" valign="top"> <fieldset><legend class="legendtext">Hauptproblematik
              Kind / Jugendliche</legend>
              <table width="90%" border="0" cellpadding="1">
                <tr>
                  <td align="center" height="40">
                    <select name="pbk" class="listbox130" style="width:310">
                    <option value=" " selected >"""

fsneu_problemeltern_t = """
                    </select>
                  </td>
                <tr>
              </table>
              </fieldset> </td>
          </tr>
          <tr>
            <td align="center" class="legendtext" valign="top"> <fieldset><legend class="legendtext">Hauptproblematik
              der Eltern</legend>
              <table width="90%" border="0" cellpadding="1">
                <tr>
                  <td align="center" height="40">
                    <select name="pbe" class="listbox130" style="width:310">
                    <option value=" " selected >"""

fsneu_problemspektrumkind_t = """
                    </select>
                  </td>
                <tr>
              </table>
              </fieldset> </td>
          </tr>
          <tr>
            <td align="center" class="legendtext" valign="top"> <fieldset><legend class="legendtext">Problemspektrum
              Kind / Jugendliche</legend>
              <table width="90%" border="0" cellpadding="1" height="186">
                <tr>
                  <td align="center">
                    <select name="pbkind" multiple size="8" class="listbox130" style="width:310">"""

fsneu_problemkindnot_t = """
                    </select>
                  </td>
                <tr>
                <tr>
                  <td align="center" class="labeltext" height="15"> Andersgeartete
                    Problemlage: </td>
                <tr>
                <tr>
                  <td align="center">
                    <input type="text" size="30"  name="no2" class="textboxlarge" style="width:310">
                  </td>
                <tr>
              </table>
              </fieldset> </td>
          </tr>"""

fsneu_problemspektrumeltern_t = """
          <tr>
            <td align="center" class="legendtext" valign="top"> <fieldset><legend class="legendtext">Problemspektrum
              Eltern</legend>
              <table width="90%" border="0" cellpadding="1" height="186">
                <tr>
                  <td align="center">
                    <select name="pbeltern" multiple size="8" class="listbox130" style="width:310">"""


fsneu_problemelternnot_t = """
                    </select>
                  </td>
                <tr>
                <tr>
                  <td align="center" class="labeltext" height="15"> Andersgeartete
                    Problemlage: </td>
                <tr>
                <tr>
                  <td align="center">
                    <input type="text" size="30" name="no3" class="textboxlarge" style="width:310">
                  </td>
                <tr>
              </table>
              </fieldset> </td>
          </tr>"""

fsneu_massnahmen_t = """
          <tr>
            <td align="center" class="legendtext" valign="top"> <fieldset><legend class="legendtext">Erbrachte
              Leistungen</legend>
              <table width="90%" border="0" cellpadding="1" height="166">
                <tr>
                  <td align="center" height="159">
                    <select name="le" multiple size="8" class="listbox130" style="width:310">"""

fsneu_zahlkontakte_t = """
                    </select>
                  </td>
              </table>
              </fieldset> </td>
          </tr>
                  <tr>
            <td align="center" class="legendtext" valign="top" height="93"> <fieldset><legend class="legendtext">Terminsumme</legend>

    <table width="90%" border="0" cellpadding="1">
      <tr>
        <td align="right" class="labeltext" width="7%">KiMu</td>
        <td align="left" width="12%">
          <input type="text" size="3" value="0" class="textboxmid" name="kkm"  onBlur="set_term_sum_fachstat('kkm')">
        </td>
        <td align="right" class="labeltext" width="6%">KiVa</td>
        <td align="left" width="12%">
          <input type="text" size="3" value="0" class="textboxmid" name="kkv" onBlur="set_term_sum_fachstat('kkv')">
        </td>
        <td align="right" class="labeltext" width="6%">Kind</td>
        <td align="left" width="12%">
          <input type="text" size="3" value="0" class="textboxmid" name="kki" onBlur="set_term_sum_fachstat('kki')">
        </td>
        <td align="right" class="labeltext" width="9%">Familie</td>
        <td align="left" width="12%">
          <input type="text" size="3" value="0" class="textboxmid" name="kfa" onBlur="set_term_sum_fachstat('kfa')">
        </td>
        <td align="right" class="labeltext" width="10%">Lehrer</td>
        <td align="left" width="4%">
          <input type="text" size="3" value="0" class="textboxmid" name="kleh" onBlur="set_term_sum_fachstat('kleh')">
        </td>
          <td align="right" height="40" class="legendtext" width="10%">Summe:</td>
        <td align="left" height="40" class="legendtext" width="4%">
          <input type="text" size="3" value="0" class="textboxmid" name="kat" onBlur="set_term_sum_fachstat('kat')">
        </td>
      <tr>
        <td align="right" class="labeltext" width="7%">Paar </td>
        <td align="left" width="12%">
          <input type="text" size="3" value="0" class="textboxmid" name="kpa" onBlur="set_term_sum_fachstat('kpa')">
        </td>
        <td align="right" class="labeltext" width="6%">Soz.</td>
        <td align="left" width="12%">
          <input type="text" size="3" value="0" class="textboxmid" name="ksoz" onBlur="set_term_sum_fachstat('ksoz')">
        </td>
        <td align="right" class="labeltext" width="6%">Erz.</td>
        <td align="left" width="12%">
          <input type="text" size="3" value="0" class="textboxmid" name="kerz" onBlur="set_term_sum_fachstat('kerz')">
        </td>
        <td align="right" class="labeltext" width="9%">Sonst.</td>
        <td align="left" width="12%">
          <input type="text" size="3" value="0" class="textboxmid" name="kson" onBlur="set_term_sum_fachstat('kson')">
        </td>
        <td align="left" width="10%" class="labeltext">Hilfebespr.</td>
        <td align="left" width="10%">
          <input type="text" size="3" value="0" class="textboxmid" name="kkonf" onBlur="set_term_sum_fachstat('kkonf')">
        </td>
        <td align="left" height="40" class="legendtext" width="10%">&nbsp;</td>
        <td align="left" height="40" class="legendtext" width="10%">&nbsp; </td>
    </table>
              </fieldset> </td>
          </tr>"""

fsneu_notizsubmit_t = """
                  <tr>
            <td align="center" class="legendtext" valign="top"> <fieldset><legend class="legendtext">Notiz</legend>
              <table width="90%" border="0" cellpadding="1">
                <tr>
                  <td align="center" height="40">
                    <input type="text" size="30" maxlength=255 class="textboxlarge" style="width:310">
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

##*************************************************************************
##
## Formular: Updaten einer Fachstatistik
##
##*************************************************************************

fsupd_t1 = """
</head>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000">
<table width="735" align="center">
  <tr>
    <td height="465" align="center" valign="top">
      <form name="fachstatform" method="post" action="klkarte">
        <table border="0" cellpadding="1" width="95%%">
          <tr>
            <td align="center" class="legendtext" valign="top"> <fieldset><legend class="legendtext">Falldaten</legend>
              <table width="90%%" border="0" cellpadding="1">
                <tr height="40">
                  <td width="20%%" align="right" class="labeltext" >Fallnummer:</td>"""
fsupd_fn_t = """
                  <input type="hidden" value="%(id)s" name="fsid">
                  <input type="hidden" value="%(fall_id)s" name="fallid">
                  <input type="hidden" value="%(stz)s" name="stz">
                  <input type="hidden" value="%(fall_fn)s" name="fall_fn">
                  <td width="10%%" align="left" class="legendtext">%(fall_fn)s</td>
                  <td width="20%%" align="right" class="labeltext" >Mitarbeiter:</td>"""

fsupd_mit_t = """
                  <input type="hidden" value="%(mit_id)d" name="mitid">
                  <td width="20%%" align="left" class="legendtext">%(mit_name)s</td>
                  <td width="10%%" align="right" class="labeltext" >Jahr:</td>
                  <td width="20%%">"""


fsupd_jahr_t = """
                    <input type="text" size="4" maxlength=4 name="jahr" value="%(year)d" class="textboxmid">
                  </td>
                </tr>
              </table>
              </fieldset> </td>
          </tr>
          <tr>
"""

fsupd_region_t = """
          <tr>
            <td align="center" class="legendtext" valign="top"> <fieldset><legend class="legendtext">Angaben
              zum Klienten und dessen Angeh&ouml;rige</legend>
              <table width="90%%" height="200" border="0" cellpadding="1">
                <tr>
                  <td width="20%%" align="right" class="labeltext">Planungsraum: </td>
                   <td width="20%%" align="left" name="plr" class="legendtext">%s</td>"""

fsupd_geschlecht_t = """
                  <td width="16%" align="right" class="labeltext">&nbsp; </td>
                  <td width="32%" align="left">&nbsp; </td>
                </tr>
                <tr>
                  <td width="20%" align="right" class="labeltext" >Geschlecht:</td>
                  <td width="32%" align="left">
                    <select name="gs" class="listbox130" style="width:180">
                    <option value=" " selected >"""

fsupd_altersgr_t = """
                    </select>
                  </td>
                  <td width="16%" align="right" class="labeltext">Alter Kind:</td>
                  <td width="32%" align="left">
                    <select name="ag" style="width:180">"""

fsupd_famstatus_t = """
                   </select>
                  </td>
                </tr>
                <tr>
                  <td width="20%" align="right" class="labeltext" >Lebensmittelpunkt
                    des Kindes:</td>
                  <td width="32%" align="left">
                    <select name="fs" class="listbox130" style="width:180">"""

fsupd_zugangsmodus_t = """
                    </select>
                  </td>
                  <td width="16%" align="right" class="labeltext">Empfohlen von:</td>
                  <td width="32%" align="left">
                    <select name="zm" style="width:180">
                    <option value=" " selected >"""

fsupd_qualikind_t= """
                    </select>
                  </td>
                </tr>
                <tr>
                  <td width="20%" align="right" class="labeltext" >Qualifikation Jugendlicher:</td>
                  <td width="32%" align="left">
                    <select name="qualij" class="listbox130" style="width:180">
                    <option value=" " selected >"""


fsupd_qualimutter_t = """
                    </select>
                  </td>
                  <td width="16%" align="right" class="labeltext">&nbsp;</td>
                  <td width="16%" align="right" class="labeltext">&nbsp;</td>
                </tr>
                <tr><td colspan="4"s>&nbsp;</td></tr>
                <tr>
                  <td width="20%" align="right" class="labeltext" >Qualifikation
                    Mutter</td>
                  <td width="32%" align="left">
                    <select name="qualikm" class="listbox130" style="width:180">
                      <option value=" " selected >"""

fsupd_qualivater_t = """
                    </select>
                  </td>
                  <td width="16%" align="right" class="labeltext">Qualifikation
                    Vater </td>
                  <td width="32%" align="left">
                    <select name="qualikv" class="listbox130" style="width:180">
                      <option value=" " selected >"""


fsupd_berufmutter_t = """
                    </select>
                  </td>
                </tr>
                <tr>
                  <td width="20%" align="right" class="labeltext" >Beruf Mutter:</td>
                  <td width="32%" align="left">
                    <select name="bkm" class="listbox130" style="width:180">
                    <option value=" " selected >"""

fsupd_berufvater_t = """
                    </select>
                  </td>
                  <td width="16%" align="right" class="labeltext">Beruf Vater:</td>
                  <td width="32%" align="left">
                    <select name="bkv" style="width:180">
                    <option value=" " selected >"""

fsupd_hkmutter_t = """
                    </select>
                  </td>
                </tr>
                <tr>
                  <td width="20%" align="right" class="labeltext" >Herkunftsland
                    Mutter:</td>
                  <td width="32%" align="left">
                    <select name="hkm" class="listbox130" style="width:180">
                    <option value=" " selected >"""

fsupd_hkvater_t = """
                    </select>
                  </td>
                  <td width="16%" align="right" class="labeltext">Herkunftsland
                    Vater:</td>
                  <td width="32%" align="left">
                    <select name="hkv" style="width:180">
                    <option value=" " selected >"""
fsupd_altermutter_t = """
                    </select>
                  </td>
                </tr>
                <tr>
                  <td width="20%" align="right" class="labeltext" height="39" >Alter
                    Mutter:</td>
                  <td width="32%" align="left" height="39">
                    <select name="agkm" class="listbox130" style="width:180">
                    <option value=" " selected >"""

fsupd_altervater_t = """
                    </select>
                  </td>
                  <td width="16%" align="right" class="labeltext" height="39">Alter
                    Vater:</td>
                  <td width="32%" align="left" height="39">
                    <select name="agkv" style="width:180">
                    <option value=" " selected >"""

fsupd_beratungsanlass1_t = """
                    </select>
                  </td>
                </tr>
              </table>
              </fieldset> </td>
          </tr>
          <tr>
            <td align="center" class="legendtext" valign="top"> <fieldset><legend class="legendtext">Problem 1
              bei der Anmeldung</legend>
              <table width="90%" border="0" cellpadding="1">
                <tr>
                  <td align="center" height="40">
                    <select name="ba1" class="listbox130" style="width:310">
                    <option value=" " selected >"""

fsupd_beratungsanlass2_t = """
                    </select>
                  </td>
                <tr>
              </table>
              </fieldset> </td>
          </tr>
          <tr>
            <td align="center" class="legendtext" valign="top"> <fieldset><legend class="legendtext">Problem 2
              bei der Anmeldung</legend>
              <table width="90%" border="0" cellpadding="1">
                <tr>
                  <td align="center" height="40">
                    <select name="ba2" class="listbox130" style="width:310">
                    <option value=" " selected >"""

fsupd_problemkind_t = """
                    </select>
                  </td>
                <tr>
              </table>
              </fieldset> </td>
          </tr>
          <tr>
            <td align="center" class="legendtext" valign="top"> <fieldset><legend class="legendtext">Hauptproblematik
              Kind / Jugendliche</legend>
              <table width="90%" border="0" cellpadding="1">
                <tr>
                  <td align="center" height="40">
                    <select name="pbk" class="listbox130" style="width:310">
                    <option value=" " selected >"""

fsupd_problemeltern_t = """
                    </select>
                  </td>
                <tr>
              </table>
              </fieldset> </td>
          </tr>
          <tr>
            <td align="center" class="legendtext" valign="top"> <fieldset><legend class="legendtext">Hauptproblematik
              der Eltern</legend>
              <table width="90%" border="0" cellpadding="1">
                <tr>
                  <td align="center" height="40">
                    <select name="pbe" class="listbox130" style="width:310">
                    <option value=" " selected >"""

fsupd_problemspektrumkind_t = """
                    </select>
                  </td>
                <tr>
              </table>
              </fieldset> </td>
          </tr>
          <tr>
            <td align="center" class="legendtext" valign="top"> <fieldset><legend class="legendtext">Problemspektrum
              Kind / Jugendliche</legend>
              <table width="90%" border="0" cellpadding="1" height="186">
                <tr>
                  <td align="center">
                    <select name="pbkind" multiple size="8" class="listbox130" style="width:310">"""

fsupd_problemkindnot_t = """
                    </select>
                  </td>
                <tr>
                <tr>
                  <td align="center" class="labeltext" height="15"> Andersgeartete
                    Problemlage: </td>
                <tr>
                <tr>
                  <td align="center">
                    <input type="text" size="30"  value="%s" name="no2" class="textboxlarge" style="width:310">
                  </td>
                <tr>
              </table>
              </fieldset> </td>
          </tr>"""

fsupd_problemspektrumeltern_t = """
          <tr>
            <td align="center" class="legendtext" valign="top"> <fieldset><legend class="legendtext">Problemspektrum
              Eltern</legend>
              <table width="90%" border="0" cellpadding="1" height="186">
                <tr>
                  <td align="center">
                    <select name="pbeltern" multiple size="8" class="listbox130" style="width:310">"""


fsupd_problemelternnot_t = """
                    </select>
                  </td>
                <tr>
                <tr>
                  <td align="center" class="labeltext" height="15"> Andersgeartete
                    Problemlage: </td>
                <tr>
                <tr>
                  <td align="center">
                    <input type="text" size="30" value="%s" name="no3" class="textboxlarge" style="width:310">
                  </td>
                <tr>
              </table>
              </fieldset> </td>
          </tr>"""

fsupd_massnahmen_t = """
          <tr>
            <td align="center" class="legendtext" valign="top"> <fieldset><legend class="legendtext">Erbrachte
              Leistungen</legend>
              <table width="90%" border="0" cellpadding="1" height="166">
                <tr>
                  <td align="center" height="159">
                    <select name="le" multiple size="8" class="listbox130" style="width:310">"""

fsupd_zahlkontakte_t = """
                    </select>
                  </td>
              </table>
              </fieldset> </td>
          </tr>
                  <tr>
            <td align="center" class="legendtext" valign="top" height="93"> <fieldset><legend class="legendtext">Terminsumme</legend>

    <table width="90%%" border="0" cellpadding="1">
      <tr>
        <td align="right" class="labeltext" width="7%%">KiMu</td>
        <td align="left" width="12%%">
          <input type="text" size="3" value="%(kkm)d" class="textboxmid" name="kkm"  onBlur="set_term_sum_fachstat('kkm')">
        </td>
        <td align="right" class="labeltext" width="6%%">KiVa</td>
        <td align="left" width="12%%">
          <input type="text" size="3" value="%(kkv)d" class="textboxmid" name="kkv" onBlur="set_term_sum_fachstat('kkv')">
        </td>
        <td align="right" class="labeltext" width="6%%">Kind</td>
        <td align="left" width="12%%">
          <input type="text" size="3" value="%(kki)d" class="textboxmid" name="kki" onBlur="set_term_sum_fachstat('kki')">
        </td>
        <td align="right" class="labeltext" width="9%%">Familie</td>
        <td align="left" width="12%%">
          <input type="text" size="3" value="%(kfa)d" class="textboxmid" name="kfa" onBlur="set_term_sum_fachstat('kfa')">
        </td>
        <td align="right" class="labeltext" width="10%%">Lehrer</td>
        <td align="left" width="8%%">
          <input type="text" size="3" value="%(kleh)d" class="textboxmid" name="kleh" onBlur="set_term_sum_fachstat('kleh')">
        </td>
          <td align="right" height="40" class="legendtext" width="10%%">Summe:</td>
        <td align="left" height="40" class="legendtext" width="8%%">
          <input type="text" size="3" value="%(kat)d" class="textboxmid" name="kat" onBlur="set_term_sum_fachstat('kat')">
        </td>
      <tr>
        <td align="right" class="labeltext" width="7%%">Paar </td>
        <td align="left" width="12%%">
          <input type="text" size="3" value="%(kpa)d" class="textboxmid" name="kpa" onBlur="set_term_sum_fachstat('kpa')">
        </td>
        <td align="right" class="labeltext" width="6%%">Soz.</td>
        <td align="left" width="12%%">
          <input type="text" size="3" value="%(ksoz)d" class="textboxmid" name="ksoz" onBlur="set_term_sum_fachstat('ksoz')">
        </td>
        <td align="right" class="labeltext" width="6%%">Erz.</td>
        <td align="left" width="12%%">
          <input type="text" size="3" value="%(kerz)d" class="textboxmid" name="kerz" onBlur="set_term_sum_fachstat('kerz')">
        </td>
        <td align="right" class="labeltext" width="9%%">Sonst.</td>
        <td align="left" width="12%%">
          <input type="text" size="3" value="%(kson)d" class="textboxmid" name="kson" onBlur="set_term_sum_fachstat('kson')">
        </td>
        <td align="left" width="6%%" class="labeltext">Hilfebespr.</td>
        <td align="left" width="6%%">
          <input type="text" size="3" value="%(kleh)d" class="textboxmid" name="kkonf" onBlur="set_term_sum_fachstat('kkonf')">
        </td>
        <td align="left" height="40" class="legendtext" width="6%%">&nbsp;</td>
        <td align="left" height="40" class="legendtext" width="6%%">&nbsp; </td>
    </table>
              </fieldset> </td>
          </tr>"""

fsupd_notizsubmit_t = """
                  <tr>
            <td align="center" class="legendtext" valign="top"> <fieldset><legend class="legendtext">Notiz</legend>
              <table width="90%%" border="0" cellpadding="1">
                <tr>
                  <td align="center" height="40">
                    <input type="text" size="30" maxlength=255  value="%(no)s" class="textboxlarge" style="width:310">
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


thupdstausw_t = """
</head>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000">
<table width="735" align="center">
  <tr>
    <td height="200" align="center" valign="top">
      <form name="fachstatform" method="post" action="updfs">
        <table border="0" cellpadding="1" width="95%%">
          <tr>
            <td align="center" class="legendtext" valign="top"> <fieldset><legend class="legendtext">Fachstatistiken</legend>
              <table width="90%%" border="0" cellpadding="1">
                <tr height="40">
                  <td width="20%%" align="center" class="labeltext" >
                  <select size=10 class="listbox" name="fsid">"""

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
