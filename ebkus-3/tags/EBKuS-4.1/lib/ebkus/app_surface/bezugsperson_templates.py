# coding: latin-1
from akte_templates import klientendaten_t, anschrift_bezugsperson_t, empty

bzpers_neu_t1 = """
</HEAD>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000" onLoad="javascript:document.persform.vn.focus();">
<table width="735" align="center">
 <tr>
    <td height="465" align="center" valign="top">
      <form name="persform" method="post" action="klkarte">
        <table border="0" cellpadding="1" width="95%">
          <tr>
            <td width="45%" align="center" class="legendtext" valign="top" height="200">
""" + (klientendaten_t % empty(legend='Bezugspersonendaten', bezug_nominativ='die Bezugsperson', bezug_genitiv='der Bezugsperson')) + \
"""            </td>
            <td valign="top" align="center" class="legendtext" width="55%" height="200">
"""

# anschrift_bezugsperson_t wird im Programm gesetzt, da hier die Anschrift vom
# Klienten uebernommen wird.

bzpers_neu_t3 = """
                    </select>
                     </td>
                     </tr>
                     </table>
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
                    <input type="text" size="50" maxlength=255 name="no"  onMouseOver="window.status='Hier k&ouml;nnen Sie einen Notiztext zur Bezugsperson eingeben';return true;" onMouseOut="window.status='';return true;" title="Hier k&ouml;nnen Sie einen Notiztext zur Bezugsperson eingeben">
                    <input type="checkbox" value="%(nobed)s"  name="nobed"  onMouseOver="window.status='Hier k&ouml;nnen Sie markieren, ob es sich um eine wichtige Notiz handelt';return true;" onMouseOut="window.status='';return true;" title="Hier k&ouml;nnen Sie markieren, ob es sich um eine wichtige Notiz handelt">Wichtig
                    <input type="hidden" value="%(vrt)s" name="vrt">
                  </td>
                </tr>
              </table>
              </fieldset> </td>
          </tr>"""

bzpers_neu_t4a = """
          <tr>
            <td align="center" class="legendtext" valign="middle" colspan="2">
              <fieldset><legend>Verwandtschaftsart</legend>
              <table width="95%" border="0" cellpadding="1">
                <tr>
                  <td width="85%" align="center" height="35" valign="middle">
                   <select name="verw" class="listbox130"  onMouseOver="window.status='Bitte w&auml;hlen Sie die Verwandtschaftsart aus';return true;" onMouseOut="window.status='';return true;" title="Bitte w&auml;hlen Sie die Verwandtschaftsart aus">"""

bzpers_neu_t4b = """
                   </select>
                  </td>
                </tr>
              </table>
              </fieldset> </td>
          </tr>"""

bzpers_neu_t5 = """
          <tr>
            <td align="center" class="legendtext" valign="middle" colspan="2">
              <fieldset>
              <table width="95%%" border="0" cellpadding="1">
                <tr height="40">
                  <td width="33%%" align="center" valign="middle">
                    <input type="submit" name="" value="Speichern" class="button" onMouseOver="window.status='Anlegen der Bezugsperson mit den angegebenen Daten';return true;" onMouseOut="window.status='';return true;" title="Anlegen der Bezugsperson mit den angegebenen Daten">
                  </td>
                  <td align="center" valign="middle" width="33%%">
                    <input type="reset" value="Zur&uuml;cksetzen" class="button" onMouseOver="window.status='Das Formular zur&uuml;cksetzen';return true;" onMouseOut="window.status='';return true;" title="Das Formular zur&uuml;cksetzen">
                  </td>
                  <td align="center" valign="middle" width="34%%">
                    <input type="button" value="Abbrechen" class="button" onClick="javascript:history.back()" onMouseOver="window.status='Zur&uuml;ck zum vorhergehenden Formular';return true;" onMouseOut="window.status='';return true;" title="Zur&uuml;ck zum vorhergehenden Formular">
                  </td>
                </tr>
              </table>
              </fieldset> </td>
          </tr>
        </table>
        """

bzpers_neu_t6 = """
      <input type="hidden" value="%(akte_id)d" name="akid">
      <input type="hidden" value="%(id)d" name="fallid">
      </form>
    </td>
  </tr>
</table>
</body>
</html>
"""

bezugsperson_kopf = """
     <tr>
     <td align="center" valign="top" colspan="2"  class="legendtext">
     <fieldset><legend class="legendtext">Bezugspersonenliste</legend>
     <table border="0" cellspacing="1" width="95%%">
     <tr>
     <td class="labeltext" align="left" width="5%%">&nbsp;</td>
      <td align="left" class="labeltext" height="20" width="15%%">Art:</td>
      <td align="left" class="labeltext" height="20" width="20%%">Vorname:</td>
      <td align="left" class="labeltext" height="20" width="25%%">Nachname:</td>
      <td align="left" class="labeltext" height="20" width="15%%">Telefon 1:</td>
      <td align="left" class="labeltext" height="20" width="15%%">Telefon 2:</td>
     </tr>"""

bezugsperson_t =  """
<tr>
  <td class="normaltext" align="left">
  <a href="#" onClick="view_details('viewpers?akid=%(akte_id)d&bpid=%(id)d')">
  <img border="0" src="/ebkus/ebkus_icons/view_details.gif">
  </a>
  </td>
  <td align="left" class="normaltext" bgcolor="#FFFFFF">&#160; %(verw__name)s </td>
  <td align="left" class="normaltext" bgcolor="#FFFFFF">&#160; %(vn)s</td>
  <td align="left" class="normaltext" bgcolor="#FFFFFF">&#160; %(na)s </td>
  <td align="left" class="normaltext" bgcolor="#FFFFFF">&#160; %(tl1)s </td>
  <td align="left" class="normaltext" bgcolor="#FFFFFF">&#160; %(tl2)s </td>
</tr>
"""

bezugsperson_ende = """
<tr height="10">
<td colspan="6">
&nbsp;
</td>
</tr>
</tr>
</table>
</fieldset>
</td>
</tr>"""

bzpers_edit_t1 = """
</HEAD>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000" onLoad="javascript:document.persform.vn.focus();">
<table width="735" align="center">
 <tr>
    <td height="465" align="center" valign="top">
      <form name="persform" method="post" action="klkarte">
        <table border="0" cellpadding="1" width="95%%">
          <tr>
            <td width="45%%" align="center" class="legendtext" valign="top" height="200">
""" + klientendaten_t + \
"""            </td>
            <td valign="top" align="center" class="legendtext" width="55%%" height="200">
""" + anschrift_bezugsperson_t

bzpers_edit_t3 = """
                    </select>
                     </td>
                     </tr>
                     </table>
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
                    <input type="text" size="50" maxlength=255 name="no" value="%(no)s" onMouseOver="window.status='Hier k&ouml;nnen Sie einen Notiztext zur Bezugsperson eingeben';return true;" onMouseOut="window.status='';return true;" title="Hier k&ouml;nnen Sie einen Notiztext zur Bezugsperson eingeben">
                    <input type="checkbox" value="%(nobed)s" %(check)s name="nobed" onMouseOver="window.status='Hier k&ouml;nnen Sie markieren, ob es sich um eine wichtige Notiz handelt';return true;" onMouseOut="window.status='';return true;" title="Hier k&ouml;nnen Sie markieren, ob es sich um eine wichtige Notiz handelt">Wichtig
                    <input type="hidden" value="%(vrt)s" name="vrt">
                  </td>
                </tr>
              </table>
              </fieldset> </td>
          </tr>"""

bzpers_edit_t4a = """
          <tr>
            <td align="center" class="legendtext" valign="middle" colspan="2">
              <fieldset><legend>Verwandtschaftsart</legend>
              <table width="95%" border="0" cellpadding="1">
                <tr>
                  <td width="85%" align="center" height="35" valign="middle">
                   <select name="verw" class="listbox130" onMouseOver="window.status='Bitte w&auml;hlen Sie die Verwandtschaftsart aus';return true;" onMouseOut="window.status='';return true;" title="Bitte w&auml;hlen Sie die Verwandtschaftsart aus">"""

bzpers_edit_t4b = """
                   </select>
                  </td>
                </tr>
              </table>
              </fieldset> </td>
          </tr>"""

bzpers_edit_t5 = """
          <tr>
            <td align="center" class="legendtext" valign="middle" colspan="2">
              <fieldset>
              <table width="95%%" border="0" cellpadding="1">
                <tr height="40">
                  <td width="33%%" align="center" valign="middle">
                    <input type="submit" name="" value="Speichern" class="button" onMouseOver="window.status='Anlegen der Bezugsperson mit den angegebenen Daten';return true;" onMouseOut="window.status='';return true;" title="Anlegen der Bezugsperson mit den angegebenen Daten">
                  </td>
                  <td align="center" valign="middle" width="33%%">
                    <input type="reset" value="Zur&uuml;cksetzen" class="button" onMouseOver="window.status='Das Formular zur&uuml;cksetzen';return true;" onMouseOut="window.status='';return true;" title="Das Formular zur&uuml;cksetzen">
                  </td>
                  <td align="center" valign="middle" width="34%%">
                    <input type="button" value="Abbrechen" class="button" onClick="javascript:history.back()" onMouseOver="window.status='Zur&uuml;ck zum vorhergehenden Formular';return true;" onMouseOut="window.status='';return true;" title="Zur&uuml;ck zum vorhergehenden Formular">
                  </td>
                </tr>
              </table>
              </fieldset> </td>
          </tr>
        </table>
        """

bzpers_edit_t6 = """
      <input type="hidden" value="%(id)d" name="bpid">"""

bzpers_edit_t6b = """
      <input type="hidden" value="%(akte_id)d" name="akid">
      <input type="hidden" value="%(id)d" name="fallid">
      </form>
    </td>
  </tr>
</table>
</body>
</html>
"""
