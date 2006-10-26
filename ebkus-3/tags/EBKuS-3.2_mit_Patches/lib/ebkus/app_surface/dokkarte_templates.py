# coding: latin-1
dokkarte_start_t1 = """
</HEAD>
<body bgcolor="#CCCCCC" link="#CCCCCC" vlink="#CCCCCC" alink="#000000">
<table width="735" align="center">
 <tr>
   <td align="center">
   <table width="95%" align="center">
"""

menuedok_t = """
<tr>
  <td align="center" height="30"  class="legendtext"> <fieldset><legend>Steuerung</legend>
    <table border="0" cellpadding="1" width="50%%" height="30">
      <form>
      <tr valign="top">
        <td align="center" height="30">
          <input type="button" name="Schaltfl&auml;che" onClick="go_to_url('menu')" value="Hauptmen&uuml;" class="button">
        </td>
        <td align="center" height="30">
          <input type="button" name="Schaltfl&auml;che"
            onClick="go_to_url('menugruppe')" value="Gruppenmen&uuml;" class="button">
        </td>
      </tr>
      </form>
    </table>
    </fieldset> </td>
  <td align="center" height="30" class="legendtext"> <fieldset><legend>Akte</legend>
    <table border="0" cellpadding="1" height="30">
      <tr>
        <td align="center" height="30">
         <A HREF="vermneu?akid=%(akte_id)d&fallid=%(id)d"" onMouseOver="window.status='Neuen Vermerk erstellen';return true;"    onMouseOut="window.status='';return true;">
          <img border="0" src="/ebkus/ebkus_icons/new_text_button.gif" width="21" height="19" alt="Neuen Vermerk erstellen"></A> </td>
        <td align="center" height="30">
        <A HREF="updvermausw?akid=%(akte_id)d&fallid=%(id)d" onMouseOver="window.status='Vermerk zum Bearbeiten ausw&auml;hlen';return true;"    onMouseOut="window.status='';return true;">
          <img border="0" src="/ebkus/ebkus_icons/edit_text_button.gif" width="21" height="19" alt="Vermerk zum Bearbeiten ausw&auml;hlen.">
          </A> </td>
          <td align="center" height="30">
          <A HREF="rmdok?akid=%(akte_id)d&fallid=%(id)d" onMouseOver="window.status='Vermerk entfernen';return true;"    onMouseOut="window.status='';return true;">
         <img border="0" src="/ebkus/ebkus_icons/del_text_button.gif" width="21" height="19" alt="Vermerk entfernen.">
         </A>
         </td>
        <td align="center" height="30">
        <A HREF="upload?akid=%(akte_id)d&fallid=%(id)d" onMouseOver="window.status='Datei hochladen';return true;"    onMouseOut="window.status='';return true;">
           <img border="0" src="/ebkus/ebkus_icons/upload_button.gif" width="21" height="19" alt="Datei hochladen.">
          </A>
        </td>
         <td align="center" class="smalltext" height="30">
         <A HREF="klkarte?akid=%(akte_id)d&fallid=%(id)d" onMouseOver="window.status='Klientenkarte anzeigen';return true;"    onMouseOut="window.status='';return true;">
         <img border="0" src="/ebkus/ebkus_icons/klientenkarte_button.gif" alt="Klientenkarte anzeigen"></A> </td>
          <td align="center" class="smalltext" height="30"> <A HREF="vorblatt?akid=%(akte_id)d&fallid=%(id)d"
          target="_new" 
         onMouseOver="window.status='Aktenvorblatt der Akte anzeigen';return true;"                                               onMouseOut="window.status='';return true;">
         <img border="0" src="/ebkus/ebkus_icons/aktenvorblatt_button.gif" alt="Aktenvorblatt der Akte anzeigen"></A> </td>
          <td align="center" class="smalltext" height="30">
            <A HREF="dokkarte?akid=%(akte_id)d&fallid=%(id)d"
            onMouseOver="window.status='Dokumentenindex der Akte anzeigen';return true;"                                             onMouseOut="window.status='';return true;">
         <img border="0" src="/ebkus/ebkus_icons/dokumenten_index.gif" alt="Dokumentenindex der Akte anzeigen"></A> </td>
          <td align="center" class="smalltext" height="30">
          <A HREF="formabfr3"
          onMouseOver="window.status='Suchen in der Kartei nach Vorname / Nachname - Fallnr. oder Grupe';return true;"             onMouseOut="window.status='';return true;">
         <img border="0" src="/ebkus/ebkus_icons/suche_button.gif"
         alt="Suchen in der Kartei nach Vorname / Nachname - Fallnr. oder Gruppe"></A> </td>
      </tr>
    </table>
    </fieldset> </td>
</tr>
"""

menuedokzda_t = """
<tr>
  <td align="center" height="30" class="legendtext"><fieldset><legend>Steuerung</legend>
    <table border="0" cellpadding="1" width="50%%" height="30">
      <form>
      <tr valign="top">
        <td align="center" height="30">
          <input type="button" name="Schaltfl&auml;che" onClick="go_to_url('menu')" value="Hauptmen&uuml;" class="button">
        </td>
        <td align="center" height="30">
          <input type="button" name="Schaltfl&auml;che"
            onClick="go_to_url('menugruppe')" value="Gruppenmen&uuml;" class="button">
        </td>
      </tr>
      </form>
    </table>
    </fieldset> </td>
  <td align="center" height="30" class="legendtext"><fieldset><legend>Akte</legend>
    <table border="0" cellpadding="1" height="30">
      <tr>
        <td align="center" height="30">&nbsp;</td>
        <td align="center" height="30">&nbsp;</td>
          <td align="center" height="30">&nbsp;</td>
        <td align="center" class="smalltext" height="30">&nbsp;</td>
        <td align="center" height="30">&nbsp;</td>
        <td align="center" class="smalltext" height="30"> <A HREF="klkarte?akid=%(akte_id)d&fallid=%(id)d" onMouseOver="window.status='Klientenkarte anzeigen';return true;" onMouseOut="window.status='';return true;">
         <img src="/ebkus/ebkus_icons/klientenkarte_button.gif" alt="Klientenkarte anzeigen"></A> </td>
          <td align="center" class="smalltext" height="30"> <A HREF="vorblatt?akid=%(akte_id)d&fallid=%(id)d" onMouseOver="window.status='Aktenvorblatt der Akte anzeigen';return true;"                                               onMouseOut="window.status='';return true;">
         <img src="/ebkus/ebkus_icons/aktenvorblatt_button.gif" alt="Aktenvorblatt der Akte anzeigen"></A> </td>
          <td align="center" class="smalltext" height="30"> <A HREF="dokkarte?akid=%(akte_id)d&fallid=%(id)d"             onMouseOver="window.status='Dokumentenindex der Akte anzeigen';return true;"                                             onMouseOut="window.status='';return true;">
         <img src="/ebkus/ebkus_icons/dokumenten_index.gif" alt="Dokumentenindex der Akte anzeigen"></A> </td>
          <td align="center" class="smalltext" height="30"> <A HREF="formabfr3"           onMouseOver="window.status='Suchen in der Kartei nach Vorname / Nachname - Fallnr. oder Grupe';return true;"             onMouseOut="window.status='';return true;">
         <img src="/ebkus/ebkus_icons/suche_button.gif" alt="Suchen in der Kartei nach Vorname / Nachname - Fallnr. oder Gruppe"></A> </td>
      </tr>
    </table>
    </fieldset> </td>
</tr>"""


dokausgabe1_t = """
<tr>
<td class="normaltext" align="center" class="legendtext" colspan="2">
<fieldset><legend class="legendtext">%s</legend>
<table width="95%%">
<tr>
<td class="legendtext" align="center" valign="middle">"""

dokausgabe2_mit_edit_t = """
<table width="95%%">
  <tr>
    <td width="20"><A HREF="updverm?fallid=%(fall_id)d&dokid=%(id)d">
    <img border="0" src="/ebkus/ebkus_icons/edit_button.gif"></A></td>
    <td width="20"><A HREF="dokview?fallid=%(fall_id)d&dokid=%(id)d" target="_new">
    <img border="0" src="/ebkus/ebkus_icons/view_details.gif"></A></td>
    <td width="70" class="normaltext" bgcolor="#FFFFFF" align="left">%(vd)d.%(vm)d.%(vy)d</td>
    <td width="70%%" class="normaltext" bgcolor="#FFFFFF" align="left">%(art__name)s: %(betr)s</td>
    <td width="30%%" class="normaltext" bgcolor="#FFFFFF" align="right">%(mit_id__na)s</td>
  </tr>
</table>
"""

dokausgabe2_ohne_edit_t = """
<table width="95%%">
  <tr>
    <td width="20"><img border="0" src="/ebkus/ebkus_icons/edit_button_inaktiv.gif"></td>
    <td width="20"><A HREF="dokview?fallid=%(fall_id)d&dokid=%(id)d" target="_new">
    <img border="0" src="/ebkus/ebkus_icons/view_details.gif"></A></td>
    <td width="70" class="normaltext" bgcolor="#FFFFFF" align="left">%(vd)d.%(vm)d.%(vy)d</td>
    <td width="70%%" class="normaltext" bgcolor="#FFFFFF" align="left">%(art__name)s: %(betr)s</td>
    <td width="30%%" class="normaltext" bgcolor="#FFFFFF" align="right">%(mit_id__na)s</td>
  </tr>
</table>
"""

#dokausgabe2_t = """
#<dt> <A HREF="dokview?fallid=%(fall_id)d&dokid=%(id)d" target="_new">%(vd)d.%(vm)d.%(vy)d</A>:</dt>
#<dd><B>%(art__name)s:</B> %(betr)s (%(mit_id__na)s)</dd>
#"""

dokausgabe2b_t = """
<table width="95%%">
  <tr>
    <td width="20"><A HREF="dokview?fallid=%(fall_id)d&dokid=%(id)d" target="_new">
    <img border="0" src="/ebkus/ebkus_icons/view_details.gif"></A></td>
    <td width="70" class="normaltext" bgcolor="#FFFFFF" align="left">%(vd)d.%(vm)d.%(vy)d</td>
    <td width="70%%" class="normaltext" bgcolor="#FFFFFF" align="left">%(art__name)s: %(betr)s</td>
    <td width="30%%" class="normaltext" bgcolor="#FFFFFF" align="right">%(mit_id__na)s</td>
  </tr>
</table>
"""

dokausgabe3_t = """
</td>
</tr>
<tr>
<td colspan="4">
&nbsp;
</td>
</tr>
</table>
</fieldset>
</td>
</tr>
"""

dokausgabe4_t = """
<table width="95%%">
  <tr>
    <td align="left" width="33%%" class="legendtext">Beraternotizen:</td>
    <td class="normaltext" width="16%%" align="right">TXT - Format </td>
    <td class="normaltext" width="17%%" align="left"><a href="dokview2?fallid=%(id)d&art=bnotiz" target="_new"><img  border="0" src="/ebkus/ebkus_icons/new_text_button.gif" width="19" height="19"></a></td>
    <td class="normaltext" width="17%%" align="right">PDF - Format </td>
    <td class="normaltext" width="17%%" align="left"><a href="print_pdf?fallid=%(id)d&art=bnotiz" target="_new"><img  border="0" src="/ebkus/ebkus_icons/show_pdf_button.gif" width="19" height="19"></a></td>
  </tr>
</table>
"""

dokausgabe5_t = """
<table width="95%%">
  <tr>
    <td align="left" width="33%%" class="legendtext">Aktentexte:</td>
    <td class="normaltext" width="16%%" align="right">TXT - Format </td>
    <td class="normaltext" width="17%%" align="left"><a href="dokview2?fallid=%(id)d&art=anotiz" target="_new"><img  border="0" src="/ebkus/ebkus_icons/new_text_button.gif" width="19" height="19"></a></td>
    <td class="normaltext" width="17%%" align="right">PDF - Format </td>
    <td class="normaltext" width="17%%" align="left"><a href="print_pdf?fallid=%(id)d&art=anotiz" target="_new"><img  border="0" src="/ebkus/ebkus_icons/show_pdf_button.gif" width="19" height="19"></a></td>
  </tr>
</table>
"""

dokausgabe6_t = """
</td>
</tr>
<tr>
<td colspan="2">
&nbsp;
</td>
</tr>
</table>
</fieldset>
</td>
</tr>
"""
dokausgabe7a_t = """
<tr>
<td colspan="2" class="legendtext" align="center">
<fieldset><legend class="legendtext">%s</legend>
 <table width="95%%" cellpadding="0" cellspacing="0">
  <form action="suchetxt" method="post">
    <tr>
      <td align="center" class="normaltext" valign="middle">
        <input type="text" class="textboxlarge" width="15" maxlength="60" value="%s" name="expr">
      </td>
      <td align="center" valign="middle" colspan="2">
        <input class="button" type="submit" value="Suchen">
    </tr>
    <tr>
      <td colspan="2">&nbsp; </td>
    </tr>"""

dokausgabe7b_t = """ 
  </form>
</table>
</fieldset>
</td>
</tr>"""

dokkarte_ende_t = """
  </table>
  </td>
  </tr>
</table>
</body>
</html>"""
