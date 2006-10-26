# coding: latin-1

body_start = """
</HEAD>
<BODY bgcolor=#CCCCCC link="#CCCCCC" vlink="#CCCCCC" alink="#000000">
<form>
"""

body_start_meldung = """
</HEAD>
<BODY bgcolor=#CCCCCC link="#CCCCCC" vlink="#CCCCCC" alink="#000000" onLoad="strassen_meldung(\'%s\')">
<form>
"""

menue_t = """
<table width="735" align="center">
<tr>
<td width="95%">
<fieldset>
<table width="95%" height="40" align="center"">
<tr>
<td align"center" valign="center" width="25%">
<input type="button" name="Schaltfl&auml;che"
            onClick="go_to_url('menu')" value="Hauptmen&uuml;" class="button" onMouseOver="window.status='Bitte dr&uuml;cken Sie diese Schaltfl&auml;che um zum Hauptmen&uuml; zu gelangen';return true;" onMouseOut="window.status='';return true;" title="Bitte dr&uuml;cken Sie diese Schaltfl&auml;che um zum Hauptmen&uuml; zu gelangen">
</td>
<td align"center" valign="center" width="25%">
<input type="button" name="Schaltfl&auml;che"
            onClick="go_to_url('menugruppe')" value="Gruppenmen&uuml;" class="button" onMouseOver="window.status='Bitte dr&uuml;cken Sie diese Schaltfl&auml;che um zum Gruppenmen&uuml; zu gelangen';return true;" onMouseOut="window.status='';return true;" title="Bitte dr&uuml;cken Sie diese Schaltfl&auml;che um zum Gruppenmen&uuml; zu gelangen">
</td>
<td align="center" valign="center" width="25%">
<select size=1 name="Auswahl" onChange="go_to_url(this.form.Auswahl.options[this.form.Auswahl.options.selectedIndex].value)" class="listbox130">
"""

menue1_t = """
                      <option value="nothing">[ Neu ]
                      <option value="akteneu?file=akteneu">- Neuaufnahme
                      <option value="persneu?akid=%(akte_id)d&fallid=%(id)d">- Familie
                      <option value="einrneu?akid=%(akte_id)d&fallid=%(id)d">- Einrichtung"""

menue2_t = """
<option value="anmneu?akid=%(id)d&fallid=%(aktueller_fall__id)d">- Anmeldung"""

menue3_t = """
<option value="leistneu?akid=%(akte_id)d&fallid=%(id)d">- Leistung
<option value="zustneu?akid=%(akte_id)d&fallid=%(id)d">- Bearbeiter
<option value="vermneu?akid=%(akte_id)d&fallid=%(id)d">- Vermerk
<option value="upload?akid=%(akte_id)d&fallid=%(id)d">- Dateiimport
<option value="fsneu?akid=%(akte_id)d&fallid=%(id)d">- Fachstatistik
<option value="jghneu?akid=%(akte_id)d&fallid=%(id)d">- Bundesstatistik
<option value="zda?akid=%(akte_id)d&fallid=%(id)d">- zu den Akten
</select>
</td>
<td align="center" valign="center" width="25%%">
<select size=1 name="Auswahl2" onChange="go_to_url(this.form.Auswahl2.options[this.form.Auswahl2.options.selectedIndex].value)" class="listbox130">
        <option value="nothing">[ Anzeige ]
        <option value="newXX vorblatt?akid=%(akte_id)d&fallid=%(id)d">- Vorblatt
        <option value="dokkarte?akid=%(akte_id)d&fallid=%(id)d">- Akte
        <option value="formabfr3">- Suche
        <option value="wordexport?akid=%(akte_id)d">- Word-Export
</select>
</td>
</tr>
</table>
</fieldset>
</td>
</tr>
</table>
"""

menuezdar_t1 = """
<option value="nothing">[ Neu ]
<option value="akteneu?file=akteneu">- Neuaufnahme
<option value="zdar?akid=%(akte_id)d&fallid=%(id)d">- zdA R&uuml;ckg&auml;ngig
</select>
</td>
<td align="center" valign="center" width="25%%">
<select size=1 name="Auswahl2" onChange="go_to_url(this.form.Auswahl2.options[this.form.Auswahl2.options.selectedIndex].value)" class="listbox130">
        <option value="nothing">[ Anzeige ]
        <option value="vorblatt?akid=%(akte_id)d&fallid=%(id)d">- Vorblatt
        <option value="dokkarte?akid=%(akte_id)d&fallid=%(id)d">- Akte
        <option value="formabfr3">- Suche
</select>
</td>
</tr>
</table>
</fieldset>
</td>
</tr>
</table>
"""

menuewaufn_t1 = """
<option value="nothing">[ Neu ]
<option value="akteneu?file=akteneu">- Neuaufnahme
<option value="waufnneu?akid=%(akte_id)d&fallid=%(id)d">- Wiederaufnahme
</select>
</td>
<td align="center" valign="center" width="25%%">
<select size=1 name="Auswahl2" onChange="go_to_url(this.form.Auswahl2.options[this.form.Auswahl2.options.selectedIndex].value)" class="listbox130">
        <option value="nothing">[ Anzeige ]
        <option value="vorblatt?akid=%(akte_id)d&fallid=%(id)d">- Vorblatt
        <option value="dokkarte?akid=%(akte_id)d&fallid=%(id)d">- Akte
        <option value="formabfr3">- Suche
</select>
</td>
</tr>
</table>
</fieldset>
</td>
</tr>
</table>
"""


klientenkarte_t="""
<table width="735" border="0" align="center" height="215">
  <tr>
    <td align="center" colspan="2" legend class="legendtext" height="170" valign="top"><fieldset><legend class="legendtext">Klientendaten</legend>
      <table border="0" height="135" width="95%%">
        <tr>
          <td align="right" class="labeltext">Vorname:</td>
          <td>
            <input type="text"  value="%(vn)s" size="14" name="textfield2" class="textbox" readonly>
          </td>
          <td class="labeltext" align="right">Strasse:</td>
          <td>
            <input type="text" value="%(str)s %(hsnr)s" size="14" name="textfield4" class="textbox" readonly>
          </td>
          <td class="labeltext" align="right">Wohnt bei:</td>
          <td>
            <input type="text" value="%(fs__name)s" size="14" name="textfield7" class="textbox" readonly>
          </td>
        </tr>
        <tr>
          <td align="right" class="labeltext">Nachname:</td>
          <td>
            <input type="text" value="%(na)s" size="14" name="textfield3" class="textbox" readonly>
          </td>
          <td class="labeltext" align="right">Postleitzahl:</td>
          <td>
            <input type="text" value="%(plz)s" size="14" name="textfield5" class="textbox" readonly>
          </td>
          <td class="labeltext" align="right">Telefon 1:</td>
          <td>
            <input type="text" value="%(tl1)s" size="14" name="textfield9" class="textbox" readonly>
          </td>
        </tr>
        <tr>
          <td align="right" class="labeltext">Geburtstag:</td>
          <td>
            <input type="text" value="%(gb)s " size="14"name="textfield8" class="textbox" readonly>
          </td>
          <td class="labeltext" align="right">Ort:</td>
          <td>
            <input type="text" value="%(ort)s" size="14" name="textfield6" class="textbox" readonly>
          </td>
          <td class="labeltext" align="right">Telefon 2:</td>
          <td>
            <input type="text" value="%(tl2)s" size="14" name="textfield10" class="textbox" readonly>
          </td>
        </tr>
        <tr valign="top">
          <td align="right" class="labeltext" height="2">Ausbildung:</td>
          <td height="2">
            <input type="text" value="%(ber)s" size="14" name="textfield11" class="textbox" readonly>
          </td>
          <td height="2" colspan="4">&nbsp;</td>
"""
klientenkarte_t2 = """
            <tr>
            <td align="center" colspan="6"><input type="button" name="Schaltfl&auml;che"
            onClick="go_to_url('updakte?akid=%(id)s')" value="Bearbeiten" class="button" onMouseOver="window.status='Bitte dr&uuml;cken Sie diese Schaltfl&auml;che um die Klientenstammdaten zu Bearbeiten';return true;" onMouseOut="window.status='';return true;" title="Bitte dr&uuml;cken Sie diese Schaltfl&auml;che um die Klientenstammdaten zu Bearbeiten"></td>
            <tr>
          </tr>
      </table>
      </fieldset>
      </tr>"""

klientenkarte_t2_keinaktfall = """
            <tr>
            <td align="center" colspan="6">&nbsp;</td>
            <tr>
          </tr>
      </table>
      </fieldset>
      </tr>"""


detail_view_bezugsperson_t="""
</head>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000">
<form>
<table width="735" border="0" align="center" height="215">
  <tr>
    <td align="center" colspan="2" height="170" valign="top" class="legendtext"><fieldset><legend class="legendtext">Bezugsperson %(verw__name)s</legend>
      <table border="0" height="135" width="95%%">
        <tr>
          <td align="right" class="labeltext">Vorname:</td>
          <td>
            <input type="text"  value="%(vn)s" name="textfield2" class="textbox" size="14" readonly>
          </td>
          <td class="labeltext" align="right">Strasse:</td>
          <td>
            <input type="text" value="%(str)s %(hsnr)s" name="textfield4" class="textbox" size="14" readonly>
          </td>
          <td class="labeltext" align="right">Wohnt bei:</td>
          <td>
            <input type="text" value="%(fs__name)s" name="textfield7" class="textbox" size="14" readonly>
          </td>
        </tr>
        <tr>
          <td align="right" class="labeltext">Nachname:</td>
          <td>
            <input type="text" value="%(na)s" name="textfield3" class="textbox" size="14" readonly>
          </td>
          <td class="labeltext" align="right">Plz.:</td>
          <td>
            <input type="text" value="%(plz)s" name="textfield5" class="textbox" size="14" readonly>
          </td>
          <td class="labeltext" align="right">Telefon 1:</td>
          <td>
            <input type="text" value="%(tl1)s" name="textfield9" class="textbox" size="14" readonly>
          </td>
        </tr>
        <tr>
          <td align="right" class="labeltext">Geburtstag:</td>
          <td>
            <input type="text" value="%(gb)s " name="textfield8" class="textbox" size="14" readonly>
          </td>
          <td class="labeltext" align="right">Ort.:</td>
          <td>
            <input type="text" value="%(ort)s" name="textfield6" class="textbox" size="14" readonly>
          </td>
          <td class="labeltext" align="right">Telefon 2:</td>
          <td>
            <input type="text" value="%(tl2)s" name="textfield10" class="textbox" size="14" readonly>
          </td>
        </tr>
        <tr valign="top">
          <td align="right" class="labeltext" height="2">Ausbildung:</td>
          <td height="2">
            <input type="text" value="%(ber)s" name="textfield11" class="textbox" size="14" readonly>
          </td>
          <td height="2" colspan="4">&nbsp;</td>
            <tr>
            <td align="center" colspan="6"><input type="button" name="Schaltfl&auml;che"
            onClick="javascript:window.close()" value="Schliessen" class="button"></td>
            <tr>
          </tr>
      </table>
      </fieldset>
      </tr>
      </td>
      </tr>
      </table>
      </form>
      </body>
      </html>
"""

bezugsperson_kopf = """
     <tr>
     <td align="center" valign="top" colspan="2" legend class="legendtext">
     <fieldset><legend class="legendtext">Bezugspersonen</legend>
     <table border="0" cellspacing="1" width="95%">
     <tr>
     <td class="labeltext" align="left" width="5%">&nbsp;</td>
     <td class="labeltext" align="left" width="5%">&nbsp;</td>
      <td align="left" class="labeltext" height="20" width="15%">Art:</td>
      <td align="left" class="labeltext" height="20" width="20%">Vorname:</td>
      <td align="left" class="labeltext" height="20" width="25%">Nachname:</td>
      <td align="left" class="labeltext" height="20" width="15%">Telefon 1:</td>
      <td align="left" class="labeltext" height="20" width="15%">Telefon 2:</td>
     </tr>"""

keine_bezugsperson_kopf = """
     <tr>
     <td align="center" valign="top" colspan="2" legend class="legendtext">
     <fieldset><legend class="legendtext">Bezugspersonen</legend>
     <table border="0"  width="95%">
     <tr>
     </tr>"""


bezugsperson_t =  """
<tr>
  <td class="normaltext" align="left">
  <a href="updpers?akid=%(akte_id)d&bpid=%(id)d"><img border="0" src="/ebkus/ebkus_icons/edit_button.gif"></a></td>
  <td class="normaltext" align="left"><a href="#" onClick="view_details('viewpers?akid=%(akte_id)d&bpid=%(id)d')">
  <img border="0" src="/ebkus/ebkus_icons/view_details.gif" onMouseOver="window.status='Bitte dr&uuml;cken Sie diese Schaltfl&auml;che um sich die Daten der Bezugsperson anzusehen';return true;" onMouseOut="window.status='';return true;" title="Bitte dr&uuml;cken Sie diese Schaltfl&auml;che um sich die Daten der Bezugsperson anzusehen"></a></td>
  <td align="left" class="normaltext" bgcolor="#FFFFFF">&#160; %(verw__name)s </td>
  <td align="left" class="normaltext" bgcolor="#FFFFFF">&#160; %(vn)s</td>
  <td align="left" class="normaltext" bgcolor="#FFFFFF">&#160; %(na)s </td>
  <td align="left" class="normaltext" bgcolor="#FFFFFF">&#160; %(tl1)s </td>
  <td align="left" class="normaltext" bgcolor="#FFFFFF">&#160; %(tl2)s </td>
</tr>
"""

bezugsperson_t_keinaktfall =  """
<tr>
  <td class="normaltext" align="left"><img border="0" src="/ebkus/ebkus_icons/edit_button_inaktiv_locked.gif" onMouseOver="window.status='Funktion gesperrt';return true;" onMouseOut="window.status='';return true;" title="Funktion gesperrt"></td>
  <td class="normaltext" align="left"><img border="0" src="/ebkus/ebkus_icons/view_details_inaktiv.gif" onMouseOver="window.status='Funktion gesperrt';return true;" onMouseOut="window.status='';return true;" title="Funktion gesperrt."></td>
  <td align="left" class="normaltext" bgcolor="#FFFFFF">&#160; %(verw__name)s </td>
  <td align="left" class="normaltext" bgcolor="#FFFFFF">&#160; %(vn)s</td>
  <td align="left" class="normaltext" bgcolor="#FFFFFF">&#160; %(na)s </td>
  <td align="left" class="normaltext" bgcolor="#FFFFFF">&#160; %(tl1)s </td>
  <td align="left" class="normaltext" bgcolor="#FFFFFF">&#160; %(tl2)s </td>
</tr>
"""


bezugsperson_ende = """
<tr>
<td colspan="7" class="normaltext" height="13" align="center">
<input type="button" name="Schaltfl&auml;che2"
   onClick="go_to_url('persneu?akid=%(id)d&fallid=%(aktueller_fall__id)d&klerv=1')" value="Hinzuf&uuml;gen" class="button" onMouseOver="window.status='Bitte dr&uuml;cken Sie diese Schaltfl&auml;che um eine neue Bezugsperson hinzuzuf&uuml;gen.';return true;" onMouseOut="window.status='';return true;" title="Bitte dr&uuml;cken Sie diese Schaltfl&auml;che um eine neue Bezugsperson hinzuzuf&uuml;gen.">
</td>
</tr>
</table>
</fieldset>
"""

bezugsperson_ende_keinaktfall = """
<tr>
<td colspan="7" class="normaltext" height="13" align="center">&nbsp;</td>
</tr>
</table>
</fieldset>
"""


keine_bezugsperson_ende = """
<tr>
<td colspan="7" class="normaltext" height="13" align="center">
<input type="button" name="Schaltfl&auml;che2"
   onClick="go_to_url('persneu?akid=%(id)d&fallid=%(aktueller_fall__id)d&klerv=1')" value="Hinzuf&uuml;gen" class="button" onMouseOver="window.status='Bitte dr&uuml;cken Sie diese Schaltfl&auml;che um eine neue Bezugsperson hinzuzuf&uuml;gen.';return true;" onMouseOut="window.status='';return true;" title="Bitte dr&uuml;cken Sie diese Schaltfl&auml;che um eine neue Bezugsperson hinzuzuf&uuml;gen.">
</td>
</tr>
</table>
</fieldset>
"""


leistung_kopf = """
     <tr>
     <td align="center" valign="top" colspan="2" legend class="legendtext">
     <fieldset><legend class="legendtext">Leistungen</legend>
     <table border="0" cellspacing="1" width="95%">
     <tr>
      <td align="left" class="labeltext" valign="middle" width="5%">&nbsp;</td>
      <td align="left" class="labeltext" height="20" width="30%">Mitarbeiter:</td>
      <td align="left" class="labeltext" height="20" width="45%">Leistung:</td>
      <td align="left" class="labeltext" height="20" width="10%">Am:</td>
      <td align="left" class="labeltext" height="20" width="10%">Bis:</td>
      </tr>"""

leistungs_t1 =  """
<tr>
<td align="left" class="labeltext" valign="middle">
<a href="updleist?fallid=%(fall_id)d&leistid=%(id)d"><img border="0" src="/ebkus/ebkus_icons/edit_button.gif" onMouseOver="window.status='Bitte dr&uuml;cken Sie diese Schaltfl&auml;che um die Leistung zu bearbeiten';return true;" onMouseOut="window.status='';return true;" title="Bitte dr&uuml;cken Sie diese Schaltfl&auml;che um die Leistung zu bearbeiten"></a>
</td>
<td align="left" class="labeltext" valign="middle" bgcolor="#FFFFFF">%(mit_id__na)s </td>
<td align="left" class="labeltext" valign="middle" bgcolor="#FFFFFF">%(le__name)s </td>
<td align="left" class="labeltext" valign="middle" bgcolor="#FFFFFF">%(bgd)d.%(bgm)d.%(bgy)d </td> """

leistungs_t1a =  """
<tr>
<td align="left" class="labeltext" valign="middle">
<img border="0" src="/ebkus/ebkus_icons/edit_button_locked.gif">
</td>
<td align="left" class="labeltext" valign="middle" bgcolor="#FFFFFF">%(mit_id__na)s </td>
<td align="left" class="labeltext" valign="middle" bgcolor="#FFFFFF">%(le__name)s </td>
<td align="left" class="labeltext" valign="middle" bgcolor="#FFFFFF">%(bgd)d.%(bgm)d.%(bgy)d </td> """


leistungs_t1a_keinaktfall =  """
<tr>
<td align="left" class="labeltext" valign="middle"><img border="0" src="/ebkus/ebkus_icons/edit_button_inaktiv_locked.gif" onMouseOver="window.status='Funktion gesperrt';return true;" onMouseOut="window.status='';return true;" title="Funktion gesperrt"></td>
<td align="left" class="labeltext" valign="middle" bgcolor="#FFFFFF">%(mit_id__na)s </td>
<td align="left" class="labeltext" valign="middle" bgcolor="#FFFFFF">%(le__name)s </td>
<td align="left" class="labeltext" valign="middle" bgcolor="#FFFFFF">%(bgd)d.%(bgm)d.%(bgy)d </td> """

leistungsendeleer_t1 = """
<td align="left" bgcolor="#FFFFFF">...</td>
</tr>
"""

leistungsendedatum_t1 = """
<td align="left" class="normaltext" bgcolor="#FFFFFF">%(ed)d.%(em)d.%(ey)d </td>"""

leistung_ende = """
<tr>
<td colspan="5" class="normaltext" height="13" align="center">
<input type="button" name="Schaltfl&auml;che2"
   onClick="go_to_url('leistneu?akid=%(id)d&fallid=%(aktueller_fall__id)d')" value="Hinzuf&uuml;gen" class="button" onMouseOver="window.status='Bitte dr&uuml;cken Sie diese Schaltfl&auml;che um eine neue Leistung hinzuzuf&uuml;gen';return true;" onMouseOut="window.status='';return true;" title="Bitte dr&uuml;cken Sie diese Schaltfl&auml;che um eine neue Leistung hinzuzuf&uuml;gen">
</td>
</tr>
</table>
</fieldset>
</td>
</tr>
"""

leistung_ende_keinaktfall = """
<tr>
<td colspan="5" class="normaltext" height="13" align="center">&nbsp;</td>
</tr>
</table>
</fieldset>
</td>
</tr>
"""


fall_kopf = """
<td align="center" valign="top" legend class="legendtext">
     <fieldset><legend class="legendtext">Stand</legend>
     <table border=0 cellspacing=1 width="90%">
      <td align="left" class="labeltext" width="10%">&nbsp;</td>
      <td align="left" class="labeltext" width="40%">Fallnummer:</td>
      <td align="left" class="labeltext" width="25%">Beginn:</td>
      <td align="left" class="labeltext" width="25%">z.d.A.: </td>"""


fall_t1 = """
<tr>
<td align="left" class="normaltext">
<a href="updfall?akid=%(akte_id)d&fallid=%(id)d">
<img border="0" src="/ebkus/ebkus_icons/edit_button.gif" onMouseOver="window.status='Bearbeiten des Fallstatus';return true;" onMouseOut="window.status='';return true;" title="Bearbeiten des Fallstatus"></a>
</td>
<td align="left" class="normaltext" bgcolor="#FFFFFF"> %(fn)s </td>
<td align="left" class="normaltext" bgcolor="#FFFFFF"> %(bgd)d.%(bgm)d.%(bgy)d </td> """

fall_t1a = """
<tr>
<td align="left" class="normaltext">
<img border="0" src="/ebkus/ebkus_icons/edit_button_locked.gif">
</td>
<td align="left" class="normaltext" bgcolor="#FFFFFF"> %(fn)s </td>
<td align="left" class="normaltext" bgcolor="#FFFFFF"> %(bgd)d.%(bgm)d.%(bgy)d </td> """


fall_t1_keinaktfall = """
<tr>
<td align="left" class="normaltext"><img border="0" src="/ebkus/ebkus_icons/edit_button_inaktiv.gif" onMouseOver="window.status='Funktion gesperrt.';return true;" onMouseOut="window.status='';return true;" title="Funktion gesperrt"></td>
<td align="left" class="normaltext" bgcolor="#FFFFFF"> %(fn)s </td>
<td align="left" class="normaltext" bgcolor="#FFFFFF"> %(bgd)d.%(bgm)d.%(bgy)d </td> """

fall_t1a_keinaktfall = """
<tr>
<td align="left" class="normaltext"><img border="0" src="/ebkus/ebkus_icons/edit_button_inaktiv_locked.gif" onMouseOver="window.status='Funktion gesperrt';return true;" onMouseOut="window.status='';return true;" title="Funktion gesperrt"></td>
<td align="left" class="normaltext" bgcolor="#FFFFFF"> %(fn)s </td>
<td align="left" class="normaltext" bgcolor="#FFFFFF"> %(bgd)d.%(bgm)d.%(bgy)d </td> """


falloffen_t1 = """
<td align="left" class="legendtext" bgcolor="#FFFFFF"> offen </td>
</tr> """

fallendedatum_t1 = """
<td align="left" class="normaltext" bgcolor="#FFFFFF"> %(zdad)d.%(zdam)d.%(zday)d </td>
</tr>
"""

######################################
##aktueller fall !!! muss noch geklärt werden wegen wiederaufnahme
##
fallende_t_aktfall="""
<tr>
<td align="center" class="normaltext" colspan="4" height="13">
<input type="button" name="Schaltfl&auml;che2"
   onClick="go_to_url('zda?akid=%(id)s&fallid=%(aktueller_fall__id)d')" value="Zu den Akten" class="button" onMouseOver="window.status='Bitte dr&uuml;cken Sie diese Schaltfl&auml;che um den Fall zu den Akten zu legen';return true;" onMouseOut="window.status='';return true;" title="Bitte dr&uuml;cken Sie diese Schaltfl&auml;che um den Fall zu den Akten zu legen">
</td>
</tr>
</table>
</fieldset>
</td>
"""

fallende_t_waufn="""
<tr>
<td align="center" class="normaltext" colspan="4" height="13">
<input type="button" name="Schaltfl&auml;che2"
   onClick="go_to_url('waufnneu?akid=%(id)d&fallid=%(letzter_fall__id)d')" value="Wiederaufnahme" class="button" onMouseOver="window.status='Bitte dr&uuml;cken Sie diese Schaltfl&auml;che um den Fall wiederaufzunehmen';return true;" onMouseOut="window.status='';return true;" title="Bitte dr&uuml;cken Sie diese Schaltfl&auml;che um den Fall wiederaufzunehmen">
</td>
</tr>
</table>
</fieldset>
</td>
"""

fallende_t_zdarueck="""
<tr>
<td align="center" class="normaltext" colspan="4" height="13">
<input type="button" name="Schaltfl&auml;che2"
   onClick="go_to_url('zdar?akid=%(id)d&fallid=%(letzter_fall__id)d')" value="ZdA r&uuml;ckg&auml;ngig" class="button" onMouseOver="window.status='Bitte dr&uuml;cken Sie diese Schaltfl&auml;che um den Fall wieder zu aktivieren';return true;" onMouseOut="window.status='';return true;" title="Bitte dr&uuml;cken Sie diese Schaltfl&auml;che um den Fall wieder zu aktivieren">
</td>
</tr>
</table>
</fieldset>
</td>
"""


bearbeiter_kopf_t1 = """
<td align="center" valign="top" legend class="legendtext">
<fieldset><legend class="legendtext">Bearbeiter</legend>
<table border=0 cellspacing=1 width="90%">
<tr>
<td class="labeltext" align="left" width="10%">&nbsp;</td>
<td class="labeltext" align="left" width="50%">Bearbeiter:</td>
<td class="labeltext" align="left" width="20%">Beginn: </td>
<td class="labeltext" align="left" width="20%">Ende:</td>
"""

bearbeiter_t1 = """
</tr>
<tr>
<td class="normaltext" align="left">
<a href="updzust?fallid=%(fall_id)d&zustid=%(id)d">
<img border="0" src="/ebkus/ebkus_icons/edit_button.gif" onMouseOver="window.status='Bearbeiten der Zust&auml;ndigkeit';return true;" onMouseOut="window.status='';return true;" title="Bearbeiten der Zust&auml;ndigkeit"></a></td>
<td class="normaltext" align="left" bgcolor="#FFFFFF"> %(mit_id__na)s </td>
<td class="normaltext" align="left" bgcolor="#FFFFFF"> %(bgd)d.%(bgm)d.%(bgy)d </td> """

bearbeiter_t1a = """
</tr>
<tr>
<td class="normaltext" align="left">
<img border="0" src="/ebkus/ebkus_icons/edit_button_locked.gif" onMouseOver="window.status='Funktion gesperrt';return true;" onMouseOut="window.status='';return true;" title="Funktion gesperrt">
</td>
<td class="normaltext" align="left" bgcolor="#FFFFFF"> %(mit_id__na)s </td>
<td class="normaltext" align="left" bgcolor="#FFFFFF"> %(bgd)d.%(bgm)d.%(bgy)d </td> """

bearbeiter_t1_keinaktfall = """
</tr>
<tr>
<td class="normaltext" align="left"><img border="0" src="/ebkus/ebkus_icons/edit_button_inaktiv.gif" onMouseOver="window.status='Funktion gesperrt';return true;" onMouseOut="window.status='';return true;" title="Funktion gesperrt"></td>
<td class="normaltext" align="left" bgcolor="#FFFFFF"> %(mit_id__na)s </td>
<td class="normaltext" align="left" bgcolor="#FFFFFF"> %(bgd)d.%(bgm)d.%(bgy)d </td> """

bearbeiter_t1a_keinaktfall = """
</tr>
<tr>
<td class="normaltext" align="left"><img border="0" src="/ebkus/ebkus_icons/edit_button_inaktiv_locked.gif" onMouseOver="window.status='';return true;" onMouseOut="window.status='Funktion gesperrt';return true;" title="Funktion gesperrt"></td>
<td class="normaltext" align="left" bgcolor="#FFFFFF"> %(mit_id__na)s </td>
<td class="normaltext" align="left" bgcolor="#FFFFFF"> %(bgd)d.%(bgm)d.%(bgy)d </td> """


bearbeiterendeoffen_t1 = """
<td class="legendtext" align="left" bgcolor="#FFFFFF"> offen </td>
</tr> """

bearbeiterendedatum_t1 = """
<td class="normaltext" align="left" bgcolor="#FFFFFF"> %(ed)d.%(em)d.%(ey)d </td>
"""

bearbeiter_ende_t1="""
<tr>
<td align="center" class="normaltext" colspan="4" height="13">
  <input type="button" name="Schaltfl&auml;che2"
   onClick="go_to_url('zustneu?akid=%(id)s&fallid=%(aktueller_fall__id)d')" value="Hinzuf&uuml;gen" class="button" onMouseOver="window.status='Bitte dr&uuml;cken Sie diese Schaltfl&auml;che um eine neue Zust&auml;ndigkeit einzutragen';return true;" onMouseOut="window.status='';return true;" title="Bitte dr&uuml;cken Sie diese Schaltfl&auml;che um eine neue Zust&auml;ndigkeit einzutragen">
</td>
<tr>
</table>
</fieldset>
</td>
</tr>
"""

bearbeiter_ende_keinaktfall="""
<tr>
<td align="center" class="normaltext" colspan="4" height="13">&nbsp;</td>
</tr>
</table>
</fieldset>
</td>
</tr>
"""


anmeldung_kopf = """
     <tr>
     <td align="center" valign="top" colspan="2" legend class="legendtext">
     <fieldset><legend class="legendtext">Anmeldungskontakte</legend>
     <table border="0" cellspacing="1" width="95%">
     <tr>
     <td class="labeltext" align="left" width="5%">&nbsp;</td>
     <td class="labeltext" align="left" width="5%">&nbsp;</td>
      <td align="left" class="labeltext" height="20" width="25%">Gemeldet von:</td>
      <td align="left" class="labeltext" height="20" width="20%">Gemeldet am:</td>
      <td align="left" class="labeltext" height="20" width="45%">Anmeldegrund:</td>
     </tr>"""

keine_anmeldung_kopf = """
     <tr>
     <td align="center" valign="top" colspan="2" legend class="legendtext">
     <fieldset><legend class="legendtext">Anmeldungskontakte</legend>
     <table border="0"  width="95%">
     <tr>
     </tr>"""


alt_anmeldung_t =  """
<tr>
  <td class="normaltext" align="left"><img border="0" src="/ebkus/ebkus_icons/edit_button_locked.gif" onMouseOver="window.status='Geh&ouml;hrt zu einem abgeschlossenem Fall.';return true;" onMouseOut="window.status='';return true;" title="Geh&ouml;hrt zu einem abgeschlossenem Fall."></td>
  <td class="normaltext" align="left">
  <a href="#" onClick="view_details('viewanm?fallid=%(fall_id)d&anmid=%(id)d')" >
  <img border="0" src="/ebkus/ebkus_icons/view_details.gif" onMouseOver="window.status='Bitte dr&uuml;cken Sie diese Schaltfl&auml;che um sich die Daten des Anmeldekontaktes anzusehen';return true;" onMouseOut="window.status='';return true;" title="Bitte dr&uuml;cken Sie diese Schaltfl&auml;che um sich die Daten des Anmeldekontaktes anzusehen"></a></td>
  <td align="left" class="normaltext" bgcolor="#FFFFFF">&#160; %(von)s </td>
  <td align="left" class="normaltext" bgcolor="#FFFFFF">&#160; %(ad)d.%(am)d.%(ay)d</td>
  <td align="left" class="normaltext" bgcolor="#FFFFFF">&#160; %(mg)s </td>
</tr>
"""

akt_anmeldung_t =  """
<tr>
  <td class="normaltext" align="left">
  <a href="updanm?fallid=%(fall_id)d&anmid=%(id)d">
  <img border="0" src="/ebkus/ebkus_icons/edit_button.gif" onMouseOver="window.status='Bearbeiten des Anmeldekontaktes.';return true;" onMouseOut="window.status='';return true;" title="Bearbeiten des Anmeldekontaktes"></a></td>
  <td class="normaltext" align="left">
  <a href="#" onClick="view_details('viewanm?fallid=%(fall_id)d&anmid=%(id)d')">
  <img border="0" src="/ebkus/ebkus_icons/view_details.gif" onMouseOver="window.status='Bitte dr&uuml;cken Sie diese Schaltfl&auml;che um sich die Daten des Anmeldekontaktes anzusehen';return true;" onMouseOut="window.status='';return true;" title="Bitte dr&uuml;cken Sie diese Schaltfl&auml;che um sich die Daten des Anmeldekontaktes anzusehen"></a></td>
  <td align="left" class="normaltext" bgcolor="#FFFFFF">&#160; %(von)s </td>
  <td align="left" class="normaltext" bgcolor="#FFFFFF">&#160; %(ad)d.%(am)d.%(ay)d</td>
  <td align="left" class="normaltext" bgcolor="#FFFFFF">&#160; %(mg)s </td>
</tr>
"""

anmeldung_t1_keinaktfall =  """
<tr>
  <td class="normaltext" align="left"><img border="0" src="/ebkus/ebkus_icons/edit_button_inaktiv_locked.gif" onMouseOver="window.status='Funktion gesperrt';return true;" onMouseOut="window.status='';return true;" title="Funktion gesperrt"></td>
  <td class="normaltext" align="left"><img border="0" src="/ebkus/ebkus_icons/view_details_inaktiv.gif" onMouseOver="window.status='Funktion gesperrt';return true;" onMouseOut="window.status='';return true;" title="Funktion gesperrt"></td>
  <td align="left" class="normaltext" bgcolor="#FFFFFF">&#160; %(von)s </td>
  <td align="left" class="normaltext" bgcolor="#FFFFFF">&#160; %(ad)d.%(am)d.%(ay)d</td>
  <td align="left" class="normaltext" bgcolor="#FFFFFF">&#160; %(mg)s </td>
</tr>
"""


anmeldung_ende_keineanm = """
<tr>
<td colspan="5" class="normaltext" height="13" align="center">
<input type="button" name="Schaltfl&auml;che2"
   onClick="go_to_url('anmneu?akid=%(id)d&fallid=%(aktueller_fall__id)d')" value="Hinzuf&uuml;gen" class="button" onMouseOver="window.status='Bitte dr&uuml;cken Sie diese Schaltfl&auml;che um einen neuen Anmeldekontakt hinzuzuf&uuml;gen';return true;" onMouseOut="window.status='';return true;" title="Bitte dr&uuml;cken Sie diese Schaltfl&auml;che um einen neuen Anmeldekontakt hinzuzuf&uuml;gen">
</td>
</tr>
</table>
</fieldset>
"""

anmeldung_ende_hatanm = """
<tr>
<td colspan="5" class="normaltext" height="13" align="center">&nbsp;</td>
</tr>
</table>
</fieldset>
"""


anmeldung_ende_keinaktfall = """
<tr>
<td colspan="5" class="normaltext" height="13" align="center">&nbsp;</td>
</tr>
</table>
</fieldset>
"""


keine_anmeldung_ende_keineanm = """
<tr>
<td colspan="5" class="normaltext" height="13" align="center">
<input type="button" name="Schaltfl&auml;che2"
   onClick="go_to_url('anmneu?akid=%(id)d&fallid=%(aktueller_fall__id)d')" value="Hinzuf&uuml;gen" class="button" onMouseOver="window.status='Bitte dr&uuml;cken Sie diese Schaltfl&auml;che um einen neuen Anmeldekontakt hinzuzuf&uuml;gen';return true;" onMouseOut="window.status='';return true;" title="Bitte dr&uuml;cken Sie diese Schaltfl&auml;che um einen neuen Anmeldekontakt hinzuzuf&uuml;gen">
</td>
</tr>
</table>
</fieldset>
"""

detail_view_anmeldung_t="""
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000">
<table width="735" border="0" align="center" height="215">
  <tr>
    <td align="center" colspan="2" height="170" valign="top" legend class="legendtext"><fieldset><legend class="legendtext">Anmeldekontakt</legend>
      <table border="0" height="135" width="95%%">
        <tr>
          <td align="right" class="labeltext">Gemeldet von:</td>
          <td>
            <input type="text"  value="%(von)s" name="textfield2" class="textbox" readonly>
          </td>
          <td class="labeltext" align="right">Anmeldegrund:</td>
          <td>
            <input type="text" value="%(mg)s" name="textfield4" class="textbox" readonly>
          </td>
        </tr>
        <tr>
        <td class="labeltext" align="right">Gemeldet am:</td>
          <td>
            <input type="text" value="%(ad)d.%(am)d.%(ay)d" name="textfield7" class="textbox" readonly>
          </td>
          <td class="labeltext" align="right">Empfehlung von:</td>
          <td>
            <input type="text" value="%(me)s" name="textfield9" class="textbox" readonly>
          </td>
        <tr>
          <td align="right" class="labeltext">Telefon:</td>
          <td>
            <input type="text" value="%(mtl)s" name="textfield3" class="textbox" readonly>
          </td>
          <td class="labeltext" align="right">Zugangsmodus:</td>
          <td>
            <input type="text" value="%(zm__name)s" name="textfield5" class="textbox" readonly>
          </td>
          <tr>
            <td align="center" colspan="4"><input type="button" name="Schaltfl&auml;che"
            onClick="javascript:window.close()" value="Schliessen" class="button"></td>
          </tr>
      </table>
      </fieldset>
      </td>
     </table>
      </body>
      </html>
"""


einrichtungskontakt_kopf = """
     <tr>
     <td align="center" valign="top" colspan="2" legend class="legendtext">
     <fieldset><legend class="legendtext">Einrichtungskontakte</legend>
     <table border="0"  width="95%">
     <tr>
     <td class="labeltext" align="left" width="5%">&nbsp;</td>
      <td align="left" class="labeltext" height="20" width="20%">Art:</td>
      <td align="left" class="labeltext" height="20" width="46%">Name:</td>
      <td align="left" class="labeltext" height="20" width="12%">Telefon 1:</td>
      <td align="left" class="labeltext" height="20" width="12%">Telefon 2:</td>
      <td align="left" class="labeltext" height="20" width="5%">Aktuell:</td>
     </tr>"""

kein_einrichtungskontakt_kopf = """
     <tr>
     <td align="center" valign="top" colspan="2" legend class="legendtext">
     <fieldset><legend class="legendtext">Einrichtungskontakte</legend>
     <table border="0" cellspacing="1" width="95%">
     <tr>
     </tr>"""


einrichtungskontakt_t =  """
<tr>
  <td class="normaltext" align="left">
  <a href="updeinr?akid=%(akte_id)d&einrid=%(id)d">
  <img border="0" src="/ebkus/ebkus_icons/edit_button.gif" onMouseOver="window.status='Bitte dr&uuml;cken Sie diese Schaltfl&auml;che um die Daten des Einrichtungskontaktes zu bearbeiten';return true;" onMouseOut="window.status='';return true;" title="Bitte dr&uuml;cken Sie diese Schaltfl&auml;che um die Daten des Einrichtungskontaktes zu bearbeiten"></a></td>
  <td align="left" class="normaltext" bgcolor="#FFFFFF">&#160; %(insta__name)s </td>
  <td align="left" class="normaltext" bgcolor="#FFFFFF">&#160; %(na)s</td>
  <td align="left" class="normaltext" bgcolor="#FFFFFF">&#160; %(tl1)s </td>
  <td align="left" class="normaltext" bgcolor="#FFFFFF">&#160; %(tl2)s </td>
  <td align="left" class="normaltext" bgcolor="#FFFFFF">&#160; %(status__code)s </td>
</tr>
"""

einrichtungskontakt_t_keinaktfall =  """
<tr>
  <td class="normaltext" align="left"><img border="0" src="/ebkus/ebkus_icons/edit_button_inaktiv_locked.gif" onMouseOver="window.status='Funktion gesperrt';return true;" onMouseOut="window.status='';return true;" title="Funktion gesperrt"></td>
  <td align="left" class="normaltext" bgcolor="#FFFFFF">&#160; %(insta__name)s </td>
  <td align="left" class="normaltext" bgcolor="#FFFFFF">&#160; %(na)s</td>
  <td align="left" class="normaltext" bgcolor="#FFFFFF">&#160; %(tl1)s </td>
  <td align="left" class="normaltext" bgcolor="#FFFFFF">&#160; %(tl2)s </td>
  <td align="left" class="normaltext" bgcolor="#FFFFFF">&#160; %(status__code)s </td>
</tr>
"""


einrichtungskontakt_ende = """
<tr>
<td colspan="6" class="normaltext" height="13" align="center">
<input type="button" name="Schaltfl&auml;che2"
   onClick="go_to_url('einrneu?akid=%(id)d&fallid=%(aktueller_fall__id)d')" value="Hinzuf&uuml;gen" class="button" onMouseOver="window.status='Bitte dr&uuml;cken Sie diese Schaltfl&auml;che um einen Einrichtungskontakt hinzuzuf&uuml;gen';return true;" onMouseOut="window.status='';return true;" title="Bitte dr&uuml;cken Sie diese Schaltfl&auml;che um einen Einrichtungskontakt hinzuzuf&uuml;gen">
</td>
</tr>
</table>
</fieldset>
"""

einrichtungskontakt_ende_keinaktfall = """
<tr>
<td colspan="6" class="normaltext" height="13" align="center">&nbsp;</td>
</tr>
</table>
</fieldset>
"""


kein_einrichtungskontakt_ende = """
<tr>
<td colspan="6" class="normaltext" height="13" align="center">
<input type="button" name="Schaltfl&auml;che2"
   onClick="go_to_url('einrneu?akid=%(id)d&fallid=%(aktueller_fall__id)d')" value="Hinzuf&uuml;gen" class="button" onMouseOver="window.status='Bitte dr&uuml;cken Sie diese Schaltfl&auml;che um einen Einrichtungskontakt hinzuzuf&uuml;gen';return true;" onMouseOut="window.status='';return true;" title="Bitte dr&uuml;cken Sie diese Schaltfl&auml;che um einen Einrichtungskontakt hinzuzuf&uuml;gen">
</td>
</tr>
</table>
</fieldset>
"""


fachstatistik_kopf_t = """
</td>
</tr>
<td align="center" valign="top" width="50%" legend class="legendtext">
<fieldset><legend class="legendtext">Fachstatistiken</legend>
<table border=0 cellspacing=1 width="90%">
<tr>
<td class="labeltext" align="left" width="10%">&nbsp;</td>
<td class="labeltext" align="left" width="90%">Jahr:</td>
</tr>
"""

fachstatistik_kopf_leer = """
</td>
</tr>
<td align="center" valign="top" width="50%" legend class="legendtext">
<fieldset><legend class="legendtext">Fachstatistiken</legend>
<table border=0 cellspacing=1 width="90%">
"""


fachstatistik_t1 = """
<tr>
<td class="normaltext" align="left">
<a href="updfs?fallid=%(fall_id)d&fsid=%(id)d">
<img border="0" src="/ebkus/ebkus_icons/edit_stat_button.gif" onMouseOver="window.status='Bearbeiten der Fachstatistik';return true;" onMouseOut="window.status='';return true;" title="Bearbeiten der Fachstatistik"></a></td>
<td class="normaltext" align="left" bgcolor="#FFFFFF"> %(jahr)s </td>
</tr>"""
fachstatistik_t1a = """
<tr>
<td class="normaltext" align="left">
<img border="0" src="/ebkus/ebkus_icons/edit_stat_button_locked.gif" onMouseOver="window.status='Funktion gesperrt';return true;" onMouseOut="window.status='';return true;" title="Funktion gesperrt"></td>
<td class="normaltext" align="left" bgcolor="#FFFFFF"> %(jahr)s </td>
</tr>"""

fachstatistik_t2 = """
<tr>
<td class="normaltext" align="left">
<img border="0" src="/ebkus/ebkus_icons/edit_stat_button_inaktiv_locked.gif" onMouseOver="window.status='Funktion gesperrt';return true;" onMouseOut="window.status='';return true;" title="Funktion gesperrt"></td>
<td class="normaltext" align="left" bgcolor="#FFFFFF"> %(jahr)s </td>
</tr>"""

fachstatistik_ende_leer = """
<tr>
<td align="center" bgcolor="#CCCCCC"><input type="button" name="Schaltfl&auml;che2"
   onClick="go_to_url('fsneu?akid=%(id)d&fallid=%(aktueller_fall__id)d')" value="Hinzuf&uuml;gen" class="button" onMouseOver="window.status='Bitte dr&uuml;cken Sie diese Schaltfl&auml;che um eine Fackstatistik hinzuzuf&uuml;gen';return true;" onMouseOut="window.status='';return true;" title="Bitte dr&uuml;cken Sie diese Schaltfl&auml;che um eine Fackstatistik hinzuzuf&uuml;gen">
</td>
</tr>
</table>
</fieldset>
</td>
"""


fachstatistik_ende = """
<tr>
<td colspan="2" align="center" bgcolor="#CCCCCC"><input type="button" name="Schaltfl&auml;che2"
   onClick="go_to_url('fsneu?akid=%(id)d&fallid=%(aktueller_fall__id)d')" value="Hinzuf&uuml;gen" class="button" onMouseOver="window.status='Bitte dr&uuml;cken Sie diese Schaltfl&auml;che um eine Fachstatistik hinzuzuf&uuml;gen';return true;" onMouseOut="window.status='';return true;" title="Bitte dr&uuml;cken Sie diese Schaltfl&auml;che um eine Fachstatistik hinzuzuf&uuml;gen">
</td>
</tr>
</table>
</fieldset>
</td>
"""

fachstatistik_kopf_t_keinaktfall = """
</td>
</tr>
<td align="center" valign="top" width="50%" legend class="legendtext">
<fieldset><legend class="legendtext">Fachstatistiken</legend>
<table border=0 cellspacing=1 width="90%">
<tr>
<td class="labeltext" align="left" width="10%">&nbsp;</td>
<td class="labeltext" align="left" width="90%">Jahr:</td>
</tr>
"""

fachstatistik_kopf_leer_keinaktfall = """
</td>
</tr>
<td align="center" valign="top" width="50%" legend class="legendtext">
<fieldset><legend class="legendtext">Fachstatistiken</legend>
<table border=0 cellspacing=1 width="90%">
"""


fachstatistik_keinaktfall = """
<tr>
<td class="normaltext" align="left">
<img border="0" src="/ebkus/ebkus_icons/edit_stat_button_inaktiv_locked.gif" onMouseOver="window.status='Funktion gesperrt';return true;" onMouseOut="window.status='';return true;" title="Funktion gesperrt"></td>
<td class="normaltext" align="left" bgcolor="#FFFFFF"> %(jahr)s </td>
</tr>"""

fachstatistik_ende_leer_keinaktfall = """
<tr>
<td class="legendtext" align="center" bgcolor="#CCCCCC">&nbsp;</td>
</tr>
</table>
</fieldset>
</td>
"""


fachstatistik_ende_keinaktfall = """
<tr>
<td colspan="2" class="legendtext" align="center" bgcolor="#CCCCCC">&nbsp;</td>
</tr>
</table>
</fieldset>
</td>
"""

jghstatistiken_kopf_t = """
<td align="center" valign="top" width="50%" legend class="legendtext">
<fieldset><legend class="legendtext">Jugendhilfestatistiken</legend>
<table border=0 cellspacing=1 width="90%">
<tr>
<td class="labeltext" align="left" width="10%">&nbsp;</td>
<td class="labeltext" align="left" width="90%">Jahr:</td>
</tr>
"""

jghstatistiken_kopf_leer = """
<td align="center" valign="top" width="50%" legend class="legendtext">
<fieldset><legend class="legendtext">Jugendhilfestatistiken</legend>
<table border=0 cellspacing=1 width="90%">
"""


jghstatistiken_t1 = """
<tr>
<td class="normaltext" align="left">
<a href="updjgh?akid=%(fall_id__akte_id)d&fallid=%(fall_id)d&jghid=%(id)d">
<img border="0" src="/ebkus/ebkus_icons/edit_stat_button.gif" onMouseOver="window.status='Bearbeiten der Bundesstatistik';return true;" onMouseOut="window.status='';return true;" title="Bearbeiten der Bundesstatistik"></a></td>
<td class="normaltext" align="left" bgcolor="#FFFFFF"> %(ey)s </td>
</tr>"""

jghstatistiken_t1a = """
<tr>
<td class="normaltext" align="left">
<img border="0" src="/ebkus/ebkus_icons/edit_stat_button_locked.gif" onMouseOver="window.status='Funktion gesperrt';return true;" onMouseOut="window.status='';return true;" title="Funktion gesperrt"></td>
<td class="normaltext" align="left" bgcolor="#FFFFFF"> %(ey)s </td>
</tr>"""

jghstatistiken_ende_leer = """
<tr>
<td align="center" bgcolor="#CCCCCC"><input type="button" name="Schaltfl&auml;che2"
   onClick="go_to_url('jghneu?akid=%(id)d&fallid=%(aktueller_fall__id)d')" value="Hinzuf&uuml;gen" class="button" onMouseOver="window.status='Bitte dr&uuml;cken Sie diese Schaltfl&auml;che um eine Bundesjugendhilfestatistik hinzuzuf&uuml;gen';return true;" onMouseOut="window.status='';return true;" title="Bitte dr&uuml;cken Sie diese Schaltfl&auml;che um eine Bundesjugendhilfestatistik hinzuzuf&uuml;gen">
</td>
</tr>
</table>
</fieldset>
</td>
"""


jghstatistiken_ende = """
<tr>
<td colspan="2" align="center" bgcolor="#CCCCCC"><input type="button" name="Schaltfl&auml;che2"
   onClick="go_to_url('jghneu?akid=%(id)d&fallid=%(aktueller_fall__id)d')" value="Hinzuf&uuml;gen" class="button" onMouseOver="window.status='Bitte dr&uuml;cken Sie diese Schaltfl&auml;che um eine Bundesjugendhilfestatistik hinzuzuf&uuml;gen';return true;" onMouseOut="window.status='';return true;" title="Bitte dr&uuml;cken Sie diese Schaltfl&auml;che um eine Bundesjugendhilfestatistik hinzuzuf&uuml;gen">
</td>
</tr>
</table>
</fieldset>
</td>
</tr>
"""

jghstatistiken_kopf_t_keinaktfall = """
<td align="center" valign="top" width="50%" legend class="legendtext">
<fieldset><legend class="legendtext">Jugendhilfestatistiken</legend>
<table border=0 cellspacing=1 width="90%">
<tr>
<td class="labeltext" align="left" width="10%">&nbsp;</td>
<td class="labeltext" align="left" width="90%">Jahr:</td>
</tr>
"""

jghstatistiken_kopf_leer_keinaktfall = """
<td align="center" valign="top" width="50%" legend class="legendtext">
<fieldset><legend class="legendtext">Jugendhilfestatistiken</legend>
<table border=0 cellspacing=1 width="90%">
"""


jghstatistiken_t1_keinaktfall = """
<tr>
<td class="normaltext" align="left"><img border="0" src="/ebkus/ebkus_icons/edit_stat_button_inaktiv_locked.gif" onMouseOver="window.status='Funktion gesperrt';return true;" onMouseOut="window.status='';return true;" title="Funktion gesperrt"></td>
<td class="normaltext" align="left" bgcolor="#FFFFFF"> %(ey)s </td>
</tr>"""

jghstatistiken_ende_leer_keinaktfall = """
<tr>
<td class="legendtext" align="center" bgcolor="#CCCCCC">&nbsp;</td>
</tr>
</table>
</fieldset>
</td>
"""


jghstatistiken_ende_keinaktfall = """
<tr>
<td colspan="2" class="legendtext" align="center" bgcolor="#CCCCCC">&nbsp;</td>
</tr>
</table>
</fieldset>
</td>
</tr>
"""


notiz_kopf = """
     <tr>
     <td align="center" valign="top" colspan="2" legend class="legendtext">
     <fieldset><legend class="legendtext">Notizen</legend>
     <table border="0"  width="95%">
     """
notiz_header = """
     <tr>
       <td align="left" colspan="4" class="legendtext" bgcolor="#CCCCCC">%s:</td>
     </tr>"""

notiz_akte_t =  """
<tr>
  <td align="left" class="normaltext" bgcolor="#FFFFFF" width="5%%">&#160;AK</td>
  <td align="left" class="normaltext" bgcolor="#FFFFFF" width="20%%">&#160;%(vn)s %(na)s </td>
  <td align="left" colspan="2" class="normaltext" bgcolor="#FFFFFF" width="75%%">&#160;%(no)s</td>
</tr>
"""


notiz_bzpers_t =  """
<tr>
  <td align="left" class="normaltext" bgcolor="#FFFFFF" width="5%%">&#160;BP</td>
  <td align="left" class="normaltext" bgcolor="#FFFFFF" width="20%%">&#160;%(vn)s %(na)s </td>
  <td align="left" class="normaltext" bgcolor="#FFFFFF" width="65%%">&#160;%(no)s</td>
  <td align="left" class="normaltext" bgcolor="#FFFFFF" width="10%%">&#160;%(nobed__name)s</td>
</tr>
"""

notiz_einrichtung_t =  """
<tr>
  <td align="left" class="normaltext" bgcolor="#FFFFFF" width="5%%">&#160;ER</td>
  <td align="left" class="normaltext" bgcolor="#FFFFFF" width="20%%">&#160;%(insta__name)s %(na)s </td>
  <td align="left" class="normaltext" bgcolor="#FFFFFF" width="65%%">&#160;%(no)s</td>
  <td align="left" class="normaltext" bgcolor="#FFFFFF" width="10%%">&#160;%(nobed__name)s</td>
</tr>
"""

notiz_anmeldung_t =  """
<tr>
  <td align="left" class="normaltext" bgcolor="#FFFFFF" width="5%%">&#160;AM</td>
  <td align="left" class="normaltext" bgcolor="#FFFFFF" width="20%%">&#160;%(von)s</td>
  <td align="left" colspan="2" class="normaltext" bgcolor="#FFFFFF" width="75%%">&#160;%(no)s</td>
</tr>
"""

notiz_ende = """
<tr>
  <td class="labeltext" colspan="4" width="100%">&nbsp;</td>
</tr>
</table>
</fieldset>
</td>
</tr>
"""


fall_gruppen_kopf = """
<tr>
<td align="center" valign="top" width="50%" legend class="legendtext">
<fieldset><legend class="legendtext">Gruppenkarten des Falls</legend>
<table border=0 cellspacing=1 width="90%">
  <tr>
  <td class="labeltext" align="left" width="15%">&nbsp;</td>
  <td class="labeltext" align="left" width="10%">Gruppenr.:</td>
  <td class="labeltext" align="left" width="75%">Name:</td>
  </tr>
"""

fall_gruppen_leer = """
<tr>
<td align="center" valign="top" width="50%">
&nbsp;
</td>
"""

fallgruppen_t1 = """
<tr>
<td class="normaltext" align="left">
<a href="gruppenkarte?gruppeid=%(gruppe_id)s">
<img border="0" src="/ebkus/ebkus_icons/edit_grp_button.gif"></a></td>
<td class="normaltext" align="left" bgcolor="#FFFFFF">%(gruppe_id__gn)s</td>
"""
fallgruppen_t2 = """
<td class="normaltext" align="left" bgcolor="#FFFFFF">%(akte_id__vn)s %(akte_id__na)s </td>
</tr>"""

fallgruppen_t1_keinaktfall = """
<tr>
<td class="normaltext" align="left"><img border="0" src="/ebkus/ebkus_icons/edit_grp_button_inaktiv.gif"></td>
<td class="normaltext" align="left" bgcolor="#FFFFFF">%(gruppe_id__gn)s</td>
"""

fall_gruppen_ende = """
<td colspan="3" class="labeltext" align="left" width="100%">&nbsp;</td>
</table>
</td>
"""

bzpersgruppen_kopf= """
<td align="center" valign="top" width="50%" legend class="legendtext">
<fieldset><legend class="legendtext">Gruppenkarten der Bezugspersonen</legend>
<table border=0 cellspacing=1 width="90%">
<tr>
<td class="labeltext" align="left" width="15%">&nbsp;</td>
<td class="labeltext" align="left" width="10%">Gruppenr.:</td>
<td class="labeltext" align="left" width="75%">Name:</td>
</tr>
"""

bzpersgruppen_leer = """
<td align="center" valign="top" width="50%">
&nbsp;
</td>
"""

bzpersgruppen_t1 = """
<tr>
<td class="normaltext" align="left">
<a href="gruppenkarte?gruppeid=%(gruppe_id)s">
<img border="0" src="/ebkus/ebkus_icons/edit_grp_button.gif"></a></td>
<td class="normaltext" align="left" bgcolor="#FFFFFF">%(gruppe_id__gn)s</td>"""

bzpersgruppen_t2 = """
<td class="normaltext" align="left" bgcolor="#FFFFFF">%(vn)s %(na)s</td>
</tr>"""

bzpersgruppen_t1_keinaktfall = """
<tr>
<td class="normaltext" align="left"><img border="0" src="/ebkus/ebkus_icons/edit_grp_button_inaktiv.gif"</td>
<td class="normaltext" align="left" bgcolor="#FFFFFF">%(gruppe_id__gn)s</td>"""


bzpersgruppen_ende = """
<td colspan="3" class="labeltext" align="left" width="100%">&nbsp;</td>
</table>
</td>
</tr>
"""

tabelle_ende = """
</table>
</form>
</body>
</html>
"""
